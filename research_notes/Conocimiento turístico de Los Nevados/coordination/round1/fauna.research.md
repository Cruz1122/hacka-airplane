# Fauna silvestre — Parque Nacional Natural Los Nevados
**Investigación profunda y registro de evidencia (Sección 11: `fauna`)**
**Fecha de corte e investigación:** 2026-11-21  
**Investigador:** Subagente de investigación profunda para la dimensión de Fauna

---

## 1. Fuentes consultadas y respaldo factual

Todas las consultas y verificaciones de fuentes primarias y secundarias autorizadas se realizaron el **2026-11-21**. Se priorizó la documentación oficial de Parques Nacionales Naturales de Colombia (PNN), el Plan de Manejo oficial del área protegida, el Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia), el Instituto Alexander von Humboldt, las corporaciones autónomas regionales (CARDER, Corpocaldas, Cortolima) y registros ornitológicos de referencia (eBird / The Cornell Lab of Ornithology).

| Fuente / Entidad | URL consultada | Fecha de publicación / versión | Evidencia consultada y soporte temático en la sección |
|---|---|---|---|
| **Parques Nacionales Naturales de Colombia (PNN)** — Portal oficial del Parque | `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/` | Actualización institucional continua (consultada 2026-11-21) | Ficha técnica oficial. Describe la fauna representativa: chivito de páramo (*Oxypogon stuebelii*), tororoi de Miller (*Grallaria milleri*), cóndor andino (*Vultur gryphus* con más de 3 m de envergadura), pato andino (*Oxyura ferruginea* / *Oxyura andina*), periquito de los nevados (*Bolborhynchus ferrugineifrons*), danta de montaña (*Tapirus pinchaque*), puma (*Puma concolor*), guagua loba (*Dinomys branickii*), oso de anteojos (*Tremarctos ornatus*), venado conejo (*Pudella mephistophiles*), loro orejiamarillo (*Ognorhynchus icterotis*). Sustenta las entradas generales y de especies emblemáticas (`fauna.fauna_overview`, `fauna.birds_overview`, `fauna.mammals_overview`, `fauna.andean_condor`, `fauna.buffy_helmetcrest`, `fauna.spectacled_bear`, `fauna.mountain_tapir`, entre otras). |
| **Plan de Manejo PNN Los Nevados (PNN)** | `https://www.parquesnacionales.gov.co/gestion-del-conocimiento/planes-de-manejo/pnn-los-nevados/` | Documento técnico de manejo y actualización | Documento técnico principal. Aporta cifras consolidadas: 778 especies de vertebrados en el parque y su área de amortiguación (14,74 % de los vertebrados del país), 38 especies endémicas o casi endémicas, 108 aves de páramo estricto y >300 aves en el gradiente altitudinal, 31 mamíferos de alta montaña (26 terrestres y 5 quirópteros) y ~60 en el macizo, 15 reptiles y entre 20 y 47 anfibios. Define los Valores Objeto de Conservación (VOC) faunísticos: *Bolborhynchus ferrugineifrons* y *Oxyura jamaicensis*, junto con especies focales sombrilla (*Tremarctos ornatus*, *Tapirus pinchaque*). Sustenta `fauna.fauna_overview`, `fauna.endemic_species`, `fauna.threatened_species`, `fauna.conservation_target_species_voc`, `fauna.birds_overview`, `fauna.mammals_overview`. |
| **SiB Colombia** — Conjunto de datos *Biodiversidad Parque Nacional Natural Nevados* | `https://doi.org/10.15472/r0e1u9` | Publicación estandarizada Darwin Core (DwC) | Registros biológicos estructurados del parque y su área de amortiguación basados en inventarios INDERENA-UNIFEM, revisiones ornitológicas y monitoreos participativos. Sustenta la presencia confirmada en el área de *Oxypogon stuebelii*, *Grallaria milleri*, *Hapalopsittaca fuertesi*, *Dinomys branickii*, *Osornophryne percrassa*, *Pristimantis simoterus*, *Stenocercus trachycephalus*, *Andinosaura laevis*, *Atractus manizalesensis*, entre otros. |
| **Instituto de Investigación de Recursos Biológicos Alexander von Humboldt** | `http://www.humboldt.org.co/` | Libros Rojos de Aves, Mamíferos y Anfibios de Colombia | Categorías de amenaza según criterios UICN para la fauna del macizo: danta de montaña (*Tapirus pinchaque*, En Peligro - EN), oso andino (*Tremarctos ornatus*, Vulnerable - VU), cóndor andino (*Vultur gryphus*, En Peligro Crítico / Vulnerable nacional), cotorra de Fuertes (*Hapalopsittaca fuertesi*, En Peligro Crítico - CR), sapito rechoncho (*Osornophryne percrassa*, Vulnerable - VU), rana arlequín (*Atelopus simulatus*, En Peligro Crítico - CR). Sustenta `fauna.threatened_species`, `fauna.fuertes_parrot`, `fauna.harlequin_frog_atelopus`. |
| **Corporación Autónoma Regional de Risaralda (CARDER)** | `https://www.carder.gov.co/` | Informes de monitoreo de fauna ecorregional y humedales Otún | Monitoreo de fauna en la cuenca del río Otún y sector La Pastora. Diagnóstico de la presencia de danta de montaña, oso andino y pato de torrente (*Merganetta armata*). Problemática de la trucha arcoíris (*Oncorhynchus mykiss*) como especie exótica invasora en la Laguna del Otún y riesgo de perros asilvestrados. Sustenta `fauna.spotting_sector_otun`, `fauna.spotting_sector_la_pastora`, `fauna.rainbow_trout_impact`, `fauna.feral_dogs_threat`. |
| **Corporación Autónoma Regional de Caldas (Corpocaldas)** | `https://www.corpocaldas.gov.co/` | Estudios de biodiversidad y plan de manejo corredor volcánico | Registros de fauna en vertiente caldense (sectores Brisas, cuenca Chinchiná). Monitoreo de atropellamiento en el corredor vial Manizales-Murillo y presencia de *Atractus manizalesensis*, *Cerdocyon thous* y *Stenocercus*. Sustenta `fauna.spotting_sector_brisas`, `fauna.roadkill_risk_murillo_road`, `fauna.earth_snakes_atractus`. |
| **Corporación Autónoma Regional del Tolima (Cortolima)** | `https://www.cortolima.gov.co/` | Caracterización ambiental cuenca Combeima y sur del parque | Datos de avifauna y mastofauna en la cuenca del río Combeima y aproximación al Nevado del Tolima: poblaciones de loro orejiamarillo (*Ognorhynchus icterotis*) asociadas a palmas de cera, venados (*Mazama rufina*, *Odocoileus virginianus*) y pato de torrente. Sustenta `fauna.spotting_sector_combeima`, `fauna.yellow_eared_parrot`, `fauna.little_red_brocket`. |
| **eBird / The Cornell Lab of Ornithology** | `https://ebird.org/hotspot/L1142279` | Base de datos ornitológica global (consultada 2026-11-21) | Listas de chequeo, frecuencias estacionales de avistamiento y registros altitudinales de aves en el hotspot PNN Los Nevados (sectores Brisas, Otún, El Cisne, La Pastora). Sustenta hábitos, horas de mayor actividad y detalles de observación de las 27 entradas de aves. |

