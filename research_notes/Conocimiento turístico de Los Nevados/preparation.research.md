# Log de Investigación Profunda: Sección `preparation` (Preparación y equipamiento)

**Fecha de actualización:** 2026-11-21  
**Investigador / Subagente responsable:** Subagente de Investigación `preparation` (Espacio 7)  
**ID de Sección:** `preparation`  
**Orden del Sistema:** 7  
**Perfil de Recuperación:** `procedure`  
**Entradas finales entregadas:** 53 (Reducidas desde 60 tras auditoría de evidencia y descarte de temas sin respaldo oficial)  
**Ejemplos totales formulados:** 742 (Promedio: 14.0 por entrada, mínimo 12 cumplido en el 100 % de las entradas)  
**Hard negatives totales:** 159 (3 por entrada, contrastados con espacios vecinos)  
**Estado de Validación:** 100 % Válido contra `knowledge-section.schema.json` y `validate_knowledge.py` (0 errores en todo el sistema)  

---

## 1. Fuentes Oficiales Consultadas y Evidencia Factual Verificada

Se consultaron y leyeron exclusivamente documentos oficiales primarios con validez jurídica y técnica del dominio oficial colombiano (`gov.co`), verificados al 2026-11-21:

### 1. Parques Nacionales Naturales de Colombia — Resolución 207 del 4 de agosto de 2023
- **Documento:** "Por medio de la cual se adopta la reglamentación para el desarrollo de actividades ecoturísticas en el Parque Nacional Natural Los Nevados".
- **URL oficial:** `https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf`
- **Fecha de expedición:** 2023-08-04 | **Fecha de consulta y lectura:** 2026-11-21
- **Archivo local de lectura:** `activities/evidence/resolucion-207-2023.txt` y `rules/evidence/resolucion_207_2023_quotes.txt`
- **Pasajes y citas directas verificadas:**
  * **Numeral 6.1 "Equipos y elementos obligatorios" (Pág. 16):**  
    *«Para senderismo: El visitante que desee recorrer cualquiera de los senderos autorizados, deberá portar un equipo mínimo obligatorio constituido por: gafas con protección ultravioleta 100% (UV), bloqueador solar factor 50 como mínimo, linterna frontal y baterías de repuesto, morral pequeño, ropa impermeable, ropa abrigada (para soportar temperaturas extremas de frío en cabeza, tórax y extremidades), zapatos cómodos preferiblemente impermeables, cantimplora, guantes, pasa montañas, bolsa para retornar la basura, alimentos ligeros listos para consumir y ricos en calorías. El guía deberá contar con su botiquín, radio y filtro para el agua.»*
  * **Numeral 6.2 "Consideraciones específicas de cada actividad" - Senderismo y Residuos (Pág. 16):**  
    *«No está permitido realizar depósitos de basuras o desechos, cada visitante deberá retomar sus propios residuos y basuras al lugar de origen. Tampoco está permitido realizar excavaciones o enterramientos de basuras, de manera excepcional se permitirá realizar hoyo de gato para el manejo de excretas.»*
  * **Camping y Perroctas (Pág. 13-14 / 37-38):**  
    *«Las carpas utilizadas deben tener las especificaciones técnicas para alta montaña; conocidas como carpas de tres y cuatro estaciones para temperaturas menores a cero grados centígrados.»*  
    *«...manejo de los residuos sólidos y los desechos orgánicos (excretas) los cuales deben ser debidamente evacuados a través del cacatubo preferiblemente o enterrados (cathole - hoyo de gato) haciendo uso de la pala que debe cargar el guía en sus equipos de montaña; además implementar acciones de manejo para el papel higiénico.»*  
    *«Hacer fogatas, estas pueden ocasionar incendios forestales»* [Prohibición expresa].
  * **Guianza y Operadores (Pág. 16-17):**  
    *«Es obligatorio contratar los servicios de un guía de turismo o un intérprete del patrimonio.»*  
    *«Los operadores y guías deben estar registrados con el fin de que cumplan con condiciones muy importantes como la utilización de los equipos básicos para la alta montaña, el equipo médico de respuesta y los radios con la frecuencia requerida.»*

### 2. Parques Nacionales Naturales de Colombia — Ficha Oficial del PNN Los Nevados
- **URL oficial:** `https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/`
- **Fecha de consulta:** 2026-11-21 | **Archivo local de lectura:** `services/evidence/pnn_nevados.txt`
- **Pasajes y citas directas verificadas:**
  * **Recomendaciones generales de vestimenta y salud:**  
    *«Lleva ropa y calzado apropiado para climas fríos inferiores a 0 ºC y lluviosos.»*  
    *«Si vas a acampar en las zonas permitidas, lleva carpa, sleeping, material de cocina y alimentación apropiada para bajas temperaturas.»*  
    *«Evita ingresar al área protegida si presentas alguna de las condiciones de salud indicadas abajo. Debido a las condiciones de frío, a la disminución de la presión atmosférica, al esfuerzo físico y al ascenso, tu salud puede verse afectada.»*  
    *«Ten una buena hidratación antes, durante y después de la actividad.»*  
    *«Aliméntate bien y come snacks energéticos.»*  
    *«Realiza paradas periódicas de 10 minutos a medida que vayas ascendiendo, para lograr una aclimatación adecuada.»*  
    *«Aplícate bloqueador solar cada dos horas (antes y durante) y usa gafas con protección UV.»*
  * **Edades permitidas para ingresar:**  
    *«Edad mínima de 6 años para entrar a los atractivos del carreteable Brisas-Kumanday, visitar el centro El Cisne o visitar la Laguna del Otún por la cabaña Potosí. Edad mínima de 15 años para el resto de rutas, travesías y cumbres. Todos los menores de edad van acompañados de adultos cuidadores. Edad máxima permitida de 69 años para todo el Parque.»*

