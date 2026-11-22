"""Write the corrected geography section from passages read on 2026-11-21.

Does not rebuild the round-1 generator. Answers stay inside those quotations.
"""

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data/knowledge/sections/geography.json"
WHEN = "2026-11-21"

PNN = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
SHEET = "https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf"
RANK = "https://www2.sgc.gov.co/Noticias/Paginas/Los-10-volcanes-mas-altos-de-Colombia.aspx"
CRATER = "https://www2.sgc.gov.co/Noticias/Paginas/El-Nuevo-Domo-de-Lava-del-Volcan-Nevado-del-Ruiz-y-la-Geomorfologia-Actual-del-Crater-Arenas-2020.aspx"
BULLETIN = "https://www2.sgc.gov.co/Publicaciones/Informes%20tcnicos/Informe_de_actividad_volcanica_segmento_norte_2023.pdf"
IDEAM_RUIZ = "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-ruiz"
IDEAM_SANTA = "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-santa-isabel"
IDEAM_TOLIMA = "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-tolima"
RAMSAR = "https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf"
CARDER = "https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/"
TOLIMA_GOV = "https://tolima.gov.co/tolima/informacion-general/turismo/1996-municipio-de-anzoategui"

SRC = {
    "pnn": ("Parques Nacionales Naturales de Colombia", PNN),
    "sheet": ("Servicio Geológico Colombiano, hoja del Nevado del Ruiz, septiembre de 2024", SHEET),
    "rank": ("Servicio Geológico Colombiano, los 10 volcanes más altos, 9 de agosto de 2024", RANK),
    "crater": ("Servicio Geológico Colombiano, morfología del cráter Arenas, 31 de enero de 2020", CRATER),
    "bulletin": ("Servicio Geológico Colombiano, boletín del segmento volcánico norte, actividad de 2023", BULLETIN),
    "ideam_ruiz": ("IDEAM, glaciar Nevado del Ruiz", IDEAM_RUIZ),
    "ideam_santa": ("IDEAM, glaciar Nevado Santa Isabel", IDEAM_SANTA),
    "ideam_tolima": ("IDEAM, glaciar Nevado del Tolima", IDEAM_TOLIMA),
    "ramsar": ("Ficha Ramsar del complejo Laguna del Otún, 17 de julio de 2006", RAMSAR),
    "carder": ("CARDER, nota sobre Los Nevados, 14 de julio de 2026", CARDER),
    "tolima_gov": ("Gobernación del Tolima, turismo de Anzoátegui", TOLIMA_GOV),
}


def sources(*keys):
    return [{"label": SRC[key][0], "url": SRC[key][1], "retrieved_at": WHEN} for key in keys]


def entry(entry_id, label, kind, examples, short, variants, related, source_keys, detail=None, steps=None, tags=None):
    answer = {"short": short, "variants": variants}
    if steps:
        answer["steps"] = steps
    if detail:
        answer["detail"] = detail
    return {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "answer": answer,
        "sources": sources(*source_keys),
        "last_verified": WHEN,
        "related": related,
        "tags": tags or [],
        "_neg": [],
    }


ENTRIES = []


def add(item, neg):
    item["_neg"] = neg
    ENTRIES.append(item)


add(entry(
    "geography.main_peaks", "nevados principales del parque", "explanation",
    [
        "qué nevados hay en el parque",
        "cuáles son las tres cumbres nevadas",
        "cómo se llaman las montañas de Los Nevados",
        "que nevados ay alla",
        "los nevados del parque cuales son",
        "Kumanday Poleka Kasue y Dulima qué montañas son",
        "hay más cumbres aparte de los tres nevados",
        "paramillos del Cisne Santa Rosa y Quindío",
        "which snow peaks are in Los Nevados",
        "what are the main mountains in the park",
        "La Olleta y La Piraña también están en el complejo",
        "mapa de cumbres del parque nacional",
    ],
    "La ficha nombra tres nevados principales: Ruiz, o Kumanday; Santa Isabel, o Poleka Kasue; y Tolima, o Dulima. En el mismo complejo están los paramillos del Cisne, de Santa Rosa y del Quindío, y los cráteres La Olleta y La Piraña.",
    ["Si buscas las montañas, empieza por Ruiz, Santa Isabel y Tolima. La ficha suma los paramillos del Cisne, Santa Rosa y Quindío, y junto al Ruiz nombra La Olleta y La Piraña."],
    ["geography.park_versus_volcano", "geography.paramillo_cisne", "geography.glacier_summits"],
    ["pnn"],
    detail="En esa ficha, el glaciar se asocia a los tres nevados. Paramillo nombra otras alturas del mismo complejo.",
    tags=["nevado", "ruiz", "paramillo"],
), ["geography.park_versus_volcano", "geography.ruiz_height", "geography.four_sectors"])

add(entry(
    "geography.ruiz_identity", "qué volcán es el Ruiz", "explanation",
    [
        "qué es el Nevado del Ruiz",
        "el Ruiz es un estratovolcán",
        "cuéntame qué tipo de volcán es Kumanday",
        "que tipo de volcan es el ruis",
        "el ruiz tiene glaciar y cráter",
        "Kumanday es el mismo Ruiz",
        "ficha corta del volcán de Caldas y Tolima",
        "está dentro del parque o es otra cosa",
        "what kind of volcano is Nevado del Ruiz",
        "is the Ruiz a stratovolcano inside the park",
        "cómo le dice la ficha del parque al Ruiz",
        "háblame del Ruiz en corto",
    ],
    "El Nevado del Ruiz, Kumanday en la ficha del parque, es un estratovolcán de la cordillera Central, en el límite de Caldas y Tolima, dentro del parque. Tiene casquete glaciar y el Servicio Geológico llama Arenas a su cráter activo. La alerta de esta semana no está en esta guía: mírala en el SGC cuando tengas conexión.",
    ["Kumanday es el Nevado del Ruiz: un estratovolcán con hielo y con el cráter Arenas, en el límite Caldas-Tolima y dentro del parque. Para la alerta de ahora abre el boletín del SGC; aquí no viene."],
    ["geography.ruiz_height", "geography.arenas_crater", "geography.park_versus_volcano"],
    ["pnn", "sheet"],
    tags=["ruiz", "estratovolcán", "kumanday"],
), ["geography.ruiz_height", "geography.arenas_crater", "geography.ruiz_age"])

add(entry(
    "geography.ruiz_height", "altura de la cima del Ruiz", "fact",
    [
        "a qué altura está el Ruiz",
        "cuánto mide la cima del Nevado del Ruiz",
        "altura del Ruiz sobre el nivel del mar",
        "cuanto mide el nevado del ruis",
        "el ruiz pasa de cinco mil metros",
        "5321 es la cumbre",
        "la altura del cráter Arenas",
        "msnm del volcán Kumanday",
        "how high is Nevado del Ruiz",
        "what is the summit elevation of the Ruiz",
        "esa cota es la cima o hasta donde llego yo",
        "me dicen la altura del mirador y yo pregunto por la cumbre",
    ],
    "La cima del Nevado del Ruiz está a 5.321 metros. Coinciden la hoja del Servicio Geológico de septiembre de 2024, su nota del 9 de agosto de 2024 y el Ideam. Ese número es la cumbre, no la altura del centro de visitantes ni del valle.",
    ["Si preguntas por la cumbre, la referencia es 5.321 metros. No es la cota de Brisas ni la del recorrido hasta el Valle de las Tumbas."],
    ["geography.arenas_crater", "geography.highest_in_park", "geography.tolima_height"],
    ["sheet", "rank", "ideam_ruiz", "crater"],
    tags=["altura", "ruiz", "5321"],
), ["geography.tolima_height", "geography.santa_isabel_height", "geography.highest_in_park"])

add(entry(
    "geography.ruiz_where", "ubicación del Nevado del Ruiz", "fact",
    [
        "dónde queda el Nevado del Ruiz",
        "el Ruiz queda entre Caldas y Tolima",
        "coordenadas del volcán",
        "a cuantos kilometros de manizales queda el ruiz",
        "el ruis queda al sureste de manizales",
        "qué tan lejos está de Bogotá en el mapa",
        "latitud y longitud de la cima",
        "Villamaría Murillo y Casabianca y el glaciar",
        "where is Nevado del Ruiz",
        "how far is the volcano from Manizales on the map",
        "en qué parte de la cordillera Central está",
        "dónde queda el Ruiz en el mapa",
    ],
    "El Ruiz está en la cordillera Central, dentro del parque, en el límite de Caldas y Tolima. El boletín del SGC lo sitúa a 4°53'43'' norte y 75°19'21'' oeste, a unos 28 kilómetros al sureste de Manizales y a unos 140 kilómetros al oeste-noroeste de Bogotá. Esas son distancias de ubicación, no los kilómetros de la carretera.",
    ["En el mapa queda en el límite Caldas-Tolima, a unos 28 kilómetros al sureste de Manizales y unos 140 al oeste-noroeste de Bogotá. No uses esas cifras como tiempo de viaje."],
    ["geography.manizales_outside", "geography.murillo_ruiz", "geography.villamaria_caldas"],
    ["bulletin", "sheet", "ideam_ruiz"],
    detail="El Ideam pone el glaciar del Ruiz en Villamaría, Casabianca y Murillo, dentro del parque.",
    tags=["ubicación", "ruiz", "coordenadas"],
), ["geography.manizales_outside", "geography.summit_line", "geography.cordillera_central"])

add(entry(
    "geography.arenas_crater", "cráter Arenas del Ruiz", "explanation",
    [
        "cómo se llama el cráter del Ruiz",
        "qué es el cráter Arenas",
        "Arenas queda en la cima",
        "el crater arenas que tan grande es",
        "diametro del crater del ruiz",
        "profundidad del cráter Arenas",
        "la medida de 2020 sigue vigente",
        "puedo asomarme al cráter en la visita",
        "what is the Arenas crater",
        "how big is the Ruiz crater",
        "Arenas es del Ruiz o del Tolima",
        "hay un domo adentro del cráter",
    ],
    "El cráter principal del Ruiz se llama Arenas y está en la cima, a 5.321 metros. La nota del SGC del 31 de enero de 2020 lo describe irregular, de unos 980 por 900 metros y cerca de 300 metros de profundidad. Esa descripción es de esa fecha; el boletín de la actividad de 2023 da otras medidas, y ninguna de las dos es un contorno en vivo.",
    ["Arenas es el cráter de la cima, a 5.321 metros. En 2020 el SGC lo midió en unos 980 por 900 metros y cerca de 300 de profundidad, y el informe de 2023 no repite esas cifras: no las tomes como el tamaño de hoy."],
    ["geography.ruiz_identity", "geography.tolima_crater", "geography.ruiz_height"],
    ["sheet", "crater", "bulletin", "ideam_ruiz"],
    detail="El boletín de 2023 dice un diámetro máximo de 800 metros y 200 metros de profundidad. El domo medido en enero de 2020 no se usa aquí como tamaño actual.",
    tags=["cráter", "arenas"],
), ["geography.tolima_crater", "geography.olleta_pirana", "geography.valle_tumbas"])

