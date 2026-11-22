# Decision Log — Curator `preparation` (Agent 8)

## Environment Proof (2026-11-22)

- (a) `fetch_evidence.py` OK: HTTP 200, descargado `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/` -> `research_notes/curation_v2/evidence/preparation/pnn-nevados-ficha.txt`, sha256_raw `707966e5c9379d9c8fd782bb64c56bf9ff83894e730b47235834fa586172ef62`, fetched_at `2026-11-22T16:51:40+00:00`.
- (b) `uv run python --version` OK: Python 3.14.8.
- (c) `knowledge.py inspect --id preparation.layering_system` OK: `"status": "ok"`, `kind: "procedure"`, `audience: "visitor"`.

## Operations Log (One line per op)

- `preparation.layering_system`: update | Clarificar label para sistema de capas en montaña y blindar con hard negatives contrastivos contra poncho y ropa de niños | metadata_only
- `preparation.first_layer_thermal`: update | Clarificar label a 'primera capa térmica y ropa interior técnica' (eliminando colisión de 'impermeable y de repuesto') y contrastar con chaqueta impermeable y dry bags | metadata_only
- `preparation.second_layer_fleece`: update | Clarificar label a 'segunda capa de abrigo y buzo polar' y contrastar con primera capa y chaqueta impermeable exterior | metadata_only
- `preparation.third_layer_waterproof`: update | Clarificar label a 'chaqueta impermeable cortavientos y tercera capa exterior' y contrastar con primera capa y forro polar | metadata_only
- `preparation.rain_poncho`: update | Clarificar label a 'uso de poncho impermeable para lluvia' y contrastar con sistema de capas y vestimenta general | metadata_only
- `preparation.hiking_boots`: update | Clarificar label a 'calzado cerrado de senderismo con buen agarre' y añadir hard negatives contra guantes de páramo | metadata_only
- `preparation.thermal_gloves`: update | Clarificar label a 'guantes abrigados para el frío de páramo' y contrastar contra linterna y mapa/gps | metadata_only
- `preparation.thermal_hat`: update | Clarificar label a 'gorro térmico abrigado que cubra orejas' y contrastar contra gafas de sol y bloqueador solar | metadata_only
- `preparation.neck_gaiter`: update | Clarificar label a 'cuello térmico buff o pasa montañas' y contrastar contra buzo polar y camiseta térmica | metadata_only
- `preparation.sunglasses_uv`: update | Clarificar label a 'gafas de sol con protección ultravioleta total' y contrastar contra sombrero de ala y gorra | metadata_only
- `preparation.sunscreen`: update | Clarificar label a 'bloqueador solar factor cincuenta o superior' y contrastar contra gafas UV y sombrero de ala | metadata_only
- `preparation.sun_hat`: update | Clarificar label a 'sombrero de ala o gorra para sol' y contrastar contra gafas con protección UV | metadata_only
- `preparation.daypack_size`: update | Clarificar label a 'morral pequeño cómodo para caminata pasadía' y contrastar contra chaqueta impermeable y checklist Brisas | metadata_only
- `preparation.dry_bags`: update | Clarificar label a 'bolsas secas estancas para aislar equipaje' y contrastar contra primera capa térmica y ropa de repuesto | metadata_only
- `preparation.water_quantity`: update | Clarificar label a 'cantidad de agua e hidratación en sendero' y contrastar contra botellas permitidas y envases plásticos | metadata_only
- `preparation.reusable_bottles`: update | Clarificar label a 'cantimploras y botellas reutilizables sin desechables' y contrastar contra cantidad de agua y deshidratación | metadata_only
- `preparation.trail_snacks`: update | Clarificar label a 'snacks calóricos y alimentos ligeros de marcha' y contrastar contra desayuno previo y víveres de travesía | metadata_only
- `preparation.pre_hike_meal`: update | Clarificar label a 'desayuno y alimentación previa al ascenso' y contrastar contra snacks de marcha y bocadillo en sendero | metadata_only
- `preparation.trail_meals_multiday`: update | Clarificar label a 'víveres y comida para travesía con campamento' y contrastar contra desayuno previo y snacks ligeros | metadata_only
- `preparation.mountain_tent`: update | Clarificar label a 'carpa técnica de alta montaña tres estaciones' y contrastar contra lista de travesía y menaje de campamento | metadata_only
- `preparation.sleeping_bag`: update | Clarificar label a 'saco de dormir sleeping para baja temperatura' y contrastar contra aislante térmico y colchoneta | metadata_only
- `preparation.sleeping_pad`: update | Clarificar label a 'aislante térmico y colchoneta para campamento' y contrastar contra saco de dormir y sleeping | metadata_only
- `preparation.camp_stove`: update | Clarificar label a 'estufa portátil de gas para cocinar acampando' y contrastar contra menaje y ollas de camping | metadata_only
- `preparation.cookware_utensils`: update | Clarificar label a 'utensilios y menaje reutilizable para cocinar acampando' y contrastar contra estufa de gas y cocineta | metadata_only
- `preparation.camp_hygiene`: update | Clarificar label a 'manejo de excretas cacatubo e higiene acampando' y contrastar contra basuras y retorno de residuos | metadata_only
- `preparation.headlamp`: update | Clarificar label a 'linterna frontal de cabeza con baterías repuesto' y contrastar contra gafas de sol con protección UV | metadata_only
- `preparation.technical_glacier_gear`: update | Clarificar label a 'equipo técnico de montaña para borde glaciar' y contrastar contra botiquín y certificación médica del guía | metadata_only
- `preparation.fitness_training`: update | Clarificar label a 'preparación física y ritmo de caminata pausado' y contrastar contra hidratación y checklist de pasadía | metadata_only
- `preparation.children_gear`: update | Clarificar label a 'ropa abrigada y calzado para niños visitantes' y contrastar contra vestirse por capas para adultos | metadata_only
- `preparation.what_not_to_pack`: update | Clarificar label a 'elementos prohibidos para empacar en la mochila' y contrastar contra poncho de lluvia y menaje reutilizable | metadata_only
- `preparation.checklist_brisas_day`: update | Clarificar label a 'checklist para visita de un día en Brisas' y contrastar contra checklist de travesía con campamento | metadata_only
- `preparation.checklist_glacier_day`: update | Clarificar label a 'checklist para caminata al Nevado Santa Isabel' y contrastar contra equipo de travesía multiruta | metadata_only
- `preparation.checklist_multiday_trek`: update | Clarificar label a 'checklist para travesía de montaña con campamento' y contrastar contra checklist de pasadía en Brisas | metadata_only
- `preparation.navigation_map_gps`: update | Clarificar label a 'mapa físico brújula o GPS sin señal', enriquecer consultas de orientación offline y contrastar con radios de guías | metadata_only

