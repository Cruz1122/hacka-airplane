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
      brisas: 'Frailejón',
      aguacerales: 'Oso de anteojos',
      arenales: 'Puma',
      valleLunar: 'Zorro de páramo',
      valleTumbas: 'Cóndor de los Andes',
    },
    stations: {
      brisas: {
        name: 'Centro de Inducción Brisas',
        blurb: 'Punto de registro, charla obligatoria y salida. Unos 4.100 m s. n. m.',
      },
      aguacerales: {
        name: 'Aguacerales: donde nace el agua',
        blurb: 'A unos 4.160 m: humedal de superpáramo que alimenta la quebrada Azufrales.',
      },
      arenales: {
        name: 'Arenales: el desierto del volcán',
        blurb: 'A 4.230 m: dunas de arena volcánica frente al Ruiz.',
      },
      valleLunar: {
        name: 'Valle Lunar: un paisaje de otro mundo',
        blurb: 'Arena, ceniza y viento entre Arenales y el Valle de las Tumbas.',
      },
      valleTumbas: {
        name: 'Valle de las Tumbas: el silencio de la montaña',
        blurb: 'A 4.450 m: final del recorrido Brisas. También llamado Desierto de la Soledad.',
      },
    },
    back: 'Volver',
    photo: 'Imagen {n} de la etapa',
    sheet: {
      more: '¡Saber más!',
      close: 'Cerrar',
      blurbs: {
        brisas:
          'La puerta de los superpáramos, a 4.100 m sobre la ladera del Nevado del Ruiz. Aquí te inscribes, escuchas la charla y conoces al guía que te llevará hasta el Valle de las Tumbas.',
        aguacerales:
          'Primera parada del superpáramo: musgos y líquenes que beben del hielo en las franjas que el glaciar fue dejando atrás. Un páramo que guarda el agua de toda la región.',
        arenales:
          'Aquí el suelo es ceniza volcánica. Caminas al pie del Ruiz, un volcán activo de 5.321 m cuyo cráter Arenas mide casi un kilómetro de ancho.',
        valleLunar:
          'Parece otro planeta: un altiplano de cenizas y rocas desde donde se asoman el Ruiz, Santa Isabel, el Quindío y el Tolima. Una de las vistas más imponentes de la ruta.',
        valleTumbas:
          'El final del camino, a 4.450 m. Sus formaciones volcánicas y fumarolas parecen un cementerio, y los Quimbaya subían hasta aquí en peregrinación a dejar ofrendas.',
      },
      species: {
        brisas:
          'Crece apenas un centímetro al año. Sus hojas peludas atrapan la niebla y la convierten en agua.',
        aguacerales:
          'El único oso de Suramérica. Las manchas claras de su cara son únicas en cada individuo, como una huella digital.',
        arenales: 'Tan esquivo que casi nunca se deja ver, aunque él sí te esté mirando.',
        valleLunar:
          'Pese a su nombre, no es un zorro verdadero: es pariente más cercano de los lobos y los chacales.',
        valleTumbas:
          'Más de tres metros de alas: puede planear horas sobre estos valles sin un solo aleteo.',
      },
    },
    camera: {
      prompt: 'Toma una foto de esta estación.',
      take: 'Tomar foto',
      denied: 'Sin permiso de cámara. Actívalo en ajustes para fotografiar esta estación.',
      unavailable: 'La cámara no está disponible aquí.',
      capturedA11y: 'Foto tomada en esta estación',
    },
    pages: {
      brisas: [
        {
          subtitle: 'Centro de inducción',
          body: 'El centro de inducción de **Brisas** es el punto de ingreso al sector norte del **PNN Los Nevados**. Hay que inscribirse y recibir obligatoriamente una charla de inducción sobre las normas y condiciones de ingreso; allí se debe contar con un **guía profesional** avalado por el PNN Los Nevados y autorizado por una operadora de turismo habilitada.\n\nEn la zona norte, el recorrido autorizado comprende el carreteable **Brisas–Arenales–Valle de las Tumbas**. El centro de inducción Brisas atiende y recibe ingresos entre las **8:00 a. m.** y las **2:00 p. m.**',
        },
        {
          subtitle: 'Cómo llegar',
          body: 'El acceso a la zona norte, ubicada en la ladera occidental del volcán **Nevado del Ruiz**, se realiza por la vía que conecta el sector de La Esperanza o El Ocho, en Manizales, con **Murillo**, Tolima. Tras aproximadamente 18 km se toma el desvío que conduce a la entrada del parque, en el sector de Brisas, a unos **4.100 m s. n. m.** Desde este punto, el recorrido autorizado para visitantes llega hasta el Valle de las Tumbas, a unos **4.450 m s. n. m.**',
        },
        {
          subtitle: 'El parque',
          body: 'Los linderos del **Parque Nacional Natural Los Nevados** fueron fijados mediante el Acuerdo **015** del 28 de marzo de **1973** del Inderena y aprobados mediante la Resolución **148** del 30 de abril de **1974**.\n\nEmpezó con cerca de **38.000** hectáreas y, a cierre de **2023**, sumaba **61.377,49** hectáreas. El parque se extiende por los departamentos de Caldas, Risaralda, Tolima y Quindío.',
        },
      ],
      aguacerales: [
        {
          subtitle: 'Donde nace el agua',
          body: 'A unos 4.160 metros sobre el nivel del mar, Aguacerales parece un paisaje pequeño, pero cumple una función enorme. Es un humedal de superpáramo donde el agua se filtra entre musgos, cojines y vegetación adaptada al frío.\n\nEstas plantas actúan como una esponja viva: retienen la lluvia y la humedad, y luego las liberan lentamente. Gracias a ese proceso, Aguacerales ayuda a regular el agua que alimenta la quebrada Azufrales y, más adelante, la cuenca del río Chinchiná.',
        },
        {
          subtitle: 'Gota a gota',
          body: 'Aquí el agua no aparece de golpe: nace gota a gota, entre musgos que pueden tardar años en crecer. Por eso, caminar por Aguacerales es comprender que un paisaje aparentemente silencioso sostiene ríos, comunidades y ciudades mucho más abajo.',
        },
        {
          subtitle: 'Cumanday',
          body: 'El lugar también forma parte de la alta montaña del Nevado del Ruiz, conocida en tradiciones indígenas como Cumanday. En las cosmovisiones andinas, el agua es un elemento vivo que conecta montañas, páramos, ríos y comunidades. Aguacerales invita a mirar el paisaje con otra mirada: no como un simple humedal, sino como el origen silencioso de un recurso esencial.',
        },
      ],
      arenales: [
        {
          subtitle: 'El desierto del volcán',
          body: 'A 4.230 metros sobre el nivel del mar, Arenales parece un pequeño desierto en medio de los Andes. Sus dunas de arena volcánica se formaron con cenizas y materiales expulsados por el Nevado del Ruiz, un volcán activo cuyo cráter principal se llama Arenas.\n\nEl viento que recorre la cordillera ha moldeado estos depósitos durante décadas, creando un paisaje que cambia con el tiempo. Aquí no hay árboles ni praderas extensas: predominan la arena, las rocas, los líquenes y algunas plantas capaces de sobrevivir al frío, a la radiación y a la escasez de agua.',
        },
        {
          subtitle: 'Cumanday',
          body: 'Desde Arenales se puede observar el borde del glaciar del Nevado del Ruiz y comprender la relación entre fuego, hielo y vida. Para los pueblos indígenas de la región, esta montaña era conocida como Cumanday, un nombre que recuerda que el territorio tiene historias anteriores a los mapas y a los nombres coloniales.',
        },
        {
          subtitle: 'Un volcán vivo',
          body: 'Arenales es un recordatorio de que el Ruiz no es una montaña estática: es un volcán vivo. Su historia incluye erupciones documentadas desde 1570 y, especialmente, la tragedia de 1985, que transformó la manera en que Colombia entiende el riesgo volcánico. Visitarlo es admirar un paisaje extraordinario, pero también reconocer la fuerza de la naturaleza y la importancia de conservar estos ecosistemas de alta montaña.',
        },
      ],
      valleLunar: [
        {
          subtitle: 'Un paisaje de otro mundo',
          body: 'Entre Arenales y el Valle de las Tumbas se encuentra el Valle Lunar, un espacio donde la arena, la ceniza y el viento han creado un paisaje que parece de otro planeta. Sus formas onduladas y su tono gris evocan la superficie de la Luna, de ahí su nombre.\n\nPero este “desierto” no es común: es un desierto frío de alta montaña, moldeado por la actividad del Nevado del Ruiz. Durante siglos, las erupciones y emisiones del volcán han depositado ceniza y materiales volcánicos en las laderas; el viento los ha redistribuido y tallado, creando las dunas y ondulaciones que se ven hoy.',
        },
        {
          subtitle: 'Un volcán vivo',
          body: 'El Valle Lunar es un recordatorio de que el Ruiz es un volcán vivo. Su paisaje cambia con el tiempo, y cada capa de arena cuenta una parte de la historia geológica de la montaña.\n\nAunque parece inhóspito, el Valle Lunar forma parte del superpáramo, un ecosistema donde la vida se adapta a condiciones extremas. Musgos, líquenes y plantas resistentes encuentran espacios para crecer, mostrando la fuerza silenciosa de la naturaleza.',
        },
        {
          subtitle: 'Territorio sagrado',
          body: 'Para algunas comunidades indígenas, este territorio tiene un valor espiritual y es escenario de prácticas como los pagamentos indígenas. En la cosmovisión andina, la montaña es un ser vivo y una fuente de agua; el Valle Lunar invita a conectar con esa idea y a admirar un paisaje que es a la vez frágil, dinámico y sagrado.',
        },
      ],
      valleTumbas: [
        {
          subtitle: 'El silencio de la montaña',
          body: 'A 4.450 metros sobre el nivel del mar, el Valle de las Tumbas es el punto final del recorrido por el sector Brisas del PNN Los Nevados. También conocido como el Desierto de la Soledad, es un paisaje de rocas, cenizas y sedimentos volcánicos donde la vegetación casi desaparece.\n\nEste valle no es un lugar común: es un desierto frío de alta montaña, moldeado por la fuerza del Nevado del Ruiz. Durante siglos, las erupciones y emisiones del volcán han depositado ceniza y materiales piroclásticos en las laderas; el viento y el tiempo los han transformado en el paisaje que se ve hoy.',
        },
        {
          subtitle: 'Un volcán vivo',
          body: 'El Valle de las Tumbas es un recordatorio de que el Ruiz es un volcán vivo. Desde allí se puede observar parte de la ladera del volcán y, en algunos momentos, fumarolas del cráter Arenas, recordando que la montaña sigue activa.',
        },
        {
          subtitle: 'Lugar sagrado',
          body: 'Pero el Valle de las Tumbas no es solo geología: es también un lugar sagrado. Para los pueblos indígenas Puyas y Quimbayas, era un destino de peregrinación y un espacio de conexión espiritual con la naturaleza. En la cosmovisión andina, la montaña —conocida como Cumanday— es un ser vivo y una fuente de agua.\n\nVisitar el Valle de las Tumbas es admirar un paisaje extraordinario, pero también reconocer la fuerza de la naturaleza, la memoria de los pueblos indígenas y la importancia de conservar estos ecosistemas de alta montaña.',
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
