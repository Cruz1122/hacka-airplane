# Geografía

Corrección del 2026-11-21, después de la revisión de calidad. Perfil `explain`, order 13. El texto de `answer` es redacción para el visitante. Las cifras salen de pasajes leídos ese día y guardados en `geography/evidence/quotations-2026-11-21.md`. No se volvió a ejecutar `geography/build_section.py`.

## Fuentes leídas en esta corrección

| Fuente | URL | Fecha de la fuente | Leído el |
|---|---|---|---|
| Ficha PNN Los Nevados | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | HTML `article:modified_time` 2026-10-31T00:11:49+00:00 | 2026-11-21 |
| SGC, hoja informativa del Ruiz | https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf | Septiembre de 2024 | 2026-11-21 |
| SGC, diez volcanes más altos | https://www2.sgc.gov.co/Noticias/Paginas/Los-10-volcanes-mas-altos-de-Colombia.aspx | 2024-08-09 | 2026-11-21 |
| SGC, morfología del cráter Arenas | https://www2.sgc.gov.co/Noticias/Paginas/El-Nuevo-Domo-de-Lava-del-Volcan-Nevado-del-Ruiz-y-la-Geomorfologia-Actual-del-Crater-Arenas-2020.aspx | 2020-01-31 | 2026-11-21 |
| SGC, boletín del segmento volcánico norte | https://www2.sgc.gov.co/Publicaciones/Informes%20tcnicos/Informe_de_actividad_volcanica_segmento_norte_2023.pdf | Actividad de 2023, documento de 2024 | 2026-11-21 |
| Ideam, glaciar del Ruiz | https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-ruiz | Sin fecha de publicación visible. Tablas hasta 2024 | 2026-11-21 |
| Ideam, glaciar de Santa Isabel | https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-santa-isabel | Sin fecha de publicación visible. Tablas hasta 2024 | 2026-11-21 |
| Ideam, glaciar del Tolima | https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-tolima | Sin fecha de publicación visible. Tablas hasta 2024 | 2026-11-21 |
| Ramsar CO1781 | https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf | Ficha llenada el 2006-07-17 | 2026-11-21 |
| Carder | https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/ | Pereira, 2026-07-14 | 2026-11-21 |
| Gobernación del Tolima, Anzoátegui | https://tolima.gov.co/tolima/informacion-general/turismo/1996-municipio-de-anzoategui | Sin fecha visible | 2026-11-21 |

No se reabrió el POE de marzo de 2026. La quinta pieza de sector y la frase que ponía paramillos sobre 5.000 m salieron de las respuestas.

## Qué se corrigió

- Los 50 temas quedaron. Se reescribieron ejemplos, respuestas cortas y variantes. Se quitaron las reflexiones de contraste, entre ellas la del valle nublado y la del río que “explica de quién es el agua”.
- `geography.geoheritage` responde solo el reconocimiento IUGS, desde 2022, como uno de 100 sitios. El Patrimonio Natural de la Nación de 2025, cuyo sujeto en la ficha es el Nevado del Ruiz, quedó en `detail`.
- `geography.watersheds` nombra las dos hoyas y unos ríos. La lista más larga y la fuente de cada río están en `steps` y `detail`.
- `geography.park_area` usa 61.388,24 ha del encabezado. 61.410 ha del relato de 1974 y 61.410,53 ha de la Carder están en `detail`.
- `geography.santa_isabel_height` da las tres cumbres del Ideam, con el método, y la cifra única de 4.965 m del ranking del 2024-08-09.
- Se sacaron de las respuestas el área glaciar en km², el 1,82 % de la ficha, la proyección de 2028 y la extinción de Conejeras (diciembre de 2023 a febrero de 2024). Ese retroceso queda en flora. El Ideam sí lo dice; no se copia aquí.
- No se copian colores de alerta. La hoja y el boletín no fijan la alerta del 2026-11-21.
- No se usa el domo de enero de 2020, el centroide Ramsar escrito con longitud este, ni la coordenada ilegible del Paramillo del Quindío.

