# Recibo de corrección: `actions` (2026-11-21)

Fuente de hallazgos: `coordination/actions.review.json`, estado `changes_required`, muestra `actions.report_fire`, `actions.report_emergency_general`, `actions.report_lost_person`, `actions.report_offline_emergency`, `actions.report_storm`.
Salida: `data/knowledge/sections/actions.json` (10 entradas, 131 ejemplos, 30 hard negatives). Schema: 0 errores.

## Hallazgos del coordinador

| # | Hallazgo | Resolución | Estado |
|---|---|---|---|
| 1 | Contradicción de no transmisión en la muestra (`lo envío solo si confirmas`, `no lo envío sin tu confirmación`). Todas las respuestas deben remitir al flujo local sin prometer envío. | Reescritas las 10 entradas (short, variants, steps, detail). Eliminadas las frases de envío. Cada respuesta de emergencia dice que la app no avisa a rescate y remite al 123 cuando haya señal. Entradas de registro dicen solo "te llevo al registro". | Resuelto |
| 2 | `report_offline_emergency` mezcla preguntas de capacidad de la app con reportes activos; podía arrancar el FSM de emergencia para una pregunta informativa. | Quitadas las preguntas sobre si la app funciona sin señal o sin datos. Quedan solo emergencias activas sin señal. Hard negatives cambiados por preguntas de otros espacios. | Resuelto |
| 3 | `needs` incluía ubicación y número de personas, lo que podía retrasar las instrucciones urgentes o sugerir que son necesarios antes de llamar a emergencias. | En los 8 tipos de emergencia, `needs: []`. La respuesta de seguridad va primero. Los slots siguen definidos para todas las `entity_filters`. `needs` se mantiene solo en los dos registros de visita. | Resuelto |
| 4 | La fuente del 123 es de 2023 y no debe marcarse como no verificada solo por su antigüedad, sin contradicción oficial. | Mantenida la fuente (Policía Nacional, nota de 12 mar 2023, leída completa). La vigencia actual queda como vacío en el log y como pendiente antes de publicar. La respuesta dice "marca el 123 cuando tengas señal" y no garantiza cobertura. | Resuelto con pendiente no bloqueante (ver abajo) |
| 5 | Etiquetas de fuente con disclaimers técnicos largos visibles al turista. | Etiquetas cortas: "Policía Nacional · línea 123 (nota del 12 mar 2023)" y "Parques Nacionales · ficha Los Nevados". El disclaimer se movió al log. | Resuelto |

## Problemas adicionales corregidos (no señalados por el coordinador)

| Problema | Resolución |
|---|---|
| Monto de comparendo `$926.320` en `report_emergency_general.detail` | Eliminado. No es necesario para el visitante. |
| Síntomas clínicos de alarma (confusión, pérdida de conocimiento, "no habla bien") como criterio médico | Reemplazados por "si empeora o no responde bien", sin síntomas específicos. |
| Protocolos sin fuente ("aléjate del fuego y del humo", "sigue las indicaciones del personal" ante rayos) | Eliminados. |
| "Te muestro un resumen", "sin conexión no puedo garantizar que quede guardado", "no lo envío sin tu confirmación" | Eliminados. |
| Frase "el registro de esta app no reemplaza el registro de ingreso" (inferencia) | Eliminada. La respuesta solo dice dónde se completa el ingreso según PNN. |
| Caveat de reserva en `register_arrival_today` | Eliminado de la respuesta de llegada; la reserva queda solo en `register_planned_visit`, con cita de PNN. |
| Descripción de la sección con "siempre con tu confirmación" y "no garantiza envío ni guardado" | Reescrita: "La app no avisa a rescate; en una emergencia real, marca el 123 cuando tengas señal." |

## Verificación

- Schema: 0 errores (`jsonschema` 4.26.0, draft 2020-12).
- Chequeo local: 0 problemas. Ejemplos únicos en la sección y sin duplicados contra archivos finales de otras secciones.
- Conteos: 10 entradas, 131 ejemplos, 30 hard negatives, 2 variantes o menos por entrada, 3 a 8 palabras por etiqueta, `related` y `featured` locales.
- Citas: 11 citas literales en `actions/evidence/quotes-and-mapping.md`, con línea del archivo fuente.

## Pendientes no resueltos

1. **Vigencia actual del 123.** Fuente única de 2023. Si se actualiza la comprobación, usar una nueva publicación institucional; no llamar al número de emergencias para hacer pruebas. No bloquea el JSON.
2. **Hard negatives entre secciones.** 1 de 30 confirmado en la sección final de `hours_status` (`a qué hora abren`). Los 29 restantes no aparecen aún como ejemplos en las secciones finales:
   - cómo reservo; cuánto cuesta entrar; necesito seguro para entrar;
   - qué hago si me pierdo; qué es el mal de altura; qué número llamar si me lastimo;
   - primeros auxilios para un esguince; cuánto cuesta el seguro de accidentes; cómo leer el mapa del sendero; qué debo llevar;
   - cómo se previene el soroche; a qué altura es peligroso subir; qué ropa llevar para el frío; cómo se previene la hipotermia; qué es la hipotermia;
   - pronóstico de lluvia para hoy; qué hacer en una tormenta; cómo llegar a la cabaña Potosí;
   - qué está prohibido con fuego en el parque; cómo cuidar el páramo; qué es un pajonal;
   - dónde hay señal de celular; qué puedes hacer sin conexión.
   Acción: el coordinador los cruza al cerrar. Los que no existan se reemplazan por ejemplos finales o se marcan para revisión. No creé ejemplos de otras secciones para completarlos.
3. **`actions/build_actions.py`.** Genera la versión anterior. Sin modificar. No ejecutar.
4. **Embeddings.** Similitud coseno ≥ 0.95 no ejecutada: no hay embeddings en este entorno.
