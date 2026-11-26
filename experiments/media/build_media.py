#!/usr/bin/env python3
"""Build the bundled park photos for the offline chat.

Turns the operator's photo export into:

- ``mobile/assets/media/<item>.<n>.webp``: 640x800 (4:5) WebP crops,
- ``mobile/assets/data/knowledge/media.json``: items, credits and topic map,
- ``mobile/src/core/media/photos.generated.ts``: the ``require`` map Metro needs.

Species photos are curated by hand in ``SPECIES`` (chosen files, order, crop
focus) after looking at labelled montages of every folder. Place photos come
from ``experiments/media/places.json``, written by the landscape classifier.

Run with ``python3 -I`` because the source tree is untrusted data::

    python3 -I experiments/media/build_media.py --src <extracted root> \
        [--places experiments/media/places.json] --review-dir <dir>
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CATALOG = REPO / "mobile/assets/data/knowledge/catalog.json"
MEDIA_DIR = Path("mobile/assets/media")
MANIFEST = Path("mobile/assets/data/knowledge/media.json")
PHOTOS_TS = Path("mobile/src/core/media/photos.generated.ts")

SPECIES_DIR = "imagenes_especies_los_nevados"
SPECIES_CREDITS = "creditos_especies_los_nevados_filtrado.json"
PLACES_DIR = "imagenes_los_nevados"
PLACES_CREDITS = "creditos_los_nevados.json"

WIDTH, HEIGHT, WEBP_QUALITY = 640, 800, 75
MAX_PHOTOS = 3
MAX_TOPIC_ITEMS = 3
BUDGET_BYTES = 12 * 1024 * 1024
# places.json gives quality 1-3; the classifier's placeholder rows use 1, so
# 3 is read as the best. Change here if the classifier says otherwise.
PLACE_QUALITY_BEST_FIRST = True

GENERATED_WEBP = re.compile(r"^(species|place)\.[a-z0-9_]+\.\d+\.webp$")
ALLOWED_LICENSE = re.compile(r"^(CC0( 1\.0)?|CC BY(-SA)? \d\.\d|Public domain)$")
NO_AUTHOR = {"", "unknown", "unknown author", "anonymous", "no rights reserved"}
AUTHOR_MAX = 60

SPECIES_SECTIONS = {
    "fauna",
    "flora_ecosystems",
    "geography",
    "activities",
    "history_culture",
    "weather_volcano",
}
PLACE_SECTIONS = {
    "geography",
    "activities",
    "weather_volcano",
    "flora_ecosystems",
    "history_culture",
}

# (fx, fy) crop centre in 0..1, optionally a zoom < 1 that crops tighter
# (used to cut plate letters off scanned figures).
Focus = tuple[float, float] | tuple[float, float, float]


@dataclass(frozen=True)
class Species:
    """Curated item for one source folder.

    ``common`` overrides the credits' nombre_comun (None keeps it); it is set
    when the park catalog names the species differently or the credits name
    is wrong. ``aliases`` are accent-free names matched in topic text, and
    ``variants`` are alternative spellings of the scientific name.
    """

    photos: tuple[tuple[str, Focus | None], ...]
    common: str | None = None
    aliases: tuple[str, ...] = ()
    variants: tuple[str, ...] = ()


@dataclass(frozen=True)
class Place:
    name: str
    aliases: tuple[str, ...]
    # Aliases tried only against the topic id (e.g. "tolima" names the nevado
    # in ids, but the department in prose).
    id_aliases: tuple[str, ...] = ()
    # The volcano's names are everywhere; only topics about it (id or label)
    # get its photos.
    label_only: bool = False


# Curated after reviewing labelled montages of every folder. Photos not listed
# are dropped; notable reasons are in DROP_NOTES.
SPECIES: dict[str, Species] = {
    "Diplostephium": Species(
        common="Romero",  # catalog: "romeros del género Diplostephium"
        aliases=("romero",),
        photos=(
            ("Diplostephium_azureum_(3)_en_el_distrito_de_Cajacay.jpg", None),
            ("Diplostephium_azureum_(2)_en_el_distrito_de_Cajacay.jpg", (0.5, 0.6)),
            (
                "Cotopaxi_National_Park_Laguna_de_Limpiopungo_Diplostephium_lavandulaefolium.jpg",
                None,
            ),
        ),
    ),
    "Drimys_granadensis": Species(
        aliases=("canelo de paramo",),
        photos=(
            ("Drimys_granadensis_1.jpg", (0.45, 0.5)),
            ("Flowers_of_Drimys_granadensis.jpg", (0.6, 0.6, 0.85)),
            ("Stem_shoots_and_leaves_of_Drimys_granadensis.jpg", (0.6, 0.6, 0.85)),
        ),
    ),
    "Espeletia": Species(
        # Genus item: "frailejón" belongs to Espeletia hartwegiana, so this
        # one only maps on the bare genus name.
        photos=(
            ("Donde_nace_el_agua.jpg", (0.68, 0.5)),
            ("Cobertura_de_frailejones_en_los_pajonales_del_Parque_Los_Nevados.jpg", None),
            ("Campo_de_frailejones_en_el_páramo_de_Murillo.jpg", None),
        ),
    ),
    "Espeletia_hartwegiana": Species(
        aliases=("frailejon",),
        photos=(
            ("Espeletia_hartwegiana_o.jpg", (0.55, 0.5)),
            ("Espeletia_hartwegiana._(9439106526).jpg", None),
            ("Espeletia_hartwegiana,_known_as_Frailejon._(9436325301).jpg", None),
        ),
    ),
    "Gynoxys": Species(
        photos=(
            ("Gynoxys_calyculisolvens_470041884.jpg", None),
            ("Gynoxys_calyculisolvens_438407305.jpg", (0.6, 0.5)),
            ("Gynoxys_nitida_545442877.jpg", None),
        ),
    ),
    "Lupinus_alopecuroides": Species(
        aliases=("lupino andino",),
        photos=(
            ("Lupinus_alopecuroides.jpg", None),
            ("Lupinus_alopecuroides_2_-_Páramo_de_Ocetá.jpg", None),
            ("Lupinus_alopecuroides_-_Páramo_de_Ocetá.jpg", None),
        ),
    ),
    "Polylepis_sericea": Species(
        common="Siete cueros de páramo",  # catalog name
        aliases=("siete cueros",),
        photos=(
            ("Sierra_Nevada,_Mérida_(2003)_06.jpg", (0.55, 0.5)),
            ("Sierra_Nevada,_Mérida_(2003)_07.jpg", None),
            ("Detalle_de_hojas_de_quenual_(Polylepis_sericea).jpg", None),
        ),
    ),
    "Vallea_stipularis": Species(
        photos=(
            ("Vallea_stipularis_(14402034659).jpg", None),
            (
                "Corqush_(Vallea_stipularis)_in_Santa_Cruz_ravine,_Cordillera_Blanca,_flowers.jpg",
                (0.45, 0.5),
            ),
            (
                "Corqush_(Vallea_stipularis)_in_Santa_Cruz_ravine,_Cordillera_Blanca,_leaves.jpg",
                None,
            ),
        ),
    ),
    "Bolborhynchus_ferrugineifrons": Species(
        aliases=("periquito de los nevados",),
        photos=(
            ("Rufous-fronted_Parakeet_(Bolborhynchus_ferrugineifrons).jpg", (0.45, 0.55)),
            (
                "Boloborhynchus_ferrugineifrons_Periquito_frentirrufo_Rufous-fronted_Parakeet_(14360849473).jpg",
                (0.45, 0.5),
            ),
        ),
    ),
    "Ensifera_ensifera": Species(
        common="Colibrí piquiespada",  # catalog name
        aliases=("colibri piquiespada", "colibri picoespada"),
        photos=(
            ("Sword-billed_Hummingbird_RWD2.jpg", (0.5, 0.5)),
            (
                "Sword-billed_hummingbird_(male)_at_Guango_Lodge,_Ecuador_(21310837273).jpg",
                (0.6, 0.5),
            ),
        ),
    ),
    "Grallaria_rufula": Species(
        common="Tororoi rufo",  # credits say "Torrero rufo", a misspelling
        aliases=("tororoi rufo",),
        photos=(
            ("Grallaria_rufula_Tororoi_flautista_Rufous_Antpitta_(8192420350).jpg", None),
            ("Grallaria_rufula_Tororoi_flautista_Rufous_Antpitta_(8192420664).jpg", None),
            ("Grallaria_rufula_saltuensis_(15014984523).jpg", (0.6, 0.5)),
        ),
    ),
    "Hapalopsittaca_amazonina": Species(
        # Credits say "Loro de indigo", which is H. fuertesi's English name.
        common="Cotorra montañera",
        aliases=("cotorra montanera",),
        variants=("Haplopsittaca amazonina",),
        photos=(
            (
                "Haplopsittaca_amazonina_Cotorra_montañera_Rusty-faced_Parrot_(8721965346)_(cropped).jpg",
                (0.45, 0.5),
            ),
            ("Haplopsittaca_amazonina_Cotorra_montañera_Rusty-faced_Parrot_(8720843951).jpg", None),
        ),
    ),
    "Hapalopsittaca_fuertesi": Species(
        # Credits say "Loro orejiamarillo", which the catalog uses for
        # Ognorhynchus icterotis. Never alias that name here.
        common="Cotorra de Fuertes",
        aliases=("cotorra de fuertes",),
        photos=(("Hapalopsittaca_fuertesi_29051448.jpg", (0.5, 0.45)),),
    ),
    "Momotus_aequatorialis": Species(
        aliases=("barranquero andino",),
        photos=(
            ("Andean_motmot_(Momotus_aequatorialis_aequatorialis)_Las_Tangaras.jpg", None),
            ("EZy_Watermark_12-02-2025_02-09-17-4590p.m.jpg", None),
        ),
    ),
    "Ochthoeca_fumicolor": Species(
        common="Pitajo ahumado",  # credits say "Petirrojo de páramo"
        aliases=("pitajo ahumado",),
        photos=(
            ("Ochthoeca_fumicolor_(Pitajo_ahumado)_(15321653930).jpg", None),
            ("Ochthoeca_fumicolor_Pitajo_ahumado_Brown-backed_Chat-Tyrant_(6867098037).jpg", None),
            ("Ochtheca_fumicolor_(Pitajo_ahumado)_(24792922056).jpg", None),
        ),
    ),
    "Oreotrochilus_chimborazo": Species(
        common="Colibrí del Chimborazo",  # credits say "Colibrí de chimbo"
        photos=(
            ("Oreotrochilus_chimborazo_11461602.jpg", None),
            ("Ecuadorian_Hillstar_(cropped).jpg", (0.3, 0.5)),
            ("Oreotrochilus_chimborazo_141044751.jpg", (0.66, 0.45)),
        ),
    ),
    "Oxypogon_stuebelii": Species(
        aliases=("chivito de paramo",),
        variants=("Oxypogon stubelii",),
        photos=(
            ("Oxypogon_stuebelii_-_Buffy_Helmetcrest_-_Colibrí_Chivito_del_Ruiz.jpg", None),
            (
                "Oxypogon_stubelii_Barbudito_paramuno_Buffy_Helmetcrest_(male)_(6865793317).jpg",
                None,
            ),
            ("Buffy_Helmetcrest_-_Manizales,_Colombia.jpg", (0.5, 0.5)),
        ),
    ),
    "Oxyura_jamaicensis": Species(
        # The catalog's Andean duck topic names both O. ferruginea and
        # O. jamaicensis, so the binomial already maps it. Only the female is
        # kept: the white-cheeked males are the North American ruddy duck,
        # which the Andean bird does not look like.
        aliases=("pato andino", "pato turrio"),
        photos=(
            (
                "065_-_RUDDY_DUCK_(11-27-07)_fem,_oso_flaco,_sloco,_ca_oso_(1)_(8718083235).jpg",
                (0.42, 0.55),
            ),
        ),
    ),
    "Vultur_gryphus": Species(
        aliases=("condor andino", "condor de los andes"),
        photos=(
            ("Andean_condor_at_the_Hoenderdaell_animal_park_in_Anna_Paulowna.jpg", (0.52, 0.5)),
            ("Andean_Condor_soaring.jpg", (0.66, 0.45)),
            ("204_-_Canyon_de_Colca_-_Condor_des_Andes_-_Juin_2010.JPG", (0.42, 0.6)),
        ),
    ),
    "Dasypus": Species(
        aliases=("armadillo",),
        photos=(
            ("9_Banded_armadillo_caught_in_the_act_of_digging_a_hole.jpg", (0.55, 0.45)),
            ("Armadillo2.jpg", (0.6, 0.5)),
        ),
    ),
    "Didelphis_albiventris": Species(
        aliases=("fara", "zarigueya"),
        photos=(
            ("Didelphis_albiventris_(Lund,_1840)_(3452473141).jpg", (0.4, 0.5)),
            ("Didelphis_albiventris_(Lund,_1840)_(3452478085).jpg", (0.45, 0.5)),
        ),
    ),
    "Leopardus_tigrinus": Species(
        aliases=("tigrillo",),
        photos=(
            ("Parc_des_felins_Felin_20.jpg", None),
            ("Parc_des_Félins_oncille_11.jpg", (0.4, 0.5)),
        ),
    ),
    "Puma_concolor": Species(
        aliases=("puma", "leon de montana"),
        photos=(
            ("DSC_0107_-_Flickr_-_stickywikit.jpg", None),
            ("Mountain_Lion_in_Glacier_National_Park.jpg", (0.55, 0.5)),
            ("Mountain_Lion_(C).jpg", (0.35, 0.5)),
        ),
    ),
    "Tapirus_pinchaque": Species(
        aliases=("danta",),
        photos=(
            ("Mountain_tapir_(2315236141).jpg", (0.6, 0.5)),
            ("Mountain_tapir_(2316045432).jpg", (0.55, 0.5)),
            ("Mountain_Tapir.jpg", (0.72, 0.5)),
        ),
    ),
    "Tremarctos_ornatus": Species(
        aliases=("oso de anteojos", "oso andino"),
        photos=(
            ("El_gran_oso_de_anteojos.jpg", None),
            (
                "2018-09-01_AT_Wien_13_Hietzing,_Tiergarten_Schönbrunn,_Tremarctos_ornatus_(50790951717).jpg",
                None,
            ),
            ("Brillenbär_im_verschneiten_Zoo_3.jpg", (0.45, 0.5)),
        ),
    ),
    "Atelopus": Species(
        aliases=("sapo arlequin",),
        photos=(
            ("Atelopus_varius_-_52676882126.jpg", None),
            ("Atelopus_certus_dorsal.jpg", None),
            ("PGF_-_22-2.jpg", (0.55, 0.5)),
        ),
    ),
    "Bombus": Species(
        common="Abejorros",  # credits say "Abejas"; Bombus are bumblebees
        aliases=("abejorro",),
        photos=(
            ("20180708_Bombus_04.jpg", (0.66, 0.5)),
            ("20180708_Bombus_03.jpg", (0.66, 0.45)),
            (
                "061_Wild_Bumblebee_in_flight_pollinating_with_Crocus_Parc_naturel_régional_Jura_vaudois_Photo_by_Giles_Laurent.jpg",
                (0.42, 0.45),
            ),
        ),
    ),
    "Colias": Species(
        # "mariposas" also names the monarchs, so no common-name alias.
        photos=(
            ("Colias_croceus_-_Clouded_yellow_01.jpg", (0.4, 0.5)),
            (
                "Colias_Croceus_Lepidoptera_butterfly_clouded_yellow_Schmetterling_Wander-Gelbling_MD284.jpg",
                None,
            ),
            ("Colias_croceus_(Dordogne).jpg", (0.55, 0.5)),
        ),
    ),
    "Danaus": Species(
        aliases=("mariposa monarca", "monarca"),
        photos=(
            ("Monarch_butterflies_on_pine_needles.jpg", None),
            ("Danaus_plexippus_MHNT.jpg", None),
            ("Danaus_plexippus_(48483657977).jpg", None),
        ),
    ),
    "Pristimantis": Species(
        aliases=("rana de lluvia",),
        photos=(
            ("Pristimantis_dorado.jpg", (0.6, 0.5)),
            ("Pristimantis_diadematus.jpg", (0.6, 0.5)),
            ("Pristimantis_cruentus_studio.jpg", (0.55, 0.5)),
        ),
    ),
}

# Folders deliberately left out, with the reason shown in the review sheet.
SKIPPED_FOLDERS: dict[str, str] = {
    "Espeletiopsis": (
        "every photo is described as Espeletia; 4 are byte-identical copies of the "
        "Espeletia folder (kept there), none is verifiably Espeletiopsis"
    ),
    "Mazama_rufina": (
        "no usable photo: Dasyprocta_fuliginosa.jpg is an agouti, the two iNaturalist "
        "CC0 rows have no identifiable author"
    ),
    "Ameiva": "empty folder",
    "Pudu_mephistophiles": "only 19th-century illustrations, no photo (operator: drop it)",
}

DROP_NOTES: dict[str, str] = {
    "Drimys_granadensis/Psittacanthus_schiedeanus_1.jpg": "mistletoe Psittacanthus, not Drimys",
    "Dasypus/9-banded-armadillo.jpg": "license 'Attribution' is not CC/PD",
    "Dasypus/A_is_for_Armadillo03.png": "text overlay 'Aa' on the photo",
    "Pudu_mephistophiles/Pudella_mephistophiles.jpg": "author unknown",
    "Leopardus_tigrinus/Leopardus_tigrinus_(Felis_tigrina)_-_Museo_Civico_di_Storia_Naturale_Giacomo_Doria_-_Genoa,_Italy_-_DSC02680.JPG": "stuffed museum specimen",
    "Tapirus_pinchaque/Mountain_tapir_(1333743054).jpg": "animal hidden behind fence; caption says T. terrestris",
    "Hapalopsittaca_fuertesi/Hapalopsittaca_fuertesi_233310815.jpg": "bird too small to see",
    "Ochthoeca_fumicolor/Brown-backed_Chat-Tyrant_-_Colombia_S4E1525.jpg": "plumage does not match the other photos",
    "Oxyura_jamaicensis/065_-_RUDDY_DUCK_(3-26-13)_mustang_island,_nueces_co,_tx_(8719200030).jpg": "North American male ruddy duck",
    "Oxyura_jamaicensis/20150713_st_hilaire_erismatureRousse_2936_b.jpg": "captive North American male ruddy duck",
    "Espeletia_hartwegiana/Espeletia_hartwegiana._(9439106526)_(2).jpg": "duplicate of (9439106526)",
    "Hapalopsittaca_amazonina/Haplopsittaca_amazonina_Cotorra_montañera_Rusty-faced_Parrot_(8721965346).jpg": "uncropped duplicate",
    "Polylepis_sericea/Sendero_con_río_y_árboles_en_Aquilpo_(edited).jpg": "edited duplicate",
    "Vallea_stipularis/Corqush_(Vallea_stipularis)_in_Santa_Cruz_ravine,_Cordillera_Blanca,_flowers_2.jpg": "near duplicate of flowers.jpg",
}

PLACES: dict[str, Place] = {
    "laguna_otun": Place("Laguna del Otún", ("otun",)),
    "nevado_santa_isabel": Place("Nevado Santa Isabel", ("santa isabel", "poleka kasue")),
    "nevado_ruiz": Place("Nevado del Ruiz", ("ruiz", "kumanday", "cumanday"), label_only=True),
    "crater_arenas": Place("Cráter Arenas", ("arenas",)),
    "nevado_tolima": Place("Nevado del Tolima", ("nevado del tolima",), id_aliases=("tolima",)),
    "laguna_verde": Place("Laguna Verde", ("laguna verde",)),
    "valle_tumbas": Place("Valle de las Tumbas", ("valle de las tumbas", "tumbas")),
    "termales": Place("Termales", ("termales",)),
    "frailejonal": Place("Frailejonal del páramo", ("frailejon", "frailejonal")),
    "glaciar": Place("Glaciar", ("glaciar", "deshielo")),
}
# Optional crop focus for landscape photos, keyed by basename.
PLACE_FOCUS: dict[str, Focus] = {}
# Classified landscape photos left out after viewing the final crops.
PLACE_SKIP: dict[str, str] = {
    "El Ruiz 20260530 100953.jpg": "portrait crop is almost all fog",
    "Parque Nacional Natural Los Nevados y Nevado del Ruiz (16986).jpg": "near duplicate of (47118)",
    "Termas 20260529 090536.jpg": "tilted pool shot",
}


# ---------------------------------------------------------------- text utils


def fold(text: str) -> str:
    """Lowercase and strip accents; keeps length per character for ASCII-only output."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()