## Entries Not Checked

Ninguna. Las 34 entradas de la sección `preparation` fueron auditadas e incluidas con evidencia primaria en `audit/preparation.csv` y actualizadas en `proposals/preparation.json`.

## Factual Gaps

- No se evidencian brechas en los datos fácticos de las respuestas: todas las prescripciones técnicas y numéricas (factor solar 50+, gafas UV 100%, temperaturas inferiores a 0 ºC, carpas 3-4 estaciones, prohibición de fogatas y plásticos de un solo uso) provienen fiel y literalmente de la Resolución 207 de 2023, la Resolución 1558 de 2019, la ficha oficial de Parques Nacionales y la guía de Semana Santa 2018.
- Se respetaron rigurosamente las fechas de corte normativo y la política offline, evitando cualquier aseveración de tiempo presente sobre clima o transitabilidad en tiempo real.

## Sources That Failed to Download

Ninguna. La prueba de descarga mediante `fetch_evidence.py` sobre la ficha oficial de PNN Los Nevados se completó con éxito (código HTTP 200). No se requirieron descargas adicionales ya que las 34 operaciones son exclusivamente de refinamiento de metadatos (etiquetas de 3–8 palabras, consultas contrastivas y hard negatives validados contra el corpus).

## Cross-Section Findings

Se documentaron formalmente 6 interacciones en `research_notes/curation_v2/findings/preparation.cross.json`:
1. `preparation.reusable_bottles` / `preparation.cookware_utensils` vs `rules.single_use_plastics`: delimitación entre equipo personal reutilizable a empacar y régimen de prohibiciones/sanciones de plásticos desechables.
2. `preparation.water_quantity` / `preparation.reusable_bottles` vs `services.drinking_water`: delimitación entre hidratación fisiológica recomendada en sendero y puntos físicos de abastecimiento o recarga en cabañas.
3. `preparation.technical_glacier_gear` / `preparation.checklist_glacier_day` vs `health_safety.guide_first_aid_kit_and_certification`: delimitación entre equipo técnico del montañista (suministrado por operador) y botiquín/certificación médica del guía.
4. `preparation.camp_hygiene` vs `rules.leave_no_waste` y `services.toilets`: delimitación del manejo de excretas en campamento silvestre (cacatubo/hoyo de gato) frente a baterías sanitarias y régimen general de basura.
5. `preparation.children_gear` vs `activities.children_visit_style` y `booking_fees.age_minimum`: delimitación de vestimenta infantil frente a senderos aptos y edades mínimas legales (6 y 15 años).
6. `preparation.navigation_map_gps` vs `services.guide_radios` y `health_safety.lost_person_protocol`: delimitación entre orientación personal preventiva y medios de radiocomunicación de emergencia o respuesta a extravío.
