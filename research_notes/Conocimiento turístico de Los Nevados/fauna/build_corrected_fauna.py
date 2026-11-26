"""Rebuild fauna.json from frozen examples plus sourced answers.

Does not edit the JSON in place. Inputs:
- source/examples.json (visitor questions kept from the previous section)
- evidence/raw/ (PNN page, Resolution 207, CARDER Darwin Core checklist, VOC sheet)

Every answer claim is backed by a quote written to evidence/quotes.md.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from round2_entries import bundle as round2_bundle

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parent.parent
SECTIONS = ROOT / "data" / "knowledge" / "sections"
TARGET = SECTIONS / "fauna.json"
RAW = HERE / "evidence" / "raw"
EXAMPLES = HERE / "source" / "examples.json"
DATE = "2026-11-21"

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
RES_URL = "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf"
VOC_URL = "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/Imagen-20-VOC-web.pdf"
SIB_URL = "https://doi.org/10.15472/r8t5xv"

SOURCES = {
    "pnn": ("Parques Nacionales Naturales de Colombia - PNN Los Nevados", PNN_URL),
    "res": ("Parques Nacionales Naturales de Colombia - Resolución 207 de 2023", RES_URL),
    "voc": ("Parques Nacionales Naturales de Colombia - lámina de valores objeto de conservación", VOC_URL),
    "sib": ("SiB Colombia - Biodiversidad Parque Nacional Natural Nevados (CARDER)", SIB_URL),
    "plan": (
        "Parques Nacionales Naturales de Colombia - Plan de manejo PNN Los Nevados 2017-2022",
        "https://www.parquesnacionales.gov.co/wp-content/uploads/2020/10/plan-de-manejo-pnn-los-nevados.pdf",
    ),
    "mads": (
        "Ministerio de Ambiente - lista SiB de la Resolución 0126 de 2024",
        "https://doi.org/10.15472/frowz3",
    ),
    "minamb": (
        "Ministerio de Ambiente y Desarrollo Sostenible - Resolución 0126 de 2024",
        "https://www.minambiente.gov.co/documento-normativa/resolucion-0126-de-2024/",
    ),
    "humboldt": (
        "Instituto Humboldt - estudios bióticos del complejo de páramos Los Nevados",
        "https://ipt.biodiversidad.co/iavh/resource?r=rrbb_nevados_faunaflora_2015",
    ),
}

ROUND2: dict | None = None

# Exact substrings of the raw files. check_quotes.py re-reads them.
QUOTES: list[tuple[str, str, str, str]] = [
    (
        "pnn-birds",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "La población de aves es abundante y variada. Sobresale el chivito de páramo ( Oxypogon stuebelii ), un colibrí de grandes alturas que extrae néctar de las flores de frailejón y que es endémico de la región, ya que no existe en ninguna otra parte del mundo. Otra especie endémica es el tororoi de Miller ( Grallaria milleri ), un ave pequeña y difícil de ver, propia de la parte baja de los bosques (sotobosque). Hay aves de gran porte, como el águila crestada ( Spizaetus isidori ), rapaz suramericana que puede superar los 70 cm de largo, y el impresionante cóndor andino ( Vultur gryphus ), ave nacional de Colombia con más de 3 m de envergadura. Otras aves representativas del Parque son el pato andino ( Oxyura ferruginea ), el periquito de los nevados ( Bolborhynchus ferrugineifrons ) y águila de páramo ( Geranoetus melanoleucus ).",
    ),
    (
        "pnn-mammals",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "Entre los mamíferos se encuentran especies icónicas de Colombia como la danta de montaña ( Tapirus pinchaque ), la guagua loba ( Dinomys branickii ) y el puma ( Puma concolor ). Se destaca la amplia variedad de murciélagos (20 especies), entre insectívoros, frugívoros y nectarívoros, que desempeñan un importante papel como polinizadores.",
    ),
    (
        "pnn-indicators",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "que incluye el estudio de especies vulnerables o indicadoras de los ecosistemas, como el oso de anteojos, el chivito de páramo, el venado conejo, el cóndor de los Andes, la danta de páramo, el loro orejiamarillo y el frailejón.",
    ),
    (
        "pnn-voc",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "así como especies en categoría de amenaza o endémicas, como el chivito de páramo ( Oxypogon stuebelii ).",
    ),
    (
        "pnn-brisas",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "En el sector Brisas-Kumanday puedes realizar observación geológica, observación de fauna y flora o fotografía no comercial.",
    ),
    (
        "pnn-cisne-otun",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "En los sectores Cisne-Poleka Kasue y Otún puedes disfrutar de senderismo, montañismo, observación de aves, observación geológica, observación de fauna y flora.",
    ),
    (
        "pnn-santa-isabel",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "Desde aquí observas los nevados del Ruiz (Kumanday) y Santa Isabel (Poleka Kasue), junto con el paramillo del Cisne.",
    ),
    (
        "pnn-otun-lagoon",
        PNN_URL,
        "raw/pnn_nevados.txt",
        "Aquí puedes conocer la Laguna del Otún, la más grande del Parque",
    ),
    (
        "res-contact",
        RES_URL,
        "raw/resolucion-207-2023.txt",
        "Evitar el contacto con la vida silvestre. No intente coger, ni alimentar ni desplazar especies de fauna de las zonas donde se encuentran.",
    ),
    (
        "res-number",
        RES_URL,
        "raw/resolucion-207-2023.txt",
        "RESOLUCION NUMERO 207",
    ),
    (
        "voc-fauna",
        VOC_URL,
        "raw/voc-page-2.txt",
        "Oxypogon stuebelii Geranoaetus melanoleucus",
    ),
    (
        "voc-heading",
        VOC_URL,
        "raw/voc-page-2.txt",
        "FAUNA Y FLORA",
    ),
    (
        "sib-citation",
        SIB_URL,
        "raw/dwca/eml.xml",
        "Biodiversidad Parque Nacional Natural Nevados. v2.2. Corporación Autónoma Regional de Risaralda - CARDER.",
    ),
]

# Scientific names that must appear verbatim in the Darwin Core taxon file.
TAXA = {
    "fauna.brown_banded_antpitta": "Grallaria milleri",
    "fauna.ruiz_parakeet": "Bolborhynchus ferrugineifrons",
    "fauna.fuertes_parrot": "Hapalopsittaca fuertesi",
    "fauna.golden_plumed_parakeet": "Leptosittaca branickii",
    "fauna.tawny_antpitta": "Grallaria quitensis",
    "fauna.chestnut_naped_antpitta": "Grallaria nuchalis",
    "fauna.torrent_duck": "Merganetta armata",
    "fauna.sword_billed_hummingbird": "Ensifera ensifera",
    "fauna.shining_sunbeam": "Aglaeactis cupripennis",
    "fauna.tyrian_metaltail": "Metallura tyrianthina",
    "fauna.white_capped_dipper": "Cinclus leucocephalus",
    "fauna.great_thrush": "Turdus fuscater",
    "fauna.hooded_mountain_toucan": "Andigena hypoglauca",
    "fauna.rufous_collared_sparrow": "Zonotrichia capensis",
    "fauna.short_eared_owl_paramo": "Asio flammeus",
    "fauna.noble_snipe": "Gallinago nobilis",
    "fauna.spectacled_bear": "Tremarctos ornatus",
    "fauna.yellow_eared_parrot": "Ognorhynchus icterotis",
    "fauna.mountain_tapir": "Tapirus pinchaque",
    "fauna.cougar_puma": "Puma concolor",
    "fauna.northern_tiger_cat": "Leopardus tigrinus subsp. pardinoides",
    "fauna.pacarana_guagua_loba": "Dinomys branickii",
    "fauna.mountain_paca": "Cuniculus taczanowskii",
    "fauna.little_red_brocket": "Mazama rufina",
    "fauna.northern_pudu": "Pudu mephistophiles",
    "fauna.white_tailed_deer": "Odocoileus virginianus",
    "fauna.mountain_coati": "Nasuella olivacea",
    "fauna.long_tailed_weasel": "Mustela frenata affinis",
    "fauna.paramo_rabbit": "Sylvilagus brasiliensis fulvescens",
    "fauna.crab_eating_fox": "Cerdocyon thous",
    "fauna.black_chested_buzzard_eagle": "Geranoaetus melanoleucus",
}

GROUP_TAXA = {
    "fauna.mountain_tanagers": [
        "Anisognathus igniventris",
        "Anisognathus lacrymosus",
        "Buthraupis montana",
        "Dubusia taeniata",
    ],
    "fauna.paramo_rodents_shrews": [
        "Thomasomys cinereiventer",
        "Akodon affinis",
        "Cryptotis thomasi",
    ],
}

LABELS = {
    "fauna.yellow_eared_parrot": "loro orejiamarillo en Los Nevados",
    "fauna.sword_billed_hummingbird": "colibrí piquiespada en Los Nevados",
    "fauna.tawny_antpitta": "tororoi leonado en Los Nevados",
    "fauna.chestnut_naped_antpitta": "tororoi nuchicastaño en Los Nevados",
    "fauna.torrent_duck": "pato de torrente en Los Nevados",
    "fauna.black_and_chestnut_eagle": "águila crestada en Los Nevados",
    "fauna.black_chested_buzzard_eagle": "águila de páramo en Los Nevados",
    "fauna.buffy_helmetcrest": "chivito de páramo en Los Nevados",
    "fauna.shining_sunbeam": "rayito de sol andino en el parque",
    "fauna.white_capped_dipper": "mirlo acuático en Los Nevados",
    "fauna.great_thrush": "mirlo negro andino en el parque",
    "fauna.rufous_collared_sparrow": "copetón o chingolo en Los Nevados",
    "fauna.short_eared_owl_paramo": "búho orejicorto en Los Nevados",
    "fauna.mountain_tanagers": "tangaras de montaña en el listado",
    "fauna.northern_pudu": "venado conejo estudiado en el parque",
    "fauna.white_tailed_deer": "venado cola blanca en el listado",
    "fauna.mountain_paca": "guagua de páramo en el listado",
    "fauna.paramo_rodents_shrews": "ratones y musarañas del listado",
    "fauna.fuertes_parrot": "cotorra de Fuertes en el listado",
    "fauna.golden_plumed_parakeet": "perico paramuno en Los Nevados",
    "fauna.northern_tiger_cat": "tigrillo lanudo en el listado del parque",
    "fauna.little_red_brocket": "venado soche en el listado del parque",
    "fauna.mountain_coati": "cusumbo andino en el listado del parque",
    "fauna.long_tailed_weasel": "comadreja de cola larga en el listado",
    "fauna.crab_eating_fox": "zorro perruno en el listado del parque",
    "fauna.paramo_rabbit": "conejo de páramo en el listado",
    "fauna.hooded_mountain_toucan": "terlaque andino en el listado del parque",
    "fauna.noble_snipe": "agachadiza noble en el listado",
}

REPLACEMENTS = {
    "fauna.mammals_overview": {
        "animales grandes en los senderos": "qué mamíferos icónicos nombra la ficha del parque",
    },
    "fauna.threatened_species": {
        "animales en peligro crítico": "qué especies vulnerables o indicadoras estudia el parque",
    },
    "fauna.ruiz_parakeet": {
        "periquito endemico del parque los nevados": "el periquito de los nevados está en la ficha",
        "periquitos volando en bandadas en el paramo": "hay periquito de los nevados en el parque",
    },
    "fauna.yellow_eared_parrot": {
        "relacion del loro con la palma de cera": "hay loro orejiamarillo en Los Nevados",
    },
    "fauna.golden_plumed_parakeet": {
        "bandadas de pericos en el bosque altoandino": "está el perico paramuno en el listado del parque",
    },
    "fauna.brown_banded_antpitta": {
        "tororoi endemico de caldas y risaralda": "el tororoi de Miller es endémico de la región",
    },
    "fauna.chestnut_naped_antpitta": {
        "pajaro terrestre grande en bosque nublado": "hay tororoi nuchicastaño en el listado del parque",
    },
    "fauna.andean_duck": {
        "pato con pico azul en el páramo": "hay pato andino en Los Nevados",
        "pato de pico celeste en los nevados": "el pato turrio está en el parque",
        "Oxyura jamaicensis andina": "Oxyura ferruginea está en la ficha del parque",
        "patos en la Laguna del Otún": "qué dice el parque del pato andino",
        "ruddy duck high mountain lake Otun": "is the Andean duck on the park fact sheet?",
    },
    "fauna.black_and_chestnut_eagle": {
        "rapaz en peligro en la cordillera central": "hay águila crestada en Los Nevados",
    },
    "fauna.black_chested_buzzard_eagle": {
        "rapaz comun en el sector brisas": "hay águila de páramo en Los Nevados",
    },
    "fauna.sword_billed_hummingbird": {
        "colibrí con pico más largo que el cuerpo": "hay colibrí piquiespada en Los Nevados",
        "pájaro con pico larguísimo en Los Nevados": "Ensifera ensifera está en el listado del parque",
        "¿cuánto mide el pico del colibrí piquiespada?": "el piquiespada sale en el inventario del parque",
        "picaflor de pico espada en bosque altoandino": "registran al colibrí piquiespada en el parque",
        "colibri que vuela con pico hacia arriba": "cómo se llama el colibrí piquiespada del parque",
    },
    "fauna.white_capped_dipper": {
        "ave acuatica en quebradas de los nevados": "hay mirlo acuático en el listado del parque",
    },
    "fauna.great_thrush": {
        "pájaro negro grande con pico naranja": "hay mirlo negro en el listado del parque",
        "¿cómo se llama el pájaro negro de ojos y pico amarillos?": "Turdus fuscater está en el inventario del parque",
    },
    "fauna.hooded_mountain_toucan": {
        "pájaro con pico multicolor en bosque nublado": "hay terlaque andino en el listado del parque",
        "ave frugivora con pico pintado en la selva": "Andigena hypoglauca está en el inventario del parque",
    },
    "fauna.short_eared_owl_paramo": {
        "ave rapaz nocturna de alta montaña": "hay búho orejicorto en el listado del parque",
        "aves rapaces nocturnas en el parque": "Asio flammeus está en el inventario del parque",
    },
    "fauna.noble_snipe": {
        "pájaro con pico largo en lodazales del páramo": "hay agachadiza noble en el listado del parque",
        "¿qué pájaro clava el pico en el barro del páramo?": "Gallinago nobilis está en el inventario del parque",
    },
    "fauna.mountain_tanagers": {
        "bandadas mixtas de aves en bosque nublado": "qué tangaras trae el listado del parque",
    },
    "fauna.mountain_tapir": {
        "danta con pelaje grueso para el frío": "hay danta de montaña en el parque",
    },
    "fauna.cougar_puma": {
        "avistamientos de pumas en senderos": "hay puma en Los Nevados",
    },
    "fauna.northern_tiger_cat": {
        "gato salvaje manchado de alta montaña": "hay tigrillo lanudo en Los Nevados",
        "felino manchado pequeño en bosque nublado": "Leopardus tigrinus está en el listado del parque",
        "tigrillo con pelaje espeso para el frio": "registran oncilla en el parque nacional",
    },
    "fauna.pacarana_guagua_loba": {
        "guagua loba de noche en la selva": "hay guagua loba en el parque",
    },
    "fauna.mountain_paca": {
        "roedor nocturno que vive cerca de quebradas": "hay guagua de páramo en Los Nevados",
        "guagua con pelaje grueso manchado": "Cuniculus taczanowskii está en el listado del parque",
        "roedor manchado cerca de riachuelos": "boruga de montaña en el parque nacional",
        "mamifero nocturno de madriguera en la montana": "la guagua de páramo sale en el inventario del parque",
    },
    "fauna.little_red_brocket": {
        "venadito cafe rojizo en el sendero": "hay venado soche en el listado del parque",
    },
    "fauna.northern_pudu": {
        "ciervo más pequeño del mundo en Los Nevados": "el parque estudia al venado conejo",
        "¿cuál es el venado más diminuto de Colombia?": "qué es el venado conejo del parque",
        "ciervo del tamaño de un perro pequeño": "hay venado conejo en Los Nevados",
        "venado miniatura en los frailejones": "venado conejo especie indicadora del parque",
        "Pudella mephistophiles": "Pudu mephistophiles está en el listado del parque",
        "Northern pudu Pudella mephistophiles Los Nevados": "is Pudu mephistophiles on the park checklist?",
        "smallest deer in the world Colombian paramo": "does the park study the rabbit deer?",
    },
    "fauna.mountain_coati": {
        "coati de cola larga en el sendero": "hay cusumbo andino en el listado del parque",
    },
    "fauna.paramo_rabbit": {
        "conejito pardo corriendo entre frailejones": "hay conejo de páramo en el listado del parque",
    },
    "fauna.crab_eating_fox": {
        "¿hay zorros en la carretera a Brisas?": "hay zorro perruno en el listado del parque",
    },
    "fauna.paramo_rodents_shrews": {
        "Akodon bogotensis": "Akodon affinis está en el listado del parque",
        "Cryptotis colombiana": "Cryptotis thomasi está en el listado del parque",
        "ratoncito con pelaje espeso en pajonales": "hay Thomasomys cinereiventer en Los Nevados",
        "ratones que viven bajo los frailejones": "qué ratones y musarañas trae el listado del parque",
    },
    "fauna.fuertes_parrot": {
        "loro en peligro de extinción en el nevado": "hay cotorra de Fuertes en el parque",
        "loro endemico de bosques altoandinos": "Hapalopsittaca fuertesi está en el listado del parque",
        "redescubrimiento de la cotorra de fuertes": "la cotorra de Fuertes sale en el inventario del parque",
        "indigo-winged parrot endangered": "is Fuertes's parrot on the park checklist?",
        "lorito pequeno con corona azul": "registran la cotorra coroniazul en el parque",
        "cotorrita amenazada de la cordillera central": "dónde aparece la cotorra de Fuertes",
        "pajaro escaso en la selva altoandina": "la cotorra de Fuertes está registrada en el parque",
    },
    "fauna.injured_wildlife_protocol": {
        "animal silvestre golpeado en la carretera Brisas Murillo": "vi un animal herido en el sendero qué hago",
    },
    "fauna.spotting_sector_brisas": {
        "avistar cóndores en Brisas": "se puede observar fauna en el sector Brisas",
        "¿qué animales se ven en Valle de las Tumbas?": "hay observación de fauna en Brisas-Kumanday",
        "que bichos salen en el valle de las tumbas": "qué actividad de fauna hay en Brisas",
        "animals near Nevado del Ruiz Valle de las Tumbas": "can I watch wildlife in the Brisas sector?",
    },
    "fauna.spotting_sector_santa_isabel": {
        "animales en el sendero Conejeras": "se puede observar fauna en el sector de Santa Isabel",
        "aves en el sendero hacia el glaciar": "hay observación de aves en Cisne Poleka Kasue",
    },
}

DELETED = {
    "fauna.amphibians_overview": "El listado Darwin Core del parque no trae anfibios y la ficha de PNN no los nombra.",
    "fauna.reptiles_overview": "No hay reptiles en el listado ni en la ficha.",
    "fauna.insects_invertebrates_overview": "No hay insectos en el listado ni en la ficha.",
    "fauna.condor_reintroduction_program": "Ninguna fuente descargada describe un programa de reintroducción.",
    "fauna.bear_diet_habits": "La ficha no describe la dieta del oso.",
    "fauna.tapir_ecological_role": "La ficha no describe un rol ecológico de la danta.",
    "fauna.andean_coot": "El listado trae Fulica americana, que no es la focha andina (Fulica ardesiaca). No se reetiquetó.",
    "fauna.paramo_toad_osornophryne": "Osornophryne no está en el listado ni en la ficha.",
    "fauna.paramo_rain_frogs": "Pristimantis no está en el listado ni en la ficha.",
    "fauna.harlequin_frog_atelopus": "Atelopus no está en el listado ni en la ficha.",
    "fauna.mountain_collared_lizard": "Stenocercus no está en el listado ni en la ficha.",
    "fauna.shade_lizards_andinosaura": "Andinosaura no está en el listado ni en la ficha.",
    "fauna.andean_chameleon_anole": "Anolis no está en el listado ni en la ficha.",
    "fauna.earth_snakes_atractus": "Atractus no está en el listado ni en la ficha.",
    "fauna.venomous_snakes_absence": "Ninguna fuente dice que no haya serpientes de importancia médica.",
    "fauna.paramo_bumblebees": "Bombus no está en el listado ni en la ficha.",
    "fauna.paramo_butterflies": "No hay mariposas en el listado ni en la ficha.",
    "fauna.rainbow_trout_impact": "Oncorhynchus no está en el listado ni en la ficha.",
    "fauna.aquatic_macroinvertebrates": "No hay macroinvertebrados en las fuentes descargadas.",
    "fauna.spotting_sector_la_pastora": "La ficha no describe fauna en La Pastora.",
    "fauna.spotting_sector_combeima": "Combeima aparece como cuenca en la lámina de VOC, no como sitio de fauna.",
    "fauna.birdwatching_altitudinal_zones": "No hay conteo ni pisos de avistamiento en las fuentes.",
    "fauna.best_hours_birding": "Ninguna fuente fija un horario de aves.",
    "fauna.best_hours_mammals": "Ninguna fuente fija un horario de mamíferos.",
    "fauna.weather_impact_wildlife": "Ninguna fuente liga el clima del día con la fauna.",
    "fauna.encounter_spectacled_bear": "No hay guía oficial de encuentro con oso en las fuentes descargadas.",
    "fauna.encounter_cougar_puma": "No hay protocolo de encuentro con puma en las fuentes.",
    "fauna.encounter_mountain_tapir": "No hay protocolo de encuentro con danta en las fuentes.",
    "fauna.safe_viewing_distance": "Ninguna fuente da una distancia en metros.",
    "fauna.wildlife_aggression_myths": "Ninguna fuente habla del temperamento de la fauna.",
    "fauna.feral_dogs_threat": "Ninguna fuente descargada menciona perros asilvestrados.",
    "fauna.roadkill_risk_murillo_road": "Ninguna fuente descargada documenta atropellos en la vía a Murillo.",
}

HANDS_OFF = "No lo cojas ni lo desplaces."


def listed(name: str) -> tuple[str, str]:
    short = (
        f"El listado Biodiversidad Parque Nacional Natural Nevados, de la CARDER, registra a {name}. "
        f"Si lo ves, {HANDS_OFF[0].lower()}{HANDS_OFF[1:]}"
    )
    variant = (
        f"{name} figura en el listado de biodiversidad del parque publicado por la CARDER. "
        "No lo cojas ni lo saques de donde está."
    )
    return short, variant


def listed_many(names: list[str]) -> tuple[str, str]:
    shown = ", ".join(names[:-1]) + " y " + names[-1]
    return listed(shown)


def source(*keys: str) -> list[dict[str, str]]:
    out = []
    for key in keys:
        label, url = SOURCES[key]
        out.append({"label": label, "url": url, "retrieved_at": DATE})
    return out


def prose(
    entry_id: str,
    kind: str,
    short: str,
    variant: str,
    sources: list[str],
    tags: list[str],
) -> dict:
    return {
        "id": entry_id,
        "kind": kind,
        "short": short,
        "variant": variant,
        "sources": sources,
        "tags": tags,
    }


ENTRIES = [
    prose(
        "fauna.fauna_overview",
        "explanation",
        "La ficha del parque habla de una población de aves abundante y variada, y entre los mamíferos icónicos nombra la danta de montaña, la guagua loba y el puma. En Brisas, Cisne-Poleka Kasue y Otún hay observación de fauna y flora; no cojas ni desplaces animales.",
        "Hay aves abundantes y variadas; de mamíferos, la ficha destaca la danta de montaña, la guagua loba y el puma. Míralos sin cogerlos ni moverlos.",
        ["pnn", "res"],
        ["fauna", "aves", "mamiferos"],
    ),
    prose(
        "fauna.birds_overview",
        "explanation",
        "La ficha destaca el chivito de páramo, el tororoi de Miller, el águila crestada, el cóndor andino, el pato andino, el periquito de los nevados y el águila de páramo. Pregunta por la observación de aves y no las cojas ni las desplaces.",
        "Esas aves están nombradas en la ficha del parque. Para intentar verlas, pregunta por la observación de aves y no las toques.",
        ["pnn", "res"],
        ["aves", "ficha"],
    ),
    prose(
        "fauna.mammals_overview",
        "explanation",
        "La ficha nombra la danta de montaña (Tapirus pinchaque), la guagua loba (Dinomys branickii) y el puma (Puma concolor), y destaca 20 especies de murciélagos, entre insectívoros, frugívoros y nectarívoros. También estudia al oso de anteojos, al venado conejo y a la danta de páramo. No los cojas ni los desplaces.",
        "Esos mamíferos salen en la ficha: tres icónicos, 20 especies de murciélagos y, como especies que el parque estudia, el oso de anteojos, el venado conejo y la danta de páramo. No los cojas.",
        ["pnn", "res"],
        ["mamiferos", "murcielagos"],
    ),
    prose(
        "fauna.endemic_species",
        "fact",
        "El chivito de páramo (Oxypogon stuebelii) es endémico de la región: la ficha dice que no existe en ninguna otra parte del mundo. Otra especie endémica que nombra es el tororoi de Miller (Grallaria milleri). No los cojas ni los desplaces.",
        "La ficha marca como endémicos al chivito de páramo y al tororoi de Miller. Obsérvalos sin cogerlos ni moverlos.",
        ["pnn", "res"],
        ["endemismo", "chivito", "tororoi"],
    ),
    prose(
        "fauna.threatened_species",
        "fact",
        "El parque estudia como especies vulnerables o indicadoras al oso de anteojos, el chivito de páramo, el venado conejo, el cóndor de los Andes, la danta de páramo y el loro orejiamarillo. No las cojas ni las desplaces.",
        "Esas seis especies son las que la ficha llama vulnerables o indicadoras. Míralas sin cogerlas ni moverlas.",
        ["pnn", "res"],
        ["vulnerables", "indicadoras"],
    ),
    prose(
        "fauna.conservation_target_species_voc",
        "fact",
        "Entre los valores objeto de conservación hay especies en categoría de amenaza o endémicas, como el chivito de páramo (Oxypogon stuebelii). La lámina de VOC también muestra a Geranoaetus melanoleucus en fauna y flora. No los cojas ni los desplaces.",
        "El chivito de páramo está en los valores objeto de conservación de la ficha, y Geranoaetus melanoleucus aparece en la lámina de fauna y flora. No los toques.",
        ["pnn", "voc", "res"],
        ["voc", "chivito"],
    ),
    prose(
        "fauna.andean_condor",
        "fact",
        "El cóndor andino (Vultur gryphus), ave nacional de Colombia, tiene según la ficha más de 3 m de envergadura. Pregunta por la observación de fauna y flora; no lo cojas ni lo desplaces.",
        "La ficha lo nombra como ave nacional y le atribuye más de 3 m de envergadura. Si lo ves, no lo cojas ni lo desplaces.",
        ["pnn", "res"],
        ["condor", "ave nacional"],
    ),
    prose(
        "fauna.buffy_helmetcrest",
        "fact",
        "El chivito de páramo (Oxypogon stuebelii) es un colibrí de grandes alturas: saca néctar de las flores de frailejón y es endémico de la región, pues no existe en ninguna otra parte del mundo. No lo cojas ni lo desplaces.",
        "Así lo describe la ficha: colibrí de altura, néctar de frailejón y endémico de la región. Míralo sin cogerlo.",
        ["pnn", "res"],
        ["chivito", "colibri", "frailejon"],
    ),
    prose(
        "fauna.brown_banded_antpitta",
        "fact",
        "El tororoi de Miller (Grallaria milleri) es, según la ficha, un ave pequeña, endémica y difícil de ver, propia del sotobosque. Ese nombre científico también está en el listado de la CARDER. No lo cojas ni lo desplaces.",
        "La ficha lo llama tororoi de Miller y el listado registra a Grallaria milleri. Si lo notas, no lo cojas ni lo desplaces.",
        ["pnn", "sib", "res"],
        ["tororoi", "miller"],
    ),
    prose(
        "fauna.andean_duck",
        "fact",
        "El pato andino (Oxyura ferruginea) es un ave representativa del parque, según su ficha. Pregunta por la observación de fauna y flora y no lo cojas ni lo desplaces.",
        "La ficha lo incluye entre las aves representativas, con el nombre Oxyura ferruginea. No lo cojas ni lo desplaces.",
        ["pnn", "res"],
        ["pato andino"],
    ),
    prose(
        "fauna.ruiz_parakeet",
        "fact",
        "El periquito de los nevados (Bolborhynchus ferrugineifrons) es un ave representativa del parque y también figura en el listado de la CARDER. No lo cojas ni lo desplaces.",
        "Sale en la ficha como ave representativa y en el listado como Bolborhynchus ferrugineifrons. No lo cojas ni lo desplaces.",
        ["pnn", "sib", "res"],
        ["periquito"],
    ),
    prose(
        "fauna.black_and_chestnut_eagle",
        "fact",
        "El águila crestada (Spizaetus isidori) es una rapaz suramericana que puede superar los 70 cm de largo, según la ficha del parque. Si la ves, no la cojas ni la desplaces.",
        "La ficha le da más de 70 cm de largo y la nombra entre las aves de gran porte. No la cojas ni la desplaces.",
        ["pnn", "res"],
        ["aguila crestada"],
    ),
    prose(
        "fauna.black_chested_buzzard_eagle",
        "fact",
        "La ficha llama águila de páramo a Geranoetus melanoleucus y la pone entre las aves representativas. La lámina de VOC escribe Geranoaetus melanoleucus en fauna y flora. No la cojas ni la desplaces.",
        "Geranoetus melanoleucus es la grafía de la ficha; Geranoaetus melanoleucus es la de la lámina de VOC y del listado. No la cojas ni la desplaces.",
        ["pnn", "voc", "sib", "res"],
        ["aguila de paramo"],
    ),
    prose(
        "fauna.spectacled_bear",
        "fact",
        "El parque estudia al oso de anteojos como especie vulnerable o indicadora. El listado de la CARDER registra a Tremarctos ornatus. Si ves uno, evita el contacto: no lo cojas, no lo alimentes y no lo desplaces.",
        "La ficha lo incluye entre las especies vulnerables o indicadoras, y el listado trae a Tremarctos ornatus. Evita el contacto y no lo muevas.",
        ["pnn", "sib", "res"],
        ["oso", "anteojos"],
    ),
    prose(
        "fauna.mountain_tapir",
        "fact",
        "La danta de montaña (Tapirus pinchaque) está entre los mamíferos icónicos de la ficha, que también estudia a la danta de páramo como especie vulnerable o indicadora. No la cojas ni la desplaces.",
        "La ficha usa los dos nombres: danta de montaña, con Tapirus pinchaque, y danta de páramo entre las especies que estudia. No la cojas ni la desplaces.",
        ["pnn", "sib", "res"],
        ["danta"],
    ),
    prose(
        "fauna.cougar_puma",
        "fact",
        "El puma (Puma concolor) está entre los mamíferos icónicos que nombra la ficha del parque. Si lo ves, evita el contacto: no lo cojas ni lo desplaces.",
        "Puma concolor figura en la ficha y en el listado de la CARDER. Evita el contacto y no lo desplaces.",
        ["pnn", "sib", "res"],
        ["puma"],
    ),
    prose(
        "fauna.pacarana_guagua_loba",
        "fact",
        "La guagua loba (Dinomys branickii) está entre los mamíferos icónicos que nombra la ficha del parque. Si la ves, no la cojas ni la desplaces.",
        "Ese nombre científico está en la ficha y en el listado de la CARDER. No la cojas ni la desplaces.",
        ["pnn", "sib", "res"],
        ["guagua loba"],
    ),
    prose(
        "fauna.highland_bats",
        "fact",
        "La ficha destaca 20 especies de murciélagos, entre insectívoros, frugívoros y nectarívoros, y les da un papel importante como polinizadores. No los cojas ni los desplaces.",
        "Son 20 especies, con esos tres hábitos y función de polinizadores, según la ficha. No los toques ni los muevas.",
        ["pnn", "res"],
        ["murcielagos", "polinizadores"],
    ),
    prose(
        "fauna.yellow_eared_parrot",
        "fact",
        "El parque estudia al loro orejiamarillo como especie vulnerable o indicadora. El listado de la CARDER registra a Ognorhynchus icterotis. No lo cojas ni lo desplaces.",
        "La ficha lo nombra entre las especies que estudia, y el listado trae a Ognorhynchus icterotis. No lo cojas ni lo desplaces.",
        ["pnn", "sib", "res"],
        ["loro orejiamarillo"],
    ),
    prose(
        "fauna.northern_pudu",
        "fact",
        "El parque estudia al venado conejo como especie vulnerable o indicadora. El listado de la CARDER registra a Pudu mephistophiles. Si ves un venado, no lo cojas ni lo desplaces.",
        "La ficha estudia al venado conejo, y el listado de la CARDER registra a Pudu mephistophiles. No cojas ni desplaces a un venado.",
        ["pnn", "sib", "res"],
        ["venado conejo", "pudu"],
    ),
    prose(
        "fauna.spotting_sector_brisas",
        "explanation",
        "En Brisas-Kumanday puedes realizar observación de fauna y flora o fotografía no comercial. No cojas ni desplaces a los animales que veas.",
        "Esa es la actividad de fauna que la ficha asigna a Brisas-Kumanday. Mira sin coger ni mover a los animales.",
        ["pnn", "res"],
        ["brisas", "observacion"],
    ),
    prose(
        "fauna.spotting_sector_otun",
        "explanation",
        "En Cisne-Poleka Kasue y en Otún puedes hacer observación de aves y observación de fauna y flora. La Laguna del Otún es la más grande del parque. No cojas ni desplaces a los animales.",
        "La ficha ofrece esas dos observaciones en Otún y dice que su laguna es la más grande del parque. No toques la fauna.",
        ["pnn", "res"],
        ["otun", "aves"],
    ),
    prose(
        "fauna.spotting_sector_santa_isabel",
        "explanation",
        "Desde el sector Cisne-Poleka Kasue ves el Nevado Santa Isabel (Poleka Kasue). Ahí puedes hacer observación de aves y de fauna y flora. No cojas ni desplaces a los animales.",
        "La ficha junta ese sector con la vista a Santa Isabel y con la observación de aves y de fauna. No toques a los animales.",
        ["pnn", "res"],
        ["santa isabel", "cisne"],
    ),
    prose(
        "fauna.injured_wildlife_protocol",
        "safety",
        "Si hallas un animal herido, no lo cojas, no lo alimentes y no lo desplaces: la Resolución 207 de 2023 pide evitar el contacto con la vida silvestre y dejarlo donde está.",
        "Aunque parezca herido, la Resolución 207 de 2023 manda no cogerlo, no alimentarlo y no sacarlo de donde está.",
        ["res"],
        ["herido", "contacto"],
    ),
]


def checklist_entries() -> list[dict]:
    rows = []
    singles = [
        ("fauna.fuertes_parrot", "fact", ["loro", "fuertes"]),
        ("fauna.golden_plumed_parakeet", "fact", ["perico"]),
        ("fauna.tawny_antpitta", "fact", ["tororoi"]),
        ("fauna.chestnut_naped_antpitta", "fact", ["tororoi"]),
        ("fauna.torrent_duck", "fact", ["pato"]),
        ("fauna.sword_billed_hummingbird", "fact", ["colibri"]),
        ("fauna.shining_sunbeam", "fact", ["colibri"]),
        ("fauna.tyrian_metaltail", "fact", ["colibri"]),
        ("fauna.white_capped_dipper", "fact", ["mirlo"]),
        ("fauna.great_thrush", "fact", ["mirlo"]),
        ("fauna.hooded_mountain_toucan", "fact", ["terlaque"]),
        ("fauna.rufous_collared_sparrow", "fact", ["copeton"]),
        ("fauna.short_eared_owl_paramo", "fact", ["buho"]),
        ("fauna.noble_snipe", "fact", ["agachadiza"]),
        ("fauna.northern_tiger_cat", "fact", ["tigrillo"]),
        ("fauna.mountain_paca", "fact", ["guagua"]),
        ("fauna.little_red_brocket", "fact", ["venado"]),
        ("fauna.white_tailed_deer", "fact", ["venado"]),
        ("fauna.mountain_coati", "fact", ["cusumbo"]),
        ("fauna.long_tailed_weasel", "fact", ["comadreja"]),
        ("fauna.paramo_rabbit", "fact", ["conejo"]),
        ("fauna.crab_eating_fox", "fact", ["zorro"]),
    ]
    for entry_id, kind, tags in singles:
        short, variant = listed(TAXA[entry_id])
        rows.append(prose(entry_id, kind, short, variant, ["sib", "res"], tags))
    for entry_id, names in GROUP_TAXA.items():
        short, variant = listed_many(names)
        rows.append(prose(entry_id, "fact", short, variant, ["sib", "res"], ["listado"]))
    return rows


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


def load_examples(entry_ids: list[str]) -> dict[str, list[str]]:
    frozen = json.loads(EXAMPLES.read_text(encoding="utf-8"))
    owned: dict[str, str] = {}
    for path in sorted(SECTIONS.glob("*.json")):
        if path.name == "fauna.json":
            continue
        for entry in json.loads(path.read_text(encoding="utf-8"))["entries"]:
            for example in entry["examples"]:
                owned[fold(example)] = entry["id"]
    result = {}
    extra_examples = ROUND2["examples"] if ROUND2 else {}
    extra_append = ROUND2["append"] if ROUND2 else {}
    for entry_id in entry_ids:
        if entry_id in extra_examples:
            examples = list(extra_examples[entry_id])
        else:
            examples = list(frozen[entry_id]["examples"])
        for old, new in REPLACEMENTS.get(entry_id, {}).items():
            if old not in examples:
                raise SystemExit(f"{entry_id}: example to replace was not found: {old}")
            examples[examples.index(old)] = new
        examples.extend(extra_append.get(entry_id, []))
        if len(examples) < 12:
            raise SystemExit(f"{entry_id}: only {len(examples)} examples")
        if len(set(examples)) != len(examples):
            raise SystemExit(f"{entry_id}: duplicate examples")
        slang = [ex for ex in examples if re.search(r"\b(parce|porfa)\b", ex, re.I)]
        if len(slang) > 1:
            raise SystemExit(f"{entry_id}: more than one parce/porfa example")
        for example in examples:
            key = fold(example)
            previous = owned.get(key)
            if previous:
                raise SystemExit(f"{entry_id}: example collides with {previous}: {example}")
            owned[key] = entry_id
        result[entry_id] = examples
    return result


def hard_negatives(entry_id: str, examples_by_id: dict[str, list[str]], order: list[str]) -> list[str]:
    own = set(examples_by_id[entry_id])
    picked = []
    start = order.index(entry_id)
    for step in range(1, len(order)):
        other = order[(start + step) % len(order)]
        for example in examples_by_id[other]:
            if example not in own and example not in picked:
                picked.append(example)
                break
        if len(picked) == 3:
            return picked
    raise SystemExit(f"{entry_id}: not enough hard negatives")


def labels_for(entry_id: str, frozen: dict) -> str:
    if entry_id in LABELS:
        label = LABELS[entry_id]
    else:
        label = frozen[entry_id]["label"]
    words = label.split()
    if not 3 <= len(words) <= 8:
        raise SystemExit(f"{entry_id}: label word count {len(words)}: {label}")
    return label


def write_quotes(taxon_text: str) -> None:
    lines = [
        "# Fauna quotes",
        "",
        "Access date for every item: 2026-11-21. Each quote is a verbatim substring of the raw file.",
        "",
    ]
    seen = set()
    for quote_id, url, filename, quote in QUOTES:
        lines += [
            f"## {quote_id}",
            f"url: {url}",
            f"retrieved: {DATE}",
            f"file: {filename}",
            f"quote: {quote}",
            "",
        ]
        seen.add(quote)
    names = sorted(set(TAXA.values()) | {name for group in GROUP_TAXA.values() for name in group})
    for name in names:
        if name not in taxon_text:
            raise SystemExit(f"taxon.txt is missing {name}")
        lines += [
            f"## taxon-{fold(name).replace(' ', '-')}",
            f"url: {SIB_URL}",
            f"retrieved: {DATE}",
            "file: raw/dwca/taxon.txt",
            f"quote: {name}",
            "",
        ]
    path = HERE / "evidence" / "quotes.md"
    path.write_text("\n".join(lines), encoding="utf-8")


def write_deletions() -> None:
    lines = [
        "# Entradas de fauna eliminadas el 2026-11-21",
        "",
        "No se reescribieron: no hay una frase en la ficha de PNN, en la Resolución 207 de 2023 ni en el listado Darwin Core de la CARDER que sostenga el tema.",
        "",
    ]
    for entry_id, reason in DELETED.items():
        lines.append(f"- `{entry_id}`: {reason}")
    lines += [
        "",
        "Round 2 (2026-11-21) no reactivó estos ids. Las entradas nuevas usan otros ids y fuentes descargadas después: plan de manejo 2017, Resolución 0126 de 2024 (lista SiB del Ministerio de Ambiente) y el estudio del Instituto Humboldt en el complejo de páramos.",
        "",
    ]
    (HERE / "deleted-ids.md").write_text("\n".join(lines), encoding="utf-8")


def answer_numbers_are_sourced(entries: list[dict]) -> None:
    corpus = []
    for filename in (
        "pnn_nevados.txt",
        "resolucion-207-2023.txt",
        "voc-page-2.txt",
        "dwca/taxon.txt",
        "dwca/eml.xml",
        "plan-manejo-2017.txt",
        "mads-amenazadas/eml.xml",
        "mads-amenazadas/taxon.txt",
        "mads-amenazadas/distribution.txt",
        "humboldt-nevados/eml.xml",
        "humboldt-nevados/occurrence.txt",
        "minambiente-resolucion-0126.html",
    ):
        corpus.append((RAW / filename).read_text(encoding="utf-8", errors="replace"))
    blob = "\n".join(corpus)
    for entry in entries:
        texts = [entry["answer"]["short"], *entry["answer"]["variants"]]
        for text in texts:
            for number in re.findall(r"\d+", text):
                if number not in blob:
                    raise SystemExit(f"{entry['id']}: number {number} is not in the raw files")


def build() -> dict:
    global ROUND2
    ROUND2 = round2_bundle(RAW)
    if not any(item[0] == "plan-2017" for item in QUOTES):
        QUOTES.extend(ROUND2["quotes"])
    LABELS.update(ROUND2["labels"])
    taxon_text = (RAW / "dwca" / "taxon.txt").read_text(encoding="utf-8")
    frozen = json.loads(EXAMPLES.read_text(encoding="utf-8"))
    records = ENTRIES + checklist_entries()
    by_id = {record["id"]: record for record in records}
    for entry_id, patch in ROUND2["overrides"].items():
        if entry_id not in by_id:
            raise SystemExit(f"override target missing: {entry_id}")
        by_id[entry_id].update(patch)
    records.extend(ROUND2["records"])
    order = [record["id"] for record in records]
    if len(order) != len(set(order)):
        raise SystemExit("duplicate entry id in the generator")
    missing_deleted = set(frozen) - set(order) - set(DELETED)
    if missing_deleted:
        raise SystemExit(f"ids neither kept nor deleted: {sorted(missing_deleted)}")
    extra_deleted = set(DELETED) & set(order)
    if extra_deleted:
        raise SystemExit(f"ids both kept and deleted: {sorted(extra_deleted)}")
    examples_by_id = load_examples(order)
    built = []
    for index, record in enumerate(records):
        entry_id = record["id"]
        short = record["short"]
        variant = record["variant"]
        if len(short) > 360:
            raise SystemExit(f"{entry_id}: short is {len(short)} chars")
        if not 1 <= short.count(".") <= 4:
            pass
        related = [order[(index + step) % len(order)] for step in (1, 2, 3)]
        built.append(
            {
                "id": entry_id,
                "label": labels_for(entry_id, frozen),
                "kind": record["kind"],
                "audience": "visitor",
                "lang": "es",
                "examples": examples_by_id[entry_id],
                "hard_negatives": hard_negatives(entry_id, examples_by_id, order),
                "needs": [],
                "answer": {"short": short, "variants": [variant]},
                "sources": source(*record["sources"]),
                "last_verified": DATE,
                "related": related,
                "tags": record["tags"],
            }
        )
    answer_numbers_are_sourced(built)
    write_quotes(taxon_text)
    write_deletions()
    return {
        "contract_version": 1,
        "id": "fauna",
        "order": 11,
        "title": "Fauna y vida silvestre",
        "description": "Animales que la ficha del parque, el listado de la CARDER, el plan de manejo y la lista nacional de especies amenazadas registran en Los Nevados o en su complejo de páramos, y cómo observarlos sin tocarlos.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.3,
            "top_k": 2,
            "min_score": None,
            "entity_filters": ["animal_group", "sector"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Buscas aves, mamíferos o una especie con nombre?",
                "¿Te interesa el cóndor, el chivito de páramo, el oso o la danta?",
                "¿Quieres saber qué especies nombra la ficha del parque?",
                "¿Vas a Brisas, a la Laguna del Otún o al sector de Santa Isabel?",
                "¿Encontraste un animal herido y quieres saber qué no debes hacer?",
                "¿Buscas la categoría de amenaza de una especie o los anfibios del complejo de páramos?",
            ],
            "slot_questions": {
                "animal_group": "¿Qué grupo buscas: aves, mamíferos u otra especie nombrada en la ficha?",
                "sector": "¿En qué sector vas: Brisas, Laguna del Otún o Santa Isabel?",
            },
            "fallback": "No tengo esa especie en la ficha, en el listado ni en la lista de amenaza que revisé. Puedo contarte del cóndor, el chivito de páramo, la danta, el oso, los anfibios del complejo de páramos o la observación de fauna en Brisas y en Otún.",
        },
        "featured": [
            "fauna.andean_condor",
            "fauna.spectacled_bear",
            "fauna.mountain_tapir",
            "fauna.buffy_helmetcrest",
            "fauna.birds_overview",
        ],
        "entries": built,
    }


def main() -> None:
    section = build()
    TARGET.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    examples = sum(len(entry["examples"]) for entry in section["entries"])
    print(f"wrote {TARGET}")
    print(f"entries {len(section['entries'])} examples {examples} deleted {len(DELETED)}")
    long = [f"{e['id']} {len(e['answer']['short'])}" for e in section["entries"] if len(e["answer"]["short"]) > 320]
    if long:
        print("over 320 chars:")
        for item in long:
            print(" ", item)


if __name__ == "__main__":
    main()
