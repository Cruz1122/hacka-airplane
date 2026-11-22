# Servicios (`services`, orden 10) — log de investigación

Fecha de corte: 2026-11-21. Perfil de recuperación: `lookup`. Sección: `data/knowledge/sections/services.json`.
Evidencia descargada: `research_notes/Conocimiento turístico de Los Nevados/services/evidence/`. Validador: `services/evidence/validate_services.py`.

Resultado: **27 entradas** (meta 40), **329 ejemplos** (mínimo 12 por entrada), **sin semilla asignada** (`[]`). La meta no se alcanzó porque las fuentes oficiales no respaldan más intenciones distintas de servicios. No añadí entradas con relleno.

---

## 1. Fuentes consultadas

### 1.1 URLs realmente leídas (HTTP y fecha de consulta)

| # | URL | Consulta | Resultado | Fecha de publicación visible |
|---|---|---|---|---|
| 1 | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | 2026-11-21 | HTTP 200, 219.898 bytes. Leída completa (`evidence/pnn_nevados.html`, `.txt`) | No visible. La página cita la Resolución 1815 del 24-07-2026 y tarifas 2026, así que es posterior a julio de 2026. |
| 2 | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx | 2026-11-21 | HTTP 200, 5.409.501 bytes, docx. Texto extraído (`evidence/pnn_informe_necesidades_2024.docx`, `.txt`) | No visible en el texto. Ruta de carga 2024/12. Cita Res. 273 (24-07-2024) y Res. 207 (04-08-2023). |
| 3 | https://www.operacionnevados.co/ | 2026-11-21 | HTTP 200. Solo página de inicio (`evidence/uton_3b654e8f.html`, `.txt`). Sin lista de servicios ni teléfono. Dirección: Cl 70 # 27-70 Palermo, Manizales. | No visible |
| 4 | https://ecoturismonevados.com.co/uton-union-temporal-operador-nevados/ | 2026-11-21 | **HTTP 404**. Enlace citado por la página de PNN; no es fuente. | — |
| 5 | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIÓN-PNN-LOS-NEVADOS-2026-V2.pdf | 2026-11-21 | Visto en búsqueda; descarga **fallida** (HTTP 404 en la URL codificada). No leído. | — |

Búsquedas web (WebSearch, modo standard), solo como pistas, no como fuente de datos:
- "Parque Los Nevados centro de visitantes Brisas servicios baños restaurante"
- "Parques Nacionales Los Nevados señal celular hospedaje alojamiento Murillo Santa Rosa de Cabal"

URLs que aparecieron en esas búsquedas y **no leí**: colombia.travel (varias), El Tiempo (artículo sin fecha sobre señal en La Cabaña, Murillo; no es el parque), Travelocity/Hotels.com/Expedia (agregadores), Wikipedia (no usada para cifras), Semana, El Espectador. No las uso como respaldo.

Fuente secundaria y no oficial: ninguna cifra de servicios proviene de agregadores.

### 1.2 Evidencia por entrada (hecho → fuente)

Todas las citas se verificaron leyendo el texto extraído. Las citas son textuales o cerca de textuales.

