"""Round-2 corrections for the frozen access snapshot.

`apply` upserts by id. It rewrites answers whose figures or rules are not in a
downloaded source, and adds routes the Manizales terminal actually publishes.
"""

from __future__ import annotations


def _set_short(entry: dict, short: str, variant: str) -> None:
    if len(short) > 320:
        raise ValueError(f"{entry['id']}: short is {len(short)} chars")
    entry["answer"]["short"] = short
    entry["answer"]["variants"] = [variant]


def _replace_answer(entry: dict, old: str, new: str) -> None:
    answer = entry["answer"]

    def walk(value):
        if isinstance(value, str):
            return value.replace(old, new)
        if isinstance(value, list):
            return [walk(item) for item in value]
        return value

    for key in list(answer):
        answer[key] = walk(answer[key])


def _entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    negatives: list[str],
    short: str,
    variant: str,
    related: list[str],
    sources: list[dict],
    entities: dict,
    tags: list[str],
    detail: str | None = None,
) -> dict:
    if len(examples) < 12:
        raise ValueError(entry_id)
    return {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "entities": entities,
        "needs": [],
        "answer": {
            "short": short,
            "variants": [variant],
            "steps": [[variant]],
            "detail": detail,
            "reflection": "Confirma el dato en el canal oficial antes de salir: las rutas publicadas cambian.",
        },
        "sources": sources,
        "last_verified": "2026-11-21",
        "valid_until": None,
        "related": related,
        "tags": tags,
    }


PNN = {
    "label": "Parques Nacionales Naturales de Colombia",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21",
}
ANEXO = {
    "label": "Reglamentación transitoria de ecoturismo, diciembre de 2023",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf",
    "retrieved_at": "2026-11-21",
}
INVIAS = {
    "label": "Instituto Nacional de Vías, estado de la red vial",
    "url": "https://www.invias.gov.co/publicaciones/4217/estado-de-la-red-vial/",
    "retrieved_at": "2026-11-21",
}


def _terminal(page: int) -> dict:
    return {
        "label": "Terminal de Transportes de Manizales, buscador de rutas",
        "url": (
            "https://terminaldemanizales.com.co/institucional/buscador-de-rutas/"
            f"?jsf=jet-engine:lista-rutas&pagenum={page}"
        ),
        "retrieved_at": "2026-11-21",
    }


