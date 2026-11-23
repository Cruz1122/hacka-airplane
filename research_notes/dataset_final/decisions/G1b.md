# Decisiones sobre contradicciones entre pares de FAQ — Agente G1b

Evaluación y resolución de las 5 parejas de entradas señaladas por revisores de pares, conforme a `BRIEF_COMMON.md` y `BRIEF_FACTUAL.md`.

---

## Análisis por pareja

### Pareja 1: Salento en el área protegida vs. 14 km al límite
- **IDs**: `geography.salento_quindio` vs. `access.from_salento_cocora`.
- **Evaluación**: No hay contradicción al leer el texto completo. `geography.salento_quindio` responde a la división territorial político-administrativa: Salento es el único municipio del departamento del Quindío que hace parte de los diez municipios con jurisdicción en el PNN Los Nevados (aportando más de 21.000 ha protegidas según la ficha PNN y el Plan de Manejo). Por su parte, `access.from_salento_cocora` aclara explícitamente que «el pueblo no es la portería» y que la distancia desde Salento por la vereda Cocora hasta el límite del parque es de 14 km. Se mantienen ambas sin cambios.
- **Fuentes**: Ficha oficial PNN Los Nevados (2026); Plan de Manejo PNN Los Nevados (2017).

### Pareja 2: Nacimiento de los ríos Lagunilla y Recio
- **IDs**: `geography.rios_lagunilla_recio` vs. `weather_volcano.ruiz_rivers`.
- **Evaluación**: Existía aparente contradicción porque `geography.rios_lagunilla_recio` afirmaba que la tabla no decía dónde nacía cada río, mientras que `weather_volcano.ruiz_rivers` aseveraba (según el SGC) que nacen en el edificio volcánico del Ruiz. Se armonizó `geography.rios_lagunilla_recio` mediante una operación de actualización (`update`), citando tanto la tabla glaciológica del Ideam (drenaje hacia la zona Alto Magdalena) como la ficha oficial del SGC que confirma que nacen en el edificio volcánico del Ruiz, orientando la seguridad del visitante ante aumentos de actividad volcánica.
- **Fuentes**: IDEAM (glaciar Nevado del Ruiz, tabla de drenaje); Servicio Geológico Colombiano (ficha de generalidades del volcán Nevado del Ruiz).

### Pareja 3: Ingreso desde Pereira por El Cedral vs. Vereda El Bosque
- **IDs**: `access.santa_rosa_vs_cedral` y `access.from_pereira_cedral` vs. `activities.sector_laguna_otun`.
- **Evaluación**: No hay contradicción al leer el texto completo y las fuentes oficiales. El Cedral es el sitio terminal de la carretera vehicular desde Pereira (vía La Florida) donde inicia la caminata, y la vereda El Bosque es la vereda rural de Pereira que atraviesa dicho camino de herradura rumbo a la Laguna del Otún. La propia ficha web oficial de Parques Nacionales utiliza ambas denominaciones para este acceso («desde Pereira por carretera en dirección al corregimiento de La Florida y el sitio El Cedral, para ascender caminando» y «desde el municipio de Pereira, a través de la vereda El Bosque»), hecho ratificado explícitamente en el catálogo por la entrada `access.cedral_and_bosque_names`. Se mantienen sin cambios.
- **Fuentes**: Ficha oficial PNN Los Nevados (Sector Otún); Plan de Manejo PNN Los Nevados (2017, camino Cedral – vereda El Bosque).

### Pareja 4: Porteo de mulas permitido vs. prohibición en Arenales y Calvito
- **IDs**: `rules.no_mules_arenales_calvito` vs. `services.mule_luggage_registered_only`.
- **Evaluación**: `services.mule_luggage_registered_only` enunciaba de forma general que arrieros avalados podían portear equipaje, omitiendo la restricción territorial crítica establecida en el mismo numeral 6 de la Resolución 207 y Anexo de Reglamentación de 2023. Se actualizó `services.mule_luggage_registered_only` para advertir expresamente que dicho porteo autorizado no ingresa a los campamentos altos de Arenales ni Calvito (donde solo se accede a pie), quedando en perfecta concordancia con `rules.no_mules_arenales_calvito`.
- **Fuentes**: PNN Los Nevados · Anexo de reglamentación ecoturística (diciembre 2023, numeral 6) / Resolución 207 de 2023.

### Pareja 5: Kilometrajes Quindío-Dulima (Cocora vs. Palomar)
- **IDs**: `access.armenia_salento_road` vs. `access.from_anzoategui_palomar`.
- **Evaluación**: No hay contradicción al leer el texto completo. Son dos corredores geográficos completamente diferentes en costados opuestos de la cordillera: `access.armenia_salento_road` trata el acceso occidental por Quindío (Salento/Cocora, 14 km al límite), mientras que `access.from_anzoategui_palomar` trata el acceso suroriental por Tolima (Anzoátegui/Palomar, 11 km al acceso). Cada entrada evalúa y advierte sobre inconsistencias históricas internas de su propio tramo en reglamentaciones de 2016 y 2023. Se mantienen ambas sin cambios.
- **Fuentes**: Ficha oficial PNN Los Nevados; Reglamentación transitoria PNN (diciembre 2023); How to get there (abril 2016).

---

## Registro por ID (touched / deliberately untouched)

- `access.armenia_salento_road`: Deliberadamente intacto. No contradice a Palomar; analiza las cifras internas del trayecto Armenia–Salento–Cocora (fuente: ficha PNN y anexo 2023).
- `access.from_anzoategui_palomar`: Deliberadamente intacto. No contradice a Armenia/Salento; evalúa el acceso tolimense por Palomar (fuente: ficha PNN y anexo 2023).
- `access.from_pereira_cedral`: Deliberadamente intacto. No contradice a El Bosque; documenta el inicio del sendero en El Cedral (fuente: ficha PNN).
- `access.from_salento_cocora`: Deliberadamente intacto. No contradice a `geography.salento_quindio`; precisa que el pueblo no es la portería y dista 14 km del límite (fuente: ficha PNN).
- `access.santa_rosa_vs_cedral`: Deliberadamente intacto. No contradice a El Bosque; diferencia la entrada por Santa Rosa de la entrada por El Cedral en Pereira (fuente: ficha PNN).
- `activities.sector_laguna_otun`: Deliberadamente intacto. No contradice a El Cedral; cita la vereda El Bosque atravesada en la ruta desde Pereira (fuente: ficha PNN).
- `geography.rios_lagunilla_recio`: Modificado (update). Se armonizó con `weather_volcano.ruiz_rivers` incorporando el nacimiento en el edificio volcánico según SGC y el drenaje Alto Magdalena según Ideam (soporte: IDEAM glaciar Ruiz y SGC generalidades Ruiz).
- `geography.salento_quindio`: Deliberadamente intacto. No contradice a `access.from_salento_cocora`; refiere a la jurisdicción municipal en el área protegida (fuente: ficha PNN).
- `rules.no_mules_arenales_calvito`: Deliberadamente intacto. Enuncia con exactitud la prohibición de porteo a campamentos altos (fuente: Res. 207 de 2023).
- `services.mule_luggage_registered_only`: Modificado (update). Se incorporó la excepción que prohíbe el porteo hacia Arenales y Calvito para armonizar con `rules.no_mules_arenales_calvito` (soporte: Anexo reglamentación PNN 2023, numeral 6).
- `weather_volcano.ruiz_rivers`: Deliberadamente intacto. Cita fehaciente del SGC que respalda el nacimiento de los cuatro ríos en el edificio volcánico (fuente: SGC generalidades Ruiz).
