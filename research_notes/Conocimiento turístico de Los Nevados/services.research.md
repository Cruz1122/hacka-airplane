# Servicios (`services`, orden 10): log de investigación, corrección 1

Fecha de corte: 2026-11-21. Perfil: `lookup`. Sección final: `data/knowledge/sections/services.json`.
Versión original (ronda 1, sin tocar): `coordination/round1/services.json`.
Evidencia: `services/evidence/` (texto extraído y HTML). Validador: `services/evidence/validate_services.py`.
Recibo de corrección: `services/correction-receipt.md`.

## 0. Resultado final

| Métrica | Valor |
|---|---|
| Entradas | 24 (21 de la corrección 1 + 3 nuevas en la ronda 2; ver §8). Antes de la corrección 1: 27 |
| Ejemplos | 300; mínimo 12, máximo 14 por entrada |
| Inglés | 1–2 por entrada |
| Hard negatives | 2 por entrada (48 en total); todos son ejemplos de otra entrada (comprobado por el generador) |
| Variantes | 1 por entrada |
| Related | 2–3 por entrada; todos son ids locales |
| Featured | 5 |
| Clarification bank | 6 preguntas; slot `sector` |
| Semillas (`assignments.json`) | `[]`. Ninguna semilla asignada a services |
| Schema | jsonschema contra `inputs/knowledge-section.schema.json`: 0 errores |
| Validador local | 0 errores, 0 advertencias |
| Duplicados | 0 exactos y 0 casi duplicados (ratio ≥ 0,9) contra las secciones presentes en `data/knowledge/sections/` |

Título, perfil (`lookup`) y orden (10) sin cambios.

## 1. Fuentes realmente leídas

Solo cuento como leídas las URLs de esta tabla. Las fechas de metadatos salen del archivo guardado, no de la página visible.

| # | URL | Consulta | Evidencia guardada | Fecha según metadatos | Uso |
|---|---|---|---|---|---|
| 1 | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ | 2026-11-21, HTTP 200 | `services/evidence/pnn_nevados.html` y `.txt` | `dateModified` 2026-10-31; `datePublished` 2025-07-14 | Fuente principal de 2026 |
| 2 | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx | 2026-11-21, HTTP 200 | `services/evidence/pnn_informe_necesidades_2024.docx` y `.txt` | `created`/`modified` 2024-12-12 (`docProps/core.xml`) | Infraestructura, servicios por área, necesidades |
| 3 | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf (acento descompuesto) | 2026-11-21, HTTP 200, 10.085.571 bytes | `services/evidence/poe2026/poe2026.pdf` y `poe2026.txt` | ModDate 2026-03-06; 23 páginas | Porteadores como categoría regulada (p. 31, número impreso); radiocomunicaciones como acción futura |
| 4 | https://www.operacionnevados.co/ | 2026-11-21, HTTP 200 | `services/evidence/uton_3b654e8f.html` y `.txt` | Sin fecha visible | Dirección UTON en Palermo; menú Reservas; no lista servicios por sector |

No usadas o fallidas:
- `https://ecoturismonevados.com.co/uton-union-temporal-operador-nevados/`: HTTP 404. No citada.
- `services/evidence/uton_3dfb6bc5.html`: **no es UTON**. Es una página de apuestas no relacionada ("Hello88"). Excluida de todas las citas. Conviene borrarla o moverla fuera de la evidencia.
- `reservasnevados.com`: aparece en la página de PNN como enlace de reserva. No fue abierta. No se cita como verificada.
- Búsquedas web, agregadores, El Tiempo, colombia.travel: no usados como fuente.

Búsqueda textual en las fuentes 1, 2 y 3 (señal, cobertura, celular, energía, carga, accesibilidad, rampas, discapacidad, agua potable): sin resultados de servicio. Solo aparecen "cobertura del área protegida" (plan), "radiocomunicaciones" (acción 2026-2030) y "implementar comunicaciones para la gestión del riesgo" (necesidad 2024).

## 2. Entradas finales

