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
