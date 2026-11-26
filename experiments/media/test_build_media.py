"""Behavior tests for build_media.py.

Run: uv run --with pytest --with pillow python -m pytest experiments/media -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_media as bm


def species_items(*folders: str) -> list[bm.Item]:
    """Items built from the production curation table, without images."""
    return [
        bm.Item(
            id="species." + bm.snake(f),
            kind="species",
            common=f,
            scientific=f.replace("_", " "),
            photos=[],
            aliases=bm.SPECIES[f].aliases,
            variants=bm.SPECIES[f].variants,
        )
        for f in folders
    ]


def place_items(*ids: str) -> list[bm.Item]:
    return [
        bm.Item(
            id="place." + p,
            kind="place",
            common=bm.PLACES[p].name,
            scientific=None,
            photos=[],
            place=bm.PLACES[p],
        )
        for p in ids
    ]


def topic(id_: str, short: str, label: str = "", section: str = "fauna", kind: str = "faq") -> dict:
    return {"id": id_, "section": section, "kind": kind, "label": label, "short": short}


# ---------------------------------------------------------------- credits


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            '<a rel="nofollow" href="https://flickr.com/x">Dick Culbert</a> from Gibsons, B.C., Canada',
            "Dick Culbert",
        ),
        ("Martin St-Amant ( S23678 )", "Martin St-Amant"),
        ("Joseph Smit (1836–1929)", "Joseph Smit"),
        ("iNaturalist user: fabien_anthelme", "fabien_anthelme"),
        ("Original: Maël Martin Derivative work: Aristeas", "Maël Martin"),
        ("C. Formanski, as an employee of the US National Park Service.", "C. Formanski"),
        ("Unknown author Unknown author", ""),
        ("no rights reserved", ""),
        ("  <span>Ana&nbsp;María\n  Pérez</span> ", "Ana María Pérez"),
    ],
)
def test_clean_author_returns_plain_name(raw: str, expected: str) -> None:
    assert bm.clean_author(raw) == expected


def test_clean_author_caps_long_credits() -> None:
    out = bm.clean_author(
        "Wolfgang Amadeus Theophilus Johannes Chrysostomus Sigismundus Mozart Salzburger"
    )
    assert len(out) <= bm.AUTHOR_MAX and out.endswith("…")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("(WT-en) Foj333 at English Wikivoyage", "Foj333"),
        ("User: (WT-shared) CONOCER at wts wikivoyage", "CONOCER"),
        ("Alex Popovkin, Bahia, Brazil from Brazil", "Alex Popovkin"),
        ("Akito Y. Kawahara, Kenji Nishida, Donald R. Davis", "Akito Y. Kawahara"),
        ("Álvaro Siabatto & José Próspero Hurtado Caro", "Álvaro Siabatto"),
        ("Ana Pérez and Luis Gómez", "Ana Pérez"),
        (
            "No machine-readable author provided. Mauricioagudelo~commonswiki assumed"
            " (based on copyright claims).",
            "Mauricioagudelo",
        ),
        ("DickDaniels ( http://theworldbirds.org/ )", "DickDaniels"),
        ("Ymblanter (talk)", "Ymblanter"),
        ("Own work, Ana Pérez https://example.org/ana", "Ana Pérez"),
        ("ALAN SCHMIERER", "Alan Schmierer"),
        # Names that only look like the patterns above stay whole.
        ("melianie_max_and_asker", "melianie_max_and_asker"),
        ("Mike's Birds from Riverside, CA, US", "Mike's Birds"),
        ("National Park Service", "National Park Service"),
        ("Cocodrilo del orinoco", "Cocodrilo del orinoco"),
        ("brian.gratwicke", "brian.gratwicke"),
        ("LBM1948", "LBM1948"),
    ],
)
def test_clean_author_keeps_one_short_name(raw: str, expected: str) -> None:
    assert bm.clean_author(raw) == expected


@pytest.mark.parametrize(
    ("license_label", "author", "ok"),
    [
        ("CC BY-SA 4.0", "Ana", True),
        ("CC BY 2.0", "Ana", True),
        ("CC0", "Ana", True),
        ("Public domain", "National Park Service", True),
        ("CC0", "", False),
        ("Attribution", "Jerry Segraves", False),
        ("GFDL 1.2", "Ana", False),
        ("", "Ana", False),
    ],
)
def test_license_filter(license_label: str, author: str, ok: bool) -> None:
    assert bm.license_ok(license_label, author) is ok


# ---------------------------------------------------------------- mapping


def test_topics_are_ordered_by_first_mention_and_capped() -> None:
    items = species_items(
        "Vultur_gryphus", "Puma_concolor", "Tapirus_pinchaque", "Tremarctos_ornatus"
    )
    catalog = [
        topic(
            "fauna.mix",
            "Viven el oso de anteojos, la danta de montaña, el cóndor andino y el puma.",
        )
    ]
    assert bm.map_topics(catalog, items) == {
        "fauna.mix": [
            "species.tremarctos_ornatus",
            "species.tapirus_pinchaque",
            "species.vultur_gryphus",
        ]
    }


def test_spelling_variants_and_accents_match() -> None:
    items = species_items("Oxypogon_stuebelii")
    catalog = [
        topic("fauna.a", "El chivito (OXYPOGON STUBELII) está en peligro."),
        topic("fauna.b", "Busca el Chivito de Páramo."),
    ]
    assert set(bm.map_topics(catalog, items)) == {"fauna.a", "fauna.b"}


def test_binomial_does_not_also_match_its_genus_item() -> None:
    items = species_items("Espeletia", "Espeletia_hartwegiana")
    catalog = [
        topic("flora.a", "El de aquí es Espeletia hartwegiana.", section="flora_ecosystems"),
        topic("flora.b", "Pajonal con Espeletia (grafía de 2006).", section="flora_ecosystems"),
    ]
    assert bm.map_topics(catalog, items) == {
        "flora.a": ["species.espeletia_hartwegiana"],
        "flora.b": ["species.espeletia"],
    }


def test_words_inside_other_words_do_not_match() -> None:
    items = species_items("Pristimantis", "Puma_concolor")
    catalog = [topic("fauna.a", "Las musarañas y la piraña no son ranas de lluvia; pumas sí.")]
    assert bm.map_topics(catalog, items) == {
        "fauna.a": ["species.pristimantis", "species.puma_concolor"]
    }
    assert bm.map_topics([topic("fauna.b", "Una musaraña y un pasaporte.")], items) == {}


def test_emergency_and_other_sections_are_skipped() -> None:
    items = species_items("Puma_concolor")
    catalog = [
        topic("health_safety.a", "Si ves un puma, retrocede.", section="health_safety"),
        topic("fauna.b", "Si ves un puma, retrocede.", kind="emergency"),
    ]
    assert bm.map_topics(catalog, items) == {}


def test_real_catalog_keeps_misnamed_parrot_and_other_antpittas_apart() -> None:
    catalog = json.loads(bm.CATALOG.read_text(encoding="utf-8"))
    topics = bm.map_topics(catalog, species_items(*bm.SPECIES))
    assert "species.hapalopsittaca_fuertesi" not in topics.get(
        "fauna.yellow_eared_national_status", []
    )
    assert topics["fauna.fuertes_parrot"] == ["species.hapalopsittaca_fuertesi"]
    for other in (
        "fauna.brown_banded_antpitta",
        "fauna.tawny_antpitta",
        "fauna.chestnut_naped_antpitta",
    ):
        assert "species.grallaria_rufula" not in topics.get(other, [])


def test_places_match_aliases_but_not_municipalities() -> None:
    items = place_items("nevado_santa_isabel", "nevado_tolima", "laguna_otun", "nevado_ruiz")
    catalog = [
        topic(
            "geography.santa_isabel_height",
            "Según el Ideam, las cumbres están a 4.950 m.",
            label="cotas de Santa Isabel",
            section="geography",
        ),
        topic(
            "geography.tolima_municipalities",
            "Murillo, Santa Isabel y Herveo.",
            label="municipios tolimenses",
            section="geography",
        ),
        topic(
            "geography.rio_otun",
            "El río nace en la Laguna del Otún. Luego baja al Ruiz.",
            label="río",
            section="geography",
        ),
        topic(
            "activities.tolima_summit",
            "Se sube con guía.",
            label="cumbre por Schimmer",
            section="activities",
        ),
        topic(
            "geography.ruiz_where",
            "Está entre Caldas y Tolima.",
            label="dónde queda el Ruiz",
            section="geography",
        ),
        topic("fauna.otun_birds", "Aves de la Laguna del Otún.", section="fauna"),
    ]
    assert bm.map_topics(catalog, items) == {
        "activities.tolima_summit": ["place.nevado_tolima"],
        "geography.rio_otun": ["place.laguna_otun"],
        "geography.ruiz_where": ["place.nevado_ruiz"],
        "geography.santa_isabel_height": ["place.nevado_santa_isabel"],
    }


# ------------------------------------------------------------- end to end


def make_jpeg(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path, "JPEG")


@pytest.fixture
def fixture_src(tmp_path: Path) -> tuple[Path, Path, Path]:
    src = tmp_path / "src"
    folder = src / bm.SPECIES_DIR / "02_aves" / "Vultur_gryphus"
    make_jpeg(folder / "Condor_one.jpg", (1200, 800), (200, 10, 10))
    make_jpeg(folder / "Condor_two.jpg", (600, 900), (10, 200, 10))
    make_jpeg(folder / "Condor_gfdl.jpg", (800, 800), (10, 10, 200))
    credits = [
        {
            "grupo": "02_aves",
            "nombre_cientifico": "Vultur gryphus",
            "nombre_comun": "cóndor andino",
            "archivo": "File:Condor one.jpg",
            "url": "",
            "autor": "<a>Ana</a> from Quito, Ecuador",
            "licencia": "CC BY 2.0",
            "descripcion": "",
        },
        {
            "grupo": "02_aves",
            "nombre_cientifico": "Vultur gryphus",
            "nombre_comun": "cóndor andino",
            "archivo": "File:Condor two.jpg",
            "url": "",
            "autor": "Beto",
            "licencia": "CC0",
            "descripcion": "",
        },
        {
            "grupo": "02_aves",
            "nombre_cientifico": "Vultur gryphus",
            "nombre_comun": "cóndor andino",
            "archivo": "File:Condor gfdl.jpg",
            "url": "",
            "autor": "Caro",
            "licencia": "GFDL 1.2",
            "descripcion": "",
        },
    ]
    (src / bm.SPECIES_CREDITS).write_text(json.dumps(credits), encoding="utf-8")
    make_jpeg(src / bm.PLACES_DIR / "Laguna del Otún 1.jpg", (1600, 900), (50, 50, 150))
    make_jpeg(src / bm.PLACES_DIR / "Laguna del Otún 2.jpg", (1600, 900), (60, 60, 160))
    make_jpeg(src / bm.PLACES_DIR / "Otún GFDL.jpg", (1600, 900), (70, 70, 170))
    place_credits = [
        {
            "titulo": "File:Laguna del Otún 1.jpg",
            "url": "",
            "descripcion": "",
            "autor": "Dani",
            "licencia": "CC BY-SA 4.0",
        },
        {
            "titulo": "File:Laguna del Otún 2.jpg",
            "url": "",
            "descripcion": "",
            "autor": "Eva",
            "licencia": "CC BY-SA 4.0",
        },
        {
            "titulo": "File:Otún GFDL.jpg",
            "url": "",
            "descripcion": "",
            "autor": "Fede",
            "licencia": "GFDL 1.2",
        },
    ]
    (src / bm.PLACES_CREDITS).write_text(json.dumps(place_credits), encoding="utf-8")
    places = tmp_path / "places.json"
    places.write_text(
        json.dumps(
            [
                {"file": "Laguna del Otún 1.jpg", "place": "laguna_otun", "quality": 2, "note": ""},
                {"file": "Laguna del Otún 2.jpg", "place": "laguna_otun", "quality": 3, "note": ""},
                {"file": "Otún GFDL.jpg", "place": "laguna_otun", "quality": 3, "note": ""},
                {"file": "Laguna del Otún 1.jpg", "place": None, "quality": 1, "note": "pending"},
            ]
        ),
        encoding="utf-8",
    )
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            [
                topic("fauna.andean_condor", "El cóndor andino (Vultur gryphus) vuela alto."),
                topic(
                    "geography.laguna_otun",
                    "La Laguna del Otún es glaciar.",
                    label="laguna del Otún",
                    section="geography",
                ),
            ]
        ),
        encoding="utf-8",
    )
    return src, places, catalog


CURATION = {
    "Vultur_gryphus": bm.Species(
        aliases=("condor andino",),
        photos=(
            ("Condor_one.jpg", (0.3, 0.5)),
            ("Condor_two.jpg", None),
            ("Condor_gfdl.jpg", None),
        ),
    )
}


def output_bytes(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()
    }


def test_build_writes_contract_and_is_idempotent(
    fixture_src: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    src, places, catalog = fixture_src
    out = tmp_path / "out"
    media = out / bm.MEDIA_DIR
    media.mkdir(parents=True)
    (media / "species.stale_item.1.webp").write_bytes(b"old")
    (media / "keep-me.png").write_bytes(b"not ours")

    bm.build(src, places, tmp_path / "review", out, catalog, CURATION)
    first = output_bytes(out)
    bm.build(src, places, tmp_path / "review", out, catalog, CURATION)
    assert output_bytes(out) == first

    data = json.loads((out / bm.MANIFEST).read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert data["items"]["species.vultur_gryphus"] == {
        "kind": "species",
        "common": "Cóndor andino",
        "scientific": "Vultur gryphus",
        "photos": [
            {"file": "species.vultur_gryphus.1.webp", "author": "Ana", "license": "CC BY 2.0"},
            {"file": "species.vultur_gryphus.2.webp", "author": "Beto", "license": "CC0"},
        ],
    }
    # Best quality first; the GFDL landscape is dropped.
    assert [p["author"] for p in data["items"]["place.laguna_otun"]["photos"]] == ["Eva", "Dani"]
    assert data["items"]["place.laguna_otun"]["scientific"] is None
    assert data["topics"] == {
        "fauna.andean_condor": ["species.vultur_gryphus"],
        "geography.laguna_otun": ["place.laguna_otun"],
    }

    assert not (media / "species.stale_item.1.webp").exists()
    assert (media / "keep-me.png").read_bytes() == b"not ours"
    ts = (out / bm.PHOTOS_TS).read_text(encoding="utf-8")
    assert ts.splitlines()[0] == "// Generated by experiments/media/build_media.py. Do not edit."
    assert (
        "  'place.laguna_otun.1.webp': require('../../../assets/media/place.laguna_otun.1.webp'),"
        in ts
    )
    for name in ("place.laguna_otun.1.webp", "species.vultur_gryphus.2.webp"):
        with Image.open(media / name) as img:
            assert (img.format, img.size) == ("WEBP", (bm.WIDTH, bm.HEIGHT))
    assert (tmp_path / "review" / "index.html").is_file()


def test_build_without_places_file_has_no_place_items(
    fixture_src: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    src, _, catalog = fixture_src
    out = tmp_path / "out"
    bm.build(src, None, None, out, catalog, CURATION)
    data = json.loads((out / bm.MANIFEST).read_text(encoding="utf-8"))
    assert list(data["items"]) == ["species.vultur_gryphus"]
    assert "place." not in (out / bm.PHOTOS_TS).read_text(encoding="utf-8")
