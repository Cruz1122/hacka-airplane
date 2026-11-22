# Investigación de `weather_volcano`

Consulta y redacción: 2026-11-21. El JSON contiene 16 entradas, 208 ejemplos, 32 hard negatives y una fecha `last_verified` en cada entrada. La sección mantiene perfil `safety` y no sirve como hecho permanente ningún nivel actual de alerta, pronóstico, cierre o emisión.

## Fuentes oficiales leídas

Todas las citas cortas están guardadas en `weather_volcano/evidence/`.

| Fuente | URL | Uso |
|---|---|---|
| IDEAM, clima en alta montaña | http://www.ideam.gov.co/web/otros-ecosistemas/investigacion-y-publicaciones?_31_INSTANCE_x5l2d9DnqhhZ_struts_action=%2Fimage_g | Clima intertropical frío, periodos húmedos/secos, precipitación, temperatura, humedad y gradiente altitudinal. Evidencia: `ideam-high-mountain.txt`. |
| Parques Nacionales, ficha PNN Los Nevados | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | Régimen bimodal y variación por pisos térmicos. Evidencia previa: `pnn-page-extracted.txt`; mapeo complementario en `pnn-snow-and-climate.txt`. |
| Parques Nacionales, nevada del 10 de octubre de 2025 | https://www.parquesnacionales.gov.co/sala-prensa/noticias/una-de-las-nevadas-mas-grandes-del-ano-cubre-el-parque-nacional-natural-los-nevados/ | Nieve documentada y condiciones que la favorecieron; no es pronóstico. Evidencia: `pnn-snow-and-climate.txt`. |
| SGC, esquema de estados de alerta | https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx | Significados y recomendaciones generales de amarillo, naranja y rojo. Evidencia: `sgc-alert-states.txt`. |
| SGC, explicación del esquema | https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx | Los estados no son secuenciales ni predicen un plazo de días/semanas. Evidencia: `sgc-alert-transitions.txt`. |
| SGC, boletines del Nevado del Ruiz | https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/boletines-volcan-nevado-del-ruiz.aspx | Canal oficial con boletines semanales, mensuales y extraordinarios. Evidencia: `sgc-ruiz-bulletins.txt`. |
| SGC, boletín del 10–16 de noviembre de 2026 | https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf | Ejemplo fechado de parámetros monitoreados y recomendación de consultar canales oficiales. No se copia su estado dinámico. Evidencia: `sgc-ruiz-bulletin-2026-11-10-16.txt`. |
| UNGRD, preparación ante erupciones | http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1 | Refugio, protección respiratoria, cierre de aberturas, distancia del volcán y diferencia entre alerta y evacuación. Evidencia: `ungrd-ash-actions.txt`. |
| SGC, hoja informativa del Nevado del Ruiz | https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf | Gases volcánicos y efectos irritantes del dióxido de azufre. Evidencia: `sgc-gases.txt`. |
| SGC, mapa de amenaza volcánica: gases | https://www2.sgc.gov.co/sgc/volcanes/VolcanAzufral/Paginas/Mapa-de-amenaza.aspx | Apoyo adicional sobre gases, sin convertirlo en medición localizada del Ruiz. Evidencia: `sgc-gases.txt`. |
| Parques Nacionales, resoluciones 259 y 268 de 2024 | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/10/Res.-No.-259-del-09-de-octubre-de-2024-PFFO-022-2024.pdf y https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf | Restricciones de cumbre/ciclomontañismo y posibilidad de cierre/evacuación por actividad volcánica. Evidencia: `pnn-volcanic-restrictions.txt`. |
| Alcaldía de Manizales, información del OVSM | https://centrodeinformacion.manizales.gov.co/el-detras-de-camaras-del-monitoreo-a-un-volcan-amenazante/ | Participación del Observatorio Vulcanológico y Sismológico de Manizales en el monitoreo que alimenta boletines del SGC. Evidencia: `ovsm-manizales-monitoring.txt`. |