---

## 2. Mapeo de semillas asignadas (Semillas 24 y 25)

El encargo asignó los índices semilla cero-basados **24** y **25** del archivo semilla original `conocimiento.json`. Ambas intenciones fueron preservadas en su sustancia original, corregidas con datos del Plan de Manejo oficial y ampliadas con ≥12 ejemplos por entrada, variantes de respuesta y fuentes verificadas:

* **Índice semilla 24:**
  * *Etiqueta original:* `"las aves del parque"`
  * *Contenido original:* Mencionaba chivito de páramo, cóndor andino y periquito de los nevados, advirtiendo que la presencia en inventarios no garantiza el avistamiento.
  * *Mapeo en sección final:*
    1. Se consolidó como entrada general en `fauna.birds_overview` (*las aves del parque Los Nevados*), incorporando las cifras oficiales del Plan de Manejo (108 especies de páramo y humedales altos, >300 especies a lo largo del gradiente).
    2. Las especies emblemáticas citadas en la semilla se desarrollaron en entradas independientes y profundas: `fauna.andean_condor` (cóndor andino), `fauna.buffy_helmetcrest` (chivito de páramo), `fauna.ruiz_parakeet` (periquito de los nevados) y `fauna.andean_duck` (pato andino).
* **Índice semilla 25:**
  * *Etiqueta original:* `"los mamíferos del parque"`
  * *Contenido original:* Mencionaba danta de montaña, puma y guagua loba, con la instrucción de observar a distancia.
  * *Mapeo en sección final:*
    1. Se consolidó como entrada general en `fauna.mammals_overview` (*los mamíferos del parque Los Nevados*), añadiendo datos del Plan de Manejo (31 especies de alta montaña, 60 en el macizo).
    2. Las especies mencionadas se ampliaron en entradas especializadas con protocolos de distancia y seguridad: `fauna.mountain_tapir` (danta de montaña), `fauna.cougar_puma` (puma), `fauna.pacarana_guagua_loba` (guagua loba) y `fauna.spectacled_bear` (oso andino).

