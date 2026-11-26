# Citas de `weather_volcano` — leídas el 2026-11-21

Cada bloque indica la URL, la fecha de acceso y el archivo bruto. Las citas entre «» se copiaron del texto de ese archivo. `weather_volcano/check_quotes.py` comprueba que aparezcan tras normalizar espacios. No se cita la portada de ninguna entidad. La página histórica del IDEAM titulada El clima en alta montaña (URL Liferay en ideam.gov.co/web/otros-ecosistemas/investigacion-y-publicaciones) no respondió: HTTP agotó el tiempo y HTTPS devolvió 404 del sitio nuevo. Esas cifras de meses, milímetros, humedad y gradiente de -5,4 °C no se usan.

## PNN — ficha del parque

- URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/pnn-nevados.txt`

- Régimen: «El Parque se caracteriza por tener dos periodos de lluvias y dos secos a lo largo del año (régimen de precipitación bimodal). La temperatura es variable debido a estos cambios de estación y a los pisos térmicos producto de su topografía montañosa.»
- Entradas: weather_volcano.park_weather, weather_volcano.rainy_seasons, weather_volcano.weather_by_elevation

## IDEAM — dónde hace más frío

- URL: https://ideam.gov.co/atencion-y-servicios-a-la-ciudadania/preguntas-frecuentes/en-colombia-donde-hace-mas-frio
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ideam-frio-faq.txt`

- Sin estaciones de latitudes medias: «Colombia no tiene estaciones climáticas similares a las de latitudes medias por estar tan cerca del ecuador.»
- Variación mensual: «Las variaciones mensuales de temperatura para un sitio determinado están asociadas a las temporadas lluviosas o temporadas secas, es decir, al comportamiento medio de las lluvias pero no son significativas.»
- Altura: «a mayor altura que se encuentre el sitio, menor temperatura.»
- Páramo y nevado: «los sitios donde se presentan las menores temperaturas corresponden a los páramos y las áreas de nevados, donde los valores de las temperaturas pueden alcanzar los cero grados e inclusive temperaturas por debajo de este valor.»
- Gradiente de referencia: «por cada 100 metros de ascenso la temperatura baja en 0.6 grados C.»
- Entradas: weather_volcano.no_temperate_seasons, weather_volcano.weather_by_elevation, weather_volcano.freezing_at_altitude, weather_volcano.park_weather

## IDEAM — glosario de helada

- URL: https://www.ideam.gov.co/atencion-y-servicios-a-la-ciudadania/glosario/helada-alertas-hidrologicas
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ideam-helada-glosario.txt`

- Definición: «En términos meteorológicos, es la ocurrencia de una temperatura igual o menor a 0 °C a un nivel de 1.5 a 2 m sobre el nivel del suelo.»
- Entradas: weather_volcano.helada_meaning

## IDEAM — nota técnica de heladas (2012)

- URL: https://bart.ideam.gov.co/meteorologia/NOTAS_TECNICAS/NT_IDEAM-2012-000_HELADAS.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ideam-heladas-2012.txt`

- Radiación: «Es la helada típica de las regiones tropicales y son factibles de presentarse a partir de los 2500 metros sobre el nivel del mar»
- Meses secos: «Afecta áreas localizadas a más de 2500 m.s.n.m, especialmente en los meses secos del año.»
- Amanecer: «desaparece generalmente a la salida del sol»
- Altiplanos: «En el territorio nacional las heladas se dan principalmente en los altiplanos»
- Entradas: weather_volcano.helada_night, weather_volcano.helada_meaning

## IDEAM — Pronósticos y Alertas

- URL: https://www.ideam.gov.co/pronosticos-y-alertas
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ideam-pronosticos-alertas.txt`

- Canal: «Pronósticos y Alertas»
- Por departamento: «Comportamiento y pronóstico de la precipitación por departamento»
- Entradas: weather_volcano.current_forecast, weather_volcano.rain_by_department, weather_volcano.national_forecast_limit

## IDEAM — boletín de tres días

- URL: https://www.ideam.gov.co/sala-de-prensa/boletines/Boletín-de-Pronóstico-Nacional-del-Tiempo-para-Tres-Días-(BPTD)
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ideam-bptd.txt`

