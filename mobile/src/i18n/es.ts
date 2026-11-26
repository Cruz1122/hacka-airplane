// Spanish UI copy: the source of truth for the label keys. Every other locale must match this
// shape (see `Labels` in ./index). `{name}` placeholders are filled with `fill()`.
export const es = {
  appTitle: 'Nevados',
  parkName: 'Parque Nacional Natural Los Nevados',
  settings: 'Configuración',
  history: 'Historial',
  inputPlaceholder: 'Escribe tu pregunta',
  send: 'Enviar',
  reset: 'Reiniciar',
  debug: 'Depuración',
  state: 'Estado',
  noSteps: 'Sin pasos todavía',
  modelMissing: 'Modelo no encontrado en el dispositivo',
  modelLoading: 'Cargando modelo...',
  modelReady: 'Listo',
  model: 'Modelo',
  station: 'Estación del dispositivo',
  stationNone: 'Ninguna',
  answerMode: 'Modo de respuesta',
  extractive: 'Extractivo',
  generate: 'Generativo',
  chat: 'Conversación libre',
  chatOn: 'Activada',
  chatOff: 'Estricta (se abstiene)',
  backend: 'Backend',
  backendDevice: 'En el dispositivo',
  backendHttp: 'HTTP (desarrollo)',
  httpUrl: 'URL del servidor',
  historyEmpty: 'Sin registros',
  // History rows are keyed by the tool that wrote them.
  register_visit: 'Registro de visita',
  report_emergency: 'Reporte de emergencia',
  ms: 'ms',
  tokens: 'tok',
  pageDot: 'Paso {n} de {total}',
  onboarding: {
    // The park comes first; the Pet is the guide. Screen 2 is provisional: offline use is the
    // product's design goal but not yet verified on the device.
    screens: [
      {
        title: 'Descubre Los Nevados',
        subtitle: 'Nevados, páramo y lagunas te esperan, y {pet} te acompaña.',
      },
      {
        title: 'Explora sin señal',
        subtitle: 'Senderos, clima, normas y seguridad del parque, aun en modo avión.',
      },
      {
        title: 'Pregúntale a {pet}',
        subtitle: 'Fauna, flora, refugios o tu ruta: {pet} conoce el parque.',
      },
    ],
    next: 'Siguiente',
    start: 'Empezar a explorar',
  },
  trail: {
    title: 'Recorrido Brisas',
    subtitle: 'Ruta vehicular hasta el Valle de las Tumbas',
    stationA11y: 'Estación {n}: {name}. {mark}',
    marks: {
      brisas: 'Puerta de entrada',
      aguacerales: 'Génesis hídrica',
      arenales: 'Memoria y cambio climático',
      valleLunar: 'Fuerzas geológicas',
      valleTumbas: 'Respeto y riesgo',
    },
    stations: {
      brisas: {
        name: 'Brisas: la puerta de entrada',
        blurb:
          'Entrada al sector norte del parque, por el flanco norte del Complejo Volcánico Nevado del Ruiz.',
      },
      aguacerales: {
        name: 'Aguacerales: el filtro de la montaña',
        blurb: 'A unos 4.160 m s. n. m.: páramo propiamente dicho, donde la niebla se vuelve agua.',
      },
      arenales: {
        name: 'Arenales: geología y memoria',
        blurb:
          'A unos 4.290 m s. n. m.: del páramo al superpáramo, entre dunas de arena volcánica.',
      },
      valleLunar: {
        name: 'Valle Lunar: la fuerza de los elementos',
        blurb: 'A unos 4.350 m s. n. m.: superpáramo de rocas partidas por el hielo.',
      },
      valleTumbas: {
        name: 'Valle de las Tumbas: espiritualidad y riesgo',
        blurb:
          'A unos 4.460 m s. n. m.: final del recorrido, entre el superpáramo y la zona nival.',
      },
    },
    back: 'Volver',
    photo: 'Imagen {n} de la etapa',
    source: 'Fuente: Guion ecoturístico UTON, 2024',
    tumak: {
      open: 'Abrir el chat de {pet}',
      title: '{pet}',
      close: 'Cerrar el chat de {pet}',
      context: 'Estamos en el contexto de la etapa {place}.',
    },
    sheet: {
      more: '¡Saber más!',
      close: 'Cerrar',
      blurbs: {
        brisas:
          'Aquí entras al Parque Nacional Natural Los Nevados, por el flanco norte del Complejo Volcánico Nevado del Ruiz. Un páramo vital para regular el agua del Eje Cafetero.',
        aguacerales:
          'A unos 4.160 m, en pleno páramo, la niebla se queda atrapada en las plantas y se vuelve agua. Aquí empieza el ciclo que alimenta los ríos de abajo.',
        arenales:
          'A unos 4.290 m el paisaje pasa de verde a gris: dunas de arena volcánica y el recuerdo de las pistas de esquí que borró el deshielo.',
        valleLunar:
          'A unos 4.350 m, en el superpáramo, casi no hay plantas. El hielo parte las rocas y el óxido las tiñe de tonos rojizos.',
        valleTumbas:
          'A unos 4.460 m termina el recorrido. Un lugar sagrado para los pueblos indígenas y el límite de ascenso frente al volcán.',
      },
      concepts: {
        brisas:
          'El 86 % del parque es páramo: unas 53.532 hectáreas protegidas que regulan el agua de la región.',
        aguacerales:
          'Sin la niebla que se condensa aquí, gota a gota, no habría agua potable en las ciudades de abajo.',
        arenales:
          'Donde antes hubo nieve permanente para esquiar, hoy queda un desierto de altura.',
        valleLunar:
          'El agua se congela en las grietas, aumenta su volumen y parte la roca desde adentro: es la gelifracción.',
        valleTumbas:
          'No se sube más allá de este punto, sobre todo por el riesgo de lahares: flujos de lodo y escombros volcánicos.',
      },
    },
    camera: {
      prompt: 'Toma una foto de esta estación.',
      take: 'Tomar foto',
      denied: 'Sin permiso de cámara. Actívalo en ajustes para fotografiar esta estación.',
      unavailable: 'La cámara no está disponible aquí.',
      capturedA11y: 'Foto tomada en esta estación',
      memory: 'Tu recuerdo',
      options: 'Opciones de la foto',
      retake: 'Volver a tomar foto',
      remove: 'Borrar',
      cancel: 'Cancelar',
    },
    pages: {
      brisas: [
        {
          subtitle: 'Puerta de entrada',
          body: 'Estás entrando al **Parque Nacional Natural Los Nevados**, un área protegida de cerca de **62.000 hectáreas**. Llegas por el flanco norte del **Complejo Volcánico Nevado del Ruiz**, formado por cuatro estructuras: **Nereidas**, **Olleta**, **Piraña** y **Arenas**, el cráter activo.\n\nLa roca que más vas a ver en el camino es la **andesita**, una roca volcánica muy común en los Andes. El Nevado del Ruiz es todo ese complejo, aunque en el día a día se le dice así sobre todo al edificio que guarda el cráter Arenas.',
        },
        {
          subtitle: 'Kumanday',
          body: 'Mucho antes de llamarse Ruiz, esta montaña se llamaba **Kumanday**. Así la nombraban las comunidades indígenas que vivían aquí, y la tradición le da significados como **“Cerro Blanco”** o **“Padre Blanco”**. Para ellas, el volcán era un ser vivo, un centinela sagrado entre la tierra y el cielo.\n\nEse blanco es un **glaciar de cumbre**: nieve que durante cientos de años se acumula, se compacta, pierde el aire y se vuelve hielo. En las épocas secas suelta agua poco a poco y mantiene el caudal de los ríos, como una cuenta de ahorros de agua sólida. Hoy ese glaciar **retrocede** rápido por el calentamiento global.',
        },
        {
          subtitle: 'Agua para el Eje Cafetero',
          body: 'Este páramo es un **regulador hídrico**: el agua del parque abastece a **37 municipios** y beneficia a cerca de **3 millones de personas** en Caldas, Risaralda, Quindío, Tolima y el norte del Valle del Cauca.\n\nEl suelo, de origen volcánico, funciona como una esponja que puede retener hasta **40 veces su peso en agua**. El clima es **bimodal**: dos temporadas de lluvia y dos secas marcan el ritmo de la montaña. A medida que subas vas a notar más radiación solar y vientos más fríos.',
        },
      ],
      aguacerales: [
        {
          subtitle: 'Donde el agua se atrapa',
          body: 'Te damos la bienvenida a **Aguacerales**, a unos **4.160 m s. n. m.**, en el páramo propiamente dicho. Aquí no solo llueve: el agua de la niebla **se atrapa**. Las plantas interceptan las nubes y el agua se **condensa** en gotas que bajan hasta los musgos que crecen sobre la roca.\n\nEsas gotas se juntan en hilos de agua que forman un riachuelo rumbo a la quebrada. Pasa las **24 horas del día, todos los días del año**, y esa caída de agua que no para le da su nombre al lugar. En las noches frías, sobre todo en temporada seca, los hilos se congelan y forman **carámbanos**.',
        },
        {
          subtitle: 'El frailejón, ingeniero del agua',
          body: 'Mira los frailejones: en el parque solo está reportada una especie, **Espeletia hartwegiana**. Sus hojas están cubiertas de pelitos blancos, la **pubescencia**, que lo protegen de la fuerte radiación UV y guardan calor. Las hojas muertas que cubren el tallo, la **necromasa**, son una chaqueta que evita que el agua de su interior se congele.\n\nExisten más de 100 especies de frailejones y cerca de 60 crecen en Colombia. El nombre **Espeletia** honra a José Manuel de Ezpeleta, virrey del Nuevo Reino de Granada.',
        },
        {
          subtitle: 'Una esponja de ceniza',
          body: 'El suelo que pisas está hecho de **ceniza volcánica** y materia orgánica. Funciona como una esponja que suelta el agua despacio hacia las cuencas de los ríos **Chinchiná** y **Gualí**.\n\nTodo este ecosistema creció sobre lo que dejó el **glaciar** al retirarse. Al retroceder, el hielo cortó las lavas como un cuchillo gigante, formó los escarpes que rodean la estación y dejó un **valle en U** al occidente. Las rocas que ves alrededor son **andesitas** de cerca de **100.000 años**.',
        },
      ],
      arenales: [
        {
          subtitle: 'Dunas de arena volcánica',
          body: 'En **Arenales**, a unos **4.290 m s. n. m.**, el páramo da paso al **superpáramo** y el paisaje cambia de verde a gris. Las **dunas** que ves las forma el viento: arrastra ceniza del volcán, partículas que arranca de las rocas y el material de la roca que se desgasta, hasta que todo choca con la barrera de rocas detrás de la cabaña.\n\nSe estima que estas dunas tienen entre **200 y 400 años**, porque se formaron después de que el glaciar se retiró, aunque faltan estudios para confirmarlo. Son **patrimonio geológico intangible**: una huella puede durar meses, así que no las pises.',
        },
        {
          subtitle: 'Del esquí al deshielo',
          body: 'Arenales siempre ha recibido visitantes: desde una bodega de papa en **1937** hasta el **Chalet Arenales**, diseñado por el arquitecto **Simón Vélez**, que se incendió en **2010**. La cabaña actual cuenta la historia del **esquí** en el Ruiz: en los años **50 y 60** hubo campeonatos sudamericanos y de ahí nació el Club de Ski de Manizales.\n\nEl esquí se acabó por el **deshielo**. Donde antes había nieve permanente, hoy queda un desierto de altura: el retroceso del glaciar es uno de los testimonios más claros del **cambio climático** en Colombia.',
        },
        {
          subtitle: 'Vida en el límite',
          body: 'La arena no es solo polvo: es **material piroclástico** y ceniza que el viento ha vuelto a mover. En el suelo puedes ver piroclastos de la erupción de **1989**. Y las rocas enormes detrás de la cabaña no las lanzó el volcán: las dejó el **glaciar** al retirarse.\n\nFíjate en las **plantas pioneras**: son muy pequeñas e intentan colonizar un suelo **pobre y ácido**. Son la prueba de que la vida resiste incluso en el límite de la supervivencia.',
        },
      ],
      valleLunar: [
        {
          subtitle: 'El hielo que rompe la roca',
          body: 'El **Valle Lunar**, también llamado **Lunares**, está a unos **4.350 m s. n. m.**, en pleno **superpáramo**. Su nombre viene de su aspecto estéril y desolado, que recuerda a otro planeta. Aquí se entiende la fuerza física del clima.\n\nEl agua se mete en las grietas de la roca y de noche se **congela**. Al congelarse aumenta su volumen y actúa como una cuña que parte las **andesitas** en pedazos angulares. Este proceso se llama **gelifracción**, y por eso las rocas están llenas de grietas.',
        },
        {
          subtitle: 'Arañazos y óxido',
          body: 'Algunas rocas tienen marcas que parecen arañazos. Son **estrías glaciares**: las dejó el glaciar al moverse y raspar la roca, y muestran hacia dónde avanzaba.\n\nLos **tonos rojizos** son otra forma de desgaste, esta vez química: el **hierro** de minerales como la hornblenda se **oxida** con el oxígeno y la humedad. En la andesita puedes distinguir dos minerales a simple vista: los claros son **plagioclasas** y los negros, **hornblendas**. Estás caminando sobre lavas antiguas que la atmósfera sigue transformando.',
        },
        {
          subtitle: 'Vida pionera',
          body: 'Casi no hay vegetación, pero la que hay resiste. La **loricaria**, también llamada **cacho de venado** o **coral de páramo**, muestra cómo la vida se adapta a condiciones extremas.\n\nLas fracturas de la roca van formando un suelo arenoso al que llega la vegetación pionera. Hace unos **100 años** aquí no había plantas, y dentro de otros 100 seguramente habrá muchas más. Desde este punto y hasta el Valle de las Tumbas, las dunas cubren buena parte de las rocas.',
        },
      ],
      valleTumbas: [
        {
          subtitle: 'Por qué se llama así',
          body: 'Llegaste a unos **4.460 m s. n. m.**, el final del recorrido, donde el superpáramo da paso a la **zona nival**. El nombre viene de unas rocas largas y planas, las **lajas**, que parecen ataúdes. Comunidades cercanas usaban rocas así para construir **tumbas de cancel**, aunque eso no quiere decir que las sacaran del Ruiz: es solo un parecido.\n\nHoy esas lajas están cubiertas de arena. El nombre llegó por tradición oral y ya se usaba en los años 80. A este lugar también lo llaman **Desierto de la Soledad**.',
        },
        {
          subtitle: 'Un lugar sagrado',
          body: 'En la época precolombina, este era un lugar sagrado. Los **Quimbayas**, **Carrapas**, **Gualíes**, **Panches**, **Ansermas** y **Pijaos** peregrinaban hasta aquí para rendir tributo a la montaña sagrada, **Kumanday**. Era un lugar de **pagamentos** y respeto, no de conquista, y algunas comunidades indígenas todavía hacen rituales aquí.\n\nSabemos poco de esas prácticas: lo más cercano son las crónicas de Indias y algunas investigaciones arqueológicas. Para los pueblos indígenas, las lagunas, los glaciares y los volcanes son lugares sagrados.',
        },
        {
          subtitle: 'El límite frente al volcán',
          body: 'El Ruiz es un **volcán activo**: nunca está “apagado”, solo tiene periodos de reposo. El **Servicio Geológico Colombiano** lo vigila las 24 horas, y el cráter Arenas, a unos **4,1 km** de aquí, emite gases constantemente. No se sube más allá de este punto, sobre todo por el riesgo de **lahares**, flujos de lodo y escombros volcánicos, y también para cuidar el frágil superpáramo.\n\nEl **13 de noviembre de 1985**, el calor de una erupción derritió el glaciar y los lahares bajaron por los ríos Gualí, Azufrado, Lagunillas y Molinos. Devastaron Armero, en el Tolima, y también Villamaría y Chinchiná: murieron **más de 23.000 personas**.',
        },
      ],
    },
  },
  chatScreen: {
    greeting:
      '¡Hola! Soy {pet}, tu compañía en Los Nevados. ¿Qué te gustaría descubrir hoy? Puedes preguntarme qué llevar al páramo o enviarme una foto de lo que encuentres en el camino.',
    greetingKeywords: ['{pet}', 'Los Nevados', 'qué llevar al páramo', 'una foto'],
    newChat: 'Nueva conversación',
    typing: '{pet} está pensando',
    seconds: '{s} s',
    milliseconds: '{ms} ms',
    // The button on an assistant message and the sheet that lists what the answer rests on.
    sources: {
      showOne: 'Ver la fuente de esta respuesta',
      showMany: 'Ver las {n} fuentes de esta respuesta',
      title: 'Fuentes',
      close: 'Cerrar fuentes',
      open: 'Abrir enlace',
      openLabel: 'Abrir {title}',
      retrieved: 'Consultada el {date}',
      favoriteLabel: 'Guardar {title} en favoritos',
      unfavoriteLabel: 'Quitar {title} de favoritos',
    },
    // Photos under an answer about a species or a place (src/ui/chat/MediaGallery.tsx).
    media: {
      // What a screen reader hears for the credit pill on a photo (it shows only the author).
      credit: 'Foto de {author}, licencia {license}',
    },
    // A photo the visitor attaches to identify a species or place (src/vision).
    photo: {
      sent: 'Foto enviada',
      attached: 'Foto adjunta',
      remove: 'Quitar foto',
      identify: 'Identificar una foto',
      captionPlaceholder: 'Escribe sobre la foto',
    },
    voice: {
      mic: 'Dictar pregunta',
      micHint: 'Mantén pulsado para hablar; al soltar, el texto aparece en el campo',
      recording: 'Grabando, suelta para transcribir',
      errorTitle: 'Dictado',
      permissionDenied: 'Necesitamos permiso de micrófono para dictar.',
      unavailable: 'El dictado no está disponible en este dispositivo.',
      busy: 'El dictado está ocupado. Intenta de nuevo.',
      error: 'No pude transcribir. Intenta de nuevo.',
      speak: 'Escuchar esta respuesta',
      speakStop: 'Detener la voz',
      speakError: 'No pude leer la respuesta en voz alta.',
    },
    // The gold sources badge of an answer taken from the official UTON guion
    // (src/ui/chat/ChatBubble.tsx) and the mark on each of its sources (SourcesSheet.tsx).
    verified: {
      badge: 'Fuente validada',
      label: 'Fuente validada por UTON. Ver la fuente',
      source: 'Validada por UTON',
    },
  },
  // Knowledge chat (top-1 curated answers, src/state/useKnowledge.ts).
  knowledge: {
    error: 'No pude procesar esa pregunta. Intenta escribirla de otra forma.',
  },
  // The cloud navigation bar over the chat and the group screens.
  nav: {
    chat: 'Chat',
    group: 'Grupo',
    route: 'Ruta',
    disabled: '{tab}, disponible pronto',
    settings: 'Configuración',
    accessibility: 'Accesibilidad',
  },
  // Group sync (/group): a guide sees the group on a line; a visitor sees its own link.
  group: {
    title: 'Grupo',
    chooseTitle: '¡Cuéntanos sobre ti!',
    chooseBody: 'Conéctate con tu grupo y recorran juntos el parque.',
    nameLabel: 'Tu nombre',
    namePlaceholder: 'Tu nombre (opcional)',
    nameHint: 'Opcional; así te verá el grupo',
    defaultGuide: 'Guía',
    defaultVisitor: 'Visitante',
    imGuide: '¡Soy guía!',
    imGuideHint: 'Empieza un grupo o únete como segundo guía',
    imVisitor: '¡Soy visitante!',
    imVisitorHint: 'Busca un guía cercano para unirte al grupo',
    searchingGuides: 'Buscando otro guía cerca…',
    bluetoothOff: 'Enciende el Bluetooth para usar Grupo.',
    permissionsDenied: 'Necesitamos permiso de Bluetooth para encontrar a tu grupo.',
    visitorsOne: '1 visitante',
    visitorsMany: '{n} visitantes',
    you: '{name} (tú)',
    guideFront: '{name}, guía de adelante',
    guideRear: '{name}, guía de atrás',
    zones: { near: 'cerca', mid: 'a media distancia', far: 'lejos', unseen: 'sin señal' },
    dot: '{name}, {zone}',
    dotAlert: '{name}, {zone}, con alerta',
    alertFar: '{name} se está alejando',
    alertLost: 'Perdimos la señal de {name}',
    alertGuideLost: 'Sin enlace con {name}, el otro guía',
    alertsMore: 'y {n} avisos más',
    lane: 'Línea del grupo, de adelante hacia atrás',
    alertDistance: 'Distancia de alerta',
    alertDistanceHint: 'Arrastra o ajusta para elegir a qué distancia te avisamos.',
    alertDistanceScale: 'Cerca hasta {near} m · alerta pasados {alert} m',
    alertDecrease: 'Acercar alerta',
    alertIncrease: 'Alejar alerta',
    cancelGuide: 'Cancelar',
    cancelGuideHint: 'Deja de guiar y vuelve a elegir tu rol',
    cancelSearch: 'Dejar de buscar',
    cancelSearchHint: 'Detiene la búsqueda y vuelve a elegir tu rol',
    leaveGroup: 'Salir del grupo',
    leaveShort: 'Salir',
    leaveGroupHint: 'Termina la conexión con el grupo y vuelve a elegir tu rol',
    meters: '{m} m',
    laneMark: '{zone} hasta {m} m',
    // The Pet customizer on the role chooser (src/ui/PetCustomizer.tsx).
    pet: {
      title: { guide: 'Tu {pet} de guía', visitor: 'Tu {pet} de visitante' },
      body: 'Elige qué lleva puesto y de qué color.',
      edit: { guide: 'Editar tu {pet} de guía', visitor: 'Editar tu {pet} de visitante' },
      done: 'Listo',
      accessory: 'Accesorio',
      color: 'Color',
      accessories: {
        none: 'Nada',
        guideHat: 'Sombrero de guía',
        visitorCap: 'Gorra',
        beanie: 'Gorro de lana',
        bandana: 'Pañoleta',
        flower: 'Flor de frailejón',
      },
      tints: { auto: 'Original', ink: 'Bosque', sky: 'Cielo', sun: 'Frailejón', lupine: 'Lupino' },
    },
    emptyTitle: 'Aún no hay visitantes',
    emptyBody:
      'Pide a cada visitante que junte su celular con el tuyo. Aparecerán aquí, en la línea del grupo.',
    visitor: {
      searchingTitle: 'Acerca tu celular al del guía',
      searchingBody: 'Junta tu celular con el de tu guía para unirte al grupo.',
      near: 'Cerca del guía',
      nearBody: 'Vas con el grupo. Disfruta el camino.',
      away: 'Te estás alejando',
      awayBody: 'Acércate a tu guía para no perder el grupo.',
      lost: 'Sin señal',
      lostBody: 'Tu guía no te encuentra. Quédate en el sendero y búscalo con la vista.',
    },
  },
  // Accessibility overlay panel (opened from the left button of CloudNavBar).
  accessibilityPanel: {
    title: 'Accesibilidad',
    close: 'Cerrar accesibilidad',
    reset: 'Restablecer',
    resetHint: 'Vuelve todos los ajustes de accesibilidad a sus valores originales',
    textSize: {
      title: 'Tamaño del texto',
      body: 'Respeta el tamaño de tu teléfono y te permite ampliarlo con vista previa.',
      decrease: 'Reducir tamaño del texto',
      increase: 'Aumentar tamaño del texto',
      sliderHint: 'Arrastra o elige un paso para cambiar el tamaño del texto',
      percent: '{pct}%',
      levels: {
        normal: 'Normal',
        large: 'Grande',
        larger: 'Muy grande',
        extra: 'Extra',
      },
      previewLabel: 'Vista previa',
      previewTitle: 'Valle de las Tumbas',
      previewBody:
        'A 4.450 m s. n. m., lleva abrigo impermeable y agua para el recorrido por el páramo.',
    },
    highContrast: {
      title: 'Alto contraste',
      body: 'Refuerza texto y bordes para leer con claridad bajo el sol.',
    },
    reduceMotion: {
      title: 'Reducir movimiento',
      body: 'Detiene animaciones decorativas y muestra los mensajes al instante.',
      systemActive: 'También está activo en los ajustes de tu teléfono.',
    },
    colorVision: {
      title: 'Daltonismo',
      body: 'Adapta la paleta y mantiene iconos y texto en cada estado.',
      previewLabel: 'Estados con icono y color',
      modes: {
        none: { label: 'Estándar', hint: 'Paleta original del parque' },
        protanopia: { label: 'Protanopía', hint: 'Rojo-verde (menor sensibilidad al rojo)' },
        deuteranopia: { label: 'Deuteranopía', hint: 'Rojo-verde (menor sensibilidad al verde)' },
        tritanopia: { label: 'Tritanopía', hint: 'Azul-amarillo' },
      },
      statuses: {
        near: 'Cerca',
        alert: 'Alerta',
        unseen: 'Sin señal',
      },
    },
  },
  // Configuration overlay panel (opened from the right button of CloudNavBar).
  settingsPanel: {
    title: 'Configuración',
    close: 'Cerrar configuración',
    back: 'Volver a configuración',
    // The knowledge chat's verified-only switch (src/state/verifiedOnly.ts).
    verifiedOnly: {
      title: 'Solo información verificada por UTON',
      body: 'El chat responde solo con el guion oficial de la Unión Temporal Operación Nevados (2024).',
    },
    savedSources: {
      title: 'Fuentes guardadas',
      countZero: 'Aún no has guardado fuentes',
      countOne: '1 fuente guardada',
      countMany: '{n} fuentes guardadas',
      emptyTitle: 'Sin fuentes guardadas',
      emptyBody:
        'Cuando abras las fuentes de una respuesta en el chat, toca la estrella para guardarlas aquí.',
      removedNotice: 'Fuente quitada de guardadas',
      undo: 'Deshacer',
    },
    about: {
      title: 'Acerca de',
      menuSubtitle: 'Nevados · v{version}',
      version: 'Versión {version}',
      summary:
        'Guía sin conexión para recorrer el Parque Nacional Natural Los Nevados con información verificada y acompañamiento en grupo.',
      offlineTitle: 'Pensada para modo avión',
      offlineBody:
        'El chat de conocimiento, el recorrido por estaciones y la sincronización de grupo funcionan en tu dispositivo sin depender de internet.',
      sourcesTitle: 'Fuentes de referencia',
      sourcesBody:
        'Contenido basado en Parques Nacionales Naturales de Colombia, Servicio Geológico Colombiano (SGC), IDEAM e iNaturalist.',
      creditsTitle: 'Créditos y licencias',
      creditsBody:
        'Tipografías Manrope y Bricolage Grotesque (OFL), iconos Lucide (ISC) y créditos fotográficos en cada imagen.',
    },
  },
  // Developer screens (Lab, design catalog).
  dev: {
    lab: 'Onboarding Lab',
    design: 'Componentes',
    // TEMPORARY web-only /group preview simulator.
    groupSim: {
      barLabel: 'Simulador temporal (web)',
      guideNearbyOn: 'Hay guía cerca: sí',
      guideNearbyOff: 'Simular guía cerca',
      addVisitor: '+ Visitante',
      addVisitorCount: '+ Visitante ({n})',
      addOtherGuide: '+ Otro guía',
      removeOtherGuide: 'Quitar otro guía',
      clear: 'Limpiar',
      simulateGuide: 'Simular guía',
      near: 'Cerca',
      away: 'Lejos',
      lost: 'Sin señal',
    },
    // The /design component workshop. Sample messages and texts are fixtures in src/design.
    workshop: {
      title: 'Componentes',
      position: '{n} / {name}',
      nav: 'Componentes del sistema',
      items: {
        composer: 'Barra de entrada',
        bubbles: 'Mensajes',
        buttons: 'Botones',
        indicators: 'Indicadores',
        foundations: 'Fundamentos',
        group: 'Grupo',
      },
      groupOne: 'Un guía',
      groupTwo: 'Dos guías',
      groupAlert: 'Alerta',
      groupUnseen: 'Sin señal',
      groupEmpty: 'Sin visitantes',
      groupRoles: 'Roles',
      groupSignal: 'Señal',
      groupMeters: 'Distancia',
      controls: 'Controles',
      appearance: 'Apariencia',
      docked: 'Acoplada',
      floating: 'Flotante',
      sample: 'Contenido',
      presetEmpty: 'Vacía',
      presetTyping: 'Escribiendo',
      presetLong: 'Texto largo',
      presetPending: 'Pendiente',
      state: 'Estado',
      stateIdle: 'En reposo',
      stateTyping: 'Con texto',
      stateSending: 'Enviando…',
      stateDisabled: 'Envío bloqueado mientras responde',
      lastSent: 'Último envío: «{text}»',
      nothingSent: 'Escribe y envía para probarla.',
      reset: 'Reiniciar demo',
      replay: 'Repetir entrada',
      replayReply: 'Repetir respuesta',
      reduceMotion: 'Reducir movimiento',
      view: 'Vista',
      bubbleView: 'Burbujas',
      screenView: 'Pantalla de chat',
      thinking: 'Pensando',
      screenState: 'Estado de la pantalla',
      thread: 'Mensajes',
      threadTalk: 'Conversación',
      threadSources: 'Fuentes',
      threadUrgent: 'Urgencia',
      threadPhotos: 'Fotos',
      gallery: 'Galería',
      gallerySingle: 'Una foto',
      galleryRows: 'Filas',
      galleryColumns: 'Columnas',
      pressed: 'Pulsado: {name} ({count})',
      notPressed: 'Pulsa un control para probarlo.',
      step: 'Paso {n} de {total}',
      previous: 'Anterior',
      next: 'Siguiente',
      colors: 'Color',
      typeScale: 'Tipografía · Manrope',
      pet: 'Mascota',
      emotion: 'Emoción',
      accessory: 'Accesorio',
    },
  },
};