def _buses() -> list[dict]:
    murillo = (
        "La Terminal de Transportes de Manizales publica un servicio de Rápido Tolima "
        "con destino Murillo, por la vía Letras. Murillo no es la portería: desde la "
        "cabecera sigues el corredor hasta Brisas. La tarifa y el horario cambian: "
        "confírmalos en el buscador de la terminal antes de salir."
    )
    ocho = (
        "La terminal de Manizales publica Rápido Tolima con destino El Ocho, por Letras. "
        "En el reglamento de diciembre de 2023 ese nombre es el parador La Esperanza, no "
        "la portería. Sigue hasta Brisas y confirma tarifa y horario en la terminal."
    )
    letras = (
        "La terminal de Manizales publica Empresa Arauca con destino Letras, por Maltería. "
        "Letras no es la entrada: es un punto de la vía hacia Bogotá. Sigue el corredor "
        "La Esperanza–Murillo hasta Brisas y confirma el horario en la terminal."
    )
    nevado = (
        "La terminal de Manizales publica Rápido Tolima con destino Nevado, por Letras. "
        "Esa ficha no dice que la parada sea el centro Brisas. No la uses como ingreso: "
        "pregunta a la empresa dónde deja y entra por la portería de tu sector."
    )
    invias = (
        "El parte de Invías cubre la red vial primaria, no la terciaria. Las vías desde "
        "Villamaría y Santa Rosa hasta Potosí y Santa Bárbara son terciarias destapadas, "
        "así que ese parte no dice si hoy se pasa. Confírmalo con el operador del sector."
    )
    neg_a = [
        "ruta manizales brisas",
        "cómo llego desde salento",
        "puedo ir en moto",
    ]
    neg_b = [
        "qué carretera agarro en Manizales hacia el parque",
        "vereda cocora hasta el límite",
        "confirmo la vía antes de salir",
    ]
    return [
        _entry(
            "access.bus_to_murillo",
            "bus de Manizales a Murillo",
            "procedure",
            [
                "hay bus de manizales a murillo",
                "rápido tolima llega a murillo",
                "desde la terminal, qué bus va a murillo",
                "el bus a murillo me deja en brisas",
                "como llego en bus hasta murillo tolima",
                "sale rápido tolima para murillo por letras",
                "is there a bus from Manizales to Murillo",
                "does the Murillo bus stop at the park gate",
                "quiero ir a murillo en bus y seguir al parque",
                "la terminal tiene ruta a murillo",
                "bus intermunicipal manizales murillo",
                "me bajo en murillo y de ahí cómo sigo al centro brisas",
            ],
            neg_a,
            murillo,
            "Toma el Rápido Tolima a Murillo por Letras y, ya en el pueblo, sigue el corredor hasta Brisas. Confirma tarifa y horario en la terminal antes de salir.",
            ["access.from_murillo", "access.no_public_bus", "access.esperanza_murillo_corridor"],
            [_terminal(19), PNN],
            {"origin": ["manizales", "murillo"], "sector": ["norte"]},
            ["bus", "murillo", "terminal"],
            "El buscador no dice que ese servicio pare en el centro de visitantes Brisas.",
        ),
        _entry(
            "access.bus_to_el_ocho",
            "bus hasta El Ocho",
            "procedure",
            [
                "hay bus hasta el ocho",
                "rápido tolima para el ocho",
                "el bus a el ocho es la portería",
                "me deja el bus en el parador el ocho",
                "desde manizales hay servicio a el ocho",
                "el ocho sale en la terminal de manizales",
                "is there a bus to El Ocho",
                "does the El Ocho bus enter the park",
                "bajo en el ocho y sigo a brisas",
                "la ruta del ocho es de rápido tolima",
                "el bus dice el ocho, es la entrada",
                "paso por el ocho en transporte público",
            ],
            neg_b,
            ocho,
            "El Ocho del buscador es el parador del reglamento de 2023, no Brisas. Sigue el corredor y confirma el horario en la terminal.",
            ["access.esperanza_murillo_corridor", "access.letras_not_the_gate", "access.brisas_visitor_center"],
            [_terminal(20), ANEXO],
            {"origin": ["manizales"], "sector": ["norte"]},
            ["bus", "el ocho", "terminal"],
        ),
        _entry(
            "access.bus_to_letras",
            "bus de la terminal hasta Letras",
            "procedure",
            [
                "empresa arauca va a letras",
                "hay bus de la terminal hasta letras",
                "arauca por maltería llega al parque",
                "el destino letras es la portería",
                "desde manizales, bus a letras",
                "me sirve el arauca para entrar a brisas",
                "is there a bus to Letras from Manizales",
                "does Empresa Arauca stop at the gate",
                "la ruta maltería letras sigue al nevado",
                "bus arauca destino letras",
                "llego a letras en bus y después qué vía tomo",
                "la terminal publica letras como destino",
            ],
            neg_a,
            letras,
            "Arauca te deja en Letras, por Maltería. Desde ahí tomas el corredor hacia Brisas y confirmas el horario en la terminal.",
            ["access.letras_highway", "access.letras_not_the_gate", "access.from_manizales"],
            [_terminal(23), PNN],
            {"origin": ["manizales"], "sector": ["norte"]},
            ["bus", "letras", "terminal"],
        ),
        _entry(
            "access.bus_labeled_nevado",
            "bus con destino Nevado",
            "fact",
            [
                "el bus que dice nevado entra al parque",
                "rápido tolima destino nevado es brisas",
                "hay un bus llamado nevado en la terminal",
                "destino nevado me deja en el centro de visitantes",
                "el rapido tolima a nevado por letras",
                "ese nevado del buscador es la portería",
                "is the bus labeled Nevado the park entrance",
                "does the Nevado bus go to Brisas",
                "vi un destino nevado en la terminal de manizales",
                "no sé si el bus nevado es el parque",
                "rápido tolima nevado por la vía letras",
                "el letrero nevado no dice brisas",
            ],
            neg_b,
            nevado,
            "El destino Nevado de Rápido Tolima no está identificado como Brisas. Pregunta dónde para y usa la portería de tu sector.",
            ["access.brisas_visitor_center", "access.no_public_bus", "access.letras_not_the_gate"],
            [_terminal(22), PNN],
            {"origin": ["manizales"], "sector": ["norte"]},
            ["bus", "nevado", "terminal"],
            "La ficha del buscador dice destino Nevado y vía Letras. No nombra el centro de visitantes.",
        ),
        _entry(
            "access.invias_not_tertiary",
            "parte de Invías y vías terciarias",
            "explanation",
            [
                "el parte de invias incluye la destapada a potosí",
                "miro invías para saber si paso a santa bárbara",
                "la red primaria avisa de la vía terciaria del cisne",
                "invias reporta las carreteras destapadas del parque",
                "antes de potosí consulto el estado de la red de invias",
                "la vía terciaria sale en el parte nacional",
                "does Invias list the dirt road to Potosi",
                "is the tertiary road in the Invias status report",
                "el parte de invías me dice si la destapada está abierta",
                "sirve el boletín de la red primaria para el cisne",
                "invias no cubre la terciaria a potosí",
                "confirmo la destapada con invias o con el operador",
            ],
            [
                "el acceso puede cambiar",
                "puedo ir en moto",
                "cómo llego desde salento",
            ],
            invias,
            "No uses el parte de la red primaria para la destapada a Potosí. Confirma ese tramo con el operador del sector.",
            ["access.dirt_roads_cisne", "access.mountain_road_conditions", "access.confirm_road_before"],
            [INVIAS, PNN],
            {"sector": ["cisne"]},
            ["invias", "destapada", "potosi"],
        ),
    ]


