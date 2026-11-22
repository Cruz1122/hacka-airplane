# hours_status fix round

Proposal: `research_notes/curation_v2/proposals/hours_status.v2.json`. Approved ops copied unchanged. Stylistic labels restored from `snapshots/sections_before/hours_status.json`.

## Review ops

- hours_status.general_opening_schedule: done. Bullet de Juntas de la Resolución 207 (cita la Resolución 268 de 2022, 6:00 a 10:00), no la frase suelta de Cocora.
- hours_status.park_open_today: done. Cita el `FileLeafRef` y el enlace del índice SGC; el índice no muestra el nivel de alerta.
- hours_status.conservation_closures: done. Cita el párrafo de cierres de la 207 (siete días y las cuatro fechas). Etiqueta documentada sin cambio de texto.
- hours_status.brisas_hours: done. Aprobada, sin cambio.
- hours_status.brisas_induction_talk_schedule: done. Aprobada, sin cambio.
- hours_status.brisas_exit_time: done. Etiqueta anterior «hora de salida del sector Brisas».
- hours_status.brisas_open_days: done. Etiqueta anterior «días de apertura del sector Brisas».
- hours_status.cisne_potan_hours: done. Etiqueta anterior «horario de registro en cabaña Potosí».
- hours_status.laguna_verde_trail_hours: done. Aprobada, sin cambio.
- hours_status.santa_isabel_conejeras_prior_day_checkin: done. Aprobada, sin cambio.
- hours_status.santa_isabel_summit_start_hour: done. Etiqueta anterior «hora de inicio para subir a Santa Isabel».
- hours_status.otun_sector_hours: done. Etiqueta anterior «horario de atencion para el sector Otun».
- hours_status.cedral_otun_hiking_schedule: done. Etiqueta anterior «horario de caminata desde El Cedral».
- hours_status.quindio_dulima_cocora_hours: done. Etiqueta anterior «horario de ingreso por Valle del Cocora».
- hours_status.quindio_dulima_juntas_anzoategui_hours: done. Bullets etiquetados de Juntas (10:00, Res. 268 de 2022) y Anzoátegui (11:00). Etiqueta anterior.
- hours_status.tolima_summit_push_hours: done. Etiqueta anterior «hora de ataque a cumbre Nevado Tolima».
- hours_status.night_entry_prohibition: done. Permiso especial del informe 2024 (Brisas y Cisne); no entrar de noche sin ese permiso para la fecha. Etiqueta nueva se mantiene.
- hours_status.camping_arrival_cutoff: done. Se quitó «prohíbe el camping en el área». Arenales–Brisas: restringido en 2023 y no habilitado en el informe 2024 (Villamaría). Arenales del Tolima: habilitación transitoria de 2023, sin dato posterior. Cita «Sitios para camping». Etiqueta anterior.
- hours_status.late_arrival_policy: done. Etiqueta anterior «política si llegas tarde a la entrada».
- hours_status.weekend_and_holiday_opening: done. Etiqueta anterior «horarios de atención en fines de semana».
- hours_status.weekday_opening: done. Etiqueta anterior «visitar el parque entre semana días hábiles».
- hours_status.pico_y_placa_hours_murillo: done. Artículos segundo, tercero y décimo sexto; es de la Secretaría de Tránsito del Tolima, no de PNN, y no nombra Brisas. `valid_until` 2027-07-20. Etiqueta anterior.
- hours_status.high_season_calendar: done. Cita la sección Temporalidad completa. Etiqueta anterior.
- hours_status.low_season_advantages: done. Etiqueta anterior «visitar Los Nevados en temporada baja».
- hours_status.high_season_operating_changes: done. Etiqueta anterior «cambios de operación durante temporada alta».
- hours_status.volcanic_alert_closures: done. Restaurados los tres ejemplos reales; retirados los dos de `_examples.json`. Quitada la frase de cumbre sin fuente. Cita la 068 y el boletín del 27 de junio de 2023. Etiqueta «suspensión de ingreso según el color de alerta».
- hours_status.weather_emergency_closures: done. Aprobada, sin cambio.
- hours_status.road_closure_status: done. El artículo octavo pide el acompañamiento de Invías cuando corresponda. Etiqueta anterior.
- hours_status.official_channels_to_check_status: done. Etiqueta documentada «web, redes y teléfono de Parques».
- hours_status.offline_status_verification_advice: done. Etiqueta anterior «verificar estado antes de perder señal».
- hours_status.why_conservation_closures_exist: done. Etiqueta anterior «motivos de los cierres por conservación».
- hours_status.open_sectors_during_conservation_closures: done. Etiqueta anterior «sectores durante descansos ambientales».
- hours_status.reopening_protocol_after_emergencies: done. Cita la 068 y el artículo 1 de la 207. Es el trámite de 2023, no un protocolo general. Etiqueta nueva se mantiene.
- hours_status.pnn_administrative_office_hours: done. Etiqueta anterior «horarios de atención de Parques Nacionales».
- hours_status.uton_concession_office_hours: done. Etiqueta anterior «horario de oficinas de concesión UTON», como pide el required_change.
- hours_status.morning_birdwatching_hours: done. Etiqueta anterior «horario para avistamiento temprano de aves».
- hours_status.unplanned_midday_closures: done. Etiqueta anterior «cierres imprevistos a mitad del día».
- hours_status.trail_maintenance_temporary_closures: done. Cita la frase completa de la facultad de restringir o cerrar. Etiqueta nueva se mantiene.
- hours_status.asomadera_potosi_entry_hours: done. Aprobada, sin cambio.
- hours_status.anzoategui_pit_la_punta_hours: done. Etiqueta documentada «PIT y La Punta: horario de atención» y bloque «Anzoátegui (Tolima)».