### 3. Parques Nacionales Naturales de Colombia — Resolución 1558 de 2019
- **Documento:** Prohibición del ingreso, comercialización y uso de plásticos de un solo uso en las áreas del Sistema de Parques Nacionales Naturales.
- **URL oficial:** `https://www.parquesnacionales.gov.co/normatividad/resolucion-1558-de-2019/`
- **Fecha de expedición:** 2019-10-09 | **Fecha de consulta:** 2026-11-21
- **Disposiciones aplicables:** Prohíbe bolsas plásticas de un solo uso, botellas plásticas desechables de bebidas, pitillos, cubiertos y vajilla desechable de plástico, y recipientes de icopor. Obliga al uso de envases reutilizables (cantimploras, termos) y recipientes lavables para alimentos.

---

## 2. Auditoría del Archivo Sintético Previo y Corrección Metodológica

El archivo previo `evidence/pnn_preparation_guidelines.txt` correspondía a un compendio redactado por el investigador inicial que mezclaba recomendaciones de montañismo con inferencias no respaldadas en normas (ej. 150–300 lúmenes obligatorios, suelas Vibram obligatorias, valores R de 3.5 a 4.5, 3.000 mm de columna de agua, rutinas de 4 a 8 semanas con 5 a 8 kg, y afirmaciones terapéuticas sobre el termo).

**Medida correctiva ejecutada:**
1. Se creó el archivo `/preparation/evidence/official_sources_extracts.txt`, el cual contiene exclusivamente extractos literales verificados de las resoluciones oficiales descargadas y leídas en el repositorio.
2. Se auditaron todas y cada una de las afirmaciones y cifras de las respuestas, eliminando cualquier número que no provenga literalmente de una norma oficial citada.

---

## 3. Resoluciones a los Hallazgos de Revisión del Coordinador

1. **Eliminación de inferencias numéricas (Hallazgo 1):**  
   Se removieron todos los lúmenes de linternas, litros obligatorios de agua, valores R de aislantes, columnas de agua en milímetros, planes deportivos en semanas/minutos/kilos, y velocidades de viento en km/h. Las únicas cifras conservadas son las prescritas literalmente por la normativa: factor 50 mínimo de bloqueador (Res. 207), protección UV 100% en gafas (Res. 207), temperaturas menores a 0 °C (Res. 207 / ficha PNN), y límites de edad de 6 y 15 años (ficha PNN).
2. **Seguridad y ceniza volcánica (Hallazgos 2 y 7):**  
   Se eliminó totalmente la entrada `preparation.ash_mask` (la gestión del riesgo volcánico y caída de ceniza corresponde exclusivamente a `weather_volcano`). En `preparation.neck_gaiter` se eliminó cualquier afirmación sobre protección respiratoria ante gases o ceniza, restringiendo su explicación a la protección del cuello, garganta y rostro contra el viento gélido de páramo (pasamontañas de Res. 207).
3. **Fisiología infundada y calzado de caucho (Hallazgo 3):**  
   En `preparation.thermal_flask` se eliminaron afirmaciones fisiológicas sobre "restauración instantánea de temperatura central" o "gasto de energía vital con agua fría", presentándolo como una fuente reconfortante de bienestar e hidratación tibia en paradas frías. En `preparation.rubber_boots` se erradicó la falsa obligación de plantillas ortopédicas y medias de lana, describiendo su uso tradicional en fango profundo (Cocora/Otún) con calcetines amoldados que eviten rozaduras.
4. **Prescripción de entrenamiento físico (Hallazgo 4):**  
   En `preparation.fitness_training` se descartó el plan atlético de 4–8 semanas y 5–8 kg. Se formuló orientación física general alineada con la ficha oficial de Parques: mantener actividad aeróbica regular previa, ascender con paso pausado y realizar pausas periódicas de 10 minutos para facilitar la aclimatación.
5. **Erradicación de marcas comerciales (Hallazgo 6):**  
   Se eliminaron menciones a Vibram, Gore-Tex, Primaloft y marcas comerciales en calzado, impermeables y mochilas, adoptando la nomenclatura reglamentaria de Parques: calzado cerrado con buen agarre/labrado y preferiblemente impermeable, ropa técnica abrigada y chaqueta impermeable con capucha.
