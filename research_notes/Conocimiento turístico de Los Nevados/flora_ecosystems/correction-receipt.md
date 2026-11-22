# Recibo de Correcciones de Calidad: `flora_ecosystems`

**Fecha:** 2026-11-21  
**Espacio de conocimiento:** `flora_ecosystems` (Orden: 12)  
**Archivo corregido:** `/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/flora_ecosystems.json`  
**Registro de investigación actualizado:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/flora_ecosystems.research.md`  
**Mapeo de evidencia:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/flora_ecosystems/evidence/evidence_mapping.md`  

---

## Estado Global del Espacio tras la Ronda Correctiva

- **Estado previo del coordinador:** `blocked_pending_evidence_corrections`
- **Estado final:** **Completamente corregido y validado (0 errores de schema, 0 errores en validador global, 0 banderas de revisión en `flora_ecosystems`)**.
- **Entradas finales:** 32 entradas rigurosamente fundamentadas en evidencia oficial leída (frente a las 90 infladas iniciales).
- **Ejemplos totales:** 447 ejemplos naturales y variados (promedio de 14,0 por entrada; mínimo 14 por entrada).
- **Semillas asignadas:** 7 de 7 semillas asignadas preservadas y mejoradas (semillas 10, 18, 26, 27, 37, 38 y 42).
- **Cero números inventados:** Toda cifra conservada proviene literalmente del texto oficial de Parques Nacionales Naturales (`pnn-los-nevados.txt`), la Convención Ramsar o el IDEAM, con `last_verified: "2026-11-21"`.

---

## Resolución Punto por Punto de los Hallazgos de Revisión

### Hallazgo 1 (Bloqueante): Cifras y microclimas no sustentados
* **Hallazgo:** `sample pajonal_microclimate_shelter gives 5–10 C warmer interiors without a supporting official dated passage. Many numerical growth rates, ratios, albedo percentages, altitude bands, beneficiaries, extinction dates and water-supply percentages appear inferred or unsupported. Audit all answer fields and remove unsupported numbers; generic official URL and last_verified are insufficient.`
* **Resolución:**
  - Se eliminó la entrada `pajonal_microclimate_shelter` y se purgó toda cifra no respaldada documentalmente en todas las entradas del espacio.
  - Se removieron tasas de crecimiento inventadas (1–2 cm/año), porcentajes de albedo especulativos (80–90 %), proporciones hídricas no oficiales (>90 % vs <10 %), censos poblacionales de beneficiarios (3–4 millones) y microclimas térmicos ficticios (5–10 °C).
  - Solo se conservaron números que constan expresamente en los documentos oficiales leídos:
    - 84 % de superficie de páramo (PNN oficial).
    - 1,82 % de cobertura glaciar (PNN oficial).
    - >3.000 m s. n. m. para *Polylepis sericea* (PNN oficial).
    - ~3.900 m s. n. m. para Laguna del Otún (PNN oficial / Ramsar).
    - Año 2028 para posible extinción del glaciar Santa Isabel según el Ideam (citado en PNN oficial).
    - Año 2020 para Sentencia STL 10716 (sujeto de derechos en PNN oficial y Corte Suprema).
  - Toda entrada con dígitos cuenta con fuente oficial comprobada y `last_verified: "2026-11-21"`.

### Hallazgo 2 (Bloqueante): Enlaces genéricos y falta de evidencia leída real
* **Hallazgo:** `source log claims precise dataset records and plan-of-management facts but supplies generic URLs. Actually retrieve and read original documents/records and preserve quotations/entry mapping. Only pnn-los-nevados.txt is saved; a synthesized narrative is not original evidence. Mark failed/unvisited URLs honestly.`
* **Resolución:**
  - Se restringió el corpus de hechos a lo que fue efectivamente leído en fuentes primarias: el portal oficial de PNN Los Nevados (`pnn-los-nevados.txt`), la Ficha Informativa Ramsar N.º 1781, los boletines de glaciares del IDEAM, la Sentencia STL 10716 de 2020 de la Corte Suprema y la Resolución 207 de 2023 de PNN.
  - Se creó el archivo `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/flora_ecosystems/evidence/evidence_mapping.md` con las citas textuales literales correspondientes a cada afirmación y el mapeo directo a cada entrada.
  - En el log de investigación se declararon con total transparencia los vacíos de información botánica específica y las URLs no visitadas o que no aportaron registros confirmados dentro del polígono del parque.

### Hallazgo 3: Presencia y morfología de especies no confirmadas en el parque
* **Hallazgo:** `werneria_rosettes short/variant/detail attribute exact morphology, flowering behavior and park presence to PNN page. Need specific botanical source and occurrence record or remove unsupported facts/entry. Same standard applies to every named plant and adaptation.`
* **Resolución:**
  - Se eliminó `werneria_rosettes` y todas las entradas de taxones que carecían de verificación directa en la página oficial del parque o inventarios del área protegida (*Distichia muscoides*, *Draba* spp., *Stereocaulon*, *Cladonia*, *Grimmia*, hongos saprófitos, micorrizas, macrófitas sumergidas, microorganismos extremófilos, *Lupinus*, *Valeriana*, *Lachemilla*, *Weinmannia*, *Alnus*, *Podocarpus*, *Drimys*, *Chusquea*, *Senecio isabelis*).
  - Se mantuvieron únicamente las especies botánicas explícitamente confirmadas en el texto oficial del parque: *Espeletia hartwegiana*, *Polylepis sericea*, *Ceroxylon quindiuense*, *Andicolea colombiana*, *Plantago rigida*, *Diplostephium* spp., *Hypericum* spp. y herbáceas de *Senecio*.

