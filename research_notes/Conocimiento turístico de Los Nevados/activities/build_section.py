#!/usr/bin/env python3
"""Build the activities knowledge section from verified visitor facts.

Sources were read on 2026-11-21. This generator only assembles hand-written
entries; it does not invent trail metrics.
"""

from __future__ import annotations

import json
from pathlib import Path

RETRIEVED = "2026-11-21"

SOURCES = {
    "ficha": {
        "label": "Parques Nacionales Naturales de Colombia, ficha PNN Los Nevados",
        "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
        "retrieved_at": RETRIEVED,
    },
    "res207": {
        "label": "Parques Nacionales Naturales, Resolución 207 del 4 de agosto de 2023",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf",
        "retrieved_at": RETRIEVED,
    },
    "letter": {
        "label": "PNN Los Nevados, radicado 20266200003411 del 11 de mayo de 2026",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf",
        "retrieved_at": RETRIEVED,
    },
    "news": {
        "label": "Parques Nacionales Naturales, noticia del Plan de Ordenamiento Ecoturístico, 6 de marzo de 2026",
        "url": "https://www.parquesnacionales.gov.co/sala-prensa/noticias/el-parque-nacional-natural-los-nevados-lanza-nuevo-plan-de-ordenamiento-ecoturistico-para-fortalecer-la-conservacion-en-la-alta-montana/",
        "retrieved_at": RETRIEVED,
    },
    "poe": {
        "label": "Parques Nacionales Naturales, versión corta del POE Los Nevados 2026",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
        "retrieved_at": RETRIEVED,
    },
}


def entry(
    eid: str,
    label: str,
    kind: str,
    examples: list[str],
    negatives: list[str],
    short: str,
    variants: list[str],
    related: list[str],
    tags: list[str],
    sources: list[str],
    sector: list[str] | None = None,
    detail: str | None = None,
    steps: list[list[str]] | None = None,
    reflection: str | None = None,
) -> dict:
    answer: dict = {"short": short, "variants": variants}
    if detail is not None:
        answer["detail"] = detail
    if steps is not None:
        answer["steps"] = steps
    if reflection is not None:
        answer["reflection"] = reflection
    item = {
        "id": eid,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "needs": [],
        "answer": answer,
        "sources": [SOURCES[key] for key in sources],
        "last_verified": RETRIEVED,
        "related": related,
        "tags": tags,
    }
    if sector:
        item["entities"] = {"sector": sector}
    return item


ENTRIES: list[dict] = []


def add(item: dict) -> None:
    ENTRIES.append(item)


# --- Visit choice and north / Ruiz ---

add(entry(
    "activities.what_to_visit",
    "qué puedes visitar en el parque",
    "explanation",
    [
        "qué puedo visitar",
        "qué hay para hacer en Los Nevados",
        "qué lugares puedo conocer",
        "qué recorrido me recomienda para empezar",
        "actividades en el parque nacional",
        "qué se hace en cada sector",
        "quiero un plan de visita sin cumbre",
        "que hay pa hacer en los nevados",
        "cual es el paseo mas facil",
        "entre Brisas y el Tolima qué elijo",
        "what can I do in Los Nevados",
        "which part of the park should a first-time visitor pick",
    ],
    [
        "cómo llego desde Manizales",
        "cuánto cuesta la entrada",
        "a qué hora abren Brisas",
    ],
    "Hay cuatro sectores de visita en la ficha: Brisas–Kumanday, Cisne–Poleka Kasue, Laguna del Otún y Quindío–Dulima. Elige Brisas si buscas una salida corta, en vehículo y con caminatas breves; los otros sectores son para varios días, más sendero o una cumbre técnica. Cada uno cambia de cupo y de condiciones, así que confirma el que elegiste antes de salir.",
    [
        "La ficha reparte la visita en cuatro sectores. Brisas sirve para una jornada corta; Santa Isabel, el Otún y el Tolima piden más camino o una cumbre. Confirma cupo y estado del sector antes de viajar.",
    ],
    ["activities.brisas_valle_tumbas", "activities.day_or_multiday", "activities.sector_tolima"],
    ["sectores", "visita", "primera vez"],
    ["ficha"],
    sector=["brisas", "santa_isabel", "otun", "tolima"],
    detail="Brisas–Kumanday se asocia al paisaje del Ruiz hasta el Valle de las Tumbas. Cisne–Poleka Kasue ofrece páramo, borde glaciar, cumbre del Santa Isabel y Laguna Verde. En el Otún está la laguna más grande del parque. Quindío–Dulima concentra el montañismo cerca del Tolima.",
    steps=[
        ["Mira primero cuánto tiempo tienes: un día apunta a Brisas; varios días abren Otún, Santa Isabel o Tolima."],
        ["Dentro de cada sector solo cuentan los senderos que el parque tenga habilitados para tu fecha."],
        ["El plan de marzo de 2026 anuncia ajustes de senderos, pero la ficha de visita sigue organizada en esos cuatro sectores."],
    ],
    reflection="Puedes armar un buen día con el paisaje que sí esté habilitado, aunque la cima se quede entre nubes.",
))

