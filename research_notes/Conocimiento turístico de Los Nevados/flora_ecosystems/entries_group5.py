# -*- coding: utf-8 -*-
"""
Entries group 5: Topics 73 to 90
Sponge mechanism, specific river basins, plant adaptations, and conservation/restoration.
"""

PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
HUMBOLDT_URL = "http://www.humboldt.org.co/es/investigacion/proyectos/actuales/item/222-paramos-de-colombia"
COURT_URL = "https://www.cortesuprema.gov.co/"
RAMSAR_URL = "https://rsis.ramsar.org/ris/1781"
DATE_VERIFIED = "2026-11-21"

ENTRIES = [
    {
        "id": "flora_ecosystems.paramo_sponge_mechanism",
        "label": "mecanismo de esponja del páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo funciona la esponja de agua del páramo",
            "por que dicen que el paramo es una esponja",
            "mecanismo de regulacion hidrica en los nevados",
            "como retiene agua el suelo del paramo",
            "venga por que el paramo suelta agua poco a poco",
            "oiga como hacen las plantas y el suelo para guardar agua",
            "suelos andisoles e histosoles como esponjas naturales",
            "infiltracion y liberacion lenta de agua en alta montaña",
            "por que el paramo no se seca en verano",
            "el colchón hidrico de los nevados explicacion",
            "how does the paramo natural water sponge mechanism work",
            "water storage and regulation in high Andean ecosystems",
            "los musgos y el suelo volcanico absorben la lluvia",
            "amortiguacion de crecientes e inundaciones por el paramo"
        ],
        "hard_negatives": [
            "cuántos filtros de agua debo empacar para trekking",
            "dónde comprar cantimploras térmicas en Manizales",
            "cuál es el costo del transporte público a Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El páramo funciona como una colosal esponja natural gracias a la combinación de nieblas frecuentes, musgos que absorben decenas de veces su peso en agua y suelos volcánicos negros (andisoles) de textura porosa. Esta estructura retiene los aguaceros y libera agua filtrada y constante durante los meses secos.",
            "variants": [
                "En lugar de dejar que la lluvia ruede velozmente por las laderas causando avalanchas, la vegetación y el suelo del páramo actúan como un inmenso depósito regulador. Absorben el agua en temporada de lluvias y la ceden poco a poco a los ríos durante el verano."
            ],
            "detail": "Los andisoles e histosoles paramunos pueden almacenar hasta un 80 % o 90 % de su volumen en agua, lo que explica por qué de las altas cumbres nacen quebradas cristalinas inagotables."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.frailejon_water_sponge_function",
            "flora_ecosystems.sphagnum_moss_peat"
        ],
        "tags": ["esponja de agua", "regulacion hidrica", "andisoles", "infiltracion", "caudal continuo"]
    },
    {
        "id": "flora_ecosystems.rio_chinchina_basin_water",
        "label": "nacimiento de cuenca río chinchina",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "dónde nace el río Chinchiná",
            "cuenca del rio chinchina en el parque los nevados",
            "de donde viene el agua de Manizales",
            "el rio chinchina nace en el nevado del ruiz",
            "venga qué quebradas del nevado forman el río chinchiná",
            "oiga de cuál cuenca toma agua la ciudad de manizales",
            "nacientes del rio chinchina en caldas",
            "abastecimiento de agua potable de manizales y villamaria",
            "cuenca alta del rio chinchina y su conservacion",
            "aguas de paramo que surten a aguas de manizales",
            "where does the Chinchina river originate in Los Nevados",
            "river basin providing drinking water to Manizales",
            "quebradas la gruta y rio claro tributarios del chinchina",
            "proteccion de la cuenca del chinchina en el parque"
        ],
        "hard_negatives": [
            "cuánto tiempo se tarda en llegar a Manizales desde Brisas",
            "dónde queda la terminal de transportes de Manizales",
            "cuál es el número de emergencias de la Cruz Roja Caldas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El río Chinchiná nace en los páramos y glaciares del costado occidental del Nevado del Ruiz, en jurisdicción de Caldas. Sus fuentes altas y quebradas tributarias abastecen de agua potable a más de 450.000 personas en el área metropolitana de Manizales y Villamaría, además de mover plantas hidroeléctricas locales.",
            "variants": [
                "La cuenca alta del río Chinchiná se nutre directamente de las turberas y frailejonales del sector norte del parque. Aguas de Manizales capta sus caudales en las partes altas protegidas para garantizar agua de altísima pureza a la capital caldense."
            ],
            "detail": "La protección de los páramos de Villamaría y el Ruiz es la principal garantía para la seguridad hídrica e industrial de todo el departamento de Caldas."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.paramo_sponge_mechanism",
            "flora_ecosystems.rio_otun_basin_water"
        ],
        "tags": ["rio chinchina", "manizales", "villamaria", "caldas", "agua potable"]
    },
    {
        "id": "flora_ecosystems.rio_otun_basin_water",
        "label": "nacimiento de cuenca río otun",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "dónde nace el río Otún",
            "cuenca del rio otun en risaralda",
            "de donde viene el agua de Pereira y Dosquebradas",
            "el rio otun nace en la laguna del otun",
            "venga qué tan importante es el río otún para pereira",
            "oiga cuantos habitantes beben del agua del río otún",
            "nacientes del rio otun en el parque nacional los nevados",
            "cuenca hidrografica del rio otun conservacion",
            "recorrido del rio otun desde el paramo hasta el cauca",
            "proteccion de la cuenca del otun por aguas y aguas de pereira",
            "where does the Otun river originate in the park",
            "river Otun basin supplying drinking water to Pereira",
            "el rio otun como eje hidrico de risaralda",
            "importancia del humedal del otun para el acueducto de pereira"
        ],
        "hard_negatives": [
            "dónde queda el viaducto César Gaviria en Pereira",
            "cuál es la mejor ruta para ir de Pereira al Cedral",
            "cuánto cobran los camperos en la chiva a La Florida"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El río Otún nace formalmente en el desagüe de la Laguna del Otún, a unos 3.900 metros de altitud en el departamento de Risaralda. Es la arteria hídrica más vital de la región, suministrando agua potable a más de 500.000 habitantes en los municipios de Pereira y Dosquebradas.",
            "variants": [
                "Toda el agua que desciende por el río Otún proviene de los humedales Ramsar y páramos del Nevado Santa Isabel. Su cuenca alta está estrictamente protegida por Parques Nacionales y la CARDER para preservar su caudal y pureza cristalina."
            ],
            "detail": "El río recorre un imponente cañón de bosque altoandino antes de llegar a los acueductos municipales, irrigando además fincas cafeteras y reservas biológicas."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Convención Ramsar",
                "url": RAMSAR_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.laguna_del_otun_ecosystem",
            "flora_ecosystems.ramsar_otun_wetland_complex",
            "flora_ecosystems.water_cycle_basin_supply"
        ],
        "tags": ["rio otun", "laguna del otun", "pereira", "dosquebradas", "risaralda"]
    },
    {
        "id": "flora_ecosystems.rio_combeima_coello_water",
        "label": "abastecimiento de cuencas combeima y coello",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "dónde nacen los ríos Combeima y Coello",
            "de donde viene el agua potable de Ibague",
            "cuenca del rio combeima en el nevado del tolima",
            "que rios del tolima nacen en el parque los nevados",
            "venga es verdad que el combeima le da agua a casi toda ibagué",
            "oiga por que es tan importante el nevado del tolima para el agua",
            "cuenca mayor del rio coello y distritos de riego",
            "nacientes del rio combeima en el canón del combeima",
            "abastecimiento del acueducto ibal desde el combeima",
            "distritos de riego usocoello agua de los nevados",
            "where does the Combeima river originate in Los Nevados",
            "river basins supplying water to Ibague and agricultural irrigation",
            "el rio combeima como fuente del ochenta por ciento de ibague",
            "quebradas que bajan del glaciar del tolima hacia el oriente"
        ],
        "hard_negatives": [
            "cómo llegar a Juntas y el Cañón del Combeima desde Ibagué",
            "dónde comprar achiras tolimenses tradicionales",
            "cuántos días se tarda la ascensión al Nevado del Tolima"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El río Combeima nace en los deshielos y páramos del Nevado del Tolima y suministra más del 80 % del agua potable a los más de 550.000 habitantes de la ciudad de Ibagué. Aguas abajo tributa a la cuenca del río Coello, cuyas aguas alimentan el gran distrito de riego de Usocoello para cultivos de arroz y algodón en la meseta tolimense.",
            "variants": [
                "Las aguas que bajan del macizo del Tolima dan vida a la cuenca del Coello-Combeima. Es el corazón socioeconómico del departamento del Tolima, pues garantiza tanto el acueducto de la capital departamental como la agricultura de exportación del valle del Magdalena."
            ],
            "detail": "Debido a las pendientes pronunciadas del Cañón del Combeima, la conservación de sus páramos y bosques de alta montaña es crítica para evitar avalanchas torrenciales."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.paramo_sponge_mechanism"
        ],
        "tags": ["rio combeima", "rio coello", "ibague", "tolima", "usocoello"]
    },
    {
        "id": "flora_ecosystems.rio_quindio_basin_water",
        "label": "nacientes de cuenca río quindio",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "dónde nace el río Quindío",
            "cuenca del rio quindio en el parque nacional los nevados",
            "de donde viene el agua potable de Armenia",
            "quebrada cardenas y rio quindio en el parque",
            "venga qué parte del parque le da agua al departamento del quindío",
            "oiga por que es vital el páramo de quindío para salento y armenia",
            "nacientes del rio quindio en la cuenca del rio la vieja",
            "acueducto de armenia y las fuentes de alta montana",
            "abastecimiento hidrico del quindio desde los nevados",
            "conservacion de la cuenca alta del rio quindio",
            "where does the Quindio river start in Los Nevados park",
            "river Quindio watershed supplying drinking water to Armenia",
            "nacimiento del rio quindio arriba del valle de cocora",
            "paramo de romerales y nacientes del rio quindio"
        ],
        "hard_negatives": [
            "cuál es el precio de la entrada a los parques temáticos del café",
            "cómo llegar de Armenia a Salento en transporte público",
            "dónde comer trucha al ajillo en Salento"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El río Quindío nace en los páramos y bosques de niebla de las estribaciones occidentales del parque, en la zona alta de Salento. Sus aguas alimentan la cuenca del río La Vieja y surten el acueducto principal de Armenia y de los municipios del centro y norte del departamento del Quindío.",
            "variants": [
                "Las quebradas Cárdenas y San José, nacidas en el páramo de Los Nevados, se unen para formar el río Quindío. Su protección asegura el agua potable de más de 300.000 quindianos y el riego de la emblemática zona cafetera regional."
            ],
            "detail": "La cuenca alta del Quindío alberga además fragmentos de bosque nublado con presencia de palma de cera y relictos de encenillales."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.wax_palm_quindio",
            "flora_ecosystems.high_andean_forest"
        ],
        "tags": ["rio quindio", "armenia", "salento", "quindio", "rio la vieja"]
    },
    {
        "id": "flora_ecosystems.rios_guali_lagunilla_recio",
        "label": "cuencas vertiente oriental del tolima",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué ríos del norte del Tolima nacen en el Ruiz",
            "rios guali lagunilla recio y azufrado",
            "cuencas de la vertiente oriental del parque los nevados",
            "de donde bajan los rios hacia murillo y armero",
            "venga que rios nacen en el costado tolimense del parque",
            "oiga cuáles quebradas bajan del nevado del ruiz hacia honda",
            "cuenca del rio guali en herveo casabianca y honda",
            "cuenca del rio lagunilla y su naciente en el nevado",
            "vertiente del magdalena cuencas hidrograficas del tolima",
            "rios que nacen en el páramo del norte del tolima",
            "which rivers of northern Tolima originate on the Ruiz volcano",
            "Guali Lagunilla and Recio river watersheds in Los Nevados",
            "nacimientos de agua en el sector murillo y la esperanza",
            "abastecimiento agricola del norte del tolima desde el parque"
        ],
        "hard_negatives": [
            "cómo llegar a Murillo Tolima por la nueva carretera",
            "cuál fue la historia de la tragedia de Armero en 1985",
            "dónde ver las termales de La Cabaña en Murillo"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En la vertiente oriental del macizo volcánico nacen los ríos Gualí, Lagunilla, Azufrado, Recio y Totare, que descienden por el departamento del Tolima hacia el río Magdalena. Estos ríos abastecen acueductos rurales y urbanos en municipios como Murillo, Herveo, Casabianca, Líbano y Honda, irrigando miles de hectáreas agrícolas.",
            "variants": [
                "Los páramos orientales de Los Nevados drenan hacia el valle del Magdalena a través de ríos caudalosos como el Gualí y el Recio. Son cuencas estratégicas cuya regulación por frailejones y turberas mitiga avalanchas y sostiene la economía campesina del norte tolimense."
            ],
            "detail": "Estas cuencas tienen además un enorme significado geológico e histórico, al coincidir sus cañones con los cauces por donde transcurrieron lahares en erupciones pasadas."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.water_cycle_basin_supply",
            "flora_ecosystems.paramo_sponge_mechanism",
            "flora_ecosystems.rio_combeima_coello_water"
        ],
        "tags": ["rio guali", "rio lagunilla", "rio recio", "tolima", "vertiente magdalena"]
    },
    {
        "id": "flora_ecosystems.adaptation_leaf_pubescence",
        "label": "pelos y vellosidades en hojas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué las plantas del páramo tienen pelos en las hojas",
            "para que sirve la vellosidad blanca en las plantas",
            "pubescencia foliar en la flora de los nevados",
            "hojas peludas y afelpadas en alta montana",
            "venga por que tantas plantas del páramo parecen de terciopelo",
            "oiga para qué le sirven esos pelitos plateados a las hojas",
            "proteccion contra rayos uv por pelos foliares",
            "colchon de aire tibio en hojas lanosas de paramo",
            "por que las hojas no se queman con el sol andino",
            "tricomas y vellosidades protectoras de la flora",
            "why do paramo plants have hairy and woolly leaves",
            "leaf pubescence and trichome adaptations in alpine plants",
            "hojas lanudas de frailejon senecio y lupinus",
            "pelos blancos como escudo contra la radiacion solar"
        ],
        "hard_negatives": [
            "qué bloqueador solar debo comprar para el rostro",
            "qué lentes de sol con filtro UV necesito en la nieve",
            "dónde conseguir guantes térmicos para el frío"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La densa capa de pelos blancos (tricomas) en plantas como frailejones, senecios y lupinos cumple una doble función vital: atrapa una microcapa de aire tibio que amortigua las heladas nocturnas y actúa como un escudo plateado que refleja la intensa radiación ultravioleta del sol de mediodía.",
            "variants": [
                "Ese aspecto de felpa o algodón en las hojas de alta montaña evita que el viento helado deshidrate la planta al reducir la velocidad del aire sobre la superficie foliar. Además, condensa las diminutas gotas de niebla facilitando su absorción."
            ],
            "detail": "Sin esta vellosidad protectora, la radiación UV dañaría el ADN celular y desnaturalizaría las enzimas de fotosíntesis de las plantas andinas."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejon_thermal_adaptation",
            "flora_ecosystems.senecio_and_arnicas",
            "flora_ecosystems.chocho_paramo_lupinus"
        ],
        "tags": ["pubescencia", "tricomas", "pelos lanosos", "radiacion uv", "adaptacion al frio"]
    },
    {
        "id": "flora_ecosystems.adaptation_rosette_growth_form",
        "label": "crecimiento en roseta contra heladas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué las plantas del páramo crecen en roseta",
            "forma de roseta en plantas de alta montana",
            "para que sirve la roseta en frailejones y senecios",
            "ventajas evolutivas de crecer en circulo de hojas",
            "venga por que casi todas las plantas del paramo parecen una rosa",
            "oiga como protege el cogollo la forma de roseta",
            "arquitectura vegetal de roseta gigante y enana",
            "movimiento nictinastico de rosetas que se cierran de noche",
            "proteccion de la yema apical en plantas paramunas",
            "rosetas arrosetadas frente al viento de cordillera",
            "why do many paramo plants grow in a rosette shape",
            "rosette growth form as an adaptation against frost and wind",
            "hojas agrupadas en espiral para resguardar el centro",
            "convergencia evolutiva de rosetas en paramos tropicales"
        ],
        "hard_negatives": [
            "cuántos kilos debe pesar la mochila para alta montaña",
            "a qué hora abren el sendero hacia el mirador",
            "dónde contratar seguro médico para ingresar al parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "La forma en roseta concentra las hojas jóvenes en un círculo apretado alrededor de la yema o meristemo central, resguardando el punto de crecimiento del frío extremo y de los vientos deshidratantes. Por las noches, muchas rosetas se cierran sobre sí mismas como un puño protector para evitar que el cogollo se congele.",
            "variants": [
                "Crecer en roseta es una de las soluciones evolutivas más exitosas en la alta montaña tropical. Las hojas exteriores absorben el impacto de las heladas y vientos, permitiendo que el centro tierno de la planta permanezca resguardado y activo."
            ],
            "detail": "Este movimiento nocturno de cierre de las hojas se conoce como nictinastia y logra mantener el meristemo varios grados por encima de la temperatura del aire ambiente."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.valeriana_paramo",
            "flora_ecosystems.werneria_rosettes"
        ],
        "tags": ["roseta", "meristemo apical", "nictinastia", "arquitectura vegetal", "heladas"]
    },
    {
        "id": "flora_ecosystems.adaptation_thick_cuticle_waxes",
        "label": "cutículas cerosas protectoras contra desecación",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué las hojas del páramo son tan duras y brillantes",
            "hojas coriaceas y cuticula cerosa en plantas de montana",
            "para que sirve la cera en las hojas de paramo",
            "por que las hojas parecen de cuero en el subparamo",
            "venga por que esas hojas tienen una capa brillante como esmalte",
            "oiga por que no se secan las plantas con el viento tan fuerte",
            "ceras epicuticulares y retencion de agua en los nevados",
            "hojas esclerofilas en el ecosistema paramuno",
            "reduccion de la transpiracion por cuticulas gruesas",
            "defensa contra la sequia fisiologica del frio",
            "why are paramo leaves thick leathery and waxy",
            "waxy cuticles and sclerophyllous leaves in alpine shrubs",
            "capa impermeable de cera en arbustos andinos",
            "las hojas duras evitan la perdida de agua por evaporacion"
        ],
        "hard_negatives": [
            "qué crema hidratante llevar para la piel reseca por el viento",
            "cuántos kilómetros por hora alcanzan los vientos en el Ruiz",
            "se puede volar cometa o encender pirotecnia en el parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Muchas plantas del páramo y subpáramo poseen hojas duras como cuero (coriáceas) recubiertas de una gruesa capa de cera impermeable (cutícula). Esta barrera impide que los vientos secos y la fuerte radiación solar evaporen el agua interna de la planta, protegiéndola contra la deshidratación.",
            "variants": [
                "En el clima paramuno el agua puede congelarse en el suelo, volviendo difícil su absorción por las raíces (sequía fisiológica). Las cutículas cerosas y hojas esclerófilas sellan las hojas para retener cada gota de humedad dentro de sus tejidos."
            ],
            "detail": "Arbustos como los romeros (Diplostephium), el chite (Hypericum) y ericáceas exhiben estas hojas esclerófilas que además resisten el daño mecánico del granizo."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.romeros_diplostephium",
            "flora_ecosystems.chite_hypericum",
            "flora_ecosystems.adaptation_leaf_pubescence"
        ],
        "tags": ["cuticula cerosa", "hojas coriaceas", "esclerofilia", "desecacion", "sequia fisiologica"]
    },
    {
        "id": "flora_ecosystems.adaptation_antifreeze_sugars",
        "label": "sustancias anticongelantes en células vegetales",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo evitan las plantas que se les congele la savia",
            "anticongelante natural en las celulas de plantas de paramo",
            "por que las hojas no se rompen con el hielo nocturno",
            "acumulacion de azucares y solutos contra heladas",
            "venga cómo hacen las maticas para no volverse hielo por dentro",
            "oiga que liquido tienen adentro las plantas que aguanta bajo cero",
            "superenfriamiento y solutos osmoticos en flora andina",
            "azucares y proteinas anticongelantes en los nevados",
            "fisiologia de la resistencia al congelamiento celular",
            "como sobreviven las celulas vegetales a cinco bajo cero",
            "how do alpine plants avoid freezing intracellular water",
            "natural antifreeze sugars and osmoprotectants in paramo flora",
            "resistencia a temperaturas bajo cero en celulas de alta montaña",
            "las plantas del paramo toleran el congelamiento extracelular"
        ],
        "hard_negatives": [
            "qué líquido anticongelante necesita el radiador de mi carro",
            "cuál es la temperatura promedio en Manizales en invierno",
            "qué hacer si el carro se vara por frío en la carretera"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las plantas del páramo acumulan altas concentraciones de azúcares solubles, prolina y proteínas especiales en el citoplasma de sus células, lo que disminuye el punto de congelación de sus fluidos internos. Esto permite que el agua dentro de las células permanezca líquida incluso cuando el termómetro baja varios grados bajo cero.",
            "variants": [
                "Al anochecer, las plantas andinas concentran solutos anticongelantes dentro de las células y permiten que los cristales de hielo se formen únicamente en los espacios intercelulares donde no rompen las membranas. Así sobreviven noche tras noche sin sufrir daños estructurales."
            ],
            "detail": "Este mecanismo bioquímico de tolerancia al congelamiento extracelular es indispensable en los trópicos de alta montaña, donde el invierno ocurre prácticamente todas las noches del año."
        },
        "sources": [
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.draba_crucifers_superparamo",
            "flora_ecosystems.frailejon_thermal_adaptation",
            "flora_ecosystems.grimmia_superparamo_moss"
        ],
        "tags": ["anticongelante celular", "azucares solubles", "heladas", "fisiologia vegetal", "superenfriamiento"]
    },
    {
        "id": "flora_ecosystems.adaptation_dwarfism_prostrate",
        "label": "porte enano y plantas pegadas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué las plantas de arriba son tan enanas",
            "porte achaparrado y rastrero en el superpáramo",
            "por que crecen pegadas a la tierra las flores de cumbre",
            "enanismo vegetal en la alta cordillera",
            "venga por que ninguna planta crece alta cerca al glaciar",
            "oiga por que las matas crecen como aplastadas en el suelo",
            "habito rastrero y enano adaptacion al viento",
            "ventajas de ser una planta enana en los nevados",
            "plantas postradas que aprovechan el calor de la tierra",
            "microclima de la capa limite superficial del suelo",
            "why are high mountain plants dwarf and ground-hugging",
            "prostrate dwarfism as an adaptation to alpine winds and frost",
            "plantas almohadilladas pegadas al piso contra vendavales",
            "el viento impide el crecimiento de tallos altos arriba"
        ],
        "hard_negatives": [
            "cuántos metros de altura tiene el mirador Valle de las Tumbas",
            "se pueden cortar ramas pequeñas para recuerdo",
            "a qué hora abren el acceso por Brisas"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En el superpáramo y páramo alto, las plantas adoptan un porte enano y rastrero pegado al suelo para evitar los vientos huracanados que quebrarían tallos erguidos. Al mantenerse a ras de tierra, aprovechan la fina capa de aire caliente que el sol calienta sobre las rocas y el suelo.",
            "variants": [
                "El enanismo vegetal es una respuesta directa al frío y al viento de Los Nevados. Las plantas reducen la longitud de sus tallos y crecen horizontales o en almohadillas para minimizar la superficie expuesta a la intemperie gélida."
            ],
            "detail": "A pocos centímetros del suelo la velocidad del viento cae drásticamente debido a la fricción superficial, creando una zona de calma térmica donde estas pequeñas hierbas logran florecer."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.superparamo_ecosystem",
            "flora_ecosystems.lachemilla_nivalis",
            "flora_ecosystems.werneria_rosettes"
        ],
        "tags": ["enanismo vegetal", "porte rastrero", "capa limite", "viento helado", "superparamo"]
    },
    {
        "id": "flora_ecosystems.adaptation_shallow_spreading_roots",
        "label": "raíces extendidas en suelos volcánicos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo son las raíces de las plantas del páramo",
            "raices superficiales y extendidas en suelos volcanicos",
            "por que las raices no crecen muy profundas en el paramo",
            "sistema radicular fasciculado de los frailejones y pastos",
            "venga cómo se agarran las plantas a esa tierra arenosa",
            "oiga por que las raices se extienden a los lados y no hacia abajo",
            "retencion de suelo volcanico por raices andinas",
            "adaptacion radicular a suelos con ceniza y rocas",
            "absorcion de agua superficial por raices de pajonal",
            "entramado de raices contra la erosion en pendientes",
            "how are plant roots adapted to shallow volcanic soils",
            "shallow spreading root systems of high Andean plants",
            "red de raices que amarra la tierra negra del paramo",
            "raices protegidas del suelo permanentemente helado"
        ],
        "hard_negatives": [
            "se pueden arrancar raíces de plantas para estudiarlas",
            "dónde comprar botas con buen agarre para roca mojada",
            "cuántos kilómetros camina un turista en el sendero corto"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Muchas plantas del páramo desarrollan redes densas de raíces fasciculadas y superficiales que se extienden horizontalmente en los primeros 20 a 30 centímetros del suelo. Esta red les permite captar rápidamente el agua de lluvias y nieblas antes de que percole en la ceniza, amarrando el suelo volcánico contra la erosión.",
            "variants": [
                "En suelos andisoles con ceniza volcánica, las raíces crecen extendidas hacia los lados para anclar con firmeza la planta frente a los vendavales. Al formar un denso tejido subterráneo, evitan que las lluvias torrenciales desmoronen las laderas de la cordillera."
            ],
            "detail": "A mayor profundidad el suelo suele ser frío, compacto y anóxico, por lo que la mayor actividad biológica y de absorción radicular se concentra en la capa orgánica superior."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.mycorrhizae_paramo_roots",
            "flora_ecosystems.pajonales_calamagrostis",
            "flora_ecosystems.permafrost_and_cryoturbation"
        ],
        "tags": ["raices superficiales", "anclaje", "suelos volcanicos", "erosion", "red radicular"]
    },
    {
        "id": "flora_ecosystems.sujeto_de_derechos_ruling",
        "label": "parque declarado sujeto de derechos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué significa que el parque sea sujeto de derechos",
            "sentencia STL 10716 de 2020 parque los nevados",
            "por que declararon al parque sujeto de derechos",
            "fallo de la corte sobre el parque nacional los nevados",
            "venga qué es eso de que la montaña y los páramos tienen derechos",
            "oiga que obligaciones tienen las gobernaciones con el parque",
            "corte suprema de justicia sentencia parque los nevados",
            "proteccion juridica de la vida y agua en los nevados",
            "plan conjunto de restauracion por sentencia judicial",
            "derechos a la vida salud y ambiente sano del parque",
            "what does it mean that Los Nevados park is a subject of rights",
            "Supreme Court ruling STL 10716 declaring the park a legal subject",
            "sentencia judicial que protege los nevados de colombia",
            "orden judicial para retirar ganado y recuperar fuentes hidricas"
        ],
        "hard_negatives": [
            "cómo presentar una queja sobre un guía turístico",
            "dónde pagar las multas de tránsito en Villamaría",
            "cuántos policías cuidan la entrada del parque"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En 2020, la Corte Suprema de Justicia de Colombia declaró al Parque Nacional Natural Los Nevados como Sujeto de Derechos mediante la Sentencia STL 10716. Este fallo histórico reconoce que el parque tiene derecho a la protección, conservación, mantenimiento y restauración de sus páramos, humedales y fuentes hídricas.",
            "variants": [
                "La declaratoria como sujeto de derechos obliga al Gobierno Nacional, Parques Nacionales y a las gobernaciones de Caldas, Risaralda, Quindío y Tolima a ejecutar un plan integral para erradicar la ganadería ilegal, frenar quemas y reforestar cuencas de alta montaña."
            ],
            "detail": "Esta jurisprudencia equipara la protección de los ecosistemas del parque a la defensa de los derechos fundamentales a la vida y al agua de las generaciones presentes y futuras."
        },
        "sources": [
            {
                "label": "Corte Suprema de Justicia de Colombia",
                "url": COURT_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.cattle_grazing_impact",
            "flora_ecosystems.ecological_restoration_programs",
            "flora_ecosystems.water_cycle_basin_supply"
        ],
        "tags": ["sujeto de derechos", "sentencia stl 10716", "corte suprema", "proteccion legal", "conservacion"]
    },
    {
        "id": "flora_ecosystems.cattle_grazing_impact",
        "label": "impacto del ganado en páramos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué hace daño el ganado en el páramo",
            "impacto de la ganaderia bovina en los nevados",
            "por que no debe haber vacas ni caballos en el parque",
            "dano del ganado a los frailejones y humedales",
            "venga por que sacan las vacas del parque nacional",
            "oiga las pezuñas de las vacas rompen los cojines de agua",
            "compactacion del suelo paramuno por pisoteo de ganado",
            "pastoreo ilegal y degradacion de turberas en caldas y tolima",
            "consumo de plantulas de frailejon por ganado vacuno",
            "contaminacion de nacimientos de agua por heces de ganado",
            "why is cattle grazing harmful to the paramo ecosystem",
            "impact of livestock trampling and grazing in Los Nevados",
            "problemas de la ganaderia extensiva en alta montana",
            "recuperacion de areas liberadas de pastoreo"
        ],
        "hard_negatives": [
            "se permite el paseo a caballo para turistas en el parque",
            "dónde comprar carne asada o comida campestre",
            "cuántos días dura la cabalgata a la Laguna del Otún"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "El ganado vacuno y equino causa graves daños en el páramo: sus pesadas pezuñas compactan los suelos esponjosos, destruyen los cojines de agua y pisotean plántulas tiernas de frailejón. Además, consumen la vegetación nativa y sus heces contaminan los nacimientos de agua que abastecen los acueductos urbanos.",
            "variants": [
                "Las vacas y caballos no pertenecen al ecosistema de alta montaña andina. Al pisar las turberas rompen su capacidad de retención hídrica y abren zanjas que aceleran la erosión de laderas, por lo que Parques Nacionales trabaja en acuerdos para su retiro voluntario."
            ],
            "detail": "El retiro del ganado en sectores como El Cisne y Otún ha demostrado que el páramo inicia una asombrosa regeneración natural de pajonales y frailejones en pocos años."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Corte Suprema de Justicia de Colombia",
                "url": COURT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.sujeto_de_derechos_ruling",
            "flora_ecosystems.cojines_plantago_rigida",
            "flora_ecosystems.ecological_restoration_programs"
        ],
        "tags": ["ganado", "pastoreo ilegal", "pisoteo", "compactacion", "contaminacion hidrica"]
    },
    {
        "id": "flora_ecosystems.wildfire_impact_and_recovery",
        "label": "incendios de cobertura y recuperación",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cómo se recupera el páramo después de un incendio",
            "impacto de los incendios forestales en la vegetacion",
            "cuanto tarda en recuperarse un frailejondal quemado",
            "quemas y fuegos en el parque nacional los nevados",
            "venga por que tardan tanto en volver a nacer las plantas tras el fuego",
            "oiga por que no se debe prender ni una colilla en la montaña",
            "regeneracion post incendio en pastizales y turberas",
            "destruccion de suelo organico por fuegos de paramo",
            "incendios en temporadas secas por fenomeno de el niño",
            "perdida de biodiversidad por incendios en caldas y tolima",
            "how does paramo vegetation recover after a wildfire",
            "wildfire damage and slow ecological recovery in Los Nevados",
            "las turberas se queman bajo tierra durante los incendios",
            "fuegos provocados por quemas agricolas descontroladas"
        ],
        "hard_negatives": [
            "cuál es el teléfono de los bomberos en Manizales",
            "se puede fumar cigarrillo electrónico en el sendero",
            "dónde comprar estufa portátil de gas para campamento"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Los incendios en el páramo calcinan la materia orgánica superficial y matan las colonias de frailejones, cuya regeneración tarda varias décadas. Aunque los pajonales pueden rebrotar en uno o dos años, la estructura esponjosa del suelo y las turberas subterráneas sufren daños severos que pueden tomar más de 50 años en sanar.",
            "variants": [
                "El fuego destruye el banco de semillas nativo y deja la tierra expuesta a que la lluvia la lave hacia los ríos. En épocas de sequía extrema o fenómeno de El Niño, un fósforo o colilla puede desencadenar desastres ecológicos de enormes proporciones."
            ],
            "detail": "En las turberas secas, el fuego puede arder bajo tierra de manera invisible durante semanas, quemando las capas de turba acumuladas durante siglos."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.frailejon_fire_vulnerability",
            "flora_ecosystems.turberas_bogs_peatlands",
            "flora_ecosystems.paramo_carbon_sequestration"
        ],
        "tags": ["incendios de cobertura", "fuego", "regeneracion natural", "ceniza", "el niño"]
    },
    {
        "id": "flora_ecosystems.invasive_plants_threat",
        "label": "riesgo de plantas exóticas invasoras",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay plantas invasoras en el parque Los Nevados",
            "amenaza del retamo espinoso en la cordillera central",
            "plantas exoticas que invaden el paramo",
            "especies vegetales invasoras en caldas y tolima",
            "venga qué plantas traidas de afuera amenazan a los frailejones",
            "oiga por que es peligroso el retamo espinoso cerca al parque",
            "ulex europaeus riesgo de invasion en los nevados",
            "pastos introducidos para ganaderia en la alta montana",
            "control de especies exoticas por parques nacionales",
            "como compiten las plantas invasoras con la flora nativa",
            "are invasive alien plants a threat in Los Nevados park",
            "threat of invasive gorse Ulex europaeus in Colombian paramos",
            "pastos foraneos que desplazan a calamagrostis",
            "medidas preventivas contra el retamo en zonas de amortiguacion"
        ],
        "hard_negatives": [
            "se pueden ingresar semillas o flores de otra región",
            "cuántos días dura la cuarentena para mascotas",
            "dónde comprar abono orgánico en Villamaría"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Especies invasoras como el retamo espinoso (Ulex europaeus) y ciertos pastos foráneos introducidos históricamente para ganadería (como Holcus lanatus) representan una grave amenaza para Los Nevados. Estas plantas exóticas crecen velozmente, acidifican el suelo, desplazan a frailejones y aumentan el riesgo de incendios.",
            "variants": [
                "Parques Nacionales monitorea y erradica oportunamente cualquier brote de retamo espinoso o especies foráneas en las vías de acceso y zonas de amortiguación. Su proliferación alteraría el equilibrio hidrológico y la biodiversidad nativa del páramo."
            ],
            "detail": "Para evitar transportar semillas foráneas adheridas al calzado o vehículos, los visitantes deben limpiar sus botas y mantenerse estrictamente en los caminos oficiales."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Instituto Alexander von Humboldt",
                "url": HUMBOLDT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.pine_eucalyptus_plantations_impact",
            "flora_ecosystems.ecological_restoration_programs",
            "flora_ecosystems.sujeto_de_derechos_ruling"
        ],
        "tags": ["plantas invasoras", "retamo espinoso", "ulex europaeus", "pastos exoticos", "bioseguridad"]
    },
    {
        "id": "flora_ecosystems.pine_eucalyptus_plantations_impact",
        "label": "impacto de plantaciones forestales exóticas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué hay pinos y eucaliptos cerca del parque",
            "impacto de los pinos y eucaliptos en el agua del paramo",
            "plantaciones forestales comerciales en zonas de amortiguacion",
            "los pinos secan las fuentes de agua en la cordillera",
            "venga por que dicen que los pinos gringos danan la tierra del monte",
            "oiga por que no crece nada debajo de los bosques de pinos",
            "acidificacion del suelo por aciculas de pino patula",
            "sustitucion de bosque nativo por plantaciones de coniferas",
            "diferencia hidrologica entre bosque nativo y pinos sembrados",
            "restauracion de antiguas plantaciones forestales en caldas",
            "impact of exotic pine and eucalyptus plantations near the park",
            "why commercial pine trees degrade native Andean watersheds",
            "pino patula y eucalipto consumo excesivo de agua",
            "conversion de pinares a bosque altoandino nativo"
        ],
        "hard_negatives": [
            "se puede talar madera de pino para fogata",
            "dónde comprar carbón vegetal en Santa Rosa de Cabal",
            "cuántos aserraderos hay en la región cafetera"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "Las antiguas plantaciones comerciales de pino pátula y eucalipto en zonas de amortiguación consumen grandes cantidades de agua y sus acículas ácidas impiden que crezcan plantas nativas en el sotobosque. Parques Nacionales y las corporaciones ambientales adelantan planes para sustituir estos monocultivos por árboles autóctonos.",
            "variants": [
                "A diferencia del bosque nativo que filtra y conserva agua, los pinos exóticos absorben gran parte de las lluvias y resecan las quebradas. Restaurar estas áreas con encenillos, alisos y Polylepis es fundamental para recuperar la capacidad hídrica de las cuencas."
            ],
            "detail": "Bajo un pinar exótico la biodiversidad de aves e insectos disminuye hasta un 80 % comparada con un bosque altoandino virgen de encenillos y bromelias."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.pino_romeron_podocarpus",
            "flora_ecosystems.high_andean_forest",
            "flora_ecosystems.ecological_restoration_programs"
        ],
        "tags": ["pinos exoticos", "eucalipto", "pino patula", "acidificacion", "restauracion forestal"]
    },
    {
        "id": "flora_ecosystems.ecological_restoration_programs",
        "label": "restauración ecológica y viveros comunitarios",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "qué programas de restauración ecológica hay en el parque",
            "proyectos de reforestacion y conservacion en los nevados",
            "como ayudan las comunidades a restaurar el paramo",
            "viveros comunitarios de alta montana en caldas y tolima",
            "venga qué estan haciendo para sembrar plantas nativas de nuevo",
            "oiga como recuperan los potreros viejos para que vuelva el bosque",
            "restauracion pasiva y activa en el parque nacional",
            "acuerdos de conservacion con campesinos locales",
            "siembra de polylepis y frailejones en areas degradadas",
            "alianzas entre parques nacionales carder corpocaldas y cortolima",
            "what ecological restoration programs exist in Los Nevados",
            "community nurseries and reforestation projects in the park",
            "aislamiento de rondas hidricas para regeneracion natural",
            "gobernanzas ambientales y restauracion participativa de cuencas"
        ],
        "hard_negatives": [
            "cómo puedo inscribirme como guardaparque voluntario",
            "dónde pagar el seguro obligatorio de asistencia médica",
            "cuál es el horario de atención de la oficina de Parques en Manizales"
        ],
        "entities": {},
        "needs": [],
        "answer": {
            "short": "En Los Nevados se adelantan programas de restauración activa y pasiva, combinando el aislamiento de áreas ganaderas con la siembra de árboles nativos (Polylepis, encenillo, aliso) y frailejones criados en viveros comunitarios. Estas iniciativas involucran a familias campesinas locales en la custodia de las cuencas.",
            "variants": [
                "Gracias a la Sentencia de Sujeto de Derechos, Parques Nacionales y las corporaciones regionales (CARDER, Corpocaldas, Cortolima y CRQ) unen esfuerzos para restaurar corredores biológicos. Se prioriza la regeneración natural permitiendo que el pajonal y el bosque reconquisten antiguos potreros."
            ],
            "detail": "Los viveros de alta montaña gestionados por asociaciones comunitarias brindan empleo local y fortalecen el sentido de pertenencia y protección de este territorio sagrado."
        },
        "sources": [
            {
                "label": "Parques Nacionales Naturales de Colombia",
                "url": PNN_URL,
                "retrieved_at": DATE_VERIFIED
            },
            {
                "label": "Corte Suprema de Justicia de Colombia",
                "url": COURT_URL,
                "retrieved_at": DATE_VERIFIED
            }
        ],
        "last_verified": DATE_VERIFIED,
        "valid_until": None,
        "related": [
            "flora_ecosystems.sujeto_de_derechos_ruling",
            "flora_ecosystems.frailejon_nursery_propagation",
            "flora_ecosystems.polylepis_sericea_colorado"
        ],
        "tags": ["restauracion ecologica", "viveros comunitarios", "regeneracion pasiva", "acuerdos campesinos", "reforestacion"]
    }
]
