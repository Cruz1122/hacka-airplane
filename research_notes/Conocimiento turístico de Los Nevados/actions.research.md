# Sección `actions`: registrar visita y reportar emergencia (corrección de revisión)

Fecha de investigación original: 2026-11-21. Corrección posterior a la revisión del coordinador: 2026-11-21.
Orden 1. Perfil de recuperación: `safety`.
Salida: `data/knowledge/sections/actions.json` (10 entradas, 131 ejemplos, 30 hard negatives).
Evidencia: `actions/evidence/` (`pnn-los-nevados.txt`, `policia-123-155.txt`, `pnn-atencion.txt`) y citas en `actions/evidence/quotes-and-mapping.md`.
Recibo de corrección: `actions/correction-receipt.md`.
Copia de la versión anterior: `coordination/round1/actions.json`.
**No ejecutar** `actions/build_actions.py`: genera el contenido anterior (sin corrección). Queda sin modificar y obsoleto.

## Clasificación

- **Hecho verificado**: leído en fuente oficial con fecha y cita literal. Ver §1 y `quotes-and-mapping.md`.
- **Texto de la app**: qué hace el flujo de registro o reporte. No tiene respaldo oficial. La app no transmite reportes ni avisa a rescate; ese límite viene del encargo del asistente offline, no de PNN ni de la Policía.
- **Vacío**: dato que no hay en fuente oficial. Ver §2.

## 1. Fuentes leídas (con fecha de lectura y cita)

| # | URL | Lectura | Fecha de publicación | Uso |
|---|---|---|---|---|
| A | https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 | 2026-11-21, texto completo | **12 mar 2023** (en la nota) | 123 como línea única de emergencias nacional; gratuita y 24 h; mal uso |
| B | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | 2026-11-21, HTML completo guardado | Sin fecha de publicación; contenido 2026 ("tarifas 2026", "© 2026") | Reserva por sector, puntos de registro e ingreso, guías registrados (equipo médico y radios) |

Notas de fecha:
- Fuente A es de marzo de 2023 y es una nota de la Policía de Meta. No la marco como no verificada solo por su antigüedad, porque no encontré contradicción oficial. Sigue sin confirmarse que el 123 esté vigente hoy con cobertura garantizada (ver §2, vacío 1).
- `last_verified` y `retrieved_at` son la fecha de mi lectura (2026-11-21), no la fecha de publicación de la fuente.

Búsqueda de corrección (2026-11-21, WebSearch estándar): devolvió fragmentos de policia.gov.co (página de 123 con descripción de línea única, 24 horas), de la CRC (2025, PDF de normatividad) y de sitios de Bogotá. **No los abrí**, así que no los cito como fuente leída. La fuente A sigue siendo la única con cita literal.

## 2. Vacíos (sin fuente oficial)

1. **Vigencia actual del 123 como número único.** Fuente A tiene 2023. La búsqueda mostró fuentes posteriores que no leí completas. Antes de publicar, confirmar en policia.gov.co o con la línea. Mientras tanto la respuesta dice "marca el 123 cuando tengas señal" y no garantiza cobertura.
2. **Línea de rescate o radio propia del parque.** B no publica ningún número de emergencia del parque. Ninguna respuesta lo inventa.
3. **Destino de un reporte de la app.** No hay evidencia de cómo PNN procesa un reporte de la app. Las respuestas dicen que la app no avisa a rescate.
4. **Número 112.** Sin fuente oficial verificada de su papel. No aparece en ninguna respuesta.
5. **Categorías oficiales de visitante.** B usa edad y residencia en tarifas. El FSM usa `nacional` y `extranjero`. No hay correspondencia oficial con `reducida`, así que no se usa en ningún slot.
6. **Hora de la llegada.** El `date` de `register_arrival_today` no se pregunta; la fecha la toma el dispositivo. Dependencia del FSM, no de fuente.

## 3. Conflictos y resolución

- **Brisas: reserva obligatoria o no.** B tiene dos líneas: 111 ("indispensable reservar… en fines de semana y puentes festivos") y 212 ("la reserva no es obligatoria… reserva con al menos un día de anticipación"). **Resolución**: no contradicen; la regla de fin de semana y festivo es más específica. La respuesta solo dice eso.
- **Reserva fuera de Brisas.** B línea 213: "la reserva sí es obligatoria" y se gestiona por la agencia registrada. Usada en `register_planned_visit`.
- **Papel del 112.** Fuentes secundarias contradictorias y no oficiales. No se usa.