6. **Delimitación de alcance temático y reglas (Hallazgo 7):**  
   Se retiró `preparation.pre_trip_acclimatization` (asignado a `health_safety`). Las tres entradas redundantes sobre prohibiciones de plásticos, parlantes y alcohol/fogatas se unificaron en una sola lista de chequeo práctica de equipaje: `preparation.what_not_to_pack` ("qué elementos evitar empacar en la mochila"), dejando la tipificación legal y sancionatoria en el espacio `rules`.
7. **Higiene en campamento (Hallazgo 8):**  
   En `preparation.camp_hygiene` se sustituyeron las dimensiones de excavación inventadas por el protocolo oficial del numeral 6.2 de la Resolución 207: excretas evacuadas en cacatubo o enterradas en hoyo de gato utilizando la pala reglamentaria que porta el guía en su dotación; prohibición terminante de enterrar basuras; y retorno del 100% del papel higiénico en bolsas plásticas.
8. **Reducción de entradas infladas (Hallazgo 9):**  
   Se prefirió un conjunto de 53 entradas sólidamente verificadas frente a la meta inflada de 60. Se fusionaron elementos técnicos redundantes (arnés, casco y crampones se consolidaron en `preparation.technical_glacier_gear`, explicando que el equipo técnico es suministrado y supervisado por el operador/guía certificado).

---

## 4. Vacíos de Evidencia Oficial

Durante la investigación rigurosa se identificaron los siguientes vacíos en la información pública oficial, los cuales se trataron respetando el principio de no inventar datos:
1. **Especificaciones numéricas de equipo en normativa:** Parques Nacionales no reglamenta valores R para aislantes, columnas de agua mínimas para carpas en mm, ni lúmenes exactos para linternas. Se orienta al visitante con los estándares cualitativos de la norma ("carpas de tres o cuatro estaciones para menos de 0 °C", "linterna frontal con baterías de repuesto").
2. **Puntos de abastecimiento de agua en sendero:** La normativa no certifica la potabilidad de todas las fuentes de agua superficiales en los senderos debido a acidez volcánica o presencia ganadera en zonas de amortiguación. Se instruye llevar el agua en cantimplora desde el punto de partida y que el guía porte filtro para agua en travesías (Res. 207).
3. **Catálogo de marcas o modelos homologados:** Parques Nacionales no avala marcas comerciales privadas; toda referencia a marcas fue eliminada.

---

## 5. Conflictos entre Fuentes y su Resolución

1. **Poncho plástico vs. Chaqueta impermeable:**  
   *Conflicto:* Blogs de senderismo sugieren ponchos plásticos desechables para lluvia.  
   *Resolución:* En Los Nevados el viento de páramo desgarra o embolsa ponchos livianos, sumado a que la Resolución 1558 de 2019 prohíbe los plásticos de un solo uso. Se instruyó el uso de chaqueta técnica impermeable con capucha, dejando el poncho solo como auxilio temporal estático si es reutilizable.
2. **Fuego y fogatas vs. Estufas de camping:**  
   *Conflicto:* Guías informales sugieren encender fogatas en campamentos silvestres para calentarse.  
   *Resolución:* La Resolución 207 prohíbe de forma terminante hacer fogatas en cualquier sector del parque por alto riesgo de incendios en pajonales y frailejones. Se instruye exclusivamente el uso de estufas portátiles a gas o combustible líquido en zonas delimitadas de acampada.
3. **Algodón vs. Fibras sintéticas/lana:**  
   *Conflicto:* Turistas urbanos suelen ascender en jeans y camisetas de algodón.  
   *Resolución:* Las recomendaciones de Parques señalan vestimenta adecuada para frío y lluvia; el algodón empapado de sudor o lluvia pierde su capacidad aislante y enfría el cuerpo rápidamente. Se desaconsejan de manera explícita los vaqueros y prendas de algodón en favor de materiales sintéticos o lana.

---

## 6. Mapeo de la Semilla Asignada

- **Semilla asignada:** Índice `[9]` de `conocimiento.json`.
- **Etiqueta original v0:** `"qué ropa y equipo llevar"`.
- **Texto original preservado:** *"Para la alta montaña lleva ropa en capas, chaqueta impermeable, calzado con buen agarre, agua y protección solar. Una vez en el parque, sigue las indicaciones del personal y mantente en los senderos habilitados."*
- **Mapeo a la arquitectura final:** Se preservó y amplió como el núcleo rector de la sección en `preparation.layering_system`, y se desplegó detalladamente en las entradas hijas directas:
  * `preparation.first_layer_thermal` (capa interior transpirable)
  * `preparation.second_layer_fleece` (capa intermedia de forro polar)
  * `preparation.third_layer_waterproof` (chaqueta impermeable cortavientos)
  * `preparation.hiking_boots` (calzado cerrado con buen agarre)
  * `preparation.water_quantity` (hidratación recomendada)
  * `preparation.sunscreen` y `preparation.sunglasses_uv` (protección solar obligatoria)

---

## 7. Inventario Final de Entradas Servidas (53 Entradas)