| Entrada | Hecho verificado | Fuente |
|---|---|---|
| `brisas_visitor_center` | "El trayecto inicia en el centro de inducción Brisas, a 4100 metros de altitud aproximadamente" | PNN ficha, sección Atractivos |
| `brisas_visitor_center` | Brisas: "Taquilla, Centro de Inducción y Cabaña"; estado "En general se encuentra en buen estado" | Informe 2024, tabla de infraestructura (p. "2. Brisas") |
| `brisas_visitor_center` | "la última charla de inducción obligatoria" en Brisas | PNN ficha, sección Horarios |
| `north_food` | "los sectores que prestan los servicios de alimentos, baños y enfermería son las cabañas de Brisas, Arenales; además para el caso del centro de visitantes el Cisne, cuenta con alojamiento y alimentación" | Informe 2024, sección "Servicios prestados en cada Área protegida" |
| `north_food` | "Aliméntate bien y come snacks energéticos"; "Ten una buena hidratación antes, durante y después" | PNN ficha, Recomendaciones |
| `toilets` | Arenales: "Un comedor y dos baterías de baños para visitantes" | Informe 2024, cabaña Arenales |
| `first_aid_points` | Arenales: "Un punto de atención de primeros auxilios" (existente) | Informe 2024, cabaña Arenales |
| `first_aid_points` | Puntos de atención identificados como **necesidades**: Brisas, Potosí, Laguna del Otún, El Cisne, El Cedral, Valle de Cocora, Juntas, Anzoátegui, municipios | Informe 2024, "Necesidades de asistencia" (no confirma operación) |
| `cisne_visitor_center` | "El acceso se realiza a través del centro de visitantes El Cisne, ubicado a 4100 metros de altitud aproximadamente"; "Alojamiento de visitantes (32 personas)" | PNN ficha; Informe 2024 (cita Plan de Ordenamiento 2017-2022) |
| `potosi_cabin` | "Accede a este sector por la cabaña Potosí, ubicada a 3920 metros de altitud aproximadamente" | PNN ficha, Laguna del Otún |
| `potosi_cabin` | Campo Alegre: "Hospedaje y alimentación en el refugio Potosí"; Potosí: "Actualmente mantenimiento correctivo y preventivo" | Informe 2024 |
| `otun_lodging` | "estadía en casas tradicionales de los habitantes históricos de la vereda El Bosque" | PNN ficha, Laguna del Otún |
| `otun_lodging` | Vereda El Bosque: "Hospedaje y alimentación. Porteo de maletas (equipaje)" | Informe 2024, rutas Otún |
| `tolima_lodging` | Termal Cañón, predio La Playa y La Primavera: "Hospedaje y alimentación"; "Porteo de maletas" | Informe 2024, ruta Juntas |
| `brisas_lodging` | UTON gestiona "reservas, ingreso, guianza, transporte, alojamiento y tienda" en el sector Brisas | PNN ficha, sección Atractivos y Contacto UTON |
| `porter_luggage` | "Servicio de Porteo de Maletas (equipaje)" en Los Chilcos–Arenales cumbre; porteo también en ruta Juntas y en El Bosque | Informe 2024 |
| `uton_services` | Contrato UTON: "taquilla, seguro obligatorio de montaña, guianza y suministro de alimentos en el sector norte hasta el valle de las Tumbas" | Informe 2024, sección "Servicios prestados" |
| `uton_offices` | "Carrera 26A #68-44, barrio Palermo"; "Calle 70 #27-70"; "lunes a viernes, 8:00 a. m. a 12:00 m. y 2:00 p. m. a 5:00 p. m."; teléfonos 321 506 6031 – 322 360 3637 | PNN ficha, Contacto UTON. Dirección corroborada por operacionnevados.co ("Cl 70 # 27-70 - Palermo") |
| `pnn_customer_service` | "Teléfono Conmutador: +57 (601) 353 2400 Ext. 3011 - 3012"; "Línea gratuita nacional desde un fijo: 018000129722"; "Lunes a viernes de 8:00 a.m. a 4:30 p.m." | PNN ficha, pie de página |
| `research_permits` | Seis tipos de permiso de investigación; "tomas audiovisuales o fotografías con fines comerciales, eventos... debes solicitar la autorización correspondiente" | PNN ficha, Conservación/Investigación y Actividades |
| `guide_radios` | Guías: "los radios con la frecuencia requerida", "equipo médico de respuesta" | PNN ficha, Guías y operadores |
| `phone_signal` | **Sin dato oficial de cobertura.** Solo se usa la obligación de radios de los guías. | — (gap) |
| `charging_power` | **Sin dato oficial.** | — (gap) |
| `accessibility` | Quindío–Dulima: "el terreno es más exigente"; "exige al visitante una preparación previa" | PNN ficha, Atractivos |
| `drinking_water` | **Sin dato oficial de agua potable.** Solo hidratación recomendada. | PNN ficha, Recomendaciones (gap + recomendación) |
| `shop_ecotienda` | Tienda UTON en Brisas (PNN); "Contenedor como punto de atención de visitantes y eco-tienda" en Valle de las Tumbas, "En buenas condiciones" | PNN ficha; Informe 2024 |
| `refugio_cabin` | "Cabaña El Refugio no habilitada. (se debe dar de baja)"; estado "En malas condiciones" | Informe 2024 |
| `camp_showers` | Arenales: "Una batería de baños para hombres y mujeres y duchas, para campistas"; "Un comedor y cocina para los campistas"; "Zona de camping no se encuentra habilitada debido a la actividad volcánica" | Informe 2024 |
| `official_sites` | Sitios: parquesnacionales.gov.co; operacionnevados.co (leído). reservasnevados.com aparece en PNN como enlace de reserva; **no lo leí**. | PNN ficha; UTON home |
| `registered_providers` | "Registro para Prestadores de Servicios Asociados al Ecoturismo (REPSE)"; "No todos los prestadores están autorizados para guiarte en todos los atractivos" | PNN ficha, Guías y operadores |
| `cabin_status_2024` | Brisas y Arenales "buen estado"; La Cueva y Laguna del Otún "buenas condiciones"; Potosí "mantenimiento correctivo y preventivo"; El Refugio "malas condiciones" | Informe 2024, tabla de infraestructura |
| `charla_induccion` | Charla de inducción obligatoria en Brisas; el informe 2024 la lista también en rutas del Cisne y del Otún | PNN ficha (Horarios); Informe 2024 |
| `quindio_dulima` | "Quindío–Dulima ... el terreno es más exigente, por lo que la actividad principal es el montañismo"; puntos de atención planeados en Valle de Cocora, Juntas, Anzoátegui; zonas de camping | PNN ficha; Informe 2024 |

