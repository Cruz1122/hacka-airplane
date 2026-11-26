"""Corrected access entries, north approach and vehicle rules. Do not import part1–part4."""

from __future__ import annotations

from common import ANEXO, FICHA, GUIDE_2016, SGC, entry

PICO = (
    "Si entras a Brisas en noviembre, un fin de semana o puente, revisa el pico y placa "
    "ambiental del Tolima, Resolución 1815 del 24 de julio de 2026, de 5:00 a. m. a 4:00 p. m."
)
PICO_V = (
    "En noviembre, fines de semana y puentes, el acceso Brisas–Valle de las Tumbas tiene pico y placa "
    "ambiental del Tolima de 5:00 a. m. a 4:00 p. m., Resolución 1815 del 24 de julio de 2026."
)

N1 = [
    entry(
        id="access.how_to_choose_sector",
        label="elegir la vía según tu ciudad",
        kind="procedure",
        examples=[
            "por dónde entro a los nevados",
            "qué vía me sirve si todavía no escojo sector",
            "salgo mañana y no sé cuál portería me queda cerca",
            "como hago pa llegar, hay varias entradas",
            "no se si me toca caldas o tolima",
            "ayúdame a escoger la puerta según mi ciudad",
            "which entrance should I use for Los Nevados",
            "I have not picked a sector, how do I choose the road",
            "voy en carro, por qué lado se entra al parque",
            "me reciben en cualquier caseta o cada sector tiene la suya",
            "dime las entradas antes de comprar el pasaje",
            "de qué pueblo sale cada camino al parque",
        ],
        hard_negatives=[
            "cuánto cuesta entrar por Brisas",
            "a qué hora abren las porterías mañana",
            "qué capas de ropa llevo a 4000 metros",
        ],
        short=(
            "No hay una sola portería: se llega por tierra y cada sector tiene la suya. "
            "Brisas sale desde Manizales o Murillo; el Cisne, desde Villamaría o Santa Rosa de Cabal; "
            "la Laguna del Otún, por Potosí o por Pereira hasta El Cedral; el sur, por Cocora, Juntas o Palomar. "
            + PICO
        ),
        variants=[
            "Primero elige la puerta, porque no forman un solo paseo: Manizales o Murillo hasta Brisas, "
            "Villamaría o Santa Rosa hasta Potosí y Santa Bárbara, Pereira por El Cedral, y Cocora, Juntas o Palomar al sur. "
            "Dime la ciudad de salida. " + PICO_V
        ],
        steps=[
            ["Desde Manizales la referencia es la carretera hacia Bogotá por Letras y luego el corredor La Esperanza–Murillo hasta Brisas. Desde Murillo se toma ese mismo corredor. " + PICO],
            ["Desde Villamaría o Santa Rosa de Cabal se llega por vías destapadas a la cabaña Potosí y al alto de Santa Bárbara."],
            ["Desde Pereira caminas después de La Florida y El Cedral. Desde Salento sigues la vereda Cocora; desde Ibagué, la vereda Juntas; desde Anzoátegui, la vereda Palomar."],
        ],
        sources=[FICHA],
        related=["access.four_sector_gates", "access.gateway_towns", "access.always_by_land"],
        tags=["entrada", "sector", "ciudad", "vía"],
        needs=["origin"],
        entities={"origin": ["manizales", "murillo", "villamaria", "santa_rosa", "pereira", "salento", "ibague", "anzoategui"]},
    ),
    entry(
        id="access.four_sector_gates",
        label="cuatro sectores y sus entradas",
        kind="explanation",
        examples=[
            "cuántas entradas tiene el parque",
            "cuáles son los cuatro sectores para entrar",
            "brisas cisne otun y tolima son porterías distintas",
            "los cuatro accesos como se llaman",
            "me explicas las puertas del parque sin el paseo",
            "is there more than one gate at Los Nevados",
            "name the four entrances and where each one starts",
            "sector brisas kumanday por donde se entra",
            "poleka kasue y dulima son la misma caseta",
            "quiero la lista corta de porterías",
            "en qué sector queda cada volcán para entrar",
            "no confundir el sector con el pueblo, cuales hay",
        ],
        hard_negatives=[
            "cuántas hectáreas tiene el parque",
            "puedo pasar de Brisas al Otún en el mismo carro",
            "qué animales hay en cada sector",
        ],
        short=(
            "La página publica cuatro sectores con entradas distintas: Brisas–Kumanday, por el corredor La Esperanza–Murillo; "
            "Cisne–Poleka Kasue, desde Villamaría o Santa Rosa hasta Potosí y Santa Bárbara; "
            "Laguna del Otún, por Potosí o por Pereira hasta El Cedral; y Quindío–Dulima, por Cocora, Juntas o Palomar. "
            + PICO
        ),
        variants=[
            "Son cuatro puertas, no una: norte por La Esperanza–Murillo a Brisas, Cisne por las destapadas hasta Potosí y Santa Bárbara, "
            "Otún también por Potosí o caminando desde El Cedral, y el Tolima por Cocora, Juntas o Palomar. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.how_to_choose_sector", "access.departments_of_access", "access.where_road_ends"],
        tags=["sectores", "portería", "brisas", "otún"],
    ),
    entry(
        id="access.departments_of_access",
        label="entradas en los cuatro departamentos",
        kind="fact",
        examples=[
            "por qué departamento se entra",
            "el parque se entra por caldas",
            "risaralda tiene portería o solo se ve de lejos",
            "acceso por el quindio cual es",
            "desde el tolima por donde subo",
            "which department has a gate",
            "can I enter from Quindío and from Tolima",
            "caldas y tolima tienen entradas distintas",
            "santa rosa es risaralda, esa vía sirve",
            "salento queda en el quindio, ahi empiezo",
            "murillo es tolima pero no se si es el sur",
            "los cuatro departamentos y su puerta",
        ],
        hard_negatives=[
            "qué departamentos comparten el polígono del parque",
            "la capital de Caldas cuál es",
            "extensión del parque en hectáreas",
        ],
        short=(
            "La página ubica puntos de acceso en Caldas, Risaralda, Quindío y Tolima. "
            "Por Caldas se va a Brisas y al Cisne; por Risaralda, a Potosí desde Santa Rosa y a El Cedral desde Pereira; "
            "por el Quindío, a Salento y Cocora; por el Tolima, a Murillo hacia el norte y a Juntas o Anzoátegui hacia el sur. "
            + PICO
        ),
        variants=[
            "No es el mapa del límite: es por dónde se entra. Caldas lleva a Brisas o al Cisne, Risaralda a Potosí o a El Cedral, "
            "el Quindío a Cocora y el Tolima a Murillo, Juntas o Palomar. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.four_sector_gates", "access.gateway_towns", "access.from_ibague_choose"],
        tags=["caldas", "risaralda", "quindío", "tolima"],
    ),
    entry(
        id="access.gateway_towns",
        label="pueblos desde donde sale la vía",
        kind="fact",
        examples=[
            "de qué pueblos sale la vía al parque",
            "qué cascos sirven de punto de partida",
            "manizales murillo y salento están en la ruta",
            "anzoategui cuenta como salida",
            "mi pueblo no sale en la lista, qué hago",
            "which towns does the park page use as trailheads",
            "is Armenia the published start of the Quindío road",
            "villamaria y santa rosa si estan escritas",
            "pereira e ibague son bases de entrada",
            "hay una lista corta de municipios de salida",
            "salgo de un pueblo chiquito, hay camino publicado",
            "no quiero un atajo, dime los pueblos que si nombra la pagina",
        ],
        hard_negatives=[
            "en qué pueblos se puede dormir cerca",
            "hay cajero en Murillo",
            "el nombre indígena del Ruiz",
        ],
        short=(
            "En cómo llegar, la página arma las rutas desde Manizales, Murillo, Villamaría, Santa Rosa de Cabal, Pereira, Salento, Ibagué y Anzoátegui. "
            "Si el tuyo no está, no hay aquí una ruta verificada ni un desvío para inventar: usa una de esas puertas y el operador de ese sector. "
            + PICO
        ),
        variants=[
            "Los puntos de salida publicados son esos ocho. Otro pueblo no trae un camino verificado en esta respuesta. "
            "Entra por la puerta del sector y coordínala con un operador registrado. " + PICO_V
        ],
        detail=(
            "La reglamentación transitoria de diciembre de 2023 describe la vía Armenia–Salento–Valle del Cocora como aproximación al Quindío. "
            "En ese mismo documento el texto dice 25 km y la tabla 37 km, así que ninguna de las dos se usa como distancia. "
            "La página actual empieza el acceso del Quindío en Salento, por la vereda Cocora."
        ),
        sources=[FICHA, ANEXO],
        related=["access.how_to_choose_sector", "access.no_published_gate_towns", "access.always_by_land"],
        tags=["pueblos", "salida", "manizales", "salento"],
    ),
    entry(
        id="access.always_by_land",
        label="al parque solo se llega por tierra",
        kind="fact",
        examples=[
            "se puede llegar en avión al parque",
            "hay vuelo hasta la portería",
            "hay pista en brisas",
            "llego en helicoptero al valle",
            "el parque tiene aeropuerto",
            "can I fly directly to the gate",
            "is there an airstrip at Los Nevados",
            "solo hay transporte terrestre, cierto",
            "dejo el avión en manizales y sigo por carretera",
            "no hay vuelo al nevado, toca por tierra",
            "como se llega si no hay aeropuerto adentro",
            "barco o avioneta sirven para entrar",
        ],
        hard_negatives=[
            "a qué aeropuerto llega el vuelo a Manizales",
            "horario del bus intermunicipal",
            "precio del transporte de UTON",
        ],
        short=(
            "Al parque se llega siempre por transporte terrestre. La página no publica aeropuerto, pista ni vuelo hasta una portería. "
            "Llegas a la ciudad o vereda de la puerta que elegiste y sigues esa carretera o ese camino. " + PICO
        ),
        variants=[
            "No hay un acceso aéreo publicado hasta la caseta. El camino es por tierra, hasta la puerta del sector que vas a visitar. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.no_public_bus", "access.from_bogota", "access.from_medellin"],
        tags=["terrestre", "avión", "portería"],
    ),
    entry(
        id="access.from_manizales",
        label="cómo llegar desde Manizales",
        kind="procedure",
        examples=[
            "ruta manizales brisas",
            "qué carretera agarro en Manizales hacia el parque",
            "salgo del centro de Manizales, por dónde sigo",
            "via desde manizales al centro de visitantes",
            "cual via cojo pa brisas saliendo de manizales",
            "voy en carro desde Manizales, dónde me desvío",
            "indicaciones de Manizales al sector norte",
            "de manizales al valle de las tumbas por cual lado",
            "how do I drive from Manizales to the Brisas gate",
            "leaving Manizales, which road reaches the park entrance",
            "manizales letras y despues el corredor, va bien",
            "no quiero quedarme en la ciudad, sigo hacia el nevado",
        ],
        hard_negatives=[
            "cuánto cuesta el ingreso desde Manizales",
            "a qué hora es la última inducción en Brisas",
            "hace frío en Letras, qué chaqueta llevo",
            "el Ruiz está en alerta naranja hoy",
        ],
        short=(
            "Desde Manizales toma la carretera hacia Bogotá por Letras y, en el parador La Esperanza, sigue el corredor La Esperanza–Murillo hasta el centro de visitantes Brisas. "
            "No te guíes por un solo poste de kilómetro: los documentos oficiales no coinciden. " + PICO
        ),
        variants=[
            "Sales de Manizales por la vía a Bogotá, giras en La Esperanza hacia el corredor de Murillo y llegas a Brisas. "
            "El número del kilómetro no es único, así que sigue esos nombres. " + PICO_V
        ],
        detail=(
            "La página actual nombra la vía Letras y el corredor, sin poste. "
            "La guía en inglés de abril de 2016 pone el giro en el kilómetro 23 y luego 14 km hasta el cruce de Murillo. "
            "La reglamentación transitoria de diciembre de 2023 dice el kilómetro 45 en La Esperanza o El Ocho, y 1 km entre el cruce de Murillo y Brisas. "
            "El Servicio Geológico, en una página sin fecha de publicación visible, habla de unos 18 km por la vía La Esperanza–Murillo antes del desvío a Brisas."
        ),
        sources=[FICHA, ANEXO, SGC, GUIDE_2016],
        related=["access.letras_highway", "access.esperanza_murillo_corridor", "access.brisas_visitor_center"],
        tags=["manizales", "letras", "brisas"],
        entities={"origin": ["manizales"], "sector": ["brisas"]},
    ),
    entry(
        id="access.from_murillo",
        label="cómo llegar desde Murillo",
        kind="procedure",
        examples=[
            "cómo salir de Murillo hacia el parque",
            "de la cabecera de Murillo a Brisas",
            "murillo queda antes de la portería",
            "corredor esperanza murillo saliendo del pueblo",
            "entro por murillo al sector norte",
            "how do I get from Murillo to Brisas",
            "is the town of Murillo the gate",
            "voy en carro desde murillo, falta mucho",
            "murillo tolima hacia el centro de visitantes",
            "el mismo corredor que viene de manizales, lo tomo al revés",
            "desde el casco de murillo cual via",
            "no es el nevado del tolima, busco brisas",
        ],
        hard_negatives=[
            "hay hotel en el casco de Murillo",
            "tarifa para entrar por el Tolima",
            "sendero del Nevado del Tolima desde Murillo",
        ],
        short=(
            "Desde la cabecera de Murillo tomas el corredor La Esperanza–Murillo hasta el centro de visitantes Brisas. "
            "Murillo no es la portería: todavía falta ese tramo, el mismo que también se usa desde Manizales. " + PICO
        ),
        variants=[
            "Sales del pueblo de Murillo por el corredor hacia La Esperanza y entras al parque en Brisas, no en la plaza. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.esperanza_murillo_corridor", "access.murillo_is_north_not_tolima", "access.brisas_visitor_center"],
        tags=["murillo", "brisas", "corredor"],
        entities={"origin": ["murillo"], "sector": ["brisas"]},
    ),
    entry(
        id="access.esperanza_murillo_corridor",
        label="corredor vial La Esperanza Murillo",
        kind="explanation",
        examples=[
            "qué es el corredor la esperanza murillo",
            "la esperanza es la portería o solo el parador",
            "el ocho queda sobre la vía a bogotá",
            "por ese corredor se llega a brisas",
            "sirve viniendo de manizales y tambien de murillo",
            "what is the La Esperanza–Murillo corridor",
            "do I enter the park at the La Esperanza stop",
            "despues del parador hacia donde sigo",
            "el corredor norte como se llama",
            "no me quiero bajar en el restaurante de la esperanza",
            "via esperanza murillo hasta el centro de visitantes",
            "el ocho y la esperanza son el mismo referente",
        ],
        hard_negatives=[
            "menú del parador La Esperanza",
            "hay peaje en el corredor",
            "clima de mañana en Murillo",
        ],
        short=(
            "El corredor La Esperanza–Murillo es la vía que la página usa para Brisas, vengas de Manizales o de Murillo. "
            "La Esperanza, o El Ocho, es el parador de referencia sobre la carretera hacia Bogotá, no la portería. "
            "La portería es el centro de visitantes Brisas. " + PICO
        ),
        variants=[
            "No te registres en el parador. La Esperanza marca el desvío; Brisas es la entrada, por el corredor que también llega a Murillo. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.from_manizales", "access.from_murillo", "access.ignore_single_kilometer"],
        tags=["esperanza", "murillo", "corredor"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.letras_highway",
        label="carretera Manizales Bogotá por Letras",
        kind="fact",
        examples=[
            "vía letras es la de manizales a bogotá",
            "por letras se sale hacia el parque",
            "la carretera manizales bogota pasa por letras",
            "letras queda antes de brisas",
            "cojo la via a bogota y despues el corredor",
            "is Letras the Manizales–Bogotá road",
            "do I stay on the Letras highway until the gate",
            "despues de letras falta el desvio",
            "la via nacional hacia bogota sirve de referencia",
            "no es una trocha, es la carretera de letras",
            "salgo por letras rumbo al nevado",
            "manizales bogota por donde dicen letras",
        ],
        hard_negatives=[
            "peajes de la vía Manizales Bogotá",
            "estado de la vía al Llano",
            "distancia en bus Bogotá Manizales",
        ],
        short=(
            "Vía Letras es el nombre de uso de la carretera Manizales–Bogotá. La página la usa como referencia para salir de Manizales hacia el corredor La Esperanza–Murillo y, por ahí, a Brisas. "
            "Letras no es la portería: después todavía tomas ese corredor. " + PICO
        ),
        variants=[
            "Tomas la Manizales–Bogotá, la que llaman Letras, y más adelante el corredor hacia Brisas. Quedarte en Letras no es entrar al parque. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.letras_not_the_gate", "access.from_manizales", "access.from_bogota"],
        tags=["letras", "bogotá", "carretera"],
        entities={"origin": ["manizales", "bogota"], "sector": ["brisas"]},
    ),
    entry(
        id="access.letras_not_the_gate",
        label="Letras no es la entrada",
        kind="fact",
        examples=[
            "letras es la entrada del parque",
            "me bajo en letras y ya entré",
            "la portería queda en letras",
            "vi el letrero de letras, es la caseta",
            "si llego a letras ya estoy en brisas",
            "is Letras the park entrance",
            "I thought the gate was at Letras",
            "letras o brisas, cual es la caseta",
            "no quiero registrarme en el punto equivocado",
            "despues de letras falta camino",
            "el control del parque no es letras",
            "donde esta la porteria de verdad si no es letras",
        ],
        hard_negatives=[
            "hay cabañas para dormir en Letras",
            "altura del páramo de Letras",
            "restaurante en la vía Letras",
        ],
        short=(
            "Letras no es la entrada. Es un punto de la carretera Manizales–Bogotá. "
            "La portería del sector norte es el centro de visitantes Brisas, después del corredor La Esperanza–Murillo. " + PICO
        ),
        variants=[
            "Si paras en Letras, todavía no has entrado. Sigue al corredor y regístrate en Brisas. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.letras_highway", "access.brisas_visitor_center", "access.termales_ruiz_not_gate"],
        tags=["letras", "portería", "brisas"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.la_enea_alternate",
        label="ruta alterna por La Enea",
        kind="procedure",
        examples=[
            "se puede subir por la enea",
            "vía alterna la gruta termales del ruiz",
            "barrio la enea hacia brisas",
            "gallinazo es camino al parque",
            "hay otra entrada desde manizales distinta a letras",
            "is the La Enea road an official alternate",
            "can I reach Brisas past the Ruiz hot springs",
            "no quiero ir por la esperanza, hay otro empalme",
            "la enea gallinazo y luego brisas",
            "esa via alterna sigue vigente o es de un documento viejo",
            "entro por los termales y empalmo a la via de brisas",
            "ruta la enea la publican ahora",
        ],
        hard_negatives=[
            "precio de los termales del Ruiz",
            "horario de baño en el termal",
            "hay alojamiento en La Enea",
        ],
        short=(
            "La reglamentación transitoria de diciembre de 2023 describe una alternativa desde Manizales por el barrio La Enea, la vereda Gallinazo y La Gruta–Termales del Ruiz, hasta empalmar con la vía de La Esperanza hacia Brisas. "
            "La página actual destaca Letras y Murillo, así que confirma con el operador si ese empalme sigue habilitado antes de usarlo. " + PICO
        ),
        variants=[
            "La Enea, Gallinazo y los termales aparecen como vía alterna en el reglamento de diciembre de 2023, no como la ruta principal de la página de ahora. Pregunta si el empalme está abierto. " + PICO_V
        ],
        detail=(
            "En la tabla de ese reglamento de diciembre de 2023, adaptada del POE, el tramo Manizales–La Enea–Termales del Ruiz–cabaña Brisas figura como 34 km. "
            "La página actual de visita no repite esa distancia."
        ),
        sources=[FICHA, ANEXO],
        related=["access.from_manizales", "access.termales_ruiz_not_gate", "access.manizales_brisas_distance"],
        tags=["la enea", "termales", "alterna"],
        entities={"origin": ["manizales"], "sector": ["brisas"]},
    ),
    entry(
        id="access.termales_ruiz_not_gate",
        label="Termales del Ruiz no es la portería",
        kind="fact",
        examples=[
            "los termales del ruiz son la entrada",
            "si llego al termal ya entré al parque",
            "la gruta es la caseta de registro",
            "me dejan pasar al valle desde el termal",
            "el termal reemplaza a brisas",
            "are the Ruiz hot springs the gate",
            "is La Gruta where I check in",
            "vi los termales y crei que era la porteria",
            "despues del baño sigo al parque o ahi termina",
            "la entrada de visitantes no es el termal",
            "brisa o termales, donde me registro",
            "el termal queda de paso y la caseta es otra",
        ],
        hard_negatives=[
            "cuánto vale entrar a los termales",
            "temperatura del agua termal",
            "puedo acampar junto al termal",
        ],
        short=(
            "Los Termales del Ruiz y La Gruta no son la portería. En el reglamento de diciembre de 2023 son un referente de la vía alterna La Enea–Gallinazo, que después empalma hacia Brisas. "
            "La entrada de visitantes del norte es el centro de inducción Brisas. " + PICO
        ),
        variants=[
            "Llegar al termal no reemplaza el registro. Esa referencia está en la vía alterna de diciembre de 2023; la entrada publicada sigue siendo Brisas. " + PICO_V
        ],
        sources=[FICHA, ANEXO],
        related=["access.la_enea_alternate", "access.brisas_visitor_center", "access.letras_not_the_gate"],
        tags=["termales", "la gruta", "brisas"],
        entities={"sector": ["brisas"]},
    ),
]
