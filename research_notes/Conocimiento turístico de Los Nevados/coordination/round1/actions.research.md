# Sección `actions`: registrar visita y reportar emergencia

Fecha de investigación: 2026-11-21. Orden 1. Perfil de recuperación: `safety`.
Salida: `data/knowledge/sections/actions.json` (10 entradas, 126 ejemplos).
Generador y validador: `actions/build_actions.py`. Evidencia descargada: `actions/evidence/`.

## Clasificación de lo que hay en esta sección

- **Hecho verificado**: leído en una fuente oficial, con fecha y cita. Ver sección 1.
- **Inferencia**: deducción mía a partir de hechos verificados. Marcada en la sección 5.
- **Texto editorial de la app**: qué hace el flujo de registro o reporte. No tiene fuente oficial y no debe leerse como respaldo de PNN, de la Policía ni del SGC. Las fuentes de cada entrada son solo para los hechos del entorno (línea 123, guías, puntos de registro).
- **Vacío**: dato que no encontré en fuente oficial. Ver sección 2.

## 1. Fuentes consultadas

Todas leídas el 2026-11-21 con `curl` y convertidas a texto con `actions/html_to_text.py`. Los archivos crudos y de texto están en `actions/evidence/`.

| # | URL | Acceso | Fecha de publicación | Uso |
|---|---|---|---|---|
| S1 | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | HTTP 200, 219 898 bytes. Leído por secciones: recomendaciones, edades, horarios, tarifas, reservas y seguro, guías, actividades, contactos. No revisé el resto de la página | No indicada en la página. Cita la Resolución 1815 del 24 jul 2026 y tarifas "para el 2026"; pie "© 2026" | Reserva, registro, guías, seguro, equipo de guías |
| S2 | https://www.parquesnacionales.gov.co/atencion-al-ciudadano/ | HTTP 200, 644 578 bytes, buscado por términos de emergencia | No indicada | Confirmar si hay línea de emergencia del parque: no la hay |
| S3 | https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155 | HTTP 200, 179 150 bytes, leído completo | **12 mar 2023** (fecha en la nota) | Línea 123: línea única nacional, gratuita, 24 horas; mal uso |

Búsquedas secundarias (no usadas como fuente de hechos; solo ayudaron a ubicar S3):
- WebSearch "línea 123 Policía Nacional Colombia emergencias" (2026-11-21).
- WebSearch "112 Número Único de Seguridad y Emergencias NUSE Colombia" (2026-11-21). Resultados contradictorios sobre el 112; ver sección 3.

Fuentes internas del proyecto (no externas, usadas para los nombres de parámetros del FSM):
- `src/nevados_bench/export_mobile.py` líneas 115–123: `report_emergency` (`st: emergency_phone, emergency_procedure`), `register_visit` (`st: daily_capacity`).
- `src/nevados_bench/world/tools.py` líneas 246–257: `report_emergency(station, emergency_type, people_count, trail_id?)` y `register_visit(station, date, group_size, visitor_type)`. Ambas requieren confirmación.
- `src/nevados_bench/export_mobile.py`, diccionario `_PROCEDURES`, justo después de la línea 123: tipos de emergencia `mal_de_altura`, `hipotermia`, `lesion`, `persona_perdida`, `tormenta_electrica`, `incendio`.
- `src/nevados_bench/suites/fc.py`: valores de `visitor_type` de prueba (`nacional`, `extranjero`, `reducida`).

### Citas usadas y soporte por entrada

