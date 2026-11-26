"""
Module 3: Entries 39 to 53 for preparation knowledge section.
Covers Sleeping Pad, Stove, Cookware, Camp Hygiene, Headlamp, Cold Battery Drain,
Whistle, Technical Glacier Gear, Fitness Training, Children Preparation,
What Not to Pack, and Checklists.
"""

def get_entries_39_to_53(SRC_RES207, SRC_PNN, SRC_RES1558):
    return [
        {
            "id": "preparation.sleeping_pad",
            "label": "aislante térmico para dormir en campamento",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve un aislante térmico para acampar en el nevado",
                "es necesario colchoneta aislante para el frío",
                "qué aislante llevar para dormir en el páramo",
                "por qué se siente tanto frío por el suelo en la carpa",
                "aislante inflable o de espuma para acampar",
                "colchoneta aislante obligatoria para campamento",
                "cómo evitar que el frío del piso pase al sleeping",
                "aislante térmico para acampar en la laguna del otún",
                "qué colchoneta de camping comprar para montaña",
                "aislante para carpa en suelo congelado",
                "esterilla termica para pernoctar en alta montana",
                "do I need an insulated sleeping pad for camping",
                "sleeping pad for freezing ground in Los Nevados",
                "cuál colchoneta aísla mejor de la humedad de la tierra"
            ],
            "hard_negatives": [
                "cuáles son las tarifas para ingresar vehículos al parque",
                "a qué hora abren el punto de atención valle del cocora",
                "cómo reportar una persona perdida en el sendero"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "Un aislante térmico es indispensable para acampar en el parque. El suelo del páramo se enfría y humedece por las heladas nocturnas; sin una colchoneta que te separe del piso, tu cuerpo perderá calor por conducción hacia la tierra aunque tu saco de dormir sea de excelente calidad.",
                "variants": [
                    "Lleva siempre una colchoneta aislante de espuma densa o inflable bajo tu saco de dormir para bloquear el frío y la humedad directa del suelo congelado.",
                    "El aislante térmico es tan importante como el sleeping; colocarlo bajo tu cuerpo crea una cámara de aire que impide que el suelo helado absorba tu calor."
                ],
                "steps": [
                    [
                        "Coloca el aislante térmico extendido en el suelo de la carpa antes de desenrollar el saco de dormir.",
                        "Si usas aislante inflable, protégelo de piedras afiladas o ramas colocando una manta o plástico protector debajo en el piso de la tienda."
                    ]
                ],
                "detail": "La mayor pérdida de calor durante la noche al acampar ocurre por contacto directo con la tierra fría; el aislante frena esa transferencia térmica.",
                "reflection": "Un buen aislante bajo tu saco de dormir marca la diferencia entre una noche de descanso reparador y pasar frío continuo."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.sleeping_bag", "preparation.mountain_tent", "preparation.camp_stove"],
            "tags": ["aislante", "colchoneta", "suelo", "frio", "campamento"]
        },
        {
            "id": "preparation.camp_stove",
            "label": "estufa portátil de camping para cocinar",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "puedo llevar estufa de camping a los nevados",
                "qué cocineta portátil usar para acampar en el parque",
                "estufa a gas para cocinar en el páramo",
                "se pueden hacer fogatas para cocinar en los nevados",
                "qué combustible usar para estufa en alta montaña",
                "hornillo de camping para calentar comida en la carpa",
                "estufa portátil permitida por la resolución 207",
                "cocineta de montaña para preparar alimentos en otún",
                "calentador a gas para agua en campamento de páramo",
                "como cocinar en el campamento del parque los nevados",
                "estufa de gas o gasolina para cocinar en altura",
                "what camping stove can I use in Los Nevados",
                "portable camp stove for high altitude cooking",
                "cuál estufa funciona mejor con el frío del páramo"
            ],
            "hard_negatives": [
                "cuáles son las sanciones legales por encender fuego",
                "dónde tramitar la devolución de una reserva no usada",
                "cómo reconocer un cóndor andino en vuelo"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque señala que para acampar debes llevar material de cocina apropiado para bajas temperaturas. Por la Resolución 207 están terminantemente prohibidas las fogatas con leña en todo el parque; debes usar una estufa portátil de camping a gas o combustible líquido con paravientos.",
                "variants": [
                    "Está prohibido hacer fuego o fogatas en el parque; lleva una estufa portátil compacta de camping a gas para hervir agua y calentar tus alimentos en zonas autorizadas.",
                    "Cocina únicamente con estufa portátil de montañismo en áreas delimitadas de campamento; los cartuchos de mezcla isobutano/propano funcionan mejor en el frío."
                ],
                "steps": [
                    [
                        "Cocina siempre al aire libre en un lugar resguardado del viento y nunca dentro del compartimento cerrado de la carpa por riesgo de asfixia o incendio.",
                        "Protege la llama con una lámina cortavientos plegable para optimizar el consumo de gas en el clima frío."
                    ]
                ],
                "detail": "La Resolución 207 de 2023 prohíbe de forma terminante hacer fogatas en cualquier sector del parque para prevenir incendios forestales en la vegetación de páramo.",
                "reflection": "Usar una estufa portátil eficiente cuida los frailejones y te permite disfrutar de comida caliente en minutos."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.cookware_utensils", "preparation.trail_meals_multiday", "preparation.what_not_to_pack"],
            "tags": ["estufa", "cocineta", "gas", "cocinar", "fogatas_prohibidas"]
        },
        {
            "id": "preparation.cookware_utensils",
            "label": "utensilios de cocina reutilizables para camping",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué menaje llevar para comer en el campamento",
                "puedo llevar platos y cubiertos desechables al nevado",
                "utensilios de cocina reutilizables para el parque",
                "olla y cubiertos de aluminio para acampar en páramo",
                "platos y vasos no desechables permitidos por parques",
                "menaje liviano de camping para cocinar en la carpa",
                "taza metálica y fiambrera lavable para el sendero",
                "prohibición de cubiertos plásticos desechables en el parque",
                "utensilios de acampada según la resolución 1558",
                "que ollas y cucharas empacar para la travesia",
                "recipientes lavables para comer en campamento",
                "what reusable camp cookware and utensils to bring",
                "cooking pot and reusable utensils for mountain camping",
                "cómo transportar platos y cubiertos sin generar basura"
            ],
            "hard_negatives": [
                "cuántos volcanes componen la cordillera central",
                "dónde conseguir hospedaje en las fincas de juntas",
                "cuáles son las señales de deshidratación grave"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "Por la Resolución 1558 de 2019 está prohibido el ingreso de platos, vasos, cubiertos y recipientes desechables de plástico o icopor. Lleva menaje de cocina reutilizable y liviano (olla pequeña, taza de aluminio o plástico rígido y cubiertos lavables) para calentar y consumir tus comidas.",
                "variants": [
                    "Empaca una olla pequeña de camping y cubiertos reutilizables lavables; los elementos desechables de plástico de un solo uso no están permitidos en el parque.",
                    "Usa recipientes y vajilla reutilizable de montaña; asegúrate de limpiar tus utensilios sin arrojar residuos de comida al suelo ni a fuentes de agua."
                ],
                "steps": [
                    [
                        "Elige menaje de aluminio anodizado o acero liviano que caliente rápido y sea fácil de limpiar con poca agua.",
                        "Guarda todos los utensilios dentro de la misma olla en una bolsa de tela para ahorrar espacio en tu mochila."
                    ]
                ],
                "detail": "La Resolución 1558 de 2019 prohíbe de manera expresa envases y utensilios de plástico de un solo uso en todas las áreas del Sistema de Parques Nacionales Naturales.",
                "reflection": "Cocinar con menaje reutilizable y retornar cada desecho demuestra tu compromiso con la conservación del parque."
            },
            "sources": [SRC_RES1558, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.camp_stove", "preparation.trail_meals_multiday", "preparation.what_not_to_pack"],
            "tags": ["menaje", "olla", "utensilios", "reutilizable", "plastico"]
        },
        {
            "id": "preparation.camp_hygiene",
            "label": "manejo de excretas e higiene en campamento",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "cómo se va al baño al acampar en los nevados",
                "qué hacer con las necesidades fisiológicas en campamento",
                "manejo de excretas según la resolución 207",
                "se puede hacer hoyo de gato para excretas en el parque",
                "quién lleva la pala para hacer hoyo de gato",
                "qué se hace con el papel higiénico en la montaña",
                "está permitido enterrar la basura en el parque",
                "cómo manejar la higiene personal acampando en páramo",
                "reglas sanitarias de campamento en los nevados",
                "manejo de heces en zonas de camping del parque",
                "como evacuar excretas en travesia segun parques",
                "how is sanitation handled while camping in the park",
                "cathole and waste management rules in Los Nevados",
                "cuál es la forma correcta de ir al baño en el sendero"
            ],
            "hard_negatives": [
                "cuánto vale la boleta para niños en brisas",
                "dónde queda la entrada al sendero conejeras",
                "qué hacer en caso de caída de ceniza volcánica"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 de 2023 establece que las excretas deben ser evacuadas preferiblemente a través del cacatubo o enterradas mediante hoyo de gato haciendo uso de la pala que debe cargar el guía en su equipo. Está terminantemente prohibido enterrar basuras; todo el papel higiénico y residuos deben retornarse en bolsas.",
                "variants": [
                    "Para hacer necesidades fisiológicas al acampar, coordina con tu guía, quien porta la pala reglamentaria para realizar el hoyo de gato en sitios autorizados; el papel higiénico nunca se entierra y debe empacarse de vuelta.",
                    "La normativa del parque prohíbe excavaciones o enterramientos de basuras y solo permite hoyo de gato para excretas bajo coordinación del guía, exigiendo retirar el 100% de los residuos higiénicos generados."
                ],
                "steps": [
                    [
                        "Acude a tu guía autorizado para el uso de la pala de dotación si no hay baños ecológicos en la zona de campamento.",
                        "Guarda el papel higiénico usado y las toallas húmedas en una bolsa plástica sellada dentro de tu morral para bajarlos del parque."
                    ]
                ],
                "detail": "El numeral 6.2 de la Resolución 207 de 2023 señala que las excretas deben ser evacuadas en cacatubo o enterradas en hoyo de gato usando la pala del guía, con manejo estricto para el papel higiénico y prohibición total de enterrar basura.",
                "reflection": "Cuidar las fuentes de agua y no dejar papel en el páramo preserva la pureza de este ecosistema esencial."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.mountain_tent", "preparation.what_not_to_pack", "preparation.checklist_multiday_trek"],
            "tags": ["higiene", "excretas", "hoyo_gato", "campamento", "basura"]
        },
        {
            "id": "preparation.headlamp",
            "label": "linterna frontal de cabeza y pilas extra",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "es obligatoria la linterna para ir a los nevados",
                "qué linterna frontal llevar al parque los nevados",
                "linterna de cabeza y baterías de repuesto obligatorias",
                "puedo usar la linterna del celular en el sendero",
                "por qué exigen linterna frontal en la resolución 207",
                "linterna recomendada para caminatas de madrugada",
                "pilas de repuesto para linterna en clima frío",
                "linterna manos libres para senderismo de páramo",
                "linterna frontal para la caminata hacia santa isabel",
                "que tipo de linterna empacar para el nevado",
                "linterna obligatoria para ingresar al parque",
                "is a headlamp mandatory for Los Nevados hiking",
                "headlamp and extra spare batteries for cold trails",
                "por qué no basta con la linterna del teléfono móvil"
            ],
            "hard_negatives": [
                "cuáles son las empresas de buses que viajan a letras",
                "cómo funciona el ciclo del agua en el frailejón",
                "qué hacer si una persona sufre hipotermia grave"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige de manera obligatoria portar linterna frontal y baterías de repuesto para recorrer los senderos del parque. Una linterna de cabeza te permite iluminar el camino con las manos libres para apoyarte o usar bastones; nunca dependas del celular, ya que el frío agota su batería con rapidez.",
                "variants": [
                    "Llevar linterna frontal con pilas extra es un requisito obligatorio; alumbra tu paso de forma segura en madrugadas o si la niebla densa oscurece el sendero.",
                    "La linterna de cabeza es fundamental para arranques de madrugada o retrasos en la ruta; guarda las baterías de repuesto en un bolsillo abrigado para protegerlas del frío."
                ],
                "steps": [
                    [
                        "Verifica que la linterna funcione correctamente antes de salir e instala pilas nuevas o carga la batería al 100%.",
                        "Guarda un juego completo de pilas de repuesto en una bolsa plástica hermética dentro de tu morral."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 lista taxativamente: 'linterna frontal y baterías de repuesto' dentro del equipo mínimo obligatorio para senderismo.",
                "reflection": "Tener tus manos libres y una buena luz sobre el camino te da seguridad si la tarde te sorprende en el páramo."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.cold_battery_drain", "preparation.whistle_emergency", "preparation.checklist_glacier_day"],
            "tags": ["linterna", "frontal", "pilas", "baterias", "obligatorio"]
        },
        {
            "id": "preparation.cold_battery_drain",
            "label": "cuidado de baterías de celular en frío",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "por qué se descarga tan rápido el celular en el nevado",
                "cómo evitar que el frío apague mi teléfono",
                "se descargan las baterías de cámaras en páramo",
                "consejos para cuidar la batería del celular en el frío",
                "llevar batería externa o power bank a los nevados",
                "cómo proteger la electrónica de temperaturas bajo cero",
                "el celular se me apagó de repente en la montaña",
                "baterías de litio y bajas temperaturas en el parque",
                "guardar el teléfono junto al pecho para el calor",
                "como hacer que dure la bateria en el frio",
                "cuidado de celulares y camaras en alta montana",
                "why does phone battery drain fast in cold weather",
                "how to protect camera batteries from freezing temperatures",
                "qué precauciones tener con la electrónica en el parque"
            ],
            "hard_negatives": [
                "cuáles son las normas de acceso para mascotas",
                "dónde pagar el derecho de ingreso en villamaría",
                "cuánta nieve ha perdido el glaciar santa isabel"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "A temperaturas cercanas o inferiores a 0 ºC las baterías de litio de celulares y cámaras se descargan con gran rapidez o se apagan de forma imprevista. Guarda tu teléfono en un bolsillo interior de tu chaqueta pegado a tu pecho para mantenerlo tibio y lleva una batería externa (power bank) abrigada.",
                "variants": [
                    "El frío extremo reduce drásticamente el rendimiento de las baterías; mantén el celular cerca del calor de tu cuerpo y activa el modo avión para ahorrar energía.",
                    "Para que tu teléfono no se apague en el páramo, transpórtalo dentro de las capas interiores de tu ropa y lleva baterías de repuesto protegidas del viento helado."
                ],
                "steps": [
                    [
                        "Activa el modo de ahorro de energía y el modo avión en tu celular, ya que la búsqueda continua de señal gasta la batería muy rápido.",
                        "Guarda la batería externa y tu teléfono en bolsillos interiores térmicos de tu chaqueta y sácalos solo cuando vayas a tomar fotos."
                    ]
                ],
                "detail": "En áreas altas del parque como Brisas o campamentos las temperaturas habituales bajan de 0 ºC, ralentizando las reacciones químicas internas de las baterías de litio.",
                "reflection": "Mantener tu celular abrigado junto al pecho te asegura tener batería para tus fotos y para consultar esta guía sin conexión."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.headlamp", "preparation.daypack_size", "preparation.spare_clothing"],
            "tags": ["baterias", "celular", "frio", "power_bank", "electronica"]
        },
        {
            "id": "preparation.whistle_emergency",
            "label": "silbato de emergencia en el morral",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve llevar silbato de emergencia al nevado",
                "por qué recomiendan silbato en la mochila",
                "pito de emergencia para senderismo en páramo",
                "cómo usar un silbato si hay niebla espesa",
                "debo colgar un silbato en la correa del morral",
                "silbato plástico para alta montaña sin bolita",
                "es útil un silbato en caso de extravío o caída",
                "silbato para pedir auxilio en senderos de los nevados",
                "equipo de seguridad personal silbato en la montaña",
                "para que sirve un silbato en el morral",
                "silbato de advertencia en caso de niebla o peligro",
                "should I carry an emergency whistle on my backpack",
                "safety whistle for fog and emergency signalling",
                "cuál es la ventaja de un silbato frente a gritar"
            ],
            "hard_negatives": [
                "cuáles son las señales tempranas de mal de montaña",
                "a qué distancia queda pereira del sector otún",
                "cuándo son los periodos de cierre por conservación"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Llevar un silbato de emergencia sujeto a la correa de tu mochila es una medida de seguridad muy sencilla y efectiva. Si una niebla repentina te desorienta o sufres una caída, el sonido agudo de un silbato viaja mucho más lejos que la voz humana y te permite alertar al grupo sin agotarte.",
                "variants": [
                    "Un silbato de plástico colgado a mano en el morral te ayuda a pedir auxilio en caso de desorientación o niebla densa sin desgastar tus cuerdas vocales.",
                    "Lleva un silbato de montaña para hacerte escuchar en caso de niebla espesa; es una herramienta ligera que facilita localizarte si te apartas del sendero."
                ],
                "steps": [
                    [
                        "Prefiere silbatos plásticos sin bola interior, ya que la bolita puede congelarse con la humedad y las heladas de montaña.",
                        "Llévalo sujeto a la correa pectoral de tu morral para poder soplarlo de inmediato sin necesidad de quitarte la mochila."
                    ]
                ],
                "detail": "Gritar en alta montaña a más de 4.000 metros exige una gran cantidad de oxígeno y acelera la fatiga; el silbato produce un sonido penetrante con mínimo esfuerzo.",
                "reflection": "Un elemento tan pequeño como un silbato en tu morral te ofrece una valiosa herramienta de comunicación en caso de niebla."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.headlamp", "preparation.daypack_size", "preparation.hiking_boots"],
            "tags": ["silbato", "seguridad", "niebla", "emergencia", "morral"]
        },
        {
            "id": "preparation.technical_glacier_gear",
            "label": "equipo técnico para borde de glaciar",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué equipo técnico se necesita para el glaciar",
                "debo comprar crampones y piolet para santa isabel",
                "quién suministra el equipo técnico de alta montaña",
                "se requiere arnés y casco para subir al nevado",
                "equipo para caminar sobre la masa glaciar",
                "es obligatorio ir con guía para usar equipo técnico",
                "crampones y cuerdas para cumbre del tolima",
                "equipo técnico de montaña exigido por parques",
                "las agencias prestan los crampones y el casco",
                "que equipo especial se usa para borde de nieve",
                "equipo homologado para montanismo en los nevados",
                "what technical glacier gear is needed for summit",
                "are crampons and helmets provided by certified guides",
                "cómo se coordina el equipo técnico para el ascenso"
            ],
            "hard_negatives": [
                "cuáles son las tarifas vigentes para camping en otún",
                "cuánto mide la extensión territorial del parque",
                "cómo funciona la línea nacional de emergencias 123"
            ],
            "entities": {"trip_duration": ["travesia", "pasadia"], "sector": ["cisne_poleka_kasue", "quindio_dulima"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 de 2023 exige de forma obligatoria el servicio de acompañamiento y guianza para actividades de montaña. Para rutas a borde de glaciar o cumbres en Santa Isabel o Tolima, el equipo técnico especializado (como casco, crampones o arnés) es coordinado y proporcionado habitualmente por tu operador o guía registrado, quien te instruirá en su uso seguro.",
                "variants": [
                    "El ascenso a cumbres o aproximación a glaciares exige guianza obligatoria; tu agencia operadora registrada te facilitará el equipo técnico necesario y revisará su correcto ajuste.",
                    "No necesitas comprar equipo técnico especializado para una visita guiada: los operadores autorizados suministran elementos como crampones o cascos y garantizan su homologación y manejo en el terreno."
                ],
                "steps": [
                    [
                        "Verifica previamente con tu agencia u operador autorizado del registro REPSE qué elementos técnicos incluye el plan contratado.",
                        "Sigue con atención las instrucciones de tu guía sobre el ajuste de correas y técnicas de marcha antes de ingresar a sectores con hielo o roca suelta."
                    ]
                ],
                "detail": "El numeral 6.1 y las directrices de la Resolución 207 establecen que los operadores y guías deben contar con dotación técnica y médica para alta montaña, velando por la seguridad de los visitantes.",
                "reflection": "Confiar en el equipo y las instrucciones de tu guía certificado te permite vivir la experiencia de la nieve con total seguridad."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.gaiters", "preparation.checklist_glacier_day"],
            "tags": ["glaciar", "equipo_tecnico", "guia", "crampones", "seguridad"]
        },
        {
            "id": "preparation.fitness_training",
            "label": "condición física y esfuerzo en la montaña",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué condición física necesito para ir a los nevados",
                "debo entrenar antes de viajar al parque los nevados",
                "es muy exigente la caminata en el nevado",
                "cómo prepararme físicamente para la montaña",
                "se cansa uno mucho caminando a cuatro mil metros",
                "ejercicio previo recomendado para subir al parque",
                "consejos físicos para no agotarse en el páramo",
                "preparación cardiovascular previa para los nevados",
                "sirve caminar o trotar semanas antes del viaje",
                "que tan en forma debo estar para ir a brisas",
                "esfuerzo fisico en alta montana recomendaciones",
                "what physical fitness is needed for Los Nevados",
                "how to physically prepare for high altitude trekking",
                "qué recomendaciones físicas da parques para el ascenso"
            ],
            "hard_negatives": [
                "cuáles son los tratamientos médicos del soroche",
                "dónde puedo consultar el boletín volcánico del sgc",
                "a qué número llamar a los bomberos de villamaría"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque advierte que las bajas temperaturas, la disminución de presión atmosférica y el ascenso pueden afectar tu salud ante el esfuerzo físico. Mantén un acondicionamiento aeróbico regular antes del viaje (caminatas, trote o bicicleta) y durante la visita mantén un paso pausado y constante realizando paradas periódicas de descanso.",
                "variants": [
                    "Llegar con una condición física aeróbica básica ayuda a sobrellevar mejor el esfuerzo en altura; no camines apresurado y haz pausas de 10 minutos recomendadas por Parques para aclimatarte.",
                    "La alta montaña exige un esfuerzo mayor al cuerpo; prepárate realizando ejercicio regular previo y en el sendero avanza a un ritmo suave que te permita respirar sin agitarte en exceso."
                ],
                "steps": [
                    [
                        "Realiza actividad física cardiovascular moderada en las semanas previas a tu viaje para fortalecer piernas y resistencia respiratoria.",
                        "En el parque, atiende la recomendación oficial de realizar paradas periódicas de 10 minutos durante el ascenso para favorecer la aclimatación."
                    ]
                ],
                "detail": "Las recomendaciones oficiales del PNN Los Nevados señalan: 'Realiza paradas periódicas de 10 minutos a medida que vayas ascendiendo, para lograr una aclimatación adecuada'. La condición física ayuda a tolerar el esfuerzo, pero el ritmo pausado es clave para todos los visitantes.",
                "reflection": "Caminar con calma y acompasar tu respiración te permite disfrutar de cada tramo sin agotar tus reservas."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.break_in_boots", "preparation.water_quantity", "preparation.trail_snacks"],
            "tags": ["condicion_fisica", "entrenamiento", "esfuerzo", "ritmo", "resistencia"]
        },
        {
            "id": "preparation.children_gear",
            "label": "ropa y calzado para niños visitantes",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué ropa llevar para niños a los nevados",
                "cómo vestir a un niño para ir al parque",
                "ropa de abrigo para niños en el nevado",
                "cuál es la edad mínima para ingresar niños",
                "calzado y abrigo para niños mayores de seis años",
                "qué cuidados de vestimenta tener con los niños",
                "chaqueta impermeable y guantes para niños en páramo",
                "equipamiento recomendado para menores en el parque",
                "cómo abrigar a mi hijo para subir a brisas",
                "que ropa ponerle a un nino en el nevado",
                "vestimenta infantil para el frio de montana",
                "what clothing should children wear to Los Nevados",
                "how to dress kids warmly for high altitude visit",
                "qué prendas son indispensables para niños en el parque"
            ],
            "hard_negatives": [
                "cuáles son las tarifas reducidas para menores de 25 años",
                "dónde tramitar el pasaporte de parques nacionales",
                "qué hacer si un niño presenta vómito y mareo"
            ],
            "entities": {"trip_duration": ["pasadia"]},
            "needs": [],
            "answer": {
                "short": "La edad mínima permitida es de 6 años para Brisas, Cisne y Otún por Potosí, y de 15 años para el resto de rutas; todos los menores deben ir con adultos cuidadores. Los niños pierden calor más rápido que los adultos: vístelos con tres capas completas, gorro que cubra orejas, guantes abrigados, calzado cómodo y lleva dos mudas secas completas.",
                "variants": [
                    "Para niños mayores de 6 años autorizados en sectores permitidos, asegura abrigo estricto en capas: chaqueta impermeable, gorro térmico, guantes y mudas secas de cambio en bolsa hermética.",
                    "Abriga a los niños con especial cuidado en cabeza, manos y pies; lleva siempre ropa impermeable y mudas extras de repuesto por si se mojan o ensucian jugando en la ruta."
                ],
                "steps": [
                    [
                        "Viste a los niños con camiseta y mallas térmicas, buzo polar abrigado y chaqueta impermeable exterior con capucha.",
                        "Revisa con frecuencia que sus manos, pies y orejas permanezcan calientes y secos a lo largo de la excursión."
                    ]
                ],
                "detail": "La ficha oficial de Los Nevados establece una edad mínima de 6 años para el carreteable Brisas-Kumanday, centro El Cisne o Laguna del Otún por Potosí, edad mínima de 15 años para cumbres y travesías, y edad máxima de 69 años para todo el parque.",
                "reflection": "Cuidar el abrigo de los niños con prendas adecuadas les permite vivir una experiencia inolvidable en la montaña."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.children_snacks_hydration", "preparation.spare_clothing"],
            "tags": ["ninos", "edad_minima", "ropa_ninos", "abrigo", "familia"]
        },
        {
            "id": "preparation.children_snacks_hydration",
            "label": "alimentación e hidratación para niños en ruta",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué comida llevar para niños al nevado",
                "snacks y bebidas para niños en el parque",
                "cómo hidratar a los niños durante la caminata",
                "qué alimentos empacar para niños mayores de seis años",
                "bebidas tibias en termo para niños en páramo",
                "refrigerios que les gusten a los niños en montaña",
                "consejos de alimentación para niños en los nevados",
                "cómo entretener y alimentar a los niños en el recorrido",
                "pasabocas energéticos para niños en el carro",
                "que comida llevar a los ninos en el sendero",
                "hidratacion constante para ninos en alta montana",
                "what food and drinks to pack for kids in the park",
                "snacks and hydration tips for children hiking",
                "qué merienda llevar para los niños en el parque"
            ],
            "hard_negatives": [
                "cuáles son las restricciones médicas para adultos mayores",
                "dónde tomar transporte público hacia santa rosa",
                "cómo identificar la ceniza volcánica en el suelo"
            ],
            "entities": {"trip_duration": ["pasadia"]},
            "needs": [],
            "answer": {
                "short": "Empaca pasabocas calóricos que los niños disfruten (bocadillos, galletas de avena, frutos secos, frutas suaves) y un termo con agua de panela tibia o bebida dulce. En la altura los niños pueden olvidar beber agua; ofréceles pequeños sorbos con frecuencia y snacks en cada parada de descanso.",
                "variants": [
                    "Lleva comida ligera y snacks atractivos para tus hijos junto con un termo tibio; haz paradas periódicas para que coman y beban sin prisas.",
                    "Mantén a los niños bien hidratados y alimentados con porciones pequeñas continuas; evita alimentos pesados o grasos antes de subir por carretera de montaña."
                ],
                "steps": [
                    [
                        "Ofrece pequeños sorbos de agua o bebida tibia a los niños cada 15 a 20 minutos de recorrido.",
                        "Lleva juegos verbales, libretas de dibujo o binoculares para hacer entretenidas las paradas de inducción y miradores sin depender de pantallas."
                    ]
                ],
                "detail": "Los niños mayores de 6 años autorizados en sectores como Brisas requieren hidratación continua y pausas regulares para asimilar el cambio de altitud y temperatura.",
                "reflection": "Hacer pausas para compartir un snack calórico hace que el camino sea emocionante y cómodo para los más pequeños."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.children_gear", "preparation.trail_snacks", "preparation.thermal_flask"],
            "tags": ["ninos", "alimentacion", "hidratacion", "snacks", "familia"]
        },
        {
            "id": "preparation.what_not_to_pack",
            "label": "qué elementos evitar empacar en la mochila",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué cosas no debo llevar al nevado",
                "qué elementos están prohibidos en la mochila",
                "puedo llevar licor o cigarrillos al parque",
                "se pueden ingresar parlantes o bafles al nevado",
                "puedo llevar drones en el morral",
                "están prohibidos los plásticos desechables en el parque",
                "qué no empacar para visitar los nevados",
                "puedo llevar a mi perro o mascota en el morral",
                "artículos que no se pueden entrar al parque",
                "que objetos estan prohibidos por la resolucion",
                "cosas que no se deben llevar a los nevados",
                "what items should I NOT pack for Los Nevados",
                "prohibited items you cannot bring into the park",
                "cuáles elementos están vetados por normativa en el parque"
            ],
            "hard_negatives": [
                "cuáles son las sanciones legales y multas vigentes",
                "dónde tramitar un derecho de petición ambiental",
                "cómo saber si el volcán está en alerta naranja"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "No empaques plásticos de un solo uso (bolsas o botellas desechables prohibidas por la Resolución 1558 de 2019), bebidas alcohólicas, sustancias psicoactivas, parlantes o bafles de música, drones sin autorización previa de Parques, armas, pólvora ni leña para fogatas. Tampoco se permite el ingreso de mascotas.",
                "variants": [
                    "Evita llevar botellas plásticas desechables, bolsas de un solo uso, alcohol, parlantes de sonido, leña y drones; están prohibidos por la normativa de conservación del parque.",
                    "Revisa tu mochila antes de salir: deja en casa plásticos desechables, parlantes, licor y drones sin permiso oficial; viaja liviano y cumpliendo las reglas del área protegida."
                ],
                "steps": [
                    [
                        "Reemplaza botellas plásticas desechables por cantimploras o termos reutilizables de aluminio o plástico duro.",
                        "Recuerda que en los puestos de control del parque los funcionarios y la policía pueden revisar el equipaje y decomisar elementos prohibidos."
                    ]
                ],
                "detail": "La Resolución 207 de 2023 y la Resolución 1558 de 2019 prohíben taxativamente plásticos de un solo uso, fogatas, bebidas alcohólicas, equipos de sonido perturbadores y drones sin permiso institucional.",
                "reflection": "Dejar en casa los elementos prohibidos protege el silencio y la pureza del páramo para todos los que lo visitan."
            },
            "sources": [SRC_RES1558, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.reusable_bottles", "preparation.camp_stove", "preparation.checklist_brisas_day"],
            "tags": ["prohibido", "que_no_llevar", "alcohol", "drones", "parlantes"]
        },
        {
            "id": "preparation.checklist_brisas_day",
            "label": "checklist para visita de un día en Brisas",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "lista de chequeo para pasadía en brisas",
                "checklist para ir un día al sector norte",
                "qué empacar para ir a brisas y valle de las tumbas",
                "lista de cosas para pasadía en los nevados",
                "resumen de qué llevar para una visita de un día",
                "checklist de equipo para el sector brisas",
                "qué no me puede faltar para ir a los nevados",
                "lista completa de elementos para pasadía",
                "qué empacar para un día en el parque los nevados",
                "lista de viaje para subir a brisas",
                "checklist oficial para senderismo de un dia",
                "checklist for a day trip to Brisas sector",
                "packing list for one day visit to Los Nevados",
                "cuál es la lista definitiva de cosas para un día"
            ],
            "hard_negatives": [
                "cuáles son las tarifas vigentes para pasadía en brisas",
                "a qué hora cierran la vía manizales murillo",
                "cómo reservar el seguro de accidentes con uton"
            ],
            "entities": {"trip_duration": ["pasadia"], "sector": ["brisas_kumanday"]},
            "needs": [],
            "answer": {
                "short": "Para un pasadía en Brisas empaca: ropa vestida en tres capas (térmica, polar e impermeable), gorro que tape orejas, guantes abrigados, pasamontañas o cuello térmico, gafas con filtro UV 100%, bloqueador solar factor 50 mínimo, protector labial, cantimplora reutilizable con agua, snacks energéticos, termo con bebida caliente, documento de identidad, dinero en efectivo y muda seca completa en el vehículo.",
                "variants": [
                    "Tu lista para Brisas incluye: sistema de tres capas, calzado cerrado con agarre, gorro, guantes, gafas UV 100%, bloqueador FPS 50, agua en envase reutilizable, comida de marcha calórica y muda de repuesto en el carro.",
                    "Antes de subir a Brisas revisa tu morral: chaqueta impermeable, prendas térmicas, protección solar y labial, cantimplora llena, pasabocas y una muda seca que te espere en el transporte."
                ],
                "steps": [
                    [
                        "Vístete con primera capa térmica, buzo polar y lleva puesta o a mano tu chaqueta impermeable.",
                        "Empaca en tu morral pequeño: agua en cantimplora, snacks (bocadillo, maní), gafas UV, bloqueador solar y termo con agua de panela.",
                        "Deja en el carro o bus una muda completa de ropa seca y calzado cómodo para cambiarte al regresar."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 exige gafas UV 100%, bloqueador factor 50, linterna frontal con baterías de repuesto, cantimplora, guantes, pasamontañas, morral pequeño, ropa impermeable y abrigada, y alimentos ligeros calóricos.",
                "reflection": "Revisar tu lista paso a paso antes de salir de la ciudad te asegura un día pleno y sin contratiempos en el páramo."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.hiking_boots", "preparation.what_not_to_pack"],
            "tags": ["checklist", "brisas", "pasadia", "lista", "equipaje"]
        },
        {
            "id": "preparation.checklist_glacier_day",
            "label": "checklist para caminata al Nevado Santa Isabel",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué empacar para caminata al nevado santa isabel",
                "checklist para sendero conejeras borde de glaciar",
                "lista de cosas para caminata a la nieve en santa isabel",
                "qué llevar para ir al borde de glaciar santa isabel",
                "equipamiento para sendero de alta montaña en cisne",
                "lista de chequeo para subir al glaciar santa isabel",
                "qué necesito para la caminata al nevado santa isabel",
                "mochila y ropa para el sendero conejeras",
                "preparación para trekking a borde de nieve",
                "que ropa llevar para ir al santa isabel",
                "checklist para caminata de altura en poleka kasue",
                "packing list for Santa Isabel glacier edge hike",
                "gear checklist for Conejeras trail to the snow",
                "cuál es el equipo necesario para subir a santa isabel"
            ],
            "hard_negatives": [
                "cuál es el estado de retroceso del glaciar santa isabel",
                "dónde pagar la entrada para el sector cisne",
                "cómo llegar al alto de santa bárbara desde villamaría"
            ],
            "entities": {"trip_duration": ["pasadia"], "sector": ["cisne_poleka_kasue"]},
            "needs": [],
            "answer": {
                "short": "Para la caminata hacia el glaciar Santa Isabel (sendero Conejeras) necesitas: botas de montaña impermeables con buen agarre, tres capas completas con chaqueta impermeable de alta protección, bastones de senderismo, linterna frontal con pilas extra para la madrugada, gafas con filtro UV 100%, bloqueador factor 50, guantes térmicos, polainas, hidratación, snacks energéticos abundantes y equipo técnico coordinado con tu guía registrado.",
                "variants": [
                    "Checklist para Santa Isabel: botas de trekking amoldadas, tres capas con impermeable resistente, linterna frontal con baterías, bastones, polainas, gafas UV 100%, bloqueador FPS 50+, cantimplora con agua y refrigerios calóricos.",
                    "Al glaciar Santa Isabel debes llevar ropa técnica para frío intenso, linterna de cabeza obligatoria, calzado con excelente tracción y coordinar cualquier equipo especial con tu guía autorizado."
                ],
                "steps": [
                    [
                        "Prepara tu linterna frontal y pilas nuevas la noche anterior en el punto de registro de Potosí.",
                        "Viste ropa por capas y empaca en tu morral agua, refrigerios energéticos, polainas, guantes abrigados y gafas oscuras certificadas.",
                        "Coordina con tu guía o agencia del registro REPSE cualquier instrucción sobre equipo técnico adicional."
                    ]
                ],
                "detail": "La caminata hacia el glaciar inicia habitualmente en madrugadas gélidas a más de 4.000 metros; la Resolución 207 exige linterna frontal, ropa abrigada e impermeable, protección solar y calzado de tracción para senderos.",
                "reflection": "Estar bien equipado te permite ascender con paso firme y admirar de cerca los últimos glaciares de la cordillera."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.technical_glacier_gear", "preparation.hiking_boots", "preparation.headlamp"],
            "tags": ["checklist", "santa_isabel", "glaciar", "conejeras", "montana"]
        },
        {
            "id": "preparation.checklist_multiday_trek",
            "label": "checklist para travesía de montaña con campamento",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "lista de equipo para travesía de varios días",
                "qué llevar para acampar en el parque los nevados",
                "checklist completo para trekking con carpa en páramo",
                "qué empacar para travesía a la laguna del otún",
                "lista de chequeo para acampar en los nevados",
                "equipamiento completo para travesía al tolima con camping",
                "mochila de varios días lista de chequeo",
                "qué equipo llevar para pernoctar en la montaña",
                "checklist de acampada según la resolución 207",
                "lista de cosas para acampar en alta montana",
                "equipo obligatorio para travesia de campamento",
                "packing checklist for multiday camping trek in Los Nevados",
                "complete gear list for multiday backpacking trip",
                "qué elementos son obligatorios para pernoctar con carpa"
            ],
            "hard_negatives": [
                "cuáles son las tarifas por noche de camping en el parque",
                "dónde contratar arrieros y mulas en el valle de cocora",
                "cómo tratar un principio de edema cerebral de altitud"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "Para travesías con campamento empaca: mochila ergonómica con rain cover, carpa técnica tres o cuatro estaciones para temperaturas menores a cero grados, sleeping para frío bajo cero en bolsa impermeable, aislante térmico, estufa portátil a gas con paravientos, menaje reutilizable, raciones de comida calculadas por día, muda seca completa de repuesto, linterna frontal con baterías extra, cantimplora con agua, bastones de marcha, bolsa para basura y equipo técnico coordinado con tu guía.",
                "variants": [
                    "Tu lista de travesía incluye: carpa de alta montaña para heladas, saco de dormir para bajas temperaturas, aislante del suelo, cocineta de gas, comida deshidratada, mudas secas selladas, frontal con pilas, cantimplora y bolsa para retornar residuos.",
                    "Antes de iniciar una travesía revisa: equipo de acampada para temperaturas bajo cero según la Resolución 207, estufa portátil (fogatas prohibidas), ropa térmica por capas, linterna de cabeza y coordinación obligatoria con guía."
                ],
                "steps": [
                    [
                        "Verifica que carpa, saco de dormir y aislante cumplan los requisitos técnicos para temperaturas menores a cero grados centígrados.",
                        "Empaca toda tu ropa seca, saco de dormir y alimentos dentro de bolsas secas impermeables en el interior de tu mochila.",
                        "Lleva bolsa resistente para retornar el 100% de la basura que generes y acuerda con tu guía el protocolo sanitario para excretas con pala."
                    ]
                ],
                "detail": "La Resolución 207 exige carpas de tres o cuatro estaciones para temperaturas menores a cero grados centígrados, prohíbe las fogatas y obliga al retorno total de residuos al lugar de origen.",
                "reflection": "Una mochila bien organizada para acampar es tu hogar autónomo durante las noches estrelladas de la cordillera."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.mountain_tent", "preparation.sleeping_bag", "preparation.camp_hygiene"],
            "tags": ["checklist", "travesia", "campamento", "carpa", "multidia"]
        }
    ]