## Critical findings (40, all high)

- hours_status.camping_arrival_cutoff: done. El texto de critical.json repetía «prohíbe el camping en el área»; se sigue la revisión y contradictions.json.
- hours_status.volcanic_alert_closures: done. El texto de critical.json incluía la frase de cumbre sin fuente; se quitó.
- hours_status.night_entry_prohibition: done. Se añadió el permiso especial de 2024, que critical.json no traía.
- hours_status.road_closure_status: done. Se corrigió el papel de Invías.
- hours_status.pico_y_placa_hours_murillo: done. Se dice que la norma es del Tolima y no nombra Brisas.
- hours_status.general_opening_schedule: done. Bullet de Juntas citado.
- hours_status.park_open_today: done. El índice no muestra el nivel.
- hours_status.conservation_closures: done. Calendario de la 207 citado entero.
- hours_status.quindio_dulima_juntas_anzoategui_hours: done. Juntas y Anzoátegui separados.
- hours_status.reopening_protocol_after_emergencies: done. Trámite de 2023, no protocolo general.
- hours_status.trail_maintenance_temporary_closures: done. Frase completa.
- hours_status.anzoategui_pit_la_punta_hours: done. Bloque PIT y La Punta.
- hours_status.brisas_hours: done. La respuesta ya fechaba la ficha; op aprobada, sin cambio.
- hours_status.brisas_induction_talk_schedule: done. Op aprobada, sin cambio.
- hours_status.brisas_exit_time: done. La respuesta ya niega hora de salida; solo volvió la etiqueta.
- hours_status.brisas_open_days: done. La respuesta ya separa «todos los días» de los tres cierres; solo volvió la etiqueta.
- hours_status.cisne_potan_hours: done. La respuesta ya nombra el registro de Cisne; solo volvió la etiqueta.
- hours_status.laguna_verde_trail_hours: done. Op aprobada, sin cambio.
- hours_status.santa_isabel_conejeras_prior_day_checkin: done. Op aprobada, sin cambio.
- hours_status.santa_isabel_summit_start_hour: done. Ausencia de hora de cumbre ya dicha; solo volvió la etiqueta.
- hours_status.otun_sector_hours: done. La respuesta ya nombra la atención de Otún; solo volvió la etiqueta.
- hours_status.cedral_otun_hiking_schedule: done. Kilómetros ya citados; solo volvió la etiqueta.
- hours_status.quindio_dulima_cocora_hours: done. Horario ya citado; solo volvió la etiqueta.
- hours_status.tolima_summit_push_hours: done. Ausencia de hora de cumbre ya dicha; solo volvió la etiqueta.
- hours_status.late_arrival_policy: done. Cortes por sector ya citados; solo volvió la etiqueta.
- hours_status.weekend_and_holiday_opening: done. Reserva de finde ya citada; solo volvió la etiqueta.
- hours_status.weekday_opening: done. Sin otro horario entre semana; solo volvió la etiqueta.
- hours_status.high_season_calendar: done. Fechas de la 207 ya en la respuesta; cita ampliada.
- hours_status.low_season_advantages: done. Sin promesa de menos gente; solo volvió la etiqueta.
- hours_status.high_season_operating_changes: done. Cupos limitados ya citados; solo volvió la etiqueta.
- hours_status.weather_emergency_closures: done. Op aprobada, sin cambio.
- hours_status.official_channels_to_check_status: done. Canales ya citados; cambió la etiqueta documentada.
- hours_status.offline_status_verification_advice: done. La ficha no es el estado del día; solo volvió la etiqueta.
- hours_status.why_conservation_closures_exist: done. Motivo ya citado; solo volvió la etiqueta.
- hours_status.open_sectors_during_conservation_closures: done. La ficha no dice qué sectores quedan abiertos; solo volvió la etiqueta.
- hours_status.pnn_administrative_office_hours: done. Horario de oficina ya citado; solo volvió la etiqueta.
- hours_status.uton_concession_office_hours: done. Horario y teléfonos ya citados; volvió la etiqueta anterior.
- hours_status.morning_birdwatching_hours: done. Horarios y play-back ya citados; solo volvió la etiqueta.
- hours_status.unplanned_midday_closures: done. Facultad de cierre ya citada; solo volvió la etiqueta.
- hours_status.asomadera_potosi_entry_hours: done. Op aprobada, sin cambio.