- Alcance: «Este boletín presenta la información del pronóstico del tiempo para los siguientes 3 días a nivel nacional, así como un resumen de las alertas vigentes.»
- Mapas: «Cada mapa representa las condiciones más probables de precipitaciones acumuladas en el periodo de tiempo y fecha indicados.»
- Entradas: weather_volcano.current_forecast, weather_volcano.national_forecast_limit

## PNN — nevada del 10 de octubre de 2025

- URL: https://www.parquesnacionales.gov.co/sala-prensa/noticias/una-de-las-nevadas-mas-grandes-del-ano-cubre-el-parque-nacional-natural-los-nevados/
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/pnn-nevada-2025.html`

- Hecho: «se registró una de las nevadas más grandes del año en el Parque Nacional Natural Los Nevados»
- Fecha en la página: «10 de octubre de 2025»
- Causas: «una alta nubosidad cargada de humedad, bajas temperaturas y cambios en la presión atmosférica que favorecieron la formación de nieve en la alta montaña.»
- Cobertura de ese evento: «el volcán Nevado del Ruiz, el Nevado de Santa Isabel, el Paramillo del Cisne y el Paramillo de Santa Rosa»
- Entradas: weather_volcano.snow_and_hail, weather_volcano.summit_visibility

## SGC — esquema de estados de alerta

- URL: https://www2.sgc.gov.co/Paginas/estados-de-alerta-volcanes.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-estados-alerta.txt`

- Verde: «Volcán activo en reposo»
- Verde, explicación: «La actividad del volcán se encuentra muy baja, es decir, todos los parámetros que se monitorean presentan niveles muy bajos.»
- Verde, superficie: «Esporádicamente se pueden producir pequeños sismos.»
- Amarilla: «Volcán activo con cambios en el comportamiento del nivel base de los parámetros monitoreados y otras manifestaciones»
- Ceniza y viento: «pueden ocurrir emisiones esporádicas de ceniza (erupciones menores) cuyo alcance y efectos son restringidos, y la dispersión de la ceniza depende de la dirección del viento»
- Sismos sentidos: «Algunos de esos sismos pueden ser sentidos por los pobladores cerca al volcán.»
- Ruidos: «Se pueden escuchar pequeñas explosiones en el cráter activo.»
- Parte alta: «Restringir el acceso a la parte alta del volcán (depende del volcán).»
- Naranja: «Volcán con cambios importantes en los parámetros monitoreados»
- Probabilidad: «aumenta la probabilidad de una o varias erupciones mayores»
- Fenómenos proximales: «lahares con volúmenes pequeños, o corrientes de densidad piroclástica restringidas a la parte proximal del edificio volcánico»
- Proyectiles: «proyectiles balísticos»
- Lahares pequeños: «Se pueden generar avalanchas (lahares) pequeñas en los ríos que nacen en el volcán.»
- Olores: «olores fuertes e irritantes en zonas cercanas al volcán»
- Roja: «Volcán en erupción»
- Evacuación: «Realizar evacuación obligatoria de zonas que pueden ser afectadas por la erupción, dependiendo del volcán y acorde con el mapa de amenaza.»
- Ríos y vías: «Restringir acceso a quebradas o ríos que nacen en el volcán, y a vías o sectores que puedan cruzar el volcán»
- Rayos: «presencia de tormentas eléctricas y rayos en la zona cercana al cráter»
- Columna: «pueden derrumbarse por su peso o salir desde el cráter hacia las laderas del mismo con gran velocidad»
- Lahares grandes: «Se pueden formar grandes avalanchas (lahares) que alcanzan grandes extensiones, incluso centenares de kilómetros.»
- Entradas: weather_volcano.alert_green_meaning, weather_volcano.alert_yellow_meaning, weather_volcano.alert_orange_meaning, weather_volcano.alert_red_meaning, weather_volcano.yellow_upper_access, weather_volcano.yellow_ash_wind, weather_volcano.felt_quakes, weather_volcano.orange_near_volcano, weather_volcano.red_rivers_roads, weather_volcano.red_crater_storms, weather_volcano.ballistic_blocks, weather_volcano.red_column_collapse, weather_volcano.sulfur_smell, weather_volcano.pyroclastic_flows