def norm_key(value: str) -> str:
    """Filename comparison key (same rule as the export's filter_creditos.py)."""
    return re.sub(r"[^a-z0-9]+", "_", fold(value)).strip("_")


def snake(value: str) -> str:
    return norm_key(value)


def plain_text(raw: str | None) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def clean_author(raw: str | None) -> str:
    """One short author name from the Commons HTML field; empty when unknown.

    The chat prints it in a small pill on the photo, so affiliations, places,
    wiki suffixes and co-authors are dropped: the first person or handle stays.
    """
    text = plain_text(raw)
    text = re.sub(r"^(iNaturalist user|User):\s*", "", text, flags=re.I)
    # Commons' placeholder names the uploader it assumed: "No machine-readable author
    # provided. Name~commonswiki assumed (based on copyright claims)."
    text = re.sub(
        r"^No machine-readable author provided\.\s*(.+?)\s+assumed\b.*$", r"\1", text, flags=re.I
    )
    text = re.sub(r"^Original:\s*(.+?)\s*Derivative work:.*$", r"\1", text)
    text = re.sub(r",?\s+as an employee of .*$", "", text, flags=re.I)
    text = re.sub(r"(https?://|www\.)\S+", "", text)
    text = re.sub(r"\s*\([^)]*\)", "", text)  # "( S23678 )", "(1836–1929)", "(talk)", "(WT-en)"
    text = re.sub(r"\bown work\b", "", text, flags=re.I)
    text = re.sub(r"~\w*wiki\b", "", text)  # "Name~commonswiki"
    text = re.sub(r"\s+at\s+.*\bwiki\w*\s*$", "", text, flags=re.I)  # "Name at English Wikivoyage"
    text = re.sub(r"\s+from\s+[^;]+$", "", text)  # Flickr "Name from City, Country"
    # Co-authors and trailing places ("Name, Bahia, Brazil"): the first name only.
    text = re.split(r"\s*(?:[,;&]|\s+and\s+)\s*", text.strip(" ,;&"))[0]
    text = re.sub(r"\s+", " ", text).strip(" ,;.")
    if text.isupper() and " " in text:  # "ALAN SCHMIERER"; one-word handles keep their case
        text = text.title()
    if re.fullmatch(r"(unknown author\s*)+", text, flags=re.I):
        text = ""
    if fold(text) in NO_AUTHOR:
        return ""
    if len(text) > AUTHOR_MAX:
        cut = text[: AUTHOR_MAX - 1].rsplit(" ", 1)[0].rstrip(" ,;")
        text = cut + "…"
    return text


