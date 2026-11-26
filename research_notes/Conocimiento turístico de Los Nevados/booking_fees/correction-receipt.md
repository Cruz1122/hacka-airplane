# Recibo de corrección — booking_fees

Fecha: 2026-11-21. Archivo corregido: `data/knowledge/sections/booking_fees.json`.

| Hallazgo del revisor | Resolución |
|---|---|
| La tarifa extranjera decía valor 2026 sin caveat en todas las salidas | Se retiraron cifras tarifarias de todas las respuestas; la respuesta orienta a comprobar la tabla oficial vigente. No quedan variantes o pasos con precio parcial. |
| Faltaba el destino exacto para reservar Brisas | Se añadió `https://www.operacionnevados.co`, enlazado desde la ficha PNN, y se aclara que requiere conexión y la app no reserva. |
| Precisar quién puede guiar | Las respuestas requieren guía o personal de agencia registrada y ordenan comprobar autorización para el atractivo; no dicen que cualquier trabajador de agencia califique. |
| Edad máxima legal frente a ficha web | La ficha dice 69; la Resolución 207 de 2023 registra el rango general 6–70. Se dejó la discrepancia visible y no se fija un máximo definitivo. Confirmar con PNN para casos de borde. |
| Categoría exacta para edad 25 no resuelta | Se retiraron montos y asignaciones por edad; el caso no se clasifica por inferencia. |
| Proveedores/inducción duplicados o fuera de sección | REPSE y requisito de acompañamiento quedan en booking_fees. Se añadió una intención de inducción basada en el pasaje de la ficha; ubicación de la charla por sector sigue sin precisar. |
| Cobertura general de reservas, pagos y requisitos | Se mantuvieron solo temas con soporte legible. Se retiraron tarifas por categoría/vehículo, exenciones, documentos, pagos en línea detallados, precios de seguro, plazos numéricos de reserva y cancelaciones no verificadas. |

## Evidencia efectivamente leída

- Ficha PNN Los Nevados: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ — consultada 2026-11-21; sin fecha editorial visible. Pasajes y mapeo de cada entrada están en `booking_fees.research.md`; copia de texto examinada: `services/evidence/pnn_nevados.txt`.
- Resolución 207 de 2023: https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf — acto de 2023-08-04. Pasaje exacto y mapeo guardados en `booking_fees/evidence/age-conflict-quotes.md`; se conserva como conflicto sobre edad y no se usa para adjudicar el límite actual.
- Resolución 551 de 2025: https://www.parquesnacionales.gov.co/wp-content/uploads/2025/12/RESOLUCION-551-DE-19-DE-DICIEMBRE-DE-2025-DG-1.pdf — descarga local lograda, pero PDF escaneado y extracción/OCR no legibles para las tablas. **No se cita como soporte factual de afirmaciones conservadas.**

## Resultado final

13 entradas, 156 ejemplos, 26 negativos, 13 etiquetas distintas (3–8 palabras), 1 variante por entrada, 5 preguntas de aclaración, 2 filtros con slot questions. Seeds preservadas: índices `2, 3, 5, 30, 31` según asignación; mapeo en el log. Pendientes de evidencia oficial clara: edad máxima vigente, clasificación exacta a los 25 años, precio de seguro, tabla de tarifas en una copia legible y ubicación de inducción por sector.