## 4. Revisión del coordinador: hallazgos y resolución

Detalle por hallazgo en `actions/correction-receipt.md`. Resumen:

1. **Contradicción de no transmisión** (ejemplos: `lo envío solo si confirmas`, `no lo envío sin tu confirmación`). **Corregido en las 10 entradas** (short, variants, steps, detail). Ninguna frase dice que la app envía, guarda, sincroniza o alerta. Cada respuesta de emergencia dice que la app no avisa a rescate y remite al 123 cuando haya señal.
2. **Alcance de `report_offline_emergency`** (preguntas de capacidad mezcladas con emergencias). **Corregido**: se quitaron las preguntas sobre si la app funciona sin señal o sin datos. Quedan solo emergencias activas sin señal. Hard negatives cambiados a preguntas de otros espacios.
3. **`needs` bloqueaba seguridad** (`sector` y `people_count` antes de responder). **Corregido**: los 8 tipos de emergencia tienen `needs: []`. La respuesta de seguridad va primero; los slots se piden después en el flujo de reporte. Los `slot_questions` siguen para todas las `entity_filters`.
4. **Fuente del 123 "no verificada por antigüedad"**. **Resuelto como no bloqueante**: la fuente se conserva con su fecha en el label y en el log. El caveat de vigencia está en §2, vacío 1.
5. **Etiquetas de fuente con disclaimers largos.** **Corregido**: etiquetas cortas ("Policía Nacional · línea 123 (nota del 12 mar 2023)", "Parques Nacionales · ficha Los Nevados"). El disclaimer de que la fuente no describe la app se quitó de la etiqueta y queda aquí en el log.

Además corregí, sin que el coordinador lo señalara, lo que no tenía soporte:
- Monto de comparendo (`$926.320`): eliminado.
- Síntomas clínicos como criterio de alarma: reemplazados por "si empeora o no responde bien" (sin cifra ni síntoma específico).
- Instrucciones de protocolo ("aléjate del fuego", "sigue indicaciones del personal" ante rayos): eliminadas.
- Frases de envío o llegada a rescate en las descripciones: eliminadas.

## 5. Mapeo de semilla

- `seed_indexes` asignados en `assignments.json`: `[]`. No hay semillas que preservar.
- Los 44 temas de `conocimiento.json` no son acciones de registro o reporte. Ninguno pasa a `actions`.

## 6. Entradas y conteos finales

| id | Ejemplos | Hard negatives | needs | Inglés |
|---|---|---|---|---|
| actions.register_planned_visit | 14 | 3 | sector, date, group_size, visitor_type | 2 |
| actions.register_arrival_today | 14 | 3 | sector, group_size, visitor_type | 2 |
| actions.report_emergency_general | 13 | 3 | — | 2 |
| actions.report_injury | 13 | 3 | — | 2 |
| actions.report_lost_person | 13 | 3 | — | 2 |
| actions.report_altitude_sickness | 13 | 3 | — | 2 |
| actions.report_hypothermia | 13 | 3 | — | 2 |
| actions.report_storm | 12 | 3 | — | 2 |
| actions.report_fire | 13 | 3 | — | 2 |
| actions.report_offline_emergency | 13 | 3 | — | 2 |

Total: 10 entradas, 131 ejemplos, 30 hard negatives. `related`: 2 por entrada, todos locales. `featured`: 5 ids locales. `clarification.bank`: 6 preguntas. `clarification.slot_questions`: 6 (una por `entity_filter`). `retrieval`: `profile: safety`, `bm25_weight: 0.3`, `top_k: 2`, `min_score: null`.

Ejemplos: entre 12 y 14 por entrada; 2 en inglés por entrada; variantes con tildes, sin tildes y erratas; sin plantillas "oiga/venga/parce". Los ejemplos no se repiten entre entradas (comparación sin tildes).

## 7. Validación ejecutada

