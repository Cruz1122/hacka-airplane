# Clima y actividad volcánica

## Fuentes consultadas y evidencia

Fecha de consulta de todas las URLs: 2026-11-21. La ficha HTML de Parques Nacionales no mostró fecha de publicación o actualización visible en el contenido consultado.

- [Parques Nacionales Naturales de Colombia — PNN Los Nevados](https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/) — respuesta HTTP 200; descargué y leí la ficha completa (texto extraído guardado en `weather_volcano/evidence/pnn-page-extracted.txt`). La sección “Clima” dice: “El Parque se caracteriza por tener dos periodos de lluvias y dos secos a lo largo del año (régimen de precipitación bimodal). La temperatura es variable debido a estos cambios de estación y a los pisos térmicos producto de su topografía montañosa.” Apoya `park_climate`, `bimodal_rainfall`, `seasonal_weather` y `weather_by_elevation`. La ficha también recomienda revisar la variación de condiciones y no asegura visibilidad de la cumbre; `summit_visibility` se limita a evitar garantías y remitir al pronóstico.
- [IDEAM — portal institucional](https://www.ideam.gov.co/) — respuesta HTTP 200; leí el contenido principal (copia extraída en `weather_volcano/evidence/ideam-homepage-extracted.txt`). La página presenta “Pronósticos y Alertas”, “Tiempo y Clima”, “Servicio de Pronósticos y Alertas” y un enlace al informe diario interactivo de pronósticos y alertas. Esto respalda dirigir al usuario al IDEAM para consultar información meteorológica actualizada (`daily_forecast`); no afirma un pronóstico concreto para el parque.
- [Servicio Geológico Colombiano — portal](https://www.sgc.gov.co/) — intento de consulta efectuado el 2026-11-21, respuesta HTTP 403; no se pudo leer su contenido.
- [SGC — ruta de boletines volcánicos](https://www.sgc.gov.co/Noticias/Paginas/Boletines-volcanicos.aspx) — intento de consulta efectuado el 2026-11-21, respuesta HTTP 403; no se pudo leer su contenido.
- [SGC — índice de volcanes](https://www2.sgc.gov.co/volcanes/index.html) — intento de consulta efectuado el 2026-11-21, respuesta HTTP 429; no se pudo leer su contenido.
- [SGC — página alternativa de boletines](https://www2.sgc.gov.co/volcanes/VolcanNevadoRuiz/Paginas/Boletines.aspx) — intento efectuado el 2026-11-21; la consulta no entregó contenido útil dentro del tiempo disponible. No se usó para sustentar un nivel de alerta ni un evento actual.

### Respaldo por tema

| Entradas | Evidencia utilizada |
|---|---|
| `weather_volcano.park_climate`, `bimodal_rainfall`, `seasonal_weather`, `weather_by_elevation` | Ficha PNN leída: clima de montaña, régimen bimodal y temperatura variable según estación y pisos térmicos. “Temporada” solo describe los dos periodos secos y lluviosos; no recomienda meses ni promete buen tiempo. |
| `weather_volcano.daily_forecast` | Portal IDEAM leído: sección de pronósticos y alertas e informe diario interactivo. La respuesta deja claro que no tiene el pronóstico puntual. |
| `weather_volcano.summit_visibility` | Editorial prudente derivada de la variabilidad meteorológica documentada por PNN: no promete visibilidad. No hay dato leído que permita anticipar visibilidad de una fecha. |
| `weather_volcano.ruiz_volcano_activity`, `current_alert`, `alert_levels_meaning`, `ash_emission` | Referencia al SGC como autoridad indicada por la semilla del proyecto; el portal no pudo leerse en esta sesión. Las respuestas no atribuyen al SGC un boletín particular ni describen estado, nivel o emisión vigentes. La limitación de acceso queda explícita; estas entradas ofrecen una ruta de verificación, no una conclusión factual derivada de boletines consultados. |

## Vacíos de información oficial

- No se pudo leer el boletín más reciente del SGC; por lo tanto, no se publica nivel de actividad/alerta vigente, fecha de cambio, pronóstico de erupción, emisión reciente, caída de ceniza ni recomendación operativa particular.
- No se pudo verificar la definición oficial vigente de cada nivel de alerta ni las acciones específicas para visitantes. `alert_levels_meaning` reconoce el vacío y remite a la guía vigente; no inventa criterios.
- La ficha PNN no permite recomendar meses concretos, horas, probabilidades de lluvia, rangos de temperatura por sector o una probabilidad de ver la cumbre. No se añadieron esas cifras o promesas.
- El portal IDEAM consultado permite ubicar sus pronósticos, pero no se consultó un pronóstico puntual georreferenciado para cada sector o fecha de visita.
- No se encontró en páginas realmente leídas una recomendación oficial de protección al visitante ante caída de ceniza específica para Los Nevados. La entrada de ceniza indica verificar al SGC y autoridades, no prescribe equipo ni conducta médica.

## Conflictos y resolución

No se encontró un conflicto factual comprobable entre fuentes realmente leídas. El principal límite es de disponibilidad: PNN describe patrones generales del clima, mientras los avisos volcánicos del SGC no pudieron recuperarse. No se interpreta ese fallo como ausencia de alertas. Las respuestas para tiempo o estado actual remiten a fuentes oficiales y advierten que cambian.

## Temas descartados y razones

- Predicción de erupción, seguridad de ingreso según nivel, nivel vigente y caída actual de ceniza: descartados como respuestas factuales porque requerían un boletín SGC actual que no fue accesible; se conservó únicamente una instrucción de consulta oficial.
- “Mejor mes”, hora típica de despeje, probabilidad de nieve/granizo/tormenta, acumulados de lluvia y temperaturas por sector: sin evidencia fechada suficiente en fuentes leídas.
- Consejos de ropa, equipo o manejo de salud en clima frío: excluidos por alcance, corresponden a `preparation` o `health_safety`.
- Historia de erupciones, Armero y consecuencias históricas: excluidas porque corresponden a `history_culture`.
- Sectores, vías y cierres de acceso: excluidos por corresponder a `access`/`hours_status`; el clima no confirma que un acceso esté abierto.

## Semilla y conteo final

- Semilla original índice cero-based `8`, etiqueta “la actividad del volcán”: cubierta por `weather_volcano.ruiz_volcano_activity`, `weather_volcano.current_alert`, `weather_volcano.alert_levels_meaning` y `weather_volcano.ash_emission`. Se conservó la intención comprobable de consultar actividad y boletines del SGC; se retiraron como aseveraciones los ejemplos/respuestas que implicaban estado actual o seguridad no verificados. El rótulo original queda asignado solo a este espacio; historia de erupciones no se incluyó.
- Entradas: 10 (meta 60; se cierra bajo meta por falta de evidencia oficial recuperable y para no fragmentar intents casi idénticos).
- Ejemplos: 120; 12 por entrada, sin duplicados dentro de la sección. Cada entrada tiene 2 hard negatives, 1 variante fiel y etiquetas de 3–5 palabras.
- Hechos: solo se afirma el patrón climático general tal como lo describe PNN y la existencia de secciones de pronóstico del IDEAM. Inferencia: un pronóstico de sector/fecha debe verificarse en el momento; la variabilidad impide prometer visibilidad. Texto editorial: respuestas breves, referencias para consulta y avisos de que no se confirma estado actual. Vacío no verificado: cualquier alerta o fenómeno volcánico vigente.
- Nota sobre comportamiento de la aplicación: textos editoriales que dicen “consulta”, “no puedo confirmar” o “sigue las indicaciones” son orientación curada, no acciones certificadas por IDEAM, SGC o Parques. La app offline no consulta ni transmite boletines, no verifica ubicación, no reporta emergencias y no garantiza alertas en tiempo real.
