# hours_status — decisión del curador

Fecha de la lectura: 2026-11-22. No se aplicó la propuesta. La app no puede saber si el parque está abierto hoy: cada respuesta de estado fecha la ficha (31 de octubre de 2026) o la Resolución 207 de 2023 y manda a confirmar con Parques Nacionales.

## Operaciones

- hours_status.general_opening_schedule | update | El resumen de la ficha es correcto y le falta la fecha; además omite que la Resolución 207 no coincide en Juntas. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.park_open_today | update | Ya niega el estado de hoy, pero no fecha la ficha ni aclara que el índice del SGC no trae el nivel. | evidencia: pnn_nevados.html, pnn_nevados.txt, sgc_boletines.html
- hours_status.conservation_closures | update | La ficha sí tiene los tres cierres de cinco días; la respuesta no fecha ni dice que la Resolución 207 trae otro calendario. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.brisas_hours | update | El horario de la ficha está bien; falta la fecha y no debe leerse como la apertura de hoy. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.brisas_induction_talk_schedule | update | La 1:30 p. m. está en la ficha; la frase de que después de esa hora no dejan iniciar no está. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.brisas_exit_time | update | La ficha no fija hora de salida; la tarde y la luz de día no están en el texto. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.brisas_open_days | update | Todos los días está en la ficha, junto con los cierres, sin aclarar si Brisas se exceptúa. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.cisne_potan_hours | update | La franja 7:30 a 10:00 está en la ficha para Cisne; se confunde con el horario de Otún en la misma cabaña. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.laguna_verde_trail_hours | update | El horario coincide con la ficha; falta decir que no confirma si el sendero está habilitado ese día. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.santa_isabel_conejeras_prior_day_checkin | update | El día anterior está en la ficha; no trae la hora de ese registro. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.santa_isabel_summit_start_hour | update | No hay hora oficial de cumbre; la madrugada del texto actual no está en la ficha. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.otun_sector_hours | update | La ficha escribe 12:00 p. m.; el dato es el de la ficha, no el estado del día. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.cedral_otun_hiking_schedule | update | Los kilómetros están en la ficha; salir de madrugada y llegar antes de la noche no. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.quindio_dulima_cocora_hours | update | Cocora 6:00 a 10:00 y los cinco días hábiles están en la ficha; falta la fecha. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.quindio_dulima_juntas_anzoategui_hours | update | La respuesta actual copia solo la ficha (ambos hasta las 11:00) y calla que la Resolución 207 cierra Juntas a las 10:00. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.tolima_summit_push_hours | update | La madrugada como práctica habitual no está en la ficha. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.night_entry_prohibition | update | Los horarios son diurnos y hay que respetarlos; la prohibición nocturna literal no aparece. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.camping_arrival_cutoff | update | Los tres puntos y la franja de Potosí están en la Resolución 207; llegar antes del anochecer no. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.late_arrival_policy | update | Los cortes de horario están en la ficha; la tolerancia no está escrita. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.weekend_and_holiday_opening | update | Se confunde con el horario de entre semana porque ambos repetían las mismas horas sin la regla de reserva. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.weekday_opening | update | Más cupo entre semana no está en la ficha; el horario sí es el mismo texto de todos los días. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.pico_y_placa_hours_murillo | update | Decir que rige en noviembre recorta la vigencia real, que va hasta el 20 de julio de 2027 en sábados, domingos y festivos. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_1815_2026.txt
- hours_status.high_season_calendar | update | La respuesta decía que no hay fechas fijas; la Resolución 207 sí las define y la ficha no las repite. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.low_season_advantages | update | Menos gente y más cupo no están en la ficha. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.high_season_operating_changes | update | Que los horarios se mantengan se sigue de que la ficha no publica otro; que se agoten rápido no está escrito. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.volcanic_alert_closures | update | Amarillo igual a sectores abiertos, y naranja o roja igual a cierre inmediato, no es una norma vigente en estas fuentes: es el cierre de 2023. | evidencia: resolucion_207_2023.txt, sgc_boletines.html
- hours_status.weather_emergency_closures | update | La facultad de cerrar por seguridad sí está; la lista de lluvias, granizo y derrumbes no. | evidencia: resolucion_207_2023.txt
- hours_status.road_closure_status | update | El estado de la carretera Manizales–Murillo no está en la ficha; se confunde con acceso. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_1815_2026.txt
- hours_status.official_channels_to_check_status | update | Los teléfonos y @ParquesColombia están en la ficha; el correo claro está en la Resolución 207, no en el texto ofuscado de la ficha. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.offline_status_verification_advice | update | El 100 % fuera de línea no está en la ficha; la ficha sí está fechada y no es el estado del día. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.why_conservation_closures_exist | update | Liberar carga y monitorear está en la ficha; la recuperación de humedales y fauna no. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.open_sectors_during_conservation_closures | update | Cerrar Cisne, Otún y Tolima y dejar Brisas a una circular no está en la ficha. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.reopening_protocol_after_emergencies | update | El procedimiento citado es el de 2023, no un protocolo que diga que cualquier emergencia de hoy ya se levantó. | evidencia: resolucion_207_2023.txt
- hours_status.pnn_administrative_office_hours | update | El horario de oficina está en la ficha y en atención al ciudadano; se confunde con los días de Brisas. | evidencia: pnn_atencion.txt, pnn_nevados.html, pnn_nevados.txt
- hours_status.uton_concession_office_hours | update | Horario, direcciones y teléfonos están en la ficha; se confunden con la portería de Brisas y con la sede de acceso. | evidencia: pnn_nevados.html, pnn_nevados.txt
- hours_status.morning_birdwatching_hours | update | Los horarios son los de la ficha; el play-back está en la Resolución 207, que la entrada no citaba. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.unplanned_midday_closures | update | La facultad existe; tormentas, ceniza y evacuación a cualquier hora no están nombradas. | evidencia: resolucion_207_2023.txt
- hours_status.trail_maintenance_temporary_closures | update | La facultad de cerrar por protección ecológica está; puentes y obras del día no. | evidencia: resolucion_207_2023.txt
- hours_status.asomadera_potosi_entry_hours | update | La respuesta ya cita la Resolución 207; le falta decir que la ficha de 2026 no repite el horario y que no es el estado del día. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt
- hours_status.anzoategui_pit_la_punta_hours | update | El PIT y La Punta están en la Resolución 207; se confunden con el horario de ingreso al sendero. | evidencia: pnn_nevados.html, pnn_nevados.txt, resolucion_207_2023.txt

