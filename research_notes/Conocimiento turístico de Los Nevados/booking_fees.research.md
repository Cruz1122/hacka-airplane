# Reservas, tarifas y requisitos de ingreso — corrección round 2

Consulta y corrección: **2026-11-21**. El contenido conserva únicamente orientación con pasajes oficiales leídos. La ficha pública no muestra fecha editorial visible. No se asigna una fecha de publicación a esa página por el hecho de haberla consultado este día.

## Evidencia leída y mapeo

1. **Parque Nacional Natural Los Nevados, Parques Nacionales Naturales**  
   URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/  
   Evidencia local consultada: `services/evidence/pnn_nevados.txt`, copia de texto extraído del HTML guardado por el investigador de `services`; los pasajes siguientes se leyeron allí el 2026-11-21. La página no expone fecha editorial en el contenido revisado.
   - “la reserva no es obligatoria” y “para asegurar tu ingreso [...] reserva con al menos un día de anticipación” → `booking_fees.brisas_reservation` (se conserva solo que es opcional, recomendada y sujeta a cupo; el plazo se quitó de respuestas servidas porque es una cifra en una página sin fecha editorial).
   - “Ingreso a los demás sectores: la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada” → `booking_fees.other_sector_reservation` y `booking_fees.reservation_requirements`.
   - “En el Parque [...] es obligatorio el servicio de acompañamiento y guianza en todos los sectores” y “No todos los prestadores están autorizados para guiarte en todos los atractivos” → `booking_fees.guide_required`, `booking_fees.registered_operator_choice`.
   - “todo ingreso al área protegida debe realizarse con una agencia operadora o guía ecoturístico inscrito [...] (REPSE)” → `booking_fees.registered_operator_choice`.
   - “seguro obligatorio de accidentes” y la explicación de pago por UTON en Brisas o por operador en otros atractivos → `booking_fees.accident_insurance_requirement`, `booking_fees.insurance_payment_channel`.
   - “la tarifa [...] (no incluyen el seguro obligatorio de accidentes)” → `booking_fees.accident_insurance_requirement`.
   - “las edades mínimas [...] dependen del atractivo” y “Todos los menores de edad van acompañados de adultos cuidadores” → `booking_fees.age_minimum_by_attraction`, `booking_fees.minor_guardian_requirement`.
   - La sección de edades también dice “Edad máxima permitida de 69 años”; por conflicto con la Resolución 207 de 2023, no se ofrece el número como regla definitiva. Se deja constancia y se remite a confirmación para casos cercanos al límite → `booking_fees.maximum_entry_age`.
   - “la última charla de inducción obligatoria” en Brisas → `booking_fees.induction_requirement`. Se omite la hora exacta porque la página no muestra fecha editorial y la hora pertenece también al tema `hours_status`.
   - La ficha enlaza el sitio de UTON y dice que los servicios de Brisas se gestionan directamente con el operador: `https://www.operacionnevados.co` → `booking_fees.brisas_booking_channel`.
   - La tabla consultada no presenta una categoría estudiantil distinta → `booking_fees.student_admission_category`. La respuesta no atribuye una tarifa ni calcula una categoría por edad.

2. **Resolución 207 de 2023, reglamentación transitoria del PNN Los Nevados**  
   URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf  
   Fecha del acto: 2023-08-04. El pasaje se verificó en la extracción de texto local `activities/evidence/resolucion-207-2023.txt` y se dejó cita literal en `booking_fees/evidence/age-conflict-quotes.md`: “El rango de edad permitido para el ingreso de personas al área protegida es entre los 6 y los 70 años.” La misma resolución prohíbe “El ingreso de niños menores de 6 años y adultos mayores de 70 años”. Contrasta con “Edad máxima permitida de 69 años” que presenta la ficha web sin fecha editorial visible. El máximo definitivo queda sin resolver y se expresa como tal al visitante (`booking_fees.maximum_entry_age`). No se adopta una cifra por asumir que una página sin fecha es posterior al acto.

3. **Resolución 551 del 19 de diciembre de 2025, Parques Nacionales Naturales**  
   URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2025/12/RESOLUCION-551-DE-19-DE-DICIEMBRE-DE-2025-DG-1.pdf  
   Descargada a `booking_fees/evidence/resolucion-551-2025.pdf` el 2026-11-21. El PDF recibido es escaneado. La extracción de texto no produjo pasajes legibles y el OCR local no permitió verificar con confianza las tablas. Por tanto, **no se usa como evidencia de cifras, exenciones, documentos, pagos en línea ni otras disposiciones** en la sección corregida. Las cifras de tarifas, vehículos y costos que aparecían antes se retiraron de las respuestas servidas.

