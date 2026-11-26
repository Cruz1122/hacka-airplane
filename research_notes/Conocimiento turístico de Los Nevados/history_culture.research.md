# Historia y cultura de Los Nevados

Corrección del 2026-11-21 después de la revisión de coordinación. Perfil `explain`, orden 14, título «Historia y cultura». No se delegó nada. No se volvió a correr `build_section.py`: ese archivo ahora se detiene para no reescribir la sección con el texto anterior.

Las citas literales y el mapa de entradas están en `history_culture/evidence/citas-2026-11-21.md`. Una URL de la ronda anterior no se vuelve a citar si el cuerpo no se releyó.

## Qué se corrigió

- Las respuestas de muestra dejaron de comparar fuentes en tres o cuatro frases. El visitante recibe el hecho y, si las cifras oficiales no coinciden, una frase que lo dice. El detalle y este log guardan las citas.
- Se reescribieron los ejemplos que sonaban a nota de investigación. Cada entrada tiene al menos doce preguntas reales, una o dos en inglés, coloquial colombiano y alguna sin tildes.
- Se eliminó `history_culture.iugs_listing`. El reconocimiento de la IUGS ya está en `geography.geoheritage`. Aquí queda solo la historia distinta: Acosta en 1846 y, en el detalle de `monitoring_since_1985`, el año 1986 de la ficha IUGS frente al monitoreo desde 1985 de la hoja del SGC. No se funden.
- `why_1985_deadly` abre con la exposición al lahar y con los factores de la hoja de 2024. Pinatubo queda en el detalle, con la cifra de 25 mil que usa esa hoja y la advertencia de que otras páginas del SGC no coinciden.
- `subject_of_rights` dice en lenguaje llano la protección, la representación y el plan. El detalle conserva la directriz de cero presencia humana de primera instancia y que la Corte modificó ese numeral.
- Ninguna respuesta elige un solo número de muertos, un solo VEI de 1985 ni una sola velocidad del lahar de esa noche.

## Conteos

- Meta de la fila: 70.
- Entradas: 45.
- Ejemplos: 541. Mínimo 12. `history_culture.armero_1985` tiene 13 porque conserva las seis frases de la semilla.
- Negativos: 3 por entrada. Variantes: 1, salvo Kumanday, la creación de 1974 y Armero, que tienen 2.
- `related`: 2 o 3, solo identificadores de este archivo.
- Banco de aclaración: 7. Filtro `volcano` con su pregunta. Ninguna entrada usa `needs`.
- Validación: `jsonschema` contra `research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json`, sin errores. Revisión local de etiquetas, ejemplos únicos, frases cortas y choques exactos con las otras secciones presentes ese día. No se reescribió `coordination/validation.json`.

Quedarse en 45 es la decisión de la compuerta de evidencia. Subir a 70 habría exigido leyendas, biografías, censos y cronologías sin pasaje oficial.

## Semilla

Índices asignados: 12, 16, 17 y 23.

| Índice | Etiqueta original | Dónde quedó | Qué se dejó fuera |
|---|---|---|---|
| 12 | el nombre Kumanday | `kumanday_name`, y también `poleka_kasue` y `dulima` | La grafía Cumanday y los nombres Tabuchía y Tama están en `ruiz_other_ancestral_names`, tomados de la hoja de septiembre de 2024 |
| 16 | la erupción de 1985 y Armero | `armero_1985` | Se conservan fecha, deshielo, lahar, Armero y Tolima. Se añaden 74 km, Chinchiná y Rioclaro, y el desacuerdo de cifras. No hay hora |
| 17 | qué es un lahar | `what_is_a_lahar` y `primary_secondary_lahar` | La definición sale del mapa de amenaza. Primario y secundario salen de la nota del 28 de abril de 2023 |
| 23 | la extensión y la creación del parque | `park_creation_1974` y `founding_approximate_area` | La creación es el 30 de abril de 1974. Las 38.000 ha son las aproximadas de 1973. Las hectáreas de hoy no se copian: geografía tiene el orden menor y la ficha trae 61.388,24 y 61.410 |

Los ejemplos «extensión», «tamaño del parque» y «cuántas hectáreas tiene» no se repiten aquí. Geografía ya usa «extensión».

## Fuentes releídas

