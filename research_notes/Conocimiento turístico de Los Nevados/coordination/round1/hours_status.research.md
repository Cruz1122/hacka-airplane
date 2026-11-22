# Registro de Investigación: Espacio `hours_status` (Horarios y Estado del Parque)

**Investigador / Subagente:** Subagente de Investigación `hours_status` (Orden 6)  
**Proyecto:** Asistente Turístico Offline para el Parque Nacional Natural Los Nevados, Colombia  
**Fecha de corte:** 2026-11-21  
**Archivo de datos producido:** `/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/hours_status.json`  
**Esquema de validación:** `/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json`  

---

## 1. Fuentes Consultadas y Fechas

Todas las consultas se realizaron con fecha de referencia **2026-11-21**. Se priorizaron fuentes primarias de autoridades ambientales, territoriales y geológicas oficiales de Colombia:

1. **Parques Nacionales Naturales de Colombia (PNNC)**
   - **URL:** `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/`
   - **Fecha de publicación / actualización:** 2026
   - **Contenido consultado:** Ficha técnica oficial del PNN Los Nevados, estado de apertura ("Abierto"), horarios oficiales por sector, cronograma reglamentario de descansos ambientales por conservación (Resolución 207 de 2023), política de reservas previas obligatorias y canales de atención ciudadana.
2. **Secretaría de Tránsito y Transporte del Tolima - Gobernación del Tolima**
   - **Acto administrativo:** **Resolución No. 1815 del 24 de julio de 2026**
   - **Vigencia:** 25 de julio de 2026 al 20 de julio de 2027
   - **Contenido consultado:** Reglamentación del Pico y Placa Ambiental en el corredor vial Murillo–La Esperanza / Cerro Gualí (acceso norte hacia Brisas), días (sábados, domingos y festivos), horario de restricción (5:00 a. m. a 4:00 p. m.), esquemas de rotación de placas y restricciones permanentes de carga pesada y buses mayores a 19 pasajeros.
3. **Servicio Geológico Colombiano (SGC) - Observatorio Vulcanológico y Sismológico de Manizales**
   - **URL:** `https://www.sgc.gov.co/`
   - **Contenido consultado:** Criterios técnicos de monitoreo de actividad volcánica del Nevado del Ruiz (Kumanday), niveles de alerta volcánica (Verde, Amarilla, Naranja, Roja) y su articulación con los protocolos de cierre preventivo de PNNC (Resolución 068 de 2023).
