"""Round-2 corrections for the frozen activities snapshot.

`apply` rewrites answers whose facts were missing, stale or contradicted by a
later official act, and upserts entries that a downloaded source actually
supports. The snapshot stays untouched.
"""

from __future__ import annotations

PNN = {
    "label": "Parques Nacionales Naturales de Colombia, ficha PNN Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21",
}
RES207 = {
    "label": "Resolución 207 del 4 de agosto de 2023, reglamentación del ecoturismo",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf",
    "retrieved_at": "2026-11-21",
}
RES017 = {
    "label": "Resolución 017 del 17 de enero de 2024, cierre parcial Juntas-Cocora",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/01/Resolucion-No.-017-de-17012024_cierre-parcial-PNN-Nevados.pdf",
    "retrieved_at": "2026-11-21",
}
RES708 = {
    "label": "Resolución del 26 de diciembre de 2024, apertura del tramo Juntas-Cocora",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Resolucion-No.708-Por-la-cual-se-ordena-la-apertura-del-tramo-del-sendero-Juntas-Cocora-PNN-Los-Nevados.pdf",
    "retrieved_at": "2026-11-21",
}
INFORME = {
    "label": "Informe de necesidades de asistencia, PNN Los Nevados, 2024",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx",
    "retrieved_at": "2026-11-21",
}
PLAN = {
    "label": "Plan de manejo PNN Los Nevados, adoptado en 2017",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2020/10/plan-de-manejo-pnn-los-nevados.pdf",
    "retrieved_at": "2026-11-21",
}
CALDAS = {
    "label": "Gobernación de Caldas, ficha Naturaleza y páramo",
    "url": "https://caldasesnatural.travel/experiencias/naturaleza-y-paramo/",
    "retrieved_at": "2026-11-21",
}
CARTA = {
    "label": "Carta del jefe del PNN Los Nevados, 11 de mayo de 2026",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf",
    "retrieved_at": "2026-11-21",
}
POE = {
    "label": "Plan de ordenamiento ecoturístico, versión corta 2026-2030",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
    "retrieved_at": "2026-11-21",
}
NEWS2016 = {
    "label": "Noticia PNN, adecuación del sendero Conejeras, 2016",
    "url": "https://old.parquesnacionales.gov.co/portal/es/parque-nacional-natural-los-nevados-adecua-el-sendero-conejeras-borde-de-glaciar-alnevado-de-santa-isabel/",
    "retrieved_at": "2026-11-21",
}
NEWS2020 = {
    "label": "Noticia PNN, reapertura del sector centro, 9 de diciembre de 2020",
    "url": "https://old.parquesnacionales.gov.co/portal/es/se-reabre-para-el-ecoturismo-el-sector-centro-del-parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21",
}

NEGATIVES = [
    "salud en altura",
    "síntomas de soroche",
    "cómo reconocer hipotermia",
    "me puedo quemar aunque esté nublado",
    "cómo es el clima en Los Nevados",
    "dónde miro el pronóstico del parque",
    "qué significa alerta amarilla del Ruiz",
    "qué alerta tiene hoy el Nevado del Ruiz",
    "hola",
    "gracias",
    "chao",
    "qué puedes hacer",
    "cómo vestirme para ir al nevado",
    "qué zapatos llevar a los nevados",
    "qué bloqueador solar llevar al nevado",
    "son obligatorias las gafas de sol en el nevado",
    "debo preguntarle al médico antes de ir",
    "nieva en Los Nevados",
    "eres un robot?",
    "qué gorro llevar al parque los nevados",
    "puedo seguir subiendo con dolor de cabeza",
    "cuándo llueve más en Los Nevados",
    "escríbeme un poema",
    "sirve un poncho de plástico para la lluvia",
]


def _set_short(entry: dict, short: str, variant: str, detail: str | None = None) -> None:
    if len(short) > 320:
        raise ValueError(f"{entry['id']}: short is {len(short)} chars")
    if len(variant) > 320:
        raise ValueError(f"{entry['id']}: variant is {len(variant)} chars")
    entry["answer"]["short"] = short
    entry["answer"]["variants"] = [variant]
    if detail is not None:
        entry["answer"]["detail"] = detail
    entry["last_verified"] = "2026-11-21"


def _entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    short: str,
    variant: str,
    related: list[str],
    sources: list[dict],
    tags: list[str],
    sector: list[str],
    negative_at: int,
) -> dict:
    words = label.split()
    if not 3 <= len(words) <= 8:
        raise ValueError(f"{entry_id}: label has {len(words)} words")
    if len(examples) != 12:
        raise ValueError(f"{entry_id}: {len(examples)} examples")
    if len(short) > 320 or len(variant) > 320:
        raise ValueError(f"{entry_id}: answer too long ({len(short)}/{len(variant)})")
    negatives = [NEGATIVES[negative_at % len(NEGATIVES)], NEGATIVES[(negative_at + 7) % len(NEGATIVES)], NEGATIVES[(negative_at + 13) % len(NEGATIVES)]]
    return {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "entities": {"sector": sector} if sector else {},
        "needs": [],
        "answer": {
            "short": short,
            "variants": [variant],
            "detail": None,
        },
        "sources": sources,
        "last_verified": "2026-11-21",
        "valid_until": None,
        "related": related,
        "tags": tags,
    }