Todas el 2026-11-21, con archivo en `history_culture/evidence/`.

- Ficha de Parques Nacionales, sobre el HTML ya guardado, más el sello `article:modified_time` 2026-10-31.
- Resolución 148 de 1974, PDF.
- Índice normativo del parque.
- Hoja del Ruiz, septiembre de 2024, PDF.
- API del portal histórico del Ruiz y del Tolima, y el listado de volcanes.
- Tabla de actividad histórica.
- Memoria del mapa de amenaza, noviembre de 2015, PDF.
- Nota de lahares del 28 de abril de 2023.
- Página de conceptos del mapa de amenaza.
- STL10716-2020, PDF.
- Ley 2505 de 2025, Secretaría del Senado.
- Ficha Unesco del paisaje cafetero, lista 1121.
- Ficha IUGS, solo para Acosta 1846 y el año 1986.

No se recuperaron, y por eso no se citan: el gestor de Función Pública de la Ley 2 y la ficha SUIN. El certificado SSL falló. La excepción de turismo de la Ley 2 no se sirve.

## Conflictos que la respuesta no cierra

- Muertos de 1985: más de 20.000 en Armero (resumen del portal); más de 23.000 en Armero (relato del día); más de 25.000 en la tabla; 25 mil en la hoja de 2024; más de 25.000 en Armero y Chinchiná, y también aproximadamente 25.000, en la memoria de 2015. El resumen del portal además junta 1595, 1845 y 1985 en más de 25.000.
- 1595: alrededor de 600 en el resumen; más de 600 en la hoja de 2024. La memoria de 2015 junta 1595 y 1845 en alrededor de 1000.
- 1845: cerca de mil en el relato; aproximadamente 1.000 en el resumen; más de mil en la hoja y en la tabla.
- VEI de 1985: 3 a 4 en la hoja de 2024; VEI 3 en la memoria de 2015. La tabla no dejó una celda VEI legible para ese día.
- Velocidad: el relato del 13 de noviembre dice más de 40 km/h. La nota de 2023 dice que los lahares primarios pueden superar 70 km/h en general. No es la medición de esa noche.
- Ríos de 1985: la memoria nombra Gualí, Azufrado, Lagunilla, Nereidas y Molinos, y atribuye Armero al Azufrado y al Lagunilla. El portal escribe Lagunillas y añade afluentes. La ficha del parque nombra Lagunilla, Gualí y Chinchiná.
- Ley 2 de 1959: 17 de enero en el Acuerdo 15; 16 de diciembre en el índice de Parques.
- Patrimonio de 2025: el título de la Ley 2505 declara; el artículo 1 reconoce; el parágrafo pide la postulación; la ficha del parque dice que fue declarado.
- Monitoreo: la hoja dice desde 1985. La ficha IUGS pone en 1986 el inicio formal de la vulcanología colombiana.
- INDERENA: la resolución y el índice no escriben el nombre igual. Se usa la sigla. El escaneo dice una vez Decreto 2420 de 1938; el resto del mismo PDF dice 1968.
- «20 días antes» en el párrafo del mapa del 7 de octubre de 1985 no cuadra con el 13 de noviembre. No se sirve.

## Qué se quitó

- `iugs_listing`. El listado de 2022 queda en geografía.
- `water_and_coffee_region`. La regulación del agua es de flora. La frase legal del agua queda dentro de `ruiz_natural_heritage`.
- `antioquian_colonization` como censo de familias del parque. Salía de un PDF de guao.org que no se volvió a usar. La Unesco sí atribuye la arquitectura de los pueblos cafeteros a colonos de Antioquia: eso está en `bahareque`.
- `ley_1959_tourism_clause`. Sin el texto de la Ley 2 no se afirma la excepción de turismo. En su lugar, `acuerdo_1973_limits` copia lo que el Acuerdo 15 sí prohíbe.
- Bahareque se mantuvo, ahora con la ficha Unesco, no con la página del operador del paisaje.
- 51 municipios, criterios tomados de esa página de operador, y el 25 de junio como día de inscripción. La ficha Unesco da 2011, criterios (v) y (vi), seis paisajes y dieciocho centros urbanos.
- Cifras de familias, el estudio de 1998 y el de 2002.
- Altura, edad del volcán, hectáreas actuales, lista de departamentos y origen físico de los ríos.
- Alerta de hoy, colores de alerta y la frase de alerta verde del Tolima.
- Hora de la erupción, biografía de víctimas, leyendas y etimología de Ruiz o de Valle de las Tumbas.
- El nivel naranja del 28 de abril de 2023.