def license_ok(license_label: str | None, author: str) -> bool:
    """CC or public domain with an identifiable author."""
    return bool(author) and bool(ALLOWED_LICENSE.match((license_label or "").strip()))


# ------------------------------------------------------------------- credits


def credit_names(row: dict) -> list[str]:
    names = []
    title = (row.get("archivo") or row.get("titulo") or "").strip()
    if title[:5].lower() == "file:":
        title = title[5:]
    if title:
        names.append(title.strip())
    url = (row.get("url") or "").strip()
    if url:
        names.append(urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name))
    return names


def index_credits(rows: list[dict]) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for row in rows:
        for name in credit_names(row):
            index.setdefault(norm_key(name), []).append(row)
    return index


@dataclass
class Photo:
    source: Path
    focus: Focus | None
    author: str
    license: str
    file: str = ""


@dataclass
class Item:
    id: str
    kind: str
    common: str
    scientific: str | None
    photos: list[Photo]
    aliases: tuple[str, ...] = ()
    variants: tuple[str, ...] = ()
    place: Place | None = None
    notes: list[str] = field(default_factory=list)


def resolve_credit(
    index: dict[str, list[dict]], filename: str, scope: str | None = None
) -> dict | None:
    rows = index.get(norm_key(filename), [])
    if scope is not None:
        rows = [
            r
            for r in rows
            if norm_key((r.get("nombre_cientifico") or "").replace(" ", "_")) == norm_key(scope)
        ]
    return rows[0] if rows else None


