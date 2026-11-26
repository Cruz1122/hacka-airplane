# Investigación: sección `conversation` (orden 15)

Fecha de trabajo: 2026-11-21. Salida: `data/knowledge/sections/conversation.json`.
Generador y validador (propiedad de esta sección): `conversation/build_section.py`, `conversation/validate_section.py`.
Evidencia descargada: `conversation/evidence/` (3 páginas oficiales, ver §1).

## Resumen

- Entradas: **29** (meta del prompt: 30). Quedé una por debajo porque las intenciones distintas de conversación se agotaron; no partí intenciones casi idénticas para inflar el conteo.
- Ejemplos: **362** (≥12 por entrada, sin repetidos dentro de la sección). 2–3 negativos duros por entrada.
- Validación: `validate_section.py` → esquema adjunto (JSON Schema 2020-12) + reglas del contrato: 0 errores, 0 advertencias. Sin colisiones de ejemplos ni de etiquetas con las cinco secciones ya presentes (`health_safety`, `weather_volcano`, `rules`, `actions`, `booking_fees`).
- Semilla: **ningún tema semilla asignado** (`assigned seed indexes: []`). No hay mapeo de índices a IDs. Ninguno de los 44 temas de `conocimiento.json` pertenece a conversación.
- Cifras en respuestas: **ninguna**. Por eso no hay `last_verified` en la mayoría de entradas; tres entradas (`park_complaint_channel`, `human_contact_request`, `info_source_trust`) lo llevan porque citan un canal oficial verificado el 2026-11-21.

## Distinción de tipos de afirmación

- **Hecho verificado**: leído en una fuente oficial o en código del repositorio, con cita.
- **Inferencia**: deducción desde código o arquitectura, sin prueba de comportamiento en el teléfono.
- **Texto editorial**: redacción del asistente. No es comunicación oficial de Parques Nacionales ni de nadie más. Sus `sources` llevan la etiqueta "Texto editorial del asistente; no es comunicación oficial de PNN" y apuntan a la página del parque solo como referencia de contexto.
- **Vacío**: dato que no se encontró o no se verificó.

## 1. Fuentes consultadas

Fecha de consulta de todas: 2026-11-21 (descarga con `curl`, agente de usuario genérico).

| # | URL | Resultado | Publicación / fecha visible | Uso |
|---|---|---|---|---|
| 1 | https://www.parquesnacionales.gov.co/ | 200, leído (`evidence/www_parquesnacionales_gov_co_.html`) | No consta fecha de publicación de la página de inicio | Menú "Formulario PQRSDF" y "Canales de atención"; bloque de contacto del conmutador. Soporta `park_complaint_channel`, `human_contact_request`, `info_source_trust`. |
| 2 | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | 200, leído (`evidence/www_parquesnacionales_gov_co_nuestros-parques_parque-nacional-natural-los-nevados_.html`) | No consta | Contexto del parque. Texto: "Estado del parque: Abierto" (dinámico, **no usado**). Texto: "Si necesitas más información, comunícate directamente con el Parque" (correo ofuscado en la página; **no copiado**). Se cita como referencia de contexto en las entradas editoriales. |
| 3 | https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx | 200, leído (`evidence/www2_sgc_gov_co_Noticias_Paginas_Boletines-semanales_aspx.html`), título "Boletines Semanales" | No consta en la página | Índice oficial de boletines. Soporta `info_source_trust` (remitir al SGC para alertas). |
| 4 | https://www.parquesnacionales.gov.co/contacto/ | **Fallo**: redirigió a un dominio no relacionado (mystyc.me). Archivo descartado y eliminado. | — | No usado. Esto es un fallo de recuperación, no una verificación. |
| 5 | Búsqueda web "Parque Nacional Natural Los Nevados parquesnacionales.gov.co" | Solo fragmentos (snippets); no se abrieron los documentos enlazados | Documentos 2017, 2023, 2026 según títulos | Se usaron solo para orientarse (plan de manejo, reglamentación transitoria). No se citó ningún dato de ellos. |
| 6 | Búsqueda web "Servicio Geológico Colombiano Nevado del Ruiz boletín semanal alerta" | Solo fragmentos; PDFs no abiertos | Último boletín en resultados: 22–28 sep 2026 | **No usado** para afirmar nivel de alerta (ver §3). |
| 7 | Código del repositorio (lectura, sin ejecución) | `mobile/package.json`, `mobile/src/state/history.ts`, `mobile/src/state/settings.ts`, `mobile/src/core/driver.ts` (líneas 108, 470, 481), `src/nevados_bench/fsm/prompts.py` (línea 94), `docs/project-context.md` | — | Ver tabla de soporte abajo. |