## Vacíos que siguen

- Hora del 13 de noviembre de 1985.
- Cifra única de muertos y cifra separada de Rioclaro.
- Velocidad medida esa noche.
- Cronología eruptiva de Santa Isabel en el portal histórico.
- Censo actual de familias.
- Dirección y horario del centro de memoria, y si el bien de interés cultural ya superó la lista de candidatos.
- Texto consolidado de la Ley 2 que cierre el día.
- Si el plan de manejo vigente es el de 2007, el de 2017 u otro posterior al índice.

## Round 2 (2026-11-21)

Alcance: auditoría de las 45 entradas existentes contra las fuentes ya descargadas, y expansión con entradas nuevas respaldadas por citas. Las citas están en `history_culture/evidence/quotes.md`; la verificación es `history_culture/check_quotes.py`.

### Conteos
- Entradas: 45 → 59 (meta 70; ver brechas). Ejemplos: 541 → 712. Ninguna entrada eliminada.
- Respuestas corregidas: 26. Ejemplos cambiados: 5. Negativos fijos: todos son ejemplos exactos de otra entrada (0 banderas `hard_negative_review` en esta sección).
- `check_quotes.py`: 260 citas, 0 fallos. Cada cifra, año, nombre propio y referencia legal de cada respuesta aparece en las citas etiquetadas a esa entrada.
- Validador: `Errors: 0; review flags: 4` (las cuatro banderas globales pertenecen a otras secciones).

### Correcciones de contenido (entradas existentes)
- `primary_secondary_lahar`: decía que el Ruiz estaba en nivel naranja el 28-IV-2023. La nota del SGC habla de una alerta del IDEAM para municipios del área de influencia. Corregido.
- `rivers_1985`, `armero_1985`, `why_1985_deadly`: se quitaron frases sin cita (hora, «20 días antes», «amanecer» solo en el detalle, «no trae una hora»).
- `indigenous_peoples`, `poleka_kasue`: se atribuía a los quimbaya el nombre Poleka Kasue, que la ficha no atribuye. Corregido. Se quitó «paramillo del Cisne» y «No hay mapa público de resguardos».
- `park_creation_1974`: decía «Resolución Ejecutiva»; el texto dice «Resolución 148». Se usa la fecha de declaratoria y el índice.
- `ley_2_1959`: el día de la Ley 2 no coincide entre fuentes; se atribuyó al Acuerdo 15 algo que dice la resolución.
- `management_plan_adoptions`: cifras de Diario Oficial con punto (46.754, 50.370).
- `coffee_landscape`: cifras de la Unesco en formato inglés (141,120 ha; 207,000 ha).
- `el_bosque`: se precisó la ruta según la ficha («desde Pereira, a través de la vereda El Bosque»).
- `memory_center`, `armero_guayabal_name`: nombres de la Ley 2505 tal como aparecen (Unidad Nacional de Gestión de Riesgos; «Armero - Guayabal»). Se quitó la alcaldía, que la ley no nombra.
- `respectful_memory`: se usa el texto del artículo 11; se quitó la frase de reflexión sin fuente.
- `tolima_history`: se quitó «alerta verde» del detalle (estado actual, no histórico) y la mención a Armero.
- Ejemplos: se quitaron pedidos de leyenda o cuento sin fuente oficial (`poleka_kasue`, `indigenous_peoples`, `eruption_1595`) y dos preguntas sobre alerta actual que pertenecen a `weather_volcano` (`eruptions_2012_and_dome`). `ruiz_natural_heritage`: se quitó «¿da entrada gratis?», que la respuesta no cubre.
- Parche de pulido `coordination/polish/history_culture.json`: se retiró. Sus 90 cambios de ejemplos quedaron en los módulos, salvo los que se retiraron arriba. Respaldo: `/tmp/claude-1000/-home-cruz1122-dev-hacka-airplane/a72e89f3-fa1e-43b5-be8c-25c619af6948/scratchpad/polish_history_culture.backup.json`.

