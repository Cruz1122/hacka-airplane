# Activities

Corrección de la sección `activities` (order 8, perfil `explain`) después de la revisión de calidad. Verificación: 2026-11-21. Cada cifra de las respuestas sale de un pasaje leído ese día y guardado en `activities/evidence/`. Una URL con fecha no se usó como prueba si el pasaje no estaba en el archivo.

La sección no tiene entradas `kind: action`. No promete envío de reportes, guardado, sincronización, GPS ni rescate.

## Fuentes leídas

1. Ficha vigente, descargada el 2026-11-21.  
   https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/  
   Texto: `activities/evidence/ficha-2026-11-21.txt`. Incluye el pico y placa de noviembre de 2026, así que el HTML está actualizado al menos a 2026. No trae una fecha de publicación visible.

2. Resolución 207 del 4 de agosto de 2023. PDF de 20 páginas.  
   https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf  
   Texto: `activities/evidence/resolucion-207-2023.txt`. Reglamentación transitoria.

3. Carta del jefe del PNN Los Nevados, radicado 20266200003411, 11 de mayo de 2026.  
   https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf  
   Texto: `activities/evidence/carta-2026-05-11.txt`.

4. Noticia del 6 de marzo de 2026.  
   https://www.parquesnacionales.gov.co/sala-prensa/noticias/el-parque-nacional-natural-los-nevados-lanza-nuevo-plan-de-ordenamiento-ecoturistico-para-fortalecer-la-conservacion-en-la-alta-montana/  
   HTML: `activities/evidence/poe-2026-noticia.html`.

5. Versión corta del POE, copyright 2025, lanzada con esa noticia.  
   https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf  
   Texto: `activities/evidence/poe-2026-corto.txt`. La versión íntegra no se obtuvo.

No se citan páginas que no se abrieron. El catálogo SGC del cráter Arenas no se abrió en esta corrección: las respuestas no afirman ese nombre.

## Qué se corrigió

Se reescribieron las respuestas en 1 a 3 frases, de tú, sin «la ficha dice», «la norma que revisé» ni advertencias sobre lo que el asistente no hace. Los ejemplos declarativos («no son la laguna verde», «la ficha dice que hay que prepararse», «dulima es montaña de verdad») salieron de todas las entradas.

`activities.demanding_south` ya no dice «antes de comprometerme». Pide preparación, que es lo que escribe la ficha, y hablar con el operador antes de comprometer la cumbre.

`activities.victor_mariposa_lagoons` describe el sendero del 4 de agosto de 2023 y dice que esa lista no lo deja abierto hoy. La variante repite la fecha y la confirmación.

`activities.vehicle_or_on_foot` conserva el hecho leído: el parque no presta transporte interno, y el valle sigue en vehículo cubierto. La variante repite las dos cosas. No se dedujo la ausencia de transporte por un horario que faltara.

`activities.picnic_on_trail` dejó de existir. El ejemplo de dejar la basura no se copió. Bote, picnic, esquí de paseo y caminata nocturna quedaron en `activities.unlisted_activities`, sin llamarlos prohibidos. «Muelle» se trata como topónimo del sendero 6. El esquí de montaña solo se nombra dentro de la definición de montañismo de 2023.

La cabaña El Refugio no se declara cerrada aquí. Esa pregunta ya está en `services.refugio_cabin` y este pase no releyó el informe de 2024.

`activities.induction_talk` se eliminó: el requisito de inducción y de guía REPSE queda en `booking_fees`. La condición distinta, guías especializados en alta montaña para subir de forma progresiva a un glaciar, quedó dentro de las cumbres y los bordes de glaciar, en la respuesta corta y en la variante.

`activities.luggage_portage` se eliminó como servicio. El límite de 2023 —porteo de maletas prohibido hacia Calvito y Arenales— quedó solo en `activities.camping_tolima` y `activities.tolima_summit_schimmer`.

`activities.four_or_five_sectors` y los perfiles de visitante del POE corto se eliminaron. Los cinco sectores de manejo son propuesta de ordenamiento, no la visita. Los cuatro sectores de la ficha siguen en `activities.what_to_visit` como menú de actividades, no como inventario de límites.

`activities.paramillo_quindio_trail` y `activities.paramillo_santa_rosa_trail` se unieron en `activities.paramillo_trails_announced`. El verbo de la noticia es «se habilitarán». La variante también dice que no se tomen como abiertos.