## Hallazgos del revisor y resolución

- Precio extranjero publicado como valor 2026 sin instrucción clara de comprobar cambios; la variante tampoco mantenía año/cautela: se quitaron montos y años de todas las respuestas tarifarias; `student_admission_category` remite a la tabla oficial vigente. No quedan respuestas independientes con precio parcial o sin caveat.
- Canal de reserva de Brisas sin destino exacto: ahora incluye `https://www.operacionnevados.co`, el enlace publicado por PNN, y aclara que requiere conexión y que la app no reserva.
- Guía/seguro: ajustado a la redacción de PNN, que requiere guía o personal de agencia registrada y pide comprobar autorización por atractivo; no se afirma que cualquier empleado califique.
- Edad máxima en conflicto: no se afirma como definitiva. La ficha consultada dice 69; la Resolución 207 de 2023 dice 6–70 como rango general. Se pide confirmación oficial para casos cerca del límite.
- Edad exacta de 25 años: se eliminó el cálculo por categorías y cualquier respuesta que asigne categoría al cumplir 25. Sigue sin resolución oficial explícita.
- Proveedores registrados e inducción: REPSE/acompañamiento queda aquí; se incorporó intención propia de inducción obligatoria. No se duplicaron sus ejemplos entre otras secciones. La ubicación de instalaciones para inducción no se especifica.

## Otros temas quitados y vacíos

Se eliminaron entradas con afirmaciones que dependían de la Resolución 551 sin tabla/pasaje verificable en esta corrección: montos de entrada por persona, tarifas de vehículos, exenciones y documentos acreditativos. También se retiraron flujos específicos de pago en línea, precios del seguro, reserva con días hábiles, condiciones de cancelación/reembolso, cupos cuantificados, descuentos estudiantiles y costos totales de guianza. El seguro no tiene precio verificado. La edad exacta para una persona de 25 años y la edad máxima vigente siguen sin resolución clara. La ficha no precisa el lugar general de la inducción para cada sector. Esos vacíos no se completan por inferencia.

## Semillas asignadas y mapeo final

Se respetaron índices de `coordination/assignments.json` (base cero):

- `2`, “cómo reservar” → `reservation_requirements`, `brisas_reservation`, `other_sector_reservation`, `brisas_booking_channel`.
- `3`, “cuánto cuesta la entrada” → `student_admission_category`; las tarifas específicas se retiraron por falta de pasaje verificable durante esta ronda.
- `5`, “si necesitas guía” → `guide_required`, `registered_operator_choice`.
- `30`, “la edad para ingresar” → `age_minimum_by_attraction`, `maximum_entry_age`, `minor_guardian_requirement`.
- `31`, “el seguro de accidentes” → `accident_insurance_requirement`, `insurance_payment_channel`.

Se agregó `induction_requirement` por la instrucción de alcance del coordinador y la evidencia de inducción obligatoria.

## Recuento final

13 entradas; 156 ejemplos (12 por entrada); 26 negativos difíciles (2 por entrada); cada entrada tiene dos variantes no numéricas en total contando `short` + una alternativa; etiquetas de 3–8 palabras; 1–2 ejemplos en inglés por entrada. Las respuestas no contienen cifras. Los negativos son ejemplos positivos de otras entradas locales. Los IDs `related` y `featured` resuelven dentro de la sección y las preguntas de aclaración cubren ambos filtros de entidad. Validación de esquema y contrato local ejecutada después de esta edición.

## Coordinator correction: legible official table retained

The previous correction removed prices and numeric booking lead times because the scanned Resolution 551 table was not readable. That removal was overly broad: the already-downloaded official PNN page contains a legible 2026 table and explicit booking/age passages. This correction restores six original IDs using ONLY that official webpage, not the unread scanned PDF. Evidence: weather_volcano/evidence/pnn-page-extracted.txt, lines 229–322 (tariffs/bookings) and 203–212 (ages), fetched 2026-11-21. The table explicitly states 2026, personal fees 12.500/24.500/68.000 for Brisas/Cisne/Otun and zero for Quindio-Dulima; insurance excluded. Quote: «realiza las reservas con tres (3) días hábiles de anticipación» and «haz tu reserva con cinco (5) días hábiles». Age minima 6/15 are published explicitly. Exact-age-25 and maximum-age conflicts stay unresolved. No vehicle-category conflict, exemptions or unread PDF claims are restored. Price entries expire after their stated year. The specific November traffic/booking notice is distinguished from the general optional Brisas reservation rule.