| id | label | Fuente principal | Hecho clave verificado |
|---|---|---|---|
| `brisas_visitor_center` | taquilla y cabaña del centro Brisas | PNN 1; informe 2 | Trayecto desde el centro de inducción Brisas, unos 4100 m (PNN). Infraestructura: taquilla, centro de inducción y cabaña (informe 2024) |
| `north_food` | comida en Brisas y Arenales | informe 2 | Cabañas de Brisas y Arenales prestan alimentos, baños y enfermería (informe 2024) |
| `toilets` | baños para visitantes en el norte | informe 2 | Arenales: "Un comedor y dos baterías de baños para visitantes" (2024). Otún, Cisne y Potosí sin dato |
| `first_aid_points` | punto de primeros auxilios en Arenales | informe 2 | Arenales: "Un punto de atención de primeros auxilios" (existente). Otros sitios figuran como necesidades |
| `cisne_visitor_center` | alojamiento en el centro El Cisne | PNN 1; informe 2 | Concesión UTON para alojamiento en el centro El Cisne (PNN); "alojamiento y alimentación" (informe 2024); 4100 m aprox. |
| `potosi_cabin` | cabaña Potosí y refugio de Campo Alegre | PNN 1; informe 2 | Cabaña Potosí a 3920 m aprox. y punto de control (PNN). Mantenimiento en 2024. Hospedaje y alimentación en "refugio Potosí" de la comunidad de Campo Alegre (informe 2024) |
| `otun_lodging` | casas de hospedaje en El Bosque | PNN 1; informe 2 | "estadía en casas tradicionales de los habitantes ... de la vereda El Bosque" (PNN). "Hospedaje y alimentación. Porteo de maletas" (informe 2024) |
| `tolima_lodging` | hospedaje en Termal Cañón y La Primavera | informe 2 | "Hospedaje y alimentación Termal Cañón, predio la Playa y la Primavera" (informe 2024; fuente declarada Plan 2017–2022) |
| `brisas_lodging` | camas en Brisas: confirmar con UTON | PNN 1; informe 2 | Conflicto interno de PNN (ver §5). Informe 2024 sin alojamiento en Brisas |
| `porter_luggage` | porteo de maletas en rutas | PNN 1; informe 2; PDF 3 | PNN: porteo "gestionado de manera propia o coordinada con guías o agencias registradas". Informe: El Bosque, ruta Juntas, Chilcos–Arenales cumbre. PDF p. 31: "Porteadores" como categoría PSAE |
| `uton_services` | qué gestiona la concesión UTON | PNN 1; informe 2; UTON 4 | PNN: "reservas, ingreso, guianza, transporte, alojamiento y tienda" (Brisas). Informe: "tiene previstos" taquilla, guianza y alimentos hasta Valle de las Tumbas |
| `guide_radios` | radios que llevan los guías | PNN 1 | Guías y operadores registrados deben llevar "los radios con la frecuencia requerida" y "equipo médico de respuesta" |
| `phone_signal` | señal de celular en el parque | PNN 1; informe 2; PDF 3 | Sin dato de cobertura. Informe: necesidad de "implementar comunicaciones para la gestión del riesgo" en algunos sectores. PDF: "Adquirir equipos ... de radiocomunicaciones" (acción) |
| `charging_power` | carga de celular o batería | — | Sin dato en ninguna fuente (búsqueda textual) |
| `accessibility` | accesibilidad para movilidad reducida | PNN 1; PDF 3 | Sin dato de accesibilidad. PNN: Quindío–Dulima "exige al visitante una preparación previa" |
| `drinking_water` | agua para tomar en el parque | PNN 1 | Sin punto de agua potable en fuentes. PNN: "Ten una buena hidratación antes, durante y después de la actividad" |
| `shop_ecotienda` | tienda y ecotienda del norte | PNN 1; informe 2 | PNN: UTON gestiona "tienda" (Brisas). Informe: "Contenedor como punto de atención de visitantes y eco-tienda", "En buenas condiciones" (Valle de las Tumbas, 2024) |
| `refugio_cabin` | cabaña El Refugio no habilitada | informe 2 | "Cabaña El Refugio no habilitada. (se debe dar de baja)"; "En malas condiciones" (2024). Ruta al borde glaciar del Ruiz "Restringido de acuerdo al nivel de actividad del VN del Ruiz" |
| `camp_showers` | duchas y cocina para campistas | informe 2 | Arenales: batería de baños "para campistas" con duchas; "Un comedor y cocina para los campistas"; "Zona de camping no se encuentra habilitada debido a la actividad volcánica" (2024) |
| `official_sites` | dónde confirmar servicios en línea | PNN 1; UTON 4 | Sitios leídos: parquesnacionales.gov.co y operacionnevados.co. UTON inicio muestra menú Reservas |
| `quindio_dulima` | servicios en Quindío–Dulima | PNN 1; informe 2 | PNN: "exige al visitante una preparación previa"; PNN nombra puntos de atención en Valle del Cocora, Juntas y Anzoátegui. Informe 2024 los lista como necesidades |