### 1.3 Clasificación del contenido: hecho, inferencia, texto editorial, vacío

**Hechos (con fuente oficial dentro de la entrada):** todas las entradas excepto las marcadas abajo.

**Inferencias (no dichas literalmente por la fuente):**
- `north_food`: "lleva snacks y agua" combina "come snacks energéticos" (PNN) con la hidratación recomendada. El agua es inferencia.
- `drinking_water`: "lleva tu propia agua" es inferencia desde la hidratación recomendada.
- `phone_signal`: "viaja con un guía registrado, que debe llevar radio" es inferencia desde la obligación de radios (PNN). La recomendación de no depender del celular es inferencia de seguridad.
- `charging_power`: "lleva batería portátil" es recomendación editorial sin fuente oficial.
- `first_aid_points`: que los puntos del Informe 2024 aparecen como *necesidades*, no como servicios operando. La entrada lo dice así.
- `brisas_lodging`: el conflicto de fuentes se resuelve sin afirmar que haya camas en Brisas.

**Texto editorial de la app (no es afirmación de PNN):**
- Todas las respuestas (`answer.short`, `variants`) son reescrituras editoriales de las fuentes listadas. Ni PNN ni UTON las avalan.
- `refugio_cabin` remite a "la sección de salud y seguridad de la app", que es una referencia interna, no una fuente.
- `official_sites` dirige a operacionnevados.co, sitio de la concesión, no del parque.

**Vacíos no verificados (no afirmados en la respuesta):**
- Cobertura de celular o internet dentro del parque (`phone_signal`).
- Puntos de carga o electricidad (`charging_power`).
- Accesibilidad física: rampas, baños accesibles, sillas de ruedas (`accessibility`).
- Agua potable en puntos de atención (`drinking_water`).
- Baños fuera del norte: Otún, El Cisne y Potosí no tienen dato de baños (`toilets` solo cubre Brisas y Arenales).
- Precios de alojamiento o comida en cualquier punto (van a `booking_fees`).
- Estado actual (2026) de cabañas, camping de Arenales, El Refugio y Potosí (`cabin_status_2024` es una foto de 2024).

---

## 2. Vacíos

Preguntas sin respuesta de fuente oficial, con la razón:

1. **Señal celular y datos.** No hay fuente de PNN. El único reportaje encontrado (El Tiempo, sin fecha visible) trata de una vereda de Murillo y no del parque. Afirmar cobertura sin fuente violaría la regla de evidencia.
2. **Carga de batería y electricidad.** Ninguna fuente oficial. Inferir enchufes sería inventar.
3. **Accesibilidad para movilidad reducida.** Ninguna fuente oficial.
4. **Agua potable.** Ninguna fuente oficial de puntos de agua.
5. **Baños en Otún, Cisne y Potosí.** El Informe 2024 solo menciona baños en Brisas y Arenales.
6. **Tienda en otros puntos.** Solo Brisas (UTON) y Valle de las Tumbas (eco-tienda, 2024).
7. **Horarios de servicios** (comida, tienda, baños). Solo hay horarios de oficinas (UTON, PNN) y de cabañas de atención, que pertenecen a `hours_status`.
8. **Estado actual de servicios 2026.** El Informe 2024 es la fuente más reciente que pude leer. El PDF 2026 de PNN no se pudo descargar.
9. **Teléfono de la UTON.** Solo aparece en la página de PNN. La página de UTON no lo muestra. Sin segunda fuente.
10. **Alojamiento comercial cerca del parque** (hoteles, termales, glamping). Solo aparecen en agregadores; no los incluí.

---