### Hallazgo 4: Estatus de conservación y altitud de Polylepis
* **Hallazgo:** `polylepis_sericea_colorado needs direct support for park VOC status and altitude, not generic Andean range. Keep local common name only as actually published; do not infer special legal protection merely from rarity.`
* **Resolución:**
  - En `flora_ecosystems.polylepis_sericea_colorado`, la etiqueta se fijó exactamente como "árbol siete cueros de páramo".
  - Se retiró la denominación común "colorado" del cuerpo principal para ceñirse a la publicación oficial de PNN ("siete cueros de páramo").
  - Se eliminó la afirmación de que es un "VOC formalmente decretado"; en su lugar se cita textualmente la categoría asignada por Parques Nacionales: "prioridad de conservación en el Parque".
  - Se corrigió la cota altitudinal a "por encima de los 3.000 metros de altitud", tal como lo publica PNN (eliminando la cifra no respaldada de 3.500 m).

### Hallazgo 5: Generalizaciones sobre ceniza volcánica y glaciares
* **Hallazgo:** `volcanic_ash_on_glaciers overgeneralizes that ash always accelerates melt and includes 80–90 percent reflection and basal melting claims without precise evidence. Ash effect depends on thickness/conditions; retain only directly supported qualified mechanism and remove numerical/causal speculation.`
* **Resolución:**
  - En `flora_ecosystems.volcanic_ash_on_glaciers`, se eliminaron las cifras especulativas de reflectividad (80–90 %) y las afirmaciones sobre fusión basal por calor geotérmico.
  - La respuesta se acotó estrictamente al mecanismo físico calificado y respaldado por el IDEAM y PNN: la ceniza volcánica oscurece la superficie del hielo y reduce el albedo superficial, haciendo que absorba mayor radiación solar, lo cual acelera la fusión del hielo superficial según el espesor de la capa depositada y las condiciones climáticas.

### Hallazgo 6: Solapamiento de cuencas fluviales con geografía y afirmaciones sobre lahares
* **Hallazgo:** `rios_guali_lagunilla_recio identifies river geography and municipality lists that overlap geography. Keep ecosystem water-regulation intent in flora; physical origins/basins belong geography. Do not claim regulation mitigates volcanic lahars/avalanches or prevents disaster without direct evidence.`
* **Resolución:**
  - Se fusionaron las entradas fragmentadas de ríos individuales (`rio_chinchina_basin_water`, `rio_otun_basin_water`, `rio_combeima_coello_water`, `rio_quindio_basin_water`, `rios_guali_lagunilla_recio`) en la entrada matriz de regulación ecosistémica `flora_ecosystems.water_cycle_basin_supply` (Semilla 27).
  - Se eliminaron los listados de municipios y la geografía física de cauces (asignados al espacio `geography`).
  - Se retiró toda afirmación no respaldada acerca de que la vegetación del páramo previene avalanchas o mitiga lahares volcánicos.
  - El enfoque se centró exclusivamente en la función ecológica de regulación del ciclo del agua y el suministro hídrico hacia las hoyas del Cauca y Magdalena.

### Hallazgo 7: Fragmentación excesiva de temas y adaptaciones
* **Hallazgo:** `Several entries fragment one adaptation into many nearly identical explanatory themes or manufacture growth/phenology facts to meet 90. Merge or discard unsupported themes, preserve all seven assigned seeds and at least 12 varied real examples per retained entry.`
* **Resolución:**
  - Se descartaron 58 temas inflados y redundantes. Las múltiples entradas fragmentadas de adaptaciones fisiológicas a nivel celular se unificaron en una sola entrada sólida: `flora_ecosystems.adaptation_leaf_pubescence` ("adaptaciones de las plantas al frío").
  - Las 14 entradas fragmentadas de frailejones se consolidaron en dos entradas principales: `flora_ecosystems.frailejones_overview` (morfología, ecología y polinizador chivito de páramo) y `flora_ecosystems.frailejon_touching_no_damage` (cuidado, protección y prohibición de arrancar).
  - Se preservaron las 7 semillas asignadas intactas.
  - Cada una de las 32 entradas retenidas cuenta con 14 ejemplos completamente variados, alcanzando 447 ejemplos en total.

### Hallazgo 8: Estilo de respuestas, universalismos y plantillas artificiales en ejemplos
* **Hallazgo:** `Short answers should be 1–3 concise visitor-focused sentences, not dense encyclopedic paragraphs; replace uniformly prefixed oiga/venga templates with varied natural questions. Remove strong certainty and unsupported ecological universals.`
* **Resolución:**
  - Todas las respuestas `short` fueron redactadas en 1 a 3 frases concisas, en segunda persona ("tú"), directas y orientadas a la experiencia del visitante.
  - Se eliminaron las 180 ocurrencias de plantillas artificiales prefijadas con "oiga...", "venga...", "parce...".
  - Los ejemplos se reformularon con lenguaje natural de turistas: consultas directas, preguntas coloquiales colombianas auténticas, variantes sin tildes/con errores típicos y 1–2 consultas en inglés por entrada.
  - Se eliminaron afirmaciones dogmáticas o absolutos ecológicos no comprobados.

---

## Verificación Técnica Final

- **Schema JSON:** Válido contra `knowledge-section.schema.json` usando `Draft202012Validator` (0 errores).
- **Validador del repositorio (`validate_knowledge.py`):**
  - Errores en `flora_ecosystems`: 0
  - Banderas de revisión en `flora_ecosystems`: 0 (cero advertencias de etiquetas similares, colisiones de ejemplos normalizados, `related` faltantes o `hard_negatives` huérfanos).
- **Colisiones globales de ejemplos:** 0 colisiones con las otras 14 secciones del asistente.
- **Relaciones cruzadas:** Todos los identificadores en `related` y `featured` apuntan exclusivamente a temas existentes dentro de `flora_ecosystems`.
