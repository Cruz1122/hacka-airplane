"""Round-2 fauna entries. Every answer claim is a quote checked against raw files.

Threat categories come from the SiB publication of Resolución 0126 de 2024.
The taxon file and the distribution file share a taxon id: the name is in one
line and the category code is in the other. The category words are defined in
the dataset abstract.
"""

from __future__ import annotations

from pathlib import Path

PLAN_URL = "https://www.parquesnacionales.gov.co/wp-content/uploads/2020/10/plan-de-manejo-pnn-los-nevados.pdf"
MADS_URL = "https://doi.org/10.15472/frowz3"
MINAMB_URL = "https://www.minambiente.gov.co/documento-normativa/resolucion-0126-de-2024/"
HUMBOLDT_URL = "https://ipt.biodiversidad.co/iavh/resource?r=rrbb_nevados_faunaflora_2015"
DATE = "2026-11-21"

RAW_FILES = (
    "plan-manejo-2017.txt",
    "mads-amenazadas/eml.xml",
    "mads-amenazadas/taxon.txt",
    "mads-amenazadas/distribution.txt",
    "humboldt-nevados/eml.xml",
    "humboldt-nevados/occurrence.txt",
    "minambiente-resolucion-0126.html",
)


def _norm(text: str) -> str:
    return " ".join(text.split())


def _require(haystack: str, quote: str, label: str) -> str:
    needle = _norm(quote)
    if needle not in haystack:
        raise SystemExit(f"round2 quote missing ({label}): {needle[:160]}")
    return needle


def _status_examples(plain: str, common: str, scientific: str, hook: str, en1: str, en2: str) -> list[str]:
    return [
        f"{plain} esta amenazado?",
        f"qué categoría de amenaza tiene {common} en Colombia",
        hook,
        f"categoria de {plain} segun la resolucion 0126",
        en1,
        en2,
        f"en que categoria puso Minambiente a {common}",
        f"{scientific} esta en la lista de especies amenazadas",
        f"que tan grave es la situacion de {plain}",
        f"{common} esta vulnerable, en peligro o en peligro critico?",
        f"quiero saber la categoria nacional de {plain}",
        f"es cierto que {common} figura en la lista roja de Colombia",
    ]


def _group_examples(rows: list[str]) -> list[str]:
    if len(rows) != 12 or len(set(rows)) != 12:
        raise SystemExit(f"group examples must be 12 unique, got {len(rows)}")
    return rows