Las respuestas usan solo los números siguientes, todos con pasaje oficial fechado:
- 4.100 m (trayecto Brisas y centro El Cisne): PNN 2026.
- 3.920 m (cabaña Potosí): PNN 2026.
- "Dos baterías de baños" (Arenales): informe 2024.
- 2017–2022: fecha del plan citado en tablas del informe 2024.

Se retiró la capacidad de "32 personas" del centro El Cisne. Esa cifra es un objetivo del plan 2017–2022 citado en el informe 2024, no una capacidad actual.

## 3. Eliminadas de services y destino

| Entrada eliminada | Motivo | Destino y estado |
|---|---|---|
| `research_permits` | Pertenece a `rules` (fusión con `rules.research_permissions`) | El dueño de `rules` debe absorber los ejemplos de filmación comercial listados en §6.1 |
| `registered_providers` | Requisito de REPSE y guía, va en `booking_fees` | `booking_fees.registered_operator_choice` ya cubre la intención. Nada que trasladar |
| `charla_induccion` | Requisito de inducción, va en `booking_fees` | `booking_fees` no tiene entrada de charla obligatoria; `activities.induction_talk` la cubre hoy. **Pendiente de asignación por el coordinador** |
| `cabin_status_2024` | Dato histórico, no intención distinta | Fusionado: Potosí (mantenimiento 2024) en `potosi_cabin`; El Refugio (no habilitada 2024) en `refugio_cabin`; Brisas "buen estado" (2024) en `brisas_visitor_center`. La Cueva ("buenas condiciones", 2024) no aparece en ninguna entrada |
| `uton_offices` | Duplica `access.uton_offices_manizales` y `hours_status.uton_concession_office_hours` | Datos verificados: PNN lista "Carrera 26A #68-44, barrio Palermo" y "Calle 70 #27-70" como oficinas en Manizales. UTON inicio muestra "Cl 70 # 27-70 - Palermo". Ambas direcciones tienen soporte oficial. Teléfonos 321 506 6031 y 322 360 3637 (PNN). Horario de UTON según la página de PNN: L–V 8:00 a. m. a 12:00 m. y 2:00 a 5:00 p. m. |
| `pnn_customer_service` | Duplica `hours_status.pnn_administrative_office_hours` | Datos verificados: conmutador +57 (601) 353 2400, ext. 3011–3012; línea gratuita 018000129722 desde fijo; L–V 8:00 a. m. a 4:30 p. m. (PNN) |

## 4. Corregidas (resumen)

- `potosi_cabin`: la cabaña del parque es punto de control y registro (PNN). El hospedaje y la comida de la zona se atribuyen al refugio Potosí de la comunidad de Campo Alegre (informe 2024). La respuesta no implica alojamiento en la cabaña.
- `brisas_lodging`: respuesta corta de confirmación ("No tengo confirmado que haya camas en Brisas..."). El conflicto de fuentes queda en `detail`.
- `charging_power`: respuesta por defecto "No tengo confirmado dónde cargar el celular..."; sin narración de búsqueda; consejo de empaque breve; ejemplo "cargador" eliminado.
- `refugio_cabin` y `camp_showers`: fecha 2024 explícita en la respuesta; sin afirmar estado actual.
- `north_food`: quité "agua" como respaldo (inferencia). Dato de 2024 explícito.
- `phone_signal` y `guide_radios`: sin "PNN no tiene cobertura"; la frecuencia de radio no se incluye porque no aparece en las fuentes.
- `porter_luggage`: quité la afirmación de que el parque "presta" el porteo; PNN dice que se gestiona por cuenta propia o con guía o agencia registrada.
- `cisne_visitor_center`: quité la capacidad de 32 (ver §2).
- Todas las entradas: quitada la repetición "confirma antes de viajar"; la cifra "2024" o "según PNN" aparece donde el dato lo requiere.

## 5. Conflictos y resolución

| Conflicto | Fuentes | Resolución |
|---|---|---|
| Alojamiento en Brisas | PNN (sección de Brisas: incluye "alojamiento"); PNN (sección de guías: "reservas, ingreso, guianza, transporte y tienda", sin alojamiento); informe 2024 (no lista alojamiento) | Respuesta de confirmación. Sin cupo ni precio |
| Servicios UTON | PNN (incluye alojamiento); informe 2024 ("tiene previstos" taquilla, guianza, alimentos hasta Valle de las Tumbas) | Ambas versiones con fecha. "Previstos" no se presenta como servicio confirmado |
| Porteo en Arenales | Informe 2024 (lista "Servicio de Porteo de Maletas" en Chilcos–Arenales cumbre); reglamentación de 2023 citada en otra sección (no lo incluye en Arenales) | La respuesta pide confirmar el tramo. **Pendiente para el dueño de `activities`/`access`** |
| Altitudes | PNN: Brisas y Cisne "4100 m aproximadamente", Potosí 3920 m. Informe 2024 (tabla de emergencias): Brisas 4150, Cisne 4180, Potosí 3800 | Se usan las cifras de PNN, marcadas como aproximadas |
| Fuente de las tablas de infraestructura | Informe 2024 cita como fuente el Plan 2017–2022 | Se indica "informe 2024" y se advierte que puede ser anterior en `detail` |

