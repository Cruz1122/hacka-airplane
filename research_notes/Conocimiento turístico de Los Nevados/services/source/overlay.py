"""Round 2 overlay for `services`. The snapshot services.v1.json stays frozen.

apply(section) edits existing entries by id and appends the new ones. The sources of every entry are
derived from its block in evidence/quotes.md, so an entry cites only the raw files that its quotes use.
Deterministic: no clocks, no network, no randomness.
"""

import copy
import re
from pathlib import Path

RETRIEVED = "2026-11-21"
QUOTES = Path(__file__).resolve().parents[1] / "evidence" / "quotes.md"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
HEADING = re.compile(r"^##\s+(services\.\S+)\s*$")

SOURCE_BY_FILE = {
    "pnn_nevados.txt": (
        "Parques Nacionales Naturales · Los Nevados (ficha oficial)",
        "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    ),
    "pnn_informe_necesidades_2024.txt": (
        "PNN Los Nevados · Informe de necesidades de asistencia 2024",
        "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx",
    ),
    "anexo_pnn_nevados_2023.txt": (
        "PNN Los Nevados · Anexo de reglamentación ecoturística (2023)",
        "https://parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf",
    ),
    "poe2026.txt": (
        "PNN · Organiza tu viaje al PNN Los Nevados 2026-2030 (PDF)",
        "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
    ),
    "nevados_2024_07.txt": (
        "PNN Los Nevados · Folleto de gestión del ejercicio (2024)",
        "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/07/nevados.pdf",
    ),
    "radicado_20266200001002.txt": (
        "PNN Los Nevados · Respuesta a derecho de petición (18-05-2026)",
        "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf",
    ),
    "mincit_que_es_rnt.html": (
        "MinCIT · Qué es el Registro Nacional de Turismo",
        "https://www.mincit.gov.co/minturismo/analisis-sectorial-y-promocion/registro-nacional-de-turismo/que-es-el-registro-nacional-de-turismo",
    ),
    "mincit_invita_renovar_rnt_2026.html": (
        "MinCIT · Llamado a renovar el RNT 2026 (11-02-2026)",
        "https://www.mincit.gov.co/prensa/noticias/turismo/mincit-invita-renovar-registro-nacional-de-turismo",
    ),
    "villamaria_rendicion_dic2025.txt": (
        "Alcaldía de Villamaría · Informe de rendición de cuentas (dic. 2025)",
        "https://villamaria-caldas.gov.co/Participa/Documents/INFORME%20RENDICION%20%20DE%20CUENTAS%20DICIEMBRE%202025%20.pdf",
    ),
}

# Entries whose answer, variants or detail changed in Round 2. Every other entry keeps its text.
EDITS = {
    "services.brisas_visitor_center": {
        "short": "Según el informe 2024 de PNN, en Brisas hay taquilla, centro de inducción y una cabaña. El centro de inducción está a unos 4100 metros de altitud, según la ficha de PNN. Confirma los servicios antes de viajar.",
        "variants": ["En Brisas encuentras taquilla, centro de inducción y una cabaña (informe 2024 de PNN). El centro de inducción queda a unos 4100 metros."],
    },
    "services.first_aid_points": {
        "short": "En Arenales, la cabaña tiene un punto de primeros auxilios, y en Brisas y Arenales hay enfermería (informe 2024). Potosí, Laguna del Otún, Cisne, Valle del Cocora, Juntas y Anzoátegui figuran como necesidades, no como servicio confirmado. Confirma el servicio antes de viajar.",
        "variants": ["En Arenales hay un punto de primeros auxilios en la cabaña, y en Brisas y Arenales hay enfermería (dato de 2024). Pregunta antes de viajar si sigue operando."],
        "detail": "Los puntos de Potosí, Laguna del Otún, Cisne, Valle de Cocora, Juntas y Anzoátegui aparecen en la sección 'necesidades de asistencia' del informe 2024, con insumos por cubrir. Eso indica necesidad, no un servicio que opera hoy.",
    },
    "services.cisne_visitor_center": {
        "short": "El centro de visitantes El Cisne está a unos 4100 metros de altitud. UTON gestiona el alojamiento allí, y en 2024 se registró también alimentación; no tengo confirmado cuántas camas hay. Pregunta a UTON antes de planear dormir allí.",
        "variants": ["El centro El Cisne queda a unos 4100 metros. UTON maneja el alojamiento, y en 2024 se registró alimentación. No tengo confirmado el número de camas."],
    },
    "services.potosi_cabin": {
        "short": "La cabaña Potosí es un punto de control y vigilancia, a unos 3920 metros de altitud. En 2024 tenía mantenimiento correctivo y preventivo. En el límite del parque, el refugio Potosí (Campo Alegre) ofrecía hospedaje y alimentación en 2024. Confirma disponibilidad antes de viajar.",
        "variants": ["La cabaña Potosí sirve para control y vigilancia del parque, a unos 3920 metros. Para hospedaje, el refugio Potosí de Campo Alegre figuraba en 2024; confirma disponibilidad antes de viajar."],
        "detail": "El informe 2024 describe la cabaña como de prevención, control y vigilancia del parque. El estado de mantenimiento es de 2024 y no confirma el estado actual. La altitud viene de la ficha de PNN.",
    },
    "services.otun_lodging": {
        "short": "En la vereda El Bosque, en el límite del parque, puedes disfrutar de la estadía en casas tradicionales de sus habitantes. El informe 2024 lista allí hospedaje, alimentación y porteo, con datos del plan 2017-2022. Confirma disponibilidad antes de viajar.",
        "variants": ["En El Bosque, en el límite del parque, hay casas tradicionales con hospedaje y alimentación (datos del informe 2024). Confirma disponibilidad antes de viajar."],
    },
    "services.brisas_lodging": {
        "short": "PNN dice que UTON gestiona alojamiento en Brisas, pero otra parte de la misma ficha no lo menciona. No tengo confirmado si hay camas: pregunta a UTON antes de planear dormir allí.",
        "variants": ["UTON gestiona alojamiento en Brisas según PNN, aunque la misma ficha omite ese servicio en otro pasaje. Confirma camas con UTON antes de viajar."],
        "detail": "Conflicto dentro de la página de PNN: en la sección de Brisas aparece 'reservas, ingreso, guianza, transporte, alojamiento y tienda', pero en la sección de guías y operadores aparece 'reservas, ingreso, guianza, transporte y tienda'. No hay un dato de camas verificado; no resuelvo el conflicto a favor de ninguna de las dos frases.",
    },
    "services.porter_luggage": {
        "short": "Según la reglamentación de 2023, el porteo de maletas solo se permite por El Cedral, Valle de Cocora y Palomar, y está prohibido en los campamentos de Calvito y Arenales. El informe 2024 también lo lista en Juntas y en Los Chilcos–Arenales; confirma la ruta con el prestador.",
        "variants": ["El porteo de maletas está permitido solo por El Cedral, Valle de Cocora y Palomar según la reglamentación de 2023, y prohibido en Calvito y Arenales. Confirma la ruta y el precio con el prestador."],
        "detail": "Conflicto sin resolver: la reglamentación de 2023 limita el porteo al sector sur y lo prohíbe en los campamentos de Calvito y Arenales. El informe 2024 lo lista en la ruta de Juntas y en Los Chilcos–Arenales cumbre. La respuesta sigue la norma de 2023; la ruta de Juntas y Chilcos debe confirmarse con el prestador y con el dueño de la sección access.",
    },
    "services.uton_services": {
        "short": "UTON gestiona en Brisas reservas, ingreso, guianza, transporte, alojamiento y tienda. En el norte, hasta Valle de las Tumbas, el contrato prevé taquilla, guianza y alimentos (dato de 2024). Pregunta a UTON qué servicios operan el día de tu visita.",
        "detail": "Las fuentes no listan lo mismo: la ficha de PNN incluye alojamiento en Brisas en un pasaje y no en otro. El informe 2024 usa 'tiene previstos', así que describe lo contratado y no un servicio confirmado hoy. Para El Cisne, la ficha menciona alojamiento dentro del contrato con UTON.",
    },
    "services.interpretive_guiding": {
        "short": "Guías y operadores registrados ofrecen guianza interpretativa en varios senderos (dato de 2024). En el sendero del Ruiz está restringida por la actividad volcánica. Pídela al operador antes de subir.",
    },
    "services.guide_radios": {
        "detail": "La ficha de PNN exige a guías y operadores radios con la frecuencia requerida y equipo médico de respuesta. El anexo de 2023 exige al guía botiquín, radio obligatorio y vestimenta de alta montaña. La frecuencia no aparece en las fuentes revisadas; no la incluyo.",
    },
    "services.phone_signal": {
        "detail": "El informe 2024 dice que, para algunos sectores, 'se requiere implementar comunicaciones para la gestión del riesgo'. El folleto 2024 cita 'Radiocomunicaciones' entre sus aciertos, sin decir dónde ni con qué cobertura. La publicación 2026 menciona 'la consolidación de radiocomunicaciones'. Ninguna fuente revisada describe cobertura celular actual.",
    },
    "services.accessibility": {
        "short": "No tengo información oficial sobre accesibilidad para silla de ruedas o movilidad reducida en el parque. En Quindío–Dulima el terreno es más exigente; pregunta al prestador antes de ir.",
        "variants": ["No tengo datos oficiales de accesibilidad para movilidad reducida. En Quindío–Dulima el terreno es más exigente: pide información al prestador."],
    },
    "services.camp_showers": {
        "short": "En la cabaña de Arenales hay una batería de baños con duchas para campistas, además de cocina y comedor para ellos (dato de 2024). En 2024 su zona de camping no estaba habilitada por actividad volcánica. Confirma antes de viajar si el camping está abierto.",
    },
    "services.official_sites": {
        "short": "Revisa los servicios en parquesnacionales.gov.co y en operacionnevados.co, la página de la concesión UTON. Los datos de servicios pueden cambiar; confirma antes de viajar.",
        "variants": ["Consulta los servicios en parquesnacionales.gov.co y en la página de UTON (operacionnevados.co) antes de viajar, porque pueden cambiar."],
        "detail": "La ficha de PNN enlaza la página de UTON. No verifiqué otros enlaces ni listados de servicios por sector en esas páginas.",
    },
    "services.quindio_dulima": {
        "short": "En Quindío–Dulima el terreno es más exigente y el montañismo es la actividad principal. La ficha de PNN menciona puntos de atención en Valle del Cocora, Juntas y Anzoátegui; el informe 2024 los listaba como necesidades, no como servicios confirmados. Confirma antes de subir.",
        "variants": ["En Quindío–Dulima el terreno es más exigente. PNN menciona puntos de atención en Valle del Cocora, Juntas y Anzoátegui, pero el informe 2024 los figuraba como necesidades."],
    },
    "services.town_lodging_rnt": {},
    "services.lost_items": {
        "short": "No tengo confirmado un servicio de objetos perdidos, y el personal de Parques Nacionales no se responsabiliza por objetos extraviados (reglamentación 2023). Para consultas, escribe a nevados@parquesnacionales.gov.co.",
        "variants": ["No tengo confirmado un procedimiento de objetos perdidos. Escribe a nevados@parquesnacionales.gov.co con la descripción del objeto y el sector donde lo perdiste."],
    },
}

NEW_ENTRIES = [
    {
        "id": "services.porter_requirements",
        "label": "requisitos para ser porteador",
        "kind": "fact",
        "audience": "visitor",
        "lang": "es",
        "hard_negatives": ["cuánto cobran por cargar la maleta", "hay quien lleve el equipaje"],
        "entities": {},
        "answer": {
            "short": "Un porteador debe ser campesino o arriero local del parque, mayor de edad y estar registrado en la base de datos de porteadores avalados por el parque. Pide que te muestre ese registro antes de contratarlo.",
            "variants": ["Para porteo, el porteador debe ser local, mayor de edad y figurar en la base de datos de porteadores avalados por el parque. Pide ese registro antes de contratar."],
            "detail": "Estos requisitos vienen del anexo de reglamentación de 2023. No verifiqué si la base de datos de porteadores está publicada ni cómo consultarla; pregúntale al prestador por su registro.",
            "reflection": None,
        },
        "examples": [
            "requisitos para ser porteador",
            "qué debe cumplir un porteador",
            "el porteador tiene que estar registrado?",
            "porteadores avalados por el parque",
            "un porteador puede ser cualquier persona?",
            "tienen que ser mayores de edad los porteadores?",
            "requisitos del porteo en Los Nevados",
            "quién puede cargar maletas en el parque",
            "el que me carga el morral tiene que ser de la zona?",
            "porteador local o de otra ciudad, da igual?",
            "cómo sé si el porteador está avalado",
            "what does a porter need to be registered",
            "can any person work as porter here",
            "pa cargar maletas tiene que ser del pueblo?",
        ],
        "related": ["services.porter_luggage", "services.mule_luggage_registered_only"],
        "tags": ["porteo", "porteador", "registro", "requisitos"],
    },
    {
        "id": "services.mule_luggage_registered_only",
        "label": "mulas para cargar equipaje",
        "kind": "fact",
        "audience": "visitor",
        "lang": "es",
        "hard_negatives": ["paseo a mula por los senderos", "el caballo sirve para la travesía"],
        "entities": {},
        "answer": {
            "short": "No entran mulas ni caballos con fines turísticos, como cabalgatas. Solo los arrieros avalados por el parque pueden cargar equipaje con mulas, previa autorización de un funcionario. Pide un arriero registrado antes de subir.",
            "variants": ["Para cargar equipaje con mulas solo hay arrieros avalados por el parque, con autorización de un funcionario. Las cabalgatas turísticas no están permitidas."],
            "detail": "El anexo de 2023 prohíbe el ingreso de equinos y mulares con fines turísticos y permite la carga solo a arrieros avalados. No encontré un listado publicado de arrieros ni tarifas.",
            "reflection": None,
        },
        "examples": [
            "puedo subir con mula pa cargar las maletas?",
            "se puede entrar con mulas al parque",
            "llevar caballo para el equipaje",
            "las mulas pueden cargar la carpa",
            "entrar con arriero y mula a Los Nevados",
            "arriero con mula, se puede?",
            "burros o mulas para subir el equipaje",
            "se puede llevar el equipaje en mula o caballo",
            "mulas para llevar la comida al campamento",
            "el arriero puede subir con los bultos?",
            "can I bring a mule to carry my bags",
            "are horses allowed to carry luggage",
        ],
        "related": ["services.porter_luggage", "services.porter_requirements"],
        "tags": ["mulas", "arrieros", "porteo", "caballos"],
    },
]


def source_map():
    """Map each entry id to its sources, in the order its quotes.md block names the raw files."""
    result, current, seen = {}, None, set()
    for line in QUOTES.read_text(encoding="utf-8").splitlines():
        heading = HEADING.match(line)
        if heading:
            current = heading.group(1)
            result[current] = []
            continue
        if current is None:
            continue
        for match in ARCHIVO.finditer(line):
            raw = match.group(1).rsplit("/", 1)[-1]
            if raw not in SOURCE_BY_FILE:
                raise ValueError(f"{current}: no source registered for {raw}")
            label, url = SOURCE_BY_FILE[raw]
            if (current, url) not in seen:
                seen.add((current, url))
                result[current].append({"label": label, "url": url, "retrieved_at": RETRIEVED})
    return result


def apply(section):
    data = copy.deepcopy(section)
    sources = source_map()
    by_id = {entry["id"]: entry for entry in data["entries"]}

    for entry_id, changes in EDITS.items():
        entry = by_id[entry_id]
        for key in ("short", "variants", "detail"):
            if key in changes:
                entry["answer"][key] = changes[key]
        entry["last_verified"] = RETRIEVED

    for entry_id, entry in by_id.items():
        if entry_id in sources:
            entry["sources"] = sources[entry_id]

    for new in NEW_ENTRIES:
        entry = copy.deepcopy(new)
        entry["sources"] = sources[entry["id"]]
        entry["last_verified"] = RETRIEVED
        entry["valid_until"] = None
        data["entries"].append(entry)

    return data