def bundle(raw: Path) -> dict:
    plan = _norm((raw / "plan-manejo-2017.txt").read_text(encoding="utf-8", errors="replace"))
    mads_eml = _norm((raw / "mads-amenazadas" / "eml.xml").read_text(encoding="utf-8", errors="replace"))
    taxon = _norm((raw / "mads-amenazadas" / "taxon.txt").read_text(encoding="utf-8", errors="replace"))
    dist = _norm((raw / "mads-amenazadas" / "distribution.txt").read_text(encoding="utf-8", errors="replace"))
    hum_eml = _norm((raw / "humboldt-nevados" / "eml.xml").read_text(encoding="utf-8", errors="replace"))
    occ = _norm((raw / "humboldt-nevados" / "occurrence.txt").read_text(encoding="utf-8", errors="replace"))
    minamb = _norm((raw / "minambiente-resolucion-0126.html").read_text(encoding="utf-8", errors="replace"))

    quotes: list[tuple[str, str, str, str]] = []

    def add(quote_id: str, url: str, filename: str, quote: str, haystack: str) -> None:
        quotes.append((quote_id, url, filename, _require(haystack, quote, quote_id)))

    add(
        "minamb-0126-title",
        MINAMB_URL,
        "raw/minambiente-resolucion-0126.html",
        "Resolución 0126 de 2024",
        minamb,
    )
    add(
        "minamb-0126-object",
        MINAMB_URL,
        "raw/minambiente-resolucion-0126.html",
        "listado oficial de las especies silvestres amenazadas de la diversidad biológica colombiana continental y marino costera",
        minamb,
    )
    add(
        "mads-def-cr",
        MADS_URL,
        "raw/mads-amenazadas/eml.xml",
        "1. En Peligro Crítico (CR): Aquellas que están enfrentando un riesgo de extinción extremadamente alto en estado de vida silvestre.",
        mads_eml,
    )
    add(
        "mads-def-en",
        MADS_URL,
        "raw/mads-amenazadas/eml.xml",
        "2. En Peligro (EN): Aquellas que están enfrentando un riesgo de extinción muy alto en estado de vida silvestre.",
        mads_eml,
    )
    add(
        "mads-def-vu",
        MADS_URL,
        "raw/mads-amenazadas/eml.xml",
        "3. Vulnerable (VU): Aquellas que están enfrentando un riesgo de extinción alto en estado de vida silvestre.",
        mads_eml,
    )
    add(
        "mads-title",
        MADS_URL,
        "raw/mads-amenazadas/eml.xml",
        "Resolución 0126 de 2024 expedida por el Ministerio de Ambiente y Desarrollo Sostenible",
        mads_eml,
    )

    wanted = {
        "Vultur gryphus": "CR",
        "Tremarctos ornatus": "VU",
        "Tapirus pinchaque": "EN",
        "Spizaetus isidori": "EN",
        "Oxypogon stubelii": "EN",
        "Hapalopsittaca fuertesi": "CR",
        "Ognorhynchus icterotis": "EN",
        "Grallaria milleri": "EN",
        "Bolborhynchus ferrugineifrons": "VU",
        "Oxyura jamaicensis": "EN",
        "Pudu mephistophiles": "EN",
        "Dinomys branickii": "VU",
        "Leopardus tigrinus": "VU",
        "Mazama rufina": "VU",
        "Leptosittaca branickii": "VU",
        "Andigena hypoglauca": "VU",
        "Osornophryne percrassa": "VU",
        "Pristimantis racemus": "VU",
    }
    taxon_lines = (raw / "mads-amenazadas" / "taxon.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    dist_lines = (raw / "mads-amenazadas" / "distribution.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    dist_by_id = {}
    for line in dist_lines[1:]:
        parts = line.split("\t")
        if len(parts) >= 3:
            dist_by_id[parts[0]] = parts[2]
    for line in taxon_lines[1:]:
        parts = line.split("\t")
        if len(parts) < 3 or parts[2] not in wanted:
            continue
        scientific = parts[2]
        taxon_id = parts[0]
        status = dist_by_id.get(taxon_id)
        if status != wanted[scientific]:
            raise SystemExit(f"{scientific}: expected {wanted[scientific]}, file has {status}")
        slug = scientific.lower().replace(" ", "-")
        add(
            f"mads-taxon-{slug}",
            MADS_URL,
            "raw/mads-amenazadas/taxon.txt",
            _norm(line),
            taxon,
        )
        add(
            f"mads-dist-{slug}",
            MADS_URL,
            "raw/mads-amenazadas/distribution.txt",
            f"{taxon_id} CO {status}",
            dist,
        )

    add(
        "plan-2017",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "PLAN DE MANEJO 2017",
        plan,
    )
    add(
        "plan-birders",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Se destaca para el caso del PNN Los Nevados la vistancia de observadores de aves que desean visualizar particularmente el cóndor de los Andes (Vultur gryphus), el chivito de páramo (Oxypogon stubelii) y el pato andino (Oxyura jamaicensis), entre otras.",
        plan,
    )
    add(
        "plan-herp-little",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Es poco lo que se conoce de la herpetofauna en el PNN Los Nevados",
        plan,
    )
    add(
        "plan-reptiles-least",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "En reptiles son el grupo de vertebrados con menor riqueza en el páramo.",
        plan,
    )
    add(
        "plan-table-buffer",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Tabla 20. Biodiversidad y endemismo en Parque Nacional Natural Los Nevados y su Zona Amortiguadora",
        plan,
    )
    add(
        "plan-reptiles-nine",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Reptiles 506 9",
        plan,
    )
    add(
        "plan-parakeet-subparamo",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "los censos indican que la es especie más abundante en las zonas de subpáramo",
        plan,
    )
    add(
        "plan-parakeet-flocks",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "bandadas bullosas de 10 \u2013 15 individuos, sin embargo en zonas cercanas a la laguna del Otún también es frecuente observar bandadas más pequeñas, incluso parejas e individuos solitarios, y más grandes entre 30 y 40 individuos.",
        plan,
    )
    add(
        "plan-duck-national",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "el pato andino (Oxyura jamaicensis) se encuentran categorizada en preocupación menor y a nivel nacional en peligro",
        plan,
    )
    add(
        "plan-duck-move",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "En el PNN Los Nevados, se ha encontrado que los individuos de esta especie se mueven entre la Laguna del Otún y otros humedales para alimentarse y reproducirse",
        plan,
    )
    add(
        "plan-deer-gone",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "como es el caso del venado de cola blanca (Odocoileus virginianus) en el PNN Los Nevados (Botero y Lotero 2004).",
        plan,
    )
    add(
        "plan-visible-1",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "entre las especies más llamativas que se pueden observar en el PNN Los Nevados se encuentra la Danta de Páramo (Tapirus pinchaque), el Venado colorado (Mazama rufina), el conejo de paramo",
        plan,
    )
    add(
        "plan-visible-2",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "(Sylvilagus brasiliensis) la Boruga (Cuniculus taczanowiski), el venado conejo (Pudume phistophiles), el Puma o León de montaña (Puma concolor), el Tigrillo (Leopardus tigrinus)",
        plan,
    )
    add(
        "plan-epi",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "3. Vultur gryphus (Cóndor Andino) 4. Leptosittaca branickii (Perico paramuno) 5. Andigena hypoglauca (Terlaque andino) 6. Ognorhynchus icterotis (Loro orejiamarillo) 7. Oxypogon stubelli (Chivito de páramo) 8. Hapalopsittaca fuertesi (Cotorra) 9. Tapirus pinchaque (Danta de páramo) 10. Pudu mephistophiles (Venado conejo) 11. Mazama rufina (Venado colorado) 12. Puma concolor (Puma) 13. Tremarctos ornatus (oso de anteojos)",
        plan,
    )
    add(
        "plan-condor-2017",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "a nivel nacional el cóndor es categorizado en peligro y el terlaque como vulnerable",
        plan,
    )
    add(
        "plan-pudu-2017",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Pudu mephistophiles VU Vulnerable NT Casi amenazada",
        plan,
    )
    add(
        "plan-tapir-2017",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "la danta de páramo (Tapirus pinchaque) se encuentra categorizada en peligro",
        plan,
    )
    add(
        "plan-toucan-2017",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Andigena hypoglauca NT Casi amenazada VU Vulnerable",
        plan,
    )
    add(
        "plan-parakeet-vu",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Bolborhynchus ferrugineifrons VU Vulnerable VU Vulnerable",
        plan,
    )
    add(
        "plan-endemic-count",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "el área cuenta con un total de especies endémicas y casi-endémicas de 30 especies. Se cuenta con 8 especies de aves endémicas",
        plan,
    )
    add(
        "plan-endemic-22",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "22 más de distribución compartida",
        plan,
    )
    add(
        "plan-adjacent",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "reportadas para el Parque Nacional Natural Los Nevados y su Zona Adyacente",
        plan,
    )
    add(
        "plan-mesofauna",
        PLAN_URL,
        "raw/plan-manejo-2017.txt",
        "Gran parte de la mesofauna del suelo paramuno aún es desconocida para la ciencia",
        plan,
    )
    add(
        "hum-six-amphibians",
        HUMBOLDT_URL,
        "raw/humboldt-nevados/eml.xml",
        "361 para 6 especies de anfibios",
        hum_eml,
    )
    add(
        "hum-beetles-spiders",
        HUMBOLDT_URL,
        "raw/humboldt-nevados/eml.xml",
        "edafofauna epigea (coleópteros y arañas)",
        hum_eml,
    )
    add(
        "hum-sites",
        HUMBOLDT_URL,
        "raw/humboldt-nevados/eml.xml",
        "Los muestreos de vertebrados se llevaron a cabo en las localidades de la Reserva Forestal Protectora Río Blanco, en Manizales, en Santa Rosa de Cabal, Anzoátegui y Murillo.",
        hum_eml,
    )
    add(
        "hum-dates",
        HUMBOLDT_URL,
        "raw/humboldt-nevados/eml.xml",
        "La fase de registro de información en campo se llevó a cabo entre los meses de marzo y julio de 2014.",
        hum_eml,
    )
    add(
        "hum-complex",
        HUMBOLDT_URL,
        "raw/humboldt-nevados/eml.xml",
        "El área de estudio se ubicó en el complejo de páramos Los Nevados",
        hum_eml,
    )
    for name in (
        "Pristimantis simoterus",
        "Pristimantis uranobates",
        "Pristimantis leptolophus",
        "Pristimantis peraticus",
        "Pristimantis racemus",
        "Osornophryne percrassa",
        "Staphylinidae",
        "Carabidae",
        "Linyphiidae",
    ):
        add(
            f"hum-name-{name.lower()}",
            HUMBOLDT_URL,
            "raw/humboldt-nevados/occurrence.txt",
            name,
            occ,
        )

    touch = "No lo cojas ni lo desplaces."
    records = []
    examples: dict[str, list[str]] = {}
    labels: dict[str, str] = {}

    def add_record(entry_id: str, kind: str, label: str, short: str, variant: str, sources: list[str], tags: list[str], rows: list[str]) -> None:
        if not 3 <= len(label.split()) <= 8:
            raise SystemExit(f"{entry_id}: label words {len(label.split())}: {label}")
        if len(short) > 320:
            raise SystemExit(f"{entry_id}: short is {len(short)} chars")
        if len(variant) > 360:
            raise SystemExit(f"{entry_id}: variant is {len(variant)} chars")
        records.append(
            {
                "id": entry_id,
                "kind": kind,
                "short": short,
                "variant": variant,
                "sources": sources,
                "tags": tags,
            }
        )
        labels[entry_id] = label
        examples[entry_id] = rows

    statuses = [
        (
            "fauna.condor_national_status",
            "cóndor andino en peligro crítico",
            "La Resolución 0126 de 2024 cataloga al cóndor de los Andes (Vultur gryphus) como En Peligro Crítico. El plan de 2017 lo tenía En Peligro a nivel nacional. Puede cambiar; confírmala en Minambiente. Si lo ves, no lo cojas ni lo desplaces.",
            "En la lista oficial de 2024 el cóndor está En Peligro Crítico; el plan de 2017 decía En Peligro a nivel nacional. Confírmala en Minambiente y no lo cojas ni lo desplaces.",
            ["minamb", "mads", "plan", "res"],
            ["condor", "CR"],
            _status_examples(
                "el condor andino",
                "el cóndor de los Andes",
                "Vultur gryphus",
                "el condor del nevado ya quedo en peligro critico?",
                "is the Andean condor critically endangered in Colombia",
                "what threat category does Colombia give the Andean condor",
            ),
        ),
        (
            "fauna.bear_national_status",
            "oso de anteojos vulnerable en Colombia",
            "La Resolución 0126 de 2024 cataloga al oso de anteojos (Tremarctos ornatus) como Vulnerable. Puede cambiar; confírmala en Minambiente. Si ves uno, no lo cojas, no lo alimentes y no lo desplaces.",
            "El oso de anteojos figura como Vulnerable en la lista oficial de 2024. Confírmala en Minambiente y no lo cojas ni lo alimentes.",
            ["minamb", "mads", "res"],
            ["oso", "VU"],
            _status_examples(
                "el oso de anteojos",
                "el oso andino",
                "Tremarctos ornatus",
                "el oso del paramo esta vulnerable o peor?",
                "is the spectacled bear listed as Vulnerable in Colombia",
                "what is the national status of the Andean bear",
            ),
        ),
        (
            "fauna.tapir_national_status",
            "danta de páramo catalogada en peligro",
            "La Resolución 0126 de 2024 y el plan de manejo catalogan a la danta de páramo (Tapirus pinchaque) como En Peligro. Puede cambiar; confírmala en Minambiente. Si ves una, no la cojas ni la desplaces.",
            "Danta de páramo y danta de montaña son el mismo nombre en esa lista: En Peligro. Confírmala en Minambiente y no la cojas.",
            ["minamb", "mads", "plan", "res"],
            ["danta", "EN"],
            _status_examples(
                "la danta de paramo",
                "la danta de montaña",
                "Tapirus pinchaque",
                "la danta del parque esta en peligro de extincion?",
                "is the mountain tapir endangered in Colombia",
                "what threat category does the mountain tapir have",
            ),
        ),
        (
            "fauna.helmetcrest_national_status",
            "chivito de páramo en la lista nacional",
            "La Resolución 0126 de 2024 cataloga a Oxypogon stubelii, chivito de páramo, como En Peligro. La ficha del parque escribe Oxypogon stuebelii. Puede cambiar; confírmala en Minambiente. No lo cojas ni lo desplaces.",
            "La lista de 2024 escribe stubelii y lo pone En Peligro; la ficha escribe stuebelii. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "pnn", "res"],
            ["chivito", "EN"],
            _status_examples(
                "el chivito de paramo",
                "el chivito de páramo",
                "Oxypogon stubelii",
                "el colibri de frailejon esta en peligro?",
                "is the Buffy helmetcrest endangered in Colombia",
                "what is the national status of Oxypogon stubelii",
            ),
        ),
        (
            "fauna.eagle_national_status",
            "águila crestada catalogada en peligro",
            "La Resolución 0126 de 2024 cataloga al águila crestada (Spizaetus isidori) como En Peligro. Puede cambiar; confírmala en Minambiente. Si la ves, no la cojas ni la desplaces.",
            "El águila crestada está En Peligro en la lista oficial de 2024. Confírmala en Minambiente y no la cojas.",
            ["minamb", "mads", "res"],
            ["aguila", "EN"],
            _status_examples(
                "el aguila crestada",
                "el águila crestada",
                "Spizaetus isidori",
                "la rapaz grande del parque esta en peligro?",
                "is the black-and-chestnut eagle endangered in Colombia",
                "what threat category does Spizaetus isidori have",
            ),
        ),
        (
            "fauna.fuertes_national_status",
            "cotorra de Fuertes en peligro crítico",
            "La Resolución 0126 de 2024 cataloga a la cotorra de Fuertes (Hapalopsittaca fuertesi) como En Peligro Crítico. Puede cambiar; confírmala en Minambiente. No la cojas ni la desplaces.",
            "Hapalopsittaca fuertesi, también llamada cotorra coroniazul en esa lista, está En Peligro Crítico. Confírmala en Minambiente y no la cojas.",
            ["minamb", "mads", "res"],
            ["fuertes", "CR"],
            _status_examples(
                "la cotorra de fuertes",
                "la cotorra coroniazul",
                "Hapalopsittaca fuertesi",
                "la lora de fuertes esta en peligro critico?",
                "is Fuertes's parrot critically endangered in Colombia",
                "what is the national status of Hapalopsittaca fuertesi",
            ),
        ),
        (
            "fauna.yellow_eared_national_status",
            "loro orejiamarillo en la lista nacional",
            "El parque estudia al loro orejiamarillo. La Resolución 0126 de 2024 cataloga a Ognorhynchus icterotis, con el nombre Perico Palmero, como En Peligro. Puede cambiar; confírmala en Minambiente. No lo cojas ni lo desplaces.",
            "Loro orejiamarillo en la ficha y Perico Palmero en la lista de 2024 son Ognorhynchus icterotis, En Peligro. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "pnn", "res"],
            ["orejiamarillo", "EN"],
            _status_examples(
                "el loro orejiamarillo",
                "el perico palmero",
                "Ognorhynchus icterotis",
                "el loro de orejas amarillas esta en peligro?",
                "is the yellow-eared parrot endangered in Colombia",
                "what threat category does Ognorhynchus icterotis have",
            ),
        ),
        (
            "fauna.miller_national_status",
            "tororoi de Miller catalogado en peligro",
            "La Resolución 0126 de 2024 cataloga al tororoi de Miller (Grallaria milleri) como En Peligro. Puede cambiar; confírmala en Minambiente. No lo cojas ni lo desplaces.",
            "Grallaria milleri está En Peligro en la lista oficial de 2024. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "res"],
            ["miller", "EN"],
            _status_examples(
                "el tororoi de miller",
                "el tororoi de Miller",
                "Grallaria milleri",
                "el pajaro de miller esta en peligro?",
                "is the brown-banded antpitta endangered in Colombia",
                "what is the national status of Grallaria milleri",
            ),
        ),
        (
            "fauna.pudu_national_status",
            "venado conejo en la lista de amenaza",
            "La Resolución 0126 de 2024 cataloga a Pudu mephistophiles como En Peligro. El plan de 2017 lo tenía Casi amenazado a nivel nacional. Puede cambiar; confírmala en Minambiente. Si ves un venado, no lo cojas ni lo desplaces.",
            "El venado conejo pasó, en las fuentes, de Casi amenazado en el plan de 2017 a En Peligro en la lista de 2024. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "plan", "res"],
            ["pudu", "EN"],
            _status_examples(
                "el venado conejo",
                "el pudú",
                "Pudu mephistophiles",
                "el venadito pequeno esta en peligro o solo casi amenazado?",
                "is the northern pudu endangered in Colombia",
                "what threat category does Pudu mephistophiles have now",
            ),
        ),
        (
            "fauna.guagua_national_status",
            "guagua loba vulnerable en Colombia",
            "La Resolución 0126 de 2024 cataloga a la guagua loba (Dinomys branickii) como Vulnerable. Puede cambiar; confírmala en Minambiente. Si la ves, no la cojas ni la desplaces.",
            "Dinomys branickii está Vulnerable en la lista oficial de 2024. Confírmala en Minambiente y no la cojas.",
            ["minamb", "mads", "res"],
            ["guagua", "VU"],
            _status_examples(
                "la guagua loba",
                "la pacarana",
                "Dinomys branickii",
                "la guagua grande del parque esta vulnerable?",
                "is the pacarana listed as Vulnerable in Colombia",
                "what is the national status of Dinomys branickii",
            ),
        ),
        (
            "fauna.oncilla_national_status",
            "tigrillo lanudo en la lista nacional",
            "La Resolución 0126 de 2024 cataloga al tigrillo (Leopardus tigrinus) como Vulnerable. Puede cambiar; confírmala en Minambiente. Si lo ves, no lo cojas ni lo desplaces.",
            "Leopardus tigrinus está Vulnerable en la lista oficial de 2024. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "res"],
            ["tigrillo", "VU"],
            _status_examples(
                "el tigrillo lanudo",
                "la oncilla",
                "Leopardus tigrinus",
                "el gato manchado del paramo esta vulnerable?",
                "is the oncilla listed as Vulnerable in Colombia",
                "what threat category does Leopardus tigrinus have",
            ),
        ),
        (
            "fauna.brocket_national_status",
            "venado colorado vulnerable en Colombia",
            "La Resolución 0126 de 2024 cataloga a Mazama rufina, el venado colorado del plan de manejo, como Vulnerable. Puede cambiar; confírmala en Minambiente. Si ves un venado, no lo cojas ni lo desplaces.",
            "El venado colorado (Mazama rufina) está Vulnerable en la lista de 2024. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "plan", "res"],
            ["venado", "VU"],
            _status_examples(
                "el venado colorado",
                "el venado soche",
                "Mazama rufina",
                "el venado rojizo del paramo esta vulnerable?",
                "is the little red brocket listed as Vulnerable in Colombia",
                "what is the national status of Mazama rufina",
            ),
        ),
        (
            "fauna.paramo_parakeet_national_status",
            "perico paramuno vulnerable en Colombia",
            "La Resolución 0126 de 2024 cataloga al perico paramuno (Leptosittaca branickii) como Vulnerable, igual que el plan de manejo. Puede cambiar; confírmala en Minambiente. No lo cojas ni lo desplaces.",
            "Leptosittaca branickii está Vulnerable en la lista de 2024 y en el plan de 2017. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "plan", "res"],
            ["perico", "VU"],
            _status_examples(
                "el perico paramuno",
                "el perico de frente dorada",
                "Leptosittaca branickii",
                "el perico de pluma dorada esta vulnerable?",
                "is the golden-plumed parakeet Vulnerable in Colombia",
                "what threat category does Leptosittaca branickii have",
            ),
        ),
        (
            "fauna.toucan_national_status",
            "terlaque andino vulnerable en Colombia",
            "La Resolución 0126 de 2024 cataloga al terlaque andino (Andigena hypoglauca) como Vulnerable. El plan de 2017 también lo tenía Vulnerable a nivel nacional. Puede cambiar; confírmala en Minambiente. No lo cojas ni lo desplaces.",
            "Andigena hypoglauca está Vulnerable en la lista de 2024 y así lo tenía el plan a nivel nacional. Confírmala en Minambiente y no lo cojas.",
            ["minamb", "mads", "plan", "res"],
            ["terlaque", "VU"],
            _status_examples(
                "el terlaque andino",
                "el tucán de montaña",
                "Andigena hypoglauca",
                "el pajaro de pico pintado esta vulnerable?",
                "is the hooded mountain toucan Vulnerable in Colombia",
                "what is the national status of Andigena hypoglauca",
            ),
        ),
    ]
    for entry_id, label, short, variant, sources, tags, rows in statuses:
        add_record(entry_id, "fact", label, short, variant, sources, tags, rows)

    add_record(
        "fauna.paramo_amphibians",
        "fact",
        "anfibios del complejo de páramos",
        "El Humboldt registró en el complejo de páramos Los Nevados a Pristimantis simoterus, Pristimantis uranobates, Pristimantis leptolophus, Pristimantis peraticus, Pristimantis racemus y Osornophryne percrassa (6 especies). Vulnerables en 2024: Osornophryne percrassa y Pristimantis racemus. No las cojas ni las desplaces.",
        "Son ranas del complejo de páramos, no una promesa de verlas en el sendero. Dos están Vulnerables en la lista de 2024. No las cojas ni las desplaces.",
        ["humboldt", "minamb", "mads", "res"],
        ["anfibios"],
        _group_examples(
            [
                "hay ranas en el paramo de los nevados?",
                "qué anfibios registró el Humboldt en el complejo de páramos Los Nevados",
                "salió un sapito en el pajonal, cuál puede ser",
                "pristimantis del complejo los nevados",
                "which frogs were recorded in the Los Nevados páramo complex",
                "are there amphibians around Los Nevados",
                "osornophryne percrassa esta en el paramo?",
                "el sapito rechoncho del nevado esta vulnerable?",
                "que ranas hay entre el bosque y el paramo de los nevados",
                "vi una rana pequena en la montaña, está en el listado?",
                "anfibios registrados por el instituto humboldt en los nevados",
                "pristimantis racemus es vulnerable?",
            ]
        ),
    )
    add_record(
        "fauna.amphibian_survey_sites",
        "explanation",
        "dónde buscaron anfibios del páramo",
        "Esos anfibios se buscaron en la Reserva Río Blanco (Manizales), Santa Rosa de Cabal, Anzoátegui y Murillo, entre marzo y julio de 2014. El plan de manejo dice que dentro del parque se conoce poco de la herpetofauna. No cojas ni desplaces ranas ni sapos.",
        "El muestreo fue en la transición bosque-páramo de esos cuatro sitios, no un mapa de avistamiento para el visitante. Dentro del área protegida el plan dice que se conoce poco. No las cojas.",
        ["humboldt", "plan", "res"],
        ["anfibios", "sitios"],
        _group_examples(
            [
                "donde buscaron las ranas del paramo",
                "en qué sitios muestreó el Humboldt los anfibios del complejo Los Nevados",
                "las ranas esas se ven en Brisas o fue en otro lado",
                "rio blanco santa rosa anzoategui murillo ranas",
                "where did they survey frogs around Los Nevados",
                "were the amphibian surveys inside the tourist trails",
                "el estudio de anfibios fue en 2014?",
                "se conoce poco de ranas dentro del parque?",
                "hay garantia de ver sapos en el sendero",
                "el plan dice que falta investigar la herpetofauna?",
                "anfibios en murillo y anzoategui",
                "por que no me prometen ver ranas en el otun",
            ]
        ),
    )
    add_record(
        "fauna.reptiles_paramo_buffer",
        "fact",
        "reptiles del páramo y la zona amortiguadora",
        "El plan de manejo dice que los reptiles son el grupo de vertebrados con menor riqueza en el páramo. Para el parque y su zona amortiguadora la tabla reporta 9 reptiles, y no trae una lista de especies para el visitante. No cojas ni desplaces reptiles.",
        "Hay un conteo viejo de 9 reptiles para el parque más la zona amortiguadora, sin nombres que puedas usar en el sendero. No cojas ni desplaces reptiles.",
        ["plan", "res"],
        ["reptiles"],
        _group_examples(
            [
                "hay lagartijas en el paramo de los nevados?",
                "cuántos reptiles reporta el plan para el parque y la zona amortiguadora",
                "vi un lagarto entre los frailejones, que hago",
                "hay serpientes en los nevados",
                "are there reptiles in Los Nevados",
                "does the management plan name the lizards",
                "el plan tiene lista de reptiles para el visitante?",
                "por que dicen que hay pocos reptiles en el paramo",
                "nueve reptiles incluyen la zona amortiguadora?",
                "puedo coger una lagartija para la foto",
                "reptiles del pnn los nevados y la zona amortiguadora",
                "el parque publico los nombres de las lagartijas?",
            ]
        ),
    )
    add_record(
        "fauna.epigeal_beetles_spiders",
        "fact",
        "escarabajos y arañas del suelo paramuno",
        "En el complejo de páramos Los Nevados el estudio del Humboldt registró coleópteros y arañas de la edafofauna; entre las familias están Staphylinidae, Carabidae y Linyphiidae. El plan dice que gran parte de la mesofauna del suelo paramuno aún es desconocida. No cojas ni desplaces invertebrados.",
        "Hay coleópteros y arañas registrados en el suelo del complejo de páramos, y el plan admite que falta mucho por conocer. No los cojas ni los desplaces.",
        ["humboldt", "plan", "res"],
        ["insectos", "aranas"],
        _group_examples(
            [
                "hay insectos en el paramo de los nevados?",
                "qué bichos del suelo registró el Humboldt en el complejo de páramos",
                "vi un escarabajo en el frailejon, lo dejo quieto?",
                "hay aranas en el pajonal",
                "were beetles and spiders recorded in the Los Nevados páramo",
                "is the soil fauna of the páramo well known",
                "staphylinidae y carabidae salen en el estudio?",
                "el plan dice que la mesofauna del suelo es desconocida?",
                "que invertebrados hay en el complejo de paramos",
                "puedo recoger un insecto del sendero",
                "coleopteros y aranas del paramo los nevados",
                "linyphiidae es una arana del estudio del humboldt?",
            ]
        ),
    )
    add_record(
        "fauna.priority_research_fauna",
        "fact",
        "especies de fauna prioritarias para investigar",
        "El plan de manejo prioriza para investigación al cóndor, el perico paramuno, el terlaque, el loro orejiamarillo, el chivito de páramo, la cotorra de Fuertes, la danta, el venado conejo, el venado colorado, el puma y el oso de anteojos. No los cojas ni los desplaces.",
        "Esas especies están en el listado de prioridad de investigación del plan, aparte de los valores objeto de conservación. No las cojas ni las desplaces.",
        ["plan", "res"],
        ["investigacion"],
        _group_examples(
            [
                "que animales prioriza el parque para investigar",
                "cuáles son las especies de fauna prioritarias del plan de manejo",
                "el condor es prioridad de investigacion del parque?",
                "lista epi de fauna de los nevados",
                "which animals does the park prioritize for research",
                "is the spectacled bear a research priority in the management plan",
                "el oso y la danta estan en las prioridades de investigacion?",
                "que especies quiere estudiar el parque",
                "la cotorra de fuertes es prioridad de investigacion?",
                "el chivito tambien esta en esa lista de investigacion?",
                "especies prioritarias de fauna del plan 2017",
                "el puma esta entre las prioridades de estudio del parque?",
            ]
        ),
    )
    add_record(
        "fauna.mammals_plan_says_visible",
        "explanation",
        "mamíferos llamativos que se pueden observar",
        "El plan de manejo dice que entre lo más llamativo que se puede observar en el parque están la danta de páramo, el venado colorado, el conejo, la boruga, el venado conejo, el puma y el tigrillo. No promete que los veas. No los cojas ni los desplaces.",
        "El plan los nombra como especies llamativas que se pueden observar, sin horario ni sendero fijo. Si aparece uno, no lo cojas ni lo desplaces.",
        ["plan", "res"],
        ["mamiferos", "observacion"],
        _group_examples(
            [
                "que mamiferos se pueden ver en el parque",
                "cuáles son los mamíferos llamativos que el plan dice que se pueden observar",
                "es verdad que se puede ver danta o puma",
                "animales grandes que el plan menciona como observables",
                "which large mammals does the management plan say you may see",
                "can I expect to see a tapir or a puma",
                "el plan habla de ver conejo boruga y tigrillo?",
                "hay chance de ver venado colorado",
                "el parque garantiza avistar puma?",
                "mamiferos llamativos del pnn los nevados",
                "la boruga esta entre los que se pueden observar?",
                "ver fauna grande en los nevados es seguro que pase?",
            ]
        ),
    )
    add_record(
        "fauna.birders_target_species",
        "explanation",
        "aves que buscan los observadores",
        "El plan de manejo destaca que hay observadores de aves que visitan el parque para ver en particular el cóndor andino, el chivito de páramo y el pato andino. Pregunta por la observación de aves y no las cojas ni las desplaces.",
        "Esas tres son las que el plan señala como el interés de quienes vienen a observar aves. Pregunta por esa actividad y no las toques.",
        ["plan", "res"],
        ["aves", "observadores"],
        _group_examples(
            [
                "que aves vienen a buscar los pajareros",
                "por qué especies de aves visitan los observadores el parque",
                "vengo a pajarear, que buscan aqui",
                "los observadores vienen por el condor?",
                "which birds do birders hope to see at Los Nevados",
                "do people visit to look for the condor and the duck",
                "el chivito de paramo es de los que buscan los pajareros?",
                "observacion de aves que especies nombra el plan",
                "quiero ver condor chivito y pato",
                "el plan dice que hay visitancia de observadores de aves?",
                "que trio de aves destaca el plan para los pajareros",
                "birding targets in los nevados according to the park plan",
            ]
        ),
    )
    add_record(
        "fauna.endemic_birds_plan_count",
        "fact",
        "aves endémicas del parque y la zona adyacente",
        "El plan de manejo de 2017 cuenta 30 aves endémicas o casi endémicas para el parque y su zona adyacente: 8 de Colombia y 22 compartidas. La ficha vigente solo llama endémicos al chivito de páramo y al tororoi de Miller. No las cojas ni las desplaces.",
        "Ese conteo de 30 incluye la zona adyacente y es del plan de 2017. La ficha actual solo marca como endémicos al chivito y al tororoi de Miller. No las cojas.",
        ["plan", "pnn", "res"],
        ["endemismo", "aves"],
        _group_examples(
            [
                "cuantas aves endemicas tiene el parque",
                "el plan cuántas aves endémicas y casi endémicas cuenta con la zona adyacente",
                "son 30 endemicas solo dentro del parque o con el borde",
                "la ficha solo llama endemicos al chivito y al tororoi?",
                "how many endemic birds does the 2017 plan count",
                "does the current fact sheet list only two endemic birds",
                "ocho aves endemicas de colombia segun el plan",
                "veintidos aves compartidas con otros paises?",
                "el numero 30 incluye la zona adyacente?",
                "no me cuentes endemicas de la ficha y del plan como si fueran iguales",
                "aves endemicas del plan de manejo 2017",
                "el chivito y el tororoi de miller son los endemicos de la ficha?",
            ]
        ),
    )

    overrides = {
        "fauna.ruiz_parakeet": {
            "short": "El plan de manejo dice que el periquito de los Nevados es más abundante en el subpáramo y que suele verse en bandadas de 10 a 15; cerca de la Laguna del Otún también hay parejas y bandadas de 30 a 40. La Resolución 0126 de 2024 lo cataloga Vulnerable. No lo cojas ni lo desplaces.",
            "variant": "Es más fácil verlo en el subpáramo, en bandadas, y junto a la Laguna del Otún también en parejas o grupos grandes. En la lista de 2024 está Vulnerable. No lo cojas ni lo desplaces.",
            "sources": ["plan", "minamb", "mads", "res"],
        },
        "fauna.andean_duck": {
            "short": "La ficha lo llama pato andino (Oxyura ferruginea). El plan de manejo usa Oxyura jamaicensis, en peligro a nivel nacional, y dice que en el parque se mueve entre la Laguna del Otún y otros humedales. No lo cojas ni lo desplaces.",
            "variant": "Ficha y plan no escriben el mismo nombre científico. El plan lo da por en peligro a nivel nacional y lo ubica entre la Laguna del Otún y otros humedales. No lo cojas.",
            "sources": ["pnn", "plan", "minamb", "mads", "res"],
        },
        "fauna.white_tailed_deer": {
            "short": "El listado de la CARDER registra a Odocoileus virginianus. El plan de manejo de 2017 dice que el venado de cola blanca desapareció del PNN Los Nevados. Si ves un venado, no lo cojas ni lo desplaces.",
            "variant": "Hay dos fuentes: el listado todavía lo trae y el plan de 2017 dice que desapareció del parque. Si ves un venado, no lo cojas ni lo desplaces.",
            "sources": ["sib", "plan", "res"],
        },
    }
    for entry_id, patch in overrides.items():
        if len(patch["short"]) > 320:
            raise SystemExit(f"{entry_id}: short is {len(patch['short'])} chars")

    append = {
        "fauna.ruiz_parakeet": [
            "el periquito de los nevados se ve en bandadas",
            "hay bandadas del periquito cerca de la laguna del otun",
            "where do the rufous-fronted parakeet flocks show up",
        ],
        "fauna.andean_duck": [
            "el pato andino se mueve entre la laguna del otun y otros humedales",
            "la ficha y el plan no usan el mismo nombre del pato",
            "does the Andean duck move between Otún and other wetlands",
        ],
        "fauna.white_tailed_deer": [
            "el venado cola blanca desaparecio del parque segun el plan",
            "el listado todavia trae al venado de cola blanca",
            "did the white-tailed deer disappear from Los Nevados",
        ],
    }

    return {
        "quotes": quotes,
        "records": records,
        "examples": examples,
        "labels": labels,
        "overrides": overrides,
        "append": append,
    }