## Sin revisar

Ninguna. Las 40 entradas de la sección tienen fila de auditoría y operación.

## Huecos de hecho

- La ficha (modificada el 31 de octubre de 2026) y la Resolución 207 de 2023 no coinciden en el calendario de cierres (3 cierres de 5 días frente a 4 de 7) ni en el horario de Juntas (ficha 6:00–11:00; resolución 6:00–10:00). Se dicen las dos versiones; no se elige una.
- El día del mes en el encabezado de la Resolución 207 no es legible en el PDF guardado. Se cita «Resolución 207 de 2023» y no se inventa el día 9.
- La rotación de placas en la Resolución 1815 está dañada por el OCR («9, 0 yhy», «7, 8 yS»). No se copia ninguna lista de placas. La vigencia sí es legible: 25 de julio de 2026 hasta el 20 de julio de 2027, sábados, domingos y festivos, 5:00–16:00, tramo Murillo–Cerro Gualí en Tolima.
- El índice del SGC nombra el boletín del Ruiz del 10 al 16 de noviembre de 2026 y no publica el nivel de alerta. No se afirma amarillo, naranja ni el estado de hoy.
- Ninguna de estas fuentes dice qué sectores siguen abiertos durante los cierres de conservación, ni una hora oficial de cumbre, ni una hora de salida en Brisas, ni que llegar después de la 1:30 impida la visita.
- El sitio de UTON no se descargó. El horario de sus oficinas sale de la ficha de Parques Nacionales.
- No se afirma que la app funcione «100 % offline»: esa frase no está en la ficha ni en una evidencia citable del repositorio.

## Descargas fallidas

Ninguna en esta pasada. Se reutilizaron los archivos ya fijados por hash de la fase 2. No se ejecutó fetch_evidence.py.

## route_check

n_removed_not_routing = 0. Se retiraron tres ejemplos de volcanic_alert_closures que preguntaban el cierre del sector nevado o de Brisas por gases, propio de weather_volcano.volcanic_closures. Los tres siguen enrutando. touched_loo_top1 = 0.5791; las confusiones de los ejemplos tocados no son fallo de la compuerta.

## Hallazgos cruzados

- hours_status.volcanic_alert_closures y weather_volcano.volcanic_closures. Solo se cambió este lado: la etiqueta pasa a «ingreso de visitantes según la alerta», se citan la Resolución 068 de 2023 y el boletín del 27 de junio de 2023, y los hard_negatives copian ejemplos del otro asiento. No se editó weather_volcano.
- hours_status.road_closure_status sigue aquí. Moverlo a access.mountain_road_conditions o access.from_murillo es de la ola 4; esta respuesta solo dice que la Resolución 1815 no es el estado de la vía.
- official_channels_to_check_status se solapa con services.official_sites; uton_concession_office_hours con access.uton_offices_manizales; brisas_induction_talk_schedule con booking_fees.induction_requirement; pico_y_placa_hours_murillo con access.own_car_brisas. Detalle en findings/hours_status.cross.json.