### Hechos verificados con cita (soporte por entrada)

- "Formulario PQRSDF" aparece en el menú de https://www.parquesnacionales.gov.co/ (fuente 1). → `conversation.park_complaint_channel`.
- "Canales de atención" aparece en el menú y en el pie de la misma página (fuente 1). → `conversation.human_contact_request`.
- Índice "Boletines Semanales" existe en https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx (fuente 3). → `conversation.info_source_trust`.
- La app guarda datos en SQLite local: `mobile/src/state/history.ts` importa `expo-sqlite`; `mobile/src/state/settings.ts` usa `expo-sqlite/kv-store`. Inferencia: el historial queda en el teléfono (no se probó en dispositivo). → `conversation.history_storage` (con etiqueta de inferencia en esta log).
- La app no declara módulos de ubicación, micrófono ni voz: búsqueda de `expo-location`, `navigator.geolocation`, `expo-av`, `expo-speech`, `microphone` en `mobile/package.json` y `mobile/src` sin resultados. Esto es ausencia de dependencia, no prueba exhaustiva. → `conversation.location_map_request`, `conversation.voice_reading_request`.
- `docs/project-context.md`: solo dos herramientas con efecto secundario, `register_visit` y `report_emergency`. → `conversation.no_outside_actions`, `conversation.capabilities_overview`, `conversation.emergency_limits`.
- `docs/project-context.md`: "Chat mode (default on) gives free replies when no tool applies." → motiva el cuidado con `conversation.free_generation_limits` (ver conflictos).
- Respuestas curadas en español (`README.md` de inputs, contrato: `answer.short` en español). → `conversation.language_request` (texto editorial, ver conflictos).

## 2. Vacíos (datos no encontrados de fuente oficial)

- **Idioma de respuesta del asistente**: el código dice "en el idioma del visitante" (`driver.ts:108`, `driver.ts:470`; `prompts.py:94`), pero el contenido curado es español. Falta confirmar en la app qué pasa con una pregunta en inglés. Las respuestas de `language_request` no prometen traducción.
- **Respuesta a poemas o código en modo chat libre**: no se probó qué genera el modelo libre. La entrada `free_generation_limits` describe el alcance del asistente, no una prueba del modelo.
- **Borrado del historial**: no encontré en el código una acción de borrado visible para el visitante. La entrada no promete borrarlo.
- **Contacto de la oficina de Manizales**: el fragmento de búsqueda menciona "Calle 69A No 24-69", pero no abrí la fuente que lo contiene y no está en la página del parque que leí. Por eso no aparece en ninguna respuesta. Se requiere confirmación oficial antes de usarlo.
- **Teléfonos y horarios de atención**: la página de inicio muestra un conmutador, una línea gratuita y un horario de atención. No los usé en conversación (la sección no debe llevar cifras); quedan disponibles para `services` o `booking_fees`, con `last_verified` 2026-11-21 y fuente 1.
- **Estado del parque (abierto/cerrado)**: la página dice "Abierto", pero es un estado dinámico sin fecha de verificación útil. No se usa en ninguna entrada.
- **Nivel de alerta del volcán**: los fragmentos de búsqueda mencionan alerta amarilla con boletines hasta el 22–28 sep 2026. No abrí esos PDFs ni confirmé un boletín posterior al 21 de noviembre. No se afirma ningún nivel de alerta.

## 3. Conflictos entre fuentes y resolución