add(entry(
    "geography.park_area", "extensión oficial del parque", "fact",
    [
        "cuántas hectáreas tiene el parque",
        "extensión de Los Nevados",
        "qué tan grande es el área protegida",
        "cuantas hectareas son",
        "extencion del parque en hectareas",
        "tamaño del parque nacional",
        "superficie en hectáreas",
        "por qué veo hectáreas distintas",
        "how many hectares is Los Nevados",
        "what is the official area of the national park",
        "con qué cifra me quedo para el tamaño",
        "área del parque en la ficha de ahora",
    ],
    "Para la visita, usa la extensión del encabezado de la ficha: 61.388,24 hectáreas. Otras publicaciones oficiales dan una cifra cercana; sigue siendo el mismo parque.",
    ["La referencia de la ficha vigente es 61.388,24 hectáreas. Si otra página oficial da una cifra cercana, es otra publicación del área, no un segundo parque."],
    ["geography.departments", "geography.municipalities", "geography.risaralda_share"],
    ["pnn", "carder"],
    detail="El apartado de historia de la ficha dice que el área geográfica protegida es de 61.410 hectáreas. La Carder, el 14 de julio de 2026, escribe 61.410,53 hectáreas. No se promedian.",
    tags=["hectáreas", "extensión"],
), ["geography.risaralda_share", "geography.departments", "geography.municipalities"])

add(entry(
    "geography.departments", "departamentos del área protegida", "fact",
    [
        "en qué departamentos queda el parque",
        "departamentos de Los Nevados",
        "queda en Caldas Risaralda Quindío y Tolima",
        "en que parte de colombia queda",
        "departamentos del parque los nevado",
        "son cuatro departamentos",
        "el Eje Cafetero cuáles abarca",
        "Caldas entra en el área protegida",
        "which departments does Los Nevados cover",
        "is the park only in Caldas and Tolima",
        "Quindío también hace parte",
        "mapa departamental del parque",
    ],
    "El parque se extiende por Caldas, Quindío, Risaralda y Tolima. Así los nombra el encabezado de la ficha, en la cordillera Central.",
    ["Son cuatro: Caldas, Quindío, Risaralda y Tolima. La ficha los publica en ese orden."],
    ["geography.municipalities", "geography.cordillera_central", "geography.manizales_outside"],
    ["pnn"],
    tags=["departamento", "caldas", "tolima"],
), ["geography.municipalities", "geography.manizales_outside", "geography.salento_quindio"])

add(entry(
    "geography.cordillera_central", "cordillera Central del parque", "explanation",
    [
        "en qué cordillera está Los Nevados",
        "queda en la cordillera Central",
        "el parque está entre el Cauca y el Magdalena",
        "los nevados quedan en el eje cafetero",
        "cordillera central de colombia",
        "es la Sierra Nevada de Santa Marta",
        "corazón del Eje Cafetero en el mapa",
        "entre qué ríos grandes está la cordillera",
        "which mountain range is the park in",
        "is Los Nevados in the Central Cordillera",
        "alta montaña del centro del país",
        "ubicación entre el Magdalena y el Cauca",
    ],
    "El parque está en la cordillera Central, en el Eje Cafetero, entre los ríos Magdalena y Cauca. La ficha lo presenta como reserva de agua para Tolima, Risaralda, Caldas y Quindío.",
    ["Piensa en la cordillera Central, entre el Magdalena y el Cauca, en el centro cafetero. De ahí sale agua para los cuatro departamentos del parque."],
    ["geography.andes_occidentales_office", "geography.watersheds", "geography.departments"],
    ["pnn"],
    tags=["cordillera", "magdalena", "cauca"],
), ["geography.andes_occidentales_office", "geography.watersheds", "geography.departments"])

add(entry(
    "geography.andes_occidentales_office", "región Andes Occidentales", "explanation",
    [
        "qué significa Andes Occidentales en la ficha",
        "región Andes Occidentales",
        "eso es la cordillera Occidental",
        "direccion territorial del parque",
        "andes occidentales es la administracion",
        "por qué la ficha dice Andes Occidentales",
        "Parques Nacionales en qué territorial lo tiene",
        "el rótulo de la región me confundió",
        "what does Andes Occidentales mean on the park page",
        "is that label the western cordillera",
        "dirección territorial Andes Occidentales",
        "Andes Occidentales y cordillera Central me confunden",
    ],
    "En la ficha, Andes Occidentales es la región de Parques Nacionales que administra el área. La montaña sigue en la cordillera Central, entre el Magdalena y el Cauca.",
    ["Andes Occidentales, en esa ficha, es la oficina territorial. El parque queda en la cordillera Central."],
    ["geography.cordillera_central", "geography.departments"],
    ["pnn"],
    tags=["andes occidentales", "territorial"],
), ["geography.cordillera_central", "geography.departments", "geography.main_peaks"])

add(entry(
    "geography.municipalities", "municipios que nombra la ficha", "fact",
    [
        "qué municipios cubre el parque",
        "lista de municipios de Los Nevados",
        "en qué pueblos está el área protegida",
        "municipios del parque nacional",
        "son diez o once municipios",
        "Santa Rosa Pereira Villamaría Murillo y los demás",
        "Anzoátegui Ibagué Salento Herveo Casabianca",
        "el municipio de Santa Isabel está en la lista",
        "which municipalities overlap the park",
        "how many towns does the protected area name",
        "jurisdicción municipal del polígono",
        "cuáles pueblos quedan dentro del área",
    ],
    "La ficha nombra diez municipios: Santa Rosa de Cabal, Pereira, Villamaría, Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca, Herveo y Salento. Quédate con esos diez, que son los que están escritos.",
    ["Los diez de la ficha son Santa Rosa de Cabal, Pereira, Villamaría, Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca, Herveo y Salento."],
    ["geography.departments", "geography.tolima_municipalities", "geography.salento_quindio"],
    ["pnn", "carder"],
    detail="La Carder, el 14 de julio de 2026, habla de 11 municipios y no escribe el undécimo. La lista que sí puedes usar es la de la ficha.",
    tags=["municipio", "ficha"],
), ["geography.departments", "geography.tolima_municipalities", "geography.ibague_highlands"])

add(entry(
    "geography.manizales_outside", "Manizales y el límite del parque", "fact",
    [
        "Manizales queda dentro del parque",
        "la ciudad de Manizales es parte de Los Nevados",
        "vivo en Manizales, estoy en el área protegida",
        "manizales esta en el parque o no",
        "manizales queda adentro del nevado",
        "el Ruiz es de Manizales o de Villamaría",
        "desde la ciudad se ve el nevado",
        "capital de Caldas y el límite del área",
        "is Manizales inside Los Nevados",
        "does the park include the city of Manizales",
        "salgo de Manizales hacia el parque",
        "cuál es el municipio caldense del área",
    ],
    "El municipio caldense que la ficha incluye es Villamaría. Manizales no está en esa lista. El Ruiz queda a unos 28 kilómetros al sureste de la ciudad: es una distancia de ubicación, no de carretera.",
    ["Sales desde Manizales, y la ciudad no está en la lista del parque. El lado caldense que sí nombra la ficha es Villamaría, a unos 28 kilómetros de ubicación del Ruiz."],
    ["geography.villamaria_caldas", "geography.ruiz_where", "geography.departments"],
    ["pnn", "bulletin"],
    tags=["manizales", "villamaría"],
), ["geography.ruiz_where", "geography.villamaria_caldas", "geography.murillo_ruiz"])

add(entry(
    "geography.park_versus_volcano", "diferencia entre parque y volcán", "explanation",
    [
        "el parque y el volcán son lo mismo",
        "diferencia entre Los Nevados y el Nevado del Ruiz",
        "el nevado queda dentro del parque",
        "parque y volcan son lo mismo",
        "el ruiz es todo el parque",
        "voy al nevado o voy al parque",
        "Santa Isabel y Tolima también están adentro",
        "si digo Ruiz ya hablo de todo el parque",
        "is the park the same thing as the volcano",
        "does Nevado del Ruiz mean the whole national park",
        "el área protegida tiene varios volcanes",
        "Los Nevados es el Ruiz o es más grande",
    ],
    "Los Nevados es el área protegida, en cuatro departamentos. El Nevado del Ruiz es un volcán dentro de ella, junto con Santa Isabel, el Tolima y otros centros como el Cisne y La Olleta. Ir al Ruiz no recorre todo el parque.",
    ["El parque es el territorio protegido. El Ruiz es uno de sus volcanes, al lado de Santa Isabel, el Tolima, el Cisne y La Olleta."],
    ["geography.main_peaks", "geography.park_area", "geography.four_sectors"],
    ["pnn", "sheet"],
    tags=["parque", "volcán"],
), ["geography.main_peaks", "geography.park_area", "geography.four_sectors"])

add(entry(
    "geography.four_sectors", "cuatro sectores de visita", "explanation",
    [
        "cuáles son los sectores del parque",
        "qué sectores de visita hay",
        "nombres de las zonas ecoturísticas",
        "sectores ecoturisticos de los nevados",
        "brisas cisne otun y dulima",
        "son cuatro sectores",
        "cada sector mira a un paisaje distinto",
        "cómo está dividido el parque para la visita",
        "what are the four visitor sectors",
        "how is the park divided for visitors",
        "Brisas-Kumanday y los otros tres",
        "mapa de sectores",
    ],
    "Para la visita, la ficha describe cuatro sectores: Brisas-Kumanday, Cisne-Poleka Kasue, Laguna del Otún y Quindío-Dulima, con puntos de acceso en Caldas, Risaralda, Quindío y Tolima. Las vías, los horarios y los cupos se confirman con el parque.",
    ["La división de visita que publica la ficha tiene cuatro nombres: Brisas-Kumanday, Cisne-Poleka Kasue, Laguna del Otún y Quindío-Dulima. Si un tramo está abierto ese día, confírmalo con Parques Nacionales."],
    ["geography.sector_brisas_kumanday", "geography.sector_cisne_poleka", "geography.sector_laguna_otun"],
    ["pnn"],
    tags=["sector", "brisas", "otún"],
), ["geography.sector_brisas_kumanday", "geography.sector_cisne_poleka", "geography.sector_quindio_dulima"])