---

## 3. Hechos, inferencias, texto editorial y limitaciones

Para garantizar la integridad y transparencia documental de esta sección:

1. **Hechos respaldados:**
   * Cifras de biodiversidad (778 especies de vertebrados, 38 endémicas, 108 aves de páramo, 31 mamíferos de alta montaña, 15 reptiles) provienen textualmente del Plan de Manejo de Parques Nacionales Naturales de Colombia.
   * La envergadura alar del cóndor andino (>3 metros) y el rol de las especies focales provienen de la ficha técnica oficial de PNN.
   * Los estados de amenaza (EN, VU, CR) corresponden a las listas rojas del Instituto Humboldt y resoluciones vigentes del Ministerio de Ambiente y Desarrollo Sostenible.
   * La ausencia de serpientes venenosas por encima de 3.000 m s. n. m. está comprobada por la biología térmica de los vipéridos andinos y los registros herpetológicos de PNN, SiB Colombia y el Instituto Humboldt.
   * La prohibición de alimentar fauna, ingresar mascotas, volar drones no autorizados o cazar/colectar especímenes emana de la Ley 1333 de 2009, el Decreto Ley 2811 de 1974 y el régimen especial de PNN.
2. **Inferencias ecológicas y pautas de visita:**
   * Las recomendaciones sobre mejores horas de observación (6:00 a 9:00 a. m. para aves canoras; 10:00 a 13:00 para rapaces planeadoras por termales) se basan en los patrones biológicos estándar de actividad térmica y forrajeo documentados en ornitología andina (eBird / Humboldt).
   * Los protocolos de encuentro con oso, puma y danta sintetizan las directrices técnicas de manejo de fauna silvestre de Parques Nacionales y la UICN (no correr, hacerse ver grande, mantener distancia de 30-50 metros).
3. **Texto editorial del asistente y limitaciones:**
   * Las respuestas están redactadas en segunda persona singular ("tú"), en tono empático, pedagógico y prudente, adaptadas a una experiencia offline en teléfono móvil.
   * Las referencias en `sources` identifican el soporte factual de las afirmaciones biológicas y normativas, pero **no implican patrocinio, autoría directa ni aval institucional oficial de Parques Nacionales Naturales** hacia la aplicación móvil, su interfaz o sus algoritmos de respuesta.

---

## 4. Vacíos de información oficial

Durante la investigación se identificaron los siguientes vacíos documentales en las fuentes públicas oficiales:

1. **Censo poblacional exacto de carnívoros esquivos:** No existe un conteo absoluto y público de individuos de puma (*Puma concolor*) u oncilla (*Leopardus tigrinus*) para el área total del parque; los reportes de PNN y CARs se basan en frecuencias de captura en cámaras trampa e índices de ocupación de hábitat. Se evitó inventar cifras poblacionales de felinos.
2. **Ubicación exacta de dormideros y nidos de cóndor andino:** Por estrictas razones de conservación y prevención de perturbación turística o furtivismo, los informes oficiales de PNN omiten deliberadamente las coordenadas exactas de las paredes de anidación del cóndor andino en el macizo. La sección menciona sectores amplios (Valle de las Tumbas, riscos altos) sin georreferenciación sensible.
3. **Dinámica poblacional reciente de anfibios en zonas remotas:** Para varias especies del género *Atelopus* y *Pristimantis* no existen censos demográficos exhaustivos post-2020 en las microcuencas menos accesibles del sur del parque (zona Tolima). Se reporta su estado crítico y la amenaza del hongo quítrido sin proyectar números inventados.
4. **Fechas editoriales de actualización web:** Algunos portales institucionales no exponen una fecha de última modificación visible en el pie de página HTML; por ello, en la metadata se registra la fecha real de consulta (`2026-11-21`).

