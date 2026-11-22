# -*- coding: utf-8 -*-
"""
Entries group 1: Topics 1 to 18
Ecosystems overview, páramo, superpáramo, subpáramo, high Andean forest,
arenales, altitudinal gradient, carbon sequestration, and frailejones biology.
"""

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
HUMBOLDT_URL = "http://www.humboldt.org.co/es/investigacion/proyectos/actuales/item/222-paramos-de-colombia"
DATE_VERIFIED = "2026-11-21"

ENTRIES = [
    {
        "id": "flora_ecosystems.park_ecosystems_overview",
        "label": "ecosistemas presentes en el parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué ecosistemas tiene el parque",
            "cuales son los ecosistemas de los nevados",
            "que paisajes ecologicos hay",
            "cuales pisos termicos se encuentran en la visita",
            "venga qué tipo de vegetacion y zonas hay en el parque",
            "oiga aqui que clases de ecosistemas protegen",
            "cuales ecosistemas voy a ver si subo al nevado",
            "ecosistemas protegidos los nevados",
            "que ecosistemas hay en el parque de los nevados",
            "diferentes zonas de vida en los nevados",
            "what ecosystems are found in Los Nevados park",
            "which ecological zones exist in the national park",
            "cuales ambientes naturales tiene los nevados",
            "hay bosque y paramo en el parque"
        ],
        "hard_negatives": [
            "qué animales viven en el parque",
            "cuánto cuesta la entrada al parque",
            "cuáles son las cumbres más altas del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El parque protege cuatro grandes ecosistemas andinos: bosque altoandino o de niebla, páramo, superpáramo y la zona nival o glaciar. En tu recorrido cruzas estos ambientes según la altitud, desde frondosos bosques nublados hasta arenales y hielos de cumbre.",
            "variants": [
                "En Los Nevados encuentras una transición de bosque altoandino, páramo con frailejones, superpáramo pedregoso y masa glaciar. Cada franja tiene flora y condiciones climáticas únicas que vas descubriendo a medida que ganas altura."
            ],
            "detail": "El gradiente altitudinal del parque va desde aproximadamente 2.600 metros en sus cañones boscosos hasta más de 5.300 metros sobre el nivel del mar en las nieves del Nevado del Ruiz."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.paramo_ecosystem",
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.high_andean_forest"
        ],
        "tags": ["ecosistemas", "paisajes", "pisos termicos", "zonas de vida", "biodiversidad"]
    },
    {
        "id": "flora_ecosystems.paramo_ecosystem",
        "label": "ecosistema de páramo del parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el páramo",
            "que es un paramo",
            "como es el ecosistema de paramo",
            "caracteristicas del paramo en los nevados",
            "a que altura empieza el paramo en el parque",
            "oiga y ese paramo qué tiene de especial",
            "venga cuénteme cómo es la vegetacion del paramo",
            "por que es tan famoso el paramo de los nevados",
            "paramo de los nevados caracteristicas",
            "que clima y plantas hay en el paramo",
            "what is the paramo ecosystem in Los Nevados",
            "can you explain what a paramo is",
            "donde queda el paramo en este recorrido",
            "es muy frio el paramo de los nevados"
        ],
        "hard_negatives": [
            "qué senderos puedo caminar en el páramo",
            "qué ropa debo llevar para el frío del páramo",
            "a qué hora abren el sector Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El páramo es un ecosistema neotropical de alta montaña ubicado aproximadamente entre 3.600 y 4.200 metros de altitud en el parque. Se caracteriza por sus extensos pajonales, colonias de frailejones, humedales y un clima frío y húmedo fundamental para regular el agua de Colombia.",
            "variants": [
                "En Los Nevados, el páramo domina entre 3.600 y 4.200 metros sobre el nivel del mar, destacando por sus frailejones, turberas y pajonales. Es una verdadera fábrica natural de agua que retiene las lluvias y nieblas andinas."
            ],
            "detail": "Colombia concentra cerca del 50 % de los páramos del mundo, y el complejo de Los Nevados es uno de los más extensos y biodiversos del país."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.water_cycle_basin_supply"
        ],
        "tags": ["paramo", "alta montana", "frailejones", "regulacion hidrica", "clima frio"]
    },
    {
        "id": "flora_ecosystems.superparamo_ecosystem",
        "label": "ecosistema de superpáramo del parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el superpáramo",
            "que es el superparamo",
            "como es el superparamo en los nevados",
            "a que altura queda el superparamo",
            "venga y qué hay mas arriba del paramo",
            "oiga qué plantas crecen en el superpáramo",
            "diferencia entre paramo y superparamo",
            "superparamo los nevados caracteristicas",
            "por que se ve tan pelado el superparamo",
            "como sobrevive la vegetacion en el superparamo",
            "what is the superparamo zone in Los Nevados",
            "how is the superparamo different from paramo",
            "cuales son las condiciones del superparamo",
            "hay vida vegetal en el superparamo"
        ],
        "hard_negatives": [
            "cómo evitar el mal de altura en el superpáramo",
            "se puede subir a la cumbre del Ruiz",
            "qué volcanes activos hay en el parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El superpáramo es la franja más alta y extrema del páramo, ubicada aproximadamente entre 4.200 y 4.700 metros de altitud, justo antes del hielo glaciar. Su suelo es pedregoso y volcánico, con heladas casi diarias y una vegetación pionera muy bajita y dispersa.",
            "variants": [
                "Ubicado entre 4.200 y 4.700 metros sobre el nivel del mar, el superpáramo presenta condiciones climáticas severas con fuertes vientos y suelos arenosos. Aquí solo sobreviven líquenes, musgos y pequeñas hierbas arrosetadas adaptadas al congelamiento."
            ],
            "detail": "En sectores como Valle de las Tumbas puedes apreciar el aspecto casi lunar del superpáramo, moldeado por la ceniza volcánica y el rigor del viento."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.paramo_ecosystem",
            "flora_ecosystems.arenales_volcanicos_ecosystem",
            "flora_ecosystems.cacho_de_venado_loricaria"
        ],
        "tags": ["superparamo", "arenales", "suelo volcanico", "heladas", "vegetacion pionera"]
    },
    {
        "id": "flora_ecosystems.subparamo_transition",
        "label": "franja de subpáramo y transición",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el subpáramo",
            "que es la zona de subparamo",
            "donde empieza el subparamo en los nevados",
            "como es la transicion de bosque a paramo",
            "venga que vegetacion hay entre el bosque y el paramo",
            "oiga por que cambia tanto el bosque antes del paramo",
            "que plantas hay en el subparamo del parque",
            "ecotono bosque altoandino paramo",
            "arbustos del subparamo en los nevados",
            "limite superior del bosque en los nevados",
            "what is the subparamo transitional zone",
            "what vegetation grows between cloud forest and paramo",
            "arboles achaparrados del subparamo",
            "subparamo altura y caracteristicas"
        ],
        "hard_negatives": [
            "dónde acampar en el bosque altoandino",
            "cuántos kilómetros hay de Manizales a Brisas",
            "qué aves habitan el subpáramo"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El subpáramo es la zona de transición o ecotono entre el bosque altoandino y el páramo abierto, situada entre 3.300 y 3.600 metros de altitud. Se distingue por una densa franja de arbustos leñosos, chusques y árboles achaparrados que pierden altura frente al viento frío.",
            "variants": [
                "Entre 3.300 y 3.600 metros de altitud cruzas el subpáramo, donde los árboles dan paso a matorrales densos de chite, romeros y ericáceas. Esta franja protege las laderas contra la erosión y amortigua los cambios de temperatura."
            ],
            "detail": "En este ecotono abundan especies de los géneros Hypericum, Diplostephium y Baccharis, que toleran tanto la humedad del bosque como las ráfagas heladas del páramo."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.high_andean_forest",
            "flora_ecosystems.paramo_ecosystem",
            "flora_ecosystems.chite_hypericum"
        ],
        "tags": ["subparamo", "transicion", "ecotono", "matorral", "limite del bosque"]
    },
    {
        "id": "flora_ecosystems.high_andean_forest",
        "label": "bosque altoandino y de niebla",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo es el bosque altoandino del parque",
            "que es el bosque de niebla en los nevados",
            "hay selva o bosque en el parque los nevados",
            "a que altura esta el bosque altoandino",
            "venga qué arboles crecen en el bosque nublado",
            "oiga por que hay tanta niebla y musgo en esos arboles",
            "bosque alto andino los nevados especies",
            "caracteristicas del bosque nuboso en los nevados",
            "arboles nativos del bosque altoandino",
            "donde se puede ver bosque altoandino en la ruta",
            "what is the high Andean cloud forest in Los Nevados",
            "cloud forest vegetation in Los Nevados national park",
            "bosque de alta montana parque los nevados",
            "flora del bosque altoandino en caldas y tolima"
        ],
        "hard_negatives": [
            "dónde ver osos de anteojos en el bosque",
            "se puede hacer fogata en el bosque",
            "qué agencia ofrece tours al bosque de niebla"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El bosque altoandino o de niebla se extiende entre los 2.600 y 3.600 metros de altitud en las laderas del parque. Sus árboles están cubiertos de musgos, orquídeas y bromelias epífitas que capturan la humedad de las nubes y alimentan los arroyos de montaña.",
            "variants": [
                "Entre 2.600 y 3.600 metros sobre el nivel del mar prospera el bosque altoandino, caracterizado por encenillos, alisos y densas capas de musgos que retienen agua. Es un ecosistema fresco y sombreado con niebla constante."
            ],
            "detail": "Este bosque actúa como barrera natural contra deslizamientos y es el refugio clave de la cuenca alta de ríos como el Otún, Chinchiná y Combeima."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.subparamo_transition",
            "flora_ecosystems.encenillos_weinmannia",
            "flora_ecosystems.epiphytic_mosses_cloud_forest"
        ],
        "tags": ["bosque altoandino", "bosque de niebla", "epifitas", "encenillos", "alta montana"]
    },
    {
        "id": "flora_ecosystems.arenales_volcanicos_ecosystem",
        "label": "arenales volcánicos y desierto paramuno",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los arenales volcánicos",
            "por que hay tanta arena y ceniza arriba",
            "como es el desierto del nevado del ruiz",
            "valle de las tumbas por que no tiene plantas",
            "venga por que se ve como un desierto de piedra y ceniza",
            "oiga por que no crecen arboles en los arenales",
            "arenales del ruiz vegetacion",
            "desierto paramuno en los nevados",
            "que plantas sobreviven en las cenizas del volcan",
            "paisaje de ceniza volcanica en el parque",
            "volcanic ash desert in Los Nevados park",
            "why are there volcanic sand plains with few plants",
            "arenales de alta montana en caldas",
            "es verdad que arriba parece la luna por la ceniza"
        ],
        "hard_negatives": [
            "cuál es el nivel de alerta volcánica del Ruiz",
            "cómo llegar al mirador Valle de las Tumbas",
            "cuál fue la última erupción del cráter Arenas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los arenales son planicies de alta montaña cubiertas por gruesas capas de ceniza, pómez y escombros expulsados por el volcán Nevado del Ruiz. La extrema porosidad del suelo, el viento constante y las heladas limitan la vegetación a escasos líquenes y plantas pioneras diminutas.",
            "variants": [
                "En sectores altos como el Valle de las Tumbas encuentras arenales volcánicos donde las cenizas impiden retener nutrientes superficiales. Por eso el paisaje parece desértico, aunque alberga líquenes y pequeñas rosetas adaptadas al sustrato volcánico móvil."
            ],
            "detail": "Pese a su aspecto yermo, este desierto de cenizas cumple una función de infiltración subterránea de aguas de deshielo y lluvias."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.stereocaulon_crustose_lichens",
            "flora_ecosystems.cacho_de_venado_loricaria"
        ],
        "tags": ["arenales", "ceniza volcanica", "desierto paramuno", "valle de las tumbas", "vegetacion pionera"]
    },
    {
        "id": "flora_ecosystems.altitudinal_gradient_changes",
        "label": "cambio de vegetación por altura",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo cambia la vegetación al subir al nevado",
            "por que cambian las plantas con la altura",
            "gradiente altitudinal de plantas en los nevados",
            "que plantas voy viendo en el camino hacia arriba",
            "venga por que se van achicando los arboles al subir",
            "oiga por que desaparecen los arboles despues de cierta altura",
            "transicion de flora de abajo hacia la cumbre",
            "pisos de vegetacion en los nevados de colombia",
            "como es el cambio de plantas segun los metros de altura",
            "limite de arboles y comienzo de frailejones",
            "how does vegetation change with altitude in Los Nevados",
            "altitudinal zonation of plants in the national park",
            "a que altura se acaban los arboles en los nevados",
            "por que la vegetacion es mas bajita arriba"
        ],
        "hard_negatives": [
            "a qué altura me puede dar soroche",
            "cuántos kilómetros tiene la subida a Brisas",
            "dónde alquilar camioneta 4x4 para subir"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "A medida que asciendes, la temperatura disminuye y el viento arrecia, por lo que los árboles altos del bosque de niebla dan paso a arbustos del subpáramo, luego a los frailejonales y pastizales del páramo, y finalmente a plantas diminutas en el superpáramo.",
            "variants": [
                "El parque muestra una clara zonificación: abajo los bosques densos captan niebla; sobre los 3.600 metros dominan frailejones y pajonales; y sobre los 4.200 metros las plantas se hacen enanas y pegadas al suelo para protegerse de las heladas."
            ],
            "detail": "El límite de árboles o 'treeline' se sitúa alrededor de los 3.600 a 3.800 metros, donde las bajas temperaturas nocturnas impiden el desarrollo de tallos leñosos altos."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.park_ecosystems_overview",
            "flora_ecosystems.high_andean_forest",
            "flora_ecosystems.adaptation_dwarfism_prostrate"
        ],
        "tags": ["gradiente altitudinal", "pisos termicos", "treeline", "adaptacion", "paisajes"]
    },
    {
        "id": "flora_ecosystems.paramo_carbon_sequestration",
        "label": "captura de carbono en páramos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo capturan carbono los páramos",
            "el paramo almacena carbono",
            "por que los suelos del paramo guardan carbono",
            "secuestro de carbono en el parque los nevados",
            "venga es verdad que el paramo ayuda contra el cambio climatico",
            "oiga por que dicen que los suelos negros guardan co2",
            "almacenamiento de carbono organico en turberas",
            "paramo sumidero de carbono en colombia",
            "cuanto carbono guardan los suelos de alta montana",
            "importancia del paramo para el clima global",
            "how do paramos store organic carbon",
            "carbon sequestration in high Andean soils",
            "suelos andisoles e histosoles carbono paramuno",
            "el frailejon y el suelo como sumidero de carbono"
        ],
        "hard_negatives": [
            "cuántas hectáreas mide el parque Los Nevados",
            "qué hacer si veo humo de un incendio",
            "dónde registrar mi visita al parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los suelos volcánicos y turberas del páramo retienen enormes volúmenes de carbono orgánico porque el frío y la humedad ralentizan la descomposición de la materia vegetal. Esto convierte a Los Nevados en un valioso sumidero natural de carbono que ayuda a mitigar el cambio climático.",
            "variants": [
                "Gracias a las bajas temperaturas y suelos saturados, los restos de frailejones y musgos se descomponen muy despacio y acumulan carbono durante milenios. Proteger el páramo evita que ese carbono atrapado se libere a la atmósfera en forma de CO2."
            ],
            "detail": "Los andisoles e histosoles de páramo pueden almacenar hasta tres veces más carbono por metro cuadrado que muchos suelos de bosques tropicales bajos."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.paramo_ecosystem",
            "flora_ecosystems.turberas_bogs_peatlands",
            "flora_ecosystems.sujeto_de_derechos_ruling"
        ],
        "tags": ["carbono", "suelos", "turberas", "cambio climatico", "andisoles"]
    },
    {
        "id": "flora_ecosystems.frailejones_overview",
        "label": "frailejones presentes en el parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué especie de frailejón hay en el parque",
            "cuales son los frailejones de los nevados",
            "hay frailejones en el parque los nevados",
            "como se llama el frailejon de los nevados",
            "venga cuénteme sobre los frailejones del ruiz",
            "oiga que planta es ese frailejon tan bonito",
            "frailejon espeletia hartwegiana los nevados",
            "donde se ven frailejones en el recorrido",
            "que caracteristicas tiene el frailejon del parque",
            "planta insignia del parque nacional los nevados",
            "what frailejon species grows in Los Nevados",
            "tell me about the frailejones in the park",
            "espeletia en los nevados de caldas y risaralda",
            "los frailejones son protegidos en colombia"
        ],
        "hard_negatives": [
            "qué colibríes visitan los frailejones",
            "está permitido llevarse una hoja de frailejón",
            "cuántos volcanes hay en el parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La especie insignia de frailejón en Los Nevados es Espeletia hartwegiana, adaptada a las laderas volcánicas de la cordillera Central. Sus hojas lanosas de color plateado forman densos bosques paramunos esenciales para capturar la niebla y nutrir los ríos.",
            "variants": [
                "En el parque predomina Espeletia hartwegiana, un frailejón de hojas blanquecinas y afelpadas que domina los paisajes entre 3.600 y 4.300 metros. Es la planta más emblemática de Los Nevados y el corazón del ciclo hídrico regional."
            ],
            "detail": "El nombre común 'frailejón' proviene de los colonizadores españoles, a quienes estas plantas cubiertas de follaje lanudo les recordaban la silueta de frailes encapuchados en medio de la neblina."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejon_growth_rate",
            "flora_ecosystems.frailejon_water_sponge_function",
            "flora_ecosystems.frailejon_species_subspecies"
        ],
        "tags": ["frailejones", "espeletia hartwegiana", "planta insignia", "paramo", "hojas lanosas"]
    },
    {
        "id": "flora_ecosystems.frailejon_growth_rate",
        "label": "crecimiento y edad de frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cuánto crece un frailejón por año",
            "que tan rapido crece un frailejon",
            "tasa de crecimiento de los frailejones",
            "cuantos anos vive un frailejon",
            "venga es verdad que los frailejones crecen un centimetro al ano",
            "oiga ese frailejón de dos metros cuántos años tiene",
            "edad de los frailejones gigantes en los nevados",
            "crecimiento lento de espeletia hartwegiana",
            "cuanto demora en crecer un frailejon en el paramo",
            "los frailejones son centenarios",
            "how fast do frailejones grow per year",
            "how old can a frailejon plant be",
            "anos de vida de un frailejon de montana",
            "por que tarda tanto en crecer un frailejon"
        ],
        "hard_negatives": [
            "cuánto mide el Nevado del Ruiz",
            "cuánto cuesta el pasadía al parque",
            "puedo plantar frailejones en el jardín de mi casa"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los frailejones crecen a un ritmo muy lento, apenas entre 1 y 2 centímetros por año debido a las bajas temperaturas de alta montaña. Un ejemplar que mida dos metros de altura puede tener fácilmente entre 100 y 150 años de vida.",
            "variants": [
                "En promedio, Espeletia hartwegiana gana entre uno y dos centímetros al año en Los Nevados. Por eso, los frailejones altos que ves a orillas del camino son verdaderos monumentos centenarios que han resistido décadas de heladas y viento."
            ],
            "detail": "Su lentísimo crecimiento hace que cualquier daño por pisoteo o fuego sea prácticamente irreparable a escala de una vida humana."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_fire_vulnerability",
            "flora_ecosystems.frailejon_touching_no_damage"
        ],
        "tags": ["crecimiento", "edad", "centenarios", "centimetros por ano", "conservacion"]
    },
    {
        "id": "flora_ecosystems.frailejon_water_sponge_function",
        "label": "captación de agua por frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo atrapan agua los frailejones",
            "como capturan agua de la niebla los frailejones",
            "funcion de esponja del frailejon",
            "por que dicen que el frailejon produce agua",
            "venga cómo hace el frailejon para sacar agua de las nubes",
            "oiga de verdad los pelos del frailejon agarran la lluvia",
            "captura de precipitacion horizontal por frailejones",
            "como baja el agua del frailejon hacia el suelo",
            "mecanismo hidrico de espeletia hartwegiana",
            "los frailejones y la niebla del paramo",
            "how do frailejones capture water from clouds and mist",
            "why are frailejones called water sponges",
            "filtracion de agua por hojas de frailejon",
            "el frailejon como regulador hidrico"
        ],
        "hard_negatives": [
            "cuántos litros de agua debo tomar para no deshidratarme",
            "dónde comprar botellas de agua en Brisas",
            "qué ríos nacen en el parque Los Nevados"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las hojas del frailejón están recubiertas de finos pelos lanosos que interceptan las microgotas de la niebla y la lluvia horizontal. Esas gotas se condensan, escurren por el tallo hacia el suelo paramuno y se infiltran lentamente alimentando las quebradas de la región.",
            "variants": [
                "Gracias a su densa vellosidad, el frailejón 'peina' las nubes y condensa la humedad ambiental. El agua capturada desciende por su tronco hasta el suelo orgánico, funcionando como una esponja natural que mantiene el caudal de los ríos en época seca."
            ],
            "detail": "Este fenómeno se conoce como 'precipitación horizontal' u oculta, y en Los Nevados aporta una fracción considerable del agua total que drena hacia los acueductos."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.paramo_sponge_mechanism",
            "flora_ecosystems.water_cycle_basin_supply"
        ],
        "tags": ["captacion de agua", "niebla", "precipitacion horizontal", "esponja", "pelos lanosos"]
    },
    {
        "id": "flora_ecosystems.frailejon_thermal_adaptation",
        "label": "adaptación del frailejón al frío",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo sobrevive el frailejón al frío extremo",
            "por que el frailejon no se congela por las noches",
            "como aguanta las heladas el frailejon",
            "adaptaciones del frailejon al clima del paramo",
            "venga por que las hojas del frailejon tienen pelos blancos",
            "oiga cómo se protege del viento helado el frailejón",
            "morfologia de espeletia contra temperaturas bajo cero",
            "resistencia al congelamiento en frailejones",
            "por que el frailejon tiene esa forma de roseta",
            "vellosidades protectoras del frailejon",
            "how do frailejones survive freezing temperatures",
            "thermal adaptations of frailejones in alpine conditions",
            "anticongelante natural de las plantas de paramo",
            "proteccion del frailejon contra la radiacion solar"
        ],
        "hard_negatives": [
            "qué abrigo debo llevar para no congelarme en el parque",
            "cuál es la temperatura mínima histórica del Ruiz",
            "qué hacer en caso de hipotermia en la montaña"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El frailejón tolera temperaturas bajo cero gracias a una combinación de adaptaciones: una densa capa de pelos plateados que retiene aire tibio, hojas organizadas en roseta que resguardan la yema central y una envoltura de hojas secas en el tallo.",
            "variants": [
                "Para resistir las heladas nocturnas, Espeletia hartwegiana utiliza pelos blancos que reflejan la intensa radiación UV y retienen una capa de aire aislante. Además, su roseta apical se cierra ligeramente en la noche protegiendo el cogollo tierno."
            ],
            "detail": "Sus células acumulan azúcares y resinas que actúan como anticongelantes biológicos, evitando que el agua interna forme cristales de hielo que rompan los tejidos."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_dead_leaves_necromass",
            "flora_ecosystems.adaptation_leaf_pubescence"
        ],
        "tags": ["adaptacion al frio", "pelos plateados", "roseta", "anticongelante", "heladas"]
    },
    {
        "id": "flora_ecosystems.frailejon_dead_leaves_necromass",
        "label": "función de hojas secas del frailejón",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué los frailejones tienen hojas secas en el tronco",
            "para que sirven las hojas muertas del frailejon",
            "se le deben quitar las hojas secas a los frailejones",
            "es verdad que las hojas secas protegen al frailejon",
            "venga por que no se le caen las hojas viejas al frailejón",
            "oiga por que el tallo del frailejon parece cubierto de abrigo",
            "necromasa foliar en espeletia hartwegiana",
            "hojas marchitas adheridas al tallo del frailejon",
            "por que nunca hay que arrancarle las hojas secas",
            "abrigo natural del tronco del frailejon",
            "why do frailejones keep dead leaves on their stems",
            "function of dry dead leaves covering frailejon trunks",
            "aislamiento termico de hojas secas en frailejon",
            "las hojas secas del frailejon son un abrigo"
        ],
        "hard_negatives": [
            "se puede recoger leña seca en el parque",
            "está permitido hacer fogatas con hojas secas",
            "cuáles son las sanciones por dañar la flora"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las hojas secas adheridas al tronco forman un abrigo térmico indispensable que aísla los vasos conductores del tallo frente a las heladas bajo cero. Nunca se deben arrancar, ya que retirarlas dejaría al frailejón desprotegido y provocaría su muerte por congelamiento.",
            "variants": [
                "Esa capa de hojas marchitas, llamada necromasa, funciona como una ruana o chaqueta que mantiene estable la temperatura del tronco. Si alguien las desprende, expone los tejidos vasculares al frío nocturno y la planta se deshidrata o congela."
            ],
            "detail": "Además de aislamiento térmico, las hojas secas albergan comunidades de pequeños insectos y microorganismos benéficos del ecosistema paramuno."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_thermal_adaptation",
            "flora_ecosystems.frailejon_touching_no_damage"
        ],
        "tags": ["hojas secas", "necromasa", "abrigo termico", "aislamiento", "tallo"]
    },
    {
        "id": "flora_ecosystems.frailejon_stem_water_storage",
        "label": "almacenamiento de agua en el tallo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo almacena agua el tallo del frailejón",
            "el frailejon guarda agua adentro del tronco",
            "medula esponjosa del tallo del frailejon",
            "cuanta agua tiene un frailejon en su interior",
            "venga es cierto que el tronco del frailejon es como una esponja",
            "oiga adentro del frailejón hay agua acumulada",
            "reservorio hidrico en el tallo de espeletia",
            "estructura interna del tronco del frailejon",
            "el frailejon almacena humedad para epocas de sequia",
            "tejido de almacenamiento de agua en frailejones",
            "how do frailejones store water inside their trunks",
            "spongy pith tissue of frailejon stems water reserve",
            "los frailejones guardan agua como los cactus",
            "capacidad de retencion de agua en el tronco de espeletia"
        ],
        "hard_negatives": [
            "se puede tomar agua directamente del frailejón",
            "qué hacer si me quedo sin agua en el sendero",
            "dónde nacen las fuentes de agua del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El tallo del frailejón posee una médula interna ancha y esponjosa compuesta por células parenquimatosas que almacenan gran cantidad de agua. Este reservorio interno le permite a la planta seguir hidratada y fotosintetizar incluso durante los días más secos y ventosos.",
            "variants": [
                "Por dentro, el tronco de Espeletia hartwegiana contiene un tejido poroso cargado de agua y savia. Funciona como un tanque de reserva que amortigua las fluctuaciones entre el calor diurno y las heladas nocturnas."
            ],
            "detail": "Este volumen de agua en el tallo también contribuye a su inercia térmica, impidiendo que el centro de la planta se enfríe con rapidez en las noches de páramo."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_water_sponge_function",
            "flora_ecosystems.frailejon_thermal_adaptation"
        ],
        "tags": ["medula esponjosa", "tallo", "almacenamiento de agua", "reserva hidrica", "inercia termica"]
    },
    {
        "id": "flora_ecosystems.frailejon_flowering_season",
        "label": "floración y flores de los frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cuándo florecen los frailejones",
            "en que epoca florecen los frailejones",
            "como son las flores del frailejon",
            "los frailejones dan flores amarillas",
            "venga en qué meses se ven los frailejones florecidos",
            "oiga por que salen esas cabezuelas amarillas en el frailejon",
            "floracion sincronizada de espeletia hartwegiana",
            "flores tipo margarita de los frailejones",
            "temporada de flores en el paramo de los nevados",
            "inflorescencias de los frailejones en el parque",
            "when do frailejones bloom in Los Nevados",
            "what do frailejon flowers look like",
            "meses de floracion del frailejon en caldas",
            "los frailejones florecen todos los anos"
        ],
        "hard_negatives": [
            "cuál es la mejor época de clima seco para visitar el parque",
            "se pueden tomar fotografías comerciales de las flores",
            "qué aves migratorias llegan en época de floración"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los frailejones producen inflorescencias con flores amarillas parecidas a margaritas, ya que pertenecen a la familia de las compuestas (Asteráceas). Suelen florecer con mayor intensidad entre octubre y enero, aprovechando periodos de transición climática para facilitar la polinización.",
            "variants": [
                "Las flores de Espeletia hartwegiana son ramilletes de margaritas amarillas que brotan en lo alto de la roseta. Aunque pueden verse flores dispersas durante el año, la floración masiva ocurre generalmente hacia el final del año e inicios de la temporada seca."
            ],
            "detail": "En algunos años ocurre una floración masiva o sincrónica en todo el páramo, ofreciendo un espectáculo visual dorado y abundante néctar para la fauna de altura."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_pollinators",
            "flora_ecosystems.senecio_and_arnicas"
        ],
        "tags": ["floracion", "flores amarillas", "margaritas", "asteraceas", "inflorescencias"]
    },
    {
        "id": "flora_ecosystems.frailejon_pollinators",
        "label": "polinización y colibrí del frailejón",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "quién poliniza los frailejones",
            "como se polinizan los frailejones",
            "que animales polinizan las flores del frailejon",
            "el colibri chivito de paramo come de los frailejones",
            "venga qué bicho o pajaro visita las flores del frailejon",
            "oiga como interactuan los colibries con los frailejones",
            "polinizadores nativos de espeletia hartwegiana",
            "oxypogon stuebelii y el frailejon de los nevados",
            "insectos y colibries polinizando en el paramo",
            "relacion ecologica entre frailejones y aves",
            "who pollinates frailejon flowers in the park",
            "pollination of frailejones by high altitude hummingbirds",
            "abejorros de paramo y flores de frailejon",
            "importancia ecologica de las flores del frailejon"
        ],
        "hard_negatives": [
            "dónde fotografiar el colibrí chivito de páramo",
            "cuántas especies de aves hay en Los Nevados",
            "qué binoculares llevar para avistamiento de fauna"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La polinización de los frailejones depende principalmente del viento y de animales de alta montaña como abejorros nativos, moscas paramunas y el emblemático colibrí chivito de páramo (Oxypogon stuebelii). Este colibrí endémico extrae néctar de sus flores y percha habitualmente sobre sus rosetas.",
            "variants": [
                "Tanto abejorros del páramo como el colibrí chivito de páramo visitan las flores de Espeletia hartwegiana en busca de polen y néctar. A cambio, transportan el polen entre plantas asegurando la fecundación y producción de semillas."
            ],
            "detail": "El chivito de páramo incluso utiliza las pelusas lanosas de las hojas de frailejón para acolchar sus nidos en grietas rocosas protegidas del viento."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_flowering_season",
            "flora_ecosystems.frailejon_water_sponge_function"
        ],
        "tags": ["polinizacion", "colibri chivito", "oxypogon stuebelii", "abejorros", "simbiosis"]
    },
    {
        "id": "flora_ecosystems.frailejon_resin_and_smell",
        "label": "resina aromática del frailejón paramuno",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "a qué huele el frailejón",
            "por que huele tan rico el paramo",
            "resina aromatica de los frailejones",
            "que olor despiden las hojas de frailejon",
            "venga por que el frailejón tiene ese aroma como a trementina",
            "oiga qué es esa sustancia pegajosa en las hojas del frailejón",
            "olor a incienso o resina en el parque los nevados",
            "aceites esenciales y resinas de espeletia",
            "para que le sirve la resina al frailejon",
            "sustancias quimicas protectoras del frailejon",
            "what does a frailejon smell like",
            "aromatic resin and essential oils of frailejones",
            "olor caracteristico del paramo en los nevados",
            "propiedades de la resina de los frailejones"
        ],
        "hard_negatives": [
            "puedo recolectar resina de frailejón para medicina",
            "por qué huele a azufre cerca del cráter",
            "qué plantas medicinales puedo comprar fuera del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El frailejón desprende un aroma resinoso penetrante similar al pino o al incienso debido a los aceites esenciales y terpenos que produce en sus hojas. Esta resina actúa como escudo químico para repeler insectos herbívoros, frenar infecciones de hongos y evitar la deshidratación.",
            "variants": [
                "Ese olor característico que percibes en el páramo proviene de la resina aromática de Espeletia hartwegiana. Estas sustancias amargas protegen las hojas jóvenes contra plagas y crean una barrera impermeable que reduce la pérdida de agua por transpiración."
            ],
            "detail": "Tradicionalmente los campesinos llamaban a esta resina 'bálsamo de páramo', pero en el parque está terminantemente prohibido extraerla o dañar la planta."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_thermal_adaptation",
            "flora_ecosystems.frailejon_touching_no_damage"
        ],
        "tags": ["resina", "aroma", "terpenos", "defensa quimica", "balsamo de paramo"]
    },
    {
        "id": "flora_ecosystems.frailejon_species_subspecies",
        "label": "especie y subespecie de frailejón",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cuántas especies de frailejón hay en Los Nevados",
            "que subespecie de frailejon vive en el parque",
            "espeletia hartwegiana subespecie centroandina",
            "hay varias clases de frailejones en los nevados",
            "venga cual es el nombre cientifico del frailejon del parque",
            "oiga este frailejon es el mismo de chingaza o sumapaz",
            "taxonomia de los frailejones en los nevados",
            "diferencia de espeletia hartwegiana con otros frailejones",
            "subespecies de frailejon en la cordillera central",
            "espeletia en caldas risaralda y tolima",
            "what specific frailejon subspecies lives in Los Nevados",
            "is Espeletia hartwegiana endemic to the Central Andes",
            "clasificacion botanica del frailejon de los nevados",
            "solo hay un tipo de frailejon en el parque"
        ],
        "hard_negatives": [
            "cuántos departamentos abarca el parque Los Nevados",
            "en qué sector se ven más frailejones",
            "dónde queda el páramo de Sumapaz"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En el Parque Nacional Natural Los Nevados la especie dominante es Espeletia hartwegiana, y la población local corresponde a la subespecie Espeletia hartwegiana subsp. centroandina. Es un frailejón adaptado a las cenizas volcánicas y laderas escarpadas de la cordillera Central colombiana.",
            "variants": [
                "A diferencia de páramos como Sumapaz o Chingaza donde coexisten muchas especies de frailejón, en Los Nevados predomina de manera casi exclusiva Espeletia hartwegiana subsp. centroandina, reconocida por su tronco robusto y hojas plateadas."
            ],
            "detail": "Fue descrita científicamente en honor al botánico alemán Karl Theodor Hartweg, quien exploró y recolectó flora andina en el siglo XIX."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.frailejon_growth_rate",
            "flora_ecosystems.paramo_ecosystem"
        ],
        "tags": ["espeletia hartwegiana", "subespecie centroandina", "taxonomia", "endemismo", "cordillera central"]
    }
]
