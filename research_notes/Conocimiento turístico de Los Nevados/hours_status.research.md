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