add(entry(
    "activities.brisas_valle_tumbas",
    "recorrido Brisas al Valle de las Tumbas",
    "explanation",
    [
        "qué es el Valle de las Tumbas",
        "cómo es el paseo de Brisas",
        "Valle del Silencio qué se recorre",
        "quiero ir al valle cerca del Ruiz",
        "el carreteable de Brisas qué muestra",
        "se ve el superpáramo en ese valle",
        "Brisas hasta las Tumbas es en carro",
        "que hay en el valle de las tumbas",
        "el valle del silencio es el mismo",
        "me llevan hasta el valle o me dejan en Brisas",
        "what is the drive from Brisas to Valle de las Tumbas",
        "is Valle del Silencio the same place as Valle de las Tumbas",
    ],
    [
        "dónde queda exactamente el valle en el mapa",
        "reserva para el sector norte del Ruiz",
        "puedo subir en moto a Brisas",
    ],
    "El paseo de Brisas sale del centro de inducción, a unos 4100 metros, y sigue en vehículo por Arenales hasta el Valle de las Tumbas, también llamado Valle del Silencio. Vas a ver superpáramo y el paisaje volcánico del Ruiz, no a entrar al cráter. Confirma qué tramo está habilitado el día de tu visita.",
    [
        "En Brisas el recorrido publicado va en vehículo desde el centro de inducción, cerca de 4100 metros, hasta el Valle de las Tumbas o Valle del Silencio. Es para mirar el superpáramo y el Ruiz desde ese tramo, no para hacer cumbre.",
    ],
    ["activities.ruiz_summit_closed", "activities.north_route_stops", "activities.cloudy_visit_landscape"],
    ["brisas", "valle de las tumbas", "valle del silencio"],
    ["ficha", "res207"],
    sector=["brisas"],
))

add(entry(
    "activities.north_route_stops",
    "paradas del recorrido norte",
    "fact",
    [
        "qué paradas tiene el carreteable del Ruiz",
        "pasamos por Aguacerales",
        "Arenales del norte queda antes de las Tumbas",
        "el orden del recorrido en Brisas",
        "dónde está Aguacerales en la ruta",
        "se baja en el valle o solo se mira",
        "nombres de las estaciones del norte",
        "aguacerales arenales y tumbas son seguidos",
        "hay varias paradas o es un solo punto",
        "el recorrido norte en que orden va",
        "what stops are on the northern scenic road",
        "does the Brisas route pass Aguacerales before the valley",
    ],
    [
        "cuántos kilómetros hay de Manizales a Brisas",
        "a qué hora es la última charla",
        "pico y placa para subir a Brisas",
    ],
    "La reglamentación de 2023 nombra un solo recorrido norte: centro de interpretación Brisas, Aguacerales, Arenales y Valle de las Tumbas. La ficha lo describe como un trayecto en vehículo hasta el valle. Esas fuentes no publican los tiempos entre paradas; el operador te dice el orden del día.",
    [
        "En el norte el sendero autorizado va de Brisas a Aguacerales, luego Arenales y termina en el Valle de las Tumbas. Se recorre en vehículo y el parque no publicó la duración de cada parada.",
    ],
    ["activities.brisas_valle_tumbas", "activities.arenales_two_places", "activities.short_walks_brisas"],
    ["aguacerales", "arenales", "paradas"],
    ["res207", "ficha"],
    sector=["brisas"],
))

