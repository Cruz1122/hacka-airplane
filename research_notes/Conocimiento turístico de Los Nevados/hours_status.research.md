# Registro de Investigación: Espacio `hours_status` (Horarios y Estado del Parque)

**Investigador / Subagente:** Subagente de Investigación `hours_status` (Orden 6)  
**Proyecto:** Asistente Turístico Offline para el Parque Nacional Natural Los Nevados, Colombia  
**Fecha de corte:** 2026-11-21  
**Archivo de datos producido:** `/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/hours_status.json`  
**Esquema de validación:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json`  
**Estado:** Ronda única de corrección posrevisión del coordinador completada.

---

## 1. Fuentes Consultadas, Metadatos y Archivos Guardados en Disco

Se utilizaron exclusivamente fuentes oficiales y actos administrativos verificados, con archivos de respaldo presentes en el repositorio:

1. **Parques Nacionales Naturales de Colombia (PNNC) · Ficha Oficial Los Nevados**
   - **URL:** `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/`
   - **Archivo en disco:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/services/evidence/pnn_nevados.txt` (metadato HTML `article:modified_time`: `2026-10-31`, consultado el `2026-11-21`).
   - **Contenido verificado:** Horarios oficiales de ingreso por sector (Brisas 8:00 a 14:00 con última charla 13:30; Cisne/Potosí 7:30 a 10:00; Otún 7:00 a 12:00; Cocora 6:00 a 10:00; Juntas y Anzoátegui 6:00 a 11:00); cronograma de tres descansos ambientales de 5 días al año (semana post-Semana Santa, cuarta semana de septiembre, cuarta semana de noviembre); política de reservas previas (Brisas en fines de semana y festivos; Cisne/Otún 3 días hábiles; Dulima 5 días hábiles); distancia a pie desde El Cedral (18 km, 7,5 km al límite); y canales de atención ciudadana.
2. **Parques Nacionales Naturales de Colombia · Resolución No. 207 de 2023**
   - **Acto administrativo:** *Reglamentación Transitoria de la Actividad Ecoturística para la Reapertura del PNN Los Nevados*.
   - **Archivo en disco:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`.
   - **Contenido verificado:** Horarios de puestos de control; registro obligatorio el día previo para cumbre Santa Isabel; sendero Laguna Verde (8:00 a 14:00); prohibición general de camping en el área protegida con habilitación transitoria de pernocte en Termales Cañón, Arenales y Calvito bajo monitoreo; prohibición de tránsito nocturno; exigencia de guía e intérprete registrado; y prohibición de playbacks.
3. **Secretaría de Tránsito y Transporte del Tolima · Gobernación del Tolima**
   - **Acto administrativo:** **Resolución No. 1815 del 24 de julio de 2026** (citada y vinculada en la ficha técnica oficial de PNNC).
   - **Contenido verificado:** Pico y Placa Ambiental en el corredor Murillo–La Esperanza (acceso a Brisas); vigencia; sábados, domingos y festivos de 5:00 a. m. a 4:00 p. m.; rotación de placas; prohibición permanente a vehículos de carga $\ge$ 3,4 toneladas y buses $>$ 19 pasajeros.
4. **Parques Nacionales Naturales de Colombia · Canales de Atención al Ciudadano**
   - **URL:** `https://www.parquesnacionales.gov.co/atencion-al-ciudadano/`
   - **Archivo en disco:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/actions/evidence/pnn-atencion.txt`.
   - **Contenido verificado:** Horario de oficina institucional de lunes a viernes de 8:00 a. m. a 4:30 p. m. continua; conmutador +57 (601) 353 2400 (ext. 3011-3012); teléfono celular +57 3229471031.
5. **Servicio Geológico Colombiano (SGC) · Monitoreo Volcánico y Boletines**
   - **URL:** `https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx`
   - **Archivo en disco:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/conversation/evidence/www2_sgc_gov_co_Noticias_Paginas_Boletines-semanales_aspx.html`.
   - **Contenido verificado:** Niveles de alerta volcánica (Verde, Amarilla, Naranja, Roja). Articulación con la Resolución PNN 068 de 2023: cierre preventivo total o de zonas de amenaza ante nivel Naranja o Rojo; operación regulada en sectores autorizados bajo nivel Amarillo.
