# Registro de decisiones del curador: sección `conversation` (Agente 16)

Fecha: 2026-11-22.
Sección: `conversation` (orden 15).
Alcance: 30 entradas (saludos, agradecimientos, despedidas, capacidades, límites del asistente).

## 1. Operaciones en la propuesta (`proposals/conversation.json`)

1. `conversation.greeting_hello` | `update` | Ajuste de etiqueta a 'saludo y bienvenida al iniciar la conversación' y adición de hard negative de tarifas para blindar contra saludos con preguntas incrustadas | metadata-only
2. `conversation.how_are_you` | `update` | Clarificación de etiqueta a 'preguntar por el estado del asistente' y adición de hard negative contrastivo | metadata-only
3. `conversation.thanks` | `update` | Precisión de etiqueta a 'agradecer la atención y ayuda recibida' y hard negatives contra cumplidos | metadata-only
4. `conversation.goodbye` | `update` | Refuerzo de hard negatives frente a cancelación de tema (`no, cambiemos de tema`) para resolver confusión mutua | metadata-only
5. `conversation.capabilities_overview` | `update` | Diferenciación de etiqueta frente a weather_volcano ('funciones generales y capacidades del asistente') y refuerzo de hard negatives | metadata-only
6. `conversation.first_time_help` | `update` | Etiqueta específica ('orientación inicial para quien visita por primera vez') y hard negative frente a capacidades | metadata-only
7. `conversation.ai_identity` | `update` | Etiqueta contrastiva ('aclarar si el asistente es robot o persona') y hard negative frente a solicitud de hablar con persona | metadata-only
8. `conversation.language_request` | `update` | Precisión de etiqueta ('solicitar respuestas o traducción en otro idioma') y contraste con elaboración | metadata-only
9. `conversation.free_generation_limits` | `update` | Etiqueta clara ('solicitar generación de poemas código o cuentos') y contraste con llamadas y chistes | metadata-only
10. `conversation.feedback_wrong_answer` | `update` | Etiqueta específica ('reportar una respuesta errada de la aplicación') y contraste con insultos | metadata-only
11. `conversation.insults_to_assistant` | `update` | Etiqueta precisa ('expresar insultos o frustración hacia el asistente') y contraste con feedback | metadata-only
12. `conversation.park_complaint_channel` | `update` | Etiqueta formal ('cómo presentar un reclamo o queja formal') y contraste con canales informales | research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_.txt
13. `conversation.human_contact_request` | `update` | Etiqueta diferenciada ('contactar o hablar con personal del parque') y hard negative frente a identidad de robot | research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_.txt
14. `conversation.joke_request` | `update` | Etiqueta específica ('pedir un chiste o comentario gracioso') y contraste con poemas y mensajes | metadata-only
15. `conversation.off_topic_question` | `update` | Etiqueta de descarte ('preguntas fuera del tema del parque nacional') y hard negative frente a hora | metadata-only
16. `conversation.repeat_or_unclear` | `update` | Etiqueta precisa ('pedir que repita o aclare la respuesta') y hard negative frente a resumen | metadata-only
17. `conversation.acknowledge_ok` | `update` | Etiqueta específica ('confirmación corta como listo entendido o bien') y contraste con cumplidos | metadata-only
18. `conversation.cancel_topic` | `update` | Etiqueta diferenciada ('cancelar o cambiar el tema de conversación') y hard negative frente a despedidas | metadata-only
19. `conversation.compliment_reply` | `update` | Etiqueta específica ('responder a un elogio o felicitación') y contraste con estado del asistente | metadata-only
20. `conversation.more_detail_followup` | `update` | Etiqueta precisa ('pedir más detalles o ampliación del tema') y contraste con petición de brevedad | metadata-only
21. `conversation.info_source_trust` | `update` | Etiqueta clara ('de qué fuentes proviene la información oficial') y contraste con idioma | research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www2_sgc_gov_co_Noticias_Paginas_Boletines-semanales_aspx.txt
22. `conversation.offline_operation` | `update` | Etiqueta específica ('uso y funcionamiento del asistente sin internet') y contraste con mapa y auxilio | metadata-only
23. `conversation.emergency_limits` | `update` | Etiqueta delimitada ('alcance y limitaciones del asistente en emergencias') y contraste con reporte activo | metadata-only
24. `conversation.history_storage` | `update` | Etiqueta precisa ('dónde se guardan los datos e historial') y contraste con registro en entrada | metadata-only
25. `conversation.no_outside_actions` | `update` | Etiqueta delimitada ('límites para hacer llamadas mensajes o alarmas') y contraste con humano | metadata-only
26. `conversation.location_map_request` | `update` | Etiqueta específica ('solicitar ubicación gps o mapa en vivo') y contraste con rutas | metadata-only
27. `conversation.voice_reading_request` | `update` | Etiqueta clara ('solicitar lectura de voz o usar micrófono') y contraste con mensajes | metadata-only
28. `conversation.opinion_request` | `update` | Etiqueta delimitada ('pedir una opinión o sugerencia al asistente') y contraste con capacidades | metadata-only
29. `conversation.time_or_date_request` | `update` | Etiqueta contrastiva ('consultar la hora actual o la fecha') y contraste con horarios de apertura | metadata-only
30. `conversation.summary_request` | `update` | Etiqueta precisa ('pedir una respuesta resumida y corta') y contraste con ampliación de tema | metadata-only