## Vacíos

- Hectárea única. Siguen publicadas 61.388,24 ha, 61.410 ha y 61.410,53 ha.
- Municipio 11. La Carder lo cuenta y no lo nombra.
- Altura única de Santa Isabel y del Cisne. Ver conflictos.
- Tamaño vigente del cráter Arenas. Hay dos descripciones fechadas.
- Altura de La Olleta, La Piraña y Nereidas. No está en las páginas leídas.
- Área del espejo de la Laguna del Otún, separada del complejo Ramsar de 2006.
- Cota actual del nacimiento del Otún. Solo está la de 4.000 m en la ficha de 2006.
- Altitud de un espejo llamado Laguna Verde, y si es el mismo punto que el relicto de hielo.
- Si la Laguna del Encanto cae dentro del polígono.
- Si Cerro Bravo, Cerro España o Cerro Machín están dentro del parque. El boletín los monitorea; la ficha no los nombra entre las cumbres.
- Fecha de publicación de las tres páginas del Ideam y de la ficha de Anzoátegui.
- Porcentajes del parque en Caldas, Quindío y Tolima. Solo está el 35,6 % de Pereira y Santa Rosa de Cabal.
- Alerta volcánica vigente. No se consultó un boletín posterior a septiembre de 2024 para declararla.
- Hoya del Campoalegre, del Quindío y del Combeima. La Carder los nombra y no dice si caen al Cauca o al Magdalena. No se asignaron.
- Hoya del Totare. En la tabla del Ideam la subzona Totare tiene vacía la celda de zona hidrográfica. No se puso en el Magdalena.

## Conflictos

- Extensión. Encabezado de la ficha: 61.388,24 ha. Relato de 1974 en la misma ficha: 61.410 ha. Carder, 2026-07-14: 61.410,53 ha. La respuesta usa el encabezado y no promedia.
- Santa Isabel. Ideam: 4.935 m, 4.923 m y 4.903 m, con SRTM 12,5 del IGAC y GPS Topcon. SGC, 2024-08-09: 4.965 m, una sola cifra. Se publican las dos formas de medir.
- Cisne. Ranking del 2024-08-09: 4.700 m. Boletín de la actividad de 2023: altura máxima 4.600 m. La respuesta da las dos.
- Santa Rosa. Ranking: 4.600 m. Boletín: 4.602 m. La respuesta da las dos.
- Cráter Arenas. Nota del 2020-01-31: unos 980 por 900 m y cerca de 300 m de profundidad. Boletín de 2023: 800 m de diámetro máximo y 200 m de profundidad. Ninguna se presenta como el contorno de hoy.
- Ruiz a 5.321 m. Hoja de 2024, ranking de 2024, boletín de 2023, nota de 2020 e Ideam coinciden. No se usa otra cota.
- Quindío a 4.700 m. Ranking y boletín coinciden.
- Laguna Verde. La ficha describe un sendero. El Ideam nombra un glaciar aún existente. No se identifican.
- Nombre Kumanday. La ficha lo publica. La etimología queda en historia.
- “Activo”. La hoja llama cráter activo a Arenas y describe Olleta, Piraña y Nereidas como no activos. Eso no es el color de alerta de esta semana.

## Temas que no se responden aquí

- Creación del parque, etimologías y Armero. Historia.
- Retroceso glaciar, km² de hielo y extinción de Conejeras. Flora y ecosistemas. La frase del Ideam sobre Conejeras se leyó y no se copió.
- Vías, kilómetros de camino y tiempos. Acceso.
- Horarios, tarifas, guía y seguro. Otras secciones.
- Qué tramo de cumbre está autorizado. La respuesta solo remite al parque cuando el lugar es un cráter o un valle cuyo estado cambia.
- Alerta, ceniza y significado de los colores. Clima y volcán. El boletín de 2023 pinta colores de ese año; no entran en la respuesta.

## Mapa de la semilla

Índices en base cero, tomados de `coordination/assignments.json`.

