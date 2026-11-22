"""Part 1 of fauna entries: Overview (1-9) and Birds (10-30)."""
from sources import (
    SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA,
    SOURCE_HUMBOLDT, SOURCE_EBIRD, SOURCE_CARDER, SOURCE_CORPOCALDAS, SOURCE_CORTOLIMA
)

ENTRIES_PART1 = [
    # 1. Overview
    {
        "id": "fauna.fauna_overview",
        "label": "fauna silvestre presente en Los Nevados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna de Los Nevados",
            "¿qué animales viven en el parque?",
            "animales del nevado",
            "qué bichos o fieras hay en el parque",
            "fauna silvestre en la alta montaña",
            "¿cuántas especies de animales hay en Los Nevados?",
            "animales tipicos del parque los nevados",
            "cuales animales puedo encontrar en el parque",
            "¿qué vida silvestre habita en esta reserva?",
            "fauna salvaje de los nevados",
            "what wildlife lives in Los Nevados National Park?",
            "which animals can I spot in Los Nevados?",
            "animalitos que se ven en el parque",
            "especies de animales en el parque nacional"
        ],
        "hard_negatives": [
            "qué plantas crecen en el páramo",
            "cuántos volcanes hay en el parque",
            "cuáles son los senderos habilitados"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El Parque Nacional Natural Los Nevados alberga una extraordinaria biodiversidad adaptada al frío extremo, con 778 especies de vertebrados registradas entre su gradiente de bosque y páramo. Aquí conviven especies emblemáticas como el cóndor andino, la danta de montaña, el oso de anteojos y colibríes únicos como el chivito de páramo. Cada piso térmico ofrece hábitats especializados para aves, mamíferos, anfibios e insectos.",
            "variants": [
                "En Los Nevados habitan 778 especies de vertebrados a lo largo de sus bosques altoandinos y páramos, destacando el cóndor andino, la danta de páramo y el oso de anteojos. La fauna del parque está adaptada a la gran altitud y las bajas temperaturas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.mammals_overview", "fauna.endemic_species"],
        "tags": ["fauna", "biodiversidad", "general", "vertebrados", "especies"]
    },
    # 2. Birds overview (Seed 24 mapping)
    {
        "id": "fauna.birds_overview",
        "label": "las aves del parque Los Nevados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "aves",
            "pájaros",
            "hay cóndores",
            "qué colibríes hay",
            "avistar el chivito de páramo",
            "avistamiento de aves",
            "aves endémicas",
            "hay aves que solo viven aquí",
            "¿cuántas clases de pájaros hay en Los Nevados?",
            "avifauna del parque nacional",
            "pajaritos del páramo",
            "cuales aves se pueden pajarear en el parque",
            "what birds can I see in Los Nevados?",
            "birdwatching in Los Nevados National Park"
        ],
        "hard_negatives": [
            "tours guiados de avistamiento de aves",
            "reglas para acampar en el parque",
            "dónde alquilar binoculares en Manizales"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "Entre las aves registradas en el parque destacan el chivito de páramo, el cóndor andino, el periquito de los nevados y el pato andino. El área protegida reúne 108 especies exclusivas de páramo y humedales altos, y más de 300 especies a lo largo de su gradiente de bosque nublado. Ten presente que la presencia de una especie en los inventarios no asegura su observación durante una caminata corta.",
            "variants": [
                "Si te interesan las aves, en Los Nevados se registran más de 300 especies en total y 108 en el páramo, incluyendo joyas como el chivito de páramo y el periquito de los nevados. Los avistamientos dependen del clima, el sector y la hora del día."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.buffy_helmetcrest", "fauna.ruiz_parakeet"],
        "tags": ["aves", "pajaros", "avifauna", "colibries", "condor", "semilla_24"]
    },
    # 3. Mammals overview (Seed 25 mapping)
    {
        "id": "fauna.mammals_overview",
        "label": "los mamíferos del parque Los Nevados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "mamíferos",
            "hay pumas",
            "hay dantas",
            "qué mamíferos se encuentran",
            "qué es una danta de montaña",
            "¿qué mamíferos viven en Los Nevados?",
            "animales de cuatro patas en el nevado",
            "hay osos en el parque",
            "mamiferos salvajes del paramo",
            "cuales mamiferos habitan en los nevados",
            "what mammals live in Los Nevados?",
            "are there large mammals in Los Nevados National Park?",
            "animales grandes en los senderos",
            "fauna de mamiferos en alta montana"
        ],
        "hard_negatives": [
            "registro de ingreso de mascotas al parque",
            "alquiler de caballos para subir al nevado",
            "vacunas necesarias para viajar a Colombia"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La danta de montaña, el puma, el oso de anteojos y la guagua loba están entre los mamíferos más emblemáticos registrados en el parque. El Plan de Manejo reporta 31 especies adaptadas a la alta montaña y unas 60 en todo el macizo volcánico. Si tienes la fortuna de cruzar caminos con alguno, mantén siempre una distancia prudente y respeta su tranquilidad.",
            "variants": [
                "En el parque habitan mamíferos notables como la danta de páramo, el oso andino, venados de montaña y el puma. Son animales esquivos y de hábitos reservados que debes contemplar siempre a distancia y sin perturbar."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.spectacled_bear", "fauna.mountain_tapir", "fauna.cougar_puma"],
        "tags": ["mamiferos", "danta", "oso", "puma", "fauna", "semilla_25"]
    },
    # 4. Amphibians overview
    {
        "id": "fauna.amphibians_overview",
        "label": "anfibios y ranas de alta montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "anfibios en Los Nevados",
            "¿hay ranas en el páramo?",
            "ranitas de la alta montaña",
            "sapos en el parque los nevados",
            "¿qué anfibios viven con tanto frío?",
            "ranas de páramo en Colombia",
            "especies de ranas en los nevados",
            "anfibios adaptados al paramo",
            "frogs in Los Nevados National Park",
            "are there amphibians in the high paramo?",
            "ranitas del frailejonal",
            "anuros en el parque nacional"
        ],
        "hard_negatives": [
            "enfermedades tropicales y vacunas",
            "humedales y lagunas del parque",
            "calzado impermeable para senderismo"
        ],
        "entities": {"animal_group": ["anfibios"]},
        "needs": [],
        "answer": {
            "short": "A pesar de las heladas nocturnas, en Los Nevados viven anfibios fascinantes como las ranas de lluvia del género Pristimantis y el sapito rechoncho Osornophryne percrassa. Estas especies no necesitan charcas grandes con renacuajos, sino que presentan desarrollo directo dentro de los huevos depositados en musgos y frailejones húmedos. Son animales muy vulnerables al cambio climático y al pisoteo.",
            "variants": [
                "En el parque habitan ranas de páramo como las del género Pristimantis y sapitos Osornophryne, adaptados a sobrevivir bajo rocas y almohadillas de musgo húmedo sin fase acuática de renacuajo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_toad_osornophryne", "fauna.paramo_rain_frogs", "fauna.harlequin_frog_atelopus"],
        "tags": ["anfibios", "ranas", "sapos", "pristimantis", "paramo"]
    },
    # 5. Reptiles overview
    {
        "id": "fauna.reptiles_overview",
        "label": "reptiles y lagartijas del parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "reptiles en Los Nevados",
            "¿hay lagartijas en el páramo?",
            "culebras en el parque",
            "reptiles adaptados al frío",
            "¿se ven lagartijas tomando el sol en las rocas?",
            "serpientes y lagartos en los nevados",
            "lagartos de alta montana",
            "reptiles presentes en el parque nacional",
            "are there reptiles in Los Nevados?",
            "lizards in the Colombian paramo",
            "lagartijitas en los senderos",
            "especies de reptiles del nevado"
        ],
        "hard_negatives": [
            "formaciones rocosas y geología del parque",
            "botiquín de primeros auxilios para montaña",
            "clima y radiación solar en el páramo"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "El parque cuenta con unas 15 especies de reptiles reportadas, siendo las lagartijas collarejas del género Stenocercus las más visibles cuando calienta el sol sobre las rocas. En la hojarasca y musgos viven pequeñas lagartijas Andinosaura y serpientes tierreras inofensivas como Atractus. En las alturas del páramo no existen serpientes venenosas.",
            "variants": [
                "Los reptiles de Los Nevados están adaptados a la radiación solar diurna; verás lagartijas Stenocercus soleándose en piedras y pequeñas culebrillas tierreras inofensivas en el suelo húmedo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_collared_lizard", "fauna.earth_snakes_atractus", "fauna.venomous_snakes_absence"],
        "tags": ["reptiles", "lagartijas", "stenocercus", "serpientes", "alta_montana"]
    },
    # 6. Insects and invertebrates overview
    {
        "id": "fauna.insects_invertebrates_overview",
        "label": "insectos e invertebrados del páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "insectos en Los Nevados",
            "¿hay insectos en el páramo?",
            "bichos en la nieve y el frío",
            "mariposas y abejas en la alta montaña",
            "invertebrados del parque los nevados",
            "¿qué insectos polinizan los frailejones?",
            "artrópodos en el páramo",
            "hay zancudos o mosquitos en el parque",
            "insects in Los Nevados National Park",
            "paramo butterflies and bumblebees",
            "mariposas de alta montana",
            "abejorros de los nevados"
        ],
        "hard_negatives": [
            "repelente de insectos en la lista de equipo",
            "polinización y flora del bosque altoandino",
            "temperatura mínima nocturna en el Ruiz"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "En el páramo habitan invertebrados asombrosos como los abejorros peludos del género Bombus, polinizadores clave de las flores de frailejón. También destacan mariposas oscuras del género Lymanopoda y larvas de tricópteros y efemerópteros en los arroyos glaciares. Debido al frío y la altitud, en las zonas altas no proliferan zancudos ni mosquitos transmisores de enfermedades.",
            "variants": [
                "Los insectos de Los Nevados cumplen funciones ecológicas vitales: los abejorros polinizan la vegetación nativa y las mariposas oscuras absorben calor solar, sin presencia de mosquitos molestos en las cotas altas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_bumblebees", "fauna.paramo_butterflies", "fauna.aquatic_macroinvertebrates"],
        "tags": ["insectos", "invertebrados", "abejorros", "mariposas", "polinizacion"]
    },
    # 7. Endemic species
    {
        "id": "fauna.endemic_species",
        "label": "especies de fauna endémicas del parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "animales endémicos de Los Nevados",
            "¿qué especies solo viven en este parque?",
            "fauna exclusiva de la cordillera central",
            "animales unicos de los nevados",
            "especies endemicas del parque nacional",
            "¿cuáles son los animales exclusivos de aquí?",
            "bichos que no existen en otra parte del mundo",
            "endemismos de fauna en los nevados",
            "endemic wildlife of Los Nevados Colombia",
            "animals found only in Los Nevados",
            "que aves solo se ven aca",
            "fauna endémica de alta montaña"
        ],
        "hard_negatives": [
            "plantas endémicas y tipos de frailejones",
            "historia geológica del macizo volcánico",
            "mapa de departamentos que componen el parque"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El macizo alberga al menos 38 especies de vertebrados endémicas o casi endémicas de Colombia. Entre las aves exclusivas resaltan el chivito de páramo (Oxypogon stuebelii), el periquito de los nevados (Bolborhynchus ferrugineifrons) y el tororoi de Miller (Grallaria milleri). En anfibios y pequeños mamíferos también existen sapitos y roedores de distribución restringida a estas cumbres.",
            "variants": [
                "Los Nevados es un refugio de endemismo con aves únicas en el planeta como el chivito de páramo y el periquito de los nevados, además del tororoi de Miller y anfibios adaptados solo a la Cordillera Central."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.buffy_helmetcrest", "fauna.ruiz_parakeet", "fauna.brown_banded_antpitta"],
        "tags": ["endemicas", "endemismo", "exclusivas", "chivito", "periquito"]
    },
    # 8. Threatened species
    {
        "id": "fauna.threatened_species",
        "label": "fauna en peligro y especies amenazadas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "especies en peligro de extinción en Los Nevados",
            "¿qué animales están amenazados en el parque?",
            "fauna en riesgo en los nevados",
            "animales en peligro crítico",
            "estado de conservación de la fauna",
            "¿el cóndor y la danta están en peligro?",
            "especies vulnerables del parque nacional",
            "cuales animales estan amenazados aqui",
            "endangered species in Los Nevados",
            "threatened animals in Colombian high Andes",
            "animales protegidos en via de extincion",
            "fauna en lista roja en el nevado"
        ],
        "hard_negatives": [
            "sanciones y multas por caza ilegal",
            "retroceso de glaciares por cambio climático",
            "donaciones y voluntariado en Parques Nacionales"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Varias especies icónicas del parque se encuentran bajo categorías de amenaza, entre ellas la danta de montaña (En Peligro), el oso andino (Vulnerable) y el cóndor de los Andes (Vulnerable a nivel nacional). Entre las aves, la cotorra de Fuertes y el periquito de los nevados sufren por la pérdida histórica de hábitat. El parque cumple un papel irremplazable como su santuario de protección.",
            "variants": [
                "En Los Nevados encuentran refugio especies amenazadas como la danta de páramo, el oso de anteojos, el loro orejiamarillo y el cóndor andino, cuyas poblaciones están bajo monitoreo continuo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_tapir", "fauna.spectacled_bear", "fauna.fuertes_parrot"],
        "tags": ["amenazadas", "peligro", "extincion", "conservacion", "lista_roja"]
    },
    # 9. Conservation targets (VOC)
    {
        "id": "fauna.conservation_target_species_voc",
        "label": "valores objeto de conservación de fauna",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "valores objeto de conservación de fauna",
            "¿cuáles son los VOC de fauna en Los Nevados?",
            "especies prioritarias para Parques Nacionales",
            "especies bandera de conservacion en el parque",
            "foco de conservacion de animales en los nevados",
            "¿qué animales monitorea Parques Nacionales?",
            "especies focales del plan de manejo",
            "cuales son los animales diana de proteccion",
            "conservation targets in Los Nevados",
            "focal wildlife species in the management plan",
            "especies clave de fauna protegida",
            "animales prioritarios del parque nacional"
        ],
        "hard_negatives": [
            "objetivos de creación histórica del parque en 1974",
            "cuencas hidrográficas y servicios hídricos del parque",
            "proceso de compra de predios por el Estado"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "En el Plan de Manejo oficial, Parques Nacionales prioriza como Valores Objeto de Conservación faunísticos al periquito de los nevados (Bolborhynchus ferrugineifrons) y al pato andino (Oxyura jamaicensis). Asimismo, especies sombrilla como el oso de anteojos y la danta de páramo reciben monitoreo constante porque protegerlas garantiza la salud de todo el ecosistema.",
            "variants": [
                "Los VOC de fauna en Los Nevados son especies focales como el periquito de los nevados y el pato andino, sumados a grandes mamíferos sombrilla como el oso andino y la danta de montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.ruiz_parakeet", "fauna.andean_duck", "fauna.spectacled_bear"],
        "tags": ["voc", "valores_objeto_conservacion", "prioritarias", "plan_manejo", "focales"]
    },
    # 10. Andean Condor
    {
        "id": "fauna.andean_condor",
        "label": "cóndor andino en Los Nevados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "el cóndor andino",
            "¿dónde puedo ver cóndores?",
            "hay condores en el parque los nevados",
            "ave nacional de Colombia en el nevado",
            "tamaño y envergadura del cóndor andino",
            "¿cómo identificar un cóndor volando?",
            "avistamiento de condores en el ruiz",
            "condor de los andes en alta montana",
            "where can I see the Andean condor?",
            "Andean condor in Los Nevados National Park",
            "condor andino volando sobre las montanas",
            "pajaro grande planeando en el cielo"
        ],
        "hard_negatives": [
            "miradores para ver el cráter del volcán Ruiz",
            "tarifa de entrada para fotógrafos de aves",
            "leyendas indígenas sobre el nevado del Ruiz"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El cóndor andino (Vultur gryphus), ave nacional de Colombia, planea con majestuosidad sobre los cañones y riscos del parque aprovechando las corrientes térmicas. Con una envergadura alar de más de 3 metros, es una de las aves voladoras más grandes del planeta. Puedes distinguirlo por su vuelo sereno casi sin aletear, su collar de plumón blanco y las manchas blancas en el dorso de sus alas.",
            "variants": [
                "El cóndor andino sobrevuela los riscos y páramos de Los Nevados con sus más de 3 metros de envergadura. Planea aprovechando los vientos de montaña en sectores abiertos como Valle de las Tumbas o cercanías de lagunas."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.condor_reintroduction_program", "fauna.carunculated_caracara", "fauna.birds_overview"],
        "tags": ["condor", "vultur_gryphus", "ave_nacional", "rapaz", "envergadura"]
    },
    # 11. Condor reintroduction program
    {
        "id": "fauna.condor_reintroduction_program",
        "label": "programa de reintroducción del cóndor andino",
        "kind": "fact",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "reintroducción de cóndores en Los Nevados",
            "¿de dónde salieron los cóndores del parque?",
            "proyecto de liberación de cóndores",
            "historia del cóndor en el parque los nevados",
            "¿cuántos cóndores hay en el parque?",
            "repoblamiento del cóndor andino en Colombia",
            "liberacion de condores en los anos noventa",
            "censo de condores en los nevados",
            "Andean condor reintroduction program Colombia",
            "how many condors live in Los Nevados?",
            "los condores fueron traidos o son nativos",
            "programa de conservacion del condor"
        ],
        "hard_negatives": [
            "horarios del centro de visitantes Brisas",
            "historia de la erupción de Armero en 1985",
            "reglamento de sobrevuelo de drones"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "A comienzos de la década de 1990, Parques Nacionales Naturales y el Zoológico de San Diego lideraron un histórico programa de reintroducción liberando ejemplares nacidos en cautiverio en Los Nevados. Gracias a este esfuerzo y a los censos nacionales de cóndor, hoy se confirma una población silvestre reproductiva con varias parejas territoriales activas. Es uno de los mayores éxitos de conservación de fauna en la Cordillera Central.",
            "variants": [
                "Los cóndores que ves hoy en Los Nevados provienen en parte del exitoso programa de reintroducción iniciado en los 90, que logró establecer parejas reproductivas que hoy anidan en los acantilados del parque."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.threatened_species", "fauna.birds_overview"],
        "tags": ["condor", "reintroduccion", "historia", "conservacion", "censo"]
    },
    # 12. Buffy Helmetcrest (Chivito de páramo)
    {
        "id": "fauna.buffy_helmetcrest",
        "label": "chivito de páramo o colibrí barbudo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "chivito de páramo",
            "colibrí barbudo del Ruiz",
            "Oxypogon stuebelii",
            "colibrí que vive en los frailejones",
            "¿qué es el chivito de páramo?",
            "colibri con barba en los nevados",
            "donde ver el chivito de paramo",
            "colibri endemico del parque los nevados",
            "Buffy helmetcrest hummingbird Los Nevados",
            "endemic hummingbird of the Colombian paramo",
            "pajarito chiquito en las flores del frailejon",
            "colibri del volcan nevado del ruiz"
        ],
        "hard_negatives": [
            "tipos de frailejones en el parque",
            "senderos habilitados en sector Brisas",
            "fotografía de alta montaña y lentes recomendados"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El chivito de páramo (Oxypogon stuebelii) es un colibrí fascinante y endémico estricto del Macizo del Ruiz y la Cordillera Central, adaptado a vivir por encima de los 3.500 metros. Los machos exhiben una cresta aguda y una llamativa barba de plumas blancas y rufas con las que cortejan. Su vida está íntimamente ligada a los frailejones: liba el néctar de sus flores y usa la suave pelusa de sus hojas para forrar el nido.",
            "variants": [
                "Este pequeño colibrí endémico, Oxypogon stuebelii, vive entre los 3.500 y 4.500 metros en Los Nevados, alimentándose de flores de frailejón y soportando temperaturas bajo cero gracias al torpor nocturno."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.endemic_species", "fauna.tyrian_metaltail"],
        "tags": ["chivito", "oxypogon_stuebelii", "colibri", "frailejon", "endemico"]
    },
    # 13. Fuertes's Parrot (Cotorra de Fuertes)
    {
        "id": "fauna.fuertes_parrot",
        "label": "cotorra de Fuertes o coroniazul",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cotorra de Fuertes",
            "Hapalopsittaca fuertesi",
            "cotorra coroniazul en Los Nevados",
            "loro en peligro de extinción en el nevado",
            "¿dónde habita la cotorra de Fuertes?",
            "cotorrita amenazada de la cordillera central",
            "loro endemico de bosques altoandinos",
            "redescubrimiento de la cotorra de fuertes",
            "Fuertes's parrot Los Nevados Colombia",
            "indigo-winged parrot endangered",
            "lorito pequeno con corona azul",
            "pajaro escaso en la selva altoandina"
        ],
        "hard_negatives": [
            "municipios de Caldas y Quindío vecinos al parque",
            "alojamiento en cabañas cercanas a Otún",
            "normativa de recolección botánica en PNN"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "La cotorra de Fuertes o aliazul (Hapalopsittaca fuertesi) es una de las aves más raras del planeta, catalogada en Peligro Crítico de extinción y endémica de una estrecha franja de bosque altoandino en la cuenca de Los Nevados. Se alimenta de frutos y muérdagos en árboles maduros y anida en cavidades naturales de robles y palmas. Su redescubrimiento a principios de siglo impulsó reservas y cajas nido para asegurar su supervivencia.",
            "variants": [
                "Hapalopsittaca fuertesi es un loro endémico y sumamente escaso que habita en los bosques de niebla de la vertiente occidental del parque, objeto de intensas iniciativas de conservación biológica."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.ruiz_parakeet", "fauna.yellow_eared_parrot", "fauna.threatened_species"],
        "tags": ["cotorra_fuertes", "hapalopsittaca", "peligro_critico", "endemica", "loros"]
    },
    # 14. Ruiz Parakeet (Periquito de los Nevados)
    {
        "id": "fauna.ruiz_parakeet",
        "label": "periquito de los nevados en páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "periquito de los nevados",
            "Bolborhynchus ferrugineifrons",
            "perico de páramo",
            "lorito que vive en el frío de la alta montaña",
            "¿dónde ver el periquito de los nevados?",
            "periquito endemico del parque los nevados",
            "cotorrita de alta montana en pajonales",
            "ave objeto de conservacion del parque",
            "Rufous-fronted parakeet Los Nevados",
            "high altitude parakeet Colombia paramo",
            "periquitos volando en bandadas en el paramo",
            "perico con frente color oxido"
        ],
        "hard_negatives": [
            "permisos para acampar en Laguna del Otún",
            "diferencia entre páramo y superpáramo",
            "vestimenta técnica para soportar el viento"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El periquito de los nevados (Bolborhynchus ferrugineifrons) es un Valor Objeto de Conservación prioritario del parque y un endemismo estricto de los páramos de la Cordillera Central. A diferencia de casi todos los loros que viven en selvas cálidas, este pequeño perico verde con frente herrumbrosa vuela veloz en pequeñas bandadas ruidosas entre los 3.200 y 4.000 metros, alimentándose de semillas de gramíneas y arbustos.",
            "variants": [
                "Bolborhynchus ferrugineifrons es un periquito verde de alta montaña que solo existe en esta región andina. Vuela en bandadas rasantes sobre los pajonales y anida en paredes rocosas y cuevas del páramo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.conservation_target_species_voc", "fauna.fuertes_parrot", "fauna.buffy_helmetcrest"],
        "tags": ["periquito_nevados", "bolborhynchus", "voc", "endemico", "paramo"]
    },
    # 15. Yellow-eared Parrot (Loro orejiamarillo)
    {
        "id": "fauna.yellow_eared_parrot",
        "label": "loro orejiamarillo y palma de cera",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "loro orejiamarillo",
            "Ognorhynchus icterotis",
            "loro que vive en las palmas de cera",
            "loro amarillo en bosque altoandino",
            "¿dónde se ve el loro orejiamarillo?",
            "relacion del loro con la palma de cera",
            "ave amenazada en la zona amortiguadora",
            "proyecto de conservacion del loro orejiamarillo",
            "Yellow-eared parrot wax palm Colombia",
            "where to see Ognorhynchus icterotis",
            "loros grandes con manchas amarillas en la cara",
            "loro de montaña en el Quindío y Tolima"
        ],
        "hard_negatives": [
            "bosques de palma de cera en el Valle de Cocora",
            "senderos de trekking hacia la cumbre del Tolima",
            "árbol nacional de Colombia y su protección"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El loro orejiamarillo (Ognorhynchus icterotis) es un ave emblemática de los Andes colombianos cuya supervivencia depende estrechamente de la palma de cera (Ceroxylon quindiuense). Utiliza las palmas maduras y secas para dormir y construir sus nidos, además de alimentarse de sus frutos. Aunque estuvo al borde de la extinción, programas conjuntos de protección de su hábitat en las cuencas del Quindío y Tolima han permitido recuperar sus poblaciones.",
            "variants": [
                "Este vistoso loro de montaña depende de los palmares de cera en la franja de bosque de niebla del parque. Su conservación ha sido un hito ambiental gracias a la protección estricta de las palmas donde anida."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.fuertes_parrot", "fauna.golden_plumed_parakeet", "fauna.threatened_species"],
        "tags": ["loro_orejiamarillo", "ognorhynchus", "palma_de_cera", "amenazada", "bosque_altoandino"]
    },
    # 16. Golden-plumed Parakeet (Perico paramuno)
    {
        "id": "fauna.golden_plumed_parakeet",
        "label": "perico paramuno en bosque altoandino",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "perico paramuno",
            "Leptosittaca branickii",
            "cotorra de penacho dorado",
            "loros de bosque de niebla en Los Nevados",
            "¿dónde habita el perico paramuno?",
            "perico con plumas amarillas en las mejillas",
            "bandadas de pericos en el bosque altoandino",
            "ave que come frutos de pino romerón",
            "Golden-plumed parakeet Los Nevados",
            "Leptosittaca branickii cloud forest",
            "periquito de montaña con cresta dorada",
            "avistamiento de cotorras paramunas"
        ],
        "hard_negatives": [
            "especies forestales nativas como el pino romerón",
            "itinerario de caminata por el cañón del Combeima",
            "recomendaciones para evitar el mal de montaña"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El perico paramuno (Leptosittaca branickii) es un loro nómada de alta montaña que recorre en ruidosas bandadas los bosques nublados y el subpáramo entre 2.800 y 3.600 metros. Se reconoce por su cuerpo verde, pecho amarillento y mechones de plumas doradas alargadas detrás de los ojos. Cumple un rol vital dispersando semillas de coníferas nativas como el pino romerón (Retrophyllum rospigliosii).",
            "variants": [
                "Leptosittaca branickii es una cotorra gregaria y llamativa que habita los bosques altos del parque, desplazándose según la fructificación de árboles nativos como coníferas y palmas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.yellow_eared_parrot", "fauna.fuertes_parrot", "fauna.birds_overview"],
        "tags": ["perico_paramuno", "leptosittaca", "bosque_niebla", "vulnerable", "loros"]
    },
    # 17. Brown-banded Antpitta (Tororoi de Miller)
    {
        "id": "fauna.brown_banded_antpitta",
        "label": "tororoi de Miller en el sotobosque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tororoi de Miller",
            "Grallaria milleri",
            "Brown-banded antpitta Los Nevados",
            "pájaro patudo de sotobosque",
            "¿dónde vive el tororoi de Miller?",
            "ave endémica difícil de ver en el bosque",
            "tororoi con banda café en el pecho",
            "pajaro caminador del suelo en el bosque de niebla",
            "where to find brown banded antpitta",
            "endemic antpitta Central Andes Colombia",
            "pajaro que salta en la hojarasca",
            "tororoi endemico de caldas y risaralda"
        ],
        "hard_negatives": [
            "fotografía macro de musgos y líquenes",
            "reserva ecológica de Río Blanco en Manizales",
            "calzado impermeable para barro en senderos"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El tororoi de Miller (Grallaria milleri) es un ave terrestre endémica de la Cordillera Central y uno de los mayores tesoros ornitológicos del parque. Tiene cuerpo redondeado, cola casi invisible y patas largas adaptadas para correr y brincar sobre la hojarasca del sotobosque denso. Debido a sus hábitos tímidos y crípticos, es mucho más fácil escuchar su silbido melodioso que lograr observarlo a simple vista.",
            "variants": [
                "Grallaria milleri habita en la espesura del bosque altoandino entre cañas de chusque y hojarasca húmeda. Es una especie endémica muy buscada por observadores de aves de todo el mundo."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.tawny_antpitta", "fauna.chestnut_naped_antpitta", "fauna.endemic_species"],
        "tags": ["tororoi_miller", "grallaria_milleri", "endemica", "sotobosque", "antpitta"]
    },
    # 18. Tawny Antpitta (Tororoi leonado)
    {
        "id": "fauna.tawny_antpitta",
        "label": "tororoi leonado en páramo abierto",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tororoi leonado",
            "Grallaria quitensis",
            "Tawny antpitta paramo",
            "pájaro patón del páramo",
            "¿qué pájaro brinca en el suelo del páramo?",
            "ave redonda con patas largas en los pajonales",
            "tororoi que se acerca a los senderistas",
            "pajaro confiado en el nevado del ruiz",
            "tawny antpitta Los Nevados Colombia",
            "ground bird hopping in the paramo",
            "pajaro bolita de plumas en el camino",
            "tororoi de montana en pajonal"
        ],
        "hard_negatives": [
            "cómo combatir el dolor de cabeza por altura",
            "guías autorizados para caminatas en Brisas",
            "estado volcánico del Nevado del Ruiz"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El tororoi leonado (Grallaria quitensis) es el tororoi más común y sociable que encontrarás en Los Nevados. A diferencia de sus parientes tímidos del bosque, este pájaro regordete de color café leonado camina sin temor entre los pajonales y senderos abiertos del páramo buscando escarabajos y lombrices. Su silbido aflautado de tres notas resuena con frecuencia en medio de la niebla matutina.",
            "variants": [
                "Grallaria quitensis es esa ave simpática y rechoncha de patas largas que verás dar saltitos a los lados del camino en el páramo. Suele ser muy curiosa y tolerante con la presencia de caminantes silenciosos."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.brown_banded_antpitta", "fauna.buffy_helmetcrest", "fauna.birds_overview"],
        "tags": ["tororoi_leonado", "grallaria_quitensis", "paramo", "antpitta", "pajonal"]
    },
    # 19. Chestnut-naped Antpitta (Tororoi nuchicastaño)
    {
        "id": "fauna.chestnut_naped_antpitta",
        "label": "tororoi nuchicastaño en bosques de niebla",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tororoi nuchicastaño",
            "Grallaria nuchalis",
            "Chestnut-naped antpitta",
            "tororoi grande de bosque altoandino",
            "¿dónde se encuentra el tororoi nuchicastaño?",
            "ave de sotobosque con nuca castaña",
            "pajaro terrestre grande en bosque nublado",
            "grallaria nuchalis en los nevados",
            "chestnut naped antpitta Colombia",
            "large antpitta in cloud forest trails",
            "tororoi gigante de la cordillera central",
            "pajarote de patas largas en la niebla"
        ],
        "hard_negatives": [
            "refugio y campamento de alta montaña Arenales",
            "pago de póliza de seguro de rescate",
            "historia de las comunidades indígenas Quimbaya"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El tororoi nuchicastaño (Grallaria nuchalis) es una de las especies más robustas de su familia, habitando los densos bosques de niebla y matorrales de bambú entre 2.700 y 3.500 metros. Su plumaje gris pizarra contrasta con una intensa corona y nuca rojiza, y sus fuertes patas le permiten remover musgo y hojarasca profunda en busca de alimento. Es un ave fascinante que suele escucharse en quebradas húmedas.",
            "variants": [
                "Grallaria nuchalis destaca por su porte grande y su nuca color castaño rojizo; habita en los bosques más tupidos de la vertiente andina y emite un canto potente y resonante."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.brown_banded_antpitta", "fauna.tawny_antpitta", "fauna.birds_overview"],
        "tags": ["tororoi_nuchicastano", "grallaria_nuchalis", "bosque_niebla", "antpitta", "aves"]
    },
    # 20. Andean Duck (Pato andino o turrio)
    {
        "id": "fauna.andean_duck",
        "label": "pato andino o pato turrio",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "pato andino",
            "pato turrio",
            "Oxyura jamaicensis andina",
            "patos en la Laguna del Otún",
            "¿qué patos viven en las lagunas de Los Nevados?",
            "pato zambullidor de alta montaña",
            "pato con pico azul en el páramo",
            "patos silvestres en humedales altoandinos",
            "Andean duck Los Nevados Colombia",
            "ruddy duck high mountain lake Otun",
            "pato de pico celeste en los nevados",
            "aves acuaticas en las lagunas del parque"
        ],
        "hard_negatives": [
            "origen volcánico y geología de la Laguna del Otún",
            "pesca deportiva de trucha y su prohibición",
            "profundidad y área de la Laguna del Otún"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El pato andino o pato turrio (Oxyura jamaicensis andina / Oxyura andina) es un Valor Objeto de Conservación del parque, adaptado a nadar y bucear en lagunas frías como la del Otún. Los machos reproductivos lucen un plumaje castaño rojizo y un característico pico azul celeste brillante con la cola rígida levantada en abanico. Se alimentan buceando hasta el fondo para capturar pequeños invertebrados y plantas acuáticas.",
            "variants": [
                "Este pato zambullidor es el habitante más representativo de los humedales del parque. Lo reconocerás fácilmente por su llamativo pico azul celeste y su cola erguida sobre el agua."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.conservation_target_species_voc", "fauna.torrent_duck", "fauna.andean_coot"],
        "tags": ["pato_andino", "pato_turrio", "oxyura", "voc", "lagunas", "otun"]
    },
    # 21. Torrent Duck (Pato de torrente)
    {
        "id": "fauna.torrent_duck",
        "label": "pato de torrente en ríos de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "pato de torrente",
            "Merganetta armata",
            "pato que nada en ríos rápidos",
            "pato de cascadas en Los Nevados",
            "¿cómo nada el pato contra la corriente?",
            "pato con cuerpo estilizado en aguas bravas",
            "pato nadando en rapidos de montana",
            "aves acuaticas en rios de alta montana",
            "Torrent duck Merganetta armata Los Nevados",
            "duck swimming in whitewater rapids Colombia",
            "pato parado sobre piedras en el rio",
            "pato buceando en corrientes frias"
        ],
        "hard_negatives": [
            "nacimiento de ríos y cuencas en Los Nevados",
            "deportes de aventura y rafting permitidos",
            "precauciones por crecientes súbitas en quebradas"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El pato de torrente (Merganetta armata) posee adaptaciones corporales prodigiosas: cuerpo hidrodinámico, cola rígida que actúa como timón y espolones en las alas para aferrarse a rocas mojadas en torrentes violentos. Es capaz de bucear y nadar río arriba contra corrientes turbulentas alimentándose de larvas de insectos acuáticos. Puedes verlo descansando sobre grandes piedras en los ríos Otún, Combeima o Chinchiná.",
            "variants": [
                "Merganetta armata desafía las aguas bravas de montaña con asombrosa facilidad; nada contracorriente en ríos glaciares y es un excelente indicador de la pureza y oxigenación del agua."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.white_capped_dipper", "fauna.aquatic_macroinvertebrates"],
        "tags": ["pato_torrente", "merganetta_armata", "rios", "cascadas", "aguas_bravas"]
    },
    # 22. Black-and-chestnut Eagle (Águila crestada)
    {
        "id": "fauna.black_and_chestnut_eagle",
        "label": "águila crestada en la selva altoandina",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "águila crestada",
            "Spizaetus isidori",
            "Oroaetus isidori",
            "águila de copete en Los Nevados",
            "gran águila de bosque altoandino",
            "rapaz en peligro en la cordillera central",
            "¿qué come el águila crestada?",
            "aguila con cresta negra y pecho castano",
            "Black-and-chestnut eagle Colombia",
            "Spizaetus isidori endangered raptor",
            "aguila cazadora de ardillas y pavas",
            "avistamiento de grandes aguilas en el bosque"
        ],
        "hard_negatives": [
            "senderismo en el bosque de La Pastora",
            "uso de bastones de trekking en senderos con pendiente",
            "horario de transporte público hacia Pereira"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El águila crestada (Spizaetus isidori) es una de las rapaces más majestuosas y amenazadas de los Andes, ubicada en la cima de la cadena trófica de los bosques de niebla. Posee una cresta prominente, pecho color castaño brillante y garras descomunales con las que caza mamíferos medianos como ardillas, guaguas y pavas de monte. Su presencia certifica la excelente salud y continuidad de los bosques maduros del parque.",
            "variants": [
                "Spizaetus isidori es el superdepredador alado de las selvas altoandinas del parque; su supervivencia depende de grandes extensiones boscosas continuas y está protegida por estrictos planes de conservación."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.black_chested_buzzard_eagle", "fauna.threatened_species", "fauna.andean_condor"],
        "tags": ["aguila_crestada", "spizaetus_isidori", "rapaz", "bosque_altoandino", "amenazada"]
    },
    # 23. Black-chested Buzzard-Eagle (Águila mora)
    {
        "id": "fauna.black_chested_buzzard_eagle",
        "label": "águila mora o gavilán cuellinegro",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "águila mora",
            "Geranoaetus melanoleucus",
            "gavilán cuellinegro",
            "águila de páramo planeando",
            "¿qué águila vuela sobre el páramo?",
            "rapaz grande sobrevolando pajonales",
            "aguila con pecho negro y alas grises",
            "cazadora de conejos y ratones en el nevado",
            "Black-chested buzzard-eagle paramo",
            "large eagle soaring over Los Nevados",
            "aguila paramuna planeando en círculos",
            "rapaz comun en el sector brisas"
        ],
        "hard_negatives": [
            "viento y sensacion termica en el Valle de las Tumbas",
            "protector solar y gafas con filtro UV para montana",
            "restricciones para volar drones de grabacion"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El águila mora o gavilán cuellinegro (Geranoaetus melanoleucus) es la rapaz diurna más representativa que verás sobrevolando el páramo abierto y los valles del parque. Con alas anchas y cola corta cuneiforme, planea en círculos sostenidos patrullando los pajonales en busca de conejos de páramo y roedores. Se distingue por su pecho negro azabache en contraste con el vientre y las alas de color gris plateado.",
            "variants": [
                "Geranoaetus melanoleucus domina el cielo abierto del páramo; aprovecha las corrientes de aire para cazar conejos y pequeños vertebrados entre los pajonales y morrenas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.carunculated_caracara", "fauna.black_and_chestnut_eagle"],
        "tags": ["aguila_mora", "geranoaetus", "rapaz", "paramo", "cazadora"]
    },
    # 24. Carunculated Caracara (Caracara curiquinge)
    {
        "id": "fauna.carunculated_caracara",
        "label": "caracara curiquinge en los pajonales",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "caracara curiquinge",
            "Phalcoboenus carunculatus",
            "curiquinga en el páramo",
            "pájaro carroñero con cara naranja",
            "¿qué ave camina por el suelo en Brisas?",
            "halcón del páramo buscando comida en el piso",
            "ave negra con pecho blanco y cara roja",
            "curiquingue en el parque los nevados",
            "Carunculated caracara Colombia",
            "Phalcoboenus carunculatus high paramo",
            "pajaro carroñero caminando entre frailejones",
            "caracara de montana en senderos"
        ],
        "hard_negatives": [
            "prohibición estricta de dejar basura o desperdicios",
            "normas sobre fogatas y campamentos no autorizados",
            "historia de nombres indígenas de los volcanes"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El curiquinge o caracara carunculado (Phalcoboenus carunculatus) es un falcónido muy curioso y caminador de la alta montaña andina. Tiene plumaje negro con pecho moteado de blanco y una cara descubierta de piel arrugada de color naranja rojizo muy llamativa. Camina con agilidad por el suelo del páramo buscando escarabajos, lombrices y carroña, y con frecuencia se posa cerca de caminos y áreas rocosas.",
            "variants": [
                "Phalcoboenus carunculatus es fácil de avistar en sectores abiertos como Brisas; camina entre los frailejones rebuscando alimento y vigilando su territorio desde promontorios de roca."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.black_chested_buzzard_eagle", "fauna.birds_overview"],
        "tags": ["curiquinge", "caracara", "phalcoboenus", "carronero", "paramo"]
    },
    # 25. Sword-billed Hummingbird (Colibrí piquiespada)
    {
        "id": "fauna.sword_billed_hummingbird",
        "label": "colibrí piquiespada y flores tubulares",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "colibrí piquiespada",
            "Ensifera ensifera",
            "colibrí con pico más largo que el cuerpo",
            "pájaro con pico larguísimo en Los Nevados",
            "¿cuánto mide el pico del colibrí piquiespada?",
            "colibri adaptado a flores de curuba silvestre",
            "picaflor de pico espada en bosque altoandino",
            "donde ver el colibri piquiespada",
            "Sword-billed hummingbird Colombia",
            "Ensifera ensifera high altitude hummingbird",
            "colibri que vuela con pico hacia arriba",
            "ave polinizadora de pasifloras de montaña"
        ],
        "hard_negatives": [
            "bebederos artificiales de néctar y su regulación",
            "senderos botánicos de plantas medicinales",
            "tiempo estimado de caminata en subida"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El colibrí piquiespada (Ensifera ensifera) ostenta un récord biológico único: es la única ave del mundo cuyo pico es más largo que el resto de su cuerpo. Esta impresionante adaptación le permite acceder al néctar profundo de flores tubulares colgantes como las pasifloras y curubas silvestres (Passiflora mixta), inaccesibles para otros polinizadores. Cuando descansa, mantiene el pico apuntando hacia arriba para equilibrar su peso.",
            "variants": [
                "Ensifera ensifera habita en los bosques altoandinos y matorrales entre 2.500 y 3.500 metros; su larguísimo pico coevolucionó exclusivamente con las flores tubulares de montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.buffy_helmetcrest", "fauna.shining_sunbeam", "fauna.birds_overview"],
        "tags": ["piquiespada", "ensifera_ensifera", "colibri", "adaptacion", "polinizador"]
    },
    # 26. Shining Sunbeam (Rayito de sol andino)
    {
        "id": "fauna.shining_sunbeam",
        "label": "rayito de sol andino en subpáramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "rayito de sol andino",
            "Aglaeactis cupripennis",
            "colibrí con lomo dorado brillante",
            "colibrí que brilla con el sol en el páramo",
            "¿dónde habita el rayito de sol?",
            "picaflor de espalda iridiscente en Los Nevados",
            "colibri territorial en matorrales de montaña",
            "ave que parece encenderse con la luz solar",
            "Shining sunbeam hummingbird Colombia",
            "Aglaeactis cupripennis high Andes",
            "colibri marron que destella colores dorados",
            "pajaro que defiende arbustos con flores"
        ],
        "hard_negatives": [
            "radiación ultravioleta y protección solar en altura",
            "fotografía de paisajes y reflejos en la nieve",
            "temperatura en el sector Brisas al mediodía"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El rayito de sol andino (Aglaeactis cupripennis) es un colibrí común y vivaz de la franja de subpáramo y bordes de bosque altoandino entre 3.000 y 4.000 metros. A la sombra luce como un ave parda discreta, pero al girar frente a la luz del sol, su espalda y rabadilla destellan un fulgor cobrizo y violeta incandescente. Es muy territorial y defiende con energía sus matas de arbustos florecidos frente a otros colibríes.",
            "variants": [
                "Aglaeactis cupripennis sorprende por el destello metálico multicolor de su dorso bajo la luz solar andina; habita en matorrales paramunos y es muy activo durante las mañanas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.buffy_helmetcrest", "fauna.tyrian_metaltail", "fauna.birds_overview"],
        "tags": ["rayito_de_sol", "aglaeactis", "colibri", "iridiscencia", "subparamo"]
    },
    # 27. Tyrian Metaltail (Colibrí coliazul y colibrí cobrizo)
    {
        "id": "fauna.tyrian_metaltail",
        "label": "colibrí Metallura tyrianthina",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "colibrí coliazul",
            "colibrí cobrizo",
            "Metallura tyrianthina",
            "Metallura williamsoni",
            "colibrí de cola metálica en Los Nevados",
            "colibries diminutos del páramo",
            "pajarito verde oliva con cola brillante",
            "colibrí de gran altura en arbustales",
            "Tyrian metaltail Los Nevados",
            "coppery metaltail hummingbird Colombia",
            "pequeno colibri posado en ramas bajas",
            "colibries enanos del bosque y pajonal"
        ],
        "hard_negatives": [
            "arbustos y vegetación leñosa del subpáramo",
            "puntos de recarga de agua potable en el parque",
            "servicios higiénicos y baños para visitantes"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "Los colibríes del género Metallura, como el colibrí coliazul (Metallura tyrianthina) y el colibrí cobrizo (Metallura williamsoni), son pequeñas gemas aladas adaptadas a altitudes de hasta 4.000 metros. Tienen picos cortos y colas de reflejos metálicos verdeazules o cobrizos con los que maniobran entre arbustos bajos de Ericáceas y Asteráceas. Para conservar calor corporal durante las heladas noches paramunas, entran en un estado de letargo profundo.",
            "variants": [
                "Estas diminutas especies de colibrí aprovechan flores pequeñas en matorrales altos; soportan las bajas temperaturas nocturnas reduciendo drásticamente su ritmo cardíaco y metabolismo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.buffy_helmetcrest", "fauna.shining_sunbeam", "fauna.birds_overview"],
        "tags": ["colibri_coliazul", "metallura", "letargo", "adaptacion", "paramo"]
    },
    # 28. White-capped Dipper (Mirlo acuático)
    {
        "id": "fauna.white_capped_dipper",
        "label": "mirlo acuático en cascadas y arroyos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "mirlo acuático",
            "Cinclus leucocephalus",
            "pájaro que bucea en ríos fríos",
            "ave con gorra blanca en las cascadas",
            "¿qué pájaro se sumerge en torrentes de montaña?",
            "mirlo que camina bajo el agua en arroyos",
            "pajaro ribereño de aguas cristalinas",
            "White-capped dipper Colombia",
            "Cinclus leucocephalus mountain stream",
            "pajaro que mueve la cola sobre piedras mojadas",
            "ave acuatica en quebradas de los nevados",
            "mirlo buceador en torrentes andinos"
        ],
        "hard_negatives": [
            "precauciones por congelamiento de agua en cantimploras",
            "deshielo de glaciares y caudal de los ríos",
            "puentes y pasos seguros sobre quebradas"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El mirlo acuático (Cinclus leucocephalus) es un ave cantora asombrosa capaz de zambullirse y caminar literalmente bajo el agua por el fondo rocoso de arroyos helados. Posee una densa capa de plumón impermeable, párpados con membrana nictitante transparente y sangre rica en hemoglobina para bucear en aguas gélidas en busca de larvas acuáticas. Lo reconocerás posado en rocas húmedas sacudiendo rítmicamente el cuerpo.",
            "variants": [
                "Cinclus leucocephalus habita en quebradas de montaña con aguas rápidas y muy limpias; bucea contracorriente para atrapar ninfas de insectos acuáticos y anida detrás de cascadas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.torrent_duck", "fauna.aquatic_macroinvertebrates", "fauna.birds_overview"],
        "tags": ["mirlo_acuatico", "cinclus", "rios", "buceo", "arroyos_glaciares"]
    },
    # 29. Great Thrush (Mirlo negro andino)
    {
        "id": "fauna.great_thrush",
        "label": "mirlo negro andino en senderos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "mirlo negro andino",
            "Turdus fuscater",
            "pájaro negro grande con pico naranja",
            "mirlo de montaña en Los Nevados",
            "ave negra común en los caminos del parque",
            "¿cómo se llama el pájaro negro de ojos y pico amarillos?",
            "mirla andina en el páramo",
            "pajaro negro cantando en la manana",
            "Great thrush Turdus fuscater Los Nevados",
            "large black bird orange bill Colombia",
            "mirlo patinaranja en los campamentos",
            "ave negra que salta por el pasto"
        ],
        "hard_negatives": [
            "regla de no alimentar a los animales con sobras",
            "aves migratorias de Norteamérica en Colombia",
            "zonas habilitadas para consumir alimentos"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El mirlo negro andino (Turdus fuscater) es el ave más visible y familiar que acompaña a los caminantes a lo largo de senderos y campamentos hasta los 4.200 metros. Tiene plumaje negro pizarra lustroso, patas y pico de un encendido color naranja y un característico anillo ocular a tono. Se alimenta de bayas silvestres y lombrices, y su canto variado y potente alegra las mañanas despejadas en la montaña.",
            "variants": [
                "Turdus fuscater es muy abundante y curioso en casi todos los sectores del parque; salta confiado por el pasto y ramas bajas buscando frutos de alta montaña e invertebrados."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.rufous_collared_sparrow", "fauna.tawny_antpitta", "fauna.birds_overview"],
        "tags": ["mirlo_negro", "turdus_fuscater", "mirla", "senderos", "comun"]
    },
    # 30. Hooded Mountain-Toucan (Terlaque andino)
    {
        "id": "fauna.hooded_mountain_toucan",
        "label": "terlaque andino o tucán de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "terlaque andino",
            "tucán de montaña",
            "Andigena hypoglauca",
            "¿hay tucanes en el frío de Los Nevados?",
            "pájaro con pico multicolor en bosque nublado",
            "tucancito de la alta montaña",
            "terlaque con pecho azul grisáceo",
            "donde ver tucanes de montana",
            "Hooded mountain-toucan Los Nevados",
            "Andigena hypoglauca cloud forest toucan",
            "tucan de clima frio en la cordillera central",
            "ave frugivora con pico pintado en la selva"
        ],
        "hard_negatives": [
            "tucanes de tierras bajas del Amazonas",
            "frutas permitidas para llevar en la mochila",
            "flora del bosque altoandino y árboles de niebla"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El terlaque andino (Andigena hypoglauca) demuestra que los tucanes no son exclusivos de selvas cálidas: esta espectacular ave de pico multicolor habita los bosques templados y nublados entre 2.500 y 3.400 metros. Posee un plumaje espeso con capucha negra, pecho azul cenizo, rabadilla amarilla y plumas bajo la cola de color rojo encendido. Vuela en parejas alimentándose de frutos silvestres y contribuyendo a la dispersión del bosque.",
            "variants": [
                "Andigena hypoglauca es un tucán adaptado a la niebla y las bajas temperaturas; su llamativo pico rayado de negro, rojo y amarillo decora el dosel de los bosques de niebla del parque."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.mountain_tanagers", "fauna.spotting_sector_la_pastora"],
        "tags": ["terlaque", "tucan_montana", "andigena", "bosque_niebla", "frugivoro"]
    }
]