## 6. Vacíos y recomendaciones

### 6.1 Candidatos para `rules` (permiso de filmación; no lo escribí en `rules`)

PNN: para "tomas audiovisuales o fotografías con fines comerciales, eventos, actividades deportivas o actividades de investigación o educación ambiental, debes solicitar la autorización correspondiente. Este requisito aplica a todos los sectores." Además, PNN dice que existen seis tipos de permiso de investigación.

Ejemplos reales que retiré de services y que `rules` puede absorber:
- "necesito permiso para grabar comercial"
- "puedo hacer un video para empresa"
- "tomas comerciales en el parque"
- "rodaje en el nevado"
- "permiso para hacer un documental"
- "can I film a commercial here"
- "toca pedir permiso para grabar un comercial?"

### 6.2 Vacíos sin fuente oficial

1. Señal de celular o datos (ni PNN 2026, ni informe 2024, ni PDF 2026).
2. Puntos de carga o electricidad.
3. Accesibilidad física (rampas, baños accesibles, sillas de ruedas).
4. Agua potable en el parque.
5. Baños fuera de Brisas y Arenales.
6. Tienda fuera de Brisas y Valle de las Tumbas.
7. Camas o cupo en Brisas, y capacidad actual del centro El Cisne.
8. Precios de porteo, de alojamiento comunitario y de comida.
9. Estado actual (2026) de cabañas, camping de Arenales, El Refugio y Potosí.
10. Frecuencia de radio de los guías.

### 6.3 Recomendaciones para el coordinador

1. `booking_fees`: asignar la charla de inducción obligatoria (Brisas: última charla 1:30 p. m., PNN). Hoy solo la cubre `activities.induction_talk`.
2. `rules`: absorber los candidatos de §6.1.
3. `access` y `activities`: `access.porteo_luggage` y `activities.luggage_portage` solapan con `services.porter_luggage`, que es dueño del servicio de porteo. Decidir la regla de Arenales (§5).
4. `access.brisas_visitor_center` solapa con `services.brisas_visitor_center`. Services cubre las instalaciones; access cubre la entrada y la ruta.
5. `access.uton_offices_manizales` queda como dueño de las oficinas UTON; `hours_status` del horario.
6. Eliminar `services/evidence/uton_3dfb6bc5.html` y su `.txt`. Son contenido de apuestas no relacionado.

## 7. Límites declarados

- No verifiqué servicios actuales de 2026. Todo dato de infraestructura viene del informe 2024.
- La fecha de la página de PNN (2026-10-31) es de metadatos. No indica la fecha de cada dato.
- No hubo búsquedas web en esta corrección.
- Ninguna entrada indica que un servicio esté abierto o cerrado hoy. No se prometen reportes de emergencia ni envío de datos.

## Coordinator final sample corrections

Historical facility/service answers now explicitly ask to confirm availability before travel. Toilets are described as recorded in 2024, not guaranteed currently operational. Brisas lodging short no longer narrates a document comparison; full conflict stays in detail. The unrelated UTON-lookalike betting response is excluded as evidence and will not be packaged. No deletion of provenance files is required. services.otun_lodging is the sole lodging-intent owner after removal of activities.el_bosque_houses.

## 8. Ronda 2 (2026-11-21): ampliación con fuentes oficiales

Generador: `services/generate_services.py` (idempotente: parte del JSON actual, aplica `CORRECTIONS` por id y hace upsert de `NEW_ENTRIES`). Ejecutar: `python3 services/generate_services.py`. Citas con URL y fecha: `services/evidence/quotes-2026-11-21.md`.

### 8.1 Resultado
| Métrica | Antes | Después |
|---|---|---|
| Entradas | 21 | 24 |
| Ejemplos | 259 | 300 |
| Entradas nuevas | — | `services.interpretive_guiding`, `services.town_lodging_rnt`, `services.lost_items` |
| Entradas corregidas | — | `porter_luggage`, `guide_radios`, `drinking_water`, `phone_signal` (solo `detail` y fuentes; respuestas sin cambio) |