1. **Idioma**: código sugiere responder en el idioma del visitante; contrato y contenido curado son en español. **Resolución**: la entrada `language_request` dice que las respuestas están en español y no promete traducción. Marcado como texto editorial a validar en la app.
2. **Modo chat libre vs. alcance**: `project-context.md` dice que el chat libre responde cuando ninguna herramienta aplica, lo que puede incluir textos creativos. El contrato prohíbe prometer generación libre. **Resolución**: la respuesta de `free_generation_limits` solo describe la función del asistente ("me enfoco en datos del parque"), sin afirmar qué hace el modelo. Esto es editorial y necesita prueba en el teléfono.
3. **Alerta del volcán**: los fragmentos de búsqueda dan alerta amarilla y boletines hasta septiembre 2026; la fecha actual es 2026-11-21, así que el dato puede estar desactualizado y no es verificable desde aquí. **Resolución**: no se afirma ningún nivel. La entrada `info_source_trust` remite al índice del SGC. Para `weather_volcano`: hace falta confirmar el boletín más reciente.
4. **Contacto del parque**: la búsqueda menciona un teléfono y un correo que no coinciden con la página del parque que leí. **Resolución**: no se publica ninguno de los dos. Las entradas remiten a los canales oficiales.
5. **Restricción de acceso norte en la página del parque**: la página menciona "Resolución No. 1815 del 24 de julio de 2026", emitida por la Secretaría de Tránsito y Transporte del Tolima, para pico y placa ambiental en fines de semana y festivos (5:00 a. m. a 4:00 p. m.). **No se usa en conversación**. Se deja como observación para los responsables de `access` y `hours_status`, que deben verificar vigencia en la fuente antes de usarla.

## 4. Temas descartados y motivos

- **Información del parque en conversación** (altura, clima, fauna, reglas, precios, horarios): pertenece a sus secciones. Aquí solo hay redirecciones.
- **Teléfonos de emergencia**: pertenecen a `health_safety`; aquí solo se remite a esa sección y a `report_emergency`.
- **Estado abierto/cerrado del parque y alerta del volcán**: dinámicos y no verificados con fecha; se remiten a la fuente oficial.
- **Teléfono, correo y dirección de la oficina de Manizales**: no confirmados; ver §2.
- **Traducción, voz, recordatorios, llamadas, mapa y GPS**: fuera de las funciones de la app (ver §1, fuente 7). Se dicen explícitamente como límites.
- **Nombre del creador o del asistente**: no hay dato verificado; la entrada `ai_identity` no nombra a nadie.
- **Chistes con contenido del parque**: no hay fuente. Se descartó inventar datos curiosos; el chiste se redirige a fauna, flora o historia.
- **Opiniones personales**: se responde con alcance, sin opinión.
- **Preguntas de "¿qué día y hora es?"**: sin reloj confiable offline; se remite al teléfono y a la página oficial para horarios.

## Mapeo de semilla

Ningún índice asignado (`[]`). Ningún tema de `conocimiento.json` se mapea a esta sección. Todos los temas de conversación de la tabla del prompt (saludos, gracias, despedidas, "qué puedes hacer", "eres un robot", cambio de idioma, quejas, chistes) están cubiertos en esta sección como entradas nuevas.

## Lista final de entradas (29)

| id | etiqueta | tipo |
|---|---|---|
| conversation.greeting_hello | saludo al iniciar la conversación | chat |
| conversation.how_are_you | preguntar cómo está el asistente | chat |
| conversation.thanks | agradecer la ayuda recibida | chat |
| conversation.goodbye | despedida al terminar la conversación | chat |
| conversation.capabilities_overview | qué puedes hacer por el visitante | chat |
| conversation.first_time_help | primera vez y no sé qué preguntar | chat |
| conversation.ai_identity | si el asistente es un robot | chat |
| conversation.language_request | pedir respuestas en otro idioma | rule |
| conversation.free_generation_limits | poemas, código o textos sin fuente | chat |
| conversation.feedback_wrong_answer | queja por una respuesta equivocada | chat |
| conversation.insults_to_assistant | insultos o groserías hacia el asistente | chat |
| conversation.park_complaint_channel | cómo presentar una queja al parque | procedure |
| conversation.human_contact_request | hablar con una persona del parque | procedure |
| conversation.joke_request | pedir un chiste al asistente | chat |
| conversation.off_topic_question | pregunta ajena al parque | chat |
| conversation.repeat_or_unclear | pedir que repita o aclare | chat |
| conversation.acknowledge_ok | confirmación corta tipo listo o ok | chat |
| conversation.cancel_topic | dejar el tema que estábamos viendo | chat |
| conversation.compliment_reply | cumplido al asistente | chat |
| conversation.more_detail_followup | pedir más detalle del tema anterior | chat |
| conversation.info_source_trust | de dónde sale la información | explanation |
| conversation.offline_operation | uso del asistente sin internet | explanation |
| conversation.emergency_limits | límites del asistente en emergencias | safety |
| conversation.history_storage | dónde se guarda el historial | explanation |
| conversation.no_outside_actions | llamadas, recordatorios y mensajes | chat |
| conversation.location_map_request | pedir tu ubicación o un mapa | chat |
| conversation.voice_reading_request | leer en voz alta o dictar | chat |
| conversation.opinion_request | opinión personal del asistente | chat |
| conversation.time_or_date_request | preguntar la hora o el día | chat |

