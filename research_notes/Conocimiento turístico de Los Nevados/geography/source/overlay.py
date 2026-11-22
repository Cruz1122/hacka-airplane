"""Round 2 overlay for the geography section (Parque Nacional Natural Los Nevados).

Applied by coordination/build_from_snapshot.py to the frozen snapshot geography.v1.json.
Deterministic: same snapshot in, same JSON out. Every fact is backed by a quote in
geography/evidence/quotes.md, which geography/check_quotes.py verifies.

Two kinds of change:
1. Corrections to existing entries: sentences that the quoted sources do not support are
   rewritten. Each replacement asserts that its old text occurs exactly once, so a changed
   snapshot fails loudly instead of silently keeping the old wording.
2. New entries: peaks, paramillos, lagoons, rivers, municipalities and wetlands named in
   the sources read on 2026-11-21 that the v1 section did not cover.
"""

import copy

DATE = "2026-11-21"


def _source(label, url):
    return {"label": label, "url": url, "retrieved_at": DATE}


PNN = _source(
    "Parques Nacionales Naturales de Colombia, ficha Los Nevados",
    "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
)
SGC_HOJA = _source(
    "Servicio Geológico Colombiano, hoja del Nevado del Ruiz, septiembre de 2024",
    "https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf",
)
SGC_TOP10 = _source(
    "Servicio Geológico Colombiano, los 10 volcanes más altos, 9 de agosto de 2024",
    "https://www2.sgc.gov.co/Noticias/Paginas/Los-10-volcanes-mas-altos-de-Colombia.aspx",
)
SGC_CRATER = _source(
    "Servicio Geológico Colombiano, morfología del cráter Arenas, 31 de enero de 2020",
    "https://www2.sgc.gov.co/Noticias/Paginas/El-Nuevo-Domo-de-Lava-del-Volcan-Nevado-del-Ruiz-y-la-Geomorfologia-Actual-del-Crater-Arenas-2020.aspx",
)
SGC_BOLETIN = _source(
    "Servicio Geológico Colombiano, boletín del segmento volcánico norte, actividad de 2023",
    "https://www2.sgc.gov.co/Publicaciones/Informes%20tcnicos/Informe_de_actividad_volcanica_segmento_norte_2023.pdf",
)
IDEAM_RUIZ = _source(
    "IDEAM, glaciar Nevado del Ruiz",
    "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-ruiz",
)
IDEAM_SANTA_ISABEL = _source(
    "IDEAM, glaciar Nevado Santa Isabel",
    "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-santa-isabel",
)
IDEAM_TOLIMA = _source(
    "IDEAM, glaciar Nevado del Tolima",
    "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-tolima",
)
RAMSAR = _source(
    "Ramsar, ficha CO1781 del complejo de humedales Laguna del Otún, 17 de julio de 2006",
    "https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf",
)
CARDER = _source(
    "CARDER, nota sobre PNN Los Nevados, 14 de julio de 2026",
    "https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/",
)
PNN_2017 = _source(
    "Parques Nacionales Naturales de Colombia, descripción de Los Nevados (portal antiguo, 2017; referencia secundaria)",
    "https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2017/12/Descripcion-PNN-Los-Nevados.pdf",
)
GOBERNACION = _source(
    "Gobernación del Tolima, turismo de Anzoátegui",
    "https://tolima.gov.co/tolima/informacion-general/turismo/1996-municipio-de-anzoategui",
)


def _replace(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"expected exactly one occurrence of {old!r}, found {text.count(old)}")
    return text.replace(old, new)


def _examples_of(reference, indexes):
    """Hard negatives are verbatim examples of another entry, picked by index."""
    return [reference["examples"][i] for i in indexes]


