# Registro de decisiones - Ronda Fix (Wave 4) - activities

## Review Items (proposals/activities.json v1 -> v2)

- activities.cloudy_visit_landscape: done (conservada etiqueta nueva justificada por contraste con weather_volcano.summit_visibility; audit row degradada a quote_missing al no haber cita oficial de política con cima tapada).
- activities.snow_and_glacier_access: done (conservada etiqueta nueva; retirada HN 'se puede ver hielo en la visita al nevado' por ser consulta propia y reemplazada por ejemplo de flora_ecosystems).
- activities.birdwatching: done (restaurada etiqueta anterior 'observación de aves en la visita' por indicación del revisor; contrastes preservados).
- activities.wildlife_from_trail: done (restaurada etiqueta anterior 'observar fauna y flora' por indicación del revisor; contrastes preservados).
- activities.termales_canon: done (restaurada etiqueta anterior 'Termales del Cañón en la ruta'; aseguradas HNs contrastivas no propias).
- activities.therapeutic_baths_banned: done (restaurada etiqueta anterior 'baños en lagunas o termales'; aseguradas HNs contrastivas con servicios sanitarios).
- activities.camping_cisne: done (conservada etiqueta nueva 'condición del camping en el centro El Cisne'; retirada HN 'puedo quedarme en el centro El Cisne' por ser consulta propia).
- activities.horseback_not_allowed: done (restaurada etiqueta anterior 'cabalgata turística en el parque'; retirada HN ambigua sobre mulas y reemplazada por ejemplos contrastivos de arriería).
- activities.north_route_stops: done (restaurada etiqueta anterior 'paradas del carreteable norte' por indicación del revisor).
- activities.aguacerales_stop: done (restaurada etiqueta anterior 'parada Aguacerales del norte'; retirada HN cuasi-copia 'Aguacerales queda en el recorrido norte').
- activities.conejeras_glacier_edge: done (restaurada etiqueta anterior 'sendero Conejeras al borde glaciar' por indicación del revisor).
- activities.south_glacier_edge: done (restaurada etiqueta anterior 'borde glaciar sur de Santa Isabel' por indicación del revisor).
- activities.unlisted_activities: done (restaurada etiqueta anterior 'actividades que no aparecen publicadas' por indicación del revisor).
- activities.ski_and_canyoning: done (restaurada etiqueta anterior 'esquí de montaña y barranquismo'; retirada HN propia 'puedo esquiar en el nevado' y reemplazada por ejemplo de unlisted_activities).
- activities.cycling_roads_2017: done (restaurada etiqueta anterior 'vías del ciclomontañismo en el plan' por indicación del revisor).
- activities.regulated_sports: done (restaurada etiqueta anterior 'ciclomontañismo y trail running' por indicación del revisor).
- activities.potosi_laguna_road: done (restaurada etiqueta anterior 'carreteable de Potosí a la laguna'; retirada HN propia 'la laguna se entra por potosi' y reemplazada por acceso vehicular).
- activities.laguna_verde: done (restaurada etiqueta anterior 'sendero al mirador Laguna Verde'; retirada HN propia 'dónde queda la Laguna Verde' y reemplazada por ejemplo contrastivo de geografía).
- activities.camping_where: done (resuelto conflicto crítico de camping en Arenales con respuesta fechada y ambas citas oficiales de Res. 207/2023 e informe 2024; restaurada etiqueta anterior 'dónde acampar en el parque'; retirada HN propia 'dónde se puede acampar en Los Nevados').
- activities.otun_cedral_walk: done (restaurada etiqueta anterior 'caminata El Cedral a Laguna del Otún'; retiradas tres HNs propias y reemplazadas por consultas contrastivas de acceso desde Pereira).
- activities.day_or_multiday: done (restaurada etiqueta anterior 'visita corta o de varios días'; retiradas dos HNs propias y reemplazadas por consultas de acceso vehicular vs pie).
- activities.brisas_valle_tumbas: done (restaurada etiqueta anterior 'recorrido Brisas al Valle de las Tumbas'; reemplazadas tres HNs propias por consultas contrastivas a pie y geográficas).

## Mandatory Findings & Critical Items

