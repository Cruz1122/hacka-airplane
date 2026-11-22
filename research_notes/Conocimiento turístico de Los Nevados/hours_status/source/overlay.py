"""Round 2 overlay for section `hours_status`."""

from __future__ import annotations

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
RES_207_URL = "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf"
RES_1815_URL = "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf"
PNN_ATENCION_URL = "https://www.parquesnacionales.gov.co/atencion-al-ciudadano/"

SRC_PNN = {
    "label": "Parques Nacionales Naturales de Colombia · PNN Los Nevados",
    "url": PNN_URL,
    "retrieved_at": "2026-11-21",
}
SRC_RES_207 = {
    "label": "Parques Nacionales Naturales de Colombia · Resolución 207 de 2023 (Reglamentación transitoria PNN Los Nevados)",
    "url": RES_207_URL,
    "retrieved_at": "2026-11-21",
}
SRC_RES_1815 = {
    "label": "Ministerio de Transporte · Resolución 1815 del 24 de julio de 2026 (Pico y Placa Ambiental Murillo–Cerro Gualí)",
    "url": RES_1815_URL,
    "retrieved_at": "2026-11-21",
}
SRC_ATENCION = {
    "label": "Parques Nacionales Naturales de Colombia · Canales de Atención",
    "url": PNN_ATENCION_URL,
    "retrieved_at": "2026-11-21",
}


