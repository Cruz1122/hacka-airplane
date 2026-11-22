"""dialogues suite: 36 scripted Spanish dialogues driven by the code-owned FSM.

Each dialogue is a script of user turns. A gold simulator that mirrors
``fsm.driver`` (same LLM-call sequence, same code replies) turns the script into
teacher-forced step cases evaluated from the gold state:

- turn-boundary info question: ``route`` (ROUTER) + ``answer`` (topic state);
- flow start / resume: ``route`` whose gold is the side-effect tool with the slots given
  so far (the driver starts the flow; ``gold.missing_required`` lists the rest);
- slot answer: ``extract`` of the pending slot;
- correction in SLOT_FILLING: ``extract`` (null) + ``route`` restating the flow call with
  the corrected slots; correction in CONFIRM: ``route`` with only the flow tool visible;
- intent switch in SLOT_FILLING: ``extract`` (null) + ``route`` + ``answer``;
- confirmation and cancellation are code-only turns (no generative step).

``gold.next_state`` is the immediate successor of ``fsm_state`` (``states.can_transition``
holds); ``tags.gold_path`` holds the full path the driver records for the step.
Every step carries both ``state_summary`` and ``history`` so either alone resolves it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nevados_bench.fsm import states as S
from nevados_bench.schemas import Case, Dialogue, DialogueTurn, Gold, ToolCall
from nevados_bench.world import World

SUITE = "dialogues"
PHENOMENA = ("slot_filling", "correction", "intent_switch", "cancel_resume", "ellipsis",
             "info_chain")  # fmt: skip

A, B, C, D = "alto_cenizo", "laguna_espejo", "valle_bruma", "refugio_quelital"
RV, RE = "register_visit", "report_emergency"

# Code replies, identical to fsm.driver.
CANCEL_FILLING_REPLY = "Listo, cancelé el trámite. ¿En qué más te puedo ayudar?"
CANCEL_CONFIRM_REPLY = "Entendido, no envié nada. ¿En qué más te puedo ayudar?"


# ----------------------------------------------------------------------------- script DSL


@dataclass(frozen=True)
class Ask:
    """Information question: route + answer (intent switch when a flow is pending)."""

    message: str
    tool: str
    args: dict[str, Any]
    values: tuple[str, ...]
    phenomenon: str | None = None  # default: info_chain, or intent_switch inside a flow
    mentions: tuple[str, ...] = ()  # stations named in the text without being queried


@dataclass(frozen=True)
class Start:
    """Start (or resume) a side-effect flow with the slots the user gave or implied."""

    message: str
    tool: str
    args: dict[str, Any]
    phenomenon: str = "slot_filling"


@dataclass(frozen=True)
class Fill:
    message: str
    value: Any
    phenomenon: str = "slot_filling"


@dataclass(frozen=True)
class Correct:
    message: str
    changes: dict[str, Any]
    phenomenon: str = "correction"


@dataclass(frozen=True)
class Confirm:
    message: str
    phenomenon: str = "slot_filling"


@dataclass(frozen=True)
class Cancel:
    message: str
    phenomenon: str = "cancel_resume"


Turn = Ask | Start | Fill | Correct | Confirm | Cancel


def _trail(trail_id: str) -> dict[str, Any]:
    return {"trail_id": trail_id}


# fmt: off
SCRIPTS: tuple[tuple[Turn, ...], ...] = (
    # ------------------------------------------------------------------ depth 3 (01-12)
    (  # 01
        Start("Hola, quiero registrar una visita a la Estación Alto Cenizo para el 5 de "
              "diciembre, somos 4 personas nacionales.", RV,
              {"station": A, "date": "2026-12-05", "group_size": 4, "visitor_type": "nacional"}),
        Confirm("Sí, confirmo"),
        Ask("Perfecto. ¿Y a qué altitud queda esa estación?", "get_station_altitude",
            {"station": A}, ("4137",), "ellipsis"),
    ),
    (  # 02
        Ask("Estoy dudando entre Alto Cenizo y Refugio Quelital. ¿A qué altura está Alto "
            "Cenizo?", "get_station_altitude", {"station": A}, ("4137",), mentions=(D,)),
        Ask("¿Y la otra?", "get_station_altitude", {"station": D}, ("4286",), "ellipsis"),
        Ask("¿Y allá cuánto cuesta la entrada para extranjeros?", "get_entry_fee",
            {"station": D, "visitor_type": "extranjero"}, ("112300",), "ellipsis"),
    ),
    (  # 03
        Start("Necesito reportar una emergencia: un compañero tiene hipotermia cerca de la "
              "Estación Valle Bruma.", RE, {"station": C, "emergency_type": "hipotermia"}),
        Fill("Es solo él, una persona.", 1),
        Confirm("Sí, envíalo ya"),
    ),
    (  # 04
        Start("Quiero registrar una visita a Valle Bruma para el 12 de diciembre.", RV,
              {"station": C, "date": "2026-12-12"}),
        Cancel("Mmm, mejor olvídalo por ahora."),
        Start("Perdón, sí lo necesito. Retoma el registro que estábamos haciendo.", RV,
              {"station": C, "date": "2026-12-12"}, "cancel_resume"),
    ),
    (  # 05
        Ask("¿A qué hora abre la Estación Laguna Espejo?", "get_opening_hours",
            {"station": B}, ("05:55",)),
        Ask("¿Y la de Valle Bruma?", "get_opening_hours", {"station": C}, ("07:25",),
            "ellipsis"),
        Ask("¿Qué equipo es obligatorio para los senderos de esa estación?",
            "get_required_gear", {"station": C}, ("linterna frontal", "polainas"), "ellipsis"),
    ),
    (  # 06
        Start("Quiero registrar una visita a la Estación Refugio Quelital para este domingo.",
              RV, {"station": D, "date": "2026-11-29"}),
        Ask("Antes de seguir, ¿qué equipo es obligatorio allá?", "get_required_gear",
            {"station": D}, ("bastones de trekking", "gafas con filtro uv")),
        Start("Listo, sigamos con el registro: vamos 3 personas.", RV,
              {"station": D, "date": "2026-11-29", "group_size": 3}, "intent_switch"),
    ),
    (  # 07
        Start("Registra por favor una visita a Laguna Espejo el 3 de diciembre para 4 "
              "personas.", RV, {"station": B, "date": "2026-12-03", "group_size": 4}),
        Fill("Somos nacionales.", "nacional"),
        Correct("Espera, somos 5, no 4.", {"group_size": 5}),
    ),
    (  # 08
        Start("Tengo que reportar una emergencia: hay una persona perdida cerca de Alto "
              "Cenizo.", RE, {"station": A, "emergency_type": "persona_perdida"}),
        Correct("Perdón, me equivoqué: estamos en Valle Bruma, no en Alto Cenizo.",
                {"station": C}),
        Fill("Es una sola persona la que está perdida.", 1),
    ),
    (  # 09
        Ask("¿Cuál es la línea de emergencias de la Estación Refugio Quelital?",
            "get_emergency_contacts", {"station": D}, ("4952",)),
        Ask("¿Y cuál es el protocolo si a alguien le da mal de altura allá?",
            "get_altitude_sickness_protocol", {"station": D}, ("370", "55"), "ellipsis"),
        Ask("¿Y el refugio contra tormentas más cercano?", "find_nearest_shelter",
            {"station": D}, ("abrigo la morrena",), "ellipsis"),
    ),
    (  # 10
        Start("Quiero inscribir una visita para 6 personas en la Estación Alto Cenizo.", RV,
              {"station": A, "group_size": 6}),
        Ask("Oye, ¿y cuánto cuesta la entrada allá para nacionales?", "get_entry_fee",
            {"station": A, "visitor_type": "nacional"}, ("38500",)),
        Ask("¿Y a qué hora cierran?", "get_opening_hours", {"station": A}, ("15:50",),
            "ellipsis"),
    ),
    (  # 11
        Start("Reporto una emergencia: dos personas lesionadas en Laguna Espejo.", RE,
              {"station": B, "emergency_type": "lesion", "people_count": 2}),
        Cancel("No."),
        Start("Perdón, sí hay que enviarlo. Retoma el reporte de las dos personas "
              "lesionadas.", RE,
              {"station": B, "emergency_type": "lesion", "people_count": 2}, "cancel_resume"),
    ),
    (  # 12
        Ask("¿Cuánto mide el Sendero Paso de la Garza?", "get_trail_details",
            _trail("sendero_paso_garza"), ("4160",)),
        Ask("¿Y cuánto tiempo se demora uno en recorrerlo?", "get_trail_details",
            _trail("sendero_paso_garza"), ("167",), "ellipsis"),
        Ask("¿A qué hora es la ventana de clima estable en esa estación?",
            "get_weather_window", {"station": B}, ("07:05", "11:20"), "ellipsis"),
    ),
    # ------------------------------------------------------------------ depth 6 (13-24)
    (  # 13
        Start("Buenas tardes, quisiera registrar una visita a la Estación Laguna Espejo.", RV,
              {"station": B}),
        Fill("Para el viernes 4 de diciembre.", "2026-12-04"),
        Fill("Vamos a ir cuatro personas.", 4),
        Correct("Ay, perdón, cambia la fecha: mejor para el sábado 5 de diciembre.",
                {"date": "2026-12-05"}),
        Fill("Todos somos extranjeros.", "extranjero"),
        Confirm("Sí, perfecto."),
    ),
    (  # 14
        Ask("¿Qué senderos salen de la Estación Valle Bruma y cuánto mide cada uno?",
            "list_trails", {"station": C}, ("2930", "1480", "5870")),
        Ask("¿Cuánto se demora uno en el Sendero Quebrada Lirio?", "get_trail_details",
            _trail("sendero_quebrada_lirio"), ("63",)),
        Ask("¿Y el de Cuchilla Parda?", "get_trail_details", _trail("sendero_cuchilla_parda"),
            ("228",), "ellipsis"),
        Ask("¿Qué edad mínima piden para esos senderos?", "get_entry_requirements",
            {"station": C}, ("9",), "ellipsis"),
        Ask("¿Y hasta qué hora es el último ingreso?", "get_opening_hours", {"station": C},
            ("12:35",), "ellipsis"),
        Ask("¿Cuál es la ventana de clima estable allá?", "get_weather_window",
            {"station": C}, ("06:35", "12:10"), "ellipsis"),
    ),
    (  # 15
        Start("Necesito reportar una emergencia en Refugio Quelital, a mi papá le dio mal de "
              "altura.", RE, {"station": D, "emergency_type": "mal_de_altura"}),
        Ask("Mientras tanto, ¿qué hacemos con él? ¿Cuál es el protocolo de mal de altura "
            "allá?", "get_altitude_sickness_protocol", {"station": D}, ("370", "55")),
        Start("Ya lo bajamos. Igual envía el reporte de emergencia que estábamos haciendo, es "
              "solo mi papá.", RE,
              {"station": D, "emergency_type": "mal_de_altura", "people_count": 1},
              "intent_switch"),
        Confirm("Sí, confirmo."),
        Ask("¿Dónde queda el puesto de oxígeno de esa estación y hasta qué hora atiende?",
            "get_altitude_sickness_protocol", {"station": D},
            ("refugio piedra larga", "17:40"), "ellipsis"),
        Ask("¿Y cuál es la línea de emergencias de allá, por si empeora?",
            "get_emergency_contacts", {"station": D}, ("4952",), "ellipsis"),
    ),
    (  # 16
        Start("Hola, quiero registrar una visita a Alto Cenizo para el 19 de diciembre.", RV,
              {"station": A, "date": "2026-12-19"}),
        Fill("Seremos 8.", 8),
        Cancel("Uy, déjalo así, primero tengo que hablar con mi grupo."),
        Ask("¿Cuántas personas máximo pueden ir en un grupo en Alto Cenizo?",
            "get_park_rules", {"station": A}, ("17",)),
        Start("Listo, ya hablé con ellos. Retomemos el registro que había empezado.", RV,
              {"station": A, "date": "2026-12-19", "group_size": 8}, "cancel_resume"),
        Fill("Son nacionales.", "nacional"),
    ),
    (  # 17
        Ask("Estamos entre Laguna Espejo y Valle Bruma. ¿Cuánto cuesta la entrada para "
            "nacionales en Laguna Espejo?", "get_entry_fee",
            {"station": B, "visitor_type": "nacional"}, ("27300",), mentions=(C,)),
        Ask("¿Y en la otra?", "get_entry_fee", {"station": C, "visitor_type": "nacional"},
            ("21700",), "ellipsis"),
        Start("Bueno, nos quedamos con la más barata. Regístranos para el domingo 29 de "
              "noviembre.", RV, {"station": C, "date": "2026-11-29"}, "ellipsis"),
        Fill("Somos tres.", 3),
        Fill("Nacionales todos.", "nacional"),
        Correct("Mmm, espera: somos cuatro, se nos unió mi prima.", {"group_size": 4}),
    ),
    (  # 18
        Start("Quiero reportar una emergencia en la Estación Laguna Espejo.", RE,
              {"station": B}),
        Fill("Mi amigo se cayó y se lastimó la pierna.", "lesion"),
        Correct("Perdón, me corrijo: no estamos en Laguna Espejo, estamos en Alto Cenizo.",
                {"station": A}),
        Fill("Solo él, una persona.", 1),
        Confirm("Sí, envíalo."),
        Ask("¿Qué debemos hacer mientras llega el rescate?", "get_emergency_procedure",
            {"emergency_type": "lesion", "station": A}, ("roca tizon", "38"), "ellipsis"),
    ),
    (  # 19
        Ask("¿A qué hora sale el bus rural hacia Refugio Quelital?", "get_transport_options",
            {"station": D}, ("04:35",)),
        Ask("¿Y cuánto dura el trayecto?", "get_transport_options", {"station": D},
            ("148",), "ellipsis"),
        Ask("¿Qué servicios tiene la estación cuando uno llega?", "get_station_services",
            {"station": D}, ("cafeteria el condor",), "ellipsis"),
        Ask("¿Se puede llevar mascota al parque?", "check_item_allowed",
            {"item": "mascotas"}, ("356200",)),
        Ask("¿Y se puede acampar?", "check_item_allowed", {"item": "carpas"}, ("3",),
            "ellipsis"),
        Ask("¿Qué protector solar exigen para los senderos de Refugio Quelital?",
            "get_required_gear", {"station": D}, ("85",)),
    ),
    (  # 20
        Start("Quiero registrar una visita a Valle Bruma el 3 de diciembre, vamos 2.", RV,
              {"station": C, "date": "2026-12-03", "group_size": 2}),
        Ask("Una pregunta antes: ¿qué está prohibido hacer allá?", "get_park_rules",
            {"station": C}, ("salir de los senderos senalizados",)),
        Ask("¿Y de cuánto es la multa?", "get_park_rules", {"station": C}, ("243100",),
            "ellipsis"),
        Start("Ok, sigamos con el registro de la visita, somos estudiantes con tarifa "
              "reducida.", RV,
              {"station": C, "date": "2026-12-03", "group_size": 2,
               "visitor_type": "reducida"}, "intent_switch"),
        Cancel("Mejor no, cancela todo."),
        Ask("¿Cuál es la tarifa reducida en Valle Bruma, para tenerla en cuenta?",
            "get_entry_fee", {"station": C, "visitor_type": "reducida"}, ("9400",)),
    ),
    (  # 21
        Start("¡Emergencia! Hay un incendio cerca de la Estación Alto Cenizo y hay tres "
              "personas atrapadas.", RE,
              {"station": A, "emergency_type": "incendio", "people_count": 3}),
        Confirm("Sí, confirmo, rápido."),
        Ask("¿Cuáles son los contactos de emergencia de esa estación? Necesito el de la "
            "brigada contra incendios.", "get_emergency_contacts", {"station": A},
            ("8357",), "ellipsis"),
        Ask("¿Y qué canal de radio usan los guías allá?", "get_emergency_contacts",
            {"station": A}, ("31",), "ellipsis"),
        Ask("¿Dónde está el refugio contra tormentas más cercano a esa estación?",
            "find_nearest_shelter", {"station": A}, ("refugio los liquenes", "760"),
            "ellipsis"),
        Ask("Si nos coge una tormenta eléctrica allá, ¿cuánto hay que esperar después del "
            "último trueno?", "get_emergency_procedure",
            {"emergency_type": "tormenta_electrica", "station": A}, ("52",), "ellipsis"),
    ),
    (  # 22
        Start("Necesito registrar una visita a Refugio Quelital.", RV, {"station": D}),
        Fill("El sábado 12 de diciembre.", "2026-12-12"),
        Ask("Antes de darte el número de personas: ¿cuál es la edad mínima allá?",
            "get_entry_requirements", {"station": D}, ("16",)),
        Start("Ok, entonces seguimos con el registro, seremos 5 adultos.", RV,
              {"station": D, "date": "2026-12-12", "group_size": 5}, "intent_switch"),
        Correct("Perdón, en realidad seremos 6, no 5.", {"group_size": 6}),
        Fill("Extranjeros.", "extranjero"),
    ),
    (  # 23
        Ask("Voy a hacer Alto Cenizo y Laguna Espejo. ¿Cuál es la línea de emergencias de "
            "Alto Cenizo?", "get_emergency_contacts", {"station": A}, ("6274",),
            mentions=(B,)),
        Ask("¿Y la de la otra estación?", "get_emergency_contacts", {"station": B},
            ("5819",), "ellipsis"),
        Ask("¿Qué hago si me da mal de altura en Laguna Espejo?",
            "get_altitude_sickness_protocol", {"station": B}, ("280", "35")),
        Ask("¿Y en Alto Cenizo cuántos metros hay que bajar?",
            "get_altitude_sickness_protocol", {"station": A}, ("340",), "ellipsis"),
        Ask("Quiero llegar a 4.600 metros. ¿Hasta qué altitud puede subir un visitante sin "
            "permiso?", "get_acclimatization_advice", {"target_altitude_m": 4600},
            ("4689",)),
        Ask("¿Y cuánto tiempo debo aclimatarme antes de subir?", "get_acclimatization_advice",
            {"target_altitude_m": 4600}, ("48",), "ellipsis"),
    ),
    (  # 24
        Start("Quiero reportar una emergencia, se perdió una persona de mi grupo en Valle "
              "Bruma.", RE,
              {"station": C, "emergency_type": "persona_perdida", "people_count": 1}),
        Cancel("Espera, no quiero enviarlo todavía, creo que ya la vi."),
        Ask("¿Qué debe hacer alguien que se pierde en esa estación?",
            "get_emergency_procedure", {"emergency_type": "persona_perdida", "station": C},
            ("6", "12"), "ellipsis"),
        Start("No era ella. Retoma el reporte de la persona perdida, por favor.", RE,
              {"station": C, "emergency_type": "persona_perdida", "people_count": 1},
              "cancel_resume"),
        Confirm("Sí, envíalo ya."),
        Ask("¿Por qué canal de radio se comunican los guías allá?", "get_emergency_contacts",
            {"station": C}, ("37",), "ellipsis"),
    ),
    # ----------------------------------------------------------------- depth 12 (25-36)
    (  # 25
        Ask("Hola, ¿a qué hora abre la Estación Refugio Quelital?", "get_opening_hours",
            {"station": D}, ("06:10",)),
        Ask("¿Y hasta qué hora se puede entrar?", "get_opening_hours", {"station": D},
            ("15:10",), "ellipsis"),
        Ask("¿Cuánto vale la entrada para nacionales allá?", "get_entry_fee",
            {"station": D, "visitor_type": "nacional"}, ("44600",), "ellipsis"),
        Ask("¿Y para extranjeros?", "get_entry_fee",
            {"station": D, "visitor_type": "extranjero"}, ("112300",), "ellipsis"),
        Start("Bien. Quiero registrar una visita allá para el domingo 20 de diciembre.", RV,
              {"station": D, "date": "2026-12-20"}, "ellipsis"),
        Fill("Vamos a ser siete.", 7),
        Ask("Antes, ¿qué equipo es obligatorio en esa estación?", "get_required_gear",
            {"station": D}, ("bastones de trekking", "gafas con filtro uv")),
        Start("Listo. Sigamos con el registro que dejamos a medias.", RV,
              {"station": D, "date": "2026-12-20", "group_size": 7}, "intent_switch"),
        Fill("Somos extranjeros, de Ecuador.", "extranjero"),
        Correct("Uy, espera, la fecha es el sábado 19, no el domingo.", {"date": "2026-12-19"}),
        Confirm("Sí, ahora sí, confirmo."),
        Ask("¿Cuál es la línea de emergencias de esa estación, por si acaso?",
            "get_emergency_contacts", {"station": D}, ("4952",), "ellipsis"),
    ),
    (  # 26
        Ask("Vamos a subir al Sendero Glaciar Viejo. ¿Cuánto mide?", "get_trail_details",
            _trail("sendero_glaciar_viejo"), ("7140",)),
        Ask("¿Y cuánto tiempo toma ida y vuelta?", "get_trail_details",
            _trail("sendero_glaciar_viejo"), ("271",), "ellipsis"),
        Ask("¿Cuál es la ventana de clima estable en la estación de ese sendero?",
            "get_weather_window", {"station": D}, ("05:45", "09:50"), "ellipsis"),
        Ask("Si escuchamos truenos en ese sendero, ¿cuánto tiempo hay que esperar para "
            "seguir?", "get_emergency_procedure",
            {"emergency_type": "tormenta_electrica", "station": D}, ("52",), "ellipsis"),
        Ask("¿Y cuál es el refugio más cercano para tormentas?", "find_nearest_shelter",
            {"station": D}, ("abrigo la morrena", "1270"), "ellipsis"),
        Start("Necesito reportar una emergencia: mi hermano tiene síntomas de hipotermia en "
              "Refugio Quelital.", RE, {"station": D, "emergency_type": "hipotermia"}),
        Ask("¿Qué hago mientras tanto con él?", "get_emergency_procedure",
            {"emergency_type": "hipotermia", "station": D}, ("manta termica", "33")),
        Start("Ya lo cubrimos. Por favor continúa con el reporte de emergencia, es una sola "
              "persona.", RE,
              {"station": D, "emergency_type": "hipotermia", "people_count": 1},
              "intent_switch"),
        Correct("Espera, mi prima también tiene frío y tiembla, son dos personas.",
                {"people_count": 2}),
        Confirm("Sí, confirmo."),
        Ask("¿Cuál es el número de la línea de rescate en montaña? Dame los contactos de "
            "emergencia de esa estación.", "get_emergency_contacts", {"station": D},
            ("3168",), "ellipsis"),
        Ask("¿Y el canal de radio de los guías de allá?", "get_emergency_contacts",
            {"station": D}, ("43",), "ellipsis"),
    ),
    (  # 27
        Start("Quiero registrar una visita a Laguna Espejo.", RV, {"station": B}),
        Fill("Para mañana.", "2026-11-27"),
        Fill("Somos dos.", 2),
        Cancel("Ay no, cancela, mañana no podemos."),
        Ask("¿Cuál es la tarifa para extranjeros en Laguna Espejo?", "get_entry_fee",
            {"station": B, "visitor_type": "extranjero"}, ("81200",)),
        Ask("¿Y la reducida?", "get_entry_fee", {"station": B, "visitor_type": "reducida"},
            ("12600",), "ellipsis"),
        Start("Bueno, retomemos el registro, pero ahora para el domingo 29.", RV,
              {"station": B, "date": "2026-11-29", "group_size": 2}, "cancel_resume"),
        Fill("Ambos somos estudiantes, tarifa reducida.", "reducida"),
        Cancel("No."),
        Ask("¿Qué está prohibido en Laguna Espejo?", "get_park_rules", {"station": B},
            ("banarse o navegar en la laguna",)),
        Start("Ok, ya entendí. Ahora sí, retoma el registro y lo confirmo.", RV,
              {"station": B, "date": "2026-11-29", "group_size": 2,
               "visitor_type": "reducida"}, "cancel_resume"),
        Confirm("Sí, confirmo."),
    ),
    (  # 28
        Ask("¿A qué altitud está la Estación Laguna Espejo?", "get_station_altitude",
            {"station": B}, ("3962",)),
        Ask("¿Y Valle Bruma?", "get_station_altitude", {"station": C}, ("3518",), "ellipsis"),
        Ask("¿Cuántas especies de aves se han registrado en Valle Bruma?",
            "get_flora_fauna_info", {"station": C}, ("211",)),
        Ask("¿Y cuál es la especie emblemática?", "get_flora_fauna_info", {"station": C},
            ("rana de lluvia brumosa",), "ellipsis"),
        Ask("¿A qué distancia hay que observar al oso de anteojos allá?",
            "list_protected_species", {"station": C}, ("81",), "ellipsis"),
        Ask("¿Y en Laguna Espejo?", "list_protected_species", {"station": B}, ("72",),
            "ellipsis"),
        Ask("¿Cuál es la especie emblemática de esa estación?", "get_flora_fauna_info",
            {"station": B}, ("zambullidor espejado",), "ellipsis"),
        Ask("¿Qué equipo piden allá para entrar a los senderos?", "get_required_gear",
            {"station": B}, ("botas impermeables", "poncho de plastico"), "ellipsis"),
        Ask("¿Se puede volar un dron en el parque?", "check_item_allowed", {"item": "drones"},
            ("412900",)),
        Ask("¿Cuántas personas puede tener un grupo en Laguna Espejo?", "get_park_rules",
            {"station": B}, ("19",)),
        Ask("¿A partir de cuántas personas hay que contratar guía en esa estación?",
            "get_entry_requirements", {"station": B}, ("8",), "ellipsis"),
        Ask("¿Y qué cobertura mínima debe tener el seguro de accidentes?",
            "get_entry_requirements", {"station": B}, ("7350000",), "ellipsis"),
    ),
    (  # 29
        Start("Quiero reportar una emergencia en Alto Cenizo.", RE, {"station": A}),
        Fill("Es una tormenta eléctrica, estamos en zona abierta.", "tormenta_electrica"),
        Ask("¿Dónde está el refugio más cercano? Necesito saberlo ya.",
            "find_nearest_shelter", {"station": A}, ("refugio los liquenes", "760")),
        Start("Vamos para allá. Sigue con el reporte: somos cuatro personas.", RE,
              {"station": A, "emergency_type": "tormenta_electrica", "people_count": 4},
              "intent_switch"),
        Correct("Corrige: somos cinco, contando al guía.", {"people_count": 5}),
        Cancel("Olvídalo, ya llegamos al refugio y estamos bien."),
        Ask("¿Cuánto tiempo hay que esperar después del último trueno para salir?",
            "get_emergency_procedure",
            {"emergency_type": "tormenta_electrica", "station": A}, ("52",), "ellipsis"),
        Ask("¿Y cuál es la ventana de clima estable en esa estación?", "get_weather_window",
            {"station": A}, ("06:55", "10:40"), "ellipsis"),
        Start("Pasó mucho rato y el guía no aparece. Retoma el reporte de emergencia, pero "
              "ahora por persona perdida: es una persona.", RE,
              {"station": A, "emergency_type": "persona_perdida", "people_count": 1},
              "cancel_resume"),
        Confirm("Sí, confirmo."),
        Ask("¿Qué debe hacer el guía si está perdido en esa estación?",
            "get_emergency_procedure", {"emergency_type": "persona_perdida", "station": A},
            ("6", "12"), "ellipsis"),
        Ask("¿Cuál es la línea de emergencias de Alto Cenizo?", "get_emergency_contacts",
            {"station": A}, ("6274",)),
    ),
    (  # 30
        Start("Buenos días, quiero registrar una visita a Alto Cenizo para el sábado.", RV,
              {"station": A, "date": "2026-11-28"}),
        Fill("Seremos cuatro.", 4),
        Correct("No, mejor para el domingo, el sábado tenemos otro plan.",
                {"date": "2026-11-29"}),
        Fill("Somos nacionales.", "nacional"),
        Correct("Ah, y somos 5, no 4.", {"group_size": 5}),
        Confirm("Sí, así está bien."),
        Ask("¿A qué hora sale el bus hacia allá?", "get_transport_options", {"station": A},
            ("05:15",), "ellipsis"),
        Ask("¿Cuánto dura el viaje?", "get_transport_options", {"station": A}, ("96",),
            "ellipsis"),
        Ask("¿Qué senderos salen de esa estación y cuánto mide cada uno?", "list_trails",
            {"station": A}, ("3740", "1860", "5290"), "ellipsis"),
        Ask("¿Cuánto se demora uno en el Sendero del Mirlo?", "get_trail_details",
            _trail("sendero_mirlo"), ("74",)),
        Ask("¿Y en el Fumarola Vieja?", "get_trail_details", _trail("sendero_fumarola_vieja"),
            ("212",), "ellipsis"),
        Ask("¿Qué hago si a alguien le da mal de altura en ese sendero?",
            "get_altitude_sickness_protocol", {"station": A}, ("340", "25"), "ellipsis"),
    ),
    (  # 31
        Start("Hola, quiero registrar una visita a Valle Bruma.", RV, {"station": C}),
        Ask("Antes de seguir, ¿a qué hora abren allá?", "get_opening_hours", {"station": C},
            ("07:25",)),
        Start("Ok. Retomemos el registro: para el viernes 4 de diciembre.", RV,
              {"station": C, "date": "2026-12-04"}, "intent_switch"),
        Fill("Vamos 10 personas.", 10),
        Ask("Con ese grupo, ¿necesitamos guía en esa estación?", "get_entry_requirements",
            {"station": C}, ("8",)),
        Ask("¿Y cuál es el tamaño máximo de grupo allá?", "get_park_rules", {"station": C},
            ("23",), "ellipsis"),
        Start("Perfecto. Sigamos con el registro que dejamos.", RV,
              {"station": C, "date": "2026-12-04", "group_size": 10}, "intent_switch"),
        Fill("Todos nacionales.", "nacional"),
        Correct("Espera, cambia la fecha al sábado 5 de diciembre.", {"date": "2026-12-05"}),
        Confirm("Sí, confirmo."),
        Ask("¿Cuál es el aforo diario de esa estación para ese día?", "check_daily_capacity",
            {"station": C, "date": "2026-12-05"}, ("758",), "ellipsis"),
        Ask("¿Y el último ingreso a qué hora es?", "get_opening_hours", {"station": C},
            ("12:35",), "ellipsis"),
    ),
    (  # 32
        Ask("¿Cuál es la línea de emergencias de Valle Bruma?", "get_emergency_contacts",
            {"station": C}, ("7436",)),
        Ask("¿Y el número del puesto de policía del parque?", "get_emergency_contacts",
            {"station": C}, ("2741",), "ellipsis"),
        Start("Necesito reportar una emergencia allá mismo.", RE, {"station": C}, "ellipsis"),
        Fill("Una señora se torció el tobillo, es una lesión.", "lesion"),
        Fill("Solo ella.", 1),
        Confirm("Sí, envíalo."),
        Ask("¿Dónde es el punto de encuentro para el rescate y cuánto tardan?",
            "get_emergency_procedure", {"emergency_type": "lesion", "station": C},
            ("puente colgante norte", "27"), "ellipsis"),
        Ask("¿Dónde está el puesto de oxígeno de Valle Bruma?",
            "get_altitude_sickness_protocol", {"station": C}, ("kiosco helecho",)),
        Ask("¿Hasta qué hora atiende?", "get_altitude_sickness_protocol", {"station": C},
            ("15:35",), "ellipsis"),
        Start("Ya pasó el susto. Quiero registrar otra visita para el domingo 20 de diciembre "
              "en Laguna Espejo.", RV, {"station": B, "date": "2026-12-20"}),
        Fill("Seremos 3.", 3),
        Cancel("Mejor déjalo, lo hago otro día."),
    ),
    (  # 33
        Start("Reporto una emergencia: hay una persona con mal de altura en Laguna Espejo.",
              RE, {"station": B, "emergency_type": "mal_de_altura", "people_count": 1}),
        Correct("No es en Laguna Espejo, es en Refugio Quelital, me confundí.",
                {"station": D}),
        Correct("Y son dos personas, no una.", {"people_count": 2}),
        Confirm("Sí, ahora sí envíalo."),
        Ask("¿Cuántos metros hay que descender con mal de altura en esa estación?",
            "get_altitude_sickness_protocol", {"station": D}, ("370",), "ellipsis"),
        Ask("¿Y cuánto deben reposar?", "get_altitude_sickness_protocol", {"station": D},
            ("55",), "ellipsis"),
        Ask("¿Cuál es la altitud de esa estación?", "get_station_altitude", {"station": D},
            ("4286",), "ellipsis"),
        Ask("¿Puedo subir hasta 4.700 metros?", "get_acclimatization_advice",
            {"target_altitude_m": 4700}, ("4689",)),
        Start("Bueno, cuando se recuperen quiero registrar una visita a Laguna Espejo para el "
              "12 de diciembre.", RV, {"station": B, "date": "2026-12-12"}),
        Fill("Seremos los mismos dos.", 2),
        Correct("Perdón, mejor para el sábado 19 de diciembre.", {"date": "2026-12-19"}),
        Fill("Nacionales.", "nacional"),
    ),
    (  # 34
        Ask("Estamos comparando Alto Cenizo y Valle Bruma. ¿A qué hora cierra Alto Cenizo?",
            "get_opening_hours", {"station": A}, ("15:50",), mentions=(C,)),
        Ask("¿Y la otra?", "get_opening_hours", {"station": C}, ("14:45",), "ellipsis"),
        Ask("¿Cuál es la edad mínima en esa?", "get_entry_requirements", {"station": C},
            ("9",), "ellipsis"),
        Ask("¿Y en Alto Cenizo?", "get_entry_requirements", {"station": A}, ("14",),
            "ellipsis"),
        Ask("¿Qué servicios hay allá?", "get_station_services", {"station": A},
            ("cafeteria la ceniza", "47"), "ellipsis"),
        Ask("¿Y en la otra?", "get_station_services", {"station": C},
            ("restaurante la orquidea", "84"), "ellipsis"),
        Ask("¿Cuál es la ventana de clima estable en Valle Bruma?", "get_weather_window",
            {"station": C}, ("06:35", "12:10")),
        Ask("¿Y en Alto Cenizo?", "get_weather_window", {"station": A}, ("06:55", "10:40"),
            "ellipsis"),
        Ask("¿Qué está prohibido allá?", "get_park_rules", {"station": A},
            ("alimentar a los animales silvestres",), "ellipsis"),
        Ask("¿Y cuánto es la multa?", "get_park_rules", {"station": A}, ("287400",),
            "ellipsis"),
        Start("Listo, me quedo con Valle Bruma. Regístrame para el viernes 27 de noviembre.",
              RV, {"station": C, "date": "2026-11-27"}),
        Fill("Voy solo yo.", 1),
    ),
    (  # 35
        Start("Quiero reportar una emergencia en Refugio Quelital.", RE, {"station": D}),
        Cancel("Olvida eso, falsa alarma."),
        Ask("¿Cuáles son los contactos de emergencia de Refugio Quelital? Necesito el de la "
            "brigada contra incendios.", "get_emergency_contacts", {"station": D},
            ("8357",)),
        Start("Ahora sí es real: retoma el reporte de emergencia, hay un incendio cerca de la "
              "estación.", RE, {"station": D, "emergency_type": "incendio"},
              "cancel_resume"),
        Ask("¿Qué debemos hacer ante el incendio?", "get_emergency_procedure",
            {"emergency_type": "incendio", "station": D}, ("8357",)),
        Start("Sigue con el reporte del incendio, somos seis personas.", RE,
              {"station": D, "emergency_type": "incendio", "people_count": 6},
              "intent_switch"),
        Confirm("Sí, confirmo."),
        Ask("¿Dónde está el refugio más cercano a la estación?", "find_nearest_shelter",
            {"station": D}, ("abrigo la morrena", "1270"), "ellipsis"),
        Ask("¿Cuál es el canal de radio de los guías allá?", "get_emergency_contacts",
            {"station": D}, ("43",), "ellipsis"),
        Ask("¿Y la línea de emergencias de la estación?", "get_emergency_contacts",
            {"station": D}, ("4952",), "ellipsis"),
        Ask("¿A qué altitud está esa estación?", "get_station_altitude", {"station": D},
            ("4286",), "ellipsis"),
        Ask("¿Cuánto tiempo de aclimatación recomiendan antes de subir a 4.500 metros?",
            "get_acclimatization_advice", {"target_altitude_m": 4500}, ("48",)),
    ),
    (  # 36
        Ask("¿Cuánto cuesta la entrada para extranjeros en Alto Cenizo?", "get_entry_fee",
            {"station": A, "visitor_type": "extranjero"}, ("96400",)),
        Ask("¿Y la reducida?", "get_entry_fee", {"station": A, "visitor_type": "reducida"},
            ("15800",), "ellipsis"),
        Start("Regístrame una visita allá para el jueves 3 de diciembre, somos 2 "
              "extranjeros.", RV,
              {"station": A, "date": "2026-12-03", "group_size": 2,
               "visitor_type": "extranjero"}, "ellipsis"),
        Cancel("No."),
        Ask("¿Qué equipo es obligatorio en Alto Cenizo?", "get_required_gear", {"station": A},
            ("chaqueta cortavientos", "guantes de lana")),
        Ask("¿Y qué protector solar piden?", "get_required_gear", {"station": A}, ("85",),
            "ellipsis"),
        Start("Ya tenemos todo. Retoma el registro que cancelé.", RV,
              {"station": A, "date": "2026-12-03", "group_size": 2,
               "visitor_type": "extranjero"}, "cancel_resume"),
        Correct("Cambia algo: somos 3, se suma mi hermano.", {"group_size": 3}),
        Confirm("Sí, confirmo."),
        Ask("¿A qué hora abre esa estación?", "get_opening_hours", {"station": A}, ("06:40",),
            "ellipsis"),
        Ask("¿Cuál es el aforo diario allá el 3 de diciembre?", "check_daily_capacity",
            {"station": A, "date": "2026-12-03"}, ("437",), "ellipsis"),
        Ask("¿Cuál es la línea de emergencias allá?", "get_emergency_contacts",
            {"station": A}, ("6274",), "ellipsis"),
    ),
)
# fmt: on


# ----------------------------------------------------------------------------- simulator


@dataclass
class Trace:
    """Gold simulation of one script: the dialogue plus what the driver must reproduce."""

    dialogue: Dialogue
    replies: list[str]  # assistant reply per user turn
    executions: list[ToolCall]  # side-effect calls executed after confirmation
    final_state: str
    turn_states: list[str]  # FSM state at the start of each user turn


@dataclass
class _Flow:
    tool: str
    slots: dict[str, Any] = field(default_factory=dict)
    pending: str | None = None


def _fmt_args(args: dict[str, Any]) -> str:
    return ", ".join(f"{k}={v}" for k, v in args.items())


class _Sim:
    def __init__(self, world: World, dialogue_id: str, script: tuple[Turn, ...]):
        self.world = world
        self.dialogue_id = dialogue_id
        self.script = script
        self.depth = len(script)
        self.state = S.ROUTER
        self.flow: _Flow | None = None
        self.memory: tuple[str, str, dict[str, Any]] | None = None  # (reason, tool, slots)
        self.last_query: str | None = None
        self.stations: list[str] = []
        self.last_trail: str | None = None
        self.history: list[dict[str, str]] = []
        self.turn_index = 0
        self.steps: list[Case] = []
        self.executions: list[ToolCall] = []

    # ------------------------------------------------------------------ helpers

    def _mention(self, station: str | None) -> None:
        if station:
            if station in self.stations:
                self.stations.remove(station)
            self.stations.append(station)

    def _note_call(self, call: ToolCall) -> None:
        self.last_query = f"{call.name}({_fmt_args(call.arguments)})"
        trail = call.arguments.get("trail_id")
        if trail:
            self.last_trail = trail
            self._mention(self.world.trails[trail].station)
        self._mention(call.arguments.get("station"))

    def _summary(self, state: str, extra: str | None = None) -> str:
        lines = [f"Estado: {state}"]
        if self.flow:
            lines.append(f"Trámite en curso: {self.flow.tool}")
            lines.append(f"Datos recibidos: {_fmt_args(self.flow.slots) or 'ninguno'}")
            if self.flow.pending:
                lines.append(f"Dato pendiente: {self.flow.pending}")
            else:
                lines.append("Dato pendiente: ninguno (esperando confirmación del usuario)")
        else:
            lines.append("Trámite en curso: ninguno")
        if self.memory:
            reason, tool, slots = self.memory
            lines.append(f"Trámite {reason}: {tool} ({_fmt_args(slots) or 'sin datos'})")
        lines.append(f"Última consulta: {self.last_query or 'ninguna'}")
        lines.append(f"Estaciones mencionadas: {', '.join(self.stations) or 'ninguna'}")
        lines.append(f"Último sendero mencionado: {self.last_trail or 'ninguno'}")
        if extra:
            lines.append(extra)
        return "\n".join(lines)

    def _step(
        self,
        call_type: str,
        fsm_state: str,
        message: str,
        gold: Gold,
        path: list[str],
        phenomenon: str,
        *,
        safety: bool,
        tool_names: list[str] | None = None,
        passage_ids: list[str] | None = None,
        slot_name: str | None = None,
        summary_extra: str | None = None,
    ) -> Case:
        S.check_path(path)
        gold.next_state = path[1]
        index = sum(1 for s in self.steps if s.tags["turn_index"] == self.turn_index)
        pending = self.flow is not None or any(
            self.world.tools[c.name].has_side_effects for c in gold.calls
        )
        case = Case(
            case_id=f"dlg-{self.dialogue_id}-t{self.turn_index:02d}-s{index}",
            suite=SUITE,
            call_type=call_type,  # type: ignore[arg-type]
            fsm_state=fsm_state,
            user_message=message,
            history=[dict(m) for m in self.history],
            state_summary=self._summary(fsm_state, summary_extra),
            tool_names=list(tool_names or []),
            passage_ids=list(passage_ids or []),
            slot_name=slot_name,
            gold=gold,
            tags={
                "dialogue_id": f"dlg-{self.dialogue_id}",
                "turn_index": self.turn_index,
                "step_index": index,
                "depth": self.depth,
                "phenomenon": phenomenon,
                "history_turns": self.turn_index,
                "safety": safety,
                "side_effect_pending": pending,
                "gold_path": list(path),
            },
        )
        self.steps.append(case)
        return case

    def _route_tools(self) -> list[str]:
        return S.visible_tools(self.world, S.ROUTER)

    def _route(
        self, origin: str, message: str, call: ToolCall, path: list[str], phen: str,
        tool_names: list[str],
    ) -> None:  # fmt: skip
        missing = (
            self.world.missing_required(call.name, call.arguments)
            if call.name in S.FLOW_STATE
            else []
        )
        gold = Gold(decision="call", calls=[call], missing_required=missing)
        self._step(
            "route", origin, message, gold, path, phen,
            safety=self.world.tools[call.name].safety or call.name == RE,
            tool_names=tool_names,
        )  # fmt: skip

    def _extract_null(self, message: str, phen: str) -> None:
        assert self.flow is not None and self.flow.pending is not None
        gold = Gold(slot_name=self.flow.pending, slot_value=None)
        self._step(
            "extract", S.SLOT_FILLING, message, gold, [S.SLOT_FILLING, S.SLOT_FILLING], phen,
            safety=self.flow.tool == RE, slot_name=self.flow.pending,
        )  # fmt: skip

    def _advance(self) -> tuple[str, str]:
        """Driver's _advance_flow: next state and assistant message."""
        assert self.flow is not None
        missing = next(
            (s for s in S.REQUIRED_SLOTS[self.flow.tool] if s not in self.flow.slots), None
        )
        self.flow.pending = missing
        if missing:
            return S.SLOT_FILLING, S.SLOT_QUESTIONS[missing]
        details = ", ".join(f"{S.SLOT_LABELS.get(k, k)}: {v}" for k, v in self.flow.slots.items())
        label = S.TOOL_LABELS.get(self.flow.tool, self.flow.tool)
        return S.CONFIRM, (
            f"Voy a enviar {label} con estos datos: {details}. ¿Confirmas? Responde sí o no."
        )

    def _merge(self, args: dict[str, Any]) -> None:
        assert self.flow is not None
        for name, value in args.items():
            errors = self.world.validate_value(name, value)
            if errors:
                raise ValueError(f"dlg-{self.dialogue_id}: invalid {name}={value!r}: {errors}")
            self.flow.slots[name] = value

    def _answer(self, turn: Ask, call: ToolCall, phen: str) -> str:
        result = self.world.execute_tool(call)
        if not result["ok"]:
            raise ValueError(f"dlg-{self.dialogue_id}: tool failed: {result['error']}")
        pids = list(result["passage_ids"])
        gold_pids: list[str] = []
        for value in turn.values:
            pid = next((p for p in pids if value in self.world.passages[p].values), None)
            if pid is None:
                raise ValueError(f"dlg-{self.dialogue_id}: {value!r} not in {call.name} result")
            if pid not in gold_pids:
                gold_pids.append(pid)
        topic = S.tool_topic(self.world, call.name)
        data = result.get("data") or {}
        extra = f"Resultado de la herramienta: {_fmt_args(data)}" if data else None
        gold = Gold(answerable=True, gold_values=list(turn.values), gold_passage_id=gold_pids[0])
        safety = self.world.tools[call.name].safety or any(
            self.world.passages[p].safety for p in gold_pids
        )
        self._step(
            "answer", topic, turn.message, gold, [topic, S.ANSWER], phen,
            safety=safety, passage_ids=pids, summary_extra=extra,
        )  # fmt: skip
        self.state = S.ANSWER
        return " ".join(f"{self.world.passages[p].text} [fuente: {p}]" for p in gold_pids)

    # ------------------------------------------------------------------ turns

    def ask(self, turn: Ask) -> str:
        call = ToolCall(name=turn.tool, arguments=dict(turn.args))
        if self.world.validate_arguments(call.name, call.arguments):
            raise ValueError(f"dlg-{self.dialogue_id}: invalid call {call}")
        topic = S.tool_topic(self.world, call.name)
        if self.state == S.SLOT_FILLING:
            assert self.flow is not None
            phen = turn.phenomenon or "intent_switch"
            self._extract_null(turn.message, phen)
            self._route(
                S.SLOT_FILLING, turn.message, call, [S.SLOT_FILLING, S.ROUTER, topic], phen,
                self._route_tools(),
            )  # fmt: skip
            self.memory = ("interrumpido", self.flow.tool, dict(self.flow.slots))
            self.flow = None
        elif self.state == S.CONFIRM:
            raise ValueError(f"dlg-{self.dialogue_id}: info question during CONFIRM")
        else:
            phen = turn.phenomenon or "info_chain"
            self._route(S.ROUTER, turn.message, call, [S.ROUTER, topic], phen, self._route_tools())
        for station in turn.mentions:
            self._mention(station)
        self._note_call(call)
        return self._answer(turn, call, phen)

    def start(self, turn: Start) -> str:
        if self.state in (S.SLOT_FILLING, S.CONFIRM):
            raise ValueError(f"dlg-{self.dialogue_id}: flow start inside a flow")
        call = ToolCall(name=turn.tool, arguments=dict(turn.args))
        flow = _Flow(tool=turn.tool)
        self.flow = flow
        self._merge(turn.args)
        nxt, reply = self._advance()
        path = [S.ROUTER, S.FLOW_STATE[turn.tool], S.SLOT_FILLING]
        if nxt == S.CONFIRM:
            path.append(S.CONFIRM)
        # Steps see the state before the call: no flow yet.
        self.flow = None
        self._route(S.ROUTER, turn.message, call, path, turn.phenomenon, self._route_tools())
        self.flow = flow
        self.memory = None
        self._note_call(call)
        self.state = nxt
        return reply

    def fill(self, turn: Fill) -> str:
        if self.state != S.SLOT_FILLING or self.flow is None or self.flow.pending is None:
            raise ValueError(f"dlg-{self.dialogue_id}: fill outside SLOT_FILLING")
        slot = self.flow.pending
        if self.world.validate_value(slot, turn.value):
            raise ValueError(f"dlg-{self.dialogue_id}: invalid {slot}={turn.value!r}")
        flow_before = _Flow(self.flow.tool, dict(self.flow.slots), self.flow.pending)
        self.flow.slots[slot] = turn.value
        nxt, reply = self._advance()
        flow_after, self.flow = self.flow, flow_before
        self._step(
            "extract", S.SLOT_FILLING, turn.message,
            Gold(slot_name=slot, slot_value=turn.value), [S.SLOT_FILLING, nxt],
            turn.phenomenon, safety=flow_after.tool == RE, slot_name=slot,
        )  # fmt: skip
        self.flow = flow_after
        self._mention(turn.value if slot == "station" else None)
        self.state = nxt
        return reply

    def correct(self, turn: Correct) -> str:
        if self.flow is None or self.state not in (S.SLOT_FILLING, S.CONFIRM):
            raise ValueError(f"dlg-{self.dialogue_id}: correction outside a flow")
        merged = dict(self.flow.slots)
        merged.update(turn.changes)
        call = ToolCall(name=self.flow.tool, arguments=merged)
        if self.state == S.SLOT_FILLING:
            self._extract_null(turn.message, turn.phenomenon)
            tools = self._route_tools()
        else:
            tools = [self.flow.tool]
        origin = self.state
        snapshot = _Flow(self.flow.tool, dict(self.flow.slots), self.flow.pending)
        self._merge(turn.changes)
        nxt, reply = self._advance()
        path = [origin, S.SLOT_FILLING, nxt] if origin == S.CONFIRM else [origin, nxt]
        after, self.flow = self.flow, snapshot
        self._route(origin, turn.message, call, path, turn.phenomenon, tools)
        self.flow = after
        self._note_call(call)
        self.state = nxt
        return reply

    def confirm(self, turn: Confirm) -> str:
        if self.state != S.CONFIRM or self.flow is None:
            raise ValueError(f"dlg-{self.dialogue_id}: confirm outside CONFIRM")
        call = ToolCall(name=self.flow.tool, arguments=dict(self.flow.slots))
        result = self.world.execute_tool(call)
        if not result["ok"]:
            raise ValueError(f"dlg-{self.dialogue_id}: execution failed: {result['error']}")
        code = result["data"].get("codigo_registro") or result["data"].get("codigo_reporte")
        self.executions.append(call)
        reply = f"Listo, quedó enviado {S.TOOL_LABELS[self.flow.tool]}. Código: {code}."
        self.flow = None
        self.memory = None
        self.state = S.ANSWER
        return reply

    def cancel(self, turn: Cancel) -> str:
        if self.flow is None or self.state not in (S.SLOT_FILLING, S.CONFIRM):
            raise ValueError(f"dlg-{self.dialogue_id}: cancel outside a flow")
        reply = CANCEL_FILLING_REPLY if self.state == S.SLOT_FILLING else CANCEL_CONFIRM_REPLY
        self.memory = ("cancelado", self.flow.tool, dict(self.flow.slots))
        self.flow = None
        self.state = S.ROUTER
        return reply

    def run(self) -> Trace:
        handlers = {
            Ask: self.ask, Start: self.start, Fill: self.fill, Correct: self.correct,
            Confirm: self.confirm, Cancel: self.cancel,
        }  # fmt: skip
        turns: list[DialogueTurn] = []
        replies: list[str] = []
        phenomena: set[str] = set()
        turn_states: list[str] = []
        for index, turn in enumerate(self.script):
            self.turn_index = index
            turn_states.append(self.state)
            first = len(self.steps)
            reply = handlers[type(turn)](turn)  # type: ignore[operator]
            steps = self.steps[first:]
            phenomena |= {s.tags["phenomenon"] for s in steps} | {turn.phenomenon or ""}
            turns.append(DialogueTurn(user_message=turn.message, steps=steps))
            replies.append(reply)
            self.history.append({"role": "user", "content": turn.message})
            self.history.append({"role": "assistant", "content": reply})
        phenomena.discard("")
        dialogue = Dialogue(
            dialogue_id=f"dlg-{self.dialogue_id}",
            depth=self.depth,
            phenomena=sorted(phenomena),
            turns=turns,
            # Derived from the gold simulation (independent of fsm.driver); the test suite
            # replays every dialogue through the driver and asserts it executes exactly these.
            expected_executions=[c.model_copy(deep=True) for c in self.executions],
        )
        return Trace(dialogue, replies, list(self.executions), self.state, turn_states)


def simulate(world: World) -> list[Trace]:
    """Gold traces for every script (used by tests to check parity with the driver)."""
    return [_Sim(world, f"{n:02d}", script).run() for n, script in enumerate(SCRIPTS, 1)]


def generate_dialogues(world: World) -> list[Dialogue]:
    """36 scripted dialogues with teacher-forced step cases (suite ``dialogues``)."""
    return [trace.dialogue for trace in simulate(world)]