add(entry(
    "geography.sector_brisas_kumanday", "sector norte Brisas Kumanday", "fact",
    [
        "qué es el sector Brisas",
        "Brisas-Kumanday dónde queda",
        "el sector norte es el del Ruiz",
        "brisas a cuantos metros queda",
        "centro de brisas 4100 metros",
        "Arenales queda antes del valle",
        "sector del volcán Nevado del Ruiz",
        "Kumanday es el nombre de ese sector norte",
        "where is the Brisas sector",
        "what landscape is next to Brisas-Kumanday",
        "el carreteable sale de Brisas hacia el valle",
        "4100 metros es el centro o la cima",
    ],
    "Brisas-Kumanday es el sector norte, junto al Nevado del Ruiz. La ficha pone el centro de inducción Brisas a unos 4.100 metros, y el carreteable sigue por Arenales hasta el Valle del Silencio, o Valle de las Tumbas. Esa cota es del centro, no de la cima, y el estado del tramo se confirma con el parque.",
    ["El sector norte se llama Brisas-Kumanday y queda junto al Ruiz. Brisas está publicada a unos 4.100 metros; la cumbre está más arriba, y si el tramo está habilitado lo confirma el parque."],
    ["geography.valle_tumbas", "geography.ruiz_where", "geography.four_sectors"],
    ["pnn"],
    tags=["brisas", "kumanday", "4100"],
), ["geography.valle_tumbas", "geography.ruiz_height", "geography.four_sectors"])

add(entry(
    "geography.sector_cisne_poleka", "sector Cisne Poleka Kasue", "explanation",
    [
        "qué es el sector del Cisne",
        "Cisne-Poleka Kasue qué montañas muestra",
        "desde ese sector se ven Ruiz y Santa Isabel",
        "el cisne es el sector o la montaña",
        "el centro El Cisne a qué altura está",
        "El Cisne queda a unos 4100 metros",
        "ahí está el sendero a la Laguna Verde",
        "cabañas La Cueva y Potosí",
        "where is the Cisne sector",
        "what can you see from Cisne-Poleka Kasue",
        "sector de Santa Isabel y del paramillo",
        "Poleka Kasue es la montaña de ese sector",
    ],
    "Cisne-Poleka Kasue es el sector desde el que la ficha dice que se observan el Ruiz, Santa Isabel y el paramillo del Cisne. El centro El Cisne está a unos 4.100 metros, y por ahí quedan las cabañas La Cueva y Potosí y el sendero hacia la Laguna Verde. El paramillo, el sector y el centro comparten nombre y son tres cosas distintas.",
    ["Ese sector junta el paisaje de Santa Isabel, o Poleka Kasue, con el paramillo del Cisne y la vista hacia el Ruiz. El centro El Cisne figura a unos 4.100 metros; la montaña no es la casa de visitantes."],
    ["geography.paramillo_cisne", "geography.santa_isabel", "geography.laguna_verde"],
    ["pnn"],
    tags=["cisne", "poleka kasue"],
), ["geography.paramillo_cisne", "geography.laguna_verde", "geography.four_sectors"])

add(entry(
    "geography.sector_laguna_otun", "sector Laguna del Otún", "fact",
    [
        "dónde queda el sector de la Laguna del Otún",
        "el sector de la laguna es Risaralda",
        "Potosí a qué altura está",
        "cabana potosi 3920 metros",
        "la laguna más grande es ese sector",
        "paramillos del Quindío y Santa Rosa la rodean",
        "vereda El Bosque es un acceso",
        "geografía del sector Laguna del Otún",
        "where is the Otún lake sector",
        "what surrounds the Otún sector",
        "Pereira es la referencia de ese lado",
        "3920 metros es Potosí o es la laguna",
    ],
    "El sector Laguna del Otún está en Risaralda. La ficha dice que la laguna es la más grande del parque y que la rodean los paramillos del Quindío y de Santa Rosa. La cabaña Potosí, uno de los accesos, está a unos 3.920 metros; esa no es la cota de la laguna.",
    ["Ese sector risaraldense se organiza alrededor de la Laguna del Otún, entre los paramillos del Quindío y de Santa Rosa. Potosí figura a unos 3.920 metros, y esa altura es de la cabaña."],
    ["geography.laguna_otun", "geography.paramillo_quindio", "geography.paramillo_santa_rosa"],
    ["pnn"],
    tags=["otún", "potosí", "risaralda"],
), ["geography.laguna_otun", "geography.rio_otun", "geography.pereira_santa_rosa"])

add(entry(
    "geography.sector_quindio_dulima", "sector Quindío Dulima", "explanation",
    [
        "qué es el sector Quindío Dulima",
        "Quindío-Dulima a qué volcán corresponde",
        "el sector del Tolima cómo se llama",
        "a dulima también le dicen tolima",
        "salento ibague y anzoategui son ese lado",
        "ese sector no es Brisas",
        "paisaje del volcán Tolima dentro del parque",
        "geografía del lado tolimense y quindiano",
        "where is the Quindío-Dulima sector",
        "which volcano is next to the Dulima sector",
        "Juntas y Palomar son referencias de ese sector",
        "el sector sur del parque es el del Tolima",
    ],
    "Quindío-Dulima es el sector de las inmediaciones del Nevado del Tolima. La ficha lo separa de los otros tres. Salento, Ibagué y Anzoátegui son las llegadas que nombra; el camino se consulta en cómo llegar.",
    ["Dulima, en el nombre del sector, apunta al Nevado del Tolima. Quindío-Dulima es esa zona del parque, con referencias en Salento, Ibagué y Anzoátegui."],
    ["geography.tolima_volcano", "geography.salento_quindio", "geography.ibague_highlands"],
    ["pnn"],
    tags=["dulima", "tolima", "sector"],
), ["geography.tolima_volcano", "geography.salento_quindio", "geography.four_sectors"])

add(entry(
    "geography.valle_tumbas", "Valle de las Tumbas", "fact",
    [
        "dónde queda el Valle de las Tumbas",
        "Valle del Silencio dónde queda",
        "el valle y el silencio son el mismo sitio",
        "que queda despues de brisas",
        "valle de las tumbas es el crater",
        "Arenales está antes de ese valle",
        "atractivo del sector norte junto al Ruiz",
        "cómo se llama el valle del sector Brisas",
        "where is Valle de las Tumbas",
        "is Valle del Silencio the same place",
        "queda en Brisas-Kumanday",
        "el valle está cerca del Ruiz",
    ],
    "El Valle de las Tumbas, llamado también Valle del Silencio en la ficha, es un atractivo del sector norte Brisas-Kumanday, junto al Nevado del Ruiz. El carreteable sale del centro Brisas, pasa por Arenales y llega a ese valle. Los tramos habilitados cambian; confírmalos con Parques Nacionales antes de viajar.",
    ["Valle de las Tumbas y Valle del Silencio son el mismo lugar de la ficha, en el norte, cerca del Ruiz. Si ese tramo está abierto, lo confirma el parque."],
    ["geography.sector_brisas_kumanday", "geography.arenas_crater", "geography.ruiz_where"],
    ["pnn"],
    tags=["valle", "tumbas", "silencio"],
), ["geography.sector_brisas_kumanday", "geography.arenas_crater", "geography.laguna_otun"])

add(entry(
    "geography.laguna_otun", "Laguna del Otún en Risaralda", "explanation",
    [
        "dónde queda la Laguna del Otún",
        "qué es la laguna del Otún",
        "es la laguna más grande del parque",
        "laguana del otun donde queda",
        "la laguna grande de los nevados",
        "queda en Pereira y Santa Rosa",
        "puedo visitar el Otún, es un sector aparte",
        "humedal Ramsar de esa laguna",
        "where is Laguna del Otún",
        "which is the largest lake in the park",
        "está entre Santa Isabel y el páramo de Santa Rosa",
        "la laguna del Otún es un sitio Ramsar",
    ],
    "La Laguna del Otún es la más grande del parque, según la ficha, y da nombre a un sector en Risaralda. Queda entre el Nevado Santa Isabel y el páramo de Santa Rosa, en Pereira y Santa Rosa de Cabal. Los humedales de esa laguna son un sitio Ramsar; la ruta y el cupo se confirman con el parque.",
    ["Si buscas la laguna grande, es la del Otún, en Risaralda, entre Santa Isabel y Santa Rosa. El sector lleva su nombre, los humedales están reconocidos por Ramsar y la entrada se confirma con el parque."],
    ["geography.sector_laguna_otun", "geography.rio_otun", "geography.laguna_otun_formation"],
    ["pnn", "ramsar"],
    detail="La ficha Ramsar del 17 de julio de 2006 da 6.578,5 hectáreas y un rango de 3.300 a 4.850 metros para el complejo de humedales, no para el espejo de agua solo. La descripción de esa ficha redondea el complejo en unas 6.579 hectáreas.",
    tags=["laguna", "otún", "ramsar"],
), ["geography.laguna_otun_formation", "geography.rio_otun", "geography.laguna_verde"])