def make_photo(source: Path, focus: Focus | None, row: dict | None, log: list[str]) -> Photo | None:
    if row is None:
        log.append(f"drop {source.name}: no credit row")
        return None
    author = clean_author(row.get("autor"))
    lic = (row.get("licencia") or "").strip()
    if not license_ok(lic, author):
        log.append(f"drop {source.name}: license {lic!r} / author {author!r}")
        return None
    return Photo(source=source, focus=focus, author=author, license=lic)


# ------------------------------------------------------------------- stages


def collect_species(src: Path, curation: dict[str, Species], log: list[str]) -> list[Item]:
    root = src / SPECIES_DIR
    rows = json.loads((src / SPECIES_CREDITS).read_text(encoding="utf-8"))
    index = index_credits(rows)
    folders = sorted(p for p in root.glob("*/*") if p.is_dir())
    unknown = [f.name for f in folders if f.name not in curation and f.name not in SKIPPED_FOLDERS]
    if unknown:
        raise SystemExit(f"error: folders without curation entry: {unknown}")

    items: list[Item] = []
    seen_hash: dict[str, str] = {}
    for folder in folders:
        spec = curation.get(folder.name)
        if spec is None:
            log.append(f"skip folder {folder.name}: {SKIPPED_FOLDERS[folder.name]}")
            continue
        photos: list[Photo] = []
        common_credit = None
        for name, focus in spec.photos:
            path = folder / name
            if not path.is_file():
                raise SystemExit(f"error: curated photo missing: {folder.name}/{name}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in seen_hash:
                raise SystemExit(f"error: {folder.name}/{name} duplicates {seen_hash[digest]}")
            seen_hash[digest] = f"{folder.name}/{name}"
            row = resolve_credit(index, name, scope=folder.name)
            if row and common_credit is None:
                common_credit = (row.get("nombre_comun") or "").strip()
            photo = make_photo(path, focus, row, log)
            if photo:
                photos.append(photo)
        photos = photos[:MAX_PHOTOS]
        if not photos:
            log.append(f"skip folder {folder.name}: no photo survived the filters")
            continue
        common = spec.common or common_credit or folder.name.replace("_", " ")
        items.append(
            Item(
                id="species." + snake(folder.name),
                kind="species",
                common=common[:1].upper() + common[1:],
                scientific=folder.name.replace("_", " "),
                photos=photos,
                aliases=spec.aliases,
                variants=spec.variants,
            )
        )
    return items


def collect_places(src: Path, places_file: Path | None, log: list[str]) -> list[Item]:
    if places_file is None or not places_file.is_file():
        log.append("places: no places.json, place items skipped")
        return []
    rows = json.loads(places_file.read_text(encoding="utf-8"))
    credits = index_credits(json.loads((src / PLACES_CREDITS).read_text(encoding="utf-8")))
    by_place: dict[str, list[dict]] = {}
    for row in rows:
        place = row.get("place")
        if place is None:
            continue
        if place not in PLACES:
            raise SystemExit(f"error: places.json uses unknown place id {place!r}")
        by_place.setdefault(place, []).append(row)

    items: list[Item] = []
    for place_id in sorted(by_place):
        ranked = sorted(
            by_place[place_id],
            key=lambda r: (
                -int(r.get("quality", 0)) if PLACE_QUALITY_BEST_FIRST else int(r.get("quality", 0)),
                r["file"],
            ),
        )
        photos: list[Photo] = []
        for row in ranked:
            if len(photos) == MAX_PHOTOS:
                break
            path = src / PLACES_DIR / Path(row["file"]).name
            if path.name in PLACE_SKIP:
                log.append(f"skip place photo {path.name}: {PLACE_SKIP[path.name]}")
                continue
            if not path.is_file():
                log.append(f"drop place photo {row['file']}: file missing")
                continue
            photo = make_photo(
                path, PLACE_FOCUS.get(path.name), resolve_credit(credits, path.name), log
            )
            if photo:
                photos.append(photo)
        if photos:
            place = PLACES[place_id]
            items.append(
                Item(
                    id="place." + place_id,
                    kind="place",
                    common=place.name,
                    scientific=None,
                    photos=photos,
                    place=place,
                )
            )
        else:
            log.append(f"place {place_id}: no photo survived the filters")
    return items


# -------------------------------------------------------------- topic mapping


def alias_pattern(alias: str) -> re.Pattern[str]:
    """Whole-word, accent-folded phrase; every word may take a plural s/es."""
    words = [re.escape(w) + "(?:es|s)?" for w in fold(alias).split()]
    return re.compile(r"(?<![a-z0-9])" + r"\s+".join(words) + r"(?![a-z0-9])")


def first_match(patterns: list[re.Pattern[str]], text: str) -> int | None:
    hits = [m.start() for p in patterns for m in [p.search(text)] if m]
    return min(hits) if hits else None


def topic_hits(entry: dict, items: list[Item], any_section: bool = False) -> dict[str, int]:
    """item id -> position of its first mention in the topic (accent-folded label | short)."""
    if entry.get("kind") == "emergency" and not any_section:
        return {}
    section = entry.get("section")
    label, short = fold(entry.get("label") or ""), fold(entry.get("short") or "")
    text = label + " | " + short
    hits: dict[str, int] = {}

    if any_section or section in SPECIES_SECTIONS:
        binomials = [
            i for i in items if i.kind == "species" and i.scientific and " " in i.scientific
        ]
        genera = [
            i for i in items if i.kind == "species" and i.scientific and " " not in i.scientific
        ]
        # Masking binomials keeps "Espeletia hartwegiana" from also matching
        # the Espeletia genus item.
        masked = text
        for item in binomials:
            for name in (item.scientific, *item.variants):
                masked = alias_pattern(name).sub(lambda m: " " * len(m.group()), masked)
        for item in binomials:
            names = (item.scientific, *item.variants, *item.aliases)
            pos = first_match([alias_pattern(n) for n in names], text)
            if pos is not None:
                hits[item.id] = pos
        for item in genera:
            names = (item.scientific, *item.variants, *item.aliases)
            pos = first_match([alias_pattern(n) for n in names], masked)
            if pos is not None:
                hits[item.id] = pos

    # Municipality topics name the town of Santa Isabel and the department of
    # Tolima, not the peaks.
    if (any_section or section in PLACE_SECTIONS) and "municipio" not in label:
        topic_id = fold(entry["id"].split(".", 1)[-1].replace("_", " "))
        first_sentence = re.split(r"(?<=[.!?])\s", short, maxsplit=1)[0]
        for item in items:
            if item.place is None:
                continue
            patterns = [alias_pattern(a) for a in item.place.aliases]
            scope = label if item.place.label_only else label + " | " + first_sentence
            pos = first_match(patterns, scope)
            if (
                pos is None
                and first_match(
                    patterns + [alias_pattern(a) for a in item.place.id_aliases], topic_id
                )
                is not None
            ):
                pos = 0
            if pos is not None:
                hits[item.id] = pos
    return hits


def map_topics(catalog: list[dict], items: list[Item]) -> dict[str, list[str]]:
    """topic id -> up to MAX_TOPIC_ITEMS item ids, ordered by first mention."""
    topics: dict[str, list[str]] = {}
    for entry in catalog:
        hits = topic_hits(entry, items)
        if hits:
            # On a shared alias ("frailejón") the species comes before the place.
            ordered = sorted(hits, key=lambda i: (hits[i], not i.startswith("species."), i))
            topics[entry["id"]] = ordered[:MAX_TOPIC_ITEMS]
    return dict(sorted(topics.items()))


def unmapped_mentions(
    catalog: list[dict], items: list[Item], topics: dict[str, list[str]]
) -> list[tuple[str, str]]:
    """(topic, species item) pairs that match in any section but are not in the map (section filter or cap)."""
    species = [i for i in items if i.kind == "species"]
    out = []
    for entry in catalog:
        for item_id in topic_hits(entry, species, any_section=True):
            if item_id not in topics.get(entry["id"], []):
                out.append((entry["id"], item_id))
    return out


# --------------------------------------------------------------------- images


def render(photo: Photo, dest: Path) -> None:
    from PIL import Image, ImageOps

    with Image.open(photo.source) as opened:
        opened.seek(0)
        image = ImageOps.exif_transpose(opened)
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGBA")
            flat = Image.new("RGB", image.size, (255, 255, 255))
            flat.paste(image, mask=image.getchannel("A"))
            image = flat
        else:
            image = image.convert("RGB")
    fx, fy, zoom = (*(photo.focus or (0.5, 0.5)), 1.0)[:3]
    w, h = image.size
    target = WIDTH / HEIGHT
    if w / h > target:
        cw, ch = round(h * target * zoom), round(h * zoom)
    else:
        cw, ch = round(w * zoom), round(w / target * zoom)
    left = min(max(round(fx * w - cw / 2), 0), w - cw)
    top = min(max(round(fy * h - ch / 2), 0), h - ch)
    image = image.crop((left, top, left + cw, top + ch)).resize(
        (WIDTH, HEIGHT), Image.Resampling.LANCZOS
    )
    image.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)


