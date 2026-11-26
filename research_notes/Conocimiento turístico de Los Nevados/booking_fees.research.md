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


## Updated entry: booking_fees.accident_insurance_requirement

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Para visitar el Parque siempre debes adquirir un seguro obligatorio de accidentes otorgado por una compañía aseguradora avalada por Parques Nacionales.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2°: La exención de ingreso no incluye el requisito obligatorio de
> adquisición de seguro de accidenten establecida en la Resolución 273 de 2024


## Updated entry: booking_fees.age_minimum_by_attraction

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Edad mínima de 6 años
> para entrar a los atractivos del carreteable Brisas-Kumanday, visitar el centro El Cisne o visitar la Laguna del Otún por la cabaña Potosí.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Edad mínima de 15 años
> para el resto de rutas, travesías y cumbres.


## Updated entry: booking_fees.alta_montana_guide_glacier

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> tu grupo debe ser liderado solamente por guías especializados en alta montaña.


## Updated entry: booking_fees.brisas_booking_channel

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives, label, sources

- https://reservasnevados.com/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_home.html`

> Sistema oficial para reservas del Parque Nacional Natural Nevados, desde este sistema podrás reservar para el sector Brisas Valle de las Tumbas y los operadores autorizados a los demás senderos.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Ingreso al sector Brisas-Kumanday:
> la reserva no es obligatoria. Sin embargo, para asegurar tu ingreso (ya que los cupos diarios son limitados), reserva con al menos un día de anticipación. Reserva para este atractivo en:
> www.reservasnevados.com

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> el operador autorizado por Parques Nacionales es la concesión Unión Temporal Operación Nevados (UTON). Ellos gestionan directamente los servicios ecoturísticos como reservas, ingreso, guianza, transporte y tienda.

- https://reservasnevados.com/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_home.html`