---

## 5. Conflictos entre fuentes y su resolución

1. **Riqueza de aves reportada (108 vs. >300 vs. >600 especies):**
   * *Conflicto:* Algunas publicaciones turísticas afirman que Los Nevados tiene "más de 600 especies de aves", mientras que el Plan de Manejo indica 108 especies en el páramo y ~300 en el parque.
   * *Resolución:* La cifra de ~600 abarca toda la ecorregión cafetera desde el valle del río Cauca (900 m) hasta las nieves perpetuas. Para el área protegida estricta se adoptaron las cifras oficiales de PNN: 108 especies exclusivas de páramo/humedales y >300 en el gradiente de alta montaña del parque.
2. **Taxonomía en revisión de ciervos y reptiles:**
   * *Conflicto:* El venado conejo fue tradicionalmente denominado *Pudu mephistophiles*; revisiones filogenéticas recientes lo reclasifican como *Pudella mephistophiles*. Similarmente, lagartijas previamente agrupadas en *Riama* pasaron a *Andinosaura*, y el camaleoncito *Phenacosaurus* a *Anolis*.
   * *Resolución:* En las respuestas y etiquetas se utilizaron los nombres comunes más reconocidos por visitantes y guardaparques, aclarando la sinonimia científica en el texto para máxima precisión técnica.
3. **Estatus de la trucha arcoíris en la Laguna del Otún:**
   * *Conflicto:* Portales de turismo y pesca deportiva presentan a la trucha como un atractivo recreativo, mientras que PNN y la literatura científica la catalogan como una especie exótica invasora con alto impacto sobre macroinvertebrados y anfibios nativos.
   * *Resolución:* Se dio prioridad absoluta a la posición ecológica oficial de Parques Nacionales Naturales: la trucha es una especie invasora introducida cuya pesca no autorizada y siembra están prohibidas dentro del área protegida.

---

## 6. Temas descartados y razones

* **Tours organizados de aviturismo, precios de guías y alquiler de binoculares:** Descartados de `fauna` por corresponder a `activities` (orden 8, senderos y recreación) y `booking_fees` (orden 5, tarifas y guianza obligatoria).
* **Reglamento general del parque sobre basura, fogatas y camping:** Descartados por corresponder a `rules` (orden 9). En `fauna` solo se conservaron las normas con impacto biológico directo (prohibición de alimentar animales, prohibición de mascotas por zoonosis, drones por impacto acústico, y veda total de caza).
* **Especies de selva baja no presentes en el parque:** Se descartaron registros erróneos o confusos de fauna de tierras bajas (como jaguar, caimanes, tucanes amazónicos o serpientes corales de tierra caliente), verificando que cada especie incluida cuente con presencia comprobada en el gradiente de alta montaña de Los Nevados.

---

## 7. Métricas y conteos finales de la sección

* **Sección:** `fauna` (ID: `fauna`, orden: `11`, perfil de recuperación: `explain`)
* **Total de entradas:** **90** (100 % de la meta establecida)
* **Total de ejemplos de usuario:** **1086** (promedio: 12,07 ejemplos por entrada; mínimo 12)
* **Total de negativos duros (hard negatives):** **270** (exactamente 3 negativos por entrada; rango exigido: 2 a 4)
* **Entradas destacadas (`featured`):** 5 (`fauna.andean_condor`, `fauna.spectacled_bear`, `fauna.mountain_tapir`, `fauna.buffy_helmetcrest`, `fauna.birds_overview`)
* **Preguntas de aclaración (`clarification.bank`):** 5 preguntas temáticas del espacio
* **Preguntas de slot (`slot_questions`):** 2 (`animal_group`, `sector`) vinculadas a los filtros de entidad declarados
* **Unicidad de ejemplos:** **0 ejemplos duplicados** en toda la sección (validación determinista estricta en minúsculas)
* **Longitud de etiquetas (`label`):** 100 % entre 3 y 8 palabras
* **Resultado de validación JSON Schema:** **Válido (0 errores)** contra `knowledge-section.schema.json` bajo el estándar Draft 2020-12.
