"""Part 3 of fauna entries: Herpetofauna 61-62, Invertebrates 63-68, Locations 69-77, Safety 78-83, Rules/Ethics 84-90."""
from sources import (
    SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA,
    SOURCE_HUMBOLDT, SOURCE_EBIRD, SOURCE_CARDER, SOURCE_CORPOCALDAS, SOURCE_CORTOLIMA
)

ENTRIES_PART3 = [
    # 61. Earth Snakes (Atractus)
    {
        "id": "fauna.earth_snakes_atractus",
        "label": "serpientes tierreras inofensivas de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "serpientes tierreras",
            "Atractus manizalesensis",
            "Atractus titanicus",
            "culebras en el suelo del parque",
            "¿son peligrosas las serpientes de Los Nevados?",
            "serpiente pequeña no venenosa en la hojarasca",
            "culebrita de tierra en la montaña",
            "serpientes del genero atractus en caldas",
            "Earth snakes Atractus Colombian high Andes",
            "harmless fossorial snakes Los Nevados",
            "culebra oscura cavando en la tierra humeda",
            "serpiente tierrera inofensiva de montana"
        ],
        "hard_negatives": [
            "suero antiofídico y primeros auxilios médicos",
            "tipos de suelo y cenizas volcánicas en el páramo",
            "botiquín básico de primeros auxilios para montaña"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "Las serpientes tierreras del género Atractus (como Atractus manizalesensis y Atractus titanicus) son reptiles de pequeño porte totalmente inofensivos para el ser humano. No poseen veneno ni colmillos inoculadores; tienen cabeza estrecha y escamas lisas diseñadas para enterrarse en suelos húmedos, hojarasca y musgos donde cazan lombrices e invertebrados. Si ves una en el camino, déjala continuar su paso sin perturbarla.",
            "variants": [
                "Las culebrillas Atractus son fosoriales y pacíficas; cumplen un papel ecológico vital en el reciclaje de nutrientes del suelo y jamás representan un peligro para los excursionistas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_CORPOCALDAS, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.venomous_snakes_absence", "fauna.reptiles_overview", "fauna.mountain_collared_lizard"],
        "tags": ["serpiente_tierrera", "atractus", "inofensiva", "no_venenosa", "suelo"]
    },
    # 62. Absence of venomous snakes in high altitude
    {
        "id": "fauna.venomous_snakes_absence",
        "label": "ausencia de serpientes venenosas en altura",
        "kind": "fact",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿hay serpientes venenosas en Los Nevados?",
            "peligro de mordedura de serpiente en el páramo",
            "hay cascabeles o corales en la montaña",
            "¿las culebras del páramo tienen veneno?",
            "riesgo de víboras en el parque los nevados",
            "¿toca llevar polainas contra serpientes al nevado?",
            "accidentes ofidicos en alta montana",
            "serpientes peligrosas en el frio",
            "Are there venomous snakes in Los Nevados paramo?",
            "snake bite risk high altitude Colombia",
            "serpientes con veneno en el nevado del ruiz",
            "tranquilidad sobre viboras en el sendero"
        ],
        "hard_negatives": [
            "serpientes venenosas de tierras bajas como la talla equis",
            "polainas impermeables para barro y agua",
            "seguro médico y teléfonos de ambulancias"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "Puedes caminar con total tranquilidad: en las zonas de páramo y superpáramo por encima de los 3.000 metros de altitud no habitan víboras ni serpientes venenosas (como Bothrops, cascabeles o corales). Las bajas temperaturas nocturnas y el clima extremo impiden la supervivencia de serpientes con veneno peligroso para las personas. Los únicos ofidios registrados a estas alturas son pequeñas culebrillas tierreras completamente inofensivas.",
            "variants": [
                "En las cotas medias y altas de Los Nevados no existe riesgo de mordedura de serpientes venenosas; la fisiología de los vipéridos les impide colonizar el frío páramo andino."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.earth_snakes_atractus", "fauna.reptiles_overview", "fauna.safe_viewing_distance"],
        "tags": ["serpientes_venenosas", "seguridad", "sin_peligro", "paramo", "altitud"]
    },
    # 63. Paramo Bumblebees (Abejorros)
    {
        "id": "fauna.paramo_bumblebees",
        "label": "abejorros de páramo y polinización",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "abejorros de páramo",
            "Bombus funebris",
            "Bombus rubicundus",
            "abejorros que polinizan frailejones",
            "¿cómo vuelan los abejorros con tanto frío?",
            "abejas peludas de alta montaña",
            "polinización por zumbido en el páramo",
            "abejorro negro grande en las flores de montaña",
            "Paramo bumblebees Bombus Los Nevados",
            "pollinating bumblebees high Andes Colombia",
            "abejorro zumbando sobre flores amarillas",
            "insectos peludos que resisten heladas"
        ],
        "hard_negatives": [
            "apicultura y miel en zonas rurales de Caldas",
            "alergias a picaduras y antihistamínicos en botiquín",
            "especies botánicas de frailejones en floración"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "Los abejorros del género Bombus (como Bombus funebris y Bombus rubicundus) son los polinizadores estrella del páramo. Su cuerpo robusto está cubierto por una densa capa de 'pelo' aislante y pueden hacer vibrar sus poderosos músculos de vuelo para generar calor interno, lo que les permite volar con temperaturas cercanas a cero grados y fuertes vientos. Son vitales para fecundar las flores de frailejón mediante polinización por zumbido.",
            "variants": [
                "Los abejorros Bombus resisten el frío extremo gracias a su pelaje y termorregulación activa; sin ellos, la reproducción de frailejones y arbustos de páramo se vería gravemente afectada."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.insects_invertebrates_overview", "fauna.paramo_butterflies", "fauna.buffy_helmetcrest"],
        "tags": ["abejorros", "bombus", "polinizacion", "frailejones", "termorregulacion"]
    },
    # 64. Paramo Butterflies (Lymanopoda)
    {
        "id": "fauna.paramo_butterflies",
        "label": "mariposas oscuras de alta montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "mariposas de páramo",
            "Lymanopoda",
            "mariposas negras en la alta montaña",
            "¿cómo sobreviven las mariposas al frío del páramo?",
            "mariposa con alas oscuras en Los Nevados",
            "mariposas satíridas de los Andes",
            "melanismo térmico en mariposas de montaña",
            "mariposas volando cerca de los frailejones",
            "Paramo butterflies Lymanopoda Los Nevados",
            "dark butterflies high Andes Colombia",
            "mariposas que toman el sol en el suelo",
            "insectos alados del superpáramo"
        ],
        "hard_negatives": [
            "mariposarios turísticos en el Eje Cafetero",
            "colección de insectos y prohibición de captura",
            "temperatura en el sector Brisas al atardecer"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "Las mariposas de alta montaña, en especial las del género Lymanopoda, poseen una adaptación térmica sorprendente: sus alas están cargadas de pigmentos oscuros de melanina que funcionan como paneles solares en miniatura. Al posarse con las alas abiertas sobre rocas y suelo expuesto, absorben con avidez la radiación infrarroja del sol para calentar su hemolinfa y poder volar en el aire gélido del páramo. Sus orugas se nutren de chusques y pastos nativos.",
            "variants": [
                "Lymanopoda es el género de mariposas más característico de Los Nevados; sus alas de tonos café, negro o azul pizarra captan el calor solar necesario para mantenerse activas en la alta montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_bumblebees", "fauna.insects_invertebrates_overview", "fauna.soil_invertebrates_paramo"],
        "tags": ["mariposas", "lymanopoda", "melanismo", "absorcion_calor", "paramo"]
    },
    # 65. Rainbow Trout Impact (Trucha arcoíris invasora)
    {
        "id": "fauna.rainbow_trout_impact",
        "label": "trucha arcoíris invasora en lagunas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "trucha arcoíris en Los Nevados",
            "Oncorhynchus mykiss",
            "¿hay peces nativos en las lagunas?",
            "impacto de la trucha en la Laguna del Otún",
            "trucha como especie exótica invasora",
            "por qué la trucha afecta a los anfibios y patos",
            "pesca de trucha en el parque nacional",
            "depredación de larvas nativas por truchas",
            "Rainbow trout invasive species Los Nevados",
            "introduced fish impact Otun lake Colombia",
            "peces sembrados en lagunas del páramo",
            "problema ecologico de la trucha arcoiris"
        ],
        "hard_negatives": [
            "restaurantes de trucha en la cuenca del Otún o Cocora",
            "permisos y vedas de pesca deportiva en Risaralda",
            "calidad fisicoquímica del agua de la Laguna del Otún"
        ],
        "entities": {"animal_group": ["invertebrados"], "sector": ["otun"]},
        "needs": [],
        "answer": {
            "short": "La trucha arcoíris (Oncorhynchus mykiss) es una especie exótica originaria de Norteamérica que fue sembrada a mediados del siglo XX en lagunas como la del Otún. Al ser un pez carnívoro voraz, ha tenido un impacto ecológico severo: depreda masivamente las ninfas de insectos acuáticos autóctonos y renacuajos de anfibios, compitiendo además por alimento con aves acuáticas nativas como el pato andino. En el parque la siembra y la pesca no autorizada están terminantemente prohibidas.",
            "variants": [
                "La trucha arcoíris introducida alteró las cadenas tróficas de los humedales del parque; su presencia reduce drásticamente las poblaciones de insectos acuáticos y anfibios nativos de alta montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_CARDER, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.aquatic_macroinvertebrates", "fauna.harlequin_frog_atelopus"],
        "tags": ["trucha_arcoiris", "oncorhynchus_mykiss", "especie_invasora", "impacto_ecologico", "otun"]
    },
    # 66. Aquatic Macroinvertebrates
    {
        "id": "fauna.aquatic_macroinvertebrates",
        "label": "macroinvertebrados acuáticos de aguas glaciares",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "macroinvertebrados acuáticos en Los Nevados",
            "larvas de insectos en arroyos de deshielo",
            "tricópteros y plecópteros en ríos de montaña",
            "bichos en el agua fría del nevado",
            "bioindicadores de agua pura en el parque",
            "¿qué animales diminutos viven en el agua helada?",
            "larvas de efímeras en quebradas de alta montaña",
            "insectos acuaticos en arroyos glaciares",
            "Aquatic macroinvertebrates glacial streams Colombia",
            "benthic insects high altitude rivers Los Nevados",
            "gusanitos y ninfas bajo piedras en los rios",
            "calidad del agua medida con insectos acuaticos"
        ],
        "hard_negatives": [
            "purificación y filtros de agua portátiles para montaña",
            "nacimientos de ríos y cuencas hidrográficas de Caldas",
            "análisis de laboratorio de metales pesados en ceniza"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "En los arroyos de deshielo y lagunas glaciares de Los Nevados habita una comunidad especializada de macroinvertebrados bentónicos, dominada por estadios larvales de plecópteros, tricópteros y efemerópteros. Estos diminutos animales viven adheridos bajo piedras en corrientes turbulentas, donde el agua está casi helada pero extraordinariamente oxigenada. Son los mejores bioindicadores de la pristinidad y pureza del agua de montaña y sirven de sustento vital para patos de torrente y mirlos acuáticos.",
            "variants": [
                "Las larvas de tricópteros y plecópteros de Los Nevados demuestran la extrema pureza de las fuentes hídricas; su abundancia alimenta a las aves acuáticas que bucean en los torrentes del parque."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.torrent_duck", "fauna.white_capped_dipper", "fauna.rainbow_trout_impact"],
        "tags": ["macroinvertebrados", "bioindicadores", "aguas_glaciares", "plecopteros", "tricopteros"]
    },
    # 67. Soil Invertebrates (Escarabajos y descomponedores)
    {
        "id": "fauna.soil_invertebrates_paramo",
        "label": "escarabajos y descomponedores del suelo paramuno",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "escarabajos de páramo",
            "invertebrados del suelo en Los Nevados",
            "descomponedores de materia orgánica en alta montaña",
            "¿qué escarabajos viven en el frío del nevado?",
            "coleópteros adaptados al suelo volcánico",
            "escarabajos negros bajo las rocas",
            "fauna edáfica del páramo",
            "insectos que descomponen estiercol de danta y oso",
            "Paramo beetles soil invertebrates Los Nevados",
            "high altitude dung beetles Colombia",
            "cucaracheros y escarabajitos en el humus",
            "reciclaje de nutrientes por bichos del suelo"
        ],
        "hard_negatives": [
            "suelos volcánicos y cenizas del cráter Arenas",
            "formación geológica de las turberas y depósitos glaciares",
            "normativa sobre no remover piedras ni arrancar musgos"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "A pesar de las bajísimas temperaturas que ralentizan la descomposición, en el suelo de Los Nevados habitan escarabajos carábidos, curculiónidos y escarabajos estercoleros de montaña adaptados a digerir la dura materia vegetal y el estiércol de dantas y venados. Con cutículas gruesas que evitan la pérdida de agua y les confieren resistencia contra las heladas, estos incansables obreros reciclan nutrientes minerales esenciales para que los frailejones y pastos puedan seguir creciendo.",
            "variants": [
                "Los escarabajos y ácaros del suelo paramuno son el motor invisible del ecosistema; transforman la materia orgánica fría en nutrientes fértiles para la flora altoandina."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.insects_invertebrates_overview", "fauna.paramo_butterflies", "fauna.tapir_ecological_role"],
        "tags": ["escarabajos", "suelo_paramuno", "descomponedores", "carabidos", "nutrientes"]
    },
    # 68. Mountain River Crabs
    {
        "id": "fauna.mountain_river_crabs",
        "label": "cangrejos de agua dulce de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cangrejos de agua dulce en Los Nevados",
            "cangrejos de río de montaña",
            "Pseudothelphusidae",
            "¿hay cangrejos viviendo en ríos fríos?",
            "cangrejo sabanero o de quebrada en la cordillera",
            "crustáceos en arroyos de alta montaña",
            "cangrejo bajo piedras en el bosque nublado",
            "crustaceos de agua dulce en el parque",
            "Mountain river crabs freshwater Colombia",
            "high altitude freshwater crabs Los Nevados",
            "cangrejitos de río en quebradas de bosque andino",
            "crustáceos nativos de cuencas de montaña"
        ],
        "hard_negatives": [
            "platos de mariscos en restaurantes de la región",
            "prohibición de extraer fauna silvestre del parque",
            "recorrido del sendero termales hacia el páramo"
        ],
        "entities": {"animal_group": ["invertebrados"]},
        "needs": [],
        "answer": {
            "short": "En las quebradas cristalinas y bosques nublados de la vertiente media y alta del parque habitan cangrejos de agua dulce de la familia Pseudothelphusidae. Son crustáceos de caparazón redondeado pardo rojizo que respiran mediante branquias protegidas y desarrollo directo sin larvas acuáticas libres. Pasan el día escondidos bajo grandes rocas sumergidas y salen al oscurecer a alimentarse de restos vegetales y pequeños invertebrados, siendo presas de nutrias y aves.",
            "variants": [
                "Los cangrejos de montaña habitan los arroyos de cabecera en las cuencas del parque; su presencia es un testimonio de la excelente calidad y baja turbidez del agua corriente."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.aquatic_macroinvertebrates", "fauna.torrent_duck", "fauna.white_capped_dipper"],
        "tags": ["cangrejos_rio", "crustaceos", "pseudothelphusidae", "agua_dulce", "quebradas"]
    },
    # 69. Spotting in Sector Brisas / Valle de las Tumbas
    {
        "id": "fauna.spotting_sector_brisas",
        "label": "avistamiento de fauna en sector Brisas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna en el sector Brisas",
            "¿qué animales se ven en Valle de las Tumbas?",
            "avistar cóndores en Brisas",
            "animales que se pueden ver en la entrada norte",
            "¿qué fauna hay cerca del Nevado del Ruiz?",
            "avistamiento en el recorrido vehicular de Brisas",
            "pajaros y conejos en el sector norte",
            "que bichos salen en el valle de las tumbas",
            "Wildlife watching Brisas sector Los Nevados",
            "animals near Nevado del Ruiz Valle de las Tumbas",
            "fauna silvestre en la ruta norte hacia el ruiz",
            "donde ver animales si entro por brisas"
        ],
        "hard_negatives": [
            "requisito de vehículo cubierto para el recorrido Brisas",
            "tarifa de ingreso de vehículos particulares en Brisas",
            "alerta volcánica y actividad del volcán Nevado del Ruiz"
        ],
        "entities": {"sector": ["brisas"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "En el sector Brisas y el recorrido hacia el Valle de las Tumbas (paisaje de páramo y superpáramo del Ruiz), es muy frecuente observar cóndores andinos y águilas moras planeando en lo alto, caracaras curiquinges caminando sobre el suelo y conejos de páramo entre los pastizales. En los frailejonales florecidos podrás divisar con paciencia al chivito de páramo libando néctar. La vegetación abierta facilita divisar aves rapaces a gran distancia.",
            "variants": [
                "El sector norte (Brisas) es ideal para observar rapaces planeadoras como el cóndor andino y el caracara curiquinge, además del chivito de páramo en los parches de Espeletia."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_EBIRD, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.buffy_helmetcrest", "fauna.carunculated_caracara"],
        "tags": ["brisas", "valle_tumbas", "avistamiento", "condor", "ruiz"]
    },
    # 70. Spotting in Sector Laguna del Otún
    {
        "id": "fauna.spotting_sector_otun",
        "label": "observación de fauna en Laguna del Otún",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna en la Laguna del Otún",
            "animales en el sector Otún",
            "aves acuáticas en la Laguna del Otún",
            "¿se ven dantas en la Laguna del Otún?",
            "avistamiento de venados y patos en Otún",
            "fauna silvestre en el humedal Ramsar",
            "que animales puedo ver si voy a la laguna del otun",
            "rastros de tapir en las orillas de la laguna",
            "Wildlife watching Lake Otun Los Nevados",
            "animals in Otun lagoon sector Colombia",
            "patos andinos y gaviotas en la laguna",
            "avistamiento de mamiferos en el sector otun"
        ],
        "hard_negatives": [
            "ruta de senderismo desde El Cedral hasta la Laguna del Otún",
            "altura sobre el nivel del mar de la Laguna del Otún",
            "reserva de cupos para camping en el sector Otún"
        ],
        "entities": {"sector": ["otun"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El sector de la Laguna del Otún es el epicentro de la avifauna acuática del parque: allí verás nadar patos andinos (turrios), tinguas andinas y bandadas de gaviotas andinas. En sus orillas pantanosas y turberas húmedas es común encontrar huellas frescas de danta de montaña, venados cola blanca pastando al amanecer y caicas de páramo sondeando el fango. El silencio y la inmensidad del agua multiplican las opciones de avistamiento.",
            "variants": [
                "La Laguna del Otún combina aves acuáticas permanentes con mamíferos de alta montaña que bajan a beber; con unos binoculares y calma verás patos turrios, tinguas y huellas de danta."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_CARDER, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.andean_gull", "fauna.mountain_tapir"],
        "tags": ["laguna_otun", "otun", "avistamiento", "patos", "danta_huellas"]
    },
    # 71. Spotting in Sector La Pastora / Cloud Forest
    {
        "id": "fauna.spotting_sector_la_pastora",
        "label": "fauna en el sendero La Pastora",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna en La Pastora",
            "animales en el sendero El Cedral La Pastora",
            "avistamiento de aves en bosque de niebla",
            "¿qué fauna vive en la cuenca media del río Otún?",
            "tucanes y loros en el camino a La Pastora",
            "mamíferos en el bosque altoandino de Risaralda",
            "pajaros en la subida por La Pastora",
            "animales salvajes en el bosque nublado",
            "Wildlife in La Pastora trail Los Nevados",
            "birdwatching El Cedral to La Pastora Colombia",
            "avistamiento de tangaras y tororois en la pastora",
            "fauna de selva andina en el camino"
        ],
        "hard_negatives": [
            "servicios de hospedaje y alimentación en el refugio La Pastora",
            "horario de chivas de transporte desde Pereira a El Cedral",
            "cuidado de rodillas y articulaciones en bajadas prolongadas"
        ],
        "entities": {"sector": ["la_pastora"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El sendero que asciende por la cuenca del Otún atravesando el sector de La Pastora recorre una selva altoandina exuberante con la mayor concentración de biodiversidad del parque. Aquí es el mejor lugar para observar tororois esquivos (incluyendo el endémico tororoi de Miller), terlaques andinos, tangaras multicolor, el veloz pato de torrente y monos nocturnos en las cotas inferiores. También se registran con cámaras trampa tapires andinos y osos de anteojos.",
            "variants": [
                "El tramo boscoso hacia La Pastora alberga una riqueza aviar inmensa: bandadas mixtas de tangaras, tucanes de montaña, mirlos acuáticos y hábitat vital del oso andino."
            ]
        },
        "sources": [SOURCE_CARDER, SOURCE_PNN_PLAN, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.hooded_mountain_toucan", "fauna.brown_banded_antpitta", "fauna.mountain_tanagers"],
        "tags": ["la_pastora", "cedral", "bosque_niebla", "avistamiento", "tangaras"]
    },
    # 72. Spotting in Sector Santa Isabel
    {
        "id": "fauna.spotting_sector_santa_isabel",
        "label": "avistamiento de fauna en Santa Isabel",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna en el Nevado Santa Isabel",
            "animales en el sendero Conejeras",
            "¿qué animales se ven subiendo a Santa Isabel?",
            "avistamiento de fauna en la ruta a la nieve",
            "lagartijas y conejos en Santa Isabel",
            "aves en el sendero hacia el glaciar",
            "animales en la morrena de Santa Isabel",
            "que fauna hay camino al glaciar santa isabel",
            "Wildlife on Santa Isabel volcano trail",
            "animals near Conejeras trail Los Nevados",
            "fauna de alta montaña en el sector central",
            "aves que vuelan cerca del hielo en santa isabel"
        ],
        "hard_negatives": [
            "estado actual de la masa glaciar del Nevado Santa Isabel",
            "equipo técnico de crampones y cuerdas para glaciar",
            "tarifa de guianza especializada para alta cumbre"
        ],
        "entities": {"sector": ["santa_isabel"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Al subir hacia el glaciar Santa Isabel por senderos como Conejeras, transitarás por un gradiente de páramo y superpáramo rocoso. Es común observar al simpático tororoi leonado brincando entre la paja, conejos de páramo asustadizos, lagartijas collarejas sobre piedras calientes y águilas moras aprovechando las corrientes de viento. Con suerte en los riscos rocosos más altos divisarás al periquito de los nevados en vuelo veloz.",
            "variants": [
                "En la aproximación a Santa Isabel abunda fauna adaptada al límite de vegetación: tororois curiosos, copetones andinos, lagartijas heliotermas y rapaces de gran altura."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.tawny_antpitta", "fauna.mountain_collared_lizard", "fauna.paramo_rabbit"],
        "tags": ["santa_isabel", "conejeras", "glaciar", "avistamiento", "superparamo"]
    },
    # 73. Spotting in Sector Combeima / Tolima
    {
        "id": "fauna.spotting_sector_combeima",
        "label": "observación de fauna en cuenca Combeima",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "fauna en el cañón del Combeima",
            "animales en la ruta al Nevado del Tolima",
            "avistamiento en Juntas y El Silencio",
            "¿qué fauna habita en la vertiente del Tolima?",
            "loros y venados subiendo al Nevado del Tolima",
            "patos de torrente en el río Combeima",
            "fauna silvestre en la vertiente oriental del parque",
            "animales en el camino de ibague al nevado",
            "Wildlife in Combeima canyon Tolima trail",
            "animals seen hiking to Nevado del Tolima",
            "avistamiento de aves en el canion del combeima",
            "fauna de montana entrando por el tolima"
        ],
        "hard_negatives": [
            "itinerario de tres días para la cumbre del Tolima",
            "alquiler de mulas y arrieros en Juntas",
            "geología del cono volcánico del Nevado del Tolima"
        ],
        "entities": {"sector": ["combeima"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "La ruta por el Cañón del Combeima hacia el Nevado del Tolima atraviesa un bellísimo gradiente ecológico. En la parte baja del cañón, en el río Combeima, es habitual ver patos de torrente desafiando las corrientes y mirlos acuáticos. Más arriba, en los bosques de niebla y palmares, habitan el loro orejiamarillo y la cotorra paramuna, mientras que en las planicies de páramo del Tolima pastan venados soche y cola blanca.",
            "variants": [
                "La vertiente del Tolima ofrece una rica variedad de fauna: desde patos de aguas rápidas en el río Combeima hasta loros de montaña y venados en los valles altos de aproximación al volcán."
            ]
        },
        "sources": [SOURCE_CORTOLIMA, SOURCE_PNN_PLAN, SOURCE_EBIRD],
        "last_verified": "2026-11-21",
        "related": ["fauna.torrent_duck", "fauna.yellow_eared_parrot", "fauna.little_red_brocket"],
        "tags": ["combeima", "tolima", "ibague", "juntas", "avistamiento"]
    },
    # 74. Birdwatching altitudinal zones
    {
        "id": "fauna.birdwatching_altitudinal_zones",
        "label": "zonas altitudinales para observar aves",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "pisos térmicos y aves en Los Nevados",
            "¿a qué altura se ven más pájaros en el parque?",
            "diferencia de aves entre bosque altoandino y páramo",
            "zonas de altitud para pajarear en Los Nevados",
            "¿dónde hay más diversidad de aves?",
            "avifauna según la altura sobre el nivel del mar",
            "gradiente altitudinal de aves en la cordillera central",
            "altitudes para avistamiento ornitologico",
            "Birdwatching elevation zones Los Nevados",
            "cloud forest vs paramo bird diversity Colombia",
            "que pajaros hay en el bosque vs en el pajonal",
            "mejores cotas de altura para observar aves"
        ],
        "hard_negatives": [
            "zonas de vegetación y pisos altitudinales de flora",
            "cambio de presión atmosférica y mal de altura",
            "límites del parque en mapas cartográficos oficiales"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "La avifauna cambia radicalmente según la altitud: el bosque altoandino (2.600 a 3.400 m s. n. m.) alberga la mayor abundancia y diversidad de especies, como tangaras, tucanes de montaña, quetzales y loros. En cambio, el páramo y superpáramo (3.500 a 4.500 m s. n. m.) presenta menor número total de especies pero un grado de especialización y endemismo extremo, con tesoros como el chivito de páramo, el cóndor andino y el periquito de los nevados.",
            "variants": [
                "Para máxima variedad de cantos y colores, explora los bosques nublados entre 2.600 y 3.400 metros; para especies endémicas exclusivas de alta montaña, enfócate en el páramo sobre los 3.500 metros."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.buffy_helmetcrest", "fauna.hooded_mountain_toucan"],
        "tags": ["altitud", "pisos_termicos", "avifauna", "bosque_vs_paramo", "pajareo"]
    },
    # 75. Best hours for birding
    {
        "id": "fauna.best_hours_birding",
        "label": "mejores horas para observar aves",
        "kind": "procedure",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿a qué hora es mejor observar aves?",
            "mejores horarios para pajarear en Los Nevados",
            "cuándo están más activas las aves en el parque",
            "¿vale la pena madrugar para ver pájaros?",
            "horario ideal para avistamiento de aves de páramo",
            "a que horas cantan mas los pajaros en el nevado",
            "momento del dia para ver colibries y tangaras",
            "pajareo matutino en alta montana",
            "Best time of day for birdwatching Los Nevados",
            "what time to spot birds in the paramo?",
            "madrugar para ver aves en el parque nacional",
            "actividad de las aves por la manana vs por la tarde"
        ],
        "hard_negatives": [
            "horarios oficiales de ingreso en taquilla de Brisas",
            "previsión del tiempo y horas de mayor lluvia",
            "desayunos y refrigerios para caminantes tempranos"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El horario cumbre para observar aves es entre las 6:00 y las 9:30 a. m., cuando los primeros rayos de sol calientan el dosel y los pájaros salen activamente a forrajear e iniciar sus coros matutinos. A media mañana (10:00 a 13:00) es el momento óptimo para ver rapaces y cóndores, ya que el aire caliente genera corrientes térmicas ascendentes que facilitan su planeo. Al atardecer hay otro pico breve de actividad antes del anochecer.",
            "variants": [
                "Madrugar es la regla de oro: las aves pequeñas están hiperactivas entre las 6:00 y las 9:00 a. m.; para cóndores y águilas, espera a que el sol caliente el aire entre media mañana y mediodía."
            ]
        },
        "sources": [SOURCE_EBIRD, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.andean_condor", "fauna.weather_impact_wildlife"],
        "tags": ["horarios", "pajareo", "manana", "madrugar", "corrientes_termicas"]
    },
    # 76. Best hours for mammals
    {
        "id": "fauna.best_hours_mammals",
        "label": "horarios para registrar mamíferos silvestres",
        "kind": "procedure",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿a qué hora se pueden ver mamíferos?",
            "cuándo salen las dantas y los venados",
            "horario para ver animales grandes en Los Nevados",
            "¿los mamíferos del parque son diurnos o nocturnos?",
            "a qué horas hay más chance de ver un oso o venado",
            "caminatas al amanecer para ver fauna silvestre",
            "momento del dia para registrar mamiferos",
            "cuando estan activos los animales en el sendero",
            "Best time to spot mammals in Los Nevados",
            "when to see deer and tapirs Colombian paramo",
            "horas para ver fauna mayor en el nevado",
            "avistar mamiferos al crepusculo o amanecer"
        ],
        "hard_negatives": [
            "prohibición de realizar caminatas nocturnas sin permiso",
            "linternas frontales y baterías resistentes al frío",
            "horarios de apertura de senderos para público general"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La mayoría de los grandes mamíferos del parque (dantas, venados, pumas y osos) tienen hábitos crepusculares y nocturnos para evitar el calor diurno y la presencia humana. Tus mayores probabilidades de avistamiento o de encontrar huellas frescas ocurren durante la primera hora del alba (5:30 a 7:00 a. m.) o al caer la tarde (17:00 a 18:30). Durante el día suelen descansar resguardados en quebradas boscosas densas o matorrales cerrados.",
            "variants": [
                "Los mamíferos de alta montaña se mueven principalmente en la penumbra del amanecer y atardecer; caminar en absoluto silencio a primera hora de la mañana multiplica tus opciones de verlos."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_tapir", "fauna.white_tailed_deer", "fauna.spectacled_bear"],
        "tags": ["horarios_mamiferos", "crepusculo", "amanecer", "dantas", "huellas"]
    },
    # 77. Weather impact on wildlife
    {
        "id": "fauna.weather_impact_wildlife",
        "label": "cómo afecta el clima los avistamientos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿el clima afecta ver animales en Los Nevados?",
            "si llueve o hay niebla se pueden ver pájaros",
            "impacto del viento fuerte en la fauna",
            "¿con frío o heladas salen los animales?",
            "cómo influye el tiempo en los avistamientos",
            "ver aves en días lluviosos en el páramo",
            "clima y actividad de la fauna silvestre",
            "¿en qué temporada del año se ven más animales?",
            "How weather affects wildlife watching Los Nevados",
            "spotting animals in rain and fog Colombian Andes",
            "si esta nublado se ven los condores",
            "temporada seca vs lluviosa para ver fauna"
        ],
        "hard_negatives": [
            "pronóstico meteorológico oficial del IDEAM",
            "temporadas de lluvia y meses secos en el Eje Cafetero",
            "ropa impermeable para caminatas con lluvia"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El clima de alta montaña condiciona drásticamente la actividad animal: la lluvia persistente y la niebla densa hacen que las aves se refugien en el sotobosque y cesen sus cantos, mientras que el viento gélido obliga a los mamíferos a protegerse en cañadas. Los días secos y despejados (comunes entre enero-febrero y julio-agosto) calientan el suelo temprano, activando a los insectos, colibríes y rapaces planeadoras. Sin embargo, en mañanas con llovizna suave los mamíferos suelen moverse con mayor confianza.",
            "variants": [
                "El sol temprano estimula a las aves e insectos, mientras que la niebla cerrada dificulta la visibilidad; las temporadas secas suelen ofrecer mejores condiciones para avistar rapaces y fauna abierta."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.best_hours_birding", "fauna.best_hours_mammals", "fauna.fauna_overview"],
        "tags": ["clima", "niebla", "lluvia", "temporadas", "avistamientos"]
    },
    # 78. Encounter Spectacled Bear (Safety Protocol)
    {
        "id": "fauna.encounter_spectacled_bear",
        "label": "qué hacer si encuentras un oso",
        "kind": "safety",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿qué hago si me encuentro un oso de anteojos?",
            "protocolo si veo un oso en el sendero",
            "qué hacer si se acerca un oso andino",
            "cómo reaccionar ante un oso en Los Nevados",
            "¿el oso de anteojos me puede atacar?",
            "pasos de seguridad ante encuentro con oso",
            "si me sale un oso andino que hago",
            "reglas de seguridad si veo un oso en la montaña",
            "What to do if you encounter a spectacled bear?",
            "bear safety protocol Los Nevados National Park",
            "me cruce con un oso en el camino que hago",
            "como actuar si veo un oso con crias"
        ],
        "hard_negatives": [
            "teléfono de la Defensa Civil y Cruz Roja para rescates",
            "síntomas y tratamiento de hipotermia grave",
            "seguro médico y póliza de asistencia en viaje"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "Mantén la calma absoluta: el oso andino es tímido y por naturaleza buscará alejarse. No corras ni grites desesperadamente; háblale con voz firme y serena para que identifique tu presencia humana y retrocede con lentitud sin darle la espalda por completo ni bloquear su vía de escape. Jamás intentes acercarte para una foto y, si observas oseznos o crías, aléjate de inmediato con máxima cautela, pues la madre defenderá con energía a sus pequeños.",
            "variants": [
                "Ante un oso, quédate quieto, habla en tono calmado y retrocede despacio sin correr ni acorralarlo. Nunca te interpongas entre una madre y sus oseznos ni le ofrezcas comida."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.spectacled_bear", "fauna.safe_viewing_distance", "fauna.wildlife_aggression_myths"],
        "tags": ["encuentro_oso", "seguridad", "protocolo", "calma", "no_correr"]
    },
    # 79. Encounter Cougar / Puma (Safety Protocol)
    {
        "id": "fauna.encounter_cougar_puma",
        "label": "protocolo ante avistamiento de un puma",
        "kind": "safety",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿qué hacer si veo un puma en el camino?",
            "protocolo de seguridad si me cruzo con un puma",
            "cómo actuar ante un león de montaña en Los Nevados",
            "¿el puma ataca a los senderistas?",
            "qué hacer si un puma no se va del sendero",
            "consejos si te encuentras un felino salvaje",
            "si veo un puma tengo que correr",
            "como defenderse o ahuyentar a un puma",
            "What to do if you see a cougar in Los Nevados?",
            "mountain lion encounter safety guidelines",
            "me salio un puma en la trocha que hago",
            "normas de seguridad si avisto un puma"
        ],
        "hard_negatives": [
            "porte de armas de fuego y su estricta prohibición en Parques",
            "puntos de primeros auxilios y brigadistas en el parque",
            "botiquín para mordeduras de perros domésticos"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "Si ves un puma, mantén la calma y jamás corras, ya que correr puede activar su instinto de persecución depredadora. Hazte ver lo más grande posible alzando los brazos o abriendo tu chaqueta, mantén contacto visual sin mirarlo de forma desafiante y sube a los niños en tus hombros si viajas en familia. Háblale con voz fuerte, grave y resuelta mientras retrocedes lentamente dejándole siempre una ruta despejada para retirarse.",
            "variants": [
                "Frente a un puma: nunca corras ni le des la espalda. Párate erguido, haz ruido con firmeza, aparenta mayor tamaño y retrocede con lentitud; el felino buscará una salida para alejarse."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.cougar_puma", "fauna.safe_viewing_distance", "fauna.wildlife_aggression_myths"],
        "tags": ["encuentro_puma", "seguridad", "protocolo", "felino", "no_correr"]
    },
    # 80. Encounter Mountain Tapir (Safety Protocol)
    {
        "id": "fauna.encounter_mountain_tapir",
        "label": "qué hacer si ves una danta",
        "kind": "safety",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿qué hacer si me encuentro una danta de montaña?",
            "cómo actuar si veo un tapir en el páramo",
            "¿la danta de montaña es agresiva con la gente?",
            "pautas de comportamiento si veo una danta en la laguna",
            "puedo acariciar o tocar una danta silvestre",
            "qué hacer si una danta se cruza en el sendero",
            "avistamiento cercano de danta de paramo",
            "como reaccionar si me sale un tapir andino",
            "What to do if you encounter a mountain tapir?",
            "tapir encounter protocol Los Nevados",
            "me encontre una danta en el camino que hago",
            "distancia para observar a la danta de paramo"
        ],
        "hard_negatives": [
            "alquiler de caballos y animales de carga en sectores rurales",
            "prohibición de acampar cerca de fuentes hídricas de consumo",
            "normas de comportamiento en el centro de visitantes"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La danta de montaña es un animal noble, tímido y totalmente pacífico que solo busca alimentarse en calma. Quédate inmóvil y en absoluto silencio para disfrutar de su observación sin ahuyentarla, mantén al menos 30 metros de distancia y jamás intentes tocarla, perseguirla ni cerrarle el paso. Deja que cruce tranquilamente el sendero y nunca le arrojes comida ni hagas movimientos bruscos.",
            "variants": [
                "Si te topas con una danta, guarda silencio y respeta su espacio a prudente distancia; no intentes acercarte ni bloquear su camino para que pueda continuar su tránsito natural."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_tapir", "fauna.safe_viewing_distance", "fauna.feeding_wildlife_prohibition"],
        "tags": ["encuentro_danta", "tapir", "silencio", "distancia", "respeto"]
    },
    # 81. Safe Viewing Distance
    {
        "id": "fauna.safe_viewing_distance",
        "label": "distancia mínima para observar fauna silvestre",
        "kind": "safety",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿a qué distancia debo observar los animales silvestres?",
            "distancia mínima de seguridad con la fauna",
            "qué tan cerca me puedo acercar a un animal en el parque",
            "regla del pulgar para observar fauna",
            "distancia recomendada para fotos de fauna",
            "por qué no debo acercarme a los animales salvajes",
            "cuantos metros de distancia debo mantener con osos o dantas",
            "distancia prudente para no asustar animales",
            "Safe distance for viewing wildlife Los Nevados",
            "how close can I get to animals in national parks?",
            "metros de separacion con animales del parque",
            "norma de distancia para avistamiento responsable"
        ],
        "hard_negatives": [
            "distancia en kilómetros entre los diferentes sectores del parque",
            "lentes y objetivos fotográficos recomendados para trekking",
            "sanciones por ingresar a zonas de reserva estricta"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "La norma internacional y de Parques Nacionales es mantener un mínimo de 30 a 50 metros de separación con mamíferos medianos y grandes (como osos, dantas y venados), y al menos 10 metros con aves en sus perchas o nidos. Aplica la 'regla del pulgar': extiende el brazo y levanta el pulgar; si tu dedo no cubre por completo la silueta del animal, estás demasiado cerca y debes retroceder. Usa binoculares o teleobjetivos para fotografiarlos sin invadir su espacio vital.",
            "variants": [
                "Conserva al menos 30 a 50 metros de distancia con mamíferos silvestres; si el animal cambia su comportamiento o te mira fijamente, es señal inequívoca de que estás demasiado cerca."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.encounter_spectacled_bear", "fauna.encounter_cougar_puma", "fauna.feeding_wildlife_prohibition"],
        "tags": ["distancia_seguridad", "regla_pulgar", "avistamiento_etico", "teleobjetivo", "respeto"]
    },
    # 82. Wildlife Aggression Myths
    {
        "id": "fauna.wildlife_aggression_myths",
        "label": "¿los animales del páramo son peligrosos?",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿los animales de Los Nevados atacan a la gente?",
            "es peligroso caminar solo por la fauna salvaje",
            "miedo a los animales en el páramo",
            "¿el puma o el oso atacan turistas en Colombia?",
            "riesgo de ataques de animales salvajes en el parque",
            "son bravos los animales del nevado",
            "mitos sobre animales agresivos en alta montana",
            "que tan seguro es caminar con animales salvajes cerca",
            "Are wild animals dangerous in Los Nevados?",
            "risk of animal attacks in Colombian national parks",
            "los animales del parque muerden o persiguen",
            "peligro real de la fauna en los senderos"
        ],
        "hard_negatives": [
            "peligro de caída en grietas glaciares o acantilados",
            "riesgo volcánico por emisión de gases y cenizas del Ruiz",
            "pérdida de rumbo en el páramo por niebla densa"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Los animales nativos de Los Nevados no son agresivos ni ven al ser humano como presa; al contrario, su instinto natural es de extrema timidez y huida ante nuestra presencia. Los incidentes solo podrían ocurrir si un animal se siente acorralado, herido, si una madre percibe amenaza directa hacia sus crías, o si se intenta alimentarlo. Caminar por los senderos autorizados, hacer notar tu presencia y mantener distancia garantiza una experiencia 100 % segura.",
            "variants": [
                "No hay registros de ataques espontáneos de fauna silvestre a turistas en Los Nevados; los animales salvajes evitan a las personas y solo reaccionan defensivamente si se invade su espacio."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.safe_viewing_distance", "fauna.encounter_spectacled_bear", "fauna.encounter_cougar_puma"],
        "tags": ["mitos", "seguridad", "agresividad", "fauna_pacifica", "senderismo"]
    },
    # 83. Injured Wildlife Protocol
    {
        "id": "fauna.injured_wildlife_protocol",
        "label": "qué hacer si hallas fauna herida",
        "kind": "procedure",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿qué hago si encuentro un animal herido?",
            "encontré un pajarito o venado lastimado en el sendero",
            "protocolo si hallo fauna silvestre herida o huérfana",
            "puedo llevarme un animal herido a la ciudad",
            "cómo reportar un animal accidentado a los guardaparques",
            "animal silvestre golpeado en la carretera Brisas Murillo",
            "que hacer con una cría abandonada en el páramo",
            "a quien aviso si veo un animal herido",
            "What to do if you find injured wildlife in Los Nevados?",
            "reporting wounded animal to park rangers Colombia",
            "vi un animalito quebrado en el camino que hago",
            "atencion de fauna silvestre accidentada en el parque"
        ],
        "hard_negatives": [
            "atención de primeros auxilios para personas con fracturas",
            "reporte de emergencias médicas humanas a la línea 123",
            "veterinarias y clínicas de mascotas en Manizales o Pereira"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Bajo ninguna circunstancia intentes manipular, cargar o trasladar al animal: un animal herido sentirá pánico y puede morder o agravar sus lesiones, y muchas crías aparentemente 'solas' tienen a sus madres vigilándolas cerca. Toma nota del punto exacto del sendero (o coordenadas GPS si tienes) y avisa de inmediato al personal de Guardaparques de PNN o en el centro de control más cercano para que veterinarios y biólogos activen el rescate técnico.",
            "variants": [
                "No toques ni muevas al animal herido; anota el lugar exacto y repórtalo de inmediato a los funcionarios de Parques Nacionales para que ellos apliquen el protocolo de rescate veterinario."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.roadkill_risk_murillo_road", "fauna.poaching_hunting_prohibition", "fauna.safe_viewing_distance"],
        "tags": ["animal_herido", "rescate", "guardaparques", "protocolo", "no_tocar"]
    },
    # 84. Feeding Wildlife Prohibition
    {
        "id": "fauna.feeding_wildlife_prohibition",
        "label": "por qué no se debe alimentar animales",
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿puedo darle comida a los animales del parque?",
            "por qué está prohibido alimentar la fauna silvestre",
            "darle pan a los pájaros o conejos en el nevado",
            "alimentar zorros o mirlos en el sendero",
            "impacto de la comida humana en animales salvajes",
            "¿qué pasa si le doy frutas o galletas a un animal?",
            "prohibicion de cebar fauna en parques nacionales",
            "dar comida a los pajaritos en los miradores",
            "Why is feeding wildlife prohibited in Los Nevados?",
            "can I feed birds or mammals in the national park?",
            "darle sobras de almuerzo a los animales",
            "razones biologicas para no alimentar fauna"
        ],
        "hard_negatives": [
            "comida y calorías recomendadas para la dieta del montañista",
            "manejo y empaque de raciones de marcha para el frío",
            "tiendas y restaurantes autorizados en las entradas del parque"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Alimentar a la fauna silvestre está estrictamente prohibido por ley y daña gravemente su salud: la comida humana contiene harinas procesadas, azúcares y sales que provocan desnutrición severa, diarreas y deformaciones óseas en animales adaptados a forrajes silvestres. Además, genera dependencia artificial, pérdida del instinto de búsqueda y conductas de mendicidad agresiva que suelen terminar en atropellamientos en las carreteras.",
            "variants": [
                "Nunca alimentes a los animales del parque; la comida procesada enferma sus sistemas digestivos y altera su comportamiento natural haciéndolos dependientes y vulnerables a accidentes."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.roadkill_risk_murillo_road", "fauna.safe_viewing_distance", "fauna.crab_eating_fox"],
        "tags": ["no_alimentar", "prohibicion", "salud_animal", "mendicidad", "norma"]
    },
    # 85. Pets Prohibition Reason
    {
        "id": "fauna.pets_prohibition_reason",
        "label": "por qué no se permiten mascotas",
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿puedo llevar mi perro a Los Nevados?",
            "por qué no dejan entrar mascotas al parque",
            "prohibición de perros y gatos en parques nacionales",
            "impacto de mascotas en la fauna silvestre",
            "¿mi perro con correa puede subir al páramo?",
            "enfermedades que los perros transmiten a la fauna",
            "razones de la prohibicion de mascotas en Los Nevados",
            "perros domesticos en el parque nacional",
            "Are dogs allowed in Los Nevados National Park?",
            "why pets are strictly banned in Colombian national parks",
            "puedo llevar a mi perrito al nevado del ruiz",
            "mascotas y conservacion de fauna en alta montana"
        ],
        "hard_negatives": [
            "guarderías caninas y hospedaje para mascotas en Manizales",
            "vacunación humana requerida para ingresar a Colombia",
            "sanciones económicas por infringir normas generales del parque"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El ingreso de perros, gatos y cualquier mascota doméstica está terminantemente prohibido en todos los sectores del parque, incluso con correa. Los caninos transmiten enfermedades virales letales para la fauna nativa como el moquillo (distemper), parvovirus y sarna, contra las cuales dantas, zorros y felinos carecen de defensas inmunológicas. Asimismo, su olor, ladridos y persecución generan pánico y estrés severo en venados y aves nidificantes.",
            "variants": [
                "Las mascotas están totalmente prohibidas en Los Nevados porque propagan epidemias mortales a carnívoros nativos y alteran los patrones reproductivos y de forrajeo de la fauna silvestre."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.feral_dogs_threat", "fauna.mountain_tapir", "fauna.feeding_wildlife_prohibition"],
        "tags": ["mascotas_prohibidas", "perros", "moquillo", "distemper", "reglamento"]
    },
    # 86. Feral Dogs Threat
    {
        "id": "fauna.feral_dogs_threat",
        "label": "amenaza de perros asilvestrados a la fauna",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "perros asilvestrados en Los Nevados",
            "perros ferales atacando fauna",
            "jaurías de perros en el páramo",
            "ataques de perros a dantas y venados",
            "problema de perros abandonados en la alta montaña",
            "¿los perros callejeros cazan en el parque?",
            "impacto de caninos cimarrones en la conservacion",
            "jaurias cazando en la laguna del otun",
            "Feral dogs threat to wildlife Los Nevados",
            "stray dogs attacking mountain tapir Colombia",
            "perros salvajes persiguiendo animales en el nevado",
            "control de perros asilvestrados por parques nacionales"
        ],
        "hard_negatives": [
            "abandono de basuras y restos de comida en senderos",
            "campañas de esterilización de mascotas en municipios vecinos",
            "normas de tenencia responsable de animales de granja"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "Los perros abandonados o sueltos por comunidades y visitantes vecinos constituyen una de las mayores amenazas para la fauna de Los Nevados. Al formar jaurías asilvestradas en el páramo, cazan en grupo persiguiendo hasta el agotamiento y la muerte a especies en peligro como la danta de montaña, el venado conejo y aves que anidan en el suelo. Parques Nacionales y las corporaciones regionales desarrollan censos y planes de manejo para controlar esta grave problemática.",
            "variants": [
                "Las jaurías de perros asilvestrados representan un peligro crítico de depredación y contagio de enfermedades para dantas y venados en Los Nevados, lo que refuerza la prohibición total de mascotas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_CARDER, SOURCE_CORPOCALDAS],
        "last_verified": "2026-11-21",
        "related": ["fauna.pets_prohibition_reason", "fauna.mountain_tapir", "fauna.threatened_species"],
        "tags": ["perros_asilvestrados", "jaurias", "ferales", "amenaza_fauna", "depredacion"]
    },
    # 87. Roadkill Risk on Murillo Road
    {
        "id": "fauna.roadkill_risk_murillo_road",
        "label": "peligro de atropellamiento en vía Brisas-Murillo",
        "kind": "safety",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "atropellamiento de animales en la vía Manizales Murillo",
            "velocidad máxima en la carretera de Los Nevados",
            "pasos de fauna en la vía a Murillo",
            "peligro para la fauna en la carretera pavimentada",
            "zorros y dantas atropellados en la vía",
            "conducir despacio por el parque para proteger animales",
            "animales cruzando la carretera entre Caldas y Tolima",
            "precauciones al manejar por la carretera del Ruiz",
            "Wildlife roadkill risk Manizales Murillo road",
            "speed limits wildlife crossing Los Nevados",
            "atropellos de fauna silvestre en la carretera",
            "senales de transito de cruce de dantas y osos"
        ],
        "hard_negatives": [
            "estado del pavimento y peajes en la vía Manizales-Murillo",
            "transporte público y horarios de buses intermunicipales",
            "miradores fotográficos a la orilla de la carretera"
        ],
        "entities": {"sector": ["brisas"], "animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "La pavimentación de la vía Manizales–Murillo ha incrementado peligrosamente el atropellamiento de fauna silvestre como zorros, conejos, comadrejas y dantas de montaña. Es imperativo conducir a baja velocidad (máximo 30 a 40 km/h en los tramos de parque y zona amortiguadora), encender luces antiniebla y redoblar la atención al amanecer, atardecer o con niebla, respetando rigurosamente los pasos de fauna señalizados.",
            "variants": [
                "Respeta los límites de velocidad reducida en la vía Brisas-Murillo; muchos animales cruzan intempestivamente entre la niebla y un manejo prudente evita muertes trágicas de especies protegidas."
            ]
        },
        "sources": [SOURCE_CORPOCALDAS, SOURCE_CORTOLIMA, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.crab_eating_fox", "fauna.mountain_tapir", "fauna.feeding_wildlife_prohibition"],
        "tags": ["atropellamiento", "via_murillo", "velocidad", "pasos_fauna", "seguridad_vial"]
    },
    # 88. Noise and Drone Disturbance
    {
        "id": "fauna.noise_drone_disturbance",
        "label": "impacto del ruido y drones en animales",
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿se puede volar dron en Los Nevados?",
            "prohibición de drones por afectación a la fauna",
            "por qué no se permite música con parlantes en el parque",
            "impacto del ruido en las aves y cóndores",
            "drones asustando a los animales del páramo",
            "estrés sonoro en la fauna silvestre",
            "puedo llevar parlante bluetooth al sendero",
            "ruido excesivo y ahuyentamiento de fauna",
            "Are drones banned in Los Nevados because of wildlife?",
            "noise pollution impact on birds Colombian national parks",
            "volar dron para filmar cóndores está permitido",
            "normas sobre silencio y grabacion aerea"
        ],
        "hard_negatives": [
            "permisos para grabaciones cinematográficas comerciales",
            "tipos de cámaras y trípodes para fotografía terrestre",
            "sanciones por desacato a los guardaparques"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "El uso de drones no autorizados y los parlantes o reproductores de música están estrictamente prohibidos en el parque. El zumbido agudo de los drones es percibido por aves rapaces y cóndores como una amenaza territorial directa o un depredador aéreo, provocando que abandonen sus nidos con huevos o polluelos y gasten energía vital huyendo en pánico. El ruido humano desorienta a la fauna y priva a los demás visitantes del sosiego natural.",
            "variants": [
                "Los drones y parlantes generan un grave estrés sonoro en cóndores, aves acuáticas y mamíferos; el parque es un santuario de silencio donde la tranquilidad acústica está protegida por ley."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_condor", "fauna.birding_playback_rules", "fauna.birds_overview"],
        "tags": ["drones_prohibidos", "ruido", "estres_acustico", "condores", "silencio"]
    },
    # 89. Birding Playback Rules
    {
        "id": "fauna.birding_playback_rules",
        "label": "uso ético de grabaciones y playback",
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿se puede usar playback para atraer aves en Los Nevados?",
            "reproducir cantos de aves con parlantes o celular",
            "ética ornitológica en avistamiento de aves",
            "prohibición de playback en especies amenazadas",
            "cómo atraer pájaros sin perjudicarlos",
            "reglas para observación ética de aves en el parque",
            "estrés por playback en colibríes y tororois",
            "normativa de Parques Nacionales sobre cantos grabados",
            "Can I use bird playback in Los Nevados?",
            "ethical birding guidelines playback restrictions Colombia",
            "poner cantos en el celular para que salgan los pajaros",
            "guia de conducta responsable para pajareros"
        ],
        "hard_negatives": [
            "aplicaciones móviles para identificación de cantos como Merlin",
            "tours comerciales organizados de aviturismo",
            "contratación de guías bilingües de aves en Caldas"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El uso intensivo o repetitivo de grabaciones de cantos (playback) para forzar la salida de aves está restringido en el parque y prohibido terminantemente en especies en peligro (como el periquito de los nevados o la cotorra de Fuertes). Esta práctica genera un desgaste metabólico crítico al hacer que el ave gaste energía buscando un intruso ficticio en vez de alimentar a sus crías o alimentarse a sí misma bajo el frío extremo. La observación paciente y en silencio es siempre la mejor práctica.",
            "variants": [
                "El playback excesivo estresa territorialmente a las aves de montaña; practica un pajareo ético y paciente sin alterar las rutinas naturales de las especies protegidas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.birds_overview", "fauna.best_hours_birding", "fauna.threatened_species"],
        "tags": ["playback", "pajareo_etico", "grabaciones", "aves_amenazadas", "estres"]
    },
    # 90. Poaching and Hunting Prohibition
    {
        "id": "fauna.poaching_hunting_prohibition",
        "label": "prohibición total de caza y recolección",
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿se puede cazar en Los Nevados?",
            "prohibición de caza y pesca en el parque",
            "sanciones por capturar animales silvestres",
            "recolección de plumas, nidos, astas o insectos",
            "delito ambiental por tráfico de fauna en Colombia",
            "llevarse mariposas o escarabajos del nevado",
            "normas contra el trampeo y la cacería furtiva",
            "ley de protección de fauna en parques nacionales",
            "Is hunting or fishing permitted in Los Nevados?",
            "strict wildlife protection and poaching penalties Colombia",
            "puedo pescar en las lagunas del parque",
            "prohibicion de colecta cientifica sin permiso formal"
        ],
        "hard_negatives": [
            "trámites formales de permisos de investigación científica en PNN",
            "compra de artesanías de lana en tiendas autorizadas",
            "normativa sobre porte de linternas y navajas de montaña"
        ],
        "entities": {"animal_group": ["general"]},
        "needs": [],
        "answer": {
            "short": "La caza, la pesca, el trampeo, el hostigamiento y la recolección de cualquier ejemplar de fauna viva o muerta (incluyendo huevos, nidos, plumas, cornamentas de venado o insectos) están totalmente prohibidos en Los Nevados. La legislación colombiana (Ley 1333 de 2009 y Código Penal) tipifica estas acciones como delitos ambientales graves sancionados con multas millonarias y penas de prisión. Toda investigación biológica exige permisos previos del Ministerio de Ambiente y PNN.",
            "variants": [
                "En el parque rige una protección absoluta: está prohibido cazar, pescar o sustraer cualquier animal o parte biológica. Respeta la vida silvestre y déjala exactamente como la encontraste."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN],
        "last_verified": "2026-11-21",
        "related": ["fauna.fauna_overview", "fauna.threatened_species", "fauna.injured_wildlife_protocol"],
        "tags": ["prohibicion_caza", "delito_ambiental", "recoleccion_prohibida", "proteccion_legal", "sanciones"]
    }
]