VARIANTS = {
    "geography.rio_coello": "Coello aparece en la tabla de drenaje del Tolima, junto con el Totare. Para el recorrido, pregunta al parque.",
    "geography.rio_azufrado": "La cabecera del Azufrado está en la cima del Ruiz, según la figura del SGC de 2020. Para subir, confirma el tramo con el parque.",
    "geography.rio_guali": "El Gualí aparece en la zona Medio Magdalena de la tabla del Ideam. Para el uso del agua, consulta al Ideam.",
    "geography.rios_lagunilla_recio": "Lagunilla y Recio figuran en la zona Alto Magdalena de la tabla del Ideam para el Ruiz. La tabla no da recorridos.",
    "geography.rio_campoalegre": "La Carder ubica en el parque las cuencas altas del Campoalegre y del Otún. El distrito Campoalegre es zona amortiguadora.",
    "geography.rios_quindio_combeima": "La Carder menciona el Quindío y el Combeima entre las cuencas que el parque protege. No dice la hoya de cada uno.",
    "geography.laguna_corazon": "La Laguna El Corazón está a 3.700 metros, según la Gobernación del Tolima. Confirma su límite con Parques Nacionales antes de ir.",
    "geography.laguna_bombona": "La Bomboná está a 3.600 metros, según la Gobernación. Su predio figura como privado; confirma con el parque si entra.",
    "geography.laguna_mellizas": "Las Mellizas y la Laguna Negra están a 3.450 metros, según la Gobernación del Tolima. Confirma el límite con el parque.",
    "geography.morro_negro": "Morro Negro forma parte del complejo Cisne-Morro Negro: el SGC da 4.700 metros y el boletín 4.600 metros de altura máxima.",
    "geography.nereidas": "Nereidas es un volcán no activo del complejo del Ruiz, según el SGC. Sin altura ni ubicación publicadas, no la marques en el mapa.",
    "geography.cerros_monitored": "Los tres cerros están en la lista de vigilancia del SGC en el segmento norte. Para saber si entran al parque, confirma con Parques Nacionales.",
}


def _new_entry(entry_id, label, kind, examples, short, sources, related, tags,
               hard_negatives, variants=(), detail=None):
    if not variants and entry_id in VARIANTS:
        variants = (VARIANTS[entry_id],)
    answer = {"short": short, "variants": list(variants)}
    if detail:
        answer["detail"] = detail
    return {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": list(examples),
        "answer": answer,
        "sources": list(sources),
        "last_verified": DATE,
        "related": list(related),
        "tags": list(tags),
        "hard_negatives": list(hard_negatives),
    }


def _swap_example(entries, entry_id, old, new):
    examples = entries[entry_id]["examples"]
    if examples.count(old) != 1:
        raise ValueError(f"{entry_id}: example {old!r} not found exactly once")
    examples[examples.index(old)] = new