### Entradas nuevas (14)
`ruiz_name_origin`, `cieza_1553_first_record`, `termales_history`, `colonizacion_antioquena`, `lahar_1995_lagunilla`, `reactivacion_1994`, `cajiao_1977_warning`, `zero_presence_directive`, `plan_conjunto_2017_2022`, `inderena_1974`, `ley_2505_guias_narrativa`, `ley_2505_educacion_riesgo`, `ruiz_1990_2010_calma`, `exploraciones_siglo_xx`.
Módulo: `history_culture/corrected_round2.py`, conectado en `emit_corrected.py`.

### Fuentes
- Sin descargas nuevas en esta ronda. Todo el texto citado sale de `history_culture/evidence/raw/`:
  - Texto decodificado (`.txt`) de las páginas HTML y de la API del SGC.
  - `pdftotext -raw` de la hoja del SGC de 2024. El modo por defecto mezcla dos columnas.
  - Copias de `services/evidence/pnn_nevados.html` y de `rules`/`activities`.
- Herramientas: `history_culture/tools/extract_text.py` y `find_text.py`.
- Búsqueda web (WebSearch) sobre leyendas y el centro de memoria de Armero: no devolvió fuentes oficiales de leyendas. Los resultados sobre el centro de memoria no se leyeron completos y no se citan.

### Brechas
- Leyendas: ninguna fuente oficial en lo descargado ni en la búsqueda. No hay entradas de leyenda.
- Meta 70: quedan 11 entradas sin fuente distinta y verificable. No se partieron hechos para llegar al número.
- Centro de memoria de Armero: la Ley 2505 no fija sede, horario ni estado de construcción. La página oficial del centro no está descargada.
- Ley 2505: la búsqueda muestra variantes de redacción entre versiones publicadas (artículos 3 y 25, «concurrirán» frente a «podrán articular»). Se usa el texto del Senado descargado; conviene confirmarlo con el Diario Oficial.
- Límites físicos y hectáreas actuales: siguen sin fuente (la ficha da 61.388,24 ha y 61.410 ha; no se sirven).
- Hora del 13-XI-1985, cifra única de muertos, velocidad medida, censo de familias: sin fuente.
- Resoluciones de cierre 068 de 2023 y 0137 de 2020 (índice normativo): son cierres y pertenecen a `hours_status`; no se citan aquí.


## Updated entry: history_culture.prior_rights_1973

- Reason: Actualizar etiqueta a "derechos adquiridos anteriores a la creación del parque" para desambiguar frente a booking_fees.exempt_property_owners, con cita verificada del artículo 4 del Acuerdo 15 de 1973.
- Changed fields: label


## Updated entry: history_culture.ruiz_name_origin

- Reason: Clarify label to improve retrieval discrimination and prevent cross-topic confusions for history_culture.ruiz_name_origin.
- Changed fields: label


## Updated entry: history_culture.termales_history

- Reason: Clarify label to improve retrieval discrimination and prevent cross-topic confusions for history_culture.termales_history.
- Changed fields: label


## Additive entry: history_culture.uton_kumanday_meanings

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Si bien es conocido el nombre indígena de Kumandai, Kumanday o Cumanday, para referirse al Volcán Nevado del Ruiz, no existe la suficiente investigación para delimitar la procedencia de la palabra, la cuál se ubica principalmente en la comunidad prehispánica Quimbaya

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> denominación que tiene muchos debates debido a que Quimbaya puede ser una referencia al trabajo orfebre de diversas comunidades que habitaron el actual territorio de Quindío, Risaralda y parte del Occidente y Centro Sur Caldense

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> “Gran padre de barbas blancas” (tradición oral guías de turismo)

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> En la cosmogonía indígena, este nombre se traduce como 'Cerro Blanco', 'El de la Nariz Humeante' o 'Padre Blanco'.