4. **Concesión Unión Temporal Operación Nevados (UTON)**
   - **URL:** `https://www.operacionnevados.co/`
   - **Contenido consultado:** Operador oficial del sector Brisas–Kumanday; horarios de atención al público en oficinas de Manizales (Carrera 26A #68-44 Palermo y Calle 70 #27-70: lunes a viernes 8:00 a 12:00 m. y 14:00 a 17:00), canales telefónicos (321 506 6031 / 322 360 3637) y coordinación de transporte e inducción en Brisas.
5. **IDEAM e Instituto Nacional de Vías (Invías)**
   - **URL:** `http://www.ideam.gov.co/` y servicio telefónico `#767`
   - **Contenido consultado:** Régimen bimodal de precipitación en la cordillera Central, historial de suspensiones por alertas hidrometeorológicas (crecientes súbitas y deslizamientos en la vía Manizales–Murillo y accesos destapados a Potosí).

---

## 2. Evidencias Factuales, Citas y Soporte Entrada por Entrada

A continuación se detalla la correspondencia entre las citas oficiales y las 40 entradas creadas, separando con rigor hechos comprobados, inferencias operativas, adaptaciones editoriales de la aplicación y vacíos no verificados:

### Hechos comprobados de fuentes oficiales (Facts)
- **Sector Brisas–Kumanday:** Abierto los 365 días del año. Horario de taquilla e ingreso: 8:00 a. m. a 2:00 p. m. Última charla obligatoria de inducción: 1:30 p. m. Evacuación y cierre del circuito carreteable: 3:30 p. m. a 4:00 p. m. (*Fuente: PNNC Ficha Los Nevados 2026*). Soportan las entradas `hours_status.brisas_hours`, `hours_status.brisas_induction_talk_schedule`, `hours_status.brisas_exit_time`, `hours_status.brisas_open_days`.
- **Sector Cisne–Poleka Kasue:** Horario de atención y registro en Cabaña Potosí y Alto de Santa Bárbara: 7:30 a. m. a 10:00 a. m. Sendero Laguna Verde: horario de 8:00 a. m. a 2:00 p. m. Sendero Conejeras (ascenso a cumbre Santa Isabel): el registro ante guardaparques se hace obligatoriamente el día anterior (*Fuente: PNNC Ficha Los Nevados 2026*). Soportan `hours_status.cisne_potan_hours`, `hours_status.laguna_verde_trail_hours`, `hours_status.santa_isabel_conejeras_prior_day_checkin`.
- **Sector Laguna del Otún:** Horario de atención y control en Cabaña Potosí: 7:00 a. m. a 12:00 m. (*Fuente: PNNC Ficha Los Nevados 2026*). Soporta `hours_status.otun_sector_hours`.
- **Sector Quindío–Dulima (Nevado del Tolima):** Punto de atención Valle del Cocora (Salento): 6:00 a. m. a 10:00 a. m. Puntos de atención Juntas (Ibagué) y Anzoátegui: 6:00 a. m. a 11:00 a. m. con reserva previa obligatoria (*Fuente: PNNC Ficha Los Nevados 2026*). Soportan `hours_status.quindio_dulima_cocora_hours`, `hours_status.quindio_dulima_juntas_anzoategui_hours`.
- **Cierres por conservación (Descansos ambientales):** Tres pausas anuales de 5 días de duración (Resolución 207 de 2023 de PNNC):
  1. Lunes inmediatamente posterior a Semana Santa hasta el viernes de esa semana.
  2. Cuarto lunes de septiembre hasta el viernes de esa semana.
  3. Cuarto lunes de noviembre hasta el viernes de esa semana.
  Soportan `hours_status.conservation_closures`, `hours_status.why_conservation_closures_exist`, `hours_status.conservation_closures_dates_schedule`, `hours_status.open_sectors_during_conservation_closures`.
- **Pico y Placa Ambiental Tolima:** Resolución 1815 del 24 de julio de 2026 de la Secretaría de Tránsito del Tolima en el corredor Murillo–La Esperanza. Horario: 5:00 a. m. a 4:00 p. m. los sábados, domingos y festivos. Prohibición 24/7 a vehículos de carga ≥ 3,4 ton y transporte público > 19 pasajeros (*Fuente: Gobernación del Tolima*). Soporta `hours_status.pico_y_placa_hours_murillo`.
- **Canales y horarios de oficina:** PNNC atiende de lunes a viernes de 8:00 a. m. a 4:30 p. m. jornada continua (+57 (601) 353 2400 / +57 3229471031). Concesión UTON en Manizales atiende de lunes a viernes de 8:00 a 12:00 m. y 14:00 a 17:00 (*Fuentes: PNNC y UTON*). Soportan `hours_status.pnn_administrative_office_hours`, `hours_status.uton_concession_office_hours`, `hours_status.official_channels_to_check_status`.
- **Plazos de reserva:** Brisas mínimo 1 día antes en reservasnevados.com; Cisne y Otún mínimo 3 días hábiles; Quindío–Dulima mínimo 5 días hábiles (*Fuente: PNNC*). Soporta `hours_status.booking_time_limits_before_visit`.

### Inferencias operativas basadas en evidencia técnica (Inferences)
- **Horas de salida a cumbre (Ataque a cumbre):** Para Santa Isabel (`hours_status.santa_isabel_summit_start_hour`), la salida entre 4:00 a. m. y 5:30 a. m. se infiere de la necesidad técnica de alcanzar el borde glaciar con nieve congelada y emprender el descenso antes de las 11:00 a. m. Para el Nevado del Tolima (`hours_status.tolima_summit_push_hours`), las salidas entre 1:00 a. m. y 3:00 a. m. desde campamentos altos responden a la exigencia de completar el recorrido de cumbre antes de las tormentas habituales de mediodía.
- **Hora límite de llegada a campamentos (`hours_status.camping_arrival_cutoff`):** Se establece entre las 4:30 p. m. y 5:00 p. m. para evitar el riesgo de hipotermia y caídas durante el montaje nocturno de carpas en temperaturas bajo cero.
- **Caminata desde El Cedral (`hours_status.cedral_otun_hiking_schedule`):** Requiere iniciar entre 5:00 a. m. y 7:00 a. m. dado el trayecto de 18 km y 7 a 9 horas de ascenso continuo.

### Texto editorial de la aplicación y advertencias offline (Editorial App Text)
- Se redactó en segunda persona del singular ("tú"), en tono empático, riguroso y conciso.
- **Limitación offline:** Se incluyó explícitamente en `hours_status.park_open_today` y `hours_status.offline_status_verification_advice` que el asistente móvil opera sin internet y no puede verificar en tiempo real si el parque cerró hoy por una contingencia climática o volcánica imprevista; se instruye al turista a verificar siempre en los canales oficiales antes de perder la señal urbana.
- No se prometieron funciones técnicas imposibles (GPS offline activo, sincronización automática de estado o reportes satelitales).

---

## 3. Vacíos de Información Oficial (Gaps)

1. **Aforos numéricos exactos por sendero para 2026:** Parques Nacionales señala que los cupos diarios son limitados y están regulados por la capacidad de carga del plan de manejo, pero no publica en la cartilla turística general una cifra estática fija para todos los senderos, ya que esta varía según conceptos biológicos y monitoreo ambiental estacional. Se omitieron números inventados y se enfatizó el deber de reservar con antelación.
2. **Horarios de portones en predios privados de acceso secundario:** Algunos accesos por caminos de servidumbre en inmediaciones de Villamaría o Santa Rosa tienen broches o portones comunitarios cuyos horarios de apertura matutina dependen de los propietarios locales y no están formalmente estandarizados por Parques Nacionales.
3. **Fechas exactas de contingencias imprevistas futuras:** No es posible conocer con antelación las fechas de cierres por erupción o deslizamientos; se documentó el protocolo reglamentario (Resolución 068) y el nivel de alerta que los desencadena.

---

## 4. Conflictos entre Fuentes y su Resolución

- **Conflicto 1: Alcance territorial de los cierres por conservación.**
  - *Discrepancia:* Algunos reportes de prensa y páginas de agencias afirmaban que durante los tres descansos ambientales anuales "todo el Parque Los Nevados cierra sus puertas sin excepción".
  - *Resolución:* Revisando las circulares operativas de PNNC y la información de la concesión UTON, se constató que la prohibición total de ingreso aplica a las rutas de senderismo pedestre y alta montaña (Cisne, Santa Isabel, Otún y Tolima), mientras que el circuito vehicular Brisas–Valle de las Tumbas suele permanecer habilitado bajo medidas de control para visitantes de pasadía. Se reflejó esta distinción en `hours_status.open_sectors_during_conservation_closures` advirtiendo siempre validar la circular específica de cada periodo.
- **Conflicto 2: Horario de apertura del punto de registro de Potosí.**
  - *Discrepancia:* Guías y blogs no oficiales indicaban indistintamente horarios de apertura a las 6:00 a. m. u 8:00 a. m.
  - *Resolución:* Se adoptó la reglamentación oficial vigente de PNNC: 7:30 a. m. a 10:00 a. m. para el sector Cisne–Poleka Kasue y 7:00 a. m. a 12:00 m. para el sector Otún.
- **Conflicto 3: Horario del Pico y Placa Ambiental en la vía Murillo–La Esperanza.**
  - *Discrepancia:* Documentos preliminares y decretos municipales de 2024 manejaban ventanas horarias de 6:00 a. m. a 6:00 p. m.
  - *Resolución:* Se aplicó con estricta prioridad la norma más reciente y de mayor jerarquía vial: la **Resolución 1815 del 24 de julio de 2026** de la Secretaría de Tránsito del Tolima, que fija taxativamente la restricción de 5:00 a. m. a 4:00 p. m. los sábados, domingos y festivos.

---

## 5. Temas Descartados y Motivo de Exclusión

Conforme a las reglas de partición de espacios del contrato y la resolución de empates por menor número de orden (`order`), se descartaron los siguientes temas para no invadir otras secciones:

- **Tarifas detalladas de boletas, cobros de vehículos y exoneraciones:** Excluidos porque pertenecen a `booking_fees` (orden 5).
- **Rutas de acceso detalladas, vías terrestres y transporte público:** Excluidos porque corresponden a `access` (orden 4).
- **Valores científicos de sismicidad, gases SO2 y ceniza volcánica:** Excluidos porque pertenecen a `weather_volcano` (orden 3).
- **Recomendaciones de vestimenta en capas y calzado de trekking:** Excluidos porque pertenecen a `preparation` (orden 7).
- **Reglamento sobre prohibición de drones, mascotas y fogatas:** Excluidos porque pertenecen a `rules` (orden 9).

---

## 6. Mapeo de la Semilla Original (`conocimiento.json`)

Los 3 temas asignados a este espacio (índices 4, 6 y 41) fueron totalmente absorbidos, preservando su contenido verificado y expandiendo sus ejemplos y variantes:

| Índice Semilla | Etiqueta Original en `conocimiento.json` | ID Final en `hours_status.json` | Etiqueta Final | Tratamiento y Mejoras Realizadas |
|---|---|---|---|---|
| **4** | `los horarios de ingreso` | `hours_status.general_opening_schedule` | `horarios generales de ingreso al parque` | Se conservó el horario de Brisas (8:00 a. m. a 2:00 p. m.) y charla (1:30 p. m.), y se amplió con los horarios verificados de Cisne, Otún y Cocora. Se incluyeron los 7 ejemplos originales y se sumaron 6 más (13 en total). |
| **6** | `si el parque está abierto` | `hours_status.park_open_today` | `verificar si el parque está abierto hoy` | Se conservó la advertencia de funcionamiento sin conexión y se complementó con las causas de cierre volcánico/climático y canales de confirmación. Se integraron los 7 ejemplos originales y se expandió a 13 ejemplos. |
| **41** | `los cierres por conservación` | `hours_status.conservation_closures` | `cierres programados por conservación y descanso` | Se enriqueció la explicación general de los 3 cierres de 5 días al año (post-Semana Santa, septiembre, noviembre) reglamentados por la Resolución 207 de 2023. Se incluyeron los 4 ejemplos originales y se expandió a 13 ejemplos. |

---

## 7. Métricas y Conteos Finales

- **Entradas generadas:** 40 entradas (meta del proyecto: 40).
- **Ejemplos totales:** 483 ejemplos (promedio: 12,075 ejemplos por entrada; mínimo 12, máximo 13).
- **Variedad de ejemplos:** Mezcla balanceada de consultas cortas, preguntas completas, expresiones coloquiales colombianas ("a qué horas abren", "hasta qué hora dejan entrar", "toca madrugar mucho", "cuándo viaja más gente"), variantes sin tilde/ortografía coloquial ("horarios de atencion", "a que hora abren", "esta abierto hoy") y 1–2 preguntas naturales en inglés por entrada.
- **Unicidad de ejemplos:** 483 / 483 ejemplos únicos en el espacio; 0 duplicados locales o colisiones intertemáticas.
- **Negativos difíciles (`hard_negatives`):** 120 preguntas (exactamente 3 por entrada, cumpliendo el rango de 2 a 4).
- **Etiquetas (`label`):** 40 / 40 etiquetas formuladas con una longitud estricta de 3 a 8 palabras (media: 6,4 palabras).
- **Respuestas (`answer.short`):** 1 a 3 frases concisas dirigidas de "tú", amables, con acción concreta y fuentes oficiales fechadas al 2026-11-21.
- **Relaciones (`related`):** Todas las referencias apuntan exclusivamente a IDs válidos y existentes dentro del mismo espacio `hours_status`.
- **Destacados (`featured`):** 5 entradas clave que cubren los aspectos más consultados: horario general, apertura hoy, cierres por conservación, horario de Brisas y Pico y Placa Ambiental.
- **Validación JSON Schema:** Validación automatizada superada al 100 % contra `knowledge-section.schema.json` mediante `jsonschema` en Python.
