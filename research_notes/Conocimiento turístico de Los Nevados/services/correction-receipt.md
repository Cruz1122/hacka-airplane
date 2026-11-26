# Recibo de corrección: services (2026-11-21)

Sección: `data/knowledge/sections/services.json`. Ronda 1 preservada en `coordination/round1/services.json`.
Resultado: 21 entradas (antes 27), 259 ejemplos, schema OK, validador local OK.

## Hallazgos del revisor

| # | Hallazgo | Resolución | Estado |
|---|---|---|---|
| 1 | Alcance: `research_permits` pertenece a `rules` | Eliminada de services. Ejemplos de filmación comercial listados en el log (§6.1) para `rules` | Resuelto en services. `rules` debe fusionar |
| 2 | Alcance: `registered_providers` y `charla_induccion` pertenecen a `booking_fees` | Eliminadas de services. REPSE ya está en `booking_fees.registered_operator_choice`. La charla obligatoria no tiene entrada en `booking_fees` | Parcial. Charla pendiente de asignación |
| 3 | `uton_offices` une dos direcciones como si ambas fueran oficinas oficiales | Ambas direcciones tienen soporte oficial: PNN lista "Carrera 26A #68-44, barrio Palermo" y "Calle 70 #27-70". UTON inicio muestra "Cl 70 # 27-70 - Palermo". Entrada eliminada de services por duplicar `access.uton_offices_manizales` y `hours_status` | Resuelto (movido) |
| 4 | `potosi_cabin` no distingue la cabaña del parque del refugio comunitario | Reescrita: la cabaña es punto de control (PNN). El hospedaje y la comida son del refugio Potosí de Campo Alegre (informe 2024). Sin implicar alojamiento en la cabaña | Resuelto |
| 5 | `brisas_lodging` muestra historial de fuentes en la respuesta | Respuesta corta de confirmación con UTON. El conflicto va a `detail`: PNN se contradice dentro de su propia página (con y sin "alojamiento") | Resuelto |
| 6 | `charging_power`: la respuesta narra "No encontré un dato oficial" y el ejemplo "cargador" es ambiguo | Respuesta: "No tengo confirmado dónde cargar el celular..." Empaque breve. Ejemplo "cargador" eliminado | Resuelto |
| 7 | `cabin_status_2024` y `refugio_cabin`: fecha no explícita o estado implícito | `cabin_status_2024` fusionado en cabañas. Fechas 2024 explícitas en `refugio_cabin`, `camp_showers` y `potosi_cabin`. Sin afirmar estado actual | Resuelto |
| 8 | Requisito: resolver UTON con ambas direcciones | Ya verificado (ver #3) | Resuelto |

## Requisitos transversales

| Requisito | Estado |
|---|---|
| Revisar todas las entradas, no solo las cinco muestreadas | Hecho: las 27 entradas originales se revisaron contra la evidencia guardada. 6 eliminadas, 21 corregidas o conservadas |
| Preservar semillas (`assignments.json`) | `services` tiene `seed_indexes: []`. Nada que preservar |
| Título, perfil y orden exactos | Sí: "Servicios del parque", `lookup`, orden 10 |
| Esquema exacto | jsonschema: 0 errores. `steps` no se incluye (null no es válido) |
| ≥ 12 ejemplos, 1–2 en inglés, typos y acentos | 12–13 ejemplos, 1–2 en inglés por entrada |
| Etiquetas de 3–8 palabras, distintas | Sí. Sin colisiones de etiqueta con otras secciones |
| 2–4 hard negatives | 2 por entrada. Los 42 son ejemplos de otra entrada |
| 1–2 variantes | 1 por entrada |
| 1–3 related locales | 2–3 por entrada, todos locales |
| 4–8 preguntas de aclaración, slots | 6 preguntas; slot `sector` |
| Sin comentario de autor ni plantillas oiga/venga/parce | Sí: 0 apariciones |
| Duplicados exactos o casi duplicados entre secciones | 0 exactos; 0 casi duplicados (≥ 0,9) |
| Fuente real con fecha y cita | Cada entrada cita fuentes leídas (ver log §1). La página de UTON `uton_3dfb6bc5` se excluyó: es contenido de apuestas no relacionado |
| Cifras con pasaje oficial fechado | 4.100 m y 3.920 m (PNN 2026); "dos baterías" y datos 2024 (informe); 2017–2022 (plan citado). Retirada la capacidad de 32 personas |
| Gaps documentados | Señal, carga, accesibilidad, agua potable, camas en Brisas y estado 2026 quedan en el log (§6.2) |

## Pendiente para otros dueños (no tocado)

1. `booking_fees`: asignar la charla de inducción obligatoria (hoy solo en `activities.induction_talk`).
2. `rules`: fusionar la intención de filmación comercial y permisos (candidatos en el log §6.1).
3. `activities` y `access`: conflicto del porteo en Arenales (informe 2024 vs reglamentación 2023 citada en otra sección). También solapan con `services.porter_luggage` y `services.brisas_visitor_center`.
4. Eliminar `services/evidence/uton_3dfb6bc5.html` y su `.txt` (contenido de apuestas).

Fuera de alcance: `weather_volcano`, `preparation`, `hours_status`, `fauna`, `flora_ecosystems`. No se modificaron.