def apply(section: dict) -> dict:
    by_id = {entry["id"]: entry for entry in section["entries"]}

    _set_short(
        by_id["access.always_by_land"],
        "Al parque se llega siempre por transporte terrestre, y cada sector tiene su propia entrada. Llega a la puerta que elegiste y sigue esa carretera o ese camino.",
        "El cómo llegar oficial es por tierra, con una entrada distinta en cada sector. Elige la puerta y sigue esa vía.",
    )
    _set_short(
        by_id["access.no_motorcycles"],
        "No se permite el ingreso de motos al atractivo de Brisas, y las tablas de vehículos lo marcan prohibido. Confirma con UTON las restricciones de circulación de noviembre de 2026.",
        "La moto no entra al atractivo de Brisas. Confirma con UTON las restricciones de circulación de noviembre de 2026.",
    )
    _set_short(
        by_id["access.dirt_roads_cisne"],
        "Las tres vías al Cisne son carreteras terciarias destapadas que llegan a Potosí y a Santa Bárbara. La página no nombra un tipo de carro: planéalas con un prestador autorizado de ese sector.",
        "Hasta Potosí y Santa Bárbara se va por destapada. La página no nombra un tipo de carro: cuadra el viaje con un prestador de ese sector.",
    )
    _set_short(
        by_id["access.parking_at_brisas"],
        "La página no publica parqueadero, cupos ni plano en Brisas. Puedes llegar en tu vehículo y el valle se recorre en vehículo cubierto. Pregunta a UTON dónde dejar el carro. Si es fin de semana o puente de noviembre, revisa el pico y placa del Tolima (Resolución 1815 del 24 de julio de 2026, de 5:00 a. m. a 4:00 p. m.).",
        "No hay parqueadero, cupos ni plano publicados. Llegas en tu vehículo y el valle sigue en vehículo cubierto; pregunta a UTON dónde dejarlo.",
    )
    _set_short(
        by_id["access.quindio_gate_is_cocora"],
        "En el Quindío el acceso publicado es Salento, por la vereda Cocora, con 14 km hasta el límite del parque. Armenia es la aproximación a ese valle, no una segunda portería. Confirma el registro con el operador de ese sector.",
        "Si estás en el Quindío, el camino publicado va a Cocora, con 14 km hasta el límite. Confirma el registro con el operador de ese sector.",
    )
    _set_short(
        by_id["access.from_ibague_juntas"],
        "Desde Ibagué vas por la vereda Juntas, con 15 km asociados a ese camino. La página actual no los da como límite del parque ni describe el tramo siguiente. Confirma ese tramo con el operador del sector.",
        "Juntas es el camino sur que sale de Ibagué. Usa los 15 km como cifra de esa vereda, no como el límite, y confirma el resto con el operador.",
    )
    _set_short(
        by_id["access.three_south_paths"],
        "Quindío–Dulima tiene tres caminos: Cocora, con 14 km hasta el límite; Juntas, con 15 km asociados; y Palomar, con 11 km asociados. Solo Cocora se indica como llegada al límite. Confirma con el operador cómo sigue cada camino.",
        "Cocora, Juntas y Palomar salen de municipios distintos. El límite se indica en los 14 km de Cocora, no en los 15 km de Juntas ni en los 11 km de Palomar.",
    )
    _set_short(
        by_id["access.esperanza_murillo_corridor"],
        "Ese corredor La Esperanza–Murillo lleva a Brisas, vengas de Manizales o de Murillo. En el reglamento de diciembre de 2023, La Esperanza o El Ocho es un parador, no la portería.",
        "No te registres en el parador: el reglamento de diciembre de 2023 llama La Esperanza o El Ocho al desvío, y la entrada es Brisas.",
    )
    _set_short(
        by_id["access.brisas_entry_altitude"],
        "Según la página oficial de visita, el centro de inducción Brisas está a unos 4100 m. Es la altura de la entrada, no la de la cima ni la del final del carreteable.",
        "Cuando te registras en Brisas estás cerca de 4100 m. Esa cota es de la portería, no de la cumbre.",
    )
    _replace_answer(
        by_id["access.brisas_entry_altitude"],
        "El Servicio Geológico también indica 4.100 m para Brisas",
        "El Servicio Geológico también indica 4100 m para Brisas",
    )
    _replace_answer(by_id["access.tumbas_end_altitude"], "4.450 m", "4450 m")
    _replace_answer(by_id["access.tumbas_end_altitude"], "4.400 m", "4,400 m")
    _set_short(
        by_id["access.potosi_control"],
        "La cabaña Potosí es control del Cisne y también punto de salida hacia la Laguna del Otún. Se llega por las destapadas desde Villamaría o Santa Rosa de Cabal, a unos 3920 m según la página oficial. Es la cabaña, no una cima.",
        "Potosí queda a unos 3920 m y se alcanza por carretera terciaria desde Villamaría o Santa Rosa. Sirve de control del Cisne y de salida hacia el Otún.",
    )
    _set_short(
        by_id["access.la_punta_control"],
        "La Punta, en la vereda La Cascada de Anzoátegui, aparece como control flotante a 3100 m en el reglamento de diciembre de 2023. Hoy no está confirmado como mostrador: pregunta al operador antes de usarlo como punto de registro.",
        "La Punta y los 3100 m son la referencia de diciembre de 2023, no una caseta garantizada ahora. Pregunta al operador si sigue vigente.",
    )
    _replace_answer(by_id["access.control_coordinates"], "3.100 m", "3100 m")

    known = set(by_id)
    for entry in _buses():
        if entry["id"] in known:
            raise ValueError(f"duplicate id {entry['id']}")
        _set_short(entry, entry["answer"]["short"], entry["answer"]["variants"][0])
        section["entries"].append(entry)
    return section