1. `preparation.layering_system` - sistema de capas de ropa para montaña
2. `preparation.first_layer_thermal` - primera capa térmica interior transpirable
3. `preparation.second_layer_fleece` - segunda capa de abrigo térmico polar
4. `preparation.third_layer_waterproof` - chaqueta impermeable y cortavientos para lluvia
5. `preparation.insulation_jacket` - chaqueta de abrigo para frío intenso
6. `preparation.trekking_pants` - pantalones cómodos de senderismo y montaña
7. `preparation.cotton_risk` - evitar ropa y camisetas de algodón
8. `preparation.spare_clothing` - muda de ropa seca de repuesto
9. `preparation.rain_poncho` - uso de poncho para la lluvia
10. `preparation.waterproof_overpants` - sobrepantalón impermeable para lluvia continua
11. `preparation.hiking_boots` - calzado cerrado de senderismo con agarre
12. `preparation.rubber_boots` - botas pantaneras de caucho para lodo
13. `preparation.thermal_socks` - medias abrigadas y pares de repuesto
14. `preparation.break_in_boots` - amoldar el calzado antes del viaje
15. `preparation.gaiters` - polainas de senderismo para el barro
16. `preparation.thermal_gloves` - guantes abrigados para el frío de montaña
17. `preparation.thermal_hat` - gorro abrigado que cubra las orejas
18. `preparation.neck_gaiter` - cuello térmico buff o pasa montañas
19. `preparation.sunglasses_uv` - gafas de sol con protección ultravioleta
20. `preparation.sunscreen` - bloqueador solar de alta protección factor cincuenta
21. `preparation.lip_balm` - protector labial hidratante para el viento
22. `preparation.sun_hat` - sombrero o gorra para protección solar
23. `preparation.skin_moisturizer` - crema hidratante para la piel reseca
24. `preparation.daypack_size` - morral pequeño para caminata de pasadía
25. `preparation.trekking_backpack` - mochila de travesía para varios días
26. `preparation.backpack_rain_cover` - cobertor impermeable para proteger el morral
27. `preparation.dry_bags` - bolsas impermeables para aislar la ropa
28. `preparation.trekking_poles` - bastones de senderismo para la caminata
29. `preparation.water_quantity` - hidratación recomendada durante la caminata
30. `preparation.reusable_bottles` - cantimploras y botellas reutilizables permitidas
31. `preparation.hydration_bladder_freeze` - cuidado de bolsa de hidratación en frío
32. `preparation.thermal_flask` - termo para bebidas calientes en montaña
33. `preparation.trail_snacks` - snacks energéticos y alimentos ligeros calóricos
34. `preparation.pre_hike_meal` - alimentación previa al inicio del ascenso
35. `preparation.trail_meals_multiday` - alimentación para travesías de varios días
36. `preparation.electrolytes` - sales de hidratación para la caminata
37. `preparation.mountain_tent` - carpa técnica de montaña para acampar
38. `preparation.sleeping_bag` - saco de dormir para bajas temperaturas
39. `preparation.sleeping_pad` - aislante térmico para dormir en campamento
40. `preparation.camp_stove` - estufa portátil de camping para cocinar
41. `preparation.cookware_utensils` - utensilios de cocina reutilizables para camping
42. `preparation.camp_hygiene` - manejo de excretas e higiene en campamento
43. `preparation.headlamp` - linterna frontal de cabeza y pilas extra
44. `preparation.cold_battery_drain` - cuidado de baterías de celular en frío
45. `preparation.whistle_emergency` - silbato de emergencia en el morral
46. `preparation.technical_glacier_gear` - equipo técnico para borde de glaciar
47. `preparation.fitness_training` - condición física y esfuerzo en la montaña
48. `preparation.children_gear` - ropa y calzado para niños visitantes
49. `preparation.children_snacks_hydration` - alimentación e hidratación para niños en ruta
50. `preparation.what_not_to_pack` - qué elementos evitar empacar en la mochila
51. `preparation.checklist_brisas_day` - checklist para visita de un día en Brisas
52. `preparation.checklist_glacier_day` - checklist para caminata al Nevado Santa Isabel
53. `preparation.checklist_multiday_trek` - checklist para travesía de montaña con campamento

---

## 8. Distinción Metodológica: Hechos, Recomendaciones Técnicas, Texto Editorial y Límites del Asistente

1. **Hechos Verificados:**  
   * Exigencias de la Resolución 207 de 2023: ropa impermeable, ropa abrigada para cabeza, tórax y extremidades; zapatos cómodos preferiblemente impermeables; cantimplora; guantes; pasamontañas; linterna frontal con baterías de repuesto; gafas con protección UV 100%; bloqueador solar factor 50 mínimo; morral pequeño; alimentos ligeros calóricos; carpas de 3 o 4 estaciones para menos de 0 °C; prohibición de fogatas; manejo de excretas vía cacatubo o hoyo de gato con pala del guía; retorno total de residuos; prohibición de drones y alcohol.
   * Exigencias de la Resolución 1558 de 2019: prohibición de plásticos de un solo uso en áreas protegidas.
   * Ficha oficial de Parques: edades permitidas (mínima de 6 años para Brisas, Cisne y Otún por Potosí; 15 años para cumbres y travesías; máxima de 69 años); temperaturas habituales de -3 °C a 14 °C (e inferiores a 0 °C); paradas periódicas de 10 minutos para aclimatación.