Nota de conteo: 29 < 30. Quedó una intención por debajo porque no encontré una intención conversacional distinta y útil que no fuera casi copia de otra. No se añadió relleno.

## Limitación de metadatos editoriales (para el coordinador)

Las entradas de tipo `chat` o `explanation` que describen la app no tienen una fuente oficial que las respalde. Para cumplir el esquema, sus `sources` usan la página del parque o el portal de PNN **con una etiqueta explícita de texto editorial**. Eso no implica que PNN avale el comportamiento de la app. Las entradas que sí citan un canal oficial (`park_complaint_channel`, `human_contact_request`, `info_source_trust`) llevan la etiqueta oficial y `last_verified`. Antes de la demo conviene que el equipo de la app confirme las afirmaciones de `language_request`, `free_generation_limits`, `history_storage`, `offline_operation` y `location_map_request`.

## Observaciones para otros responsables (no modificadas)

- `access` / `hours_status`: revisar la Resolución 1815 del 24 de julio de 2026 citada en la página del parque (fuente 2) antes de usarla.
- `weather_volcano`: los boletines del SGC encontrados llegan hasta el 22–28 sep 2026; confirmar el boletín vigente.
- `services` / `booking_fees`: el conmutador y el horario de atención de la página de inicio (fuente 1) están disponibles con fecha de consulta 2026-11-21.

## Coordinator correction

On 2026-11-21, ambiguous location examples were narrowed to explicit app/GPS/map capability questions. Generic “where am I” must not divert a potentially lost visitor from safety clarification. The action and safety sections retain priority.

## Round 2 (2026-11-21): auditoría de hechos y expansión

Entradas 29 → 30; ejemplos 362 → 376; hard negatives 83 → 86.

**Hechos del parque en respuestas:** ninguna respuesta da cifra, regla ni lugar del parque. Quedan el nombre del parque (`greeting_hello`) y punteros a canales oficiales (`park_complaint_channel`, `human_contact_request`, `info_source_trust`). Las citas están en `conversation/evidence/quotes.md` y `conversation/check_quotes.py`: 6 citas, 0 fallos.

**Reescrita:** `conversation.repeat_or_unclear`. Sus ejemplos piden repetir o simplificar la respuesta del asistente ("repite por favor", "explícamelo de nuevo", "puedes decirlo más fácil"), pero la respuesta pedía al usuario reformular su pregunta. Ahora ofrece repetir el texto preparado y dice que no hay una versión más sencilla. La app no reescribe respuestas.

**Añadida:** `conversation.summary_request` ("pedir una respuesta más corta"). Ninguna sección tenía ejemplos con resumen, corto, breve ni "al grano". 14 ejemplos, 2 en inglés, 3 hard negatives existentes. Cero flags del validador.

**Decisiones:**
- "Hablar más despacio" no se añadió: la app no tiene voz y "voz" ya lo cubre `voice_reading_request`.
- `history_storage`: verificado en código. `mobile/src/state/history.ts` guarda en SQLite (`nevados.db`) en el dispositivo.

**Descargas:** `https://pqrsd.parquesnacionales.gov.co/principal` → `conversation/evidence/pqrsd-principal.html`. Es una aplicación de una sola página; el texto extraído es solo el título, así que no sirve como cita.

**Vacíos y riesgos:**
1. Formulario PQRSDF: la única fuente citable es la portada (`https://www.parquesnacionales.gov.co/`). No hay URL profunda verificable.
2. 81 `hard_negative_review` heredados en `conversation`. No se añadieron nuevos.


## Updated entry: conversation.acknowledge_ok

- Reason: Restore label from snapshot per review: confirmación corta tipo listo o ok. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.ai_identity

- Reason: Clarify label and strengthen contrastive hard negatives for conversation.ai_identity.
- Changed fields: hard_negatives, label


