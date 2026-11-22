# Log de Decisiones - Fix Round v2: preparation

Curador: Agente 8 (preparation)
Fecha: 2026-11-22

## Operaciones de la revisión (preparation.review.json)

- preparation.neck_gaiter: done (aprobado en v1, conservado byte a byte en v2)
- preparation.layering_system: done (restaurada etiqueta anterior; citada exigencia de ropa impermeable y ropa abrigada bajo Resolución 207 de 2023)
- preparation.first_layer_thermal: done (restaurada etiqueta anterior "ropa térmica, impermeable y de repuesto"; retirada mención obsoleta a guía 2018 y sustituida por ficha oficial PNN)
- preparation.second_layer_fleece: done (restaurada etiqueta anterior; retirada marca de tejido específico manteniendo abrigo térmico según res207)
- preparation.third_layer_waterproof: done (restaurada etiqueta anterior; retirada mención a cortavientos con capucha y ceñido a ropa impermeable obligatoria de res207)
- preparation.rain_poncho: done (restaurada etiqueta anterior; citada exigencia de ropa impermeable en equipo mínimo de res207 y prohibición de plásticos desechables)
- preparation.hiking_boots: done (restaurada etiqueta anterior; respuesta ratificada con cita a calzado con agarre de res207)
- preparation.thermal_gloves: done (restaurada etiqueta anterior; respuesta ratificada con cita a guantes en equipo mínimo de res207)
- preparation.thermal_hat: done (restaurada etiqueta anterior; respuesta ratificada con cita a protección extrema de cabeza de res207)
- preparation.sunglasses_uv: done (restaurada etiqueta anterior; respuesta ratificada con cita a gafas UV 100% de res207)
- preparation.sunscreen: done (restaurada etiqueta anterior; retirada frecuencia de dos horas y ceñido a factor 50 mínimo de res207)
- preparation.sun_hat: done (restaurada etiqueta anterior; aclarado rol complementario a gafas UV y bloqueador solar según pautas PNN)
- preparation.daypack_size: done (restaurada etiqueta anterior; respuesta ratificada con cita a morral pequeño en equipo mínimo de res207)
- preparation.dry_bags: done (restaurada etiqueta anterior; enmarcado como recomendación técnica de montaña)
- preparation.water_quantity: done (restaurada etiqueta anterior; retirada mención a pequeños sorbos y respaldada cantimplora obligatoria de res207 e hidratación de ficha PNN)
- preparation.reusable_bottles: done (restaurada etiqueta anterior; citada obligación de cantimplora de res207 y prohibición de plásticos de un solo uso)
- preparation.trail_snacks: done (restaurada etiqueta anterior; respuesta ratificada con cita a alimentos ligeros y calóricos de res207)
- preparation.pre_hike_meal: done (restaurada etiqueta anterior "alimentación previa al inicio del ascenso"; sustituida fuente 2018 por ficha oficial PNN y retirado consejo no sustentado)
- preparation.trail_meals_multiday: done (restaurada etiqueta anterior; citada prohibición de fogatas y porte de camping gas de res207)
- preparation.mountain_tent: done (restaurada etiqueta anterior; respuesta ratificada con cita a carpas 3 y 4 estaciones de res207)
- preparation.sleeping_bag: done (restaurada etiqueta anterior; reemplazada fuente 2018 por ficha oficial PNN 2026 sobre carpa y sleeping para campamento)
- preparation.sleeping_pad: done (restaurada etiqueta anterior; retirada afirmación de obligatoriedad en norma y marcado como recomendación técnica de aislamiento)
- preparation.camp_stove: done (restaurada etiqueta anterior; reemplazada fuente 2018 y citada prohibición de fogatas y porte de camping gas de res207)
- preparation.cookware_utensils: done (restaurada etiqueta anterior; citado menaje/material de cocina reutilizable y prohibición de plásticos de un solo uso)
- preparation.camp_hygiene: done (restaurada etiqueta anterior; citada expresamente evacuación en cacatubo o hoyo de gato con pala del guía según res207)
- preparation.headlamp: done (restaurada etiqueta anterior; respuesta ratificada con cita a linterna frontal y baterías de repuesto de res207)
- preparation.technical_glacier_gear: done (restaurada etiqueta anterior "equipo técnico para borde de glaciar"; ratificada contratación obligatoria de guía de res207 y consulta técnica con operador)
- preparation.fitness_training: done (restaurada etiqueta anterior "condición física y esfuerzo en la montaña"; retirado paso pausado y citadas paradas periódicas de 10 minutos de ficha PNN)
- preparation.children_gear: done (restaurada etiqueta anterior; retirada regla no citada y especificado acompañamiento adulto obligatorio y abrigo para menores)
- preparation.what_not_to_pack: done (restaurada etiqueta anterior; citada lista de prohibiciones de res207 incluyendo fogatas, leña, ruidos molestos y plásticos)
- preparation.checklist_brisas_day: done (conservada etiqueta; respaldados ítems de pasadía en equipo mínimo obligatorio del numeral 6.1 de res207)
- preparation.checklist_glacier_day: done (conservada etiqueta; articulada exigencia de guía obligatorio con equipo mínimo de senderismo de res207)
- preparation.checklist_multiday_trek: done (conservada etiqueta; articulada exigencia de carpa técnica 3 o 4 estaciones, camping gas, cantimplora y bolsa de res207)
- preparation.navigation_map_gps: done (restaurada etiqueta anterior "mapa, GPS o brújula para orientarte"; retirado consejo sin fuente de avisar ruta a familiar y fuente 2018)