## 3. Conflictos y resolución

| Conflicto | Fuentes | Resolución |
|---|---|---|
| **Alojamiento y tienda en Brisas.** PNN dice que UTON gestiona alojamiento y tienda en Brisas. El Informe 2024 solo menciona alimentos, baños y enfermería allí, y el contrato UTON no incluye alojamiento. | PNN ficha (2026) vs Informe 2024 | Ambos se citan. `brisas_lodging` dice que no hay que contar con cama sin confirmar. `uton_services` señala que los documentos no listan lo mismo. Preferí la fuente más reciente (PNN) pero sin afirmar disponibilidad. |
| **Cierre total del parque en 2023.** Un resumen de búsqueda afirmaba que un documento oficial de 2024 citaba un cierre total y que no había confirmación de vigencia. | Búsqueda (no fuente) vs Informe 2024 | **Resuelto con el propio Informe 2024:** la Res. 068 del 31-03-2023 ordenó el cierre total; la **Res. 207 del 04-08-2023 ordenó la apertura** y reglamentó el ecoturismo. No hay fuente de 2026 que diga que el cierre esté vigente. No lo afirmo en servicios. |
| **Cierres por conservación 2026.** La página de PNN da una regla (tres cierres de cinco días: semana santa, cuarto lunes de septiembre, cuarto lunes de noviembre). Por esa regla, el cierre de noviembre sería del 23 al 27 de noviembre de 2026. | PNN ficha (regla) | **Inferencia de fecha, no aviso oficial.** No lo afirmo aquí. Lo transmito a `hours_status` (ver 4.3). |
| **Pico y placa ambiental.** PNN cita la Res. 1815 del 24-07-2026 (Tránsito del Tolima), que aplica en fines de semana y puentes festivos de 5:00 a. m. a 4:00 p. m. | PNN ficha | Es tema de acceso y horario. No lo incluyo en servicios. Lo transmito a `access`/`hours_status`. |
| **Estado de cabañas.** El Informe 2024 da estados que pueden haber cambiado. | Informe 2024 | `cabin_status_2024` declara que es un dato de 2024 y pide confirmar. |
| **Puntos de primeros auxilios.** El Informe 2024 lista "sitios de atención" que son necesidades; solo Arenales tiene primeros auxilios descritos como existentes. | Informe 2024 | `first_aid_points` diferencia existentes (Arenales) de necesidades (otros). |
| **Altitud del Cisne y de Brisas.** PNN dice "4100 metros de altitud aproximadamente" para ambos. | PNN ficha | No es conflicto real, pero es aproximada. La respuesta dice "unos" y no se usa como dato exacto. |
| **Datos del plan 2017-2022 dentro del informe 2024.** La capacidad de 32 personas y algunos servicios comunitarios vienen del plan 2017-2022, citado en el Informe 2024. | Informe 2024 | Se indica la antigüedad en las respuestas (`tolima_lodging`, `cisne_visitor_center`). |

---

## 4. Temas descartados

Descartados por no ser de servicios o por pertenecer a otra sección:

- **Parqueadero y transporte de la concesión:** `access` (incluye parqueo y transporte).
- **Reservas, seguro, precios, guía obligatorio y cupos:** `booking_fees`.
- **Horarios de puntos de atención (Potosí 7–12, Valle de Cocora 6–10, Juntas y Anzoátegui 6–11), horario de la última charla (1:30 p. m.) y cierres:** `hours_status`.
- **Ambulancia y puntos de atención municipales (Santa Isabel, Murillo):** `health_safety`. El informe los trata como necesidades de emergencia.
- **Refugios de emergencia y cabaña El Refugio como albergue en emergencia:** `health_safety` para el uso de emergencia. Aquí solo se responde que El Refugio no está habilitado.
- **Basureros y "espacio para basuras" (Arenales):** `rules`, por residuos.
- **Alojamientos comerciales de agregadores** (Hotel Termales del Ruiz, Termales Santa Rosa de Cabal, Finca Hotel Barilloche, Termales del Otoño, Cabañas La Herradura, Glamping Lumbre, Hotel Areca, Hotel El Mirador del Cocora): no son fuente oficial y no los respaldo.
- **Artículo de El Tiempo sobre señal en La Cabaña (Murillo):** no es el parque y no tiene fecha. Solo sirvió de contexto de vacío.
- **Enlace ecoturismonevados.com.co:** 404.
- **PDF PNN 2026 de publicación:** no descargable; no leído.
- **Servicios de guía de alta montaña, tours y bicicletas (Santa Rosa Bikes en la lista de la concesión):** sin fuente de servicio; `registered_providers` cubre cómo verificar prestadores.
- **Perros y mascotas, fotografía no comercial, drones:** `rules` y `activities`.