def _corrections(entries):
    _swap_example(entries, "geography.laguna_encanto", "de qué laguna sale el río Totare",
                  "cuánto mide de altura la laguna del Encanto")
    _swap_example(entries, "geography.laguna_encanto", "does the Totare river start at that lake",
                  "how high is Laguna del Encanto")
    _swap_example(entries, "geography.watersheds", "¿El Campoalegre también nace en el parque?",
                  "¿hacia qué lado cae el agua del parque?")
    _swap_example(entries, "geography.watersheds", "¿A qué vertiente pertenecen el Gualí y el Recio?",
                  "¿el parque alimenta solo un río grande o varios?")
    _swap_example(entries, "geography.olleta_pirana", "nereidas entra en el mismo complejo",
                  "¿La Olleta tiene altura publicada?")
    _swap_example(entries, "geography.olleta_pirana", "Nereidas también sale en el SGC, ¿verdad?",
                  "¿La Piraña sale en el SGC como volcán?")
    _swap_example(entries, "geography.paramillo_cisne", "Morro Negro va con el Cisne",
                  "¿El Cisne tiene altura propia?")
    _swap_example(entries, "geography.paramillo_cisne", "Morro Negro, ¿eso es el mismo Cisne?",
                  "¿Qué altura tiene el Paramillo del Cisne?")
    _swap_example(entries, "geography.volcanic_centers", "Cerro Bravo está en la lista del parque",
                  "qué volcanes activos hay en el complejo del Ruiz")
    _swap_example(entries, "geography.summit_line", "Cerro Bravo está en el parque",
                  "cuál cumbre queda más al norte, Ruiz o Tolima")

    answer = entries["geography.sector_brisas_kumanday"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "Brisas-Kumanday es el sector norte, junto al Nevado del Ruiz.",
        "Brisas-Kumanday es el sector norte del parque, y su nombre es el del Ruiz (Kumanday).",
    )
    answer["variants"] = [
        _replace(v, "y queda junto al Ruiz.", "y su nombre es el del Ruiz (Kumanday).")
        for v in answer["variants"]
    ]

    answer = entries["geography.valle_tumbas"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "es un atractivo del sector norte Brisas-Kumanday, junto al Nevado del Ruiz.",
        "es un atractivo del sector Brisas-Kumanday, en la zona norte del parque.",
    )
    answer["variants"] = [
        _replace(v, "son el mismo lugar, en el norte, cerca del Ruiz.",
                 "son el mismo lugar, en la zona norte del parque.")
        for v in answer["variants"]
    ]

    answer = entries["geography.sector_quindio_dulima"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "del Nevado del Tolima, separado de los otros tres.",
        "del Nevado del Tolima.",
    )

    answer = entries["geography.laguna_otun_formation"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "Es permanente, entre ese nevado y el páramo de Santa Rosa.",
        "Queda entre ese nevado y el páramo de Santa Rosa.",
    )
    answer["detail"] = _replace(answer["detail"], "No es un inventario de 2026.", "No es un inventario actual.")

    answer = entries["geography.laguna_encanto"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "Anzoátegui es puerta de entrada al parque, pero no hay confirmación de que el espejo esté dentro del límite: confirma el punto con Parques Nacionales antes de ir.",
        "Confirma con Parques Nacionales si el espejo entra en el límite antes de ir.",
    )
    answer["detail"] = _replace(
        answer["detail"],
        "Otras lagunas de esa ficha turística, como El Corazón, Bomboná y Las Mellizas, figuran en predio privado y no se tratan aquí como lagunas del parque.",
        "Esa página también nombra El Corazón, Bomboná y Las Mellizas; no se tratan aquí como lagunas del parque.",
    )

    answer = entries["geography.tolima_municipalities"]["answer"]
    answer["short"] = _replace(answer["short"], " Cada nombre cubre la parte del municipio que entra al área.", "")
    # The 2026 fact sheet lists the ten municipalities without a department split; the Tolima
    # grouping comes from the 2017 PNN description (secondary, its list also names Villahermosa,
    # which the 2026 list omits and this section does not use).
    entries["geography.tolima_municipalities"]["sources"].append(PNN_2017)

    answer = entries["geography.municipalities"]["answer"]
    answer["short"] = _replace(answer["short"], "Son esos diez, no más.",
                               "La CARDER, en 2026, cuenta 11 municipios y no nombra el undécimo.")
    answer["detail"] = _replace(
        answer["detail"],
        "La lista que sí puedes usar es la de la ficha.",
        "La descripción anterior del PNN nombra a Villahermosa como undécimo municipio del Tolima; la ficha vigente no lo lista. Usa la lista de la ficha vigente.",
    )

    answer = entries["geography.tolima_municipalities"]["answer"]
    answer["short"] = _replace(
        answer["short"],
        "En el Tolima, el parque incluye seis municipios: Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca y Herveo. El Líbano y Armero no están en esa lista.",
        "Seis de los diez municipios de la ficha vigente están en el Tolima: Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca y Herveo. El Líbano y Armero no están en esa lista.",
    )
    answer["detail"] = "La división por departamento viene de la descripción PNN anterior, que además nombra a Villahermosa como municipio tolimense; la ficha vigente no lo lista. La Carder habla de 11 municipios sin nombrar el undécimo."

    answer = entries["geography.ibague_highlands"]["answer"]
    answer["short"] = _replace(answer["short"], " Eso corresponde a la parte alta del municipio.", "")

    answer = entries["geography.santa_isabel_height"]["answer"]
    answer["detail"] = _replace(
        answer["detail"],
        "La página no trae una fecha de publicación aparte; las cotas están en la tabla leída el 21 de noviembre de 2026.",
        "La página no trae una fecha de publicación visible.",
    )

    answer = entries["geography.ruiz_age"]["answer"]
    answer["short"] = _replace(answer["short"], "tiene unos 66.000 años", "tiene unos 66 mil años")
    answer["variants"] = [
        _replace(v, "Unos 66.000 años corresponden", "Unos 66 mil años corresponden") for v in answer["variants"]
    ]