Seed 3 (general admission price) is preserved in booking_fees.sector_entry_fee_difference and the three category-specific fee entries. Final coordinator count: 19 entries and 230 examples.

## Expansión de la sección, 2026-11-21

Alcance: reservas y canales, anticipación, tarifas 2026 por sector y categoría, seguro, guía, documentos, edad, grupos, cancelación y cupos. Fuera de alcance: horarios, acceso, reglas de conducta y servicios.

Resultado: 19 → 31 entradas; 230 → 374 ejemplos. No se eliminó ninguna entrada.

Entradas nuevas (12): `exempt_young_children_and_seniors`, `exempt_disability_visitors`, `exemption_no_insurance_waiver`, `documents_to_carry`, `reservation_data_required`, `insurer_names_2023`, `group_guide_capacity`, `alta_montana_guide_glacier`, `vehicle_entry_fee`, `entry_payment_channels`, `cancellation_refund_policy`, `reservation_validation_window`.

Fuente de verdad: `entries.json` (autorado). `build_section.py` genera `data/knowledge/sections/booking_fees.json`. Cada cita está en `evidence/quotes.md` y `check_quotes.py` la verifica en `evidence/raw/`.

### Correcciones verificadas

1. Brisas, fines de semana y puentes festivos: la reserva es indispensable con al menos un día de anticipación (PNN 2026, Q02). La versión anterior decía sólo "opcional". La Resolución 207 de 2023 dice que Brisas no requiere reserva (Q33). Se sirve la regla más reciente y se registra el conflicto.
2. Canal de reserva de Brisas: `https://reservasnevados.com/` es el sistema oficial de reservas, operado por UTON (Q54, Q56). La versión anterior remitía a `operacionnevados.co`, que es la web de la concesión y redirige a `visitnevados.co`.
3. Tarifa de menores de 25 años: incluye "extranjero residente" (Res. 551, tabla de art. 6, Q21). La versión anterior lo omitía.
4. Estudiantes: no hay tarifa de estudiante, pero el numeral 4 del art. 13 exceptúa a estudiantes y profesores en programas de educación ambiental del parque, en temporada baja, con aprobación previa y ocho días calendario de anticipación (Q26, Q27). La versión anterior decía "sin categoría", lo cual era incompleto.
5. Quindío-Dulima: la página PNN muestra $0 (Q18). La Resolución 551 tiene una sola fila para todo Los Nevados (Q21) y no separa sectores. La Resolución 207 de 2023 recomendó un acceso sin cobro transitorio en la zona sur (Q64); no consta si sigue vigente. Conflicto sin resolver: se sirve como tal.
6. Vehículos: la Resolución 551 (art. 7, imagen pág. 8) da automóvil $10.000, colectivo $27.500, bus-buseta $56.000 y moto prohibida (Q22). La web usa otra etiqueta ("Microbús o buseta" a $27.500, Q19). Se sirve la resolución. Queda cerrado el gap de categorías de vehículo.
7. Edad máxima: 69 años en la web (Q13) frente a 70 años en la Resolución 207 de 2023 (Q36). Sin resolver; no se da por definitivo.
8. Edad exacta de 25 años: sin resolver. La resolución usa "Menor de 25 años" y "Mayor de 25 años" (Q62, imagen pág. 6), sin cubrir el 25 exacto.
9. Base legal del seguro: la Resolución 551 cita la Resolución 273 de 2024 (Q28). La 207 cita la Resolución 135 de 2014 y la 092 de 2018. Se usa la 551 por ser la más reciente.

### Fuentes leídas y guardadas en `evidence/raw/`