## SGC — los estados no son una cuenta regresiva

- URL: https://www2.sgc.gov.co/Noticias/Paginas/Como-saber-en-que-estado-de-alerta-por-actividad-volcanica-estan-los-volcanes-del-pais.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-transiciones.txt`

- Sin plazo: «este no estima la probabilidad de una erupción en término de días o semanas»
- Impredecibles: «las erupciones son eventos imposibles de predecir y mientras un volcán esté activo puede hacer erupción en cualquier momento.»
- No secuencial: «un volcán puede pasar de estado de alerta por actividad volcánica Verde a Naranja sin haber tenido que pasar por Amarilla»
- Sin escala numérica: «Tampoco se mantiene la escala numérica asociada a ellos»
- Entradas: weather_volcano.alert_states_nonsequential, weather_volcano.eruptions_not_predictable, weather_volcano.old_alert_numbers

## SGC — tabla del esquema (14 de septiembre de 2023)

- URL: https://www2.sgc.gov.co/Noticias/tpaginas/Tabla-Esquema-estados-de-alerta-volcanes-SGC.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-tabla-alertas.txt`

- Vigencia del esquema: «A partir de septiembre 14 de 2023»
- Entradas: weather_volcano.old_alert_numbers

## UNGRD — comunidades preparadas ante erupciones volcánicas

- URL: http://repositorio.gestiondelriesgo.gov.co/bitstream/handle/20.500.11762/19985/Comunidades_preparadas_ante_erupciones_volcanicas.pdf?sequence=1
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ungrd-comunidades-erupciones.txt`

- Alerta no es evacuación: «No todas las alertas por actividad volcánica significan evacuación inmediata. Las autoridades evaluarán la situación e indicarán cuándo hacerlo.»
- Ceniza: «Ante la emisión de ceniza, proteja vías respiratorias y use sombrilla o capa. Retire la ceniza de los techos, sin utilizar agua.»
- Cierres: «Cierre todas las ventanas, puertas y aberturas por donde pueda ingresar la ceniza.»
- Agua almacenada: «Aliste una reserva de agua y tape los depósitos para que no se contaminen.»
- No acercarse: «No se acerque al volcán, ni a ríos que nacen en él, la curiosidad puede poner en riesgo su vida.»
- Lahares: «Los flujos de lodo o lahares: pueden arrasar y destruir la vegetación, las viviendas y todo lo que se encuentre a su paso.»
- Rugido: «generan un ruido, como un fuerte rugido, al moverse a grandes velocidades por los cauces de los ríos y las quebradas que nacen en el cráter del volcán.»
- Alto: «Si el tiempo no es suficiente para llegar a los puntos de encuentro, busque el lugar más alto y alejado de ríos y quebradas.»
- Agua de río: «Evite consumir agua de ríos o quebradas de montaña o cercanos al volcán, puede estar contaminada.»
- Conducir: «Evite conducir vehículos por vías donde haya caído ceniza, si lo hace, que sea a baja velocidad.»
- Zona segura: «No se mueva de las zonas seguras hasta que las autoridades así lo indiquen.»
- Gases: «Gases volcánicos: una exposición prolongada puede provocar irritación de los ojos y problemas respiratorios.»
- Piroclásticos: «Flujos piroclásticos: son mortales para los seres vivos, debido a que estas nubes calientes de rocas y gases tóxicos se desplazan a grandes velocidades por las laderas del volcán.»
- Sismos: «Los sismos volcánicos: pueden generar pánico en la población, daños en viviendas, deslizamientos en laderas.»
- Escala vieja, en conflicto con el SGC 2023: «(II) Erupción probable en término de días o semanas.»
- Alarma: «Infórmese acerca de cuál es el mecanismo de alarma, cómo funciona, cómo suena o se ve y cómo debe actuar usted.»
- Ruta: «Infórmese acerca del plan de evacuación. Identifique en él las zonas de riesgo, rutas de evacuación y puntos de encuentro en caso de erupción volcánica.»
- Entradas: weather_volcano.alert_not_evacuation, weather_volcano.ash_actions, weather_volcano.ash_roofs, weather_volcano.ash_water, weather_volcano.ash_driving, weather_volcano.stay_safe_zone, weather_volcano.lahar_visitor, weather_volcano.do_not_approach, weather_volcano.volcanic_gases, weather_volcano.pyroclastic_flows, weather_volcano.felt_quakes, weather_volcano.old_alert_numbers, weather_volcano.volcanic_alarm, weather_volcano.evacuation_route

## SGC — guía de preparación ante lluvia de cenizas

- URL: https://www2.sgc.gov.co/Direcciones-Tecnicas/Geoamenazas/Documents/Guia_preparacion_lluvia_cenizas.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-guia-ceniza.txt`