| Índice | Tema de la semilla | Entrada |
|---|---|---|
| 11 | los nevados del parque | `geography.main_peaks` |
| 13 | qué es el Nevado del Ruiz | `geography.ruiz_identity` |
| 14 | la altura del Ruiz | `geography.ruiz_height` |
| 19 | la Laguna del Otún | `geography.laguna_otun` |
| 22 | los departamentos | `geography.departments` |
| 23 | la extensión | `geography.park_area` |
| 34 | el nombre del cráter | `geography.arenas_crater` |
| 36 | los cuatro sectores | `geography.four_sectors` |
| 39 | diferencia parque y volcán | `geography.park_versus_volcano` |
| 43 | Valle de las Tumbas | `geography.valle_tumbas` |

La fecha de creación que venía mezclada en la semilla 23 no se responde aquí.

## Conteos y validación

- Meta del encargo: 70. Entregadas: 50. Ejemplos: 600, 12 por entrada.
- El faltante no se rellenó. Partir municipios o ríos que ya tienen entrada habría repetido la misma pregunta.
- `hard_negatives`: 3 por entrada, copiados de ejemplos de otra entrada de esta sección.
- `related` y `featured` resuelven dentro de `geography`.
- `retrieval.profile`: `explain`. `entity_filters`: `landform`, `sector`, con `slot_questions`. Ninguna entrada usa `needs`.
- `featured`: `geography.main_peaks`, `geography.ruiz_height`, `geography.park_versus_volcano`, `geography.laguna_otun`, `geography.four_sectors`.
- Validación el 2026-11-21 con `jsonschema` contra `research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json`: 0 errores. Reglas locales de la sección: 0 errores. No se reescribió `coordination/validation.json`, porque ese informe cubre las otras secciones.
- Generador de esta corrección: `geography/write_corrected_section.py`.
- No se instalaron dependencias, no se tocó código de la aplicación y no se modificaron otras secciones.

## Coordinator final sample

Five corrected entries were checked against the dated quoted passages. Twelve remaining author-like example fragments in that sample were converted into visitor questions without adding factual claims. Final count remains 50 entries and 600 examples.

## Round 2 (2026-11-21): auditoría con citas y ampliación a 63

Sección de snapshot. Todo cambio entra por `geography/source/overlay.py`, aplicado con `python3 coordination/build_from_snapshot.py geography`, luego `coordinator_fixes.py` y `validate_knowledge.py`. `geography.v1.json` no se tocó.

### Conteos

- Entradas: 50 → 63. Meta 70: faltan 7. Las siete candidatas solapaban otra sección y se descartaron (ver abajo).
- Ejemplos: 600 → 756 (12 por entrada).
- `hard_negatives`: 3 por entrada, copiados literalmente de otras entradas. Ninguno pregunta la cuestión de su propia entrada.
- Validador: `Errors: 0`. Las dos banderas que quedan son de `hours_status` y `booking_fees`, fuera de esta sección. Geografía sin advertencias.
- `geography/check_quotes.py`: 153 citas, 63 entradas, 0 sin cita, 0 cifras sin respaldo en las citas de su propia entrada, 0 fallos.

### Auditoría de las 50 entradas originales

Todas tienen al menos una cita en `geography/evidence/quotes.md`. Se corrigieron estas frases:

