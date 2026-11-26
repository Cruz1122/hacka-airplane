# -*- coding: utf-8 -*-
"""
Entries group 3: Topics 37 to 54
Cushion plants, superpáramo flora, rosette plants, cryptogams (mosses, lichens, fungi).
"""

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
HUMBOLDT_URL = "http://www.humboldt.org.co/es/investigacion/proyectos/actuales/item/222-paramos-de-colombia"
DATE_VERIFIED = "2026-11-21"

ENTRIES = [
    {
        "id": "flora_ecosystems.cojines_plantago_rigida",
        "label": "cojines de agua plantago rigida",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los colchones o cojines de agua",
            "planta en cojin plantago rigida",
            "almohadillas de agua en los humedales del parque",
            "que son esos tapetes verdes duros que parecen musgo",
            "venga qué planta es ese cojín donde brota agua",
            "oiga por que le dicen colchón de agua a esa planta",
            "cojines de turbera plantago rigida caracteristicas",
            "plantas almohadilladas de alta montana en colombia",
            "por que no se deben pisar los cojines de agua",
            "vegetacion de cojin en humedales altoandinos",
            "what are the cushion plants Plantago rigida in Los Nevados",
            "hard green cushion bogs in high Andean wetlands",
            "llanten de paramo en forma de almohadilla",
            "como retiene agua el cojin de plantago rigida"
        ],
        "hard_negatives": [
            "se puede acampar encima de los cojines de agua",
            "cuántos litros de agua potable debo llevar en la mochila",
            "cuánto mide el sendero hacia la Laguna del Otún"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los 'colchones de agua' son formaciones densas dominadas por Plantago rigida, una planta cuyas diminutas rosetas crecen tan compactadas que forman tapetes convexos duros como rocas. Crecen en bordes de lagunas y turberas, reteniendo agua subterránea que filtran gota a gota hacia los ríos.",
            "variants": [
                "Plantago rigida forma almohadillas rígidas que actúan como diques naturales en los humedales de Los Nevados. Aunque parecen esponjas blandas por fuera, son estructuras vegetales muy compactas que tardan décadas en crecer y nunca deben ser pisadas."
            ],
            "detail": "Pisar estos cojines rompe su entramado interno y crea canales de drenaje que pueden secar la turbera circundante en pocos meses."
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
            "flora_ecosystems.cushion_bogs_damage_trampling",
            "flora_ecosystems.distichia_cushion_bog",
            "flora_ecosystems.high_andean_wetlands"
        ],
        "tags": ["plantago rigida", "cojines de agua", "almohadillas", "turberas", "retencion hidrica"]
    },
    {
        "id": "flora_ecosystems.distichia_cushion_bog",
        "label": "cojines de turbera distichia muscoides",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la planta Distichia muscoides",
            "cojines de turbera del genero distichia",
            "almohadillas duras de juncaceas en humedales",
            "que plantas forman los bofedales altoandinos",
            "venga que diferencia hay entre distichia y plantago",
            "oiga por que esas almohadillas de turbera parecen piedra",
            "juncacea de alta montana distichia muscoides",
            "turbera de cojines en el parque nacional los nevados",
            "como se forman los bofedales con distichia",
            "plantas que acumulan turba en el fondo de los valles",
            "what is the cushion bog plant Distichia muscoides",
            "high altitude peat forming cushion bogs in Colombia",
            "distichia en los humedales del nevado santa isabel",
            "acumulacion de materia organica por cojines de turbera"
        ],
        "hard_negatives": [
            "dónde alquilar caballos para cruzar las turberas",
            "cuánto cuesta contratar un guía oficial del parque",
            "qué ropa impermeable comprar para la lluvia"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Distichia muscoides es una juncácea diminuta que crece apretada formando montículos o almohadillas densas en depresiones inundadas del páramo. Al morir sus tallos basales, no se descomponen por el frío y la falta de oxígeno, formando gruesas capas de turba que retienen agua y carbono.",
            "variants": [
                "Junto a Plantago rigida, Distichia muscoides es la principal arquitecta de los bofedales y turberas de alta montaña en Los Nevados. Sus colonias se extienden lentamente creando suelos saturados de agua vitales para el equilibrio hídrico regional."
            ],
            "detail": "Estas formaciones de cojines pueden tener varios metros de profundidad de turba acumulada a lo largo de miles de años desde la última glaciación."
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
            "flora_ecosystems.cojines_plantago_rigida",
            "flora_ecosystems.turberas_bogs_peatlands",
            "flora_ecosystems.high_andean_wetlands"
        ],
        "tags": ["distichia muscoides", "bofedales", "turberas", "juncaceas", "almohadillas"]
    },
    {
        "id": "flora_ecosystems.cacho_de_venado_loricaria",
        "label": "planta cacho de venado superpáramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la planta cacho de venado",
            "loricaria colombiana o andicolea colombiana",
            "planta endemica del superparamo de los nevados",
            "cacho de venado arbustillo con ramas escamosas",
            "venga que planta es esa que parece una ramita seca de ciervo",
            "oiga por que le dicen cacho de venado a esa matica",
            "especie andicolea colombiana en los arenales",
            "flora endemica adaptada a suelos volcanicos extremos",
            "donde crece el cacho de venado en el parque",
            "arbusto xerofitico de alta montaña loricaria",
            "what is the cacho de venado plant Loricaria colombiana",
            "endemic dwarf shrub of the superparamo in Colombia",
            "ramas en forma de cornamenta en el superparamo",
            "adaptacion extrema de loricaria en valle de las tumbas"
        ],
        "hard_negatives": [
            "se ven venados de cola blanca en Valle de las Tumbas",
            "cuántos kilómetros hay entre Brisas y el cráter",
            "dónde queda el refugio del Ruiz"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El cacho de venado (Loricaria colombiana o Andicolea colombiana) es un arbusto enano y leñoso endémico de Colombia que sobrevive en los pedregales y arenales del superpáramo. Sus ramas aplanadas y cubiertas de escamas recuerdan la forma de la cornamenta de un ciervo, reduciendo al mínimo la evaporación por viento.",
            "variants": [
                "Entre 4.200 y 4.700 metros de altitud en Los Nevados destaca el cacho de venado, adaptado a condiciones casi lunares de frío y ceniza volcánica. Sus diminutas hojas imbricadas como tejas le permiten resistir la desecación y el congelamiento diario."
            ],
            "detail": "Es una de las plantas vasculares que alcanza mayor altitud en la cordillera Central colombiana, desafiando vientos de más de 60 km/h."
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
            "flora_ecosystems.arenales_volcanicos_ecosystem",
            "flora_ecosystems.draba_crucifers_superparamo"
        ],
        "tags": ["cacho de venado", "loricaria colombiana", "andicolea", "superparamo", "endemismo"]
    },
    {
        "id": "flora_ecosystems.chocho_paramo_lupinus",
        "label": "chocho o lupino de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el chocho o lupino de páramo",
            "lupinus alopecuroides en los nevados",
            "planta lanosa con espiga de flores moradas o azules",
            "chocho de paramo caracteristicas y hojas peludas",
            "venga que flor es esa espiga plateada tan bonita en el arenal",
            "oiga por que parece una cola de zorro esa planta del páramo",
            "lupinus de alta montaña en suelo volcanico",
            "leguminosa de paramo fijadora de nitrogeno",
            "pelos blancos y densos en lupinus alopecuroides",
            "donde ver chochos de paramo en el parque",
            "what is the Lupinus alopecuroides lupine in the paramo",
            "woolly high altitude lupine plant in Los Nevados",
            "espiga floral de lupinus en el superparamo",
            "adaptacion del chocho a suelos de ceniza volcanica"
        ],
        "hard_negatives": [
            "las semillas del chocho de páramo son comestibles",
            "qué comida rápida venden en el restaurante Brisas",
            "cuántos baños públicos hay en el sendero"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El chocho o lupino de páramo (Lupinus alopecuroides) es una llamativa planta silvestre de alta montaña con una densa capa de pelos blancos lanudos que cubren sus hojas y su espiga floral. Sus flores azules o violáceas emergen de esa espiga afelpada que le da aspecto de cola de zorro plateada.",
            "variants": [
                "Lupinus alopecuroides crece tanto en el páramo alto como en los arenales del superpáramo. Como toda leguminosa, enriquece los suelos volcánicos fijando nitrógeno mediante bacterias radiculares, facilitando la llegada de otras plantas pioneras."
            ],
            "detail": "Su vellosidad lanuda actúa como un suéter térmico que impide que los botones florales se congelen durante las madrugadas heladas."
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
            "flora_ecosystems.arenales_volcanicos_ecosystem",
            "flora_ecosystems.adaptation_leaf_pubescence"
        ],
        "tags": ["chocho de paramo", "lupinus alopecuroides", "leguminosa", "vellosidad lanosa", "espiga azul"]
    },
    {
        "id": "flora_ecosystems.valeriana_paramo",
        "label": "valeriana silvestre de alta montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay valeriana silvestre en el parque Los Nevados",
            "que es la valeriana de paramo",
            "valeriana plantaginea en los nevados",
            "hierbas en roseta basal valeriana de montana",
            "venga qué planta medicinal es la valeriana del páramo",
            "oiga por que le dicen valeriana si crece pegada a la piedra",
            "especies de valeriana en la alta cordillera central",
            "propiedades tradicionales de la valeriana andina",
            "rosetas arrosetadas carnosas en suelo paramuno",
            "valerianas nativas de colombia protegidas",
            "is wild Valeriana found in Los Nevados national park",
            "high altitude Valeriana plantaginea rosette species",
            "valeriana de paramo hojas carnosas pegadas al suelo",
            "esta permitido recolectar raices de valeriana"
        ],
        "hard_negatives": [
            "puedo tomar té de valeriana antes de subir para no marearme",
            "dónde comprar pastillas para el mal de montaña en Manizales",
            "cuáles son los síntomas del edema pulmonar"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En el páramo de Los Nevados crecen varias especies de valeriana nativa, como Valeriana plantaginea, caracterizadas por hojas carnosas en roseta pegadas al suelo para no sufrir con el viento helado. Aunque parientes lejanas de la valeriana medicinal europea, en el parque están estrictamente protegidas de recolección.",
            "variants": [
                "Las valerianas de alta montaña forman almohadillas o rosetas aplanadas entre los pajonales y turberas. Sus hojas coriáceas acumulan agua y nutrientes en suelos pedregosos, produciendo pequeñas flores blancas o rosadas."
            ],
            "detail": "Arrancar sus raíces altera el suelo orgánico y está severamente sancionado por las leyes de conservación de Parques Nacionales."
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
            "flora_ecosystems.werneria_rosettes",
            "flora_ecosystems.adaptation_rosette_growth_form"
        ],
        "tags": ["valeriana de paramo", "valeriana plantaginea", "roseta", "alta montana", "proteccion"]
    },
    {
        "id": "flora_ecosystems.lachemilla_nivalis",
        "label": "planta rastrera lachemilla nivalis",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la planta Lachemilla nivalis",
            "plantas rastreras plateadas del borde glaciar",
            "lachemilla en el superparamo de los nevados",
            "hierba rastrera con hojas sedosas en la alta montana",
            "venga qué es ese tapete gris plateado pegado a las piedras",
            "oiga por que crece tan bajita la lachemilla",
            "asociacion vegetal baccharis y lachemilla nivalis",
            "rosaceas nativas de alta montana en colombia",
            "hierbas pioneras de suelos pedregosos frios",
            "lachemilla nivalis adaptacion al hielo",
            "what is Lachemilla nivalis creeping alpine plant",
            "silvery dwarf Rosaceae species in the superparamo",
            "plantas que crecen al borde de los glaciares",
            "tapete vegetal contra el viento en morrenas"
        ],
        "hard_negatives": [
            "se puede caminar descalzo sobre los tapetes vegetales",
            "dónde comprar crampones para caminar en el glaciar",
            "cuántos metros de desnivel hay en el sendero"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Lachemilla nivalis es una hierba rastrera de la familia de las rosáceas que forma densos tapetes plateados pegados a las rocas morrénicas y suelos del superpáramo. Sus diminutas hojas están cubiertas de pelos sedosos que la resguardan del hielo y reducen el impacto del viento extremo.",
            "variants": [
                "Esta pequeña planta andina se arrastra a ras de suelo en sectores cercanos a los glaciares de Los Nevados. Al crecer pegada a la roca, aprovecha el calor residual absorbido por la piedra durante el día para resistir las heladas nocturnas."
            ],
            "detail": "Junto con arbustillos de Baccharis caespitosa, forma una de las asociaciones vegetales pioneras más características descritas en el Plan de Manejo del parque."
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
            "flora_ecosystems.moraines_primary_succession",
            "flora_ecosystems.adaptation_dwarfism_prostrate"
        ],
        "tags": ["lachemilla nivalis", "planta rastrera", "superparamo", "pelos sedosos", "morrenas"]
    },
    {
        "id": "flora_ecosystems.helechos_licopodios_huperzia",
        "label": "licopodios y helechos de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay helechos y licopodios en el páramo",
            "que son los licopodios huperzia en los nevados",
            "helechos de alta montaña en el parque los nevados",
            "licopodio con ramitas como pinos diminutos",
            "venga que son esas plantitas verdes que parecen pinos chiquitos",
            "oiga los helechos crecen a mas de tres mil metros",
            "especies de huperzia y lycopodium en turberas",
            "plantas vasculares primitivas sin semillas en el paramo",
            "helechos adaptados a la humedad del bosque y paramo",
            "helecho arborescente Dicksonia en el bosque altoandino",
            "are there clubmosses and ferns like Huperzia in the paramo",
            "Lycopodium and alpine ferns in Los Nevados park",
            "licopodios de alta montana en colombia",
            "helechos pequenos entre los pajonales humedos"
        ],
        "hard_negatives": [
            "se pueden recolectar helechos para adorno navideño",
            "dónde tomar fotos del atardecer en el nevado",
            "cuántos días dura el permiso de ingreso al parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En Los Nevados habitan licopodios (géneros Huperzia y Lycopodium) y helechos de alta montaña, plantas ancestrales que se reproducen por esporas. En el páramo crecen como tallos erguidos o rastreros parecidos a pinos en miniatura, mientras que en el bosque altoandino destacan los helechos arborescentes de gran porte.",
            "variants": [
                "Los licopodios son fósiles vivientes muy comunes en turberas y pajonales húmedos del parque. Sus pequeñas hojas rígidas toleran temperaturas gélidas y suelos saturados donde muchas plantas con flores no prosperan."
            ],
            "detail": "En los cañones boscosos del flanco risaraldense y quindiano aún se observan helechos arbóreos de los géneros Dicksonia y Cyathea, que alcanzan varios metros de altura."
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
            "flora_ecosystems.sphagnum_moss_peat"
        ],
        "tags": ["licopodios", "huperzia", "helechos", "esporas", "fosiles vivientes"]
    },
    {
        "id": "flora_ecosystems.draba_crucifers_superparamo",
        "label": "crucíferas draba de suelos helados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es la planta Draba en el superpáramo",
            "cruciferas diminutas de suelos congelados",
            "draba en los arenales del parque los nevados",
            "plantas con florecitas blancas que resisten hielo",
            "venga qué planta tan chiquita crece entre las piedras del ruiz",
            "oiga cómo sobreviven las flores al congelamiento diario",
            "especies del genero draba en la alta cordillera",
            "flora pionera del borde glaciar en colombia",
            "draba adaptacion a heladas diurnas y nocturnas",
            "familia de la mostaza en el superparamo andino",
            "what is the Draba plant growing in frozen volcanic soils",
            "tiny high alpine crucifers in Los Nevados superparamo",
            "flores microscopicas en los pedregales altos",
            "hierbas enanas que florecen a mas de cuatro mil metros"
        ],
        "hard_negatives": [
            "a qué hora amanece despejado en el nevado",
            "cuántas capas de guantes debo ponerme",
            "dónde queda el centro de interpretación en Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Draba es un género de diminutas hierbas de la familia de las crucíferas adaptadas a vivir en los suelos más fríos y congelados del superpáramo, por encima de 4.300 metros. Forman pequeñas rosetas con hojas carnosas y producen diminutas flores blancas o amarillas capaces de abrirse entre escarcha matutina.",
            "variants": [
                "Entre las gravas y cenizas de sectores altos del Ruiz y Santa Isabel encuentras especies de Draba. Sus raíces profundas se anclan con firmeza en el terreno pedregoso para no ser arrastradas por el viento ni por el deshielo superficial."
            ],
            "detail": "Estas plantas acumulan solutos especiales en el citoplasma de sus células que bajan el punto de congelación celular, impidiendo que el hielo rompa sus membranas."
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
            "flora_ecosystems.arenales_volcanicos_ecosystem",
            "flora_ecosystems.adaptation_antifreeze_sugars"
        ],
        "tags": ["draba", "cruciferas", "superparamo", "heladas", "flores diminutas"]
    },
    {
        "id": "flora_ecosystems.werneria_rosettes",
        "label": "rosetas enanas werneria del suelo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son las plantas Werneria en el páramo",
            "werneria nubigena margaritas a ras de suelo",
            "rosetas pegadas a la tierra con flores blancas",
            "por que las flores de werneria no tienen tallo largo",
            "venga que flor es esa que parece una margarita sin tronco",
            "oiga por que esa flor brota directo de la tierra",
            "werneria en turberas y humedales de los nevados",
            "adaptacion acaule de werneria nubigena",
            "compuestas enanas de alta montaña andina",
            "flores protegidas del viento helado en el suelo",
            "what are the Werneria pygmy rosettes in the paramo",
            "stemless Werneria nubigena flowers hugging alpine soil",
            "werneria en el parque nacional los nevados",
            "margaritas acaules que florecen pegadas a la roca"
        ],
        "hard_negatives": [
            "se puede pisar fuera del sendero para tomar una foto",
            "qué cámara fotográfica funciona mejor en frío",
            "dónde comprar postales y recuerdos del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Werneria (como Werneria nubigena) es una planta andina cuyas rosetas de hojas carnosas y flores parecidas a margaritas crecen completamente pegadas al suelo, casi sin tallo visible (hábito acaule). Al evitar elevarse en el aire, se resguarda del viento gélido y aprovecha el calor del sustrato.",
            "variants": [
                "En bordes de turberas y laderas húmedas de Los Nevados puedes descubrir a Werneria floreciendo a ras de tierra. Sus cabezuelas blancas con centro amarillo se abren con el sol matutino y se cierran rápidamente cuando la niebla o la escarcha cubren la montaña."
            ],
            "detail": "Esta arquitectura enana es un ejemplo clásico de convergencia evolutiva en plantas alpinas tropicales sometidas a oscilaciones térmicas extremas cada 24 horas."
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
            "flora_ecosystems.cojines_plantago_rigida",
            "flora_ecosystems.adaptation_dwarfism_prostrate"
        ],
        "tags": ["werneria", "werneria nubigena", "roseta acaule", "margarita enana", "adaptacion al viento"]
    },
    {
        "id": "flora_ecosystems.ericaceas_mortino_uva_camarona",
        "label": "mortiño y uva camarona silvestre",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el mortiño y la uva camarona",
            "arbustos con frutos silvestres en los nevados",
            "macleania rupestris uva camarona de paramo",
            "hesperomeles y gaultheria en el subparamo",
            "venga que fruticas moradas crecen en esos matorrales",
            "oiga los frutos del mortiño se pueden comer en el camino",
            "ericaceas del bosque altoandino y subparamo",
            "arbustos de bayas silvestres en caldas y tolima",
            "importancia del mortino para las aves de paramo",
            "flores acampanadas rojas y rosadas de ericaceas",
            "what are wild mortiño berries and Macleania rupestris",
            "wild Ericaceae shrubs with edible berries in Colombia",
            "uva camarona silvestre en el parque los nevados",
            "plantas con campanitas rosadas en el ecotono"
        ],
        "hard_negatives": [
            "está permitido recolectar frutos silvestres para comer",
            "dónde venden dulces de mortiño en Manizales",
            "qué repelente de insectos debo utilizar"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El mortiño (Hesperomeles ferruginea) y la uva camarona (Macleania rupestris) son arbustos nativos de la familia de las ericáceas que crecen en el bosque altoandino y subpáramo. Producen flores en campanitas rosadas o rojas y pequeñas bayas oscuras que constituyen un alimento fundamental para aves y mamíferos silvestres.",
            "variants": [
                "Las ericáceas son muy abundantes en las laderas húmedas de Los Nevados, destacando por sus hojas duras y bayas silvestres. Aunque tradicionalmente son comestibles para el ser humano, dentro del parque nacional está prohibido cosecharlas para no privar de alimento a la fauna nativa."
            ],
            "detail": "Estas bayas son la principal fuente de energía de tucanes andinos, mirlas de montaña y osos de anteojos durante sus desplazamientos estacionales."
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
            "flora_ecosystems.high_andean_forest",
            "flora_ecosystems.chite_hypericum"
        ],
        "tags": ["mortiño", "uva camarona", "ericaceas", "macleania rupestris", "frutos silvestres"]
    },
    {
        "id": "flora_ecosystems.sphagnum_moss_peat",
        "label": "musgo sphagnum en las turberas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el musgo Sphagnum en el páramo",
            "musgo de turbera sphagnum en los nevados",
            "por que el musgo sphagnum absorbe tanta agua",
            "cuanta agua puede chupar el musgo de turbera",
            "venga qué tipo de musgo forma los pantanos del parque",
            "oiga por que el suelo se siente acolchonado al caminar cerca a lagunas",
            "capacidad de absorcion de agua del musgo sphagnum",
            "formacion de turba por musgos en alta montana",
            "musgos hidrofugos y esponjas vivas en colombia",
            "importancia hidrologica del genero sphagnum",
            "what is Sphagnum peat moss in the high wetlands",
            "water holding capacity of Sphagnum moss in Los Nevados",
            "musgo esponjoso de los humedales paramunos",
            "sphagnum retencion de agua y acidez en turberas"
        ],
        "hard_negatives": [
            "se puede recolectar musgo para el pesebre en diciembre",
            "cuál es la sanción por extraer musgo en Colombia",
            "qué botas impermeables son mejores para el fango"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El musgo Sphagnum es el principal componente vivo de las turberas altoandinas de Los Nevados. Posee células huecas especializadas (hialocitos) que pueden retener entre 15 y 25 veces su peso seco en agua, actuando como una inmensa esponja que amortigua crecientes y surte arroyos en épocas secas.",
            "variants": [
                "Los densos tapetes rojizos o verdes de Sphagnum tapizan las depresiones húmedas del parque. Al absorber las lluvias y liberar lentamente el agua filtrada, este musgo es el engranaje hidrológico más eficiente de los humedales paramunos."
            ],
            "detail": "Además, Sphagnum acidifica el medio ambiente acuático, lo que inhibe el crecimiento bacteriano y detiene la descomposición orgánica, originando la turba."
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
            "flora_ecosystems.turberas_bogs_peatlands",
            "flora_ecosystems.high_andean_wetlands",
            "flora_ecosystems.paramo_sponge_mechanism"
        ],
        "tags": ["sphagnum", "musgo de turbera", "hialocitos", "retencion hidrica", "esponja viva"]
    },
    {
        "id": "flora_ecosystems.paramo_lichens_overview",
        "label": "líquenes de páramo y superpáramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los líquenes del parque Los Nevados",
            "liquenes en las rocas y suelo del paramo",
            "simbiosis de alga y hongo en alta montana",
            "por que hay manchas de colores en las piedras del parque",
            "venga que son esas costras verdes y amarillas sobre las rocas",
            "oiga como hacen los líquenes para vivir en el frío extremo",
            "diversidad de liquenes en el superparamo del ruiz",
            "liquenes foliaceos crustaceos y fruticulosos",
            "resistencia a la radiacion ultravioleta en liquenes",
            "importancia de los liquenes como bioindicadores de aire limpio",
            "what are the lichens found in the paramo and superparamo",
            "crustose and fruticose lichens in Los Nevados park",
            "manchas anaranjadas y grises en rocas volcanicas",
            "los liquenes como primeros colonizadores de la roca"
        ],
        "hard_negatives": [
            "se pueden rayar o pintar las rocas del parque",
            "cuántos años tienen las rocas volcánicas del Ruiz",
            "dónde conseguir mapa geológico del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los líquenes son organismos simbióticos formados por la unión de un hongo y un alga o cianobacteria, capaces de sobrevivir sobre rocas desnudas y ceniza volcánica donde ninguna planta común subsistiría. En Los Nevados forman manchas amarillas, verdes, grises y anaranjadas en piedras expuestas a intensa radiación UV.",
            "variants": [
                "Gracias a su capacidad de deshidratarse y entrar en latencia sin morir, los líquenes toleran heladas nocturnas y vientos abrasadores. Son pioneros en disgregar la roca volcánica para generar las primeras partículas de suelo orgánico."
            ],
            "detail": "Su extrema sensibilidad a la contaminación los convierte en excelentes bioindicadores: su abundancia y colorido en Los Nevados demuestran la pureza del aire de cordillera."
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
            "flora_ecosystems.stereocaulon_crustose_lichens",
            "flora_ecosystems.cladonia_reindeer_moss",
            "flora_ecosystems.superparamo_ecosystem"
        ],
        "tags": ["liquenes", "simbiosis", "bioindicadores", "rocas volcanicas", "radiacion uv"]
    },
    {
        "id": "flora_ecosystems.stereocaulon_crustose_lichens",
        "label": "líquenes colonizadores de roca volcánica",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué es el liquen Stereocaulon en los nevados",
            "liquenes que crecen sobre ceniza y lava volcanica",
            "stereocaulon en los arenales del nevado del ruiz",
            "liquenes de aspecto coralino en rocas de alta montana",
            "venga que son esos ramitos grises como corales sobre la piedra",
            "oiga por que crecen liquenes en la ceniza volcanica reciente",
            "fijacion de nitrogeno por liquenes stereocaulon",
            "colonizacion primaria de coladas de lava y morrenas",
            "especies pioneras de sustratos volcanicos en caldas",
            "pseudopodios y talo del liquen stereocaulon",
            "what is Stereocaulon lichen colonizing volcanic rocks",
            "coral-like lichens on volcanic pumice and moraines",
            "liquen gris cenizo pionero en el superparamo",
            "asociacion de cianobacterias en stereocaulon"
        ],
        "hard_negatives": [
            "se pueden recolectar muestras de lava o ceniza del parque",
            "cuándo fue la última emisión de ceniza del volcán",
            "cuál es la distancia de seguridad al cráter Arenas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Stereocaulon es un género de líquenes pioneros de aspecto coralino o ramificado que coloniza activamente las rocas volcánicas, pumitas y escombros morrénicos en el superpáramo del Ruiz y Santa Isabel. Posee estructuras especiales (cefalodios) que albergan cianobacterias capaces de fijar nitrógeno directamente de la atmósfera.",
            "variants": [
                "Sobre las piedras volcánicas del Valle de las Tumbas abundan pequeños ramilletes grises de Stereocaulon. Al incorporar nitrógeno a la roca estéril, este liquen prepara el terreno para que años después puedan nacer pequeños musgos y plantas de alta montaña."
            ],
            "detail": "Su estructura tridimensional es altamente resistente al impacto abrasivo de las partículas de ceniza transportadas por las ventiscas del Ruiz."
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
            "flora_ecosystems.paramo_lichens_overview",
            "flora_ecosystems.arenales_volcanicos_ecosystem",
            "flora_ecosystems.moraines_primary_succession"
        ],
        "tags": ["stereocaulon", "liquenes saxicolas", "ceniza volcanica", "fijacion de nitrogeno", "pioneros"]
    },
    {
        "id": "flora_ecosystems.cladonia_reindeer_moss",
        "label": "líquenes cladonia entre los pastizales",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son los líquenes Cladonia en el páramo",
            "liquenes que parecen arbolitos diminutos en el suelo",
            "cladonia en los pajonales del parque los nevados",
            "liquenes de copa o liquen de los renos en colombia",
            "venga qué son esos ramilletes blancos entre la paja",
            "oiga por que hay líquenes que parecen musgo seco en la tierra",
            "talos fructicosos de cladonia en suelos organicos",
            "copitas y ramas bifurcadas de liquenes cladonia",
            "microbosques de liquenes en el suelo del paramo",
            "especies del genero cladonia en los nevados",
            "what are Cladonia lichens growing in tussock grasslands",
            "cup lichens and miniature branching lichens in paramo soils",
            "cladonia protegiendo el suelo de la evaporacion",
            "liquenes con forma de trompeta o copa diminuta"
        ],
        "hard_negatives": [
            "se puede fumar o encender cerillos en el pastizal",
            "cuántos senderos autorizados tiene el parque",
            "dónde botar la basura que genero durante el recorrido"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los líquenes del género Cladonia forman microbosques en miniatura entre las matas de pajonal y frailejones en Los Nevados. Tienen formas fascinantes de pequeñas trompetas o ramas blanquecinas intrincadas que cubren el suelo orgánico, protegiéndolo de la erosión del viento y la pérdida de humedad.",
            "variants": [
                "Entre el pastizal andino es común ver alfombras de Cladonia, líquenes fruticulosos que crecen erguidos sobre el suelo. Funcionan como una suave cubierta biológica que retiene rocío y resguarda a diminutos invertebrados del páramo."
            ],
            "detail": "Cuando el clima es seco se vuelven quebradizos y crujen ligeramente, pero tras unos minutos de niebla o llovizna recuperan su flexibilidad esponjosa."
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
            "flora_ecosystems.paramo_lichens_overview",
            "flora_ecosystems.pajonales_calamagrostis",
            "flora_ecosystems.paramo_sponge_mechanism"
        ],
        "tags": ["cladonia", "liquenes de copa", "microbosques", "pajonales", "suelo organico"]
    },
    {
        "id": "flora_ecosystems.epiphytic_mosses_cloud_forest",
        "label": "musgos epífitos del bosque nublado",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué hay tanto musgo en los árboles del bosque",
            "musgos y hepaticas epifitas en el bosque altoandino",
            "barbas y cojines de musgo colgando de las ramas",
            "arboles forrados de musgo en los nevados",
            "venga por que los troncos parecen vestidos de verde",
            "oiga para que sirve todo ese musgo que cuelga de las ramas",
            "biomasa de briofitas en el bosque de niebla",
            "captacion de agua por musgos epifitos",
            "bromelias y musgos sobre encenillos y alisos",
            "plantas que viven sobre otras sin ser parasitas",
            "why are cloud forest trees covered in epiphytic mosses",
            "mosses and liverworts absorbing fog in Andean forests",
            "epifitas del bosque nuboso en caldas y risaralda",
            "los musgos epifitos no le chupan savia al arbol"
        ],
        "hard_negatives": [
            "se pueden comprar orquídeas a orillas de la carretera",
            "cuánto tiempo dura el traslado desde Manizales a Brisas",
            "qué ropa técnica de montaña es indispensable"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los árboles del bosque altoandino están densamente forrados de musgos y hepáticas epífitas debido a la constante neblina que choca contra la montaña. Estos musgos no son parásitos: solo usan las ramas como soporte físico para capturar agua y nutrientes del aire, actuando como esponjas aéreas que gotean agua pura hacia el suelo.",
            "variants": [
                "Esa capa verde y mullida que cubre los troncos en Los Nevados está compuesta por decenas de especies de briofitas. Pueden retener varias veces su peso en agua de niebla, alimentando las raíces de los árboles y regulando la humedad ambiental de todo el bosque."
            ],
            "detail": "Estas alfombras aéreas crean microhábitats donde habitan ranas andinas, orquídeas miniatura y cientos de artrópodos del dosel."
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
            "flora_ecosystems.sphagnum_moss_peat"
        ],
        "tags": ["musgos epifitos", "bosque de niebla", "briofitas", "esponjas aereas", "humedad"]
    },
    {
        "id": "flora_ecosystems.grimmia_superparamo_moss",
        "label": "musgos oscuros grimmia del superpáramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué musgos viven en las rocas del superpáramo",
            "musgo negro o verde oscuro en piedras frias",
            "grimmia en el parque nacional los nevados",
            "musgos almohadillados saxicolas de alta montana",
            "venga que son esas bolitas negras pegadas a las piedras de cumbre",
            "oiga por que ese musgo parece quemado por el sol",
            "especies del genero grimmia adaptadas a heladas",
            "musgos que viven a mas de cuatro mil quinientos metros",
            "resistencia a desecacion en musgos de superparamo",
            "almohadillas diminutas de musgo en morrenas glaciares",
            "what are the dark rock mosses Grimmia in the superparamo",
            "saxicolous cushion mosses surviving extreme freezing",
            "musgos que aguantan nieve y hielo en las rocas",
            "pigmentos oscuros protectores de musgos alpinos"
        ],
        "hard_negatives": [
            "a qué altura empieza la nieve en el Nevado del Ruiz",
            "cuántos días se necesitan para aclimatar el cuerpo",
            "se puede usar dron en el sector de las morrenas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En las rocas más altas y frías del superpáramo crecen musgos del género Grimmia, formando almohadillas redondeadas y oscuras muy apretadas. Su color negruzco o verde pardo se debe a pigmentos protectores que filtran la excesiva radiación ultravioleta y absorben calor solar para descongelar sus células.",
            "variants": [
                "Los musgos Grimmia están diseñados para resistir el congelamiento absoluto durante la noche y el calor abrasador diurno. Cuentan con vellosidades transparentes en las puntas de sus hojas que rompen el viento y condensan rocío nocturno."
            ],
            "detail": "Pueden pasar meses completamente desecados y, con unas pocas gotas de lluvia o deshielo, reviven y reanudan su fotosíntesis en cuestión de minutos."
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
            "flora_ecosystems.paramo_lichens_overview",
            "flora_ecosystems.adaptation_antifreeze_sugars"
        ],
        "tags": ["grimmia", "musgos saxicolas", "superparamo", "pigmentos oscuros", "radiacion uv"]
    },
    {
        "id": "flora_ecosystems.paramo_fungi_decomposers",
        "label": "hongos descomponedores de suelos fríos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay hongos en el páramo de Los Nevados",
            "que hongos descomponen la materia en el frio",
            "fungi en suelos de alta montana andina",
            "setas y champinones silvestres en los nevados",
            "venga qué hongos crecen entre el pajonal y el musgo",
            "oiga como se descomponen las hojas muertas con tanto frío",
            "hongos saprofitos en el ecosistema paramuno",
            "descomposicion lenta de materia organica por hongos",
            "hongos diminutos que viven en la necromasa del frailejon",
            "biodiversidad del reino fungi en los nevados",
            "are there decomposer fungi in the cold soils of Los Nevados",
            "high altitude saprophytic fungi in paramo ecosystems",
            "setas de colores en el bosque y paramo humedo",
            "papel de los hongos en el reciclaje de nutrientes frios"
        ],
        "hard_negatives": [
            "se pueden recolectar hongos silvestres para comer",
            "qué hacer en caso de intoxicación alimentaria en el parque",
            "dónde comprar alimentos calientes en el refugio"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En el suelo del páramo y bosque altoandino habita una notable diversidad de hongos saprófitos que descomponen la hojarasca, la necromasa del frailejón y las raíces muertas. Aunque las bajas temperaturas hacen que su actividad sea lenta, su labor es esencial para reciclar nutrientes en suelos volcánicos.",
            "variants": [
                "Los hongos de alta montaña en Los Nevados están adaptados a temperaturas cercanas a cero grados. Sus filamentos microscópicos (hifas) colonizan la materia vegetal muerta y liberan fósforo y nitrógeno que luego alimentan a las plantas nativas."
            ],
            "detail": "Durante las épocas lluviosas es posible divisar pequeños cuerpos fructíferos (setas) anaranjadas o marrones brotando discretamente entre el musgo y el pajonal."
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
            "flora_ecosystems.mycorrhizae_paramo_roots",
            "flora_ecosystems.paramo_carbon_sequestration",
            "flora_ecosystems.frailejon_dead_leaves_necromass"
        ],
        "tags": ["hongos", "saprofitos", "descomposicion", "reino fungi", "reciclaje de nutrientes"]
    },
    {
        "id": "flora_ecosystems.mycorrhizae_paramo_roots",
        "label": "asociaciones micorrícicas en raíces paramunas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué son las micorrizas en las plantas del páramo",
            "asociacion de hongos y raices en suelos volcanicos",
            "como ayudan los hongos a las plantas de los nevados",
            "micorrizas arbusculares en frailejones y pastos",
            "venga por que las plantas necesitan hongos en sus raices",
            "oiga como absorben fosforo las plantas en suelos de ceniza",
            "simbiosis micorrizica en el ecosistema de paramo",
            "hongos micorrizicos fijacion de nutrientes en alta montana",
            "redes subterraneas de hongos en el parque nacional",
            "supervivencia vegetal en andisoles pobres gracias a hongos",
            "what are mycorrhizal fungi in high Andean plant roots",
            "symbiotic root fungi helping paramo plants absorb phosphorus",
            "hongos en las raices de espeletia y polylepis",
            "redes fungicas en suelos volcanicos de los nevados"
        ],
        "hard_negatives": [
            "se pueden desenterrar plantas para ver sus raíces",
            "cuántas horas dura el recorrido guiado en Brisas",
            "dónde pagar la tasa de ingreso al parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las micorrizas son asociaciones simbióticas entre hongos del suelo y las raíces de frailejones, pajonales y árboles como Polylepis. En los suelos volcánicos del parque el fósforo queda químicamente atrapado por las cenizas, pero las hifas del hongo logran disolverlo y entregárselo a la planta a cambio de azúcares.",
            "variants": [
                "Casi todas las plantas nativas de Los Nevados dependen de hongos micorrícicos para nutrirse en suelos fríos y pobres. Esta red subterránea multiplica el alcance de las raíces, mejorando además la captación de agua durante periodos secos."
            ],
            "detail": "Estas redes micorrícicas también tejen el suelo orgánico, dándole estructura porosa y previniendo la erosión hídrica en las pendientes del parque."
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
            "flora_ecosystems.paramo_fungi_decomposers",
            "flora_ecosystems.adaptation_shallow_spreading_roots",
            "flora_ecosystems.frailejones_overview"
        ],
        "tags": ["micorrizas", "simbiosis", "fosforo", "suelos volcanicos", "raices"]
    }
]