def _new_entries() -> list[dict]:
    rows = [
        _entry(
            "activities.potosi_laguna_road",
            "carreteable de Potosí a la laguna",
            "fact",
            [
                "de Potosí se puede seguir hasta la laguna",
                "qué hay entre Potosí y la Laguna del Otún",
                "Corraleja queda en el camino a la laguna?",
                "el carreteable pasa por el Muelle",
                "cuántos kilómetros hay de Potosí a la laguna",
                "puedo pasar de la Asomadera y seguir a la laguna",
                "esa vía de interpretación llega a la laguna o se queda antes",
                "potosi corraleja asomadera hasta donde llega",
                "me dejan bajar del mirador hasta el agua?",
                "el sendero 6 es el de la laguna completa?",
                "how far is the road from Potosí to Laguna del Otún",
                "does the Potosí road actually reach the lake",
            ],
            "El sendero de la norma del 4 de agosto de 2023 sale de Potosí, pasa por Corraleja y la Asomadera, y sigue a Muelle y la Laguna del Otún. Un informe de 2024, citando el plan 2017-2022, le da 11 km. La pasadía sin dormir llega solo hasta la Asomadera. Confirma con el parque hasta dónde sigues ese día.",
            "De Potosí a la laguna el reglamento nombra Corraleja, Asomadera y Muelle, con 11 km en el informe de 2024. Sin pernoctar, la pasadía se queda en la Asomadera. Pregunta hasta dónde está habilitado tu día.",
            ["activities.asomadera_day", "activities.sector_laguna_otun", "activities.victor_mariposa_lagoons"],
            [RES207, INFORME],
            ["potosi", "laguna", "carreteable"],
            ["otun"],
            0,
        ),
        _entry(
            "activities.laguna_el_mosquito",
            "punto Laguna El Mosquito",
            "fact",
            [
                "puedo ir a la Laguna El Mosquito",
                "la laguna del mosquito es una parada o un paseo aparte",
                "dónde queda El Mosquito en el camino del Otún",
                "esa lagunita sale en la travesía al Cocora?",
                "me desvío a El Mosquito o va en el mismo sendero",
                "hay un mirador propio de la Laguna El Mosquito",
                "cuánto se demora solo hasta El Mosquito",
                "el mosquito esta antes de berlin o despues",
                "quiero conocer esa laguna chiquita del otun",
                "se puede acampar en El Mosquito",
                "is Laguna El Mosquito its own hike",
                "where does El Mosquito sit on the Otún trails",
            ],
            "Laguna El Mosquito es un punto de dos senderos de la norma del 4 de agosto de 2023: el que baja de la Laguna del Otún hacia El Cedral y el que sigue hacia el Cocora por la cuchilla de Berlín. No tiene paseo ni duración propios. Pídela solo dentro del sendero que el parque te confirme.",
            "El Mosquito no es una salida suelta: está nombrada en la bajada al Cedral y en la travesía hacia el Cocora. Confirma con el parque que ese sendero esté abierto y no le armes un plan aparte.",
            ["activities.otun_cedral_walk", "activities.otun_cocora_traverse", "activities.sector_laguna_otun"],
            [RES207],
            ["mosquito", "otun", "sendero"],
            ["otun"],
            1,
        ),
        _entry(
            "activities.recreation_zone_trails",
            "zona donde están las caminatas",
            "rule",
            [
                "puedo caminar por todo el parque o solo por una zona",
                "qué es la zona de recreación general exterior",
                "las caminatas están limitadas a unos senderos",
                "me puedo salir del camino si el paisaje está al lado",
                "el parque entero está abierto para recorrer",
                "hay zonas donde el ecoturismo no entra",
                "por qué me obligan a seguir el sendero marcado",
                "si conozco un atajo entre dos caminos, sirve?",
                "la zona de visita es solo la de los senderos del mapa",
                "12 senderos son toda el area de caminata?",
                "can I hike anywhere inside the park",
                "which zone are the official walks in",
            ],
            "Las caminatas de la norma del 4 de agosto de 2023 están en la Zona de Recreación General Exterior, sobre los senderos de ese reglamento. Usar otros caminos puede terminar en sanción. Un informe de 2024 sigue describiendo 12 senderos en esa zona. Confirma con el parque cuál te toca y no te salgas.",
            "El ecoturismo de esa norma va por la zona de recreación exterior y por sus senderos, no por el resto del parque. El informe de 2024 mantiene la cuenta de 12. Pregunta el tuyo y quédate en él.",
            ["activities.published_trails", "activities.what_to_visit", "activities.unlisted_activities"],
            [RES207, INFORME],
            ["zonificacion", "senderos", "sancion"],
            [],
            2,
        ),
        _entry(
            "activities.permitted_activity_menu",
            "actividades que el reglamento nombra",
            "explanation",
            [
                "qué actividades deja hacer el reglamento",
                "cuál es la lista oficial de cosas para hacer",
                "además de caminar, qué más está escrito",
                "foto, aves y educación entran en la misma lista?",
                "el parque publica un menú de actividades",
                "qué puedo pedir sin que sea un permiso raro",
                "relajarme también está permitido o solo caminar",
                "hay observacion de glaciares en la lista?",
                "que actividades nombra la resolucion de nevados",
                "sirve esa lista para cualquier sector",
                "what activities does the park regulation allow",
                "is there an official list of things visitors can do",
            ],
            "La norma del 4 de agosto de 2023 permite, en sus senderos, mirar el paisaje, pasadía, caminata de páramo, foto y video sin fines comerciales, relajación, senderismo interpretativo, observación de fauna, flora, geología y glaciares, y educación ambiental. Confirma el tramo con el parque antes de armar el día.",
            "Esa lista es de la norma de agosto de 2023 y vale dentro de los senderos que ella nombra. Elige una y pregunta al parque si tu sector la tiene habilitada ese día.",
            ["activities.what_to_visit", "activities.photography_amateur", "activities.published_trails"],
            [RES207],
            ["actividades", "reglamento", "lista"],
            [],
            3,
        ),
        _entry(
            "activities.paramo_walk",
            "caminata por el páramo",
            "explanation",
            [
                "puedo caminar por el páramo",
                "hay un paseo solo para ver frailejones",
                "la caminata de páramo es una actividad aparte",
                "me dejan recorrer el páramo si no voy a una cumbre",
                "eso de caminar entre frailejones está permitido",
                "puedo cruzar el pajonal por donde yo quiera",
                "el páramo se visita caminando o solo en carro",
                "una caminata suave de paramo, donde",
                "quiero ver el ecosistema sin subir a la nieve",
                "el reglamento nombra la caminata de paramo?",
                "can I just walk through the páramo",
                "is a páramo hike a listed activity",
            ],
            "La norma del 4 de agosto de 2023 nombra la caminata en ecosistema de páramo entre las actividades permitidas. Se hace por los senderos de esa norma, no por el pajonal abierto. Dile a tu operador que buscas esa caminata y confirma el sendero del día.",
            "Caminar el páramo sí está escrito, siempre sobre un sendero permitido. No abras trocha entre frailejones: pregunta cuál sendero te corresponde.",
            ["activities.permitted_activity_menu", "activities.published_trails", "activities.short_walks_brisas"],
            [RES207],
            ["paramo", "caminata", "sendero"],
            [],
            4,
        ),
        _entry(
            "activities.interpretive_hiking",
            "senderismo interpretativo en la visita",
            "explanation",
            [
                "qué es el senderismo interpretativo",
                "hay una caminata en la que te explican el lugar",
                "el sendero interpretativo es distinto de una cumbre",
                "puedo pedir que me cuenten el paisaje mientras camino",
                "eso de interpretación ambiental es una actividad",
                "el carreteable de Potosí es de interpretación?",
                "me sirven un recorrido para aprender, no para la cima",
                "senderismo interpretativo esta en el reglamento?",
                "quiero el paseo en el que explican el paramo",
                "hace falta un guía para que sea interpretativo",
                "what is an interpretive hike in the park",
                "can the walk include an explanation of the landscape",
            ],
            "La norma del 4 de agosto de 2023 incluye el senderismo interpretativo entre las actividades culturales permitidas. Quien explica el recorrido es un guía o intérprete del operador registrado. Pide esa caminata al operador de tu sector y no la confundas con una cumbre.",
            "El senderismo interpretativo está permitido: es la caminata en la que te explican el lugar, con un guía del operador. Confirma con él en qué sendero la hacen el día de tu visita.",
            ["activities.permitted_activity_menu", "activities.conservation_values_trail", "services.interpretive_guiding"],
            [RES207],
            ["interpretacion", "senderismo", "guia"],
            [],
            5,
        ),
        _entry(
            "activities.wellness_on_trail",
            "relajación durante la visita",
            "explanation",
            [
                "puedo ir al parque a relajarme",
                "hay alguna actividad de bienestar",
                "el reglamento deja descansar y contemplar",
                "eso de salud y relajación es un spa",
                "puedo hacer una parada larga solo para mirar",
                "bienestar significa meterme al agua",
                "está escrita la relajación como actividad",
                "quiero un plan tranquilo, sin cumbre",
                "relajacion y salud que permite la norma",
                "sirve ir sin prisa por el sendero",
                "is relaxation a permitted visit activity",
                "can I go just to rest and look at the landscape",
            ],
            "La norma del 4 de agosto de 2023 nombra relajación, bienestar y salud entre lo permitido, dentro de los senderos. No convierte las lagunas ni los termales en un baño: esa prohibición va aparte. Quédate en el recorrido autorizado y no entres al agua.",
            "Relajarte en el sendero sí está escrito. Bañarte en el agua del parque no. Confirma el recorrido con tu operador y deja el cuerpo fuera del agua.",
            ["activities.therapeutic_baths_banned", "activities.permitted_activity_menu", "activities.short_walks_brisas"],
            [RES207],
            ["relajacion", "bienestar", "sendero"],
            [],
            6,
        ),
        _entry(
            "activities.environmental_education",
            "salida de educación ambiental",
            "explanation",
            [
                "puedo llevar un grupo a una salida educativa",
                "la educación ambiental es una visita normal",
                "un colegio puede entrar a aprender",
                "eso cuenta como investigación o como visita",
                "hay caminatas para contar el ecosistema",
                "quiero una jornada pedagógica en el parque",
                "educación ambiental pide otro permiso",
                "la norma deja hacer educacion ambiental?",
                "si vamos a observar y no a colectar, qué pido",
                "una salida de clase es distinta de un proyecto",
                "can a school group do an environmental outing",
                "is environmental education a normal visit",
            ],
            "La norma del 4 de agosto de 2023 incluye la educación ambiental entre las actividades permitidas de la visita. Investigar o recoger muestras es otro permiso, no esta salida. Cuéntale al operador que el grupo va a aprender y confirma el sendero con el parque.",
            "Una salida para aprender entra en la visita. Si el plan es investigar o llevarse muestras, pide el permiso de investigación y no lo metas en la caminata.",
            ["activities.permitted_activity_menu", "activities.interpretive_hiking", "rules.research_permissions"],
            [RES207],
            ["educacion", "colegio", "visita"],
            [],
            7,
        ),
        _entry(
            "activities.ski_and_canyoning",
            "esquí de montaña y barranquismo",
            "procedure",
            [
                "puedo hacer esquí de montaña",
                "el barranquismo está permitido",
                "canyoning entra en el nevado",
                "sky de montaña es un paseo o un deporte",
                "hay cascadas para hacer rápel de cañón",
                "eso del canyoning lo ofrece el parque",
                "esquiar en nieve cuenta como montañismo",
                "barranquismo esta en la definicion de montanismo?",
                "quiero bajar un cañón, a quién le pido permiso",
                "el esquí de travesía se pide como club",
                "is ski mountaineering allowed for visitors",
                "does canyoning count as a normal hike",
            ],
            "La definición de montañismo del 4 de agosto de 2023 mete el esquí de montaña y el barranquismo o canyoning entre las actividades deportivas, no como un paseo. Pide el trámite de montañismo deportivo al parque antes de planearlo y no lo contrates como caminata.",
            "Esquí de montaña y barranquismo aparecen dentro del montañismo deportivo. No son un tour de un día: pregunta al parque el trámite del club antes de llevar el equipo.",
            ["activities.sport_mountaineering", "activities.unlisted_activities", "activities.regulated_sports"],
            [RES207],
            ["esqui", "barranquismo", "deporte"],
            [],
            8,
        ),
        _entry(
            "activities.cambio_climatico_trail",
            "sendero llamado Cambio climático",
            "fact",
            [
                "existe el sendero Cambio climático",
                "leí que había un sendero de cambio climático",
                "ese camino del centro todavía se llama así",
                "Cambio climático es Conejeras o es otro",
                "la noticia vieja de 2020 lo deja abierto",
                "puedo pedir el sendero Cambio climático",
                "en los senderos de ahora sale ese nombre",
                "cambio climatico sigue en la lista?",
                "un blog habla de ese sendero del Cisne",
                "lo reabrieron en la pandemia y ya",
                "is there still a Climate Change trail",
                "did the 2020 reopening keep that trail name",
            ],
            "Una noticia del parque del 9 de diciembre de 2020 nombra el sendero Cambio climático entre los que volvieron a recorrerse en el sector centro. La lista del 4 de agosto de 2023 no trae ese nombre. No lo tomes como abierto: pregunta al parque si ese sendero sigue existiendo.",
            "Cambio climático aparece en la noticia de diciembre de 2020 y no en los senderos de agosto de 2023. Pregunta al parque antes de buscarlo con ese nombre.",
            ["activities.conejeras_glacier_edge", "activities.published_trails", "activities.conservation_values_trail"],
            [NEWS2020, RES207],
            ["cambio climatico", "cisne", "sendero"],
            ["santa_isabel"],
            9,
        ),
        _entry(
            "activities.calvito_overnight",
            "pernocte en el punto Calvito",
            "fact",
            [
                "puedo dormir en Calvito",
                "Calvito es un camping del Tolima",
                "dónde queda ese punto de Calvito",
                "Calvito está abierto como los otros",
                "me cargan la maleta hasta Calvito",
                "Calvito es lo mismo que Arenales",
                "ese sitio es transitorio o definitivo",
                "calvito sirve para la noche antes de la cumbre?",
                "que carpa piden si duermo en calvito",
                "puedo hacer fogata en Calvito si hace mucho frío",
                "can I camp at Calvito",
                "is Calvito one of the Tolima overnight spots",
            ],
            "Calvito es uno de los tres puntos que la norma del 4 de agosto de 2023 habilitó, de forma transitoria, para dormir junto al Tolima. El porteo de maletas hasta Calvito está prohibido. Confirma con el parque si esa noche sigue autorizada y lleva carpa de tres o cuatro estaciones, sin fogata.",
            "Calvito es pernocte transitorio de 2023, no un camping garantizado, y no te pueden portear la maleta hasta allá. Pregunta si sigue abierto y arma la carpa de alta montaña sin fuego.",
            ["activities.camping_tolima", "activities.tolima_summit_schimmer", "activities.camping_where"],
            [RES207],
            ["calvito", "camping", "tolima"],
            ["tolima"],
            10,
        ),
        _entry(
            "activities.cocora_named_stops",
            "paradas entre Termales y Cocora",
            "fact",
            [
                "el sendero pasa por Acaime",
                "Estrella de Agua queda en la travesía",
                "puedo ver la Laguna del Encanto",
                "Valle de Placer es una parada del Tolima",
                "La Primavera y La Playa están en el camino",
                "Aquilino sale en la ruta al Cocora",
                "cuáles nombres hay después de Termales del Cañón",
                "acaime es del parque o del valle",
                "quiero el tramo de las fincas hacia Salento",
                "hay horas publicadas entre el cañón y Cocora",
                "which places are named between the hot springs and Cocora",
                "is Laguna del Encanto on the official trail",
            ],
            "Entre Termales del Cañón y el Valle del Cocora, la norma del 4 de agosto de 2023 nombra la Laguna el Encanto, el Valle de Placer, Aquilino, La Playa, La Primavera, Estrella de Agua y Acaime. No publica horas. Confirma con el parque que ese tramo esté habilitado para tu fecha.",
            "Esos nombres son paradas del sendero de 2023, no paseos sueltos, y la norma no les pone duración. Pregunta al parque si el tramo de tu fecha incluye el que buscas.",
            ["activities.combeima_cocora_traverse", "activities.termales_canon", "activities.chilcos_trail"],
            [RES207],
            ["cocora", "acaime", "encanto"],
            ["tolima"],
            11,
        ),
        _entry(
            "activities.south_operation_transitory",
            "operación transitoria del sur",
            "fact",
            [
                "los senderos del sur son definitivos",
                "la operación del Tolima es transitoria",
                "por qué el sur tiene una medida especial",
                "el reglamento dice que el sur es temporal",
                "esa norma cita otra resolución de 2022",
                "los senderos de cumbre del Tolima pueden cambiar",
                "el sur está en el mismo régimen que Brisas",
                "medida transitoria del nevado del tolima",
                "la resolucion 268 de 2022 que tiene que ver",
                "puedo confiar en que el sur sigue igual el otro año",
                "is the southern operation temporary",
                "why does the Tolima side have a transitional rule",
            ],
            "La norma del 4 de agosto de 2023 regula los senderos del sur como medida de manejo transitoria y la apoya en la Resolución 268 de 2022. Confirma con el parque si la ruta sur de tu fecha sigue en esa medida.",
            "El sur no quedó como un régimen cerrado: agosto de 2023 lo llama medida transitoria y cita la Resolución 268 de 2022. Pregunta al parque si tu ruta sigue bajo esa medida.",
            ["activities.sector_tolima", "activities.tolima_summit_schimmer", "activities.published_trails"],
            [RES207],
            ["sur", "transitorio", "tolima"],
            ["tolima"],
            12,
        ),
        _entry(
            "activities.mirador_laguna_otun",
            "mirador de la Laguna del Otún",
            "fact",
            [
                "hay un mirador de la Laguna del Otún",
                "el mirador de la laguna está en buen estado",
                "puedo llegar a un balcón sobre la laguna",
                "ese mirador es distinto de la Asomadera",
                "en qué estado está el mirador del Otún",
                "el informe dice que el mirador está regular",
                "cuánto se camina hasta el mirador de la laguna",
                "mirador laguna del otun queda en pereira?",
                "sirve ir solo por la foto desde ese mirador",
                "está cerrado por el estado de la estructura",
                "is there a viewpoint over Laguna del Otún",
                "what condition is the Otún lake overlook in",
            ],
            "El informe de necesidades de 2024 lista un mirador de la Laguna del Otún, en Pereira, y lo describe en condiciones regulares. No publica cuánto se camina hasta allá. Pregunta al operador si ese mirador entra en tu recorrido antes de contarlo.",
            "Hay un mirador de la laguna en el inventario de 2024, en estado regular, sin tiempo de caminata publicado. Confirma con el operador si lo vas a alcanzar.",
            ["activities.sector_laguna_otun", "activities.asomadera_day", "activities.potosi_laguna_road"],
            [INFORME],
            ["mirador", "otun", "laguna"],
            ["otun"],
            13,
        ),
        _entry(
            "activities.gazaperas_climb",
            "escalada y rapel en Gazaperas",
            "fact",
            [
                "puedo escalar en roca en el parque",
                "hay rapel en Arenales",
                "Gazaperas es un sitio de escalada",
                "el plan viejo dejaba rapel y ahora",
                "escalada en roca está en la norma de 2023",
                "dónde es el cordón de Gazaperas",
                "el operador pone el horario del rapel",
                "gazaperas sigue abierto para escalar?",
                "quiero rapel, no una cumbre de nieve",
                "eso de escalar piedra pide permiso",
                "is rock climbing at Gazaperas still allowed",
                "does the current rule still list rappelling",
            ],
            "El plan de manejo de 2017 describe escalada en roca y rapel por el cordón de Gazaperas, en Arenales, con permiso y horario del operador. La lista de actividades de la norma del 4 de agosto de 2023 no repite esas dos. Pregunta al parque si hoy las autoriza antes de llevar la cuerda.",
            "Gazaperas está en el plan de 2017, no en la lista de actividades de agosto de 2023. No llegues con el equipo de rapel sin una autorización actual del parque.",
            ["activities.regulated_sports", "activities.arenales_two_places", "activities.sport_mountaineering"],
            [PLAN, RES207],
            ["escalada", "rapel", "gazaperas"],
            ["brisas"],
            14,
        ),
        _entry(
            "activities.special_permit_activities",
            "cursos y carreras con permiso",
            "procedure",
            [
                "hay cursos de rescate en el Santa Isabel",
                "puedo hacer una carrera de orientación",
                "el yoga en el sendero está permitido",
                "actividades especiales piden permiso",
                "un curso de escala en el Tolima",
                "la carrera de orientación pasa por Brisas",
                "eso del yoga en Chilcos es oficial",
                "el informe las atribuye a la resolucion y ella no",
                "quiero entrenar en el parque, a quién escribo",
                "sin permiso me dejan dictar un curso",
                "are rescue courses something I can book",
                "do orientation races need a separate permit",
            ],
            "El informe de 2024 lista, como permiso especial, cursos de rescate en Santa Isabel y el Tolima, carreras de orientación en Brisas y hacia la laguna, y yoga en Los Chilcos. Se los atribuye a la norma de agosto de 2023, que no los nombra. Pide autorización escrita al parque.",
            "Esas actividades salen en el informe de 2024 como permiso especial, no en el texto de actividades de la norma que el informe cita. No las planees hasta que el parque te las autorice por escrito.",
            ["activities.regulated_sports", "activities.unlisted_activities", "activities.chilcos_trail"],
            [INFORME, RES207],
            ["permiso", "curso", "carrera"],
            [],
            15,
        ),
        _entry(
            "activities.la_cueva_start",
            "empezar la caminata en La Cueva",
            "fact",
            [
                "puedo empezar a caminar desde La Cueva",
                "La Cueva es salida de los senderos del Cisne",
                "de La Cueva se va a la Laguna Verde",
                "Potosí y La Cueva sirven para la misma visita",
                "hay un sendero que nace solo en La Cueva",
                "la ficha nombra La Cueva como acceso a las actividades",
                "me dejan el grupo en La Cueva y sigo a pie",
                "la cueva es cabaña o es un sendero",
                "desde la cueva se sube al santa isabel?",
                "cuál cabaña es el inicio, Cisne o La Cueva",
                "can I start the Cisne hikes at La Cueva",
                "is La Cueva a trailhead for those activities",
            ],
            "La ficha del parque dice que las actividades del Cisne también se entran desde las cabañas La Cueva y Potosí, además del centro El Cisne. No describe un sendero que salga solo de La Cueva. Confirma con tu operador desde qué cabaña empieza tu caminata.",
            "La Cueva y Potosí son puertas de las actividades del Cisne, junto con el centro. La ficha no les inventa un sendero propio: pregunta al operador cuál es tu punto de salida.",
            ["activities.sector_santa_isabel", "activities.laguna_verde", "activities.cisne_viewpoints"],
            [PNN],
            ["la cueva", "cisne", "inicio"],
            ["santa_isabel"],
            16,
        ),
        _entry(
            "activities.sietecuerales_point",
            "punto Sietecuerales en Conejeras",
            "fact",
            [
                "qué es Sietecuerales",
                "Sietecuerales queda en Conejeras",
                "ese punto del sendero todavía existe",
                "leí Sietecuerales en una noticia vieja",
                "es un mirador o solo un tramo empinado",
                "cuánto falta de Sietecuerales al glaciar",
                "la noticia de 2016 describe ese punto",
                "sietecuerales es un descanso del borde",
                "me sirven de referencia ese nombre",
                "sigue señalizado Sietecuerales",
                "what is Sietecuerales on the Conejeras trail",
                "is Sietecuerales still a named point",
            ],
            "Una noticia del parque, actualizada el 22 de diciembre de 2016, llama Sietecuerales a un punto del sendero Conejeras donde hicieron terraceo. No da duración ni dice que sea un mirador. Pregunta al operador si ese punto sigue en el recorrido de tu fecha.",
            "Sietecuerales es un nombre de la adecuación de Conejeras en 2016, no una ficha de visita actual. Pregunta si todavía lo usan como referencia en el sendero.",
            ["activities.conejeras_glacier_edge", "activities.santa_isabel_summit", "activities.cambio_climatico_trail"],
            [NEWS2016],
            ["sietecuerales", "conejeras", "sendero"],
            ["santa_isabel"],
            17,
        ),
        _entry(
            "activities.aguacerales_stop",
            "parada Aguacerales del norte",
            "fact",
            [
                "qué es Aguacerales",
                "Aguacerales queda entre Brisas y Arenales",
                "el carro para en Aguacerales",
                "hay una cascada que se llama Aguacerales",
                "ese nombre está en el sendero del valle",
                "puedo bajarme en Aguacerales",
                "aguacerales es un mirador o una parada",
                "cuanto hay de brisas a aguacerales",
                "sale en el recorrido del Ruiz",
                "la norma nombra Aguacerales",
                "what is the Aguacerales stop",
                "is Aguacerales on the way to the valley",
            ],
            "En la norma del 4 de agosto de 2023, Aguacerales es una parada del sendero norte: va entre el centro de interpretación de Brisas y Arenales, camino al Valle de las Tumbas. No publica duración ni la describe como cascada. Confirma con tu operador si el carro para ahí.",
            "Aguacerales es un nombre del carreteable, entre Brisas y Arenales, no un paseo aparte. Pregunta al operador si esa parada está en el tramo de tu fecha.",
            ["activities.north_route_stops", "activities.brisas_valle_tumbas", "activities.arenales_two_places"],
            [RES207],
            ["aguacerales", "brisas", "parada"],
            ["brisas"],
            18,
        ),
        _entry(
            "activities.ruiz_glacier_edge",
            "borde glaciar del Ruiz",
            "rule",
            [
                "puedo ir al borde del glaciar del Ruiz",
                "el refugio hacia el hielo del Ruiz está cerrado",
                "ese borde sigue restringido por el volcán",
                "la carta de 2026 también cubre el filo de hielo",
                "Refugio y borde glaciar es un sendero",
                "me dejan ver la nieve del Ruiz de cerca",
                "el informe de 2024 todavía lo marca restringido",
                "borde del ruiz por el refugio se puede",
                "es distinto de la cima prohibida",
                "hay algún tramo de hielo en el norte",
                "can I walk the Ruiz glacier edge",
                "is the refuge-to-ice route still restricted",
            ],
            "El informe de 2024 sigue rotulando el tramo Refugio–borde glaciar del Ruiz como restringido por la actividad volcánica. La carta del parque del 11 de mayo de 2026 prohíbe la cima y el cráter. No planees ese borde: pregunta al parque si hay algún tramo de hielo autorizado en el norte.",
            "El borde del Ruiz por el Refugio sigue marcado como restringido en el informe de 2024, y la cima está prohibida por la carta de mayo de 2026. Pregunta antes de buscar hielo en el norte.",
            ["activities.ruiz_summit_closed", "activities.snow_and_glacier_access", "activities.conejeras_glacier_edge"],
            [INFORME, CARTA],
            ["ruiz", "glaciar", "refugio"],
            ["brisas"],
            19,
        ),
        _entry(
            "activities.cycling_roads_2017",
            "vías del ciclomontañismo en el plan",
            "fact",
            [
                "por dónde puedo ir en bici dentro del parque",
                "el plan nombra las vías de ciclomontañismo",
                "Brisas Olleta Cisne es ruta de bici",
                "se puede pedalear hasta el Muelle",
                "Cisne Santa Bárbara Potosí está en el plan",
                "la bici va por las vías de los carros",
                "el plan de 2026 repite esas vías",
                "ciclomontañismo es por carretera o por sendero",
                "puedo llevar la bici al valle y seguir",
                "esas tres vias siguen vigentes?",
                "which roads did the management plan allow for bikes",
                "is the bike route still Brisas to Olleta",
            ],
            "El plan de manejo de 2017 define el ciclomontañismo como bici de montaña por vías autorizadas para vehículos, y nombra Brisas–Olleta–Cisne, Cisne–Santa Bárbara–Potosí y Potosí–Muelle. La edición corta del plan 2026 no repite esas vías. Confirma la ruta con el parque antes de llevar la bici.",
            "Esas tres vías son del plan de 2017. El texto corto de 2026 no las vuelve a escribir. Pregunta al parque cuál, si alguna, está autorizada para tu fecha.",
            ["activities.regulated_sports", "activities.brisas_valle_tumbas", "activities.potosi_laguna_road"],
            [PLAN, POE],
            ["bici", "ciclomontañismo", "vias"],
            [],
            20,
        ),
        _entry(
            "activities.conejeras_hut",
            "caseta del sendero Conejeras",
            "fact",
            [
                "hay una caseta en Conejeras",
                "la caseta de Conejeras vende algo",
                "ese kiosco del sendero todavía está",
                "puedo guarecerme en la caseta",
                "Conejeras tiene infraestructura o solo camino",
                "el informe lista la caseta",
                "queda en Villamaría esa caseta",
                "la caseta es un refugio para dormir",
                "que hay dentro de la caseta de conejeras",
                "sirve como punto de control",
                "is there a hut on the Conejeras trail",
                "what does the Conejeras shelter offer",
            ],
            "El informe de necesidades de 2024 incluye una caseta Conejeras en la infraestructura de ese sector, en Villamaría. No describe qué hay adentro ni si se puede dormir ahí. Pregunta al operador qué encuentras en esa caseta el día de la caminata.",
            "La caseta Conejeras está en el inventario de 2024 y no trae una lista de servicios. No la cuentes como refugio: pregunta qué hay ese día.",
            ["activities.conejeras_glacier_edge", "activities.santa_isabel_summit", "activities.sietecuerales_point"],
            [INFORME],
            ["caseta", "conejeras", "infraestructura"],
            ["santa_isabel"],
            21,
        ),
    ]
    return rows


