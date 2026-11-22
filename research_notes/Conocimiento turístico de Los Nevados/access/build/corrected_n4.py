"""Corrected access entries: Cisne, Potosí, Santa Rosa and Pereira."""

from __future__ import annotations

from common import ANEXO, FICHA, GUIDE_2016, entry

N4 = [
    entry(
        id="access.from_villamaria",
        label="cómo llegar desde Villamaría",
        kind="procedure",
        examples=[
            "cómo llego desde villamaria",
            "villamaria hacia el paramo o potosi",
            "la via del cisne sale de villamaria",
            "veredas el paramo y potosi",
            "de villamaria a santa barbara",
            "how do I get there from Villamaría",
            "which villages lead from Villamaría to the park",
            "no es la via de brisas, es la del cisne",
            "tres trochas destapadas desde ese municipio",
            "villamaria caldas al sector santa isabel",
            "salgo de villamaria rumbo a la cabaña",
            "potosi y el paramo son las veredas",
        ],
        hard_negatives=[
            "hospedaje en Villamaría",
            "altura del Cisne",
            "tarifa del sector Potosí",
        ],
        short=(
            "Desde Villamaría la página indica las veredas El Páramo o Potosí, hacia los controles de la cabaña Potosí y el alto de Santa Bárbara. "
            "Esas vías, con la de Santa Rosa, son tres carreteras terciarias destapadas del sector Cisne–Poleka Kasue. "
            "No es el corredor de Brisas."
        ),
        variants=[
            "Sales de Villamaría hacia El Páramo o Potosí y llegas a Potosí o a Santa Bárbara por carretera destapada. Esa no es la entrada de Brisas."
        ],
        sources=[FICHA],
        related=["access.villamaria_not_brisas_road", "access.potosi_control", "access.dirt_roads_cisne"],
        tags=["villamaría", "potosí", "cisne"],
        entities={"origin": ["villamaria"], "sector": ["cisne"]},
    ),
    entry(
        id="access.villamaria_not_brisas_road",
        label="Villamaría no es la vía de Brisas",
        kind="explanation",
        examples=[
            "villamaria lleva a brisas",
            "por villamaria llego al ruiz en carro",
            "la via de villamaria es la del norte",
            "confundo villamaria con manizales",
            "el cisne y brisas salen del mismo pueblo",
            "does Villamaría lead to the Brisas gate",
            "is Villamaría on the Letras road",
            "voy al valle de las tumbas, villamaria me sirve",
            "santa isabel se entra por villamaria, el ruiz no",
            "no cojo la misma carretera para los dos sectores",
            "villamaria es puerta del cisne",
            "brisas se va por letras, no por estas veredas",
        ],
        hard_negatives=[
            "distancia Villamaría Manizales",
            "festival de Villamaría",
            "clima en el pueblo",
        ],
        short=(
            "Villamaría es la salida hacia el Cisne, por El Páramo o Potosí, hasta Potosí y Santa Bárbara. "
            "Brisas se alcanza por el corredor La Esperanza–Murillo, desde Manizales o desde Murillo, no por esas veredas."
        ),
        variants=[
            "Si buscas Brisas, no armes el viaje por Villamaría. Esa vía va al sector del Cisne y de Santa Isabel."
        ],
        sources=[FICHA],
        related=["access.from_villamaria", "access.from_manizales", "access.circuit_not_scenic_loop"],
        tags=["villamaría", "brisas", "cisne"],
        entities={"origin": ["villamaria"], "sector": ["cisne", "brisas"]},
    ),
    entry(
        id="access.la_cueva_on_the_road",
        label="La Cueva en la vía del Cisne",
        kind="fact",
        examples=[
            "la cueva queda de camino",
            "cabaña la cueva es control",
            "paso por la cueva hacia santa barbara",
            "la cueva es otra porteria distinta",
            "desde la cueva tambien se accede al cisne",
            "is La Cueva a separate gate",
            "where is La Cueva on the Villamaría road",
            "la cueva y potosi son cabañas del mismo sector",
            "no es un pueblo, es un punto del camino",
            "el centro el cisne tambien se alcanza desde la cueva",
            "via villamaria la cueva santa barbara",
            "me citaron en la cueva, es del cisne",
        ],
        hard_negatives=[
            "se puede dormir en La Cueva",
            "hay servicio de comida en la cabaña",
            "altura de La Cueva",
        ],
        short=(
            "La Cueva es una cabaña del sector Cisne, en la vía que desde Villamaría sigue hacia Santa Bárbara. "
            "La página dice que el acceso también se hace desde La Cueva y Potosí, además del centro El Cisne. "
            "No es la portería de Brisas."
        ),
        variants=[
            "La Cueva queda sobre el acceso del Cisne, no es una entrada del Ruiz por Brisas. Potosí y Santa Bárbara son los controles que nombra cómo llegar."
        ],
        detail=(
            "La reglamentación transitoria de diciembre de 2023 describe el ingreso desde Villamaría hasta La Cueva–Santa Bárbara, o por La Telaraña–Hortensias–Potosí. "
            "La página actual no repite los kilómetros de esa tabla."
        ),
        sources=[FICHA, ANEXO],
        related=["access.from_villamaria", "access.santa_barbara_control", "access.el_cisne_approach"],
        tags=["la cueva", "cisne", "cabaña"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.potosi_control",
        label="cabaña Potosí como control",
        kind="fact",
        examples=[
            "potosi es un control del parque",
            "la cabaña potosi a que altura esta",
            "llego a potosi por carretera",
            "potosi sirve para el cisne y para el otun",
            "3920 es la cabaña o la cima",
            "where is the Potosí control cabin",
            "how high is the Potosí cabin",
            "punto de registro potosi",
            "desde villamaria o santa rosa se llega alla",
            "potosi no es brisas",
            "la pagina la pone a unos 3920",
            "control de la cabaña, no del pueblo",
        ],
        hard_negatives=[
            "hay alojamiento en Potosí",
            "tarifa de ingreso por Potosí",
            "sendero de la Laguna Verde",
        ],
        short=(
            "La cabaña Potosí es punto de control del Cisne y también inicio hacia la Laguna del Otún. "
            "Se llega por las destapadas desde Villamaría o Santa Rosa de Cabal. La página la sitúa a unos 3.920 m: es la cabaña, no una cima."
        ),
        variants=[
            "Potosí queda a unos 3.920 m y se alcanza por carretera terciaria desde Villamaría o Santa Rosa. Sirve de control del Cisne y de salida a pie hacia el Otún."
        ],
        sources=[FICHA],
        related=["access.from_villamaria", "access.from_santa_rosa", "access.otun_via_potosi"],
        tags=["potosí", "control", "3920"],
        entities={"sector": ["cisne", "otun"]},
    ),
    entry(
        id="access.santa_barbara_control",
        label="alto de Santa Bárbara",
        kind="fact",
        examples=[
            "santa barbara es un control",
            "el alto de santa barbara donde queda",
            "potosi y santa barbara son los dos puntos",
            "llego a santa barbara por la destapada",
            "santa barbara no es el pueblo de caldas",
            "where is the Santa Bárbara checkpoint",
            "is Santa Bárbara the same as Potosí",
            "registro en el alto, no en brisas",
            "las tres vias llegan a potosi y a santa barbara",
            "conejeras se registra por ese lado",
            "alto de santa barbara sector cisne",
            "no confundir con otro santa barbara",
        ],
        hard_negatives=[
            "fiestas de Santa Bárbara",
            "horario de 7:30 a 10:00",
            "mal de altura en el alto",
        ],
        short=(
            "El alto de Santa Bárbara es, con la cabaña Potosí, uno de los dos controles que la página nombra para el Cisne. "
            "Las vías destapadas desde Villamaría y desde Santa Rosa llegan ahí. No es la portería de Brisas."
        ),
        variants=[
            "Santa Bárbara y Potosí son los controles del sector Cisne. Se llega por carretera terciaria, no por el carreteable de Brisas."
        ],
        sources=[FICHA],
        related=["access.potosi_control", "access.conejeras_not_brisas", "access.la_cueva_on_the_road"],
        tags=["santa bárbara", "control", "cisne"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.dirt_roads_cisne",
        label="vías destapadas hacia el Cisne",
        kind="fact",
        examples=[
            "las vias al cisne son destapadas",
            "carretera terciaria hasta potosi",
            "me exigen 4x4",
            "tres trochas al sector",
            "se puede ir en carro bajo",
            "are the Cisne roads paved",
            "does the page require a 4x4",
            "destapada desde villamaria y desde santa rosa",
            "planear con un prestador de ese sector",
            "no es pavimento hasta la cabaña",
            "vias terciarias potosi y santa barbara",
            "la pagina no dice la marca del carro",
        ],
        hard_negatives=[
            "estado del derrumbe hoy",
            "llantas recomendadas qué medida",
            "parte de vías de Invías",
        ],
        short=(
            "Las tres vías al Cisne son carreteras terciarias destapadas y llegan a Potosí y a Santa Bárbara. "
            "La página pide planearlas con prestadores autorizados. No exige una marca ni un 4x4."
        ),
        variants=[
            "Hasta Potosí y Santa Bárbara se va por destapada. No hay un 4x4 obligatorio escrito; sí conviene cuadrar el viaje con un prestador de ese sector."
        ],
        detail=(
            "La tabla de la reglamentación transitoria de diciembre de 2023, adaptada del POE, anota 42 km para Villamaría–La Telaraña–Hortensias–Potosí–Laguna "
            "y 60 km para Villamaría–Playa Larga–La Cueva–Santa Bárbara–Potosí. La página actual no repite esas distancias."
        ),
        sources=[FICHA, ANEXO],
        related=["access.from_villamaria", "access.from_santa_rosa", "access.mountain_road_conditions"],
        tags=["destapada", "cisne", "terciaria"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.el_cisne_approach",
        label="cómo llegar al centro El Cisne",
        kind="procedure",
        examples=[
            "cómo llego al cisne",
            "centro de visitantes el cisne por donde",
            "poleka kasue se entra por que via",
            "paramillo del cisne, la carretera",
            "de villamaria o de santa rosa al centro",
            "how do I reach the El Cisne center",
            "which road leads to the Cisne visitor center",
            "el cisne no es brisas",
            "llego por potosi, la cueva o santa barbara",
            "tres destapadas hasta los controles",
            "ruta al sector santa isabel",
            "el centro queda en ese sector, no en el norte",
        ],
        hard_negatives=[
            "hay alojamiento en El Cisne",
            "a qué altura está el centro El Cisne",
            "puedo subir a la cumbre de Santa Isabel",
        ],
        short=(
            "Al Cisne se llega por el sector Cisne–Poleka Kasue: desde Villamaría hacia El Páramo o Potosí, o desde Santa Rosa de Cabal por la vereda Páramo de Santa Rosa. "
            "Las tres son carreteras terciarias destapadas y arriban a la cabaña Potosí y al alto de Santa Bárbara. "
            "El centro El Cisne es el acceso de ese sector, también desde La Cueva y Potosí."
        ),
        variants=[
            "La vía al centro El Cisne sale de Villamaría o de Santa Rosa, por destapada, hasta Potosí y Santa Bárbara. No es el carreteable de Brisas."
        ],
        sources=[FICHA],
        related=["access.from_villamaria", "access.la_cueva_on_the_road", "access.dirt_roads_cisne"],
        tags=["cisne", "ruta", "destapada"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.conejeras_not_brisas",
        label="Conejeras no sale de Brisas",
        kind="procedure",
        examples=[
            "conejeras se entra por brisas",
            "la cumbre de santa isabel sale del carreteable",
            "registro de conejeras en que control",
            "voy a conejeras, por villamaria o por letras",
            "el sendero conejeras es del cisne",
            "is Conejeras reached from Brisas",
            "where do I check in for the Conejeras trail",
            "la pagina dice el dia anterior",
            "potosi o santa barbara, no el valle de tumbas",
            "cumbre del nevado santa isabel por que puerta",
            "no mezclo conejeras con el carro a tumbas",
            "paso por los controles del cisne",
        ],
        hard_negatives=[
            "horario de 7:30 a 10:00 en Potosí",
            "puedo hacer cumbre sin guía",
            "equipo técnico para el glaciar",
        ],
        short=(
            "El sendero Conejeras, hacia la cumbre de Santa Isabel, no sale del carreteable de Brisas. "
            "El paso es por los controles del Cisne, cabaña Potosí o alto de Santa Bárbara. "
            "La página dice que ese registro se hace el día anterior al ingreso programado."
        ),
        variants=[
            "Para Conejeras te registras en Potosí o Santa Bárbara, no en Brisas, y la página pide ese paso el día anterior a la cumbre."
        ],
        sources=[FICHA],
        related=["access.santa_barbara_control", "access.potosi_control", "access.from_villamaria"],
        tags=["conejeras", "cisne", "registro"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.from_santa_rosa",
        label="cómo llegar desde Santa Rosa",
        kind="procedure",
        examples=[
            "cómo llego desde santa rosa de cabal",
            "vereda paramo de santa rosa",
            "santa rosa hasta potosi",
            "risaralda hacia el cisne",
            "de santa rosa a santa barbara",
            "how do I get there from Santa Rosa de Cabal",
            "is the Santa Rosa road the same as El Cedral",
            "paramo santa rosa es la vereda de salida",
            "destapada desde santa rosa al control",
            "no salgo de pereira para esta puerta",
            "santa rosa de cabal al sector cisne",
            "llegar a la cabaña potosi desde santa rosa",
        ],
        hard_negatives=[
            "termales de Santa Rosa precio",
            "hotel en Santa Rosa de Cabal",
            "entrada por El Cedral",
        ],
        short=(
            "Desde Santa Rosa de Cabal la página indica la vereda Páramo de Santa Rosa, por carretera terciaria destapada, hasta Potosí y el alto de Santa Bárbara. "
            "Es una de las tres vías del Cisne. No es el camino de Pereira por El Cedral."
        ),
        variants=[
            "Sales de Santa Rosa por Páramo de Santa Rosa y llegas a los controles de Potosí y Santa Bárbara. El Cedral es la otra puerta, la de Pereira."
        ],
        detail=(
            "La tabla de diciembre de 2023 anota 45 km para Santa Rosa de Cabal–Potosí. La página actual no repite esa distancia."
        ),
        sources=[FICHA, ANEXO],
        related=["access.santa_rosa_vs_cedral", "access.potosi_control", "access.dirt_roads_cisne"],
        tags=["santa rosa", "potosí", "destapada"],
        entities={"origin": ["santa_rosa"], "sector": ["cisne"]},
    ),
    entry(
        id="access.santa_rosa_vs_cedral",
        label="Santa Rosa no es El Cedral",
        kind="explanation",
        examples=[
            "santa rosa y pereira entran por el mismo sitio",
            "el cedral queda en santa rosa",
            "paramo de santa rosa es el cedral",
            "las dos son la via de la laguna",
            "confundo potosi con el cedral",
            "is Santa Rosa the same trailhead as El Cedral",
            "do both towns use the Cedral road",
            "una es destapada a potosi y la otra es pereira",
            "no son el mismo letrero",
            "risaralda tiene dos puertas distintas",
            "santa rosa potosi, pereira el cedral",
            "cual de las dos va a la laguna",
        ],
        hard_negatives=[
            "distancia Pereira Santa Rosa",
            "bus entre los dos pueblos",
            "aves en el Otún",
        ],
        short=(
            "Santa Rosa de Cabal va por la vereda Páramo de Santa Rosa hasta Potosí y Santa Bárbara. "
            "Pereira va por La Florida y El Cedral, y de ahí se sigue a pie. "
            "Las dos pueden acercarte a la Laguna del Otún, pero no son el mismo punto de partida."
        ),
        variants=[
            "No salgas de Santa Rosa buscando el letrero de El Cedral. Potosí es la puerta de Santa Rosa; El Cedral es la de Pereira."
        ],
        sources=[FICHA],
        related=["access.from_santa_rosa", "access.from_pereira_cedral", "access.choose_otun_trailhead"],
        tags=["santa rosa", "cedral", "otún"],
        entities={"origin": ["santa_rosa", "pereira"], "sector": ["cisne", "otun"]},
    ),
    entry(
        id="access.from_pereira_cedral",
        label="cómo llegar desde Pereira por El Cedral",
        kind="procedure",
        examples=[
            "cómo llego desde pereira",
            "la florida y el cedral",
            "pereira hacia la laguna del otun",
            "en el cedral se acaba el carro",
            "corregimiento la florida y despues a pie",
            "how do I get from Pereira to El Cedral",
            "where does the drive from Pereira end",
            "vereda el bosque o el cedral",
            "salgo de pereira al sector otun",
            "no es la destapada de santa rosa",
            "camino de herradura despues del cedral",
            "pereira la florida el cedral laguna",
        ],
        hard_negatives=[
            "horario de la cabaña Potosí",
            "hospedaje en la vereda El Bosque",
            "precio de la entrada al Otún",
        ],
        short=(
            "Desde Pereira sales por carretera hacia el corregimiento de La Florida y el sitio El Cedral. "
            "Ahí empieza la subida a pie: la página da unos 7,5 km hasta el límite del parque y 18 km hasta la Laguna del Otún. "
            "No es la vía de Santa Rosa a Potosí."
        ),
        variants=[
            "El carro desde Pereira llega por La Florida hasta El Cedral. Después caminas unos 7,5 km al límite y 18 km a la laguna, no por la destapada de Santa Rosa."
        ],
        detail=(
            "La reglamentación transitoria de diciembre de 2023 encadena La Florida–La Suiza–El Cedral y anota 26 km para Pereira–La Suiza–El Cedral. "
            "La guía de abril de 2016 también decía unos 26 km hasta el fin del carro. La página actual no repite esos 26 km; sí repite los 7,5 km y los 18 km a pie."
        ),
        sources=[FICHA, ANEXO, GUIDE_2016],
        related=["access.cedral_walk_distances", "access.cedral_and_bosque_names", "access.santa_rosa_vs_cedral"],
        tags=["pereira", "cedral", "otún"],
        entities={"origin": ["pereira"], "sector": ["otun"]},
    ),
    entry(
        id="access.cedral_walk_distances",
        label="caminata desde El Cedral",
        kind="fact",
        examples=[
            "cuántos km a pie desde el cedral",
            "7,5 km hasta el límite",
            "18 km a la laguna del otun",
            "la caminata sale de pereira o del cedral",
            "kilometros aproximados del camino",
            "how many kilometers is the footpath from El Cedral to Laguna del Otún",
            "is 7.5 km the whole way to Otún",
            "del cedral al limite y de ahi a la laguna",
            "son kilometros a pie, no de carro",
            "la pagina dice aproximadamente",
            "18 kilometros no es hasta el cedral",
            "distancia de la caminata del otun",
        ],
        hard_negatives=[
            "cuántas horas se demora la caminata",
            "dificultad del sendero",
            "puedo acampar en la laguna",
        ],
        short=(
            "Desde El Cedral la página calcula unos 7,5 km a pie hasta el límite del parque y 18 km hasta la Laguna del Otún. "
            "Son distancias aproximadas de esa caminata, no del carro desde Pereira. "
            "No publica las horas."
        ),
        variants=[
            "A pie, después de El Cedral, cuenta unos 7,5 km para tocar el límite y 18 km para llegar a la laguna. El carro no recorre esas dos cifras."
        ],
        sources=[FICHA],
        related=["access.from_pereira_cedral", "access.no_official_travel_time", "access.otun_via_potosi"],
        tags=["cedral", "7,5", "18"],
        entities={"sector": ["otun"]},
    ),
    entry(
        id="access.cedral_and_bosque_names",
        label="El Cedral y la vereda El Bosque",
        kind="explanation",
        examples=[
            "el bosque y el cedral son lo mismo",
            "pereira por la vereda el bosque",
            "la florida el cedral o el bosque",
            "dos nombres del lado de pereira",
            "me citan en el bosque y yo iba al cedral",
            "are El Bosque and El Cedral the same trailhead",
            "which name should I give the driver",
            "la pagina usa los dos en el otun",
            "no son dos ciudades",
            "confirmo el punto con el operador",
            "vereda el bosque hacia la laguna",
            "el cedral es el sitio y el bosque la vereda",
        ],
        hard_negatives=[
            "fincas de la vereda El Bosque",
            "hay señal de celular en El Cedral",
            "cabaña para dormir en El Bosque",
        ],
        short=(
            "En el sector Otún la página habla de Pereira por la vereda El Bosque y, en cómo llegar, de La Florida y El Cedral para seguir a pie. "
            "No los trates como dos ciudades. El punto exacto donde te encuentras sí debes confirmarlo con quien coordina el ingreso."
        ),
        variants=[
            "El Bosque y El Cedral están del lado de Pereira hacia la laguna. No asumas que el letrero del encuentro es el mismo: confírmalo con el operador."
        ],
        detail=(
            "El reglamento de diciembre de 2023 encadena La Florida–La Suiza–El Cedral antes del camino de herradura. "
            "No declara que El Bosque y El Cedral sean el mismo letrero."
        ),
        sources=[FICHA, ANEXO],
        related=["access.from_pereira_cedral", "access.choose_otun_trailhead", "access.santa_rosa_vs_cedral"],
        tags=["cedral", "el bosque", "pereira"],
        entities={"origin": ["pereira"], "sector": ["otun"]},
    ),
    entry(
        id="access.otun_via_potosi",
        label="Laguna del Otún por Potosí",
        kind="procedure",
        examples=[
            "la laguna se entra por potosi",
            "otro camino al otun distinto al cedral",
            "carro hasta la cabaña y luego a pie",
            "potosi hacia la laguna",
            "villamaria o santa rosa y despues camino",
            "can I reach Otún lake via Potosí",
            "is Potosí a second start for the lake",
            "no es la caminata de el cedral",
            "la pagina no le pone kilometros a ese tramo",
            "desde la linda y potosi, eso esta en el reglamento",
            "elijo potosi para la laguna",
            "despues de la cabaña se camina",
        ],
        hard_negatives=[
            "profundidad de la Laguna del Otún",
            "puedo nadar en la laguna",
            "aves de la laguna",
        ],
        short=(
            "También se llega a la Laguna del Otún por carretera hasta la cabaña Potosí, por las vías del Cisne desde Villamaría o Santa Rosa, y de ahí a pie. "
            "No es la caminata de El Cedral. La página no publica kilómetros propios de ese tramo después de la cabaña."
        ),
        variants=[
            "Si entras por Potosí, llegas en la destapada del Cisne y luego caminas a la laguna. Quien sale de Pereira camina desde El Cedral."
        ],
        detail=(
            "El reglamento de diciembre de 2023 describe ese ingreso desde Santa Rosa de Cabal–La Linda–Potosí y luego por camino. "
            "La página actual no repite el nombre La Linda ni una distancia de la cabaña a la laguna."
        ),
        sources=[FICHA, ANEXO],
        related=["access.potosi_control", "access.choose_otun_trailhead", "access.from_santa_rosa"],
        tags=["otún", "potosí", "caminata"],
        entities={"sector": ["otun", "cisne"]},
    ),
    entry(
        id="access.choose_otun_trailhead",
        label="elegir el inicio hacia el Otún",
        kind="procedure",
        examples=[
            "dos formas de llegar a la laguna",
            "potosi o el cedral, cual escojo",
            "inicio de la caminata al otun",
            "no hay una tercera porteria de la laguna",
            "desde que ciudad salgo a la laguna",
            "Potosí or El Cedral for Otún lake",
            "which trailhead should I use for the lake",
            "villamaria santa rosa o pereira",
            "las dos llegan al agua por caminos distintos",
            "elijo una antes de salir",
            "no son la misma via con dos nombres",
            "laguna del otun por donde empiezo",
        ],
        hard_negatives=[
            "tamaño de la laguna",
            "humedal Ramsar qué significa",
            "puedo pescar en el Otún",
        ],
        short=(
            "La página publica dos inicios hacia la Laguna del Otún. Uno es en carro hasta Potosí, desde Villamaría o Santa Rosa, y luego a pie. "
            "El otro sale de Pereira por La Florida y El Cedral, con unos 7,5 km al límite y 18 km a la laguna. "
            "No hay una tercera portería de la laguna en esa página."
        ),
        variants=[
            "Potosí y El Cedral son los dos comienzos publicados. El primero se acerca por las destapadas del Cisne; el segundo sale de Pereira y sigue a pie unos 7,5 km al límite y 18 km a la laguna."
        ],
        sources=[FICHA],
        related=["access.otun_via_potosi", "access.from_pereira_cedral", "access.santa_rosa_vs_cedral"],
        tags=["otún", "potosí", "cedral"],
        entities={"sector": ["otun"]},
    ),
    entry(
        id="access.from_pereira_choose",
        label="desde Pereira hay que elegir puerta",
        kind="procedure",
        examples=[
            "desde pereira cuál entrada",
            "pereira brisas o pereira cedral",
            "salgo de pereira al parque",
            "la pagina que via me da en pereira",
            "pereira no es manizales",
            "which gate do I use if I start in Pereira",
            "from Pereira, is Brisas the published road",
            "la florida el cedral es la de pereira",
            "potosi no sale como carretera directa de pereira",
            "elijo el otun o me voy a otra ciudad",
            "pereira hacia los nevados por donde",
            "no hay una sola via pereira parque",
        ],
        hard_negatives=[
            "vuelo a Pereira",
            "terminal de Pereira horarios",
            "café en el eje cafetero",
        ],
        short=(
            "Desde Pereira la vía que la página publica es La Florida y El Cedral, y después a pie hacia la Laguna del Otún. "
            "Potosí se alcanza por las carreteras del Cisne, desde Villamaría o Santa Rosa, no como una segunda autopista escrita desde Pereira. "
            "Brisas se arma desde Manizales o Murillo."
        ),
        variants=[
            "Si estás en Pereira y quieres la laguna, sigue a El Cedral. Brisas y Potosí salen de otras ciudades, no de un desvío que la página marque en Pereira."
        ],
        sources=[FICHA],
        related=["access.from_pereira_cedral", "access.from_santa_rosa", "access.from_manizales"],
        tags=["pereira", "cedral", "elegir"],
        entities={"origin": ["pereira"], "sector": ["otun"]},
    ),
]
