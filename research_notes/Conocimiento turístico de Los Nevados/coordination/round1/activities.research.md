# Activities

Investigación de la sección `activities` (order 8, perfil `explain`) para el asistente offline de visitantes del Parque Nacional Natural Los Nevados. Fecha de verificación: 2026-11-21. No se afirma ninguna página que no se haya leído.

Las citas de Parques Nacionales documentan el parque. No significan que la entidad respalde este asistente, su registro de visita, un reporte de emergencia, GPS, rescate ni sincronización. La sección no tiene entradas `kind: action`.

## Fuentes consultadas

Páginas leídas el 2026-11-21:

1. Ficha vigente, Parques Nacionales Naturales de Colombia.  
   URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/  
   Fecha de publicación: no figura en el HTML leído. El texto incluye el pico y placa de noviembre de 2026 (Resolución 1815 del 24 de julio de 2026, Secretaría de Tránsito del Tolima), así que el contenido está actualizado al menos a 2026.  
   Uso: sectores, actividades por sector, descripción de Brisas, Cisne, Otún y Quindío–Dulima, alturas aproximadas, elección de visita corta frente a travesía, fotografía no comercial, observación de aves, fauna y flora, geología, casas de El Bosque, distancias a pie hacia la Laguna del Otún.

2. Resolución 207 del 4 de agosto de 2023, «Por medio de la cual se ordena la apertura y se adopta la reglamentación del ecoturismo». PDF leído.  
   URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf  
   Publicación: Bogotá, 4 de agosto de 2023. El anexo se titula reglamentación transitoria.  
   Uso: lista de senderos, camping, cumbres, prohibiciones de actividades, porteo, guías, montañismo deportivo.

3. Carta del jefe del PNN Los Nevados, radicado 20266200003411, Manizales, 11 de mayo de 2026. PDF leído.  
   URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf  
   Uso: prohibición vigente, a esa fecha, de ascender a la cima y al cráter del Ruiz, y remisión a la Resolución 207 de 2023.

4. Noticia institucional, 6 de marzo de 2026. Página leída.  
   URL: https://www.parquesnacionales.gov.co/sala-prensa/noticias/el-parque-nacional-natural-los-nevados-lanza-nuevo-plan-de-ordenamiento-ecoturistico-para-fortalecer-la-conservacion-en-la-alta-montana/  
   Uso: anuncio de dos senderos nuevos (paramillo de Santa Rosa y paramillo del Quindío) y de 15 senderos con regulación. El verbo es prospectivo («se habilitarán», «contará»).

5. Versión corta del Plan de Ordenamiento Ecoturístico, copyright 2025, lanzada con la noticia del 6 de marzo de 2026. PDF leído en su capa de texto.  
   URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf  
   Uso: el plan dice unificar la Resolución 207 de 2023 y otras normas; inventario de 26 rutas evaluadas y 15 favorables; cinco sectores de manejo propuestos; tres perfiles de visita; ciclomontañismo y trail running como deportes con requisitos. La capa de texto no extrajo el mapa ni los nombres de esos 15 senderos. El propio PDF remite el reglamento completo a la versión íntegra, que no se recuperó.

No se abrieron, y por eso no se usan como prueba: catálogo SGC del Ruiz, boletines IDEAM, Humboldt, SiB, eBird, iNaturalist, Corpocaldas, Carder, Cortolima y gobernaciones. La regulación de actividades es de Parques Nacionales. No hacía falta una lista de especies: eso pertenece a `fauna`.

Snippets de búsqueda, no páginas leídas, y por eso descartados como cifra: portal viejo en inglés (menciona 4.400 m s. n. m. y cierre del glaciar del Ruiz), colombia.travel (menciona refugio o valle a unos 4.450 m), El Nuevo Día (6 de diciembre de 2025, 4.450 m y prohibición de bicicletas). No se copió ninguna de esas cifras.

## Evidencia y soporte por tema

Hecho, salvo que se marque como inferencia o texto editorial.

### Sectores y tipo de visita

La ficha leída dice que hay cuatro sectores ecoturísticos: Brisas–Kumanday, Cisne–Poleka Kasue, Laguna del Otún y Quindío–Dulima. Brisas conviene a una visita ocasional y caminatas cortas; los demás, a varios días, cumbres técnicas o más permanencia. El parque no presta transporte interno.

