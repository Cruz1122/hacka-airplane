"""
Module 2: Entries 21 to 38 for preparation knowledge section.
Covers Sun Protection Accessories, Backpacks, Trekking Poles, Hydration, Food, and Mountain Tent/Sleeping Bag.
"""

def get_entries_21_to_38(SRC_RES207, SRC_PNN, SRC_RES1558):
    return [
        {
            "id": "preparation.lip_balm",
            "label": "protector labial hidratante para el viento",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve llevar protector labial al nevado",
                "cómo evitar que se me partan los labios en el frío",
                "protector labial con filtro solar para montaña",
                "bálsamo de labios recomendado para páramo",
                "manteca de cacao para el frío y viento",
                "por qué se resecan tanto los labios en el parque",
                "cuidado de los labios en alta montaña",
                "bálsamo labial para el clima de los nevados",
                "protector labial hidratante para senderismo",
                "que crema usar para labios partidos en el frio",
                "protector labial con proteccion solar para montana",
                "should I bring lip balm with sunscreen",
                "how to prevent chapped lips in high altitude",
                "remedio para no tener labios agrietados en la ruta"
            ],
            "hard_negatives": [
                "cuáles son las señales de hipotermia leve",
                "cómo reservar entrada por la plataforma web",
                "dónde nace el río otún en el parque"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Lleva un protector labial hidratante o bálsamo con filtro solar. El aire seco, las bajas temperaturas y la radiación intensa de alta montaña resecan la piel de los labios con facilidad, provocando dolorosas fisuras si no se protegen con frecuencia durante la caminata.",
                "variants": [
                    "Aplica bálsamo labial o manteca de cacao con protección solar varias veces durante la caminata para prevenir labios resecos y cortados por el viento frío.",
                    "El viento helado y el sol de páramo agrietan los labios rápidamente; tener un protector labial a la mano en un bolsillo accesible te brinda alivio continuo."
                ],
                "steps": [
                    [
                        "Aplícate bálsamo labial antes de iniciar la marcha al aire libre.",
                        "Reaplica periódicamente cada vez que bebas agua o sientas los labios tirantes por el viento."
                    ]
                ],
                "detail": "En altitudes superiores a los 3.500 metros la baja humedad relativa combinada con el viento sostenido deshidrata rápidamente las mucosas expuestas.",
                "reflection": "Un pequeño bálsamo en el bolsillo te evita molestias y dolor al sonreír o comer durante tu excursión."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.sunscreen", "preparation.sunglasses_uv", "preparation.skin_moisturizer"],
            "tags": ["labial", "balsamo", "viento", "sol", "hidratacion"]
        },
        {
            "id": "preparation.sun_hat",
            "label": "sombrero o gorra para protección solar",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "debo llevar sombrero o gorra al nevado",
                "sirve una gorra para el sol en el páramo",
                "sombrero con ala ancha para alta montaña",
                "cuándo usar gorra durante la caminata",
                "gorra para protegerse del sol en el parque",
                "sombrero de senderismo recomendado para nevados",
                "pucho o sombrero para caminatas de día",
                "es mejor gorra deportiva o sombrero de ala",
                "protección para la cara y cuello contra el sol",
                "que tipo de sombrero llevar al parque",
                "gorra con protector de cuello para el sendero",
                "should I wear a sun hat in Los Nevados",
                "wide brim hat for high altitude sun protection",
                "cuál prenda usar en la cabeza durante el día soleado"
            ],
            "hard_negatives": [
                "a qué hora cierran el paso en valle de las tumbas",
                "cuáles senderos están autorizados para bicicletas",
                "dónde pagar el seguro obligatorio de accidentes"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Empaca un sombrero de ala ancha o una gorra con visera para las horas del día en que el sol esté despejado. Aunque sientas frío por el viento, la radiación cenital en alta montaña es muy fuerte y una gorra protege tu rostro, frente y ojos del resplandor directo.",
                "variants": [
                    "Lleva una gorra con visera o sombrero amplio para protegerte del sol durante las caminatas diurnas, alternándolo con el gorro térmico si baja la temperatura.",
                    "Un sombrero para el sol complementa el bloqueador solar y las gafas oscuras, resguardando tu cabeza de insolaciones cuando el cielo se despeja."
                ],
                "steps": [
                    [
                        "Usa la gorra o sombrero durante las caminatas de media mañana y mediodía cuando la radiación solar es más perpendicular.",
                        "Si el viento arrecia, ajusta el cordón bajo la barbilla para evitar que el sombrero vuele sobre el páramo."
                    ]
                ],
                "detail": "La Resolución 207 exige medidas de protección para la cabeza ante condiciones climáticas extremas; alternar gorra solar y gorro abrigado asegura protección integral.",
                "reflection": "Cuidarte del sol diurno previene dolores de cabeza causados por el exceso de resplandor sobre el rostro."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.sunscreen", "preparation.sunglasses_uv", "preparation.thermal_hat"],
            "tags": ["sombrero", "gorra", "sol", "visera", "radiacion"]
        },
        {
            "id": "preparation.skin_moisturizer",
            "label": "crema hidratante para la piel reseca",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve llevar crema hidratante al nevado",
                "cómo cuidar la piel de la resequedad en la montaña",
                "crema humectante para el viento de páramo",
                "por qué se reseca la piel en los nevados",
                "debo empacar crema para manos y rostro",
                "crema para después de la caminata en frío",
                "remedio para la piel tirante por el viento helado",
                "cuidado facial para visitar el parque los nevados",
                "crema para resequedad en alta montaña",
                "que crema usar para no quemarse con el viento",
                "crema humectante recomendada para senderistas",
                "should I pack skin moisturizer for cold wind",
                "how to prevent dry skin during high mountain hike",
                "qué producto ayuda a recuperar la piel tras el frío"
            ],
            "hard_negatives": [
                "cuánto cobran los porteadores en el sector sur",
                "cuáles son los nombres de las lagunas del parque",
                "cómo identificar el mal agudo de montaña"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Llevar una crema hidratante para manos y rostro es muy conveniente para contrarrestar la resequedad que provocan el aire frío y el viento del páramo. Aplicarla al terminar la jornada o en el campamento ayuda a reponer la barrera protectora de la piel.",
                "variants": [
                    "Empaca una crema humectante densa para aplicar en mejillas y manos después de caminar; alivia la tirantez provocada por el viento gélido de montaña.",
                    "El clima frío deshidrata la piel con rapidez; una crema hidratante en tu equipaje te brinda confort y previene descamaciones tras la excursión."
                ],
                "steps": [
                    [
                        "Aplica crema hidratante por la noche en el alojamiento o campamento sobre rostro y manos limpios.",
                        "Durante el día al aire libre, prioriza siempre el bloqueador solar factor 50 sobre la crema humectante común."
                    ]
                ],
                "detail": "Las bajas temperaturas reducen la producción natural de lípidos de la piel, haciendo que la exposición prolongada al viento provoque irritación.",
                "reflection": "Cuidar tu piel al terminar el sendero te permite descansar con total comodidad."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.lip_balm", "preparation.sunscreen", "preparation.sun_hat"],
            "tags": ["crema", "hidratante", "piel", "resequedad", "viento"]
        },
        {
            "id": "preparation.daypack_size",
            "label": "morral pequeño para caminata de pasadía",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué morral llevar para pasadía en los nevados",
                "sirve un morral pequeño para ir a brisas",
                "qué tamaño de mochila usar en una caminata de un día",
                "morral de ataque recomendado para el parque",
                "mochila pequeña para llevar agua y chaqueta",
                "puedo llevar morral escolar al nevado",
                "qué empacar en el morral para un solo día",
                "mochila cómoda para caminata corta en páramo",
                "morral para pasadía en el sector norte",
                "que tipo de maletín llevar a los senderos",
                "morral liviano para el sendero valle de las tumbas",
                "what daypack should I bring for a day trip",
                "small backpack for one day hike in Los Nevados",
                "cómo organizar el morral para una visita de un día"
            ],
            "hard_negatives": [
                "a qué distancia queda manizales de murillo",
                "dónde puedo ver cóndores en libertad",
                "cuáles son las sanciones por ingresar drones"
            ],
            "entities": {"trip_duration": ["pasadia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige portar un morral pequeño como parte del equipo obligatorio para senderismo. Elige una mochila cómoda y liviana donde quepan tus prendas de abrigo, chaqueta impermeable, cantimplora con agua, snacks energéticos y tus documentos personales.",
                "variants": [
                    "Para pasadías lleva un morral pequeño con correas acolchadas; debe tener espacio suficiente para guardar tu chaqueta impermeable, comida de marcha y agua.",
                    "Un morral compacto y ergonómico te permite transportar tus capas de ropa y elementos obligatorios sin cargarte de peso innecesario en senderos de un día."
                ],
                "steps": [
                    [
                        "Empaca en el fondo las prendas que no usarás de inmediato y deja arriba la chaqueta impermeable y los refrigerios.",
                        "Ajusta bien las correas a tus hombros y pecho para que la mochila quede pegada a tu espalda y no desequilibre tu marcha."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 lista taxativamente el 'morral pequeño' dentro de los elementos mínimos obligatorios para recorrer cualquier sendero autorizado.",
                "reflection": "Llevar solo lo necesario en un morral liviano te permite caminar con mayor soltura y disfrutar cada mirador."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.backpack_rain_cover", "preparation.reusable_bottles", "preparation.trail_snacks"],
            "tags": ["morral", "mochila", "pasadia", "pequeno", "equipaje"]
        },
        {
            "id": "preparation.trekking_backpack",
            "label": "mochila de travesía para varios días",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué mochila llevar para travesía de varios días",
                "cómo debe ser la mochila para acampar en el parque",
                "mochila grande de trekking para travesía en los nevados",
                "mochila de montaña con soporte lumbar y cinturón",
                "qué morral usar para travesía a la laguna del otún",
                "mochila para cargar carpa y saco de dormir",
                "cómo empacar la mochila de travesía en páramo",
                "ajuste de mochila pesada para caminar en altura",
                "mochila de expedición recomendada para el tolima",
                "que tamano de morral llevar para varios dias",
                "mochila tecnica de carga para alta montana",
                "what backpack do I need for multiday trek",
                "large trekking backpack for camping in Los Nevados",
                "cómo distribuir el peso en una mochila de travesía"
            ],
            "hard_negatives": [
                "cuáles son los refugios de montaña disponibles",
                "dónde tramitar el seguro de alta montaña",
                "cuándo ocurrió la tragedia de armero"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "Para travesías de varios días con campamento necesitas una mochila técnica de travesía con cinturón lumbar acolchado y ajuste de pecho. Su estructura distribuye la mayor parte del peso sobre tus caderas en lugar de los hombros, facilitando el transporte de carpa, sleeping y víveres.",
                "variants": [
                    "Usa una mochila ergonómica con soporte lumbar regulable para travesías largas; reparte el peso sobre la pelvis para evitar sobrecargas en la espalda durante ascensos prolongados.",
                    "Para rutas de pernocta en Otún o Tolima, una mochila con buen arnés de carga y compartimentos exteriores es indispensable para llevar equipo de acampada y comida ordenada."
                ],
                "steps": [
                    [
                        "Coloca el saco de dormir en el fondo, los elementos pesados como carpa o cocineta pegados a tu espalda, y la ropa impermeable arriba.",
                        "Ajusta primero el cinturón lumbar sobre las crestas ilíacas y luego templa las hombreras para repartir el peso adecuadamente."
                    ]
                ],
                "detail": "Cargar peso excesivo mal distribuido a más de 3.800 metros incrementa el gasto energético y el cansancio muscular durante jornadas exigentes de montaña.",
                "reflection": "Una mochila bien ajustada a tus medidas convierte una carga pesada en un paso firme y estable."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.backpack_rain_cover", "preparation.dry_bags", "preparation.mountain_tent"],
            "tags": ["mochila", "travesia", "carga", "lumbar", "campamento"]
        },
        {
            "id": "preparation.backpack_rain_cover",
            "label": "cobertor impermeable para proteger el morral",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve el cobertor de lluvia para la mochila",
                "cómo proteger mi morral del agua en el nevado",
                "forro impermeable para mochila de trekking",
                "debo comprar funda de lluvia para el morral",
                "rain cover para morral en clima lluvioso",
                "cómo evitar que se moje el equipaje en el páramo",
                "protector impermeable exterior para la mochila",
                "funda para la lluvia obligatoria para senderistas",
                "protector de morral contra aguaceros en la montaña",
                "como tapar el morral cuando llueve en el parque",
                "forro de lluvia para maleta de senderismo",
                "do I need a backpack rain cover in Los Nevados",
                "waterproof pack cover for high altitude rain",
                "qué accesorios protegen el morral de la humedad"
            ],
            "hard_negatives": [
                "cuáles son las tarifas de camping en potosí",
                "dónde observar frailejones gigantes en el parque",
                "cómo activar el protocolo de socorro con el guía"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Un cobertor impermeable exterior (rain cover) es indispensable para proteger tu mochila de la lluvia, la neblina densa y el barro. Aunque la tela del morral sea resistente, las cremalleras y costuras filtran agua con rapidez si llueve de manera constante.",
                "variants": [
                    "Lleva un forro impermeable elástico para cubrir tu morral apenas comience a lloviznar, evitando que el agua penetre hacia tus prendas de abrigo o comida.",
                    "El cobertor de mochila mantiene tu equipaje a salvo del fango y la lluvia; mantenlo a la mano en un bolsillo lateral para colocarlo rápidamente."
                ],
                "steps": [
                    [
                        "Asegura el cobertor elástico cubriendo completamente la parte frontal, superior y laterales del morral.",
                        "Combina siempre el cobertor exterior con bolsas secas interiores para garantizar doble protección a tus mudas secas."
                    ]
                ],
                "detail": "Las precipitaciones en la cordillera pueden presentarse de forma repentina; tener el cobertor listo evita que tu equipo de abrigo se empape en el camino.",
                "reflection": "Proteger tu mochila desde la primera gota te asegura tener ropa seca y caliente cuando llegues a descansar."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.dry_bags", "preparation.daypack_size", "preparation.spare_clothing"],
            "tags": ["cobertor", "rain_cover", "mochila", "impermeable", "lluvia"]
        },
        {
            "id": "preparation.dry_bags",
            "label": "bolsas impermeables para aislar la ropa",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirven las bolsas secas para empacar la ropa",
                "cómo aislar la ropa seca dentro del morral",
                "dry bags para travesías en los nevados",
                "bolsas herméticas para proteger el saco de dormir",
                "cómo evitar que se moje la muda de repuesto",
                "bolsas plásticas reutilizables para organizar la maleta",
                "proteger celulares y electrónica del agua en montaña",
                "bolsa estanca recomendada para campamento",
                "bolsas secas impermeables para alta montaña",
                "como empacar la ropa para que no se moje",
                "bolsas selladas para proteger la carga en travesia",
                "should I use dry bags inside my backpack",
                "waterproof stuff sacks for clothes and sleeping bag",
                "cuál es el mejor método para impermeabilizar el equipaje"
            ],
            "hard_negatives": [
                "cuánto tiempo dura la inducción obligatoria en brisas",
                "cuáles son las especies de mamíferos amenazados",
                "dónde pagar la entrada con tarjeta débito"
            ],
            "entities": {"trip_duration": ["travesia", "pasadia"]},
            "needs": [],
            "answer": {
                "short": "Usa bolsas secas impermeables (dry bags) o bolsas herméticas reutilizables para empacar tu ropa de cambio, saco de dormir y dispositivos electrónicos dentro del morral. Esta barrera interior garantiza que tu equipo permanezca seco aunque caiga un fuerte aguacero sobre la mochila.",
                "variants": [
                    "Organiza tu equipaje en bolsas estancas dentro de la mochila; es la forma más segura de evitar que el agua arruine tu muda seca y documentos.",
                    "Empacar en bolsas impermeables por categorías mantiene tu ropa protegida y hace mucho más fácil encontrar cada prenda sin desarmar todo el morral."
                ],
                "steps": [
                    [
                        "Guarda tu muda seca de repuesto y tu saco de dormir en bolsas secas con cierre por enrollado.",
                        "Recuerda usar bolsas resistentes y reutilizables, cumpliendo con la prohibición de plásticos de un solo uso de la Resolución 1558 de 2019."
                    ]
                ],
                "detail": "En travesías de alta montaña donde no hay refugios con secadoras, mantener el saco de dormir y la ropa seca es vital para prevenir la hipotermia nocturna.",
                "reflection": "Saber que tu ropa y tu saco de dormir están completamente aislados del agua te da total tranquilidad bajo la lluvia."
            },
            "sources": [SRC_PNN, SRC_RES1558],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.spare_clothing", "preparation.backpack_rain_cover", "preparation.what_not_to_pack"],
            "tags": ["bolsas_secas", "dry_bags", "impermeable", "aislar", "equipaje"]
        },
        {
            "id": "preparation.trekking_poles",
            "label": "bastones de senderismo para la caminata",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirven los bastones de senderismo en el nevado",
                "son necesarios los bastones de trekking para el parque",
                "bastones telescópicos recomendados para montaña",
                "ayudan los bastones en las bajadas empinadas",
                "cuándo usar bastones de caminata en los nevados",
                "es obligatorio llevar bastones al parque",
                "bastones para no cansarme las rodillas al bajar",
                "cómo usar bastones de marcha en terreno con barro",
                "bastones de senderismo para senderos de páramo",
                "para que sirven los bastones de trekking",
                "llevar bastones para subir al nevado santa isabel",
                "are trekking poles useful in Los Nevados",
                "should I use hiking poles for mountain trails",
                "qué ventajas tienen los bastones en senderos de altura"
            ],
            "hard_negatives": [
                "cuáles son las coordenadas geográficas de los picos",
                "dónde conseguir guía registrado en salento",
                "qué hacer si sufro dolor de cabeza intenso en brisas"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Los bastones de senderismo son muy recomendables para caminar en Los Nevados. Proporcionan puntos de apoyo adicionales que mejoran tu equilibrio en terrenos pedregosos o resbalosos, facilitan el ritmo de subida y alivian el impacto sobre rodillas y tobillos durante los descensos pronunciados.",
                "variants": [
                    "Usar un par de bastones telescópicos te ayuda a mantener la estabilidad en caminos quebrados y reduce la fatiga articular al bajar pendientes largas.",
                    "Aunque no son de porte obligatorio individual, los bastones de trekking son una excelente ayuda para cruzar tramos de lodo, arena y rocas con mayor seguridad."
                ],
                "steps": [
                    [
                        "Ajusta la longitud de los bastones para que tu codo quede en un ángulo de 90 grados al apoyarlos en terreno plano.",
                        "Acorta ligeramente su extensión para las subidas empinadas y alárgalos unos centímetros para las bajadas pronunciadas."
                    ]
                ],
                "detail": "En terrenos como las morrenas de Santa Isabel o los descensos por Cocora, los bastones previenen caídas y resbalones sobre barro o gravilla suelta.",
                "reflection": "Caminar con dos apoyos extras te da firmeza y ritmo constante a lo largo de toda la jornada."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.hiking_boots", "preparation.gaiters", "preparation.fitness_training"],
            "tags": ["bastones", "trekking", "senderismo", "equilibrio", "rodillas"]
        },
        {
            "id": "preparation.water_quantity",
            "label": "hidratación recomendada durante la caminata",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "cuánta agua llevar a los nevados",
                "es necesario tomar mucha agua en el parque",
                "cuánta hidratación empacar para la caminata",
                "por qué da tanta sed en alta montaña",
                "hidratación recomendada para visitar el nevado",
                "cuánta agua tomar para no deshidratarse en el frío",
                "debo llevar agua desde la ciudad",
                "hidratarse antes durante y después del ascenso",
                "cuántos litros de líquido empacar para el sendero",
                "cuanta agua llevar para subir a brisas",
                "consejos de hidratacion para alta montana",
                "how much water should I bring to Los Nevados",
                "hydration recommendations for high altitude hike",
                "por qué es tan importante tomar líquidos en el páramo"
            ],
            "hard_negatives": [
                "cuáles son los síntomas del edema pulmonar de altura",
                "dónde puedo comprar recuerdos artesanales en el parque",
                "a qué hora abren el registro en cabaña potosí"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque recomienda mantener una buena hidratación antes, durante y después de la actividad. En alta montaña el aire seco y la respiración acelerada aumentan la pérdida de líquidos sin que lo notes, por lo que debes beber pequeños sorbos continuos durante todo el recorrido.",
                "variants": [
                    "Hidrátate de manera constante a lo largo del sendero: lleva suficiente agua o infusiones en envases reutilizables y bebe con frecuencia sin esperar a tener sed.",
                    "La deshidratación empeora los efectos de la altura; asegúrate de cargar tus recipientes con agua desde el inicio y beber de forma regular en cada parada."
                ],
                "steps": [
                    [
                        "Inicia una buena hidratación desde el día previo a tu visita en la ciudad de origen.",
                        "Durante la caminata bebe sorbos cortos cada 15 a 20 minutos para mantener el equilibrio hídrico sin sobrecargar el estómago."
                    ]
                ],
                "detail": "Las recomendaciones oficiales de Parques Nacionales señalan textualmente: 'Ten una buena hidratación antes, durante y después de la actividad'. Además, la Resolución 207 exige cantimplora en el equipo básico.",
                "reflection": "Beber agua a sorbos continuos te mantiene con energía y ayuda a que tu organismo se adapte mejor a la altitud."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.reusable_bottles", "preparation.thermal_flask", "preparation.electrolytes"],
            "tags": ["agua", "hidratacion", "cantimplora", "liquidos", "altura"]
        },
        {
            "id": "preparation.reusable_bottles",
            "label": "cantimploras y botellas reutilizables permitidas",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué botellas de agua están permitidas en el parque",
                "puedo llevar botellas de plástico desechable al nevado",
                "cantimplora obligatoria según la resolución",
                "en qué recipiente llevar el agua a los nevados",
                "están prohibidas las botellas desechables en el parque",
                "recipientes reutilizables para bebidas en el sendero",
                "cantimplora o termo reutilizable para caminar",
                "botilito de agua para ingresar a los nevados",
                "puedo entrar con botellas plásticas comerciales",
                "que tipo de cantimplora llevar al parque",
                "botellas permitidas por la resolucion 1558",
                "what reusable water bottles are allowed",
                "are single use plastic bottles banned in the park",
                "por qué no se pueden llevar botellas plásticas comunes"
            ],
            "hard_negatives": [
                "cuáles son las tarifas para extranjeros no residentes",
                "cómo llegar al nevado desde la terminal de ibagué",
                "cuándo se fundó el parque nacional los nevados"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Por la Resolución 1558 de 2019 está terminantemente prohibido el ingreso de botellas plásticas desechables de un solo uso. La Resolución 207 exige portar cantimplora; debes transportar tus líquidos exclusivamente en botellas reutilizables, botilitos rígidos o termos.",
                "variants": [
                    "Lleva tu agua en cantimploras o botellas reutilizables de aluminio o plástico duro; no se permite entrar con botellas plásticas desechables comerciales.",
                    "Los envases de agua desechables están prohibidos en el parque; utiliza cantimploras o termos lavables que puedas recargar y retornar contigo."
                ],
                "steps": [
                    [
                        "Llena tus cantimploras o botellas reutilizables en tu hotel o ciudad de partida antes de salir.",
                        "Verifica que las tapas cierren de forma hermética para evitar fugas de líquido dentro de tu morral."
                    ]
                ],
                "detail": "La Resolución 1558 de 2019 de Parques Nacionales prohíbe los plásticos de un solo uso en todas las áreas protegidas para evitar la contaminación de ecosistemas frágiles.",
                "reflection": "Usar recipientes reutilizables cuida el páramo y garantiza que no dejes ningún rastro de plástico en el parque."
            },
            "sources": [SRC_RES1558, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.water_quantity", "preparation.thermal_flask", "preparation.what_not_to_pack"],
            "tags": ["cantimplora", "reutilizable", "botella", "plastico", "norma"]
        },
        {
            "id": "preparation.hydration_bladder_freeze",
            "label": "cuidado de bolsa de hidratación en frío",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve una bolsa de hidratación en el nevado",
                "se congela la manguera del camelbak en la montaña",
                "cómo evitar que se congele el agua en la manguera",
                "problemas con vejiga de agua en clima bajo cero",
                "usar camelbak para senderismo en los nevados",
                "consejos para bolsa de agua en alta montaña",
                "por qué no sale agua de la manguera del morral",
                "manguera congelada por heladas en el páramo",
                "sirve vejiga de hidratación en el sendero a brisas",
                "como descongelar la valvula de la bolsa de agua",
                "bolsa de agua en la espalda para caminar en frio",
                "can I use a hydration bladder in freezing weather",
                "how to prevent hydration hose from freezing in park",
                "qué precauciones tener con la bolsa de hidratación"
            ],
            "hard_negatives": [
                "cuántos refugios de emergencia tiene el parque",
                "cuáles son las restricciones para mujeres gestantes",
                "dónde tomar transporte hacia villamaría"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Puedes usar bolsa de hidratación, pero ten en cuenta que a temperaturas cercanas o inferiores a 0 ºC el agua estancada en la manguera exterior y la boquilla se congela con facilidad. Tras beber, sopla el aire de vuelta por la manguera para empujar el líquido al interior protegido de la mochila.",
                "variants": [
                    "Si llevas bolsa de hidratación en la mochila, sopla aire hacia la manguera después de cada sorbo para que el agua no se congele dentro del tubo expuesto al viento gélido.",
                    "En madrugadas muy frías las mangueras de las bolsas de agua suelen bloquearse con hielo; llevar además una cantimplora clásica dentro del morral te asegura acceso al agua."
                ],
                "steps": [
                    [
                        "Sopla el aire tras beber para devolver el agua a la bolsa dentro del morral.",
                        "Si la manguera cuenta con funda aislante térmica, mantenla cerrada para reducir el impacto del viento."
                    ]
                ],
                "detail": "En áreas altas y campamentos las temperaturas descienden con frecuencia por debajo del punto de congelación, afectando mangueras y válvulas exteriores de agua.",
                "reflection": "Conocer este pequeño truco de soplar la manguera te evita quedarte sin poder beber durante las horas más frías."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.water_quantity", "preparation.reusable_bottles", "preparation.thermal_flask"],
            "tags": ["hidratacion", "camelbak", "congelar", "manguera", "frio"]
        },
        {
            "id": "preparation.thermal_flask",
            "label": "termo para bebidas calientes en montaña",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve llevar un termo al parque los nevados",
                "debo llevar termo con agua de panela caliente",
                "termo metálico para bebidas calientes en páramo",
                "vale la pena cargar termo térmico a la montaña",
                "llevar café o té caliente para el nevado",
                "qué bebidas calientes llevar al parque",
                "termo para mantener agua tibia en el frío",
                "conviene llevar termo con líquido caliente a brisas",
                "termo insulado para caminatas de alta montaña",
                "termo para no tomar agua fria en el paramo",
                "bebidas calientes recomendadas para el sendero",
                "should I bring an insulated thermal flask",
                "hot tea or panela in a thermos for cold hike",
                "por qué es agradable tomar algo tibio en las paradas"
            ],
            "hard_negatives": [
                "cuáles son las señales de congelamiento en los dedos",
                "dónde tramitar el permiso para acampar en otún",
                "cuál es la historia de la erupción de 1985"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Llevar un termo con agua de panela, té o infusión caliente es muy reconfortante durante las paradas de descanso en el clima frío del parque. Beber algo tibio ayuda a hidratarte de forma agradable sin tener que consumir agua helada mientras descansas expuesto al viento.",
                "variants": [
                    "Empacar un termo con bebida caliente te brinda una sensación agradable de confort en descansos y miradores fríos a más de 4.000 metros.",
                    "Un termo térmico conserva tus infusiones calientes durante horas; es un excelente complemento de tu cantimplora de agua para reanimarte en las pausas."
                ],
                "steps": [
                    [
                        "Llena tu termo con agua de panela o té bien caliente antes de salir hacia el parque en la mañana.",
                        "Bébela en pequeños sorbos durante las paradas de inducción o descansos de caminata para disfrutar su calidez."
                    ]
                ],
                "detail": "En sectores como Brisas o Santa Isabel las temperaturas habituales oscilan entre -3 °C y 14 °C; tener una bebida caliente a mano hace mucho más acogedor el recorrido.",
                "reflection": "Tomar un sorbo de agua de panela caliente contemplando el paisaje de páramo es uno de los mejores momentos de la visita."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.water_quantity", "preparation.reusable_bottles", "preparation.trail_snacks"],
            "tags": ["termo", "bebidas_calientes", "panela", "confort", "frio"]
        },
        {
            "id": "preparation.trail_snacks",
            "label": "snacks energéticos y alimentos ligeros calóricos",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué comida llevar al parque los nevados",
                "snacks recomendados para caminar en el nevado",
                "qué refrigerios empacar para el sendero",
                "alimentos energéticos para alta montaña",
                "sirve llevar bocadillo de guayaba y frutos secos",
                "comida de marcha ligera para no cansarse",
                "qué pasabocas llevar para subir a brisas",
                "alimentos calóricos listos para consumir",
                "qué comer durante la caminata en páramo",
                "comida ligera para el ascenso al nevado",
                "alimentos obligatorios segun la resolucion 207",
                "what trail snacks should I pack for hiking",
                "energy food and snacks for high altitude trek",
                "cuáles alimentos aportan energía rápida en montaña"
            ],
            "hard_negatives": [
                "cuál es la diferencia entre páramo y superpáramo",
                "dónde puedo ver osos de anteojos en el parque",
                "cómo consultar las tarifas de entrada actualizadas"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 exige portar alimentos ligeros listos para consumir y ricos en calorías. La ficha del parque recomienda snacks energéticos como bocadillos de guayaba, frutos secos, maní, chocolates, panela o barritas de cereales, que aportan energía rápida de fácil digestión durante la marcha.",
                "variants": [
                    "Empaca refrigerios calóricos y ligeros que no requieran preparación: bocadillo, frutos secos, uvas pasas y chocolate para comer en pequeñas porciones durante el camino.",
                    "Llevar comida de marcha rica en carbohidratos es obligatorio y fundamental para mantener tus niveles de energía frente al esfuerzo y el frío de la montaña."
                ],
                "steps": [
                    [
                        "Distribuye los pasabocas en bolsillos exteriores de tu morral para comer pequeñas raciones cada hora sin detenerte por largo tiempo.",
                        "Recuerda empacar los alimentos en recipientes reutilizables y retornar todos los envoltorios en tu bolsa de basura personal."
                    ]
                ],
                "detail": "El numeral 6.1 de la Resolución 207 de 2023 exige de forma expresa 'alimentos ligeros listos para consumir y ricos en calorías' dentro del equipo obligatorio para senderismo.",
                "reflection": "Comer pequeñas porciones de frutos secos o bocadillo a lo largo del sendero te ayuda a mantener un ritmo firme sin fatiga."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.pre_hike_meal", "preparation.water_quantity", "preparation.trail_meals_multiday"],
            "tags": ["snacks", "comida", "calorias", "bocadillo", "energia"]
        },
        {
            "id": "preparation.pre_hike_meal",
            "label": "alimentación previa al inicio del ascenso",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué desayunar antes de subir al nevado",
                "comida recomendada antes de ir a los nevados",
                "debo desayunar fuerte antes de la caminata",
                "qué alimentos evitar antes de subir a la montaña",
                "desayuno liviano para evitar malestares en altura",
                "puedo comer lácteos o grasas antes de subir",
                "consejos de alimentación antes de salir al parque",
                "qué comer en manizales antes de subir a brisas",
                "desayuno energético y digestivo para el páramo",
                "que desayunar para no marearse en el nevado",
                "alimentacion previa recomendada por parques",
                "what should I eat for breakfast before the hike",
                "recommended meal before ascending to high altitude",
                "cómo debe ser la alimentación antes de iniciar la ruta"
            ],
            "hard_negatives": [
                "a qué altitud comienza el mal agudo de montaña",
                "cuáles son los números de emergencia de la policía",
                "dónde tramitar licencias para fotografía comercial"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque recomienda alimentarte bien antes de la actividad. Toma un desayuno balanceado y de fácil digestión rico en carbohidratos (avena, tostadas, fruta) al menos una hora antes de iniciar el ascenso; evita fritos pesados, carnes grasas o exceso de lácteos que entorpezcan la digestión en altura.",
                "variants": [
                    "Desayuna alimentos nutritivos y livianos antes de subir: la digestión se vuelve más lenta en la altura, por lo que las comidas grasosas pueden provocarte náuseas o pesadez.",
                    "Come bien antes de partir pero sin sobrecargar tu estómago; prioriza cereales, panela y frutas no ácidas para contar con reservas de energía desde el inicio."
                ],
                "steps": [
                    [
                        "Desayuna con anticipación suficiente antes de abordar el transporte hacia el parque.",
                        "Evita alimentos muy condimentados o pesados que causen malestar estomacal durante las curvas de la carretera de montaña."
                    ]
                ],
                "detail": "A mayor altitud y menor disponibilidad de oxígeno el flujo sanguíneo prioriza los músculos y el cerebro, haciendo que digestiones muy pesadas incrementen la fatiga y el mareo.",
                "reflection": "Empezar la jornada con un desayuno liviano y nutritivo prepara a tu cuerpo para rendir al máximo en el sendero."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.trail_snacks", "preparation.water_quantity", "preparation.fitness_training"],
            "tags": ["desayuno", "alimentacion", "digestion", "energia", "previo"]
        },
        {
            "id": "preparation.trail_meals_multiday",
            "label": "alimentación para travesías de varios días",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué comida empacar para travesía de varios días",
                "alimentación para acampar en el parque los nevados",
                "comida deshidratada o liviana para travesía",
                "cómo planear la comida para varios días en montaña",
                "qué llevar para cocinar en el campamento",
                "menú recomendado para trekking de pernocta en páramo",
                "comida nutritiva y de poco peso para acampar",
                "víveres para travesía hacia la laguna del otún",
                "planificación de raciones diarias para campamento",
                "que alimentos llevar para cocinar en la carpa",
                "alimentacion apropiada para bajas temperaturas pnn",
                "what food should I pack for a multiday trek",
                "meal planning for high altitude mountain camping",
                "qué víveres no se dañan con el frío en travesías"
            ],
            "hard_negatives": [
                "cuáles son las zonas permitidas para hacer camping",
                "cuánto cobran los guías locales por día",
                "cómo identificar la danta de montaña en el bosque"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque señala que para acampar debes llevar alimentación apropiada para bajas temperaturas. Elige alimentos no perecederos, livianos y de cocción rápida (arroz precocido, pastas, sopas deshidratadas, atún, frutos secos, avena) que aporten suficientes calorías sin requerir mucho combustible.",
                "variants": [
                    "Planifica tus comidas por raciones diarias priorizando carbohidratos ligeros y fáciles de preparar en estufa portátil con agua hirviendo a temperaturas frías.",
                    "Para travesías largas empaca alimentos densos en energía que no pesen demasiado en la mochila y que se preparen rápidamente para economizar gas de cocina."
                ],
                "steps": [
                    [
                        "Calcula las raciones por cada día de marcha y añade una comida adicional de reserva por si surge algún retraso en la ruta.",
                        "Transporta los alimentos en recipientes reutilizables o bolsas selladas, cumpliendo la prohibición de empaques plásticos desechables."
                    ]
                ],
                "detail": "En alta montaña el agua hierve a menor temperatura debido a la baja presión atmosférica, por lo que los alimentos crudos tardan más tiempo en cocinarse por completo.",
                "reflection": "Planificar bien tus comidas de campamento te asegura recuperar fuerzas cada noche sin cargar peso muerto."
            },
            "sources": [SRC_PNN, SRC_RES1558],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.camp_stove", "preparation.cookware_utensils", "preparation.trail_snacks"],
            "tags": ["comida_travesia", "campamento", "viveres", "nutricion", "calorias"]
        },
        {
            "id": "preparation.electrolytes",
            "label": "sales de hidratación para la caminata",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "sirve llevar suero oral o sales al nevado",
                "debo tomar electrolitos durante la caminata",
                "suero de hidratación oral para alta montaña",
                "bebidas isotónicas recomendadas para el parque",
                "cuándo tomar sales de rehidratación en el sendero",
                "sales minerales para evitar calambres en el frío",
                "es bueno llevar sobres de suero oral en el morral",
                "electrolitos en polvo para disolver en la cantimplora",
                "hidratación con electrolitos para el esfuerzo físico",
                "sirven las bebidas rehidratantes para el nevado",
                "electrolitos para caminar en altura los nevados",
                "should I take electrolyte drinks during the hike",
                "oral rehydration salts for high mountain trekking",
                "por qué ayudan las sales minerales en el ascenso"
            ],
            "hard_negatives": [
                "cuáles son los medicamentos autorizados para el soroche",
                "dónde conseguir oxígeno de emergencia en manizales",
                "cómo se formaron los glaciares de los nevados"
            ],
            "entities": {"trip_duration": ["pasadia", "travesia"]},
            "needs": [],
            "answer": {
                "short": "Llevar sobres de sales de rehidratación oral o electrolitos en polvo para disolver en tu cantimplora es muy útil. El esfuerzo físico en altura acelera la pérdida de sales minerales por transpiración y respiración; reponerlas ayuda a mantener el balance hídrico y prevenir calambres o fatiga.",
                "variants": [
                    "Disolver electrolitos en parte de tu agua de consumo ayuda a reponer las sales que pierdes por el esfuerzo físico prolongado en el sendero.",
                    "Los sobres de suero oral son ligeros de cargar y complementan tu hidratación en jornadas largas o si sientes fatiga muscular por el ascenso."
                ],
                "steps": [
                    [
                        "Disuelve un sobre de sales de hidratación en una de tus botellas reutilizables de agua según las indicaciones del empaque.",
                        "Bébela alternando con agua pura a lo largo de las horas de mayor exigencia física de la caminata."
                    ]
                ],
                "detail": "La hidratación adecuada recomendada por Parques Nacionales es más eficiente cuando se reponen los minerales perdidos durante caminatas de varias horas en terrenos empinados.",
                "reflection": "Mantener tus sales equilibradas te ayuda a que tus músculos respondan con soltura en los tramos más empinados."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": None,
            "valid_until": None,
            "related": ["preparation.water_quantity", "preparation.reusable_bottles", "preparation.trail_snacks"],
            "tags": ["electrolitos", "suero", "hidratacion", "sales", "calambres"]
        },
        {
            "id": "preparation.mountain_tent",
            "label": "carpa técnica de montaña para acampar",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué carpa llevar para acampar en los nevados",
                "sirve una carpa playera común en el parque",
                "carpa de tres o cuatro estaciones para montaña",
                "especificaciones técnicas de carpas para acampar",
                "carpa resistente a vientos y heladas en páramo",
                "carpa obligatoria para temperaturas bajo cero",
                "qué tipo de carpa exige la resolución 207",
                "carpa de alta montaña para acampar en otún",
                "carpa con cubretecho impermeable completo",
                "que carpa comprar para el parque los nevados",
                "carpa para resistir lluvia y viento en el nevado",
                "what tent is required for camping in Los Nevados",
                "three or four season mountain tent for freezing cold",
                "cómo debe ser la carpa para pernoctar en el parque"
            ],
            "hard_negatives": [
                "a qué hora abren el sector brisas para vehículos",
                "cuáles son los volcanes que conforman el parque",
                "cómo reservar cupo de pernocta en cabaña potosí"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "La Resolución 207 estipula que las carpas utilizadas deben tener especificaciones técnicas para alta montaña, conocidas como carpas de tres o cuatro estaciones para temperaturas menores a cero grados centígrados. No se permiten carpas playeras o livianas sin sobrecarpa completa.",
                "variants": [
                    "Para acampar en el parque es obligatorio usar carpas técnicas de montaña (tres o cuatro estaciones) que soporten vientos fuertes, lluvia intensa y heladas bajo cero.",
                    "La normativa exige carpas con estructura firme y doble techo completo aptas para frío extremo; una carpa común puede colapsar o filtrarse con las heladas nocturnas."
                ],
                "steps": [
                    [
                        "Verifica que la carpa sea autoportante con varillas resistentes de aluminio o fibra de alta resistencia y sobretecho hasta el suelo.",
                        "Instala la carpa únicamente en las zonas delimitadas autorizadas por el personal del parque, orientando la parte más baja hacia la dirección del viento."
                    ]
                ],
                "detail": "La Resolución 207 de 2023 señala expresamente: 'Las carpas utilizadas deben tener las especificaciones técnicas para alta montaña; conocidas como carpas de tres y cuatro estaciones para temperaturas menores a cero grados centígrados'.",
                "reflection": "Una carpa de alta montaña bien asegurada es tu refugio seguro frente a las noches más frías de la cordillera."
            },
            "sources": [SRC_RES207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.sleeping_bag", "preparation.sleeping_pad", "preparation.camp_hygiene"],
            "tags": ["carpa", "camping", "tres_estaciones", "viento", "frio"]
        },
        {
            "id": "preparation.sleeping_bag",
            "label": "saco de dormir para bajas temperaturas",
            "kind": "procedure",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "qué saco de dormir llevar a los nevados",
                "sirve un sleeping normal para acampar en el parque",
                "sleeping para temperaturas bajo cero en páramo",
                "saco de dormir de pluma o fibra sintética",
                "sleeping térmico adecuado para la laguna del otún",
                "qué temperatura debe soportar el sleeping bag",
                "saco de dormir obligatorio para campamento",
                "sleeping abrigado para pernoctar en alta montaña",
                "sleeping de confort negativo para el nevado",
                "que sleeping comprar para acampar en el parque",
                "saco de dormir para heladas nocturnas en los nevados",
                "what sleeping bag temperature rating do I need",
                "sleeping bag for freezing temperatures in Los Nevados",
                "cómo elegir el saco de dormir para acampar en el páramo"
            ],
            "hard_negatives": [
                "cuáles son las tarifas de ingreso para extranjeros",
                "dónde tomar transporte público en salento hacia cocora",
                "cómo solicitar rescate aéreo en la alta montaña"
            ],
            "entities": {"trip_duration": ["travesia"]},
            "needs": [],
            "answer": {
                "short": "La ficha del parque señala que para acampar debes llevar un saco de dormir (sleeping) apropiado para bajas temperaturas. En los campamentos las noches suelen alcanzar temperaturas menores a cero grados centígrados, por lo que tu saco debe ofrecer aislamiento térmico para frío extremo.",
                "variants": [
                    "Empaca un sleeping técnico diseñado para soportar temperaturas bajo cero; los sacos delgados de clima cálido no protegen del frío nocturno del páramo.",
                    "Llevar un saco de dormir abrigado es indispensable para acampar con seguridad; asegúrate de transportarlo dentro de una bolsa completamente impermeable."
                ],
                "steps": [
                    [
                        "Elige sacos de dormir tipo momia con capucha ajustable para evitar que el calor escape por el cuello y la cabeza.",
                        "Protégelo dentro de una bolsa seca impermeable dentro de tu morral para que nunca se humedezca con la lluvia durante el día."
                    ]
                ],
                "detail": "Las recomendaciones de Parques Nacionales indican expresamente: 'Si vas a acampar en las zonas permitidas, lleva carpa, sleeping, material de cocina y alimentación apropiada para bajas temperaturas'.",
                "reflection": "Dormir caliente y protegido te garantiza recuperar energías para la siguiente jornada de travesía."
            },
            "sources": [SRC_PNN, SRC_RES207],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": ["preparation.sleeping_pad", "preparation.mountain_tent", "preparation.dry_bags"],
            "tags": ["sleeping", "saco_dormir", "frio", "campamento", "aislamiento"]
        }
    ]