### 4.1 Mapeo de semilla

- **Índices originales asignados a `services`:** `[]`. Ninguno de los 44 temas de `conocimiento.json` cae en servicios.
- Seeds vecinos que no tomé: "el seguro de accidentes" y "si necesitas guía" (`booking_fees`); "cómo llegar desde Manizales" y "dónde queda la entrada Brisas" (`access`); "el sector Santa Isabel" y "el sector Nevado del Tolima" (`activities`).
- Ninguna etiqueta mía coincide con una etiqueta semilla.

### 4.2 Conteos finales y validación

| Métrica | Valor |
|---|---|
| Entradas | 27 (meta 40; no alcanzada por falta de evidencia y de intenciones distintas) |
| Ejemplos totales | 329; mínimo 12 por entrada; máximo 13 |
| Ejemplos en inglés | 1–2 por entrada |
| Hard negatives | 3 por entrada (rango 2–4 cumplido) |
| Featured | 5 |
| Clarification bank | 5 preguntas |
| Slot questions | `sector` (única `entity_filter`) |
| Entradas `kind` | 23 `fact`, 4 `procedure` |
| Labels | 3–8 palabras (todas verificadas) |
| Schema | **OK** con `jsonschema` contra `knowledge-section.schema.json` |
| Duplicados internos y cruzados | 0 exactos contra las 5 secciones ya publicadas |
| Casi duplicados (ratio ≥ 0,9) | 0 |
| Referencias `related` y `featured` | Todas resuelven en `services` |
| Cifras con `last_verified` | Todas las entradas tienen `last_verified: 2026-11-21` |
| `valid_until` | `null` en todas. Ninguna fuente oficial da fecha de caducidad. |

Advertencias del validador (no errores): `uton_offices` y `pnn_customer_service` tienen más de 3 frases aparentes porque el conteo cuenta las abreviaturas "a. m." y "p. m.". Su texto tiene 3 frases.

**Hard negatives pendientes de otras secciones:** 7 textos son ejemplos de la semilla (`conocimiento.json`), que aún no están publicados en las secciones de access, activities y booking_fees: "dónde queda la entrada Brisas", "dónde es el valle", "cuál es el acceso por Salento", "puedo tomar fotos", "cómo contrato un operador", "requisitos para entrar", "dónde compro boletas". Verifiqué que existen literalmente en la semilla. Quedan bajo revisión del coordinador.

### 4.3 Notas de coordinación para otras secciones (no las edité)

1. **`hours_status`:** La regla de cierres de PNN, cuarto lunes de noviembre, da del 23 al 27 de noviembre de 2026. Es una inferencia. Hay que verificar si hay aviso oficial antes de publicar esa fecha.
2. **`access` / `hours_status`:** Pico y placa ambiental, Res. 1815 de 2026, fines de semana y festivos de 5:00 a. m. a 4:00 p. m. en el acceso norte.
3. **`health_safety`:** La palabra "refugio" aparece como ejemplo en `services.refugio_cabin` (cabaña El Refugio no habilitada). Puede chocar con los refugios de emergencia. La respuesta remite a salud y seguridad.
4. **`booking_fees`:** REPSE, cupos y guía obligatorio están en `services.registered_providers`. Hay que revisar que no se repitan respuestas de precios.
5. **Teléfonos:** `services.uton_offices` y `services.pnn_customer_service` usan teléfonos del sitio de PNN. Conviene que el coordinador los contraste con los de emergencia de `health_safety`.
6. **Seguimiento de fuentes:** si el PDF 2026 de PNN o la página de reservas se pueden leer, podrían confirmar servicios actuales y reemplazar el Informe 2024.

### 4.4 Límites declarados

- No hay fecha de publicación de la página principal de PNN. Todas las fechas `last_verified` son fecha de consulta, no de publicación.
- El Informe 2024 es la fuente más reciente de servicios por sector que pude leer. Sus estados de cabañas y puntos de atención son de 2024.
- No pude leer la sección de servicios de UTON porque su sitio no tiene texto de servicios en la página de inicio, y el enlace de ecoturismonevados.com.co responde 404.
- No marqué ninguna entrada como "abierta" ni con "alerta activa". Todas remiten a confirmar con la fuente oficial antes de viajar.