# -------------------------------------------------------------------- outputs


def manifest(items: list[Item], topics: dict[str, list[str]]) -> dict:
    return {
        "version": 1,
        "items": {
            item.id: {
                "kind": item.kind,
                "common": item.common,
                "scientific": item.scientific,
                "photos": [
                    {"file": p.file, "author": p.author, "license": p.license} for p in item.photos
                ],
            }
            for item in sorted(items, key=lambda i: i.id)
        },
        "topics": topics,
    }


def photos_ts(files: list[str]) -> str:
    lines = [
        "// Generated by experiments/media/build_media.py. Do not edit.",
        "export const PHOTOS: Record<string, number> = {",
        *[f"  '{name}': require('../../../assets/media/{name}')," for name in sorted(files)],
        "};",
        "",
    ]
    return "\n".join(lines)


def write_outputs(items: list[Item], topics: dict[str, list[str]], out_root: Path) -> list[Path]:
    media_dir = out_root / MEDIA_DIR
    media_dir.mkdir(parents=True, exist_ok=True)
    for old in media_dir.iterdir():
        if GENERATED_WEBP.match(old.name):
            old.unlink()
    written: list[Path] = []
    for item in items:
        for n, photo in enumerate(item.photos, start=1):
            photo.file = f"{item.id}.{n}.webp"
            render(photo, media_dir / photo.file)
            written.append(media_dir / photo.file)
    manifest_path = out_root / MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest(items, topics), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # The require map goes last: a require() of a missing webp breaks the bundle.
    ts_path = out_root / PHOTOS_TS
    ts_path.parent.mkdir(parents=True, exist_ok=True)
    ts_path.write_text(photos_ts([p.name for p in written]), encoding="utf-8")
    return written


