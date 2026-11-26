# Registro de decisiones - Fix round (wave 4) - flora_ecosystems

## 1. Revisión de operaciones de propuesta v1 (flora_ecosystems.review.json)

- `flora_ecosystems.superparamo_ecosystem`: done (ampliada la cita en pnn-los-nevados.txt para incluir paisaje lunar, extremófilos, rocas y cenizas; respuesta ajustada a la cita).
- `flora_ecosystems.high_andean_forest`: done (restaurada etiqueta previa 'bosque altoandino y selva de niebla'; ampliada la cita para incluir la declaratoria de Ceroxylon quindiuense como árbol nacional de Colombia).
- `flora_ecosystems.arenales_volcanicos_ecosystem`: done (restaurada etiqueta previa 'arenales volcánicos y paisaje lunar superpáramo'; agregada cita de recorrido Brisas-Arenales-Valle de las Tumbas).
- `flora_ecosystems.frailejones_overview`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.wax_palm_quindio`: done (adoptada etiqueta 'palma de cera del Quindío' de labels.json; ampliada la cita a bosques altoandinos o nublados).
- `flora_ecosystems.chite_hypericum`: done (retirado término 'chite' de la etiqueta, adoptando 'velillos del género Hypericum').
- `flora_ecosystems.romeros_diplostephium`: done (restaurada etiqueta previa 'romeros de páramo y herbáceas senecio').
- `flora_ecosystems.cacho_de_venado_loricaria`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.pajonales_calamagrostis`: done (restaurada etiqueta previa 'pajonales y pastizales del páramo').
- `flora_ecosystems.cojines_plantago_rigida`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.high_andean_wetlands`: done (restaurada etiqueta previa 'humedales altoandinos lagunas y turberas'; retiradas afirmaciones no sustentadas en la cita de PNN).
- `flora_ecosystems.ramsar_otun_wetland_complex`: done (retirado extracto manual ramsar-otun-1781.txt y URL externa tras bloqueo HTTP 418 en refetch; preservada fuente oficial PNN y retirada afirmación de vulnerabilidad).
- `flora_ecosystems.cattle_grazing_impact`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.ecological_restoration_programs`: done (acotada respuesta a conservación, mantenimiento y restauración sustentadas textualmente en la cita).
- `flora_ecosystems.glaciers_share_of_park`: done (indicado 'sin fecha' para la cifra del 1,82 % de la ficha PNN; retirada afirmación sobre variación con deshielo).
- `flora_ecosystems.espeletia_centroandina_otun`: done (adoptada etiqueta 'características y categoría del frailejón' de labels.json; fechada la categoría UICN en 2006; citadas fuentes PNN y RIS Ramsar).
- `flora_ecosystems.complex_flora_1036`: done (adoptada etiqueta 'número de especies de flora del complejo' de labels.json, retirando 'vascular'; removida pregunta de plantas endémicas en ejemplos).
- `flora_ecosystems.complex_endemic_plants`: done (restaurada etiqueta previa 'plantas endémicas del complejo').
- `flora_ecosystems.otun_wetland_mosaic`: done (adoptada etiqueta 'lagunas y pantanos que rodean el Otún' de labels.json; mantenida respuesta base sin afirmaciones florísticas no citadas).
- `flora_ecosystems.otun_main_wetland`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.otun_peatland_plants`: dropped (instrucción de revisión de mantener la etiqueta previa dejó la operación sin cambios frente al corpus).
- `flora_ecosystems.santa_isabel_projection_three_years`: done (aprobada en revisión v1; preservada byte a byte).
- `flora_ecosystems.santa_isabel_five_relicts`: dropped (instrucción de revisión de mantener la etiqueta previa dejó la operación sin cambios frente al corpus).
- `flora_ecosystems.santa_isabel_low_altitude_cause`: done (restaurada etiqueta previa 'causa del retroceso rápido del Santa Isabel'; cita cambiada a ideam-nevado-santa-isabel.html).
- `flora_ecosystems.santa_isabel_retreat_below_4900`: dropped (instrucción de revisión de mantener la etiqueta previa dejó la operación sin cambios frente al corpus).
- `flora_ecosystems.glaciers_snow_presence`: done (aprobada en revisión v1; preservada byte a byte).

## 2. Hallazgos (findings)

- `contradictions.json` (`flora_ecosystems.conejeras_extinct_march_2024`): done (incorporada op en v2 retirando 'marzo de 2024' de la variante y citando el intervalo 'entre diciembre de 2023 y febrero de 2024' de ideam-nevado-santa-isabel.html).
- `contradictions.json` (`flora_ecosystems.native_species_nurseries`): declined: el vivero a 3.850 m ya está distinguido de la cabaña de control a 3.920 m de services.potosi_cabin; no existe contradicción interna en flora_ecosystems ni cita de cabaña en la evidencia de viveros.
- `contradictions.json` (`flora_ecosystems.santa_isabel_projection_three_years`): done (op aprobada en v1 separando la proyección IDEAM 2024 de la ficha 2028; preservada byte a byte).
- `arbiter.json` (`flora_ecosystems.laguna_del_otun_ecosystem`, `flora_ecosystems.otun_river_supplies_pereira`, `geography.laguna_otun`): done (incorporada op en v2 retirando 'a que altura esta la laguna del otun' de laguna_del_otun_ecosystem y adoptando etiqueta de labels.json; altitud de 4.000 m se mantiene en otun_river_supplies_pereira y geography.laguna_otun).
- `taxonomy.json` (`flora_ecosystems.complex_endemic_plants`, `flora_ecosystems.complex_flora_1036`): done (contrastadas etiquetas; retiradas preguntas por 'cuántas plantas endémicas' de complex_flora_1036 y no repetido el total en complex_endemic_plants).
- `labels.json` (`flora_ecosystems.glaciers_snow_presence`): declined: op aprobada byte a byte en revisión v1; review_gate.py exige preservarla intacta.
- `labels.json` (`flora_ecosystems.wax_palm_quindio`): done (adoptada 'palma de cera del Quindío').
- `labels.json` (`flora_ecosystems.complex_flora_1036`): done (adoptada 'número de especies de flora del complejo').
- `labels.json` (`flora_ecosystems.conservation_target_values`): declined: no formó parte de la propuesta v1 y mantiene su alcance temático de cuencas y glaciares sin colisión en routing.
- `labels.json` (`flora_ecosystems.espeletia_centroandina_otun`): done (adoptada 'características y categoría del frailejón').
- `labels.json` (`flora_ecosystems.otun_wetland_mosaic`): done (adoptada 'lagunas y pantanos que rodean el Otún').
- `labels.json` (`flora_ecosystems.high_andean_wetlands`): declined: el revisor ordenó explícitamente conservar la etiqueta previa 'humedales altoandinos lagunas y turberas'.
- `labels.json` (`flora_ecosystems.glacier_retreat_climate_change`): declined: no formó parte de la propuesta v1 y describe el retroceso general documentado en IDEAM.
- `labels.json` (`flora_ecosystems.laguna_del_otun_ecosystem`): done (adoptada 'páramo y humedales alrededor de la laguna').
- `labels.json` (`flora_ecosystems.santa_isabel_projection_three_years`): declined: op aprobada byte a byte en revisión v1; preservada intacta.
- `labels.json` (`flora_ecosystems.otun_wetlands_glacial_origin`): declined: no formó parte de la propuesta v1; preserva delimitación frente a geography.
- `labels.json` (`flora_ecosystems.glacial_hollow_lagoons`): declined: no formó parte de la propuesta v1.
- `critical.json` (`actions.report_altitude_sickness` / `flora_ecosystems.glaciers_snow_presence`): declined: glaciers_snow_presence fue aprobada en v1; la regla 1 exige mantenerla byte a byte en esta ronda.
- `findings/*.cross.json` (`actions.cross.json`, `geography.cross.json`, `history_culture.cross.json`, `activities.cross.json`, `flora_ecosystems.cross.json`): done (delimitaciones temáticas mantenidas: flora conserva ecosistemas, historia de incendios pasados, humedales y dinámica glaciar; no invade reportes en tiempo real de actions, geología de geography ni guianza de activities).
- `reviews/_examples.json`: done (cero ejemplos listados para flora_ecosystems en la lista de drop).

## 3. Justificación de routing (route_check.py)

- `flora_ecosystems.laguna_del_otun_ecosystem` (`a que altura esta la laguna del otun`): retirado intencionalmente conforme al arbitraje de `findings/arbiter.json`, dado que dicha entrada describe la vegetación y humedales circundantes y no responde a la altitud del lago. La consulta enruta correctamente hacia `geography.laguna_otun` (top 1) y `flora_ecosystems.otun_river_supplies_pereira`, que sí responden la cota altimétrica de 4.000 m.

## 4. Auditoría CSV (audit/flora_ecosystems.csv)

- Corregidas las 7 filas calificadas con soporte `none` en la revisión independiente con citas textuales y exactas (en `pnn-los-nevados.txt`, `ideam-glaciares-2024.txt`, `ideam-nevado-santa-isabel.html` y `pnn-incendio-africa-2026.html`).
- Reclasificadas a `secondary_only` las filas `partial` donde la entrada del corpus contiene datos secundarios o compilados (CARDER, Corpocaldas, Humboldt 2017) sin cita primaria específica para cada cifra en el repositorio, o actualizados sus extractos a citas completas para las entradas modificadas en v2.
- Ningún `primary_ok` con soporte `none` permanece en la auditoría.