> Sistema oficial para reservas del Parque Nacional Natural Nevados, desde este sistema podrás reservar para el sector Brisas Valle de las Tumbas

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/radicado_20266200001002.txt`

> recientemente    se    recibieron   notificaciones   informando
>        cancelaciones de reservas


## Updated entry: booking_fees.can_countries_fee

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> CAN: Comunidad Andina de Naciones, los países que la conforman son: Bolivia,
> Colombia, Ecuador y Perú.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Estos son los valores de ingreso para el 2026 en pesos colombianos (no incluyen el seguro obligatorio de accidentes):
> Sector
> Menor de 25 años


## Updated entry: booking_fees.center_otun_reservation_lead

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> realiza las reservas con tres (3) días hábiles de anticipación.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Visita a los atractivos de los sectores Cisne-Poleka Kasue y Otún:
> realiza las reservas con tres (3) días hábiles de anticipación.


## Updated entry: booking_fees.documents_to_carry

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> debe demostrar con la presentación del Registro Civil de Nacimiento, Tarjeta de
> Identidad, Cédula de Ciudadanía, Cédula de Extranjería Colombiana expedida en
> Colombia o Visa (Negocios, Temporal o Residente), o Pasaporte según
> corresponda.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> Todas las personas deben presentar documento de identificación (Cédula de ciudadanía, registro civil de nacimiento,
>      pasaporte o DNI).

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> autorización de ingreso acompañada
>      del soporte de pago, póliza


## Updated entry: booking_fees.entry_fee_discounts

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTÍCULO 18. DESCUENTOS. Parques Nacionales Naturales de Colombia podrá
> realizar descuentos en los valores establecidos en esta resolución en el marco
> de convenios con entidades públicas, privadas y/o de naturaleza mixta, que no
> estén incluidas en el régimen de excepciones, cuya finalidad sea incentivar el
> ecoturismo en las áreas protegidas, a que se refiere esta resolución.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> RESOLUCIÓN 551
> 
> DE 19 DE DICIEMBRE DE 2025
> 
> “Por medio de la cual se actualiza el valor de los derechos de ingreso y
> servicios complementarios a las áreas protegidas del Sistema de Parques
> Nacionales Naturales de Colombia y se unifican disposiciones.”
> 
> Para el
> Parque Nacional Natural Los Corales del Rosario y San Bernardo la
> temporada alta se contemplada para las siguientes fechas: entre el primero (1)
> de noviembre y treinta y uno (31) de enero, entre el quince (15) de junio y el
> quince (15) de agosto, semana santa.
> Consecuentemente, la temporada baja estará contemplada en las fechas que no
> se consideran temporada alta.
> Visitante: Persona autorizada por Parques Nacionales Naturales para ingresar en
> una de las áreas del Sistema de Parques Nacionales Naturales, para visitar o
> realizar una o varias de las actividades o servicios regulados por el administrador
> del Sistema en un periodo definido y continuo.
> CAPÍTULO 5
> DEROGATORIA Y VIGENCIA
> ARTÍCULO 21. – Publíquese esta resolución en el Diario Oficial y en el sitio de
> internet de Parques Nacionales Naturales de Colombia.
> Comuníquese a las
> áreas protegidas mencionadas en esta resolución, a las respectivas Direcciones
> Territoriales y a las Subdirecciones de la entidad.
> ARTÍCULO 22. – La presente resolución rige a partir del primero de enero de
> 2026 y deroga a partir de esta fecha las disposiciones que le sean contrarias,
> entre éstas, la Resolución 695 de 2024 .
> Dada en Bogotá D.C., a los 19
> 
> días del mes de diciembre de 2025.


## Updated entry: booking_fees.entry_payment_channels

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTÍCULO 5. COMPRA DEL DERECHO DE INGRESO. El visitante de las áreas
> protegidas administradas por Parques Nacionales Naturales de Colombia podrá
> pagar el valor de derecho de ingreso así:
> 1. Pago presencial: De acuerdo con los procedimientos de cada Área Protegida
> se hará el pago en la sede o en la oficina de atención del usuario de la central
> en Bogotá o en la cuenta bancaria que la entidad establezca.
> 2. Pago en Línea: Se podrá hacer el pago a través del enlace ubicado en el sitio
> de internet de la entidad, a través de medios bancarios electrónicos disponibles.
> Los pagos en línea generarán costos por el uso de las plataformas de reservas


## Updated entry: booking_fees.exempt_company_staff_inside_park

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Personal de las Fuerzas Armadas y los trabajadores de empresas,
> cooperativas y/o asociaciones públicas o privadas que cuenten con
> instalaciones ubicadas dentro de las áreas protegidas que deban ingresar
> por razón de sus funciones, previa revisión y aprobación del jefe del área
> protegida.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_culture_agents

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los agentes culturales que estén registrados en “Soy Cultura – Registro
> Único Nacional de Agentes Culturales” del Ministerio de Cultura en
> temporada baja.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_disability_visitors

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los Nacionales o Extranjeros en condición de discapacidad.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2°: La exención de ingreso no incluye el requisito obligatorio de
> adquisición de seguro de accidenten establecida en la Resolución 273 de 2024


## Updated entry: booking_fees.exempt_donors

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los representantes de organismos públicos o privados, nacionales,
> internacionales y Organizaciones No Gubernamentales (ONG) que donen
> bienes en dinero o especie, en beneficio de Parques Nacionales Naturales
> de Colombia, para coadyuvar la función de salvaguarda y protección de las
> áreas del Sistema de Parques Nacionales Naturales, con el objetivo de
> verificar la destinación de los recursos donados y/o en el marco de los
> convenios celebrados.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_indigenous_communities

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los miembros de las comunidades indígenas, afrocolombianas, rom y
> raizales que vivan dentro del Área Protegida o los que habiten en las
> inmediaciones de las áreas del Sistema de Parques Naciones Naturales e
> ingresen para realizar actividades de pagamento


## Updated entry: booking_fees.exempt_journalists

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los periodistas en ejercicio de sus funciones, debidamente acreditados.


## Updated entry: booking_fees.exempt_nearby_residents

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los nativos o residentes de los centros poblados menores a 10.000
> habitantes

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los pobladores de la región que deben ingresar al área en actividades de
> paso.


## Updated entry: booking_fees.exempt_official_mission

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los servidores públicos, contratistas, de las fuerzas armadas de las
> instituciones oficiales y públicas en misión oficial, al igual que misiones
> medicas en desarrollo de su labor.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_park_volunteers

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los Guardaparques Voluntarios por el término de su voluntariado y un año
> más, contado a partir de la terminación del mismo, así como los Guarda
> Parques Honorarios durante el término de diez años contado a partir de su
> designación.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_police_family

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> El cónyuge o compañera (o) permanente y los hijos menores de veinticinco
> (25) años sobrevivientes o, a falta de estos, los padres, de los miembros
> de la Fuerza Pública fallecidos en servicio activo, únicamente por hechos o
> actos ocurridos por causa y razón del mismo, o por acción directa del
> 
> Página 12 de 16
> 
> RESOLUCIÓN 551
> 
> DE 19 DE DICIEMBRE DE 2025
> 
> “Por medio de la cual se actualiza el valor de los derechos de ingreso y
> servicios complementarios a las áreas protegidas del Sistema de Parques
> Nacionales Naturales de Colombia y se unifican disposiciones.”
> 
> 17.
> 18.
> 
> 19.
> 
> 20.
> 
> enemigo o en combate, y que por ello les haya sido reconocida pensión, en
> calidad de beneficiarios de la Ley 1699 de 2013, con la presentación de
> documento que para tal efecto determinen los grupos de prestaciones


## Updated entry: booking_fees.exempt_promotion_programs

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los beneficiarios del incentivo de exoneración del pago de valor de ingreso
> en el marco de los distintos programas de promoción y apropiación de las
> áreas protegidas que establezca la entidad, tales como el "Pasaporte' de
> las áreas del Sistema de Parques Nacionales Naturales de Colombia.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTICULO 15. –EXCEPCIONES PROGRAMA DE PROMOCIÓN. Parques Nacionales
> Naturales podrá implementar las excepciones de pago, en relación con el factor
> personal y de medio de transporte, como parte de un programa de inclusión
> social y ambiental, en el marco del deber público y de garantizar los derechos a
> la educación y recreación asociados a la conservación en las áreas protegidas
> del Sistema de Parques Nacionales Naturales de Colombia.
> La designación de las áreas protegidas y la fecha de excepción se realizará,
> previo concepto económico proveniente de la Subdirección de Sostenibilidad y
> Negocios Ambientales, con aval de la Subdirección de Gestión y Manejo.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> RESOLUCIÓN 551
> 
> DE 19 DE DICIEMBRE DE 2025
> 
> “Por medio de la cual se actualiza el valor de los derechos de ingreso y
> servicios complementarios a las áreas protegidas del Sistema de Parques
> Nacionales Naturales de Colombia y se unifican disposiciones.”
> 
> Para el
> Parque Nacional Natural Los Corales del Rosario y San Bernardo la
> temporada alta se contemplada para las siguientes fechas: entre el primero (1)
> de noviembre y treinta y uno (31) de enero, entre el quince (15) de junio y el
> quince (15) de agosto, semana santa.
> Consecuentemente, la temporada baja estará contemplada en las fechas que no
> se consideran temporada alta.
> Visitante: Persona autorizada por Parques Nacionales Naturales para ingresar en
> una de las áreas del Sistema de Parques Nacionales Naturales, para visitar o
> realizar una o varias de las actividades o servicios regulados por el administrador
> del Sistema en un periodo definido y continuo.
> CAPÍTULO 5
> DEROGATORIA Y VIGENCIA
> ARTÍCULO 21. – Publíquese esta resolución en el Diario Oficial y en el sitio de
> internet de Parques Nacionales Naturales de Colombia.
> Comuníquese a las
> áreas protegidas mencionadas en esta resolución, a las respectivas Direcciones
> Territoriales y a las Subdirecciones de la entidad.
> ARTÍCULO 22. – La presente resolución rige a partir del primero de enero de
> 2026 y deroga a partir de esta fecha las disposiciones que le sean contrarias,
> entre éstas, la Resolución 695 de 2024 .
> Dada en Bogotá D.C., a los 19
> 
> días del mes de diciembre de 2025.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTICULO 15. –EXCEPCIONES PROGRAMA DE PROMOCIÓN. Parques Nacionales
> Naturales podrá implementar las excepciones de pago, en relación con el factor
> personal y de medio de transporte, como parte de un programa de inclusión
> social y ambiental, en el marco del deber público y de garantizar los derechos a
> la educación y recreación asociados a la conservación en las áreas protegidas
> del Sistema de Parques Nacionales Naturales de Colombia.
> La designación de las áreas protegidas y la fecha de excepción se realizará


## Updated entry: booking_fees.exempt_property_owners

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los propietarios de predios privados que se encuentren dentro de un área
> del Sistema de Parques Nacionales Naturales, su cónyuge y familiares hasta
> el cuarto grado de consanguinidad, segundo de afinidad y primero civil, a
> través de la presentación del registro civil de nacimiento o matrimonio y
> en caso de unión marital con declaración juramentada; datos que se
> ingresarán en el registro de propietarios que lleve el área protegida.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los propietarios de predios privados que se encuentren dentro de un área
> del Sistema de Parques Nacionales Naturales, su cónyuge y familiares hasta
> el cuarto grado de consanguinidad, segundo de afinidad y primero civil, a
> través de la presentación del registro civil de nacimiento

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 10, 14 y
> 17 del presente capitulo
> deberán informar previamente los nombres


## Updated entry: booking_fees.exempt_researchers

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los investigadores con previa revisión y aprobación del jefe del área
> protegida en desarrollo de sus actividades en proyectos autorizados de las
> áreas del Sistema de Parques Nacionales Naturales.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.exempt_tourist_guides_and_providers

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los guías de turismo debidamente acreditados que prestan sus servicios en
> la respectiva área protegida según lo señala el artículo 2.2.4.4.10.5 del
> decreto 1379 de 2021.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los Prestadores de Servicios Asociados al Ecoturismo inscritos en el
> Registro para Prestadores de Servicios Asociados al Ecoturismo, en el
> marco de la prestación de sus servicios en la respectiva área protegida en
> la que tienen su registro, adicionalmente estos prestadores de servicios
> asociados podrán ingresar en temporada baja para reconocimiento de rutas
> o avanzadas.


## Updated entry: booking_fees.exempt_young_children_and_seniors

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los niños nacionales o extranjeros residentes en Colombia o miembros de
> la Comunidad Andina de Naciones
> menores de 5 años, y los adultos
> nacionales o extranjeros mayores de 62 años residentes en Colombia o
> miembros de la Comunidad Andina de Naciones; quienes deben acreditar
> su edad, a través de la presentación de cédula de ciudadanía o cédula de
> extranjería colombiana o visa (negocios, temporal o residente), pasaporte,
> o registro civil respectivo.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Edad mínima de 6 años
> para entrar a los atractivos del carreteable Brisas-Kumanday, visitar el centro El Cisne o visitar la Laguna del Otún por la cabaña Potosí.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Edad mínima de 15 años
> para el resto de rutas, travesías y cumbres.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> El rango de edad permitido para el ingreso de personas al área protegida es entre los 6 y los 70 años.


## Updated entry: booking_fees.exemption_no_insurance_waiver

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2°: La exención de ingreso no incluye el requisito obligatorio de
> adquisición de seguro de accidenten establecida en la Resolución 273 de 2024


## Updated entry: booking_fees.exemption_not_guaranteed

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> En todos los casos anteriormente expuestos la autorización de
> ingreso a los exceptuados de pago dependerá de la capacidad de manejo y la
> zonificación del área protegida, salvo para quienes habitan de manera
> permanente en las áreas del Sistema de Parques Nacionales Naturales.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTÍCULO 13. EXCEPCIONES AL PAGO DE LOS DERECHOS DE INGRESO A LAS
> ÁREAS PROTEGIDAS. Se encuentran exceptuados del pago del derecho de
> ingreso a las áreas protegidas, tanto del factor personal como factor medio de
> transporte

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 1°: En todos los casos anteriormente expuestos la autorización de
> ingreso a los exceptuados de pago dependerá de la capacidad de manejo

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2°: La exención de ingreso no incluye el requisito obligatorio de
> adquisición de seguro de accidenten establecida en la Resolución 273 de 2024


## Updated entry: booking_fees.exemption_proof_deadline

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario previos a la visita que
> se pretenda efectuar, ante el jefe del área protegida correspondiente, quién
> emitirá aprobación vía electrónica y llevará un informe mensual para control y
> seguimiento.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.guide_required

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> es obligatorio el servicio de acompañamiento y guianza en todos los sectores.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> Estar acompañado de un guía avalado por el PNN Los Nevados, quien a su vez deberá estar autorizado por una
>      operadora de turismo avalada para realizar tal actividad, ningún visitante podrá ingresar solo

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> Estar acompañado de un guía avalado por el PNN Los Nevados


## Updated entry: booking_fees.induction_requirement

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> Recibir una charla de inducción: Se establece como requisito obligatorio para el ingreso al Área Protegida recibir la
> charla de inducción de manera presencial

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> la última charla de inducción obligatoria se realiza a la 1:30 p. m.


## Updated entry: booking_fees.insurance_payment_channel

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Lo debes pagar a través de la Unión Temporal Operación Nevados (UTON) en el sector Brisas-Kumanday, o a través de la agencia operadora de tu elección en los demás atractivos.


## Updated entry: booking_fees.insurance_price_not_published

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Para visitar el Parque siempre debes adquirir un seguro obligatorio de accidentes otorgado por una compañía aseguradora avalada por Parques Nacionales.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2°: La exención de ingreso no incluye el requisito obligatorio de
> adquisición de seguro de accidenten establecida en la Resolución 273 de 2024


## Updated entry: booking_fees.minor_guardian_requirement

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Todos los menores de edad
> van acompañados de adultos cuidadores.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> superar los 15 años de edad, contar con la autorización de los padres o
>      tutores


## Updated entry: booking_fees.other_sector_reservation

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Ingreso a los demás sectores
> : la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje.


## Updated entry: booking_fees.permanence_four_days

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> termino de cuatro (4) días calendario continuos, conforme al artículo
> 2.2.2.1.10.1 del Decreto 1076 de 2015
> Tratándose de visitantes con paquete turístico, adquirido con agencias y/o
> operadores turísticos, el derecho de permanencia será por un término igual al
> que prevea el paquete comprado.


## Updated entry: booking_fees.platform_payment_methods

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://reservasnevados.com/static/js/main.340cd8ff.js (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_main.js`

