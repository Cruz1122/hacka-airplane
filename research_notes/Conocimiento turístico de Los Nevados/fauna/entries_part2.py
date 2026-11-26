"""Part 2 of fauna entries: Birds 31-36, Mammals 37-54, Herpetofauna 55-60."""
from sources import (
    SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA,
    SOURCE_HUMBOLDT, SOURCE_EBIRD, SOURCE_CARDER, SOURCE_CORPOCALDAS, SOURCE_CORTOLIMA
)

ENTRIES_PART2 = [
    # 31. Rufous-collared Sparrow (Copetón)
    {
        "id": "fauna.rufous_collared_sparrow",
        "label": "copetón o chingolo andino en alta montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "copetón andino",
            "Zonotrichia capensis",
            "chingolo en Los Nevados",
            "pájaro con cresta pequeña y collar rufo",
            "¿hasta qué altura suben los copetones?",
            "pajarito común en páramo y morrenas",
            "copeton cantando en la manana fria",
            "ave pequena en rocas y arbustos",
            "Rufous-collared sparrow high altitude",
            "Zonotrichia capensis in the paramo",
            "copetoncito buscando migas en el suelo",
            "pajaro cantor de montaña en Colombia"
        ],
        "hard_negatives": [
            "prohibición de alimentar a las aves con pan",
            "vestuario térmico y guantes para frío",
            "registro de visitantes en puestos de control"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "El copetón (Zonotrichia capensis) es un pájaro extraordinariamente resistente y adaptable que acompaña al visitante desde las ciudades cafeteras hasta el superpáramo por encima de los 4.300 metros. Se reconoce por su pequeño copete eréctil, rayas negras en la cabeza y un cálido collar rufo en la nuca. Salta incansable entre rocas, arena volcánica y arbustos buscando pequeñas semillas e insectos.",
            "variants": [
                "Zonotrichia capensis desafía el frío extremo y el viento en las morrenas volcánicas; su silbido matutino de cuatro notas es una compañía constante en casi todos los refugios del parque."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.great_thrush", "fauna.tawny_antpitta", "fauna.birds_overview"],
        "tags": ["copeton", "zonotrichia", "chingolo", "comun", "alta_montana"]
    },
    # 32. Paramo Short-eared Owl & pygmy owl
    {
        "id": "fauna.short_eared_owl_paramo",
        "label": "búho de páramo y lechuzas altoandinas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "búho de páramo",
            "Asio flammeus bogotensis",
            "lechuzas en Los Nevados",
            "Glaucidium jardinii",
            "mochuelo andino",
            "¿hay búhos cazando en el páramo?",
            "ave rapaz nocturna de alta montaña",
            "buho cazador de ratones en pajonales",
            "Short-eared owl Colombian paramo",
            "Andean pygmy-owl Los Nevados",
            "lechucita que vuela al atardecer",
            "aves rapaces nocturnas en el parque"
        ],
        "hard_negatives": [
            "linternas frontales y equipo de campamento nocturno",
            "riesgo de hipotermia por descenso de temperatura",
            "reglamento de pernoctada en zonas de camping"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "En el parque habitan rapaces nocturnas y crepusculares como el búho de páramo (Asio flammeus bogotensis) y el mochuelo andino (Glaucidium jardinii). A diferencia de otros búhos de bosque, el búho de páramo caza activamente al atardecer y amanecer, planeando a baja altura sobre los pajonales para capturar ratones andinos. Su plumaje beige jaspeado le brinda un camuflaje impecable entre las macollas secas.",
            "variants": [
                "Asio flammeus bogotensis patrulla el páramo abierto al caer la tarde en busca de pequeños roedores; su vuelo silencioso y su capacidad de girar la cabeza lo convierten en un depredador muy eficiente."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_rodents_shrews", "fauna.black_chested_buzzard_eagle", "fauna.birds_overview"],
        "tags": ["buho_paramo", "asio_flammeus", "mochuelo", "rapaz_nocturna", "pajonales"]
    },
    # 33. Andean Gull
    {
        "id": "fauna.andean_gull",
        "label": "gaviota andina en lagunas de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "gaviota andina",
            "Chroicocephalus serranus",
            "Larus serranus",
            "¿hay gaviotas en la montaña y lagunas?",
            "gaviota de páramo en Los Nevados",
            "pájaro blanco con cabeza negra en la laguna",
            "ave marina viviendo a cuatro mil metros",
            "gaviota de agua dulce en alta montaña",
            "Andean gull high mountain lakes Colombia",
            "Chroicocephalus serranus Los Nevados",
            "gaviotas volando sobre la Laguna del Otún",
            "ave acuatica blanca en lagunas paramunas"
        ],
        "hard_negatives": [
            "senderos peatonales alrededor de la Laguna del Otún",
            "clima y precipitaciones en la cuenca del río Otún",
            "mitos sobre criaturas mágicas en las lagunas"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "La gaviota andina (Chroicocephalus serranus) rompe la idea habitual de que las gaviotas son exclusivas del mar: esta especie vive todo el año en lagunas y humedales de la cordillera andina entre 3.000 y 4.500 metros. Durante la época reproductiva exhibe una capucha de plumas negras en la cabeza que contrasta con su cuerpo blanco y alas grises. Se alimenta de insectos acuáticos, lombrices y pequeños peces en las orillas de la Laguna del Otún.",
            "variants": [
                "Chroicocephalus serranus es una auténtica gaviota de alta montaña; planea sobre lagunas y turberas del parque alimentándose de invertebrados acuáticos sin descender jamás al nivel del mar."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.andean_coot", "fauna.spotting_sector_otun"],
        "tags": ["gaviota_andina", "chroicocephalus", "lagunas", "humedales", "otun"]
    },
    # 34. Andean Coot (Tingua o focha andina)
    {
        "id": "fauna.andean_coot",
        "label": "tingua o focha andina en humedales",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tingua andina",
            "focha andina",
            "Fulica americana columbiana",
            "pájaro negro de agua con escudo blanco",
            "tingua de páramo en humedales",
            "¿qué ave nada entre los juncos en la laguna?",
            "gallareta de alta montaña",
            "pajaro acuatico oscuro en Los Nevados",
            "Andean coot Colombia wetlands",
            "Fulica americana high altitude lake",
            "tingua nadando con crias en el agua",
            "aves de juncal en humedales altoandinos"
        ],
        "hard_negatives": [
            "sitio Ramsar del Complejo de Humedales Otún",
            "prohibición de nadar en lagunas del parque",
            "fuentes de agua para consumo en el páramo"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "La tingua o focha andina (Fulica americana columbiana) es un ave acuática de cuerpo redondeado y color pizarra oscuro con un distintivo pico y escudete frontal de color blanco marfil. Habita en humedales tranquilos y orillas de lagunas altoandinas como la del Otún, donde construye grandes nidos flotantes anclados a la vegetación. Nada con un movimiento característico de cabeza y se alimenta de algas y plantas acuáticas sumergidas.",
            "variants": [
                "Esta ave acuática protegida habita en los juncales de lagunas altoandinas; sus patas con dedos lobulados le permiten nadar con agilidad y caminar sobre vegetación flotante."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.andean_gull", "fauna.noble_snipe"],
        "tags": ["tingua", "focha_andina", "fulica", "humedales", "laguna_otun"]
    },
    # 35. Noble Snipe (Agachadiza noble)
    {
        "id": "fauna.noble_snipe",
        "label": "agachadiza noble o caica de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "agachadiza noble",
            "caica de páramo",
            "Gallinago nobilis",
            "Gallinago jamesoni",
            "pájaro con pico largo en lodazales del páramo",
            "ave zancuda pequeña en turberas",
            "¿qué pájaro clava el pico en el barro del páramo?",
            "agachadiza andina camuflada en el pasto",
            "Noble snipe Colombian paramo",
            "Gallinago nobilis bogs Los Nevados",
            "pajaro que vuela rapido en zigzag al asustarse",
            "ave limicola de alta montaña"
        ],
        "hard_negatives": [
            "turberas y colchones de agua como reguladores hídricos",
            "tipo de calzado para no resbalar en lodazales",
            "erosión de senderos por paso de caminantes"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "La agachadiza noble (Gallinago nobilis) es un ave limícola de alta montaña con un pico recto excepcionalmente largo y sensible, adaptado para sondear el barro blando de turberas y bofedales en busca de lombrices. Su plumaje pardo rayado imita con tal exactitud los pajonales secos que permanece inmóvil hasta que alguien casi la pisa, momento en el que despega con un vuelo rápido en zigzag y un graznido áspero.",
            "variants": [
                "Gallinago nobilis se especializa en turberas y zonas pantanosas de páramo; su plumaje mimético la hace prácticamente invisible mientras se alimenta sondeando el suelo saturado de agua."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.andean_duck", "fauna.andean_coot", "fauna.birds_overview"],
        "tags": ["agachadiza", "caica", "gallinago_nobilis", "turberas", "camuflaje"]
    },
    # 36. Mountain Tanagers (Tangaras de montaña)
    {
        "id": "fauna.mountain_tanagers",
        "label": "tangaras de montaña y bandadas mixtas",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tangaras de montaña",
            "Anisognathus igniventris",
            "Buthraupis montana",
            "bandadas mixtas de aves en bosque nublado",
            "pájaros de colores brillantes en el frío",
            "tangara ventriescarlata en Los Nevados",
            "tangara azul y negra de alta montaña",
            "¿por qué viajan juntos tantos pájaros de colores?",
            "Mountain tanagers cloud forest Colombia",
            "mixed species feeding flocks Los Nevados",
            "pajaritos de colores en arboles de niebla",
            "tangaras comiendo frutas de bosque altoandino"
        ],
        "hard_negatives": [
            "árboles frutales y flora arbórea del bosque nublado",
            "zonas habilitadas para picnic en el sendero",
            "servicios de fotografía turística en el parque"
        ],
        "entities": {"animal_group": ["aves"]},
        "needs": [],
        "answer": {
            "short": "En los bosques de niebla de Los Nevados podrás presenciar el espectáculo de las bandadas mixtas: decenas de tangaras de vivos colores, como la tangara ventriescarlata (Anisognathus igniventris) y la tangara montana (Buthraupis montana), desplazándose juntas por el dosel. Al forrajear en grupo aumentan su eficiencia para encontrar frutos y bayas silvestres mientras disminuyen el riesgo de ser atacadas por rapaces.",
            "variants": [
                "Las tangaras de montaña aportan destellos de azul, amarillo y escarlata entre la niebla del bosque altoandino; viajan en grupos ruidosos que avanzan rápido de árbol en árbol."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_EBIRD, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.hooded_mountain_toucan", "fauna.birds_overview", "fauna.spotting_sector_la_pastora"],
        "tags": ["tangaras", "anisognathus", "buthraupis", "bandadas_mixtas", "bosque_niebla"]
    },
    # 37. Spectacled Bear (Oso de anteojos)
    {
        "id": "fauna.spectacled_bear",
        "label": "oso de anteojos u oso andino",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "oso de anteojos",
            "oso andino",
            "Tremarctos ornatus",
            "¿hay osos en Los Nevados?",
            "único oso de Sudamérica en el parque",
            "características del oso de anteojos",
            "¿el oso andino es peligroso para los turistas?",
            "oso con manchas blancas en los ojos",
            "Spectacled bear Los Nevados National Park",
            "Andean bear Tremarctos ornatus Colombia",
            "donde vive el oso de anteojos en el parque",
            "mamifero grande con antifaz blanco"
        ],
        "hard_negatives": [
            "protocolo de evacuación médica por helicóptero",
            "registro de visitantes con guías certificados",
            "historias y leyendas sobre el oso en Colombia"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El oso de anteojos u oso andino (Tremarctos ornatus) es el único úrsido nativo de Sudamérica y una de las especies prioritarias de conservación en Los Nevados. Se reconoce por su pelaje negro o castaño oscuro y las manchas blanquecinas alrededor de los ojos y el pecho, que forman un patrón único e irrepetible en cada individuo. Es un animal pacífico, solitario y esquivo que rehúye el contacto humano.",
            "variants": [
                "Tremarctos ornatus habita entre los bosques nublados y páramos del parque; es tímido por naturaleza y cumple una función crucial como dispersor de semillas y modelador de la vegetación."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.bear_diet_habits", "fauna.encounter_spectacled_bear", "fauna.mammals_overview"],
        "tags": ["oso_anteojos", "oso_andino", "tremarctos_ornatus", "mamiferos", "sombrilla"]
    },
    # 38. Bear diet and habits
    {
        "id": "fauna.bear_diet_habits",
        "label": "alimentación y hábitos del oso andino",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "¿qué come el oso de anteojos?",
            "dieta del oso andino en Los Nevados",
            "el oso de anteojos es carnívoro o vegetariano",
            "alimentacion a base de frailejones y bromelias",
            "plataformas en los árboles construidas por osos",
            "costumbres y horarios del oso de anteojos",
            "como busca comida el oso en el paramo",
            "bromelias comidas por osos en el sendero",
            "Spectacled bear diet high Andes",
            "what does the Andean bear eat?",
            "el oso come carne o plantas",
            "huellas y rastros de osos comiendo achupallas"
        ],
        "hard_negatives": [
            "alimentación y raciones recomendadas para caminatas",
            "bromelias y orquídeas del bosque altoandino",
            "manejo de basuras en zonas de campamento"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "Más del 90 % de la dieta del oso de anteojos es de origen vegetal: consume corazones tiernos de bromelias terrestres (achupallas o Puyas), cogollos de frailejón, cortezas de árboles y frutos silvestres de montaña. En los bosques de niebla trepa a grandes alturas y dobla ramas para fabricar 'plataformas' de descanso donde duerme y se alimenta con tranquilidad. Ocasionalmente complementa su nutrición con pequeños invertebrados.",
            "variants": [
                "El oso andino es predominantemente vegetariano; sus poderosas mandíbulas le permiten desarmar espinosas bromelias y frailejones para extraer sus bases nutritivas y jugosas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_CARDER],
        "last_verified": "2026-11-21",
        "related": ["fauna.spectacled_bear", "fauna.encounter_spectacled_bear", "fauna.mammals_overview"],
        "tags": ["dieta_oso", "bromelias", "puya", "habitos", "alimentacion"]
    },
    # 39. Mountain Tapir (Danta de montaña)
    {
        "id": "fauna.mountain_tapir",
        "label": "danta de montaña o danta de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "danta de montaña",
            "danta de páramo",
            "Tapirus pinchaque",
            "tapir lanudo en Los Nevados",
            "¿qué es la danta de montaña?",
            "mamífero con trompa en el páramo",
            "características de la danta de los nevados",
            "danta con pelaje grueso para el frío",
            "Mountain tapir Tapirus pinchaque Los Nevados",
            "woolly tapir endangered Colombia",
            "donde ver dantas de paramo",
            "animal grande parecido a un burrito con trompa"
        ],
        "hard_negatives": [
            "dantas amazónicas de tierras bajas",
            "paseos a caballo prohibidos en senderos de conservación",
            "vestimenta y calzado para cruzar humedales"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La danta de montaña o tapir andino (Tapirus pinchaque) es el mamífero terrestre nativo más grande de los Andes septentrionales, catalogado En Peligro de extinción. Para soportar el frío y los vientos gélidos, posee un pelaje denso y lanudo de color pardo oscuro, labios orlados de blanco y una trompa prensil flexible con la que ramonea hojas, brotes tiernos y cortezas. Es un nadador excelente que disfruta de los baños en lagunas y turberas.",
            "variants": [
                "Tapirus pinchaque es un sobreviviente prehistórico del páramo; su tupida capa de pelo lanoso lo diferencia de las dantas de tierras bajas y le permite habitar hasta los 4.300 metros."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.tapir_ecological_role", "fauna.encounter_mountain_tapir", "fauna.mammals_overview"],
        "tags": ["danta_montana", "tapir_andino", "tapirus_pinchaque", "lanudo", "peligro"]
    },
    # 40. Tapir ecological role (Jardinera del páramo)
    {
        "id": "fauna.tapir_ecological_role",
        "label": "rol de la danta como jardinera del páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "por qué a la danta le dicen la jardinera del páramo",
            "rol ecológico de la danta de montaña",
            "dispersión de semillas por la danta",
            "importancia de la danta para el ecosistema",
            "¿qué pasa si desaparece la danta de páramo?",
            "danta y propagación de frailejones y palmas",
            "funcion de la danta en la alta montana",
            "como ayuda el tapir a regenerar el bosque",
            "ecological role of mountain tapir",
            "mountain tapir seed disperser paramo",
            "semillas que germinan en el estiercol de danta",
            "la gran jardinera de los andes"
        ],
        "hard_negatives": [
            "restauración ecológica y siembra comunitaria de árboles",
            "estudios botánicos de semillas de frailejón",
            "historia de las haciendas ganaderas en el páramo"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "A la danta de montaña se le conoce cariñosamente como la 'jardinera del páramo' porque recorre largas distancias consumiendo cientos de frutos y hojas, cuyas semillas pasan intactas por su tracto digestivo. Al defecar en cúmulos abonados por todo el parque, disemina y fertiliza especies clave como frailejones, lupinos y árboles altoandinos que de otro modo tendrían baja dispersión. Además, al abrir sendas entre la vegetación densa, facilita el paso de fauna menor.",
            "variants": [
                "La danta es una especie clave para la salud de Los Nevados; sus hábitos de ramoneo y dispersión de semillas garantizan la regeneración natural tanto del páramo como del bosque nublado."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_PNN_PORTAL],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_tapir", "fauna.threatened_species", "fauna.conservation_target_species_voc"],
        "tags": ["danta", "jardinera_paramo", "dispersion_semillas", "rol_ecologico", "semillas"]
    },
    # 41. Puma / Mountain Lion
    {
        "id": "fauna.cougar_puma",
        "label": "puma o león de montaña en el parque",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "el puma en Los Nevados",
            "Puma concolor",
            "león de montaña en el parque",
            "¿hay pumas en el páramo?",
            "felino grande en Los Nevados",
            "avistamientos de pumas en senderos",
            "¿el puma ataca a las personas en el parque?",
            "territorio del puma en la alta montaña",
            "Cougar Puma concolor Los Nevados National Park",
            "mountain lion in Colombian Andes",
            "rastros de puma en la nieve o barro",
            "puma cazador en los nevados"
        ],
        "hard_negatives": [
            "protocolo de rescate en caso de extravío en la niebla",
            "normativa de porte de cuchillos o armas en el parque",
            "registro fotográfico con cámaras trampa de científicos"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El puma (Puma concolor) es el mayor depredador carnívoro presente en Los Nevados, habitando desde los bosques nublados hasta los arenales del superpáramo por encima de los 4.000 metros. Posee un pelaje leonado uniforme que le permite mimetizarse a la perfección entre los pajonales secos mientras acecha venados, conejos y roedores. Es un animal sumamente sigiloso y esquivo que casi nunca se deja ver por los turistas y evita activamente a las personas.",
            "variants": [
                "Puma concolor es el felino cumbre de la alta montaña; mantiene el equilibrio de las poblaciones de herbívoros en el parque y patrulla grandes extensiones territoriales de forma solitaria y discreta."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.encounter_cougar_puma", "fauna.mammals_overview", "fauna.northern_tiger_cat"],
        "tags": ["puma", "puma_concolor", "leon_montana", "depredador", "felino"]
    },
    # 42. Northern Tiger Cat / Oncilla (Tigrillo lanudo)
    {
        "id": "fauna.northern_tiger_cat",
        "label": "tigrillo lanudo u oncilla en bosques altos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "tigrillo lanudo",
            "Leopardus tigrinus",
            "oncilla en Los Nevados",
            "gato salvaje manchado de alta montaña",
            "¿hay tigrillos en el páramo?",
            "felino manchado pequeño en bosque nublado",
            "diferencia entre tigrillo y puma",
            "gato montés en la cordillera central",
            "Northern tiger cat oncilla Los Nevados",
            "Leopardus tigrinus high altitude cat",
            "tigrillo con pelaje espeso para el frio",
            "pequeno leopardo de montaña en Colombia"
        ],
        "hard_negatives": [
            "prohibición de ingreso de gatos domésticos al parque",
            "talleres de pintura y artesanías locales en Manizales",
            "guía de huellas de animales en el lodo"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El tigrillo lanudo u oncilla (Leopardus tigrinus) es uno de los felinos silvestres más pequeños y hermosos de América, adaptado a los bosques altoandinos y bordes de páramo. Su cuerpo, del tamaño de un gato doméstico pero más esbelto, está cubierto por un pelaje denso y lanudo de fondo ocre con llamativas rosetas negras. De hábitos principalmente nocturnos y crepusculares, trepa con agilidad en busca de aves, ranas y roedores.",
            "variants": [
                "Leopardus tigrinus es un pequeño felino manchado protegido en Los Nevados; su pelaje espeso lo aísla del frío húmedo mientras caza sigilosamente entre las ramas y el sotobosque."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.cougar_puma", "fauna.mammals_overview", "fauna.threatened_species"],
        "tags": ["tigrillo_lanudo", "oncilla", "leopardus_tigrinus", "felino", "nocturno"]
    },
    # 43. Pacarana / Guagua loba
    {
        "id": "fauna.pacarana_guagua_loba",
        "label": "guagua loba o pacarana en Los Nevados",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "guagua loba",
            "pacarana",
            "Dinomys branickii",
            "¿qué es la guagua loba?",
            "roedor gigante en Los Nevados",
            "guagua con rayas y manchas blancas",
            "animal pacífico de bosque de niebla",
            "roedor raro y amenazado en el parque",
            "Pacarana Dinomys branickii Los Nevados",
            "giant rodent cloud forest Colombia",
            "guagua loba de noche en la selva",
            "roedor grande y lento de montaña"
        ],
        "hard_negatives": [
            "gastronomía típica y platos tradicionales de la región",
            "normativa sobre fogones y cocinetas de gas en campamentos",
            "clasificación de mamíferos en el Museo de Historia Natural"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La guagua loba o pacarana (Dinomys branickii) es un roedor gigante fascinante y muy raro que puede pesar hasta 15 kilos, habitando las laderas boscosas y quebradas del parque. Tiene cabeza ancha, cuerpo robusto con pelaje negro decorado con hileras de manchas blancas y una cola carnosa. Es un herbívoro nocturno, pausado y completamente inofensivo que come frutas caídas, hojas y brotes tiernos apoyándose en sus patas traseras.",
            "variants": [
                "Dinomys branickii es un roedor prehistórico y apacible de los bosques nublados de Los Nevados; sus poblaciones son muy escasas y se encuentra catalogada bajo amenaza a nivel nacional."
            ]
        },
        "sources": [SOURCE_PNN_PORTAL, SOURCE_PNN_PLAN, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_paca", "fauna.mammals_overview", "fauna.threatened_species"],
        "tags": ["guagua_loba", "pacarana", "dinomys_branickii", "roedor_gigante", "bosque_niebla"]
    },
    # 44. Mountain Paca (Guagua de páramo o boruga)
    {
        "id": "fauna.mountain_paca",
        "label": "guagua de páramo o boruga de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "guagua de páramo",
            "boruga de montaña",
            "Cuniculus taczanowskii",
            "lapa de alta montaña",
            "¿qué diferencia hay entre guagua y pacarana?",
            "roedor nocturno que vive cerca de quebradas",
            "guagua con pelaje grueso manchado",
            "boruga paramuna en Los Nevados",
            "Mountain paca Cuniculus taczanowskii",
            "high altitude paca Colombia",
            "roedor manchado cerca de riachuelos",
            "mamifero nocturno de madriguera en la montana"
        ],
        "hard_negatives": [
            "prohibición estricta de la cacería deportiva y de consumo",
            "puntos limpios para depósito de residuos orgánicos",
            "temperatura del agua en los baños del parque"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La guagua de montaña o boruga (Cuniculus taczanowskii) es un roedor mediano de hábitos nocturnos adaptado a los bosques altos y subpáramos húmedos hasta los 3.500 metros. A diferencia de la guagua de tierras bajas, posee un pelaje notablemente más largo, denso y oscuro para protegerse de las heladas, salpicado de hileras de puntos blancos. Excava madrigueras profundas cerca de arroyos y sale de noche a forrajear raíces, tubérculos y semillas.",
            "variants": [
                "Cuniculus taczanowskii habita en las riberas boscosas del parque; es un consumidor clave de semillas que contribuye a la salud vegetal del bosque altoandino."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.pacarana_guagua_loba", "fauna.mammals_overview", "fauna.paramo_rodents_shrews"],
        "tags": ["guagua_paramo", "boruga", "cuniculus_taczanowskii", "roedor", "nocturno"]
    },
    # 45. Little Red Brocket (Venado soche)
    {
        "id": "fauna.little_red_brocket",
        "label": "venado soche o venado rojo de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "venado soche",
            "venado rojo de montaña",
            "Mazama rufina",
            "ciervo colorado en Los Nevados",
            "¿cómo es el venado soche?",
            "venadito pequeño de color rojizo",
            "ciervo de páramo con cuernitos cortos",
            "venado rojo tímido en los matorrales",
            "Little red brocket Mazama rufina Los Nevados",
            "red dwarf brocket deer Colombia paramo",
            "venadito cafe rojizo en el sendero",
            "avistamiento de venados en bosque altoandino"
        ],
        "hard_negatives": [
            "diferencia entre senderos de trekking y senderos de herradura",
            "equipo básico para caminatas de más de seis horas",
            "sanciones por transitar fuera de la senda autorizada"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El venado soche (Mazama rufina) es un ciervo pequeño y esbelto de pelaje castaño rojizo intenso con la cara y las patas de tono negruzco, adaptado a la densa vegetación entre 2.500 y 3.800 metros. Los machos no tienen astas ramificadas sino dos pequeños pitones rectos y cortos. Es un animal sumamente tímido que ante el menor ruido huye con saltos elásticos para esconderse entre matorrales y cañas de chusque.",
            "variants": [
                "Mazama rufina es el venadito rojizo que habita los bosques nublados y ecotonos del páramo; se alimenta de hojas tiernas, brotes y hongos silvestres en horas tempranas de la mañana."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.northern_pudu", "fauna.white_tailed_deer", "fauna.mammals_overview"],
        "tags": ["venado_soche", "mazama_rufina", "ciervo_rojo", "mamiferos", "timido"]
    },
    # 46. Northern Pudu (Venado conejo)
    {
        "id": "fauna.northern_pudu",
        "label": "venado conejo en matorrales paramunos",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "venado conejo",
            "Pudella mephistophiles",
            "Pudu mephistophiles",
            "ciervo más pequeño del mundo en Los Nevados",
            "¿cuál es el venado más diminuto de Colombia?",
            "venadito enano del páramo",
            "ciervo del tamaño de un perro pequeño",
            "caracteristicas del pudu en los nevados",
            "Northern pudu Pudella mephistophiles Los Nevados",
            "smallest deer in the world Colombian paramo",
            "venado miniatura en los frailejones",
            "pudu del norte en alta montana"
        ],
        "hard_negatives": [
            "tarifa de entrada para niños y adultos mayores",
            "altura máxima permitida para ascenso de menores",
            "alquiler de caballos y mulas de carga"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El venado conejo (Pudella mephistophiles) ostenta el título de ser el ciervo más pequeño del mundo, midiendo apenas entre 30 y 35 centímetros de altura a la cruz y pesando unos 5 a 6 kilos. Su cuerpo rechoncho, patas cortas y pelaje pardo oscuro tupido le permiten deslizarse con increíble facilidad por túneles naturales debajo de pajonales densos y matorrales de páramo. Es una especie rara y vulnerable exclusiva de los altos Andes.",
            "variants": [
                "Pudella mephistophiles parece una mezcla entre un venadito enano y un conejo; vive oculto en la espesura del páramo alto y está estrictamente protegido en el parque."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.little_red_brocket", "fauna.white_tailed_deer", "fauna.threatened_species"],
        "tags": ["venado_conejo", "pudu", "pudella", "enano", "vulnerable"]
    },
    # 47. White-tailed Deer (Venado cola blanca)
    {
        "id": "fauna.white_tailed_deer",
        "label": "venado cola blanca de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "venado cola blanca",
            "Odocoileus virginianus",
            "Odocoileus goudotii",
            "ciervo grande en Los Nevados",
            "venado de páramo con cuernos grandes",
            "¿dónde se ven venados cola blanca en el parque?",
            "ciervo que levanta la cola blanca al correr",
            "venados pastando en valles abiertos",
            "White-tailed deer paramo Colombia",
            "Odocoileus virginianus Los Nevados",
            "venado grande en pajonales abiertos",
            "manadas de venados en alta montaña"
        ],
        "hard_negatives": [
            "horario de apertura y cierre de las puertas del parque",
            "campamentos autorizados en el valle del río Combeima",
            "servicio de guianza turística obligatoria"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La subespecie andina del venado cola blanca (Odocoileus virginianus goudotii) es el cérvido más grande del parque, reconocible por su porte majestuoso, pelaje grisáceo parduzco espeso y cornamentas ramificadas en los machos adultos. Suele observarse en valles abiertos y amplias planicies de páramo forrajeando en pequeños grupos familiares durante las primeras horas del día. Al huir, alza su cola mostrando la parte inferior blanca brillante como señal de alarma.",
            "variants": [
                "Este hermoso venado pasta en las extensas llanuras de pajonal del parque; su pelaje denso y grisáceo lo aísla del frío y el viento constante de la alta montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_PNN_PORTAL, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.little_red_brocket", "fauna.northern_pudu", "fauna.mammals_overview"],
        "tags": ["venado_cola_blanca", "odocoileus", "ciervo", "paramo_abierto", "cornamenta"]
    },
    # 48. Mountain Coati / Cusumbo andino
    {
        "id": "fauna.mountain_coati",
        "label": "cusumbo andino o coatí de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "cusumbo andino",
            "coatí de montaña",
            "Nasuella olivacea",
            "animal con trompa móvil y cola anillada",
            "¿qué es un cusumbo?",
            "mamífero diurno escarbando la tierra",
            "cusumbo de páramo en Los Nevados",
            "coati de cola larga en el sendero",
            "Mountain coati Nasuella olivacea Los Nevados",
            "Andean coati foraging in the paramo",
            "cusumbito buscando comida entre musgos",
            "animalito simpatico con cola parada"
        ],
        "hard_negatives": [
            "prohibición de arrojar cáscaras de fruta en el camino",
            "senderos interpretativos para niños en el centro de visitantes",
            "alquiler de carpas térmicas en las ciudades de salida"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El cusumbo andino (Nasuella olivacea) es un pequeño prociónido pariente del mapache, caracterizado por su hocico alargado y flexible y su cola peluda que suele llevar erguida en alto al caminar. A diferencia de muchos mamíferos nocturnos, el cusumbo es muy activo durante el día, caminando entre la hojarasca y los frailejones mientras usa su sensible trompa para desenterrar escarabajos, lombrices y raíces. Es curioso pero prudente frente a los excursionistas.",
            "variants": [
                "Nasuella olivacea es un mamífero diurno muy simpático que verás husmeando el suelo con su trompa móvil en los bordes de bosque y páramo; nunca intentes tocarlo ni darle comida."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.long_tailed_weasel", "fauna.paramo_rabbit", "fauna.mammals_overview"],
        "tags": ["cusumbo", "coati_montana", "nasuella_olivacea", "diurno", "omnivoro"]
    },
    # 49. Long-tailed Weasel (Comadreja andina)
    {
        "id": "fauna.long_tailed_weasel",
        "label": "comadreja andina de cola larga",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "comadreja andina",
            "Neogale frenata",
            "Mustela frenata",
            "comadreja de cola larga en Los Nevados",
            "animal largo y delgado corriendo entre piedras",
            "pequeño carnívoro ágil del páramo",
            "chucha ratonera o comadreja en el nevado",
            "cazadora veloz de ratones en pajonales",
            "Long-tailed weasel Neogale frenata high Andes",
            "Andean weasel Los Nevados National Park",
            "comadreja con punta de cola negra",
            "mamifero alargado cruzando el camino"
        ],
        "hard_negatives": [
            "botas con soporte de tobillo para caminar en pedregales",
            "seguro de asistencia médica por accidentes personales",
            "refugio El Cisne y servicios básicos disponibles"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "La comadreja andina (Neogale frenata) es un carnívoro hiperactivo de cuerpo alargado, patas cortas y cuello estilizado, perfectamente adaptado para entrar en madrigueras subterráneas. Su pelaje es castaño en el dorso, amarillento en el vientre y termina en una distintiva cola con punta negra. Con reflejos fulminantes, recorre las grietas de roca y pajonales cazando ratones y conejos, cumpliendo un papel biológico esencial como controladora de roedores.",
            "variants": [
                "Neogale frenata es una cazadora incansable del páramo; se desplaza a saltos veloces inspeccionando túneles entre los pajonales en busca de presas para alimentar su rápido metabolismo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_rabbit", "fauna.paramo_rodents_shrews", "fauna.mammals_overview"],
        "tags": ["comadreja", "neogale_frenata", "mustela", "carnivoro", "controlador"]
    },
    # 50. Paramo Rabbit (Conejo de páramo)
    {
        "id": "fauna.paramo_rabbit",
        "label": "conejo de páramo o tapetí andino",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "conejo de páramo",
            "tapetí andino",
            "Sylvilagus andinus",
            "Sylvilagus brasiliensis",
            "conejos silvestres en Los Nevados",
            "¿hay conejos en la alta montaña?",
            "conejo pequeño escondido en el pajonal",
            "animales herbívoros comunes en el parque",
            "Paramo rabbit Sylvilagus andinus Colombia",
            "wild rabbit high elevation grasslands",
            "conejito pardo corriendo entre frailejones",
            "conejo silvestre cruzando la trocha"
        ],
        "hard_negatives": [
            "impacto de fogatas en los pastizales de alta montaña",
            "recolección de plantas medicinales y frailejones",
            "tiendas de souvenirs en la entrada del parque"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El conejo de páramo (Sylvilagus andinus) es el herbívoro menor más abundante del parque, adaptado a vivir en los pajonales y morrenas hasta los 4.400 metros. Tiene orejas más cortas y redondeadas que los conejos domésticos, y un pelaje denso de tonos pardos y grisáceos que le permite mimetizarse entre las pajas secas de Calamagrostis. Es una presa fundamental en la dieta de rapaces diurnas, búhos y carnívoros como el puma y la comadreja.",
            "variants": [
                "Sylvilagus andinus se alimenta de pastos duros de páramo; si caminas en silencio al amanecer, verás cómo se congela inmóvil entre la hierba confiando en su camuflaje."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.black_chested_buzzard_eagle", "fauna.cougar_puma", "fauna.mammals_overview"],
        "tags": ["conejo_paramo", "sylvilagus", "tapeti", "herbiivoro", "pajonal"]
    },
    # 51. Rufous Porcupine (Puercoespín andino)
    {
        "id": "fauna.rufous_porcupine",
        "label": "puercoespín andino de cola corta",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "puercoespín andino",
            "Coendou rufescens",
            "erizo de montaña en Los Nevados",
            "¿hay puercoespines en el parque?",
            "animal con espinas rojizas en bosque altoandino",
            "puercoespin de cola corta en árboles",
            "roedor con púas en la cordillera central",
            "caracteristicas del puercoespin andino",
            "Rufous porcupine Coendou rufescens Los Nevados",
            "Andean porcupine cloud forest",
            "animal nocturno espinoso en los arboles",
            "puercoespin que no lanza las puas"
        ],
        "hard_negatives": [
            "precauciones médicas ante espinas de plantas como la Puya",
            "prohibición de acampar fuera de zonas designadas",
            "flora leñosa y arbustos espinosos del subpáramo"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El puercoespín andino (Coendou rufescens) es un roedor arborícola de hábitos nocturnos cubierto por una densa armadura de púas afiladas de color pardo rojizo con puntas negras. Pasa el día durmiendo enrollado en horquetas de árboles o grietas rocosas, y de noche trepa lentamente para alimentarse de cortezas tiernas, brotes y hojas. Es un mito que 'dispare' sus púas: solo se desprenden por contacto directo si un depredador intenta morderlo.",
            "variants": [
                "Coendou rufescens habita en los bosques de niebla y matorrales altos; su defensa pasiva con espinas afiladas lo mantiene a salvo de casi todos los depredadores de la montaña."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_coati", "fauna.mammals_overview", "fauna.highland_bats"],
        "tags": ["puercoespin", "coendou_rufescens", "espinas", "arboricola", "nocturno"]
    },
    # 52. Crab-eating Fox (Zorro perruno)
    {
        "id": "fauna.crab_eating_fox",
        "label": "zorro perruno o zorro cangrejero",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "zorro perruno",
            "zorro cangrejero",
            "Cerdocyon thous",
            "zorros en Los Nevados",
            "¿hay zorros en la carretera a Brisas?",
            "cánido silvestre en el páramo",
            "zorro gris patrullando las vías",
            "animal parecido a un perro salvaje en el parque",
            "Crab-eating fox Cerdocyon thous Los Nevados",
            "wild fox Colombian Andes paramo",
            "zorro comiendo cerca del camino vehicular",
            "zorro andino en la zona amortiguadora"
        ],
        "hard_negatives": [
            "presencia de perros domésticos y asilvestrados",
            "límite de velocidad vehicular en la vía Manizales-Murillo",
            "vacunación contra la rabia en animales domésticos"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El zorro perruno (Cerdocyon thous) es un cánido silvestre oportunista y muy adaptable que incursiona con frecuencia a lo largo de bordes de bosque, potreros y márgenes de carretera en el parque. De tamaño mediano y pelaje grisáceo jaspeado con negro, patrulla al crepúsculo y durante la noche buscando pequeños roedores, insectos, ranas y frutos silvestres. Por su propia seguridad y la tuya, jamás le ofrezcas alimento si lo ves al borde de la vía.",
            "variants": [
                "Cerdocyon thous es el zorro silvestre de la región; recorre caminos en horas de poca luz buscando alimento. Es vital conducir despacio por las vías del parque para evitar atropellarlo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_CORPOCALDAS, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.roadkill_risk_murillo_road", "fauna.feeding_wildlife_prohibition", "fauna.mammals_overview"],
        "tags": ["zorro_perruno", "cerdocyon_thous", "canido", "nocturno", "via_murillo"]
    },
    # 53. Highland Bats (Murciélagos de alta montaña)
    {
        "id": "fauna.highland_bats",
        "label": "murciélagos de alta montaña y polinizadores",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "murciélagos en Los Nevados",
            "Anoura geoffroyi",
            "Histiotus montanus",
            "Sturnira",
            "¿hay murciélagos con tanto frío en el páramo?",
            "murciélagos polinizadores de altura",
            "quirópteros en el parque nacional los nevados",
            "murciélago orejudo de montaña",
            "Highland bats Los Nevados Colombia",
            "pollinating bats high Andes mountains",
            "murcielagos comiendo nectar en la noche",
            "quirópteros adaptados al clima frío"
        ],
        "hard_negatives": [
            "cuevas volcánicas cerradas al turismo por seguridad",
            "enfermedades respiratorias provocadas por ceniza volcánica",
            "linternas y uso de flash en fotografía nocturna"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "Aunque parezca insólito por las heladas, en Los Nevados se registran especies de murciélagos muy especializadas, como el murciélago lengüetón (Anoura geoffroyi) y el murciélago orejudo (Histiotus montanus). Poseen un pelaje excepcionalmente largo y afelpado que atrapa aire caliente para aislar su cuerpo mientras vuelan en la noche. Especies nectarívoras como Anoura son polinizadores cruciales de bromelias, orquídeas y flores nocturnas del bosque de niebla.",
            "variants": [
                "Los murciélagos altoandinos de Los Nevados polinizan plantas de montaña y controlan poblaciones de insectos nocturnos, refugiándose durante el día en cuevas de lava y grietas rocosas."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.mammals_overview", "fauna.insects_invertebrates_overview", "fauna.highland_bats"],
        "tags": ["murcielagos", "quiropteros", "anoura", "histiotus", "polinizadores"]
    },
    # 54. Paramo Rodents & Shrews
    {
        "id": "fauna.paramo_rodents_shrews",
        "label": "ratones y musarañas de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "ratones de páramo",
            "Akodon bogotensis",
            "Thomasomys",
            "musaraña de montaña",
            "Cryptotis colombiana",
            "pequeños roedores en la alta montaña",
            "ratoncito con pelaje espeso en pajonales",
            "mamíferos pequeños del suelo del páramo",
            "Paramo mice and shrews Los Nevados",
            "small mammals high Andes Colombia",
            "ratones que viven bajo los frailejones",
            "musaranas insectivoras de montana"
        ],
        "hard_negatives": [
            "almacenamiento de comida en tiendas para evitar roedores",
            "higiene y control de plagas en zonas de refugio",
            "normas de disposición de sobras de comida"
        ],
        "entities": {"animal_group": ["mamiferos"]},
        "needs": [],
        "answer": {
            "short": "El suelo del páramo bulle de vida con pequeños mamíferos como el ratón de páramo (Akodon bogotensis), las ratas de monte arborícolas (Thomasomys) y diminutas musarañas endémicas como Cryptotis colombiana. Poseen un pelaje denso y espeso y metabolizan grasas rápidamente para mantener su temperatura corporal en túneles excavados bajo las macollas de pasto. Constituyen el pilar alimentario esencial para búhos, águilas, comadrejas y pumas.",
            "variants": [
                "Estos pequeños roedores y musarañas sostienen la cadena trófica de Los Nevados; viven resguardados entre las raíces de frailejones y musgos alimentándose de semillas e invertebrados."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.long_tailed_weasel", "fauna.short_eared_owl_paramo", "fauna.mammals_overview"],
        "tags": ["ratones", "musaranas", "akodon", "thomasomys", "cryptotis"]
    },
    # 55. Paramo Toad (Osornophryne percrassa)
    {
        "id": "fauna.paramo_toad_osornophryne",
        "label": "sapito rechoncho de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "sapito rechoncho de páramo",
            "Osornophryne percrassa",
            "sapo pequeño verrugoso en Los Nevados",
            "anfibio endémico de la cordillera central",
            "¿cómo sobrevive un sapo al frío del nevado?",
            "sapito que camina despacio en el musgo",
            "sapito de páramo amenazado",
            "sapo rechoncho de alta montana",
            "Osornophryne percrassa paramo toad",
            "endemic high altitude toad Colombia",
            "sapito gordo entre almohadillas de vegetacion",
            "anfibio vulnerable del parque nacional"
        ],
        "hard_negatives": [
            "colchones de agua y turberas como ecosistema frágil",
            "prohibición de pisar o arrancar plantas de páramo",
            "impacto de fogatas en el suelo orgánico"
        ],
        "entities": {"animal_group": ["anfibios"]},
        "needs": [],
        "answer": {
            "short": "El sapito rechoncho (Osornophryne percrassa) es un anfibio fascinante y endémico de la Cordillera Central de Colombia, catalogado como especie Vulnerable. De cuerpo pequeño, rechoncho y cubierto de verrugas glandulares de tono pardo oscuro, no salta sino que camina con lentitud entre almohadillas de musgo y frailejones entre 2.700 y 3.800 metros. Se refugia bajo rocas para protegerse de las heladas y es extremadamente sensible al pisoteo.",
            "variants": [
                "Osornophryne percrassa es un sapito adaptado a sobrevivir al borde del congelamiento; sus movimientos lentos y su coloración críptica le permiten pasar inadvertido en el suelo húmedo."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_rain_frogs", "fauna.amphibians_overview", "fauna.threatened_species"],
        "tags": ["sapito_rechoncho", "osornophryne", "anfibios", "endemico", "vulnerable"]
    },
    # 56. Paramo Rain Frogs (Pristimantis)
    {
        "id": "fauna.paramo_rain_frogs",
        "label": "ranas de lluvia del páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "ranas de lluvia del páramo",
            "Pristimantis simoterus",
            "Pristimantis simoteriscus",
            "ranitas que nacen sin renacuajo",
            "desarrollo directo en anfibios de montaña",
            "¿dónde ponen huevos las ranas del páramo?",
            "ranitas camufladas entre hojas de frailejón",
            "ranas diminutas cantando en el musgo",
            "Paramo rain frogs Pristimantis Los Nevados",
            "direct developing frogs high Andes",
            "ranitas transparentes o pardas en la alta montana",
            "anfibios que soportan el hielo"
        ],
        "hard_negatives": [
            "impermeabilización de carpas contra lluvias torrenciales",
            "temperatura del agua en las quebradas de deshielo",
            "fotografía de aproximación y normas sobre no manipular fauna"
        ],
        "entities": {"animal_group": ["anfibios"]},
        "needs": [],
        "answer": {
            "short": "Las ranas de lluvia del género Pristimantis (como Pristimantis simoterus y P. simoteriscus) dominan la comunidad de anfibios de Los Nevados. Poseen una adaptación evolutiva magistral llamada 'desarrollo directo': no dependen de lagunas abiertas ni pasan por fase de renacuajo, sino que las crías nacen ya formadas como ranitas diminutas directamente desde los huevos puestos en musgos húmedos. Esto les permite colonizar el páramo sin que el hielo destruya sus larvas.",
            "variants": [
                "Pristimantis es el grupo de ranas más exitoso en Los Nevados gracias a que sus huevos eclosionan directamente como ranas completas dentro de la hojarasca y musgos del frailejonal."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.paramo_toad_osornophryne", "fauna.amphibians_overview", "fauna.harlequin_frog_atelopus"],
        "tags": ["pristimantis", "ranas_lluvia", "desarrollo_directo", "anfibios", "paramo"]
    },
    # 57. Harlequin Frogs (Atelopus) & chytrid fungus
    {
        "id": "fauna.harlequin_frog_atelopus",
        "label": "ranas arlequín de montaña y quitridiomicosis",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "ranas arlequín",
            "Atelopus simulatus",
            "Atelopus lozanoi",
            "hongo quítrido en anfibios de Los Nevados",
            "¿por qué desaparecieron las ranas arlequín?",
            "ranas de colores en peligro crítico",
            "quitridiomicosis y declive de anfibios andinos",
            "crisis de extinción de ranas de alta montaña",
            "Harlequin frog Atelopus chytrid fungus Colombia",
            "endangered harlequin frogs Los Nevados",
            "ranitas arlequin de quebradas de montana",
            "desinfección de botas para proteger anfibios"
        ],
        "hard_negatives": [
            "desinfección de agua para consumo humano en caminatas",
            "enfermedades gastrointestinales por beber agua cruda",
            "reglamento de acceso a zonas intangibles del parque"
        ],
        "entities": {"animal_group": ["anfibios"]},
        "needs": [],
        "answer": {
            "short": "Las ranas arlequín de alta montaña (género Atelopus, como Atelopus simulatus) sufrieron un colapso poblacional devastador desde finales del siglo XX debido a la quitridiomicosis, una enfermedad infecciosa provocada por el hongo microscópico Batrachochytrium dendrobatidis, agravada por el calentamiento global. Hoy se consideran en Peligro Crítico. Para proteger a las pocas sobrevivientes, es vital no pisar las orillas de riachuelos y limpiar bien el barro de las botas antes de entrar al parque.",
            "variants": [
                "El género Atelopus representa la mayor emergencia de conservación entre los anfibios andinos por el ataque del hongo quítrido; cualquier avistamiento debe reportarse inmediatamente a los guardaparques."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.amphibians_overview", "fauna.paramo_rain_frogs", "fauna.threatened_species"],
        "tags": ["atelopus", "rana_arlequin", "quitridiomicosis", "peligro_critico", "hongo"]
    },
    # 58. Mountain Collared Lizard (Stenocercus)
    {
        "id": "fauna.mountain_collared_lizard",
        "label": "lagartija collareja de páramo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "lagartija collareja",
            "Stenocercus trachycephalus",
            "lagarto de páramo tomando el sol",
            "lagartija con collar en Los Nevados",
            "¿cómo calientan su cuerpo los reptiles en el frío?",
            "heliotermia en lagartos de alta montaña",
            "lagartijita sobre rocas en el sendero",
            "lagartijas comunes en el sector Brisas",
            "Mountain collared lizard Stenocercus Los Nevados",
            "high altitude basking lizard Colombia",
            "lagarto escamoso sobre piedras calientes",
            "reptil diurno en el nevado del ruiz"
        ],
        "hard_negatives": [
            "bloqueador solar y recomendaciones de radiación en altura",
            "superficie y geología de las morrenas volcánicas",
            "horarios de mayor insolación en el parque"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "La lagartija collareja (Stenocercus trachycephalus) es el reptil más visible del parque, adaptado a vivir en ambientes rocosos y matorrales hasta los 3.800 metros. Al ser ectoterma, depende de la 'heliotermia': en las mañanas soleadas se aposta sobre rocas oscuras orientadas hacia el sol para absorber calor rápidamente y alcanzar la temperatura necesaria para forrajear insectos. Posee un característico collar oscuro en el cuello y escamas aquilladas ásperas.",
            "variants": [
                "Stenocercus trachycephalus aprovecha la intensa radiación solar de la montaña; cuando el cielo se nubla o baja la temperatura, se esconde velozmente bajo piedras profundas para evitar congelarse."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_SIB_COLOMBIA, SOURCE_HUMBOLDT],
        "last_verified": "2026-11-21",
        "related": ["fauna.shade_lizards_andinosaura", "fauna.reptiles_overview", "fauna.andean_chameleon_anole"],
        "tags": ["stenocercus", "lagartija_collareja", "heliotermia", "reptiles", "rocas"]
    },
    # 59. Shade Lizards (Andinosaura / Riama)
    {
        "id": "fauna.shade_lizards_andinosaura",
        "label": "lagartijas de hojarasca y musgo",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "lagartijas de hojarasca",
            "Andinosaura laevis",
            "Riama striata",
            "lagartos de sombra en el páramo",
            "micro lagartijas bajo el musgo",
            "reptiles semifosoriales de Los Nevados",
            "lagartija pequeña con escamas brillantes",
            "lagartos que viven enterrados en la vegetación húmeda",
            "Shade lizards Andinosaura paramo Colombia",
            "cryptozoic lizards high Andes",
            "lagartijitas diminutas debajo de piedras",
            "gimnoftálmidos de alta montaña"
        ],
        "hard_negatives": [
            "musgos y turberas como retenedores de agua dulce",
            "botas con suela antideslizante para barro",
            "fotografía de macro en ambientes húmedos"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "Las pequeñas lagartijas de los géneros Andinosaura y Riama (familia Gymnophthalmidae) están especializadas en la vida críptica bajo la densa hojarasca, almohadillas de musgo y turberas húmedas del bosque altoandino y subpáramo. Con cuerpos cilíndricos, patas reducidas y escamas lisas y brillantes, se desplazan sinuosamente como si nadaran entre la materia orgánica fría en descomposición, cazando diminutos invertebrados del suelo.",
            "variants": [
                "Estas lagartijas de hábitos semifosoriales casi nunca salen a tomar el sol directamente; su fisiología está adaptada para mantenerse activas a bajas temperaturas bajo el colchón vegetal."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_collared_lizard", "fauna.reptiles_overview", "fauna.earth_snakes_atractus"],
        "tags": ["andinosaura", "riama", "lagartijas_hojarasca", "gimnoftalmidos", "cripticas"]
    },
    # 60. Andean Chameleon Anole
    {
        "id": "fauna.andean_chameleon_anole",
        "label": "camaleoncito andino o anolis de montaña",
        "kind": "explanation",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "camaleoncito andino",
            "Anolis heterodermus",
            "Phenacosaurus heterodermus",
            "falso camaleón de montaña en Los Nevados",
            "lagarto con cola prensil en ramas altas",
            "lagartija de movimientos lentos en el bosque",
            "anolis adaptado al frío de alta montaña",
            "¿hay camaleones nativos en Colombia?",
            "Andean chameleon anole Anolis heterodermus",
            "high altitude slow lizard Colombia",
            "lagarto camaleonico que cambia de tono",
            "anolis de ramas y musgo en bosque nublado"
        ],
        "hard_negatives": [
            "camaleones del Viejo Mundo importados como mascotas",
            "árboles y epífitas del bosque de niebla",
            "técnicas de senderismo con bastones en descensos"
        ],
        "entities": {"animal_group": ["reptiles"]},
        "needs": [],
        "answer": {
            "short": "El camaleoncito andino (Anolis heterodermus, antes clasificado en Phenacosaurus) es un lagarto arborícola fascinante que habita en los bosques de niebla y matorrales de subpáramo. Posee una cola prensil que utiliza como una quinta extremidad para asegurarse a ramas cubiertas de líquenes, ojos de movimiento independiente y un andar pausado y balanceado que imita una hoja mecida por el viento. Puede cambiar sutilmente entre tonalidades verdes, pardas y grises.",
            "variants": [
                "Anolis heterodermus es el falso camaleón de los Andes; sus movimientos lentos y su camuflaje perfecto entre ramas musgosas le permiten cazar insectos sin ser detectado."
            ]
        },
        "sources": [SOURCE_PNN_PLAN, SOURCE_HUMBOLDT, SOURCE_SIB_COLOMBIA],
        "last_verified": "2026-11-21",
        "related": ["fauna.mountain_collared_lizard", "fauna.reptiles_overview", "fauna.shade_lizards_andinosaura"],
        "tags": ["camaleoncito_andino", "anolis_heterodermus", "phenacosaurus", "arboricola", "camuflaje"]
    }
]