add(entry(
    "geography.laguna_otun_formation", "origen de la Laguna del Otún", "explanation",
    [
        "cómo se formó la Laguna del Otún",
        "la laguna es de origen glacial",
        "una lava del Santa Isabel la represó",
        "de donde salio la laguna del otun",
        "es una laguna volcanica o de glaciar",
        "represamiento de un valle glacial",
        "por qué hay agua entre Santa Isabel y Santa Rosa",
        "origen de la laguna grande",
        "how did Laguna del Otún form",
        "is the Otún lake a lava-dammed valley",
        "el IGAC explicó el origen y Ramsar lo recoge",
        "hay más humedales alrededor de esa laguna",
    ],
    "La ficha Ramsar del 17 de julio de 2006, con base en el IGAC de 1993, explica la Laguna del Otún como un valle glacial que una lava del Santa Isabel represó. Es una laguna permanente entre ese nevado y el páramo de Santa Rosa. Ese texto describe el origen; no mide el hielo de ahora.",
    ["El Otún se formó cuando una colada del Santa Isabel cerró un valle glacial, según la ficha Ramsar de 2006. Esa explicación no dice cuánto hielo queda hoy."],
    ["geography.laguna_otun", "geography.santa_isabel", "geography.rio_otun"],
    ["ramsar"],
    detail="La misma ficha de 2006 habla de otros 17 humedales menores alrededor. No es un inventario de 2026.",
    tags=["origen", "otún", "glacial"],
), ["geography.laguna_otun", "geography.rio_otun", "geography.santa_isabel"])

add(entry(
    "geography.laguna_verde", "Laguna Verde del sector Cisne", "explanation",
    [
        "dónde queda la Laguna Verde",
        "Laguna Verde es del sector del Cisne",
        "hay una laguna verde cerca de Santa Isabel",
        "laguna verde donde queda",
        "la laguna verde es un glaciar o un lago",
        "sendero Laguna Verde en Cisne-Poleka Kasue",
        "el Ideam usa el mismo nombre",
        "a qué altura está el espejo de la Laguna Verde",
        "where is Laguna Verde",
        "is Laguna Verde a lake or leftover ice",
        "vertiente de Santa Isabel y la laguna",
        "la ficha habla de un sendero hacia esa laguna",
    ],
    "La ficha describe un sendero hacia la Laguna Verde en el sector Cisne-Poleka Kasue, el de Santa Isabel y el paramillo del Cisne. El Ideam usa el mismo nombre para un relicto de hielo de Santa Isabel que en su página sigue existente. No dice que el sendero y ese hielo sean el mismo punto, y no publica la altitud de un espejo de agua.",
    ["Busca el sendero Laguna Verde en el sector del Cisne. El Ideam también llama Laguna Verde a un resto de hielo de Santa Isabel, y las dos páginas no dicen que sea el mismo sitio ni dan la cota de una laguna."],
    ["geography.sector_cisne_poleka", "geography.glacier_summits", "geography.santa_isabel"],
    ["pnn", "ideam_santa"],
    tags=["laguna verde", "cisne"],
), ["geography.glacier_summits", "geography.sector_cisne_poleka", "geography.laguna_encanto"])

add(entry(
    "geography.laguna_encanto", "Laguna del Encanto en Anzoátegui", "fact",
    [
        "dónde queda la Laguna del Encanto",
        "Laguna del Encanto",
        "la laguna de la base del Tolima",
        "laguna del encanto a cuantos metros",
        "en hoyo frio nace el totare",
        "Anzoátegui y la laguna del nevado",
        "está dentro del parque o en el municipio",
        "4.000 metros según la Gobernación",
        "where is Laguna del Encanto",
        "does the Totare river start at that lake",
        "vereda Hoyo Frío y el Tolima",
        "la laguna del Encanto es la del Otún",
    ],
    "La Gobernación del Tolima ubica la Laguna del Encanto en la vereda Hoyo Frío de Anzoátegui, a unos 4.000 metros, en la base del Nevado del Tolima, y dice que allí nace el río Totare. Anzoátegui es puerta de entrada al parque, pero esa página no dice si el espejo cae dentro del límite. Confirma el punto con Parques Nacionales antes de la visita.",
    ["El Encanto, según la Gobernación, está en Hoyo Frío, Anzoátegui, a unos 4.000 metros, al pie del Tolima, y de ahí sale el Totare. Falta una frase oficial que lo meta o lo saque del polígono, así que confírmalo con el parque."],
    ["geography.tolima_volcano", "geography.sector_quindio_dulima", "geography.watersheds"],
    ["tolima_gov", "pnn"],
    detail="La página de la Gobernación no muestra fecha de publicación. Otras lagunas de esa ficha turística, como El Corazón, Bomboná y Las Mellizas, figuran en predio privado y no se tratan aquí como lagunas del parque.",
    tags=["encanto", "totare", "anzoátegui"],
), ["geography.sector_quindio_dulima", "geography.tolima_height", "geography.laguna_otun"])

add(entry(
    "geography.santa_isabel", "forma del Nevado Santa Isabel", "explanation",
    [
        "qué es el Nevado Santa Isabel",
        "la ficha llama Poleka Kasue a Santa Isabel",
        "Santa Isabel es un conjunto de domos",
        "santa isabel tiene un solo crater",
        "tres cumbres norte centro y sur",
        "la cumbre norte se llama Hongo",
        "queda entre Risaralda Caldas y Tolima",
        "es uno de los tres nevados del parque",
        "what is Nevado Santa Isabel",
        "is Santa Isabel a single crater like the Ruiz",
        "alineado de norte a sur",
        "domos del nevado de en medio",
    ],
    "Santa Isabel, Poleka Kasue en la ficha, es un conjunto de domos alineados de norte a sur, con cumbres Norte o Hongo, Central y Sur. El Ideam lo distingue de un cono con un solo cráter. El SGC lo sitúa entre Risaralda, Caldas y Tolima, y el parque lo cuenta entre sus tres nevados.",
    ["Poleka Kasue es Santa Isabel: un grupo de domos con tres cumbres, no un cráter único. Está en Risaralda, Caldas y Tolima, y es uno de los nevados del parque."],
    ["geography.santa_isabel_height", "geography.sector_cisne_poleka", "geography.glacier_summits"],
    ["pnn", "ideam_santa", "rank"],
    tags=["santa isabel", "domo", "poleka kasue"],
), ["geography.santa_isabel_height", "geography.sector_cisne_poleka", "geography.paramillo_cisne"])

add(entry(
    "geography.santa_isabel_height", "cotas oficiales de Santa Isabel", "fact",
    [
        "a qué altura está Santa Isabel",
        "cuánto mide el Nevado de Santa Isabel",
        "las tres cumbres no tienen la misma cota",
        "cuanto mide santa isabel",
        "4965 o 4935 cual uso",
        "cumbre Sur Central y Norte en metros",
        "Hongo es la más baja de las tres",
        "altitud del domo",
        "how high is Nevado Santa Isabel",
        "why do the summit heights differ from 4965",
        "4.935 la sur y 4.903 la norte",
        "metros de Poleka Kasue",
    ],
    "Para ubicar cada cumbre, usa el Ideam: Sur 4.935 metros, Central 4.923 y Norte, o Hongo, 4.903, calculadas con el modelo SRTM 12,5 del IGAC y un GPS topográfico. El 9 de agosto de 2024 el SGC publicó una sola altura, 4.965 metros, sin ese desglose.",
    ["El Ideam separa tres cumbres: Sur 4.935 m, Central 4.923 m y Norte (Hongo) 4.903 m, con SRTM 12,5 y GPS. El ranking del SGC del 9 de agosto de 2024 da 4.965 m en una sola cifra."],
    ["geography.santa_isabel", "geography.ruiz_height", "geography.highest_in_park"],
    ["ideam_santa", "rank"],
    detail="El Ideam llama a Santa Isabel el glaciar de menor altitud del país, a 4.903 metros, que es la cumbre Norte de su tabla. La página no trae una fecha de publicación aparte; las cotas están en la tabla leída el 21 de noviembre de 2026.",
    tags=["altura", "santa isabel"],
), ["geography.ruiz_height", "geography.tolima_height", "geography.santa_isabel"])

add(entry(
    "geography.tolima_volcano", "forma del Nevado del Tolima", "explanation",
    [
        "qué es el Nevado del Tolima",
        "Dulima es el volcán del Tolima",
        "es un cono en el sur del parque",
        "el tolima es un estratovolcan",
        "nevado del tolima en ibague y anzoategui",
        "una sola cumbre, no tres como Santa Isabel",
        "hace parte del parque junto con Ruiz y Santa Isabel",
        "forma cónica del volcán",
        "what is Nevado del Tolima",
        "is Tolima a cone-shaped stratovolcano",
        "coordenadas aproximadas 4 grados 39 norte",
        "el glaciar está sobre un cono",
    ],
    "El Nevado del Tolima, Dulima en la ficha, es un estratovolcán cónico de una sola cumbre. El Ideam lo ubica cerca de 4°39' norte y 75°19' oeste, en Ibagué y Anzoátegui, dentro del parque.",
    ["Dulima es el Tolima: un volcán en forma de cono, con una cumbre, en Ibagué y Anzoátegui y dentro del parque."],
    ["geography.tolima_height", "geography.sector_quindio_dulima", "geography.tolima_crater"],
    ["pnn", "ideam_tolima", "tolima_gov"],
    tags=["tolima", "dulima", "cono"],
), ["geography.tolima_height", "geography.sector_quindio_dulima", "geography.tolima_crater"])

add(entry(
    "geography.tolima_height", "altura de la cima del Tolima", "fact",
    [
        "a qué altura está el Tolima",
        "cuánto mide la cumbre del Tolima",
        "altura del Nevado del Tolima",
        "cuantos metros tiene el tolima",
        "5215 es la cima",
        "el SGC y el Ideam coinciden en el Tolima",
        "pasa de cinco mil doscientos metros",
        "cota de la única cumbre",
        "how high is Nevado del Tolima",
        "what elevation does the SGC give for Tolima",
        "altitud estimada con el modelo del IGAC",
        "metros de Dulima",
    ],
    "La cumbre única del Nevado del Tolima está a 5.215 metros. Coinciden el ranking del SGC del 9 de agosto de 2024 y el Ideam, que la estima con el modelo SRTM 12,5 del IGAC. Esa cota es la cima, no el punto hasta el que llega cualquier camino.",
    ["Si la pregunta es la cima del Tolima, la cifra compartida es 5.215 metros. Es la cumbre del volcán, no la altura de un sendero."],
    ["geography.tolima_volcano", "geography.ruiz_height", "geography.highest_in_park"],
    ["rank", "ideam_tolima"],
    tags=["altura", "tolima", "5215"],
), ["geography.ruiz_height", "geography.highest_in_park", "geography.tolima_volcano"])