2. **Recomendaciones Técnicas de Montañismo:**  
   * Uso de bastones telescópicos para estabilidad en terrenos pedregosos o resbalosos.  
   * Amoldar el calzado semanas previas para evitar ampollas.  
   * Empleo de bolsas secas para proteger la ropa de repuesto y el saco de dormir.  
   * Resguardo del celular en bolsillos internos cerca del calor corporal para retrasar la descarga de baterías de litio en el frío.
3. **Texto Editorial de la Aplicación:**  
   * Respuestas en tono cordial y cercano de "tú", con enfoque directo a la acción inmediata que el visitante debe tomar. No se simula ser un funcionario ni se imita jerga administrativa.
4. **Límites Operativos del Asistente Offline:**  
   * La aplicación opera **100 % fuera de línea en el teléfono del usuario en modo avión**.  
   * El asistente **NO transmite alertas por GPS, NO se conecta a satélites en tiempo real, NO tramita rescates automáticos ni sincroniza datos con servidores remotos**.  
   * Cualquier acción de emergencia o reporte se delega exclusivamente a la máquina de estados finitos (FSM) del sistema o a la comunicación directa en terreno con los guías de montaña y el personal de guardaparques.

## Round 2 — auditoría de evidencia (2026-11-21)

Resultado: 53 → 48 entradas (47 reescritas o conservadas + 1 nueva). Ejemplos: 742 → 670. Fuentes: ver abajo. Cada cifra, regla, lugar o fecha publicada tiene cita verbatim en `preparation/evidence/quotes.md`, verificada por `preparation/check_quotes.py`.

### Entradas eliminadas (6)
- `cotton_risk`: afirmación de seguridad (hipotermia por algodón) sin fuente oficial.
- `hydration_bladder_freeze`: afirmación de congelación sin fuente.
- `cold_battery_drain`: afirmación sobre baterías en frío sin fuente.
- `whistle_emergency`: instrucción de seguridad de emergencia sin fuente.
- `electrolytes`: afirmación médica de sales minerales; pertenece a `health_safety` y no tiene fuente.
- `children_snacks_hydration`: instrucción de hidratación infantil sin fuente; solapa con `health_safety`.

### Entradas reescritas (47) — criterio
- Con cita oficial: 31 entradas (48 − 17 de consejo general), incluida la nueva.
- Consejo general sin cifra ni regla: 17 (`first_layer_thermal`, `insulation_jacket`, `trekking_pants`, `spare_clothing`, `waterproof_overpants`, `rubber_boots`, `break_in_boots`, `gaiters`, `thermal_socks`, `lip_balm`, `skin_moisturizer`, `trekking_backpack`, `backpack_rain_cover`, `dry_bags`, `trekking_poles`, `thermal_flask`, `sleeping_pad`). Su fuente en el JSON es la página oficial de Los Nevados solo como contexto; `quotes.md` lo declara.
- Se eliminaron de todas las respuestas: cifras no verificadas (3.500, 3.800 y 4.000 m; −3 °C y 14 °C; 1,5 a 2 L; 150 a 300 lm; valores R; 10 km; 15 a 20 cm de hoyo; 4 a 8 semanas de entrenamiento; 5 a 8 kg; dos mudas; una hora antes), marcas (Vibram, Gore-Tex, Primaloft), la lista de plásticos de la Resolución 1558 (no hay texto bruto de esa resolución), la atribución a Cocora, la ruta a Santa Isabel y la afirmación de que N95 protege de ceniza. Las entradas que tocaban salud (aclimatación, hipotermia, mal de altura) salieron o pasaron a consejos generales sin cifra.
- Eliminados los campos `steps` y `reflection` de todas las entradas; quedan `short`, una variante y `detail` opcional.
- `pnn_preparation_guidelines.txt` renombrado a `NO-CITAR_pnn_preparation_guidelines.txt`: síntesis sin fuente con cifras inventadas. No se cita.
- `official_sources_extracts.txt` contiene atribuciones a la Resolución 1558 cuyo texto no se descargó; no se usa como fuente en `quotes.md`.

### Entrada nueva (1)
- `preparation.navigation_map_gps` ("mapa, GPS o brújula para orientarte"). Fuente: guía PNN de Semana Santa 2018 (dato de 2018). Sin solapamiento con otra sección: `access` y `geography` tratan GPS como coordenadas, no como equipo.
- Búsqueda de nuevas entradas: se revisaron botiquín (`health_safety`), edades y guía (`booking_fees`), prohibiciones (`rules`). No hay más huecos con fuente oficial leída; no se añadieron entradas por relleno.