add(entry(
    "activities.arenales_two_places",
    "dos sitios llamados Arenales",
    "explanation",
    [
        "Arenales del Ruiz y Arenales del Tolima",
        "cuál Arenales es el del valle",
        "me confundí con el campamento Arenales",
        "Arenales es una parada o un camping",
        "hay dos Arenales en el parque",
        "el Arenales de Brisas se puede dormir",
        "Arenales de la cumbre del Tolima",
        "arenales es lo mismo en todo el parque",
        "cuando dicen arenales de cual hablan",
        "no sé si Arenales queda en el norte",
        "which Arenales is on the way to the Ruiz valley",
        "is the Arenales camp the same as the Brisas stop",
    ],
    [
        "cómo llego en carro hasta Brisas",
        "puedo acampar esta noche sin reserva",
        "altura del Nevado del Ruiz",
    ],
    "Arenales, en el recorrido de Brisas, es una zona del camino hacia el Valle de las Tumbas. Otro Arenales queda en la ruta de cumbre del Tolima y allí la norma de 2023 hablaba de un campamento de travesía. No son el mismo punto: pregunta siempre en qué sector está el Arenales de tu plan.",
    [
        "Si vas por Brisas, Arenales es una parte del recorrido en vehículo hacia el valle. El Arenales del Tolima es otro lugar, asociado a la travesía de cumbre. Confirma el sector para no mezclarlos.",
    ],
    ["activities.north_route_stops", "activities.camping_tolima", "activities.camping_brisas_restricted"],
    ["arenales", "homónimo", "sector"],
    ["res207", "ficha"],
    sector=["brisas", "tolima"],
))

add(entry(
    "activities.ruiz_summit_closed",
    "cima y cráter del Ruiz",
    "fact",
    [
        "puedo subir al cráter",
        "se puede llegar a la cima del Ruiz",
        "puedo caminar por el glaciar del Ruiz",
        "puedo entrar al cráter Arenas",
        "cómo hago cumbre en el Nevado del Ruiz",
        "me dejan pisar la nieve del Ruiz",
        "quiero asomarme al cráter",
        "se puede subir a la nieve del ruiz",
        "hay forma de llegar al crater",
        "el glaciar del Ruiz está abierto a turistas",
        "can I hike to the Ruiz crater",
        "is the summit of Nevado del Ruiz open to visitors",
    ],
    [
        "qué alerta tiene hoy el Ruiz",
        "cuánto mide el Nevado del Ruiz",
        "qué pasó en Armero en 1985",
    ],
    "No está permitido ascender a la cima ni al cráter del Nevado del Ruiz. El paseo turístico del norte termina en el Valle de las Tumbas y no es una entrada al glaciar. El parque lo reiteró por escrito en mayo de 2026; igual confirma la restricción antes de viajar, porque depende de la reglamentación vigente.",
    [
        "La cima y el cráter del Ruiz no son un recorrido de visitante. Desde Brisas se llega al Valle de las Tumbas, sin pasar al glaciar. Esa prohibición la sostuvo el parque en mayo de 2026 y conviene reconfirmarla.",
    ],
    ["activities.brisas_valle_tumbas", "activities.snow_and_glacier_access", "activities.refugio_not_the_route"],
    ["cráter", "cumbre", "ruiz", "prohibido"],
    ["letter", "ficha", "res207"],
    sector=["brisas"],
    detail="La carta del jefe del área protegida, del 11 de mayo de 2026, dice que la Resolución 207 de 2023 incluye la prohibición de ascender a la cima y al cráter del Ruiz. En esa resolución el sendero norte autorizado llega hasta el Valle de las Tumbas.",
    steps=[
        ["Planea el norte como un recorrido hasta el Valle de las Tumbas, no como un intento de cumbre."],
        ["Si alguien te ofrece el cráter o la nieve del Ruiz, no es un recorrido publicado para el visitante."],
        ["La alerta del día se consulta en el Servicio Geológico Colombiano; esta ficha no trae el nivel vigente."],
    ],
))

