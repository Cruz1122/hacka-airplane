# weather_volcano fix round

Fecha: 2026-11-22. Refetch UNGRD: HTTP 200 en `research_notes/curation_v2/evidence/weather_volcano/ungrd-comunidades-erupciones-refetch.txt`. La extracción nueva intercala columnas: «sin utilizar» y «agua» no quedan seguidos. El texto legado, con hash, sí trae la frase seguida.

## Revisión

- `weather_volcano.alert_yellow_meaning` revise: done. Citas del bloque Amarilla (definición, desgasificación, sismos sentidos). Se quitó «q significa la alerta amarilla».
- `weather_volcano.alert_orange_meaning` revise: done. Citas de ceniza frecuente y olores fuertes del bloque Naranja.
- `weather_volcano.alert_red_meaning` revise: done. Cita literal del encabezado (con caracteres invisibles del HTML) y «Erupción mayor (considerable) en curso».
- `weather_volcano.alert_green_meaning` revise: done. Cita de gases, olores y fuentes termales. Se quitó «no te autoriza el cráter». La UNGRD queda citada: no acercarse al volcán ni a los ríos que nacen en él.
- `weather_volcano.alert_states_nonsequential` approve: done. Copiado igual.
- `weather_volcano.old_alert_numbers` revise: done. El refetch trajo «(II) Erupción probable en término de días o semanas.» Se conserva el dato y la evidencia apunta a la descarga nueva.
- `weather_volcano.volcanic_closures` revise: done. Cita ampliada hasta «en cualquier momento se puede tomar la determinación de cierre y evacuación». Etiqueta: «cumbre y ciclomontañismo restringidos por volcán».
- `weather_volcano.yellow_upper_access` approve: done. Copiado igual.
- `weather_volcano.bulletin_kinds` revise: done. Cita «Boletines mensuales emitidos para el Volcán».
- `weather_volcano.santa_isabel_bulletin` approve: done. Copiado igual.
- `weather_volcano.machin_bulletin` approve: done. Copiado igual.
- `weather_volcano.ash_water` revise: done. Se quitó «no un veneno automático». Cita completa: el agua de ríos o quebradas cercanos al volcán puede estar contaminada. El refetch de esa frase sí cuadra.
- `weather_volcano.current_alert` revise: done. Etiqueta «dónde ver la alerta actual del Ruiz». Se devolvieron «el Observatorio de Manizales publica informes» y «cómo saber qué reportó el observatorio».
- `weather_volcano.ovsm_role` revise: done. Se quitaron esos dos ejemplos. Queda «toca revisar SGC u Observatorio».
- `weather_volcano.summit_visibility` approve: done. Copiado igual.
- `weather_volcano.snow_and_hail` approve: done. Copiado igual.
- `weather_volcano.park_weather` approve: done. Copiado igual.
- `weather_volcano.current_forecast` approve: done. Copiado igual.
- `weather_volcano.national_forecast_limit` approve: done. Copiado igual.
- `weather_volcano.helada_meaning` approve: done. Copiado igual.
- `weather_volcano.helada_night` approve: done. Copiado igual.
- `weather_volcano.orange_near_volcano` approve: done. Copiado igual.
- `weather_volcano.volcanic_activity` approve: done. Copiado igual.
- `weather_volcano.alert_not_evacuation` approve: done. Copiado igual.
- `weather_volcano.separate_volcano_alerts` approve: done. Copiado igual.
- `weather_volcano.volcanic_gases` approve: done. Copiado igual.
- `weather_volcano.gases_dilute` approve: done. Copiado igual.
- `weather_volcano.sulfur_smell` approve: done. Copiado igual.
- `weather_volcano.pyroclastic_flows` approve: done. Copiado igual.
- `weather_volcano.ballistic_blocks` approve: done. Copiado igual.

## Fuera de la propuesta v1