## 2. Entradas marcadas como not_checked

27 entradas se clasificaron como `not_checked` en `audit/conversation.csv`. Estas corresponden a interacciones puramente conversacionales (saludos, gracias, despedidas, insultos, confirmaciones, chistes, off-topic) o afirmaciones sobre el alcance técnico del asistente móvil. Las reglas de curaduría exigen que `primary_ok` se reserve exclusivamente para afirmaciones contrastadas con fragmentos textuales idénticos en fuentes de evidencia web fijadas (disponibles para los canales oficiales de PNN y SGC en `park_complaint_channel`, `human_contact_request` e `info_source_trust`). La conducta del asistente se comprobó directamente en el repositorio (`mobile/src/state/history.ts`, `mobile/app/history.tsx`, `mobile/src/core/tools.ts`, `mobile/src/state/useAssistant.ts`).

## 3. Brechas factuales identificadas

- `conversation.history_storage`: La respuesta actual indica que "La app guarda esta conversación en tu teléfono. Si quieres volver a leerla, ábrela ahí en la app." Sin embargo, la inspección del código en `mobile/src/state/history.ts` y `mobile/app/history.tsx` demuestra que la base de datos local SQLite (`nevados.db`) únicamente persiste los efectos secundarios de herramientas (`register_visit` y `report_emergency`), mientras que el historial de texto conversacional se gestiona en memoria volátil de sesión React (`useState`) y se reinicia al salir. Se documenta para revisión técnica y editorial de la app.

## 4. Fuentes que fallaron en descarga

Ninguna. No se requirieron descargas web externas para operaciones de metadatos, y las 3 fuentes oficiales de canales PNN y boletines SGC se verificaron contra los archivos de evidencia legada fijados en `legacy_evidence_manifest.json`.

## 5. Hallazgos inter-sección (`findings/conversation.cross.json`)

1. Límites en emergencias vs reporte de emergencia: `conversation.emergency_limits` se enfoca en el alcance técnico y limitaciones de la app offline, evitando solaparse con `actions.report_emergency_general` ni con protocolos de `health_safety`.
2. Reloj vs horarios: `conversation.time_or_date_request` atiende la pregunta por la hora/fecha del dispositivo, contrastada frente a `hours_status.general_opening_schedule`.
3. Mapas en app vs orientación de ruta: `conversation.location_map_request` clarifica que la app no incluye GPS ni mapa dinámico, diferenciándose de las guías de navegación en `preparation`.
4. Hablar con humano vs identidad virtual: `conversation.human_contact_request` y `conversation.ai_identity` se separan netamente en etiquetas y negativos duros.
5. Saludos con pregunta incrustada: Se confirmó que ninguna entrada de `conversation` contiene preguntas sustantivas del parque incrustadas en saludos, protegiendo el enrutamiento hacia `booking_fees`, `access` y demás secciones temáticas.
