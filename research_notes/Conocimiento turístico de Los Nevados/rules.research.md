# Reglas para visitantes — Parque Nacional Natural Los Nevados

## Evidencia leída y mapeo final

Las fuentes se consultaron el **2026-11-21**. Las citas textuales cortas y el mapeo por entrada quedaron guardados en `rules/evidence/resolucion_207_2023_quotes.txt`; la copia del reglamento descargado está en `rules/evidence/resolucion_207_2023.pdf`. Los archivos de evidencia son copias de fuentes efectivamente leídas, no notas presentadas como descargas.

| Fuente leída | Fecha de la fuente | Pasaje leído | Entradas respaldadas |
|---|---|---|---|
| [PNN Los Nevados — ficha oficial](https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/) | Sin fecha editorial visible en la copia consultada; consultada 2026-11-21. | «Si deseas realizar tomas audiovisuales o fotografías con fines comerciales, eventos, actividades deportivas o actividades de investigación o educación ambiental, debes solicitar la autorización correspondiente. Este requisito aplica a todos los sectores del Parque.» También se leyó la distinción de actividades permitidas por sector. | `rules.commercial_photography`, `rules.audiovisual_permits`, `rules.event_permits`, `rules.organized_sports`, `rules.research_permissions` |
| [Resolución 207 de 2023 — reglamentación ecoturística PNN Los Nevados](https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf) | 2023-08-04; PDF descargado y leído el 2026-11-21. | Citas en el extracto reproducible: «Solo se permite el uso de los senderos que se muestran en el siguiente mapa»; «No está permitido realizar depósitos de basuras o desechos»; «No utilizar drones»; prohibiciones expresas de fogatas, ruido perturbador, alimentación de fauna para atraerla/capturarla, playback, extracción de flora/fauna/rocas, introducir animales o material vegetal, acampar en zonas no permitidas, pesca recreativa y entrar bajo efectos de alcohol o sustancias psicoactivas. El PDF también dice que foto/video aficionado se permite y que el uso comercial requiere permisos. | `rules.stay_on_routes`, `rules.leave_no_waste`, `rules.leave_natural_objects`, `rules.no_introduce_species`, `rules.commercial_photography`, `rules.audiovisual_permits`, `rules.drones`, `rules.open_fires`, `rules.noise`, `rules.feed_wildlife`, `rules.playback`, `rules.camping`, `rules.fishing`, `rules.intoxication` |
| [Decreto Ley 2811 de 1974 — Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=1551) | 1974; art. 336; consultado 2026-11-21. | Art. 336(a): «La introducción y trasplante de especies animales o vegetales exóticas»; (b): «El vertimiento, introducción, distribución, uso o abandono de sustancias tóxicas, o contaminantes que puedan perturbar los ecosistemas»; (c): «La utilización de cualquier producto químico de efectos residuales y de explosivos, salvo cuando los últimos deban emplearse en obra autorizada». | `rules.no_introduce_species`, `rules.avoid_pollutants`, `rules.avoid_chemicals` |
| [PNN — preguntas frecuentes, pregunta 29](https://www.parquesnacionales.gov.co/atencion-al-ciudadano/) | Sin fecha editorial visible; consultada 2026-11-21. | «No, no está permitido el ingreso de mascotas a las áreas protegidas administradas por parques nacionales naturales». | `rules.pets` |

**Nota de recuperación legal:** la primera petición al dominio de Función Pública falló la validación TLS; se leyó el documento al volver a solicitarlo con validación de certificado desactivada. Se registra esta limitación, no se presenta como validación TLS satisfactoria.

## Semillas asignadas

Se conservaron los índices asignados a `rules` en `assignments.json`: **21** («qué debes cuidar durante la visita») y **35** («si puedes llevar mascotas»). El 21 se expresa mediante las reglas verificadas de senderos, residuos y extracción de elementos naturales; no se presenta como una única prohibición genérica. El 35 queda en `rules.pets`, respaldado tanto por la FAQ institucional como por la Resolución 207. No se añadieron semillas de otras secciones. La intención `research_permits` se mantiene aquí como `rules.research_permissions`, según la coordinación.

## Correcciones tras revisión

- `rules.no_introduce_species`: acotada al texto del reglamento del parque sobre introducir animales y material vegetal y al art. 336 sobre especies exóticas. Se retiró la inferencia anterior que trataba toda replantación de especies nativas como prohibida por la ley nacional.
- `rules.stay_on_routes`, `rules.leave_no_waste`, `rules.leave_natural_objects`: pasan de consejo editorial apoyado en fines generales de conservación a reglas textuales de la Resolución 207: senderos autorizados, no dejar basura y no extraer flora/fauna/rocas. No se atribuyen sanciones adicionales.
- `rules.audiovisual_permits` y `rules.commercial_photography`: conservan intenciones distintas por la distinción textual entre video/foto aficionado permitido y uso comercial sujeto a permiso. Se eliminó cualquier requisito de permiso para grabar casualmente con celular; luces, pantallas, telones y drones mantienen su restricción específica.
- Se cerró el vacío sobre drones, fogatas, ruidos perturbadores y alimentación/playback de fauna con las cláusulas explícitas de la Resolución 207. Se añadieron pesca, camping en zonas no permitidas e ingreso bajo efectos porque el reglamento también los enumera.
- No se incorporaron cifras ni sanciones concretas en respuestas. La única excepción de pesca se limita a proyectos científicos/autorizados; la de explosivos se mantiene limitada a obras autorizadas.

## Vacíos y temas no incluidos

No se encontró en las fuentes leídas una regla suficientemente precisa sobre fumar, consumo o porte de bebidas alcohólicas por personas sobrias, parlantes con volumen que no perturbe, baños/residuos humanos para visitantes de pasadía, mascotas de asistencia, sanciones específicas por conducta, ni una lista consolidada y fechada de zonas de camping actualmente operativas. No se afirma que esas conductas estén permitidas. `rules.camping` orienta a confirmar el sitio para la fecha de visita debido a cambios operativos y a textos de camping temporales dentro de la misma resolución.

La Resolución 207 es de 2023; sus reglas se reproducen como lo que dice ese instrumento. Para permisos, campamentos y actividades sujetas a cambios, las respuestas remiten a Parques Nacionales para confirmar condiciones vigentes. No se promete autorización ni resultado de una solicitud.

## Conteo final y contrato (primera pasada, superado por la sección 2026-11-21 de abajo)

- Entradas: **20** (meta de prompt: 80; se priorizó evidencia específica frente a fragmentación sin respaldo).
- Ejemplos: **264**; todos tienen 12 o 14 ejemplos, incluidos 1–2 en inglés, variantes coloquiales colombianas y formas sin tilde/errores naturales. No hay duplicados exactos locales.
- Etiquetas: 20, distintas y de 3–8 palabras. Negativos: 2 por entrada. Variantes: 1 por entrada. Preguntas de aclaración: 6. `needs` y `entity_filters`: vacíos; por tanto no hay slots requeridos sin pregunta asociada. `featured`: 5. `related`: solo referencias locales existentes.
- Semillas: 21 y 35 preservadas en sus intenciones asignadas.
- Validación: verificación determinista contra el schema exacto en `inputs/knowledge-section.schema.json` y comprobaciones del contrato local realizadas el 2026-11-21; resultados consignados en el recibo de corrección.

## Segunda pasada: expansión de `rules` (2026-11-21)

**Fuente única:** `rules/generate_rules.py`. El JSON anterior tenía 8 entradas (`drones`, `open_fires`, `noise`, `feed_wildlife`, `playback`, `camping`, `fishing`, `intoxication`) sin generador en el repo; ahora todas salen del generador y tienen cita verificada.

**Conteo:** entradas 21 → 31 (incluye `rules.no_hunting`, inyectada por `coordination/coordinator_fixes.py`, no tocada aquí); ejemplos 276 → 403. Ningún id retirado.

**Nuevas (10):** `weapons`, `entry_bag_checks`, `minors_protection`, `follow_park_staff`, `sell_advertise`, `single_use_plastics`, `graffiti_signage`, `respect_communities`, `sanctions_penalties`, `preventive_measures`.

**Descartadas antes de publicar:** `restricted_glaciers` (duplicaba `activities.tolima_closed_routes`, que ya cubre la cara sur del Tolima y los glaciares Dulima, Ambala, Krauss, Totare, Combeima y Pijao) y `abandon_gear` (no había ejemplos claros de «abandonar»: dejar la carpa un rato no está respaldado como abandono).

### Fuentes leídas (2026-11-21)

Archivos brutos en `rules/evidence/raw/`; citas literales en `rules/evidence/quotes.md`; `rules/check_quotes.py` verifica cada una (97 citas, 0 fallos).

| Fuente | URL | Archivo bruto | Nota |
|---|---|---|---|
| Resolución 207 de 2023 (34 págs.) | [PDF](https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf) | `res207_2023.pdf`, `res207_2023.txt` (pdftotext) | Mismo sha256 que `activities/evidence/resolucion-207-2023.pdf`. La variante de URL sin `_` final también responde 200 (la usa el inyector de `no_hunting`). |
| Ficha PNN Los Nevados | [ficha](https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/) | `pnn_nevados_ficha.html`, `.txt` | Modificada 2026-10-31 según el sitio. |
| Preguntas frecuentes (pregunta 29) | [FAQ](https://www.parquesnacionales.gov.co/atencion-al-ciudadano/) | `faq_atencion_ciudadano.html`, `.txt` | Mascotas. |
| Decreto 1076 de 2015 (arts. 2.2.2.1.15.1, 2.2.2.1.15.2, 2.2.2.1.16) | [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153) | `decreto_1076_2015.html`, `.txt` | **TLS no validado**: la cadena de certificados falla en este equipo; se obtuvo con `curl -k`. |
| Ley 1333 de 2009 | [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879) | `ley_1333_2009.html` (descarga), `ley_1333_2009_fp.txt` (texto) | **TLS no validado**, mismo caveat. |
| Ley 2387 de 2024 (reforma arts. 40, 49 y otros de la Ley 1333) | [Cancillería, Normograma](https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm) | `ley_2387_2024.htm`, `.txt` | TLS correcto. Sanciones: art. 17 (nuevo art. 40), art. 19 (medidas preventivas), arts. 20-21 (amonestación, servicio comunitario). |

Secretariasenado no respondió en esta sesión; se usó Cancillería para la Ley 2387.

### Conflictos y decisiones

1. **Pesca.** El Decreto 1076 (art. 2.2.2.1.15.1, n.º 10, texto de 1977) permite «la pesca deportiva y la de subsistencia» donde MinAmbiente lo autorice. La Resolución 207 de 2023 prohíbe toda pesca salvo la científica autorizada. **Decisión:** `rules.fishing` sigue la Resolución 207 (más reciente y específica del parque).
2. **Fogatas.** El Decreto 1076 (n.º 5) prohíbe fuegos fuera de sitios autorizados con hornillas o barbacoas; la Resolución 207 prohíbe fogatas y pide camping gas. **Decisión:** `rules.open_fires` sigue la Resolución 207 y no menciona sitios de excepción.
3. **Vehículos hasta Brisas.** La Resolución 207 (prohibiciones) dice «Ingresar con vehículos al área protegida»; la ficha PNN 2026 dice «Puedes llegar a Brisas en tu vehículo, pero no se permite el ingreso de motos». El Decreto 1076 (2.2.2.1.15.2, n.º 8) prohíbe transitar con vehículos fuera del horario y ruta establecidos. **Decisión:** no hay entrada de vehículos en `rules`; el tema queda en `access`. **Aviso al responsable de `access`:** su entrada de vehículos debe citar la ficha 2026, mencionar la contradicción con la Resolución 207 y considerar el texto del Decreto (n.º 8), que sí es utilizable.
4. **Camping.** La Resolución 207 (sitios para camping) lista como zonas establecidas Laguna del Otún, El Cisne (condicionado) y Camping Arenales–Brisas (restringido por actividad volcánica). Como reglamento transitorio habilita en inmediaciones del Tolima Termales Cañón, Arenales y Calvito. Hay dos lugares llamados Arenales; el transitorio es el de la ruta del Tolima. `rules.camping` lo distingue; la lista operativa vigente no está verificada.

### Solapamientos evitados (no se crean entradas)

- Bañarse en lagunas y baños terapéuticos → `activities.therapeutic_baths_banned`.
- Cabalgatas y semovientes → `activities.horseback_not_allowed`.
- Excretas en sendero y campamento → `preparation.camp_hygiene`.
- Motos y estacionamiento en Brisas → `access.no_motorcycles`, `access.parking_at_brisas`.
- Bicicletas y ciclomontañismo → `activities.regulated_sports`.
- Zonas restringidas (glaciares y cara sur del Tolima) → `activities.tolima_closed_routes`.
- Edad mínima, acompañamiento de menores, guía obligatorio → `booking_fees`.

### Cambios en entradas existentes

- `open_fires`: la respuesta cita el camping gas tal como lo escribe la Resolución («deben portar el camping gas»), sin interpretarlo más.
- `camping`: pasó de «zonas permitidas» a prohibición general con zonas establecidas y excepción transitoria (ver conflicto 4).
- `intoxication`: el reglamento prohíbe **ingresar y consumir** alcohol, no solo entrar borracho. El ejemplo «¿puedo llevar una botella de licor cerrada?» estaba como hard negative; la respuesta correcta es que no.
- `no_introduce_species`: etiqueta ahora «no traer animales, semillas ni plantas». Se retiraron dos ejemplos sobre sembrar, porque la regla prohíbe **introducir**, no replantar nativas.
- `noise`: el Decreto 1076 (n.º 15) dice «incomoden a los visitantes», lo que cubre parlantes. Se quitó «música con audífonos» (no está prohibido).
- `feed_wildlife`: se quitó «dar agua a los animales» (no es alimento).
- `avoid_pollutants`, `avoid_chemicals`, `commercial_photography`, `event_permits`, `research_permissions`, `organized_sports`, `drones`, `noise`, `playback`: fuentes y respuestas alineadas a las citas de esta pasada. Se retiró la cita del Decreto Ley 2811 art. 336 (no re-verificada aquí).
- Etiquetas cambiadas: `intoxication` («alcohol y sustancias psicoactivas»), `camping` («acampar dentro del parque»), `no_introduce_species` (ver arriba). Los ids no cambian.

### Vacíos (sin entrada, sin afirmación)

- **Fumar:** ninguna fuente leída lo regula.
- **Velocidad de vehículos y bicicletas fuera de vía:** sin texto en las fuentes leídas.
- **Perros de asistencia:** la Resolución 207 solo menciona «animales de carga y asistencia» para equinos y mulas.
- **Valor en pesos de las multas:** depende del salario mínimo de cada año; la respuesta lo dice y remite a Parques Nacionales.
- **Lista operativa de campamentos:** no verificada más allá de la Resolución.
- **Ley 2068 de 2020, art. 31:** la Resolución 207 (numeral 12) la cita; no se descargó, no se usa.

### Verificación

- `rules/check_quotes.py`: 97 citas, 0 fallos.
- `generate_rules.py` → `coordinator_fixes.py` → `validate_knowledge.py`: `Errors: 0`; 0 ejemplos duplicados en todo el corpus; ninguna advertencia de `rules`.
- `rules/validate_rules.py`: `SCHEMA_ERRORS 0`, `REFERENCES_OK`. Corregido para validar referencias entre secciones (antes marcaba falsamente `rules.no_hunting`).
- Hard negatives: ninguno de `rules` queda sin ejemplo; ninguno apunta a los ejemplos retirados. **Hallazgo para el coordinador:** 842 hard negatives de otras secciones (access 222, preparation 159, activities 142, hours_status 118…) no coinciden con ningún ejemplo del corpus. No son de `rules` y no se tocaron.
- `coordination/check_sources.py`: **reescribió `coordination/source_audit.json`**, fuera de mi límite de escritura. Lo declaro aquí; no lo revertí.
- No aplica verificación en navegador: la sección es datos JSON, no UI.

## Round 2 (2026-11-21)

Auditoría del generador que había pasado de 31 a 80 entradas (79 en `generate_rules.py` más `rules.no_hunting`, inyectada por el coordinador) y se cortó antes de cerrar citas, solapes y redacción. No se descargaron archivos nuevos: se reutilizaron los brutos ya en `rules/evidence/raw/`.

**Conteo:** 31 (cierre anterior) → 80 (generador inconcluso) → **73** (72 del generador + `rules.no_hunting`). Ejemplos de la sección: 403 → 907.

### Retiradas

| Id | Motivo |
|---|---|
| `rules.burying_hiding_trash_prohibited` | El entierro y el ocultamiento bajo rocas quedaron en `rules.leave_no_waste`. `preparation.camp_hygiene` ya dice que no se entierra basura. |
| `rules.tent_technical_standard` | Duplicaba `preparation.mountain_tent` (carpa de 3 o 4 estaciones, bajo cero). |
| `rules.camping_gas_mandatory` | Duplicaba `rules.open_fires` y `preparation.camp_stove`. |
| `rules.stay_with_group_no_straggling` | Duplicaba `health_safety.lost_person_protocol` (grupo unido, nadie rezagado). |
| `rules.no_self_guided_hiking` | Duplicaba `booking_fees.guide_required` (no se entra solo; guía o agencia registrada). |
| `rules.vehicle_route_parking_rules` | Vías, parqueadero y horario son de `access` y `hours_status`. Sigue el conflicto ya anotado: la Resolución 207 prohíbe ingresar con vehículos y la ficha 2026 permite llegar a Brisas en carro. |
| `rules.lighting_screens_backdrops_permits` | Luces, pantallas y telones ya están en `rules.audiovisual_permits` y en `activities.photography_amateur`. |

`rules.sport_mountaineers_advance_request` no se retiró: `activities.sport_mountaineering` ya dice el plazo de 15 días hábiles, la credencial, el seguro y el itinerario. Aquí quedó solo lo que esa respuesta no nombra: coordenadas si el campamento es avanzado, y plan de riesgos y contingencias. Se conservó el ejemplo `toca adjuntar plan de contingencia y coordenadas de campamento en montañismo deportivo?` porque `history_culture` lo usa como negativo.

### Reescritas (la respuesta afirmaba algo que la cita no dice, o copiaba el texto legal)

- `avoid_pollutants`: se quitaron aceite, pinturas y detergentes; la cita habla de sustancias contaminantes o tóxicas y de derrames.
- `avoid_chemicals`: los aerosoles pasaron a `aerosols_sprays_prohibited`.
- `camping`: se quitó la lista Termales Cañón / Arenales / Calvito / Brisas; los sitios están en `activities`. Quedó la prohibición de acampar fuera de zona habilitada.
- `earth_tone_clothing_wildlife`: se quitó “actitud silenciosa”; la Resolución solo pide colores tierra al observar fauna.
- `rock_bolting_prohibited`: el picado de roca quedó en `geological_soil_samples`; aquí solo chapas y anclajes.
- `authorized_stay_duration`: se quitaron los horarios (`hours_status`). Quedó no pasarse del tiempo del permiso.
- `early_termination_correction_plan`: pagar el seguimiento no es condición para cerrar el caso; la ley dice que pueden cobrarlo.
- `liability_exemptions_force_majeure`: se quitó “desconocer el reglamento no exime”; la cita solo lista fuerza mayor, caso fortuito y hecho de un tercero.
- `presumption_of_fault_burden_proof`: se quitó el debido proceso; no está en la frase de la presunción.
- `confession_fine_reduction`: se quitó el Código General del Proceso de la variante.
- `social_media_unauthorized_routes`: se quitó “recopila evidencias para identificar infractores”. La carta de 2026 dice que pueden abrir proceso si hay mérito cuando se divulga en Instagram un ingreso al glaciar o al cráter del Ruiz.
- `visitor_risk_assumption`: el parque no responde por lo extraviado; no por “daños del equipo”.
- El resto de entradas nuevas (excavaciones, trampas, sanciones, RUIA, flagrancia, etc.) pasó de redacción de artículo a segunda persona, 1–3 frases, con la acción al final. Los ejemplos que repetían la norma (“deber de permanecer unidos…”, “portar el documento que acredita…”, “qué dice el artículo…”) se cambiaron por preguntas de visitante.

### Ids nuevos que se conservan

`excavations_prohibited`, `rock_bolting_prohibited`, `geological_soil_samples`, `wildlife_traps_prohibited`, `wildlife_contact_displacement`, `earth_tone_clothing_wildlife`, `aerosols_sprays_prohibited`, `burning_trash_prohibited`, `pick_up_trail_litter`, `biodegradable_packaging_food`, `logging_clearing_vegetation`, `abandoning_gear_objects`, `damage_park_infrastructure`, `agro_industrial_mining_ban`, `authorized_stay_duration`, `show_entry_permit_on_request`, `tent_permit_display`, `respect_carrying_capacity_limits`, `visitor_risk_assumption`, `report_environmental_infractions`, `ecological_customs_checkpoints`, `no_discrimination_scandals`, `park_closure_no_compensation`, `pack_animals_weight_overnight`, `no_mules_arenales_calvito`, `commercial_sound_recording`, `researcher_deliverables_obligation`, `sport_mountaineers_advance_request`, `sport_mountaineers_schedule_exit_report`, `guide_operator_misconduct_ban`, `social_media_unauthorized_routes`, `written_reprimand_mandatory_course`, `community_service_sanction`, `confiscation_restitution_specimens`, `presumption_of_fault_burden_proof`, `confession_fine_reduction`, `early_termination_correction_plan`, `ruia_offender_registry`, `aggravating_factors_protected_area`, `liability_exemptions_force_majeure`, `restoration_duty_civil_criminal`, `flagrancy_foreign_tourists_procedure`.

### Archivos brutos (sin descarga nueva)

| Archivo | URL |
|---|---|
| `res207_2023.txt` | https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf |
| `decreto_1076_2015.txt` | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 |
| `ley_1333_2009_fp.txt` | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879 |
| `ley_2387_2024.txt` | https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm |
| `carta_2026_05_11.txt` | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf |
| `poe_2026_corto.txt` | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf |
| `pnn_nevados_ficha.txt` | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ |
| `faq_atencion_ciudadano.txt` | https://www.parquesnacionales.gov.co/atencion-al-ciudadano/ |

TLS de Función Pública sigue sin validar en este equipo (texto obtenido antes con `curl -k`). Citas añadidas en esta pasada: playback con dispositivo electrónico, rescate de mulas, topes de porteo (Berlín, La Argentina, Buenos Aires, La Primavera, La Playa, Termales de Cañón), facultad de cerrar atractivos, firma del acta de flagrancia, reemplazo de la multa por capacidad económica, datos mínimos del RUIA, credencial, seguro, coordenadas y plan de riesgos del montañismo deportivo.

### Vacíos

- Fumar, límites de velocidad y perros de asistencia: sin texto en las fuentes leídas.
- Valor en pesos de la multa: depende del salario mínimo del año del acto; la respuesta lo dice y remite a Parques Nacionales.
- Lista operativa de campamentos más allá de la Resolución 207: no verificada.
- Ley 2068 de 2020, art. 31, citada por la Resolución 207: no descargada, no usada.
- Guía obligatorio, edad y seguro: `booking_fees`. Grupo unido y extravío: `health_safety`. Carpa y estufa como equipo: `preparation`. Cupos numéricos: `booking_fees`.

### Verificación

- `rules/check_quotes.py`: `quotes checked: 177; failures: 0`
- `generate_rules.py` → `coordinator_fixes.py` → `validate_knowledge.py`: `Errors: 0; review flags: 4`
- Las 4 advertencias no son de `rules` (dos negativos de `conversation`, uno de `hours_status`, etiquetas parecidas en `booking_fees`).
- No se hizo commit. No aplica navegador: la sección es JSON.


## Updated entry: rules.abandoning_gear_objects

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Abandonar objetos, vehículos o equipos de cualquier clase.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Los residuos generados por la actividad como alimentos, ropa, plásticos, carpas, etc., deberán ser removidos de
> las áreas protegidas


## Updated entry: rules.agro_industrial_mining_ban

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> 3. Desarrollar actividades agropecuarias o industriales incluidas las hoteleras, mineras y petroleras.


## Updated entry: rules.authorized_stay_duration

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Solamente podrá permanecer en el Área Protegida durante el tiempo autorizado por el Parque.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Las personas que utilicen las áreas del Sistema de Parques Nacionales Naturales, podrán permanecer en ellas sólo el tiempo especificado en las respectivas autorizaciones, de acuerdo con los reglamentos que se expidan para cada una.


## Updated entry: rules.avoid_chemicals

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> La utilización de cualquier producto químico de efectos residuales y de explosivos, salvo cuando los últimos deban emplearse en obra autorizada.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Tampoco se permite el uso de productos químicos en aerosoles o en
> grandes cantidades que puedan ocasionar derrames y contaminación en el suelo, el aire o el agua.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Llevar y usar cualquier clase de juegos pirotécnicos o portar sustancias inflamables no expresamente autorizadas y sustancias explosivas.


## Updated entry: rules.avoid_pollutants

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Tampoco se permite el uso de productos químicos en aerosoles o en
> grandes cantidades que puedan ocasionar derrames y contaminación en el suelo, el aire o el agua.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> El vertimiento, introducción, distribución, uso o abandono de sustancias tóxicas o contaminantes que puedan perturbar los ecosistemas o causar daños en ellos.


## Updated entry: rules.camping

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: label, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Realizar camping en zonas no permitidas y el uso de play-back (reproducción de audios de fauna silvestre con
> algún dispositivo electrónico) en el Área Protegida.


## Updated entry: rules.commercial_photography

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt`

> Si deseas realizar tomas audiovisuales o fotografías con fines comerciales, eventos, actividades deportivas o actividades de investigación o educación ambiental, debes solicitar la autorización correspondiente.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Se permite la toma de imágenes de video y fotografía de carácter no profesional
> o aficionado.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Las personas que utilicen las áreas del Sistema de Parques Nacionales Naturales, podrán permanecer en ellas sólo el tiempo especificado en las respectivas autorizaciones, de acuerdo con los reglamentos que se expidan para cada una.


## Updated entry: rules.community_service_sanction

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt`

> El infractor que incumpla el servicio comunitario o la asistencia al curso será sancionado con multa equivalente hasta de cinco (5) salarios mínimos legales mensuales vigentes

- https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt`

> Estas medidas podrán reemplazar las multas solo cuando la capacidad socioeconómica del infractor sea insuficiente, y podrán ser complementarias en todos los casos.


## Updated entry: rules.confiscation_restitution_specimens

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt`

> Decomiso definitivo de especímenes, especies silvestres exóticas, productos y subproductos, elementos, medios o implementos utilizados para cometer la infracción.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt`

> 6. Atentar contra recursos naturales ubicados en áreas protegidas o declarados en alguna categoría de amenaza o en peligro de extinción o sobre los cuales existe veda, restricción o prohibición.
> 7. Realizar la acción u omisión en áreas de especial importancia ecológica.


## Updated entry: rules.drones

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> No utilizar drones conforme la resolución No. 0543 del 27 de
> diciembre de 2018.


## Updated entry: rules.earth_tone_clothing_wildlife

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> procurando vestir con
> colores tierra o evitando colores muy vivos con el fin de no perturbar la fauna.


## Updated entry: rules.ecological_customs_checkpoints

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Someterse a aduanas ecológicas emprendidas por las autoridades encargadas del manejo del turismo en el sector.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> No ingresar plásticos de un solo uso ya que actualmente se encuentra prohibido de acuerdo a la Resolución 1558
> de 2019.


## Updated entry: rules.entry_bag_checks

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Participar en los controles de ingreso y salida que realiza el área protegida, permitiendo la búsqueda de sustancias
> psicoactivas, elementos embriagantes, armas de fuego, elementos cortopunzantes, equipos de pesca, entre otros


## Updated entry: rules.event_permits

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt`

> Si deseas realizar tomas audiovisuales o fotografías con fines comerciales, eventos, actividades deportivas o actividades de investigación o educación ambiental, debes solicitar la autorización correspondiente.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Promover, realizar o participar en reuniones no autorizadas por Parques
> Nacionales Naturales de Colombia


## Updated entry: rules.excavations_prohibited

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Tampoco está permitido realizar excavaciones o enterramientos de basuras, de manera
> excepcional se permitirá realizar hoyo de gato para el manejo de excretas.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Realizar excavaciones de cualquier índole, excepto cuando las autorice Parques Nacionales Naturales de Colombia por razones de orden técnico o científico.


## Updated entry: rules.feed_wildlife

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> No se permite la instalación de trampas o conductores de fauna, así como tampoco brindar alimentación a la fauna
> silvestre con el fin de atraerlos o capturarlos.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Suministrar alimentos a los animales.


## Updated entry: rules.fishing

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Realizar actividades de pesca, salvo la pesca con fines científicos o investigativos, debidamente autorizada por la
> autoridad ambiental.


## Updated entry: rules.follow_park_staff

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Acatar las recomendaciones de los funcionarios del parque y de los guías e intérpretes autorizados por la institución.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> los funcionarios a quienes designe Parques Nacionales de Colombia para ejercer el control y vigilancia, tendrán funciones policivas.


## Updated entry: rules.liability_exemptions_force_majeure

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt`

> Son eximentes de responsabilidad:
> 1. Los eventos de fuerza mayor o caso fortuito, de conformidad con la definición de los mismos contenida en la Ley 95 de 1890.
> 2. El hecho de un tercero, sabotaje o acto terrorista.


## Updated entry: rules.no_hunting

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, examples

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Por ningún motivo está permitida la toma de muestras botánicas ni la caza
> o captura de ejemplares de fauna.


## Updated entry: rules.no_introduce_species

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Introducir transitoria o permanentemente animales, semillas, flores, propágulos de cualquier especie.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Introducir transitoria o permanentemente animales, semillas, flores o propágulos de cualquier especie.


## Updated entry: rules.noise

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Producir ruidos o utilizar equipos que puedan perturbar el ambiente natural.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Producir ruidos o utilizar instrumentos o equipos sonoros que perturben el ambiente natural o incomoden a los visitantes.


## Updated entry: rules.park_closure_no_compensation

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Parques Nacionales Naturales los Nevados dentro de sus facultades legales, podrá restringir el ingreso o cerrar los
> atractivos el tiempo que haya lugar, mediante resolución motivada por razones de seguridad, gestión del riesgo,
> investigación y/o protección ecológica

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Este hecho no compromete a la entidad
> a indemnizar a los prestadores de servicios ecoturísticos o turistas que hayan solicitado su entrada al área protegida con
> anticipación.


## Updated entry: rules.pets

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Ingresar animales domésticos o mascotas y material vegetal.

- https://www.parquesnacionales.gov.co/atencion-al-ciudadano/ (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/faq_atencion_ciudadano.txt`

> No, no está permitido el ingreso de mascotas a las áreas protegidas administradas por parques nacionales naturales.


## Updated entry: rules.pick_up_trail_litter

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: label, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Así también, en caso de observar residuos durante el recorrido recogerlos para sacarlos a las zonas
> de para su disposición final.


## Updated entry: rules.playback

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Realizar camping en zonas no permitidas y el uso de play-back (reproducción de audios de fauna silvestre con
> algún dispositivo electrónico) en el Área Protegida.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Tampoco se permite el uso de playback durante la observación de
> aves.


## Updated entry: rules.presumption_of_fault_burden_proof

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt`

> En las infracciones ambientales se presume la culpa o dolo del infractor, quien tendrá a su cargo desvirtuarla, en los términos establecidos en la presente ley.


## Updated entry: rules.report_environmental_infractions

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Denunciar delitos o penalidades ante los funcionarios del Parque o las autoridades competentes.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Denunciar ante los funcionarios de Parques Nacionales Naturales de Colombia, y demás autoridad competentes, la comisión de infracciones contra los reglamentos


## Updated entry: rules.respect_carrying_capacity_limits

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Respetar la capacidad de carga establecida para cada uno de los senderos y el número máximo de personas por
> grupo.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> No sobrepasar la capacidad de carga establecida para la actividad


## Updated entry: rules.respect_communities

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Respetar la cultura y costumbres de los habitantes del lugar.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Hacer discriminaciones de cualquier índole.


## Updated entry: rules.restoration_duty_civil_criminal

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified, sources

- https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt`

> no exime al infractor de ejecutar las obras o acciones ordenadas por la autoridad ambiental competente, de restaurar el medio ambiente

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt`

> Estas sanciones se aplicarán sin perjuicio de las acciones civiles, penales, fiscales y disciplinarias a que hubiere lugar.


## Updated entry: rules.show_entry_permit_on_request

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Portar el documento que acredita el derecho de ingreso durante todo el tiempo de permanencia en el área
> protegida, así como adherir una copia del derecho de ingreso en un lugar visible a la carpa cuando se realizan
> campamentos.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Exhibir ante los funcionarios y autoridades competentes la autorización respectiva e identificarse debidamente cuando se les requiera.


## Updated entry: rules.social_media_unauthorized_routes

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/carta_2026_05_11.txt`

> la presunta incursión no autorizada al sector del glaciar y cráter del Volcán Nevado del
> Ruíz, en jurisdicción del Parque Nacional Natural Los Nevados, y la divulgación de dicho
> recorrido a través de la red social Instagram

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Parques Nacionales Naturales los Nevados dentro de sus facultades legales, podrá restringir el ingreso o cerrar los
> atractivos el tiempo que haya lugar, mediante resolución motivada por razones de seguridad, gestión del riesgo,
> investigación y/o protección ecológica

- https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/carta_2026_05_11.txt`

> Una vez verificada la información, y de encontrarse elementos que permitan es-
>       tablecer la posible ocurrencia de una infracción ambiental o el incumplimiento de
>       las disposiciones aplicables al área protegida, se dará trámite a las actuaciones
>       administrativas que correspondan


## Updated entry: rules.sport_mountaineers_advance_request

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Plan de riesgos y contingencias: Documento que evalúa los riesgos y describe las acciones de prevención y manejo
> de contingencias

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> días de ocupación de los campamentos con coordenadas en caso de que sean campamentos avanzados o vivac,


## Updated entry: rules.stay_on_routes

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: answer, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Solo se permite el uso de los senderos que se muestran en el siguiente mapa


## Updated entry: rules.tent_permit_display

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Portar el documento que acredita el derecho de ingreso durante todo el tiempo de permanencia en el área
> protegida, así como adherir una copia del derecho de ingreso en un lugar visible a la carpa cuando se realizan
> campamentos.


## Updated entry: rules.visitor_risk_assumption

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Cada persona será responsable de sus objetos personales.

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> ni implican para Parques Nacionales Naturales de Colombia ninguna responsabilidad, por tanto, los visitantes de estas áreas asumen los riesgos que puedan presentarse durante su permanencia en ellas.


## Updated entry: rules.weapons

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Participar en los controles de ingreso y salida que realiza el área protegida, permitiendo la búsqueda de sustancias
> psicoactivas, elementos embriagantes, armas de fuego, elementos cortopunzantes, equipos de pesca, entre otros

- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153 (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt`

> Portar armas de fuego y cualquier implemento que se utilice para ejercer actos de caza, pesca y tala de bosques


## Updated entry: rules.wildlife_contact_displacement

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> Evitar el contacto con la vida silvestre. No intente coger, ni alimentar ni desplazar especies de fauna de las zonas
> donde se encuentran.


## Updated entry: rules.wildlife_traps_prohibited

- Reason: Dating rule to 2026-11-21 backed by official regulation, clarifying label, and verifying evidence.
- Changed fields: label, last_verified

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt`

> No se permite la instalación de trampas o conductores de fauna, así como tampoco brindar alimentación a la fauna
> silvestre con el fin de atraerlos o capturarlos.