- Schema: `jsonschema` 4.26.0, draft 2020-12, contra `inputs/knowledge-section.schema.json`. **0 errores.**
- Chequeo local (`scratchpad/check_actions.py`, no guardado en el repo):
  - ids únicos y con prefijo `actions.`; etiquetas de 3 a 8 palabras;
  - 12 o más ejemplos por entrada; 2 a 4 hard negatives; no son ejemplos de la misma entrada;
  - 1 a 2 variantes; cada variante con "123" conserva "señal";
  - `related` y `featured` resuelven localmente; cada `needs` y cada `entity_filter` tiene `slot_questions`;
  - texto con dígitos tiene `last_verified`;
  - sin frases prohibidas: "envío", "enviar", "lo envío", "GPS", "ya quedó", "sincroniz", "guardado", "garantiz".
  - **Resultado: 0 problemas.** El único aviso previo ("english count") era falso positivo de la heurística y se recontó a mano: 2 por entrada.
- Duplicados entre secciones: 0 ejemplos de `actions` aparecen en otro archivo final.
- **No verificado**: similitud coseno de embeddings (no ejecutado en este entorno).

## 8. Hard negatives entre secciones (pendiente de cierre)

Los hard negatives deben ser ejemplos reales de otra entrada o quedar marcados para revisión (contrato, regla 3). Estado en el momento de la corrección:

- Confirmado en la sección final de `hours_status`: `a qué hora abren` (1 de 30).
- No encontrado todavía en las secciones finales (las demás siguen revisándose en paralelo): 29 de 30. Lista en `actions/correction-receipt.md`, sección "Pendientes de cierre".

Acción para el coordinador: al cerrar todas las secciones, revisar esos 29 textos contra los ejemplos finales. Los que no existan se reemplazan por ejemplos existentes o se marcan para revisión. No he creado ejemplos de otras secciones para completar esto.

## 9. Pendientes para el coordinador

1. Confirmar la vigencia del 123 en policia.gov.co o con la línea antes de publicar (§2, vacío 1).
2. Cerrar los 29 hard negatives entre secciones (§8).
3. Decidir si `actions/build_actions.py` se borra o se archiva. Lo dejé sin tocar porque genera la versión anterior.

## 10. Incidencias del proceso

- Llamada accidental a `mcp__t3-code__request_secret` con valor de prueba `noop` en la investigación original. Creó un archivo fuera del workspace (`/home/cruz1122/.t3/userdata/secrets/files/2212dfa78ef3fb09eb3a6b641ab8d04b`). No contiene datos del proyecto. No lo borré; queda para decisión del usuario.
- No hay WebFetch en la sesión. Las páginas se leyeron desde archivos descargados con `curl`. No usé subagentes en la corrección.

## Coordinator final sample

The corrected five-entry sample no longer promises transmission. Offline emergency advice now prioritizes informing the guide and conditions obtaining signal on avoiding additional danger. Emergency numbers must never be called merely to test a dataset. Cross-section hard negatives remain queued for final review, not proof of missing positive-topic coverage.

## Round 2 (2026-11-21): auditoría de citas

Alcance: solo auditoría. Entradas 10 → 10; ejemplos 131 → 131; hard negatives 30 → 30. Sin entradas añadidas ni eliminadas.

**Reescritas (2 entradas, por falta de respaldo o de precisión):**
- `actions.register_planned_visit` (paso 2): la versión anterior aplicaba la regla de reserva obligatoria de fin de semana a "Brisas-Kumanday". La ficha tiene dos líneas: la 111 (sector "Brisas–Valle de las Tumbas"): reserva indispensable en fines de semana y puentes festivos; la 212 (sector "Brisas-Kumanday"): no obligatoria, con un día de anticipación recomendado. Ahora se citan ambas, cada una con su alcance.
- `actions.report_emergency_general` (detalle): "puede impedir la atención" → "puede evitar la atención", el texto de la Policía.

**Descargas (URL → archivo):**
- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 → `actions/evidence/raw/policia-123-155.html` y `.txt`
- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ → `actions/evidence/raw/pnn-los-nevados.html` y `.txt` (registro e ingreso, reservas, guías)