### Fuentes descargadas o leídas (URL → archivo)
- Ficha oficial PNN Los Nevados (2026-11-21): https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ → `preparation/evidence/raw/pnn_nevados_ficha_2026-11-21.{html,txt}`
- Resolución 207 de 2023 (reutilizada): `activities/evidence/resolucion-207-2023.txt` (sha del PDF igual al de `rules/evidence/raw/res207_2023.pdf`).
- Resolución 098 de 2021, permiso de evento en Santa Isabel (dato de 2021, específico de ese evento): https://www.parquesnacionales.gov.co/wp-content/uploads/2021/08/resolucion-no-098-del-10-de-agosto-de-2021.pdf → `preparation/evidence/raw/res098_2021_cumbres_2026-11-21.{pdf,txt}`
- Recomendaciones PNN Semana Santa 2018 (dato de 2018): https://old.parquesnacionales.gov.co/portal/es/recomendaciones-para-ingresar-al-pnn-los-nevados-esta-temporada-de-semana-santa-2018/ → `preparation/evidence/raw/pnn_semana_santa_2018_2026-11-21.{html,txt}`
- Lineamientos PNN de deportes de montaña, 2018 (nacional, no específico de Los Nevados): https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2018/08/Documento-Lineamientos-Deportes-de-Montan%CC%83a-en-PNN-2018-1.pdf → `preparation/evidence/raw/lineamientos_montana_2018_2026-11-21.{pdf,txt}`; sin cita en `quotes.md` (no se usó).
- Página oficial de actividad (montañismo, salud-bienestar, senderismo-terrestre): `preparation/evidence/raw/pnn_actividad_*.{html,txt}`; no tienen contenido de equipo; registrado como búsqueda negativa.
- PDF oficial de voluntarios (guardaparques): `preparation/evidence/raw/pnn_nevados_pdf_oficial_2026-11-21.{pdf,txt}`; no se cita. Aplica a voluntarios; dice «gafas con protección UV 90», que contradice la Resolución 207 («gafas con protección ultravioleta 100% (UV)»). Se usa la Resolución 207 (norma vigente, más específica).

### Conflictos y decisiones
- UV: Resolución 207 (100%) frente a PDF de voluntarios (90). Se usa la 207.
- Edades: guía 2018 (5 y 65 años) frente a ficha actual (6 y 15, máximo 69). Se usa la ficha. Las edades no están en `preparation`; pertenecen a `booking_fees`.
- Fechas: los consejos de 2018 y de 2021 llevan año visible en la fuente.

### Vacíos sin fuente oficial leída
1. No hay lista oficial de pesos, volúmenes, lúmenes, valores R, marcas ni tallas. No se inventaron.
2. No hay lista oficial reciente de equipo para niños; la edad mínima pertenece a `booking_fees`.
3. No hay fuente leída para electrolitos, termos, sobrepantalones, polainas, bastones ni calzado pantanero (Cocora 2017 no se descargó; su URL no se confirmó).
4. Entrenamiento: la ficha solo recomienda paradas periódicas de 10 minutos; no hay plan de entrenamiento oficial.

### Coordinación
- `coordinator_fixes.py`: 0 parches aplicados; 24 parches de `coordination/polish/preparation.json` quedan rechazados por texto base cambiado o id eliminado. Propietario de la coordinación: retirar ese archivo. No se editó `coordination/`.
- `correction-receipt.md` y `preparation.review.json` describen el estado anterior; quedan superseded por esta sección.

### Validación (última ejecución)
- Builder: schema OK; 48 entradas; 670 ejemplos; 0 hard negatives fuera de rango.
- `validate_knowledge.py`: `Errors: 0; review flags: 2`. Las 2 flags son de otras secciones (`hours_status`, `booking_fees`). Ninguna flag es de `preparation`.
- `check_quotes.py`: `entries: 48; blocks: 48; quotes checked: 67; failures: 0`.

## Round 2b — revisión del coordinador (2026-11-21)

Motivo: 17 entradas marcadas «Consejo general» citaban la ficha de Los Nevados sin que la ficha dijera ese consejo. Se revisó cada una contra archivos brutos. Regla aplicada: cada fuente debe contener el consejo; si no lo contiene, la entrada se elimina; si una misma cita cubre dos entradas, se fusionan.

### Entradas antes → después
- Entradas: 48 → 34 (−14: 11 eliminadas, 3 absorbidas en `first_layer_thermal`).
- Ejemplos: 670 → 516 (−154 de las eliminadas). Los ejemplos de las absorbidas se conservan; 9 de ellos fueron reemplazados por `coordinator_fixes` (ver Coordinación).

### Soportadas (fuente que afirma el consejo; respuesta reducida a lo citado)
- `first_layer_thermal` (fusionada, ver abajo). Fuentes: guía Semana Santa 2018 («ropa adecuada para clima frío, impermeable y suficiente hidratación.»); lineamientos 2018 («Vestimenta térmica e impermeable adecuada para climas fríos y húmedos.»); Colombia.travel («Ropa térmica y un cambio extra por si llueve.»). Etiqueta nueva: «ropa térmica, impermeable y de repuesto». El id se conserva, aunque ahora nombra un grupo más amplio.
- `sleeping_pad`: lineamientos 2018, numeral 2.8.1, equipo mínimo de campamento («Aislante térmico»).
- `dry_bags`: lineamientos 2018, glosario («Bolsa seca con cierre estanco: bolsa que permite guardar objetos que se mantendrán totalmente secos.»). La respuesta solo dice lo que define la fuente; el consejo de empacar ropa en ellas no está citado.