add(entry(
    "activities.cloudy_visit_landscape",
    "visita cuando la cima está nublada",
    "explanation",
    [
        "si está nublado qué hago en el recorrido",
        "vale la pena ir si no se ve la cima",
        "qué miro en el valle cuando hay niebla",
        "el paseo sirve aunque el Ruiz no aparezca",
        "puedo disfrutar Brisas sin ver la cumbre",
        "nubes tapan el volcán y ya vamos en camino",
        "que se ve si el volcan esta escondido",
        "si amanece cerrado igual recorro el valle",
        "me da rabia si no se destapa el nevado",
        "el paisaje del valle alcanza sin cumbre",
        "is the valley worth it when the peak is hidden",
        "what do I actually see if the summit stays in cloud",
    ],
    [
        "estará despejado para ver el nevado",
        "qué clima va a hacer mañana en el parque",
        "va a llover el día de mi visita",
    ],
    "Si la cima del Ruiz amanece tapada, el recorrido autorizado sigue siendo el paisaje que tienes delante: superpáramo y el Valle de las Tumbas. La ficha no promete ver el volcán despejado. Pregunta al operador cómo está el tramo ese día; el pronóstico, cuando tengas señal, lo miras en la fuente meteorológica.",
    [
        "Una cima entre nubes no borra el paseo de Brisas: el valle y el superpáramo son el recorrido publicado. Nadie puede garantizarte el Ruiz despejado. El estado del día lo confirmas con el operador.",
    ],
    ["activities.brisas_valle_tumbas", "activities.superparamo_landscape", "activities.summit_views_cisne"],
    ["nubes", "paisaje", "sin cumbre"],
    ["ficha"],
    sector=["brisas"],
    reflection="Puedes disfrutar el tramo que sí está a tu alcance aunque no elijas cómo amanece la cima.",
))

add(entry(
    "activities.snow_and_glacier_access",
    "dónde el recorrido toca el hielo",
    "explanation",
    [
        "en qué sector sí hay nieve",
        "puedo pisar hielo en Santa Isabel",
        "el Ruiz tiene nieve para el turista",
        "dónde se acerca uno al glaciar",
        "la nieve es solo de mirar o se camina",
        "quiero ver hielo sin subir al Ruiz",
        "en el Tolima el glaciar es de la cumbre",
        "se camina sobre el hielo o se mira de lejos",
        "hay nieve en Brisas o solo piedras",
        "borde del glaciar cuenta como pisar nieve",
        "where can visitors actually approach ice",
        "does the Brisas tour reach the snow",
    ],
    [
        "por qué se están derritiendo los glaciares",
        "hay nieve todo el año según el Ideam",
        "qué es un glaciar",
    ],
    "En Brisas no entras al glaciar del Ruiz: el paseo llega al Valle de las Tumbas. El hielo de visita está en otros recorridos autorizados, como el borde glaciar del Santa Isabel y la cumbre del Tolima por el glaciar Schimmer, siempre con el guía que corresponda. No te prometo nieve a la vista: las nubes y el retroceso del hielo cambian lo que encuentras.",
    [
        "El norte del Ruiz no es un paseo sobre nieve. El borde del Santa Isabel y la ruta Schimmer del Tolima son los acercamientos al hielo que sí aparecen como recorridos regulados. Confirma que sigan abiertos y no cuentes con ver hielo sí o sí.",
    ],
    ["activities.ruiz_summit_closed", "activities.conejeras_glacier_edge", "activities.tolima_summit_schimmer"],
    ["nieve", "glaciar", "hielo"],
    ["ficha", "letter", "res207"],
    sector=["brisas", "santa_isabel", "tolima"],
))