- critical.json activities.conejeras_hut: done (actualizada en proposal con fuente primaria oficial informe 2024, eliminando afirmaciones no respaldadas sobre servicios o albergue y con cita verbatim verificada).
- critical.json activities.mirador_laguna_otun: done (actualizada en proposal con fuente primaria oficial informe 2024, eliminando afirmaciones no respaldadas sobre tiempos de caminata y con cita verbatim verificada).
- contradictions.json Match 2 (activities.camping_where, activities.camping_tolima, activities.camping_brisas_restricted): done (resuelto en activities.camping_where separando Arenales norte no habilitado en 2024 de Arenales Tolima transitorio 2023 y requiriendo confirmación oficial previa).
- contradictions.json Match 1 (activities.sector_laguna_otun cotas): declined: la entrada describe el sector general y no fija cotas contradictorias; el ajuste numérico corresponde a access y flora.
- contradictions.json Match 3 (activities.cycling_roads_2017 y regulated_sports): done (mantenida atribución histórica al plan 2017 y etiqueta anterior).
- contradictions.json Match 4 (activities.unlisted_activities y prohibición nocturna): done (etiqueta anterior restaurada y fila de auditoría degradada a quote_missing).
- contradictions.json Match 5 (activities.calvito_overnight y porteo): done (se mantiene la prohibición en Calvito/Arenales; arriería de carga se delega a services).
- contradictions.json Match 6 (activities.therapeutic_baths_banned y baños de salud): done (se mantiene prohibición de ingreso a cuerpos de agua y etiqueta anterior).

## Taxonomy, Labels & Arbiter Findings

- taxonomy.json birdwatching vs wildlife_from_trail: done (contrastadas en etiquetas y ejemplos).
- taxonomy.json camping_cisne vs services.cisne_visitor_center: done (contrastadas carpa vs camas).
- taxonomy.json horseback_not_allowed vs services.mule_luggage: done (contrastada prohibición turística vs arriería de carga).
- taxonomy.json activities.horseback_not_allowed (move to rules): declined: por regla de BRIEF_FIX.md los traslados los gestiona la sección receptora en su archivo; activities mantiene la entrada.
- taxonomy.json activities.therapeutic_baths_banned (move to rules): declined: traslado corresponde a rules; activities mantiene la entrada en este lote.
- taxonomy.json activities.ski_and_canyoning (move to rules): declined: traslado corresponde a rules; activities mantiene la entrada en este lote.
- taxonomy.json access.cedral_walk_distances vs activities.otun_cedral_walk: done (entrada sobreviviente activities.otun_cedral_walk conservada).
- labels.json activities.cloudy_visit_landscape: done (etiqueta conservada).
- labels.json activities.birdwatching: done (etiqueta anterior restaurada por revisor).
- labels.json activities.termales_canon: done (etiqueta anterior restaurada por revisor).
- labels.json activities.camping_cisne: done (etiqueta nueva aceptada por revisor).
- labels.json activities.otun_cedral_walk: done (etiqueta anterior restaurada por revisor).
- labels.json activities.potosi_laguna_road: done (etiqueta anterior restaurada por revisor).
- labels.json activities.aguacerales_stop: done (etiqueta anterior restaurada por revisor).
- labels.json activities.interpretive_hiking: declined: la etiqueta original fue validada sin objeciones por el revisor.
- labels.json activities.cycling_roads_2017: done (etiqueta anterior restaurada por revisor).
- labels.json activities.calvito_overnight: declined: etiqueta original no requirió cambio.
- arbiter.json (todos los pares de contraste que involucran activities): done (contrastes reflejados en etiquetas y hard negatives de las operaciones de activities).
- cross findings (*.cross.json que nombran activities): done (alineación semántica implementada).

## Explicación de advertencias en verify_evidence (--refetch)

- activities.camping_where, activities.mirador_laguna_otun, activities.conejeras_hut: advierten que las citas no se encontraron en la descarga en vivo de `Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx`. Esto ocurre porque el archivo remoto es un zip/docx binario que `extract_text` no descomprime en texto plano en tiempo real; el contenido está respaldado y verificado por hash SHA256 en el archivo legado `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/raw/pnn_informe_necesidades_2024.txt` registrado en `legacy_evidence_manifest.json`.

## Auditoría CSV (audit/activities.csv)

- Total filas: 70.
- primary_ok: 30 (26 aprobadas en revisión completa + 4 entradas corregidas con citas textuales íntegras: camping_where, mirador_laguna_otun, conejeras_hut, cambio_climatico_trail).
- quote_missing: 40 (degradadas honestamente desde partial/none tras dictamen del revisor independiente, eliminando afirmaciones no sustentadas en excerpts).