def apply(section: dict) -> dict:
    by_id = {entry["id"]: entry for entry in section["entries"]}

    _set_short(
        by_id["activities.combeima_cocora_traverse"],
        "Ese tramo Juntas–Perlas hasta Termales del Cañón se cerró con la Resolución 017 del 17 de enero de 2024. Otra resolución, del 26 de diciembre de 2024, ordenó abrirlo y volvió a autorizar visitantes y servicios ecoturísticos. Confirma con el parque que esa apertura siga vigente antes de salir.",
        "Entre enero y diciembre de 2024 ese tramo pasó de cierre a apertura. La resolución del 26 de diciembre de 2024 autoriza de nuevo el paso. Pregunta al parque si sigue así.",
        "La Resolución 017 prohibió visitantes y servicios en Juntas–Perlas–La Pradera–Estambul–Alto Nieves–Escuela El Salto–Termales del Cañón. La resolución del 26 de diciembre de 2024 ordena abrir el mismo tramo. Confirma ese estado: un cierre nuevo puede publicarse después.",
    )
    by_id["activities.combeima_cocora_traverse"]["sources"] = [RES017, RES708, RES207]

    _set_short(
        by_id["activities.asomadera_day"],
        "La norma del 4 de agosto de 2023 permite ir y volver el mismo día, sin dormir, hasta la Asomadera desde Potosí. Muelle es un punto del camino, no un bote. La ficha turística de Caldas estima unas 3 horas y dificultad medio-baja; el parque no publica ese tiempo. Confírmalo con tu operador.",
        "La pasadía llega hasta la Asomadera y Muelle no es un embarcadero. Las 3 horas y la dificultad medio-baja son de la ficha de Caldas, no del parque. Confirma el tramo con el operador.",
    )
    by_id["activities.asomadera_day"]["sources"] = [RES207, CALDAS, PNN]

    _set_short(
        by_id["activities.otun_cocora_traverse"],
        "La norma del 4 de agosto de 2023 describe la travesía desde la Laguna del Otún por la azufrera, la Laguna del Mosquito, la cuchilla de Berlín, la finca Buenos Aires y el Mojón de Cárdenas hasta el Valle del Cocora. No publica kilómetros ni horas. Confírmala con el parque antes de salir.",
        "Buenos Aires y el Mojón de Cárdenas van en esa travesía, con la azufrera, El Mosquito y Berlín. La norma no da tiempo. Pregunta al parque si puedes hacerla en tu fecha.",
    )

    _set_short(
        by_id["activities.ruiz_summit_closed"],
        "La carta del parque del 11 de mayo de 2026 prohíbe la cima y el cráter del Nevado del Ruiz. La ficha nombra La Olleta y La Piraña como cráteres del complejo, y los senderos de 2023 no los incluyen. El recorrido del norte es el carreteable hasta el Valle de las Tumbas. Pregunta al parque antes de buscar otro filo.",
        "Cima y cráter del Ruiz siguen prohibidos por la carta del 11 de mayo de 2026. La Olleta y La Piraña están nombradas como cráteres, no como sendero de 2023. Confirma cualquier otro filo con el parque.",
        "La carta, radicado 20266200003411, atribuye la prohibición de cima y cráter a la Resolución 207 del 4 de agosto de 2023. En esa resolución, el ascenso turístico descrito con nombre es el del Tolima por el glaciar Schimmer. La ficha solo presenta La Olleta y La Piraña como cráteres del complejo.",
    )
    by_id["activities.ruiz_summit_closed"]["sources"] = [CARTA, RES207, PNN]

    _set_short(
        by_id["activities.camping_brisas_restricted"],
        "El informe de 2024 dice que el camping de Arenales no está habilitado por la actividad volcánica. La norma del 4 de agosto de 2023 ya lo tenía restringido. No lo cuentes como sitio disponible. Si el parque te autoriza otro punto, pregunta cuál y lleva carpa de tres o cuatro estaciones, sin fogata.",
        "Arenales no está habilitado para acampar, según el informe de 2024, por la actividad volcánica. No lo armes en el plan. Si te autorizan otro punto, confirma cuál y usa carpa de alta montaña, sin fogata.",
    )
    by_id["activities.camping_brisas_restricted"]["sources"] = [INFORME, RES207]

    _set_short(
        by_id["activities.camping_otun"],
        "La norma del 4 de agosto de 2023 deja el camping de la Laguna del Otún en proceso de acondicionamiento. El informe de 2024 describe la cabaña del sector en buenas condiciones y no dice que el camping ya esté abierto. Confirma con el parque; si te autorizan, lleva carpa de tres o cuatro estaciones y no hagas fogata.",
        "Que la cabaña esté en buen estado en el informe de 2024 no abre el camping: en 2023 seguía en acondicionamiento. Pregunta al parque y, si hay permiso, lleva carpa de alta montaña sin fogata.",
    )
    by_id["activities.camping_otun"]["sources"] = [RES207, INFORME]

    _set_short(
        by_id["activities.camping_cisne"],
        "La norma del 4 de agosto de 2023 condiciona el camping de El Cisne a la actividad volcánica o a la operación. El informe de 2024 dice que el centro está en buenas condiciones y sigue nombrando camping, sin abrirlo por sí solo. Confirma con el parque; si te autorizan, carpa de tres o cuatro estaciones y sin fogata.",
        "El centro puede estar en buen estado y el camping seguir condicionado, como en la norma de 2023. No llegues a dormir sin confirmación. Si te autorizan, usa carpa de alta montaña y no hagas fogata.",
    )
    by_id["activities.camping_cisne"]["sources"] = [RES207, INFORME]

    _set_short(
        by_id["activities.camping_where"],
        "Acampa solo donde el parque te confirme para tu fecha. El informe de 2024 dice que Arenales no está habilitado por actividad volcánica, y la norma de 2023 no garantiza los demás puntos. Confirma el lugar con Parques Nacionales y tu operador antes de planear la noche.",
        "Ningún camping de la norma de 2023 queda garantizado hoy, y Arenales figura no habilitado en el informe de 2024. Pregunta el punto exacto antes de cargar la carpa.",
    )
    by_id["activities.camping_where"]["sources"] = [RES207, INFORME]

    _set_short(
        by_id["activities.laguna_verde"],
        "Puedes caminar a la Laguna Verde por el sendero habilitado, desde El Cisne, La Cueva o Potosí. En la norma del 4 de agosto de 2023 ese mirador depende de que haya operación de servicios. El informe de 2024 lo describe en condiciones regulares. Confirma con tu operador que haya salida ese día.",
        "El mirador de Laguna Verde sigue condicionado a la operación y, en el informe de 2024, está en estado regular. Pregunta si hay salida desde El Cisne, La Cueva o Potosí.",
    )
    by_id["activities.laguna_verde"]["sources"] = [PNN, RES207, INFORME]

    _set_short(
        by_id["activities.geology_watching"],
        "En Brisas puedes hacer observación geológica, y Cisne, Otún y Quindío–Dulima también. La norma del 4 de agosto de 2023 nombra además la observación glaciológica. Hazla desde el recorrido autorizado de tu sector. Si vas a tomar muestras o a investigar, pide el permiso del parque.",
        "Mirar el terreno y el glaciar está en la visita y en la norma de agosto de 2023. Hazlo desde el sendero o el carreteable. Para muestras o investigación, pide el permiso.",
    )
    by_id["activities.geology_watching"]["sources"] = [PNN, RES207]

    _set_short(
        by_id["activities.unlisted_activities"],
        "Bote y picnic no están en la norma del 4 de agosto de 2023. El esquí de montaña solo aparece dentro del montañismo deportivo. El informe de 2024 lista caminata nocturna en Brisas y Cisne como permiso especial, pero esa norma no la nombra. Pregunta al parque antes de contarla.",
        "Ni el bote ni el picnic están en la norma. El esquí de montaña es deporte, no un paseo. La caminata de noche solo aparece como permiso en el informe de 2024: pídela por escrito al parque.",
    )
    by_id["activities.unlisted_activities"]["sources"] = [RES207, INFORME]

    _set_short(
        by_id["activities.therapeutic_baths_banned"],
        "La norma del 4 de agosto de 2023 no permite baños terapéuticos en los cuerpos de agua del parque. El informe de 2024 lista «baños de salud» como actividad especial y se los atribuye a esa norma, que no usa esa frase. No entres al agua y confirma con el parque qué actividad de bienestar sí autoriza.",
        "Aunque el informe de 2024 hable de baños de salud, la norma que cita prohíbe los baños terapéuticos. No entres al agua y pregunta qué otra cosa de bienestar está autorizada.",
    )
    by_id["activities.therapeutic_baths_banned"]["sources"] = [RES207, INFORME]

    _set_short(
        by_id["activities.published_trails"],
        "Usa el sendero que el parque te confirme. La norma del 4 de agosto de 2023 sanciona otros caminos y no deja ofertar lo que no está en ese reglamento. El informe de 2024 sigue en 12 senderos. De 26 rutas evaluadas, 15 salieron favorables en el plan corto, sin nombres. Pregunta cuál está abierto hoy.",
        "Doce senderos siguen siendo la cuenta del informe de 2024. Las 15 rutas favorables del plan corto no traen nombres, y lo que no está en la norma de 2023 no se puede ofertar. Confirma el tuyo con el parque.",
    )
    by_id["activities.published_trails"]["sources"] = [RES207, INFORME, POE]

    known = set(by_id)
    for entry in _new_entries():
        if entry["id"] in known:
            raise ValueError(f"duplicate id {entry['id']}")
        section["entries"].append(entry)
    return section