## Contradictions

- horas de Potosí (cisne, otún, asomadera, camping, general): done. Cada respuesta nombra el trámite; no se dice que Potosí cierra a una sola hora.
- camping Arenales (activities.camping_tolima, camping_brisas_restricted, camping_where, hours_status.camping_arrival_cutoff): done. Norte: no habilitado en 2024 por el volcán. Tolima: transitorio de 2023, sin confirmación posterior. No se manda acampar en Arenales a secas.
- ingreso de noche (night_entry, cedral, camping): done en night_entry. cedral no afirma prohibición nocturna. camping ya no dice que esté prohibido transitar de noche.
- alerta amarilla (volcanic_alert_closures, yellow_upper_access, alert_yellow_meaning): done. No se dice que en amarillo los sectores sigan abiertos. El dato de 2023 no autoriza el ingreso. La restricción de la parte alta queda en weather_volcano.
- Juntas 10:00 frente a 11:00: done en el short de juntas y en el resumen general.

## Labels, taxonomy, arbiter, examples, cross

- labels.json volcanic_alert_closures: done. «suspensión de ingreso según el color de alerta».
- labels.json conservation_closures: done. Ya era «fechas de los cierres por conservación».
- labels.json official_channels_to_check_status: done. «web, redes y teléfono de Parques».
- labels.json uton_concession_office_hours: declined: el required_change nombra la etiqueta anterior «horario de oficinas de concesión UTON»; no se usa «horario y teléfonos de UTON en Manizales».
- labels.json anzoategui_pit_la_punta_hours: done. «PIT y La Punta: horario de atención».
- labels.json general_opening_schedule: declined: el required_change no pide cambiar la etiqueta y label_change es n/a; se deja «horarios generales de ingreso al parque».
- taxonomy volcanic_alert_closures frente a weather_volcano.volcanic_closures: done. Aquí quedan los umbrales de 2023; se quitó la frase de cumbre y el ejemplo que la mezclaba. El traslado de la restricción operativa no se escribe en weather_volcano.
- arbiter brisas_hours frente a weekend_and_holiday_opening: done. brisas_hours está aprobada y no se toca. El finde conserva la etiqueta de fines de semana y la regla de reserva; no se añadieron ejemplos casi copia.
- _examples.json drop «alerta amarilla significa que hoy dejan entrar al parque»: done. Retirada.
- _examples.json drop «la alerta del ruiz no es el cierre de la cumbre nevada»: done. Retirada.
- hours_status.cross volcanic frente a weather_volcano: done. Sin frase de cumbre; el cierre de 2023 queda aquí.
- hours_status.cross road frente a access: done. Esta respuesta no afirma el estado de hoy ni que Invías controle. El traslado a access queda en el dueño de access.
- hours_status.cross canales frente a services.official_sites: done. Aquí quedan teléfono, horario y correo.
- hours_status.cross UTON frente a access.uton_offices_manizales: done. Aquí queda el horario; la sede sigue en access.
- hours_status.cross charla frente a booking_fees.induction_requirement: done. Op de la hora aprobada, sin cambio.
- hours_status.cross pico y placa frente a access.own_car_brisas: done. Aquí queda la Resolución 1815, sin decir que sea el acceso a Brisas.
- weather_volcano.cross alerta amarilla: done. No se presenta la amarilla como apertura de hoy.
- booking_fees.cross charla: done. hours_status conserva la hora; la op está aprobada.
- booking_fees.cross hours_status.booking_time_limits_before_visit: declined: ese id no existe en hours_status; la antelación queda en booking_fees.
- access.cross UTON: done. Horario aquí, sede en access.
- access.cross vías: done. Esta entrada no afirma el cierre de hoy.
- conversation.cross «qué hora es»: done. Ya es hard negative de general_opening_schedule.
- rules.cross cierre sin indemnización: done. unplanned y trail informan la facultad de 2023; la exención sigue en rules. No se fusiona.
- actions.cross pico y placa: done. El horario de placa queda aquí; no se fusiona con actions.

## Refetch warns

- verify --refetch: done con `"fail": []` y 56 warns. La ficha HTML y el índice SGC no repiten en la descarga de hoy el texto pinneado (página dinámica; el review v1 ya los marcó warn). El PDF de la Resolución 1815 no coincide carácter a carácter con el OCR guardado. El docx de 2024 no extrae la misma cadena que el txt pinneado de activities; la cita sigue en ese archivo del manifiesto. La Resolución 207 sí reapareció en la descarga.