Validador del proyecto (`coordination/validate_knowledge.py`): `Errors: 0`. Esquema del repositorio (`docs/schemas/knowledge-section.schema.json`): OK. Duplicados globales de ejemplos entre todas las secciones: 0.

### 8.2 Fuentes nuevas leídas (acceso 2026-11-21)
| # | URL | Archivo guardado | Uso |
|---|---|---|---|
| 5 | https://parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf | `services/evidence/new/anexo_pnn_nevados_2023.pdf` y `.txt` | Requisitos de guías (registro PNN, tarjeta, botiquín, radio), prohibición de porteo en campamentos temporales de Calvito y Arenales, correo del parque. Documento de 2023 |
| 6 | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/07/nevados.pdf | `new/nevados_2024_07.pdf` y `.txt` | "Radiocomunicaciones" y "Conectividad" como aciertos (sin cobertura por sector) |
| 7 | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf | `new/radicado_20266200001002.pdf` y `.txt` | Correo general del parque en el pie (2026). El tema es la plataforma de reservas |
| 8 | https://www.mincit.gov.co/minturismo/analisis-sectorial-y-promocion/registro-nacional-de-turismo/que-es-el-registro-nacional-de-turismo | `new/mincit_que_es_rnt.html` | RNT obligatorio, renovación 1 ene–31 mar, integración con RUES |
| 9 | https://www.mincit.gov.co/prensa/noticias/turismo/mincit-invita-renovar-registro-nacional-de-turismo (11-02-2026) | `new/mincit_invita_renovar_rnt_2026.html` | Ventana de renovación 2026 y suspensión si no se renueva |
| 10 | https://villamaria-caldas.gov.co/Participa/Documents/INFORME%20RENDICION%20%20DE%20CUENTAS%20DICIEMBRE%202025%20.pdf (dic. 2025) | `new/villamaria_rendicion_dic2025.pdf` y `.txt` | Correo de la Oficina de Turismo de Villamaría (línea 107); informe de gestión 2025 sin listado de alojamientos |
| 11 | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/02/Protocolo-de-reservas-nevado-del-Tolima.pdf | `new/protocolo_reservas_tolima_2024.pdf` | Leído; trata reservas y pago de ingreso (booking_fees). No se usa en services |

Fuentes 1–4 de §1 (ronda 1) se mantienen; la numeración 5–11 es de esta ronda. Las URL con tilde sin codificar dieron 404 y se descartaron (`Respuesta-Radicado-Anónimo-*.pdf`).

### 8.3 Entradas nuevas: decisiones
- `interpretive_guiding` (fact): la guianza se publica por sendero en el informe 2024 (§7 "prestados por terceros"). El sector del Ruiz corresponde a Brisas–Kumanday; se asigna `brisas` por inferencia del acceso, no por una cita literal. No nombra operadores ni tarifas: las tarifas son de booking_fees.
- `town_lodging_rnt` (procedure): no hay listado oficial de alojamientos por municipio en ninguna fuente abierta. Por eso la entrada enseña a verificar el RNT y da el correo de Villamaría. Murillo y Santa Rosa no tienen contacto oficial verificado. No se nombra ningún negocio privado (las búsquedas mostraron hoteles privados en Villamaría y Santa Rosa; se descartan).
- `lost_items` (procedure): no hay procedimiento de objetos perdidos publicado. La respuesta da el correo general del parque y lo marca como "no confirmado". No inventa punto de entrega ni horario.

### 8.4 Correcciones a entradas existentes (ronda 2)
- `porter_luggage`: el detalle ahora cita la prohibición del anexo 2023 para Calvito y Arenales. El conflicto con el informe 2024 queda abierto; la respuesta sigue pidiendo confirmar el tramo.
- `guide_radios`: el detalle cita los requisitos del anexo 2023 (botiquín, radio portable, certificado de primeros auxilios de 20 horas). La frecuencia de radio sigue sin dato.
- `drinking_water`: el detalle aclara que el filtro de agua del guía no es un punto de agua.
- `phone_signal`: el detalle cita el folleto 2024 (radiocomunicaciones y conectividad como aciertos) sin afirmar cobertura.