Soporta `activities.what_to_visit`, `activities.day_or_multiday`, `activities.four_or_five_sectors`, `activities.visit_profiles`, `activities.vehicle_or_on_foot`, `activities.children_visit_style`, `activities.demanding_south`.

El POE corto propone cinco sectores de manejo, «diferenciados de los sectores operativos»: Brisas Kumanday, Cisne Poleka Kasue, Otún Paramillo Santa Rosa, Quindío Dulima y Santa Isabel Murillo. Es propuesta de ordenamiento, no la lista de la ficha de visita. La respuesta al visitante deja la ficha como guía práctica y pide confirmar la puerta de entrada.

El mismo PDF nombra tres perfiles (explorador recreativo, montañista expedicionario, aventurero deportivo) y tres experiencias, sin asignar senderos en el texto extraído. `activities.visit_profiles` no inventa esa asignación.

### Brisas y Ruiz

Ficha: el trayecto sale del centro de inducción Brisas, a 4100 m aproximadamente, y sigue en vehículo por Arenales hasta el Valle del Silencio o Valle de las Tumbas. Hay superpáramo y formaciones que la ficha compara con un paisaje análogo a Marte. Actividades de ese sector: observación geológica, observación de fauna y flora, fotografía no comercial.

Resolución 207, sendero 1: «Centro de Interpretación Brisas – Aguacerales – Arenales – Valle de las tumbas». Pasadía sin pernoctar en la zona norte. Camping Arenales del sector Brisas, restringido por actividad volcánica.

Carta del 11 de mayo de 2026, punto 5: la Resolución 207 contiene «la prohibición de realizar ascenso a la cima y al cráter del Volcán Nevado del Ruíz».

Soporta `activities.brisas_valle_tumbas`, `activities.north_route_stops`, `activities.arenales_two_places`, `activities.ruiz_summit_closed`, `activities.superparamo_landscape`, `activities.short_walks_brisas`, `activities.geology_watching`, `activities.camping_brisas_restricted`, `activities.cloudy_visit_landscape`, `activities.refugio_not_the_route`.

`activities.cloudy_visit_landscape` conserva la semilla «si se puede ver la cumbre» como consecuencia de la visita: la ficha no promete el volcán despejado y el recorrido publicado sigue siendo el valle. El pronóstico y la probabilidad de verlo ya están en `weather_volcano.summit_visibility` (order 3). No se duplicaron sus ejemplos.

Inferencia, marcada en el tono de la respuesta y no como dato nuevo: si el refugio no aparece en la ficha vigente, no se envía al visitante allí. No se afirma que el edificio esté destruido o abierto.

### Santa Isabel / Cisne

Ficha: desde el sector se observan Ruiz, Santa Isabel y paramillo del Cisne. Se puede recorrer el borde glaciar, ascender a la cumbre del Santa Isabel o caminar a la Laguna Verde. Centro El Cisne a unos 4100 m. Accesos por La Cueva y Potosí, sin convertir esta sección en una ruta de carretera.

Ficha, frase separada: «Para subir progresivamente a un glaciar: tu grupo debe ser liderado solamente por guías especializados en alta montaña.»

Resolución 207: Conejeras–borde glaciar cara centro; mirador Laguna Verde; sendero Valores Objeto de Conservación; control de la cumbre del Santa Isabel el día anterior; el intérprete del patrimonio no hace cumbre a ningún glaciar.

Soporta `activities.sector_santa_isabel`, `activities.santa_isabel_summit`, `activities.conejeras_glacier_edge`, `activities.laguna_verde`, `activities.conservation_values_trail`, `activities.summit_views_cisne`, `activities.paramillo_cisne_view`, `activities.high_mountain_guide`.

Inferencia explícita: no hay una cumbre turística publicada solo del paramillo del Cisne. Es ausencia en la lista leída, no una prohibición con nombre propio.

### Laguna del Otún

Ficha: la laguna más grande del parque, entre los paramillos del Quindío y Santa Rosa; páramo y humedales con musgos y colchones de agua; casas tradicionales de la vereda El Bosque; cabaña Potosí a unos 3920 m. A pie desde el lado de Pereira: aproximadamente 7,5 km al límite y 18 km a la laguna. Esas dos cifras son de la ficha, en el apartado de acceso, y se usan aquí porque describen la caminata. El cómo llegar en carro queda para `access`.

