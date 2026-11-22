#!/usr/bin/env python3
"""
Applies all corrections to hours_status.json after quality coordinator review.
Complies strictly with input contract, schema, and evidence rules.
"""

import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SECTION_PATH = Path("/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/hours_status.json")
SCHEMA_PATH = Path("/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json")

SRC_PNN = {
    "label": "Parques Nacionales Naturales de Colombia · PNN Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21",
}
SRC_PNN_ATENCION = {
    "label": "Parques Nacionales Naturales de Colombia · Canales de Atención",
    "url": "https://www.parquesnacionales.gov.co/atencion-al-ciudadano/",
    "retrieved_at": "2026-11-21",
}
SRC_SGC = {
    "label": "Servicio Geológico Colombiano · Monitoreo Volcánico y Boletines",
    "url": "https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx",
    "retrieved_at": "2026-11-21",
}
SRC_UTON = {
    "label": "Concesión Unión Temporal Operación Nevados (UTON)",
    "url": "https://www.operacionnevados.co/",
    "retrieved_at": "2026-11-21",
}

CORRECTIONS = {
    "hours_status.general_opening_schedule": {
        "label": "horarios generales de ingreso al parque",
        "answer": {
            "short": "El horario de ingreso en Brisas es de 8:00 a. m. a 2:00 p. m. (última charla 1:30 p. m.). En Cisne–Potosí el registro es de 7:30 a. m. a 10:00 a. m., en Otún de 7:00 a. m. a 12:00 m., y en Cocora de 6:00 a. m. a 10:00 a. m. Los horarios pueden variar por clima o alertas; confirma siempre con Parques Nacionales antes de viajar.",
            "variants": [
                "Cada sector maneja sus propios horarios: Brisas atiende de 8:00 a. m. a 2:00 p. m., Potosí de 7:30 a 10:00 a. m. (o hasta mediodía para Otún), y Cocora de 6:00 a 10:00 a. m. Consulta con Parques Nacionales el estado y posibles variaciones antes de salir."
            ],
            "steps": [
                [
                    "Sector Brisas–Kumanday: ingreso de 8:00 a. m. a 2:00 p. m., con última inducción a la 1:30 p. m.",
                    "Sector Cisne–Poleka Kasue: registro en Cabaña Potosí y Alto de Santa Bárbara de 7:30 a. m. a 10:00 a. m."
                ],
                [
                    "Sector Otún: registro en Cabaña Potosí de 7:00 a. m. a 12:00 m.",
                    "Sector Quindío–Dulima: punto Cocora de 6:00 a. m. a 10:00 a. m., y Juntas/Anzoátegui de 6:00 a. m. a 11:00 a. m."
                ]
            ],
            "detail": "Los horarios corresponden a las franjas de registro diurno fijadas en la reglamentación oficial. Fuera de esos horarios los puestos de control cierran el acceso al público.",
            "reflection": "Planear tu llegada temprano te permite cumplir con la inducción y disfrutar el recorrido con luz natural."
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.park_open_today": {
        "label": "verificar si el parque está abierto hoy",
        "answer": {
            "short": "La apertura del parque se debe confirmar directamente con Parques Nacionales para la fecha y sector que visites, ya que este asistente funciona sin conexión a internet. El acceso puede suspenderse de forma preventiva por alertas volcánicas del Ruiz, lluvias intensas o descansos ambientales.",
            "variants": [
                "Para saber si el parque está abierto hoy, consulta los canales oficiales de Parques Nacionales antes de salir hacia la montaña. Esta aplicación offline no actualiza en vivo y el estado puede cambiar por clima, conservación o alertas del volcán."
            ],
            "steps": [
                [
                    "Consulta el portal www.parquesnacionales.gov.co o las redes @ParquesColombia mientras tengas señal en la ciudad.",
                    "Confirma con tu operador o guía registrado que el sector que vas a visitar se encuentre habilitado."
                ]
            ],
            "detail": "En la alta montaña la señal celular es inexistente en la mayoría de los tramos, por lo que debes verificar antes de ascender.",
            "reflection": None
        },
        "sources": [SRC_PNN, SRC_SGC],
        "last_verified": "2026-11-21"
    },
    "hours_status.conservation_closures": {
        "label": "cierres programados por conservación y descanso",
        "answer": {
            "short": "El parque programa tres cierres al año de cinco días cada uno para permitir la recuperación de los ecosistemas y monitoreo ambiental: la semana posterior a Semana Santa, la cuarta semana de septiembre y la cuarta semana de noviembre. Confirma las fechas exactas con Parques Nacionales antes de viajar.",
            "variants": [
                "Por conservación y descanso ambiental, Los Nevados cierra cinco días tres veces al año (tras Semana Santa, a finales de septiembre y a finales de noviembre). Consulta los comunicados oficiales de Parques Nacionales para verificar si tu viaje coincide con alguna de estas pausas."
            ],
            "steps": [
                [
                    "Primer descanso ambiental: semana siguiente a Semana Santa (lunes a viernes).",
                    "Segundo descanso ambiental: cuarta semana de septiembre (lunes a viernes).",
                    "Tercer descanso ambiental: cuarta semana de noviembre (lunes a viernes)."
                ]
            ],
            "detail": "Durante estos periodos se restringe el acceso a senderos de montaña para disminuir la presión turística y adelantar labores técnicas de conservación.",
            "reflection": "Respetar estos descansos ayuda a que el páramo y sus fuentes de agua se conserven para el futuro."
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.brisas_hours": {
        "label": "horario de ingreso del sector Brisas",
        "answer": {
            "short": "El horario de taquilla e ingreso por el sector Brisas–Kumanday es de 8:00 a. m. a 2:00 p. m., con la última charla obligatoria de inducción a la 1:30 p. m. Este horario puede variar por alertas del volcán o condiciones climáticas; confirma la apertura con Parques Nacionales antes de viajar.",
            "variants": [
                "Para visitar Brisas y el Valle de las Tumbas, el ingreso está habilitado entre las 8:00 a. m. y las 2:00 p. m., debiendo tomar la inducción antes de la 1:30 p. m. Consulta con Parques Nacionales el estado del acceso antes de salir hacia la cordillera."
            ],
            "steps": [
                [
                    "Llega al centro de visitantes Brisas dentro de la franja de 8:00 a. m. a 2:00 p. m.",
                    "Toma la charla de inducción obligatoria a más tardar a la 1:30 p. m."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.brisas_induction_talk_schedule": {
        "label": "horario de la última charla obligatoria",
        "answer": {
            "short": "La última charla de inducción obligatoria en el centro de visitantes Brisas se realiza a la 1:30 p. m. Si llegas después de esa hora no se permite iniciar el recorrido hacia el atractivo, aunque la taquilla cierre a las 2:00 p. m. Confirma horarios y estado con Parques Nacionales antes de partir.",
            "variants": [
                "Para entrar por Brisas debes participar en la inducción antes de la 1:30 p. m., hora fijada por Parques Nacionales para la última sesión del día. Te recomendamos madrugar y verificar el estado del sector en los canales oficiales antes de tu viaje."
            ],
            "steps": [
                [
                    "Las charlas de inducción se realizan de manera continua en la mañana para los grupos que van llegando.",
                    "A la 1:30 p. m. inicia la última sesión programada del día."
                ]
            ],
            "detail": None,
            "reflection": "La charla de inducción te entrega pautas esenciales para cuidar tu salud en alta montaña."
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.brisas_exit_time": {
        "label": "hora de salida del sector Brisas",
        "answer": {
            "short": "Parques Nacionales no fija en su reglamentación una hora numérica de salida para Brisas, pero el ingreso concluye a las 2:00 p. m. y el recorrido concluye por la tarde para salir del parque con luz diurna. Debes seguir las indicaciones de tu guía autorizado y consultar horarios operativos con Parques.",
            "variants": [
                "Las actividades en Brisas se desarrollan durante el día para evacuar el circuito antes del anochecer bajo la coordinación del guía acompañante. Consulta con Parques Nacionales o con el operador los tiempos de retorno previstos para tu fecha de visita."
            ],
            "steps": [
                [
                    "El ingreso al sector finaliza a las 2:00 p. m. en el centro de visitantes.",
                    "El recorrido guiado por el carreteable concluye en la tarde para descender antes de la caída del sol."
                ]
            ],
            "detail": "En la alta montaña las temperaturas caen bruscamente al atardecer y la niebla reduce la visibilidad vial, por lo que no se permite la permanencia nocturna en el circuito.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.brisas_open_days": {
        "label": "días de apertura del sector Brisas",
        "answer": {
            "short": "Parques Nacionales señala que el sector Brisas opera habitualmente todos los días del año de 8:00 a. m. a 2:00 p. m., pero el acceso está sujeto a cambios por alertas volcánicas, mal tiempo, mantenimiento vial o cierres por conservación. Verifica siempre el estado del día con Parques Nacionales antes de viajar.",
            "variants": [
                "Aunque el sector Brisas atiende regularmente de lunes a domingo incluyendo festivos, el servicio puede suspenderse por actividad del volcán Ruiz, lluvias torrenciales o medidas ambientales. Confirma siempre con Parques Nacionales que el acceso esté abierto antes de subir."
            ],
            "steps": [
                [
                    "El sector programa atención habitual de lunes a domingo, incluyendo días festivos.",
                    "Consulta los canales oficiales antes de tu viaje para confirmar que no existan cierres temporales vigentes."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.cisne_potan_hours": {
        "label": "horario de registro en cabaña Potosí",
        "answer": {
            "short": "En el sector Cisne–Poleka Kasue, los puestos de control de Cabaña Potosí y Alto de Santa Bárbara atienden registro de 7:30 a. m. a 10:00 a. m. Debes presentarte dentro de esa franja con reserva previa y guía autorizado, confirmando siempre posibles variaciones con Parques Nacionales.",
            "variants": [
                "El registro para ingresar hacia los atractivos del sector Cisne opera entre las 7:30 a. m. y las 10:00 a. m. en Potosí y Alto de Santa Bárbara. Recuerda verificar con Parques Nacionales el estado de las vías y la apertura antes de desplazarte."
            ],
            "steps": [
                [
                    "Llega al puesto de control entre las 7:30 a. m. y las 10:00 a. m.",
                    "Presenta tu soporte de reserva, póliza de accidentes y documento de identidad."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.laguna_verde_trail_hours": {
        "label": "horario de ingreso al sendero Laguna Verde",
        "answer": {
            "short": "El sendero hacia la Laguna Verde, en el sector Cisne, tiene un horario oficial de 8:00 a. m. a 2:00 p. m. Es obligatorio ingresar con guía autorizado y reserva confirmada. Consulta con Parques Nacionales antes de tu visita para confirmar que el sendero se encuentre habilitado.",
            "variants": [
                "Para visitar la Laguna Verde el horario autorizado por Parques Nacionales es de 8:00 a. m. a 2:00 p. m. Como las condiciones del páramo pueden obligar a cierres preventivos, verifica el estado del sendero con la autoridad ambiental antes de salir."
            ],
            "steps": [
                [
                    "El ingreso al sendero Laguna Verde está permitido de 8:00 a. m. a 2:00 p. m.",
                    "Realiza la caminata siempre por la ruta señalizada y en compañía de tu guía."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.santa_isabel_conejeras_prior_day_checkin": {
        "label": "registro el día previo para Santa Isabel",
        "answer": {
            "short": "Para el sendero Conejeras hacia la cumbre o glaciar del Nevado Santa Isabel, Parques Nacionales exige realizar el registro y control el día anterior a la fecha programada para el ascenso. Confirma este trámite y los cupos disponibles con tu operador registrado y con Parques Nacionales antes de viajar.",
            "variants": [
                "Si vas al Santa Isabel por el sendero Conejeras, la normativa del parque exige pasar por los sitios de control el día previo al ingreso a la cima. Consulta con Parques Nacionales o tu agencia autorizada para coordinar este registro obligatorio a tiempo."
            ],
            "steps": [
                [
                    "Pasa por el sitio de control (Cabaña Potosí o Alto de Santa Bárbara) el día previo a la fecha de cumbre.",
                    "Presenta la autorización de ingreso, soporte de pago, seguro obligatorio y chequeo de equipo ante guardaparques."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.santa_isabel_summit_start_hour": {
        "label": "hora de inicio para subir a Santa Isabel",
        "answer": {
            "short": "Parques Nacionales no fija en su reglamento una hora oficial única de partida a la cumbre, pero exige registrarse el día previo e ingresar con guía autorizado. Las cordadas suelen iniciar el ascenso de madrugada según la coordinación de tu guía para aprovechar el clima y descender con seguridad. Confirma el itinerario con tu operador y con Parques.",
            "variants": [
                "El horario de inicio del ascenso a Santa Isabel lo define tu guía especializado en horas de la madrugada, considerando el estado del tiempo y las normas del parque. Recuerda que el registro ante guardaparques se hace obligatoriamente el día previo; consulta con Parques Nacionales antes de subir."
            ],
            "steps": [
                [
                    "Efectúa el control y verificación de equipo ante guardaparques el día anterior.",
                    "Inicia la aproximación en la madrugada bajo la dirección de tu guía de montaña."
                ]
            ],
            "detail": "Las salidas de madrugada buscan evitar la densa nubosidad y el riesgo de tormentas eléctricas que se presentan habitualmente después del mediodía en la alta montaña.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.otun_sector_hours": {
        "label": "horario de atencion para el sector Otun",
        "answer": {
            "short": "Para el sector de la Laguna del Otún, el horario oficial de atención en la cabaña Potosí es de 7:00 a. m. a 12:00 m. Debes realizar tu registro dentro de esta franja con reserva previa y guía autorizado, verificando posibles ajustes operativos con Parques Nacionales antes de desplazarte.",
            "variants": [
                "El punto de control de Cabaña Potosí para el sector Otún funciona de 7:00 a. m. a 12:00 m. Te recomendamos coordinar tu llegada dentro de esta franja matutina y confirmar el estado de apertura con Parques Nacionales o tu operador registrado."
            ],
            "steps": [
                [
                    "Preséntate en el puesto de registro de Cabaña Potosí entre las 7:00 a. m. y las 12:00 m.",
                    "Presenta la reserva y la póliza obligatoria tramitadas con tu operador autorizado."
                ]
            ],
            "detail": "La reglamentación de Parques Nacionales fija la franja de 7:00 a. m. a 12:00 m. en Potosí para el control de ingreso al sector Otún. El tiempo posterior de caminata varía según la ruta elegida y el clima.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.cedral_otun_hiking_schedule": {
        "label": "horario de caminata desde El Cedral",
        "answer": {
            "short": "Parques Nacionales indica que el recorrido a pie desde El Cedral hasta la Laguna del Otún tiene 18 km (7,5 km hasta el límite del parque). Aunque no hay un horario de taquilla fijado en El Cedral, debes iniciar la caminata muy temprano con tu guía para alcanzar los sitios autorizados antes de la noche. Confirma el estado de la ruta con Parques antes de partir.",
            "variants": [
                "Para ascender desde El Cedral hacia el Otún, los guías recomiendan partir en las primeras horas de la mañana debido a la distancia de 18 km por bosque y páramo. Consulta con Parques Nacionales y con tu operador el estado del sendero y las condiciones climáticas antes de iniciar."
            ],
            "steps": [
                [
                    "Inicia la travesía a pie a primera hora de la mañana con tu guía registrado.",
                    "Camina 7,5 km hasta el límite del parque y continúa hacia los puntos autorizados de pernocte."
                ]
            ],
            "detail": "Transitar de noche en el área protegida está prohibido por seguridad y conservación ambiental.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.quindio_dulima_cocora_hours": {
        "label": "horario de ingreso por Valle del Cocora",
        "answer": {
            "short": "En el sector Quindío–Dulima, el horario oficial en el punto de atención de Parques Nacionales en el Valle del Cocora es de 6:00 a. m. a 10:00 a. m. Debes ingresar con reserva previa tramitada con al menos cinco días hábiles de anticipación y guía registrado. Confirma siempre con Parques Nacionales antes de tu viaje.",
            "variants": [
                "El control de ingreso en el Valle del Cocora hacia el Nevado del Tolima opera de 6:00 a. m. a 10:00 a. m. Es obligatorio contar con reserva previa aprobada y guía de montaña. Verifica posibles cambios de horario con Parques Nacionales antes de salir."
            ],
            "steps": [
                [
                    "Preséntate en el puesto de registro de Cocora entre las 6:00 a. m. y las 10:00 a. m.",
                    "Acredita la reserva previa gestionada con al menos 5 días hábiles de antelación y tu póliza vigente."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.quindio_dulima_juntas_anzoategui_hours": {
        "label": "horarios de ingreso por Juntas y Anzoátegui",
        "answer": {
            "short": "Los puntos de registro de Parques Nacionales en Juntas (Ibagué) y Anzoátegui atienden de 6:00 a. m. a 11:00 a. m. bajo reserva previa obligatoria gestionada con al menos cinco días hábiles de antelación. Debes presentarte con tu guía autorizado y verificar el estado del acceso con Parques Nacionales antes de desplazarte.",
            "variants": [
                "Para entrar por Juntas o Anzoátegui hacia el sector del Tolima, el puesto de control atiende entre las 6:00 a. m. y las 11:00 a. m. con reserva confirmada y guía registrado. Confirma siempre las condiciones de la ruta con Parques Nacionales antes de viajar."
            ],
            "steps": [
                [
                    "Llega al punto de registro en Juntas o Anzoátegui dentro de la franja de 6:00 a. m. a 11:00 a. m.",
                    "Verifica con los guardaparques la reserva previa y las condiciones del sendero."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.tolima_summit_push_hours": {
        "label": "hora de ataque a cumbre Nevado Tolima",
        "answer": {
            "short": "Parques Nacionales no fija en su reglamento una hora oficial de ataque a la cumbre del Nevado del Tolima, sino los horarios de registro de ingreso en la base. Las cordadas suelen partir de madrugada desde campamentos autorizados según el plan de seguridad coordinado por su guía certificado. Confirma siempre las condiciones del sector con Parques Nacionales.",
            "variants": [
                "La hora de salida hacia el glaciar del Tolima la determina tu guía de alta montaña en horas de la madrugada, evaluando el clima y la seguridad del terreno. Recuerda que el ingreso al parque debe haberse registrado en los puntos de control oficiales matutinos; consulta con Parques antes de viajar."
            ],
            "steps": [
                [
                    "Regístrate en los horarios de control matutino en el acceso al parque.",
                    "Inicia la jornada de cumbre en la madrugada según las directrices de seguridad de tu guía."
                ]
            ],
            "detail": "Madrugar permite avanzar sobre terreno firme y emprender el descenso antes de las tormentas habituales de la tarde en la cumbre.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.night_entry_prohibition": {
        "label": "prohibición de ingreso nocturno al parque",
        "answer": {
            "short": "El ingreso nocturno al Parque Nacional Natural Los Nevados está prohibido en todos los sectores. Los puntos de control operan exclusivamente en franjas diurnas matutinas y no se autoriza el paso de personas fuera de esos horarios. Confirma los horarios habilitados con Parques Nacionales antes de emprender tu viaje.",
            "variants": [
                "Por normas de seguridad y protección ambiental, está prohibido ingresar al parque de noche o circular sin autorización fuera de los horarios oficiales de los puestos de control. Planifica tu itinerario de día y verifica siempre con Parques Nacionales."
            ],
            "steps": [
                [
                    "Ingresa únicamente en las franjas horarias diurnas autorizadas para cada sector.",
                    "No circules por senderos o carreteras del parque en horas de la noche."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.camping_arrival_cutoff": {
        "label": "hora de llegada a zonas de campamento",
        "answer": {
            "short": "Parques Nacionales no establece una hora reglamentaria fija de llegada al campamento ni protocolos de búsqueda automática a una hora determinada. Lo que exige la norma es ingresar con equipo en los horarios de registro matutinos (como 7:00 a. m. a 12:00 m. en Potosí), acampar solo en sitios autorizados (Termales Cañón, Arenales o Calvito) y llegar antes del anochecer con tu guía. Confirma siempre las condiciones con Parques.",
            "variants": [
                "En la reglamentación del parque no existe un horario límite oficial de llegada a carpas ni un protocolo que active búsquedas automáticas a una hora fija. Debes iniciar tu caminata temprano en los horarios autorizados y coordinar con tu guía para arribar con luz de día a las zonas de pernocte permitidas."
            ],
            "steps": [
                [
                    "Ingresa en los horarios oficiales matutinos de control con equipo de montaña permitido.",
                    "Pernocta únicamente en los sitios habilitados por la reglamentación transitoria o refugios autorizados.",
                    "Organiza el avance de la caminata con tu guía para llegar al campamento antes del anochecer."
                ]
            ],
            "detail": "La Resolución 207 de 2023 prohíbe el camping general en el área protegida, salvo en puntos transitorios autorizados bajo monitoreo. Está prohibido transitar de noche por senderos.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.late_arrival_policy": {
        "label": "política si llegas tarde a la entrada",
        "answer": {
            "short": "Si llegas a un puesto de control después del horario oficial de cierre de registro (por ejemplo, después de las 2:00 p. m. en Brisas o las 10:00 a. m. en Cocora y Cisne), no se te permitirá ingresar. Parques Nacionales aplica estos límites para garantizar la seguridad de los visitantes en la montaña. Verifica los horarios con Parques antes de salir.",
            "variants": [
                "Los horarios de los puestos de control son estrictos: si te presentas fuera de la franja fijada, los guardaparques no autorizarán el acceso, incluso si tienes reserva previa. Te recomendamos madrugar y consultar con Parques Nacionales el estado de las vías para evitar retrasos."
            ],
            "steps": [
                [
                    "Verifica con antelación la hora límite de registro del sector que elegiste.",
                    "Planea tu transporte con margen de tiempo ante posibles demoras en la carretera."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.weekend_and_holiday_opening": {
        "label": "horarios de atención en fines de semana",
        "answer": {
            "short": "Los fines de semana y festivos el parque atiende en sus horarios oficiales habituales (Brisas de 8:00 a. m. a 2:00 p. m. y sectores de montaña desde las 6:00 o 7:30 a. m.). Sin embargo, la afluencia es mayor y para Brisas se solicita reservar con antelación en reservasnevados.com. Confirma la disponibilidad y posibles cambios con Parques Nacionales.",
            "variants": [
                "Durante sábados, domingos y puentes festivos los horarios de ingreso se mantienen, pero los cupos diarios se agotan con rapidez y en la vía Murillo–La Esperanza aplica Pico y Placa Ambiental. Te sugerimos reservar con tiempo y consultar con Parques Nacionales antes de viajar."
            ],
            "steps": [
                [
                    "Reserva tu cupo con anticipación en reservasnevados.com si visitas Brisas en fin de semana.",
                    "Consulta si tu vehículo tiene restricción de Pico y Placa Ambiental en la vía Murillo–La Esperanza."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.weekday_opening": {
        "label": "visitar el parque entre semana días hábiles",
        "answer": {
            "short": "Entre semana (lunes a viernes) el parque opera en sus horarios regulares en los sectores habilitados: Brisas de 8:00 a. m. a 2:00 p. m. y puntos de montaña según su cronograma matutino. Visitar en días hábiles facilita conseguir cupos y evita el pico y placa de fin de semana. Confirma con Parques Nacionales antes de salir.",
            "variants": [
                "De lunes a viernes los accesos funcionan en su horario habitual, con menor flujo de visitantes y sin restricción de placas en la carretera Murillo–La Esperanza. Recuerda verificar con Parques Nacionales que no coincida con un cierre programado por conservación antes de tu visita."
            ],
            "steps": [
                [
                    "El parque opera de lunes a viernes en los horarios estándar de cada sector.",
                    "Verifica previamente que la fecha no corresponda a una de las tres semanas de cierre ambiental."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.pico_y_placa_hours_murillo": {
        "label": "horarios del pico y placa ambiental Murillo",
        "answer": {
            "short": "El Pico y Placa Ambiental en el corredor Murillo–La Esperanza rige los sábados, domingos y días festivos de 5:00 a. m. a 4:00 p. m., según la Resolución 1815 de 2026 de la Secretaría de Tránsito del Tolima. Esta medida busca ordenar el tráfico hacia el sector Brisas; verifica las placas autorizadas con la Gobernación del Tolima o Parques Nacionales antes de tu viaje.",
            "variants": [
                "En la vía Manizales–Murillo (sector tolimense de acceso a Brisas), la restricción ambiental de vehículos opera fines de semana y festivos de 5:00 a. m. a 4:00 p. m. Confirma el cronograma de placas y posibles cambios con Parques Nacionales o Tránsito del Tolima antes de desplazarte."
            ],
            "steps": [
                [
                    "Días de aplicación: sábados, domingos y festivos oficiales.",
                    "Horario de restricción: de 5:00 a. m. a 4:00 p. m.",
                    "Consulta el último dígito de placa autorizado antes de tomar la vía Murillo–La Esperanza."
                ]
            ],
            "detail": "Aplica a automóviles, camperos, camionetas y motocicletas en el corredor regulado. La medida busca proteger el ecosistema de páramo.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.high_season_calendar": {
        "label": "temporadas altas y afluencia en el parque",
        "answer": {
            "short": "Parques Nacionales no establece fechas fijas de inicio y fin para la temporada alta, pero el flujo de visitantes aumenta a fin de año, enero, Semana Santa, vacaciones de mitad de año y puentes festivos. Para Brisas se solicita reservar en reservasnevados.com para fines de semana y festivos, y se recomienda en periodos de alto tráfico como noviembre. Consulta la disponibilidad con Parques Nacionales.",
            "variants": [
                "El parque no maneja un calendario oficial cerrado de temporadas altas, aunque la mayor afluencia coincide con periodos vacacionales y festivos. Te aconsejamos asegurar tu cupo con antelación y consultar con Parques Nacionales o tu operador antes de viajar."
            ],
            "steps": [
                [
                    "En Brisas–Valle de las Tumbas, reserva con antelación en reservasnevados.com para fines de semana y festivos.",
                    "Para sectores de travesía (Cisne, Otún y Tolima), coordina tu cupo con la agencia u operador registrado con anticipación."
                ]
            ],
            "detail": "Durante épocas de alto turismo la capacidad de carga de los senderos se completa rápidamente, por lo que no es prudente viajar sin reserva confirmada.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.low_season_advantages": {
        "label": "visitar Los Nevados en temporada baja",
        "answer": {
            "short": "Visitar Los Nevados fuera de puentes y vacaciones escolares suele ofrecer senderos con menor congestión, mayor disponibilidad de cupos y atención más pausada. Sin embargo, debes verificar que tu viaje no coincida con los tres cierres anuales de cinco días por conservación. Confirma siempre el estado del parque con Parques Nacionales.",
            "variants": [
                "Los periodos regulares entre semana y fuera de temporadas de vacaciones son ideales para disfrutar de la montaña con tranquilidad y conseguir reservas fácilmente. Antes de viajar, asegúrate de consultar con Parques Nacionales el cronograma de cierres ambientales y el clima."
            ],
            "steps": [
                [
                    "Planifica tu visita en días hábiles fuera de semanas vacacionales para evitar aglomeraciones.",
                    "Revisa las fechas de los descansos de conservación (post-Semana Santa, septiembre y noviembre) para no encontrar accesos cerrados."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.high_season_operating_changes": {
        "label": "cambios de operación durante temporada alta",
        "answer": {
            "short": "En épocas de alta afluencia los horarios oficiales de ingreso no se amplían, pero los cupos diarios por capacidad de carga se agotan con rapidez. Te recomendamos gestionar tu reserva previa con suficiente anticipación y llegar temprano al puesto de control. Confirma los requisitos y el estado del sector con Parques Nacionales antes de viajar.",
            "variants": [
                "Durante temporadas de alto turismo los puestos de registro mantienen sus horarios habituales pero cierran el paso apenas se completa la capacidad permitida. Planifica tu visita con antelación y consulta siempre con Parques Nacionales antes de subir a la montaña."
            ],
            "steps": [
                [
                    "Reserva con tiempo en reservasnevados.com o a través de tu agencia autorizada.",
                    "Llega puntualmente en la primera franja de atención del puesto de registro correspondiente."
                ]
            ],
            "detail": "El aforo diario busca que no se supere la capacidad de carga fijada para la conservación de los senderos.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.volcanic_alert_closures": {
        "label": "cierres por alerta volcánica del Ruiz",
        "answer": {
            "short": "Si el Servicio Geológico Colombiano eleva la alerta del Nevado del Ruiz a nivel naranja o rojo, Parques Nacionales suspende el ingreso de visitantes de manera inmediata y preventiva en las zonas de amenaza volcánica o en todo el parque. En nivel amarillo el acceso a sectores autorizados permanece habilitado. Consulta el boletín del SGC y el estado con Parques Nacionales.",
            "variants": [
                "El parque activa cierres preventivos cuando la actividad del volcán Ruiz pasa a alerta naranja o roja. Si el volcán está en nivel amarillo, las visitas a los atractivos autorizados continúan bajo monitoreo continuo. Verifica siempre el estado del parque y los reportes oficiales antes de tu viaje."
            ],
            "steps": [
                [
                    "El SGC emite boletines técnicos periódicos sobre la actividad del volcán.",
                    "Parques Nacionales determina la suspensión de actividades si el nivel de alerta volcánica se eleva a naranja o rojo.",
                    "El ingreso se reactiva cuando la autoridad ambiental levanta formalmente la medida preventiva."
                ]
            ],
            "detail": "La articulación entre el SGC y Parques Nacionales busca proteger la vida ante posibles erupciones o emisiones graves de ceniza.",
            "reflection": None
        },
        "sources": [SRC_PNN, SRC_SGC],
        "last_verified": "2026-11-21"
    },
    "hours_status.weather_emergency_closures": {
        "label": "cierres por mal tiempo y lluvias",
        "answer": {
            "short": "Parques Nacionales puede suspender temporalmente el ingreso o evacuar senderos ante lluvias torrenciales, granizadas, tormentas eléctricas o derrumbes en las vías. Estas medidas preventivas se toman en el puesto de control para proteger la vida. Confirma el pronóstico y el estado de los sectores con Parques Nacionales antes de salir.",
            "variants": [
                "En caso de emergencias por mal tiempo extremo o riesgo de deslizamiento, los guardaparques pueden cerrar senderos o restringir el acceso temporalmente. Te aconsejamos consultar las condiciones climáticas y la apertura del parque con las autoridades ambientales antes de viajar."
            ],
            "steps": [
                [
                    "Los guardaparques monitorean las condiciones del clima en los accesos de montaña.",
                    "Ante tormentas eléctricas o crecientes súbitas se suspende el paso de visitantes por seguridad."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.road_closure_status": {
        "label": "estado de las vías y cierres carreteros",
        "answer": {
            "short": "Las vías de acceso hacia Los Nevados (como la carretera Manizales–Murillo o las trochas a Potosí) pueden presentar cierres temporales o pasos restringidos por deslizamientos y mantenimiento. Te recomendamos consultar el estado de la red vial con el #767 de Invías o con la Policía de Tránsito y Parques Nacionales antes de viajar.",
            "variants": [
                "El tránsito hacia las entradas del parque puede verse afectado por derrumbes o reparaciones en carreteras de montaña. Antes de iniciar el recorrido, verifica el estado de las vías con Invías (#767) o con las oficinas de Parques Nacionales."
            ],
            "steps": [
                [
                    "Consulta el estado de las carreteras nacionales llamando al #767 de Invías.",
                    "Pregunta en las terminales locales o a tu operador sobre el estado de los caminos destapados de acceso."
                ]
            ],
            "detail": "Las vías terciarias hacia Potosí y Juntas son destapadas y en temporadas de lluvias pueden requerir vehículos camperos 4x4.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.official_channels_to_check_status": {
        "label": "canales oficiales para consultar la apertura",
        "answer": {
            "short": "Para consultar si el parque está abierto y verificar alertas, ingresa a www.parquesnacionales.gov.co, revisa las redes oficiales @ParquesColombia, el portal reservasnevados.com, escribe a losnevados@parquesnacionales.gov.co o llama al celular +57 3229471031. Confirma siempre en fuentes oficiales antes de viajar.",
            "variants": [
                "Los medios oficiales para informarte sobre horarios y aperturas son el portal web de Parques Nacionales Naturales de Colombia, las cuentas @ParquesColombia en redes, el correo institucional losnevados@parquesnacionales.gov.co y el conmutador +57 (601) 353 2400."
            ],
            "steps": [
                [
                    "Portal web institucional: https://www.parquesnacionales.gov.co/",
                    "Plataforma de reservas: https://www.reservasnevados.com/",
                    "Redes sociales oficiales: @ParquesColombia",
                    "Línea de atención telefónica: +57 3229471031 y conmutador +57 (601) 353 2400"
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.offline_status_verification_advice": {
        "label": "verificar estado antes de perder señal",
        "answer": {
            "short": "Este asistente móvil funciona 100 % fuera de línea y no puede conectarse a internet para verificar el estado de hoy en tiempo real. Por ello, debes confirmar la apertura del parque, el clima y las alertas volcánicas en las páginas oficiales mientras tengas señal en la ciudad de origen antes de subir a la montaña.",
            "variants": [
                "Ten presente que esta guía offline no recibe actualizaciones en vivo en tu teléfono. Te recomendamos consultar el estado de los sectores y las vías en los canales de Parques Nacionales antes de salir de Manizales, Pereira, Armenia o Ibagué, donde aún cuentas con cobertura celular."
            ],
            "steps": [
                [
                    "Revisa los boletines y el estado del parque antes de abandonar la zona urbana con señal.",
                    "Descarga o guarda tus comprobantes de reserva y póliza en tu dispositivo."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.why_conservation_closures_exist": {
        "label": "motivos de los cierres por conservación",
        "answer": {
            "short": "Los cierres por conservación son una estrategia ambiental de Parques Nacionales para liberar de carga turística los ecosistemas sensibles de páramo y humedales, facilitando su recuperación natural y permitiendo labores de monitoreo e investigación. Confirma las fechas de estos descansos con Parques Nacionales al planear tu viaje.",
            "variants": [
                "Estos periodos de descanso buscan reducir la presión del turismo sobre el suelo, las fuentes de agua y la fauna del parque, además de permitir evaluaciones técnicas de los senderos. Consulta el calendario oficial con Parques Nacionales para evitar programar tu visita en días de cierre."
            ],
            "steps": [
                [
                    "Permitir la autorregulación natural del ecosistema tras temporadas de alto flujo de visitantes.",
                    "Facilitar a los guardaparques y biólogos realizar monitoreo de fauna, flora y estado de senderos."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.conservation_closures_dates_schedule": {
        "label": "fechas de los tres cierres anuales",
        "answer": {
            "short": "Parques Nacionales establece tres cierres por conservación de cinco días cada uno durante el año: 1) del lunes inmediatamente posterior a Semana Santa hasta el viernes; 2) del cuarto lunes de septiembre hasta el viernes; y 3) del cuarto lunes de noviembre hasta el viernes. Confirma las fechas exactas y las circulares vigentes con Parques Nacionales antes de viajar.",
            "variants": [
                "El cronograma reglamentario de descansos ambientales contempla tres semanas al año (después de Semana Santa, a finales de septiembre y a finales de noviembre). Te sugerimos validar el calendario específico con Parques Nacionales antes de reservar."
            ],
            "steps": [
                [
                    "Primer descanso ambiental: semana de Pascua (lunes posterior a Semana Santa al viernes).",
                    "Segundo descanso ambiental: cuarto lunes de septiembre al viernes de esa semana.",
                    "Tercer descanso ambiental: cuarto lunes de noviembre al viernes de esa semana."
                ]
            ],
            "detail": "Las fechas se programan después de temporadas de alta visitancia para evaluar y reparar los senderos e instalaciones.",
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.open_sectors_during_conservation_closures": {
        "label": "sectores durante descansos ambientales",
        "answer": {
            "short": "Durante los cierres por conservación, las rutas de senderismo y alta montaña en Cisne, Otún y Tolima permanecen cerradas. En el caso del circuito carreteable Brisas–Valle de las Tumbas, su habilitación o restricción depende de la circular específica que expida Parques Nacionales para cada periodo. Consulta siempre el comunicado oficial antes de desplazarte.",
            "variants": [
                "Los descansos ambientales inhabilitan los senderos pedestres de montaña, mientras que el acceso por Brisas puede o no habilitarse según determine Parques Nacionales en su aviso operativo. Es fundamental consultar directamente con la autoridad ambiental qué sectores estarán abiertos."
            ],
            "steps": [
                [
                    "Los senderos de trekking y cumbres en Cisne, Otún y Tolima cierran totalmente durante los descansos ambientales.",
                    "Verifica en la circular emitida por Parques Nacionales si el circuito vehicular de Brisas cuenta con autorización de pasadía."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.reopening_protocol_after_emergencies": {
        "label": "protocolo de reapertura tras una emergencia",
        "answer": {
            "short": "Para saber si el parque reabre tras una emergencia climática o volcánica, consulta los comunicados oficiales en www.parquesnacionales.gov.co o las redes @ParquesColombia. La reapertura se comunica formalmente cuando la autoridad ambiental levanta la medida preventiva, lo cual permite el ingreso pero no exime de los riesgos naturales de la alta montaña.",
            "variants": [
                "La reapertura de sectores cerrados por contingencias se notifica mediante actos o comunicados institucionales de Parques Nacionales. Antes de viajar debes verificar si el levantamiento de la restricción ya fue publicado oficialmente, recordando que las condiciones de montaña son dinámicas."
            ],
            "steps": [
                [
                    "Consulta www.parquesnacionales.gov.co y @ParquesColombia para confirmar el comunicado formal de reapertura.",
                    "Verifica con tu operador o guía registrado si tu sendero cuenta con acceso habilitado.",
                    "Recuerda que la reapertura administrativa no elimina los riesgos naturales inherentes a la alta montaña."
                ]
            ],
            "detail": "El cese de un cierre preventivo habilita nuevamente el acceso regulado, pero no garantiza la ausencia total de eventos climáticos o geológicos propios de la cordillera. Siempre acata las recomendaciones de seguridad de los guardaparques.",
            "reflection": None
        },
        "sources": [SRC_PNN, SRC_SGC],
        "last_verified": "2026-11-21"
    },
    "hours_status.pnn_administrative_office_hours": {
        "label": "horarios de atención de Parques Nacionales",
        "answer": {
            "short": "La atención administrativa y telefónica de Parques Nacionales Naturales de Colombia opera de lunes a viernes de 8:00 a. m. a 4:30 p. m. en jornada continua. Puedes comunicarte en ese horario a través del conmutador +57 (601) 353 2400 (extensiones 3011 y 3012) o al celular +57 3229471031. Confirma los horarios antes de acudir a las sedes.",
            "variants": [
                "Para trámites, radicación de consultas y atención al ciudadano, las oficinas de Parques Nacionales atienden en días hábiles de 8:00 a. m. a 4:30 p. m. Los puestos de control en la montaña manejan horarios propios de registro matutino que debes consultar por separado."
            ],
            "steps": [
                [
                    "Horario de atención institucional: lunes a viernes de 8:00 a. m. a 4:30 p. m. en jornada continua.",
                    "Canales telefónicos: conmutador +57 (601) 353 2400 (ext. 3011-3012) y celular +57 3229471031."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN_ATENCION, SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.uton_concession_office_hours": {
        "label": "horario de oficinas de concesión UTON",
        "answer": {
            "short": "Las oficinas de la concesión Unión Temporal Operación Nevados (UTON) en Manizales (barrio Palermo y calle 70) atienden al público de lunes a viernes de 8:00 a. m. a 12:00 m. y de 2:00 p. m. a 5:00 p. m. Puedes comunicarte a las líneas 321 506 6031 o 322 360 3637 para coordinar servicios en Brisas. Confirma la disponibilidad antes de tu visita.",
            "variants": [
                "Para contactar al operador concesionado del sector Brisas (UTON) en Manizales, el horario de atención en oficina es de lunes a viernes de 8:00 a. m. a 12:00 m. y de 2:00 p. m. a 5:00 p. m. Te aconsejamos llamar previamente a sus líneas telefónicas para asegurar tu trámite."
            ],
            "steps": [
                [
                    "Atención en oficinas de Manizales: lunes a viernes de 8:00 a. m. a 12:00 m. y de 2:00 p. m. a 5:00 p. m.",
                    "Teléfonos de contacto: 321 506 6031 y 322 360 3637."
                ]
            ],
            "detail": "Parques Nacionales publica en su portal oficial la información de contacto de la concesión UTON como operador de servicios ecoturísticos para el sector Brisas.",
            "reflection": None
        },
        "sources": [SRC_PNN, SRC_UTON],
        "last_verified": "2026-11-21"
    },
    "hours_status.morning_birdwatching_hours": {
        "label": "horario para avistamiento temprano de aves",
        "answer": {
            "short": "Parques Nacionales no tiene un horario especial de madrugada para observación de aves; la actividad se realiza dentro de los horarios oficiales de cada sector (desde las 6:00 a. m. en Cocora, 7:00 a. m. en Otún, 7:30 a. m. en Potosí y 8:00 a. m. en Brisas). Debes ir con guía autorizado por senderos permitidos y sin usar playbacks. Confirma con Parques Nacionales antes de viajar.",
            "variants": [
                "El aviturismo en Los Nevados debe desarrollarse respetando los horarios regulares de apertura de los puestos de control y en compañía de un guía registrado. Consulta con Parques Nacionales o con tu operador especializado el sector y turno más conveniente para tu visita."
            ],
            "steps": [
                [
                    "Ingresa en el primer turno oficial de atención matutino del sector elegido.",
                    "Realiza la actividad con guía acreditado, sin salir de senderos y sin usar reproducciones sonoras de aves."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.booking_time_limits_before_visit": {
        "label": "antelación requerida para reservar cupo",
        "answer": {
            "short": "Parques Nacionales indica que para Brisas–Valle de las Tumbas debes reservar con al menos un día de anticipación en reservasnevados.com para fines de semana y festivos; para los sectores Cisne y Otún se solicitan al menos tres días hábiles, y para Quindío–Dulima cinco días hábiles ante tu operador. Confirma disponibilidad con Parques Nacionales antes de tu viaje.",
            "variants": [
                "Los plazos oficiales para tramitar reservas son: al menos un día antes para Brisas en festivos y fines de semana, tres días hábiles para Cisne y Otún, y cinco días hábiles para el sector del Tolima. Te recomendamos reservar con suficiente tiempo y verificar cupos con Parques Nacionales."
            ],
            "steps": [
                [
                    "Sector Brisas: al menos 1 día de anticipación en www.reservasnevados.com para fines de semana y festivos.",
                    "Sectores Cisne y Otún: al menos 3 días hábiles de antelación con tu operador registrado.",
                    "Sector Quindío–Dulima: al menos 5 días hábiles antes de tu ingreso."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    },
    "hours_status.unplanned_midday_closures": {
        "label": "cierres imprevistos a mitad del día",
        "answer": {
            "short": "Sí, los guardaparques y autoridades pueden ordenar la suspensión de actividades y la evacuación de senderos en cualquier momento del día si se presentan tormentas eléctricas, emisión de cenizas o riesgo de derrumbes. En esos casos debes seguir con calma las instrucciones de tu guía para descender. Confirma las condiciones con Parques Nacionales antes de subir.",
            "variants": [
                "Por seguridad ante cambios bruscos del clima o actividad volcánica inesperada, el parque puede disponer el cierre inmediato a mitad de jornada y pedir el retiro de los visitantes. Acata siempre las indicaciones del personal oficial y consulta el estado del día antes de viajar."
            ],
            "steps": [
                [
                    "Sigue de inmediato las indicaciones de evacuación impartidas por tu guía y los guardaparques.",
                    "Desciende con precaución por la ruta autorizada sin apartarte del grupo."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN, SRC_SGC],
        "last_verified": "2026-11-21"
    },
    "hours_status.trail_maintenance_temporary_closures": {
        "label": "cierres por mantenimiento de senderos",
        "answer": {
            "short": "Parques Nacionales puede restringir temporalmente el acceso a senderos específicos cuando se adelantan labores de mantenimiento, adecuación de puentes o recuperación de vegetación. Estos cierres puntuales se notifican en los canales oficiales de Parques y a través de los operadores registrados. Consulta siempre el estado de las rutas antes de tu viaje.",
            "variants": [
                "De manera preventiva, algunos senderos o tramos pueden inhabilitarse temporalmente por obras técnicas o protección ecológica, mientras otros sectores continúan abiertos. Te aconsejamos verificar con Parques Nacionales qué recorridos están habilitados para tu fecha."
            ],
            "steps": [
                [
                    "Consulta en www.parquesnacionales.gov.co los avisos de senderos inhabilitados por adecuación.",
                    "Verifica con tu agencia qué senderos alternos autorizados están operando."
                ]
            ],
            "detail": None,
            "reflection": None
        },
        "sources": [SRC_PNN],
        "last_verified": "2026-11-21"
    }
}


def apply_updates():
    raw = SECTION_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    
    updated_count = 0
    for entry in data["entries"]:
        eid = entry["id"]
        if eid in CORRECTIONS:
            corr = CORRECTIONS[eid]
            entry["label"] = corr["label"]
            entry["answer"] = corr["answer"]
            entry["sources"] = corr["sources"]
            entry["last_verified"] = corr["last_verified"]
            updated_count += 1
            
    print(f"Applied updates to {updated_count} entries.")
    
    # Validate against JSON schema
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(data))
    if errors:
        print("Schema validation errors:")
        for err in errors:
            print(f"  - {err.message} at path {list(err.path)}")
        sys.exit(1)
    else:
        print("Draft202012Validator: PASSED (0 errors)")
        
    # Write back to file with clean formatting
    SECTION_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Successfully saved updated {SECTION_PATH}")

if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: hours_status now builds from hours_status/source/hours_status.v1.json via coordination/build_from_snapshot.py hours_status; rerunning this script would revert reviewed corrections.")
    apply_updates()