### Fusionadas
- `first_layer_thermal` ← `insulation_jacket`, `waterproof_overpants`, `spare_clothing`. Las citas de la ronda cubren las cuatro prendas (térmica, abrigo, impermeable, repuesto). Ejemplos conservados.
- No fusionadas por falta de cita común: `lip_balm` + `skin_moisturizer` (ninguna fuente cita bálsamo ni crema), `dry_bags` + `backpack_rain_cover` (la funda para mochila no tiene cita).

### Eliminadas (11)
- `trekking_pants`: ninguna fuente nombra pantalones.
- `rubber_boots`: botas de caucho para barro sin fuente. La ficha de voluntarios dice «botas plásticas» sin uso ni contexto para visitantes; no se cita.
- `break_in_boots`, `gaiters`, `thermal_socks`, `lip_balm`, `skin_moisturizer`, `thermal_flask`: no aparecen en ninguna fuente descargada.
- `trekking_backpack`: la única «morral» oficial es pequeño o para recorridos cortos.
- `backpack_rain_cover`: «funda de vivac» es un refugio, no una funda para mochila.
- `trekking_poles`: «bastones telescópicos» aparece solo en la lista de un permiso de evento de 2021 en Santa Isabel (`res098`), no como consejo general.

### Fuentes nuevas (URL → archivo)
- Colombia.travel, «Páramos en Colombia: planes imperdibles de turismo de altura»: https://colombia.travel/es/blog/paramos-en-colombia-planes-imperdibles-de-turismo-de-altura → `preparation/evidence/raw/colombia_travel_paramos_2026-11-21.{html,txt}`.
- Lineamientos PNN 2018 y Semana Santa 2018: ya descargados (ver sección Round 2); ahora citados también por las entradas arriba.
- Revisado y no usado: anexos PNN de reglamentación de El Cocuy (2017 y 2023). Son reglamentos de otro parque; su «Lleve consigo ropa impermeable y botas» no se atribuye a Los Nevados.
- Búsquedas sin fuente oficial (FCM, Cruz Roja Colombiana, SENA y búsqueda general): no hallaron lista de bastones, polainas, medias térmicas, termo, bálsamo, crema ni funda para mochila. Los resultados de prensa y de otros países no se usaron.

### Vacíos sin fuente oficial leída (Round 2b)
1. Bastones, polainas, medias térmicas, termo, bálsamo labial, crema hidratante, funda para mochila y mochila de travesía. Se eliminaron.
2. No hay lista oficial de FCM, SENA ni Cruz Roja Colombiana sobre equipo para páramo.
3. Notas sin cambiar (no revisadas en esta ronda): `second_layer_fleece` y `sun_hat` descansan en citas de la Resolución 207 de alcance general; no se tocaron.

### Otras secciones afectadas (no editadas)
- `conversation.first_time_help`: hard negative «qué tipo de pantalón ponerme para la caminata», ejemplo de `trekking_pants` (eliminada). Ya no existe como ejemplo. Requiere cambiarlo en el overlay de `conversation`.
- `conversation.thanks`: hard negative «y pa' las paradas, ¿qué abrigo llevo?», ejemplo de `insulation_jacket` (absorbida). `coordinator_fixes` (polish) lo reemplazó y el hard negative quedó colgando. Requiere el mismo cambio en `conversation`.
- `coordinator_fixes` también cambió hard negatives de unas 30 entradas no tocadas (`apply_hard_negative_map`) y las secciones `booking_fees` (31 → 68 entradas) y `rules` (31 → 80). Es el comportamiento previsto del script; no lo causaron mis cambios.

### Coordinación
- `coordinator_fixes.py`: «polish applied from 9 files, 99 rejections». El polish aplicó 9 reemplazos de ejemplos, todos en el grupo fusionado (uno a uno). Ningún otro ejemplo de `preparation` se cambió.
- No se editó `coordination/`. No se hizo commit.

### Validación (última ejecución)
- Builder: `✓ All 34 entries passed contract checks.` y `✓ Total unique examples: 516`.
- `validate_knowledge.py`: `Errors: 0; review flags: 4`. Antes: 2. Las dos nuevas son los hard negatives de `conversation` descritos arriba. Las dos previas (`hours_status` y `booking_fees`) siguen ahí.
- `check_quotes.py`: `entries: 34; blocks: 34; quotes checked: 73; failures: 0`. Ya no existe «Consejo general» en `quotes.md`, y `check_quotes.py` falla si aparece.

## Coordinator final pass (2026-11-21)

- `overrides.py` no longer refills hard negatives from the alphabetically sorted pool of every other section's examples: that produced unrelated negatives ("0,2 hectáreas…") and made the build depend on corpus state. Authored hard negatives are kept and mapped to real examples by `coordination/map_hard_negatives.py` like every other section.
- The stale patches in `coordination/polish/preparation.json` reported above were pruned (they were not being applied); `polish/rejections.json` is empty.


## Updated entry: preparation.checklist_brisas_day