Resolución 207, senderos 5 a 9: Asomadera, Laguna de Víctor y Laguna Mariposa; Potosí–Corraleja–Asomadera–Muelle; Alsacia y borde glaciar cara sur del Santa Isabel; Peña Bonita, azufrera, Laguna El Mosquito, El Bosque, La Pastora, El Cedral; cruce hacia el Cocora por cuchilla de Berlín, Buenos Aires y Mojón de Cárdenas. Pasadía sin pernoctar hasta la Asomadera. Camping de la Laguna del Otún «en proceso de acondicionamiento».

«Muelle» se trata como topónimo del sendero. No se infiere un embarcadero.

Soporta `activities.sector_laguna_otun`, `activities.otun_wetland_walk`, `activities.asomadera_day`, `activities.victor_mariposa_lagoons`, `activities.otun_cedral_walk`, `activities.laguna_mosquito`, `activities.azufrera_stop`, `activities.otun_cocora_traverse`, `activities.el_bosque_houses`, `activities.south_glacier_edge`, `activities.camping_otun`, `activities.boat_not_offered`.

### Tolima / Quindío–Dulima

Ficha: atractivos junto al Tolima, senderismo y travesías; transición de bosque altoandino a glaciar por subpáramo, páramo y superpáramo; terreno más exigente; actividad principal, montañismo.

Resolución 207: travesía Juntas–Cocora con Laguna del Encanto y Termales del Cañón; Los Chilcos (Anzoátegui–Palomar–Laguna Bombona–Vancouver–Termales del Cañón); Arenales–cumbre por el glaciar Schimmer. Prohibición textual de operación turística en la cara sur y en los glaciares Dulima, Ambala, Krauss, Totare, Combeima y Pijao; esas rutas quedan para clubes según la Resolución 474 de 2018. Camping transitorio en Termales del Cañón, Arenales y Calvito. Porteo de maletas solo hasta El Berlín, La Argentina o Buenos Aires, La Primavera o La Playa, y Termales del Cañón; prohibido hacia Calvito y Arenales. Carpas de tres o cuatro estaciones para temperaturas menores a 0 °C. Prohibidas las fogatas.

Soporta `activities.sector_tolima`, `activities.tolima_ecosystem_transition`, `activities.tolima_summit_schimmer`, `activities.tolima_closed_routes`, `activities.combeima_cocora_traverse`, `activities.laguna_encanto`, `activities.termales_canon`, `activities.chilcos_trail`, `activities.laguna_bombona`, `activities.camping_tolima`, `activities.luggage_portage`.

Noticia del 6 de marzo de 2026: sendero nuevo en el paramillo del Quindío y otro en el paramillo de Santa Rosa, sin distancia ni fecha de apertura. Soporta `activities.paramillo_quindio_trail`, `activities.paramillo_santa_rosa_trail`, `activities.quindio_summit_not_listed`. La ausencia de cumbre del Quindío es un vacío de la lista, no una prohibición citada.

### Actividades permitidas y no ofertadas

Resolución 207, actividades de esparcimiento: senderos permitidos, pasadía, fotografía y video no comercial, caminata en páramo, relajación. Culturales: senderismo interpretativo, observación de fauna y flora, observación geológica y glaciológica, educación ambiental.

Fotografía: aficionada permitida; comercial, con permiso; sin luces, pantallas ni telones sin permiso; «No utilizar drones» conforme a la Resolución 0543 del 27 de diciembre de 2018. La ficha repite que la fotografía comercial, los eventos, el deporte organizado y la investigación piden autorización. Esas autorizaciones ya tienen entradas en `rules` (`rules.commercial_photography`, `rules.audiovisual_permits`, `rules.event_permits`, `rules.organized_sports`, `rules.research_permissions`). Aquí se responde la foto de recuerdo (`activities.photography_amateur`, `activities.photo_places`) y se deja el trámite comercial como negativo.

Aves: la ficha las nombra en Cisne, Otún y, por inclusión de las actividades anteriores, en Quindío–Dulima. Brisas lista fauna y flora, no un producto llamado avistamiento. La norma prohíbe el playback. No se nombran especies: `fauna` es dueña de esa lista. Soporta `activities.birdwatching` y `activities.wildlife_from_trail`.

Otras prohibiciones leídas y usadas como respuesta de actividad, no como código sancionatorio: cabalgata y transporte de pasajeros en semovientes; baños terapéuticos; pesca salvo investigación; acampar fuera de los sitios; equipos de pesca que no deben ingresar. Soporta `activities.horseback_not_allowed`, `activities.no_swimming`, `activities.no_fishing`, `activities.no_camping_outside`.