add(entry(
    "geography.paramillo_quindio", "cota del Paramillo del Quindío", "fact",
    [
        "a qué altura está el Paramillo del Quindío",
        "Paramillo del Quindío",
        "el Quindío todavía es un nevado con hielo",
        "paramillo del quindio a cuantos metros",
        "4700 metros en el limite de tres departamentos",
        "Tolima Quindío y Risaralda se tocan ahí",
        "rodea la Laguna del Otún junto con Santa Rosa",
        "eje de la cordillera Central",
        "how high is Paramillo del Quindío",
        "where do the three departments meet at Quindío",
        "el SGC lo lista en 4.700 metros",
        "qué tan lejos está de Armenia en el mapa",
    ],
    "El Paramillo del Quindío figura a 4.700 metros en el ranking del SGC del 9 de agosto de 2024 y en el boletín del segmento norte. Está en el eje de la cordillera Central, en el límite de Tolima, Quindío y Risaralda. La ficha del parque lo pone, con el de Santa Rosa, alrededor de la Laguna del Otún, y no lo incluye entre los tres nevados del glaciar.",
    ["El Quindío de este parque es un paramillo de 4.700 metros en el límite de tres departamentos. La ficha no lo cuenta entre los tres nevados con glaciar, y lo ubica junto a la Laguna del Otún."],
    ["geography.paramillo_santa_rosa", "geography.laguna_otun", "geography.salento_quindio"],
    ["rank", "bulletin", "pnn"],
    detail="El boletín lo sitúa a 38 kilómetros al nororiente de Armenia. Esa es una distancia de ubicación, no el recorrido por carretera. La coordenada impresa en ese boletín mezcla grados y minutos, así que no se copia.",
    tags=["quindío", "paramillo", "4700"],
), ["geography.paramillo_santa_rosa", "geography.salento_quindio", "geography.glacier_summits"])

add(entry(
    "geography.paramillo_cisne", "cota del Cisne y Morro Negro", "fact",
    [
        "qué es el Paramillo del Cisne",
        "el Cisne es un nevado o un paramillo",
        "Morro Negro va con el Cisne",
        "paramillo del cisne altura",
        "4700 entre caldas y tolima",
        "es un domo al lado de Santa Isabel",
        "da nombre al sector pero es otra cosa",
        "Cisne-Morro Negro en el ranking del SGC",
        "what is Paramillo del Cisne",
        "is El Cisne one of the snow-capped peaks",
        "queda entre el Ruiz y Santa Isabel",
        "la cabaña El Cisne es la montaña",
    ],
    "En la nota del SGC del 9 de agosto de 2024, el Paramillo del Cisne-Morro Negro está a 4.700 metros, entre Caldas y Tolima. El boletín de la actividad de 2023 da una altura máxima de 4.600 metros y lo describe como un complejo de domos entre el Ruiz y Santa Isabel. La montaña, el sector Cisne-Poleka Kasue y el centro El Cisne no son el mismo sitio.",
    ["El ranking de agosto de 2024 lista el Cisne-Morro Negro a 4.700 metros, entre Caldas y Tolima. El boletín de 2023 dice 4.600 metros de altura máxima: usa la nota reciente para la lista pública y ten presente la otra cifra. No es la cabaña El Cisne."],
    ["geography.sector_cisne_poleka", "geography.santa_isabel", "geography.main_peaks"],
    ["rank", "bulletin", "pnn"],
    tags=["cisne", "morro negro", "paramillo"],
), ["geography.sector_cisne_poleka", "geography.santa_isabel", "geography.main_peaks"])

add(entry(
    "geography.paramillo_santa_rosa", "cota del Paramillo de Santa Rosa", "fact",
    [
        "a qué altura está el Paramillo de Santa Rosa",
        "Paramillo de Santa Rosa",
        "el paramillo queda en Risaralda",
        "santa rosa de cabal es el paramillo o el pueblo",
        "4600 metros publica el SGC",
        "junto con el Quindío enmarca la laguna",
        "ese paramillo es el nevado Santa Isabel",
        "montaña del lado de la Laguna del Otún",
        "how high is Paramillo de Santa Rosa",
        "is Santa Rosa a glacier peak of the park",
        "departamento de Risaralda",
        "4602 metros salen en el boletín",
    ],
    "El ranking del SGC del 9 de agosto de 2024 pone el Paramillo de Santa Rosa en 4.600 metros, en Risaralda. El boletín de la actividad de 2023 precisa 4.602 metros y lo deja contiguo a la Laguna del Otún. No es el municipio de Santa Rosa de Cabal ni el nevado Santa Isabel.",
    ["Santa Rosa, como montaña, queda cerca de 4.600 metros: 4.600 en el ranking del 9 de agosto de 2024 y 4.602 en el boletín de 2023, junto a la Laguna del Otún. El pueblo y Santa Isabel son otros lugares."],
    ["geography.paramillo_quindio", "geography.laguna_otun", "geography.pereira_santa_rosa"],
    ["rank", "bulletin", "pnn"],
    tags=["santa rosa", "paramillo", "4600"],
), ["geography.paramillo_quindio", "geography.laguna_otun", "geography.pereira_santa_rosa"])

add(entry(
    "geography.olleta_pirana", "volcanes La Olleta y La Piraña", "explanation",
    [
        "qué es el volcán La Olleta",
        "La Piraña también es del Ruiz",
        "La Olleta sigue activa",
        "la olleta ya se apago",
        "nereidas entra en el mismo complejo",
        "la ficha nombra Olleta y Piraña junto al Ruiz",
        "altura de La Olleta",
        "volcanes al lado del cráter Arenas",
        "what are La Olleta and La Piraña",
        "are those cones still active",
        "el complejo del Ruiz no es solo la cima",
        "Nereidas lo nombra el SGC",
    ],
    "La Olleta, La Piraña y Nereidas son volcanes que el SGC describe como no activos, en el complejo del Ruiz. La hoja de septiembre de 2024 y el boletín del segmento norte lo dicen así, y la ficha del parque nombra los cráteres La Olleta y La Piraña junto a Kumanday. Esas páginas no publican la altura de estos conos.",
    ["Olleta, Piraña y Nereidas acompañan al Ruiz y el SGC los trata como volcanes que no están activos. No hay una cota de esos conos en las páginas consultadas."],
    ["geography.ruiz_identity", "geography.arenas_crater", "geography.volcanic_centers"],
    ["sheet", "bulletin", "pnn"],
    tags=["olleta", "piraña", "nereidas"],
), ["geography.arenas_crater", "geography.ruiz_identity", "geography.volcanic_centers"])

add(entry(
    "geography.glacier_summits", "cumbres del parque con glaciar", "explanation",
    [
        "qué cumbres del parque tienen glaciar",
        "cuáles nevados siguen con hielo",
        "Santa Isabel todavía tiene nieve",
        "el ruiz tiene casquete glaciar",
        "ruiz santa isabel y tolima son los tres",
        "los paramillos tienen glaciar en la ficha",
        "dónde hay hielo en Los Nevados",
        "el glaciar cambia de un año a otro",
        "which summits still have glaciers",
        "does Santa Isabel still have ice",
        "el Ideam describe hielo en las tres",
        "ver la nieve depende del día",
    ],
    "La ficha asocia el glaciar del parque con tres volcanes: Ruiz, Santa Isabel y Tolima. El Ideam sigue describiendo hielo en esas tres cumbres. Cuánto queda cambia con los años; para el retroceso mira las páginas del Ideam cuando tengas conexión.",
    ["Ruiz, Santa Isabel y Tolima son las tres cumbres a las que la ficha y el Ideam asocian el hielo. Cuánto queda cambia; el Ideam es quien publica esa actualización."],
    ["geography.santa_isabel", "geography.main_peaks", "geography.laguna_verde"],
    ["pnn", "ideam_ruiz", "ideam_santa", "ideam_tolima"],
    detail="El Ideam publica aparte cuánto hielo queda y cómo ha cambiado. Esta respuesta solo dice en qué cumbres ese hielo sigue descrito.",
    tags=["glaciar", "hielo"],
), ["geography.laguna_verde", "geography.santa_isabel", "geography.paramillo_quindio"])

add(entry(
    "geography.highest_in_park", "cumbre más alta del parque", "fact",
    [
        "cuál es la cumbre más alta del parque",
        "el punto más alto de Los Nevados",
        "el Ruiz le gana al Tolima en metros",
        "que montaña es la mas alta alla",
        "5321 contra 5215",
        "Santa Isabel queda por debajo de las dos",
        "dentro del parque, no en Colombia",
        "comparación de las cotas publicadas",
        "what is the highest summit in the park",
        "is Ruiz higher than Tolima",
        "la más alta de las cumbres nombradas",
        "cuál nevado supera los 5.300 metros",
    ],
    "Entre las cotas publicadas, el Ruiz a 5.321 metros queda por encima del Tolima a 5.215 y de Santa Isabel, cuyas cumbres el Ideam pone bajo 5.000 metros y el SGC lista a 4.965. Con esas cifras, el Ruiz es la cumbre más alta medida dentro del parque.",
    ["Si comparas las alturas publicadas, 5.321 metros del Ruiz superan los 5.215 del Tolima y las cotas de Santa Isabel, todas bajo 5.000 en el Ideam y 4.965 en el ranking del SGC. Por eso el Ruiz es la cima más alta de este parque."],
    ["geography.ruiz_height", "geography.ruiz_versus_huila", "geography.tolima_height"],
    ["sheet", "rank", "ideam_ruiz", "ideam_tolima", "ideam_santa"],
    detail="La comparación usa las cotas de las cumbres nombradas por el SGC y el Ideam. No es un barrido nuevo de todo el polígono.",
    tags=["cima", "más alta"],
), ["geography.ruiz_versus_huila", "geography.ruiz_height", "geography.tolima_height"])

add(entry(
    "geography.ruiz_versus_huila", "Ruiz y el Nevado del Huila", "fact",
    [
        "el Ruiz es el volcán más alto de Colombia",
        "qué volcán colombiano lo supera",
        "el Huila es más alto que el Ruiz",
        "el ruiz es el mas alto del pais",
        "5364 contra 5321",
        "el Huila está en este parque",
        "segundo puesto en el ranking del SGC",
        "Cauca Huila y Tolima son del otro nevado",
        "is Nevado del Ruiz the highest volcano in Colombia",
        "which volcano is taller than the Ruiz",
        "los 10 más altos, puesto del Ruiz",
        "ranking del 9 de agosto de 2024",
    ],
    "En el ranking del SGC del 9 de agosto de 2024 el más alto es el Nevado del Huila, con 5.364 metros, entre Cauca, Tolima y Huila. El Ruiz figura segundo, con 5.321 metros, y es la cumbre más alta de las publicadas dentro de Los Nevados.",
    ["El Huila, a 5.364 metros, supera al Ruiz, a 5.321, en la nota del 9 de agosto de 2024. El Huila queda fuera de este parque."],
    ["geography.highest_in_park", "geography.ruiz_height"],
    ["rank"],
    tags=["huila", "ranking"],
), ["geography.highest_in_park", "geography.ruiz_height", "geography.tolima_volcano"])