| Id | Cambio | Motivo |
|---|---|---|
| `sector_brisas_kumanday` | Quitado "junto al Nevado del Ruiz"; el nombre Kumanday es el Ruiz | La ficha no dice que Brisas esté junto al Ruiz |
| `valle_tumbas` | "sector norte" → "zona norte del parque"; quitado "cerca del Ruiz" | La ficha dice zona norte; "cerca del Ruiz" no está en la fuente |
| `sector_quindio_dulima` | Quitado "separado de los otros tres" | Afirmación sin fuente |
| `laguna_otun_formation` | Quitado "Es permanente"; "2026" → "actual" | Ramsar no dice que sea permanente |
| `laguna_encanto` | Respuesta corta de 340 a 315 caracteres; detalle reescrito | El predio privado de El Corazón y Bomboná sí aparece en la página de la Gobernación, pero esa página no dice si las lagunas entran al polígono. El detalle anterior podía leerse como si el predio decidiera el tema |
| `municipalities` | "Son esos diez, no más." → la CARDER cuenta 11 y no nombra el undécimo; el detalle nombra a Villahermosa de la descripción PNN anterior | Conflicto de fuentes documentado; la ficha vigente lista diez |
| `tolima_municipalities` | "seis" → "seis de los diez de la ficha vigente"; la división por departamento viene de la descripción PNN anterior (fuente secundaria declarada) | La ficha vigente no separa por departamento |
| `ibague_highlands` | Quitado "corresponde a la parte alta del municipio" | Afirmación sin fuente |
| `santa_isabel_height` | Quitada la fecha de lectura del detalle | Fecha de acceso no es fecha de la fuente |
| `ruiz_age` | "66.000" → "66 mil años" | Así lo escribe el SGC |

Ejemplos reasignados, porque preguntaban por una entrada nueva: `laguna_encanto` (2), `watersheds` (2), `olleta_pirana` (2), `paramillo_cisne` (2), `volcanic_centers` (1), `summit_line` (1).

No se eliminó ninguna entrada original. Las cifras en conflicto siguen con sus dos fuentes: Santa Isabel (Ideam 4.935/4.923/4.903 m frente a SGC 4.965 m), Cisne (4.700 frente a 4.600 m), Santa Rosa (4.600 frente a 4.602 m), cráter Arenas (2020 frente a 2023) y área del parque.

### Entradas nuevas (13)

- Ríos y cuencas: `rio_totare`, `rio_coello`, `rio_azufrado`, `rio_guali`, `rios_lagunilla_recio`, `rio_campoalegre`, `rios_quindio_combeima`.
- Lagunas nombradas por la Gobernación del Tolima: `laguna_corazon`, `laguna_bombona`, `laguna_mellizas`. La página no dice si están dentro del polígono.
- Cumbres y volcanes: `morro_negro` (4.700 m en el ranking del SGC de 2024 y 4.600 m de altura máxima en el boletín de 2023, ambas cifras en la respuesta), `nereidas` (no activo; sin altura publicada).
- Cerros monitoreados: `cerros_monitored` (Bravo, España, Machín). El SGC los vigila; la ficha del parque no los nombra entre cumbres.

### Descartadas por solapamiento (no se rellenan)

| Id candidato | Sección que ya responde | Motivo |
|---|---|---|
| `ramsar_humedales_menores` | `flora_ecosystems` | Preguntas casi idénticas sobre humedales del Otún (`otun_wetland_group_names`, `otun_main_wetland`) |
| `ramsar_subcomplejos` | `flora_ecosystems` | Mismo caso: `otun_wetland_group_names` |
| `glaciares_tolima` | `flora_ecosystems` | Glaciares son de flora (`glaciers_snow_presence`, `tolima_glacier_measured_2024`) |
| `hot_springs_ruiz` | `access` | `termales_ruiz_not_gate` y `la_enea_alternate` tratan los termales del Ruiz |
| `anzoategui_municipio` | `access` | `gateway_towns` y `from_anzoategui_palomar` responden la puerta de entrada |
| `casabianca_herveo` | `access` | `no_published_gate_towns` hace la misma pregunta sobre si quedan dentro |
| `santa_isabel_municipio` | `access` | `santa_isabel_town_vs_sector` hace la misma pregunta |

Solapamientos aceptados, porque la pregunta es otra: `rio_azufrado`, `rio_guali` y `rios_lagunilla_recio` con los lahares de `history_culture` (esas responden la tragedia, no la ubicación); `rio_campoalegre` con `ucumari_buffer` (esa responde la zona amortiguadora, no el nacimiento).

### Fuentes descargadas (`geography/evidence/raw/`, 2026-11-21)