POE corto, bloque de deportes: montañismo o andinismo, ciclomontañismo y trail running, con requisitos distintos a los del visitante tradicional. La norma de 2023, al citar la Resolución 474 de 2018, pide la solicitud deportiva con al menos 15 días hábiles, credencial, seguro de rescate e itinerario. El texto completo de 2026 no está en la versión corta. Soporta `activities.cycling_as_sport`, `activities.trail_running_sport`, `activities.sport_mountaineering`, `activities.ski_not_offered`.

El esquí de montaña, el barranquismo y la escalada en hielo aparecen en la definición de montañismo de 2023, no en la oferta de la ficha. No se describe técnica.

Charla de inducción: la ficha y la norma la hacen obligatoria. La hora queda para `hours_status`. Soporta `activities.induction_talk`.

`activities.picnic_on_trail` y `activities.night_hike_not_offered` registran ausencias: no hay zona de picnic ni caminata nocturna en los textos leídos. `activities.trail_duration_gap` y `activities.authorized_trail_names` dicen lo mismo sobre horas, grados y la lista de 15 nombres.

### Cifras que sí entran en respuestas

Todas con `last_verified` 2026-11-21:

- 4100 m aproximados: Brisas y El Cisne (ficha).
- 3920 m aproximados: Potosí (ficha; la resolución escribe 3.920 m s. n. m.).
- 7,5 km al límite y 18 km a la Laguna del Otún (ficha).
- 15 días hábiles de la solicitud deportiva (Resolución 207, que cita la 474 de 2018), con aviso de que el plan 2026 puede haber reescrito el trámite.
- 26 rutas evaluadas y 15 favorables (POE corto); 15 senderos anunciados en la noticia, en futuro.
- 0 °C y carpas de tres o cuatro estaciones (Resolución 207), dentro del detalle de camping.
- Años 2023 y 2026 cuando identifican la norma o el plan.

No se usaron capacidades diarias de la Resolución 252 de 2008 ni los cupos de 2023 (1.036, 2.073, 43, 25, 72, 35, 82, 70, 76). El POE 2026 no los republica en el texto leído y presentarlos como vigentes sería falso.

## Vacíos

- Distancia, duración y grado de dificultad de casi todos los senderos. La única longitud de caminata leída es 7,5 km y 18 km hacia el Otún.
- Altura del Valle de las Tumbas. No está en la ficha leída. No se usó 4.400 ni 4.450.
- Lista nominal de los 15 senderos favorables y si los dos senderos nuevos ya están abiertos. El mapa del PDF corto no salió en la capa de texto. La versión íntegra del POE no se obtuvo.
- Estado de camping después de marzo de 2026: la carta de mayo sigue citando la Resolución 207 para lugares habilitados y restricciones, pero no reescribe la lista de carpas.
- Si el refugio del Ruiz existe como edificio visitable.
- Si hay bote, picnic, esquí comercial o caminata nocturna. La ausencia en estos documentos no prueba una prohibición distinta de las que sí están escritas.
- Cumbre del Nevado del Quindío y del paramillo del Cisne: no están en la lista leída. No se redactó un «prohibido» que la norma no dice.
- Horas de entrada, tarifas, edad exacta, seguro, reserva y pronóstico: existen en otras secciones o no se repitieron para no duplicar.
- Nombre oficial «Arenas» para el cráter. La semilla lo trae desde un catálogo del SGC que no se abrió en esta tarea. Las respuestas dicen «cráter del Ruiz» y los ejemplos sí contienen la forma en que pregunta el visitante.
- Corporaciones y Humboldt: no se consultaron. No aportaban, en el alcance buscado, una tabla de senderos.

## Conflictos y resolución

1. Cuatro sectores (ficha, leída el 2026-11-21) frente a cinco sectores de manejo (POE corto, marzo de 2026). Resolución: la ficha sigue siendo la guía de visita. El plan se explica como propuesta y no como puerta nueva ya abierta. Entrada `activities.four_or_five_sectors`.

2. La Resolución 207 de 2023 es «transitoria» y el POE de marzo de 2026 dice unificarla. La carta del parque del 11 de mayo de 2026 sigue remitiendo a esa resolución para la prohibición de cima y cráter del Ruiz. Resolución: la prohibición del Ruiz se trata como vigente a mayo de 2026. El resto de la norma de 2023 se cita con la fecha y con la orden de confirmar, porque el reglamento completo de 2026 no se leyó.