> aria-label":"PSE",children:(0,Or.jsx)("b",{children:"PSE"})}),(0,Or.jsxs)("span",{className:"medio-pago-logo medio-pago-logo--daviplata","aria-label":"Daviplata",children:[(0,Or.jsx)("b",{children:"Davi"}),(0,Or.jsx)("small",{children:"Plata"})]}),(0,Or.jsx)("span",{className:"medio-pago-logo medio-pago-logo--visa","aria-label":"Visa",children:"VISA"}),(0,Or.jsxs)("span",{className:"medio-pago-logo medio-pago-logo--mastercard","aria-label":"Mastercard",children:[(0,Or.jsx)("i",{}),(0,Or.jsx)("i",{})]}),(0,Or.jsxs)("span",{className:"medio-pago-logo medio-pago-logo--amex","aria-label":"American Express"

- https://reservasnevados.com/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_home.html`

> Sistema oficial para reservas del Parque Nacional Natural Nevados, desde este sistema podrás reservar para el sector Brisas Valle de las Tumbas y los operadores autorizados a los demás senderos.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> ARTÍCULO 5. COMPRA DEL DERECHO DE INGRESO. El visitante de las áreas
> protegidas administradas por Parques Nacionales Naturales de Colombia podrá
> pagar el valor de derecho de ingreso así:
> 1. Pago presencial: De acuerdo con los procedimientos de cada Área Protegida
> se hará el pago en la sede o en la oficina de atención del usuario de la central
> en Bogotá o en la cuenta bancaria que la entidad establezca.
> 2. Pago en Línea: Se podrá hacer el pago a través del enlace ubicado en el sitio
> de internet de la entidad, a través de medios bancarios electrónicos disponibles.
> Los pagos en línea generarán costos por el uso de las plataformas de reservas y
> de los medios de pago, servicios complementarios que deberán ser asumidos
> por el visitante y sumarse al valor final a pagar.