| Hecho | Cita literal | Fuente | Entradas que lo usan |
|---|---|---|---|
| 123 es la línea única de emergencias nacional, gratuita, 24 horas | "La Línea de emergencia 123, es la línea única de emergencias Nacional… ofrece… gratuitamente las 24 horas del día" | S3 (2023-03-12) | las 8 de reporte de emergencia |
| El mal uso puede impedir atender una emergencia real | "el mal uso de la línea puede evitar la atención de una emergencia real" | S3 | `report_emergency_general` (detalle) |
| Guías y operadores registrados son obligatorios en todos los sectores | "es obligatorio el servicio de acompañamiento y guianza en todos los sectores" | S1 | lesión, persona perdida, mal de altura, hipotermia, tormenta, incendio, sin señal |
| Los guías registrados deben tener equipo médico de respuesta y radios | "Los operadores y guías deben estar registrados… el equipo médico de respuesta y los radios con la frecuencia requerida" | S1 | ídem |
| Hay puntos de registro e ingreso | "los puntos de registro e ingreso del Parque" | S1 | `register_planned_visit`, `register_arrival_today` |
| Brisas, fines de semana y festivos: reservar con al menos un día | "es indispensable reservar con al menos un día de anticipación para asegurar tu ingreso. Hazlo en: www.reservasnevados.com" | S1 | `register_planned_visit` |
| Otros sectores: reserva obligatoria, la gestiona la agencia | "Ingreso a los demás sectores: la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada" | S1 | `register_planned_visit` |

Nota de las fechas de S1: la ficha no tiene fecha de publicación propia. Su contenido es de 2026 (tarifas 2026 y resolución de julio de 2026). Por eso `last_verified` es la fecha de mi lectura, no una fecha de publicación de la ficha.

## 2. Vacíos (datos que no encontré de fuente oficial)

1. **Línea de emergencia propia del parque o de rescate de Los Nevados.** S1 y S2 no publican ningún número de emergencia del parque. El único número de emergencia usado es el 123 (S3). Pendiente: consultar con PNN si hay línea de rescate o radio del parque.
2. **Destino de un reporte de la app.** No hay evidencia de que un reporte de `report_emergency` llegue a un equipo de rescate, ni de cómo lo procesa PNN. Las respuestas no prometen envío ni rescate.
3. **Si PNN acepta una pre-inscripción de visita desde una app.** No encontré evidencia. Las respuestas dicen que la acción no reemplaza el registro en el punto de ingreso, lo que es inferencia a partir de S1 (ver sección 5).
4. **Categorías oficiales de visitante.** La tabla de tarifas de S1 usa categorías por edad y residencia (menor o mayor de 25 años, residente, nacional, CAN, extranjero residente, extranjero no residente). El FSM usa `nacional`, `extranjero` y `reducida`. No hay correspondencia oficial verificada de `reducida`, así que no la usé en ningún slot.
5. **Número de emergencias 112.** No hay fuente oficial verificada sobre su papel (ver sección 3). No aparece en ninguna respuesta.
6. **Vigencia actual de la línea 123.** S3 es de marzo de 2023. No encontré una confirmación posterior en fuente oficial. `last_verified` indica que leí S3 el 2026-11-21, no que el número esté confirmado hoy. Antes de publicar, confirmar en policia.gov.co o con la línea misma.

## 3. Conflictos entre fuentes y resolución

- **Reserva en Brisas: S1 dice dos cosas.** Línea 111: "es indispensable reservar con al menos un día de anticipación" en fines de semana y puentes festivos. Línea 212: "Ingreso al sector Brisas-Kumanday: la reserva no es obligatoria… para asegurar tu ingreso (ya que los cupos diarios son limitados), reserva con al menos un día de anticipación." **Resolución**: no contradicen; la regla de fin de semana y festivo es más específica. La respuesta solo dice eso, para fin de semana y festivos, y no afirma que la reserva sea obligatoria en general.
- **Papel del 112.** Fuentes secundarias contradicen: un documento de la CRC de 2014 lo lista como número de Policía, otra respuesta de la CRC dice que en Bogotá se redirige a la línea 123, y una guía para viajeros lo presenta como número de emergencia. **Resolución**: ninguna es oficial y vigente. No lo uso. Queda como vacío 5.
- **Plazos de reserva por sector** (S1: Cisne y Otún con tres días hábiles; Quindío–Dulima con cinco). No los uso en acciones: pertenecen a `booking_fees`.
- **Categorías de visitante**: FSM y tarifas oficiales no coinciden (ver vacío 4). **Resolución**: usar solo `nacional` y `extranjero` en los slots, y no mencionar tarifas.