## Resolución de conflictos y límites

- **Clima:** la ficha de Parques da el patrón general, mientras que IDEAM aporta el detalle climatológico de alta montaña. Se usa IDEAM para cifras y meses, y Parques para el contexto del parque. No se presenta ningún valor como pronóstico.
- **Terminología volcánica:** documentos antiguos usan “nivel de actividad” y la escala anterior; se prioriza el esquema actual del SGC, que habla de “estados de alerta”. La entrada de transición explica que los colores no son una secuencia ni una cuenta regresiva.
- **Boletín fechado:** se leyó el boletín del 17 de noviembre de 2026, pero su estado y observaciones pueden haber cambiado al 21 de noviembre. Se usa para explicar qué contiene un boletín, no para fijar la alerta vigente.
- **Restricciones:** las resoluciones de 2024 prueban que la actividad volcánica puede limitar cumbre, ciclomontañismo, cierre o evacuación; no prueban el cierre vigente de cada sector. El JSON remite a los avisos actuales.
- **Nieve, granizo, niebla y visibilidad:** hay evidencia de una nevada documentada y de nubosidad/humedad alta. No se encontró una frecuencia oficial de granizo ni un pronóstico de visibilidad por fecha; las respuestas no prometen nieve, granizo o cumbres despejadas.

## Vacíos que quedan explícitos

- No se sirve la alerta vigente del Nevado del Ruiz.
- No se sirve un pronóstico meteorológico concreto para fecha, hora o sector.
- No se afirma frecuencia, acumulación o pronóstico de granizo.
- No se da una concentración “segura” de gases ni diagnóstico médico; ante síntomas o irritación se indica alejarse y seguir al guía/autoridad.
- No se convierten cierres por actividad volcánica en horarios generales: esos corresponden a `hours_status`.

## Temas recuperados, fusionados o descartados

- `park_climate`, `bimodal_rainfall` y `seasonal_weather` se consolidaron en `park_weather` y `rainy_seasons` para evitar tres entradas casi idénticas.
- `weather_by_elevation`, `summit_visibility`, `daily_forecast`, `ruiz_volcano_activity` y `current_alert` se conservaron con nombres curatoriales nuevos y respuestas limitadas a su evidencia.
- `alert_levels_meaning` se dividió en `alert_yellow_meaning`, `alert_orange_meaning`, `alert_red_meaning` y `alert_states_nonsequential`, ahora que la guía oficial del SGC sí fue leída.
- `ash_emission` se convirtió en `ash_actions` con recomendaciones de UNGRD/SGC; no afirma que haya ceniza ahora.
- Se añadieron `snow_and_hail`, `volcanic_gases`, `bulletin_channels`, `volcanic_activity` y `volcanic_closures` con citas específicas.
- Historia de erupciones, Armero y lahares históricos siguen fuera, en `history_culture`. Ropa, salud, horarios y cierres ambientales siguen en sus secciones propias.

## Round 2 — 2026-11-21

Entradas: 16 / 208 ejemplos → 56 / 688 ejemplos. No se borró ningún id. Las 16 respuestas se reescribieron: la página Liferay del IDEAM «El clima en alta montaña» no volvió a descargarse (HTTP sin respuesta, HTTPS 404), así que salieron los meses, los milímetros, la humedad del 70 % y el gradiente de −5,4 °C/1000 m. `snow_and_hail` ya no afirma granizo. `current_forecast` deja de citar la portada del IDEAM. El hard negative inventado «qué ropa llevar al parque los nevados» se reemplazó por ejemplos reales de otras secciones.