### 8.5 Conflictos nuevos (ronda 2)
| Conflicto | Fuentes | Resolución |
|---|---|---|
| Dirección de la oficina PNN en Manizales | Anexo 2023: "Calle 69 A No 24-69 Barrio La Camelia"; carta 2026: "Calle 68 No. 23A – 25 Barrio Palermo"; ronda 1 (PNN): "Carrera 26A #68-44" y "Calle 70 #27-70" | No es de services. Se registra para `access` y `hours_status`. Services no da dirección de PNN |
| Porteo en Arenales | Anexo 2023 (prohibido en campamento temporal Calvito y Arenales) vs informe 2024 (porteo en Chilcos–Arenales cumbre) | Sin resolver. Se cita ambas fuentes y se pide confirmar el tramo |
| Cobertura de radio y conectividad | Folleto 2024 (aciertos) vs informe 2024 (necesidad de comunicaciones) | Sin cobertura confirmada. `phone_signal` no afirma señal |

### 8.6 Vacíos (sin fuente oficial; no hay entrada)
1. Alquiler de equipo (carpas, bastones, botas): ninguna fuente.
2. Cajeros y datáfonos dentro del parque: ninguna fuente. El pago de ingreso es de booking_fees.
3. Gasolina en la ruta: ninguna fuente oficial. Pertenece a `access`.
4. Wifi por sector: el folleto 2024 no dice cobertura. Queda en el vacío de `phone_signal`.
5. Procedimiento y horario de objetos perdidos: no publicado.
6. Estado actual de cabañas, camping y refugios: solo hay datos de 2024.
7. Lista de alojamientos en Murillo y Santa Rosa de Cabal: no hay fuente oficial abierta.
8. Contacto oficial de turismo en Murillo y Santa Rosa: no verificado.

### 8.7 Temas descartados (dueño de otra sección)
- Parqueadero y transporte: `access` (contrato: access cubre parking).
- Camping, zonas de campamento y hora de llegada: `activities` y `hours_status`.
- Guía obligatorio, operador registrado REPSE, seguro: `booking_fees`.
- Tarifas de guianza y de ingreso: `booking_fees`.
- Residuos y botellas de un solo uso: `rules`. Anexo 2023 y folleto 2024 lo mencionan.
- Centro de interpretación Romerales: el folleto 2024 lo cita como proyecto, no como servicio vigente. No entrada.
- Permiso de filmación comercial: `rules` (ya listado en §6.1).

### 8.8 Limpieza pendiente (no hecha)
- `services/evidence/uton_3dfb6bc5.html` y `.txt`: contenido de apuestas no relacionado. Siguen en la carpeta. Pendiente de aprobación para borrar.
- Etiquetas duplicadas fuera de services: `activities.otun_cedral_walk` y `access.cedral_walk_distances` tienen la misma etiqueta normalizada. Lo reporta el dueño de esas secciones.

## Coordinator note 2026-11-21

- `services/evidence/uton_3dfb6bc5.html` and `.txt` (unrelated gambling content) were deleted with user approval.
- `services/evidence/uton_3b654e8f.html` was deleted by mistake and re-fetched the same day. `https://www.operacionnevados.co/` now redirects to `https://www.visitnevados.co/` (HTTP 200); the re-fetched page still names "Unión Temporal Operación Nevados", the Reservas menu and the Palermo address. `.txt` regenerated from the HTML.

## 9. Ronda 2 (2026-11-21, brief de coordinación): auditoría de citas y ampliación

Esta ronda sigue `coordination/ROUND2_BRIEF.md` y `coordination/EVIDENCE_PROTOCOL.md`. La sección se construye desde el snapshot congelado: `python3 coordination/build_from_snapshot.py services` aplica `services/source/overlay.py`. La sección 8 de este documento describe una ronda anterior con el generador antiguo; ese generador ya no es la fuente.

### 9.1 Resultado
| Métrica | Antes | Después |
|---|---|---|
| Entradas | 24 | 26 |
| Ejemplos | 300 | 326 |
| Entradas eliminadas | — | ninguna |
| Entradas nuevas | — | `services.porter_requirements`, `services.mule_luggage_registered_only` |
| Citas verificadas | — | 90 (`check_quotes.py`: 26/26 entradas con bloque; 25 cifras trazadas a su archivo bruto) |

Gates: `coordinator_fixes.py` aplicado; `validate_knowledge.py`: `Errors: 0; review flags: 2` (ninguna de services); auditoría de fuentes (`check_sources.audit`, sin escribir `source_audit.json`): 0 URL de inicio, 0 cifras sin evidencia; 0 ejemplos duplicados entre secciones; hard negatives válidos.

Nota sobre `polish/services.json`: el coordinador aplica parches de redacción solo mientras el texto coincida con la base de la versión anterior. Los textos de esta ronda no coinciden, así que sus respuestas no se sobrescriben. Sí se intercambian algunos ejemplos ya listados en ese archivo.

