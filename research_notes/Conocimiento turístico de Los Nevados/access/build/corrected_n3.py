"""Corrected access entries: contacts, kilometer conflicts, Bogotá and Medellín."""

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

N3 = [
    entry(
        id="access.uton_offices_manizales",
        label="oficinas de UTON en Manizales",
        kind="fact",
        examples=[
            "dónde queda la oficina de uton",
            "dirección de la concesión en manizales",
            "carrera 26a 68-44 es de uton",
            "calle 70 27-70 también es oficina",
            "barrio palermo, la concesion atiende ahi",
            "UTON office addresses in Manizales",
            "what phone numbers does the park page list for UTON",
            "horario de la oficina entre semana",
            "dos sedes, palermo y la calle 70",
            "celulares 321 506 6031 y 322 360 3637",
            "atienden lunes a viernes mañana y tarde",
            "confirmo los datos porque pueden cambiar",
        ],
        hard_negatives=[
            "horario de la portería de Brisas",
            "correo de la concesión que la página ocultó",
            "precio de la reserva con UTON",
        ],
        short=(
            "La página lista dos oficinas de UTON en Manizales: carrera 26A #68-44, barrio Palermo, y calle 70 #27-70. "
            "Atienden lunes a viernes de 8:00 a. m. a 12:00 m. y de 2:00 p. m. a 5:00 p. m., y publica los celulares 321 506 6031 y 322 360 3637. "
            "Vuelve a mirar la página antes de ir: pueden cambiar."
        ),
        variants=[
            "Confirma en la página las dos sedes de Manizales, carrera 26A #68-44 en Palermo y calle 70 #27-70, los celulares 321 506 6031 y 322 360 3637, y el horario de lunes a viernes de 8:00 a. m. a 12:00 m. y de 2:00 p. m. a 5:00 p. m., porque pueden cambiar."
        ],
        sources=[FICHA],
        related=["access.uton_brisas_transport", "access.park_email_routes", "access.park_or_concession_contact"],
        tags=["uton", "oficina", "teléfono"],
        entities={"origin": ["manizales"]},
    ),
    entry(
        id="access.park_email_routes",
        label="correo del parque para la visita",
        kind="fact",
        examples=[
            "correo del parque los nevados",
            "nevados@parquesnacionales.gov.co",
            "a qué mail escribo por la vía",
            "email del area protegida",
            "escribir al parque antes de salir",
            "what email does the park page publish",
            "is nevados@parquesnacionales.gov.co the visit address",
            "no es el correo de la concesion",
            "dudas de la visita al area protegida",
            "mail oficial que si se ve en la pagina",
            "los de uton salen ocultos, el del parque no",
            "confirmo el correo en la pagina por si cambia",
        ],
        hard_negatives=[
            "correo para un permiso de investigación",
            "radicar una queja en Bogotá",
            "email de la alcaldía de Manizales",
        ],
        short=(
            "Para saber más de la visita, la página publica nevados@parquesnacionales.gov.co. "
            "No es el correo de la concesión: los de UTON no se leen en la página. "
            "Si el mensaje rebota, vuelve a leer la página."
        ),
        variants=[
            "El correo visible del área es nevados@parquesnacionales.gov.co. Úsalo para la visita y confírmalo en la página si cambia."
        ],
        sources=[FICHA],
        related=["access.park_or_concession_contact", "access.confirm_road_before", "access.uton_offices_manizales"],
        tags=["correo", "contacto", "parques"],
    ),
    entry(
        id="access.park_or_concession_contact",
        label="parque o concesión, a quién escribir",
        kind="procedure",
        examples=[
            "escribo a uton o al parque",
            "brisa se coordina con la concesion",
            "los otros sectores no son uton",
            "a quien le pido el transporte del norte",
            "el correo del parque no reserva el valle",
            "who do I contact for Brisas versus another sector",
            "is the park email the same as UTON",
            "concesion para brisas, agencia para el resto",
            "no mezclo el mail del area con la oficina de palermo",
            "transporte del cisne no se lo pido a uton",
            "dos contactos distintos segun el sector",
            "uton en brisas y operador registrado en los demas",
        ],
        hard_negatives=[
            "teléfono de emergencias",
            "guardar el reporte de una emergencia",
            "número de la policía de carreteras",
        ],
        short=(
            "En Brisas el transporte y el ingreso se coordinan con UTON. En los otros sectores, con un operador registrado de ese ingreso. "
            "El correo nevados@parquesnacionales.gov.co es el del área protegida, no la oficina de la concesión. " + PICO
        ),
        variants=[
            "UTON es el contacto del norte. Los demás sectores van con su operador, y el correo del parque no reemplaza a la concesión. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.park_email_routes", "access.uton_brisas_transport", "access.operator_transport_other"],
        tags=["contacto", "uton", "correo"],
    ),
    entry(
        id="access.pico_placa_north",
        label="pico y placa en el acceso norte",
        kind="rule",
        examples=[
            "hay pico y placa para subir a brisas",
            "restriccion de placas en noviembre",
            "fines de semana no dejan pasar cualquier carro",
            "resolucion 1815 del tolima",
            "de 5 de la mañana a 4 de la tarde",
            "is there a plate restriction on the north access",
            "does the November rule apply on weekdays",
            "puentes festivos en el acceso al valle",
            "pico y placa ambiental del tolima",
            "reviso las placas al reservar",
            "brisas valle de las tumbas, cuales carros circulan",
            "no es el pico y placa de manizales ciudad",
        ],
        hard_negatives=[
            "pico y placa en Manizales el lunes",
            "comparendo si me cogen sin placa",
            "el parque cierra en noviembre",
        ],
        short=(
            "La página avisa, para el acceso Brisas–Valle de las Tumbas, el pico y placa ambiental del Tolima, Resolución 1815 del 24 de julio de 2026. "
            "Aplica en noviembre, fines de semana y puentes, de 5:00 a. m. a 4:00 p. m. "
            "Revisa el cronograma de placas al reservar: no es una regla de todo el año ni de las otras porterías."
        ),
        variants=[
            "En noviembre, sábado, domingo y puente, de 5:00 a. m. a 4:00 p. m., el Tolima restringe placas en el acceso a Brisas y al valle, por la Resolución 1815 del 24 de julio de 2026. Mira el calendario al reservar; las otras entradas no quedan cubiertas por ese aviso."
        ],
        sources=[FICHA],
        related=["access.own_car_brisas", "access.confirm_road_before", "access.from_manizales"],
        tags=["pico y placa", "noviembre", "brisas"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.stay_on_official_gate",
        label="usar la portería publicada",
        kind="rule",
        examples=[
            "me meto por un hueco que vi en el mapa",
            "hay un atajo sin caseta",
            "entro por donde salen los de la vereda",
            "sin registro se puede colar",
            "una trocha mas corta que la porteria",
            "can I skip the official gate",
            "is an unmarked track an entrance",
            "solo uso la puerta del sector que voy a visitar",
            "no mezclo brisas con cocora en el mismo ingreso",
            "el mapa muestra una linea, esa cuenta",
            "paso por el control que publica la pagina",
            "atajo de moto o de a pie por fuera",
        ],
        hard_negatives=[
            "multa por salirme del sendero",
            "puedo llevar el dron",
            "sanción por entrar sin guía",
        ],
        short=(
            "Entra por la portería que la página publica para tu sector y regístrate ahí. "
            "Una línea en un mapa no es una entrada verificada. Brisas, Potosí y Santa Bárbara, El Cedral, Cocora, Juntas y Palomar no se cambian entre sí."
        ),
        variants=[
            "Usa solo la puerta publicada del sector que vas a visitar. No tomes un atajo que esta respuesta no tenga escrito."
        ],
        sources=[FICHA],
        related=["access.brisas_visitor_center", "access.circuit_not_scenic_loop", "access.esperanza_murillo_corridor"],
        tags=["portería", "registro", "atajo"],
    ),
    entry(
        id="access.ignore_single_kilometer",
        label="no fiarse de un solo kilómetro",
        kind="explanation",
        examples=[
            "en qué kilómetro me desvío",
            "poste 23 o poste 45",
            "cuantos kilometros hay antes de brisas",
            "el ocho queda en el km 45",
            "la esperanza es el km 23",
            "which kilometer marker is the turnoff",
            "why do the official kilometer posts disagree",
            "18 km y luego el desvio, es el de ahora",
            "no coinciden los postes, que hago",
            "sigo los nombres y no el numero",
            "la esperanza el ocho murillo y brisas",
            "un solo km me puede dejar mal",
        ],
        hard_negatives=[
            "kilómetros de la vía Bogotá Villavicencio",
            "odómetro del carro cómo se calibra",
            "distancia de la cima al cráter",
        ],
        short=(
            "No hay un poste único para el desvío. Sigue La Esperanza o El Ocho, sobre la carretera Manizales–Bogotá, y de ahí el corredor hacia Murillo hasta Brisas. "
            "Las cifras publicadas no coinciden, así que confírmalas con el operador. " + PICO
        ),
        variants=[
            "No navegues por un solo kilómetro. Los nombres que sí se repiten son La Esperanza, El Ocho, Murillo y Brisas. " + PICO_V
        ],
        detail=(
            "La guía en inglés de abril de 2016 pone el giro en el kilómetro 23 de La Esperanza y luego 14 km hasta el cruce de Murillo. "
            "La reglamentación transitoria de diciembre de 2023 dice el kilómetro 45 en La Esperanza o El Ocho, y 1 km entre el cruce de Murillo y Brisas. "
            "El Servicio Geológico, en su página de generalidades y sin fecha de publicación visible, habla de unos 18 km por la vía La Esperanza–Murillo antes del desvío. "
            "La página actual nombra el corredor y no publica un poste."
        ),
        sources=[FICHA, ANEXO, SGC, GUIDE_2016],
        related=["access.esperanza_murillo_corridor", "access.from_manizales", "access.manizales_brisas_distance"],
        tags=["kilómetro", "esperanza", "desvío"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.manizales_brisas_distance",
        label="distancia Manizales hasta Brisas",
        kind="fact",
        examples=[
            "cuántos kilómetros de manizales a brisas",
            "40 km es la vía de ahora",
            "28 km hasta el volcán sirven para el carro",
            "la pagina trae la distancia por carretera",
            "manizales brisas cuantos km",
            "how far is the drive from Manizales to Brisas",
            "is 28 km the road distance",
            "no quiero la distancia en linea recta",
            "el reglamento viejo decia 40",
            "la distancia del volcan no es el recorrido en carro",
            "cuanto falta por carretera de verdad",
            "distancia del centro de manizales a la porteria",
        ],
        hard_negatives=[
            "altura del Ruiz en metros",
            "tiempo en bus Manizales Pereira",
            "kilómetros del glaciar que se derritieron",
        ],
        short=(
            "La página actual no publica los kilómetros por carretera entre Manizales y Brisas. "
            "No uses la distancia del volcán a la ciudad como si fuera ese recorrido. " + PICO
        ),
        variants=[
            "No hay un kilometraje vigente de Manizales a Brisas en la página de visita. Los 28 km del volcán no son esa carretera. " + PICO_V
        ],
        detail=(
            "La reglamentación transitoria de diciembre de 2023 anota 40 km para Manizales–La Esperanza–cabaña Brisas. "
            "El Servicio Geológico indica 28 km al sureste de Manizales como posición del volcán, en una página sin fecha de publicación visible. "
            "No son la misma medida, y la página actual no repite los 40 km."
        ),
        sources=[FICHA, ANEXO, SGC],
        related=["access.from_manizales", "access.la_enea_alternate", "access.ignore_single_kilometer"],
        tags=["distancia", "manizales", "brisas"],
        entities={"origin": ["manizales"], "sector": ["brisas"]},
    ),
    entry(
        id="access.from_bogota",
        label="cómo llegar desde Bogotá",
        kind="procedure",
        examples=[
            "cómo llego desde bogotá al parque",
            "salgo de bogotá, por cuál puerta",
            "la vía bogotá manizales pasa por letras",
            "tengo que entrar a manizales antes del desvío",
            "desde bogotá al valle de cocora es otra ruta",
            "how do I get to the park from Bogotá",
            "must I reach Manizales city before the Letras turnoff",
            "bogota a brisas por la carretera a caldas",
            "si voy al tolima no paso por manizales",
            "el desvio de la esperanza se toma en la via, sin meterme a la ciudad",
            "bogota y varias porterias, cual me toca",
            "no busco un vuelo a la caseta, busco la carretera",
        ],
        hard_negatives=[
            "pasaje de avión Bogotá Manizales",
            "terminal de Salitre a qué hora sale",
            "140 km en línea recta hasta el cráter",
        ],
        short=(
            "Desde Bogotá no hay una portería propia. Para el norte, la referencia es la carretera hacia Manizales por Letras: tomas el corredor La Esperanza–Murillo hasta Brisas sin necesidad de entrar al casco de Manizales. "
            "Para el Cisne, el Otún o el Tolima usa la puerta de ese sector, no desvíes a Manizales. " + PICO
        ),
        variants=[
            "Si vas a Brisas, sigues la Bogotá–Manizales por Letras y giras al corredor de La Esperanza; no hace falta cruzar la ciudad. "
            "Cocora, Juntas, Palomar, Pereira, Villamaría y Santa Rosa son otras puertas. " + PICO_V
        ],
        detail=(
            "El Servicio Geológico ubica el Nevado del Ruiz a 140 km al noroeste de Bogotá y a 28 km al sureste de Manizales. Esa página de generalidades no muestra fecha de publicación. "
            "Es la posición del volcán, no los kilómetros de carretera hasta una portería."
        ),
        sources=[FICHA, SGC],
        related=["access.letras_highway", "access.from_ibague_choose", "access.manizales_brisas_distance"],
        tags=["bogotá", "letras", "brisas"],
        entities={"origin": ["bogota"]},
    ),
    entry(
        id="access.from_medellin",
        label="cómo llegar desde Medellín",
        kind="procedure",
        examples=[
            "cómo llego desde medellín",
            "hay vía publicada medellín parque",
            "salgo de medellín, cuál portería",
            "medellin a brisas no está escrita",
            "desde antioquia por donde entro",
            "how do I get there from Medellín",
            "is there an official Medellín-to-gate road",
            "no quiero un atajo inventado desde medellin",
            "elijo sector y uso esa puerta",
            "medellin pereira o medellin manizales, la pagina no escoge",
            "llegar desde medellin al nevado",
            "no hay kilometros oficiales desde alla",
        ],
        hard_negatives=[
            "vuelo Medellín Manizales",
            "peajes de la autopista a Caldas",
            "tiempo en carro Medellín Pereira",
        ],
        short=(
            "La página no publica una ruta desde Medellín hasta una portería, ni kilómetros de ese recorrido. "
            "Elige el sector y usa la puerta que sí está escrita: Brisas por Letras y La Esperanza, el Cisne por Villamaría o Santa Rosa, el Otún por El Cedral o Potosí, el sur por Cocora, Juntas o Palomar. " + PICO
        ),
        variants=[
            "No hay un camino Medellín–caseta en la página. Llegas a la puerta publicada del sector que elegiste, sin un desvío inventado. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.from_manizales", "access.from_pereira_choose", "access.always_by_land"],
        tags=["medellín", "ruta", "portería"],
        entities={"origin": ["medellin"]},
    ),
    entry(
        id="access.no_official_travel_time",
        label="sin tiempo oficial de viaje",
        kind="fact",
        examples=[
            "cuánto me demoro en carro",
            "horas de manizales a brisas",
            "cuanto es la caminata a la laguna",
            "la pagina dice las horas",
            "7 horas es el dato de ahora",
            "how long is the drive to the gate",
            "does the current page publish a walking time",
            "no me des un tiempo de una guia vieja",
            "minutos hasta el valle",
            "cuanto tardo de salento al limite",
            "tiempo de viaje no esta publicado",
            "demora del camino, dato oficial",
        ],
        hard_negatives=[
            "horario de apertura de Brisas",
            "a qué hora anochece",
            "pronóstico de mañana",
        ],
        short=(
            "La página actual no publica cuánto se demora el carro ni la caminata. "
            "No te doy horas de guías viejas como si fueran el tiempo de hoy. Confirma el tramo con el operador del sector. " + PICO
        ),
        variants=[
            "No hay una duración vigente en la página de visita. Un horario de 2016 no es tu tiempo de carretera, y en Brisas sigue el pico y placa de noviembre: fines de semana y puentes, de 5:00 a. m. a 4:00 p. m., Resolución 1815 del 24 de julio de 2026."
        ],
        sources=[FICHA],
        related=["access.cedral_walk_distances", "access.confirm_road_before", "access.mountain_road_conditions"],
        tags=["tiempo", "carro", "caminata"],
    ),
]