- `weather_volcano.ash_roofs` contradictions.json critical: done. Una orden: no empapar, no subirse, avisar al personal. No se ofrecen la limpieza en seco de la UNGRD y el rociado del SGC como alternativas. Citas: `ungrd-comunidades-erupciones.txt` y `sgc-guia-ceniza.txt`.

## Hallazgos

- contradictions `volcanic_closures` stale: done. La respuesta ya está fechada en las resoluciones 268 y 259 de 2024; la cita ahora incluye el cierre y la evacuación.
- contradictions ciclismo 2017 / `volcanic_closures`: done en este lado (restricción fechada). El plan de 2017 lo escribe activities.
- contradictions amarilla vs `hours_status.volcanic_alert_closures`: declined. `yellow_upper_access` está aprobado y ya dice que el esquema no abre ni cierra hoy. El horario lo corrige hours_status.
- labels `current_alert`: done. «dónde ver la alerta actual del Ruiz».
- labels `volcanic_closures`: done. «cumbre y ciclomontañismo restringidos por volcán».
- labels `alert_yellow_meaning`: done. Ya era «qué significa la alerta amarilla».
- labels `orange_near_volcano`, `helada_meaning`: declined. Ops aprobados; la etiqueta de v1 ya estaba justificada y el gate no deja tocarla.
- labels `park_weather`: declined. Op aprobado. La revisión dijo que el relabel no bloquea.
- taxonomy `volcanic_closures` / `hours_status.volcanic_alert_closures`: declined el merge. Siguen separadas: cumbre y ciclomontañismo aquí, color de alerta en hours.
- critical.json de esta sección: done. Los textos de alerta, boletines, agua y cierres ya estaban en v1; v2 añade las citas que faltaban.
- `_examples.json` drop «q significa la alerta amarilla»: done.
- `_examples.json` drop «el Observatorio de Manizales publica informes»: done al sacarlo de `ovsm_role`. Se restauró en `current_alert` porque la revisión y el encargo lo piden ahí, donde estaba en el corpus.
- `_examples.json` drop «con la cima tapada me salgo del sendero para la foto?»: declined. `summit_visibility` está aprobado; cambiarlo rompe `review_gate.py`.
- `health_safety.cross.json` rayos: declined. No se mueve la conducta ante el rayo a esta sección.
- `activities.cross.json` y `weather_volcano.cross.json` visibilidad: declined el traslado. La meteorología queda en `summit_visibility`.
- `history_culture.cross.json` lahar y flujos: declined. La conducta del visitante queda aquí; 1985 queda en history.
- `hours_status.cross.json`: done. Este lado no describe el cierre total de 2023; la cumbre queda fechada en 2024.
- arbiter.json: ningún id de esta sección.

## Auditoría

- `summit_visibility`, `helada_night`, `volcanic_alarm`: `quote_missing`. Hay cita para parte de la respuesta y no para «nadie puede garantizar», «cede al salir el sol» ni «no hay un sonido único». Esos tres ops no se reescribieron: dos están aprobados y el tercero no estaba en la revisión.
- `helada_meaning`, `snow_and_hail`, `volcanic_activity`, `volcanic_gases`, `lahar_visitor`: el extracto ahora es una frase que sí sostiene el dato que la revisión marcó parcial.

## Ruteo

- `n_removed_not_routing` = 1: «toca revisar SGC u Observatorio» salió de `current_alert` y queda en `ovsm_role`. El top 1 es `ovsm_role`, que responde esa pregunta (la alerta usable es el boletín del SGC). No se devolvió a `current_alert`: la revisión pide dejarlo en `ovsm_role`, y repetirlo en las dos fichas es un ejemplo duplicado.

## Aviso de refetch esperado

- `weather_volcano.ash_roofs`: la cita «Retire la ceniza de los techos, sin utilizar agua» está en el texto legado. En la descarga nueva el extractor mete la otra columna entre «sin utilizar» y «agua». No se quitó la frase: el PDF se descargó y el texto legado sigue fijado por hash.