- `pnn_nevados.html` y `pnn_nevados.txt`: ficha PNN Los Nevados (copias de `services/evidence`, misma fecha de acceso).
- `resolucion-551-2025.pdf`: re-descargada con HTTP 200 y sha256 `5e65a5a1…f4def`, igual que la copia previa. `resolucion-551-2025.pdftotext.txt` está vacío (PDF escaneado). Las citas usan `resolucion-551-2025-ocr.txt`, y las cifras y la tabla de vehículos se confirmaron en imagen (páginas 6, 8, 11 y 12).
- `resolucion-207-2023.txt`: texto extraído de la reglamentación de ecoturismo.
- `protocolo_reservas_tolima_2024.pdf` y `.txt`: protocolo de reservas zona sur, fechado agosto de 2023 y publicado en 2024/02. Aplica sólo a Quindío y Tolima.
- `radicado_20266200001002.pdf` y `.txt`: respuesta PNN del 18-05-2026 (radicado 20266200003531) a agencias avaladas. Trata devoluciones pendientes y validación de reservas.
- `reservasnevados_home.html` y `reservasnevados_main.js`: sistema de reservas (SPA). El bundle contiene los campos de la tabla de reglas por ruta (edad mínima y máxima, días mínimos, visitantes por guía), pero sus valores vienen de la plataforma y no se consultaron.
- `operacionnevados_home.html`: redirige a `visitnevados.co`.

Verificación de citas: 71 de 71 pasan `check_quotes.py`. Las citas de la Resolución 551 se verifican contra OCR, porque el PDF no tiene texto nativo. Las cifras se confirmaron además en imagen.

### Vacíos (no servidos, no inferidos)

- Cancelación y devolución vigentes para todos los sectores: no hay política pública verificada. Sólo existen el protocolo sur de 2023 y el radicado de 2026, que dice que las devoluciones pendientes no se resolvieron de fondo.
- Precio del seguro obligatorio: no publicado en las fuentes.
- Precio de la guianza en Brisas: la web muestra $22.000, pero la unidad (por persona o por grupo) no consta. No se sirve.
- Cupos diarios numéricos: sólo hay cifras de un estudio de capacidad de carga de 2008 (Res. 207). No se sirven como cupo vigente.
- Valores por ruta de edad y de días de antelación en la app de reservas: no consultados. No se usan APIs internas.
- Exención por promoción (art. 15 de la Res. 551): sin detalle en la fuente.
- Forma de acreditar la discapacidad para la exención: no descrita en la fuente.
- Lista vigente de aseguradoras: sólo hay lista de 2023.
- Edad exacta de 25 años y edad máxima definitiva: sin resolver (ver correcciones 7 y 8).

### Cruces con otras secciones (no editadas)

- `hours_status.booking_time_limits_before_visit` repite la antelación de Brisas. Solapa `brisas_reservation`; conviene decidir a cuál sección pertenece.
- `access.no_motorcycles` trata la moto en Brisas; `vehicle_entry_fee` sólo da su tarifa (la moto no entra). El alcance es distinto.

### Verificación ejecutada

- `python3 booking_fees/build_section.py`: 31 entradas, 374 ejemplos.
- `python3 coordination/coordinator_fixes.py`: aplicado.
- `python3 coordination/validate_knowledge.py`: `Errors: 0`. Cero duplicados de ejemplos en el corpus. Aviso de revisión: `under25_admission_fee` y `adult_resident_admission_fee` tienen etiquetas casi idénticas (ratio 0,935).
- `python3 booking_fees/check_quotes.py`: `Quotes checked: 71; failed: 0`.
- Archivos fuera de la sección: el coordinador escribió `coordination/validation.json` y `coordination/polish/`. `fauna.json` cambió entre dos corridas; no se editó desde esta sesión.

## Round 2 (2026-11-21): auditoría, verificación y ampliación

Conteo: **31 → 67 entradas**; **386 → 818 ejemplos** tras `coordinator_fixes.py` (806 autorados más 12 que el coordinador fusiona en `reservation_requirements`). Ninguna entrada original eliminada.

Verificación final: `check_quotes.py` → `Quotes checked: 139; failed: 0` y `Entries checked: 67; failed: 0`. Validador → `Errors: 0`. Banderas globales: 4; de ellas, 1 pertenece a `booking_fees` (`similar_labels`, entre las tarifas de menores y mayores de 25; se conserva porque son categorías distintas), 1 es `hard_negative_review` en `hours_status` y 2 en `conversation` (ninguna entrada de esta sección las usa). Duplicados: 0. Respuestas servidas = respuestas autoradas (comparadas).

