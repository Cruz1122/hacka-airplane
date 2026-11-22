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
