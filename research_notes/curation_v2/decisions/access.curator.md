# access curator — decision log

## Environment proof (2026-11-22)

- (a) `fetch_evidence.py` OK: HTTP 200, `research_notes/curation_v2/evidence/access/pnn-nevados-portal.txt`, sha256_raw `d450bfb6b6c942433668a9fdd70da35818edbbc77d772866291bdef5827990a5`, fetched_at `2026-11-22T16:45:40+00:00`.
- (b) `uv run python --version` OK: Python 3.14.8.
- (c) `knowledge.py inspect --id access.how_to_choose_sector` OK: `"status": "ok"`, section `access`.

## Operaciones (una línea por op)

- `access.cedral_walk_distances`: update | Ajustar label a 'distancia caminando desde El Cedral al Otún', eliminar mención a tiempo no publicado y blindar con hard negatives | metadata_only
- `access.operator_transport_other`: update | Clarificar label a 'transporte con operadores turísticos fuera de Brisas' para diferenciarlo de UTON en Brisas | metadata_only
- `access.control_coordinates`: update | Precisar label a 'coordenadas geográficas de los puntos de control', enriquecer consultas GPS y contrastar con puntos de control | metadata_only
- `access.departments_of_access`: update | Clarificar label a 'departamentos con vías de acceso al parque' y contrastar con municipios específicos | metadata_only
- `access.always_by_land`: update | Enfocar label en 'acceso exclusivamente por transporte terrestre al parque' y contrastar con horarios y tarifas | metadata_only
- `access.esperanza_murillo_corridor`: update | Diferenciar label a 'corredor vial La Esperanza a Murillo hacia Brisas' frente a la portería y al municipio | metadata_only
- `access.brisas_visitor_center`: update | Especificar label a 'portería y centro de visitantes Brisas norte' y blindar con hard negatives contra La Olleta | metadata_only
- `access.tumbas_end_altitude`: update | Precisar label a 'altitud máxima del carreteable en Valle de Tumbas' y contrastar con cota de Brisas y cima | metadata_only
- `access.hire_vehicle_brisas`: update | Enfocar label en 'contratar vehículo cubierto en el centro Brisas' y contrastar con vehículos descubiertos | metadata_only
- `access.bus_or_van_entry`: update | Diferenciar label a 'ingreso en bus microbús o buseta a Brisas' frente a automóvil particular | metadata_only
- `access.uton_brisas_transport`: update | Delimitar label a 'servicio de transporte de la concesión UTON Brisas' frente al catálogo general de servicios | metadata_only
- `access.park_or_concession_contact`: update | Clarificar label a 'contacto entre Parques Nacionales y la concesión UTON' según el trámite de acceso | metadata_only
- `access.ignore_single_kilometer`: update | Enfocar label en 'discrepancias de kilometraje en la vía a Brisas' para resolver colisiones por mojones kilométricos | metadata_only
- `access.dirt_roads_cisne`: update | Precisar label a 'estado de carreteras terciarias destapadas hacia El Cisne' y contrastar con vías pavimentadas | metadata_only
- `access.choose_otun_trailhead`: update | Diferenciar label a 'elegir punto de partida hacia Laguna del Otún' entre vía Potosí y camino El Cedral | metadata_only
- `access.road_visit_or_trail`: update | Clarificar label a 'diferencia entre sectores vehiculares y rutas a pie' entre Brisas y sectores de trekking | metadata_only
- `access.organized_tour_transport`: update | Diferenciar label a 'llegar en excursión o paquete turístico organizado' con agencias privadas frente a UTON | metadata_only
- `access.from_murillo`: update | Especificar label a 'cómo llegar en vehículo desde Murillo a Brisas' para separarlo de Manizales y del transporte público | metadata_only
- `access.stay_on_official_gate`: update | Enfocar label en 'obligación de ingresar únicamente por porterías oficiales autorizadas' frente a caminos no regulados | metadata_only
- `access.el_cisne_approach`: update | Enfocar label en 'aproximación vehicular y acceso al centro El Cisne' por carreteras terciarias | metadata_only
- `access.from_pereira_cedral`: update | Diferenciar label a 'cómo llegar de Pereira al inicio El Cedral' detallando la ruta por La Florida | metadata_only
- `access.cocora_before_park`: update | Precisar label a 'distancia desde Valle del Cocora al límite' delimitando el tramo de 14 km | metadata_only
- `access.from_anzoategui_palomar`: update | Especificar label a 'cómo llegar desde Anzoátegui por vereda Palomar' para el acceso por Tolima sur | metadata_only
- `access.three_south_paths`: update | Enfocar label en 'tres senderos peatonales de acceso al sector sur' (Cocora, Juntas y Palomar) | metadata_only
- `access.mountain_road_conditions`: update | Enfocar label en 'condiciones cambiantes en vías destapadas de montaña' y ausencia de parte en tiempo real | metadata_only
- `access.santa_rosa_vs_cedral`: update | Diferenciar label a 'diferencia entre Santa Rosa y El Cedral' separando acceso vehicular a Potosí de caminata pedestre | metadata_only
- `access.own_car_brisas`: update | Enfocar label en 'llegar en automóvil particular propio a Brisas' diferenciándolo de buses y tours | metadata_only
- `access.from_pereira_choose`: update | Enfocar label en 'elección de ruta de acceso saliendo de Pereira' hacia El Cedral o hacia Potosí | metadata_only
- `access.bus_to_letras`: update | Diferenciar label a 'bus intermunicipal de Manizales hasta páramo de Letras' frente a la carretera y caseta | metadata_only
- `access.letras_highway`: update | Especificar label a 'carretera nacional Manizales a Bogotá por Letras' separándola de la portería del parque | metadata_only
- `access.letras_not_the_gate`: update | Enfocar label en 'aclaración sobre que Letras no es la portería' con contrastes directos hacia Brisas | metadata_only

## No comprobado, huecos, descargas, cruces

- Entradas sin revisar: ninguna. Las 78 entradas tienen fila completa en `audit/access.csv` con evidencia de lectura verificada (`primary_ok`).
- Hueco: no hay tiempo de viaje vehicular oficial vigente en la ficha de Parques para los tramos Manizales-Brisas, Bogotá-Brisas o Medellín-porterías; se mantiene la recomendación de consultar al operador.
- Hueco: no existe parte del día en tiempo real para las vías terciarias destapadas hacia El Cisne y Potosí; Invías solo reporta la red primaria nacional.
- Hueco: no hay datos oficiales publicados de capacidad ni mapa de parqueaderos en el centro Brisas.
- Hueco: no existen rutas publicadas de servicio de taxi regulado hasta las porterías del parque.
- Descargas fallidas: ninguna. La descarga de prueba de `fetch_evidence.py` (`pnn-nevados-portal.txt`) completó con HTTP 200 y sha256 validado.
- Cruces: documentados en `research_notes/curation_v2/findings/access.cross.json` (7 hallazgos entre access, services, hours_status, booking_fees, activities y geography).
- Verificaciones:
  - `knowledge.py stage`: `status: staged`, warnings vacíos (`orphaned_hard_negatives: []`, `similar_labels: []`).
  - `verify_evidence.py`: `fail: []`, `flags: []`, `warn: []`.
  - `route_check.py`: `n_removed_not_routing: 0`, `removed_examples: 0`.
  - `audit_check.py`: `fail: []`, 78 filas, 78 `primary_ok`.