Camping, cumbres, senderos de 2023, deportes y la prohibición del Ruiz repiten la fecha o la condición en la variante, no solo en la respuesta corta.

## Conteos

- Entradas: 49. Meta de la fila: 90. La diferencia son temas sin pasaje propio o fusionados por ser la misma respuesta.
- Ejemplos: 588, doce por entrada.
- Negativos: 3 por entrada.
- Variantes: 1 por entrada, con la salvedad material de la respuesta corta.
- `related`: 3, todos dentro de esta sección.
- Banco de aclaraciones: 7. `slot_questions.sector` cubre el filtro `sector`. `needs` vacío.
- `featured`: `what_to_visit`, `brisas_valle_tumbas`, `ruiz_summit_closed`, `camping_where`, `sector_tolima`.
- jsonschema Draft 2020-12 contra `inputs/knowledge-section.schema.json`: 0 errores, el 2026-11-21, después de regenerar solo esta sección.
- Ejemplos idénticos dentro de la sección y contra los JSON de las otras secciones en ese momento: 0.
- No se escribió `coordination/validation.json`. Otras secciones seguían en corrección.

## Mapa de semillas

Índices de `coordination/assignments.json`: 1, 7, 20, 28, 29, 33, 40.

| Índice | Etiqueta original | Entrada | Qué quedó |
|---|---|---|---|
| 1 | qué se puede visitar | `activities.what_to_visit`; Brisas en `activities.brisas_valle_tumbas` | Cuatro sectores y el valle. Se usa «visita esporádica y caminatas cortas», como la ficha. |
| 7 | si se puede subir al cráter | `activities.ruiz_summit_closed` | Prohibición de cima y cráter del Ruiz según la carta del 11 de mayo de 2026. El recorrido publicado es el valle. |
| 20 | acampar en el parque | `activities.camping_where` y las de Otún, Cisne, Brisas y Tolima | Zonas de 2023 con el conflicto interno. Ninguna se da por abierta. Carpa de tres o cuatro estaciones bajo cero y sin fogata, en corta y variante. |
| 28 | el sector Santa Isabel | `activities.sector_santa_isabel` | Borde glaciar, cumbre, Laguna Verde, El Cisne a unos 4100 m, La Cueva y Potosí. Las vías quedan en acceso. |
| 29 | el sector Nevado del Tolima | `activities.sector_tolima` | Travesía, montañismo y terreno más exigente. El Cocora como carretera no se repite. |
| 33 | la fotografía en el parque | `activities.photography_amateur` | Foto y video no comerciales. El trámite comercial queda como negativo, no como instructivo. |
| 40 | si se puede ver la cumbre | `activities.cloudy_visit_landscape` | El carreteable es un recorrido desde donde se puede observar el Ruiz. Si la cima no se ve, el plan publicado sigue siendo el valle. El pronóstico queda en clima. |

## Cifras que sí entran

Todas con `last_verified` 2026-11-21 y fuente oficial:

- 4100 metros aproximados: Brisas y El Cisne, ficha.
- 3920 metros aproximados: Potosí, ficha.
- 7,5 km al límite y 18 km a la Laguna del Otún, ficha, en la caminata desde El Cedral.
- 4 de agosto de 2023, 11 de mayo de 2026, 6 de marzo de 2026, Resolución 474 de 2018.
- 15 días hábiles de la solicitud deportiva, Resolución 207 citando la 474 de 2018, con la salvedad de que el plan corto de 2026 remite el reglamento completo a la versión íntegra.
- 26 rutas evaluadas y 15 favorables, POE corto; 15 senderos en futuro, noticia del 6 de marzo de 2026. No se presentan como senderos abiertos.
- Carpas de tres o cuatro estaciones para temperaturas menores a cero grados, Resolución 207.

No entran cupos de 2008 ni de 2023, edades, horarios, tarifas, 80 kg de carga, tamaños de grupo recomendados, 316 km de evaluación ni la cifra de visitantes de la noticia.

## Vacíos

