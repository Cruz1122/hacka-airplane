# -*- coding: utf-8 -*-
"""
Entries group 4: Topics 55 to 72
Wetlands, Ramsar site Laguna del Otún, peatlands, lakes, glaciers,
glacier retreat, moraines, cryoturbation, and water basin supply.
"""

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
IDEAM_URL = "http://www.ideam.gov.co/web/ecosistemas/glaciares-colombia"
RAMSAR_URL = "https://rsis.ramsar.org/ris/1781"
HUMBOLDT_URL = "http://www.humboldt.org.co/es/investigacion/proyectos/actuales/item/222-paramos-de-colombia"
DATE_VERIFIED = "2026-11-21"

ENTRIES = [
    {
        "id": "flora_ecosystems.high_andean_wetlands",
        "label": "humedales altoandinos y turberas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los humedales altoandinos",
            "humedales y lagunas en el parque los nevados",
            "cuales humedales hay en los nevados",
            "turberas pantanos y lagunas de alta montana",
            "venga qué tipo de humedales protegen en el parque",
            "oiga por que son tan importantes los charcos y lagunas de arriba",
            "complejo de humedales en caldas risaralda y tolima",
            "funciones ecologicas de los humedales de paramo",
            "que plantas y musgos viven en los humedales",
            "los humedales como reserva hidrica estrategica",
            "what are high Andean wetlands in Los Nevados",
            "alpine wetlands peatlands and glacial lakes in Colombia",
            "red de humedales en el parque nacional",
            "importancia de las turberas y bofedales para el agua"
        ],
        "hard_negatives": [
            "se puede nadar o bañarse en las lagunas del parque",
            "dónde alquilar botes o kayaks en la Laguna del Otún",
            "qué patos habitan las lagunas altoandinas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los humedales altoandinos de Los Nevados comprenden un mosaico interconectado de lagunas glaciares, turberas, pantanos y bofedales de cojines de agua ubicados sobre los 3.300 metros. Cumplen una función vital regulando el caudal de los ríos, reteniendo sedimentos y albergando flora y fauna únicas.",
            "variants": [
                "En el parque, los humedales de montaña actúan como inmensos amortiguadores que retienen excesos de lluvia y liberan agua pura gradualmente. Su red de turberas y lagunillas sostiene el abastecimiento de agua potable de millones de habitantes del Eje Cafetero y Tolima."
            ],
            "detail": "Muchos de estos cuerpos de agua se formaron por el deshielo milenario de los glaciares cuaternarios que esculpieron los valles en forma de 'U' de la cordillera."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Convención Ramsar",
                "url": RAMSAR_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.ramsar_otun_wetland_complex",
            "flora_ecosystems.turberas_bogs_peatlands",
            "flora_ecosystems.water_cycle_basin_supply"
        ],
        "tags": ["humedales", "turberas", "lagunas", "regulacion hidrica", "alta montana"]
    },
    {
        "id": "flora_ecosystems.ramsar_otun_wetland_complex",
        "label": "sitio ramsar laguna del otun",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el sitio Ramsar de la Laguna del Otún",
            "complejo de humedales laguna del otun ramsar",
            "por que la laguna del otun es un humedal ramsar",
            "cuando declararon ramsar la laguna del otun",
            "venga qué significa que la laguna del otún sea sitio ramsar",
            "oiga qué importancia internacional tiene el humedal del otún",
            "declaratoria ramsar 1781 en los nevados de colombia",
            "area protegida ramsar laguna del otun hectareas",
            "biodiversidad y conservacion del complejo otun",
            "humedal de importancia internacional en risaralda",
            "what is the Laguna del Otun Ramsar wetland complex",
            "Ramsar site 1781 in Los Nevados national park",
            "cuales lagunas componen el sitio ramsar del otun",
            "proteccion internacional de humedales en los nevados"
        ],
        "hard_negatives": [
            "cómo llegar en carro particular a la Laguna del Otún",
            "cuál es la tarifa de ingreso al sector Otún",
            "se puede pescar trucha arcoíris en la Laguna del Otún"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El Complejo de Humedales de la Laguna del Otún fue designado como Sitio Ramsar N.º 1781 el 25 de junio de 2008, abarcando inicialmente 6.579 hectáreas dentro del parque. Es un reconocimiento internacional a su valor excepcional como reserva hídrica y refugio de aves acuáticas amenazadas de los Andes.",
            "variants": [
                "La declaratoria Ramsar de 2008 certifica a la Laguna del Otún y sus humedales aledaños como un ecosistema de importancia planetaria. Protege la naciente del río Otún, que abastece a más de 500.000 habitantes en Pereira y Dosquebradas."
            ],
            "detail": "El complejo incluye además de la laguna principal cuerpos lénticos como El Silencio, La Leona, El Bosque y extensos bofedales de almohadillas."
        },
        "sources": [
            {
                "label": "Convención Ramsar",
                "url": RAMSAR_URL,
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
            "flora_ecosystems.high_andean_wetlands",
            "flora_ecosystems.laguna_del_otun_ecosystem",
            "flora_ecosystems.rio_otun_basin_water"
        ],
        "tags": ["sitio ramsar", "laguna del otun", "humedal internacional", "ramsar 1781", "pereira"]
    },
    {
        "id": "flora_ecosystems.turberas_bogs_peatlands",
        "label": "formación y función de turberas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo se forman las turberas en el páramo",
            "que es una turbera altoandina",
            "como funciona una turbera en los nevados",
            "por que las turberas guardan tanta agua y carbono",
            "venga qué es esa tierra negra y blanda en los valles del páramo",
            "oiga por que no se pudren los musgos en las turberas",
            "acumulacion de turba en el parque nacional",
            "bofedales y turberas de esfagno en caldas",
            "cuantos anos tarda en formarse un metro de turba",
            "el papel de las turberas contra el calentamiento global",
            "how do peatlands and bogs form in the paramo",
            "ecological function of high altitude peat bogs in Colombia",
            "suelo histosol saturado de agua en los nevados",
            "turberas como gigantescos filtros de agua natural"
        ],
        "hard_negatives": [
            "se puede extraer turba para abono de plantas",
            "cuántos refugios de alta montaña hay para montañistas",
            "dónde reportar un rescate de emergencia en el parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las turberas se forman en depresiones mal drenadas donde el agua helada y la escasez de oxígeno impiden que los restos de musgos (Sphagnum) y plantas de cojín se descompongan por completo. A lo largo de milenios, esa materia orgánica acumulada forma capas de turba que actúan como colosales esponjas de agua y sumideros de carbono.",
            "variants": [
                "En los valles glaciares de Los Nevados, las turberas acumulan materia vegetal sin pudrirse debido al pH ácido y la anoxia. Un solo metro de profundidad de turba puede tardar hasta 1.000 años en formarse, convirtiéndolas en archivos climáticos insustituibles."
            ],
            "detail": "Cuando una turbera se drena o se pisotea, entra oxígeno y la turba se descompone velozmente, liberando a la atmósfera dióxido de carbono almacenado durante milenios."
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
            "flora_ecosystems.sphagnum_moss_peat",
            "flora_ecosystems.distichia_cushion_bog",
            "flora_ecosystems.paramo_carbon_sequestration"
        ],
        "tags": ["turberas", "turba", "sphagnum", "anoxia", "sumidero de carbono"]
    },
    {
        "id": "flora_ecosystems.laguna_del_otun_ecosystem",
        "label": "ecosistema acuático de laguna otun",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo es el ecosistema de la Laguna del Otún",
            "vida acuatica en la laguna del otun",
            "vegetacion alrededor de la laguna del otun",
            "que profundidad tiene la laguna del otun",
            "venga que plantas crecen en la orilla de la laguna del otún",
            "oiga por que el agua de la laguna del otun es tan fria y transparente",
            "cuerpo de agua lentico en el parque los nevados",
            "fauna y flora acuatica de la laguna del otun",
            "nacimiento del rio otun en la laguna",
            "temperatura del agua en la laguna del otun",
            "what is the aquatic ecosystem of Laguna del Otun",
            "ecology and vegetation around Laguna del Otun in Los Nevados",
            "espejo de agua de la laguna del otun a 3900 metros",
            "flora palustre y algas en la laguna del otun"
        ],
        "hard_negatives": [
            "se puede navegar en kayak en la Laguna del Otún",
            "cuántas horas de caminata hay desde El Cedral hasta la laguna",
            "dónde acampar en el sector de la Laguna del Otún"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La Laguna del Otún es el mayor cuerpo de agua del parque, situada a unos 3.900 metros de altitud y alimentada históricamente por deshielos del Nevado Santa Isabel y ríos paramunos. Sus aguas frías y cristalinas están rodeadas de cojines de Plantago rigida, frailejones y pastizales que protegen la naciente del río Otún.",
            "variants": [
                "Con un espejo de agua de aproximadamente 1,5 km² y profundidades de hasta 70 metros, la Laguna del Otún es un ecosistema léntico oligotrófico de baja temperatura. En sus orillas crecen briófitos y macrófitas adaptadas a aguas de deshielo ricas en oxígeno."
            ],
            "detail": "Es el hábitat de descanso y alimentación de aves acuáticas altoandinas como el pato andino (Oxyura ferruginea) y la focha americana."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Convención Ramsar",
                "url": RAMSAR_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.ramsar_otun_wetland_complex",
            "flora_ecosystems.lagunas_glaciares_origen",
            "flora_ecosystems.rio_otun_basin_water"
        ],
        "tags": ["laguna del otun", "ecosistema acuatico", "naciente", "rio otun", "lago oligotrofico"]
    },
    {
        "id": "flora_ecosystems.lagunas_glaciares_origen",
        "label": "origen glaciar de lagunas paramunas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo se originaron las lagunas de Los Nevados",
            "origen glaciar de las lagunas del parque",
            "por que hay tantas lagunas en la alta cordillera",
            "cubetas glaciares y morrenas represando agua",
            "venga quién formó esas lagunas tan hondas en la montaña",
            "oiga por que las lagunas tienen esa forma ovalada entre las rocas",
            "geologia y ecologia de las lagunas de alta montana",
            "lagunas glaciarias cuaternarias en colombia",
            "como el retroceso del hielo dejo lagunas en los nevados",
            "formacion de lagos por morrenas frontales",
            "how did the glacial lakes of Los Nevados form",
            "origin of alpine lakes carved by ancient glaciers in Colombia",
            "lagunas de origen glaciar en caldas y tolima",
            "erosion glaciar y represamiento natural de lagunas"
        ],
        "hard_negatives": [
            "cuántos metros sobre el nivel del mar está la Laguna del Encanto",
            "cuál es el pico más alto de la cordillera Central",
            "qué ropa térmica impermeable debo llevar"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las lagunas del parque se originaron durante las últimas glaciaciones, cuando inmensas masas de hielo excavaron cubetas profundas en la roca volcánica. Al retirarse los glaciares hace unos 10.000 años, las morrenas de piedra represaron el agua de deshielo y lluvia, creando estos emblemáticos espejos de agua.",
            "variants": [
                "Cuerpos de agua como Otún, Verde y lagunillas menores ocupan depresiones talladas por la erosión glaciar del Pleistoceno. Están represadas por diques naturales de morrenas o flujos de lava que retienen el agua de cordillera."
            ],
            "detail": "Estas cubetas glaciares tienen fondos de roca pulida y estrías visibles en sus bordes que atestiguan el paso de lenguas de hielo milenarias."
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
            "flora_ecosystems.laguna_del_otun_ecosystem",
            "flora_ecosystems.laguna_verde_ecosystem",
            "flora_ecosystems.moraines_primary_succession"
        ],
        "tags": ["origen glaciar", "cubetas", "morrenas", "lagunas", "glaciaciones"]
    },
    {
        "id": "flora_ecosystems.laguna_verde_ecosystem",
        "label": "laguna verde y lagunas volcánicas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la Laguna Verde en el parque",
            "por que la laguna verde tiene ese color esmeralda",
            "laguna verde en los nevados ecosistema",
            "minerales volcanicos y color del agua en lagunas",
            "venga por que se ve verde el agua de esa laguna alta",
            "oiga en la laguna verde hay peces o plantas",
            "lagunas volcanicas del sector cisne y santa isabel",
            "azufre y minerales disueltos en lagunas de altura",
            "ecologia extrema de la laguna verde en caldas",
            "espejo de agua esmeralda en el parque nacional",
            "what is Laguna Verde in Los Nevados national park",
            "why is the water emerald green in Laguna Verde Colombia",
            "origen y minerales de la laguna verde del nevado",
            "color verde esmeralda por azufre y sedimentos finos"
        ],
        "hard_negatives": [
            "se puede entrar al sendero de Laguna Verde hoy",
            "cuántos kilómetros hay desde el parador El Cisne",
            "cuál es el precio de la entrada al sector Cisne"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Laguna Verde destaca por su intenso color esmeralda, producido por la suspensión de minerales volcánicos muy finos (harina de roca) y compuestos de azufre arrastrados desde las laderas volcánicas. Su entorno es pedregoso y frío, albergando algas microscópicas extremófilas adaptadas a aguas ácidas y gélidas.",
            "variants": [
                "El tono verde brillante de esta laguna se debe a la dispersión de la luz solar en las micropartículas minerales y sedimentos glaciovolcánicos en suspensión. Su baja temperatura y acidez limitan la vegetación en sus orillas a líquenes y musgos pioneros."
            ],
            "detail": "Debido a su fragilidad ecosistémica y a su proximidad a zonas de riesgo volcánico, el acceso a sus orillas está estrictamente regulado por Parques Nacionales."
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
            "flora_ecosystems.lagunas_glaciares_origen",
            "flora_ecosystems.microorganisms_extreme_lakes",
            "flora_ecosystems.superparamo_ecosystem"
        ],
        "tags": ["laguna verde", "minerales volcanicos", "color esmeralda", "aguas frias", "extremofilas"]
    },
    {
        "id": "flora_ecosystems.cushion_bogs_damage_trampling",
        "label": "daño por pisar los cojines",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué está prohibido pisar los cojines de agua",
            "que pasa si piso los colchones de agua",
            "dano del pisoteo en las turberas de paramo",
            "es malo caminar sobre las almohadillas de plantago",
            "venga por que el guia no nos deja pisar esos tapetes verdes",
            "oiga por que se hunde el pie y se drena el agua si piso un cojín",
            "impacto del senderismo no regulado en humedales",
            "compactacion del suelo en turberas por turistas",
            "cuanto tarda en recuperarse un cojin de agua pisoteado",
            "por que debemos quedarnos en la pasarela o sendero",
            "why is stepping on cushion bogs forbidden in the park",
            "trampling damage to fragile alpine cushion wetlands",
            "destruccion de almohadillas hidricas por pisadas",
            "los cojines de agua tardan decadas en crecer"
        ],
        "hard_negatives": [
            "cuáles son las multas ambientales en el parque",
            "dónde comprar botas pantaneras antes de subir",
            "se puede cruzar a caballo por las turberas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Pisar los cojines de agua compacta sus diminutos tallos entrelazados y abre grietas por donde el agua acumulada se drena rápidamente, secando la turbera. Como estas plantas apenas crecen unos pocos milímetros al año, una sola pisada puede destruir décadas de formación vegetal.",
            "variants": [
                "Al caminar sobre las almohadillas rompes la estructura que retiene el agua subterránea. El pisoteo crea surcos de barro que aceleran la erosión y destruyen la capacidad de filtración del humedal, por lo que debes transitar exclusivamente por los senderos autorizados."
            ],
            "detail": "En áreas muy transitadas de humedales, Parques Nacionales instala pasarelas elevadas de madera para permitir la contemplación sin alterar el flujo hidrológico."
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
            "flora_ecosystems.cojines_plantago_rigida",
            "flora_ecosystems.distichia_cushion_bog",
            "flora_ecosystems.turberas_bogs_peatlands"
        ],
        "tags": ["dano por pisoteo", "cojines de agua", "compactacion", "conservacion", "senderismo responsable"]
    },
    {
        "id": "flora_ecosystems.aquatic_macrophytes_paramo",
        "label": "plantas acuáticas de lagunas paramunas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué plantas acuáticas viven en las lagunas del páramo",
            "vegetacion sumergida en lagunas de alta montana",
            "isoetes y plantas acuaticas en los nevados",
            "macrofitas de aguas frias en la laguna del otun",
            "venga qué hierbas crecen adentro del agua en el páramo",
            "oiga hay plantas flotantes en las lagunas de montaña",
            "especies del genero isoetes en lagunas andinas",
            "adaptacion de macrofitas a la radiacion y agua helada",
            "flora acuatica sumergida en humedales altoandinos",
            "purificacion del agua por plantas acuaticas nativas",
            "what aquatic macrophytes grow in high paramo lakes",
            "submerged Isoetes and water plants in alpine lakes Colombia",
            "plantas que viven bajo el agua en la laguna del otun",
            "oxigenacion de lagunas por macrofitas de montana"
        ],
        "hard_negatives": [
            "se puede navegar en bote para ver plantas acuáticas",
            "qué peces nativos viven en las lagunas del parque",
            "dónde comprar licencia de pesca deportiva"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En el fondo de lagunas como Otún crecen macrófitas sumergidas especializadas, destacando licopodios acuáticos del género Isoetes y especies de Myriophyllum. Estas plantas toleran temperaturas del agua cercanas a 4 °C, oxigenan el ecosistema lacustre y proporcionan alimento a aves acuáticas.",
            "variants": [
                "Las plantas acuáticas de Los Nevados realizan fotosíntesis en aguas gélidas y con baja concentración de dióxido de carbono disuelto. Isoetes forma pequeños céspedes sumergidos que fijan sedimentos en el lecho rocoso de las lagunas."
            ],
            "detail": "Estas comunidades sumergidas son muy sensibles a la turbidez provocada por ganado o residuos, por lo que su presencia es indicador de excelente calidad hídrica."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Convención Ramsar",
                "url": RAMSAR_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.laguna_del_otun_ecosystem",
            "flora_ecosystems.high_andean_wetlands",
            "flora_ecosystems.microorganisms_extreme_lakes"
        ],
        "tags": ["plantas acuaticas", "macrofitas", "isoetes", "laguna del otun", "oxigenacion"]
    },
    {
        "id": "flora_ecosystems.microorganisms_extreme_lakes",
        "label": "vida microscópica en aguas glaciares",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué microorganismos viven en las lagunas glaciares",
            "vida microscopica en aguas heladas de los nevados",
            "diatomeas y algas extremófilas en alta montana",
            "bacterias que aguantan el frio y azufre del volcan",
            "venga hay microbios vivos en el agua que viene del deshielo",
            "oiga qué tipo de algas microscopicas habitan los nevados",
            "comunidades de diatomeas en lagunas glaciarias",
            "microbiologia de ambientes extremos en el ruiz y santa isabel",
            "fitoplancton de alta montana en el parque nacional",
            "organismos extremófilos en aguas minerales del nevado",
            "what microscopic life lives in glacial lakes of Los Nevados",
            "extremophile algae and diatoms in high Andean alpine waters",
            "diatomeas como bioindicadores del clima pasado",
            "algas unicelulares resistentes a rayos ultravioleta"
        ],
        "hard_negatives": [
            "se puede tomar agua cruda directamente de los arroyos",
            "qué pastillas purificadoras de agua debo comprar",
            "cuántos grados de temperatura tiene el agua de las termales"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las lagunas y arroyos de deshielo en Los Nevados albergan comunidades microscópicas de diatomeas (algas con caparazón de sílice), cianobacterias y bacterias extremófilas. Estos microorganismos sobreviven a radiación UV intensa, bajas concentraciones de nutrientes y aguas cercanas al punto de congelación.",
            "variants": [
                "A pesar del frío extremo, las aguas glaciares hierven de vida microscópica. Las diatomeas son la base de la cadena alimenticia acuática y sus frústulos fosilizados en el lodo permiten a los científicos reconstruir cómo cambió el clima en los últimos miles de años."
            ],
            "detail": "En lagunas con influencia de fumarolas volcánicas se han aislado bacterias que metabolizan azufre, adaptadas a condiciones similares a las de la Tierra primitiva."
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
            "flora_ecosystems.laguna_verde_ecosystem",
            "flora_ecosystems.laguna_del_otun_ecosystem",
            "flora_ecosystems.glaciers_snow_presence"
        ],
        "tags": ["microorganismos", "diatomeas", "extremofilas", "aguas glaciares", "bioindicadores"]
    },
    {
        "id": "flora_ecosystems.glaciers_snow_presence",
        "label": "nieve y glaciares en picos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cuáles volcanes tienen nieve y glaciares",
            "hay nieve en el parque los nevados hoy",
            "que nevados conservan hielo glaciar",
            "cuales picos tienen casquete de hielo",
            "venga todavía queda nieve en el nevado del ruiz",
            "oiga por que algunos dias se ve blanco y otros no",
            "masas glaciares activas en la cordillera central",
            "ruiz santa isabel y tolima tienen glaciar",
            "donde se puede ver nieve perpetua en colombia",
            "diferencia entre nieve caida y hielo glaciar",
            "which peaks have snow and glaciers in Los Nevados",
            "is there permanent glacier ice in the national park",
            "nevados con cobertura de hielo en caldas y tolima",
            "glaciares de montana tropical en colombia"
        ],
        "hard_negatives": [
            "cuánto cuesta el tour para subir al glaciar",
            "se puede esquiar en la nieve de Los Nevados",
            "cuál es la mejor época del año para ver nieve"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El parque conserva glaciares en tres volcanes: el Nevado del Ruiz (aprox. 7,17 km² de hielo en 2024), el Nevado del Tolima (aprox. 0,45 km²) y pequeños relictos en el Nevado Santa Isabel (aprox. 0,16 km²). Lo que alcances a ver en tu visita turística depende de la nubosidad y de los senderos autorizados de cada sector.",
            "variants": [
                "En Los Nevados sobreviven tres masas de hielo: el casquete principal del Ruiz, la cima cónica del Tolima y restos mínimos en Santa Isabel. Recuerda que las nevadas frescas son temporales, mientras que el glaciar es el hielo milenario compactado en la cumbre."
            ],
            "detail": "El Ruiz concentra más del 90 % de su masa sobre los 5.000 metros de altitud, lo que le permite mantenerse como el glaciar más extenso de la cordillera Central colombiana."
        },
        "sources": [
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
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
            "flora_ecosystems.glacier_retreat_climate_change",
            "flora_ecosystems.santa_isabel_glacier_extinction",
            "flora_ecosystems.glaciers_vs_paramo_water_role"
        ],
        "tags": ["glaciares", "nieve", "nevado del ruiz", "nevado del tolima", "santa isabel"]
    },
    {
        "id": "flora_ecosystems.glacier_retreat_climate_change",
        "label": "retroceso glaciar por calentamiento global",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué se están derritiendo los glaciares",
            "retroceso glaciar en el parque los nevados",
            "cuanto hielo han perdido los nevados de colombia",
            "deshielo por cambio climatico en los nevados",
            "venga por que cada ano hay menos nieve en el Ruiz",
            "oiga cuando se van a derretir todos los nevados",
            "monitoreo del ideam sobre deshielo glaciar",
            "tasa anual de perdida de masa glaciar en colombia",
            "desaparicion del hielo en la cordillera central",
            "impacto del calentamiento global en las cumbres nevadas",
            "why are glaciers melting rapidly in Los Nevados",
            "tropical glacier retreat due to climate change in Colombia",
            "perdida de area glaciar en los nevados desde 1850",
            "balance de masa negativo de los glaciares colombianos"
        ],
        "hard_negatives": [
            "cuál es la temperatura del aire hoy en Manizales",
            "cuántos gases emite el cráter Arenas del Ruiz",
            "dónde consultar el mapa de amenazas volcánicas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Según los registros oficiales del IDEAM, Colombia ha perdido más del 90 % de su superficie glaciar desde mediados del siglo XIX debido al calentamiento global. En Los Nevados, los glaciares retroceden a tasas de entre el 3 % y 5 % de su área cada año, reduciendo el espesor de hielo y fragmentando sus cumbres.",
            "variants": [
                "El aumento de las temperaturas medias y eventos meteorológicos extremos como el fenómeno de El Niño aceleran el deshielo de nuestros volcanes. El balance de masa glaciar es deficitario: se derrite mucho más hielo del que las nevadas logran acumular anualmente."
            ],
            "detail": "A nivel nacional solo quedan alrededor de 30 a 31 km² de hielo repartidos en seis masas glaciares, todas ellas en franco y continuo retroceso."
        },
        "sources": [
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.santa_isabel_glacier_extinction",
            "flora_ecosystems.moraines_primary_succession"
        ],
        "tags": ["retroceso glaciar", "calentamiento global", "ideam", "deshielo", "cambio climatico"]
    },
    {
        "id": "flora_ecosystems.santa_isabel_glacier_extinction",
        "label": "deshielo crítico del nevado santa isabel",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cuándo desaparecerá el glaciar del Nevado Santa Isabel",
            "extincion del glaciar poleka kasue",
            "desaparicion del glaciar conejeras en santa isabel",
            "cuanto hielo le queda al nevado santa isabel",
            "venga es verdad que el santa isabel ya no tiene casi nada de nieve",
            "oiga por que se derritió tan rapido el glaciar santa isabel",
            "estado critico del glaciar santa isabel segun ideam",
            "perdida del glaciar del otun y conejeras",
            "fragmentacion del hielo en cumbres del santa isabel",
            "ultimo reporte de area glaciar santa isabel",
            "when will the Santa Isabel volcano glacier disappear",
            "critical melting of Poleka Kasue Santa Isabel glacier",
            "extincion del hielo en poleka kasue colombia",
            "area remanente de hielo en santa isabel menos de un kilometro"
        ],
        "hard_negatives": [
            "cómo llegar a la entrada de Santa Isabel desde Villamaría",
            "cuánto cobran los operadores turísticos por ir a Conejeras",
            "qué hacer si sufro mal de páramo en Santa Isabel"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El Nevado Santa Isabel (Poleka Kasue) es el glaciar más vulnerable y cercano a extinguirse en Colombia: para 2024 apenas conservaba cerca de 0,16 km² de hielo fragmentado en pequeños parches. Históricos sectores de monitoreo como el glaciar Conejeras ya desaparecieron por completo.",
            "variants": [
                "Debido a su menor altitud (alrededor de 4.900 metros) y morfología aplanada de domos, el Santa Isabel ha perdido más del 95 % de su masa helada original. Los glaciólogos del IDEAM proyectan que sus últimos relictos de hielo podrían extinguirse en pocos años."
            ],
            "detail": "El retroceso en Santa Isabel deja al descubierto extensas áreas de morrenas y roca estéril donde los científicos monitorean la llegada de las primeras plantas pioneras."
        },
        "sources": [
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.glacier_retreat_climate_change",
            "flora_ecosystems.moraines_primary_succession"
        ],
        "tags": ["santa isabel", "poleka kasue", "extincion glaciar", "conejeras", "deshielo critico"]
    },
    {
        "id": "flora_ecosystems.moraines_primary_succession",
        "label": "colonización vegetal en morrenas glaciares",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué plantas colonizan el suelo cuando se retira el glaciar",
            "sucesion ecologica primaria en morrenas de los nevados",
            "como nacen las plantas en la tierra que dejo el hielo",
            "colonizacion vegetal post glaciar en santa isabel",
            "venga qué crece primero en las piedras que deja el deshielo",
            "oiga por que hay maticas pequenas entre las rocas morrenicas",
            "etapas de colonizacion de plantas en morrenas recientes",
            "liquenes musgos y hierbas pioneras tras el glaciar",
            "estudios de sucesion vegetal en el parque los nevados",
            "como se forma suelo despues del retroceso del hielo",
            "how do plants colonize terrain left by retreating glaciers",
            "primary ecological succession on glacial moraines in Colombia",
            "plantas pioneras en el suelo que deja el deshielo",
            "morrenas frontales colonizadas por stereocaulon y senecio"
        ],
        "hard_negatives": [
            "se pueden escalar las paredes de roca morrénica",
            "qué seguro de accidentes es obligatorio para montañistas",
            "dónde registrar la salida del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Al retirarse el hielo glaciar, las morrenas de roca desnuda son colonizadas primero por líquenes (Stereocaulon) y musgos (Grimmia), que fijan nitrógeno y retienen polvo atmosférico. Tras varias décadas, sobre ese incipiente suelo orgánico logran germinar hierbas como Senecio isabelis, Lachemilla nivalis y pequeños pastos.",
            "variants": [
                "La sucesión ecológica primaria en Los Nevados muestra cómo la vida conquista el terreno dejado por el glaciar. Primero llegan criptógamas microscópicas, luego líquenes saxícolas y finalmente rosetas andinas capaces de tolerar el congelamiento nocturno."
            ],
            "detail": "Los sectores de deshielo reciente de Santa Isabel son un laboratorio natural al aire libre para que botánicos estudien la velocidad de colonización vegetal frente al cambio climático."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.santa_isabel_glacier_extinction",
            "flora_ecosystems.stereocaulon_crustose_lichens",
            "flora_ecosystems.senecio_isabelis_endemic"
        ],
        "tags": ["sucesion primaria", "morrenas", "colonizacion vegetal", "pioneras", "deshielo"]
    },
    {
        "id": "flora_ecosystems.volcanic_ash_on_glaciers",
        "label": "impacto de ceniza volcánica en glaciares",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué la ceniza del volcán derrite más rápido el glaciar",
            "impacto de la ceniza volcanica en el hielo del ruiz",
            "albedo del glaciar oscurecido por ceniza",
            "por que la nieve del nevado del ruiz se ve gris o negra",
            "venga es verdad que la ceniza del cráter calienta el hielo",
            "oiga por que el volcán acelera el deshielo de su propia nieve",
            "disminucion del albedo por cenizas del crater arenas",
            "ceniza volcanica y absorcion de calor solar en glaciares",
            "como afecta la actividad volcanica al glaciar del ruiz",
            "emision de calor y ceniza sobre el casquete glaciar",
            "how does volcanic ash accelerate glacier melting in Ruiz",
            "reduced albedo and heat absorption on ash-covered glaciers",
            "nieve con ceniza volcanica en caldas y tolima",
            "fusión acelerada del hielo por caida de ceniza"
        ],
        "hard_negatives": [
            "cuántos kilómetros alcanza la pluma de ceniza hoy",
            "es peligroso respirar ceniza volcánica en Manizales",
            "dónde comprar mascarillas N95 para la ceniza"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Cuando el volcán Nevado del Ruiz emite ceniza, esta cubre el hielo de una capa gris oscura que reduce drásticamente su albedo (capacidad de reflejar la luz solar). En lugar de reflejar los rayos solares, la superficie oscura absorbe el calor, acelerando de forma notable la fusión y el derretimiento del glaciar.",
            "variants": [
                "La nieve limpia refleja hasta el 80 % o 90 % de la radiación solar, pero cubierta de ceniza absorbe la mayor parte del calor diurno. Este calentamiento superficial multiplica el deshielo del Ruiz, sumándose al impacto global del cambio climático."
            ],
            "detail": "Además de la ceniza, el flujo de gases calientes y calor geotérmico subterráneo por la actividad del cráter Arenas contribuye a la fusión basal de tramos de hielo."
        },
        "sources": [
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
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
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.glacier_retreat_climate_change",
            "flora_ecosystems.arenales_volcanicos_ecosystem"
        ],
        "tags": ["ceniza volcanica", "albedo", "deshielo acelerado", "nevado del ruiz", "crater arenas"]
    },
    {
        "id": "flora_ecosystems.glaciers_vs_paramo_water_role",
        "label": "aporte de agua de glaciar y páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "quién aporta más agua el glaciar o el páramo",
            "el agua que tomamos viene del glaciar o del paramo",
            "diferencia de aporte hidrico entre deshielo y paramo",
            "si se derrite el glaciar nos quedamos sin agua",
            "venga es verdad que la mayor parte del agua la da el páramo",
            "oiga de donde sale el agua de los acueductos del eje cafetero",
            "porcentaje de agua aportado por glaciares vs paramos",
            "el paramo como regulador permanente del agua",
            "rol hidrologico del glaciar comparado con frailejonales",
            "importancia relativa del glaciar en el caudal de los rios",
            "does most drinking water come from glaciers or the paramo",
            "hydrological role of paramos versus tropical glaciers",
            "el deshielo es solo un aporte estacional",
            "los paramos y bosques aportan mas del 90 por ciento del agua"
        ],
        "hard_negatives": [
            "cuánta agua debo consumir por día en altura",
            "dónde están las plantas de tratamiento de agua de Manizales",
            "a qué hora abren las termales del Ruiz"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Contrario a la creencia popular, más del 90 % del agua que abastece a las ciudades del Eje Cafetero y Tolima proviene del páramo, las turberas y el bosque altoandino, no del glaciar. Los glaciares aportan una reserva menor y estacional, mientras que el páramo es la verdadera esponja que mantiene el caudal todo el año.",
            "variants": [
                "Aunque el deshielo de los nevados alimenta directamente algunas quebradas altas, la gran 'fábrica' de agua potable es el páramo con sus frailejones y suelos orgánicos. Por eso, incluso si los glaciares desaparecen, el suministro hídrico dependerá de conservar intactos los páramos."
            ],
            "detail": "Estudios hidrológicos del IDEAM confirman que el aporte glaciar a las cuencas bajas rara vez supera el 5 % al 10 % del caudal medio anual en la cordillera Central."
        },
        "sources": [
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
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
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.paramo_sponge_mechanism",
            "flora_ecosystems.glacier_retreat_climate_change"
        ],
        "tags": ["aporte hidrico", "glaciares vs paramo", "regulacion hidrica", "acueductos", "esponja natural"]
    },
    {
        "id": "flora_ecosystems.nival_zone_no_vascular_plants",
        "label": "límite nival sin vegetación vascular",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué no crecen plantas en la nieve y el hielo",
            "limite nival del parque nacional los nevados",
            "por que no hay arboles ni plantas en la cumbre",
            "zona nival condiciones para la vida vegetal",
            "venga hasta qué altura crecen las plantas en el nevado",
            "oiga por que no hay frailejones cerca a la nieve",
            "ausencia de vegetacion vascular sobre 4800 metros",
            "limite altitudinal maximo de la flora en colombia",
            "barrera fisiologica del hielo y temperaturas bajo cero",
            "piso nival en los nevados de caldas tolima y risaralda",
            "why are there no vascular plants in the permanent snow zone",
            "upper altitudinal limit of vegetation in Los Nevados",
            "hielo perpetuo y limite de la fotosintesis",
            "suelo congelado donde ninguna planta con raices sobrevive"
        ],
        "hard_negatives": [
            "cómo llegar a la cumbre del Nevado del Tolima",
            "se requiere guía de alta montaña para pisar la nieve",
            "qué crampones y piolet debo alquilar"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Por encima de aproximadamente 4.700 a 4.800 metros de altitud, la presencia de hielo permanente, temperaturas bajo cero constantes y la falta de suelo orgánico impiden la supervivencia de plantas vasculares. En esta zona nival solo subsisten microalgas de nieve y esporas microscópicas arrastradas por el viento.",
            "variants": [
                "El piso nival marca el límite biológico absoluto para plantas con raíces y flores en Los Nevados. El agua está congelada en forma de hielo y no está disponible para absorción radicular, generando una sequía fisiológica extrema."
            ],
            "detail": "Incluso las rosetas más resistentes del superpáramo detienen su avance alrededor de los 4.700 metros, donde las heladas duran las 24 horas del día."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "IDEAM - Glaciares de Colombia",
                "url": IDEAM_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.altitudinal_gradient_changes"
        ],
        "tags": ["zona nival", "limite de vegetacion", "sequia fisiologica", "hielo", "altitud extrema"]
    },
    {
        "id": "flora_ecosystems.permafrost_and_cryoturbation",
        "label": "suelos congelados y crioturbación paramuna",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la crioturbación en los suelos del páramo",
            "agujas de hielo nocturnas en la tierra del parque",
            "por que se levanta la tierra con el hielo en las mañanas",
            "suelos periglaciales y congelamiento superficial",
            "venga qué son esos filamentos de hielo que brotan del suelo",
            "oiga por que las plantas tienen que aguantar que el suelo se mueva",
            "procesos de crioturbacion en el superparamo",
            "formacion de pipkrakes o agujas de hielo en los nevados",
            "movimiento de suelo por congelamiento y descongelamiento",
            "adaptacion de raices al estres de crioturbacion",
            "what is cryoturbation and needle ice in high paramo soils",
            "soil freezing and needle ice pipkrakes in the Andes",
            "tierra congelada que expulsa piedritas hacia arriba",
            "efecto del ciclo diario de congelacion en las raices"
        ],
        "hard_negatives": [
            "cuántos pares de medias térmicas debo ponerme",
            "qué hacer si resbalo en un sendero con escarcha",
            "cuál es el pronóstico del clima para mañana en el Ruiz"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En las madrugadas gélidas del superpáramo y páramo alto, el agua del suelo se congela formando diminutas agujas verticales de hielo llamadas 'pipkrakes'. Al formarse y derretirse a diario, este hielo mueve las piedras y remueve el sustrato (crioturbación), obligando a las plantas a tener raíces elásticas y profundas para no ser desenterradas.",
            "variants": [
                "El ciclo diario de congelación nocturna y deshielo diurno sacude mecánicamente los primeros centímetros del suelo andino. Las plántulas jóvenes sufren este desarraigo constante, por lo que solo sobreviven especies especializadas en anclarse con raíces flexibles."
            ],
            "detail": "Este fenómeno periglacial impide que muchas semillas germinen en suelo abierto, favoreciendo a plantas que crecen resguardadas bajo macollas de paja o cojines."
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
            "flora_ecosystems.draba_crucifers_superparamo",
            "flora_ecosystems.adaptation_shallow_spreading_roots"
        ],
        "tags": ["crioturbacion", "agujas de hielo", "pipkrakes", "suelo periglacial", "heladas"]
    },
    {
        "id": "flora_ecosystems.water_cycle_basin_supply",
        "label": "estrella hídrica y cuencas abastecidas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué ríos nacen en el parque Los Nevados",
            "por que los nevados es una estrella hidrica",
            "a cuanta gente le da agua el parque los nevados",
            "cuencas hidrograficas del magdalena y cauca",
            "venga qué ciudades toman agua de los nevados",
            "oiga de donde viene el agua potable de manizales y pereira",
            "cuencas abastecidas por el parque nacional natural",
            "rio chinchina otun combeima y quindio nacientes",
            "abastecimiento de agua para tres millones de personas",
            "importancia hidrica regional del parque los nevados",
            "why is Los Nevados called a regional water tower",
            "river basins fed by Los Nevados national park in Colombia",
            "distritos de riego y acueductos abastecidos por el parque",
            "el parque como fuente de agua para el eje cafetero y tolima"
        ],
        "hard_negatives": [
            "dónde pagar el recibo del agua en Manizales",
            "cuáles son los mejores hoteles del Eje Cafetero",
            "qué platos típicos probar en Santa Rosa de Cabal"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El Parque Nacional Natural Los Nevados es la mayor 'estrella hídrica' del centro del país, abasteciendo de agua potable a entre 3 y 4 millones de habitantes en cerca de 38 municipios de Caldas, Risaralda, Quindío y Tolima, incluyendo capitales como Manizales, Pereira, Armenia e Ibagué.",
            "variants": [
                "De sus cumbres nacen ríos tributarios de las macrocuencas del Cauca (Chinchiná, Otún, Quindío) y del Magdalena (Combeima, Coello, Gualí, Lagunilla, Recio). Además de consumo humano, sus aguas sustentan la caficultura y los extensos distritos de riego agrícola del Tolima."
            ],
            "detail": "Su divisoria de aguas en la cordillera Central separa los drenajes hacia el occidente cafetero y el oriente tolimense, convirtiendo a este macizo en un tesoro estratégico nacional."
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
            "flora_ecosystems.paramo_sponge_mechanism",
            "flora_ecosystems.rio_chinchina_basin_water",
            "flora_ecosystems.rio_otun_basin_water"
        ],
        "tags": ["estrella hidrica", "cuencas hidrograficas", "acueductos", "magdalena y cauca", "agua potable"]
    }
]