- PNN ficha Los Nevados: `pnn_ficha_nevados.html` y `.txt`. https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/
- SGC hoja del Ruiz, sep. 2024: `sgc_hoja_ruiz_2024.pdf` y `.txt`. https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf
- SGC 10 volcanes más altos, 9/8/2024: `sgc_10_volcanes_mas_altos_2024.html` y `.txt`.
- SGC cráter Arenas, 31/1/2020: `sgc_crater_arenas_2020.html` y `.txt`.
- SGC boletín segmento norte (actividad 2023): `sgc_boletin_segmento_norte_2023.pdf` y `.txt`.
- IDEAM glaciares Ruiz, Santa Isabel, Tolima: `ideam_glaciar_ruiz`, `ideam_glaciar_santa_isabel`, `ideam_glaciar_tolima` (`.html` y `.txt`).
- Ramsar CO1781: `ramsar_co1781.pdf` y `.txt`. https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf
- CARDER, 14/7/2026: `carder_pnn_nevados_2026.html` y `.txt`.
- Gobernación del Tolima, Anzoátegui: `gobtolima_anzoategui.html` y `.txt`.
- PNN descripción, portal antiguo (fuente secundaria, no vigente): `pnn_descripcion_los_nevados_2017.pdf` y `.txt`. https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2017/12/Descripcion-PNN-Los-Nevados.pdf
- IGAC noticia Catastro Verde, 8/8/2025: `igac_catastro_verde_pnn.html` y `.txt`. No trae cifras de Los Nevados.

Los `.txt` de HTML salen de `evidence/html_to_text.py`. Las citas se verifican contra esos `.txt`.

### Brechas (sin fuente oficial que cierre el punto)

1. Área oficial única. Hay 61.388,24 ha (ficha 2026, encabezado), 61.410 ha (ficha 2026, historia), 61.410,53 ha (CARDER 2026) y 61.420 ha (PNN, portal antiguo). La respuesta usa 61.388,24 y no promedia.
2. Municipios. La ficha vigente lista diez. La CARDER cuenta 11 sin nombrar el undécimo. La descripción PNN anterior nombra a Villahermosa en Tolima, que la ficha vigente no lista. No se resolvió.
3. IGAC. La búsqueda no trajo una ficha IGAC de Los Nevados, y la noticia del Catastro Verde no la trae. Los fragmentos de búsqueda con 61.376,22 ha, 58.300 ha y el municipio Villahermosa no son fuente leída y no se usaron.
4. Alturas de La Olleta, La Piraña y Nereidas: no publicadas en las fuentes leídas.
5. Predio y polígono de Corazón, Bomboná y Mellizas: no confirmados.
6. Laguna Verde (sendero del Cisne) y el "glaciar Laguna Verde" del Ideam: no se identifica si son el mismo punto.
7. Cerros Bravo, España y Machín: no se confirma si entran al polígono.
8. Espejo de agua de la Laguna del Otún y cota actual del nacimiento del Otún: no publicados.
9. Alerta volcánica vigente: no se estableció; las respuestas remiten al SGC.
10. Cráter Arenas: dos medidas fechadas (2020: 980 × 900 m y 300 m; boletín 2023: 800 m y 200 m). Ninguna se presenta como tamaño actual.
11. Faltan 7 entradas para la meta de 70. Las candidatas eran de flora o access; no se rellenó.

## Coordinator final pass (2026-11-21)

- `geography.sector_laguna_otun` merged into `geography.laguna_otun` (near-duplicate review, pair "dónde queda el sector" / "dónde queda la laguna"). The kept short now carries the paramillos del Quindío y Santa Rosa and the note that the Potosí cabin altitude is not the lake's; quotes retagged in `evidence/quotes.md`.
- The quote that backed `geography.glacier_summits` (merged earlier into `flora_ecosystems.glaciers_snow_presence`) is kept as a provenance note.
- Entries: 62 → 61.


## Updated entry: geography.four_sectors

- Reason: Aclarar los 4 sectores ecoturísticos globales frente a sectores individuales y senderos.
- Changed fields: examples, hard_negatives


