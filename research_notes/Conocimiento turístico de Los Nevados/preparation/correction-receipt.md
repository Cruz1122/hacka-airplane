# Recibo de Corrección: Sección `preparation` (Preparación y equipamiento)

**Fecha:** 2026-11-21  
**Responsable:** Subagente de Investigación `preparation` (Espacio 7)  
**Sección auditada:** `/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/preparation.json`  
**Log de investigación actualizado:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/preparation.research.md`  
**Evidencia factual verificada:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/preparation/evidence/official_sources_extracts.txt`  
**Semilla asignada:** Índice 9 de `conocimiento.json` ("qué ropa y equipo llevar"), preservada y fortalecida en `preparation.layering_system`.  

---

## 1. Estado de la Sección y Métricas Finales

- **Total de entradas entregadas:** 53 (Auditadas y reducidas desde 60 para eliminar temas sin evidencia, duplicados normativos y desbordes de alcance).
- **Total de ejemplos de usuario:** 742 (Promedio de 14.0 ejemplos por entrada; mínimo 12 cumplido en el 100 % de las entradas; variedad de consultas cortas, preguntas formales, giros coloquiales colombianos, errores/sin tildes y 1–2 preguntas naturales en inglés).
- **Total de hard negatives:** 159 (3 por entrada, apuntando a espacios vecinos como `health_safety`, `rules`, `booking_fees`, `weather_volcano`).
- **Etiquetas (`label`):** 53 etiquetas formuladas con rigor léxico (todas estrictamente entre 3 y 8 palabras, semánticamente diferenciadas).
- **Validación JSON Schema (`knowledge-section.schema.json`):** 0 errores.
- **Validación cruzada de IDs:** 0 referencias rotas (`related` y `featured` resuelven al 100 %).

---

## 2. Matriz de Hallazgos de Revisión y Resoluciones Concretas

