# Recibo de Corrección — Sección Fauna (`fauna`)
**Parque Nacional Natural Los Nevados**  
**Fecha:** 2026-11-21  
**Autor:** Subagente de Investigación Profunda - Dimensión Fauna  
**Estado general:** Resuelto satisfactoriamente (0 errores de validación)

---

## Detalle de Hallazgos de la Revisión del Coordinador y Resoluciones

| # | Hallazgo de la Revisión (`fauna.review.json`) | Estado | Resolución aplicada y evidencia documental |
|---|---|---|---|
| **1** | **BLOCKING EVIDENCE:** No había evidencia descargada presente, solo módulos de datos y URLs genéricas. Se requería leer registros y documentos oficiales, preservar texto fuente e identificar evidencia de ocurrencia en el parque. | **RESUELTO** | Se descargó y archivó el conjunto Darwin Core oficial de SiB Colombia / CARDER (`https://doi.org/10.15472/r8t5xv`, 1.122 registros). Se extrajeron pasajes textuales oficiales de la Ficha Técnica de Parques Nacionales Naturales de Colombia, de la Resolución 207 de 2023 y de las directrices técnicas de fauna silvestre, quedando guardados en `fauna/evidence/`. |
| **2** | **Muestra `fauna.mountain_river_crabs`:** Afirmaba Pseudothelphusidae en el parque, comportamientos y excelente calidad de agua sin soporte a nivel de registro. | **RESUELTO** | **Entrada eliminada**. No existe evidencia de presencia ni registro documental de crustáceos decápodos dulceacuícolas (Pseudothelphusidae) en los páramos de alta montaña de Los Nevados. Se registró como vacío de información y se removió de `fauna.json`. |
| **3** | **Muestra `fauna.little_red_brocket`:** Asignaba 2500–3800 m exactos y comportamiento con páginas genéricas. Cada número requería pasaje oficial fechado y presencia en parque. | **RESUELTO** | Se comprobó la presencia de *Mazama rufina* en el conjunto Darwin Core de la CARDER (Mammalia, Cervidae) y en el Plan de Manejo de PNN Los Nevados. Se eliminaron las cifras altitudinales inventadas (2.500–3.800 m) y descripciones no respaldadas, describiendo su presencia comprobada en bosques altoandinos y ecotonos del páramo en tono conciso y prudente. |
| **4** | **Muestras `fauna.black_chested_buzzard_eagle` y `fauna.mountain_tanagers`:** Prometían lo que el visitante vería y hacían afirmaciones anatómicas/ecológicas sin soporte preciso. | **RESUELTO** | Se eliminaron todas las garantías y promesas de avistamiento ("que verás", "podrás presenciar el espectáculo"). Se adoptó una redacción condicional que subraya el carácter fortuito de los avistamientos según el viento y la visibilidad. Rasgos de *Geranoetus melanoleucus* y bandadas mixtas (*Anisognathus*, *Buthraupis*) fueron alineados con la ficha técnica de PNN y el conjunto de datos de la CARDER. |
| **5** | **Muestra `fauna.encounter_spectacled_bear`:** Protocolo de seguridad atribuido a páginas generales con predicciones de temperamento. | **RESUELTO** | Se reescribió íntegramente siguiendo las directrices técnicas oficiales de Parques Nacionales Naturales ante encuentros con *Tremarctos ornatus*: guardar la calma, no correr, mantener distancia mínima de 10 a 30 metros, jamás bloquear su ruta de escape ni acercarse a crías, retroceder con lentitud y notificar a los guardaparques del sector. |
| **6** | **Verificación de DOI `10.15472/r0e1u9` y eBird `L1142279`:** Verificar si resuelven a los datos previstos. | **RESUELTO** | El DOI `10.15472/r0e1u9` arrojaba error 404 (era erróneo). Se identificó y verificó el DOI real en SiB Colombia: `https://doi.org/10.15472/r8t5xv` (*Biodiversidad Parque Nacional Natural Nevados*, publicado por CARDER, v2.2). El identificador eBird `L1142279` también arrojaba 404 y fue eliminado, reemplazándolo por fuentes oficiales `.gov.co` (PNN y CARDER) que satisfacen los requerimientos del contrato. |
| **7** | **Categorías de amenaza y conteos de especies:** Distinguir estatus global (UICN) vs. nacional (Libros Rojos/MinAmbiente), año de evaluación y no mezclar conteo de parque con área de amortiguación. | **RESUELTO** | Se explicitó la diferencia en `fauna.threatened_species`: cóndor andino (Vulnerable global UICN, pero En Peligro Crítico en Colombia), danta de montaña (En Peligro - EN), oso andino (Vulnerable - VU). En `fauna.fauna_overview` se aclaró que los 778 vertebrados corresponden a todo el macizo y su zona de amortiguación regional, mientras que el páramo estricto del parque alberga 108 aves y mamíferos especializados. |
| **8** | **Revisión de TODAS las entradas y reducción de inventario:** Auditar taxonomía, endemismos, anfibios/reptiles/invertebrados, cifras numéricas y eliminar relleno enciclopédico. | **RESUELTO** | Se auditaron las 90 entradas. Se eliminaron 5 entradas que carecían de soporte de presencia en el parque o constituían relleno enciclopédico (`fauna.mountain_river_crabs`, `fauna.carunculated_caracara`, `fauna.andean_gull`, `fauna.rufous_porcupine`, `fauna.soil_invertebrates_paramo`), dejando **85 entradas de alta calidad**. Se eliminaron todos los rangos altitudinales, pesos y velocidades no respaldados en pasajes fechados. |

---

## Métricas Finales de Entrega

* **Total de entradas:** 85 (reducción desde 90 aprobada por el mandato de preferir un conjunto de datos verificado más pequeño frente a metas infladas).
* **Total de ejemplos:** 1.026 ejemplos de usuario (promedio de 12,07 por entrada; mínimo 12 en todas).
* **Total de negativos duros:** 255 (exactamente 3 por entrada).
* **Entradas destacadas (`featured`):** 5 (`fauna.birds_overview`, `fauna.mammals_overview`, `fauna.buffy_helmetcrest`, `fauna.andean_condor`, `fauna.spectacled_bear`).
* **Preguntas de aclaración (`bank`):** 5 preguntas de desambiguación.
* **Preguntas de slot (`slot_questions`):** 2 (`animal_group` y `sector`), en correspondencia 1:1 con `entity_filters`.
* **Semillas asignadas:** Preservadas y ampliadas en `fauna.birds_overview` (Semilla 24) y `fauna.mammals_overview` (Semilla 25).
* **Validación de esquema y reglas globales:** **0 errores** al ejecutar `validate_knowledge.py`.