Ids nuevos: `no_temperate_seasons`, `freezing_at_altitude`, `helada_meaning`, `helada_night`, `national_forecast_limit`, `alert_green_meaning`, `eruptions_not_predictable`, `old_alert_numbers`, `alert_not_evacuation`, `yellow_upper_access`, `yellow_ash_wind`, `felt_quakes`, `orange_near_volcano`, `red_rivers_roads`, `red_crater_storms`, `bulletin_kinds`, `santa_isabel_bulletin`, `tolima_bulletin`, `machin_bulletin`, `separate_volcano_alerts`, `ovsm_role`, `ash_contacts`, `ash_water`, `ash_driving`, `ash_roofs`, `ash_asthma`, `stay_safe_zone`, `lahar_visitor`, `ruiz_rivers`, `tolima_lahars`, `do_not_approach`, `gases_dilute`, `pyroclastic_flows`, `ballistic_blocks`, `red_column_collapse`, `sulfur_smell`, `rain_by_department`, `ash_resuspends`, `evacuation_route`, `volcanic_alarm`.

Descargas en `weather_volcano/evidence/raw/` (2026-11-21):

| Archivo | URL |
|---|---|
| `pnn-nevados.html` | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ |
| `pnn-nevada-2025.html` | https://www.parquesnacionales.gov.co/sala-prensa/noticias/una-de-las-nevadas-mas-grandes-del-ano-cubre-el-parque-nacional-natural-los-nevados/ |
| `pnn-res-268-2024.pdf` | https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf |
| `pnn-res-259-2024.pdf` | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/10/Res.-No.-259-del-09-de-octubre-de-2024-PFFO-022-2024.pdf |
| `ideam-frio-faq.html` | https://ideam.gov.co/atencion-y-servicios-a-la-ciudadania/preguntas-frecuentes/en-colombia-donde-hace-mas-frio |
| `ideam-helada-glosario.html` | https://www.ideam.gov.co/atencion-y-servicios-a-la-ciudadania/glosario/helada-alertas-hidrologicas |
| `ideam-heladas-2012.pdf` | https://bart.ideam.gov.co/meteorologia/NOTAS_TECNICAS/NT_IDEAM-2012-000_HELADAS.pdf |
| `ideam-pronosticos-alertas.html` | https://www.ideam.gov.co/pronosticos-y-alertas |
| `ideam-bptd.html` | https://www.ideam.gov.co/sala-de-prensa/boletines/Boletín-de-Pronóstico-Nacional-del-Tiempo-para-Tres-Días-(BPTD) |
| `ideam-caldas-lang-2025.pdf` | https://bart.ideam.gov.co/meteorologia/NOTAS_TECNICAS/NT_IDEAM-2025-003_ACTUALIZACION_CALDAS_LANG.pdf |
| `sgc-estados-alerta.html` | https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx |
| `sgc-transiciones.html` | https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx |
| `sgc-cambio-esquema.html` | https://www2.sgc.gov.co/Noticias/Paginas/Colombia-cambia-su-esquema-de-medicion-de-la-actividad-volcanica.aspx |
| `sgc-tabla-alertas.pdf` | https://www2.sgc.gov.co/Noticias/tpaginas/Tabla-Esquema-estados-de-alerta-volcanes-SGC.pdf |
| `sgc-ruiz-boletines.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/boletines-volcan-nevado-del-ruiz.aspx |
| `sgc-ruiz-boletin-2026-11-10-16.pdf` | https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf |
| `sgc-santa-isabel-boletin-2026-11-10-16.pdf` | https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_de_Santa_Isabel_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf |
| `sgc-ruiz-generalidades.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/generalidades-volcan-nevado-ruiz.aspx |
| `sgc-santa-isabel-generalidades.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadodeSantaIsabel/Paginas/generalidades-volcan-nevado-santa-isabel.aspx |
| `sgc-tolima-generalidades.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoTolima/Paginas/generalidades-volcan-nevado-tolima.aspx |
| `sgc-machin-generalidades.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/generalidades-volcan-cerro-machin.aspx |
| `sgc-machin-boletines.html` | https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/Boletines-Volcan-Cerro-Machin.aspx |
| `sgc-hoja-ruiz.pdf` | https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf |
| `sgc-guia-ceniza.pdf` | https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf |
| `ungrd-comunidades-erupciones.pdf` | http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1 |
| `ovsm-manizales.html` | https://centrodeinformacion.manizales.gov.co/el-detras-de-camaras-del-monitoreo-a-un-volcan-amenazante/ |

Los PDF tienen el texto de `pdftotext` al lado. Los HTML tienen un `.txt` extraído; las citas de la nevada apuntan al HTML porque el extractor se comió el cuerpo.

Conflictos, resueltos sin fijar un color vigente:

- La ficha del Santa Isabel sigue diciendo «volcán activo en estado de reposo»; el boletín semanal del 10 al 16 de noviembre de 2026 es más reciente y no se copia su color. La respuesta manda al boletín.
- La ficha del Machín trae a la vez una línea de estado y la frase de reposo. Tampoco se fija.
- Las resoluciones 259 y 268 de 2024 dicen «alerta amarilla». Sirven para el cierre y la cumbre restringida, no como color de hoy.
- La UNGRD aún imprime la escala I–IV («erupción probable en días o semanas»). Manda el esquema del SGC vigente desde septiembre de 2023.
- Techos: la UNGRD dice retirar la ceniza sin agua; la guía del SGC permite humedecer poco sin empapar. La respuesta da las dos y pide no subirse en el parque.
- Helada: el glosario de 2024 habla de 1,5 a 2 m; la nota de 2012, de 2 m. Se usa el glosario para la definición.
- El gradiente de referencia del IDEAM es 0,6 °C cada 100 m. El −5,4 °C/1000 m medido en el río Claro no pudo re-descargarse.

Vacíos (no se rellenan): meses concretos de lluvia, totales en mm, humedad relativa, gradiente del parque, frecuencia de granizo, calendario de heladas propio del parque (la nota de 2012 habla sobre todo de altiplanos), velocidad del viento, rayos fuera de una erupción en rojo, índice de boletines del Tolima y del Santa Isabel (ambas URL probadas devolvieron 404). El color de alerta no se fija. Historia eruptiva y Armero siguen en `history_culture`. Faltan 4 entradas para la meta de 60; no hay más pregunta de visitante con fuente oficial distinta.


## Updated entry: weather_volcano.alert_not_evacuation

- Reason: An alert color is not by itself an evacuation order, and it is not each volcano's own bulletin.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.alert_orange_meaning

- Reason: Cite the orange-block ash emissions and strong irritating smells.
- Changed fields: answer, hard_negatives, label, sources

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> aumenta la probabilidad de una o varias erupciones mayores

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> Se pueden generar avalanchas
> (lahares) pequeñas en los ríos que nacen en el volcán.

- https://www2.sgc.gov.co/Noticias/Paginas/Colombia-cambia-su-esquema-de-medicion-de-la-actividad-volcanica.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-cambio-esquema.txt`