### 9.2 Auditoría de entradas existentes (24)
Cambios de respuesta:
- `brisas_visitor_center`, `cisne_visitor_center`: "4.100" pasa a "4100", que es como lo escribe la ficha de PNN (`check_sources` busca la cifra tal cual). Se añade cierre con acción.
- `first_aid_points`: reescrita. Antes decía que solo había un punto en Arenales. Ahora: punto de primeros auxilios en la cabaña de Arenales; Brisas y Arenales con enfermería (informe 2024); Potosí, Laguna del Otún, Cisne, Valle del Cocora, Juntas y Anzoátegui figuran como necesidades, no como servicio confirmado.
- `potosi_cabin`: reescrita. Es punto de control y vigilancia (informe 2024), a 3920 m (ficha). El hospedaje y la alimentación son del refugio Potosí de Campo Alegre, en el límite del parque (2024).
- `otun_lodging`: el texto de la ficha sobre "casas tradicionales" sí está citado. Se aclara que los datos de hospedaje y porteo vienen del plan 2017-2022 que cita el informe.
- `brisas_lodging`: reescrita por conflicto interno de la ficha de PNN (ver 9.5, punto 1). No afirma que haya camas.
- `porter_luggage`: reescrita con la regla de 2023: porteo solo por El Cedral, Valle de Cocora y Palomar; prohibido en Calvito y Arenales. El informe 2024 lo lista en Juntas y en Los Chilcos–Arenales; queda para confirmar con el prestador.
- `accessibility`: se elimina "En Quindío–Dulima se exige preparación previa" porque ninguna fuente lo dice. La ficha dice "el terreno es más exigente".
- `quindio_dulima`: la ficha de PNN (2026) menciona puntos de atención en Valle del Cocora, Juntas y Anzoátegui. El informe 2024 los lista como necesidades. La respuesta lo dice así.
- `lost_items`: se añade que el personal de PNN no se responsabiliza por objetos extraviados (anexo 2023). El correo se presenta como consulta general, no como canal de objetos.
- `official_sites`: se quita "Hazlo con conexión". Se deja de citar la página de inicio de UTON como fuente; la ficha enlaza su página.
- `uton_services`, `camp_showers`, `interpretive_guiding`: se añade cierre con acción. `uton_services` añade "Pregunta a UTON qué servicios operan el día de tu visita."
- `guide_radios`: se elimina "certificado de primeros auxilios de 20 horas" del detalle; no aparece en ninguna fuente revisada.
- `phone_signal`: el detalle ya no atribuye a la publicación 2026 "adquirir equipos de radiocomunicaciones". Sí dice "la consolidación de radiocomunicaciones", que es lo que aparece en el texto.
- Fuentes: cada entrada cita solo los archivos brutos que usan sus citas (`evidence/quotes.md`).

Sin cambios de respuesta: `north_food`, `toilets`, `tolima_lodging`, `shop_ecotienda`, `refugio_cabin`, `drinking_water`, `charging_power`, `town_lodging_rnt`.

### 9.3 Entradas nuevas (2)
- `services.porter_requirements` (fact): requisitos del porteador según el anexo 2023 (local, mayor de edad, registrado en la base de datos de porteadores). Ejemplos: 14. Hard negatives: dos ejemplos de `porter_luggage`.
- `services.mule_luggage_registered_only` (fact): el anexo 2023 prohíbe el ingreso de equinos y mulares con fines turísticos (cabalgatas). La carga de equipaje con mulas solo la hacen arrieros avalados, con autorización de un funcionario. Ejemplos: 12. Hard negatives: dos ejemplos de `activities.horseback_not_allowed`.

### 9.4 Fuentes
Descargas nuevas: ninguna en esta ronda. Se reutilizaron los brutos ya guardados, con la fecha de acceso de la ronda 1 (2026-11-21):
| Archivo bruto (`services/evidence/raw/`) | URL |
|---|---|
| `pnn_nevados.txt` / `.html` (copia; el original sigue en `services/evidence/`) | https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ |
| `pnn_informe_necesidades_2024.txt` / `.docx` | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx |
| `anexo_pnn_nevados_2023.txt` / `.pdf` | https://parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf |
| `poe2026.txt` / `.pdf` | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf |
| `nevados_2024_07.txt` / `.pdf` | https://www.parquesnacionales.gov.co/wp-content/uploads/2024/07/nevados.pdf |
| `radicado_20266200001002.txt` / `.pdf` | https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-No.-20266200001002.pdf |
| `mincit_que_es_rnt.html` | https://www.mincit.gov.co/minturismo/analisis-sectorial-y-promocion/registro-nacional-de-turismo/que-es-el-registro-nacional-de-turismo |
| `mincit_invita_renovar_rnt_2026.html` | https://www.mincit.gov.co/prensa/noticias/turismo/mincit-invita-renovar-registro-nacional-de-turismo |
| `villamaria_rendicion_dic2025.txt` / `.pdf` | https://villamaria-caldas.gov.co/Participa/Documents/INFORME%20RENDICION%20%20DE%20CUENTAS%20DICIEMBRE%202025%20.pdf |
| `uton_3b654e8f.html` / `.txt` (página de inicio de visitnevados.co; no citada en entradas) | https://www.visitnevados.co (la nota del coordinador indica redirección desde operacionnevados.co) |

