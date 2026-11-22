#!/usr/bin/env python3
"""Audit the retrieval examples that the curation v2 proposals add, change or remove.

Run from the repository root:

    uv run --project experiments/laya python research_notes/curation_v2/tools/examples_audit.py

Inputs: snapshots/sections_before/<S>.json (baseline corpus, hash-pinned to the current corpus),
proposals/<S>.json (operations, applied here in memory in file order: update replaces in place,
add appends, delete removes; nothing is written to the corpus). Output: reviews/_examples.json.

Checks per section and across the whole after-corpus:
  - exact and accent-folded duplicates of an added example (any entry, any proposal);
  - e5 near-duplicates (route_check.embed, cosine): >= 0.95 to an example of the same entry,
    >= 0.92 to an example of another entry (exact/folded duplicates excluded);
  - template filler: word trigrams (with at least one non-stopword) shared by >= 3 and >= 25 % of
    one entry's added examples;
  - shares of added examples: <= 3 words, >= 15 words, English, no-accent and unknown-token
    candidates. The last two are heuristics against es_CO hunspell (affix-stripped lookup); they
    locate examples for a reader and are not verdicts;
  - removed examples with <= 2 words (the brief forbids removing short tourist queries for length).

Judgements that need a reader (natural phrasing, asks this entry's question, contrast) are the
MANUAL table below: each row was taken from the printed sample of that section, and the script
checks that every dropped example really is an added example of that section.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import route_check  # noqa: E402  (embed() shares the e5 cache and its lock)

W = TOOLS.parent
SNAP = W / "snapshots" / "sections_before"
PROPS = W / "proposals"
OUT = W / "reviews" / "_examples.json"
DEFAULT_DIC = Path("/usr/share/hunspell/es_CO.dic")

THRESH_SAME = 0.95
THRESH_OTHER = 0.92
SAMPLE_SIZE = 12
SHORT_MAX = 3
LONG_MIN = 15

STOP = {
    "de", "la", "el", "en", "y", "a", "que", "un", "una", "unos", "unas", "los", "las", "por",
    "para", "pa", "con", "del", "al", "se", "lo", "mi", "me", "te", "es", "no", "o", "si", "ya",
    "tu", "su", "sus", "mis", "hay", "yo", "ni", "son", "ser",
}
# Tokens that are English and not Spanish. Each one makes an example an English form.
ENGLISH = {
    "the", "i", "want", "to", "my", "is", "how", "can", "where", "what", "when", "do", "does",
    "for", "we", "need", "our", "are", "with", "you", "and", "it", "be", "this", "that", "of",
    "visit", "trail", "park", "tickets", "ticket", "register", "hike", "hours", "next", "weekend",
}
# Suffixes stripped before a hunspell lookup, so conjugated and plural forms are not "unknown".
SUFFIXES = ("mente", "ando", "iendo", "ados", "idos", "adas", "idas", "ado", "ido", "ada", "ida",
            "aron", "ieron", "aste", "ste", "amos", "emos", "imos", "mos", "ndo", "ar", "er",
            "ir", "es", "as", "os", "an", "en", "s", "n", "o", "a", "e")

# "X, no Y" or "no es / no la ..." clauses. In this corpus they name another entry's concept
# (exemptions, reservation rules, ages), so the example sits between two entries.
CONTRAST_RE = re.compile(
    r",\s*no\s|\bno (es|son) (la|el|las|los|una|un|de)\b|\bno la (tarifa|de|reserva)\b", re.I)
WHY_TAIL = ("Contraste 'X, no Y' que nombra el concepto de otra entrada: el vector queda entre "
            "las dos y el ejemplo no pregunta solo lo suyo. Si hace falta el contraste, va como "
            "hard_negative copiado de esa entrada.")
WHY_NEAR = "Casi copia (cos >= 0.95) de otro ejemplo de la misma entrada; no aporta discriminación."

# Judgement from reading every added example of each section (523 in total). Each drop must be
# an added example of its section: the script asserts it. Notes are Spanish prose.
MANUAL: dict[str, dict] = {
    "access": {
        "drop": [
            {"id": "access.from_murillo", "example": "cómo voy desde el pueblo de Murillo a la entrada del parque", "why": WHY_NEAR + " Cos 0.9678 con 'cómo salir de Murillo hacia el parque'."},
            {"id": "access.brisas_visitor_center", "example": "ubicación de la portería norte de Brisas", "why": WHY_NEAR + " Cos 0.9596 con 'brisas es la portería del norte'."},
            {"id": "access.brisas_visitor_center", "example": "Brisas visitor center entrance location", "why": WHY_NEAR + " Cos 0.953 con 'where is the Brisas visitor center'."},
            {"id": "access.own_car_brisas", "example": "can I drive my own private car to Brisas", "why": WHY_NEAR + " Cos 0.9888 con 'can I drive my own car to Brisas'."},
            {"id": "access.el_cisne_approach", "example": "por dónde se llega al centro de visitantes El Cisne", "why": WHY_NEAR + " Cos 0.9729 con 'centro de visitantes el cisne por donde'."},
            {"id": "access.el_cisne_approach", "example": "road route to El Cisne visitor center", "why": WHY_NEAR + " Cos 0.9516 con 'which road leads to the Cisne visitor center'."},
            {"id": "access.from_pereira_cedral", "example": "how to get from Pereira to El Cedral trailhead", "why": WHY_NEAR + " Cos 0.9694 con 'how do I get from Pereira to El Cedral'."},
            {"id": "access.from_anzoategui_palomar", "example": "how to access through Anzoátegui and Palomar", "why": WHY_NEAR + " Cos 0.9613 con 'how do I get from Anzoátegui to Palomar'."},
            {"id": "access.three_south_paths", "example": "cuáles son las tres rutas a pie para el Nevado del Tolima", "why": WHY_NEAR + " Cos 0.9656 con 'tres caminos al nevado del tolima'."},
            {"id": "access.bus_to_letras", "example": "intercity bus from Manizales terminal to Letras", "why": WHY_NEAR + " Cos 0.9519 con 'is there a bus to Letras from Manizales'."},
        ],
        "notes": ("124 añadidos en 31 entradas; exactamente 1 en inglés por entrada (dentro de la guía de 1–2). "
                  "Ninguna forma de 3 palabras o menos. Preguntas de acceso naturales y específicas. "
                  "'por cuáles cuatro departamentos se entra a Los Nevados' queda a 0.9675 de geography.departments "
                  "('cuales son los 4 departamentos de Los Nevados'); se conserva porque pregunta por la entrada, "
                  "pero conviene que su hard_negatives lleve esa pregunta de geografía."),
    },
    "booking_fees": {
        "drop": [
            {"id": "booking_fees.under25_admission_fee", "example": "tengo 22 y soy colombiano, cuanto es la entrada, no la de extranjero", "why": WHY_TAIL},
            {"id": "booking_fees.adult_resident_admission_fee", "example": "mayor de 25 residente, no es la tarifa del menor", "why": WHY_TAIL},
            {"id": "booking_fees.foreign_nonresident_admission_fee", "example": "extranjero no residente, no la tarifa de la CAN", "why": WHY_TAIL},
            {"id": "booking_fees.student_admission_category", "example": "solo el programa ambiental del parque exime al colegio, no un descuento", "why": WHY_TAIL},
            {"id": "booking_fees.entry_fee_discounts", "example": "el descuento del convenio no es la promocion de entrada gratis", "why": WHY_TAIL},
            {"id": "booking_fees.entry_fee_discounts", "example": "rebaja por convenio de mi empresa, eso no es quedar exento", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_promotion_programs", "example": "el pasaporte de parques es promocion, no una exencion personal", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_promotion_programs", "example": "entrada gratis por programa no es el descuento de un convenio", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_company_staff_inside_park", "example": "exencion por trabajar en una empresa de adentro, no por ser funcionario", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_government_staff", "example": "contratista de pnn no es empleado de una empresa de adentro", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_official_mission", "example": "mision oficial del ejercito no es un proyecto de investigacion", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_researchers", "example": "exencion de investigador con proyecto, no de una mision oficial", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_researchers", "example": "el permiso de investigacion me exime aunque no sea militar", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_nearby_residents", "example": "exencion por vivir en un pueblo pequeno, no por tener finca adentro", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_property_owners", "example": "exencion del dueno del predio, no del vecino del pueblo", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_indigenous_communities", "example": "exencion de comunidad indigena por usos tradicionales, no por ser vecino", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_disability_visitors", "example": "exencion por discapacidad, no por ser mayor de 62", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_disability_visitors", "example": "la discapacidad no es la tarifa de estudiante", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_young_children_and_seniors", "example": "exencion de mayores de 62 residentes, distinta de la de discapacidad", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_journalists", "example": "exencion del periodista acreditado, no de un funcionario", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_donors", "example": "exencion del representante de un donante, no de un investigador", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_park_volunteers", "example": "exencion de guardaparque voluntario, no de funcionario de planta", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_police_family", "example": "exencion de la familia del uniformado fallecido, no del militar en mision", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_police_family", "example": "hijo de un policia muerto en servicio, eso no es una mision oficial", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_culture_agents", "example": "exencion de soy cultura solo en temporada baja, no la de investigador", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_culture_agents", "example": "agente cultural registrado no es un periodista acreditado", "why": WHY_TAIL},
            {"id": "booking_fees.exempt_tourist_guides_and_providers", "example": "la exencion es del guia acreditado, el turista si paga su entrada", "why": "Declarativa que describe la exención de otra persona (el guía); la pregunta del visitante ya está en 'prestador del repse no paga, yo como visitante si'."},
            {"id": "booking_fees.exemption_not_guaranteed", "example": "la exencion no es un cupo: pueden negar el ingreso", "why": "Declarativa, no una pregunta de visitante; el riesgo de negación queda en la respuesta, no en el ejemplo."},
            {"id": "booking_fees.exemption_no_insurance_waiver", "example": "la exencion de pago y el seguro son cosas distintas", "why": "Declarativa que repite 'estar exento de la tarifa no borra el seguro obligatorio' (mismo concepto)."},
            {"id": "booking_fees.exemption_proof_deadline", "example": "el plazo de ocho dias no es la regla de vecinos ni de periodistas", "why": WHY_TAIL},
            {"id": "booking_fees.brisas_reservation", "example": "la regla de brisas es el dia, no la pagina web", "why": WHY_TAIL},
            {"id": "booking_fees.brisas_booking_channel", "example": "cual es la pagina para reservar brisas, no si es obligatoria", "why": WHY_TAIL},
            {"id": "booking_fees.brisas_booking_channel", "example": "reservasnevados es el canal, no la regla del fin de semana", "why": WHY_TAIL},
            {"id": "booking_fees.other_sector_reservation", "example": "fuera de brisas la reserva la pide el operador, no yo en la web", "why": WHY_TAIL},
            {"id": "booking_fees.center_otun_reservation_lead", "example": "cisne y otun piden tres dias habiles, no cinco", "why": WHY_TAIL},
            {"id": "booking_fees.quindio_reservation_lead", "example": "quindio dulima pide cinco dias habiles, no tres", "why": WHY_TAIL},
            {"id": "booking_fees.quindio_reservation_lead", "example": "el plazo del tolima no es el mismo de cisne", "why": WHY_TAIL},
            {"id": "booking_fees.age_minimum_by_attraction", "example": "la edad minima es 6 en brisas y 15 en travesia, no es la edad maxima", "why": WHY_TAIL},
            {"id": "booking_fees.maximum_entry_age", "example": "la edad maxima es 69 en la ficha y 70 en la resolucion, no es la minima", "why": WHY_TAIL},
            {"id": "booking_fees.maximum_entry_age", "example": "alguien cerca de 70 tiene que confirmar, no es la regla de los 6 años", "why": WHY_TAIL},
            {"id": "booking_fees.guide_required", "example": "es obligatorio ir con guia, eso no es el seguro de accidentes", "why": WHY_TAIL},
            {"id": "booking_fees.documents_to_carry", "example": "que documento de identidad llevo, no el formato de ingreso", "why": WHY_TAIL},
            {"id": "booking_fees.documents_to_carry", "example": "cedula o pasaporte para el control, distinto del formulario", "why": WHY_TAIL},
            {"id": "booking_fees.registration_form_required", "example": "el formato de ingreso es un papel distinto de la cedula", "why": WHY_TAIL},
            {"id": "booking_fees.reservation_data_required", "example": "que nombres y cedulas piden para armar la reserva, no si ya pague", "why": WHY_TAIL},
            {"id": "booking_fees.platform_pays_services", "example": "en la plataforma se registran y se pagan los servicios, no cuales tarjetas hay", "why": WHY_TAIL},
            {"id": "booking_fees.platform_pays_services", "example": "pagar la reserva no es la lista de pse o visa", "why": WHY_TAIL},
            {"id": "booking_fees.vehicle_not_parking_fee", "example": "el cobro del carro es derecho de ingreso, no parqueadero", "why": WHY_TAIL},
            {"id": "booking_fees.sector_entry_fee_difference", "example": "quindio dulima sale en cero en la ficha y la resolucion no lo separa", "why": "Meta-texto sobre el documento ('en la ficha', 'la resolución'); no es la pregunta de un visitante."},
            {"id": "booking_fees.brisas_guide_price", "example": "la ficha dice 22000 de guianza pero no si es por persona", "why": "Meta-texto sobre la ficha; la versión de visitante ('la guía de 22000 es por persona?') sí valdría."},
        ],
        "notes": ("88 añadidos. 40 usan el patrón 'X, no Y' o 'no es la …' que nombra el concepto de la "
                  "entrada hermana (exenciones, reservas, edades, pagos). Ese patrón acerca cada ejemplo a "
                  "la entrada vecina (near_other_entry_ge_0.92 = 32 en la sección). Se retiran 50 (40 de ese "
                  "patrón más 10 declarativas o meta-texto). El contraste entre exenciones va en hard_negatives "
                  "copiados de la entrada hermana. Quedan 38 ejemplos. Los de exención se parecen entre sí "
                  "por construcción: esa es la fuente de la confusión, no un problema de redacción."),
    },
    "geography": {
        "drop": [
            {"id": "geography.main_peaks", "example": "como se llaman las tres cumbres nevadas principales", "why": WHY_NEAR + " Cos 0.9808 con 'cuáles son las tres cumbres nevadas'."},
            {"id": "geography.ruiz_identity", "example": "el Ruiz es un estratovolcan activo con glaciar", "why": WHY_NEAR + " Declarativa; cos 0.9616 con 'el Ruiz es un estratovolcán'."},
            {"id": "geography.arenas_crater", "example": "dimensiones y profundidad del crater Arenas", "why": WHY_NEAR + " Cos 0.9648 con 'profundidad del cráter Arenas'."},
            {"id": "geography.municipalities", "example": "lista de municipios que conforman el parque nacional", "why": WHY_NEAR + " Cos 0.9792 con 'municipios del parque nacional'."},
            {"id": "geography.four_sectors", "example": "cuales son los cuatro sectores para visitar en el parque", "why": WHY_NEAR + " Cos 0.9505 con 'cuáles son los sectores del parque'."},
            {"id": "geography.laguna_otun", "example": "donde se localiza la Laguna del Otun exactamente", "why": WHY_NEAR + " Cos 0.9539 con 'laguana del otun donde queda'."},
            {"id": "geography.paramillo_quindio", "example": "a cuantos metros esta el Paramillo del Quindio", "why": WHY_NEAR + " Tercera variante de la misma pregunta de altura (cos 0.9681 con 'donde queda y que altura tiene')."},
            {"id": "geography.paramillo_quindio", "example": "altura oficial y ubicacion del Paramillo del Quindio", "why": WHY_NEAR + " Cos 0.9626 con 'donde queda y que altura tiene'."},
            {"id": "geography.paramillo_cisne", "example": "a que altura esta el Paramillo del Cisne", "why": WHY_NEAR + " Cos 0.9876 con '¿Qué altura tiene el Paramillo del Cisne?'."},
            {"id": "geography.paramillo_cisne", "example": "altitud oficial del complejo Paramillo del Cisne", "why": WHY_NEAR + " Cos 0.9591 con 'a que altura esta el Paramillo del Cisne'."},
            {"id": "geography.highest_in_park", "example": "cual es el punto mas alto de todo el parque Los Nevados", "why": WHY_NEAR + " Cos 0.9679 con 'el punto más alto de Los Nevados'."},
            {"id": "geography.volcanic_centers", "example": "el complejo volcanico del Ruiz que volcanes incluye", "why": WHY_NEAR + " Cos 0.9568 con 'qué volcanes activos hay en el complejo del Ruiz'; sintaxis rota."},
            {"id": "geography.olleta_pirana", "example": "conos volcanicos adventicios de La Olleta y La Piraña", "why": "Jerga de cartografía, no pregunta de visitante; repite el nombre de la otra pareja de ejemplos."},
            {"id": "geography.valle_tumbas", "example": "el Valle del Silencio y Valle de las Tumbas en el norte", "why": "Fragmento sin pregunta; repite el mismo nombre en 3 de 3 ejemplos (plantilla 'Nombre del Y')."},
            {"id": "geography.rio_otun", "example": "el rio Otun nace en la Laguna del Otun verdad", "why": "Cos 0.9568 con el ejemplo de flora_ecosystems 'el rio otun nace en la laguna del otun' (otra sección, misma pregunta)."},
            {"id": "geography.geoheritage", "example": "el Nevado del Ruiz como uno de los 100 sitios de patrimonio geologico", "why": "Declarativa de dato, no pregunta de visitante."},
            {"id": "geography.tolima_volcano", "example": "el Nevado del Tolima es un cono volcanico simetrico", "why": "Declarativa de dato, no pregunta de visitante."},
        ],
        "notes": ("108 añadidos. Plantilla por nombre propio: 13 frases de 3 de 3 ejemplos en 7 entradas "
                  "(valle_tumbas, laguna_otun, laguna_otun_formation, paramillo_quindio, paramillo_santa_rosa, "
                  "olleta_pirana, rio_otun). Se retiran 17: casi copias (paramillos, Otún, municipios, cumbres), "
                  "declarativas y dos fragmentos. Lo que queda son lecturas de búsqueda ('paisaje lunar del "
                  "Valle de las Tumbas en Brisas'), no preguntas completas. Ningún ejemplo nuevo en inglés. "
                  "Se mantiene 'la Laguna del Otún en qué municipio y departamento queda'; revisar "
                  "'ruiz_versus_huila': dos formas de la misma comparación, se conserva la pregunta."),
    },
    "services": {
        "drop": [
            {"id": "services.north_food", "example": "venden desayuno o almuerzo para visitantes en Arenales", "why": WHY_NEAR + " Cos 0.9528 con 'venden comida en Arenales'."},
            {"id": "services.toilets", "example": "dónde hay baños para visitantes en el parque", "why": WHY_NEAR + " Cos 0.9653 con 'hay baños en el parque'."},
            {"id": "services.first_aid_points", "example": "dónde hay puntos de primeros auxilios y atención médica en el parque", "why": WHY_NEAR + " Cos 0.9685 con 'hay puesto de primeros auxilios en el parque'."},
            {"id": "services.potosi_cabin", "example": "el refugio Potosí en Campo Alegre ofrece hospedaje y comida?", "why": WHY_NEAR + " Cos 0.9513 con 'dónde queda el refugio Campo Alegre cerca a Potosí para hospedarse' (también añadido)."},
            {"id": "services.brisas_lodging", "example": "hay habitaciones disponibles para turistas en el sector Brisas", "why": WHY_NEAR + " Cos 0.9508 con 'hay alojamiento en Brisas'."},
            {"id": "services.brisas_lodging", "example": "se puede reservar noche de hospedaje en la cabaña de Brisas", "why": WHY_NEAR + " Cos 0.954 con 'se puede dormir en la cabaña de Brisas'."},
            {"id": "services.refugio_cabin", "example": "cuál es el estado actual de la cabaña El Refugio", "why": WHY_NEAR + " Cos 0.9607 con 'estado de la cabaña El Refugio'."},
            {"id": "services.camp_showers", "example": "las duchas de la cabaña de Arenales están en servicio", "why": WHY_NEAR + " Cos 0.9709 con 'hay duchas para bañarse en la cabaña de Arenales'; además afirma un estado actual."},
            {"id": "services.camp_showers", "example": "instalaciones sanitarias y duchas para campistas en Arenales", "why": WHY_NEAR + " Cos 0.9668 con 'hay duchas para campistas en Arenales'."},
            {"id": "services.lost_items", "example": "perdí un objeto personal o morral en el parque", "why": WHY_NEAR + " Cos 0.9544 con 'perdi un objeto en el parque'."},
            {"id": "services.guide_radios", "example": "es obligatorio que los guías y operadores registrados tengan radio", "why": "Cos 0.9282 con health_safety.guide_first_aid_kit_and_certification (otra sección, misma pregunta sobre radio de guías) y paráfrasis de otro ejemplo de la misma entrada."},
        ],
        "notes": ("108 añadidos, con formas naturales y específicas. 11 retiradas por casi copia. "
                  "Ninguna forma de 3 palabras o menos: falta la forma corta que escribe el turista ('baños', "
                  "'señal'), que el brief pide. services.guide_radios tiene 5 variantes de la misma pregunta de "
                  "radio. El proposal también quita 'el guía lleva botiquín?' (pregunta de "
                  "health_safety.guide_first_aid_kit_and_certification: retirarla está bien) y 'cómo confirmo antes de "
                  "viajar' (general; su sustituto es parecido, conviene confirmarlo)."),
    },
    "health_safety": {
        "drop": [
            {"id": "health_safety.altitude_sickness_symptoms", "example": "me duele la cabeza y tengo nauseas pero camino coordinado", "why": WHY_NEAR + " Cos 0.9547 con 'me duele la cabeza y tengo náuseas arriba'."},
            {"id": "health_safety.altitude_temperature_drop_rate", "example": "esa baja de grados por cada 100 metros es el clima de hoy", "why": "Pregunta por el clima de hoy, que es de weather_volcano y no puede responderse con datos fechados; no pregunta la tasa de enfriamiento."},
            {"id": "health_safety.wind_and_wetness_heat_loss", "example": "el viento de hoy esta a cuantos grados, o solo multiplica el frio", "why": "Pregunta el viento de hoy (clima actual, fuera de esta entrada y sin dato fechado)."},
        ],
        "notes": ("62 añadidos, en su mayoría naturales y específicos (síntomas, primeros auxilios, 123/119/144). "
                  "Sin formas en inglés ni de 3 palabras o menos. Retiradas 3 (una casi copia y dos preguntas de "
                  "clima actual). Las entradas de congelación y de hipotermia se distinguen por síntoma y "
                  "acción, no por la misma frase; varias preguntas comparten 'lo dejo quieto'."),
    },
    "weather_volcano": {
        "drop": [
            {"id": "weather_volcano.alert_yellow_meaning", "example": "q significa la alerta amarilla", "why": WHY_NEAR + " Cos 0.9927 con 'qué significa alerta amarilla' (solo cambia la tilde y una letra)."},
            {"id": "weather_volcano.ovsm_role", "example": "el Observatorio de Manizales publica informes", "why": "Declarativa, no pregunta de visitante. Movida desde current_alert; si se quiere conservar, reformularla como pregunta."},
            {"id": "weather_volcano.summit_visibility", "example": "con la cima tapada me salgo del sendero para la foto?", "why": "La pregunta es si puedo salirme del sendero (rules.stay_on_routes, cos 0.9458); la de visibilidad de la cumbre queda en el resto del ejemplo."},
        ],
        "notes": ("7 añadidos. Movimiento: 3 ejemplos pasaron de current_alert a ovsm_role; route_check marca "
                  "not_routing 3 para current_alert. Es un traslado, no una pérdida, pero debe constar en el "
                  "decision log. 'alerta amarilla' pierde su variante casi idéntica. Sin formas en inglés."),
    },
    "fauna": {
        "drop": [
            {"id": "fauna.spotting_sector_santa_isabel", "example": "animales en la ruta al glaciar Santa Isabel", "why": WHY_NEAR + " Cos 0.9507 con 'que fauna hay camino al glaciar santa isabel'."},
        ],
        "notes": ("7 añadidos. 'birds_overview' tiene 4 formas de la misma pregunta de aves (variantes aceptables, "
                  "no casi copias). Sin formas en inglés ni de 3 palabras o menos."),
    },
    "hours_status": {
        "drop": [
            {"id": "hours_status.volcanic_alert_closures", "example": "alerta amarilla significa que hoy dejan entrar al parque", "why": "Premisa sobre el estado de hoy (cierre o entrada) que la app no puede confirmar; la pregunta válida ya está en 'si pasan el ruiz a naranja cierran el ingreso'."},
            {"id": "hours_status.volcanic_alert_closures", "example": "la alerta del ruiz no es el cierre de la cumbre nevada", "why": "Declarativa, no pregunta de visitante."},
        ],
        "notes": ("4 añadidos; 2 retiradas. Se retiraron además 3 ejemplos del propio proposal "
                  "('cierre por actividad volcánica', 'cierran brisas si el volcán emite gases', 'is the park closed "
                  "due to volcanic activity'): route_check da not_routing 0 para ellos, pero son núcleo de la "
                  "entrada y conviene recuperar al menos la primera. Las dos preguntas de cierre siguen siendo "
                  "de estado actual: la respuesta debe declarar la fecha de la información."),
    },
    "actions": {
        "drop": [
            {"id": "actions.register_planned_visit", "example": "quiero registrar el grupo para otro dia, no es una pregunta de horario", "why": WHY_TAIL + " Además es meta-texto dirigido al asistente."},
            {"id": "actions.register_arrival_today", "example": "ya estoy en la porteria, abre el registro de hoy y no la reserva de otro dia", "why": WHY_TAIL + " Ademas es una orden, no una pregunta de visitante."},
            {"id": "actions.report_lost_person", "example": "falta una persona del grupo, abre el reporte, no se me perdio un objeto", "why": WHY_TAIL + " Además es una orden al asistente."},
            {"id": "actions.report_emergency_general", "example": "abre el reporte de emergencia y dime el 123, no me mandes ayuda", "why": "Orden al asistente con una negación sin sentido para el visitante; el resto del ejemplo ya cubre la emergencia."},
        ],
        "notes": ("12 añadidos, todos leídos. Se retiran 4 con meta-texto. Se retiraron además 6 ejemplos "
                  "coloquiales naturales sin que pregunten otra entrada ('se pegó una caída feísima', 'se cortó "
                  "feo con una piedra', 'tiene los labios morados y tirita sin parar', 'alguien tirita sin parar', "
                  "'veo llamas en la montaña', 'estoy sin señal y hay gente tirada en la montaña'). route_check da "
                  "not_routing 0, pero el proposal pierde la lengua de tourista. Recomiendo restaurarlos. "
                  "Varias entradas de reporte empiezan con 'quiero preparar el reporte de…'."),
    },
    "preparation": {
        "drop": [],
        "notes": ("2 añadidos, naturales y en español. Sin retiradas de ejemplos de forma corta."),
    },
    "rules": {
        "verdict": "issues",
        "drop": [],
        "notes": ("1 añadido ('está permitida la cacería de animales en el parque'), natural. Se retira "
                  "'pongo una trampa para ver qué animales hay', que pregunta por captura, o sea la misma "
                  "entrada: el proposal no lo justifica; conviene restaurarla."),
    },
    "activities": {"drop": [], "notes": "Sin ejemplos añadidos ni retirados en esta propuesta; sin revisión de ejemplos."},
    "conversation": {"drop": [], "notes": "Sin ejemplos añadidos ni retirados en esta propuesta; sin revisión de ejemplos."},
    "flora_ecosystems": {"drop": [], "notes": "Sin ejemplos añadidos ni retirados en esta propuesta; sin revisión de ejemplos."},
    "history_culture": {"drop": [], "notes": "Sin ejemplos añadidos ni retirados en esta propuesta; sin revisión de ejemplos."},
}


def fold(text: str) -> str:
    """Lowercase, strip accents and punctuation, collapse spaces. Used for folded duplicates."""
    s = unicodedata.normalize("NFD", text.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.split())


def raw_key(text: str) -> str:
    return " ".join(text.lower().split())


def load_hunspell(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]
    raw = {ln.split("/")[0].split("\t")[0].strip().lower() for ln in lines}
    raw.discard("")
    folded = {fold(w) for w in raw}
    accented_of: dict[str, set[str]] = defaultdict(set)
    for w in raw:
        accented_of[fold(w)].add(w)
    return raw, folded, accented_of


def in_dic(ft: str, folded: set[str]) -> bool:
    if ft in folded:
        return True
    for suf in SUFFIXES:
        if ft.endswith(suf) and len(ft) - len(suf) >= 3 and ft[: -len(suf)] in folded:
            return True
    return False


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", text)


def load_baseline() -> dict[str, list[dict]]:
    out = {}
    for p in sorted(SNAP.glob("*.json")):
        out[p.stem] = json.loads(p.read_text(encoding="utf-8"))["entries"]
    return out


def apply_ops(section: str, ops: list[dict], corpus: dict, owner: dict, errors: list) -> dict:
    """Apply one proposal in memory. Returns {entry_id: section} for the ids it touched."""
    touched = {}
    for rec in ops:
        op = rec.get("op", "add")
        eid = rec["id"] if op == "delete" else rec["entry"]["id"]
        if not eid.startswith(section + "."):
            errors.append({"section": section, "id": eid, "error": "id outside section"})
            continue
        if op == "add":
            if eid in owner:
                errors.append({"section": section, "id": eid, "error": "add of existing id"})
                continue
            corpus[section].append(rec["entry"])
            owner[eid] = section
        elif op == "update":
            if owner.get(eid) != section:
                errors.append({"section": section, "id": eid, "error": "update of unknown id"})
                continue
            entries = corpus[section]
            idx = next(i for i, e in enumerate(entries) if e["id"] == eid)
            entries[idx] = rec["entry"]
        elif op == "delete":
            if owner.get(eid) != section:
                errors.append({"section": section, "id": eid, "error": "delete of unknown id"})
                continue
            corpus[section] = [e for e in corpus[section] if e["id"] != eid]
            del owner[eid]
        else:
            errors.append({"section": section, "id": eid, "error": f"unknown op {op}"})
            continue
        touched[eid] = section
    return touched


def pct(n: int, d: int):
    return round(n / d, 4) if d else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dic", type=Path, default=DEFAULT_DIC, help="hunspell .dic for es_CO")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    base = load_baseline()
    sections = sorted(base)
    assert len(sections) == 15, f"expected 15 baseline sections, found {len(sections)}"

    before_entries = {e["id"]: (s, e) for s, es in base.items() for e in es}
    corpus = {s: list(es) for s, es in base.items()}
    owner = {e["id"]: s for s, es in base.items() for e in es}
    errors: list[dict] = []
    proposal_of: dict[str, str] = {}
    for s in sections:
        ops = json.loads((PROPS / f"{s}.json").read_text(encoding="utf-8"))["operations"]
        for eid in apply_ops(s, ops, corpus, owner, errors):
            proposal_of[eid] = s
    assert not errors, errors

    after_entries = {e["id"]: (s, e) for s, es in corpus.items() for e in es}
    # Flat list of every example in the after-corpus; "added" marks those no baseline entry had.
    rows = []
    for eid, (sec, e) in after_entries.items():
        before_set = set(before_entries[eid][1]["examples"]) if eid in before_entries else set()
        for text in e["examples"]:
            rows.append({
                "id": eid, "section": sec, "text": text, "fold": fold(text),
                "added": text not in before_set, "label": e["label"],
                "answer_short": e.get("answer", {}).get("short", ""),
                "audience": e["audience"], "proposal": proposal_of.get(eid),
            })
    removed = []
    for eid, (sec, e) in before_entries.items():
        after_set = set(after_entries[eid][1]["examples"]) if eid in after_entries else set()
        for text in e["examples"]:
            if text not in after_set:
                removed.append({"section": sec, "id": eid, "example": text,
                                "words": len(text.split()), "deleted_entry": eid not in after_entries})

    # Duplicate groups over the whole after-corpus, keyed by raw and folded text.
    by_fold: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_fold[r["fold"]].append(i)

    dup_partners: dict[int, list[dict]] = defaultdict(list)
    for key, idxs in by_fold.items():
        if len(idxs) < 2 or not any(rows[i]["added"] for i in idxs):
            continue
        for i in idxs:
            if not rows[i]["added"]:
                continue
            for j in idxs:
                if j == i:
                    continue
                kind = "exact" if raw_key(rows[i]["text"]) == raw_key(rows[j]["text"]) else "folded"
                dup_partners[i].append({"kind": kind, "id": rows[j]["id"], "section": rows[j]["section"],
                                        "added": rows[j]["added"], "text": rows[j]["text"]})

    cross_groups = []
    for key, idxs in by_fold.items():
        if len(idxs) < 2 or not any(rows[i]["added"] for i in idxs):
            continue
        ids = {rows[i]["id"] for i in idxs}
        if len(ids) < 2:
            continue
        cross_groups.append({
            "fold": key,
            "example": rows[idxs[0]]["text"],
            "occurrences": [{"id": rows[i]["id"], "section": rows[i]["section"],
                             "status": "added" if rows[i]["added"] else "existing",
                             "proposal": rows[i]["proposal"]} for i in idxs],
            "sections": sorted({rows[i]["section"] for i in idxs}),
        })
    cross_groups.sort(key=lambda g: (-len(g["occurrences"]), g["fold"]))

    # e5 near-duplicates for each added example against every after-corpus example.
    entry_index = {eid: k for k, eid in enumerate(after_entries)}
    owner_idx = np.array([entry_index[r["id"]] for r in rows])
    vecs = route_check.embed([r["text"] for r in rows])
    near: dict[int, dict[str, list[dict]]] = {}
    for i, r in enumerate(rows):
        if not r["added"]:
            continue
        sims = vecs @ vecs[i]
        sims[i] = -1.0
        same = owner_idx == owner_idx[i]
        same_hits = np.nonzero(same & (sims >= THRESH_SAME))[0]
        other_hits = np.nonzero(~same & (sims >= THRESH_OTHER))[0]
        bucket = {"same_entry": [], "other_entry": []}
        for kind, hits in (("same_entry", same_hits), ("other_entry", other_hits)):
            for j in hits[np.argsort(-sims[hits])]:
                if rows[j]["fold"] == r["fold"]:
                    continue  # already reported as a folded duplicate
                bucket[kind].append({"id": rows[j]["id"], "section": rows[j]["section"],
                                     "text": rows[j]["text"], "cos": round(float(sims[j]), 4)})
        near[i] = bucket

    # Template filler: trigrams with a content word, repeated across one entry's added examples.
    added_by_entry: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        if r["added"]:
            added_by_entry[r["id"]].append(i)
    filler: dict[str, list[dict]] = defaultdict(list)
    for eid, idxs in added_by_entry.items():
        n = len(idxs)
        frame_hits: dict[str, list[str]] = defaultdict(list)
        for i in idxs:
            toks = rows[i]["fold"].split()
            grams = {" ".join(toks[k:k + 3]) for k in range(len(toks) - 2)
                     if any(t not in STOP for t in toks[k:k + 3])}
            for g in grams:
                frame_hits[g].append(rows[i]["text"])
        for frame, texts in frame_hits.items():
            if len(texts) >= 3 and len(texts) / n >= 0.25:
                filler[rows[idxs[0]]["section"]].append({
                    "id": eid, "frame": frame, "count": len(texts), "of_added": n, "examples": texts})

    # Hunspell heuristics for unknown tokens and no-accent forms.
    raw_dic, folded_dic, accented_of = load_hunspell(args.dic)

    def token_flags(text: str) -> tuple[list[str], list[str], bool]:
        unknown, no_accent = [], []
        english = False
        for t in tokens(text):
            lt = t.lower()
            ft = fold(lt)
            if lt in ENGLISH:
                english = True
                continue
            if len(lt) < 3 or t[0].isupper() or any(ch.isdigit() for ch in lt):
                continue
            if lt not in raw_dic and any(f != lt for f in accented_of.get(ft, ())):
                no_accent.append(lt)
            elif not in_dic(ft, folded_dic):
                unknown.append(lt)
        return unknown, no_accent, english

    per_section: dict[str, dict] = {}
    for s in sections:
        s_added = [i for i, r in enumerate(rows) if r["added"] and r["section"] == s]
        n_add = len(s_added)
        entries_changed = {rows[i]["id"] for i in s_added} | {
            x["id"] for x in removed if x["section"] == s}
        s_removed = [x for x in removed if x["section"] == s]
        short3 = long15 = noacc = unk = eng = tail = 0
        typo_list, noacc_list, eng_list = [], [], []
        exact, folded_dups, near_same, near_other = [], [], [], []
        for i in s_added:
            r = rows[i]
            words = len(r["text"].split())
            short3 += words <= SHORT_MAX
            long15 += words >= LONG_MIN
            tail += bool(CONTRAST_RE.search(r["text"]))
            unknown, no_accent, english = token_flags(r["text"])
            if no_accent:
                noacc += 1
                noacc_list.append({"id": r["id"], "example": r["text"], "tokens": no_accent})
            if unknown:
                unk += 1
                typo_list.append({"id": r["id"], "example": r["text"], "tokens": unknown})
            if english:
                eng += 1
                eng_list.append({"id": r["id"], "example": r["text"]})
            partners = dup_partners.get(i, [])
            if partners:
                kinds = {p["kind"] for p in partners}
                row_out = {"id": r["id"], "example": r["text"], "partners": partners}
                (exact if "exact" in kinds else folded_dups).append(row_out)
            if i in near:
                if near[i]["same_entry"]:
                    near_same.append({"id": r["id"], "example": r["text"], "hits": near[i]["same_entry"]})
                if near[i]["other_entry"]:
                    near_other.append({"id": r["id"], "example": r["text"], "hits": near[i]["other_entry"]})
        pick = list(range(n_add)) if n_add <= SAMPLE_SIZE else [
            round(k * (n_add - 1) / (SAMPLE_SIZE - 1)) for k in range(SAMPLE_SIZE)]
        sample = [{"id": rows[s_added[k]]["id"], "label": rows[s_added[k]]["label"],
                   "answer_short": rows[s_added[k]]["answer_short"][:160],
                   "example": rows[s_added[k]]["text"]} for k in pick]
        frames = filler.get(s, [])
        manual = MANUAL.get(s, {})
        drops = manual.get("drop", [])
        added_texts = {(rows[i]["id"], rows[i]["text"]) for i in s_added}
        for d in drops:
            assert (d["id"], d["example"]) in added_texts, f"drop not an added example: {d}"
        blockers = bool(drops or exact or folded_dups or near_same or frames)
        per_section[s] = {
            "entries_changed": len(entries_changed),
            "added_examples": n_add,
            "removed_examples": len(s_removed),
            "removed_short_le2": [x for x in s_removed if x["words"] <= 2],
            "share_short_le3": pct(short3, n_add),
            "share_long_ge15": pct(long15, n_add),
            "share_english": pct(eng, n_add),
            "english_max_per_entry": max(Counter(x["id"] for x in eng_list).values(), default=0),
            "share_contrast_tail": pct(tail, n_add),
            "near_cross_section_ge_0.92": sum(
                1 for i in s_added for h in near.get(i, {}).get("other_entry", []) if h["section"] != s),
            "share_no_accent_candidates": pct(noacc, n_add),
            "share_unknown_token_candidates": pct(unk, n_add),
            "exact_or_folded_duplicates": len(exact) + len(folded_dups),
            "near_same_entry_ge_0.95": len(near_same),
            "near_other_entry_ge_0.92": len(near_other),
            "template_frames": len(frames),
            "exact_duplicates": exact,
            "folded_duplicates": folded_dups,
            "near_same_entry": near_same,
            "near_other_entry": near_other,
            "template_frame_list": frames,
            "english_examples": eng_list,
            "no_accent_candidates": noacc_list,
            "unknown_token_candidates": typo_list,
            "sample_read": sample,
            "verdict": manual.get("verdict", "issues" if blockers else "ok"),
            "drop": drops,
            "notes": manual.get("notes", ""),
        }

    cross_near = []
    for i, r in enumerate(rows):
        if not r["added"] or i not in near:
            continue
        for h in near[i]["other_entry"]:
            if h["section"] != r["section"]:
                cross_near.append({"kind": "near_cross_section", "cos": h["cos"],
                                   "example": r["text"], "id": r["id"], "section": r["section"],
                                   "other_id": h["id"], "other_section": h["section"],
                                   "other_example": h["text"]})
    cross_near.sort(key=lambda x: -x["cos"])

    report = {
        "generated_by": "research_notes/curation_v2/tools/examples_audit.py",
        "baseline": "research_notes/curation_v2/snapshots/sections_before",
        "thresholds": {"near_same_entry": THRESH_SAME, "near_other_entry": THRESH_OTHER,
                       "short_max_words": SHORT_MAX, "long_min_words": LONG_MIN},
        "heuristics_note": ("no_accent and unknown_token shares are hunspell es_CO heuristics "
                            "(affix-stripped lookup). no_accent is informative; unknown_token is noisy "
                            "(conjugated verbs such as 'tiene' are missing from the lexicon). Both "
                            "locate examples for a reader and are not verdicts. contrast_tail matches "
                            "'X, no Y' and 'no es/no la' clauses."),
        "totals": {"added_examples": sum(v["added_examples"] for v in per_section.values()),
                   "removed_examples": len(removed),
                   "exact_or_folded_groups_with_added": len(cross_groups)},
        "errors": errors,
        "per_section": per_section,
        "cross_proposal_duplicates": [dict(kind="exact_or_folded", **{k: v for k, v in g.items()})
                                      for g in cross_groups] + cross_near,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    summary = {s: {k: per_section[s][k] for k in ("added_examples", "removed_examples",
                                                 "exact_or_folded_duplicates",
                                                 "near_same_entry_ge_0.95", "template_frames",
                                                 "verdict")} for s in sections}
    print(json.dumps({"totals": report["totals"], "per_section": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