- Duración y grado de casi todos los senderos. La única longitud de caminata leída es 7,5 km y 18 km.
- Altura del Valle de las Tumbas. No está en la ficha leída.
- Nombres de las 15 rutas favorables. El texto del PDF corto anuncia un mapa y no los escribe.
- Apertura real de los senderos de los paramillos. La noticia está en futuro.
- Si algún camping de 2023 sigue habilitado después de esa fecha. La carta de mayo de 2026 no reescribe la lista.
- Reglamento deportivo completo de 2026. La edición corta dice que hay que leer la versión íntegra.
- Nombre oficial del cráter. No se abrió el catálogo del SGC en esta corrección.
- Si existe una zona física de picnic, un bote, un esquí de paseo o una caminata nocturna. La ausencia en estos documentos no se convirtió en prohibición.

## Conflictos

1. Cuatro sectores en la ficha y cinco sectores de manejo propuestos en el POE corto. La visita usa los cuatro de la ficha. Los cinco no tienen entrada.
2. La carta del 11 de mayo de 2026 atribuye a la Resolución 207 la prohibición de cima y cráter del Ruiz. El cuerpo extraído de esa resolución describe el ascenso turístico del Tolima por Schimmer y no repite la frase del Ruiz. Se responde con la carta y se deja la diferencia en el detalle de `activities.ruiz_summit_closed`.
3. La misma Resolución 207 nombra camping en el Otún, El Cisne condicionado y Arenales de Brisas restringido, y en las prohibiciones solo habilita de forma transitoria Termales del Cañón, Arenales y Calvito. El Otún además está «en proceso de acondicionamiento». No se promete ningún camping abierto.
4. «Ingresar con vehículos» está prohibido en la Resolución 207, y la ficha autoriza vehículo cubierto en Brisas. La respuesta sigue la ficha, que es la página de visita más reciente leída.
5. El POE corto dice que el deportista de ciclomontañismo o trail running no requiere necesariamente guía, y remite el reglamento a la versión completa, que no está en el PDF. La ficha exige acompañamiento registrado para la visita. La respuesta no autoriza salir sin operador.

## Temas que salieron de esta sección

Inducción, guía REPSE general, edades, seguro, reservas y tarifas: `booking_fees`. Horarios, «¿está abierto?» y ingreso de noche: `hours_status`. Carreteras, moto y parqueo: `access`. Porteo como servicio y cabaña El Refugio: `services`. Pesca, playback, dron, basura, fuego como norma general y fotografía comercial: `rules` o `fauna`. Especies, páramo como ecosistema, agua y glaciares como sistema: `fauna` y `flora_ecosystems`. Alturas de cumbres, departamentos y cuenta de sectores: `geography`. Mal de altura y aclimatación: `health_safety`. Alerta y ceniza: `weather_volcano`.

## Hecho, inferencia y límite

- Hecho: lo citado en `activities/evidence/quotes.md`.
- Inferencia marcada en el tono, no como dato nuevo: que un nombre ausente de la lista de 2023 no es una cumbre ofertada; que «Muelle» no prueba un bote; que la noticia en futuro no abre el sendero. Esas frases piden confirmación al parque.
- No verificado como abierto en 2026: senderos y campings nombrados solo en la Resolución 207, y los dos senderos anunciados el 6 de marzo de 2026.

## Coordinator final sample corrections

Camping short/variant now lead with date-specific official authorization; the full 2023 source conflict remains in detail. Removed cross-scope gear/fire positive examples. Photography short now focuses on amateur photos and relevant commercial/production permit conditions. Removed activities.el_bosque_houses as lodging duplicated services.otun_lodging, with related links rewired. All seven assigned seeds remain. Final count: 48 entries and 576 examples.

## Round 2 (2026-11-21)

Snapshot frozen. Changes go through `activities/source/overlay.py` and `coordination/build_from_snapshot.py`. `build_section.py` and `corrected_section.py` were not run.

Counts: 48 entries / 576 examples → 70 entries / 840 examples. Removed ids: none.

### Rewritten