def check_invariants(out_root: Path) -> int:
    data = json.loads((out_root / MANIFEST).read_text(encoding="utf-8"))
    media_dir = out_root / MEDIA_DIR
    listed = {p["file"] for item in data["items"].values() for p in item["photos"]}
    on_disk = {p.name for p in media_dir.iterdir() if GENERATED_WEBP.match(p.name)}
    ts = (out_root / PHOTOS_TS).read_text(encoding="utf-8")
    in_ts = set(re.findall(r"^  '([^']+)': require", ts, flags=re.M))
    problems = []
    if listed != on_disk:
        problems.append(f"manifest vs disk differ: {sorted(listed ^ on_disk)}")
    if listed != in_ts:
        problems.append(f"manifest vs PHOTOS differ: {sorted(listed ^ in_ts)}")
    for item_id, item in data["items"].items():
        if not 1 <= len(item["photos"]) <= MAX_PHOTOS:
            problems.append(f"{item_id}: {len(item['photos'])} photos")
        for p in item["photos"]:
            if not p["author"] or not p["license"]:
                problems.append(f"{p['file']}: missing credit")
    for topic, ids in data["topics"].items():
        if len(ids) > MAX_TOPIC_ITEMS or any(i not in data["items"] for i in ids):
            problems.append(f"topic {topic}: bad ids {ids}")
    total = sum((media_dir / name).stat().st_size for name in on_disk)
    if total > BUDGET_BYTES:
        problems.append(f"media total {total} bytes exceeds {BUDGET_BYTES}")
    if problems:
        raise SystemExit("error: invariant check failed:\n  " + "\n  ".join(problems))
    return total


