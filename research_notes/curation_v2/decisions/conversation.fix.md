# conversation fix round

- conversation.greeting_hello (revise): done. Conservada la etiqueta anterior ("saludo al iniciar la conversación"). Mantiene hard negative de tarifas.
- conversation.how_are_you (revise): done. Conservada la etiqueta anterior ("preguntar cómo está el asistente"). Mantiene hard negative.
- conversation.thanks (revise): done. Conservada la etiqueta anterior ("agradecer la ayuda recibida"). Mantiene hard negative.
- conversation.goodbye (approve): done. Copiada byte a byte de v1.
- conversation.capabilities_overview (revise): done. Conservada la etiqueta anterior ("qué puedes hacer por el visitante"). Respuesta actualizada conforme a findings/critical.json y código mobile/ (mobile/src/core/tools.ts, mobile/src/state/useAssistant.ts, mobile/src/ui/strings.ts): la app no envía reportes ni solicita rescate; guía inmediata a guía/personal y al 123 si hay señal.
- conversation.first_time_help (revise): done. Conservada la etiqueta anterior ("primera vez y no sé qué preguntar"). Mantiene hard negative.
- conversation.ai_identity (approve): done. Copiada byte a byte de v1.
- conversation.language_request (revise): done. Conservada la etiqueta anterior ("pedir respuestas en otro idioma"). Mantiene hard negative.
- conversation.free_generation_limits (revise): done. Conservada la etiqueta anterior ("poemas, código o textos sin fuente"). Mantiene hard negative.
- conversation.feedback_wrong_answer (revise): done. Conservada la etiqueta anterior ("queja por una respuesta equivocada"). Mantiene hard negative.
- conversation.insults_to_assistant (revise): done. Conservada la etiqueta anterior ("insultos o groserías hacia el asistente"). Mantiene hard negative.
- conversation.park_complaint_channel (revise): done. Conservada la etiqueta anterior ("cómo presentar una queja al parque"). En auditoría se actualizó el extracto a "Canales de atención Formulario PQRSDF", citando textualmente el PQRSDF de la evidencia legada (research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www_parquesnacionales_gov_co_.txt).
- conversation.human_contact_request (approve): done. Copiada byte a byte de v1.
- conversation.joke_request (revise): done. Conservada la etiqueta anterior ("pedir un chiste al asistente"). Mantiene hard negative.
- conversation.off_topic_question (revise): done. Conservada la etiqueta anterior ("pregunta ajena al parque"). Mantiene hard negative.
- conversation.repeat_or_unclear (revise): done. Conservada la etiqueta anterior ("pedir que repita o aclare"). Mantiene hard negative.
- conversation.acknowledge_ok (revise): done. Conservada la etiqueta anterior ("confirmación corta tipo listo o ok"). Mantiene hard negative.
- conversation.cancel_topic (revise): done. Conservada la etiqueta anterior ("dejar el tema que estábamos viendo"). Mantiene hard negative.
- conversation.compliment_reply (revise): done. Conservada la etiqueta anterior ("cumplido al asistente"). Mantiene hard negative.
- conversation.more_detail_followup (revise): done. Conservada la etiqueta anterior ("pedir más detalle del tema anterior"). Mantiene hard negative.
- conversation.info_source_trust (revise): done. Conservada la etiqueta anterior ("de dónde sale la información"). En auditoría se ajustó source_status a not_checked (eliminando support none del revisor) ya que describe la trazabilidad editorial interna de la app y no un hecho externo de página SGC.
- conversation.offline_operation (revise): done. Conservada la etiqueta anterior ("uso del asistente sin internet"). Respuesta actualizada conforme a findings/critical.json y código mobile/ (mobile/src/state/settings.ts, mobile/src/state/useAssistant.ts): requiere modelo local instalado y seleccionado; sin alertas en tiempo real.
- conversation.emergency_limits (revise): done. Conservada la etiqueta anterior ("límites del asistente en emergencias"). Respuesta actualizada conforme a findings/critical.json (severidad crítica) y código mobile/ (mobile/src/core/tools.ts, mobile/src/state/useAssistant.ts): la app no llama, no envía reportes ni localiza; remite de inmediato al guía o personal y al 123 con señal; la preparación de reporte es estrictamente local en el dispositivo.
- conversation.history_storage (revise): done. Conservada la etiqueta anterior ("dónde se guarda el historial"). Respuesta actualizada conforme a findings/critical.json y código mobile/ (mobile/src/state/history.ts, mobile/src/state/useAssistant.ts): el texto de la conversación no se persiste en SQLite (solo vive en memoria de interfaz); el historial local solo conserva registros de efectos ejecutados (visita o reporte).
- conversation.no_outside_actions (revise): done. Conservada la etiqueta anterior ("llamadas, recordatorios y mensajes"). Mantiene hard negative.
- conversation.location_map_request (approve): done. Copiada byte a byte de v1.
- conversation.voice_reading_request (revise): done. Conservada la etiqueta anterior ("leer en voz alta o dictar"). Mantiene hard negative. Verificada la ausencia total de APIs de voz/micrófono en mobile/.
- conversation.opinion_request (revise): done. Conservada la etiqueta anterior ("opinión personal del asistente"). Mantiene hard negative.
- conversation.time_or_date_request (approve): done. Copiada byte a byte de v1.
- conversation.summary_request (revise): done. Conservada la etiqueta anterior ("pedir una respuesta más corta"). Mantiene hard negative.

