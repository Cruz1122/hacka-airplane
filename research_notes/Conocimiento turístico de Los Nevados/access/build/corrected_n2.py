"""Corrected access entries: Brisas vehicle, contacts, Bogotá and Medellín."""

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

N2 = [
    entry(
        id="access.brisas_visitor_center",
        label="centro de visitantes Brisas",
        kind="fact",
        examples=[
            "dónde queda el centro de visitantes brisas",
            "brisas es la portería del norte",
            "centro de inducción y centro de visitantes es el mismo",
            "kumanday se entra por brisas",
            "la caseta del sector norte como se llama",
            "where is the Brisas visitor center",
            "is Brisas the north gate",
            "ahi empieza el carreteable al valle",
            "no queda en letras ni en murillo",
            "brisas sobre el corredor esperanza murillo",
            "registro del norte en que centro",
            "valle del silencio sale de ese centro",
        ],
        hard_negatives=[
            "hay baño y cafetería en Brisas",
            "a qué hora cierra la inducción",
            "precio de la guianza en Brisas",
        ],
        short=(
            "Brisas es la portería del sector norte, también llamado Brisas–Kumanday. "
            "La página lo nombra centro de visitantes y centro de inducción, y desde ahí sale el carreteable hacia el Valle de las Tumbas o Valle del Silencio. "
            "Queda sobre el corredor La Esperanza–Murillo, no en Letras ni en el pueblo de Murillo. " + PICO
        ),
        variants=[
            "El registro del norte es Brisas. Ahí empieza el recorrido en vehículo hacia el valle, después del corredor, no en Letras. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.from_manizales", "access.brisas_entry_altitude", "access.brisas_tumbas_drive"],
        tags=["brisas", "centro", "portería"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.brisas_entry_altitude",
        label="altura de la entrada Brisas",
        kind="fact",
        examples=[
            "a qué altura queda brisas",
            "la portería está a 4100",
            "cota del centro de inducción",
            "brisas queda tan alto como la cima",
            "cuantos metros tiene la entrada norte",
            "how high is the Brisas gate",
            "is 4100 the summit or the entrance",
            "altitud aproximada de brisas",
            "llego a registrarme y ya estoy a esa cota",
            "no es la altura del valle ni del crater",
            "el centro de induccion a cuantos metros",
            "altura de la caseta, no de la nieve",
        ],
        hard_negatives=[
            "altura de la cima del Ruiz",
            "síntomas del mal de altura",
            "cuánto oxigeno llevo a brisas",
        ],
        short=(
            "El centro de inducción Brisas está a unos 4.100 m, según la página actual de visita. "
            "Es la altura de esa entrada, no la de la cima ni la del final del carreteable."
        ),
        variants=[
            "Cuando te registras en Brisas estás cerca de 4.100 m. Esa cota es de la portería, no de la cumbre."
        ],
        detail=(
            "La página dice «a 4100 metros de altitud aproximadamente». "
            "La reglamentación transitoria de diciembre de 2023 anota el control de Brisas en 4.107 m. "
            "El Servicio Geológico también indica 4.100 m para Brisas, en una página sin fecha de publicación visible. "
            "Ninguna de esas cotas es la cumbre."
        ),
        sources=[FICHA, ANEXO, SGC],
        related=["access.brisas_visitor_center", "access.tumbas_end_altitude", "access.potosi_control"],
        tags=["altura", "brisas", "4100"],
    ),
    entry(
        id="access.brisas_tumbas_drive",
        label="carreteable de Brisas a Tumbas",
        kind="procedure",
        examples=[
            "el valle se recorre en carro",
            "de brisas a tumbas hay carreteable",
            "paso por arenales en vehículo",
            "no es un sendero a la cima",
            "el atractivo del norte es por carretera",
            "is the valley a drive from Brisas",
            "can I walk the summit from that road",
            "valle del silencio en carro cubierto",
            "despues del centro de induccion sigue el carro",
            "arenales queda en ese trayecto",
            "el recorrido norte no es una trocha a pie hasta el crater",
            "como es el carreteable del sector brisas",
        ],
        hard_negatives=[
            "puedo subir al cráter Arenas",
            "fotos comerciales en el valle",
            "hay nieve para esquiar",
        ],
        short=(
            "En el norte el recorrido publicado empieza en el centro de inducción Brisas, sigue en vehículo por Arenales y llega al Valle del Silencio o Valle de las Tumbas. "
            "Se hace en un vehículo cubierto. No es el camino a la cima. " + PICO
        ),
        variants=[
            "De Brisas al valle vas en vehículo cubierto, pasando por Arenales. La página no lo ofrece como sendero a la cumbre. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.covered_vehicle_required", "access.tumbas_and_silencio_same_road", "access.own_car_brisas"],
        tags=["carreteable", "tumbas", "arenales"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.tumbas_and_silencio_same_road",
        label="Tumbas y Valle del Silencio",
        kind="explanation",
        examples=[
            "tumbas y silencio son dos valles",
            "valle del silencio es otro acceso",
            "me dijeron tumbas y en la reserva dice silencio",
            "busco dos porterías, una por nombre",
            "el mismo carreteable tiene dos nombres",
            "are Tumbas and Valle del Silencio different gates",
            "which name is the end of the Brisas road",
            "no quiero ir al valle equivocado",
            "silencio o tumbas, entro por brisas igual",
            "es un solo atractivo con dos letreros",
            "la reserva dice silencio y yo pedia tumbas",
            "hay que escoger entre los dos nombres",
        ],
        hard_negatives=[
            "dónde queda el valle en el mapa geológico",
            "leyenda del valle del silencio",
            "puedo acampar en tumbas",
        ],
        short=(
            "No busques dos porterías. La página usa Valle de las Tumbas y Valle del Silencio para el mismo recorrido que sale de Brisas. "
            "Entras por el centro de visitantes y el vehículo sigue hasta ese valle."
        ),
        variants=[
            "Tumbas y Silencio son dos nombres del mismo tramo en carro desde Brisas. La reserva y el letrero hablan del mismo final."
        ],
        sources=[FICHA],
        related=["access.brisas_tumbas_drive", "access.brisas_visitor_center", "access.tumbas_end_altitude"],
        tags=["tumbas", "silencio", "nombre"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.tumbas_end_altitude",
        label="altura al final del carreteable",
        kind="fact",
        examples=[
            "a qué altura termina el carro",
            "cota del valle de las tumbas",
            "el final del carreteable es la cima",
            "cuantos metros hay en tumbas",
            "la nieve empieza donde para el vehículo",
            "how high is the end of the Brisas road",
            "does the car reach the snow line",
            "altura del valle, no de brisas",
            "me dieron dos cotas distintas del valle",
            "4.400 o 4.450, cual uso",
            "la pagina de ahora trae la altura del valle",
            "no quiero confundir la porteria con el final",
        ],
        hard_negatives=[
            "altura del cráter Arenas",
            "retroceso del glaciar en metros",
            "riesgo de hipotermia en el valle",
        ],
        short=(
            "La página actual no publica una sola altura para el final del carreteable en el Valle de las Tumbas. "
            "No uses una cota suelta para creer que el carro llega a la nieve: el tramo habilitado lo define Parques para tu fecha."
        ),
        variants=[
            "No hay una cifra única y vigente del final del valle en la página de visita. Una altura vieja no prueba que el vehículo llegue a la nieve."
        ],
        detail=(
            "El Servicio Geológico ubica el Valle de las Tumbas a 4.450 m en su página de generalidades, que no muestra fecha de publicación. "
            "La guía de Parques de abril de 2016 decía 4.400 m y 5 km después de Brisas, y en ese texto ligaba el sector a una alerta amarilla desde 2010. "
            "La página actual no repite esa alerta ni elige una de esas cotas. El mismo Servicio Geológico pide consultar a Parques por las restricciones vigentes."
        ),
        sources=[FICHA, SGC, GUIDE_2016],
        related=["access.brisas_entry_altitude", "access.brisas_tumbas_drive", "access.from_bogota"],
        tags=["altura", "tumbas", "valle"],
    ),
    entry(
        id="access.own_car_brisas",
        label="llegar en carro propio a Brisas",
        kind="procedure",
        examples=[
            "puedo subir en mi carro",
            "llego a brisas con el vehículo propio",
            "se puede entrar en carro particular",
            "mi carro pasa a la portería",
            "puedo entrar con mi vehiculo",
            "can I drive my own car to Brisas",
            "is a private car allowed at the north gate",
            "voy en carro de la casa hasta el centro",
            "el valle es otra cosa, yo pregunto por llegar",
            "carro propio si, moto no",
            "subo en el mío o me toca dejarlo abajo",
            "particular hasta brisas esta permitido",
        ],
        hard_negatives=[
            "cuánto cobran por el carro",
            "seguro del vehículo lo exige el parque",
            "hay gasolina en Brisas",
        ],
        short=(
            "Sí puedes llegar en tu carro al centro de visitantes Brisas: la página lo dice. "
            "El tramo del valle es aparte y se hace en un vehículo cubierto, que puede ser el tuyo o uno contratado; las motos no entran al atractivo. " + PICO
        ),
        variants=[
            "Tu carro puede llegar a Brisas. Para seguir al valle tiene que ser un vehículo cubierto, y la moto no está permitida en el atractivo. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.covered_vehicle_required", "access.no_motorcycles", "access.parking_at_brisas"],
        tags=["carro", "brisas", "propio"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.no_motorcycles",
        label="las motos no entran a Brisas",
        kind="rule",
        examples=[
            "puedo ir en moto",
            "la moto entra a brisas",
            "enduro hasta el valle",
            "moto de viaje la dejan pasar",
            "está prohibida la moto en el atractivo",
            "are motorcycles allowed at Brisas",
            "can I ride to the valley",
            "en la tabla tambien dice moto prohibida",
            "hay alguna excepcion para motos",
            "subo en moto hasta la porteria y ahi la dejo",
            "dos ruedas no pasan al recorrido",
            "me dijeron que en semana la moto si entra",
        ],
        hard_negatives=[
            "alquiler de motos en Manizales",
            "casco obligatorio en la vía nacional",
            "pico y placa de motos en la ciudad",
        ],
        short=(
            "La página no permite el ingreso de motos al atractivo de Brisas y lo repite en las tablas de vehículos. "
            "Puedes llegar en carro y hacer el valle en un vehículo cubierto; no hay una excepción publicada para moto de viaje o de enduro. " + PICO
        ),
        variants=[
            "La moto sigue prohibida en el atractivo de Brisas. El pico y placa de noviembre no abre una excepción para motos: regula placas en ese acceso, de 5:00 a. m. a 4:00 p. m., fines de semana y puentes, Resolución 1815 del 24 de julio de 2026."
        ],
        sources=[FICHA],
        related=["access.own_car_brisas", "access.covered_vehicle_required", "access.bus_or_van_entry"],
        tags=["moto", "prohibido", "brisas"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.covered_vehicle_required",
        label="vehículo cubierto hacia el valle",
        kind="rule",
        examples=[
            "el valle pide vehículo cubierto",
            "puedo seguir en carro destapado",
            "un convertible pasa de brisas a tumbas",
            "carro sin techo cuenta como cubierto",
            "el mío tiene techo, sirve",
            "does the valley require a covered vehicle",
            "is an open jeep allowed past Brisas",
            "propio o contratado, los dos sirven si van cubiertos",
            "la moto no reemplaza al vehículo cubierto",
            "que quiere decir cubierto, la pagina lo define",
            "contratar el carro alla mismo",
            "antes de subir pregunto si el mío vale",
        ],
        hard_negatives=[
            "qué marca de 4x4 recomiendan",
            "llantas para nieve qué medida",
            "precio del carro contratado",
        ],
        short=(
            "Para seguir de Brisas al Valle de las Tumbas la página pide un vehículo cubierto, propio o contratado antes o en el sitio. "
            "No define marcas ni dice si un carro sin techo cuenta, y las motos siguen prohibidas. Confírmalo con UTON antes de subir. " + PICO
        ),
        variants=[
            "El tramo del valle es en vehículo cubierto. La página no aclara el carro sin techo, así que pregúntale a UTON, y no cuentes con la moto. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.brisas_tumbas_drive", "access.hire_vehicle_brisas", "access.own_car_brisas"],
        tags=["cubierto", "valle", "uton"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.parking_at_brisas",
        label="dejar el carro en el centro",
        kind="fact",
        examples=[
            "hay parqueadero en brisas",
            "dejo el carro en el centro de visitantes",
            "cuántos cupos hay para parquear",
            "plano de celdas en brisas",
            "puedo dejar el carro y seguir en otro",
            "is there a parking lot at Brisas",
            "how many parking spaces are published",
            "llego en el mío y lo dejo en la caseta",
            "no encuentro un mapa del parqueadero",
            "el carro se queda en brisas mientras subo al valle",
            "hay bahia publicada para visitantes",
            "parqueo del centro, lo dice la pagina",
        ],
        hard_negatives=[
            "cuánto cobran el parqueadero",
            "hay vigilante toda la noche",
            "el derecho de ingreso del carro es parqueadero",
        ],
        short=(
            "Puedes llegar en tu carro hasta Brisas. La página no publica un cupo de parqueadero ni un plano de celdas. "
            "Si dejas el tuyo y sigues al valle, ese tramo es en vehículo cubierto. " + PICO
        ),
        variants=[
            "No hay un número de celdas ni un plano publicados. El carro puede llegar al centro, y el valle sigue en vehículo cubierto. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.own_car_brisas", "access.hire_vehicle_brisas", "access.covered_vehicle_required"],
        tags=["parqueadero", "brisas", "carro"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.hire_vehicle_brisas",
        label="contratar vehículo en Brisas",
        kind="procedure",
        examples=[
            "contrato el carro en brisas",
            "hay vehículo para el valle en el sitio",
            "lo puedo reservar antes de subir",
            "uton alquila el recorrido",
            "propio o contratado allí mismo",
            "can I hire the valley vehicle at Brisas",
            "should I book the car before I arrive",
            "no llevo carro cubierto, lo consigo arriba",
            "el transporte del norte lo gestiona la concesion",
            "quiero el carro del valle con la uton",
            "se contrata con anterioridad o en la caseta",
            "no es un bus publico, es el vehículo del recorrido",
        ],
        hard_negatives=[
            "tarifa del transporte en Brisas",
            "incluye seguro el carro contratado",
            "horario de la oficina de UTON",
        ],
        short=(
            "La página permite hacer el valle en un vehículo cubierto contratado en Brisas o antes. "
            "En ese sector el transporte lo gestiona la concesión UTON, no un cupo que la página numere. " + PICO
        ),
        variants=[
            "Puedes contratar el vehículo del valle con UTON, allí o por adelantado. La página no publica un cupo. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.uton_brisas_transport", "access.covered_vehicle_required", "access.uton_offices_manizales"],
        tags=["uton", "contratar", "vehículo"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.bus_or_van_entry",
        label="bus o buseta hacia Brisas",
        kind="fact",
        examples=[
            "puedo entrar en bus",
            "la buseta sube a brisas",
            "un microbus entra al valle",
            "colectivo hasta la portería",
            "la tabla de tarifas autoriza el bus",
            "does a fee category mean my bus can enter",
            "is a van allowed on the Brisas road today",
            "buseta o bus, la pagina los nombra distinto",
            "quiero subir un bus de 30 y no se si cabe",
            "la moto no, pero el bus si o no",
            "no confundir la tarifa con el permiso del dia",
            "pico y placa y ademas la categoria del vehiculo",
        ],
        hard_negatives=[
            "cuánto vale el ingreso del bus",
            "horario del bus urbano a Brisas",
            "empresa de flota que sube al parque",
        ],
        short=(
            "En Brisas puedes llegar en tu vehículo y recorrer el valle en uno cubierto; las motos están prohibidas. "
            "Las tablas de tarifas nombran bus, buseta o colectivo, pero no son el permiso para que ese vehículo circule ese día: la misma página las rotula de dos formas. "
            "Confírmalo con UTON. " + PICO
        ),
        variants=[
            "Que exista una categoría de bus o buseta en la tarifa no autoriza el ingreso de hoy. "
            "La vía del valle pide vehículo cubierto, la moto está prohibida y UTON confirma el vehículo. " + PICO_V
        ],
        detail=(
            "En el bloque de Brisas la página lista automóvil, colectivo y buseta, y en otro cuadro automóvil, microbús o buseta, y bus. "
            "La moto figura prohibida en ambos. Los valores en pesos están en la tabla de 2026 y no se responden aquí. "
            "Ninguno de los dos cuadros dice que el vehículo esté autorizado en la vía durante el pico y placa de noviembre."
        ),
        sources=[FICHA],
        related=["access.no_motorcycles", "access.no_public_bus", "access.own_car_brisas"],
        tags=["bus", "buseta", "tarifa"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.taxi_not_published",
        label="taxi hasta la portería",
        kind="fact",
        examples=[
            "hay taxi hasta brisas",
            "un taxi me deja en la portería",
            "tomo un taxi en manizales al parque",
            "la pagina publica una ruta de taxi",
            "el taxi cuenta como transporte del parque",
            "is there an official taxi to the gate",
            "can a taxi drive me to Brisas",
            "no veo taxis en como llegar",
            "uber o taxi hasta el centro de visitantes",
            "si el taxi sube, igual mira el pico y placa",
            "no esta descrito como servicio de la concesion",
            "llegar en taxi no aparece escrito",
        ],
        hard_negatives=[
            "tarifa del taxi Manizales Brisas",
            "apps de taxi en Manizales",
            "turno del pico y placa en la ciudad",
        ],
        short=(
            "La página no publica una ruta de taxi hasta la portería ni lo describe como servicio del parque. "
            "A Brisas puedes llegar en tu vehículo o con el transporte que gestiona UTON. " + PICO
        ),
        variants=[
            "No hay un taxi oficial escrito en cómo llegar. Si un carro particular sube a Brisas, no está exento del pico y placa de noviembre. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.hire_vehicle_brisas", "access.no_public_bus", "access.covered_vehicle_required"],
        tags=["taxi", "brisas", "transporte"],
        entities={"sector": ["brisas"]},
    ),
    entry(
        id="access.no_park_shuttle",
        label="el parque no opera transporte interno",
        kind="fact",
        examples=[
            "hay bus interno del parque",
            "parques nacionales me lleva entre sectores",
            "hay shuttle de brisas al valle",
            "el parque opera la buseta",
            "transporte al interior lo pone el parque",
            "does the park run an internal shuttle",
            "is there a park bus between gates",
            "quien opera el transporte si el parque no",
            "en brisas es la uton, en los otros un operador",
            "no hay carro oficial de un sector a otro",
            "tengo que coordinar el transporte yo",
            "de la porteria al atractivo no hay servicio del parque",
        ],
        hard_negatives=[
            "precio del transporte interno",
            "el guía es obligatorio",
            "porteo de maletas con mula",
        ],
        short=(
            "El parque no cuenta con servicio de transporte al interior. "
            "En Brisas el transporte lo gestiona la concesión UTON. En los demás sectores se coordina contigo o con un operador registrado de ese ingreso. " + PICO
        ),
        variants=[
            "No hay un shuttle del parque entre porterías. Brisas se mueve con UTON; los otros sectores, con un operador registrado o por tu cuenta. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.no_public_bus", "access.uton_brisas_transport", "access.operator_transport_other"],
        tags=["transporte", "uton", "interno"],
    ),
    entry(
        id="access.no_public_bus",
        label="bus público hasta la portería",
        kind="fact",
        examples=[
            "hay bus urbano hasta brisas",
            "qué bus intermunicipal llega a la portería",
            "ruta de bus público al parque",
            "me bajo del bus en la caseta",
            "la terminal tiene despacho al nevado",
            "is there a public bus to the gate",
            "which city bus stops at Brisas",
            "no veo empresa ni horario publicados",
            "buseta de tarifa no es una ruta urbana",
            "como llego en transporte publico al sector norte",
            "hay colectivo de pueblo en pueblo hasta la entrada",
            "la pagina no trae terminal ni frecuencia",
        ],
        hard_negatives=[
            "horario de la terminal de Manizales",
            "pasaje del bus a Murillo",
            "la buseta de la tarifa cuesta",
        ],
        short=(
            "La página no publica una ruta de bus urbano ni intermunicipal hasta una portería, ni empresa ni horario. "
            "Que la tarifa de Brisas nombre bus o buseta no crea esa línea. " + PICO
        ),
        variants=[
            "No hay un bus público escrito hasta la caseta. La categoría de la tarifa es otra cosa, y en noviembre el acceso a Brisas tiene pico y placa de 5:00 a. m. a 4:00 p. m. los fines de semana y puentes, Resolución 1815 del 24 de julio de 2026."
        ],
        sources=[FICHA],
        related=["access.no_park_shuttle", "access.always_by_land", "access.organized_tour_transport"],
        tags=["bus", "público", "ruta"],
    ),
    entry(
        id="access.uton_brisas_transport",
        label="transporte de Brisas con UTON",
        kind="procedure",
        examples=[
            "quién lleva el transporte en brisas",
            "uton es la concesión del norte",
            "operacion nevados organiza el carro",
            "la uton gestiona transporte y guianza allá",
            "para brisas no busco otra agencia",
            "who runs transport at Brisas",
            "is UTON the north operator",
            "el sitio operacionnevados sale en la pagina",
            "reservas ingreso y transporte van con la concesion",
            "la union temporal es quien mueve brisas",
            "en el cisne la uton no es el mismo paquete de transporte",
            "brisa kumanday se coordina con uton",
        ],
        hard_negatives=[
            "teléfono de UTON",
            "precio de la guianza de UTON",
            "oficina de la concesión en qué calle",
        ],
        short=(
            "En Brisas–Kumanday el operador autorizado es la concesión UTON: gestiona reservas, ingreso, guianza, transporte y tienda. "
            "La página publica el enlace https://www.operacionnevados.co. " + PICO
        ),
        variants=[
            "El transporte del sector norte se pide a UTON, la concesión que la página nombra para Brisas. " + PICO_V
        ],
        sources=[FICHA],
        related=["access.uton_offices_manizales", "access.hire_vehicle_brisas", "access.operator_transport_other"],
        tags=["uton", "brisas", "concesión"],
        entities={"sector": ["brisas"]},
    ),
]