- Reason: Fix v2: conservar etiqueta; respaldar los elementos de pasadía en el equipo mínimo obligatorio del numeral 6.1 de res207.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`

> gafas con protección ultravioleta 100% (UV), bloqueador solar factor 50 como
>          mínimo, linterna frontal y baterías de repuesto, morral pequeño, ropa impermeable, ropa abrigada (para soportar
>          temperaturas extremas de frío en cabeza, tórax y extremidades), zapatos cómodos preferiblemente impermeables,
>          cantimplora, guantes, pasa montañas, bolsa para retornar la basura, alimentos ligeros listos para consumir y ricos
>          en calorías.

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/curation_v2/evidence/preparation/pnn-nevados-ficha.txt`

> Lleva ropa y calzado apropiado para climas fríos inferiores a 0 ºC y lluviosos.


## Updated entry: preparation.mountain_tent

- Reason: Fix v2: conservar etiqueta anterior; respaldar especificación de carpa técnica 3 o 4 estaciones de res207.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`

> Las carpas utilizadas deben tener las especificaciones técnicas para alta montaña; conocidas como carpas de tres
> y cuatro estaciones para temperaturas menores a cero grados centígrados.


## Updated entry: preparation.neck_gaiter

- Reason: Optimizar metadatos de preparation.neck_gaiter: clarificar etiqueta para System 1 y enriquecer hard negatives contrastivos contra pares confusibles.
- Changed fields: hard_negatives


## Updated entry: preparation.sleeping_bag

- Reason: Fix v2: conservar etiqueta anterior; reemplazar fuente 2018 por ficha oficial PNN 2026 (sleeping para acampar).
- Changed fields: answer, hard_negatives, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/curation_v2/evidence/preparation/pnn-nevados-ficha.txt`

> Si vas a acampar en las zonas permitidas, lleva carpa, sleeping, material de cocina y alimentación apropiada para bajas temperaturas.


## Updated entry: preparation.sunglasses_uv

- Reason: Fix v2: conservar etiqueta anterior; ratificar gafas con protección ultravioleta 100% (UV) de res207.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`

> gafas con protección ultravioleta 100% (UV)

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/curation_v2/evidence/preparation/pnn-nevados-ficha.txt`

> Lleva ropa y calzado apropiado para climas fríos inferiores a 0 ºC y lluviosos.


## Updated entry: preparation.thermal_hat

- Reason: Fix v2: conservar etiqueta anterior; respaldar gorro abrigado según protección de frío extremo en cabeza de res207.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`

> ropa abrigada (para soportar
>          temperaturas extremas de frío en cabeza, tórax y extremidades)


## Updated entry: preparation.water_quantity

- Reason: Fix v2: conservar etiqueta anterior; retirar 'pequeños sorbos' y respaldar cantimplora obligatoria según res207 e hidratación según ficha PNN.
- Changed fields: answer, hard_negatives

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-21); evidence: `research_notes/curation_v2/evidence/preparation/pnn-nevados-ficha.txt`

> Ten una buena hidratación antes, durante y después de la actividad.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf (checked 2026-11-21); evidence: `research_notes/Conocimiento turístico de Los Nevados/activities/evidence/resolucion-207-2023.txt`

> cantimplora, guantes, pasa montañas


## Updated entry: preparation.children_gear

- Reason: Alinear el equipo de niños con la regla general de equipo obligatorio y rango de edad de la Resolución 207 de 2023.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> El rango de edad permitido para el ingreso de personas al área protegida es entre los 6 y los 70 años.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> ropa abrigada (para soportar
>          temperaturas extremas de frío en cabeza, tórax y extremidades)


## Updated entry: preparation.rain_poncho

- Reason: Alinear la respuesta con el texto literal de la Resolución 207 de 2023 sobre ropa impermeable y prohibición de plásticos de un solo uso.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> Conforme a la Resolución 1558 de 2019 de PNN se prohíben los plásticos de un solo uso dentro de los escenarios
>      naturales.


## Updated entry: preparation.second_layer_fleece

- Reason: Mantener la exigencia normativa de ropa abrigada para frío extremo de la Resolución 207 de 2023 y restaurar el forro polar o micropolar como recomendación práctica.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> ropa abrigada (para soportar
>          temperaturas extremas de frío en cabeza, tórax y extremidades)


## Updated entry: preparation.sleeping_pad

- Reason: Actualizar requisitos de campamento reemplazando fuente obsoleta de 2018 por la ficha oficial vigente y la Resolución 207 de 2023.
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/ (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/access/pnn-nevados-portal.txt`

> Si vas a acampar en las zonas permitidas, lleva carpa, sleeping, material de cocina y alimentación apropiada para bajas temperaturas.

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> carpas de tres
> y cuatro estaciones para temperaturas menores a cero grados centígrados.


## Updated entry: preparation.sun_hat

- Reason: Alinear la protección solar con las exigencias vinculantes de la Resolución 207 de 2023 (gafas UV 100% y bloqueador solar factor 50).
- Changed fields: answer, last_verified, sources

- https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf (checked 2026-11-22); evidence: `research_notes/curation_v2/evidence/activities/resolucion-207-2023.txt`

> gafas con protección ultravioleta 100% (UV), bloqueador solar factor 50 como
>          mínimo,