- `activities.combeima_cocora_traverse`. The August 2023 text still names the Juntas–Cocora traverse. Resolution 017 of 17 January 2024 closed the Juntas–Perlas–Termales stretch. The resolution of 26 December 2024 orders that same stretch reopened and again authorizes visitors and ecotourism services. The answer gives both acts and asks the visitor to confirm the later one still stands.
- `activities.asomadera_day`. Kept the 2023 day-trip limit and the fact that Muelle is a place name. Added the Caldas tourism ficha figure (about 3 hours, medium-low) and said the park page does not publish that time.
- `activities.otun_cocora_traverse`. The answer now names Laguna del Mosquito, Buenos Aires and Mojón de Cárdenas, which the 2023 trail line and the existing examples already used.
- `activities.ruiz_summit_closed`. La Olleta and La Piraña stay craters named on the park page. The 2023 permitted-trail list does not include a visit to them. The May 2026 letter still bans the Ruiz summit and crater.
- `activities.camping_where`, `activities.camping_brisas_restricted`, `activities.camping_otun`, `activities.camping_cisne`. The 2024 needs report says the Arenales camping zone is not enabled because of volcanic activity. Otún camping remains “being fitted out” in the 2023 rule; the 2024 report calls the cabin in good condition and does not declare the camp open. Cisne stays conditional.
- `activities.laguna_verde`. Added the 2024 report’s “regular condition” for that viewpoint.
- `activities.geology_watching`. Added glaciological observation from the 2023 permitted-activity list.
- `activities.unlisted_activities`. Boat and picnic stay off the 2023 list. Mountain ski stays inside sport mountaineering. A night activity is listed as a special permit in the 2024 report for Brisas and Cisne, and that report attributes the list to Resolution 207, whose activity section does not name it.
- `activities.therapeutic_baths_banned`. The same 2024 list says “baños de salud” and attributes it to Resolution 207. The resolution forbids therapeutic baths. The answer follows the resolution.
- `activities.published_trails`. Added the 2024 report’s count of 12 trails from the 2023 rule, and the sentence that routes not in that rule cannot be offered.

### Added

`activities.potosi_laguna_road`, `activities.laguna_el_mosquito`, `activities.recreation_zone_trails`, `activities.permitted_activity_menu`, `activities.paramo_walk`, `activities.interpretive_hiking`, `activities.wellness_on_trail`, `activities.environmental_education`, `activities.ski_and_canyoning`, `activities.cambio_climatico_trail`, `activities.calvito_overnight`, `activities.cocora_named_stops`, `activities.south_operation_transitory`, `activities.mirador_laguna_otun`, `activities.gazaperas_climb`, `activities.special_permit_activities`, `activities.la_cueva_start`, `activities.sietecuerales_point`, `activities.aguacerales_stop`, `activities.ruiz_glacier_edge`, `activities.cycling_roads_2017`, `activities.conejeras_hut`.

### Raw files

Fetched this round:

- https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Resolucion-No.708-Por-la-cual-se-ordena-la-apertura-del-tramo-del-sendero-Juntas-Cocora-PNN-Los-Nevados.pdf → `activities/evidence/raw/pnn_res_708_2024_reabre_juntas.pdf` and `.txt`

Reused from `activities/evidence/raw/` (already on disk; URLs recorded in `quotes.md`): park ficha, Resolution 207 of 2023, May 2026 letter, March 2026 news, short 2026 POE, Resolution 017 of 2024, 2024 needs report, 2017 management plan, Caldas “Naturaleza y páramo” ficha, 2016 Conejeras news, 2020 centre-reopening news.

`check_quotes.py`: 147 quotes, 0 failures, every entry id marked in `quotes.md`.

### Gaps (why this stops at 70, not 90)

- PNN does not publish duration or difficulty for the trails. The only timed walk found is the Caldas operator ficha for Asomadera (about 3 hours, medium-low). The 11 km Potosí–Muelle figure is the 2017–2022 POE table quoted by the 2024 report, not a 2026 measurement.
- Daily capacities in Resolution 207 still cite Resolution 252 of 2008 and a 2019 technical note. The short 2026 plan does not restate operating numbers. They were not copied forward.
- The short 2026 plan says 15 of 26 evaluated routes were favorable and does not name them.
- The 6 March 2026 news still uses the future tense for the Paramillo de Santa Rosa and Paramillo del Quindío trails.
- No downloaded act after December 2024 says whether each 2023 campsite is open, except Arenales (not enabled in the 2024 report).
- Resolution 268 of 2022 is cited by the 2023 rule as the basis of the transitional southern operation. The file `pnn_res_268_2023.txt` is a different act (20 November 2023) and was not used.
- The 2024 report’s special-activity list (night activity, rescue courses, orientation races, yoga, “baños de salud”) is attributed to Resolution 207, but that resolution’s activity section does not contain those items. They are questions, not permissions.
- Rock climbing and rappelling at Gazaperas, and the three cycling roads, are in the 2017 plan and are not repeated as current permissions.
- Bird species, lodging, porter rules, ages, hours and road distances stay in their own sections.