## Additive entry: history_culture.uton_peoples_cumanday

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las comunidades prehispánicas que habitaron en cercanías a Cumanday (Volcán Nevado del Ruiz) fueron:

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Quimbayas ● Pijaos ● Pantágoras ● Ansermas

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Entre ellas tenían relaciones de intercambio económico y cultural.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> quienes realizaban peregrinaciones religiosas para rendir tributo a la montaña sagrada conocida como Kumanday

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Es posible que estas comunidades tuvieran una relación ritual con Cumanday (Volcán Nevado del Ruiz) sin embargo el registro arqueológico actual no permite caracterizar en qué consistía dicha relación.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Lastimosamente el conocimiento mas cercano que se tiene de las comunidades indígenas que habitaron la región se encuentra ligado a las crónicas de indias y algunas investigaciones arqueológicas que no han lanzado muchas luces en relación con las prácticas rituales

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> es poco probable que en las zonas de páramo se puedan encontrar amplios registros, esto debido a que eran lugares de tránsito para las comunidades prehispánicas

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> manufactura de piezas en aleación de oro y cobre, conocida como Tumbaga

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> los canasteros, quienes recorrían grandes distancias para intercambiar objetos, principalmente, de un alto valor simbólico: plumas, conchas, sale y diferentes minerales.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Hoy en día, algunas comunidades indígenas continúan realizando rituales en este lugar, que consideran sagrado.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Manizales 9 de septiembre de 2024


## Additive entry: history_culture.uton_valle_tumbas_name

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> recibe su nombre por la presencia de rocas largas y planas (lajas) que se asemejan a ataúdes. Algunas comunidades cercanas al PNNN usaban rocas con esta forma para construir tumbas de cancel, (esto no quiere decir que fueran extraídas del Ruiz, es solo una similitud), estas rocas

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> están hoy cubiertas por arena, el nombre de Valle de las Tumbas así como el de las anteriores estaciones es heredado por tradición oral, y hay registros de que en los 80´s ya recibía este nombre.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El sitio también es conocido como "Desierto de la Soledad", nombres que reflejan tanto el tranquilo paisaje del lugar como su significado místico y cultural.


## Additive entry: history_culture.uton_paramo_word

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La palabra páramo proviene del latín paramus, existía en España hasta antes de la llegada de los romanos.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Básicamente el páramo es un lugar yermo, desértico y árido.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En España existe un paisaje similar conocido como la paramera de Castilla.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La forma de relacionarse con los páramos ha variado durante la historia humana indígenas, españoles, instituciones y visitantes tienen miradas que le dan sentido al páramo.


## Additive entry: history_culture.uton_paramo_inhabited

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Los páramos han sido habitados, por comunidades humanas, desde hace unos 10.000 años aproximadamente.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> las diferentes comunidades se asentaban cerca de los ríos y construían terrazas en las laderas con el fin de construir sus viviendas. La forma de habitar se daba a través de un movimiento vertical y horizontal en la cordillera.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> las comunidades prehispánicas se desplazaban a lo largo y ancho para obtener plantas medicinales, frutos y cazar animales

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Las planicies de los páramos fueron utilizadas para llevar a pastar a los animales, pero su principal significado, se encuentra relacionado con los rituales de peregrinación y en los páramos habitan diferentes seres, sobre todo en las lagunas, volcanes y nevados.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> para las comunidades indígenas los páramos fueron lugares destinados para la recolección de plantas medicinales, el pastoreo de animales y el uso ritual

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> eran lugares de tránsito para las comunidades prehispánicas


## Additive entry: history_culture.uton_spanish_paramo

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> para las comunidades indígenas los páramos fueron lugares destinados para la recolección de plantas medicinales, el pastoreo de animales y el uso ritual, esa mirada cambiaría con la llegada de los españoles.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Ellos vieron en la alta montaña un territorio desolado y desabrigado, un lugar sumamente frío y hostil.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> A medida que los españoles fueron “pacificando” a las comunidades indígenas que habitaban las tierras de mayor riqueza productiva y con climas más benévolos, estas fueron ubicadas en Resguardos Indígenas a más de 3000 metros de altura.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Si hubo algo que movilizó a los españoles en su proceso de “conquista” fue las leyendas relacionadas con el oro de las comunidades indígenas. A todos nos suena de algo la leyenda del dorado