Movimientos de archivos en esta ronda: los brutos de `new/`, `poe2026/`, el `.docx` y el `.txt` del informe, y `uton_3b654e8f.*` pasan a `services/evidence/raw/`. `docx_core/` también pasa a `raw/`. Se conservan en `evidence/`: `pnn_nevados.html/.txt` (otras secciones citan esa ruta en sus notas y guías), `quotes-2026-11-21.md` (histórico, ya superseded por `quotes.md`), `validate_services.py` y `other_sections_examples.json`. Las rutas de §1 y §8.2 de este documento y las de `quotes-2026-11-21.md` ya no existen tal cual; la ruta vigente es `services/evidence/raw/`.

### 9.5 Conflictos
1. Alojamiento en Brisas: la ficha de PNN dice en un pasaje que UTON gestiona "alojamiento" y en otro lo omite. Sin resolver. La respuesta no afirma camas.
2. Porteo: anexo 2023 (solo sector sur; prohibido en Calvito y Arenales) frente a informe 2024 (lista Juntas y Los Chilcos–Arenales). Se sigue la norma de 2023. Pendiente para el dueño de `access` o `activities`.
3. Altitud de Brisas: ficha 4100 m (inicio del trayecto) frente a informe 4150 m (tabla de emergencias). Se usa 4100, con el detalle.
4. Altitud de Potosí: ficha 3920 m frente a informe 3800 msnm (tabla de emergencias). Se usa 3920.
5. Quindío–Dulima: ficha 2026 (puntos de atención con horario) frente a informe 2024 (necesidades). Los horarios no entran en `services`; son de `hours_status`.
6. Capacidad de El Cisne: 32 personas viene del plan 2017-2022 que cita el informe. No se publica como capacidad actual.
7. Dirección de la oficina de PNN en Manizales (anexo 2023 frente a carta de 2026): no es de `services`, ya registrada en §8.5 para `access` y `hours_status`.

### 9.6 Vacíos (sin fuente oficial o con dueño de otra sección; no hay entrada)
- Cajeros o ATM: ninguna fuente. Pagos de entrada: `booking_fees.entry_payment_channels` ya lo cubre.
- Alquiler de equipo: ninguna fuente.
- Señal o cobertura celular actual, carga de batería, accesibilidad para movilidad reducida, agua potable dentro del parque: ninguna fuente. Las entradas que lo dicen son "no confirmado" con búsqueda registrada en `quotes.md`.
- Baños y comida fuera de Brisas, Arenales, El Cisne, Potosí, El Bosque y Termal Cañón: el informe 2024 no los menciona.
- Parqueadero en las rutas de El Cisne (informe 2024): dueño `access` (`access.parking_at_brisas` existe; falta el de Cisne).
- Charla de inducción por ruta: dueño `booking_fees` o `activities` (`activities.induction_talk` existe).
- Registro de guías y operadores: dueño `booking_fees` (`guide_required`, `registered_operator_choice`). Los requisitos del anexo ya aparecen citados en `guide_radios` e `interpretive_guiding`.
- Transporte interior: `access.no_park_shuttle` existe. Horario de oficinas UTON: `hours_status.uton_concession_office_hours` existe.
- Estado de cabañas La Cueva y Laguna del Otún: solo estado de 2024 en la tabla del informe; sin uso de servicio claro. No añadido.
- Objetos perdidos: no hay procedimiento publicado.

### 9.7 Verificación y límites
- `services/check_quotes.py`: 90 citas verbatim, 26/26 entradas cubiertas, 25 cifras trazadas, 0 fallos.
- Validador de conocimiento: 0 errores; ninguna advertencia de services.
- No se verificó el estado actual de ningún dato de 2024 (horarios, camas, mantenimiento, cabañas). Esos datos siguen marcados con su año.
- No hay commit.