3. Dentro de la misma Resolución 207, el cuerpo habilita camping en la Laguna del Otún y condiciona El Cisne, mientras el listado de prohibiciones dice que acampar está prohibido salvo Termales del Cañón, Arenales y Calvito como medida transitoria. Resolución: no se promete ningún camping como abierto. Se nombran los sitios con ese conflicto y se pide confirmación. Arenales de Brisas se mantiene como restringido por actividad volcánica, que es otra frase del mismo documento.

4. Edad. La ficha leída: mínimo 6 años en el carreteable de Brisas, centro El Cisne y Laguna del Otún por Potosí; 15 años en el resto de rutas, travesías y cumbres; máximo 69 en todo el parque. La Resolución 207, en prohibiciones: menores de 6 y mayores de 70. Esas cifras ya están en `booking_fees.age_minimum_by_attraction` y `booking_fees.maximum_entry_age`. Esta sección no las repite. Describe qué tipo de actividad es corta y cuál es cumbre, y remite el número a las condiciones de ingreso.

5. Visibilidad de la cumbre. Semilla asignada a esta sección, pero `weather_volcano.summit_visibility` (order 3) ya responde si se verá el nevado y pide el pronóstico. Gana el order menor en el empate del pronóstico. Aquí quedó el paisaje que sí se recorre cuando la cima está tapada, sin los mismos ejemplos.

6. Fotografía comercial, deporte organizado, salir del sendero y guía obligatorio ya están en `rules` o `booking_fees`. No se clonaron sus ejemplos. Esta sección responde la actividad (foto de recuerdo, ciclomontañismo como deporte regulado, nombres de senderos, guía de alta montaña para el glaciar).

7. «Ingresar con vehículos» figura entre prohibiciones de la Resolución 207, y la ficha autoriza vehículo cubierto en Brisas y prohíbe motos en el atractivo. Resolución: no se dijo que el carro esté prohibido en Brisas. Las motos y el parqueo quedan en `access`.

8. Snippets de prensa y de colombia.travel sobre 4.450 m, refugio y bicicleta prohibida no se elevaron a hecho. La bicicleta se respondió con el POE 2026: ciclomontañismo regulado, no paseo libre, y Brisas en vehículo cubierto.

## Temas descartados

- Índice 23 (extensión y creación): geografía e historia, fuera de alcance.
- Rutas en carro, kilómetros de ciudad a la entrada, moto, bus y parqueo: `access`. Se conservó solo la longitud de la caminata El Cedral–laguna.
- Tarifas, reserva, seguro, edad numérica y «¿entro sin guía?»: `booking_fees`.
- Horarios, «¿está abierto?» y cierres de septiembre o noviembre: `hours_status`.
- Mal de altura, dosis, listas de enfermedades y el texto del POE sobre soroche: `health_safety`. Las cumbres solo dicen que, si hay malestar, se avisa al guía y no se sigue.
- Alerta del día, ceniza y pronóstico: `weather_volcano`.
- Especies, frailejón, Ramsar, retroceso glaciar a 2028 y definición de páramo: `fauna` y `flora_ecosystems`.
- Alturas de cumbres, nombre Arenas como dato geográfico, departamentos y diferencia parque/volcán: `geography`.
- Drones como tema propio, mascotas, fuego como norma completa, basura, alcohol y sanciones: `rules`. La fogata se menciona solo dentro del camping, porque la norma de camping la prohíbe. El dron se nombra en una frase de la foto, porque así está escrito en el párrafo de fotografía de 2023.
- Cómo registrar la visita o reportar emergencia: `actions`. No se promete envío, guardado ni rescate.
- Investigación y recolección: `rules.research_permissions`.
- Cabalgata en el Valle del Cocora fuera del parque, Termales del Ruiz como hotel y termales de Santa Rosa: no son actividades internas leídas en la ficha.
- Técnica de cuerda, grietas, anclajes o vivac. La norma prohíbe instalar chapas; no se explica cómo escalar.
- Cupos numéricos de 2008 y 2023, por el riesgo de darlos como vigentes.
- Cada finca de la travesía (Estambul, Acaime, Aquilino, La Primavera) como entrada propia: son puntos de una misma ruta, no intenciones distintas.
- Esquí, barranquismo y escalada en hielo se agruparon en una sola entrada. Separarlos habría sido la misma ausencia repetida.