> ya no existe ninguna categoría en la que se afirme que es probable que se dé una erupción en cuestión de días, semanas u horas

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> emisiones de ceniza frecuentes (erupciones menores) cuyo volumen no afecta de manera importante el diario vivir

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> olores fuertes e irritantes en zonas cercanas al volcán


## Updated entry: weather_volcano.alert_red_meaning

- Reason: Cite the red heading (volcano in eruption) and the major-eruption line.
- Changed fields: answer, hard_negatives, label, sources

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> Realizar evacuación obligatoria de zonas que pueden ser afectadas por la erupción, dependiendo del volcán y acorde con el mapa de amenaza.

- https://www2.sgc.gov.co/Noticias/Paginas/Colombia-cambia-su-esquema-de-medicion-de-la-actividad-volcanica.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-cambio-esquema.txt`

> a partir del 14 de septiembre de 2023 entrará en vigencia el esquema de estados de alerta por actividad volcánica

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> Alerta Roja
> Volcán en er​​upción

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> Erupción mayor
> (considerable) en curso


## Updated entry: weather_volcano.alert_states_nonsequential

- Reason: Date the non-sequential scheme and point the label at the jump between colors, not at yellow access.
- Changed fields: answer, examples, hard_negatives, label

- https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-transiciones.txt`

> un volcán puede pasar de estado de alerta por actividad volcánica Verde a Naranja sin haber tenido que pasar por Amarilla

- https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-transiciones.txt`