def apply(section: dict) -> dict:
    by_id = {e["id"]: e for e in section["entries"]}

    # 1. Remove unsupported (#767) phone number from road_closure_status and ground in Res. 1815/2026 + PNN
    if "hours_status.road_closure_status" in by_id:
        e = by_id["hours_status.road_closure_status"]
        e["answer"]["short"] = (
            "Las vías hacia Los Nevados, como la carretera Manizales–Murillo o los accesos rurales a Potosí y Juntas, "
            "pueden tener cierres o pasos restringidos por derrumbes, clima o mantenimiento. Antes de salir, consulta el "
            "estado vial con Invías, la Policía Nacional de Tránsito o Parques Nacionales."
        )
        e["answer"]["variants"] = [
            "El tránsito hacia las entradas del parque puede verse afectado por deslizamientos o reparaciones en carreteras de montaña. "
            "Antes de iniciar el recorrido, verifica el estado de las vías con Invías, la Secretaría de Tránsito del Tolima o Parques Nacionales."
        ]
        e["answer"]["steps"] = [
            [
                "Consulta el estado del corredor vial con Invías, la Policía Nacional de Tránsito o la Secretaría de Tránsito y Transporte del Tolima.",
                "Pregunta a tu operador autorizado o a Parques Nacionales sobre el estado de los carreteables rurales de acceso.",
            ]
        ]
        e["sources"] = [SRC_PNN, SRC_RES_1815]

    # 2. Remove homepage URL https://www.operacionnevados.co/ from uton_concession_office_hours (backed by pnn_nevados.txt)
    if "hours_status.uton_concession_office_hours" in by_id:
        e = by_id["hours_status.uton_concession_office_hours"]
        e["sources"] = [SRC_PNN]

    # 3. Document the schedule conflict/update between Res. 207 de 2023 (Juntas 6-10 a.m.) and PNN web page (Juntas/Anzoátegui 6-11 a.m.)
    if "hours_status.quindio_dulima_juntas_anzoategui_hours" in by_id:
        e = by_id["hours_status.quindio_dulima_juntas_anzoategui_hours"]
        e["answer"]["detail"] = (
            "En la ficha web vigente de Parques Nacionales el horario de registro para Juntas y Anzoátegui figura de 6:00 a. m. a 11:00 a. m. "
            "(bajo reserva previa), mientras que la Resolución 207 de 2023 fijaba Juntas de 6:00 a. m. a 10:00 a. m. y Anzoátegui de 6:00 a. m. a 11:00 a. m."
        )
        e["sources"] = [SRC_PNN, SRC_RES_207]

    # 4. Ground pico_y_placa_hours_murillo with direct PDF source of Resolución 1815 de 2026
    if "hours_status.pico_y_placa_hours_murillo" in by_id:
        e = by_id["hours_status.pico_y_placa_hours_murillo"]
        e["answer"]["detail"] = (
            "Según la Resolución 1815 del 24 de julio de 2026, la medida rige del 25 de julio de 2026 al 20 de julio de 2027 "
            "los sábados, domingos y festivos de 5:00 a. m. a 4:00 p. m. entre Murillo (PR43+500) y Cerro Gualí (PR0+000) para "
            "automóviles, camperos, camionetas y motocicletas."
        )
        e["sources"] = [SRC_PNN, SRC_RES_1815]

    # 5. Add Res. 207 de 2023 source to entries directly supported by it
    for eid in [
        "hours_status.general_opening_schedule",
        "hours_status.cisne_potan_hours",
        "hours_status.santa_isabel_conejeras_prior_day_checkin",
        "hours_status.santa_isabel_summit_start_hour",
        "hours_status.otun_sector_hours",
        "hours_status.cedral_otun_hiking_schedule",
        "hours_status.quindio_dulima_cocora_hours",
        "hours_status.tolima_summit_push_hours",
        "hours_status.night_entry_prohibition",
        "hours_status.camping_arrival_cutoff",
        "hours_status.late_arrival_policy",
        "hours_status.volcanic_alert_closures",
        "hours_status.weather_emergency_closures",
        "hours_status.reopening_protocol_after_emergencies",
        "hours_status.unplanned_midday_closures",
        "hours_status.trail_maintenance_temporary_closures",
    ]:
        if eid in by_id:
            urls = {s["url"] for s in by_id[eid]["sources"]}
            if RES_207_URL not in urls:
                by_id[eid]["sources"].append(SRC_RES_207)

    # 6. Append 2 well-sourced entries from Resolución 207 de 2023 to reach target 40
    new_entries = [
        {
            "id": "hours_status.asomadera_potosi_entry_hours",
            "label": "horario de ingreso hacia La Asomadera",
            "kind": "fact",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "horario potosí la asomadera",
                "a qué hora dejan entrar hacia la asomadera",
                "hasta qué hora puedo subir a la asomadera desde potosí",
                "¿Cuál es el horario de ingreso para el recorrido Potosí - La Asomadera?",
                "horario caminata a la asomadera sin equipamiento",
                "a q hora cierran el paso de potosi a la asomadera",
                "puedo entrar a la 1 pm para ir solo a la asomadera?",
                "horario límite en potosí para pasadía a la asomadera",
                "hasta las 2 pm dejan subir a la asomadera sin equipo?",
                "a qué hora abren el sendero potosí la asomadera porfa",
                "what are the entry hours for the Potosi to La Asomadera trail?",
                "schedule for hiking to La Asomadera from Potosi",
            ],
            "hard_negatives": [
                "puedo ir y volver a la Asomadera",
                "horario cabaña potosí",
                "horario laguna del otún",
            ],
            "entities": {
                "sector": ["otun"]
            },
            "needs": [],
            "answer": {
                "short": (
                    "Según la Resolución 207 de 2023, el ingreso para el recorrido Potosí–La Asomadera es de 7:30 a. m. a 12:00 m., "
                    "y para caminatas a La Asomadera sin equipamiento se amplía hasta las 2:00 p. m. El horario puede cambiar por "
                    "clima o alertas; confirma con Parques Nacionales antes de viajar."
                ),
                "variants": [
                    "Para el tramo Potosí–La Asomadera, la Resolución 207 de 2023 fija ingreso de 7:30 a. m. a 12:00 m., ampliado "
                    "hasta las 2:00 p. m. en caminatas sin equipamiento. Verifica con Parques Nacionales que el sendero esté abierto antes de subir."
                ],
                "steps": [
                    [
                        "Regístrate en el puesto de control de Cabaña Potosí desde las 7:30 a. m. hasta las 12:00 m.",
                        "Si realizas solo la caminata a La Asomadera sin equipamiento de acampada, el ingreso se permite hasta las 2:00 p. m.",
                    ]
                ],
                "detail": (
                    "La ampliación hasta las 2:00 p. m. aplica exclusivamente para caminatas de pasadía hasta el mirador de La Asomadera "
                    "sin equipamiento de pernocta."
                ),
                "reflection": None,
            },
            "sources": [SRC_RES_207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": [
                "hours_status.otun_sector_hours",
                "hours_status.cisne_potan_hours",
                "activities.asomadera_day",
            ],
            "tags": [
                "horario",
                "asomadera",
                "potosí",
                "pasadía",
                "otún",
            ],
        },
        {
            "id": "hours_status.anzoategui_pit_la_punta_hours",
            "label": "horario de atención en PIT Anzoátegui",
            "kind": "fact",
            "audience": "visitor",
            "lang": "es",
            "examples": [
                "horario pit anzoátegui",
                "qué días atiende el punto de información turística de anzoátegui",
                "horario del punto de control flotante la punta en anzoátegui",
                "¿Qué días y en qué horario funciona el PIT de Anzoátegui y el control de La Punta?",
                "a q hora abren el punto de informacion de anzoategui en el centro",
                "los lunes atiende el pit de anzoategui?",
                "horario jueves a sábado control la punta vereda la cascada",
                "a qué hora atienden en la calle 13 de anzoátegui parques nacionales",
                "dias de atencion en la punta anzoategui tolima porfa",
                "horario de oficina o pit de parques en el casco urbano de anzoátegui",
                "what are the opening days and hours for the Anzoategui PIT and La Punta checkpoint?",
                "operating hours of La Punta floating control point in Anzoategui",
            ],
            "hard_negatives": [
                "horario puesto de control anzoátegui",
                "¿La Punta es el control que queda en Anzoátegui?",
                "horario de atención oficinas parques nacionales",
            ],
            "entities": {
                "sector": ["quindio_dulima"]
            },
            "needs": [],
            "answer": {
                "short": (
                    "Según la Resolución 207 de 2023, en Anzoátegui el Punto de Información Turística (PIT, Calle 13 entre Carreras 2 y 3) "
                    "atiende de martes a sábado de 8:00 a. m. a 5:00 p. m., y el control flotante La Punta (vereda La Cascada) de jueves a "
                    "sábado de 8:00 a. m. a 5:00 p. m. Confirma con Parques Nacionales: el ingreso al sendero es de 6:00 a 11:00 a. m."
                ),
                "variants": [
                    "En Anzoátegui (Tolima), la Resolución 207 de 2023 fija atención en el PIT del barrio Centro de martes a sábado "
                    "(8:00 a. m. a 5:00 p. m.) y en el punto flotante La Punta de jueves a sábado (8:00 a. m. a 5:00 p. m.), mientras "
                    "que la franja de ingreso al parque es de 6:00 a. m. a 11:00 a. m. Verifica con Parques Nacionales antes de ir."
                ],
                "steps": [
                    [
                        "Punto de Información Turística (PIT) en el casco urbano de Anzoátegui (Calle 13 entre Carrera 2 y 3): martes a sábado de 8:00 a. m. a 5:00 p. m.",
                        "Punto de control flotante La Punta (vereda La Cascada): jueves a sábado de 8:00 a. m. a 5:00 p. m.",
                        "Horario de ingreso de visitantes con reserva previa por Anzoátegui: 6:00 a. m. a 11:00 a. m.",
                    ]
                ],
                "detail": (
                    "La Resolución 207 de 2023 distingue el horario de atención de los puntos de información y control flotante (8:00 a. m. a 5:00 p. m.) "
                    "de la ventana matutina de ingreso a los senderos del sector Cuencas Quindío y Dulima (6:00 a. m. a 11:00 a. m.)."
                ),
                "reflection": None,
            },
            "sources": [SRC_RES_207, SRC_PNN],
            "last_verified": "2026-11-21",
            "valid_until": None,
            "related": [
                "hours_status.quindio_dulima_juntas_anzoategui_hours",
                "access.la_punta_control",
                "hours_status.pnn_administrative_office_hours",
            ],
            "tags": [
                "horario",
                "anzoátegui",
                "pit",
                "la punta",
                "tolima",
            ],
        },
    ]

    for ne in new_entries:
        if ne["id"] not in by_id:
            section["entries"].append(ne)
        else:
            idx = next(i for i, x in enumerate(section["entries"]) if x["id"] == ne["id"])
            section["entries"][idx] = ne

    # Email typo from round 1: no downloaded source has "losnevados@"; Res. 207/2023 gives nevados@.
    e = by_id.get("hours_status.official_channels_to_check_status")
    if e:
        fix = lambda s: s.replace("losnevados@parquesnacionales.gov.co", "nevados@parquesnacionales.gov.co")
        e["answer"]["short"] = fix(e["answer"]["short"])
        e["answer"]["variants"] = [fix(v) for v in e["answer"].get("variants", [])]

    return section