## Updated entry: geography.manizales_outside

- Reason: Aclarar que la ciudad de Manizales no está dentro del parque, separando de ruta desde Manizales.
- Changed fields: examples, hard_negatives, label


## Updated entry: geography.paramillo_santa_rosa

- Reason: Diferenciar cota del Paramillo de Santa Rosa del municipio homónimo y de Santa Isabel.
- Changed fields: examples


## Updated entry: geography.rio_otun

- Reason: Delimitar nacimiento fluvial geográfico frente a abastecimiento de acueducto.
- Changed fields: examples


## Updated entry: geography.ruiz_versus_huila

- Reason: Enfocar comparación explícita de cotas entre ambos volcanes colombianos.
- Changed fields: examples, hard_negatives, label


## Updated entry: geography.sector_cisne_poleka

- Reason: Delimitar sector geográfico frente a accesos y avistamiento faunístico.
- Changed fields: examples


## Updated entry: geography.park_area

- Reason: Añadir fecha de consulta de la ficha PNN (22-11-2026) a las cifras de 61.388,24 y 61.410 ha, conservando Carder al 14-07-2026.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/pnn_ficha_nevados.txt`

> Extensión total
> 61.388,24 ha

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/pnn_ficha_nevados.txt`

> área geográfica de 61.410 hectáreas distribuidas en diez municipios: Santa Rosa de Cabal, Pereira,

- https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/carder_pnn_nevados_2026.txt`

> de 1974, y cuenta con una extensión de 61.410,53 hectáreas distribuidas entre los departamentos de

- https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/carder_pnn_nevados_2026.txt`

> Pereira, 14 de julio de 2026.


## Updated entry: geography.andes_occidentales_office

- Reason: Sustentar la pertenencia a la región Andes Occidentales, la ubicación en la cordillera Central y la distribución en cuatro departamentos exclusivamente con la ficha oficial vigente de Parques Nacionales, retirando el documento de 2019.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/access/pnn-nevados-portal.txt`

> Región
> Andes Occidentales

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/access/pnn-nevados-portal.txt`