> A partir de septiembre 14 de 2023

- https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-transiciones.txt`

> este no estima la probabilidad de una erupción en término de días o semanas


## Updated entry: weather_volcano.ash_roofs

- Reason: One instruction: do not soak the roof, do not climb it, tell park staff. Both sources are quoted and are not offered as equivalent do-it-yourself steps. Round 3 (orchestrator, per re-review required_change): SGC roof/stairs precaution quoted; single instruction unchanged.
- Changed fields: answer, last_verified, sources

- http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1 (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/ungrd-comunidades-erupciones.txt`

> Retire la ceniza de los techos, sin utilizar
> agua.

- https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

> Se deben rociar con
> agua los depósitos de cenizas antes de utilizar las palas para quitarlas, cuidando
> de que no se humedezcan demasiado cuando cubren los techos, ya que eso
> aumentaría el peso de la carga y habría peligro de que colapsen los techos.

- https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

> Deben extremarse las precauciones en escaleras y techos. Las cenizas hacen el
> piso muy resbaloso, y como consecuencia muchas personas mueres al caer
> cuando están limpiando cenizas de los techos.

- https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

> Tome precaución con respecto al
> sobrepeso al subirse a una superficie de por si sobrecargada por las cenizas


## Updated entry: weather_volcano.ash_water

- Reason: Drop the poison paraphrase, cite the full UNGRD contaminated-water sentence, and keep the successful refetch.
- Changed fields: answer