| # | Hallazgo de Coordinación (`preparation.review.json`) | Estado | Resolución Aplicada en Esta Ronda Correctiva |
|---|---|---|---|
| **1** | **BLOCKING: Inferencia numérica sin sustento oficial.** Se exigió remover volúmenes de mochila, lúmenes de linterna, valores R, milímetros de columna de agua, rutinas de entrenamiento, litros de agua obligatorios, porcentajes de reducción articular y rangos térmicos no respaldados. | **RESUELTO** | Se eliminaron **todas** las cifras inferidas en todos los campos (`short`, `variants`, `steps`, `detail`, `reflection`). Se erradicaron los 150–300 lúmenes de `headlamp`, los valores R 3.5–4.5 de `sleeping_pad`, los 3.000/5.000 mm de `mountain_tent`, los litros arbitrarios en mochilas y agua, y los 40–60 km/h en viento. Cada número remanente corresponde estrictamente a textos de la Resolución 207 de 2023 (gafas UV 100%, bloqueador factor 50 mínimo, temperaturas menores a 0 °C) o la ficha oficial (edades de 6 y 15 años). |
| **2** | **BLOCKING SAFETY: Mascarilla volcánica N95 y cuello térmico.** N95 no protege de gases volcánicos ni el olor a azufre valida su suficiencia; `neck_gaiter` no debe prometer protección respiratoria o volcánica; respuesta a ceniza pertenece a `weather_volcano`. | **RESUELTO** | `preparation.ash_mask` fue **completamente eliminada** de `preparation` (su cobertura corresponde exclusivamente a `weather_volcano`). En `preparation.neck_gaiter` se eliminó cualquier mención de protección respiratoria o frente a ceniza, acotando su función a la protección térmica del cuello, garganta y orejas contra el viento gélido de páramo, citando el pasamontañas de la Resolución 207. |
| **3** | **BLOCKING SAFETY: Termo con bebidas calientes y botas de caucho.** `thermal_flask` afirmaba restauración instantánea de temperatura central y que el agua fría gasta energía vital; `rubber_boots` inventaba obligatoriedad de plantillas ortopédicas y medias de lana. | **RESUELTO** | En `preparation.thermal_flask` se eliminaron todas las afirmaciones fisiológicas o terapéuticas infundadas; se redactó como una fuente de confort térmico y bienestar en paradas frías. En `preparation.rubber_boots` se eliminó la falsa obligación de plantillas ortopédicas o calcetines de lana, presentando la bota pantanera como calzado práctico tradicional para aproximaciones con barro espeso (Cocora / El Cedral). |
| **4** | **Prescripción de entrenamiento físico.** `fitness_training` inventaba plan de 4–8 semanas, sesiones de 45 minutos, cargas de 5–8 kg, 3 días de descanso y doble esfuerzo cardiovascular a 4.000 m. | **RESUELTO** | Se eliminó por completo la rutina deportiva prescrita. Se redactó orientación física general basada en la advertencia de salud de Parques Nacionales ("debido a las condiciones de frío, disminución de presión y esfuerzo físico"): mantener actividad aeróbica previa regular, ascender con paso pausado y realizar paradas periódicas de 10 minutos para facilitar la aclimatación. |
| **5** | **Evidencia sintética `pnn_preparation_guidelines.txt`.** El archivo previo era una síntesis no oficial sin citas directas. | **RESUELTO** | Se creó el archivo formal `/evidence/official_sources_extracts.txt` con los textos originales descargados y leídos de la Resolución 207 de 2023, la ficha oficial de Los Nevados y la Resolución 1558 de 2019, incluyendo fecha de verificación (2026-11-21), URL oficial del dominio `gov.co`, citas breves textuales y mapeo unívoco hacia cada una de las entradas servidas. |
| **6** | **Marcas comerciales y exigencias técnicas no reglamentadas.** Se alegaba obligatoriedad de suelas Vibram, membranas Gore-Tex, plumón Primaloft y marcas específicas. | **RESUELTO** | Se eliminaron todas las marcas registradas y tecnicismos comerciales. Se ajustó la terminología a las exigencias normativas de la Resolución 207: "ropa abrigada", "ropa impermeable", "zapatos cómodos preferiblemente impermeables" y calzado con suela de buen labrado/agarre. |
| **7** | **Coordinación de alcance temático.** `pre_trip_acclimatization` corresponde a `health_safety`; `ash_mask` a `weather_volcano`; `prohibited_single_use_plastics`, `prohibited_speakers_drones`, `prohibited_alcohol_fire` corresponden a `rules`. | **RESUELTO** | Se retiraron `pre_trip_acclimatization` y `ash_mask`. Las tres entradas de prohibiciones se consolidaron en una única lista de chequeo práctica de equipaje: `preparation.what_not_to_pack` ("qué elementos evitar empacar en la mochila"), orientada al turista para no cargar objetos restringidos, dejando la tipificación sancionatoria y legal en el espacio `rules`. |
| **8** | **Higiene en campamento y hoyos de gato.** Se recomendaban dimensiones de hoyo de gato sin autorización ambiental específica del parque. | **RESUELTO** | Se alineó taxativamente con el texto oficial del numeral 6.2 de la Resolución 207 de 2023: las excretas deben evacuarse en cacatubo preferiblemente o enterrarse en hoyo de gato usando la pala que porta obligatoriamente el guía de montaña; el papel higiénico debe manejarse y retornarse en bolsa plástica; y está rotundamente prohibido enterrar basuras. |
| **9** | **Revisión integral de campos y reducción de entradas infladas.** Revisar la totalidad de respuestas para eliminar garantías médicas, acortar párrafos verbose y preferir un conjunto reducido con respaldo genuino sobre metas infladas. | **RESUELTO** | Se auditaron las 53 entradas. Cada respuesta corta (`answer.short`) tiene entre 1 y 3 oraciones concisas, en tono amigable de "tú", enfocada en la acción inmediata, libre de jerga meta-investigativa y sin prometer rescates, transmisiones GPS o sincronizaciones. La sección se redujo de 60 a 53 entradas genuinamente soportadas. |

---

## 3. Asuntos No Resueltos o Vacíos Normativos Registrados

- **Ausencia de catálogo oficial de marcas o especificaciones numéricas en calzado/mochilas:** Parques Nacionales no publica un manual con gramajes, marcas permitidas o lúmenes de linterna. Esto se respeta como vacío oficial y se instruye al visitante con recomendaciones cualitativas estándar sin inventar normas inexistentes.
- **Reglamentación de equipo de alta cumbre:** La normativa no exige que el turista compre crampones, piolet o cascos homologados, sino que exige la contratación obligatoria de guías/operadores registrados (REPSE), quienes proveen y supervisan dicho equipo técnico. Se reflejó esta realidad en `preparation.technical_glacier_gear`.