add(entry(
    "geography.watersheds", "vertientes Cauca y Magdalena", "explanation",
    [
        "a qué ríos grandes cae el agua del parque",
        "qué ríos nacen hacia cada vertiente",
        "el agua baja al Cauca o al Magdalena",
        "rios que salen de los nevados",
        "chinchina otun guali y lagunilla",
        "Campoalegre y Quindío también",
        "Totare y Coello por el Tolima",
        "Azufrado y Recio por el Ruiz",
        "which rivers drain Los Nevados",
        "does the park feed both the Cauca and the Magdalena",
        "el parque reparte agua hacia las dos hoyas",
        "de qué lado cae el Chinchiná",
    ],
    "El parque está en la cordillera Central y su agua baja hacia el Cauca y hacia el Magdalena. Por el Cauca se cuentan, entre otros, el Otún y el Chinchiná; por el Magdalena, el Gualí, el Lagunilla y el Recio.",
    ["Son dos vertientes: Cauca y Magdalena. Por el Cauca están, entre otros, el Otún y el Chinchiná; por el Magdalena, el Gualí, el Azufrado, el Lagunilla, el Recio y el Coello."],
    ["geography.rio_otun", "geography.rio_chinchina", "geography.cordillera_central"],
    ["pnn", "carder", "ideam_ruiz", "ideam_tolima", "ideam_santa"],
    steps=[[
        "Hacia el Cauca, la ficha Ramsar pone el Otún y el Ideam pone la subzona Chinchiná. Hacia el Magdalena, el Ideam asocia al Ruiz el Azufrado y el Gualí en el Medio Magdalena, y el Lagunilla y el Recio en el Alto Magdalena; al Tolima le asocia el Coello, también en el Alto Magdalena. La subzona Totare sale en esa tabla sin la hoya escrita. No es la lista de cada quebrada.",
    ]],
    detail="La Carder dice que en el parque nacen las cuencas altas del Otún y del Campoalegre, y que también protege las del Chinchiná, el Quindío y el Combeima. No dice a qué hoya caen Campoalegre, Quindío y Combeima. La Gobernación del Tolima pone el nacimiento del Totare en la Laguna del Encanto, sin decir que esa laguna esté dentro del polígono.",
    tags=["río", "cauca", "magdalena"],
), ["geography.rio_otun", "geography.rio_chinchina", "geography.cordillera_central"])

add(entry(
    "geography.rio_otun", "nacimiento del río Otún", "fact",
    [
        "en qué laguna empieza el río Otún",
        "el Otún sale de la laguna",
        "a qué altura nace el río según Ramsar",
        "el rio otun nace a 4000",
        "la cabecera está en Pereira",
        "cae a la cuenca del Cauca",
        "la laguna y el río comparten origen",
        "nacimiento del Otún en el parque",
        "where does the Otún river start",
        "is the river born in the lake",
        "4.000 metros es la ficha de 2006",
        "cabecera en la Laguna del Otún",
    ],
    "El río Otún nace en la Laguna del Otún, en Pereira, y hace parte de la cuenca del Cauca. La ficha Ramsar del 17 de julio de 2006 publica esa cabecera a 4.000 metros. Es la cota de ese documento, no un levantamiento nuevo.",
    ["El Otún empieza en su laguna, del lado de Pereira, camino a la cuenca del Cauca. Los 4.000 metros son los de la ficha Ramsar de 2006, no una medición de este año."],
    ["geography.laguna_otun", "geography.laguna_otun_formation", "geography.watersheds"],
    ["ramsar", "carder", "pnn"],
    tags=["otún", "nacimiento", "4000"],
), ["geography.laguna_otun", "geography.laguna_otun_formation", "geography.watersheds"])

add(entry(
    "geography.rio_chinchina", "nacimiento del río Chinchiná", "explanation",
    [
        "de qué lado del Ruiz baja el Chinchiná",
        "el Chinchiná nace en el Ruiz",
        "chinchina baja hacia el cauca",
        "la cuenca alta es valor de conservación del parque",
        "Río Claro y Río Blanco van por esa subzona",
        "lado occidental del Ruiz",
        "el agua del Ruiz y el Chinchiná",
        "de dónde sale el río Chinchiná",
        "where does the Chinchiná river come from",
        "does the Ruiz drain toward Chinchiná",
        "tabla del Ideam, subzona Chinchiná",
        "Villamaría y la vertiente caldense",
    ],
    "La ficha incluye la cuenca alta del Chinchiná entre lo que conserva el parque, y el Ideam muestra que parte del hielo del Ruiz drena a esa subzona, hacia el Cauca. En la misma tabla aparecen el río Chinchiná, el Río Claro y el Río Blanco.",
    ["El Chinchiná cabecea en el lado del Ruiz que mira al Cauca. El Ideam lo agrupa con el Río Claro y el Río Blanco, y el parque nombra esa cuenca alta."],
    ["geography.watersheds", "geography.ruiz_where", "geography.villamaria_caldas"],
    ["pnn", "ideam_ruiz", "carder"],
    tags=["chinchiná", "cauca"],
), ["geography.watersheds", "geography.rio_otun", "geography.villamaria_caldas"])

add(entry(
    "geography.ruiz_age", "edad geológica del Ruiz", "explanation",
    [
        "qué edad tiene el Nevado del Ruiz",
        "cuántos años tiene el volcán",
        "66.000 años o 1,8 millones",
        "cuantos años tiene el nevado del ruiz",
        "el complejo es más viejo que la cima actual",
        "edad del edificio y edad del conjunto",
        "hoja del SGC de septiembre de 2024",
        "el Ruiz ancestral es otra etapa",
        "how old is Nevado del Ruiz",
        "is the volcano 66 thousand or 1.8 million years old",
        "edad geológica, no una erupción",
        "La Olleta nace en una etapa del complejo",
    ],
    "La hoja del SGC de septiembre de 2024 estima en unos 66.000 años el volcán que se ve hoy y en 1,8 millones de años la historia del complejo, donde también están La Olleta y La Piraña. Son dos edades distintas. No es la fecha de una erupción.",
    ["Unos 66.000 años corresponden al Ruiz actual, según la hoja de 2024, y unos 1,8 millones al complejo. Si juntas las dos cifras, estás mezclando dos historias, y ninguna es el año de una erupción."],
    ["geography.ruiz_identity", "geography.olleta_pirana", "geography.volcanic_centers"],
    ["sheet", "bulletin"],
    detail="El boletín detalla el Ruiz ancestral entre 1,8 y 0,97 millones de años, y la etapa inicial del edificio actual en 66 mil años, con un margen de 5,6 mil, y 26,8 mil años, con el mismo margen. La respuesta corta usa la hoja pública de 2024.",
    tags=["edad", "ruiz"],
), ["geography.ruiz_identity", "geography.geoheritage", "geography.volcanic_centers"])

add(entry(
    "geography.volcanic_centers", "volcanes activos del complejo", "explanation",
    [
        "cuáles volcanes del parque están activos",
        "el Tolima está apagado para siempre",
        "Santa Isabel también lo monitorean",
        "la olleta no esta activa",
        "el Ruiz es el estratovolcán del complejo",
        "Cisne Quindío y Santa Rosa están en la red del SGC",
        "reposo y activo no son la misma palabra",
        "qué volcán del macizo tiene el cráter Arenas",
        "which volcanoes here does the geological service call active",
        "does inactive mean La Olleta is extinct forever",
        "Cerro Bravo está en la lista del parque",
        "la alerta de hoy dónde se mira",
    ],
    "La hoja del SGC de septiembre de 2024 describe al Ruiz como estratovolcán con el cráter activo Arenas, y a La Olleta, La Piraña y Nereidas como volcanes que no están activos. El color de alerta de hoy no está en esta guía: míralo en el SGC cuando tengas conexión.",
    ["El Ruiz es el volcán al que el SGC asigna el cráter activo Arenas. Olleta, Piraña y Nereidas figuran como no activos en la hoja de 2024. La alerta de esta semana se consulta en el SGC; aquí no viene."],
    ["geography.ruiz_identity", "geography.olleta_pirana", "geography.glacier_summits"],
    ["sheet", "bulletin"],
    detail="El SGC vigila un segmento más amplio que las cumbres de la ficha. En ese listado también están Cerro Bravo, Cerro España y Cerro Machín, que la ficha del parque no nombra entre sus montañas. El color de alerta de cualquier año se consulta en el boletín vigente del SGC.",
    tags=["activo", "alerta", "sgc"],
), ["geography.olleta_pirana", "geography.ruiz_identity", "geography.ruiz_faults"])

add(entry(
    "geography.geoheritage", "patrimonio geológico del Ruiz", "fact",
    [
        "el Ruiz es patrimonio geológico",
        "la IUGS lo incluyó entre cien sitios",
        "patrimonio geológico internacional del volcán",
        "patrimonio natural de la nacion en 2025",
        "la unesco geologica y el ruiz",
        "qué reconocimiento tiene el Nevado del Ruiz",
        "sitio de patrimonio geológico",
        "cien sitios de relevancia internacional",
        "is the Ruiz a geological heritage site",
        "what does the IUGS listing mean",
        "el parque dice patrimonio natural de la nación",
        "desde cuándo está en esa lista",
    ],
    "Desde 2022, la IUGS reconoce al Nevado del Ruiz como uno de 100 sitios de patrimonio geológico de relevancia internacional.",
    ["El Ruiz está, desde 2022, entre los 100 sitios de patrimonio geológico de la IUGS. Así lo dice la hoja del SGC de septiembre de 2024."],
    ["geography.ruiz_identity", "geography.arenas_crater"],
    ["sheet", "pnn"],
    detail="La hoja de septiembre de 2024 dice que ese reconocimiento de la IUGS, vinculada a la Unesco, es desde 2022. La ficha del parque añade que en 2025 el Nevado del Ruiz fue declarado Patrimonio Natural de la Nación por su valor simbólico, ambiental y por ser parte de un ecosistema esencial para la vida que ordena el territorio alrededor del agua.",
    tags=["iugs", "patrimonio"],
), ["geography.ruiz_identity", "geography.arenas_crater", "geography.ruiz_age"])