**Verificación:** `actions/check_quotes.py`: 15 citas, 0 fallos. Validador: `Errors: 0`. Los 28 `hard_negative_review` de `actions` son heredados del snapshot; no se añadieron nuevos.

**Archivos nuevos:** `actions/evidence/quotes.md`, `actions/check_quotes.py`, `actions/source/overlay.py`. `actions/build_actions.py` sigue sin ejecutar (genera la versión anterior).

**Vacíos y riesgos:**
1. Vigencia del 123: la nota es del 12 de marzo de 2023. No hay confirmación oficial posterior.
2. "marca el 123 cuando tengas señal" y "avisa a tu guía": instrucciones operativas sin fuente oficial. El número y la capacidad del guía sí están citados.
3. Nombres de Brisas: la ficha usa "Brisas–Valle de las Tumbas" y "Brisas-Kumanday". No confirmé que sean el mismo recorrido.
4. "La app no avisa a rescate": límite de la app, no dato de fuente. Ningún answer promete envío de datos.
5. 28 hard negatives sin ejemplo en ninguna sección: quedan para reemplazo por ejemplos existentes.


## Updated entry: actions.register_arrival_today

- Reason: Drop the contrast order, and stop saying the app completes official entry; the screen stores a local record and hours depend on the park's registration points.
- Changed fields: answer, hard_negatives, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Los horarios dependen del sector ecoturístico que quieras visitar y de los puntos de registro e ingreso del Parque:


## Updated entry: actions.register_planned_visit

- Reason: Date the ficha rules, keep Brisas-Valle de las Tumbas distinct from Brisas-Kumanday, and say the app screen is a local record, not a Parques Nacionales booking.
- Changed fields: answer, hard_negatives, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Los horarios dependen del sector ecoturístico que quieras visitar y de los puntos de registro e ingreso del Parque:

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Para el recorrido Brisas–Valle de las Tumbas (zona norte del Parque Nacional Natural Los Nevados) en fines de semana y puentes festivos, es indispensable reservar con al menos un día de anticipación para asegurar tu ingreso. Hazlo en: www.reservasnevados.com

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Ingreso al sector Brisas-Kumanday: la reserva no es obligatoria. Sin embargo, para asegurar tu ingreso (ya que los cupos diarios son limitados), reserva con al menos un día de anticipación. Reserva para este atractivo en: www.reservasnevados.com

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Ingreso a los demás sectores: la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> Si vas a visitar el atractivo Brisas–Valle de las Tumbas del Parque Nacional Natural Los Nevados, durante el mes de noviembre ten presente el Pico y Placa Ambiental emitido por la Secretaría de Tránsito y Transporte del Tolima, mediante la Resolución No. 1815 del 24 de julio de 2026, el cual aplica para fines de semana y puentes festivos con horario de restricción de 5:00 a. m. a 4:00 p. m.


## Updated entry: actions.report_altitude_sickness

- Reason: Separate an altitude-sickness report from children's symptoms and from hypothermia; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_emergency_general

- Reason: Date the 123 institutional claim to the 12 March 2023 police note and label the app handoff.
- Changed fields: answer, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_fire

- Reason: Separate a fire report from a past páramo fire and from a generic emergency; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_hypothermia

- Reason: Separate the hypothermia report from first-aid questions; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_injury

- Reason: Separate an injury report from an environmental complaint and from first aid; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_lost_person

- Reason: Separate a missing person from a lost object and from the speaker being lost; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.


## Updated entry: actions.report_offline_emergency

- Reason: Keep the no-signal report distinct from CPR and from calling 123, and date the 123 instruction.
- Changed fields: answer, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.


## Updated entry: actions.report_storm

- Reason: Separate a storm report from snow, hail and lightning first aid; date the 123 instruction.
- Changed fields: answer, examples, hard_negatives, label, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> 12 March, 2023
> Estas líneas se encuentran a disposición las 24 horas del día, los siete días de la semana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> La Línea de emergencia 123, es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año; esta permite la atención de manera oportuna de cualquier requerimiento ciudadano en tema de seguridad y convivencia ciudadana.

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`

> el mal uso de la línea puede evitar la atención de una emergencia real.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`

> En el Parque Nacional Natural Los Nevados es obligatorio el servicio de acompañamiento y guianza en todos los sectores. Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.
