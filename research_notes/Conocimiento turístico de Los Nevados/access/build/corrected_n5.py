"""Corrected access entries: south gates, gaps and 2023 checkpoints."""

from __future__ import annotations

from common import ANEXO, FICHA, GUIDE_2016, entry

PICO = (
    "Si entras a Brisas en noviembre, un fin de semana o puente, revisa el pico y placa "
    "ambiental del Tolima, Resolución 1815 del 24 de julio de 2026, de 5:00 a. m. a 4:00 p. m."
)
PICO_V = (
    "En noviembre, fines de semana y puentes, el acceso Brisas–Valle de las Tumbas tiene pico y placa "
    "ambiental del Tolima de 5:00 a. m. a 4:00 p. m., Resolución 1815 del 24 de julio de 2026."
)

N5 = [
    entry(
        id="access.from_salento_cocora",
        label="cómo llegar desde Salento por Cocora",
        kind="procedure",
        examples=[
            "cómo llego desde salento",
            "vereda cocora hasta el límite",
            "14 km por cocora",
            "salento no es la portería",
            "valle del cocora y despues el parque",
            "how do I get from Salento to the park boundary",
            "is Salento itself the gate",
            "sector quindio dulima por cocora",
            "catorce kilometros hasta el limite del parque",
            "sigo al valle y de ahi al area protegida",
            "no es la via de brisas ni la de potosi",
            "salento cocora nevado del tolima",
        ],
        hard_negatives=[
            "cabalgata en el Valle del Cocora",
            "horario del punto de atención",
            "precio de la entrada por Cocora",
        ],
        short=(
            "Desde Salento la página manda por la vereda Cocora y precisa 14 km hasta el límite del parque. "
            "El pueblo no es la portería: sigues al Valle del Cocora, el punto de atención de Quindío–Dulima, y de ahí el camino. "
            "Confirma el registro con el operador de ese sector."
        ),
        variants=[
            "Salento es la salida y Cocora el corredor. La cifra de la página actual es 14 km por esa vereda hasta el límite del parque."
        ],
        sources=[FICHA],
        related=["access.cocora_before_park", "access.cocora_registration", "access.quindio_gate_is_cocora"],
        tags=["salento", "cocora", "14 km"],
        entities={"origin": ["salento"], "sector": ["quindio"]},
    ),
    entry(
        id="access.cocora_before_park",
        label="Cocora todavía no es el límite",
        kind="explanation",
        examples=[
            "el valle del cocora ya es el parque",
            "las palmas son la portería",
            "entre las palmas ya entré",
            "cocora y el límite son el mismo punto",
            "14 km hasta donde empieza el area",
            "is the Cocora valley already inside the park",
            "do the palm trees mark the gate",
            "puedo estar en cocora y seguir fuera",
            "el limite queda despues de la vereda",
            "no doy la vuelta en las palmas",
            "el punto de atencion no es el aviso de que ya pase",
            "cocora acerca, el limite esta mas adelante",
        ],
        hard_negatives=[
            "cuántas palmas hay en Cocora",
            "fincas de alquiler en el valle",
            "caballo hasta Acaime",
        ],
        short=(
            "El Valle del Cocora es el corredor y el punto de atención, no el aviso de que ya pasaste el límite. "
            "La página mide 14 km por la vereda Cocora hasta el límite del parque. "
            "Puedes estar entre palmas y todavía no haber entrado por esa portería."
        ),
        variants=[
            "No des la vuelta en las palmas creyendo que esa es la entrada. Cocora acerca; el límite publicado está 14 km por la vereda."
        ],
        sources=[FICHA],
        related=["access.from_salento_cocora", "access.cocora_registration", "access.three_south_paths"],
        tags=["cocora", "límite", "palmas"],
        entities={"sector": ["quindio"]},
    ),
    entry(
        id="access.cocora_registration",
        label="registro en el Valle del Cocora",
        kind="fact",
        examples=[
            "dónde me registro en cocora",
            "punto de atención del quindio",
            "la puerta azul sigue siendo el control",
            "kilometro 11 de salento cocora",
            "truchera es el registro de ahora",
            "where do I check in for the Cocora access",
            "is the blue gate still the checkpoint",
            "valle del cocora es el punto que nombra la pagina",
            "el reglamento decia 2400 metros",
            "confirmo el mostrador con el operador",
            "no doy por sentado el km 11",
            "registro del sector dulima en cocora",
        ],
        hard_negatives=[
            "horario de 6:00 a 10:00 en Cocora",
            "entrada a la truchera cuánto vale",
            "reserva con cinco días",
        ],
        short=(
            "La página actual nombra el Valle del Cocora como punto de atención de Quindío–Dulima. "
            "El reglamento de diciembre de 2023 ubicaba el registro en la puerta azul de la truchera, kilómetro 11, a unos 2.400 m. "
            "No des por sentado que el mostrador siga en ese punto: confírmalo con el operador."
        ),
        variants=[
            "Hoy la página dice Valle del Cocora. En diciembre de 2023 el texto precisaba el kilómetro 11, la puerta azul y unos 2.400 m, y eso no garantiza el mismo mostrador."
        ],
        sources=[FICHA, ANEXO],
        related=["access.from_salento_cocora", "access.cocora_before_park", "access.control_coordinates"],
        tags=["cocora", "registro", "2023"],
        entities={"sector": ["quindio"]},
    ),
    entry(
        id="access.armenia_salento_road",
        label="Armenia como aproximación a Cocora",
        kind="explanation",
        examples=[
            "desde armenia cómo llego",
            "armenia salento cocora cuantos km",
            "25 o 37 kilometros, cual es",
            "armenia es la porteria",
            "la via pavimentada hasta el valle",
            "how do I approach the park from Armenia",
            "which kilometer figure should I trust",
            "armenia no es una segunda entrada",
            "el dato vigente es el de la vereda",
            "14 km hasta el limite, no el de armenia",
            "salgo de armenia hacia salento",
            "los kilometros de 2023 no coinciden",
        ],
        hard_negatives=[
            "bus Armenia Salento horario",
            "peaje Armenia",
            "hotel en Salento",
        ],
        short=(
            "Armenia no es una portería. La página actual empieza el acceso del Quindío en Salento, por la vereda Cocora, 14 km hasta el límite. "
            "El reglamento de diciembre de 2023 describe Armenia–Salento–Cocora, pero en el texto dice 25 km y en la tabla 37 km. "
            "No elijas una de esas dos."
        ),
        variants=[
            "Desde Armenia vas hacia Salento y Cocora, sin una portería propia. Quédate con los 14 km de la vereda hasta el límite; los 25 km y los 37 km de diciembre de 2023 se contradicen."
        ],
        detail=(
            "La guía de abril de 2016 decía unos 25 km de Armenia a Salento y al Valle del Cocora. "
            "Esa cifra coincide con la prosa de 2023 y no con la tabla del mismo reglamento. La página actual no la usa."
        ),
        sources=[FICHA, ANEXO, GUIDE_2016],
        related=["access.from_salento_cocora", "access.quindio_gate_is_cocora", "access.ignore_single_kilometer"],
        tags=["armenia", "salento", "kilómetros"],
        entities={"origin": ["armenia", "salento"], "sector": ["quindio"]},
    ),
    entry(
        id="access.quindio_gate_is_cocora",
        label="en el Quindío la puerta es Cocora",
        kind="fact",
        examples=[
            "en el quindio por donde se entra",
            "filandia tiene porteria",
            "circasia es otra entrada",
            "solo cocora esta publicada",
            "armenia es via, no caseta",
            "is there a second Quindío gate",
            "does Filandia have a park entrance",
            "salento vereda cocora 14 km",
            "una sola puerta quindiana en como llegar",
            "no aparece otro municipio del quindio",
            "quiero el parque y estoy en el quindio",
            "cocora es el acceso publicado",
        ],
        hard_negatives=[
            "pueblo más bonito del Quindío",
            "café de Filandia",
            "distancia Armenia Circasia",
        ],
        short=(
            "En el Quindío la página publica un acceso: Salento, por la vereda Cocora, 14 km hasta el límite del parque. "
            "Armenia es aproximación a ese valle, no una segunda portería. "
            "Filandia o Circasia no aparecen en cómo llegar."
        ),
        variants=[
            "Si estás en el Quindío, el camino publicado va a Cocora, 14 km hasta el límite. No hay otra portería del departamento en esa página."
        ],
        sources=[FICHA],
        related=["access.from_salento_cocora", "access.armenia_salento_road", "access.three_south_paths"],
        tags=["quindío", "cocora", "portería"],
        entities={"origin": ["salento"], "sector": ["quindio"]},
    ),
    entry(
        id="access.from_ibague_juntas",
        label="cómo llegar desde Ibagué por Juntas",
        kind="procedure",
        examples=[
            "cómo llego desde ibagué por juntas",
            "vereda juntas 15 km",
            "15 km llegan al límite",
            "ibague al nevado del tolima",
            "juntas es la puerta sur",
            "how do I get from Ibagué through Juntas",
            "do the 15 km reach the park boundary",
            "no es murillo ni anzoategui",
            "despues de la vereda se sigue a pie",
            "la pagina asocia 15 km a ese camino",
            "cañon del combeima es de una guia vieja",
            "ibague juntas sector dulima",
        ],
        hard_negatives=[
            "10 horas de sendero es el dato de ahora",
            "termales del cañón horario",
            "reserva con cinco días",
        ],
        short=(
            "Desde Ibagué la página indica la vereda Juntas y asocia 15 km a ese camino. "
            "No dice, en esa frase, que los 15 km lleguen hasta el límite, como sí lo precisa en Cocora. "
            "Después de la vereda el sector sigue a pie, no en una carretera hasta la nieve."
        ),
        variants=[
            "Juntas es la puerta sur que sale de Ibagué. Usa los 15 km como la cifra de la página para ese camino y no los leas como el límite, porque esa precisión solo está escrita en Cocora."
        ],
        detail=(
            "La guía de abril de 2016 llamaba Cañón del Combeima a la vía desde Ibagué, con unos 47 km hasta donde terminaba el carro y un sendero de 10 horas. "
            "La página actual no repite esas cifras."
        ),
        sources=[FICHA, GUIDE_2016],
        related=["access.from_ibague_choose", "access.three_south_paths", "access.murillo_is_north_not_tolima"],
        tags=["ibagué", "juntas", "15 km"],
        entities={"origin": ["ibague"], "sector": ["quindio"]},
    ),
    entry(
        id="access.from_anzoategui_palomar",
        label="cómo llegar desde Anzoátegui por Palomar",
        kind="procedure",
        examples=[
            "cómo llego desde anzoategui",
            "vereda palomar 11 km",
            "anzoategui al sector sur",
            "palomar es una de las tres entradas",
            "32 o 85 km cual uso",
            "how do I get from Anzoátegui to Palomar",
            "is 11 km the current figure",
            "no uses la distancia vieja de ibague",
            "palomar junto con cocora y juntas",
            "la punta era el control de 2023",
            "once kilometros asocia la pagina",
            "entro por anzoategui al tolima",
        ],
        hard_negatives=[
            "bus Ibagué Anzoátegui",
            "horario del punto de Anzoátegui",
            "finca La Aurora se puede visitar",
        ],
        short=(
            "Desde Anzoátegui la página indica la vereda Palomar y asocia 11 km a ese acceso. "
            "Es una de las tres entradas de Quindío–Dulima, con Cocora y Juntas. "
            "No uses 32 km ni 85 km: se contradicen y la página actual no elige una."
        ),
        variants=[
            "Palomar es la salida de Anzoátegui. La cifra de la página actual es 11 km para ese acceso; las distancias viejas hasta el pueblo no son esa cifra."
        ],
        detail=(
            "La guía de abril de 2016 decía que Anzoátegui está a 32 km de Ibagué y que el carro terminaba en la vereda La Cascada. "
            "La tabla de diciembre de 2023 anota 85 km para Ibagué–Anzoátegui–Palomar. "
            "No miden, con seguridad, el mismo tramo, y la página actual no las repite."
        ),
        sources=[FICHA, ANEXO, GUIDE_2016],
        related=["access.la_punta_control", "access.three_south_paths", "access.from_ibague_juntas"],
        tags=["anzoátegui", "palomar", "11 km"],
        entities={"origin": ["anzoategui"], "sector": ["quindio"]},
    ),
    entry(
        id="access.la_punta_control",
        label="punto de control La Punta",
        kind="fact",
        examples=[
            "la punta es el control de anzoategui",
            "vereda la cascada donde me registro",
            "control flotante sigue igual",
            "3100 metros es la caseta de ahora",
            "finca la aurora es la entrada vigente",
            "is La Punta still the checkpoint",
            "should I navigate to the 2023 coordinate",
            "la pagina habla de palomar, no de la punta",
            "no mezcles 11 km con la altura vieja",
            "antes de salir le pregunto al operador si la punta sigue",
            "el reglamento de 2023 lo llamo flotante",
            "anzoategui la punta o palomar",
        ],
        hard_negatives=[
            "horario de jueves a sábado en La Punta",
            "coordenada para el GPS de hoy",
            "permiso de ingreso en el PIT",
        ],
        short=(
            "La Punta, en la vereda La Cascada de Anzoátegui, es un control del reglamento de diciembre de 2023, llamado flotante y anotado a unos 3.100 m. "
            "La página actual habla de Anzoátegui por Palomar y no repite ese nombre. "
            "No lo uses como el mostrador de hoy sin confirmarlo con el operador."
        ),
        variants=[
            "La Punta y los 3.100 m son la referencia de diciembre de 2023, no una caseta garantizada ahora. La página vigente habla de Palomar y de sus 11 km, que son otra cifra."
        ],
        sources=[FICHA, ANEXO],
        related=["access.from_anzoategui_palomar", "access.control_coordinates", "access.cocora_registration"],
        tags=["la punta", "2023", "anzoátegui"],
        entities={"origin": ["anzoategui"], "sector": ["quindio"]},
    ),
    entry(
        id="access.from_ibague_choose",
        label="desde Ibagué hay varias entradas",
        kind="procedure",
        examples=[
            "desde ibagué cuál entrada",
            "ibague a brisas o a juntas",
            "murillo o palomar saliendo de ibague",
            "varias vias, no es la misma",
            "el tolima y el ruiz no salen juntos",
            "which gate do I use from Ibagué",
            "from Ibagué, is Murillo the Tolima volcano",
            "juntas 15 km o palomar 11 km",
            "brisas se va por murillo",
            "elijo el nevado antes de salir",
            "ibague tiene mas de una porteria",
            "no son desvios de una sola carretera",
        ],
        hard_negatives=[
            "terminal de Ibagué horarios",
            "alquiler de carro en Ibagué",
            "clima en el cañón",
        ],
        short=(
            "Desde Ibagué hay que elegir sector. A Brisas se va por Murillo y el corredor La Esperanza–Murillo. "
            "Al sector del Tolima, la página ofrece Juntas, con 15 km asociados, o Anzoátegui por Palomar, con 11 km. " + PICO
        ),
        variants=[
            "Ibagué sirve de base a más de una puerta: Murillo mira a Brisas, Juntas y Anzoátegui miran al sur. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.from_murillo", "access.from_ibague_juntas", "access.from_anzoategui_palomar"],
        tags=["ibagué", "murillo", "juntas"],
        entities={"origin": ["ibague"]},
    ),
    entry(
        id="access.three_south_paths",
        label="tres caminos al sector del Tolima",
        kind="explanation",
        examples=[
            "tres caminos al nevado del tolima",
            "cocora juntas y palomar",
            "14, 15 y 11 son lo mismo",
            "el sur se recorre en carro hasta la cumbre",
            "cual de las tres entradas",
            "what are the three southern approaches",
            "do all three distances reach the boundary",
            "quindio dulima tiene tres puertas",
            "despues de la vereda se camina",
            "no hay circuito en carro entre las tres",
            "salento ibague o anzoategui",
            "elige una con el operador",
        ],
        hard_negatives=[
            "dificultad de la cumbre del Tolima",
            "se puede ver el cráter",
            "días de caminata oficiales",
        ],
        short=(
            "Quindío–Dulima tiene tres caminos publicados: Cocora, 14 km hasta el límite; Juntas, con 15 km asociados; y Palomar, con 11 km asociados. "
            "Solo en Cocora la página dice que los kilómetros llegan al límite. "
            "Los tres siguen a pie y no hay una carretera de visitantes hasta la cumbre."
        ),
        variants=[
            "Cocora, Juntas y Palomar salen de municipios distintos. La página precisa «hasta el límite» en los 14 km de Cocora, no en los 15 km de Juntas ni en los 11 km de Palomar."
        ],
        sources=[FICHA],
        related=["access.from_salento_cocora", "access.from_ibague_juntas", "access.from_anzoategui_palomar"],
        tags=["tolima", "cocora", "juntas", "palomar"],
        entities={"sector": ["quindio"]},
    ),
    entry(
        id="access.murillo_is_north_not_tolima",
        label="Murillo lleva al norte, no al Tolima",
        kind="explanation",
        examples=[
            "murillo es la entrada del tolima",
            "desde murillo al nevado del tolima",
            "el pueblo esta en el tolima y la via es al ruiz",
            "confundo murillo con juntas",
            "murillo brisas no es palomar",
            "does Murillo lead to Nevado del Tolima",
            "Murillo is in Tolima, so is that the south gate",
            "el corredor va al sector norte",
            "para el tolima salgo por cocora juntas o palomar",
            "no uso murillo como puerta del dulima",
            "mismo departamento, otro nevado",
            "murillo queda al lado del ruiz",
        ],
        hard_negatives=[
            "historia del Nevado del Tolima",
            "nombre indígena Dulima",
            "cumbre permitida del Tolima",
        ],
        short=(
            "Murillo está en el Tolima, pero la vía publicada desde ese pueblo va al sector norte: el corredor La Esperanza–Murillo hasta Brisas, junto al Ruiz. "
            "No es el acceso al Nevado del Tolima. Para ese sector sal por Cocora, por Juntas o por Palomar. " + PICO
        ),
        variants=[
            "No uses Murillo para el Nevado del Tolima. Ese pueblo conecta con Brisas. El sur publicado es Cocora, Juntas o Palomar. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.from_murillo", "access.three_south_paths", "access.from_ibague_choose"],
        tags=["murillo", "tolima", "brisas"],
        entities={"origin": ["murillo"], "sector": ["brisas"]},
    ),
    entry(
        id="access.olleta_not_a_gate",
        label="La Olleta no es una entrada publicada",
        kind="fact",
        examples=[
            "la olleta es una portería",
            "entro por el crater de la olleta",
            "la piraña tiene caseta",
            "desvio a la olleta para visitantes",
            "el cono es una entrada",
            "is La Olleta a visitor gate",
            "can I enter at La Piraña",
            "la pagina no la lista en como llegar",
            "el norte se entra por brisas",
            "ver el nombre en el mapa no abre una puerta",
            "caballete de la olleta es del circuito viejo",
            "no hay ruta verificada por la olleta",
        ],
        hard_negatives=[
            "qué tipo de cráter es La Olleta",
            "altura de La Olleta",
            "erupción de La Piraña",
        ],
        short=(
            "La página de visita no publica La Olleta ni La Piraña como portería. "
            "No hay aquí una ruta de visitantes verificada por ese cono. El ingreso norte publicado es Brisas y el carreteable hasta el valle."
        ),
        variants=[
            "Ver La Olleta en un mapa del volcán no crea una entrada. La portería del norte sigue siendo Brisas; por La Olleta no tengo un camino verificado."
        ],
        detail=(
            "La página nombra los cráteres La Olleta y La Piraña al describir el complejo volcánico, no en cómo llegar. "
            "El reglamento de diciembre de 2023 incluye el caballete de La Olleta en un circuito vial de infraestructura, no como un paseo autorizado de portería a portería."
        ),
        sources=[FICHA, ANEXO],
        related=["access.brisas_visitor_center", "access.circuit_not_scenic_loop", "access.stay_on_official_gate"],
        tags=["olleta", "portería", "brisas"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.santa_isabel_town_vs_sector",
        label="pueblo Santa Isabel o sector del nevado",
        kind="explanation",
        examples=[
            "el pueblo santa isabel es la porteria",
            "municipio santa isabel o el nevado",
            "entro al sector por el casco urbano",
            "santa isabel tolima tiene via publicada",
            "el sector se llama igual que el pueblo",
            "is the town of Santa Isabel the gate",
            "Santa Isabel the municipality or the volcano sector",
            "villamaria y santa rosa si, el casco no",
            "poleka kasue no sale de ese municipio",
            "no hay caseta en el pueblo santa isabel",
            "confundo el nombre del volcan con el del pueblo",
            "por donde entra el sector santa isabel",
        ],
        hard_negatives=[
            "altura del Nevado de Santa Isabel",
            "cumbre de Conejeras",
            "hospedaje en el municipio",
        ],
        short=(
            "El sector del Nevado de Santa Isabel se entra por Villamaría o por Santa Rosa de Cabal, hasta Potosí y Santa Bárbara. "
            "El municipio de Santa Isabel, en el Tolima, está en el área del parque, pero la página no publica una portería desde su casco. "
            "No hay aquí una ruta verificada desde ese pueblo."
        ),
        variants=[
            "Si dices Santa Isabel, aclara si hablas del nevado o del municipio. Al nevado se va por Villamaría o Santa Rosa; del casco no tengo un camino publicado."
        ],
        sources=[FICHA],
        related=["access.from_villamaria", "access.from_santa_rosa", "access.no_published_gate_towns"],
        tags=["santa isabel", "pueblo", "cisne"],
        entities={"origin": ["santa_isabel"], "sector": ["cisne"]},
    ),
    entry(
        id="access.no_published_gate_towns",
        label="municipios sin acceso de visitantes publicado",
        kind="fact",
        examples=[
            "cómo entro desde herveo",
            "casabianca tiene porteria",
            "desde el casco de santa isabel",
            "esos pueblos estan en el parque",
            "hay sendero publicado desde herveo",
            "is there a visitor route from Herveo",
            "can I enter from Casabianca",
            "no aparece en como llegar",
            "quiero la puerta oficial, no un atajo",
            "que hago si mi pueblo no esta en la lista",
            "herveo casabianca y santa isabel",
            "usa una entrada que si este escrita",
        ],
        hard_negatives=[
            "alcaldía de Herveo teléfono",
            "límites del municipio de Casabianca",
            "historia de esos pueblos",
        ],
        short=(
            "No tengo una ruta de visitantes verificada desde Herveo, Casabianca ni desde el casco de Santa Isabel. "
            "Esos municipios están en el área del parque, pero cómo llegar no publica el camino. "
            "Entra por una puerta de sector que sí esté publicada y coordínala con un operador registrado de ese sector."
        ),
        variants=[
            "Desde Herveo, Casabianca o el casco de Santa Isabel no hay aquí un camino verificado. No te mando por un desvío concreto: usa una entrada publicada y el operador de ese sector."
        ],
        sources=[FICHA],
        related=["access.gateway_towns", "access.santa_isabel_town_vs_sector", "access.how_to_choose_sector"],
        tags=["herveo", "casabianca", "ruta"],
        entities={"origin": ["herveo", "casabianca", "santa_isabel"]},
    ),
    entry(
        id="access.where_road_ends",
        label="hasta dónde llega el carro",
        kind="explanation",
        examples=[
            "hasta dónde llega el carro",
            "en todos los sectores se entra en vehículo",
            "el carro llega a la nieve",
            "brisas en carro y los otros a pie",
            "potosi se alcanza por carretera",
            "where does the car have to stop",
            "can I drive to every sector",
            "el cedral cocora juntas y palomar siguen a pie",
            "el valle norte si sigue en vehiculo cubierto",
            "no hay via publicada hasta la cumbre",
            "donde se acaba la carretera",
            "carro hasta el control y luego camino",
        ],
        hard_negatives=[
            "dificultad de los senderos",
            "puedo llevar la bicicleta",
            "estado de la vía hoy",
        ],
        short=(
            "El carro no entra igual en todos lados. En el norte llegas a Brisas y el valle sigue en vehículo cubierto. "
            "A Potosí y Santa Bárbara se llega por destapada y después hay camino; en El Cedral, Cocora, Juntas y Palomar la página continúa a pie. " + PICO
        ),
        variants=[
            "Solo el norte deja el valle en vehículo cubierto después de Brisas. En el Cisne el carro llega a los controles; en El Cedral y en el sur se sigue a pie. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.road_visit_or_trail", "access.brisas_tumbas_drive", "access.cedral_walk_distances"],
        tags=["carro", "a pie", "final"],
    ),
    entry(
        id="access.road_visit_or_trail",
        label="visita por carretera o acceso a pie",
        kind="explanation",
        examples=[
            "cuál sector es en carro",
            "brisas es la visita corta",
            "los otros son travesía",
            "quiero ir en vehículo, cuál puerta",
            "caminata larga por cual sector",
            "which sector is the drive-up visit",
            "where do I go if I need a vehicle access",
            "el carreteable es el del norte",
            "cocora y juntas no son un paseo en carro",
            "visita esporadica en brisas",
            "varios dias, los otros sectores",
            "elijo segun si voy en carro o a pie",
        ],
        hard_negatives=[
            "qué hacer en el valle",
            "camping en el sur",
            "edad mínima para entrar",
        ],
        short=(
            "Si necesitas un acceso en vehículo, la página describe Brisas–Valle de las Tumbas como el recorrido carreteable del norte. "
            "Los otros sectores se alcanzan por carretera hasta un control o una vereda y siguen a pie; la misma página los presenta para travesías de varios días. " + PICO
        ),
        variants=[
            "Brisas es la visita en vehículo cubierto. Cisne, Otún y el sur llegan por carretera solo hasta su control o su vereda, y de ahí se camina. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.where_road_ends", "access.brisas_tumbas_drive", "access.four_sector_gates"],
        tags=["carro", "travesía", "brisas"],
    ),
    entry(
        id="access.circuit_not_scenic_loop",
        label="el circuito interno no es un paseo",
        kind="rule",
        examples=[
            "puedo cruzar de brisas al cisne en carro",
            "el circuito manizales olleta villamaria",
            "recorro todas las porterias en un dia",
            "la via alta esta abierta al paseo",
            "caballete de la olleta es un mirador publico",
            "can I drive the high circuit between gates",
            "is the 2023 loop a scenic drive",
            "de un sector a otro por dentro",
            "el reglamento describe la infraestructura",
            "no es un permiso para atravesar",
            "uso solo la entrada de mi sector",
            "brisas otun y cocora no se cruzan en carro",
        ],
        hard_negatives=[
            "mapa de los senderos autorizados",
            "días que el parque cierra",
            "multa por salir de la vía",
        ],
        short=(
            "El reglamento de diciembre de 2023 describe un circuito que cruza la parte alta: Manizales, La Esperanza, Brisas, el caballete de La Olleta, El Cisne, Santa Bárbara y Villamaría. "
            "Eso explica la infraestructura. No autoriza un paseo de un sector a otro. "
            "Usa solo la entrada del sector que vas a visitar."
        ),
        variants=[
            "Ver ese circuito de diciembre de 2023 no abre la carretera para ir de portería en portería. Cada ingreso se hace por su acceso publicado."
        ],
        sources=[FICHA, ANEXO],
        related=["access.stay_on_official_gate", "access.olleta_not_a_gate", "access.where_road_ends"],
        tags=["circuito", "2023", "sector"],
    ),
    entry(
        id="access.mountain_road_conditions",
        label="vías de montaña sin parte del día",
        kind="fact",
        examples=[
            "cómo está la vía hoy",
            "hay derrumbe en la destapada",
            "la pagina trae el parte de vías",
            "se pasa hoy al cisne",
            "carretera de montaña, quien avisa",
            "does the park page post today's road report",
            "is the dirt road open this morning",
            "niebla y derrumbe no estan en un boletin de la pagina",
            "planeo con el prestador del sector",
            "no hay un mapa de vias abiertas en la visita",
            "antes de salir pregunto si se pasa",
            "la terciaria puede cambiar",
        ],
        hard_negatives=[
            "pronóstico del IDEAM para mañana",
            "alerta volcánica de hoy",
            "cierre por conservación en noviembre",
        ],
        short=(
            "Hacia el Cisne la página habla de carreteras terciarias destapadas y pide planearlas con prestadores autorizados. "
            "No publica un parte de derrumbes ni si hoy se pasa. "
            "Confírmalo con el operador del sector antes de salir."
        ),
        variants=[
            "La página no trae el estado de la vía de esta mañana. En el Cisne son destapadas; pregunta al prestador de ese sector si el tramo se pasa."
        ],
        sources=[FICHA],
        related=["access.confirm_road_before", "access.dirt_roads_cisne", "access.pico_placa_north"],
        tags=["vía", "destapada", "estado"],
        entities={"sector": ["cisne"]},
    ),
    entry(
        id="access.confirm_road_before",
        label="confirmar el estado de la vía",
        kind="procedure",
        examples=[
            "confirmo la vía antes de salir",
            "el acceso puede cambiar",
            "obras o decision del parque",
            "donde miro si la carretera sigue",
            "no des por hecho que esta habilitada",
            "how do I check the road before leaving",
            "the access can change, where do I look",
            "pagina de parques y el operador del sector",
            "clima obra o volcan pueden cerrar el tramo",
            "si no pude confirmar, no lo doy por abierto",
            "revisar brisas ademas del pico y placa",
            "estado del corredor la esperanza",
        ],
        hard_negatives=[
            "el parque está abierto hoy",
            "boletín semanal del Ruiz",
            "grupo de WhatsApp de la vía",
        ],
        short=(
            "La página no publica si la vía está abierta hoy. El acceso cambia por clima, obra o una decisión del parque. "
            "Revísala, o confirma con el operador del sector, antes de salir. " + PICO
        ),
        variants=[
            "No des el tramo por habilitado si no lo confirmaste en la página o con el operador. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.mountain_road_conditions", "access.park_email_routes", "access.pico_placa_north"],
        tags=["confirmar", "vía", "cambio"],
    ),
    entry(
        id="access.operator_transport_other",
        label="transporte con operador en otros sectores",
        kind="procedure",
        examples=[
            "quién lleva el transporte fuera de brisas",
            "cocora no es uton",
            "operador registrado del sector",
            "el cedral con que agencia",
            "juntas y palomar se coordinan aparte",
            "who arranges transport outside Brisas",
            "is UTON the operator for Cocora",
            "en el cisne la uton no cubre el transporte",
            "lo gestiono yo o con un operador de ese ingreso",
            "cada sector tiene su gente",
            "no pidas el carro de brisas para el sur",
            "agencia registrada segun la puerta",
        ],
        hard_negatives=[
            "lista REPSE completa",
            "el guía es obligatorio en todos los sectores",
            "precio del operador en Cocora",
        ],
        short=(
            "Fuera de Brisas, la página dice que el transporte se coordina contigo o con un guía o una agencia registrada de ese sector. "
            "UTON es la concesión del norte; no la uses como el transporte de Cocora, Juntas, Palomar o El Cedral. "
            "En El Cisne el transporte va con la agencia registrada que elijas."
        ),
        variants=[
            "El transporte de los sectores distintos a Brisas se acuerda con un operador registrado de esa puerta, no con la concesión del norte."
        ],
        sources=[FICHA],
        related=["access.uton_brisas_transport", "access.organized_tour_transport", "access.no_park_shuttle"],
        tags=["operador", "transporte", "sectores"],
    ),
    entry(
        id="access.organized_tour_transport",
        label="llegar con un tour organizado",
        kind="procedure",
        examples=[
            "un tour me lleva al parque",
            "la agencia pone el carro y la puerta",
            "el tour inventa otra entrada",
            "salgo con operador al sector",
            "brisas con uton dentro del plan",
            "does a tour create a new gate",
            "can an agency drive me to a different entrance",
            "el norte sigue siendo brisas",
            "cocora sigue siendo cocora aunque vaya en tour",
            "el vehiculo lo organiza la agencia registrada",
            "no me saltan la porteria por ir en grupo",
            "tour al cisne por villamaria o santa rosa",
        ],
        hard_negatives=[
            "precio del tour",
            "cancelar la reserva del tour",
            "el guía va incluido",
        ],
        short=(
            "Un tour organiza el vehículo y el ingreso por la portería del sector. No crea otra vía: el norte sigue siendo Brisas, el Cisne sale por Villamaría o Santa Rosa, el Otún por Potosí o El Cedral, y el sur por Cocora, Juntas o Palomar. "
            "En Brisas ese operador es UTON. " + PICO
        ),
        variants=[
            "Ir con agencia no cambia la puerta. Brisas, Potosí, El Cedral, Cocora, Juntas y Palomar siguen siendo las entradas publicadas, y UTON es la del norte. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.operator_transport_other", "access.uton_brisas_transport", "access.four_sector_gates"],
        tags=["tour", "agencia", "portería"],
    ),
    entry(
        id="access.control_coordinates",
        label="coordenadas de los controles de ingreso",
        kind="fact",
        needs=["sector"],
        examples=[
            "coordenadas de la portería",
            "punto gps del control",
            "latitud de brisas",
            "coordenada de potosi",
            "el punto de cocora en grados",
            "GPS coordinates of the checkpoints",
            "are the 2023 coordinates still the gate",
            "la punta tiene coordenada publicada",
            "no las uses como el mostrador de hoy",
            "reglamento de diciembre de 2023",
            "dime brisas potosi cocora o la punta",
            "ubicacion vieja del registro",
        ],
        hard_negatives=[
            "coordenada del cráter Arenas",
            "track GPX para seguir en el teléfono",
            "altura de la cima del Ruiz",
        ],
        short=(
            "Las coordenadas publicadas están en la reglamentación transitoria de diciembre de 2023 y no garantizan que el control siga ahí. "
            "Dime si buscas Brisas, Potosí, Cocora o La Punta. No las cargues como el mostrador de hoy."
        ),
        variants=[
            "Esas coordenadas son de diciembre de 2023, no la ubicación asegurada del control actual. Pide Brisas, Potosí, Cocora o La Punta y confirma el punto con el operador."
        ],
        steps=[
            ["Brisas, reglamento de diciembre de 2023: N 04°56'0'' W 075°20'59'', 4.107 m. No es un control garantizado hoy."],
            ["Potosí, en ese mismo reglamento: N 04°49'52'' W 075°24'58'', 3.920 m. Confírmalo antes de salir; no reemplaza el registro."],
            ["Cocora, diciembre de 2023: puerta azul de la truchera, kilómetro 11, N 04°38'17,5'' W 075°29'11,3'', unos 2.400 m. La página actual nombra el Valle del Cocora y no repite ese punto."],
            ["La Punta, vereda La Cascada, diciembre de 2023, control flotante: N 04°38'10,7'' W 075°12'43,7'', 3.100 m. La página actual habla de Palomar, no de este punto."],
        ],
        sources=[ANEXO, FICHA],
        related=["access.brisas_entry_altitude", "access.potosi_control", "access.cocora_registration"],
        tags=["coordenadas", "2023", "control"],
        entities={"sector": ["brisas", "cisne", "quindio"]},
    ),
]
