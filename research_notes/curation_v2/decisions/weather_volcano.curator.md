# weather_volcano curator — decision log

## Operaciones

- `weather_volcano.alert_yellow_meaning` update: fecha el esquema del SGC (14 de septiembre de 2023) y deja la frase de alerta amarilla en esta ficha. Evidencia: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-cambio-esquema.txt`, `sgc-estados-alerta.txt`.
- `weather_volcano.alert_orange_meaning` update: fecha naranja y la separa de los lahares pequeños junto al cráter y del color de hoy. Evidencia: `sgc-cambio-esquema.txt`, `sgc-estados-alerta.txt`.
- `weather_volcano.alert_red_meaning` update: fecha roja y dice que esta ficha no sabe si hoy está en rojo. Evidencia: `sgc-cambio-esquema.txt`, `sgc-estados-alerta.txt`.
- `weather_volcano.alert_green_meaning` update: fecha verde; reposo no es el color de hoy ni permiso para el cráter. Evidencia: `sgc-cambio-esquema.txt`, `sgc-estados-alerta.txt`.
- `weather_volcano.alert_states_nonsequential` update: fecha el esquema no secuencial y la etiqueta apunta al salto de colores. Evidencia: `sgc-transiciones.txt`.
- `weather_volcano.old_alert_numbers` update: la escala numérica termina el 14 de septiembre de 2023; el folleto de la UNGRD es ese PDF, no el boletín de hoy. Evidencia: `sgc-tabla-alertas.txt`, `sgc-transiciones.txt`, `ungrd-comunidades-erupciones.txt`.
- `weather_volcano.volcanic_closures` update: fecha las resoluciones 268 y 259 de 2024; su frase de amarilla y la cumbre restringida no son el estado de hoy. Evidencia: `pnn-res-259-2024.txt`, `pnn-res-268-2024.txt`.
- `weather_volcano.yellow_upper_access` update: separa la recomendación de parte alta (2023) de la restricción de cumbre de 2024 y del ingreso de hoy. Evidencia: `pnn-res-268-2024.txt`, `sgc-cambio-esquema.txt`, `sgc-estados-alerta.txt`.
- `weather_volcano.bulletin_kinds` update: el «últimos 20» es el texto de la página, con el boletín del 10 al 16 de noviembre de 2026 como ejemplo que puede ya no servir. Evidencia: `sgc-machin-boletines.txt`, `sgc-ruiz-boletines.txt`.
- `weather_volcano.santa_isabel_bulletin` update: la frase de reposo de la ficha no es la alerta de hoy; el boletín del 10 al 16 de noviembre de 2026 es un ejemplo fechado. Evidencia: `sgc-santa-isabel-boletin-2026-11-10-16.txt`, `sgc-santa-isabel-generalidades.txt`.
- `weather_volcano.machin_bulletin` update: la ficha mezcla cambios frente al nivel base y la frase de reposo; la lista incluye el 10 al 16 de noviembre de 2026 y no fija el estado de hoy. Evidencia: `sgc-machin-boletines.txt`, `sgc-machin-generalidades.txt`.
- `weather_volcano.ash_water` update: la guía del SGC habla de sabor desagradable, no de agua no apta; la UNGRD pide no beber de ríos de montaña y tapar depósitos. Evidencia: `sgc-guia-ceniza.txt`, `ungrd-comunidades-erupciones.txt`.
- `weather_volcano.current_alert` update: la etiqueta queda en la alerta de hoy y salen las preguntas del observatorio. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.ovsm_role` update: esas tres preguntas pasan aquí; el observatorio vigila desde 1986 y la alerta es el boletín del SGC. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.summit_visibility` update: separa «¿se verá la cumbre?» del paseo nublado y de la nieve. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.snow_and_hail` update: la nevada documentada no es el clima general del parque. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.park_weather` update: el clima general no absorbe la nevada ni la visibilidad de la cumbre. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.current_forecast` update: dónde abrir el pronóstico no es el límite del mapa nacional ni el clima general. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.national_forecast_limit` update: el mapa de tres días es nacional, no el sendero ni una cumbre despejada. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.helada_meaning` update: la definición de 0 °C no es el horario de la helada de radiación ni la nieve. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.helada_night` update: la helada de radiación al amanecer no es la definición meteorológica ni la nieve. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.orange_near_volcano` update: el riesgo junto al cráter en naranja no es el significado general del color. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.volcanic_activity` update: lo que mide un boletín no es el color de hoy ni la nota del observatorio. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.alert_not_evacuation` update: el color no es por sí solo la orden de evacuar ni el boletín de cada volcán. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.separate_volcano_alerts` update: cada volcán tiene su boletín; no es la orden de evacuar ni el color de hoy del Ruiz. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.volcanic_gases` update: qué gases emite el Ruiz no es el olor a azufre ni la dilución antes del pueblo. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.gases_dilute` update: la dilución no responde qué gases hay ni si el olor autoriza el cráter. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.sulfur_smell` update: el olor a azufre no es la lista de gases ni la definición de verde. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.pyroclastic_flows` update: el flujo piroclástico no es el proyectil balístico. Evidencia: sin evidencia (solo metadatos).
- `weather_volcano.ballistic_blocks` update: los bloques cerca del cráter no son el flujo piroclástico ni el lahar pequeño. Evidencia: sin evidencia (solo metadatos).

Los `.txt` de evidencia están en `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/`.

## Frase que debe seguir aquí

- `weather_volcano.alert_yellow_meaning` conserva `qué significa alerta amarilla del Ruiz` y suma `qué significa alerta amarilla`. La etiqueta pasa a `qué significa la alerta amarilla`.

## Comprobación de rutas

- `route_check`: `n_removed_not_routing` = 3. Los tres salieron de `weather_volcano.current_alert` y el top 1 es `weather_volcano.ovsm_role`, que es quien responde.
- `el Observatorio de Manizales publica informes` → ovsm_role, access.letras_highway, access.uton_offices_manizales. Pregunta si el observatorio publica; la ficha dice que vigila desde 1986 y que la alerta es el boletín del SGC.
- `cómo saber qué reportó el observatorio` → ovsm_role, volcanic_activity, conversation.info_source_trust. El reporte del observatorio no es el color de hoy.
- `toca revisar SGC u Observatorio` → ovsm_role, volcanic_activity, conversation.history_storage. La ficha distingue el observatorio del boletín del SGC.
- `stage`: status staged, warnings vacíos. `verify_evidence`: fail []. `audit_check`: fail [].

## No comprobado, huecos, descargas, cruces

- Entradas sin revisar: ninguna. Las 54 tienen fila en `audit/weather_volcano.csv` y un pasaje leído en evidencia fijada de la fase 2.
- Hueco: no se sirve el color de alerta de hoy. El ejemplo fechado sigue siendo el boletín del Ruiz del 10 al 16 de noviembre de 2026.
- Hueco: el índice de boletines del Tolima no está en el corpus (404 en la fase 2). No se inventa `tolima_bulletin`.
- Hueco: la página del IDEAM «El clima en alta montaña» sigue sin respaldo redescargado. No vuelven meses, milímetros ni el gradiente de −5,4 °C.
- Hueco: no hay frecuencia oficial de granizo.
- Descargas fallidas en esta curación: ninguna. No hizo falta un fetch nuevo: cada URL citada ya estaba en el manifiesto legado.
- Cruces: `research_notes/curation_v2/findings/weather_volcano.cross.json` (3).
