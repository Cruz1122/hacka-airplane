"""Generate the curated weather_volcano knowledge section from reviewed evidence."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from round2_entries import extra_entries


ROOT = Path(__file__).parents[3]
OUTPUT = ROOT / "data/knowledge/sections/weather_volcano.json"
SECTIONS = ROOT / "data/knowledge/sections"
DATE = "2026-11-21"

PNN = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
IDEAM = (
    "http://www.ideam.gov.co/web/otros-ecosistemas/investigacion-y-publicaciones"
    "?_31_INSTANCE_x5l2d9DnqhhZ_struts_action=%2Fimage_g"
)
SGC_ALERTS = "https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx"
SGC_TRANSITIONS = (
    "https://www2.sgc.gov.co/Noticias/Paginas/"
    "Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx"
)
SGC_BULLETINS = (
    "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/"
    "boletines-volcan-nevado-del-ruiz.aspx"
)
SGC_LATEST_BULLETIN = (
    "https://www2.sgc.gov.co/Noticias/boletinesDocumentos/"
    "Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf"
)
UNGRD = (
    "http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/"
    "19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1"
)
SGC_GASES = (
    "https://www2.sgc.gov.co/Temas-destacados/Documents/"
    "Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf"
)
SNGRD_GASES = "https://www2.sgc.gov.co/sgc/volcanes/VolcanAzufral/Paginas/Mapa-de-amenaza.aspx"
PNN_RESOLUTION = (
    "https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/"
    "Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf"
)
PNN_RESOLUTION_259 = (
    "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/10/"
    "Res.-No.-259-del-09-de-octubre-de-2024-PFFO-022-2024.pdf"
)
OVSM = (
    "https://centrodeinformacion.manizales.gov.co/"
    "el-detras-de-camaras-del-monitoreo-a-un-volcan-amenazante/"
)
SNOW = (
    "https://www.parquesnacionales.gov.co/sala-prensa/noticias/"
    "una-de-las-nevadas-mas-grandes-del-ano-cubre-el-parque-nacional-natural-los-nevados/"
)


def source(label: str, url: str) -> dict[str, str]:
    return {"label": label, "url": url, "retrieved_at": DATE}


def entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    short: str,
    variants: list[str],
    sources: list[dict[str, str]],
    hard_negatives: list[str],
    related: list[str],
    tags: list[str],
) -> dict:
    if len(examples) < 12:
        raise ValueError(f"{entry_id} needs at least 12 examples")
    if len(set(examples)) != len(examples):
        raise ValueError(f"{entry_id} has duplicate examples")
    return {
        "id": f"weather_volcano.{entry_id}",
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "needs": [],
        "answer": {"short": short, "variants": variants},
        "sources": sources,
        "last_verified": DATE,
        "related": [f"weather_volcano.{item}" for item in related],
        "tags": tags,
    }


entries = [
    entry(
        "park_weather",
        "clima general del parque",
        "explanation",
        [
            "cómo es el clima en Los Nevados",
            "qué tiempo suele hacer en el parque",
            "clima general de los nevados",
            "qué clima hace por allá arriba",
            "el clima cambia mucho en la montaña",
            "qué tal está el clima allá arriba",
            "es frío el parque nacional",
            "cómo es el tiempo en la alta montaña",
            "clima de Los Nevados sin pronóstico",
            "como es el clima alla en los nevados",
            "parce que clima hace en el parque",
            "what is the weather like in Los Nevados",
            "is the park weather cold",
        ],
        "El IDEAM describe la alta montaña colombiana como un clima intertropical frío, con cambios importantes durante el día. En Los Nevados el tiempo también depende de la topografía y la altura; para tu fecha, revisa el pronóstico oficial.",
        [
            "Es un clima frío de alta montaña y puede variar bastante en el día. No tomes esta descripción general como el pronóstico de tu visita: consulta el IDEAM.",
        ],
        [
            source("IDEAM, clima en alta montaña", IDEAM),
            source("Parques Nacionales, ficha PNN Los Nevados", PNN),
        ],
        ["qué ropa llevar al parque los nevados", "está abierto hoy"],
        ["rainy_seasons", "weather_by_elevation", "current_forecast"],
        ["clima", "alta montaña", "tiempo"],
    ),
    entry(
        "rainy_seasons",
        "lluvias por temporada",
        "fact",
        [
            "cuándo llueve más en Los Nevados",
            "cómo se distribuyen las lluvias del año",
            "hay dos temporadas de lluvia",
            "cuáles son los meses húmedos del parque",
            "cuándo son las épocas secas",
            "llueve todo el año en la montaña",
            "qué meses tienen más lluvia allá",
            "temporadas de lluvia y de verano en los nevados",
            "la lluvia es bimodal en el parque",
            "en que meses llueve mas por el nevado",
            "toca esperar temporada seca para ir",
            "does it rain all year in the park",
            "when are the rainy seasons",
        ],
        "El IDEAM identifica dos periodos húmedos aproximados, de marzo a mayo y de septiembre a noviembre, y dos secos, de diciembre a febrero y de junio a agosto. Es un patrón climático, no una garantía para el día de tu visita; comprueba el pronóstico.",
        [
            "La lluvia tiene un patrón de dos periodos húmedos y dos secos, pero puede cambiar de un día a otro. Consulta el pronóstico antes de salir.",
        ],
        [
            source("IDEAM, clima en alta montaña", IDEAM),
            source("Parques Nacionales, ficha PNN Los Nevados", PNN),
        ],
        ["está abierto hoy", "qué pasó en Armero"],
        ["park_weather", "current_forecast", "summit_visibility"],
        ["lluvia", "temporada", "precipitación"],
    ),
    entry(
        "weather_by_elevation",
        "clima según la altura",
        "explanation",
        [
            "el clima cambia al subir",
            "hace el mismo tiempo en todo el parque",
            "cómo varía el clima por altura",
            "diferencia de temperatura entre sectores",
            "por qué arriba hace más frío",
            "clima de páramo y zona nival",
            "cada piso térmico tiene otro clima",
            "qué pasa con el tiempo mientras asciendes",
            "temperatura según la elevación en los nevados",
            "como cambia el clima con la altura",
            "se siente distinto el clima entre abajo y arriba",
            "weather by elevation in Los Nevados",
            "does altitude change the weather there",
        ],
        "La temperatura y la precipitación no son iguales en todo el recorrido: el IDEAM reporta variación con la altura y un gradiente térmico en la alta montaña. No extrapoles el tiempo de un pueblo o acceso a la cota más alta; revisa las condiciones del sector que visitarás.",
        [
            "La altura modifica las condiciones meteorológicas, así que un pronóstico local no representa necesariamente todo el parque. Verifica el sector de tu ruta.",
        ],
        [
            source("IDEAM, clima en alta montaña", IDEAM),
            source("IDEAM, actualización climática de Caldas", "https://bart.ideam.gov.co/meteorologia/NOTAS_TECNICAS/NT_IDEAM-2025-003_ACTUALIZACION_CALDAS_LANG.pdf"),
        ],
        ["es pesado para el cuerpo ir al parque", "qué ropa llevar al parque los nevados"],
        ["park_weather", "rainy_seasons", "summit_visibility"],
        ["altura", "temperatura", "pisos térmicos"],
    ),
    entry(
        "summit_visibility",
        "niebla y visibilidad de cumbres",
        "safety",
        [
            "se va a ver la cumbre del Ruiz",
            "puedo ver el nevado desde el recorrido",
            "habrá visibilidad para tomar fotos",
            "la niebla tapa la cima",
            "qué tan despejado estará arriba",
            "se alcanza a ver la cumbre hoy",
            "las nubes dejan ver el volcán",
            "me garantizan ver el nevado",
            "cómo saber si habrá buena visibilidad",
            "se ve el ruiz con lluvia",
            "que tal la visibilidad en la cima",
            "can I see the summit during my visit",
            "will the volcano be visible from the trail",
        ],
        "No se puede garantizar que veas una cumbre: el IDEAM describe humedad alta y nubosidad variable en la alta montaña, y Parques documentó una nevada asociada a nubosidad densa. Revisa el pronóstico del sector y sigue solo las indicaciones oficiales del recorrido.",
        [
            "La cumbre puede quedar oculta por nubes o niebla; no hay garantía de visibilidad. Consulta el pronóstico y disfruta el paisaje que esté visible.",
        ],
        [
            source("IDEAM, clima en alta montaña", IDEAM),
            source("Parques Nacionales, nevada de octubre de 2025", SNOW),
        ],
        ["está abierto hoy", "qué ropa llevar al parque los nevados"],
        ["current_forecast", "park_weather", "rainy_seasons"],
        ["niebla", "nubosidad", "visibilidad", "cumbre"],
    ),
    entry(
        "snow_and_hail",
        "nieve y granizo",
        "fact",
        [
            "nieva en Los Nevados",
            "hay nieve en el parque",
            "se puede ver nieve en el Ruiz",
            "cuándo cae nieve en la alta montaña",
            "la nevada es normal allá arriba",
            "puede caer granizo en el recorrido",
            "nieve o granizo en los nevados",
            "qué tan frecuente es la nieve",
            "el parque se cubre de nieve",
            "ha nevado por el nevado del ruiz",
            "hay nieve hoy en la cumbre",
            "does it snow in Los Nevados",
            "can there be hail on the trail",
        ],
        "Parques Nacionales documentó una nevada amplia en octubre de 2025, favorecida por nubosidad húmeda, bajas temperaturas y cambios de presión. Esa noticia no permite pronosticar nieve o granizo para tu fecha; revisa el pronóstico y los avisos oficiales.",
        [
            "Sí se han documentado nevadas en la alta montaña, pero no puedo prometer nieve ni confirmar granizo para tu visita. Consulta las condiciones actualizadas del sector.",
        ],
        [
            source("Parques Nacionales, nevada de octubre de 2025", SNOW),
            source("IDEAM, clima en alta montaña", IDEAM),
        ],
        ["qué ropa llevar al parque los nevados", "me dio dolor de cabeza al llegar arriba"],
        ["summit_visibility", "current_forecast", "weather_by_elevation"],
        ["nieve", "granizo", "alta montaña"],
    ),
    entry(
        "current_forecast",
        "pronóstico para la visita",
        "procedure",
        [
            "dónde miro el pronóstico del parque",
            "qué clima hará mañana en Los Nevados",
            "va a llover el día de mi visita",
            "cómo reviso el tiempo antes de viajar",
            "pronóstico para el fin de semana en Brisas",
            "hay pronóstico para el sector Otún",
            "necesito el clima actualizado del nevado",
            "dónde consulto el tiempo por sector",
            "cómo saber si estará despejado",
            "pronostico de mañana para los nevados",
            "toca mirar el IDEAM antes de subir",
            "what is the forecast for the park",
            "where can I check the weather forecast",
        ],
        "Consulta los “Pronósticos y Alertas” del IDEAM y busca el sector y la fecha de tu visita. Esta ficha offline no confirma el tiempo en tiempo real; vuelve a comprobarlo antes de salir.",
        [
            "Para una fecha concreta, revisa el servicio de pronósticos del IDEAM. El clima puede cambiar y esta respuesta no sustituye una consulta actualizada.",
        ],
        [
            source("IDEAM, portal de pronósticos y alertas", "https://www.ideam.gov.co/"),
            source("Parques Nacionales, ficha PNN Los Nevados", PNN),
        ],
        ["está abierto hoy", "qué pasó en Armero"],
        ["park_weather", "rainy_seasons", "bulletin_channels"],
        ["pronóstico", "fecha", "sector"],
    ),
    entry(
        "alert_yellow_meaning",
        "alerta amarilla y visita",
        "safety",
        [
            "qué significa alerta amarilla del Ruiz",
            "qué implica el amarillo para un turista",
            "puedo ir con alerta amarilla",
            "cómo entender el estado amarillo",
            "alerta amarilla es peligroso",
            "qué cambios indica el amarillo",
            "el nivel amarillo permite entrar",
            "qué hago si el Ruiz está amarillo",
            "amarillo significa erupción inminente",
            "que quiere decir alerta amarilla del volcan",
            "toca seguir al guardaparque con alerta amarilla",
            "what does yellow volcanic alert mean",
            "does yellow alert mean the park is closed",
        ],
        "Para el SGC, la alerta amarilla significa un volcán activo con cambios respecto a su nivel base y otras manifestaciones; puede incluir emisiones esporádicas de ceniza. No decide por sí sola tu ingreso: consulta el boletín vigente y acata al personal del Parque, porque el acceso puede restringirse.",
        [
            "Amarilla no equivale automáticamente a cierre ni a permiso de entrada. Revisa el boletín del SGC y las instrucciones del Parque antes de acercarte.",
        ],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
        ["está abierto hoy", "qué pasó en Armero"],
        ["alert_orange_meaning", "current_alert", "volcanic_closures"],
        ["alerta amarilla", "SGC", "actividad volcánica"],
    ),
    entry(
        "alert_orange_meaning",
        "significado de alerta naranja",
        "safety",
        [
            "qué significa alerta naranja del Ruiz",
            "qué implica naranja para los visitantes",
            "cómo actuar si el volcán está naranja",
            "alerta naranja es erupción",
            "qué cambios hay en estado naranja",
            "puedo subir con alerta naranja",
            "qué restricciones trae el naranja",
            "naranja significa que ya está haciendo erupción",
            "qué debe hacer un turista ante alerta naranja",
            "que hago si cambian a naranja",
            "toca cancelar la visita con alerta naranja",
            "what does orange volcanic alert mean",
            "is orange alert an eruption",
        ],
        "Según el SGC, la alerta naranja indica cambios importantes en los parámetros monitoreados y una mayor probabilidad de erupciones mayores; no significa necesariamente que ya haya una erupción. Para una visita, espera las instrucciones oficiales y respeta cualquier restricción o evacuación.",
        [
            "Naranja es un estado de mayor inestabilidad, no una predicción horaria de erupción. No subas por tu cuenta: revisa el SGC y sigue a las autoridades.",
        ],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
        ["está abierto hoy", "qué ropa llevar al parque los nevados"],
        ["alert_yellow_meaning", "alert_red_meaning", "current_alert"],
        ["alerta naranja", "restricción", "evacuación"],
    ),
    entry(
        "alert_red_meaning",
        "respuesta ante alerta roja",
        "safety",
        [
            "qué significa alerta roja del Ruiz",
            "qué implica rojo para los turistas",
            "qué hago si el volcán está en rojo",
            "alerta roja significa erupción",
            "se puede visitar con alerta roja",
            "qué ordena el estado rojo",
            "rojo es evacuación obligatoria",
            "cómo actuar ante alerta roja volcánica",
            "qué pasa con los accesos en rojo",
            "que quiere decir rojo en el semaforo volcanico",
            "toca alejarse si hay alerta roja",
            "what does red volcanic alert mean",
            "is the park open during red alert",
        ],
        "Para el SGC, la alerta roja corresponde a un volcán en erupción y contempla evacuación obligatoria de las zonas que puedan ser afectadas, según el volcán y el mapa de amenaza. No te acerques ni intentes ingresar: sigue las instrucciones de las autoridades.",
        [
            "Roja significa erupción en curso según el esquema del SGC. Si se declara, aléjate y cumple la evacuación o restricción que ordenen las autoridades.",
        ],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
        ["está abierto hoy", "qué pasó en Armero"],
        ["alert_orange_meaning", "current_alert", "ash_actions"],
        ["alerta roja", "erupción", "evacuación"],
    ),
    entry(
        "alert_states_nonsequential",
        "cambio entre estados de alerta",
        "explanation",
        [
            "los colores del volcán son una escala que siempre sube",
            "el Ruiz debe pasar por amarillo antes de naranja",
            "puede saltar de amarillo a rojo",
            "cómo cambian los estados de alerta",
            "los colores predicen días para una erupción",
            "alerta naranja significa erupción en días",
            "la alerta volcánica es progresiva",
            "qué significa que cambie el color",
            "el volcán puede volver a bajar de alerta",
            "como se pasa de un estado a otro",
            "toca esperar que pase por todos los colores",
            "are volcanic alert colors sequential",
            "can a volcano jump from yellow to red",
        ],
        "El SGC aclara que los estados de alerta no son una secuencia obligatoria y no asignan un plazo de días o semanas para una erupción. Por eso, consulta siempre el boletín más reciente en vez de inferir el riesgo solo por el color anterior.",
        [
            "Los estados pueden cambiar sin recorrer todos los colores y no son un reloj de cuenta regresiva. Usa el boletín vigente para decidir tu visita.",
        ],
        [source("SGC, explicación del esquema de alertas", SGC_TRANSITIONS)],
        ["está abierto hoy", "cuándo se creó el parque"],
        ["alert_yellow_meaning", "alert_orange_meaning", "current_alert"],
        ["estados", "colores", "alerta"],
    ),
    entry(
        "current_alert",
        "alerta vigente del Ruiz",
        "procedure",
        [
            "qué alerta tiene hoy el Nevado del Ruiz",
            "cuál es el estado actual del Ruiz",
            "dónde miro la alerta de hoy",
            "hay alerta volcánica para visitar",
            "qué nivel reporta el SGC ahora",
            "sigue activo el volcán hoy",
            "último estado de actividad del Ruiz",
            "cómo confirmo la alerta vigente",
            "hay novedades del volcán para el viaje",
            "alerta actual del nevado ruiz",
            "toca revisar el boletín antes de ir",
            "what is the current Ruiz alert",
            "where do I check the current volcano status",
        ],
        "No tomes esta ficha como confirmación del estado vigente: la alerta puede cambiar. Antes de viajar, abre el boletín más reciente del SGC sobre el Nevado del Ruiz y sigue también las indicaciones de Parques y de las autoridades locales.",
        [
            "Para saber el estado de hoy, consulta directamente el boletín más reciente del SGC. Aquí no se fija una alerta actual porque puede cambiar.",
        ],
        [
            source("SGC, boletines del Nevado del Ruiz", SGC_BULLETINS),
            source("SGC, boletín semanal del 10 al 16 de noviembre de 2026", SGC_LATEST_BULLETIN),
        ],
        ["está abierto hoy", "qué ropa llevar al parque los nevados"],
        ["bulletin_channels", "alert_yellow_meaning", "volcanic_closures"],
        ["alerta", "estado actual", "Ruiz"],
    ),
    entry(
        "bulletin_channels",
        "dónde ver boletines",
        "procedure",
        [
            "dónde consulto los boletines del Ruiz",
            "qué página publica la actividad del volcán",
            "cómo leer el boletín del SGC",
            "dónde miro las novedades del Nevado del Ruiz",
            "el Observatorio de Manizales publica informes",
            "qué fuente oficial vigila el volcán",
            "dónde están los boletines semanales",
            "cómo saber qué reportó el observatorio",
            "boletines oficiales del nevado",
            "donde veo el ultimo boletin del ruiz",
            "toca revisar SGC u Observatorio",
            "where are the official Ruiz bulletins",
            "how can I check volcano updates",
        ],
        "El SGC reúne los boletines semanales del Nevado del Ruiz y enlaza los más recientes; el Observatorio Vulcanológico y Sismológico de Manizales participa en el monitoreo que los alimenta. Consulta el boletín más nuevo y no uses una copia antigua para decidir si ingresas.",
        [
            "Busca la página de boletines del Nevado del Ruiz en el SGC; también puedes contrastar la información del Observatorio de Manizales. La publicación más reciente es la referencia para el estado dinámico.",
        ],
        [
            source("SGC, boletines del Nevado del Ruiz", SGC_BULLETINS),
            source("Alcaldía de Manizales, monitoreo del OVSM", OVSM),
        ],
        ["está abierto hoy", "qué pasó en Armero"],
        ["current_alert", "volcanic_activity", "ash_actions"],
        ["boletín", "SGC", "Observatorio de Manizales"],
    ),
    entry(
        "volcanic_activity",
        "qué monitorea el SGC",
        "explanation",
        [
            "qué señales vigila el SGC en el Ruiz",
            "cómo monitorean la actividad volcánica",
            "qué mide el observatorio del nevado",
            "cómo saben si el volcán cambia",
            "qué significa actividad inestable",
            "el SGC mira sismos y gases",
            "qué revisan en un boletín del Ruiz",
            "cómo se vigila el cráter Arenas",
            "qué datos aparecen en los informes",
            "que monitorea el observatorio volcanico",
            "como saben si aumenta la actividad",
            "what does the SGC monitor at Ruiz",
            "how is Nevado del Ruiz monitored",
        ],
        "Los boletines del SGC describen, entre otros parámetros, sismicidad, gases volcánicos, altura y dispersión de la columna, y anomalías térmicas. Esos datos sirven para seguir la evolución del volcán; no permiten que esta ficha prediga una erupción.",
        [
            "El monitoreo combina señales sísmicas, gases, columnas y temperatura del cráter. Para saber qué cambió recientemente, consulta el boletín fechado más reciente.",
        ],
        [
            source("SGC, boletín semanal del 10 al 16 de noviembre de 2026", SGC_LATEST_BULLETIN),
            source("Alcaldía de Manizales, monitoreo del OVSM", OVSM),
        ],
        ["síntomas de soroche", "qué pasó en Armero"],
        ["bulletin_channels", "current_alert", "volcanic_gases"],
        ["monitoreo", "sismos", "gases", "cráter"],
    ),
    entry(
        "ash_actions",
        "qué hacer ante ceniza",
        "safety",
        [
            "qué hago si cae ceniza volcánica",
            "cómo protegerme de la ceniza del Ruiz",
            "me alcanzó una nube de ceniza",
            "qué hacer si el volcán bota ceniza",
            "ceniza en el camino qué hago",
            "debo seguir caminando si cae ceniza",
            "cómo respirar durante una caída de ceniza",
            "qué hago con ceniza en los ojos",
            "hay que cerrar puertas por ceniza",
            "que hacer si cae ceniza en los nevados",
            "toca buscar refugio si hay ceniza",
            "what should I do if ash starts falling",
            "how do I protect myself from volcanic ash",
        ],
        "Si empieza a caer ceniza, busca refugio bajo techo o dentro de un vehículo, cubre nariz y boca con una mascarilla, pañuelo o trapo, y evita los lentes de contacto. Cierra puertas y ventanas, no te acerques al volcán y sigue las instrucciones oficiales; si hay evacuación, obedécela.",
        [
            "Ante ceniza, resguárdate, protege nariz y boca, cierra aberturas y escucha a las autoridades. No intentes acercarte para mirar ni continúes hacia la zona de riesgo.",
        ],
        [
            source("UNGRD, comunidades preparadas ante erupciones volcánicas", UNGRD),
            source("SGC, guía de preparación ante lluvia de cenizas", "https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf"),
        ],
        ["qué ropa llevar al parque los nevados", "me dio dolor de cabeza al llegar arriba"],
        ["volcanic_gases", "current_alert", "bulletin_channels"],
        ["ceniza", "refugio", "protección"],
    ),
    entry(
        "volcanic_gases",
        "riesgo de gases volcánicos",
        "safety",
        [
            "qué gases emite el Nevado del Ruiz",
            "los gases del volcán son peligrosos",
            "qué hago si huelo azufre arriba",
            "el dióxido de azufre afecta la respiración",
            "cómo reconocer riesgo por gases volcánicos",
            "puedo acercarme si veo fumarola",
            "qué pasa si hay olor fuerte en el cráter",
            "los gases se quedan en el aire",
            "hay que alejarse por gases del Ruiz",
            "que hacer con olor a azufre en la montaña",
            "toca salir si me irritan los ojos",
            "what are the volcanic gas risks",
            "is sulfur dioxide dangerous near Ruiz",
        ],
        "El SGC explica que el Ruiz puede emitir vapor de agua, dióxido de carbono y dióxido de azufre, entre otros gases; el dióxido de azufre irrita ojos, garganta y vías respiratorias. Si notas olor fuerte o irritación, aléjate del cráter y sigue las instrucciones del personal y de las autoridades.",
        [
            "Los gases pueden irritar ojos y vías respiratorias, y no debes acercarte al cráter para comprobarlos. Aléjate y avisa al guía o guardaparque si notas síntomas o una emisión.",
        ],
        [
            source("SGC, hoja informativa del Nevado del Ruiz", SGC_GASES),
        ],
        ["qué riesgo tiene la altura", "qué pasó en Armero"],
        ["ash_actions", "volcanic_activity", "current_alert"],
        ["gases", "SO2", "irritación"],
    ),
    entry(
        "volcanic_closures",
        "cierres por actividad volcánica",
        "rule",
        [
            "pueden cerrar un sector por el volcán",
            "qué pasa si aumenta la actividad del Ruiz",
            "cierran Brisas por alerta volcánica",
            "se puede subir a la cumbre del Ruiz",
            "qué accesos restringe la actividad del nevado",
            "hay evacuación por actividad volcánica",
            "por qué no dejan llegar a la nieve del Ruiz",
            "el camino Brisas Arenales está restringido",
            "puedo hacer ciclomontañismo por Brisas",
            "cierre del parque por el volcán",
            "toca obedecer si cierran por alerta",
            "can volcanic activity close a park sector",
            "is summit access restricted because of Ruiz",
        ],
        "Por actividad volcánica, Parques ha señalado restricciones para el ascenso a la cumbre y para el ciclomontañismo en el tramo Brisas–Arenales–Valle de las Tumbas; también puede ordenar cierre y evacuación. No confundas esto con los cierres ambientales u horarios: verifica el aviso vigente y sigue al personal del Parque.",
        [
            "La actividad del Ruiz puede restringir un sector o provocar cierre y evacuación. Antes de ir, confirma el aviso de Parques y acata cualquier instrucción en el lugar.",
        ],
        [
            source("Parques Nacionales, Resolución 268 de 2024", PNN_RESOLUTION),
            source("Parques Nacionales, Resolución 259 de 2024", PNN_RESOLUTION_259),
        ],
        ["hay cierres", "está abierto hoy"],
        ["current_alert", "alert_yellow_meaning", "bulletin_channels"],
        ["cierre", "restricción", "sector", "evacuación"],
    ),
]

FAQ = "https://ideam.gov.co/atencion-y-servicios-a-la-ciudadania/preguntas-frecuentes/en-colombia-donde-hace-mas-frio"
HELADA = "https://www.ideam.gov.co/atencion-y-servicios-a-la-ciudadania/glosario/helada-alertas-hidrologicas"
PRON = "https://www.ideam.gov.co/pronosticos-y-alertas"
BPTD = (
    "https://www.ideam.gov.co/sala-de-prensa/boletines/"
    "Bolet%C3%ADn-de-Pron%C3%B3stico-Nacional-del-Tiempo-para-Tres-D%C3%ADas-%28BPTD%29"
)
TRANSITIONS = SGC_TRANSITIONS
ASH_GUIDE = (
    "https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/"
    "Guia_preparacion_lluvia_cenizas.pdf"
)

NEGATIVES = [
    "está abierto hoy",
    "qué pasó en Armero",
    "síntomas de soroche",
    "hay cierres",
    "cuándo se creó el parque",
    "me dio dolor de cabeza al llegar arriba",
    "qué riesgo tiene la altura",
    "es pesado para el cuerpo ir al parque",
]


def negatives(index):
    return [NEGATIVES[index % len(NEGATIVES)], NEGATIVES[(index + 3) % len(NEGATIVES)]]


REWRITES = {
    "park_weather": (
        "En Los Nevados hay dos periodos de lluvia y dos secos, y la temperatura cambia con esos periodos y con la altura. El IDEAM añade que a más altura hace más frío. Esto no es el pronóstico de tu día: revísalo en el IDEAM antes de salir.",
        ["No armes el día con un clima genérico. Mira el pronóstico del IDEAM para la fecha y el sector."],
        [source("Parques Nacionales, ficha PNN Los Nevados", PNN), source("IDEAM, dónde hace más frío", FAQ)],
    ),
    "rainy_seasons": (
        "El parque tiene dos temporadas de lluvia y dos secas, pero la ficha no publica los meses. La lluvia de un pueblo no es la de la cumbre. Consulta el pronóstico del IDEAM para tu fecha y tu sector.",
        ["Hay un régimen bimodal, sin una lista de meses en la ficha del parque. Confirma el día en el IDEAM."],
        [source("Parques Nacionales, ficha PNN Los Nevados", PNN), source("IDEAM, Pronósticos y Alertas", PRON)],
    ),
    "weather_by_elevation": (
        "A mayor altura, menor temperatura: el IDEAM estima unos 0.6 grados C menos por cada 100 metros de ascenso. Páramo y zona nival no se leen con el clima del pueblo. Revisa el pronóstico del sector al que vas a subir.",
        ["Subir enfría. No traslades el parte del pueblo a la cumbre: consulta el IDEAM para ese sector."],
        [source("IDEAM, dónde hace más frío", FAQ)],
    ),
    "summit_visibility": (
        "Nadie puede garantizarte la cumbre despejada. Parques explicó la nevada del 10 de octubre de 2025 por nubosidad cargada de humedad. Si el día está cerrado, sigue el recorrido permitido y no te salgas a buscar la foto.",
        ["La cima puede quedar tapada. Disfruta lo que se vea y no abandones el sendero para perseguir el nevado."],
        [source("Parques Nacionales, nevada de octubre de 2025", SNOW), source("IDEAM, Pronósticos y Alertas", PRON)],
    ),
    "snow_and_hail": (
        "Parques documentó una nevada grande el 10 de octubre de 2025, con nubosidad húmeda, frío y cambios de presión; cubrió Ruiz, Santa Isabel, Cisne y Santa Rosa. No hay una cifra oficial de granizo para tu fecha: mira el pronóstico y no cuentes con nieve.",
        ["Esa nevada ya ocurrió. No promete nieve ni granizo para tu visita: revisa el pronóstico del sector."],
        [source("Parques Nacionales, nevada de octubre de 2025", SNOW)],
    ),
    "current_forecast": (
        "El tiempo de tu fecha no cabe en esta ficha. Entra a Pronósticos y Alertas del IDEAM y al boletín de los siguientes 3 días. Es un mapa del país, no del sendero. Vuelve a mirarlo antes de salir.",
        ["Para una fecha concreta abre el IDEAM de nuevo. Esta respuesta no reemplaza ese pronóstico."],
        [source("IDEAM, Pronósticos y Alertas", PRON), source("IDEAM, boletín de pronóstico para tres días", BPTD)],
    ),
    "alert_yellow_meaning": (
        "Amarilla significa cambios frente al nivel base: puede haber sismos, más gases y ceniza esporádica de poco alcance, que el viento dispersa. El SGC recomienda restringir la parte alta, según el volcán. El ingreso lo definen el boletín vigente y el personal del parque.",
        ["Amarilla no abre ni cierra sola. Lee el boletín del SGC y obedece al personal del parque."],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
    ),
    "alert_orange_meaning": (
        "Naranja es un cambio importante y una probabilidad mayor de erupciones grandes. No significa que la erupción ya empezó ni dice el día. Puede haber ceniza, olores fuertes y lahares pequeños. No subas por tu cuenta: sigue al SGC y a las autoridades.",
        ["Naranja no es un reloj. No te acerques por tu cuenta y espera la instrucción del SGC y de las autoridades."],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
    ),
    "alert_red_meaning": (
        "Roja, en el esquema del SGC, es un volcán en erupción. Incluye evacuación obligatoria de las zonas que el mapa de amenaza marque. No te acerques ni intentes ingresar: cumple lo que ordenen las autoridades.",
        ["Si declaran rojo, aléjate. La evacuación la marca el mapa de amenaza y la orden de las autoridades."],
        [source("SGC, esquema de estados de alerta", SGC_ALERTS)],
    ),
    "alert_states_nonsequential": (
        "Los colores no son una escalera: un volcán puede pasar de verde a naranja sin amarillo, y el esquema no pone la erupción en días o semanas. No calcules el riesgo con el color anterior. Lee el boletín más reciente del SGC.",
        ["No esperes a que recorra todos los colores. Usa el boletín vigente para decidir si viajas."],
        [source("SGC, explicación del esquema de alertas", TRANSITIONS)],
    ),
    "current_alert": (
        "Esta ficha no fija la alerta de hoy, porque cambia. El boletín del Ruiz del 10 al 16 de noviembre de 2026 ya puede no servir. Abre el más reciente en el SGC y sigue también a Parques y a la UNGRD.",
        ["El estado de esa semana no es el de ahora. Abre el boletín nuevo del SGC antes de salir."],
        [source("SGC, boletines del Nevado del Ruiz", SGC_BULLETINS), source("SGC, boletín semanal del 10 al 16 de noviembre de 2026", SGC_LATEST_BULLETIN)],
    ),
    "bulletin_channels": (
        "Los boletines semanales, mensuales y extraordinarios del Ruiz están en la página del SGC. El Observatorio de Manizales monitorea desde 1986, pero no reemplaza ese boletín. Usa siempre el documento más nuevo.",
        ["Mira la lista del SGC y quédate con el último. Una nota del observatorio no es la alerta vigente."],
        [source("SGC, boletines del Nevado del Ruiz", SGC_BULLETINS), source("Alcaldía de Manizales, monitoreo del OVSM", OVSM)],
    ),
    "volcanic_activity": (
        "Un boletín del Ruiz comenta sismicidad, gases como el dióxido de azufre, la columna y anomalías térmicas del cráter Arenas. Esos datos son de la semana del informe. Para saber qué cambió, abre el boletín nuevo: esta ficha no predice una erupción.",
        ["El informe describe señales de esa semana, no el futuro. Lee el boletín fechado más reciente del SGC."],
        [source("SGC, boletín semanal del 10 al 16 de noviembre de 2026", SGC_LATEST_BULLETIN)],
    ),
    "ash_actions": (
        "Si cae ceniza, busca techo o un vehículo, cúbrete nariz y boca con máscara, pañuelo o trapo, y cierra puertas y ventanas. También puedes usar sombrilla o capa. No te acerques al volcán y obedece si ordenan evacuar.",
        ["Resguárdate, tápate la cara y cierra el sitio. Si hay orden de salir, cúmplela y no te acerques a mirar."],
        [source("UNGRD, comunidades preparadas ante erupciones volcánicas", UNGRD), source("SGC, guía de preparación ante lluvia de cenizas", ASH_GUIDE)],
    ),
    "volcanic_gases": (
        "El Ruiz puede emitir vapor de agua, dióxido de carbono y dióxido de azufre. Ese último irrita ojos, garganta y vías respiratorias. Si hueles azufre fuerte o te irritas, aléjate del cráter y avisa al guía o al guardaparque.",
        ["No te acerques a comprobar el olor. Aléjate y avisa al personal si te arden ojos o garganta."],
        [source("SGC, hoja informativa del Nevado del Ruiz", SGC_GASES)],
    ),
    "volcanic_closures": (
        "Parques ha restringido la cumbre nevada y el ciclomontañismo entre Brisas, Arenales y Valle de las Tumbas por actividad volcánica, y puede ordenar cierre y evacuación en cualquier momento. No es el horario del parque. Confirma el aviso del día con el personal.",
        ["Esas restricciones no dicen si hoy está abierto. Pregunta el aviso vigente al personal del parque antes de subir."],
        [source("Parques Nacionales, Resolución 268 de 2024", PNN_RESOLUTION), source("Parques Nacionales, Resolución 259 de 2024", PNN_RESOLUTION_259)],
    ),
}

for item in entries:
    key = item["id"].split(".", 1)[1]
    short, variants, sources = REWRITES[key]
    item["answer"]["short"] = short
    item["answer"]["variants"] = variants
    item["sources"] = sources

entries.extend(extra_entries(entry, source, negatives))
for index, item in enumerate(entries):
    item["hard_negatives"] = negatives(index)


data = {
    "contract_version": 1,
    "id": "weather_volcano",
    "order": 3,
    "title": "Clima y actividad volcánica",
    "description": "Clima de montaña, heladas, pronóstico, alertas volcánicas, ceniza, lahares y cómo consultar el estado de cada volcán sin fijar el color del día.",
    "retrieval": {
        "profile": "safety",
        "bm25_weight": 0.25,
        "top_k": 3,
        "min_score": None,
        "entity_filters": [],
    },
    "clarification": {
        "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
        "bank": [
            "¿Buscas el clima general, una helada o el pronóstico para una fecha?",
            "¿Tu duda es sobre lluvia, altura, niebla o nieve?",
            "¿Quieres saber qué significa un color o cuál es el estado vigente?",
            "¿Preguntas por el Ruiz, el Santa Isabel, el Tolima o el Machín?",
            "¿Tu caso es ceniza, gases, un lahar o un cierre de sector?",
            "¿Quieres el boletín del SGC o el pronóstico del IDEAM?",
        ],
        "slot_questions": {},
        "fallback": "Puedo orientarte sobre clima, visibilidad, nieve, alertas, ceniza, gases y cierres por actividad volcánica. Para condiciones del día, verifica el IDEAM, el SGC y las indicaciones de Parques antes de viajar.",
    },
    "featured": [
        "weather_volcano.current_forecast",
        "weather_volcano.current_alert",
        "weather_volcano.ash_actions",
        "weather_volcano.lahar_visitor",
        "weather_volcano.alert_yellow_meaning",
    ],
    "entries": entries,
}


def fold(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


def raw_corpus():
    blob = []
    raw_dir = Path(__file__).resolve().parent / "evidence" / "raw"
    for path in raw_dir.iterdir():
        if path.suffix.lower() not in {".txt", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for invisible in ("\u200b", "\u200c", "\u200d", "\ufeff"):
            text = text.replace(invisible, "")
        blob.append(text)
    return "\n".join(blob)


CORPUS = raw_corpus()
known_ids = {item["id"] for item in entries}
seen_examples = {}
problems = []
for item in entries:
    label_words = item["label"].split()
    if not 3 <= len(label_words) <= 8:
        problems.append(f"{item['id']} label words {len(label_words)}")
    short = item["answer"]["short"]
    if len(short) > 320:
        problems.append(f"{item['id']} short {len(short)}")
    for variant in item["answer"]["variants"]:
        if len(variant) > 320:
            problems.append(f"{item['id']} variant {len(variant)}")
    slang = sum(1 for example in item["examples"] if re.search(r"parce|porfa", example, re.I))
    if slang > 1:
        problems.append(f"{item['id']} slang {slang}")
    for related in item["related"]:
        if related not in known_ids:
            problems.append(f"{item['id']} related {related}")
    for example in item["examples"]:
        key = fold(example)
        if key in seen_examples:
            problems.append(f"normalized duplicate {example!r} {item['id']} {seen_examples[key]}")
        seen_examples[key] = item["id"]
    for text in [short, *item["answer"]["variants"]]:
        for number in re.findall(r"\d+(?:[.,]\d+)*", text):
            if number not in CORPUS:
                problems.append(f"{item['id']} number {number} not in raw files")
if problems:
    raise SystemExit("\n".join(problems))

other_examples: dict[str, str] = {}
other_folded: dict[str, str] = {}
for section_path in SECTIONS.glob("*.json"):
    if section_path == OUTPUT:
        continue
    section = json.loads(section_path.read_text())
    for section_entry in section.get("entries", []):
        for example in section_entry.get("examples", []):
            other_examples.setdefault(example, section_entry["id"])
            other_folded.setdefault(fold(example), section_entry["id"])

for section_entry in entries:
    for example in section_entry["examples"]:
        if example in other_examples:
            raise ValueError(
                f"example collision: {example!r} in {section_entry['id']} and {other_examples[example]}"
            )
        owner = other_folded.get(fold(example))
        if owner:
            raise ValueError(f"normalized collision: {example!r} in {section_entry['id']} and {owner}")

for section_entry in entries:
    for negative in section_entry["hard_negatives"]:
        if negative not in other_examples:
            raise SystemExit(f"hard negative missing: {section_entry['id']} {negative!r}")

OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print(f"Generated {OUTPUT} with {len(entries)} entries and {sum(len(item['examples']) for item in entries)} examples.")