### Auditoría de la Ronda 1 (corregida)

- Línea base del validador antes de esta ronda: `booking_fees` tenía 1 advertencia (la misma de arriba).
- Resolución 551: la copia escaneada se revisó en imagen (páginas 6 y 8). Los Nevados: 12.500 / 24.500 / 68.000 en una sola fila; vehículos 10.000 / 27.500 / 56.000, moto prohibida.
- Hallazgo: PNN publica una segunda copia de la misma resolución con capa de texto (2026/02). Las citas nuevas Q65 a Q103 y Q129 a Q135 se verifican contra ella. Las citas anteriores basadas en OCR (Q21 a Q31) siguen válidas.
- Columnas de la ficha PNN: se confirmaron en la tabla HTML (`raw/pnn_nevados.html`). La guianza de Brisas ($22.000) cae bajo "Servicios ecoturísticos de interpretación y guianza"; "No aplica" cae bajo vehículos en Cisne-Poleka Kasue y Laguna del Otún.
- Entradas corregidas (no eliminadas):
  - `exempt_young_children_and_seniors`: los menores de 5 están exentos, pero la edad mínima de 6 años (Brisas, Cisne y Otún) y de 15 (resto de rutas) les impide entrar.
  - `vehicle_entry_fee`: alcance en Brisas según la ficha PNN; la resolución da el valor para todo el parque. Se registra el conflicto de etiquetas de la web.
  - `brisas_reservation`: conflicto Res. 207 (no requiere reserva) frente a PNN 2026 (sí en fines de semana). Se sirve 2026.
  - `sector_entry_fee_difference`, `under25_admission_fee`, `adult_resident_admission_fee`: aclaración de los 25 años exactos (la tabla no lo resuelve) y del protocolo sur de 2023.
  - `insurer_names_2023`, `reservation_data_required`: se quitó una afirmación sobre 2026 sin cita y se agregó la cita que la respalda.
  - `reservation_requirements`: se quitaron dos ejemplos propios en inglés y se agregaron dos en español (quedan 12 autorados; el coordinador fusiona 12 más, con 2 en inglés).

### Entradas nuevas (36)

- Exenciones de la Resolución 551, art. 13 (una entrada por categoría; el numeral 14, de buceo, no aplica a Los Nevados): `exempt_government_staff`, `exempt_official_mission`, `exempt_company_staff_inside_park`, `exempt_nearby_residents` (numerales 5 y 11), `exempt_researchers`, `exempt_indigenous_communities`, `exempt_property_owners`, `exempt_journalists`, `exempt_donors`, `exempt_park_volunteers`, `exempt_police_family`, `exempt_tourist_guides_and_providers` (17 y 19), `exempt_culture_agents`, `exempt_promotion_programs` (18 y art. 15), `exemption_not_guaranteed` (parágrafo 1), `exemption_proof_deadline` (art. 14).
- Tarifas y condiciones generales: `permanence_four_days` (art. 11), `tariff_annual_update` (arts. 12 y 22), `foreign_resident_definition` (art. 20), `can_countries_fee` (art. 20), `entry_fee_discounts` (art. 18), `vehicle_not_parking_fee` (art. 3, parágrafo 2).
- Reservas sur, atribuidas al protocolo de agosto de 2023: `south_reservation_order`, `south_cancel_by_email`, `south_modify_members` (incluye la nota de que PNN prepara nuevas "Condiciones del Servicio"), `south_reservation_status`, `south_payment_before_review`, `south_summit_capacity`.
- Otras: `brisas_daily_capacity` (Res. 207), `registration_form_required` (Res. 207), `reservation_by_operator` (Res. 207), `brisas_guide_price` ($22.000, ficha PNN, sin unidad), `platform_pays_services` (radicado 18-05-2026), `platform_payment_methods` (código público de reservasnevados.com: PSE, Daviplata, Visa, Mastercard, American Express), `insurance_price_not_published` y `guide_price_cisne_otun` (respuestas que dicen que el precio no está publicado).
- Eliminada antes de servir: una entrada de "Condiciones del Servicio" pendientes, fusionada con `south_modify_members` porque ambas respondían la misma duda.

### Fuentes descargadas (Ronda 2)