## Mapa de semillas

Índices base cero asignados: 1, 7, 20, 28, 29, 33, 40.

| Índice | Etiqueta original | Entrada final | Qué se conservó y qué cambió |
|---|---|---|---|
| 1 | qué se puede visitar | `activities.what_to_visit`; el detalle de Brisas en `activities.brisas_valle_tumbas` | Se conserva Brisas–Valle de las Tumbas y la necesidad de confirmar tramos. Se amplía a los cuatro sectores, porque la ficha ya no reduce la visita al norte. |
| 7 | si se puede subir al cráter | `activities.ruiz_summit_closed` | La semilla solo decía «usa recorridos autorizados». La carta del 11 de mayo de 2026 permite decir que la cima y el cráter del Ruiz están prohibidos. |
| 20 | acampar en el parque | `activities.camping_where` y las entradas de Otún, Cisne, Brisas y Tolima | Se conservan «zonas autorizadas» y «confirmar». Se nombran los sitios de 2023 con el conflicto interno y sin darlos por abiertos. |
| 28 | el sector Santa Isabel | `activities.sector_santa_isabel` | Se conservan Cisne–Poleka Kasue, borde glaciar, cumbre, Laguna Verde y El Cisne. Las vías desde Villamaría y Santa Rosa quedan en acceso. |
| 29 | el sector Nevado del Tolima | `activities.sector_tolima` | Se conserva Quindío–Dulima como sector de travesía y el Cocora como una puerta, sin itinerario de carretera. Se añade que la ficha lo marca como el más exigente. |
| 33 | la fotografía en el parque | `activities.photography_amateur` | Se conserva la fotografía no comercial desde puntos habilitados. El permiso comercial ya está en `rules` y queda como negativo. |
| 40 | si se puede ver la cumbre | `activities.cloudy_visit_landscape` | Se conserva que la nube puede tapar la cima y que el recorrido sigue. El pronóstico queda en clima, de menor order. |

El índice 43 («dónde queda Valle de las Tumbas») no estaba en esta asignación. El doble nombre Valle del Silencio queda dentro de `activities.brisas_valle_tumbas`, que es la visita. La localización geográfica no se reclamó.

El índice 19 (Laguna del Otún como sector) no era semilla de esta fila. La visita sí entra en «qué visitar». No se tomaron hectáreas ni el dato Ramsar.

## Conteos y validación

- Entradas: 73. Meta de la fila: 90. La diferencia son senderos sin ficha propia, no copias de la misma pregunta.
- Ejemplos: 876, doce por entrada, sin duplicados internos.
- Negativos: 2 a 4 por entrada, apuntando a acceso, tarifas, horarios, clima, fauna, flora, geografía, salud, reglas o acciones.
- Etiquetas: 3 a 8 palabras, las 73 distintas.
- `related` y `featured` resuelven dentro de esta sección. No se enlazó a otros archivos porque seguían editándose en paralelo.
- `needs` vacío. Hay `slot_questions.sector` porque `entity_filters` incluye `sector`.
- Validación con jsonschema 4.26 contra el schema adjunto (Draft 2020-12): 0 errores, el 2026-11-21, después de regenerar el JSON.
- Cruce de ejemplos idénticos contra las secciones ya escritas en ese momento: 0 choques, tras corregir tres frases que coincidían con `services` y `geography`.
- No se ejecutó el validador global del repositorio ni un modelo de embeddings. La similitud casi duplicada entre secciones queda para el coordinador.

## Hechos, inferencias, texto editorial y límites

- Hecho: lo que la ficha, la Resolución 207, la carta de mayo de 2026, la noticia o el POE corto dicen de forma explícita, citado arriba.
- Inferencia: que un nombre ausente de la lista leída no es una cumbre ofertada; que «Muelle» no prueba un bote; que el refugio no es el destino publicado. Esas inferencias están escritas como ausencia de oferta, no como dato físico nuevo.
- Texto editorial: la reflexión de algunas entradas (disfrutar el tramo visible, avisar al guía, no dejar huella al fotografiar). No agrega cifras ni permisos.
- Vacío no disfrazado de verificación: duraciones, dificultad, altura del valle, lista de los 15 senderos, apertura real de los senderos nuevos, camping posterior a 2026 y el PDF completo del POE.
- El asistente no reserva casas, no reemplaza la charla de inducción, no da el horario del sector y no transmite emergencias. Esas frases son límite del producto, no una función ofrecida.