def _new_entries(before):
    laguna_encanto = before["geography.laguna_encanto"]
    watersheds = before["geography.watersheds"]
    arenas = before["geography.arenas_crater"]
    ucumari = before["geography.ucumari_buffer"]
    laguna_otun = before["geography.laguna_otun"]
    municipalities = before["geography.municipalities"]
    tolima_municipalities = before["geography.tolima_municipalities"]
    santa_isabel = before["geography.santa_isabel"]
    ruiz_identity = before["geography.ruiz_identity"]
    tolima_volcano = before["geography.tolima_volcano"]
    paramillo_cisne = before["geography.paramillo_cisne"]
    olleta = before["geography.olleta_pirana"]
    volcanic_centers = before["geography.volcanic_centers"]

    return [
        _new_entry(
            "geography.rio_totare",
            "nacimiento del río Totare",
            "fact",
            [
                "de dónde nace el río totare",
                "dónde nace el totare",
                "el totare nace en la laguna del encanto?",
                "cuál es el nacimiento del río Totare, en qué laguna",
                "por cuál laguna baja el totare",
                "pa' saber de dónde viene el totare",
                "where does the Totare river start",
                "rio totare nacimiento",
                "necesito saber si el totare sale de la laguna del encanto",
                "el río totare de dónde es, de qué nevado baja",
                "el totare nace cerca de Anzoátegui?",
                "el Totare nace en la laguna o en el nevado?",
            ],
            "Según la Gobernación del Tolima, el río Totare nace en la Laguna El Encanto, en la vereda Hoyo Frío de Anzoátegui. Esa página no confirma que la laguna esté dentro del parque, así que pregunta a Parques Nacionales antes de ir.",
            [GOBERNACION],
            ["geography.laguna_encanto", "geography.tolima_volcano", "geography.watersheds"],
            ["río", "totare", "laguna del encanto"],
            _examples_of(laguna_encanto, [0, 1, 2]),
            variants=[
                "El Totare sale de la Laguna El Encanto, según la Gobernación, en Hoyo Frío, Anzoátegui. Antes de ir, confirma con el parque si esa laguna entra en el polígono.",
            ],
        ),
        _new_entry(
            "geography.rio_coello",
            "río Coello en el Tolima",
            "fact",
            [
                "qué río sale del Tolima hacia el Magdalena",
                "el río Coello nace en el parque?",
                "cuál es el río coello",
                "de qué cerro sale el coello",
                "rio coelo en qué zona está",
                "qué ríos bajan del Nevado del Tolima",
                "the Coello river, is it in the park",
                "el coello va para el magdalena o pal cauca",
                "pa' donde corre el río coello",
                "qué drenaje tiene el Tolima por el lado del Magdalena",
                "hay un río que se llame Coello en el parque",
                "qué cuencas nacen en el nevado del tolima",
            ],
            "En la tabla de drenaje del Ideam para el Nevado del Tolima aparece el río Coello en la zona Alto Magdalena, dentro de la vertiente del Magdalena. La tabla no da su recorrido ni dónde nace, así que para la ruta consulta al parque o al Ideam.",
            [IDEAM_TOLIMA],
            ["geography.rio_totare", "geography.watersheds", "geography.tolima_volcano"],
            ["río", "coello", "magdalena"],
            _examples_of(watersheds, [0, 1, 2]),
        ),
        _new_entry(
            "geography.rio_azufrado",
            "río Azufrado en la cima del Ruiz",
            "fact",
            [
                "cuál es el río Azufrado",
                "dónde nace el río Azufrado",
                "el azufrado sale del ruiz?",
                "rio azufrado en el nevado del ruiz",
                "qué río sale del cráter del Ruiz",
                "cabecera del azufrado, en qué parte está",
                "es el azufrado un río del parque",
                "Azufrado river Ruiz source",
                "el azufrado baja pal magdalena o pal cauca",
                "de qué volcán sale el río azufrado",
                "a dónde va el agua del azufrado",
                "el azufrado donde empieza, cerca del cráter?",
            ],
            "El SGC señala la cabecera del río Azufrado en la cima del Ruiz, en su figura de 2020 junto al cráter Arenas. El Ideam lo ubica en la zona Medio Magdalena. Para subir a la cima, el tramo lo confirma el parque; la foto no es un permiso.",
            [SGC_CRATER, IDEAM_RUIZ],
            ["geography.arenas_crater", "geography.ruiz_identity", "geography.watersheds"],
            ["río", "azufrado", "ruiz"],
            _examples_of(arenas, [0, 1, 2]),
        ),
        _new_entry(
            "geography.rio_guali",
            "río Gualí del Ruiz",
            "fact",
            [
                "río gualí dónde queda",
                "el gualí es del parque?",
                "a dónde va el río Gualí",
                "rio guali en el magdalena",
                "qué río es el gualí",
                "el gualí baja al magdalena?",
                "is the Gualí river in the park",
                "de qué lado del Ruiz sale el gualí",
                "gualí medio magdalena zona",
                "quiero saber del río gualí de la cordillera",
                "pa' donde corre el gualí, al magdalena o al cauca",
                "el río gualí sale del nevado?",
            ],
            "El Ideam incluye el río Gualí en la tabla de drenaje del Nevado del Ruiz, en la zona Medio Magdalena. Esa tabla solo indica la zona hidrográfica, no el recorrido completo, así que para el uso del agua consulta al Ideam.",
            [IDEAM_RUIZ],
            ["geography.rio_azufrado", "geography.rios_lagunilla_recio", "geography.watersheds"],
            ["río", "gualí", "magdalena"],
            _examples_of(watersheds, [3, 4, 5]),
        ),
        _new_entry(
            "geography.rios_lagunilla_recio",
            "ríos Lagunilla y Recio del Ruiz",
            "fact",
            [
                "río lagunilla del ruiz",
                "el río recio sale del nevado",
                "rio recio dónde nace",
                "qué son los ríos lagunilla y recio",
                "lagunilla o recio, cuál baja al magdalena",
                "ríos que nacen en el Ruiz hacia el Magdalena",
                "is the Recio river on the Ruiz",
                "el recio y la lagunilla pa' qué lado van",
                "cuáles son los ríos del Ruiz que van al Alto Magdalena",
                "tienen algo que ver el recio y el lagunilla con el parque",
                "lagunilla recio drenaje del ruiz",
                "qué ríos salen del Ruiz por el lado tolimense",
            ],
            "El Ideam incluye los ríos Lagunilla y Recio en la tabla de drenaje del Nevado del Ruiz, dentro de la zona Alto Magdalena. La tabla no dice dónde nace cada uno, así que no la tomes como mapa de quebradas.",
            [IDEAM_RUIZ],
            ["geography.rio_guali", "geography.rio_azufrado", "geography.watersheds"],
            ["río", "lagunilla", "recio"],
            _examples_of(watersheds, [6, 7, 8]),
        ),
        _new_entry(
            "geography.rio_campoalegre",
            "cuenca alta del río Campoalegre",
            "fact",
            [
                "río campoalegre",
                "el campoalegre nace en el parque?",
                "dónde nace el campoalegre",
                "cuenca del campoalegre, es del parque",
                "el campoalegre da agua a risaralda?",
                "rio campoalegre pereira",
                "is the Campoalegre river in the park",
                "de qué nevado nace el campoalegre",
                "el río campoalegre sirve para el agua de pereira",
                "el campoalegre es un río o un distrito",
                "campoalegre cuenca alta dónde queda",
                "que río nace cerca de Santa Rosa, el Campoalegre?",
            ],
            "La Carder dice que en el parque nacen las cuencas altas de los ríos Otún y Campoalegre, fuentes de abastecimiento para Risaralda. El distrito de conservación de suelos Campoalegre es zona amortiguadora, no el parque, y la nota no dice a qué hoya cae el río.",
            [CARDER],
            ["geography.risaralda_share", "geography.ucumari_buffer", "geography.rio_otun"],
            ["río", "campoalegre", "risaralda"],
            _examples_of(ucumari, [0, 1, 2]),
        ),
        _new_entry(
            "geography.rios_quindio_combeima",
            "cuencas altas de los ríos Quindío y Combeima",
            "fact",
            [
                "rio quindío nace en el parque",
                "el combeima sale del nevado del tolima?",
                "cuencas del quindío y del combeima",
                "rio combeima dónde nace",
                "el río quindio es del nevado?",
                "qué ríos protege el parque en el quindío y el tolima",
                "does the Combeima river start in the park",
                "combeima cuenca alta",
                "el quindio y el combeima son del parque",
                "de dónde sale el combeima, pa' saber",
                "ríos que el parque cuida además del otún y el chinchiná",
                "el río quindío queda cerca de salento?",
            ],
            "La Carder dice que el parque protege las cuencas altas de los ríos Otún, Chinchiná, Quindío y Combeima. La nota no dice a qué hoya llega cada uno, así que no supongas la cuenca por el nombre del río.",
            [CARDER],
            ["geography.watersheds", "geography.rio_chinchina", "geography.rio_otun"],
            ["río", "quindío", "combeima"],
            _examples_of(watersheds, [9, 10, 11]),
        ),
        _new_entry(
            "geography.laguna_corazon",
            "Laguna El Corazón en Anzoátegui",
            "fact",
            [
                "laguna el corazón",
                "cómo es la laguna del corazón de anzoátegui",
                "la laguna corazón queda en el parque?",
                "la laguna con forma de corazón en el tolima",
                "a cuántos metros está la laguna el corazón",
                "laguna el corazon hoyo frio",
                "is Laguna El Corazón inside the park",
                "la laguna corazón es del parque o de un predio privado?",
                "la laguna del corazón, altura",
                "cuál es la altura de la laguna el corazón",
                "laguna corazón trucha",
                "la laguna en forma de corazón que queda cerca de hoyo frío",
            ],
            "Según la Gobernación del Tolima, la Laguna El Corazón está sobre los 3.700 metros, en el camino hacia la vereda Hoyo Frío. La misma página marca su predio como privado y no dice que esté dentro del parque; confírmalo con Parques Nacionales antes de planear.",
            [GOBERNACION],
            ["geography.laguna_encanto", "geography.laguna_bombona", "geography.laguna_otun"],
            ["laguna", "corazón", "anzoátegui"],
            _examples_of(laguna_encanto, [3, 4, 5]),
        ),
        _new_entry(
            "geography.laguna_bombona",
            "Laguna Bomboná en la vereda La Cascada",
            "fact",
            [
                "laguna bomboná",
                "dónde queda la laguna bombona",
                "a cuántos metros está la bomboná",
                "laguna bombona vereda la cascada",
                "la laguna de la cascada en el tolima, cómo se llama",
                "es la bomboná del parque?",
                "where is Bomboná lake",
                "laguna bomboná altura",
                "la bombona es privada o pública",
                "cuánto mide de altura la bombona",
                "laguna bombona de Anzoátegui",
                "lagunas con trucha en el tolima, la bomboná",
            ],
            "Según la Gobernación del Tolima, la Laguna Bomboná está a 3.600 metros, en la vereda La Cascada, y su predio aparece como privado. La página no dice que esté dentro del parque; confírmalo con Parques Nacionales antes de ir.",
            [GOBERNACION],
            ["geography.laguna_corazon", "geography.laguna_encanto", "geography.laguna_otun"],
            ["laguna", "bomboná", "la cascada"],
            _examples_of(laguna_encanto, [6, 7, 8]),
        ),
        _new_entry(
            "geography.laguna_mellizas",
            "Las Mellizas y la Laguna Negra",
            "fact",
            [
                "laguna las mellizas",
                "qué son las mellizas",
                "dónde queda la laguna negra de las mellizas",
                "las mellizas en el tolima, cuántas lagunas",
                "complejo de lagunas las mellizas",
                "las lagunas mellizas a qué altura quedan",
                "is Las Mellizas inside the park",
                "las mellizas están dentro del parque?",
                "laguna negra y las mellizas, dónde",
                "cuál es la altura de las mellizas",
                "las mellisas laguna",
                "lagunas mellizas páramo bajo",
            ],
            "Según la Gobernación del Tolima, Las Mellizas es un complejo de tres lagunas, con la Laguna Negra, en zona de páramo bajo a 3.450 metros. La página no dice que esté dentro del parque, así que confirma el límite con Parques Nacionales.",
            [GOBERNACION],
            ["geography.laguna_corazon", "geography.laguna_bombona", "geography.laguna_encanto"],
            ["laguna", "mellizas", "laguna negra"],
            _examples_of(laguna_otun, [0, 1, 2]),
        ),
        _new_entry(
            "geography.morro_negro",
            "Morro Negro y el complejo del Cisne",
            "explanation",
            [
                "morro negro es un nevado?",
                "qué es morro negro",
                "dónde queda morro negro",
                "cerro morro negro del parque",
                "morro negro y el cisne son lo mismo",
                "altura de morro negro",
                "is Morro Negro a separate peak",
                "morro negro, paramillo del cisne",
                "morro negro domo",
                "domos del cisne, qué es el morro negro",
                "morro negro cuanto mide",
                "what is Morro Negro",
            ],
            "Morro Negro no aparece como cumbre aparte: el SGC lo nombra en el Paramillo del Cisne-Morro Negro, con 4.700 metros en el ranking de 2024. El boletín de 2023 da 4.600 metros de altura máxima para el Paramillo del Cisne. Si necesitas la cifra exacta, consulta la fuente del SGC.",
            [SGC_TOP10, SGC_BOLETIN],
            ["geography.paramillo_cisne", "geography.santa_isabel", "geography.sector_cisne_poleka"],
            ["morro negro", "domo", "cisne"],
            _examples_of(paramillo_cisne, [0, 1, 2]),
        ),
        _new_entry(
            "geography.nereidas",
            "volcán Nereidas del complejo del Ruiz",
            "fact",
            [
                "qué es nereidas",
                "volcán nereidas",
                "nereidas es un volcán del ruiz?",
                "cráter nereidas dónde queda",
                "nereidas activo o inactivo",
                "es nereidas un volcán que sigue activo",
                "what is Nereidas volcano",
                "altura del volcán nereidas",
                "la nereidas del complejo, cuál es",
                "las nereidas, olleta y piraña son volcanes",
                "nereidas en el mapa del parque",
                "nereidas, qué tipo de volcán",
            ],
            "Nereidas es uno de los volcanes no activos del complejo del Ruiz, según el SGC en su hoja de septiembre de 2024. Las fuentes que leí no dan su altura ni su ubicación exacta, así que no la supongas.",
            [SGC_HOJA, SGC_BOLETIN],
            ["geography.olleta_pirana", "geography.volcanic_centers", "geography.ruiz_identity"],
            ["nereidas", "volcán", "no activo"],
            _examples_of(olleta, [0, 1, 2]),
        ),
        _new_entry(
            "geography.cerros_monitored",
            "Cerro Bravo, Cerro España y Cerro Machín",
            "explanation",
            [
                "cerro bravo queda dentro de los nevados?",
                "cerro machín es parte de los nevados",
                "cerro españa dentro del parque",
                "volcanes que vigila el sgc en el norte",
                "cerro bravo y cerro machín, qué son",
                "el cerro machín queda en el parque nacional",
                "is Cerro Machín inside Los Nevados",
                "cerro españa volcán, cuánto mide",
                "cerro bravo es un volcán del nevado",
                "cuáles volcanes del norte están en el parque",
                "machín y bravo, son del parque o no",
                "el sgc monitorea cerro bravo, cerro españa y cerro machín",
            ],
            "El SGC incluye Cerro Bravo, Cerro España y Cerro Machín en la lista de volcanes del segmento norte que vigila, pero la ficha del parque no los nombra entre sus cumbres. Para saber si alguno entra en el polígono, confirma con Parques Nacionales.",
            [SGC_BOLETIN, PNN],
            ["geography.volcanic_centers", "geography.park_versus_volcano", "geography.summit_line"],
            ["cerro", "segmento norte", "monitoreo"],
            _examples_of(volcanic_centers, [0, 1, 2]),
        ),
    ]


def apply(section):
    data = copy.deepcopy(section)
    by_id = {entry["id"]: entry for entry in data["entries"]}
    _corrections(by_id)
    # Hard negatives are copied from the corrected examples, so they match the final section.
    before = {entry["id"]: copy.deepcopy(entry) for entry in data["entries"]}
    data["entries"].extend(_new_entries(before))
    return data