## 4. Temas descartados y motivos

- **"Consultar un reporte" (check a report).** El contrato lo menciona, pero la asignación limita las acciones a `register_visit` y `report_emergency`.
- **Consultar cupo diario (`check_daily_capacity`).** No está en el alcance de acciones; el cupo y la reserva son de `booking_fees`.
- **Cancelar o modificar un registro.** El FSM no tiene esa herramienta.
- **Registro de salida.** No hay herramienta en el FSM ni evidencia oficial leída.
- **Reportar fauna peligrosa (por ejemplo, un oso).** No hay tipo de emergencia en el FSM; no lo añadí para no inventar una acción nueva.
- **Infracciones (basura, fuego prohibido, mascotas).** Son reglas, no emergencias: pertenecen a `rules`.
- **"Me perdí" (yo mismo).** Es información de qué hacer, de `health_safety`. Queda como hard negative de `report_lost_person`.
- **Números de emergencia como pregunta informativa.** Pertenecen a `health_safety`.
- **Separar tormenta de rayos y tormenta general.** Misma intención y mismo tipo FSM; fusionado en una entrada.
- **Separar mal de altura propio y de otra persona.** Misma intención y mismo tipo; fusionado.
- **Entrada para niños o adultos mayores en emergencia.** No hay tipo FSM propio; la edad se trata en `health_safety`.

Entradas de acción: se llegó exactamente a 10 con intenciones distintas. No se partieron intenciones casi idénticas para inflar el conteo. Ver sección 5 sobre llegada frente a planificada.

## 5. Facts, inferences, editorial text and gaps (clasificación)

**Inferencias (mías):**
- `station` del FSM corresponde a `sector` en la app. El FSM usa nombres de estación de un mundo de prueba (`valle_bruma`, `alto_cenizo`), no sectores reales. Usé los cuatro sectores oficiales de S1.
- El `date` de `register_arrival_today` no se pregunta al visitante; el handoff debe tomarlo de la fecha del dispositivo. Dependencia abierta para quien implemente el FSM. Un reloj del dispositivo mal configurado daría una fecha errónea.
- La llegada y la planificación son dos entradas distintas por cuándo ocurren (hoy o después), aunque usen el mismo `register_visit`. Si el coordinador lo considera casi idéntico, puede fusionarlas y pasar la sección a 9 entradas.
- "No reemplaza el registro oficial" es inferencia desde S1, que exige registro en puntos de ingreso.

**Texto editorial de la app (sin respaldo oficial):** todo lo que describe cómo funciona el flujo: "te muestro un resumen", "no lo envío sin tu confirmación", "sin conexión no puedo garantizar que quede guardado", "puedo preparar el reporte con el sector y cuántas personas". Ninguno de esos enunciados viene de PNN, la Policía ni el SGC.

**Vacíos:** ver sección 2.

## 6. Mapeo de semilla (`conocimiento.json`)

- `seed_indexes` asignados: `[]`.
- Revisé los 44 temas. Ninguno es una acción de registro o reporte. Ninguno pasa a `actions`.
- Ningún tema semilla queda sin asignar por esta sección.

## 7. Conteos finales

| id | Ejemplos | Hard negatives |
|---|---|---|
| actions.register_planned_visit | 14 | 3 |
| actions.register_arrival_today | 13 | 3 |
| actions.report_emergency_general | 13 | 3 |
| actions.report_injury | 13 | 3 |
| actions.report_lost_person | 13 | 3 |
| actions.report_altitude_sickness | 12 | 3 |
| actions.report_hypothermia | 12 | 3 |
| actions.report_storm | 12 | 3 |
| actions.report_fire | 12 | 3 |
| actions.report_offline_emergency | 12 | 3 |

