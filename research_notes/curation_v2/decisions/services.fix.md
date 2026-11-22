# Decision Log: Fix Round v2 (Section `services`)

Curator: Agent 11 (services)
Fecha: 2026-11-22

## 1. Review items (`reviews/services.review.json`)

- `services.brisas_visitor_center`: done (op aprobada v1 conservada byte a byte; fila de auditoría clarifica 4100 m en ficha web PNN 2026 vs 4150 m en informe 2024).
- `services.north_food`: done (conservada etiqueta 'comida en Brisas y Arenales'; retirado ejemplo casi duplicado de `_examples.json`).
- `services.toilets`: done (op aprobada v1 conservada byte a byte).
- `services.first_aid_points`: done (op aprobada v1 conservada byte a byte).
- `services.cisne_visitor_center`: done (op aprobada v1 conservada byte a byte; fila de auditoría clarifica que 4100 m proviene de ficha web PNN nov 2026 frente a 4180 m del informe mayo 2024).
- `services.potosi_cabin`: done (op aprobada v1 conservada byte a byte).
- `services.otun_lodging`: done (conservada etiqueta anterior 'casas de hospedaje en El Bosque').
- `services.tolima_lodging`: done (conservada etiqueta anterior 'hospedaje en Termal Cañón y La Primavera').
- `services.brisas_lodging`: done (conservada etiqueta anterior 'camas en Brisas: confirmar con UTON'; retirados 2 ejemplos de `_examples.json`).
- `services.porter_luggage`: done (op aprobada v1 conservada byte a byte; documentado conflicto Juntas/Chilcos con informe 2024 en fila de auditoría).
- `services.uton_services`: done (op aprobada v1 conservada byte a byte).
- `services.guide_radios`: done (conservada etiqueta 'radios que llevan los guías'; restaurado ejemplo 'el guía lleva botiquín?'; retirado ejemplo casi duplicado).
- `services.phone_signal`: done (conservada etiqueta anterior 'señal de celular en el parque').
- `services.charging_power`: done (conservada etiqueta anterior 'carga de celular o batería'; fila de auditoría verificada en quote_missing sin primary_ok).
- `services.accessibility`: done (conservada etiqueta anterior 'accesibilidad para movilidad reducida').
- `services.drinking_water`: done (conservada etiqueta anterior 'agua para tomar en el parque').
- `services.shop_ecotienda`: done (conservada etiqueta anterior 'tienda y ecotienda del norte').
- `services.refugio_cabin`: done (conservada etiqueta anterior 'cabaña El Refugio no habilitada'; retirado ejemplo casi duplicado).
- `services.camp_showers`: done (op aprobada v1 conservada byte a byte).
- `services.official_sites`: done (conservada etiqueta 'dónde confirmar servicios en línea'; restaurado ejemplo 'cómo confirmo antes de viajar').
- `services.quindio_dulima`: done (conservada etiqueta anterior 'servicios en Quindío–Dulima').
- `services.interpretive_guiding`: done (adoptada etiqueta 'guías registrados para los senderos' de labels.json / revisión).
- `services.town_lodging_rnt`: done (conservada etiqueta anterior 'alojamiento en pueblos cercanos y RNT').
- `services.lost_items`: done (op aprobada v1 conservada byte a byte).
- `services.porter_requirements`: done (conservada etiqueta anterior 'requisitos para ser porteador'; excerpt de auditoría corregido al bloque completo del anexo 2023).
- `services.mule_luggage_registered_only`: done (op aprobada v1 conservada byte a byte).

## 2. Examples drop items (`reviews/_examples.json`)

- `services.north_food` ("venden desayuno o almuerzo para visitantes en Arenales"): done (retirado).
- `services.brisas_lodging` ("hay habitaciones disponibles para turistas en el sector Brisas"): done (retirado).
- `services.brisas_lodging` ("se puede reservar noche de hospedaje en la cabaña de Brisas"): done (retirado).
- `services.refugio_cabin` ("cuál es el estado actual de la cabaña El Refugio"): done (retirado).
- `services.guide_radios` ("es obligatorio que los guías y operadores registrados tengan radio"): done (retirado).
- `services.toilets` ("dónde hay baños para visitantes en el parque"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.
- `services.first_aid_points` ("dónde hay puntos de primeros auxilios y atención médica en el parque"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.
- `services.potosi_cabin` ("el refugio Potosí en Campo Alegre ofrece hospedaje y comida?"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.
- `services.camp_showers` ("las duchas de la cabaña de Arenales están en servicio"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.
- `services.camp_showers` ("instalaciones sanitarias y duchas para campistas en Arenales"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.
- `services.lost_items` ("perdí un objeto personal o morral en el parque"): declined: op aprobada en v1; review_gate prohíbe modificar ops aprobadas.

## 3. Findings

- `labels.json` (`services.interpretive_guiding` -> 'guías registrados para los senderos'): done.
- `critical.json` (`services.charging_power`): done (respuesta negativa orientativa preservada sin afirmar existencia de tomas públicas; source_status en quote_missing).
- `contradictions.json` (`services.potosi_cabin` altitud): done (documentada en auditoría; op aprobada sin cambios).
- `contradictions.json` (`services.porter_luggage` rutas autorizadas vs informe 2024): done (conflicto Juntas/Chilcos explícito en notas de auditoría).
- `contradictions.json` (`services.brisas_lodging` vs `services.uton_services`): done (incertidumbre de camas en Brisas explícita en label y respuesta).
- `taxonomy.json` (`services.cisne_visitor_center` vs `activities.camping_cisne`): done (resuelto en v1; aprobado).
- `taxonomy.json` (`services.mule_luggage_registered_only` vs `activities.horseback_not_allowed`): done (resuelto en v1; aprobado).
- `cross.json` (`access`, `activities`, `preparation`, `hours_status`, `booking_fees`): done (contrastes delimitados mediante etiquetas y hard_negatives en v1/v2).