add(entry(
    "activities.short_walks_brisas",
    "caminatas cortas en Brisas",
    "explanation",
    [
        "hay caminatas cortas en Brisas",
        "se puede bajar del carro a caminar",
        "Brisas es solo mirador o también se camina",
        "un paseo a pie de poca distancia",
        "no quiero una travesía, solo estirar las piernas",
        "caminar un rato en el sector norte",
        "el norte es para gente que no va a trekear",
        "hay sendero peatonal largo en Brisas",
        "se camina todo el valle o tramos cortos",
        "brincar del vehiculo y caminar un poco",
        "are there short walks around Brisas",
        "can I stretch my legs or is it only a vehicle tour",
    ],
    [
        "qué ropa llevo para caminar",
        "puedo ir en bicicleta por Brisas",
        "está permitido salir del carreteable",
    ],
    "La ficha recomienda Brisas justamente para una visita ocasional y caminatas cortas, y a la vez dice que el trayecto al valle sigue en vehículo. No publica la longitud de un sendero a pie separado. Camina solo donde te indiquen en el recorrido habilitado y no lo conviertas en una expedición por tu cuenta.",
    [
        "Brisas está pensado como salida corta, con tramos a pie breves y el valle en vehículo. No hay una distancia oficial de una caminata larga en ese sector. Sigue el tramo que te habiliten ese día.",
    ],
    ["activities.brisas_valle_tumbas", "activities.vehicle_or_on_foot", "activities.day_or_multiday"],
    ["caminata corta", "brisas", "a pie"],
    ["ficha"],
    sector=["brisas"],
))

add(entry(
    "activities.superparamo_landscape",
    "paisaje de superpáramo en Brisas",
    "explanation",
    [
        "cómo se ve el paisaje de Brisas",
        "eso parece la luna o Marte",
        "qué paisaje hay en el valle",
        "el superpáramo se recorre en el norte",
        "piedras y ceniza en el camino al valle",
        "es un paisaje pelado cerca del Ruiz",
        "quiero ver el paisaje lunar del parque",
        "como es el paramo alto en brisas",
        "hay frailejones todo el camino o ya es piedra",
        "el valle es verde o es roca",
        "what does the landscape on the Brisas road look like",
        "is the valley a rocky high-mountain landscape",
    ],
    [
        "qué es el superpáramo",
        "qué planta crece en el superpáramo",
        "por qué el páramo produce agua",
    ],
    "En el recorrido de Brisas la ficha describe paisajes de superpáramo, roca y formaciones que comparan con un paisaje de otro mundo, junto a huellas del pasado geológico. Es lo que vas a mirar desde el vehículo y las paradas habilitadas. Cómo funciona ese ecosistema es otro tema; aquí se trata de lo que encuentras en el paseo.",
    [
        "El paseo norte es, sobre todo, superpáramo y roca volcánica hasta el Valle de las Tumbas. La ficha lo cuenta como un paisaje extremo, no como un bosque. Lo recorres por el tramo autorizado.",
    ],
    ["activities.brisas_valle_tumbas", "activities.geology_watching", "activities.cloudy_visit_landscape"],
    ["superpáramo", "paisaje", "brisas"],
    ["ficha"],
    sector=["brisas"],
))

add(entry(
    "activities.geology_watching",
    "observación geológica en la visita",
    "explanation",
    [
        "puedo ver geología en el parque",
        "observar rocas y el volcán de lejos",
        "hay recorrido de observación geológica",
        "me interesa el paisaje volcánico",
        "se puede mirar el cráter sin subirlo",
        "actividad de geología para visitantes",
        "quiero entender las formas del valle",
        "se permiten fotos a las rocas",
        "puedo partir una piedra para verla",
        "geologia del ruiz desde el camino",
        "can I join a geology viewing visit",
        "is looking at the volcanic landscape an allowed activity",
    ],
    [
        "me puedo llevar una piedra de recuerdo",
        "cómo se llama el cráter principal",
        "el Ruiz es un estratovolcán",
    ],
    "La observación geológica es una actividad de la ficha en Brisas y también en Cisne, Otún y el sector del Tolima. Se hace desde el sendero o el carreteable habilitado, mirando el paisaje volcánico. No está permitido llevarte rocas ni picar el material: eso queda por fuera de la visita.",
    [
        "Puedes observar el paisaje geológico en los sectores donde la ficha ofrece esa actividad. Mira desde el recorrido autorizado y deja las rocas en su sitio.",
    ],
    ["activities.superparamo_landscape", "activities.azufrera_stop", "activities.photography_amateur"],
    ["geología", "rocas", "volcán"],
    ["ficha", "res207"],
))