Total: 10 entradas, 126 ejemplos. Meta de la asignación: 10. Cada entrada tiene 1–2 ejemplos en inglés. `featured` tiene 5 ids. `clarification.bank` tiene 6 preguntas. `retrieval`: `profile: safety`, `bm25_weight: 0.3`, `top_k: 2`, `min_score: null`.

## 8. Validación ejecutada

- `python3 build_actions.py` genera el JSON y lo valida contra el snapshot del schema (`inputs/knowledge-section.schema.json`, JSON Schema draft 2020-12, jsonschema 4.26.0). **Resultado: 0 errores de schema, 0 errores de contrato.**
- Reglas de contrato verificadas: ids únicos y con prefijo de sección; etiquetas de 3 a 8 palabras; al menos 12 ejemplos; 2 a 4 hard negatives; `related` y `featured` resuelven; cada `needs` y cada `entity_filter` tiene `slot_questions`; toda respuesta con dígitos tiene `last_verified`; ningún ejemplo repetido entre entradas (comparación normalizada sin tildes); ninguna frase prometedora prohibida (GPS, "ya quedó enviado", "rescate llegará").
- Prueba negativa del validador: se corrompieron copias y se detectaron los seis tipos de fallo (duplicado, etiqueta corta, related colgante, acción sin `action`, promesa prohibida, dígitos sin `last_verified`).
- Casi-duplicados: escaneo por similitud de tokens (Jaccard ≥ 0.6) entre entradas. Encontré un par (tormenta y emergencia general, ambos "…how do I report it") y lo reescribí. Escaneo posterior: 0 pares.
- **No verificado**: similitud coseno con embeddings (el validador del proyecto de coseno ≥ 0.95 no lo ejecuté; no hay embeddings en este entorno).
- **No verificado**: que las hard negatives sean ejemplos de otras secciones. Ver sección 9.

## 9. Pendiente para el coordinador

1. **Hard negatives de otras secciones.** Estas hard negatives tienen que ser ejemplos reales de otros espacios para cumplir la regla 3 del contrato. No las he podido confirmar porque los otros archivos se están escribiendo en paralelo: `cómo reservo`, `cuánto cuesta entrar`, `a qué hora abren`, `necesito seguro para entrar`, `qué hago si me pierdo`, `qué es el mal de altura`, `qué número llamar si me lastimo`, `cómo se previene el soroche`, `a qué altura es peligroso subir`, `qué ropa llevar para el frío`, `cómo se previene la hipotermia`, `qué es la hipotermia`, `pronóstico de lluvia para hoy`, `qué hacer en una tormenta`, `cómo llegar a la cabaña Potosí`, `qué está prohibido con fuego en el parque`, `cómo cuidar el páramo`, `qué es un pajonal`, `dónde hay señal de celular`, `cómo llegar a Brisas`, `primeros auxilios para un esguince`, `cuánto cuesta el seguro de accidentes`, `cómo leer el mapa del sendero`, `qué debo llevar`.
2. **Metadata de fuentes.** Las fuentes de las entradas de emergencia son S3 y S1, con etiquetas que dicen que no describen la app. Ninguna fuente implica respaldo oficial del flujo de la app. Confirmar si el coordinador quiere otra forma de marcar texto editorial.
3. **Vigencia de la línea 123.** Confirmar antes de publicar (vacío 6).
4. **Entrada 'reportar emergencia sin señal'.** Usa `kind: action` con `report_emergency`. La respuesta no promete envío. Si el FSM sigue enviando sin señal, esa frase debe revisarse.

## 10. Incidencias del proceso

- Hice una llamada accidental a `mcp__t3-code__request_secret` con el valor de prueba `noop`. Creó el archivo `/home/cruz1122/.t3/userdata/secrets/files/2212dfa78ef3fb09eb3a6b641ab8d04b`, fuera del workspace. No contiene datos del proyecto ni credenciales. No lo borré: queda para decisión del usuario.
- No tengo `WebFetch` en esta sesión. Las páginas se leyeron con `curl` y texto extraído; no usé subagentes.