# ---------------------------------------------------------------- review sheet


def write_review(
    review_dir: Path,
    items: list[Item],
    topics: dict[str, list[str]],
    catalog: list[dict],
    out_root: Path,
    total: int,
    log: list[str],
) -> None:
    img_dir = review_dir / "img"
    if img_dir.exists():
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True)
    by_item: dict[str, list[str]] = {}
    for topic, ids in topics.items():
        for item_id in ids:
            by_item.setdefault(item_id, []).append(topic)
    species = [i for i in items if i.kind == "species"]
    no_topic = [i.id for i in species if i.id not in by_item]
    unmapped = unmapped_mentions(catalog, items, topics)
    photo_count = sum(len(i.photos) for i in items)

    esc = html.escape
    cards = []
    for item in sorted(items, key=lambda i: i.id):
        caption = item.common + (f" ({item.scientific})" if item.scientific else "")
        figs = []
        for p in item.photos:
            shutil.copyfile(out_root / MEDIA_DIR / p.file, img_dir / p.file)
            figs.append(
                f'<figure><img src="img/{esc(p.file)}" width="160" height="200" alt="">'
                f"<figcaption>{esc(p.author)} · {esc(p.license)}<br><small>{esc(p.source.name)}</small></figcaption></figure>"
            )
        topic_list = ", ".join(esc(t) for t in by_item.get(item.id, [])) or "<em>no topic</em>"
        cards.append(
            f"<section><h2>{esc(caption)}</h2><code>{esc(item.id)}</code>"
            f'<div class="row">{"".join(figs)}</div><p class="topics">{topic_list}</p></section>'
        )
    stats = [
        ("items", f"{len(items)} ({len(species)} species, {len(items) - len(species)} places)"),
        ("photos", str(photo_count)),
        ("size", f"{total / 1024 / 1024:.2f} MB"),
        ("topics mapped", str(len(topics))),
        ("species with no topic", ", ".join(no_topic) or "none"),
        (
            "topics naming a species but unmapped",
            "; ".join(f"{t} → {i}" for t, i in unmapped) or "none",
        ),
    ]
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Media review</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font:14px/1.4 system-ui,sans-serif;margin:16px;background:#f6f6f4;color:#1c1c1a}}
table{{border-collapse:collapse;margin-bottom:16px}}td{{border:1px solid #ccc;padding:4px 8px;vertical-align:top}}
section{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:12px;margin:12px 0}}
h2{{margin:0 0 4px;font-size:16px}}.row{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}}
figure{{margin:0;width:160px}}img{{display:block;border-radius:4px;background:#eee}}
figcaption{{font-size:11px;color:#555}}.topics{{font-size:12px;color:#333}}pre{{white-space:pre-wrap;font-size:11px}}
</style></head><body>
<h1>Media review</h1>
<table>{"".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in stats)}</table>
{"".join(cards)}
<h2>Build log</h2><pre>{esc(chr(10).join(log))}</pre>
<h2>Curation notes</h2><pre>{esc(chr(10).join(f"{k}: {v}" for k, v in {**SKIPPED_FOLDERS, **DROP_NOTES}.items()))}</pre>
</body></html>
"""
    (review_dir / "index.html").write_text(page, encoding="utf-8")


# ------------------------------------------------------------------------ cli


def build(
    src: Path,
    places_file: Path | None,
    review_dir: Path | None,
    out_root: Path = REPO,
    catalog_path: Path = CATALOG,
    curation: dict[str, Species] = SPECIES,
) -> dict:
    log: list[str] = []
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    items = collect_species(src, curation, log) + collect_places(src, places_file, log)
    topics = map_topics(catalog, items)
    write_outputs(items, topics, out_root)
    total = check_invariants(out_root)
    if review_dir is not None:
        write_review(review_dir, items, topics, catalog, out_root, total, log)
    return {
        "items": len(items),
        "photos": sum(len(i.photos) for i in items),
        "bytes": total,
        "topics": len(topics),
        "log": log,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--src", type=Path, required=True, help="extracted export root")
    parser.add_argument(
        "--places", type=Path, default=None, help="places.json from the landscape classifier"
    )
    parser.add_argument(
        "--review-dir", type=Path, default=None, help="where to write the review sheet"
    )
    parser.add_argument(
        "--out-root",
        type=Path,
        default=REPO,
        help="repo root to write outputs under (tests use a temp dir)",
    )
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args(argv)
    result = build(args.src, args.places, args.review_dir, args.out_root, args.catalog)
    for line in result["log"]:
        print(line)
    print(
        f"items {result['items']}, photos {result['photos']}, topics {result['topics']}, total {result['bytes'] / 1024 / 1024:.2f} MB"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
