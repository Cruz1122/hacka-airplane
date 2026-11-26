# Decision Log — Curator `rules` (Agent 10)

## Environment Proof (2026-11-22, before curation)

- (a) `fetch_evidence.py` OK: HTTP 200, `research_notes/curation_v2/evidence/rules/test_fetch.txt`, sha256_raw `aa9f88f344ea96cf804ceb62702e6227aa9d6f9afee685966b58353db71daec1`, fetched_at `2026-11-22T16:45:58+00:00`.
- (b) `uv run python --version` OK: Python 3.14.8.
- (c) `knowledge.py inspect --id rules.pets` OK: `"status": "ok"`, `kind: "rule"`, `in_featured: true`.

## Operations Log (One line per op)

- `rules.pets`: update | Prohibición estricta de mascotas; fijar last_verified al 2026-11-21 y label en minúsculas | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.stay_on_routes`: update | Permanecer en senderos oficiales; fijar last_verified al 2026-11-21 y label descriptivo | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.leave_no_waste`: update | Retorno obligatorio de residuos; fijar last_verified al 2026-11-21 y contrastar con residuos ajenos | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.leave_natural_objects`: update | Prohibición de extraer elementos naturales; fijar last_verified al 2026-11-21 y contrastar con introducción | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.no_introduce_species`: update | Prohibición de ingresar especies/semillas; fijar last_verified al 2026-11-21 y contrastar con extracción | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.avoid_pollutants`: update | Prohibición de verter contaminantes; fijar last_verified al 2026-11-21 y clarificar fuentes hídricas | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.avoid_chemicals`: update | Restricción de químicos y explosivos; fijar last_verified al 2026-11-21 y clarificar excepción de obras | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.commercial_photography`: update | Permiso de fotos comerciales; fijar last_verified al 2026-11-21 y contrastar con filmaciones | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt
- `rules.audiovisual_permits`: update | Permiso de rodaje audiovisual; fijar last_verified al 2026-11-21 y contrastar con foto comercial | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt
- `rules.event_permits`: update | Autorización para eventos en el parque; fijar last_verified al 2026-11-21 y contrastar con deportes | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt
- `rules.organized_sports`: update | Permiso para competencias deportivas; clarificar label y contrastar con eventos generales | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/pnn_nevados_ficha.txt
- `rules.research_permissions`: update | Permiso de investigación científica; fijar last_verified al 2026-11-21 y contrastar con extracción | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.drones`: update | Prohibición de uso de drones; fijar last_verified al 2026-11-21 y label expandido a 5 palabras | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.open_fires`: update | Prohibición estricta de fogatas; fijar last_verified al 2026-11-21 y uso de camping gas | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.noise`: update | Prohibición de ruidos molestos y parlantes; fijar last_verified al 2026-11-21 y label a 6 palabras | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.feed_wildlife`: update | Prohibición de alimentar fauna silvestre; fijar last_verified al 2026-11-21 y label a 5 palabras | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.playback`: update | Prohibición de playback para aves; fijar last_verified al 2026-11-21 y label a 7 palabras | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.camping`: update | Prohibición de acampar fuera de zonas habilitadas; fijar last_verified al 2026-11-21 y contrastar con sitios | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.fishing`: update | Prohibición de pesca en el parque; fijar last_verified al 2026-11-21 y clarificar excepción científica | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.intoxication`: update | Prohibición de alcohol y sustancias psicoactivas; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.weapons`: update | Prohibición de armas y elementos cortopunzantes; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.entry_bag_checks`: update | Controles e inspección de equipaje al ingreso; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.minors_protection`: update | Protección integral de niños y adolescentes; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.follow_park_staff`: update | Deber de acatar instrucciones del personal; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.sell_advertise`: update | Prohibición de venta y publicidad no autorizada; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.single_use_plastics`: update | Prohibición de plásticos de un solo uso; contrastar con botellas reutilizables | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.graffiti_signage`: update | Prohibición de rayar rocas y dañar señales; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.respect_communities`: update | Respeto a costumbres de comunidades locales; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.sanctions_penalties`: update | Sanciones y multas por infracciones ambientales; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.preventive_measures`: update | Medidas preventivas y decomiso de implementos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.excavations_prohibited`: update | Prohibición de excavaciones y remoción de tierra; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.rock_bolting_prohibited`: update | Prohibición de instalar anclajes o chapas en roca; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.geological_soil_samples`: update | Prohibición de tomar muestras geológicas o rocas; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.wildlife_traps_prohibited`: update | Prohibición de instalar trampas para fauna silvestre; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.wildlife_contact_displacement`: update | Prohibición de tocar, coger o desplazar fauna; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.earth_tone_clothing_wildlife`: update | Ropa de colores tierra para avistar fauna; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.aerosols_sprays_prohibited`: update | Prohibición de aerosoles y pinturas en el parque; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.burning_trash_prohibited`: update | Prohibición de quemar o incinerar basuras; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.pick_up_trail_litter`: update | Recoger basura ajena encontrada en senderos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.biodegradable_packaging_food`: update | Uso de empaques biodegradables para alimentos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.logging_clearing_vegetation`: update | Prohibición de tala o corte de vegetación; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.abandoning_gear_objects`: update | Prohibición de abandonar carpas, equipos u objetos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.damage_park_infrastructure`: update | Prohibición de dañar instalaciones y senderos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.agro_industrial_mining_ban`: update | Prohibición de actividades agropecuarias o mineras; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.authorized_stay_duration`: update | Permanecer solo durante el tiempo autorizado; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.show_entry_permit_on_request`: update | Obligación de portar y exhibir el permiso; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.tent_permit_display`: update | Fijar copia del permiso visible en la carpa; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.respect_carrying_capacity_limits`: update | Respetar capacidad de carga y tamaño de grupo; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.visitor_risk_assumption`: update | Asunción de riesgos personales y cuidado de objetos; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.report_environmental_infractions`: update | Obligación de denunciar infracciones ambientales; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.ecological_customs_checkpoints`: update | Controles en puestos de aduanas ecológicas; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.no_discrimination_scandals`: update | Prohibición de escándalos y conductas discriminatorias; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.park_closure_no_compensation`: update | Cierre temporal de atractivos sin indemnización; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.pack_animals_weight_overnight`: update | Límite de carga y descanso de mulas; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.no_mules_arenales_calvito`: update | Prohibición de mulas hacia Arenales y Calvito; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.commercial_sound_recording`: update | Autorización para grabaciones comerciales de sonido; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.researcher_deliverables_obligation`: update | Entrega de informes y muestras de investigación; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/decreto_1076_2015.txt
- `rules.sport_mountaineers_advance_request`: update | Solicitud anticipada y plan de montañismo; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.sport_mountaineers_schedule_exit_report`: update | Reporte obligatorio de salida de expedición; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt
- `rules.guide_operator_misconduct_ban`: update | Sanciones y expulsión de operadores infractores; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/poe_2026_corto.txt
- `rules.social_media_unauthorized_routes`: update | Procesos por divulgar rutas prohibidas en redes; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/carta_2026_05_11.txt
- `rules.written_reprimand_mandatory_course`: update | Amonestación escrita y curso ambiental obligatorio; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.community_service_sanction`: update | Sanción de servicio comunitario en materia ambiental; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.confiscation_restitution_specimens`: update | Decomiso definitivo y restitución de especímenes; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.presumption_of_fault_burden_proof`: update | Presunción de culpa o dolo en faltas ambientales; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.confession_fine_reduction`: update | Reducción de multas por confesión voluntaria; clarificar label | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.early_termination_correction_plan`: update | Terminación anticipada del proceso por compensación; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.ruia_offender_registry`: update | Registro único de infractores ambientales ruia; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt
- `rules.aggravating_factors_protected_area`: update | Causales agravantes por daño en áreas protegidas; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt
- `rules.liability_exemptions_force_majeure`: update | Eximentes de responsabilidad ambiental por fuerza mayor; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt
- `rules.restoration_duty_civil_criminal`: update | Obligación de restaurar daño ambiental causado; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_2387_2024.txt
- `rules.flagrancy_foreign_tourists_procedure`: update | Procedimiento en flagrancia y turistas extranjeros; fijar last_verified al 2026-11-21 | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/ley_1333_2009_fp.txt
- `rules.no_hunting`: update | Prohibición de caza y captura de fauna silvestre; reemplazado ejemplo de trampa por consulta directa de cacería | research_notes/Conocimiento turístico de Los Nevados/rules/evidence/raw/res207_2023.txt

## Entries Not Checked

Ninguna. Las 73 entradas de la sección `rules` fueron completamente auditadas e incluidas en `audit/rules.csv` y `proposals/rules.json`.

## Factual Gaps

- Se completó la vigencia fechada de las 64 entradas que carecían de `last_verified`, asignando la fecha de verificación `2026-11-21`. Cada una cuenta con respaldo documental oficial directo de la Resolución 207 de 2023, Decreto 1076 de 2015, Ley 2387 de 2024, Ley 1333 de 2009 o Ficha PNN.
- Las respuestas no modifican números ni montos económicos en pesos, manteniendo la política offline de remisión al valor del salario mínimo legal vigente (SMMLV) a la fecha de expedición del acto correspondiente.
- Se mantienen delimitados los vacíos normativos que no tienen texto en las fuentes leídas (fumar, velocidad exacta de bicicletas y perros de asistencia).

## Sources That Failed to Download

Ninguna. La prueba de entorno con `fetch_evidence.py` descargó exitosamente la ficha institucional de PNN Los Nevados (`test_fetch.txt`, HTTP 200). Las citas de la propuesta se basan en la evidencia documental primaria de Fase 2, hash-pinned y verificada en `legacy_evidence_manifest.json`.

## Cross-Section Findings

Registrados en `findings/rules.cross.json` (7 hallazgos):
1. `rules.camping` vs `activities.camping_where`: Delimitación entre prohibición legal de acampar fuera de zonas habilitadas y la oferta/descripción de sitios autorizados.
2. `rules.single_use_plastics` vs `preparation.reusable_bottles` y `preparation.cookware_utensils`: Delimitación entre prohibición legal normativa y recomendaciones de equipo.
3. `rules.commercial_photography` y `rules.audiovisual_permits` vs `activities.photography_amateur`: Fotos aficionadas libres vs sesiones comerciales sujetas a permiso.
4. `rules.event_permits` y `rules.organized_sports` vs `activities.regulated_sports`: Autorizaciones para eventos y competencias vs prácticas recreativas autorizadas.
5. `rules.wildlife_contact_displacement` y `rules.feed_wildlife` vs `health_safety.no_published_wildlife_protocol` y `fauna.injured_wildlife_protocol`: Prohibiciones de interacción vs respuesta a emergencias con fauna.
6. `rules.show_entry_permit_on_request` vs `booking_fees.documents_to_carry`: Obligación de exhibición ante autoridades en campo vs documentación de compra previa.
7. `rules.park_closure_no_compensation` vs `hours_status.unplanned_midday_closures` y `hours_status.trail_maintenance_temporary_closures`: Exención legal de indemnización vs estado operativo de senderos.

## Verification Summary

1. `knowledge.py stage`: `"status": "staged"`, 0 orphaned hard negatives, 0 similar labels.
2. `verify_evidence.py`: `"fail": []`, `"flags": []`, `"warn": []`.
3. `route_check.py`: `"n_removed_not_routing": 0` (el único ejemplo retirado de `rules.no_hunting` era sobre trampas y enrutó hacia `rules.wildlife_traps_prohibited`).
4. `audit_check.py`: `"fail": []` en las 73 entradas de la sección.