## Additive entry: history_culture.uton_arenales_history

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El sector Arenales ha sido históricamente una zona de camping con varias construcciones para los visitantes, desde una bodega de papa en 1937 hasta el Chalet Arenales, diseñado por el arquitecto Simón Vélez, que se incendió en 2010.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La actual cabaña exhibe pendones sobre la historia del esquí en el nevado del Ruiz

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El área también cuenta con un camping en proceso de reglamentación y una zona de escalada llamada Gazaperas.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Aquí ocurrió un accidente en 2006 con el montañista Nelson Cardona, el primer latinoamericano en escalar el Everest con una prótesis, quien sufrió una caída en este sector.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El viento es tan fuerte en algunas ocasiones que arranco las escaleras de la cabaña, actualmente se encuentran en otra posición.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Manizales 9 de septiembre de 2024


## Additive entry: history_culture.uton_ski_ruiz

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La actual cabaña exhibe pendones sobre la historia del esquí en el nevado del Ruiz en los años 50 y 60, cuando se realizaron campeonatos sudamericanos que llevaron a la creación del Club de Ski de Manizales. La actividad de esquí se detuvo debido al deshielo que afectó las instalaciones.

- research_notes/uton_guion_2024/guion_turistico_zona_norte.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`

> Aquí funcionó el antiguo Chalet Arenales, un recordatorio del retroceso glaciar; donde antes hubo nieve permanente para el esquí, hoy queda un desierto de altura.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Manizales 9 de septiembre de 2024


## Additive entry: history_culture.uton_arenales_ghost_girl

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Hay un mito que viene desde los 80´s sobre una niña fantasma, se dice que ella mora en este sector, y que diversos guías, guardaparques, montañistas y rescatistas la han visto.


## Additive entry: history_culture.uton_juan_diaz_mohan

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Juan Díaz Jaramillo, fue un español que, proveniente del Ecuador, decidió asentarse en Tocaima

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> persiguiendo el rastro del oro indígena durante la segunda mitad del siglo XVI.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> exploró la actual zona del Norte del Tolima, principalmente el Cañón del Río Lagunilla, en donde fue instalando diferentes minas, las cuales fueron arrasadas por la erupción del Volcán Nevado del Ruiz (conocido para la época como volcán de Cartago) en 1595.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Antes de ese suceso en 1581 una avalancha arrasó con su casa en Tocaima, la casa del Rico del pueblo.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En la memoria colectiva se juntaron las dos avalanchas como un solo suceso que dejó a Juan Díaz Jaramillo sin un ápice de riqueza, convirtiéndolo en un mohán o en un “encantado” que gobierna las avalanchas, las crecientes y los “volcanes”

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> en su ambición negó compartir un poco con un cura vestido de mendigo que llegó hasta su casa

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> y posteriormente con sus padres, quienes lo maldijeron

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> una de estas se lleva la casa de Juan Díaz con toda su riqueza, pero, él no muere, se convierte en un encantado un mohán que propicia las avenidas torrenciales. Luego de las avenidas torrenciales o avalanchas queda al descubierto el oro, regado en las riberas de los ríos.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En la memoria popular se habla de que esa avalancha fue generada por Juan Díaz

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> es con el objetivo de mostrar otros conocimientos, en este caso el campesino, surgido en la época colonial y que le da sentido a diferentes fenómenos como la erupción de un volcán.


## Additive entry: history_culture.uton_events_1595_1845

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Nadie sabe por qué se hizo un emplazamiento en el lugar donde habían ocurrido dos avalanchas documentadas: la de 1595, por Fray Pedro Simón, y la de 1845, por viajeros del siglo XIX.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Informe de Uldarico Leiva gobernador de la provincia de Mariquita:

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> se ha esperimentado una avenida horrible del Río Lagunilla, que ha inundado más de siete leguas sobre sus márjenes. Inumerables trozos de nieve han rodado por todas partes acompañados de barro, que, según los datos que se comunican, no son sino el producto de algún volcán en el páramo de Ruiz

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Claridad: para la época la palabra volcán se refiere a un derrumbe o deslizamiento de tierra.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En esta erupción murieron alrededor de 1000 personas en los que para ese entonces era San Lorenzo actuales ruinas de Armero.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> llegaron en 1895 a la zona en la que después se edificó el pueblo

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> el Decreto 1049 del 29 de septiembre de 1908 para bautizar al nuevo municipio como San Lorenzo.


## Additive entry: history_culture.uton_armero_founding

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> A finales del siglo XIX, las grandes haciendas ubicadas en las inmediaciones de lo que después sería Armero necesitaban tener cerca a sus trabajadores

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> las de Raimundo Melo, Sinforoso Chacón y Dominga Cano de Rada, entre otras, llegaron en 1895 a la zona en la que después se edificó el pueblo

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Dicen que el general Reyes firmó sobre la espalda de un trabajador de la época el Decreto 1049 del 29 de septiembre de 1908 para bautizar al nuevo municipio como San Lorenzo.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En 1930, la Asamblea del Tolima decidió cambiar el nombre por el de Armero, en honor José León Armero, prócer nacido en Mariquita, en 1775.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Nadie sabe por qué se hizo un emplazamiento en el lugar donde habían ocurrido dos avalanchas documentadas

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Mediante el Decreto 106 del 11 de noviembre de 1930 se nombró al primer alcalde, el liberal Jorge Ferreira.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> principalmente cultivos de algodón, arroz, la ganadería y la fertilidad de una tierra asentada sobre el lecho de varios ríos, Armero comenzó a ser un foco de migración muy importante en el país.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Según un informe de la Cámara de Comercio de Honda, citado por Hugo Viana Castro, más de 50 extranjeros llegaron al pueblo apenas cinco años después de fundado.


## Additive entry: history_culture.uton_armero_aviation

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Los pilotos alemanes llegaron a Armero pasada la Segunda Guerra Mundial, pues ya el municipio era famoso por la instalación de la Granja Experimental Agrícola desde 1934

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Debido al rápido avance de cultivos como el algodón, una década después fue necesario fumigar con aeronaves una zona que iba a convertirse en la capital blanca de Colombia.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Cuenta la historia que el capitán Hans Hoffman, en un Piper modelo J3-CUB, de 65 caballos de fuerza, inició la fumigación animado por don Martín Delgado, propietario de un cultivo que estaba siendo devorado por el gusano de Alabama.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> La fumigación aérea nació en Armero. Temerarios pilotos como Jorge Montealegre sobrevolaron por muchos años los cultivos blancos de algodón.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> En Armero se instalaron importantes empresas de aviación como Cofa, EFA, Cayta, Helicol y AR.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> en los años cincuenta, llegaron oficiales retirados de la Fuerza Aérea, como el mayor Rafael Millán. Los jóvenes, entusiasmados con la idea de volar, se convirtieron en versátiles pilotos

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> el loco Jorge Montealegre, que pasaba por la mitad del pueblo atravesando la iglesia y sobrevolando el Club Campestre.


## Additive entry: history_culture.uton_armero_memory

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Armero sigue siendo una diáspora. Nunca hubo duelo, los muertos quedaron sepultados.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Décadas han pasado y en Armero se continúa recolectando la memoria dispersa por el país y el mundo,

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> en Guayabal, actual casco urbano del municipio y anteriormente corregimiento, viven muchos de los sobrevivientes, quienes a través de ejercicios de memoria como el de la Fundación Armando Armero, buscan encontrar nuevos caminos sin olvidar la tragedia, uno de esos caminos es el que sigue los rastros de los niños sobrevivientes que fueron adoptados de manera regular o irregular y diseminados por todo colombia e incluso el mundo.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Cada año se recuerda a esos niños quienes en la actualidad son adultos que bordean los cuarenta años. Cada año padres y madres recuerdan la tragedia y renuevan las esperanzas del tan ansiado reencuentro.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Manizales 9 de septiembre de 2024


## Additive entry: history_culture.uton_arenas_crater_name

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> El nombre del cráter Arenas se dio en honor al geógrafo que lo “descubrió” en 1950.

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Otro nombre que recibió el volcán fueron Volcán de Cartago (crónicas de Indias).

- research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt (checked 2026-11-26); evidence: `research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt`

> Es importante recordar que el Nevado del Ruiz es un complejo volcánico compuesto por cuatro estructuras (Nereidas, Olleta, Piraña y Arenas), aunque comúnmente se le conoce como Nevado del Ruiz al edificio que alberga el cráter Arenas.


## Updated entry: history_culture.uton_valle_tumbas_name

- Reason: Keep Valle Lunar naming questions off the Tumbas name entry.
- Changed fields: hard_negatives


## Updated entry: history_culture.uton_arenales_ghost_girl

- Reason: Station chat phrasing: 'aquí espantan'.
- Changed fields: examples