- https://reservasnevados.com/static/js/main.340cd8ff.js (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_main.js`

> aria-label":"Medios de pago disponibles"


## Updated entry: booking_fees.platform_pays_services

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives, label

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/radicado_20266200001002.txt`

> registro de
> visitantes, validación de información y pago de los servicios ecoturísticos
> asociados a la visita

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/radicado_20266200001002.txt`

> recientemente    se    recibieron   notificaciones   informando
>        cancelaciones de reservas

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/radicado_20266200001002.txt`

> Frente a las solicitudes de devolución mencionadas, se informa que el Parque
> Nacional Natural Los Nevados no cuenta actualmente con información específica
> que permita emitir un pronunciamiento de fondo


## Updated entry: booking_fees.quindio_reservation_lead

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> haz tu reserva con cinco (5) días hábiles antes del día de tu ingreso al Parque.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2024/02/Protocolo-de-reservas-nevado-del-Tolima.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/protocolo_reservas_tolima_2024.txt`

> La solicitud de reserva se debe generar con mínimo cinco (5) días hábiles de antelación a la fecha de ingreso al Área Protegida
>         entre los días lunes y viernes según orden de solicitud, sin contar los sábados, domingos o festivos.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Sector Quindío-Dulima:
> haz tu reserva con cinco (5) días hábiles