> Distribución en departamentos
> Caldas, Quindío, Risaralda, Tolima

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/access/pnn-nevados-portal.txt`

> Se ubica en la cordillera Central entre dos ríos principales del país —Magdalena y Cauca—


## Additive entry: geography.uton_aguacerales_station

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La caída de agua que observamos y escuchamos no para, de allí el nombre de Aguacerales.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Este fenómeno de condensación se da durante las 24 horas del día, todos los días del año, durante las noches frías, los hilos de agua se congelan y forman carámbanos (habitualmente ocurre en temporada seca).

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> 4.160 msnm aproximadamente.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Flanco occidental edificio volcánico, a 5.2 Km aproximadamente del Cráter Arenas.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Paramo propiamente dicho.


## Additive entry: geography.uton_arenales_dunes

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> se estima que estas dunas deben de tener alrededor de unos 200 o 400 años aproximadamente puesto que se forman posterior al retroceso glaciar

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> si son pisadas, la huellas pueden perdurar meses

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> 4.290 msnm aproximadamente.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Transición Paramo a Superparamo.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las dunas, están sobre Andesitas (lavas del viejo Ruiz/ older Ruiz) que tienen una edad aproximada de 100 mil años


## Additive entry: geography.uton_lunares_station

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Lunares Altura 4.350 msnm aproximadamente. Ubicación Flanco occidental edificio volcánico, a 4.8 Km aproximadamente del Cráter Arenas Ecosistema o Bioma Superáramo

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Ofrece un paisaje único y desértico que evoca la superficie de otros planetas. Sus características geológicas, producto de la erosión glaciar y la meteorización, han esculpido rocas de tonalidades rojizas y fracturas profundas. La escasez de vegetación, salvo por especies resistentes como la loricaria, resalta la dureza de las condiciones ambientales.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Los visitantes pueden observar de cerca los procesos geológicos que han dado forma al paisaje, como las grietas producidas por el congelamiento y descongelamiento del agua en las rocas

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Meteorización (gelifracción y oxidación)

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Si pudiésemos viajar en el tiempo, unos 100 años atrás en esta estación no habría vegetación, y si pudiéramos ir en el futuro en unos 100 años seguramente esta estación tendría mucha más vegetación

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Nodo 3: Valle Lunar (4.350 msnm)

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> un laboratorio natural para estudiar los efectos del cambio climático


## Additive entry: geography.uton_gelifraccion

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> este proceso es conocido como gelifracción que es un tipo de meteorización, ocurre cuando el agua se congela, el agua tiene la propiedad de aumentar su volumen al congelarse, si el agua esta confinada a los poros o grietas previas de la roca, al congelarse va a someter a un desgaste o fracturamiento por el aumento en su volumen, por esta razón las rocas están llenas de grietas.

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> El agua se filtra en las grietas de la roca, se congela por la noche aumentando su volumen y las estalla desde adentro actúa como una cuña que rompe las rocas andesíticas en pedazos angulares.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Estas fracturas contribuyen a la formación de suelo arenoso y la llegada de vegetación pionera.


## Additive entry: geography.uton_red_rocks_oxidation

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> el color rojizo obedece a otro tipo de meteorización, esta es de origen químico, acontece que las rocas están formadas por minerales, y a su vez lo minerales están formados por elementos químicos, algunos de estos elementos son susceptibles a reaccionar con el oxígeno, en este caso la oxidación del hierro (almacenado en minerales como las Hornblendas) deja en evidencia tonalidades rojizas sobre la roca.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Meteorización (gelifracción y oxidación)

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Los tonos rojizos que observan son el resultado de la oxidación de minerales ferrosos es oxidación de hierro y azufre presentes en la lava vieja al entrar en contacto con el oxígeno y la humedad ambiental.


## Additive entry: geography.uton_glacial_striae

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> También es común ver las rocas con marcas en superficies que parecen “arañazos” , esto estas son llamada estrías glaciares y son el resultado del movimiento del mismo, su acción abrasiva sobre la roca deja como evidencia estas marcas que sirven como herramienta para determinar la dirección del movimiento del glaciar.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Dunas, flujos granulares, depósitos eólicos y lavas, till, estrías, lavas con relieve invertido.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Pequeños abanicos, lavas superpuestas, estrías, lavas con relieve invertido, circo glaciar.


## Additive entry: geography.uton_glacial_landforms

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Un valle en U es una formación geológica caracterizada por lados altos y empinados y un fondo de valle redondeado o plano. Estos valles son el resultado de la erosión glacial, que transforma valles preexistentes en forma de V en valles más anchos y profundos con forma de U.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Un circo glacial es una depresión en forma de anfiteatro producida por la erosión glaciar en las paredes montañosas o en el nacimiento de los valles. Es la zona de acumulación del glaciar donde la masa de nieve comprimida se mueve por deslizamiento, formando una concavidad rocosa

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Una morrena es una acumulación de sedimentos transportados por un glaciar, que puede incluir bloques, cantos y arena. Existen varios tipos de morrenas según su ubicación en relación con el glaciar: • Morrena de fondo: Se sitúa bajo el hielo, en contacto con el lecho. • Morrena lateral: Los derrubios se sitúan en los laterales del lecho glacial. • Morrena central: Formada por la unión de morrenas laterales en la confluencia de dos glaciares. • Morrena frontal o terminal: Depósitos de derrubios en la zona de deshielo del glaciar.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Pequeños abanicos, lavas superpuestas, estrías, lavas con relieve invertido, circo glaciar.


## Additive entry: geography.uton_andesite_minerals

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Las rocas predominantes son andesitas, típicas de volcanes de zona de subducción como el nuestro

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las andesitas del Ruiz dejan en evidencia dos minerales fáciles de identificar, los claros/incoloros son plagioclasas y los negros son Hornblendas, el resto de minerales es difícil de apreciar en muestra de mano, hay que usar microscopio.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las dunas, están sobre Andesitas (lavas del viejo Ruiz/ older Ruiz) que tienen una edad aproximada de 100 mil años

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las Andesitas que se encuentran en el Valle de las Tumbas son principalmente del volcán Nereidas.


## Additive entry: geography.uton_valle_tumbas_station

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Valle de las tumbas Altura 4.460 msnm aproximadamente. Ubicación Flanco occidental edificio volcánico, a 4.1 Km aproximadamente del Cráter Arenas, a un costado del Cañón del rio Molinos. Ecosistema o Bioma Superparamo con transición a zona nival Fauna Característica: Cóndor, águila (Zona de paso). Pantas Características Algunas especies de pastos colonizadores y musgo. (Líquenes)

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Pequeños abanicos, lavas superpuestas, estrías, lavas con relieve invertido, circo glaciar.

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Importancia: Es el cierre del recorrido.


## Additive entry: geography.uton_ruiz_four_structures

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> es un complejo volcánico compuesto por cuatro estructuras (Nereidas, Olleta, Piraña y Arenas), aunque comúnmente se le conoce como Nevado del Ruiz al edificio que alberga el cráter Arenas.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La Olleta: Volcán que comenzó su formación hace 107,000 años

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Piraña y Nereidas: Surgieron nuevos volcanes como Piraña y Nereidas, y continuó la construcción del Volcán La Olleta.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Este período comenzó hace aproximadamente 66 ka con la construcción del volcán actual.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Nereidas: Situado 2 km al suroeste del VNR, con una altitud de 5000 msnm aprox,

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Nereidas no tiene cráter visible como si lo tiene La olleta.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Piraña: Ubicado a 3.8 km al este del Arenas Crater

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Geología base: El Complejo Volcánico Nevado del Ruiz (CVNR) está compuesto por cuatro estructuras: Nereidas, Olleta, Piraña y Arenas.


## Additive entry: geography.uton_arenas_crater_size

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El NRV es un volcán compuesto activo que alcanza un máximo de 5321 msnm y está coronado por el Cráter Arenas (aproximadamente 750 m de diámetro y 200 m de profundidad).

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Actualmente tiene una cubierta glaciar de 9,3 km2” (CEBALLOS–HERNÁNDEZ et al., 2020)

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> entre los departamentos de Caldas y Tolima, y aproximadamente a 140 km al NO de Bogotá, capital de Colombia, y 28 km al SE de Manizales


## Additive entry: geography.uton_park_water_supply

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El Parque Nacional Natural Los Nevados tiene cerca de 62.000 (62.142) hectáreas de las cuales protege aproximadamente 53,532 hectáreas de páramos, lo que corresponde al 86% del área protegida, abastece de agua a 37 municipios y beneficia a cerca de 3 millones de personas en la región del eje cafetero

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El agua del parque abastece a 37 municipios de la región cafetera, beneficiando a cerca de 3 millones de personas en los departamentos de Tolima, Risaralda, Caldas, Quindío y norte del Valle del Cauca.


## Updated entry: geography.uton_lunares_station

- Reason: Hackathon slide questions (Reto de IA, slides 5-22) routed to the wrong entry.
- Changed fields: examples


## Updated entry: geography.uton_arenales_dunes

- Reason: Hackathon slide questions (Reto de IA, slides 5-22) routed to the wrong entry.
- Changed fields: examples


## Additive entry: geography.uton_lunares_fracture_color

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Meteorización (gelifracción y oxidación)

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> el agua tiene la propiedad de aumentar su volumen al congelarse, si el agua esta confinada a los poros o grietas previas de la roca, al congelarse va a someter a un desgaste o fracturamiento por el aumento en su volumen

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> el color rojizo obedece a otro tipo de meteorización, esta es de origen químico

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> la oxidación del hierro (almacenado en minerales como las Hornblendas) deja en evidencia tonalidades rojizas sobre la roca

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Concepto clave: Gelifracción y oxidación.
