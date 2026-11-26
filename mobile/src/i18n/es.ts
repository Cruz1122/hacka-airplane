// Spanish UI copy: the source of truth for the label keys. Every other locale must match this
// shape (see `Labels` in ./index). `{name}` placeholders are filled with `fill()`.
export const es = {
  appTitle: 'Nevados',
  parkName: 'Parque Nacional Natural Los Nevados',
  settings: 'Ajustes',
  history: 'Historial',
  inputPlaceholder: 'Escribe tu pregunta',
  send: 'Enviar',
  reset: 'Reiniciar',
  thinking: 'Pensando...',
  debug: 'Depuración',
  state: 'Estado',
  noSteps: 'Sin pasos todavía',
  modelMissing: 'Modelo no encontrado en el dispositivo',
  modelLoading: 'Cargando modelo...',
  modelError: 'Error del modelo',
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
  tabs: {
    chat: 'Chat',
    trail: 'Recorrido',
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
        name: 'Sector Aguacerales',
        blurb: 'Primera parada de interpretación: páramo y vestigios volcánicos.',
      },
      arenales: {
        name: 'Arenales',
        blurb: 'Terrenos volcánicos, ceniza y formaciones de paisaje lunar.',
      },
      valleLunar: {
        name: 'Valle Lunar',
        blurb: 'Punto panorámico de gran valor paisajístico en la ruta.',
      },
      valleTumbas: {
        name: 'Valle de las Tumbas / Valle del Silencio',
        blurb: 'Final del recorrido vehicular. Acceso máximo con el Ruiz en nivel amarillo.',
      },
    },
    back: 'Volver',
    photo: 'Imagen {n} de la etapa',
    photoCredit: 'Foto: {author}',
    photoCreditA11y: 'Imagen {n} de la etapa. Foto: {author}',
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
          body: 'El centro de visitantes de **Brisas** es la puerta de entrada a los superpáramos. Hay que inscribirse y recibir una charla sobre las normas; allí asignan el **guía** que acompaña hasta el Valle de las Tumbas.\n\nEn la zona norte el recorrido va desde el centro de inducción hasta el Valle de Tumbas, con ingreso entre las **8:00 a. m.** y las **2:00 p. m.**',
        },
        {
          subtitle: 'Cómo llegar',
          body: 'El acceso a la zona norte, en la ladera occidental del volcán **Nevado del Ruiz**, sale de la vía que une La Esperanza–El Ocho (Manizales) con **Murillo** (Tolima).\n\nTras unos 18 km se toma el desvío a Brisas, a **4.100 m s. n. m.** Desde este punto el recorrido autorizado para visitantes llega hasta el Valle de las Tumbas, a **4.450 m**.',
        },
        {
          subtitle: 'El parque',
          body: 'El **Parque Nacional Natural Los Nevados** se declaró área protegida en **1974** (acuerdo 015 de 1973 del Inderena y resolución 148 del 30 de abril de 1974).\n\nEmpezó con cerca de 38 mil hectáreas y a cierre de 2023 sumaba **61.377,49 ha**: 47,1 % en el Tolima, 35,6 % en Risaralda, 13,5 % en Caldas y 3,8 % en el Quindío.',
        },
      ],
      aguacerales: [
        {
          subtitle: 'Superpáramo',
          body: 'Desde Brisas el camino de tierra atraviesa **superpáramos**: franjas de retroceso del glaciar, con musgos, líquenes y hierbas resistentes.\n\n**Aguacerales** es de las primeras paradas de esa ruta: musgos que beben del hielo, antes de las cenizas de Arenales y del Valle Lunar.',
        },
        {
          subtitle: 'Frailejones',
          body: 'Por encima de los **3.000 m**, los bosques de niebla y los prados dan paso al páramo, donde reinan los **frailejones**, endémicos de los Andes del norte.\n\nEsa planta capta el agua de la niebla y la lleva al suelo; en estas alturas también se ven **cóndores** y colibríes chivitos entre los frailejones.',
        },
        {
          subtitle: 'Agua y glaciares',
          body: 'El páramo es el mayor **regulador de agua** de la región. El parque guarda el **50 %** de las montañas nevadas de Colombia: Kumanday (Ruiz), Poleka Kasue (Santa Isabel) y Dulima (Tolima).\n\nEl cambio climático ha acelerado el derretimiento de esos glaciares en los últimos **70 años**.',
        },
      ],
      arenales: [
        {
          subtitle: 'Cenizas',
          body: '**Arenales** es el tramo de cenizas volcánicas en la ruta de tierra hacia el Valle de las Tumbas.\n\nJunto con Aguacerales y el Valle Lunar completa un paisaje volcánico de otro mundo en el superpáramo del Ruiz.',
        },
        {
          subtitle: 'El volcán',
          body: 'El Ruiz es un **estratovolcán** activo de **5.321 m**, a 28 km al sureste de Manizales. Tiene dos conos parásitos, **La Olleta** y La Piraña, y el cráter activo **Arenas**, de 870 × 830 m y 247 m de profundidad.\n\nEn época precolombina se le llamó Cumanday (Cerro Blanco), Tabuchía (candela o fuego) o Tama (Padre Mayor).',
        },
        {
          subtitle: 'Actividad',
          body: 'El volcán cubre más de **200 km²**. El cráter Arenas mide cerca de 1 km de ancho. Hay erupciones documentadas desde **1570**; la erupción actual comenzó en noviembre de **2014**, con emisiones de gas y ceniza y sismos.\n\nEl Servicio Geológico Colombiano mantiene la alerta en **amarillo**, el segundo de cuatro niveles.',
        },
      ],
      valleLunar: [
        {
          subtitle: 'La parada',
          body: 'El **Valle Lunar** es una de las paradas de mayor valor paisajístico en el camino de superpáramo, entre las cenizas de Arenales y el final en el Valle de las Tumbas.',
        },
        {
          subtitle: 'Cuatro nevados',
          body: 'En este altiplano se yerguen el **Ruiz**, **Santa Isabel**, el **Quindío** y el **Tolima**, entre fumarolas, cráteres, lagunas de alta montaña y páramos.\n\nEl paisaje lunar del Nevado del Ruiz es uno de los retratos más citados de esa ruta.',
        },
        {
          subtitle: 'Ecosistemas',
          body: 'El parque, en la cordillera Central, protege **páramos**, superpáramos, humedales altoandinos, bosques andinos y glaciares.\n\nEl Ruiz ofrece glaciares, rocas volcánicas y terrenos de origen tectónico y geotérmico.',
        },
      ],
      valleTumbas: [
        {
          subtitle: 'El final del recorrido',
          body: 'Aquí termina el recorrido autorizado para visitantes, a **4.450 m s. n. m.** El **Valle de las Tumbas** es un paraje desolado a más de 4.000 m, con paisajes lunares, géiseres y cascadas.\n\nEs el destino habitual de las visitas que salen de Brisas.',
        },
        {
          subtitle: 'El nombre',
          body: 'El nombre viene de formaciones volcánicas y fumarolas con aspecto de cementerio. Los **Quimbaya** no se enterraban aquí, pero sí era un lugar de peregrinación: se han hallado cerámicas interpretadas como ofrendas.',
        },
        {
          subtitle: '13 de noviembre de 1985',
          body: 'El **13 de noviembre de 1985** la erupción del Ruiz provocó lahares que arrasaron **Armero**, con cerca de **25 mil** muertos.\n\nEl volcán sigue activo; en 2012 una minierupción sentida desde la cabaña de Brisas llevó el parque a cerrar nueve meses, y la alerta permanece en **amarillo**.',
        },
      ],
    },
  },
  chatScreen: {
    greeting: '¡Hola! Soy {pet}. Pregúntame por senderos, clima, normas o seguridad del parque.',
    more: 'Más opciones',
    newChat: 'Nueva conversación',
    debugShow: 'Mostrar depuración',
    debugHide: 'Ocultar depuración',
    typing: '{pet} está pensando',
    seconds: '{s} s',
    // The browser loads the e5 model from the dev server (metro.config.js) out of models/knowledge.
    webNoModel:
      'En web el modelo se carga desde models/knowledge con el servidor de desarrollo (npx expo start --web).',
    // The button on an assistant message and the sheet that lists what the answer rests on.
    sources: {
      showOne: 'Ver la fuente de esta respuesta',
      showMany: 'Ver las {n} fuentes de esta respuesta',
      title: 'Fuentes',
      close: 'Cerrar fuentes',
      open: 'Abrir enlace',
      openLabel: 'Abrir {title}',
      retrieved: 'Consultada el {date}',
    },
  },
  // Knowledge chat (top-1 curated answers, src/state/useKnowledge.ts).
  knowledge: {
    error: 'No pude procesar esa pregunta. Intenta escribirla de otra forma.',
  },
  // Developer screens (Lab, design catalog).
  dev: {
    lab: 'Onboarding Lab',
    design: 'Componentes',
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
      },
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
      pressed: 'Pulsado: {name} ({count})',
      notPressed: 'Pulsa un control para probarlo.',
      step: 'Paso {n} de {total}',
      previous: 'Anterior',
      next: 'Siguiente',
      colors: 'Color',
      typeScale: 'Tipografía · Manrope',
      pet: 'Mascota',
      emotion: 'Emoción',
    },
  },
};