## Findings
- critical.json conversation.emergency_limits: done. Severidad crítica atendida: el texto abre con aviso inmediato a guía/personal y llamada al 123 con señal; explicita que no llama, no envía reportes ni localiza; aclara que solo permite consultar pautas o preparar reporte local en el dispositivo (mobile/src/core/tools.ts:116-173, mobile/src/state/useAssistant.ts:124).
- critical.json conversation.capabilities_overview: done. Severidad alta atendida: elimina toda sugerencia de transmisión o despacho; remite a guía/personal y al 123 (mobile/src/core/tools.ts:116-173, mobile/src/ui/strings.ts:30-31).
- critical.json conversation.history_storage: done. Severidad media atendida: el texto del chat no se guarda en SQLite (mobile/src/state/useAssistant.ts:43); el historial local almacena únicamente registros de acciones ejecutadas (mobile/src/state/history.ts:14-32).
- critical.json conversation.offline_operation: done. Severidad alta atendida: aclara que la consulta offline requiere un modelo local instalado y seleccionado en ajustes (mobile/src/state/settings.ts:26, mobile/src/state/useAssistant.ts:70-73); no recibe alertas en tiempo real.
- actions.cross.json (conversation.emergency_limits): done. Límites de emergencia estrictamente enfocados en limitaciones técnicas del asistente sin prometer despacho de auxilio.
- conversation.cross.json: done. Mantiene las separaciones contrastivas de ai_identity vs human_contact_request, time_or_date_request en hora de dispositivo, location_map_request sin GPS/mapa en vivo, y greeting_hello como saludo puro.
- labels.json, taxonomy.json, contradictions.json, arbiter.json: declined: sin hallazgos dirigidos a la sección conversation.
- reviews/_examples.json: done. Lista drop vacía para conversation (drop: []).

## Verificación de código en mobile/
- Sin GPS ni mapas en vivo: comprobado en mobile/package.json y mobile/src/ (ausencia de módulos de geolocalización o mapas interactivos).
- Sin llamadas telefónicas ni despacho de rescate: comprobado en mobile/src/core/tools.ts (la ejecución de herramientas es un mock determinístico con letterCode local, sin conexión a servicios de emergencia) y mobile/src/state/useAssistant.ts.
- Sin entrada ni salida por voz: comprobado en mobile/src/ (sin APIs de grabación de audio, reconocimiento de voz o TTS).
- Registro local de acciones: comprobado en mobile/src/state/history.ts (SQLite gestiona únicamente la tabla history con id, at, kind, args, result para register_visit y report_emergency; los mensajes de chat son volátiles en useState de mobile/src/state/useAssistant.ts).