- Respiración previa: «Si tiene bronquitis crónica, enfisema o asma, permanezca dentro de la casa y evite exposiciones innecesarias»
- Adentro: «Permanezca adentro de un edificio»
- Cobijo: «Si usted está al aire libre, busque cobijo (por ejemplo, en un vehículo o edificio)»
- Boca: «Use una máscara, pañuelo o trapo sobre su nariz y boca»
- Lentes: «No use lentes de contacto ya que usándolos podría estar expuesto a una abrasión en la córnea»
- Agua: «Si encuentra cenizas en el agua, déjela reposar y luego use el agua limpia.»
- Sabor: «El agua contaminada con cenizas generalmente tiene sabor desagradable, más que riesgo a producir daños a la salud»
- Se vuelve a levantar: «en los climas secos la ceniza puede ser fácilmente agitada y transportada por el aire y el tráfico»
- Techos, en conflicto con la UNGRD: «Se deben rociar con agua los depósitos de cenizas antes de utilizar las palas para quitarlas, cuidando de que no se humedezcan demasiado cuando cubren los techos»
- Entradas: weather_volcano.ash_actions, weather_volcano.ash_contacts, weather_volcano.ash_water, weather_volcano.ash_asthma, weather_volcano.ash_resuspends, weather_volcano.ash_roofs, weather_volcano.ash_driving

## SGC — hoja informativa del Nevado del Ruiz

- URL: https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-hoja-ruiz.txt`

- Gases: «Los gases característicos que un volcán puede emitir mediante este proceso son: vapor de agua (el más abundante de todos), dióxido de carbono y dióxido de azufre.»
- Irritación: «el dióxido de azufre es irritante a los ojos, garganta y vías respiratorias»
- Dilución: «la mayoría de los gases volcánicos se dispersan y diluyen rápidamente en el aire antes de llegar a zonas pobladas.»
- Entradas: weather_volcano.volcanic_gases, weather_volcano.gases_dilute, weather_volcano.sulfur_smell

## SGC — boletines del Nevado del Ruiz

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/boletines-volcan-nevado-del-ruiz.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-ruiz-boletines.txt`

- Semanales: «En esta página puede consultar los últimos 20 de los Boletines semanales emitidos para el Volcán Nevado del Ruiz.»
- Lista fechada, no es el estado permanente: «Boletín semanal de actividad del volcán Nevado del Ruiz del 10 de noviembre al 16 de noviembre de 2026»
- Mensuales: «Boletines Mensuales»
- Extraordinarios: «Boletines Extraordinarios»
- Extraordinarios, frase: «En esta página puede consultar los Boletines Extraordinarios emitidos para el Volcán Nevado del Ruiz.»
- Entradas: weather_volcano.current_alert, weather_volcano.bulletin_channels, weather_volcano.bulletin_kinds, weather_volcano.separate_volcano_alerts