- http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1 (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/ungrd-comunidades-erupciones.txt`

> Evite consumir agua de ríos o quebradas de montaña o cercanos
> al volcán, puede estar contaminada.

- http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1 (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/ungrd-comunidades-erupciones.txt`

> Aliste una reserva de agua y tape los depósitos

- https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

> Si encuentra cenizas en el agua, déjela reposar y luego use el agua limpia.

- https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

> El agua contaminada con cenizas generalmente tiene sabor
> desagradable, más que riesgo a producir daños a la salud


## Updated entry: weather_volcano.ballistic_blocks

- Reason: Ballistic blocks near the crater are not a pyroclastic flow and not a small lahar.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.current_alert

- Reason: Replace the today-alert label and restore the two observatory examples that ovsm_role does not answer.
- Changed fields: examples, hard_negatives, label


## Updated entry: weather_volcano.current_forecast

- Reason: Where to open the IDEAM forecast is not the national map's limit and not the general climate.
- Changed fields: hard_negatives, label


## Updated entry: weather_volcano.gases_dilute

- Reason: Dilution before towns does not answer which gases are emitted or whether a sulfur smell is safe.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.helada_meaning

- Reason: The 0 °C definition is not the radiation-frost schedule and not snowfall.
- Changed fields: hard_negatives, label


## Updated entry: weather_volcano.helada_night

- Reason: Radiation frost at dawn is not the meteorological definition and not snow.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.machin_bulletin

- Reason: Date the Machín bulletin list and record that the general page mixes a status line with the repose sentence.
- Changed fields: answer, hard_negatives

- https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/Boletines-Volcan-Cerro-Machin.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-machin-boletines.txt`

> Boletín semanal de actividad del volcán Cerro Machín del 10 de noviembre al 16 de noviembre de 2026

- https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/Boletines-Volcan-Cerro-Machin.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-machin-boletines.txt`

> Boletines Extraordinarios

- https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/generalidades-volcan-cerro-machin.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-machin-generalidades.txt`

> Es un volcán activo en estado de reposo

- https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/generalidades-volcan-cerro-machin.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-machin-generalidades.txt`

> cambios en el comportamiento del nivel base de los parámetros


## Updated entry: weather_volcano.national_forecast_limit

- Reason: The three-day national map is not the trail forecast and not a promise of a clear summit.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.orange_near_volcano

- Reason: Near-crater orange hazards are not the general meaning of orange alert.
- Changed fields: hard_negatives, label


## Updated entry: weather_volcano.ovsm_role

- Reason: Remove the two examples the answer does not cover; keep the SGC-or-observatory check.
- Changed fields: examples, hard_negatives


## Updated entry: weather_volcano.park_weather

- Reason: Keep general climate questions from taking the documented-snowfall and summit-visibility cards.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.pyroclastic_flows

- Reason: A pyroclastic flow on the slope is not a ballistic block thrown near the crater.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.santa_isabel_bulletin

- Reason: Stop saying the Santa Isabel page still shows repose as if that sentence were today's alert.
- Changed fields: answer, hard_negatives

- https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_de_Santa_Isabel_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-santa-isabel-boletin-2026-11-10-16.txt`

> Volcán Nevado de Santa Isabel

- https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_de_Santa_Isabel_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-santa-isabel-boletin-2026-11-10-16.txt`

> Durante la semana comprendida entre el 10 y el 16 de noviembre de 2026

- https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadodeSantaIsabel/Paginas/generalidades-volcan-nevado-santa-isabel.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-santa-isabel-generalidades.txt`

> Es un volcán activo en estado de reposo.


## Updated entry: weather_volcano.separate_volcano_alerts

- Reason: Each volcano has its own bulletin; that is not the evacuation order and not the Ruiz color of the day.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.snow_and_hail

- Reason: The October 2025 snowfall is not the general climate of the park.
- Changed fields: hard_negatives, label


## Updated entry: weather_volcano.sulfur_smell

- Reason: A sulfur smell near the volcano is not the gas list and not a green-alert definition.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.summit_visibility

- Reason: Separate a guaranteed clear summit from a cloudy visit that is still worth doing, and from snow.
- Changed fields: examples, hard_negatives, label


## Updated entry: weather_volcano.volcanic_activity

- Reason: What a bulletin measures is not today's color and not the Manizales observatory note.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.volcanic_closures

- Reason: Extend the Resolution 268 quote through the closure-and-evacuation sentence and distinguish the summit rule from alert-color closures.
- Changed fields: answer, hard_negatives, label

- https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-268-2024.txt`

> Ascenso a cumbre o cima nevada (restringido por actividad volcánica).

- https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-268-2024.txt`

> Ciclo montañismo tramo carretera Brisas – Arenales – Valle de Las Tumbas

- https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-268-2024.txt`

> en alerta amarilla: que corresponde a volcán activo con cambios en el
> comportamiento del nivel base

- https://www.parquesnacionales.gov.co/wp-content/uploads/2024/10/Res.-No.-259-del-09-de-octubre-de-2024-PFFO-022-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-259-2024.txt`

> determinación de cierre y evacuación, para lo cual deben seguir estrictamente las
> recomendaciones de los guardaparques.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-268-2024.txt`

> en cualquier momento se puede tomar la determinación
> de cierre y evacuación


## Updated entry: weather_volcano.volcanic_gases

- Reason: Which gases the Ruiz can emit is not the sulfur-smell card and not the dilution card.
- Changed fields: hard_negatives


## Updated entry: weather_volcano.yellow_upper_access

- Reason: Separate the 2023 yellow recommendation for the upper zone from the dated 2024 summit restriction and from today's access.
- Changed fields: answer, hard_negatives, label, sources

- https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-estados-alerta.txt`

> Restringir el acceso a la parte alta del volcán (depende del volcán).

- https://www2.sgc.gov.co/Noticias/Paginas/Colombia-cambia-su-esquema-de-medicion-de-la-actividad-volcanica.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/sgc-cambio-esquema.txt`

> Bogotá, 14 de septiembre de 2023. A partir de hoy, el Servicio Geológico Colombiano (SGC) cambiará el esquema

- https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/weather_volcano/evidence/raw/pnn-res-268-2024.txt`

> Ascenso a cumbre o cima nevada (restringido por actividad volcánica).