- `https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf` → `evidence/raw/resolucion-551-2025-pnn-2026-02.pdf` y `.txt` (texto digital, 16 páginas, HTTP 200, sha256 `1ca000dc…3721`). Cifras idénticas a la copia escaneada.
- `https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf` (enlazada desde la ficha PNN): escaneo sin capa de texto, 22 páginas; el enlace la describe como cronograma de Pico y Placa Ambiental. No se incorporó a evidencia (pertenece a `hours_status`); copia solo en scratchpad.
- `https://reservasnevados.com/static/js/main.340cd8ff.js` (script de la página, guardado como `evidence/raw/reservasnevados_main.js`): solo para los medios de pago visibles en el código. No se llamó al backend ni se consultaron rutas de API.
- Búsqueda de una página nacional de exenciones de PNN: sin resultado con la lista de exenciones; la fuente es la Resolución 551.

### Conflictos (se sirve la fuente más reciente u oficial, y se registra)

1. Reserva en Brisas: Res. 207 (no requiere) frente a PNN 2026 (sí en fines de semana). Se sirve 2026.
2. Vehículos: etiquetas de la web ("Microbús o buseta" $27.500) frente a la resolución ("Colectivo" $27.500). Se sirve la resolución; alcance en Brisas según la tabla de la ficha.
3. Pago: Res. 207 pide pago personal en las oficinas; Res. 551, art. 5, permite pago en línea. Se sirve la 551.
4. Modificación de integrantes: protocolo 2023 permite hasta 30%; radicado 2026 anuncia nuevas condiciones. Se sirve el protocolo, atribuido y con advertencia.
5. Cancelación: el protocolo indica cancelación por correo entre 24 y 72 horas y, en su política, la limita a fuerza mayor. Se sirve con advertencia.
6. Quindío-Dulima: PNN muestra $0; la Res. 551 tiene una sola tarifa para el parque; el protocolo 2023 recomendó no cobrar en el sur de forma transitoria. Sin resolver.
7. Edad máxima: 69 (ficha PNN, sin fecha editorial) frente a 70 (Res. 207). Sin resolver.
8. Capacidad de Brisas: 2.073 personas/día (Res. 207, estudio de 2008) no es el cupo asignado; se sirve con esa advertencia.

### Vacíos (no servidos, no inferidos)

1. Edad exacta de 25 años: la tabla no la asigna a ninguna categoría.
2. Precio del seguro obligatorio: no publicado (se responde como tal).
3. Guianza en Cisne y Otún: sin valor oficial (depende del operador; se responde como tal).
4. Guianza en Brisas ($22.000): la unidad (persona o grupo) no consta.
5. Política vigente de cancelación y devolución: no hay documento público vigente; el radicado de 2026 indica devoluciones pendientes sin pronunciamiento.
6. Forma de acreditar la discapacidad para la exención: no descrita en la resolución.
7. Programas de promoción (art. 15): sin áreas ni fechas publicadas para Los Nevados.
8. Cupo diario vigente: no hay cifra actual; solo estudios de 2008 y 2023.
9. Número máximo de turistas por sector: la ficha dice que existe, sin cifra.
10. "Condiciones del Servicio" de UTON y PNN: en proceso según el radicado de 18-05-2026; no publicado.
11. Pasos para reservar en el sur (protocolo 2023): no servidos; describen un formulario de Google que el radicado de 2026 indica que la plataforma de UTON reemplazó.
12. Art. 14 de la Res. 551 (numerales 10, 14 y 17, con nombres previos): integrado en las entradas de propietarios y de guías.

### Cruces con otras secciones (no editadas)

- Pico y Placa (Res. 1815/2026): pertenece a `hours_status`.
- Restricción por embarazo o problemas cardiovasculares (Res. 207): pertenece a `health_safety`; no se duplicó.
- `hours_status.booking_time_limits_before_visit` repite la antelación de Brisas; ya estaba señalado en la Ronda 1.

### Comandos ejecutados

- `python3 booking_fees/check_quotes.py` → `Quotes checked: 139; failed: 0` / `Entries checked: 67; failed: 0`.
- `python3 booking_fees/build_section.py` → `67 entries, 806 examples`; luego `python3 coordination/coordinator_fixes.py` → `coordinator fixes applied`; luego `python3 coordination/validate_knowledge.py` → `Errors: 0; review flags: 4`.
- No se hizo commit. El coordinador escribió en `coordination/validation.json` y `coordination/polish/` (compartido con otros agentes).