## SGC — boletín semanal del Ruiz, 10 al 16 de noviembre de 2026

- URL: https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_del_Ruiz_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-ruiz-boletin-2026-11-10-16.txt`
- El PDF fija un color para esa semana. Ninguna respuesta lo copia como alerta vigente.

- Qué se vigila: «la emisión de vapor de agua y gases volcánicos, principalmente dióxido de azufre»
- Cráter: «anomalías térmicas en el fondo del cráter Arenas»
- Canal: «desde el SGC recomendamos seguir atentamente su evolución a través de los boletines semanales y demás información publicada por nuestros canales oficiales, así como atender las instrucciones de las autoridades locales, departamentales y de la Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD).»
- Entradas: weather_volcano.volcanic_activity, weather_volcano.current_alert, weather_volcano.bulletin_channels

## SGC — boletín semanal del Santa Isabel, misma semana

- URL: https://www2.sgc.gov.co/Noticias/boletinesDocumentos/Boletin_semanal_de_actividad_del_volcan_Nevado_de_Santa_Isabel_del_10_de_noviembre_al_16_de_noviembre_de_2026.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-santa-isabel-boletin-2026-11-10-16.txt`
- Tampoco se copia el color de esa semana.

- Volcán distinto: «Volcán Nevado de Santa Isabel»
- Canal propio: «desde el SGC recomendamos seguir atentamente su evolución a través de los boletines semanales y demás información publicada por nuestros canales oficiales»
- Entradas: weather_volcano.santa_isabel_bulletin, weather_volcano.separate_volcano_alerts

## SGC — ficha del Santa Isabel

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadodeSantaIsabel/Paginas/generalidades-volcan-nevado-santa-isabel.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-santa-isabel-generalidades.txt`

- Frase vieja de la ficha, en conflicto con el boletín semanal más reciente descargado: «Es un volcán activo en estado de reposo.»
- Entradas: weather_volcano.santa_isabel_bulletin

## SGC — ficha del Tolima

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoTolima/Paginas/generalidades-volcan-nevado-tolima.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-tolima-generalidades.txt`

- Lahares: «El hecho de ser un volcán nevado ha incrementado las condiciones favorables para la generación de flujos de lodo (lahares).»
- Entradas: weather_volcano.tolima_bulletin, weather_volcano.tolima_lahars

## SGC — ficha del Ruiz, drenajes

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/generalidades-volcan-nevado-ruiz.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-ruiz-generalidades.txt`

- Ríos: «en el edificio volcánico nacen los ríos Güalí, Lagunillas y Recio, afluentes del río Magdalena, y el río Chinchiná, afluente del Cauca; se trata de valles estrechos, profundos y de alta pendiente.»
- Entradas: weather_volcano.ruiz_rivers

## SGC — boletines del Cerro Machín

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/Boletines-Volcan-Cerro-Machin.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-machin-boletines.txt`

- Semanales: «Boletines Semanales»
- Extraordinarios: «En esta página puede consultar los Boletines Extraordinarios emitidos para el Volcán Cerro Machín.»
- Hay lista semanal hasta: «Boletín semanal de actividad del volcán Cerro Machín del 10 de noviembre al 16 de noviembre de 2026»
- Entradas: weather_volcano.machin_bulletin, weather_volcano.bulletin_kinds, weather_volcano.separate_volcano_alerts

## SGC — ficha del Cerro Machín

- URL: https://www2.sgc.gov.co/sgc/volcanes/VolcanCerroMachin/Paginas/generalidades-volcan-cerro-machin.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/sgc-machin-generalidades.txt`

- La misma página trae una línea de estado y, más abajo, «Es un volcán activo en estado de reposo». No se fija ninguna de las dos como alerta de hoy.
- Departamento: «en el departamento del Tolima»
- Entradas: weather_volcano.machin_bulletin

## Parques — Resolución 268 de 2024

- URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2025/01/Res.-No.-268-del-22-de-octubre-de-2024-MODIFICA-PFFO-029-2024.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/pnn-res-268-2024.txt`
- El acto dice «en alerta amarilla» con fecha de 2024. Esa frase no se sirve como color vigente.

- Cumbre: «Ascenso a cumbre o cima nevada (restringido por actividad volcánica).»
- Ciclomontañismo: «Ciclo montañismo tramo carretera Brisas – Arenales – Valle de Las Tumbas (restringido por actividad volcánica).»
- Cierre: «en cualquier momento se puede tomar la determinación de cierre y evacuación, para lo cual deben seguir estrictamente las recomendaciones del personal del Parque.»
- Entradas: weather_volcano.volcanic_closures, weather_volcano.yellow_upper_access

## Parques — Resolución 259 de 2024

- URL: https://www.parquesnacionales.gov.co/wp-content/uploads/2024/10/Res.-No.-259-del-09-de-octubre-de-2024-PFFO-022-2024.pdf
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/pnn-res-259-2024.txt`

- Cierre: «en cualquier momento se puede tomar la determinación de cierre y evacuación, para lo cual deben seguir estrictamente las recomendaciones de los guardaparques.»
- Entradas: weather_volcano.volcanic_closures

## Alcaldía de Manizales — Observatorio

- URL: https://centrodeinformacion.manizales.gov.co/el-detras-de-camaras-del-monitoreo-a-un-volcan-amenazante/
- Fecha de acceso: 2026-11-21
- Archivo: `weather_volcano/evidence/raw/ovsm-manizales.txt`

- Monitoreo: «El Observatorio Vulcanológico y Sismológico de Manizales fue creado en 1986 tras la necesidad sentida de realizar un permanente monitoreo al volcán Nevado del Ruiz»
- Entradas: weather_volcano.ovsm_role, weather_volcano.bulletin_channels

## Cobertura

weather_volcano.park_weather
weather_volcano.rainy_seasons
weather_volcano.no_temperate_seasons
weather_volcano.weather_by_elevation
weather_volcano.freezing_at_altitude
weather_volcano.helada_meaning
weather_volcano.helada_night
weather_volcano.summit_visibility
weather_volcano.snow_and_hail
weather_volcano.current_forecast
weather_volcano.national_forecast_limit
weather_volcano.alert_green_meaning
weather_volcano.alert_yellow_meaning
weather_volcano.alert_orange_meaning
weather_volcano.alert_red_meaning
weather_volcano.alert_states_nonsequential
weather_volcano.eruptions_not_predictable
weather_volcano.old_alert_numbers
weather_volcano.alert_not_evacuation
weather_volcano.yellow_upper_access
weather_volcano.yellow_ash_wind
weather_volcano.felt_quakes
weather_volcano.orange_near_volcano
weather_volcano.red_rivers_roads
weather_volcano.red_crater_storms
weather_volcano.current_alert
weather_volcano.bulletin_channels
weather_volcano.bulletin_kinds
weather_volcano.volcanic_activity
weather_volcano.santa_isabel_bulletin
weather_volcano.tolima_bulletin
weather_volcano.machin_bulletin
weather_volcano.separate_volcano_alerts
weather_volcano.ovsm_role
weather_volcano.ash_actions
weather_volcano.ash_contacts
weather_volcano.ash_water
weather_volcano.ash_driving
weather_volcano.ash_roofs
weather_volcano.ash_asthma
weather_volcano.stay_safe_zone
weather_volcano.lahar_visitor
weather_volcano.ruiz_rivers
weather_volcano.tolima_lahars
weather_volcano.do_not_approach
weather_volcano.volcanic_gases
weather_volcano.gases_dilute
weather_volcano.pyroclastic_flows
weather_volcano.ballistic_blocks
weather_volcano.red_column_collapse
weather_volcano.sulfur_smell
weather_volcano.rain_by_department
weather_volcano.ash_resuspends
weather_volcano.evacuation_route
weather_volcano.volcanic_alarm
weather_volcano.volcanic_closures
