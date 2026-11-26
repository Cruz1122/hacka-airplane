"""
Module 1: Entries 1 to 20 for preparation knowledge section.
Covers Clothing, Layering, Footwear, and Extremities.
"""

def get_entries_1_to_20(SRC_RES207, SRC_PNN, SRC_RES1558):
    return [
        {
            "id": "preparation.layering_system",
            "label": "sistema de capas de ropa para montaña",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "cómo vestirme para ir al nevado",
                "qué ropa llevar al parque los nevados",
                "cómo funciona el sistema de capas",
                "qué ropa me pongo para no pasar frío",
                "ropa recomendada para alta montaña",
                "con qué ropa voy a los nevados",
                "cómo vestir por capas en el páramo",
                "qué me pongo para subir al nevado",
                "consejos de vestimenta para clima frío",
                "que ropa llevar para el frio",
                "como vestirse para el parque",
                "what clothes should I wear to Los Nevados",
                "how should I dress in layers for the park",
                "qué ropa empaco para la visita"
            ],
            "hard_negatives": [
                "qué síntomas produce el mal de altura",
                "cuánto cuesta la entrada al parque",
                "a qué hora abren el sector brisas"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Para visitar el parque vístete con el sistema de tres capas: primera capa transpirable pegada a la piel, segunda capa de abrigo térmico y tercera capa impermeable y cortavientos. Este esquema te permite regular tu temperatura quitando o agregando prendas según el clima y tu nivel de esfuerzo.",
                "variants": [
                    "Vístete por capas para adaptarte al frío y la lluvia: capa interior para mantenerte seco, capa intermedia para retener calor y chaqueta impermeable exterior para frenar el viento y el agua.",
                    "Usa ropa técnica combinable en lugar de una sola prenda pesada: camiseta térmica interior, forro polar intermedio y chaqueta impermeable exterior con capucha."
                ],
                "steps": [
                    [
                        "Ponte primero ropa interior térmica sintética o de lana que aleje el sudor de tu piel.",
                        "Añade un buzo o chaqueta de forro polar para conservar el calor corporal durante las caminatas.",
                        "Lleva encima una chaqueta impermeable y cortavientos para protegerte de la llovizna y el viento del páramo."
                    ]
                ],
                "detail": "La normativa del parque exige llevar ropa abrigada e impermeable para soportar temperaturas bajas en cabeza, tórax y extremidades.",
                "reflection": "Vestirte por capas te ayuda a regular el abrigo según el ritmo de marcha y las condiciones del sendero."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.first_layer_thermal", "preparation.second_layer_fleece", "preparation.third_layer_waterproof"],
            "tags": ["capas", "ropa", "vestimenta", "frio", "abrigo"]
        },
        {
            "id": "preparation.first_layer_thermal",
            "label": "primera capa térmica interior transpirable",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué es la primera capa térmica",
                "qué camiseta térmica llevar al nevado",
                "para qué sirve la ropa interior térmica",
                "qué material debe ser la primera capa",
                "puedo llevar licra térmica a los nevados",
                "primera capa de ropa recomendada",
                "necesito licras térmicas para el frío",
                "camiseta interior para el páramo",
                "mallas térmicas para caminar en montaña",
                "que tipo de camiseta termica empacar",
                "primera capa transpirable para alta montaña",
                "what base layer should I wear",
                "thermal underwear for high altitude hike",
                "cómo debe ser la ropa pegada al cuerpo"
            ],
            "hard_negatives": [
                "dónde puedo comprar pastillas para el soroche",
                "cómo llegar a las cabañas de potosí",
                "cuáles animales habitan el páramo"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La primera capa debe ser una camiseta de manga larga y pantalón térmico ajustados al cuerpo, confeccionados en fibras sintéticas o lana. Su función principal es evacuar el sudor para mantener tu piel seca, evitando que la humedad te enfríe cuando te detengas.",
                "variants": [
                    "Usa ropa interior térmica transpirable que absorba el sudor y lo transporte al exterior, manteniendo tu cuerpo seco durante la caminata.",
                    "La capa base debe ser de material transpirable de secado rápido, nunca de algodón, para asegurar que la transpiración no se enfríe sobre tu piel."
                ],
                "steps": [
                    [
                        "Elige camisetas y mallas térmicas de poliéster, polipropileno o lana de corte ajustado.",
                        "Evita camisetas interiores comunes de algodón porque retienen humedad y multiplican la sensación de frío."
                    ]
                ],
                "detail": "Al ascender en alta montaña el cuerpo transpira por el esfuerzo; si esa humedad permanece en la piel, el viento gélido acelera el enfriamiento corporal.",
                "reflection": "Mantenerte seco es el primer paso para no sentir frío durante toda la jornada."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.cotton_risk", "preparation.second_layer_fleece"],
            "tags": ["primera_capa", "termica", "transpirable", "mallas", "camiseta"]
        },
        {
            "id": "preparation.second_layer_fleece",
            "label": "segunda capa de abrigo térmico polar",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué buzo o forro polar llevar",
                "para qué sirve la segunda capa de ropa",
                "qué chaqueta intermedia usar en el nevado",
                "sirve un buzo térmico para el frío",
                "chaqueta de forro polar para páramo",
                "qué saco de abrigo me pongo",
                "segunda capa para caminar en el parque",
                "chaqueta polar recomendada para montaña",
                "buzo de lana o fleece para senderismo",
                "que tipo de abrigo intermedio empacar",
                "chaqueta de abrigo para el sendero",
                "what mid layer fleece should I wear",
                "warm fleece jacket for cold weather",
                "cuál chaqueta térmica intermedia llevar"
            ],
            "hard_negatives": [
                "cuánto vale alquilar caballos en el parque",
                "cuándo es la temporada de lluvias en caldas",
                "dónde tramitar el permiso de investigación"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La segunda capa es la encargada de retener el calor que produce tu cuerpo. Se recomienda un buzo o chaqueta de forro polar liviano o micropolar que sea abrigado, transpirable y que no resulte demasiado pesado para caminar.",
                "variants": [
                    "Usa una prenda intermedia como buzo polar o chaqueta térmica liviana para conservar el calor corporal sin perder transpirabilidad.",
                    "La capa media retiene el aire caliente generado por tu cuerpo; los forros polares sintéticos son ideales por su ligereza y secado rápido."
                ],
                "steps": [
                    [
                        "Usa una chaqueta o buzo de forro polar de grosor medio con cremallera frontal para ventilar si sientes calor.",
                        "Si el frío es moderado durante el ascenso, puedes caminar solo con primera y segunda capa."
                    ]
                ],
                "detail": "La Resolución 207 establece el requisito de ropa abrigada para soportar temperaturas frías en cabeza, tórax y extremidades.",
                "reflection": "Poder abrir o quitarte la segunda capa te ayuda a no sofocarte en las subidas exigentes."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.third_layer_waterproof", "preparation.insulation_jacket"],
            "tags": ["segunda_capa", "polar", "fleece", "abrigo", "buzo"]
        },
        {
            "id": "preparation.third_layer_waterproof",
            "label": "chaqueta impermeable y cortavientos para lluvia",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué chaqueta impermeable llevar al parque",
                "sirve una chaqueta cortavientos para el nevado",
                "tercera capa de ropa recomendada",
                "chaqueta para protegerse de la lluvia y el viento",
                "qué tipo de impermeable llevar a la montaña",
                "necesito chaqueta con membrana impermeable",
                "chaqueta con capucha para el páramo",
                "impermeable obligatorio para ingresar al parque",
                "chaqueta para tormenta y frío en los nevados",
                "que chaqueta corta viento comprar",
                "impermeable para alta montaña los nevados",
                "what waterproof jacket do I need",
                "rain jacket and windbreaker for páramo",
                "cómo debe ser la chaqueta exterior"
            ],
            "hard_negatives": [
                "cuáles son las tarifas para ingresar en carro",
                "dónde ver el cóndor andino en el parque",
                "qué hacer si me extravío en el páramo"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La tercera capa debe ser una chaqueta impermeable y cortavientos con capucha. Su función es actuar como barrera contra la lluvia, la neblina y las ráfagas heladas de páramo, protegiendo las capas interiores para que no se mojen.",
                "variants": [
                    "Lleva una chaqueta exterior resistente al agua y al viento con capucha ajustable, indispensable para afrontar los cambios repentinos de clima en el parque.",
                    "La capa exterior protege todo tu sistema de abrigo frente a lloviznas y vientos fuertes; asegúrate de que tenga capucha y costuras protegidas."
                ],
                "steps": [
                    [
                        "Verifica que la chaqueta tenga capucha amplia ajustable y puños con velcro para cerrar el paso del aire frío.",
                        "Úsala siempre en la parte exterior de tu morral para sacarla de inmediato apenas empiece a llover o sople viento fuerte."
                    ]
                ],
                "detail": "La Resolución 207 de 2023 exige de manera expresa portar ropa impermeable dentro del equipo mínimo obligatorio para recorrer los senderos del parque.",
                "reflection": "Una buena chaqueta impermeable evita que el viento y la llovizna te enfríen en pocos minutos."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.rain_poncho", "preparation.waterproof_overpants"],
            "tags": ["tercera_capa", "impermeable", "chaqueta", "cortavientos", "lluvia"]
        },
        {
            "id": "preparation.insulation_jacket",
            "label": "chaqueta de abrigo para frío intenso",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "debo llevar chaqueta acolchada al nevado",
                "sirve una chaqueta de plumas para el páramo",
                "chaqueta de plumón o fibra para el frío",
                "chaqueta térmica gruesa para descansos",
                "necesito abrigo pesado para ir a brisas",
                "chaqueta para temperaturas bajo cero",
                "abrigo adicional para paradas y campamento",
                "chaqueta acolchada para alta montaña",
                "vale la pena llevar chaqueta de pluma",
                "que tipo de chaqueta gruesa empacar",
                "chaqueta de descanso para campamento",
                "do I need an insulated down jacket",
                "warm insulated coat for cold stops",
                "cuándo usar la chaqueta de pluma en la ruta"
            ],
            "hard_negatives": [
                "cuántos volcanes activos hay en el parque",
                "dónde tomar transporte público en pereira",
                "cómo tratar un esguince de tobillo"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Una chaqueta acolchada de pluma o fibra sintética es muy útil para colocarte durante las paradas de descanso, en miradores ventosos o en el campamento. Al detener la caminata tu cuerpo deja de generar calor y este tipo de prenda evita enfriamientos rápidos.",
                "variants": [
                    "Empaca una chaqueta térmica acolchada compacta para abrigarte apenas termines de caminar o durante descansos prolongados en zonas altas.",
                    "Llevar un abrigo aislante liviano te protege en momentos estáticos donde el viento de alta montaña baja la sensación térmica con rapidez."
                ],
                "steps": [
                    [
                        "Guarda la chaqueta acolchada dentro de una bolsa protegida contra el agua en tu morral para que nunca se humedezca.",
                        "Póntela de inmediato al hacer pausas de almuerzo o llegar al punto más alto antes de que tu cuerpo se enfríe."
                    ]
                ],
                "detail": "En áreas como Brisas o campamentos altos las temperaturas pueden descender por debajo de 0 ºC, especialmente en madrugadas y paradas estáticas.",
                "reflection": "Tener un abrigo a la mano para las paradas hace más placentero el disfrute del paisaje."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.second_layer_fleece", "preparation.spare_clothing"],
            "tags": ["chaqueta", "pluma", "abrigo", "aislante", "descanso"]
        },
        {
            "id": "preparation.trekking_pants",
            "label": "pantalones cómodos de senderismo y montaña",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué pantalones llevar a los nevados",
                "puedo ir en sudadera al parque",
                "pantalón de trekking recomendado para páramo",
                "con qué pantalón caminar en el nevado",
                "sirve un pantalón impermeable de montaña",
                "pantalones cómodos para caminar en altura",
                "qué tipo de pantalón ponerme para la caminata",
                "pantalón de secado rápido para los nevados",
                "ropa para las piernas en senderos fríos",
                "que pantalon usar para subir al nevado",
                "pantalones adecuados para alta montaña",
                "what hiking pants should I wear",
                "comfortable trekking pants for cold weather",
                "qué ropa llevar puesta en las piernas"
            ],
            "hard_negatives": [
                "cuánto cobran por parquear en el sector norte",
                "cuáles son las plantas endémicas del páramo",
                "a qué número llamar ante una emergencia médica"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Usa pantalones de senderismo cómodos, resistentes y de secado rápido, preferiblemente de material sintético como poliamida o poliéster. Si eres friolero o el clima está muy frío, combínalos con unas mallas térmicas interiores debajo.",
                "variants": [
                    "Lleva pantalones técnicos de montaña que permitan libertad de movimiento y sequen rápido; evita vaqueros o pantalones de mezclilla.",
                    "Elige pantalones resistentes al viento y la abrasión con tela sintética ligera, complementados con mallas térmicas si hace mucho frío."
                ],
                "steps": [
                    [
                        "Prefiere pantalones con bolsillos seguros con cremallera y refuerzos en rodillas o tobillos.",
                        "Combina tu pantalón de senderismo con mallas térmicas interiores en sectores de más de 4.000 metros o madrugadas frías."
                    ]
                ],
                "detail": "La normativa del parque pide ropa abrigada y adecuada para soportar condiciones climáticas frías en extremidades inferiores.",
                "reflection": "Caminar con un pantalón flexible y liviano previene rozaduras y fatiga en tramos empinados."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.first_layer_thermal", "preparation.waterproof_overpants", "preparation.cotton_risk"],
            "tags": ["pantalon", "trekking", "senderismo", "piernas", "ropa"]
        },
        {
            "id": "preparation.cotton_risk",
            "label": "evitar ropa y camisetas de algodón",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "por qué no llevar ropa de algodón al nevado",
                "puedo llevar jeans al parque los nevados",
                "es malo usar camisetas de algodón en el frío",
                "por qué desaconsejan los vaqueros en montaña",
                "qué pasa si uso ropa de algodón en páramo",
                "puedo ir en buso de algodón al parque",
                "riesgo de mojarse con ropa de algodón",
                "por qué el algodón da frío en la montaña",
                "se pueden usar medias de algodón en el nevado",
                "porque no usar algodon en alta montana",
                "ropa prohibida o desaconsejada para caminar",
                "why avoid cotton clothes in Los Nevados",
                "can I wear blue jeans to the park",
                "cuál es el problema con las prendas de algodón"
            ],
            "hard_negatives": [
                "dónde puedo contratar guías autorizados repse",
                "cuál es el origen geológico de las cenizas",
                "cómo consultar las alertas del nevado del ruiz"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Evita vestir prendas de algodón como jeans, camisetas o medias convencionales. El algodón absorbe el sudor y la lluvia como una esponja, tarda horas en secarse en clima frío y pierde por completo su capacidad de aislamiento, aumentando drásticamente la sensación de frío.",
                "variants": [
                    "No uses ropa de algodón en el parque: cuando se humedece por sudor o neblina retiene el agua y acelera la pérdida de calor corporal.",
                    "Las prendas de algodón y los vaqueros son peligrosos en montaña porque se empapan con facilidad y permanecen mojados y helados contra la piel."
                ],
                "steps": [
                    [
                        "Reemplaza camisetas de algodón por camisetas técnicas de poliéster, polipropileno o lana.",
                        "Cambia jeans por pantalones de senderismo sintéticos que sequen rápido y no se vuelvan rígidos con la humedad."
                    ]
                ],
                "detail": "Las recomendaciones de Parques Nacionales señalan que la vestimenta debe ser apta para climas fríos y lluviosos, privilegiando materiales sintéticos y lana.",
                "reflection": "Elegir las fibras adecuadas en tu ropa marca una gran diferencia en tu bienestar durante el recorrido."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.first_layer_thermal", "preparation.trekking_pants"],
            "tags": ["algodon", "jeans", "riesgo", "humedad", "frio"]
        },
        {
            "id": "preparation.spare_clothing",
            "label": "muda de ropa seca de repuesto",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "debo llevar ropa de repuesto al nevado",
                "llevar muda seca en la mochila o carro",
                "cuánta ropa de cambio empacar para el viaje",
                "es necesario llevar medias y camiseta extra",
                "muda completa seca para después de la caminata",
                "llevar cambio de ropa por si llueve",
                "ropa de repuesto recomendada para el parque",
                "dejo ropa seca en el vehículo",
                "muda de emergencia en bolsa hermética",
                "cuanta ropa de cambio llevar al parque",
                "muda seca para cambiarse al regresar",
                "should I pack spare dry clothes",
                "extra change of clothes for after hike",
                "por qué es importante tener una muda seca"
            ],
            "hard_negatives": [
                "cuáles senderos tienen mayor avistamiento de aves",
                "cuánto vale la entrada para estudiantes can",
                "qué hacer si una persona entra en hipotermia"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Lleva siempre una muda completa de ropa seca (camiseta, pantalón, ropa interior y medias) empacada en una bolsa impermeable. Si haces pasadía puedes dejarla en el vehículo para cambiarte al terminar; en travesías largas debe ir protegida dentro de tu mochila.",
                "variants": [
                    "Empaca un cambio completo de ropa seca en bolsa sellada; cambiarte de inmediato al volver al transporte si te mojaste previene enfriamientos innecesarios.",
                    "Tener ropa seca de reserva es una medida básica de seguridad por si te sorprende un aguacero en la montaña o transpiras en exceso."
                ],
                "steps": [
                    [
                        "Empaca camiseta, medias térmicas y pantalón seco dentro de una bolsa plástica reutilizable o bolsa seca.",
                        "Si vas en tour o carro particular, deja la muda limpia en el vehículo junto con calzado de descanso cómodo."
                    ]
                ],
                "detail": "Terminar la caminata con ropa húmeda y esperar transporte a bajas temperaturas enriquece el enfriamiento corporal; cambiarte a prendas secas devuelve el confort.",
                "reflection": "Saber que tienes ropa seca esperándote te da tranquilidad frente a cualquier chubasco en ruta."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.dry_bags", "preparation.thermal_socks"],
            "tags": ["muda", "repuesto", "ropa_seca", "cambio", "mochila"]
        },
        {
            "id": "preparation.rain_poncho",
            "label": "uso de poncho para la lluvia",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve un poncho de plástico para la lluvia",
                "puedo llevar capa o poncho al nevado",
                "es mejor poncho impermeable o chaqueta",
                "sirve el poncho plástico desechable en montaña",
                "usar capa impermeable para caminar en páramo",
                "poncho de agua para senderismo en los nevados",
                "se puede usar poncho para cubrir el morral",
                "por qué no recomiendan ponchos plásticos delgados",
                "impermeable tipo capa para el parque",
                "sirve capa plastica para la lluvia en el nevado",
                "poncho impermeable resistente para caminar",
                "is a rain poncho suitable for Los Nevados",
                "rain jacket versus rain poncho in high wind",
                "qué inconveniente tiene el poncho en el páramo"
            ],
            "hard_negatives": [
                "cuáles son las normas sobre fogatas en el parque",
                "dónde ver las lagunas verdes de páramo",
                "cómo funciona la inducción en brisas"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Es preferible usar una chaqueta impermeable técnica antes que un poncho plástico liviano. En el páramo el viento fuerte suele embolsar y desgarrar los ponchos delgados, dejando entrar el agua y limitando tu visibilidad y movimiento al caminar.",
                "variants": [
                    "Se recomienda chaqueta impermeable con capucha en vez de poncho plástico, ya que las ráfagas de viento en alta montaña rompen las capas delgadas y las vuelven incómodas.",
                    "Un poncho resistente puede servir como auxilio temporal, pero para caminar en senderos abiertos una chaqueta impermeable ajustada ofrece mucha mejor protección."
                ],
                "steps": [
                    [
                        "Prioriza una chaqueta impermeable con mangas ajustables que no flamee con las corrientes de aire.",
                        "Recuerda que la Resolución 1558 de 2019 prohíbe el ingreso de plásticos desechables de un solo uso en el parque."
                    ]
                ],
                "detail": "Además del aspecto técnico por el viento, los ponchos plásticos desechables vulneran la prohibición de plásticos de un solo uso en Parques Nacionales.",
                "reflection": "Una prenda ajustada y resistente te protege mejor de la lluvia sin entorpecer tus pasos en el sendero."
            },
            "sources": [SRC_RES207, SRC_RES1558],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.third_layer_waterproof", "preparation.waterproof_overpants", "preparation.what_not_to_pack"],
            "tags": ["poncho", "lluvia", "impermeable", "viento", "plastico"]
        },
        {
            "id": "preparation.waterproof_overpants",
            "label": "sobrepantalón impermeable para lluvia continua",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "necesito pantalón impermeable para el nevado",
                "qué es un sobrepantalón impermeable",
                "pantalón para lluvia en caminatas de páramo",
                "debo comprar sobrepantalón para ir al parque",
                "pantalón impermeable para senderismo lluvioso",
                "sirve un pantalón impermeable sobre el de trekking",
                "pantalón de lluvia para travesías largas",
                "cómo proteger las piernas de la lluvia en montaña",
                "sobrepantalón cortavientos para frío extremo",
                "pantalon impermeable para alta montana",
                "cuando usar sobrepantalon en el parque",
                "do I need waterproof rain pants",
                "overpants for heavy rain in high altitude",
                "vale la pena llevar pantalón impermeable extra"
            ],
            "hard_negatives": [
                "cuál es la historia de la erupción de armero",
                "dónde se realiza el registro en cabaña potosí",
                "qué medicamentos están contraindicados en altura"
            ],
            "entities": {"trip_duration": ["travesia", "pasadia"]},
            "needs": [],
            "answer": {
                "short": "Un sobrepantalón impermeable es muy recomendable para travesías de varios días o caminatas con pronóstico de lluvia continua. Se coloca directamente encima de tu pantalón de senderismo para mantener las piernas completamente secas y cortar el viento frío.",
                "variants": [
                    "Empacar un pantalón impermeable ligero para poner sobre tu ropa habitual te protege en jornadas de lluvia persistente o tramos con vegetación empapada.",
                    "Para pasadías cortos suele bastar un buen pantalón de secado rápido, pero en travesías largas o cumbres el sobrepantalón impermeable aporta gran seguridad."
                ],
                "steps": [
                    [
                        "Elige sobrepantalones livianos y plegables, idealmente con cremalleras laterales para ponerlos sin quitarte las botas.",
                        "Úsalos cuando la lluvia sea constante o al atravesar pajonales altos cubiertos de rocío y agua."
                    ]
                ],
                "detail": "La Resolución 207 estipula ropa impermeable como parte del equipo obligatorio para senderos del Parque Nacional Natural Los Nevados.",
                "reflection": "Tener las piernas secas durante una marcha larga previene el agotamiento prematuro."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.trekking_pants", "preparation.third_layer_waterproof", "preparation.gaiters"],
            "tags": ["sobrepantalon", "impermeable", "lluvia", "piernas", "montana"]
        },
        {
            "id": "preparation.hiking_boots",
            "label": "calzado cerrado de senderismo con agarre",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué zapatos llevar a los nevados",
                "puedo ir en tenis al parque",
                "botas recomendadas para caminar en el nevado",
                "calzado adecuado para el parque los nevados",
                "qué tipo de botas usar en alta montaña",
                "sirven tenis deportivos normales para el sendero",
                "calzado obligatorio para ingresar a los senderos",
                "botas de caña media para senderismo",
                "botas impermeables con buen labrado",
                "que zapatos ponerme para subir al nevado",
                "calzado para no resbalar en el paramo",
                "what boots should I wear to Los Nevados",
                "can I wear running sneakers to the park",
                "cómo debe ser la suela del calzado"
            ],
            "hard_negatives": [
                "a qué altitud se ubica la laguna del otún",
                "cuánto vale la póliza de seguro de accidentes",
                "qué especies de frailejón crecen en el parque"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Lleva calzado cerrado de senderismo o botas de montaña con suela de buen agarre y labrado profundo, preferiblemente impermeables. No se recomienda usar tenis urbanos de suela lisa o lona, ya que resbalan en roca húmeda o arena volcánica y se empapan con facilidad.",
                "variants": [
                    "Usa botas de trekking de caña media con soporte en el tobillo y suela antideslizante para caminar con seguridad sobre barro, piedras y arena.",
                    "La normativa del parque exige zapatos cómodos y preferiblemente impermeables; evita zapatillas lisas que aumentan el riesgo de resbalones y torceduras."
                ],
                "steps": [
                    [
                        "Elige botas cerradas que sujeten bien el tobillo para protegerte en terrenos irregulares.",
                        "Revisa que la suela tenga estrías profundas que garanticen tracción en arena volcánica y fango húmedo."
                    ]
                ],
                "detail": "La Resolución 207 de 2023 exige de manera explícita zapatos cómodos preferiblemente impermeables como equipo mínimo obligatorio para todos los senderos.",
                "reflection": "Un calzado firme y con buena tracción te da confianza en cada paso sobre el terreno de montaña."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.break_in_boots", "preparation.thermal_socks", "preparation.rubber_boots"],
            "tags": ["botas", "calzado", "zapatos", "trekking", "suela"]
        },
        {
            "id": "preparation.rubber_boots",
            "label": "botas pantaneras de caucho para lodo",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirven las botas pantaneras de caucho en el nevado",
                "cuándo usar botas de caucho en los nevados",
                "botas pantaneras para la ruta por cocora",
                "se pueden usar botas de hule para el barro",
                "botas de caucho recomendadas para senderos con lodo",
                "botas machitas para aproximación a los nevados",
                "es mejor bota pantanera o bota de trekking",
                "sirven botas de plástico para caminar en el fango",
                "botas de caucho para tramos pantanosos de acceso",
                "cuando llevar botas pantaneras al parque",
                "botas de goma para el sendero de estrella de agua",
                "are rubber rain boots good for muddy trails",
                "rubber boots for cocora muddy approach",
                "conviene usar botas pantaneras en el parque"
            ],
            "hard_negatives": [
                "cuánto demora la caminata al nevado del tolima",
                "cuáles son las reglas para no perturbar a la fauna",
                "dónde recargar agua potable en manizales"
            ],
            "entities": {"sector": ["quindio_dulima", "otun"]},
            "needs": [],
            "answer": {
                "short": "Las botas pantaneras de caucho son muy utilizadas y prácticas para tramos de acceso con barro espeso, como la ruta desde el Valle de Cocora o el ingreso por El Cedral hacia Otún. Para caminatas prolongadas conviene usarlas con medias abrigadas y cómodas que eviten roces y ampollas.",
                "variants": [
                    "En senderos húmedos de bosque andino con fango profundo, las botas pantaneras de caucho ofrecen excelente protección contra el lodo antes de llegar a la roca alta.",
                    "Si recorres aproximaciones con barro espeso como Cocora, las botas de caucho son una alternativa funcional; acompáñalas con calcetines adecuados para no maltratarte los pies."
                ],
                "steps": [
                    [
                        "Usa botas de caucho en sectores de bosque andino con lodo denso y cambia a botas de trekking al llegar al terreno pedregoso de páramo si llevas calzado de cambio.",
                        "Utiliza medias gruesas y ajustadas para proteger los talones y empeines de la fricción del caucho rígido."
                    ]
                ],
                "detail": "Muchos caminantes y operadores en la vertiente occidental del parque usan botas pantaneras para los primeros kilómetros de aproximación donde las mulas y lluvias crean barriales profundos.",
                "reflection": "Elegir el calzado según el estado del fango en la aproximación te ahorra mojarte los pies desde el primer día."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.thermal_socks", "preparation.gaiters"],
            "tags": ["botas_caucho", "pantaneras", "lodo", "barro", "cocora"]
        },
        {
            "id": "preparation.thermal_socks",
            "label": "medias abrigadas y pares de repuesto",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué medias usar para ir al nevado",
                "cuántos pares de medias empacar para el viaje",
                "medias térmicas recomendadas para páramo",
                "sirven calcetines de lana para el frío",
                "qué medias evitan ampollas en la caminata",
                "medias gruesas para botas de trekking",
                "calcetines térmicos para alta montaña",
                "medias de lana o sintéticas para los nevados",
                "cuántas medias de cambio llevar a la montaña",
                "que tipo de calcetines empacar",
                "medias para no pasar frio en los pies",
                "what warm socks should I pack",
                "thermal hiking socks to prevent blisters",
                "de qué material deben ser las medias"
            ],
            "hard_negatives": [
                "dónde contratar seguro médico para el parque",
                "cuáles son los límites territoriales de caldas",
                "cómo armar una carpa bajo la lluvia"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Usa medias térmicas de lana o fibras sintéticas transpirables, sin costuras gruesas que causen fricción. Lleva siempre al menos uno o dos pares adicionales de repuesto completamente secos en tu morral para cambiarte si se te humedecen los pies.",
                "variants": [
                    "Empaca calcetines abrigados de lana o tejido sintético y lleva pares extra protegidos en bolsa impermeable; tener medias secas es clave para mantener los pies calientes.",
                    "Evita medias comunes de algodón porque retienen sudor; prefiere calcetines técnicos para senderismo con refuerzo en talón y puntera."
                ],
                "steps": [
                    [
                        "Ponte un par de medias térmicas secas antes de iniciar la caminata matutina.",
                        "Guarda en tu morral dos pares secos de repuesto dentro de una bolsa hermética para usarlos en el campamento o al terminar la ruta."
                    ]
                ],
                "detail": "La normativa del parque exige ropa abrigada en extremidades; los pies húmedos pierden calor con gran rapidez al caminar sobre suelo frío o congelado.",
                "reflection": "Un par de medias secas en tu morral es uno de los mejores alivios tras horas de caminata."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.spare_clothing", "preparation.break_in_boots"],
            "tags": ["medias", "calcetines", "termicas", "lana", "pies"]
        },
        {
            "id": "preparation.break_in_boots",
            "label": "amoldar el calzado antes del viaje",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "puedo estrenar botas en el nevado",
                "cómo amoldar botas de montaña antes del viaje",
                "por qué no estrenar calzado en la caminata",
                "cuánto tiempo antes usar las botas nuevas",
                "consejos para que las botas no saquen ampollas",
                "ablandar zapatos de trekking para el parque",
                "es malo estrenar calzado en alta montaña",
                "cómo preparar mis botas para la caminata",
                "prevenir ampollas por calzado nuevo en sendero",
                "como amoldar botas para caminar en el parque",
                "estrenar botas de senderismo en los nevados",
                "can I wear brand new hiking boots to the park",
                "how to break in boots before high mountain hike",
                "por qué recomiendan usar calzado ya usado"
            ],
            "hard_negatives": [
                "cuál es la temperatura promedio en manizales",
                "dónde solicitar permisos de sobrevuelo de drones",
                "cuándo fue declarada área protegida los nevados"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Nunca estrenes botas de senderismo el mismo día de tu visita al parque. Úsalas en caminatas previas durante varias semanas para que la caña y la suela se ablanden y se adapten a la forma de tus pies, reduciendo el riesgo de ampollas dolorosas.",
                "variants": [
                    "Amolda tu calzado antes de viajar haciendo caminatas cortas por tu ciudad o senderos cercanos; estrenar botas en montaña empinada suele causar rozaduras severas.",
                    "Usa botas que ya conozcas y que estén adaptadas a tus pies; el calzado nuevo y rígido puede lesionarte en los primeros kilómetros de ascenso."
                ],
                "steps": [
                    [
                        "Usa tus botas nuevas con las mismas medias térmicas que llevarás al nevado durante salidas de prueba previas.",
                        "Si sientes algún punto de roce durante el amoldado, ajusta los cordones o coloca cinta preventiva antes de subir a la montaña."
                    ]
                ],
                "detail": "En recorridos de 10 o más kilómetros por terreno quebrado, una ampolla causada por calzado rígido sin amoldar puede obligarte a retrasar o suspender tu avance.",
                "reflection": "Cuidar tus pies con calzado ya amoldado te garantiza caminar con comodidad durante todo el sendero."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.thermal_socks", "preparation.fitness_training"],
            "tags": ["amoldar", "calzado", "botas", "ampollas", "senderismo"]
        },
        {
            "id": "preparation.gaiters",
            "label": "polainas de senderismo para el barro",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "para qué sirven las polainas en montaña",
                "debo llevar polainas a los nevados",
                "polainas de senderismo para barro y arena",
                "cuándo usar polainas impermeables en el parque",
                "sirven las polainas para no mojarme las botas",
                "polainas recomendadas para alta montaña",
                "polainas para proteger el tobillo del fango",
                "es obligatorio usar polainas en el sendero",
                "polainas para caminar hacia santa isabel",
                "polainas de montanismo para el paramo",
                "como colocar polainas en las botas",
                "do I need hiking gaiters for mud and sand",
                "are gaiters useful for Los Nevados trails",
                "qué función cumplen las polainas de montaña"
            ],
            "hard_negatives": [
                "cuánta distancia hay de manizales a brisas",
                "cuáles son los nombres indígenas del nevado del tolima",
                "cómo reportar una emergencia en el parque"
            ],
            "entities": {"trip_duration": ["travesia", "pasadia"]},
            "needs": [],
            "answer": {
                "short": "Las polainas de montaña son fundas que se ajustan sobre la caña de la bota y la parte baja del pantalón. Son muy útiles para impedir que ingresen agua, barro, arena volcánica o piedrecillas al interior del calzado durante la caminata.",
                "variants": [
                    "Llevar polainas impermeables protege tus tobillos y evita que el lodo o la arena suelta de los senderos se metan en tus botas.",
                    "Aunque no son de porte obligatorio individual, las polainas son un accesorio muy recomendable para mantener secas y limpias tus medias en senderos lodosos o arenosos."
                ],
                "steps": [
                    [
                        "Ajusta la correa inferior por debajo de la suela de la bota antes de abrochar la cremallera o velcro frontal.",
                        "Asegura el gancho metálico en los cordones delanteros para que la polaina permanezca tensa y sellada."
                    ]
                ],
                "detail": "En terrenos volcánicos como el sector Brisas o las arenas de Santa Isabel, las partículas pequeñas entran con facilidad al calzado si no se cuenta con protección en el tobillo.",
                "reflection": "Unas polainas bien ajustadas mantienen el interior de tus botas limpio y seco durante horas de marcha."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.rubber_boots", "preparation.waterproof_overpants"],
            "tags": ["polainas", "gaiters", "barro", "arena", "tobillo"]
        },
        {
            "id": "preparation.thermal_gloves",
            "label": "guantes abrigados para el frío de montaña",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué guantes llevar a los nevados",
                "son obligatorios los guantes para el parque",
                "guantes impermeables para el frío extremo",
                "sirven guantes de lana comunes en el nevado",
                "guantes térmicos recomendados para alta montaña",
                "qué tipo de guantes empacar para páramo",
                "guantes para viento y lluvia en los nevados",
                "debo llevar dos pares de guantes a la montaña",
                "guantes con membrana impermeable para el sendero",
                "guantes obligatorios segun la resolucion",
                "que guantes comprar para subir a brisas",
                "what warm gloves should I wear to the park",
                "waterproof insulated gloves for cold weather",
                "cómo proteger las manos del frío y viento"
            ],
            "hard_negatives": [
                "cuáles son los horarios de ingreso en cocora",
                "dónde tramitar tarjeta de crédito para reservas",
                "qué especies de colibrí viven en el páramo"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige portar guantes como parte del equipo obligatorio para senderismo. Lleva guantes térmicos abrigados y preferiblemente cortavientos o impermeables para proteger tus dedos, ya que las extremidades son las primeras en enfriarse con el viento helado.",
                "variants": [
                    "Portar guantes es un requisito obligatorio de la normativa del parque; elige guantes abrigados y resistentes al viento para mantener tus manos calientes.",
                    "Lleva guantes térmicos adecuados para clima frío; para caminatas largas conviene tener un par interior fino y guantes exteriores impermeables."
                ],
                "steps": [
                    [
                        "Elige guantes con ajuste elástico en la muñeca para evitar que entre aire helado o agua de lluvia.",
                        "Si vas a cumbres o travesías frías, empaca un par de repuesto seco por si los principales se humedecen al apoyarte en rocas."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 lista explícitamente los guantes dentro de los elementos mínimos obligatorios para recorrer cualquier sendero del parque.",
                "reflection": "Tener las manos abrigadas te permite manejar bastones y morral con agilidad y confort."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.layering_system", "preparation.thermal_hat", "preparation.neck_gaiter"],
            "tags": ["guantes", "manos", "frio", "abrigo", "extremidades"]
        },
        {
            "id": "preparation.thermal_hat",
            "label": "gorro abrigado que cubra las orejas",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué gorro llevar al parque los nevados",
                "sirve un gorro de lana para el frío",
                "gorro térmico obligatorio para la cabeza",
                "gorro que tape las orejas en el páramo",
                "gorro de forro polar para alta montaña",
                "con qué abrigarme la cabeza en el nevado",
                "gorro para no pasar frío en los nevados",
                "qué tipo de gorro empacar para brisas",
                "gorro abrigador recomendado por parques",
                "gorro termico para viento y heladas",
                "gorro para el frío extremo en la montaña",
                "what warm winter hat should I bring",
                "thermal beanie covering ears for high altitude",
                "por qué es importante abrigarse la cabeza"
            ],
            "hard_negatives": [
                "cuánta es la tarifa para adultos nacionales",
                "dónde se localiza el cráter arenas del ruiz",
                "cómo solicitar rescate en caso de extravío"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Lleva un gorro abrigado de forro polar o lana que cubra por completo la cabeza y las orejas. Una gran parte del calor corporal se disipa por la cabeza expuesta al viento helado, por lo que protegerla es fundamental para mantener el confort térmico.",
                "variants": [
                    "Empaca un gorro térmico que cubra tus orejas contra las ráfagas heladas; la normativa exige ropa abrigada para soportar frío extremo en la cabeza.",
                    "Un gorro abrigado de lana o tejido polar es indispensable en cualquier sector del parque para protegerte del viento y las bajas temperaturas."
                ],
                "steps": [
                    [
                        "Elige un gorro que ajuste bien sin apretar y baje cubriendo las orejas y la nuca.",
                        "Úsalo especialmente en las primeras horas de la mañana, en miradores abiertos y al caer la tarde."
                    ]
                ],
                "detail": "La Resolución 207 estipula el porte de ropa abrigada para soportar temperaturas extremas de frío en cabeza, tórax y extremidades.",
                "reflection": "Cubrirte bien la cabeza desde que sales del transporte cambia por completo tu experiencia en el frío."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.neck_gaiter", "preparation.thermal_gloves", "preparation.sun_hat"],
            "tags": ["gorro", "cabeza", "orejas", "abrigo", "frio"]
        },
        {
            "id": "preparation.neck_gaiter",
            "label": "cuello térmico buff o pasa montañas",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve un cuello térmico o buff en el nevado",
                "debo llevar pasamontañas a los nevados",
                "cuello de forro polar para el viento",
                "para qué sirve el cuello térmico en montaña",
                "pasa montañas obligatorio según la norma",
                "proteger el cuello y la cara del frío",
                "buff o bufanda para caminar en el parque",
                "es mejor bufanda o cuello térmico",
                "cuello térmico para taparse la boca y nariz",
                "pasa montanas para el frio en el nevado",
                "cuello tubular para senderismo de paramo",
                "should I bring a neck gaiter or balaclava",
                "buff or neck warmer for cold wind in the park",
                "cómo abrigar el cuello en alta montaña"
            ],
            "hard_negatives": [
                "cuáles son las alertas volcánicas del nevado del ruiz",
                "qué hacer si cae ceniza volcánica en la vía",
                "dónde tomar bus desde bogotá hacia letras"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 incluye el pasamontañas dentro del equipo mínimo obligatorio para senderismo. Un cuello térmico tipo buff o pasamontañas protege tu cuello, garganta y rostro del viento helado del páramo, evitando la pérdida de calor y la irritación por aire frío.",
                "variants": [
                    "Lleva un cuello térmico tubular o pasamontañas para abrigar garganta y mejillas; es mucho más cómodo y seguro que una bufanda larga suelta.",
                    "El pasamontañas o cuello de forro polar te ayuda a respirar aire templado y protege tu rostro contra el viento gélido de los senderos altos."
                ],
                "steps": [
                    [
                        "Prefiere cuellos tubulares térmicos elásticos que puedas subir hasta la nariz o bajar al cuello según la intensidad del viento.",
                        "Evita bufandas largas de lana pesada con flecos sueltos que puedan enredarse con mochilas o ramas."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 señala expresamente el 'pasa montañas' como parte del equipo obligatorio para ingresar a senderos del parque.",
                "reflection": "Proteger tu cuello y barbilla del viento gélido hace mucho más llevadera la caminata en alturas superiores a 4.000 metros."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.thermal_hat", "preparation.thermal_gloves", "preparation.lip_balm"],
            "tags": ["cuello", "buff", "pasamontanas", "viento", "garganta"]
        },
        {
            "id": "preparation.sunglasses_uv",
            "label": "gafas de sol con protección ultravioleta",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "son obligatorias las gafas de sol en el nevado",
                "qué tipo de gafas llevar al parque los nevados",
                "gafas con protección uv para alta montaña",
                "sirven gafas de sol comunes para el páramo",
                "gafas con filtro ultravioleta cien por ciento",
                "por qué llevar gafas oscuras a la montaña",
                "protección ocular contra el sol en el parque",
                "gafas de sol obligatorias según la resolución",
                "lentes con filtro uv para caminar en el nevado",
                "que gafas comprar para ir a los nevados",
                "gafas oscuras para proteger los ojos del reflejo",
                "are sunglasses mandatory in Los Nevados",
                "sunglasses with UV protection for high altitude",
                "por qué el sol daña los ojos en el páramo"
            ],
            "hard_negatives": [
                "cuánto mide de altura el volcán nevado del tolima",
                "dónde están las oficinas de parques en manizales",
                "qué fauna nocturna habita en los bosques"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige de manera obligatoria gafas con protección ultravioleta 100% (UV) para recorrer los senderos del parque. En la alta montaña la radiación solar es muy intensa y el reflejo en arena volcánica o hielo puede causar fatiga ocular y quemaduras en la córnea.",
                "variants": [
                    "Llevar gafas con filtro UV al 100% es obligatorio para todos los visitantes; protegen tus ojos de la fuerte radiación solar y del viento en el páramo.",
                    "Usa gafas de sol con protección UV certificada para evitar daños oculares causados por la intensa luminosidad y radiación de altura en Los Nevados."
                ],
                "steps": [
                    [
                        "Verifica que los lentes tengan etiqueta de protección UV 100% o UV400 certificada.",
                        "Si vas a bordes de glaciar o zonas de arena clara, prefiere gafas envolventes que cubran la luz lateral."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 exige textualmente: 'gafas con protección ultravioleta 100% (UV)' dentro del equipo obligatorio para senderismo.",
                "reflection": "Cuidar tus ojos con gafas adecuadas te permite contemplar los horizontes de la cordillera sin encandilarte ni sufrir ardor."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.sunscreen", "preparation.sun_hat", "preparation.lip_balm"],
            "tags": ["gafas", "sol", "uv", "ojos", "radiacion"]
        },
        {
            "id": "preparation.sunscreen",
            "label": "bloqueador solar de alta protección factor cincuenta",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué bloqueador solar llevar al nevado",
                "es obligatorio el bloqueador solar en el parque",
                "bloqueador solar factor cincuenta como mínimo",
                "cada cuánto aplicarse bloqueador en la montaña",
                "protector solar para alta montaña los nevados",
                "sirve bloqueador normal para ir a brisas",
                "bloqueador solar obligatorio por resolución",
                "por qué el sol quema tanto en el páramo",
                "cuál protector solar empacar para el sendero",
                "que bloqueador llevar al parque los nevados",
                "bloqueador factor 50 para el rostro y cuello",
                "what sunscreen should I use in Los Nevados",
                "sunscreen factor 50 mandatory for high altitude",
                "cómo proteger la piel del sol en el parque"
            ],
            "hard_negatives": [
                "a qué edad mínima pueden ingresar los niños",
                "cuáles son los síntomas de la deshidratación severa",
                "cuándo fue creada la ley de parques nacionales"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige portar bloqueador solar con factor de protección 50 como mínimo. La ficha del parque recomienda aplicarlo antes de iniciar la caminata y reaplicarlo cada dos horas en rostro, cuello, orejas y manos, ya que la radiación ultravioleta es extrema en altura.",
                "variants": [
                    "Llevar bloqueador solar factor 50 mínimo es un requisito obligatorio; aplícalo en todas las zonas expuestas y repite cada dos horas incluso con cielo nublado.",
                    "La radiación en Los Nevados quema la piel con rapidez; usa protector solar FPS 50+ y no olvides cubrir orejas, nariz y cuello durante todo el recorrido."
                ],
                "steps": [
                    [
                        "Aplícate una capa generosa de bloqueador solar al menos 20 minutos antes de comenzar la exposición al aire libre.",
                        "Reaplica el producto cada dos horas de caminata, especialmente tras transpirar o limpiarte el rostro."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 fija el 'bloqueador solar factor 50 como mínimo' como parte del equipo obligatorio para senderismo.",
                "reflection": "Protegerte la piel desde temprano te ahorra quemaduras solares que pueden arruinarte el resto del viaje."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.sunglasses_uv", "preparation.lip_balm", "preparation.sun_hat"],
            "tags": ["bloqueador", "protector_solar", "fps50", "radiacion", "piel"]
        }
    ]
