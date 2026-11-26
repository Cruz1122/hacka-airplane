# Decision Log — Curator `services` (Agent 11, Round 2)

## Operations Log (One line per op)
- `services.brisas_visitor_center`: update | Clarificar label a 'taquilla y centro de inducción Brisas', diferenciar de alojamiento/comida y enriquecer consultas | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt
- `services.north_food`: update | Clarificar label a 'restaurantes y comida en Brisas y Arenales', blindar contra sanitarios y alojamiento | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.toilets`: update | Clarificar label a 'servicios sanitarios y baños para visitantes', restaurar consulta real corta 'baños' y contrastar con baños termales | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.first_aid_points`: update | Clarificar label a 'puntos de primeros auxilios y enfermería', restaurar consulta real corta 'primeros auxilios' y añadir contrastes con hipotermia | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.cisne_visitor_center`: update | Clarificar label a 'alojamiento y camas en centro El Cisne' y diferenciar de acampada con carpa | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.potosi_cabin`: update | Clarificar label a 'cabaña de control Potosí y refugio Campo Alegre' y diferenciar puesto de control de refugio comunitario | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.otun_lodging`: update | Clarificar label a 'hospedaje campesino en vereda El Bosque' y blindar con hard negatives contra camping en laguna del Otún | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.tolima_lodging`: update | Clarificar label a 'fincas de hospedaje en sector Tolima' y blindar contra confusión con camping transitorio | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.brisas_lodging`: update | Clarificar label a 'disponibilidad de alojamiento y camas en Brisas' y contrastar con taquilla y centro de inducción | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt
- `services.porter_luggage`: update | Clarificar label a 'rutas autorizadas para porteo de maletas', restaurar consultas reales cortas 'porteo' y 'porteador', contrastar con requisitos y mulas | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.uton_services`: update | Clarificar label a 'servicios operados por la concesión turística UTON', restaurar sigla real 'UTON' y blindar contra transporte/reserva | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.guide_radios`: update | Clarificar label a 'radios de comunicación obligatorios de los guías', retirar 'el guía lleva botiquín?' por pertenecer a health_safety, contrastar con botiquín | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.phone_signal`: update | Clarificar label a 'cobertura y señal de celular en el parque', restaurar consulta real corta 'señal' y contrastar con radios de guías | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.charging_power`: update | Clarificar label a 'puntos para cargar celulares y baterías eléctricas', enriquecer consultas sobre tomas y orientar sobre powerbank | none (quote_missing en fuentes oficiales)
- `services.accessibility`: update | Clarificar label a 'accesibilidad para visitantes con movilidad reducida', restaurar consulta real corta 'accesibilidad' y contrastar con exenciones | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt
- `services.drinking_water`: update | Clarificar label a 'disponibilidad de agua potable en el parque', enriquecer consultas sobre bebederos y contrastar con hidratación previa | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt
- `services.shop_ecotienda`: update | Clarificar label a 'tienda de recuerdos y ecotienda en el norte', restaurar consultas reales cortas 'tienda' y 'ecotienda', contrastar con snacks | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.refugio_cabin`: update | Clarificar label a 'cabaña El Refugio no habilitada para dormir', enriquecer consultas sobre estado cerrado y pernocte | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.camp_showers`: update | Clarificar label a 'duchas y cocina en cabaña de Arenales', restaurar consulta real corta 'duchas' y diferenciar de higiene en campamento | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.official_sites`: update | Clarificar label a 'sitios web oficiales para verificar servicios', retirar consulta genérica 'cómo confirmo antes de viajar' por solapamiento con vías | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt
- `services.quindio_dulima`: update | Clarificar label a 'servicios turísticos en sector Quindío Dulima' y blindar contra descripción geográfica del sector | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_informe_necesidades_2024.txt
- `services.interpretive_guiding`: update | Clarificar label a 'servicio de guianza ambiental e interpretativa autorizada' y contrastar con senderismo interpretativo | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.town_lodging_rnt`: update | Clarificar label a 'hoteles y hospedajes con RNT en municipios cercanos' y blindar contra confusión con rutas de buses | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/mincit_que_es_rnt.html
- `services.lost_items`: update | Clarificar label a 'objetos y pertenencias personales extraviadas' y blindar con hard negatives contra reporte de personas extraviadas | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.porter_requirements`: update | Clarificar label a 'requisitos y acreditación de porteadores autorizados' y agregar preguntas sobre acreditación de arrieros | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt
- `services.mule_luggage_registered_only`: update | Clarificar label a 'transporte de carga con mulas y arrieros autorizados' y blindar con hard negatives contra cabalgatas | research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt

