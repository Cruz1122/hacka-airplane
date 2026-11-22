# Comprobante de Corrección (Correction Receipt): Espacio `hours_status`

**Fecha:** 2026-11-21  
**Subagente:** Investigación `hours_status` (Orden 6)  
**Sección:** `/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/hours_status.json`  
**Registro de investigación:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/hours_status.research.md`  
**Registro de evidencias:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/sources.md`  
**Estado:** Resuelto y validado (0 errores de esquema, 0 infracciones de fuentes/cifras).

---

## 1. Tratamiento Detallado de Hallazgos de la Revisión Coordinadora (`hours_status.review.json`)

| # | Hallazgo de Revisión | Estado | Resolución Aplicada en `hours_status.json` y Fuentes |
|---|---|---|---|
| **1** | **BLOCKING:** `camping_arrival_cutoff` inventa hora obligatoria de llegada a las 16:30/17:00 y activación automática de búsqueda de rescate a las 17:30. | **RESUELTO** | Se eliminaron de forma exhaustiva las horas inventadas (16:30, 17:00) y el falso protocolo de búsqueda automática a las 17:30 en `short`, `variants`, `steps` y `detail`. Se ajustó la respuesta a la normativa real (Resolución 207 de 2023 de PNN): el parque no fija hora reglamentaria de carpa ni rescate automático, sino que controla el ingreso matutino con equipo (7:00 a 12:00 en Potosí), autoriza camping transitorio únicamente en puntos específicos (Termales Cañón, Arenales, Calvito) y prohíbe el tránsito nocturno. |
| **2** | **BLOCKING:** `reopening_protocol_after_emergencies` afirma un protocolo universal de comité multiactores que certifica terreno seguro tras emergencias. | **RESUELTO** | Se eliminó la afirmación de comités técnicos universales que certifiquen terreno totalmente seguro. La respuesta se reformuló para explicar con precisión operativa cómo verificar los comunicados oficiales y resoluciones administrativas de Parques Nacionales levantando la restricción, advirtiendo claramente al turista que el cese de una medida preventiva no elimina los riesgos naturales propios de la alta montaña. |
| **3** | `high_season_calendar` fija límites calendario exactos (15 dic, fin de enero, mitad de junio, julio) y afirma reserva obligatoria general en toda fecha. | **RESUELTO** | Se eliminaron las fechas calendario cerradas no respaldadas y la exigencia de reserva general para todos los días en Brisas. Se sustituyó por la regla oficial: no hay calendario cerrado oficial; los picos coinciden con fin de año, Semana Santa, mitad de año y festivos; en Brisas la reserva en `reservasnevados.com` se solicita para fines de semana y festivos (y se recomienda en periodos de alto tráfico como noviembre por el pico y placa), mientras que en sectores de travesía la reserva previa con operador sí es obligatoria. |
| **4** | `otun_sector_hours` tiene respaldo para el horario 07:00–12:00 en Potosí, pero conflaciona registro con llegar a la laguna antes de mediodía, añade prohibición categórica de registro tardío y cupos reducidos Ramsar no soportados. | **RESUELTO** | Se conservó el horario verificado en Cabaña Potosí (7:00 a. m. a 12:00 m.). Se eliminó la implicación de llegar a la laguna antes del mediodía y el argumento no oficial sobre cuotas Ramsar. Se aclaró que la caminata posterior depende de la ruta y se instruyó confirmar variaciones con Parques Nacionales. |
| **5** | Auditoría de las 40 entradas para eliminar afirmaciones operativas fabricadas (horarios de salida, horas de cumbre, portones privados, turnos de personal, garantías de rescate). | **RESUELTO** | Se auditaron las 40 entradas: se eliminaron las horas de salida inventadas en Brisas (3:30/4:00 p. m. en `brisas_exit_time`), las horas de salida a cumbre inventadas (4:00–5:30 a. m. en Santa Isabel y 1:00–3:00 a. m. en Tolima, aclarando que PNN fija el registro en base/día previo y que el guía coordina la madrugada), y la chiva de las 5:30 a. m. en Cedral. Cada cifra cuenta con sustento textual oficial fechado. |
| **6** | `sources.md` en prosa no es prueba de fuentes descargadas; registrar citas textuales exactas, mapeo por entrada y etiquetar enlaces no visitados con honestidad. | **RESUELTO** | Se reescribió `evidence/sources.md` con citas textuales literales de los archivos guardados en disco (`pnn_nevados.txt`, `resolucion-207-2023.txt`, `pnn-atencion.txt`, boletines SGC). Se declaró honestamente que el dominio de UTON no se pudo consultar directamente en el entorno offline, sustentando sus direcciones en Manizales y teléfonos en la transcripción oficial de la página de Parques Nacionales. Se incluyó tabla de mapeo de las 40 entradas y registro de vacíos. |
| **7** | Cada variante servida sobre horarios o estado debe mencionar que puede cambiar y dirigir a Parques Nacionales antes de viajar o al tener conexión; no afirmar apertura 365 días sin salvedades. | **RESUELTO** | En todas las respuestas principales (`answer.short`) y en todas sus reformulaciones independientes (`answer.variants`) se incorporó la advertencia expresa de que los horarios y el acceso están sujetos a cambios por condiciones climáticas, volcánicas o descansos de conservación, dirigiendo siempre al visitante a confirmar en los canales oficiales de Parques Nacionales antes de viajar. Se corrigió `brisas_open_days` para eliminar la garantía incondicional de 365 días. |

---

## 2. Métricas y Validación Final

- **Total de entradas:** 40 entradas (meta del proyecto: 40).
- **Semillas originales integradas:**
  - Semilla 4 (`los horarios de ingreso`) $\rightarrow$ `hours_status.general_opening_schedule`
  - Semilla 6 (`si el parque está abierto`) $\rightarrow$ `hours_status.park_open_today`
  - Semilla 41 (`los cierres por conservación`) $\rightarrow$ `hours_status.conservation_closures`
- **Total de ejemplos:** 483 ejemplos (mínimo 12 por entrada, promedio 12,08; 0 duplicados en la sección).
- **Variedad de ejemplos:** Consultas breves, preguntas completas, expresiones coloquiales colombianas, variantes sin tilde/ortografía coloquial y 1–2 ejemplos naturales en inglés en cada una de las 40 entradas.
- **Negativos difíciles (`hard_negatives`):** 120 preguntas (3 por entrada).
- **Etiquetas (`label`):** 40/40 con longitud estricta de 3 a 8 palabras, claramente diferenciadas.
- **Validación JSON Schema (`knowledge-section.schema.json`):** 0 errores (`Draft202012Validator: PASSED`).
- **Validación de reglas contractuales (cifras y fuentes oficiales):** 0 errores.
- **Asuntos pendientes no resueltos:** Ninguno.