## Updated entry: booking_fees.registered_operator_choice

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> No todos los prestadores están autorizados para guiarte en todos los atractivos.


## Updated entry: booking_fees.registration_form_required

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> diligenciar debidamente el formato de ingreso


## Updated entry: booking_fees.reservation_by_operator

- Reason: v2: date the changeable rule and cite the passage that supports it.
- Changed fields: answer

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-207-2023.txt`

> Los operadores avalados por el área protegida deberán solicitar la reservación de ingreso al área protegida de la siguiente

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt`

> Ingreso a los demás sectores
> : la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje.

- https://reservasnevados.com/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/reservasnevados_home.html`

> Sistema oficial para reservas del Parque Nacional Natural Nevados, desde este sistema podrás reservar para el sector Brisas Valle de las Tumbas


## Updated entry: booking_fees.south_payment_before_review

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2024/02/Protocolo-de-reservas-nevado-del-Tolima.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/protocolo_reservas_tolima_2024.txt`

> Después de ser efectuado y verificado el pago correspondiente según soporte presentado por la empresa de turismo interesada, se
>        evaluará con los demás soportes en el momento de la respectiva solicitud de reserva


## Updated entry: booking_fees.student_admission_category

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los estudiantes y profesores de instituciones públicas o privadas en el
> marco de programas de educación ambiental desarrollados por el área
> protegida en temporada baja y con previa revisión y aprobación del jefe del
> área protegida.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> RESOLUCIÓN 551
> 
> DE 19 DE DICIEMBRE DE 2025
> 
> “Por medio de la cual se actualiza el valor de los derechos de ingreso y
> servicios complementarios a las áreas protegidas del Sistema de Parques
> Nacionales Naturales de Colombia y se unifican disposiciones.”
> 
> Para el
> Parque Nacional Natural Los Corales del Rosario y San Bernardo la
> temporada alta se contemplada para las siguientes fechas: entre el primero (1)
> de noviembre y treinta y uno (31) de enero, entre el quince (15) de junio y el
> quince (15) de agosto, semana santa.
> Consecuentemente, la temporada baja estará contemplada en las fechas que no
> se consideran temporada alta.
> Visitante: Persona autorizada por Parques Nacionales Naturales para ingresar en
> una de las áreas del Sistema de Parques Nacionales Naturales, para visitar o
> realizar una o varias de las actividades o servicios regulados por el administrador
> del Sistema en un periodo definido y continuo.
> CAPÍTULO 5
> DEROGATORIA Y VIGENCIA
> ARTÍCULO 21. – Publíquese esta resolución en el Diario Oficial y en el sitio de
> internet de Parques Nacionales Naturales de Colombia.
> Comuníquese a las
> áreas protegidas mencionadas en esta resolución, a las respectivas Direcciones
> Territoriales y a las Subdirecciones de la entidad.
> ARTÍCULO 22. – La presente resolución rige a partir del primero de enero de
> 2026 y deroga a partir de esta fecha las disposiciones que le sean contrarias,
> entre éstas, la Resolución 695 de 2024 .
> Dada en Bogotá D.C., a los 19
> 
> días del mes de diciembre de 2025.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> Los estudiantes y profesores de instituciones públicas o privadas en el
> marco de programas de educación ambiental desarrollados por el área
> protegida en temporada baja

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> numerales 2, 3, 4, 6, 9, 12, 13, 19 y 20 deberá acreditar la condición
> correspondiente con no menos de ocho (8) días calendario


## Updated entry: booking_fees.vehicle_not_parking_fee

- Reason: v2: apply the review required_change, restore the documented label, and attach the missing quote.
- Changed fields: answer, examples, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2: El valor por factor medio de transporte no constituye un servicio
> de parqueo o alquiler de estacionamiento; corresponde al derecho de ingreso
> al área protegida con un vehículo autorizado.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt`

> PARÁGRAFO 2: El valor por factor medio de transporte no constituye un servicio
> de parqueo o alquiler de estacionamiento