6. **Concesión Unión Temporal Operación Nevados (UTON)**
   - **Portal web:** `https://www.operacionnevados.co/` (declarado honestamente como no accesible directamente en el entorno aislado de pruebas).
   - **Sustentación fáctica:** Todos los datos de UTON (oficinas en Manizales en Carrera 26A #68-44 Palermo y Calle 70 #27-70; horario de atención de lunes a viernes 8:00 a 12:00 m. y 14:00 a 17:00; teléfonos 321 506 6031 / 322 360 3637) provienen de la transcripción oficial de la página oficial de Parques Nacionales Naturales de Colombia.

---

## 2. Correcciones Realizadas Tras la Revisión Coordinadora

En cumplimiento estricto del informe de revisión (`hours_status.review.json`), se realizaron las siguientes correcciones de fondo en todo el espacio:

1. **Eliminación de horarios y protocolos de rescate inventados en `camping_arrival_cutoff` (BLOQUEANTE):**
   - Se suprimió la afirmación de llegada obligatoria a las 16:30 o 17:00 y la supuesta activación automática de búsqueda de rescate a las 17:30 en todos los campos (`short`, `variants`, `steps`, `detail`).
   - Se reemplazó por la normativa oficial: Parques Nacionales no fija una hora reglamentaria de llegada a carpas ni rescate automático, sino que controla el ingreso matutino con equipo de montaña (7:00 a 12:00 en Potosí), autoriza camping transitorio únicamente en puntos específicos (Termales Cañón, Arenales, Calvito) y prohíbe el tránsito nocturno.
2. **Corrección de protocolos de reapertura en `reopening_protocol_after_emergencies` (BLOQUEANTE):**
   - Se eliminó la afirmación de un comité multiactores universal que "certifica terreno seguro".
   - Se explicó el procedimiento real de verificación ciudadana: consultar los comunicados oficiales y resoluciones administrativas de Parques Nacionales levantando la medida preventiva, advirtiendo explícitamente que el cese del cierre no exime de los riesgos naturales dinámicos de la alta montaña.
3. **Corrección de temporadas altas en `high_season_calendar`:**
   - Se eliminaron las fechas calendario cerradas (15 de diciembre, fin de enero, mitad de junio, julio) y la afirmación de reserva obligatoria diaria en Brisas.
   - Se describieron los periodos tradicionales de alta afluencia (fin de año, Semana Santa, mitad de año, festivos) y se precisó la política de reserva: solicitada en Brisas para fines de semana y festivos (y aconsejada en periodos de alto tráfico como noviembre por el pico y placa), mientras que en sectores de travesía siempre es obligatoria con operador registrado.
4. **Corrección del sector Otún en `otun_sector_hours`:**
   - Se mantuvo el horario oficial publicado en Cabaña Potosí (7:00 a. m. a 12:00 m.).
   - Se eliminó la implicación de llegar a la laguna antes de mediodía y el argumento no sustentado sobre cupos Ramsar reducidos, instruyendo a verificar cambios operativos con Parques Nacionales.
5. **Auditoría general de afirmaciones operativas en las 40 entradas:**
   - En `brisas_exit_time`: se eliminaron los horarios de evacuación inventados (3:30 / 4:00 p. m.), aclarando que PNN fija el ingreso hasta las 2:00 p. m. y que el descenso diurno se coordina con el guía antes del anochecer.
   - En `brisas_open_days`: se eliminó la promesa de apertura incondicional los 365 días del año, detallando que opera habitualmente a diario pero está sujeto a suspensiones por alertas volcánicas, clima o descansos ambientales.
   - En `santa_isabel_summit_start_hour` y `tolima_summit_push_hours`: se eliminaron las horas fijas de madrugada reglamentarias (4:00–5:30 a. m. y 1:00–3:00 a. m.), explicando que PNN regula los puestos de control en base y el día anterior, mientras que el guía coordina la partida de madrugada por seguridad técnica.
   - En `cedral_otun_hiking_schedule`: se eliminó el horario inventado de la chiva de las 5:30 a. m., manteniendo la distancia oficial de 18 km (7,5 km al límite) y la necesidad de madrugar con guía.
6. **Advertencia de dinamismo y redirección a PNNC en todas las variantes servidas:**
   - Cada respuesta (`answer.short`) y cada variante independiente (`answer.variants`) advierte que los horarios y accesos están sujetos a cambios y dirige al visitante a consultar los canales oficiales de Parques Nacionales antes de viajar o al recuperar conexión.

---

## 3. Vacíos de Información Oficial Documentados Honestamente (Gaps)

1. **Hora fija reglamentaria de salida en Brisas:** Parques Nacionales no publica una hora límite de salida obligatoria; regula el cierre de ingreso a las 2:00 p. m. y última inducción a la 1:30 p. m.
2. **Hora reglamentaria de llegada a carpas:** No existe una hora límite de llegada a campamentos ni un protocolo de búsqueda automática a las 17:30 en los reglamentos de PNNC.
3. **Hora oficial de ataque a cumbres:** No existe un horario de partida de campamento alto fijado en resoluciones; depende de la coordinación del guía autorizado y las condiciones nivológicas del día.
4. **Límites calendario estáticos de temporadas:** PNNC no fija fechas exactas de corte anual para temporada alta o baja.
5. **Aforos numéricos estáticos por sendero:** Varían según conceptos técnicos biológicos estacionales y no se publican como números fijos inmutables en la cartilla turística general.

---

## 4. Conflictos entre Fuentes y Resolución Aplicada

- **Cierres por conservación (Descansos ambientales):**
  - *Conflicto:* La Resolución 207 de 2023 establecía en su texto inicial cuatro descansos de 7 días al año (febrero, Semana Santa, julio, noviembre). La ficha oficial actualizada de PNNC (modificada en 2026) establece taxativamente tres descansos de 5 días al año (semana siguiente a Semana Santa, cuarta semana de septiembre y cuarta semana de noviembre).
  - *Resolución:* Se adoptó la regla vigente más reciente de Parques Nacionales (tres descansos de 5 días), reflejándola en `hours_status.conservation_closures` y `hours_status.conservation_closures_dates_schedule`.
- **Pico y Placa Ambiental en Murillo–La Esperanza:**
  - *Conflicto:* Documentos locales previos manejaban horarios de 6:00 a. m. a 6:00 p. m.
  - *Resolución:* Se aplicó la **Resolución No. 1815 del 24 de julio de 2026** de la Secretaría de Tránsito y Transporte del Tolima (citada por PNNC), que fija el horario de 5:00 a. m. a 4:00 p. m. los sábados, domingos y festivos.

---

## 5. Mapeo de la Semilla Original (`conocimiento.json`)

Los tres temas asignados a este espacio fueron preservados, corregidos y expandidos:

| Índice Semilla | Etiqueta Original en `conocimiento.json` | ID Final en `hours_status.json` | Etiqueta Final | Tratamiento y Mejoras Realizadas |
|---|---|---|---|---|
| **4** | `los horarios de ingreso` | `hours_status.general_opening_schedule` | `horarios generales de ingreso al parque` | Mantiene el horario de Brisas (8:00 a 14:00 con charla 13:30) y los horarios oficiales de Cisne, Otún y Cocora. Advierte que pueden variar y remite a PNN. Posee 13 ejemplos variados, incluyendo inglés y giros colombianos. |
| **6** | `si el parque está abierto` | `hours_status.park_open_today` | `verificar si el parque está abierto hoy` | Mantiene la advertencia de funcionamiento offline, explica las causas de suspensión (alertas volcánicas, clima, conservación) y remite a los canales oficiales. Posee 13 ejemplos. |
| **41** | `los cierres por conservación` | `hours_status.conservation_closures` | `cierres programados por conservación y descanso` | Detalla los tres descansos anuales de 5 días reglamentados por Parques Nacionales (post-Semana Santa, septiembre, noviembre). Posee 13 ejemplos. |

---

## 6. Métricas y Validación Final

- **Total de entradas:** 40 entradas (meta del proyecto: 40).
- **Total de ejemplos:** 483 ejemplos (media: 12,08 ejemplos por entrada; mínimo 12, máximo 13).
- **Variedad de ejemplos:** Consultas cortas, preguntas completas, giros colombianos ("a qué horas abren", "hasta qué hora dejan entrar", "toca madrugar mucho"), variantes sin tilde/ortografía coloquial y 1–2 preguntas naturales en inglés en cada una de las 40 entradas.
- **Unicidad de ejemplos:** 483 / 483 ejemplos únicos en el espacio; 0 colisiones locales.
- **Negativos difíciles (`hard_negatives`):** 120 preguntas (exactamente 3 por entrada).
- **Etiquetas (`label`):** 40 / 40 formuladas con una longitud de 3 a 8 palabras, claramente diferenciadas.
- **Respuestas (`answer.short`):** 1 a 3 frases en "tú", amables, con acción concreta y advertencia de verificación ante Parques Nacionales.
- **Validación JSON Schema (`knowledge-section.schema.json`):** 100 % superada (`Draft202012Validator: PASSED`, 0 errores).
- **Validación contractual de cifras y fuentes oficiales:** 100 % superada (0 errores de citas o números sin `last_verified` o sin fuente oficial `.gov.co`).

---

## 7. Ronda 2 — Auditoría de Evidencia Cruda, `overlay.py` y `check_quotes.py` (2026-11-21)

### 7.1 Conteo antes → después
- **Antes (snapshot `hours_status.v1.json` posfusión de Ronda 1):** 38 entradas / 471 ejemplos.
- **Después (construido mediante `hours_status/source/overlay.py`):** 40 entradas / 495 ejemplos (meta exacta de la sección: 40 entradas).

### 7.2 Archivos crudos descargados y almacenados en `hours_status/evidence/raw/`
1. **`pnn_nevados.html` y `pnn_nevados.txt`**
   - **URL:** `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/` (`article:modified_time`: `2026-10-31`).
   - **Ruta:** `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html` y `pnn_nevados.txt`.
2. **`resolucion_207_2023.pdf` y `resolucion_207_2023.txt`**
   - **URL:** `https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf`
   - **Ruta:** `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.pdf` y `resolucion_207_2023.txt`.
3. **`resolucion_1815_2026.pdf` y `resolucion_1815_2026.txt` (extraído por OCR de 22 páginas)**
   - **URL:** `https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf`
   - **Ruta:** `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_1815_2026.pdf` y `resolucion_1815_2026.txt`.
4. **`pnn_atencion.html` y `pnn_atencion.txt`**
   - **URL:** `https://www.parquesnacionales.gov.co/atencion-al-ciudadano/`
   - **Ruta:** `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_atencion.html` y `pnn_atencion.txt`.
5. **`sgc_boletines.html`**
   - **URL:** `https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx`
   - **Ruta:** `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/sgc_boletines.html`.

### 7.3 Entradas modificadas o añadidas en `hours_status/source/overlay.py`
- **`hours_status.road_closure_status` (reescrita):** Se eliminó el número telefónico `(#767)` que no figuraba en los documentos crudos descargados y se respaldó la verificación vial con Invías, la Policía Nacional de Tránsito, la Secretaría de Tránsito y Transporte del Tolima y Parques Nacionales conforme a la Resolución 1815 de 2026 y la ficha oficial del PNN Los Nevados.
- **`hours_status.uton_concession_office_hours` (fuentes depuradas):** Se eliminó la URL raíz `https://www.operacionnevados.co/` (marcada como `homepage_source` en la auditoría), conservando la URL profunda de la ficha oficial de Parques Nacionales (`pnn_nevados.txt`), de donde provienen textualmente las direcciones, horarios y teléfonos de UTON en Manizales.
- **`hours_status.quindio_dulima_juntas_anzoategui_hours` (conflicto de fuentes documentado):** Se añadió en `detail` y `sources` la comparación explícita entre la ficha web vigente de Parques Nacionales (Juntas y Anzoátegui de 6:00 a. m. a 11:00 a. m. bajo reserva previa) y la Resolución 207 de 2023 (que fijaba Juntas de 6:00 a. m. a 10:00 a. m. y Anzoátegui de 6:00 a. m. a 11:00 a. m.).
- **`hours_status.pico_y_placa_hours_murillo` (fuente primaria añadida):** Se vinculó la URL profunda del PDF de la Resolución 1815 del 24 de julio de 2026 (`RESOLUCION-1815-2026.pdf`) y se precisó en `detail` su vigencia del 25 de julio de 2026 al 20 de julio de 2027 entre Murillo (`PR43+500`) y Cerro Gualí (`PR0+000`).
- **`hours_status.asomadera_potosi_entry_hours` (añadida, +12 ejemplos):** Cubre el horario oficial del recorrido Potosí–La Asomadera fijado en la Resolución 207 de 2023 (7:30 a. m. a 12:00 m., ampliado hasta las 2:00 p. m. para caminatas a La Asomadera sin equipamiento).
- **`hours_status.anzoategui_pit_la_punta_hours` (añadida, +12 ejemplos):** Cubre los días y horarios de atención del Punto de Información Turística (PIT) de Anzoátegui en la Calle 13 entre Carreras 2 y 3 (martes a sábado de 8:00 a. m. a 5:00 p. m.) y del punto de control flotante La Punta en la vereda La Cascada (jueves a sábado de 8:00 a. m. a 5:00 p. m.) según la Resolución 207 de 2023, distinguiéndolos del horario de ingreso al sendero (6:00 a. m. a 11:00 a. m.).

### 7.4 Verificación automática (`check_quotes.py`, `check_sources.py`, `validate_knowledge.py`)
- `python3 "research_notes/Conocimiento turístico de Los Nevados/hours_status/check_quotes.py"`: `Checked 56 quotes across 4 raw files; failed=0`.
- `python3 "research_notes/Conocimiento turístico de Los Nevados/coordination/check_sources.py"`: `hours_status` con `entries: 40`, `homepage: 0`, `missing_tokens: 0`.
- `python3 "research_notes/Conocimiento turístico de Los Nevados/coordination/validate_knowledge.py"`: `Errors: 0; review flags: 2` (0 errores y 0 advertencias o flags en `hours_status`).


## Coordinator final pass (2026-11-21)

- `hours_status.official_channels_to_check_status` gave `losnevados@parquesnacionales.gov.co`, which no downloaded source contains. Corrected in `source/overlay.py` to `nevados@parquesnacionales.gov.co` (Resolución 207 de 2023, quote added to `evidence/quotes.md`). The WhatsApp/celular +57 3229471031 is on the PNN page and stays.


## Updated entry: hours_status.anzoategui_pit_la_punta_hours

- Reason: Use the documented label and cite the full Anzoátegui (Tolima) block for the PIT and La Punta.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Horario de ingreso al Área Protegida entre las 6:00 a.m. y las 11:00 a.m. por tratarse de una travesía

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Anzoátegui (Tolima): Punto de Información Turística (PIT) Calle 13 entre Carrera 2 y 3 barrio centro
>       Horario: martes a sábado de 8:00 a.m. a 5:00 p.m.
> 
>  ●    La Punta (Vereda La Cascada) Anzoátegui-Tolima: (este sitio se establece como punto de control flotante)
>       Horario: jueves a sábado de 8:00 a.m. a 5:00 p.m.


## Updated entry: hours_status.asomadera_potosi_entry_hours

- Reason: La respuesta ya cita la Resolución 207; le falta decir que la ficha de 2026 no repite el horario y que no es el estado del día.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Potosí – La Asomadera: Horario de ingreso entre las 7:30 a.m. a 12:00 m. Para caminatas a la asomadera sin

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> equipamiento se amplía hasta las 2:00 p.m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario de atención en la cabaña Potosí es de 7:00 a. m. a 12:00 p. m.


## Updated entry: hours_status.brisas_exit_time

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.


## Updated entry: hours_status.brisas_hours

- Reason: El horario de la ficha está bien; falta la fecha y no debe leerse como la apertura de hoy.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.


## Updated entry: hours_status.brisas_induction_talk_schedule

- Reason: La 1:30 p. m. está en la ficha; la frase de que después de esa hora no dejan iniciar no está.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.


## Updated entry: hours_status.brisas_open_days

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Son tres (3) cierres al año con una duración de cinco (5) días, así:


## Updated entry: hours_status.camping_arrival_cutoff

- Reason: Remove the false area-wide camping ban. Distinguish Brisas Arenales (2024: not enabled) from Tolima Arenales (transitory 2023).
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> identificados como Termales Cañón, Arenales y Calvito para el pernocte

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> 7:00 a.m. hasta las 12:00 m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario de atención en la cabaña Potosí es de 7:00 a. m. a 12:00 p. m.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> 2.   Sitios para camping:
> 
>  A la luz del Plan de Ordenamiento Ecoturístico las zonas de camping establecidas al interior del PNN Los Nevados
>  corresponden a:
> ● Laguna del Otún.
> ● Centro de visitantes El Cisne (camping Cisne): condicionado por actividad volcánica u operación de servicios
>      ecoturísticos.
> ● Camping Arenales - Sector Brisas (restringido por actividad volcánica).
> 
>  No obstante, en este reglamento temporal transitorio, se habilitan los puntos en inmediaciones al nevado del
>  Tolima, conocidos como:
> ● Termales Cañón.
> ● Arenales.
> ● Calvito.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/raw/pnn_informe_necesidades_2024.txt`

> 3. Arenales – camping
> Zona de camping no se encuentra habilitada debido a la actividad volcánica.
> Cabaña inaugurada en el año 2013. 240 mt2 primer piso – 98 mt2 terraza con área útil caminable y capacidad de máximo 80 personas.
> En el primer piso consta de:
> 1. Un espacio de cocina y bodega.
> 2. Un comedor y dos baterías de baños para visitantes.
> 3. Un punto de atención de primeros auxilios.
> 4. Dos habitaciones y un baño para los empleados. 5. Una batería de baños para hombres y mujeres y duchas, para campistas. 6. Un espacio para basuras y zona de aseo. 7. Un comedor y cocina para los campistas. 8. Depósito para el gas
> Villamaría, Caldas


## Updated entry: hours_status.cedral_otun_hiking_schedule

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> aproximadamente 7,5 km al límite del Parque y 18 km a la Laguna del Otún.


## Updated entry: hours_status.cisne_potan_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> puedes llegar a los puntos de registro del Parque Nacional (cabaña Potosí – alto de Santa Bárbara) desde las 7:30 a. m. hasta las 10:00 a. m.


## Updated entry: hours_status.conservation_closures

- Reason: Cite the full Resolución 207 closure paragraph (seven days and four dates). Keep the documented label.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Son tres (3) cierres al año con una duración de cinco (5) días, así:

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Lunes inmediatamente posterior a Semana Santa hasta el viernes de esa misma semana.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Cuarto lunes de septiembre hasta el viernes de esa misma semana.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Cuarto lunes de noviembre hasta el viernes de esa misma semana.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> En cuanto al cierre del Área Protegida se establecen las siguientes fechas para el cierre que tendrán una duración de
>  siete (7) días después de las temporadas altas; esto con el fin de permitir el descanso y conservación de los ecosistemas.
> 1. La segunda semana de febrero después de la temporada correspondiente a los meses de diciembre y enero.
> 2. Después de la temporada de Semana Santa según corresponda al mes de marzo o abril.
> 3. La cuarta semana del mes de julio, después de la temporada alta de mitad de año.
> 4. La primera semana del mes de noviembre.


## Updated entry: hours_status.general_opening_schedule

- Reason: Cite the Juntas bullet of Resolución 207 (Resolución 268 de 2022), not the unlabeled Cocora hours sentence.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> puedes llegar a los puntos de registro del Parque Nacional (cabaña Potosí – alto de Santa Bárbara) desde las 7:30 a. m. hasta las 10:00 a. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario de atención en la cabaña Potosí es de 7:00 a. m. a 12:00 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Horario de ingreso al Área Protegida entre las 6:00 a.m. y las 11:00 a.m. por tratarse de una travesía

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Juntas: Recorrido desde quebrada Perlas hasta Escuela El Salto o Termales Cañón.
>     Horario de ingreso al Área Protegida entre las 6:00 a.m. hasta las 10:00 a.m. por tratarse de una travesía (Resolución
>     No. 268 de julio 2022).


## Updated entry: hours_status.high_season_calendar

- Reason: Cite the full Temporalidad section of Resolución 207. Keep the previous label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> @ParquesColombia
> @parquescolombia
> @ParquesNaturales
> +573229471031
> @parquescolombia
> Parques

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Temporalidad: Se considera temporada alta los puentes festivos (desde el día jueves que los antecede) y los periodos de
> vacaciones del 15 de diciembre al 30 de enero, 15 junio al 15 de julio, semana santa y la semana de receso escolar
> (octubre).


## Updated entry: hours_status.high_season_operating_changes

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> los cupos diarios son limitados

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.


## Updated entry: hours_status.laguna_verde_trail_hours

- Reason: El horario coincide con la ficha; falta decir que no confirma si el sendero está habilitado ese día.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el sendero Laguna Verde tiene un horario de 8:00 a. m. a 2:00 p. m.


## Updated entry: hours_status.late_arrival_policy

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> puedes llegar a los puntos de registro del Parque Nacional (cabaña Potosí – alto de Santa Bárbara) desde las 7:30 a. m. hasta las 10:00 a. m.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Respetar los horarios establecidos para realizar cada una de las actividades turísticas.


## Updated entry: hours_status.low_season_advantages

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Se considera temporada alta los puentes festivos (desde el día jueves que los antecede)

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Son tres (3) cierres al año con una duración de cinco (5) días, así:


## Updated entry: hours_status.official_channels_to_check_status

- Reason: Use the label documented in findings/labels.json.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> @ParquesColombia
> @parquescolombia
> @ParquesNaturales
> +573229471031
> @parquescolombia
> Parques

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> +57 3229471031
> Horario de atención: Lunes a viernes de
> 8:00 a.m. a 4:30 p.m.
> Jornada Conti

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> +57 (601) 353 2400
> Ext. 3011 - 3012
> Línea gratuita nacional desde un fijo:
> 018000129722
> Te

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Ext. 3011 - 3012
> Línea gratuita nacional desde un fijo:
> 018000129722
> Teléfono celular:
> +57

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> 8:00 a.m. a 4:30 p.m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Jornada Continua
> Correo atención al usuario:
> [email protected]
> Correo de notificaciones ju

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> www.reservasnevados.com

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> nevados@parquesnacionales.gov.co


## Updated entry: hours_status.offline_status_verification_advice

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> @ParquesColombia
> @parquescolombia
> @ParquesNaturales
> +573229471031
> @parquescolombia
> Parques


## Updated entry: hours_status.open_sectors_during_conservation_closures

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Son tres (3) cierres al año con una duración de cinco (5) días, así:

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el área protegida tiene establecidos algunos cierres como una estrategia ambiental para liberar de carga estos lugares naturales y hacer trabajos de monitoreo.


## Updated entry: hours_status.otun_sector_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario de atención en la cabaña Potosí es de 7:00 a. m. a 12:00 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> puedes llegar a los puntos de registro del Parque Nacional (cabaña Potosí – alto de Santa Bárbara) desde las 7:30 a. m. hasta las 10:00 a. m.


## Updated entry: hours_status.park_open_today

- Reason: Cite the SGC index link and say the index does not show the alert level.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/sgc_boletines.html`

> Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> @ParquesColombia
> @parquescolombia
> @ParquesNaturales
> +573229471031
> @parquescolombia
> Parques

- https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/sgc_boletines.html`

> "FileLeafRef": "Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf",

- https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/sgc_boletines.html`

> "serverurl.progid": "1https:\u002f\u002fwww2.sgc.gov.co\u002fNoticias\u002fboletinesDocumentos\u002fBoletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf?d=wfef52b863a304b1695f1daa2f1addc55",


## Updated entry: hours_status.pnn_administrative_office_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> 8:00 a.m. a 4:30 p.m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Jornada Continua
> Correo atención al usuario:
> [email protected]
> Correo de notificaciones ju

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> +57 (601) 353 2400
> Ext. 3011 - 3012
> Línea gratuita nacional desde un fijo:
> 018000129722
> Te

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Ext. 3011 - 3012
> Línea gratuita nacional desde un fijo:
> 018000129722
> Teléfono celular:
> +57

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> +57 3229471031
> Horario de atención: Lunes a viernes de
> 8:00 a.m. a 4:30 p.m.
> Jornada Conti

- https://www.parquesnacionales.gov.co/atencion-al-ciudadano/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_atencion.txt`

> Horario de atención: Lunes a viernes de 8:00 a.m. a 4:30 p.m. Jornada Continua


## Updated entry: hours_status.quindio_dulima_cocora_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> cinco (5) días hábiles


## Updated entry: hours_status.quindio_dulima_juntas_anzoategui_hours

- Reason: Cite the labeled Juntas and Anzoátegui bullets of Resolución 207. Keep the previous label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Juntas: Recorrido desde quebrada Perlas hasta Escuela El Salto o Termales Cañón.
>     Horario de ingreso al Área Protegida entre las 6:00 a.m. hasta las 10:00 a.m. por tratarse de una travesía (Resolución
>     No. 268 de julio 2022).

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Anzoátegui: Recorrido desde la punta (Finca la Aurora) hasta finca Vancouver o Termales Cañón.
>     Horario de ingreso al Área Protegida entre las 6:00 a.m. y las 11:00 a.m. por tratarse de una travesía (Resolución
>     No. 268 del 29 de julio 2022).


## Updated entry: hours_status.reopening_protocol_after_emergencies

- Reason: Cite the full 068 clause and article 1 of Resolución 207. This is the 2023 procedure, not a general protocol. Keep the new label.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> se ordena ia apertura y se adopta la reglamentacion del

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> www.parquesnacionales.gov.co

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Que Parques Nacionales Naturales de Colombia expidio la Resolucion 068 del 31
> de marzo de 2023, "Por medio de la $ual se ordena el CIERRE TOTAL y en
> consecuencia se prohibe el ingreso de visitantes y la prestacion de servicios
> ecotunsticos en el Parque Nacional Natural Los Nevados"; la cual resuelve en los
> articulos 1° y 3° que el cierre del Parque Nacional Natural Los Nevados se
> mantendra "hasta que la Oficina Asesora de Gestion del Riesgo emita el
> correspondiente informe tecnico, con bas$ en la informacion que emita el Servicio
> Geologico Colombiano y demas autoridades competentes" y, por el otro, que las
> actividades misionales, tecnicas, operativas y administrativas se pueden reanudar
> cuando "cesen los factores de riesgo ile desastre natural que motivan esta
> decision ",

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> ARTICULO 1°: Ordenar la APERTURA del Parque Nacional Natural Los Nevados, y
> adoptar la Reglamentacion Transitoria del ecoturismo


## Updated entry: hours_status.road_closure_status

- Reason: Artículo Octavo asks for Invías accompaniment when appropriate. Keep the previous label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> @ParquesColombia
> @parquescolombia
> @ParquesNaturales
> +573229471031
> @parquescolombia
> Parques

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_1815_2026.txt`

> El tramo comprendido entre Murillo y Cerro Guali, desde el PR43+500 Murillo

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_1815_2026.txt`

> El Invias, cuando corresponda.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/08/RESOLUCION-1815-2026.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_1815_2026.txt`

> La Secretaria solicitara el acompafiamiento de:


## Updated entry: hours_status.santa_isabel_conejeras_prior_day_checkin

- Reason: El día anterior está en la ficha; no trae la hora de ese registro.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el registro o paso por los sitios de control se hace el día anterior al ingreso programado para la cima


## Updated entry: hours_status.santa_isabel_summit_start_hour

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el registro o paso por los sitios de control se hace el día anterior al ingreso programado para la cima


## Updated entry: hours_status.tolima_summit_push_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el horario en el punto de atención Valle del Cocora es de 6:00 a. m. a 10:00 a. m., mientras que en Juntas y Anzoátegui es de 6:00 a. m. a 11:00 a. m. (bajo reserva previa)


## Updated entry: hours_status.trail_maintenance_temporary_closures

- Reason: Cite the full restriction sentence of Resolución 207. Keep the new label.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> www.parquesnacionales.gov.co

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Parques Nacionales Naturales los Nevados dentro de sus facultades legales, podrá restringir el ingreso o cerrar los
> atractivos el tiempo que haya lugar, mediante resolución motivada por razones de seguridad, gestión del riesgo,
> investigación y/o protección ecológica (la protección ecológica se debe tener en cuenta mediante los resultados producto
> del monitoreo de impactos al ecoturismo) o por recomendación de alguna entidad.


## Updated entry: hours_status.unplanned_midday_closures

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> podrá limitar la entrada o cerrar alguno de los atractivos turísticos si lo

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> www.parquesnacionales.gov.co


## Updated entry: hours_status.uton_concession_office_hours

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Horario de atención: lunes a viernes, 8:00 a. m. a 12:00 m. y 2:00 p. m. a 5:00 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> 321 506 6031 – 322 360 3637

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Carrera 26A #68-44, barrio Palermo

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> Calle 70 #27-70
> 🕒 Horario de atención: lunes a viernes, 8:00 a. m. a 12:00 m. y 2:00 p. m.


## Updated entry: hours_status.volcanic_alert_closures

- Reason: Restore three real examples, drop two flagged ones, remove the unsourced summit sentence, and cite Resolución 068 plus the 27 June 2023 bulletin. Round 3b (orchestrator, per re-review required_change): removed the example that weather_volcano.alert_orange_meaning answers better. Resolves the high yellow-alert contradiction (no 'siguen abiertos'). r3b-2: removed the statement about the SGC bulletin index (the live index does show a dated level; a dynamic page is not cited for state).
- Changed fields: answer, examples, hard_negatives, label, last_verified, related, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> NIVEL NARANJA o (II): ERUPCION PROBABLE EN TERMING DE DIAS O
> SEMANAS (...).
> Que la Oficina

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Boletm Extraordinario del 27

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> de junio de 2023, declara que "Desoues de 89 dfas en nivel de actividad Narania,
> el volcan

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> permite $ambiar su nivel a Amarillo

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> www.parquesnacionales.gov.co

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Que Parques Nacionales Naturales de Colombia expidio la Resolucion 068 del 31
> de marzo de 2023, "Por medio de la $ual se ordena el CIERRE TOTAL y en
> consecuencia se prohibe el ingreso de visitantes y la prestacion de servicios
> ecotunsticos en el Parque Nacional Natural Los Nevados"; la cual resuelve en los
> articulos 1° y 3° que el cierre del Parque Nacional Natural Los Nevados se
> mantendra "hasta que la Oficina Asesora de Gestion del Riesgo emita el
> correspondiente informe tecnico, con bas$ en la informacion que emita el Servicio
> Geologico Colombiano y demas autoridades competentes" y, por el otro, que las
> actividades misionales, tecnicas, operativas y administrativas se pueden reanudar
> cuando "cesen los factores de riesgo ile desastre natural que motivan esta
> decision ",

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> Que el Servicio Geologico Colombiano, a traves del Boletm Extraordinario del 27
> de junio de 2023, declara que "Desoues de 89 dfas en nivel de actividad Narania,
> el volcan ha retornado a un rUve! de menor inestabilidad v la orobabilidad de
> ocurrencia de una eruodon de maanitud considerable en terminos de dfas o
> semanas ha disminuido. lo cual permite $ambiar su nivel a Amarillo.


## Updated entry: hours_status.weather_emergency_closures

- Reason: La facultad de cerrar por seguridad sí está; la lista de lluvias, granizo y derrumbes no.
- Changed fields: answer, label, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> podrá limitar la entrada o cerrar alguno de los atractivos turísticos si lo

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> podrá restringir el ingreso o cerrar los

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt`

> www.parquesnacionales.gov.co


## Updated entry: hours_status.weekday_opening

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> es indispensable reservar con al menos un día de anticipación

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> la reserva no es obligatoria


## Updated entry: hours_status.weekend_and_holiday_opening

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> es indispensable reservar con al menos un día de anticipación

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> la reserva no es obligatoria

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> www.reservasnevados.com


## Updated entry: hours_status.why_conservation_closures_exist

- Reason: Keep the previous label; the review marked the wording change as stylistic or named that label.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.html`

> article:modified_time" content="2026-10-31T00:11:49+00:00"

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt`

> el área protegida tiene establecidos algunos cierres como una estrategia ambiental para liberar de carga estos lugares naturales y hacer trabajos de monitoreo.