add(entry(
    "activities.vehicle_or_on_foot",
    "ir en vehículo o caminando",
    "explanation",
    [
        "el valle se hace a pie o en carro",
        "Brisas es un tour en vehículo",
        "los otros sectores son caminando",
        "puedo caminar desde Brisas hasta el valle",
        "dónde toca ir a pie sí o sí",
        "el parque tiene paseo en carro y trekking",
        "solo el norte es motorizado",
        "en el Tolima no hay carretera escenica",
        "se recorre todo el parque en campero",
        "cual sector es caminado y cual en carro",
        "which visits are by vehicle and which are hikes",
        "do I have to walk to reach Valle de las Tumbas",
    ],
    [
        "puedo subir en moto al atractivo",
        "hay bus público hasta la laguna",
        "dónde dejo el carro parqueado",
    ],
    "Hasta el Valle de las Tumbas la ficha dice que el trayecto sigue en vehículo cubierto. En Cisne, Otún y Tolima la visita es de sendero, travesía o cumbre, y el parque no presta un transporte interno general. No uses el carreteable del norte como si fuera una caminata libre: muévete en el modo que corresponda a tu sector.",
    [
        "El valle del Ruiz se recorre en vehículo cubierto. Los otros sectores se caminan o se hacen en travesía, sin un bus del parque por dentro. Confirma el modo de tu recorrido con el operador.",
    ],
    ["activities.brisas_valle_tumbas", "activities.short_walks_brisas", "activities.day_or_multiday"],
    ["vehículo", "a pie", "carreteable"],
    ["ficha"],
    sector=["brisas", "santa_isabel", "otun", "tolima"],
))


def section_document() -> dict:
    return {
        "contract_version": 1,
        "id": "activities",
        "order": 8,
        "title": "Qué hacer y qué visitar",
        "description": "Recorridos, senderos, miradores, cumbres, camping, fotografía y otras actividades de visita en Los Nevados, según el sector.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.35,
            "top_k": 2,
            "min_score": None,
            "entity_filters": ["sector"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Buscas una salida corta por Brisas o una travesía de varios días?",
                "¿Quieres caminar, ver un mirador o intentar una cumbre autorizada?",
                "¿Te interesa el Ruiz, Santa Isabel, la Laguna del Otún o el Tolima?",
                "¿Preguntas por acampar, por fotografiar o por un sendero?",
                "¿Es una visita con niños o un ascenso de alta montaña?",
                "¿Quieres saber si esa actividad está permitida o cómo es el recorrido?",
            ],
            "slot_questions": {
                "sector": "¿En qué sector quieres hacer la actividad: Brisas, Santa Isabel, Laguna del Otún o Tolima?",
            },
            "fallback": "No tengo ese recorrido con ese nombre. Puedo contarte qué se visita en Brisas, Santa Isabel, la Laguna del Otún o el Tolima, y qué cumbres están autorizadas. Confirma siempre el sendero con Parques Nacionales antes de salir.",
        },
        "featured": [
            "activities.what_to_visit",
            "activities.brisas_valle_tumbas",
            "activities.ruiz_summit_closed",
            "activities.camping_where",
            "activities.sector_tolima",
        ],
        "entries": ENTRIES,
    }


def main() -> None:
    import entries_b
    import entries_c
    import entries_d

    entries_b.register(add, entry)
    entries_c.register(add, entry)
    entries_d.register(add, entry)
    out = Path("/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/activities.json")
    out.write_text(json.dumps(section_document(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"entries={len(ENTRIES)} -> {out}")


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: activities now builds from activities/source/activities.v1.json via coordination/build_from_snapshot.py activities; rerunning this script would revert reviewed corrections.")
    raise SystemExit(
        "Refusing to rebuild activities.json from the pre-correction entries. "
        "Run corrected_section.py."
    )