add(entry(
    "geography.ruiz_faults", "fallas Palestina y Villamaría", "explanation",
    [
        "en qué fallas está el Ruiz",
        "falla de Palestina y falla Termales Villamaría",
        "por qué hay un volcán en ese cruce",
        "por que hay un volcan ahi",
        "geologia del limite caldas tolima",
        "qué fallas destaca el SGC",
        "la cordillera Central y las fallas del Ruiz",
        "ubicación estructural del estratovolcán",
        "why is the Ruiz on those faults",
        "which faults does the geological service mention",
        "Palestina y Termales-Villamaría",
        "el volcán está en un cruce de fallas",
    ],
    "El Ruiz está en la cordillera Central, en el límite de Caldas y Tolima, donde el SGC señala el cruce de varios sistemas de fallas. Las que destaca en su hoja de septiembre de 2024 son Palestina y Termales-Villamaría. Eso ubica el volcán; la alerta de esta semana se mira en el boletín del SGC.",
    ["Palestina y Termales-Villamaría son las fallas que la hoja de 2024 resalta bajo el Ruiz. Para saber cómo está el volcán ahora, abre el boletín del SGC: el nombre de la falla no lo reemplaza."],
    ["geography.ruiz_where", "geography.ruiz_identity", "geography.volcanic_centers"],
    ["sheet"],
    tags=["falla", "palestina"],
), ["geography.ruiz_where", "geography.volcanic_centers", "geography.ruiz_identity"])

add(entry(
    "geography.summit_line", "cumbre que queda más al norte", "explanation",
    [
        "cuál nevado queda más al norte",
        "el Ruiz está al norte del Tolima",
        "de norte a sur cuáles van",
        "el tolima es el del sur",
        "4 grados 53 contra 4 grados 39",
        "en qué orden nombra el SGC el segmento",
        "Cerro Bravo está en el parque",
        "Cisne queda entre el Ruiz y Santa Isabel",
        "which summit is the northernmost",
        "is the Ruiz north of Tolima",
        "latitud del Ruiz y latitud del Tolima",
        "el Quindío queda antes del Tolima en la lista",
    ],
    "El Ruiz queda más al norte que el Tolima. El boletín del SGC lo pone a 4°53'43'' norte y el Ideam pone el Tolima cerca de 4°39' norte.",
    ["De las cumbres del parque, el Ruiz está al norte del Tolima. La diferencia sale de las latitudes publicadas: cerca de 4°53' norte para el Ruiz y cerca de 4°39' para el Tolima."],
    ["geography.main_peaks", "geography.ruiz_where", "geography.tolima_volcano"],
    ["bulletin", "ideam_tolima"],
    detail="El boletín enumera, sin llamarlo un camino de norte a sur, Ruiz, Cisne, Santa Isabel, Santa Rosa, Quindío y Tolima, y dice que el Cisne está entre el Ruiz y Santa Isabel. En esa red también están Cerro Bravo, Cerro España y Cerro Machín, que la ficha del parque no incluye entre sus cumbres. El orden de la lista no es un itinerario.",
    tags=["norte", "latitud"],
), ["geography.main_peaks", "geography.ruiz_where", "geography.tolima_volcano"])

add(entry(
    "geography.risaralda_share", "porcentaje del parque en Risaralda", "fact",
    [
        "qué parte del parque está en Risaralda",
        "qué porcentaje les toca a Pereira y Santa Rosa",
        "35,6 por ciento según la Carder",
        "risaralda tiene mas de un tercio",
        "me dijeron que Risaralda tiene como un tercio",
        "cuánta área es de Pereira y Santa Rosa",
        "Otún y Campoalegre salen por ese lado",
        "porcentaje de Risaralda",
        "how much of the park is in Risaralda",
        "what share do Pereira and Santa Rosa hold",
        "un tercio largo del polígono",
        "la Carder publicó el 35,6",
    ],
    "La Carder informó el 14 de julio de 2026 que Pereira y Santa Rosa de Cabal concentran el 35,6 por ciento del parque. En ese lado risaraldense están la Laguna del Otún y la cuenca alta del Campoalegre.",
    ["Risaralda, por Pereira y Santa Rosa, tiene el 35,6 por ciento del área según la Carder en julio de 2026. La Laguna del Otún queda de ese lado."],
    ["geography.park_area", "geography.pereira_santa_rosa", "geography.laguna_otun"],
    ["carder"],
    detail="La ficha de Parques Nacionales no repite ese porcentaje. La cifra es de la autoridad ambiental de Risaralda.",
    tags=["risaralda", "35,6"],
), ["geography.park_area", "geography.pereira_santa_rosa", "geography.laguna_otun"])

add(entry(
    "geography.salento_quindio", "Salento en el área protegida", "fact",
    [
        "el parque llega a Salento",
        "Salento es el municipio quindiano del área",
        "Armenia está dentro de Los Nevados",
        "en quindio solo nombran a salento",
        "la ficha escribe Salento",
        "lado quindiano del sector Dulima",
        "Salento sí está en los diez municipios",
        "el pueblo de Salento es la cumbre",
        "does the park reach Salento",
        "is Armenia inside Los Nevados",
        "un municipio quindiano en el texto oficial",
        "Cocora es la vereda que nombra la ficha",
    ],
    "En Quindío, la ficha nombra a Salento entre los municipios del área protegida. No nombra a Armenia. Salento es también una llegada publicada hacia el sector Quindío-Dulima, por la vereda Cocora.",
    ["El municipio quindiano que la ficha escribe es Salento. Armenia no aparece en esa lista, y por Salento se entra hacia el lado del Tolima."],
    ["geography.sector_quindio_dulima", "geography.paramillo_quindio", "geography.municipalities"],
    ["pnn"],
    tags=["salento", "quindío"],
), ["geography.sector_quindio_dulima", "geography.paramillo_quindio", "geography.municipalities"])

add(entry(
    "geography.villamaria_caldas", "Villamaría en el lado caldense", "fact",
    [
        "Villamaría hace parte del parque",
        "el municipio caldense es Villamaría",
        "el glaciar del Ruiz pasa por Villamaría",
        "villamaria o manizales cual es",
        "caldas tiene un municipio en la lista de diez",
        "veredas El Páramo y Potosí salen de Villamaría",
        "lado caldense del Ruiz",
        "is Villamaría inside the national park",
        "which Caldas municipality does the park include",
        "Ideam y Villamaría en el glaciar",
        "desde Villamaría se habla del sector Cisne",
        "Villamaría está en la ficha",
    ],
    "Villamaría es el municipio de Caldas que la ficha incluye en el parque. El Ideam también lo pone en la jurisdicción del glaciar del Ruiz, junto con Murillo y Casabianca. Hacia el sector del Cisne, la ficha nombra las veredas El Páramo y Potosí al salir de Villamaría.",
    ["Del lado caldense, el municipio que sí nombra la ficha es Villamaría. El Ideam lo incluye en el glaciar del Ruiz, con Murillo y Casabianca."],
    ["geography.manizales_outside", "geography.ruiz_where", "geography.sector_cisne_poleka"],
    ["pnn", "ideam_ruiz"],
    tags=["villamaría", "caldas"],
), ["geography.manizales_outside", "geography.ruiz_where", "geography.murillo_ruiz"])

add(entry(
    "geography.tolima_municipalities", "municipios tolimenses del parque", "fact",
    [
        "qué municipios del Tolima toca el parque",
        "Murillo Anzoátegui Ibagué Santa Isabel Casabianca y Herveo",
        "seis nombres tolimenses en la ficha",
        "el libano esta en la lista del parque",
        "Herveo y Casabianca sí aparecen",
        "Santa Isabel es municipio y también es nevado",
        "lista tolimense del área protegida",
        "Armero está entre los diez",
        "which Tolima towns overlap Los Nevados",
        "does the park include Herveo and Casabianca",
        "el Tolima tiene seis municipios en la ficha",
        "Casabianca queda del lado del Ruiz",
    ],
    "En el Tolima, la ficha nombra seis municipios: Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca y Herveo. El Líbano y Armero no están en esa lista. El nombre cubre la parte del municipio que entra al área.",
    ["Los seis del Tolima en la ficha son Murillo, Anzoátegui, Ibagué, Santa Isabel, Casabianca y Herveo. Santa Isabel, en esta lista, es el municipio."],
    ["geography.municipalities", "geography.murillo_ruiz", "geography.ibague_highlands"],
    ["pnn"],
    tags=["tolima", "municipio"],
), ["geography.municipalities", "geography.murillo_ruiz", "geography.ibague_highlands"])

add(entry(
    "geography.pereira_santa_rosa", "Pereira y Santa Rosa de Cabal", "fact",
    [
        "Pereira queda dentro del parque",
        "Santa Rosa de Cabal también entra",
        "la ciudad de Pereira es la laguna",
        "pereira queda en los nevados",
        "los dos municipios risaraldenses de la ficha",
        "la parte alta de Pereira",
        "El Cedral está en la laguna",
        "are Pereira and Santa Rosa inside the park",
        "is downtown Pereira part of the national park",
        "la ficha los nombra a los dos",
        "vereda El Bosque del lado de Pereira",
        "35,6 por ciento de esos dos municipios",
    ],
    "Pereira y Santa Rosa de Cabal son los dos municipios de Risaralda que la ficha incluye. La Laguna del Otún está en la parte alta, no en el centro de Pereira. La Carder, el 14 de julio de 2026, les asigna juntas el 35,6 por ciento del área.",
    ["Sí entran Pereira y Santa Rosa de Cabal, por su zona alta. La ciudad de Pereira no es la laguna, y el 35,6 por ciento es la cifra de la Carder del 14 de julio de 2026 para los dos municipios juntos."],
    ["geography.laguna_otun", "geography.risaralda_share", "geography.sector_laguna_otun"],
    ["pnn", "carder", "ramsar"],
    tags=["pereira", "santa rosa"],
), ["geography.sector_laguna_otun", "geography.risaralda_share", "geography.ucumari_buffer"])