## Entries Not Checked
Ninguna. Todas las 26 entradas de `services` fueron leídas e inspeccionadas contra la evidencia histórica fijada (Phase 2). Se verificó que 25 entradas cuentan con pasajes textuales de respaldo directo en los documentos oficiales (`primary_ok`), mientras que 1 entrada (`services.charging_power`) carece de mención en fuentes oficiales (`quote_missing`), manteniendo una respuesta negativa orientativa honesta.

## Factual Gaps
1. `services.charging_power`: ninguna fuente oficial (PNN 2026, informe necesidades 2024, POE 2026) menciona disponibilidad de tomas de corriente públicas en cabañas o refugios. Se mantiene como vacío con recomendación práctica de powerbank.
2. `services.accessibility`: no existe protocolo ni datos oficiales de accesibilidad física o rampas para visitantes con movilidad reducida en el área protegida. La respuesta se restringe a señalar la exigencia del terreno montañoso y recomendar consultar a PNN.
3. `services.phone_signal`: sin cobertura celular confirmada en el parque; la reglamentación 2023 solo exige radios con frecuencia obligatoria a los guías.
4. `services.drinking_water`: sin puntos de agua potable confirmados en los senderos; se mantiene recomendación de hidratación oficial de PNN y llevar agua propia.

## Sources That Failed to Download
Ninguna. No se requirieron descargas web adicionales; se utilizaron las fuentes oficiales previamente descargadas y fijadas en el manifiesto de evidencia legacy bajo `research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/`.

## Cross-Section Findings
Registrados en `findings/services.cross.json`:
1. `services.uton_services` vs `access.uton_brisas_transport` y `booking_fees.brisas_booking_channel`: delimitación de concesión general vs transporte específico y compra de boletos.
2. `services.cisne_visitor_center` vs `activities.camping_cisne`: delimitación de camas en centro de visitantes vs acampada en carpa.
3. `services.mule_luggage_registered_only` vs `activities.horseback_not_allowed`: delimitación de porteo de equipaje en mulas vs prohibición de cabalgatas turísticas.
4. `services.lost_items` vs `actions.report_lost_person`: delimitación de objetos olvidados vs emergencia por personas extraviadas.
5. `services.camp_showers` vs `preparation.camp_hygiene`: delimitación de duchas en Arenales vs pautas de higiene personal en campamento.
6. `services.toilets` vs `activities.therapeutic_baths_banned`: conservación de 'baños' en services.toilets y diferenciación con label ('servicios sanitarios y baños para visitantes') y hard negatives hacia baños termales.

## Removed Examples Justification
Se eliminaron únicamente 2 ejemplos en toda la propuesta:
1. `services.guide_radios`: se retiró 'el guía lleva botiquín?' porque corresponde estrictamente a la intención médica/primeros auxilios de `health_safety.guide_first_aid_kit_and_certification`.
2. `services.official_sites`: se retiró 'cómo confirmo antes de viajar' por ser una consulta excesivamente genérica que colisiona con la confirmación del estado vial en `access.confirm_road_before`.
Ambos casos fueron verificados mediante `route_check.py`, resultando en `n_removed_not_routing: 0`.
