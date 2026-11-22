# -*- coding: utf-8 -*-
"""
Entries group 2: Topics 19 to 36
Frailejones threats, conservation, Polylepis trees, wax palms, shrubs, and pajonales.
"""

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
HUMBOLDT_URL = "http://www.humboldt.org.co/es/investigacion/proyectos/actuales/item/222-paramos-de-colombia"
DATE_VERIFIED = "2026-11-21"

ENTRIES = [
    {
        "id": "flora_ecosystems.frailejon_pests_larvae_fungi",
        "label": "plagas y hongos en frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué plagas atacan a los frailejones",
            "por que se estan muriendo algunos frailejones",
            "enfermedades del frailejon en los nevados",
            "larvas barrenadoras que comen frailejon",
            "venga qué es ese hongo que seca a los frailejones",
            "oiga por que hay frailejones negros o marchitos",
            "sindrome de declive del frailejon en colombia",
            "polillas y hongos fusarium en el paramo",
            "amenazas biologicas contra espeletia hartwegiana",
            "como combaten las plagas de los frailejones",
            "what pests and fungi attack frailejones in the park",
            "why are some frailejon plants dying from caterpillars",
            "afectacion de insectos en el cogollo del frailejon",
            "es verdad que el calor sube plagas al paramo"
        ],
        "hard_negatives": [
            "se pueden aplicar insecticidas en el parque",
            "qué vacunas necesito para viajar a Colombia",
            "por qué se declaran alertas volcánicas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los frailejones enfrentan el ataque de larvas de polillas y escarabajos que barrenan el cogollo o yema apical, abriendo camino a hongos patógenos como Fusarium. Este síndrome de declive se ha agravado con el cambio climático, ya que temperaturas más cálidas facilitan el ascenso de insectos al páramo.",
            "variants": [
                "En varias zonas paramunas se reporta la muerte de frailejones causada por larvas que destruyen su único punto de crecimiento. Detrás de las larvas entran hongos que pudren el tallo, un problema monitoreado sin químicos para no alterar las fuentes hídricas."
            ],
            "detail": "Parques Nacionales y el Instituto Humboldt realizan monitoreo constante de este fenómeno, descartando plaguicidas sintéticos que contaminarían el agua potable de millones de personas."
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
            "flora_ecosystems.frailejon_growth_rate",
            "flora_ecosystems.glacier_retreat_climate_change"
        ],
        "tags": ["plagas", "larvas barrenadoras", "hongos", "fusarium", "declive de frailejones"]
    },
    {
        "id": "flora_ecosystems.frailejon_fire_vulnerability",
        "label": "vulnerabilidad del frailejón ante incendios",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué los frailejones son tan vulnerables al fuego",
            "que pasa si se quema un frailejondal",
            "el frailejon se quema muy rapido",
            "los incendios matan a los frailejones",
            "venga por que arden tan facil las hojas de frailejón",
            "oiga cuanto demora en recuperarse un paramo quemado",
            "impacto del fuego en espeletia hartwegiana",
            "resinas inflamables en las hojas de frailejon",
            "por que esta prohibido prender fuego en el parque",
            "danos por incendios de cobertura vegetal en los nevados",
            "why are frailejones so susceptible to wildfires",
            "how do forest fires destroy frailejon populations",
            "los frailejones rebrotan despues de un incendio",
            "muerte del meristemo apical del frailejon por quemas"
        ],
        "hard_negatives": [
            "se puede llevar estufa de gas al campamento",
            "dónde reportar un conato de incendio en el parque",
            "cuáles son las multas por hacer fogatas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las hojas secas y resinas aromáticas del frailejón son altamente inflamables y arden con gran intensidad durante los incendios forestales. Cuando el fuego alcanza la yema o cogollo central de la planta, el frailejón muere de inmediato sin posibilidad de rebrote.",
            "variants": [
                "Un incendio en el páramo destruye décadas de crecimiento en pocos minutos. Aunque las hojas secas protegen al tallo del frío, ante el fuego funcionan como combustible y calcinan el meristemo terminal del que depende la vida de la planta."
            ],
            "detail": "La regeneración natural de un frailejonal arrasado por el fuego puede tardar entre 50 y 100 años si no cuenta con banco de semillas viable o si ingresa ganado al área quemada."
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
            "flora_ecosystems.frailejon_growth_rate",
            "flora_ecosystems.wildfire_impact_and_recovery"
        ],
        "tags": ["incendios", "inflamabilidad", "meristemo apical", "vulnerabilidad", "quemas"]
    },
    {
        "id": "flora_ecosystems.frailejon_nursery_propagation",
        "label": "viveros y propagación de frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "se pueden cultivar frailejones en viveros",
            "como reproducen frailejones en los nevados",
            "viveros de alta montana para frailejones",
            "germinacion de semillas de espeletia hartwegiana",
            "venga es posible sembrar frailejones para reforestar",
            "oiga donde reproducen plantulas de frailejon",
            "proyectos de propagacion de frailejones en caldas y tolima",
            "restauracion con frailejones de vivero",
            "cuanto tarda en germinar una semilla de frailejon",
            "cultivo de frailejones en laboratorio y vivero",
            "can frailejones be propagated in high mountain nurseries",
            "reforestation and nursery seedling production of frailejones",
            "siembra de frailejones en zonas degradadas",
            "comunidades campesinas cuidando viveros de paramo"
        ],
        "hard_negatives": [
            "puedo comprar plántulas de frailejón para llevar a casa",
            "cuánto cobran los guías locales por la caminata",
            "qué programas de voluntariado hay en Parques Nacionales"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Parques Nacionales, corporaciones ambientales y comunidades locales han implementado viveros de alta montaña para germinar semillas de Espeletia hartwegiana. Estas plántulas se cuidan durante meses en condiciones controladas de altitud antes de trasplantarlas a zonas de páramo degradadas por quemas o ganado.",
            "variants": [
                "La propagación de frailejones en viveros comunitarios es una estrategia clave de restauración ecológica en Los Nevados. Requiere recolectar semillas maduras y reproducir el microclima frío del páramo para lograr que las plántulas enraícen con éxito."
            ],
            "detail": "Las semillas de frailejón tienen porcentajes bajos de viabilidad natural, por lo que los viveros aplican técnicas de estratificación en frío para romper su dormancia."
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
            "flora_ecosystems.ecological_restoration_programs"
        ],
        "tags": ["viveros", "propagacion", "semillas", "restauracion", "reforestacion"]
    },
    {
        "id": "flora_ecosystems.frailejon_touching_no_damage",
        "label": "cuidado y prohibición de arrancar frailejones",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "se pueden tocar los frailejones",
            "puedo abrazar un frailejon en el parque",
            "por que no se deben arrancar hojas de frailejon",
            "es malo pisar las plantulas de frailejon",
            "venga puedo tocar la hoja de frailejon para sentir la lana",
            "oiga por que dicen que no se deben abrazar los frailejones",
            "normas de respeto hacia los frailejones en la visita",
            "dano al meristemo del frailejon por turistas",
            "por que esta prohibido llevarse un frailejon",
            "como cuidar los frailejones durante la caminata",
            "can visitors touch or hug frailejones in the park",
            "why is it forbidden to pluck frailejon leaves",
            "cuidado de la yema apical del frailejon",
            "pisar el suelo alrededor de los frailejones causa dano"
        ],
        "hard_negatives": [
            "cuánto es la multa por llevarse plantas del parque",
            "se permite el ingreso de mascotas con correa",
            "dónde comprar artesanías afuera del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Está prohibido arrancar hojas, desprender la necromasa seca del tronco o abrazar con fuerza los frailejones, pues se compacta el suelo y se puede quebrar su cogollo central. Aunque puedes rozar suavemente una hoja para apreciar su textura lanosa, mantente siempre en el sendero demarcado.",
            "variants": [
                "Abrazar frailejones o pisar sus raíces compacta el suelo esponjoso e introduce patógenos en el cogollo apical. Observa y admira su belleza sin maltratar su follaje ni arrancarle ningún tejido protector."
            ],
            "detail": "Arrancar o comerciar con partes de frailejón es un delito ambiental en Colombia castigado por la legislación penal y ambiental vigente."
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
            "flora_ecosystems.sujeto_de_derechos_ruling"
        ],
        "tags": ["cuidado", "prohibicion", "conservacion", "pisoteo", "respeto ambiental"]
    },
    {
        "id": "flora_ecosystems.polylepis_sericea_colorado",
        "label": "árbol siete cueros de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el árbol siete cueros de páramo",
            "arbol colorado o quinual en los nevados",
            "polylepis sericea en el parque los nevados",
            "arboles que crecen a mas de tres mil metros",
            "venga cuál es ese arbol de tronco rojizo en la quebrada",
            "oiga qué arbol es ese que tiene corteza como papel",
            "bosques de polylepis en la cordillera central",
            "siete cueros de alta montana especie protegida",
            "donde se ven arboles de coloradito en el parque",
            "arbol emblematico de paramo polylepis",
            "what is the Polylepis sericea tree in Los Nevados",
            "the high altitude paperbark tree of the Andes",
            "siete cueros arbol valor objeto de conservacion",
            "relictos de bosque de quinual en los nevados"
        ],
        "hard_negatives": [
            "dónde ver el cóndor andino en el parque",
            "qué senderos tienen mayor dificultad física",
            "cuántos refugios de montaña hay en el parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El siete cueros de páramo o colorado (Polylepis sericea) es un árbol altoandino capaz de crecer por encima de los 3.500 metros de altitud, formando parches boscosos en quebradas resguardadas. Es un Valor Objeto de Conservación prioritario en Los Nevados por su rareza y su papel protector de cuencas.",
            "variants": [
                "Polylepis sericea es uno de los árboles que vive a mayor altitud en el planeta, adaptado a laderas rocosas y cañadas paramunas. Sus pequeños bosques regulan el agua, frenan vientos helados y dan refugio a aves especializadas de montaña."
            ],
            "detail": "Históricamente estos bosques sufrieron tala para leña y carbón vegetal, por lo que hoy los parches sobrevivientes son celosamente protegidos y restaurados por los guardaparques."
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
            "flora_ecosystems.polylepis_papery_bark_adaptation",
            "flora_ecosystems.high_andean_forest",
            "flora_ecosystems.subparamo_transition"
        ],
        "tags": ["polylepis sericea", "siete cueros", "colorado", "arbol altoandino", "objeto de conservacion"]
    },
    {
        "id": "flora_ecosystems.polylepis_papery_bark_adaptation",
        "label": "corteza de papel del siete cueros",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué la corteza de Polylepis parece papel",
            "para que le sirve la corteza en capas al siete cueros",
            "corteza exfoliante de polylepis sericea",
            "por que se le cae la cáscara en hojas al arbol colorado",
            "venga por que el tronco de ese arbol parece tener muchas telas rojas",
            "oiga por que le dicen siete cueros al arbol de paramo",
            "aislamiento termico de la corteza de polylepis",
            "laminas rojizas de corteza en arboles de alta montana",
            "como protege el frio la corteza del quinual",
            "corteza papiracea de polylepis adaptacion",
            "why does Polylepis bark peel in thin paper-like layers",
            "thermal adaptation of paperbark tree in the Andes",
            "arbol con tronco de capas de papel en los nevados",
            "corteza laminada contra el hielo nocturno"
        ],
        "hard_negatives": [
            "puedo usar la corteza del árbol para encender fuego",
            "qué hacer si un árbol bloquea la carretera",
            "dónde comprar artesanías de madera en Manizales"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El nombre 'siete cueros' se debe a que su tronco está envuelto en múltiples láminas finas y rojizas de corteza superpuestas como hojas de papel. Esta estructura multicapa atrapa bolsas de aire aislante que protegen los conductos internos del árbol contra el congelamiento nocturno.",
            "variants": [
                "La corteza papirácea de Polylepis sericea se descascara continuamente en capas rojizas. Cada lámina actúa como un aislante térmico natural que impide que las temperaturas bajo cero dañen la savia y los tejidos vitales del tronco."
            ],
            "detail": "Estas láminas también dificultan que las plantas epífitas o insectos dañinos colonicen masivamente el tronco, al desprenderse de forma periódica."
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
            "flora_ecosystems.polylepis_sericea_colorado",
            "flora_ecosystems.frailejon_dead_leaves_necromass",
            "flora_ecosystems.adaptation_thick_cuticle_waxes"
        ],
        "tags": ["corteza papiracea", "siete cueros", "aislamiento termico", "polylepis", "adaptacion al frio"]
    },
    {
        "id": "flora_ecosystems.wax_palm_quindio",
        "label": "palma de cera en zonas bajas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay palmas de cera en el parque Los Nevados",
            "donde estan las palmas de cera en los nevados",
            "palma de cera del quindio ceroxylon quindiuense",
            "se ven palmas de cera subiendo al parque",
            "venga en que parte del parque crece el arbol nacional de colombia",
            "oiga hay palmas de cera en los bosques nublados",
            "ceroxylon quindiuense en la zona de amortiguacion",
            "palmas de cera en la cuenca del rio otun o quindio",
            "a que altura crecen las palmas de cera",
            "arbol nacional de colombia en el parque los nevados",
            "are wax palms found inside Los Nevados national park",
            "where do Quindio wax palms grow near the park",
            "palma de cera en el bosque altoandino",
            "bosques de palma de cera en salento y los nevados"
        ],
        "hard_negatives": [
            "cómo llegar al Valle de Cocora desde Salento",
            "dónde comprar boletos para el Valle de Cocora",
            "qué loro habita en las palmas de cera"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La palma de cera del Quindío (Ceroxylon quindiuense), árbol nacional de Colombia, habita en las franjas de bosque altoandino y zonas de amortiguación del parque, principalmente entre 2.500 y 3.100 metros de altitud. Sobresale por sus troncos blancos que superan los 50 metros emergiendo sobre el dosel de la niebla.",
            "variants": [
                "En los cañones boscosos de las cuencas del Quindío, Otún y Combeima encuentras palmas de cera dentro de la zona de influencia del parque. Son gigantes vegetales que coronan el bosque de niebla y sirven de hogar a especies amenazadas como el loro orejiamarillo."
            ],
            "detail": "La capa de cera natural de su tronco protegía históricamente a la planta de la radiación ultravioleta y el exceso de humedad, aunque hoy está estrictamente protegida de cualquier explotación comercial."
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
            "flora_ecosystems.subparamo_transition",
            "flora_ecosystems.encenillos_weinmannia"
        ],
        "tags": ["palma de cera", "ceroxylon quindiuense", "arbol nacional", "bosque de niebla", "amortiguacion"]
    },
    {
        "id": "flora_ecosystems.chite_hypericum",
        "label": "arbusto chite de flores amarillas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el arbusto chite en el páramo",
            "arbusto de flores amarillas chite o romerito",
            "hypericum laricifolium en los nevados",
            "que son esos matorrales con flores amarillas",
            "venga qué planta es ese chite tan comun en el camino",
            "oiga por que hay tantos arbustos amarillos en el subpáramo",
            "velillo o chite de paramo hypericum",
            "usos tradicionales y ecologia del chite",
            "arbustos densos del subparamo y paramo bajo",
            "caracteristicas de hypericum en la alta montana",
            "what is the chite shrub with yellow flowers in the paramo",
            "Hypericum laricifolium bush in Los Nevados",
            "matorral de chite en el parque nacional",
            "planta con florecitas amarillas y hojas pequenas"
        ],
        "hard_negatives": [
            "cuál es el estado de las vías hacia el parque",
            "qué calzado se recomienda para caminar en barro",
            "dónde almorzar cerca de la entrada Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El chite o romerito de páramo (Hypericum laricifolium) es uno de los arbustos más comunes y vistosos del subpáramo y páramo bajo en Los Nevados. Se reconoce por sus hojas diminutas parecidas a agujas de pino y sus llamativas flores amarillas de cinco pétalos.",
            "variants": [
                "Perteneciente al género Hypericum, el chite forma matorrales tupidos entre 3.200 y 3.800 metros de altitud. Sus flores doradas alegran las laderas y proporcionan polen a insectos andinos adaptados al clima frío."
            ],
            "detail": "Sus ramas densas y compactas ayudan a estabilizar laderas empinadas y protegen el suelo contra la erosión causada por lluvias torrenciales."
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
            "flora_ecosystems.romeros_diplostephium",
            "flora_ecosystems.chusque_bamboo_paramo"
        ],
        "tags": ["chite", "hypericum laricifolium", "flores amarillas", "arbustos", "subparamo"]
    },
    {
        "id": "flora_ecosystems.romeros_diplostephium",
        "label": "romeros de páramo diplostephium",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los romeros de páramo",
            "arbustos romero diplostephium en los nevados",
            "romerillo de paramo caracteristicas",
            "que plantas leñosas crecen junto a los frailejones",
            "venga cuál es ese romero silvestre de monte",
            "oiga por que le dicen romero si no huele a romero de cocina",
            "especies del genero diplostephium en el parque",
            "arbustos con hojas plateadas por debajo en el paramo",
            "flora leñosa de alta montana en colombia",
            "romeros nativos de la cordillera central",
            "what are the paramo rosemary shrubs Diplostephium",
            "woody shrubs growing alongside frailejones in Los Nevados",
            "diplostephium en el ecosistema de paramo",
            "arbusto de hojas duras y flores blancas o lilas"
        ],
        "hard_negatives": [
            "se puede usar romero de páramo para cocinar en el campamento",
            "cuántos días dura la travesía completa del parque",
            "qué hacer si sufro síntomas de hipotermia"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los romeros de páramo (Diplostephium spp.) son arbustos nativos con hojas duras y coriáceas cubiertas de pelos blanquecinos en el envés. Aunque su nombre recuerda al romero europeo de cocina por la forma alargada de sus hojas, pertenecen a la familia de las margaritas andinas y no son aromáticos culinarios.",
            "variants": [
                "El género Diplostephium reúne arbustos leñosos típicos del páramo de Los Nevados, capaces de soportar vientos helados gracias a sus hojas gruesas con reverso afelpado. Producen pequeñas flores blancas o moradas que alimentan mariposas y escarabajos de altura."
            ],
            "detail": "Su follaje coriáceo cuenta con una capa cerosa que reduce la evaporación durante las mañanas soleadas de páramo."
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
            "flora_ecosystems.chite_hypericum",
            "flora_ecosystems.adaptation_thick_cuticle_waxes"
        ],
        "tags": ["diplostephium", "romero de paramo", "arbustos", "hojas coriaceas", "margaritas andinas"]
    },
    {
        "id": "flora_ecosystems.chusque_bamboo_paramo",
        "label": "chusque y bambúes de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el chusque en el páramo",
            "bambues de alta montana en los nevados",
            "chusquea tessellata en el parque los nevados",
            "carrizo o chusque de paramo caracteristicas",
            "venga que son esas varitas verdes como bambu enano",
            "oiga por que hay tantos matorrales de chusque en el camino",
            "chuscales de alta montaña en caldas y tolima",
            "graminea leñosa chusquea en los andes",
            "importancia ecologica de los chuscales",
            "chusque refugio de animales en el bosque y paramo",
            "what is the chusque highland bamboo in Los Nevados",
            "Chusquea tessellata native dwarf bamboo of the paramo",
            "los chusques de paramo son bambues",
            "densos matorrales de carrizo en la montana"
        ],
        "hard_negatives": [
            "se pueden cortar varas de chusque para bastón de caminata",
            "dónde alquilar bastones de trekking en Manizales",
            "qué mamíferos se alimentan del chusque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El chusque de páramo (Chusquea tessellata) es un bambú nativo de tallos sólidos y porte erecto que forma densos matorrales en el subpáramo y páramo húmedo. Sus tallos flexibles amortiguan los vientos de cordillera, amarran el suelo y ofrecen un refugio seguro a aves y pequeños mamíferos.",
            "variants": [
                "Chusquea tessellata es la especie de bambú más resistente al frío en Los Nevados, adaptada a vivir entre 3.200 y 3.900 metros de altitud. Forma rodales impenetrables conocidos como chuscales que retienen humedad y previenen deslizamientos de tierra."
            ],
            "detail": "Recuerda que está prohibido cortar varas de chusque para usarlas como bastones de senderismo; debes llevar tus propios bastones técnicos de trekking."
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
            "flora_ecosystems.pajonales_calamagrostis",
            "flora_ecosystems.pajonal_microclimate_shelter"
        ],
        "tags": ["chusque", "chusquea tessellata", "bambu de paramo", "chuscales", "gramineas leñosas"]
    },
    {
        "id": "flora_ecosystems.senecio_and_arnicas",
        "label": "árnicas y senecios de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son las árnicas de páramo",
            "senecios y arnica en el parque los nevados",
            "senecio niveoaureus arnica de montana",
            "margaritas amarillas y lanudas en el paramo",
            "venga que planta es esa con hojas blancas y flor dorada",
            "oiga por que le dicen árnica si es una planta silvestre",
            "compuestas del genero senecio en alta montaña",
            "propiedades tradicionales del senecio de paramo",
            "plantas lanosas amarillas cerca a la nieve",
            "senecios adaptados al suelo volcanico",
            "what are the paramo arnica and Senecio plants",
            "yellow composite flowers of Senecio in Los Nevados",
            "senecios del superparamo y paramo alto",
            "la arnica de paramo se puede recolectar"
        ],
        "hard_negatives": [
            "se pueden recolectar plantas medicinales en el parque",
            "qué botiquín de primeros auxilios debo llevar",
            "dónde queda la farmacia más cercana a Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las llamadas 'árnicas de páramo' son hierbas del género Senecio, como Senecio niveoaureus y Senecio canescens, reconocidas por sus densos pelos blancos y brillantes flores amarillas. Aunque en la medicina popular campesina se usaron contra golpes, en el parque están totalmente protegidas y no se pueden recolectar.",
            "variants": [
                "Los senecios de Los Nevados exhiben un denso manto lanudo que les da un tono plateado o dorado bajo el sol andino. Esta pubescencia los aísla de las heladas y refleja la intensa radiación ultravioleta de las alturas."
            ],
            "detail": "Pertenecen a la misma familia botánica que los frailejones (Asteráceas), compartiendo inflorescencias en capítulo compuestas por decenas de diminutas flores tubulares y liguladas."
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
            "flora_ecosystems.senecio_isabelis_endemic",
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.adaptation_leaf_pubescence"
        ],
        "tags": ["senecio", "arnica de paramo", "senecio niveoaureus", "asteraceas", "flores amarillas"]
    },
    {
        "id": "flora_ecosystems.senecio_isabelis_endemic",
        "label": "especie endémica senecio isabelis",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la planta Senecio isabelis",
            "margarita endemica del nevado santa isabel",
            "senecio isabelis flor del volcan santa isabel",
            "plantas unicas del sector santa isabel",
            "venga qué planta solo vive en el nevado santa isabel",
            "oiga que margarita endemica crece en las morrenas",
            "especie botanica senecio isabelis en los nevados",
            "flora exclusiva de la cordillera central colombiana",
            "senecio de alta montaña en suelo morrenico",
            "plantas pioneras del glaciar santa isabel",
            "what is Senecio isabelis endemic flower",
            "endemic plant species growing on Santa Isabel volcano",
            "flora endemica de los nevados de colombia",
            "senecio isabelis adaptacion al frio glaciar"
        ],
        "hard_negatives": [
            "cómo llegar al sendero Conejeras en Santa Isabel",
            "cuántas horas toma subir al glaciar Santa Isabel",
            "cuál es el estado de apertura del sector Santa Isabel"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Senecio isabelis es una planta endémica de alta montaña descrita originalmente en los alrededores del volcán Nevado Santa Isabel. Esta singular compuesta crece pegada al suelo pedregoso y morrénico, soportando vientos huracanados y temperaturas gélidas al borde del superpáramo.",
            "variants": [
                "Bautizada en honor al Nevado Santa Isabel, Senecio isabelis representa una de las joyas botánicas más escasas y especializadas del parque. Su porte arrosetado y piloso le permite colonizar sustratos volcánicos donde pocas especies logran arraigar."
            ],
            "detail": "Su distribución restringida a la alta montaña de la cordillera Central la hace especialmente vulnerable a las alteraciones térmicas por el cambio climático global."
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
            "flora_ecosystems.senecio_and_arnicas",
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.santa_isabel_glacier_extinction"
        ],
        "tags": ["senecio isabelis", "endemismo", "santa isabel", "superparamo", "morrenas"]
    },
    {
        "id": "flora_ecosystems.encenillos_weinmannia",
        "label": "árboles encenillos del bosque altoandino",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los encenillos en el parque",
            "arbol encenillo weinmannia rollottii",
            "bosques de encenillo en los nevados",
            "arboles dominantes del bosque altoandino",
            "venga cómo es el arbol encenillo que tanto nombran",
            "oiga por que son importantes los encenillos para el agua",
            "especies de weinmannia en la cordillera central",
            "hojas y corteza del encenillo de montana",
            "arboles nativos en las laderas bajas del parque",
            "encenillal de niebla en caldas y risaralda",
            "what are encenillo trees Weinmannia in the high forest",
            "cloud forest encenillo species in Los Nevados",
            "madera y conservacion del encenillo andino",
            "papel ecologico del encenillo en la captacion de niebla"
        ],
        "hard_negatives": [
            "dónde comprar artesanías de madera en Pereira",
            "qué tipo de calzado necesito para no resbalar",
            "a qué hora cierran el centro de visitantes"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los encenillos (especies del género Weinmannia, como Weinmannia rollottii) son los árboles más característicos y dominantes del bosque altoandino en Los Nevados. Sus copas frondosas y ramas cargadas de musgo interceptan la niebla constante, actuando como un primer filtro hidrológico antes del páramo.",
            "variants": [
                "Entre 2.800 y 3.400 metros de altitud cruzas bosques dominados por encenillos, árboles de hojas compuestas y pequeñas espigas florales. Son pilares para la fauna del bosque nublado y protegen los nacimientos de agua de la cordillera."
            ],
            "detail": "La corteza del encenillo es rica en taninos, lo que históricamente motivó su tala para curtiembres antes de la creación y protección estricta del Parque Nacional en 1974."
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
            "flora_ecosystems.aliso_alnus_acuminata",
            "flora_ecosystems.epiphytic_mosses_cloud_forest"
        ],
        "tags": ["encenillo", "weinmannia", "bosque altoandino", "arbol nativo", "captacion de niebla"]
    },
    {
        "id": "flora_ecosystems.aliso_alnus_acuminata",
        "label": "árbol aliso de ribera montañosa",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el aliso en el bosque andino",
            "arbol aliso alnus acuminata en los nevados",
            "arboles pioneros de riberas y quebradas",
            "por que el aliso fija nitrogeno en el suelo",
            "venga que arbol es ese de hojas dentadas junto al rio",
            "oiga por que siembran alisos para restaurar la montana",
            "aliso andino recuperacion de suelos",
            "arbol de crecimiento rapido en el bosque nublado",
            "especie nativa alnus acuminata en caldas",
            "bosques de aliso en las cuencas del parque",
            "what is the Andean alder tree Alnus acuminata",
            "alder trees in riparian mountain forests of Los Nevados",
            "fijacion de nitrogeno por alisos nativos",
            "el aliso como arbol protector de cuencas hidricas"
        ],
        "hard_negatives": [
            "se puede pescar trucha en las quebradas del parque",
            "dónde contratar guía para la cuenca del Otún",
            "cuántos días toma caminar hasta la Laguna del Otún"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El aliso (Alnus acuminata) es un árbol andino de rápido crecimiento que coloniza orillas de ríos, quebradas y taludes en el bosque altoandino del parque. Gracias a bacterias simbiontes en sus raíces, fija nitrógeno atmosférico enriqueciendo suelos volcánicos pobres y acelerando la recuperación del bosque.",
            "variants": [
                "Alnus acuminata es indispensable para proteger las riberas montañosas contra desmoronamientos de tierra. Sus raíces forman nódulos que nutren el suelo, facilitando que otras especies nativas se establezcan con éxito."
            ],
            "detail": "Por su capacidad de colonizar terrenos perturbados y estabilizar márgenes de agua, es una de las especies prioritarias en proyectos de restauración ecológica en el Eje Cafetero."
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
            "flora_ecosystems.encenillos_weinmannia",
            "flora_ecosystems.ecological_restoration_programs"
        ],
        "tags": ["aliso", "alnus acuminata", "riberas", "fijacion de nitrogeno", "restauracion forestal"]
    },
    {
        "id": "flora_ecosystems.pino_romeron_podocarpus",
        "label": "pino romerón y coníferas nativas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay coníferas nativas en el parque Los Nevados",
            "que es el pino romeron",
            "arbol retrophyllum rospigliosii o podocarpus",
            "pinos autoctonos de colombia en el bosque de niebla",
            "venga es verdad que colombia tiene sus propios pinos nativos",
            "oiga ese pino que se ve es sembrado o es nativo",
            "coniferas andinas protegidas en los nevados",
            "pino chaquiro o pino romeron en caldas y tolima",
            "diferencia entre pinos nativos y pinos sembrados",
            "arboles de podocarpaceas en el parque nacional",
            "are there native conifers like pino romeron in Los Nevados",
            "native Podocarpus and Retrophyllum trees in Colombia",
            "el pino romeron esta en peligro de extincion",
            "coniferas de alta montana en la cordillera central"
        ],
        "hard_negatives": [
            "está permitido recolectar piñas de pino en el parque",
            "qué equipo para camping debo empacar",
            "dónde queda el santuario de flora y fauna Otún Quimbaya"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Sí, Colombia cuenta con coníferas nativas de la familia de las podocarpáceas, destacando el pino romerón (Retrophyllum rospigliosii y especies de Podocarpus). Crecen en los bosques altoandinos del parque y se diferencian de los pinos comerciales introducidos porque no tienen acículas en racimo ni acidifican agresivamente el suelo.",
            "variants": [
                "En los cañones boscosos de Los Nevados sobreviven ejemplares de pino romerón, coníferas nativas de hojas planas y copa elegante. Son árboles protegidos de gran valor biológico cuyas semillas alimentan aves y pequeños roedores de montaña."
            ],
            "detail": "Estas coníferas autóctonas sufrieron intensa explotación maderera en el siglo XX, por lo que las poblaciones remanentes dentro del parque son objeto de especial conservación."
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
            "flora_ecosystems.pine_eucalyptus_plantations_impact",
            "flora_ecosystems.encenillos_weinmannia"
        ],
        "tags": ["pino romeron", "coniferas nativas", "retrophyllum", "podocarpus", "bosque altoandino"]
    },
    {
        "id": "flora_ecosystems.canelo_de_paramo_drimys",
        "label": "canelo de páramo de hoja perenne",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el canelo de páramo",
            "arbol drimys granadensis en los nevados",
            "canelo andino caracteristicas y aroma",
            "arbol de hojas verdes y flores blancas en el subparamo",
            "venga que arbol es ese que tiene corteza aromatica a pimienta",
            "oiga por que le dicen canelo de páramo a esa planta",
            "especie drimys granadensis de la familia winteraceae",
            "arbol antiguo y primitivo en la alta montana",
            "canelo silvestre en el ecotono del parque",
            "usos tradicionales del canelo de paramo",
            "what is the Drimys granadensis mountain cinnamon tree",
            "native highland evergreen tree Drimys in Los Nevados",
            "hojas perennes y aromáticas del canelo andino",
            "arbol con flor blanca estrellada en el bosque altoandino"
        ],
        "hard_negatives": [
            "se puede arrancar corteza de canelo para aromática",
            "cuál es el precio de la entrada para estudiantes",
            "qué hacer si llueve torrencialmente en el sendero"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El canelo de páramo (Drimys granadensis) es un árbol nativo perennifolio del bosque altoandino y subpáramo, conocido por sus hojas de envés verdeazulado y su corteza picante y aromática. Pertenece a una de las familias botánicas más antiguas del planeta (Winteráceas) y produce delicadas flores blancas estrelladas.",
            "variants": [
                "Drimys granadensis habita entre 2.800 y 3.600 metros de altitud en Los Nevados. Sus hojas brillantes despiden un aroma especiado similar a la canela y la pimienta, una defensa química natural contra herbívoros del clima frío."
            ],
            "detail": "Botánicamente es un fósil viviente, ya que sus tejidos conductores de savia carecen de vasos perforados modernos, conservando traqueidas primitivas similares a las coníferas."
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
            "flora_ecosystems.subparamo_transition",
            "flora_ecosystems.adaptation_thick_cuticle_waxes"
        ],
        "tags": ["canelo de paramo", "drimys granadensis", "arbol primitivo", "corteza aromatica", "flores blancas"]
    },
    {
        "id": "flora_ecosystems.pajonales_calamagrostis",
        "label": "pajonales de páramo calamagrostis",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los pajonales de páramo",
            "paja brava calamagrostis effusa en los nevados",
            "pastos amarillos del parque nacional los nevados",
            "que pasto es ese que cubre todo el paramo",
            "venga como se llama esa paja alta que corta las manos",
            "oiga por que el paisaje del páramo se ve como un pastizal dorado",
            "gramineas nativas del genero calamagrostis",
            "calamagrostis y festuca en la alta montaña",
            "pastos duros de paramo adaptacion",
            "extension de los pajonales en los nevados",
            "what are the Calamagrostis paramo tussock grasslands",
            "tussock grass species covering the park landscape",
            "paja de paramo y su funcion ecologica",
            "los pastizales de alta montana en colombia"
        ],
        "hard_negatives": [
            "se puede alimentar a los caballos con paja del parque",
            "cuántos grados bajo cero hace en la noche",
            "se permite acampar sobre el pastizal"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los pajonales son extensos pastizales dominados por gramíneas en macolla, principalmente la paja de páramo (Calamagrostis effusa). Cubren miles de hectáreas entre 3.600 y 4.300 metros, dando al páramo su característico color pajizo y dorado bajo la luz andina.",
            "variants": [
                "Calamagrostis effusa crece en manojos apretados o macollas de hojas largas y silíceas muy resistentes al viento. Junto a los frailejones, los pajonales forman la matriz vegetal principal que protege los suelos paramunos de la erosión."
            ],
            "detail": "Sus bordes son cortantes debido a microcristales de sílice, una defensa natural que evita que herbívoros silvestres o domésticos las devoren con facilidad."
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
            "flora_ecosystems.pajonal_microclimate_shelter",
            "flora_ecosystems.frailejones_overview"
        ],
        "tags": ["pajonales", "calamagrostis effusa", "paja de paramo", "macollas", "gramineas"]
    },
    {
        "id": "flora_ecosystems.pajonal_microclimate_shelter",
        "label": "refugio biológico en los pajonales",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué animales se refugian en los pajonales",
            "microclima dentro de las macollas de paja",
            "por que los pajonales son importantes para la fauna",
            "como abrigan las macollas de pasto del frío",
            "venga es verdad que debajo de la paja hace menos frío",
            "oiga qué bichos y aves viven metidos en el pajonal",
            "refugio termico de calamagrostis effusa",
            "anidacion de aves en la base de los pajonales",
            "humedad y temperatura dentro del pastizal paramuno",
            "nidos y madrigueras en el pajonal de los nevados",
            "how do tussock grass bunches provide microclimate shelter",
            "wildlife refuge inside paramo tussock grasslands",
            "la base del pajonal como trampa de calor",
            "roedores e insectos que viven entre la paja"
        ],
        "hard_negatives": [
            "dónde ver venados de cola blanca en el parque",
            "qué hacer si me muerde una serpiente en la montaña",
            "cuáles son los senderos para avistamiento de aves"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La base tupida de las macollas de pajonal crea un microclima estable donde la temperatura puede ser de 5 a 10 °C más cálida que el aire exterior durante las heladas nocturnas. Este colchón térmico sirve de refugio vital para roedores, ranitas de páramo, escarabajos y nidos de aves andinas.",
            "variants": [
                "Los manojos densos de Calamagrostis actúan como aislantes contra el viento y la escarcha. En su interior resguardado proliferan plántulas de otras especies y fauna pequeña que no sobreviviría a la intemperie nocturna del páramo."
            ],
            "detail": "Aves como el chamicero de páramo o el cucarachero construyen sus nidos profundamente encajados en la base de estas macollas para proteger sus huevos del congelamiento."
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
            "flora_ecosystems.pajonales_calamagrostis",
            "flora_ecosystems.paramo_ecosystem",
            "flora_ecosystems.adaptation_dwarfism_prostrate"
        ],
        "tags": ["refugio biologico", "microclima", "macollas", "aislamiento termico", "fauna y flora"]
    }
]