add(entry(
    "geography.ibague_highlands", "Ibagué en la parte alta", "fact",
    [
        "Ibagué queda dentro del nevado",
        "el municipio de Ibagué sí está en la ficha",
        "la parte alta de Ibagué toca el Tolima",
        "ibague es el parque o solo la vereda",
        "Juntas es la referencia de acceso",
        "Anzoátegui comparte ese volcán con Ibagué",
        "el casco urbano y el glaciar",
        "is the city of Ibagué inside the park",
        "does Ibagué municipality reach Nevado del Tolima",
        "Ibagué está en la lista de diez",
        "Ideam: glaciar en jurisdicción de Ibagué",
        "la ciudad de Ibagué es la cima",
    ],
    "Ibagué está en la lista de municipios del parque, y el Ideam pone el glaciar del Tolima en su jurisdicción, junto con Anzoátegui. Eso es la parte alta del municipio. La ficha usa la vereda Juntas como referencia de llegada; el camino se confirma en cómo llegar.",
    ["El municipio de Ibagué sí llega al Nevado del Tolima por su zona alta, según la ficha y el Ideam. La ciudad no es el glaciar, y Juntas es la referencia de llegada que publica el parque."],
    ["geography.tolima_volcano", "geography.sector_quindio_dulima", "geography.tolima_municipalities"],
    ["pnn", "ideam_tolima"],
    tags=["ibagué", "juntas"],
), ["geography.tolima_volcano", "geography.sector_quindio_dulima", "geography.tolima_height"])

add(entry(
    "geography.murillo_ruiz", "Murillo en el lado del Ruiz", "fact",
    [
        "Murillo queda junto al Ruiz",
        "el municipio de Murillo entra al parque",
        "Murillo es Tolima y el volcán queda en el límite",
        "murillo queda debajo del ruiz",
        "el Ideam lo pone en el glaciar del Ruiz",
        "Casabianca es el otro tolimense de ese hielo",
        "is Murillo inside Los Nevados",
        "does the Ruiz glacier reach Murillo",
        "pueblo tolimense del límite con Caldas",
        "Murillo y Villamaría comparten el glaciar",
        "el casco de Murillo es la cima",
        "sector norte visto desde el Tolima",
    ],
    "Murillo, en el Tolima, está en la lista de municipios del parque. El Ideam lo incluye en la jurisdicción del glaciar del Ruiz, junto con Casabianca y Villamaría. El volcán queda en el límite Caldas-Tolima; el casco de Murillo no es la cima.",
    ["Murillo sí entra en el área y en la jurisdicción del hielo del Ruiz, con Casabianca y Villamaría. El pueblo y la cumbre son dos puntos distintos."],
    ["geography.ruiz_where", "geography.tolima_municipalities", "geography.villamaria_caldas"],
    ["pnn", "ideam_ruiz"],
    tags=["murillo", "ruiz"],
), ["geography.ruiz_where", "geography.villamaria_caldas", "geography.sector_brisas_kumanday"])

add(entry(
    "geography.ucumari_buffer", "Ucumarí junto al parque nacional", "explanation",
    [
        "Ucumarí es el Parque Los Nevados",
        "el parque regional Ucumarí queda dentro del nacional",
        "Campoalegre es zona amortiguadora",
        "ucumari es otro parque",
        "la Carder los separa",
        "El Cedral está en Ucumarí",
        "conecta con el parque nacional",
        "zona amortiguadora de Risaralda",
        "is Ucumarí part of Los Nevados",
        "what is the buffer next to the national park",
        "Distrito de Conservación de Suelos Campoalegre",
        "la Laguna del Otún es de Ucumarí o de Los Nevados",
    ],
    "El Parque Regional Natural Ucumarí no es el Parque Nacional Natural Los Nevados. La Carder, el 14 de julio de 2026, lo describe junto con el Distrito de Conservación de Suelos Campoalegre como zona amortiguadora que conecta con el parque nacional. La Laguna del Otún sí está dentro de Los Nevados.",
    ["Ucumarí y Campoalegre acompañan al parque nacional por Risaralda y la Carder los trata como zona amortiguadora. La laguna del Otún sigue siendo de Los Nevados."],
    ["geography.laguna_otun", "geography.pereira_santa_rosa", "geography.rio_otun"],
    ["carder", "pnn", "ramsar"],
    tags=["ucumarí", "campoalegre"],
), ["geography.laguna_otun", "geography.rio_otun", "geography.pereira_santa_rosa"])

add(entry(
    "geography.tolima_crater", "cráter del Nevado del Tolima", "explanation",
    [
        "el Tolima tiene cráter",
        "cómo es el cráter del Tolima",
        "El Oído son fumarolas antes de la cima",
        "el crater del tolima se llama arenas",
        "volcán cónico con fumarolas cerca de la cumbre",
        "el Ideam menciona El Oído",
        "Arenas es del Ruiz",
        "una cumbre y un cráter",
        "does Tolima have its own crater",
        "what is El Oído on the Tolima",
        "fumarolas antes de la cima del Tolima",
        "el cráter del Tolima está en la cumbre",
    ],
    "El Tolima tiene su propio cráter: el Ideam lo describe en un estratovolcán de una sola cumbre y menciona fumarolas en el punto que los montañistas llaman El Oído, antes de la cima. No es el cráter Arenas, que es del Ruiz. Si ese tramo está autorizado, se confirma con el parque.",
    ["El Tolima tiene cráter y fumarolas cerca de la cima, en el sitio llamado El Oído. Arenas es el cráter del Ruiz, y la autorización del tramo la da el parque."],
    ["geography.tolima_volcano", "geography.arenas_crater", "geography.tolima_height"],
    ["ideam_tolima"],
    tags=["cráter", "tolima", "oído"],
), ["geography.arenas_crater", "geography.tolima_volcano", "geography.tolima_height"])


def normalized(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


def sentence_count(text):
    masked = re.sub(r"\d\.\d", lambda match: match.group(0).replace(".", ""), text)
    parts = re.split(r"[.!?]+", masked)
    return len([part for part in parts if part.strip()])


def main():
    by_id = {item["id"]: item for item in ENTRIES}
    errors = []
    if len(ENTRIES) != len(by_id):
        errors.append("duplicate ids")
    seen = {}
    for item in ENTRIES:
        words = item["label"].split()
        if not 3 <= len(words) <= 8:
            errors.append(f"label words {item['id']}: {len(words)} {item['label']}")
        if len(item["examples"]) < 12 or len(set(item["examples"])) != len(item["examples"]):
            errors.append(f"examples {item['id']}")
        if not 1 <= len(item["answer"]["variants"]) <= 2:
            errors.append(f"variants {item['id']}")
        if not 1 <= len(item["related"]) <= 3:
            errors.append(f"related count {item['id']}")
        for related in item["related"]:
            if related not in by_id:
                errors.append(f"missing related {item['id']} -> {related}")
        if sentence_count(item["answer"]["short"]) > 3:
            errors.append(f"short sentences {item['id']}: {item['answer']['short']}")
        for variant in item["answer"]["variants"]:
            if sentence_count(variant) > 3:
                errors.append(f"variant sentences {item['id']}: {variant}")
        for example in item["examples"]:
            key = normalized(example)
            seen.setdefault(key, []).append(item["id"])
        item["hard_negatives"] = []
        for other_id in item["_neg"]:
            item["hard_negatives"].append(by_id[other_id]["examples"][0])
        if not 2 <= len(item["hard_negatives"]) <= 4:
            errors.append(f"negatives {item['id']}")
        del item["_neg"]
    for key, owners in seen.items():
        if len(owners) > 1:
            errors.append(f"dup example {key}: {owners}")
    labels = [(item["id"], normalized(item["label"])) for item in ENTRIES]
    for index, (id_a, label_a) in enumerate(labels):
        for id_b, label_b in labels[index + 1:]:
            ratio = SequenceMatcher(None, label_a, label_b).ratio()
            if ratio >= 0.88:
                errors.append(f"similar labels {id_a} / {id_b} {ratio:.3f}")
    banned = ("desde este entorno", "norma que revis", "aval de esta", "patrimonio de la aplicación", " oiga", " venga", "parce")
    for item in ENTRIES:
        blob = json.dumps(item["answer"], ensure_ascii=False).lower()
        for phrase in banned:
            if phrase in blob:
                errors.append(f"banned {phrase} in {item['id']}")
    if errors:
        raise SystemExit("\n".join(errors))
    section = {
        "contract_version": 1,
        "id": "geography",
        "order": 13,
        "title": "Geografía del parque",
        "description": "Nevados, paramillos, alturas, lagunas, ríos, departamentos, municipios, sectores y la diferencia entre el área protegida y el volcán.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.25,
            "top_k": 3,
            "min_score": None,
            "entity_filters": ["landform", "sector"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Preguntas por el parque completo o por una cumbre en particular?",
                "¿Cuál te interesa: Ruiz, Santa Isabel, Tolima, Quindío o Cisne?",
                "¿Buscas una laguna: Otún, Verde o del Encanto?",
                "¿Hablas de un sector de visita o de la montaña que le da nombre?",
                "¿Quieres la ubicación, la altura o la diferencia entre el parque y el volcán?",
                "¿La duda es el departamento, el municipio o la cordillera?",
                "¿Preguntas por el cráter Arenas del Ruiz o por el cráter del Tolima?",
            ],
            "slot_questions": {
                "landform": "¿Preguntas por un nevado, una laguna, un río, un cráter o por el parque completo?",
                "sector": "¿Te interesa Brisas-Kumanday, Cisne-Poleka Kasue, la Laguna del Otún o Quindío-Dulima?",
            },
            "fallback": "Puedo ubicarte los nevados, las lagunas, los sectores y los departamentos del parque. Dime cuál de esos lugares tienes en mente.",
        },
        "featured": [
            "geography.main_peaks",
            "geography.ruiz_height",
            "geography.park_versus_volcano",
            "geography.laguna_otun",
            "geography.four_sectors",
        ],
        "entries": ENTRIES,
    }
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n")
    examples = sum(len(item["examples"]) for item in ENTRIES)
    print(f"entries {len(ENTRIES)} examples {examples}")


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: geography now builds from geography/source/geography.v1.json via coordination/build_from_snapshot.py geography; rerunning this script would revert reviewed corrections.")
    main()