## Updated entry: conversation.cancel_topic

- Reason: Restore label from snapshot per review: dejar el tema que estábamos viendo. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.capabilities_overview

- Reason: Critical fix per findings/critical.json: app does not transmit reports or dispatch rescue; direct to guide/123. Restore label per review.
- Changed fields: answer, hard_negatives, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_nuestros-parques_parque-nacional-natural-los-nevados_.txt`

> Parque Nacional Natural Los Nevados • Parques Nacionales Naturales de Colombia

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/health_safety/evidence/raw/policia_123.html`

> es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año


## Updated entry: conversation.compliment_reply

- Reason: Restore label from snapshot per review: cumplido al asistente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.emergency_limits

- Reason: Critical fix per findings/critical.json: state app does not call/locate/transmit, direct to guide and 123, clarify local preparation only. Restore label per review.
- Changed fields: answer, hard_negatives, last_verified, sources

- https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/health_safety/evidence/raw/policia_123.html`

> es la línea única de emergencias Nacional, que permite que en un sólo número los colombianos puedan acceder a todos los servicios de emergencia y seguridad que ofrece el Estado gratuitamente las 24 horas del día todos los días del año


## Updated entry: conversation.feedback_wrong_answer

- Reason: Restore label from snapshot per review: queja por una respuesta equivocada. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.first_time_help

- Reason: Restore label from snapshot per review: primera vez y no sé qué preguntar. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.free_generation_limits

- Reason: Restore label from snapshot per review: poemas, código o textos sin fuente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.goodbye

- Reason: Clarify label and strengthen contrastive hard negatives for conversation.goodbye.
- Changed fields: hard_negatives


## Updated entry: conversation.greeting_hello

- Reason: Restore label from snapshot per review: saludo al iniciar la conversación. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.history_storage

- Reason: Fix per findings/critical.json: chat text is not persisted in SQLite history; history stores only local action records. Restore label per review.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_nuestros-parques_parque-nacional-natural-los-nevados_.txt`

> Parque Nacional Natural Los Nevados • Parques Nacionales Naturales de Colombia


## Updated entry: conversation.how_are_you

- Reason: Restore label from snapshot per review: preguntar cómo está el asistente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.human_contact_request

- Reason: Clarify label and strengthen contrastive hard negatives for conversation.human_contact_request.
- Changed fields: hard_negatives, label


## Updated entry: conversation.insults_to_assistant

- Reason: Restore label from snapshot per review: insultos o groserías hacia el asistente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.joke_request

- Reason: Restore label from snapshot per review: pedir un chiste al asistente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.language_request

- Reason: Restore label from snapshot per review: pedir respuestas en otro idioma. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.location_map_request

- Reason: Clarify label and strengthen contrastive hard negatives for conversation.location_map_request.
- Changed fields: hard_negatives, label


## Updated entry: conversation.more_detail_followup

- Reason: Restore label from snapshot per review: pedir más detalle del tema anterior. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.no_outside_actions

- Reason: Restore label from snapshot per review: llamadas, recordatorios y mensajes. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.off_topic_question

- Reason: Restore label from snapshot per review: pregunta ajena al parque. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.offline_operation

- Reason: Fix per findings/critical.json: offline operation requires local model installed and selected; no real-time alerts. Restore label per review.
- Changed fields: answer, hard_negatives, last_verified

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_nuestros-parques_parque-nacional-natural-los-nevados_.txt`

> Parque Nacional Natural Los Nevados • Parques Nacionales Naturales de Colombia


## Updated entry: conversation.opinion_request

- Reason: Restore label from snapshot per review: opinión personal del asistente. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.repeat_or_unclear

- Reason: Restore label from snapshot per review: pedir que repita o aclare. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.summary_request

- Reason: Restore label from snapshot per review: pedir una respuesta más corta. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.thanks

- Reason: Restore label from snapshot per review: agradecer la ayuda recibida. Maintain contrastive hard negatives.
- Changed fields: hard_negatives


## Updated entry: conversation.time_or_date_request

- Reason: Clarify label and strengthen contrastive hard negatives for conversation.time_or_date_request.
- Changed fields: hard_negatives, label


## Updated entry: conversation.voice_reading_request

- Reason: Restore label from snapshot per review: leer en voz alta o dictar. Maintain contrastive hard negatives.
- Changed fields: hard_negatives