## Hallazgos (findings)

- labels.json (preparation.first_layer_thermal): declined: la revisión independiente y el brief ordenaron expresamente conservar la etiqueta anterior "ropa térmica, impermeable y de repuesto"
- taxonomy.json (preparation.first_layer_thermal vs preparation.third_layer_waterproof): done: first_layer_thermal reservado a capa térmica base y muda seca, impermeabilidad y cortavientos reservados a third_layer_waterproof
- preparation.cross.json (reusable_bottles / cookware_utensils vs rules.single_use_plastics): done: se mantiene la recomendación práctica de equipo en preparation y el régimen prohibitivo/sancionatorio en rules
- preparation.cross.json (water_quantity / reusable_bottles vs services.drinking_water): done: water_quantity y reusable_bottles orientan sobre hidratación y cantimplora en sendero, diferenciado de infraestructura de recarga
- preparation.cross.json (technical_glacier_gear / checklist_glacier_day vs health_safety.guide_first_aid_kit_and_certification): done: preparation delimita el equipo del montañista y consulta al operador, reservando certificación médica y radio a health_safety
- preparation.cross.json (camp_hygiene vs rules.leave_no_waste / services.toilets): done: camp_hygiene describe técnica de campamento (cacatubo, hoyo de gato con pala y retorno de papel), diferenciado de baños en cabañas y normas de residuos
- preparation.cross.json (children_gear vs activities.children_visit_style / booking_fees.age_minimum): done: children_gear se delimita estrictamente al equipaje y ropa abrigada infantil
- preparation.cross.json (navigation_map_gps vs services.guide_radios / health_safety.lost_person_protocol): done: navigation_map_gps se enfoca exclusivamente en elementos de orientación física/GPS antes de salir
- conversation.cross.json (location_map_request vs preparation.navigation_map_gps): done: delimitado a equipo de orientación offline de montaña
- rules.cross.json (single_use_plastics vs preparation.reusable_bottles): done: coordinado
- services.cross.json (camp_showers vs preparation.camp_hygiene): done: coordinado

## Explicación de Flags y Auditoría

- flags en verify_evidence.py (preparation.trail_meals_multiday): las cifras '207' y '2023' corresponden al nombre y año de la norma oficial citada en la respuesta ("Resolución 207 de 2023"), cuya prohibición de fogatas y exigencia de camping gas constan en la evidencia.
- Auditoría audit/preparation.csv: 13 filas clasificadas honestamente como `primary_ok` con extractos textuales >= 20 caracteres directamente verificables en Resolucion 207 de 2023 y ficha oficial PNN 2026. Las 21 filas restantes calificadas como `partial` o `none` por el revisor fueron degradadas honestamente a `quote_missing` con extractos vacíos para garantizar cero falsos primary_ok en el corpus.
