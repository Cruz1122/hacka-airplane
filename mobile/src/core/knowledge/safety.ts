// Text rules that run before any model: an urgent-safety notice and an offline live-status notice.
// They are a recall-first safety net, not a classifier: a false alarm costs one banner above the
// normal menu, a miss can leave a visitor in danger with only the menu. Every reply still carries
// the curated 123 line regardless of these rules (docs/phase3-architecture.md §1.2).
//
// Matching runs on folded text: lower case, Spanish accents removed with an explicit map (Hermes
// support for String.prototype.normalize and Intl is unverified), punctuation to spaces, doubled
// vowels squeezed ("auxilioo", "nooo"). Rules are written in that folded form.

export interface SafetyResult {
  urgent: boolean;
  liveStatus: boolean;
  matched: string[]; // fired rule names, "emergency:<rule>" or "live:<rule>"
}

// Explicit fold table, upper case included so it does not depend on Unicode-aware toLowerCase.
const FOLD_FROM = 'áàäâãéèëêíìïîóòöôõúùüûñçÁÀÄÂÃÉÈËÊÍÌÏÎÓÒÖÔÕÚÙÜÛÑÇ';
const FOLD_TO = 'aaaaaeeeeiiiiooooouuuuncaaaaaeeeeiiiiooooouuuunc';
const FOLD: Record<string, string> = {};
for (let i = 0; i < FOLD_FROM.length; i++) FOLD[FOLD_FROM.charAt(i)] = FOLD_TO.charAt(i);

/** Folded form the rules match against (exported for tests and for the engine's diagnostics). */
export function foldText(text: string): string {
  let out = '';
  for (let i = 0; i < text.length; i++) {
    const ch = text.charAt(i);
    out += FOLD[ch] ?? ch;
  }
  return out
    .toLowerCase()
    .replace(/[\u0300-\u036f]/g, '') // combining marks from decomposed input
    .replace(/[^a-z0-9]+/g, ' ')
    .replace(/([aeiou])\1+/g, '$1') // "auxilioo", "nooo", "ayudaaa"
    .replace(/([b-df-hj-np-tv-z])\1{2,}/g, '$1$1') // "socorrrro" -> "socorro"
    .trim();
}

interface Rule {
  name: string;
  re: RegExp;
  // Weak rules describe situations people also ask about hypothetically ("qué hago si hay
  // tormenta"); the hypothetical/informational frame disables them. Strong rules always fire.
  weak?: boolean;
  unless?: RegExp; // rule-specific suppressor
}

const rx = (src: string) => new RegExp(`\\b(?:${src})\\b`);
const G = (n: number) => `(?: [a-z0-9]+){0,${n}}`; // up to n intervening words

const PERSON =
  '(?:amig[oa]s?|herman[oa]s?|hij[oa]s?|nin[oa]s?|nene|nena|bebe|papa|mama|padre|madre|espos[oa]|novi[oa]|' +
  'compa|companer[oa]s?|parce|parcero|parcera|llave|socio|mano|prim[oa]|ti[oa]|abuel[oa]|sobrin[oa]|' +
  'senor|senora|persona|turista|guia|pelad[oa]|chin[oa]|muchach[oa]|cuch[oa]|viejo|vieja|pareja|' +
  'acompanante|compadre|comadre|cunad[oa]|suegr[oa]|mujer|marido|alguien|uno del grupo|una del grupo)';
const BODY =
  '(?:piernas?|brazos?|tobillos?|munecas?|manos?|pies?|rodillas?|cadera|cuello|espalda|columna|clavicula|' +
  'hombros?|costillas?|dedos?|hueso|nariz|codo|craneo|mandibula|pantorrilla|rodilla)';
const DET = '(?:el |la |los |las |mi |mis |su |sus |un |una )?';

const EMERGENCY_RULES: Rule[] = [
  // Cries for help. "ayuda" alone is too common ("ayúdame a reservar"); require the imperative
  // plural/pronoun forms not followed by a task, or an urgency word.
  {
    name: 'cry',
    re: rx('a?uxilio|socorro|socoro|sokorro|zocorro|sokoro|auxlio|ausilio|help'),
  },
  {
    name: 'cry',
    re: rx('ayud(?:a|e)(?:me|nos|nme|nnos)(?! (?:a|con|para|por favor a) )|ayudenme|ayudennos'),
  },
  {
    name: 'cry',
    re: rx(
      '(?:necesito|necesitamos|pido|pedimos) ayuda (?:urgente|ya|rapido|por favor)|ayuda (?:urgente|rapido|ya)',
    ),
  },
  {
    name: 'call_rescue',
    re: rx(
      '(?:necesito|necesitamos|pidan|pide|llamen|llama|llame|manden|envien|mande|traigan) ' +
        '(?:una |un |a (?:una |un |los )?)?(?:ambulancia|rescate|rescatista|helicoptero|socorrista|paramedico|bomberos|medico ya)\\w*',
    ),
  },
  {
    name: 'call_rescue',
    re: rx(
      '(?:llamen|llama|llame|marquen|marca|marque) (?:al |a la linea )?(?:123|112|911|132|119|144)',
    ),
  },
  {
    name: 'injured',
    re: rx(
      '(?:esta|estan|estoy|estamos|quedo|quedaron|salio|salieron) (?:muy |mal |gravemente |bastante )?(?:herid|lesionad|golpead|accidentad)[oa]s?',
    ),
  },
  {
    name: 'injured',
    weak: true,
    re: rx(
      '(?:hay|tenemos|tengo) (?:un |una |varios |dos |tres )?(?:herid|lesionad|accidentad)[oa]s?',
    ),
  },
  {
    name: 'trapped',
    re: rx(
      '(?:estoy|estamos|esta|estan|quedamos|quede|quedo|nos quedamos) (?:atrapad|atascad|aislad|varad|enterrad)[oa]s?',
    ),
  },
  {
    name: 'unwell',
    weak: true,
    re: rx(
      '(?:me|se|nos) (?:siento|siente|sentimos|sienten) (?:muy |super |demasiado |horrible |fatal |terrible )mal|(?:estoy|esta|estamos) (?:muy |super |demasiado )(?:mal|maread[oa]s?)(?! (?:con|de) )|(?:estoy|esta|estamos) maread[oa]s?',
    ),
  },
  {
    name: 'shock',
    re: rx(
      '(?:esta|se puso|se esta poniendo|lo veo|la veo) (?:muy )?(?:palid|gris)[oa]s?|sudando frio|sudor frio',
    ),
  },
  {
    name: 'grave',
    re: rx(
      'se (?:esta |nos esta |me esta )?muriendo|(?:me|nos) (?:voy|vamos) a morir|se va a morir|(?:esta|estoy|estamos) (?:muy |super )?grave|parece muert[oa]',
    ),
  },
  {
    name: 'emergency_report',
    weak: true,
    re: rx(
      '(?:tenemos|tengo|tuvimos|tiene) una emergencia|estamos en (?:una )?emergencia|(?:esto|es) es una emergencia|es una emergencia',
    ),
  },

  // Not breathing, unconscious, fainting, choking, seizure.
  {
    name: 'not_breathing',
    re: rx(
      'no (?:esta |estoy )?respir\\w*|dejo de respirar|no (?:puede|puedo|podemos|pueden|logra|logro) respirar|casi no (?:puede|puedo|podemos) respirar',
    ),
  },
  {
    name: 'unresponsive',
    re: rx(
      'no (?:responde|reacciona|despierta|se despierta|abre los ojos|se mueve)|casi no reacciona',
    ),
  },
  {
    name: 'unresponsive',
    re: rx(
      'incons?c?ien(?:te|tes)|perdio (?:el conocimiento|el sentido|la conciencia)|quedo (?:tirad[oa]|privad[oa]|inconsciente)|esta (?:tirad[oa]|privad[oa])',
    ),
  },
  {
    name: 'fainted',
    re: rx(
      'se (?:me |nos |le )?(?:desmayo|desmallo|desvanecio|desplomo|privo|desmayaron)|(?:le|me) dio un (?:desmayo|patatus|soponcio|vahido)|esta desmayad[oa]',
    ),
  },
  {
    name: 'fainted',
    weak: true,
    re: rx('se (?:me |nos |le )?(?:desmaya|desmalla|desvanece|desploma)'),
  },
  {
    name: 'choking',
    re: rx(
      'se (?:esta |nos esta )?(?:ahogando|atragantando|atorando)|se (?:atraganto|atoro|ahogo)|esta atragantad[oa]',
    ),
  },
  {
    name: 'seizure',
    re: rx(
      'convulsion(?:ando|a|o)?|esta convulsionando|(?:le|me) (?:dio|esta dando) (?:un ataque|una convulsion|un infarto|un paro)',
    ),
  },
  {
    name: 'cyanosis',
    re: rx(
      '(?:esta|se puso|se esta poniendo|tiene la cara|tiene los labios|labios) morad[oa]s?|labios azules',
    ),
  },
  {
    name: 'chest_pain',
    re: rx(
      '(?:me|le|nos) duele (?:mucho |muchisimo |fuerte )?el pecho|dolor (?:muy )?fuerte (?:en el|de) pecho',
    ),
  },

  // Altitude sickness (soroche, HAPE, HACE).
  {
    name: 'altitude',
    re: rx(
      `(?:me|le|nos|les) (?:dio|dieron|esta dando|pego|cogio|agarro|da|dan)${G(2)} (?:soroche|mal de (?:altura|montana|paramo)|edema|hipotermia|congelamiento)`,
    ),
  },
  {
    name: 'altitude',
    re: rx(
      `(?:tose|tosiendo|escupe|escupiendo|bota|botando|sale)${G(3)} (?:espuma|sangre)|espuma rosad[oa]`,
    ),
  },
  {
    name: 'altitude',
    re: rx(
      '(?:me|le|nos|les) (?:falta|cuesta) (?:el aire|respirar|mucho respirar)|(?:me|nos|se) (?:estoy |estamos |esta )?ahogando',
    ),
  },
  {
    name: 'altitude',
    re: rx(
      '(?:estoy|esta|estamos|estan|anda|ando|sigue|siguen|lo veo|la veo|se ve|se puso) (?:muy |super |bastante |demasiado )?(?:confundid|desorientad)[oa]s?(?! (?:con|sobre|por|de|en) )',
    ),
  },
  {
    name: 'altitude',
    re: rx(
      '(?:se|esta|estoy) (?:tambalea|tambaleando)|no sabe (?:donde esta|quien es|donde estamos)|habla (?:raro|incoherente|enredado|arrastrado)',
    ),
  },
  {
    name: 'altitude',
    re: rx(
      '(?:estoy|esta|estamos|estan|sigue|siguen|no para de|no paro de|no deja de) (?:vomitando|vomitar|trasbocando|trasbocar|devolviendo)|vomit(?:a|o) (?:mucho|sangre|sin parar)',
    ),
  },
  {
    name: 'altitude',
    weak: true,
    re: rx(
      `(?:me|le|nos) duele (?:mucho|muchisimo|demasiado|horrible|terrible|durisimo|full|severo|fuertisimo)${G(1)} la cabeza`,
    ),
  },
  {
    name: 'diagnosis',
    re: rx(
      `creo que${G(3)} (?:tiene|tengo|tenemos|le dio|le esta dando|me dio|es|esta con) (?:una |un |el )?(?:hipotermia|soroche|mal de altura|edema|fractura|congelamiento|infarto|hemorragia|esguince)`,
    ),
  },
  {
    name: 'diagnosis',
    weak: true,
    re: rx(
      '(?:tengo|tiene|tenemos|tienen|esta con|estoy con) (?:una |un |el |los )?(?:hipotermia|soroche|mal de (?:altura|montana|paramo)|edema|congelamiento|fractura|esguince|sintomas de (?:hipotermia|soroche|mal de altura|edema|congelamiento))',
    ),
  },

  // Hypothermia and frostbite.
  {
    name: 'hypothermia',
    re: rx(
      '(?:estoy|esta|estamos|estan|sigue|siguen|no para de|no paro de|no paramos de|no deja de|no dejo de|no puede parar de) (?:temblando|temblar|tiritando|tiritar)',
    ),
  },
  {
    name: 'hypothermia',
    re: rx(
      `(?:dedos|manos|pies|orejas|nariz|labios)${G(2)} (?:morad|negr|azul|insensibl|congelad|entumid)\\w*`,
    ),
  },
  {
    name: 'hypothermia',
    re: rx(
      `no (?:siento|sentimos|siente|sienten)${G(1)} ${DET}(?:dedos|pies|manos|piernas|brazos|cara|orejas|nariz)`,
    ),
  },
  {
    name: 'hypothermia',
    weak: true,
    re: rx(
      '(?:me|nos|se) (?:estoy |estamos |esta |estan )?congelando|(?:estoy|estamos|esta) (?:congelad|entumid)[oa]s?',
    ),
  },

  // Lost person, missing child, separated from the group.
  {
    name: 'lost',
    re: rx(
      '(?:me|nos) (?:perdi|perdimos|extravie|extraviamos|desoriente|desorientamos)(?! (?:el|la|los|las|un|una|mi) (?:bus|buseta|reserva|cita|tour|vuelo|entrada|turno|clase|partido|carro))',
    ),
  },
  {
    name: 'lost',
    re: rx(
      '(?:estoy|estamos|esta|estan|andamos|ando|anda|quedamos|quede|quedo|seguimos|sigo) (?:medio |totalmente |completamente |re |muy |como )?(?:perdid|extraviad|desorientad)[oa]s?(?! con )',
    ),
  },
  {
    name: 'lost',
    re: rx(
      `${PERSON}${G(2)} se (?:nos |me |le )?(?:perdio|extravio|desaparecio|perdieron|desaparecieron|alejo|separo)`,
    ),
  },
  {
    name: 'lost',
    re: rx(
      `se (?:nos |me |le )?(?:perdio|extravio|desaparecio) ${DET}${PERSON}|perdimos a ${DET}${PERSON}|perdi a ${DET}${PERSON}`,
    ),
  },
  {
    name: 'lost',
    re: rx(
      `no (?:encuentro|encontramos|encuentra|encuentran|hallo|hallamos|vemos|veo) (?:a )?${DET}${PERSON}|${PERSON} no (?:aparece|aparecen|ha aparecido|contesta|responde)`,
    ),
  },
  {
    name: 'lost',
    re: rx(
      `no (?:encuentro|encontramos|vemos|veo|hallamos) ${DET}(?:sendero|camino|regreso|salida|ruta|refugio|grupo|carro|guia)(?: de (?:regreso|vuelta))?(?! (?:a|hacia|para|de) )`,
    ),
  },
  {
    name: 'lost',
    re: rx(
      'no (?:se|sabemos|sabe) (?:donde (?:estoy|estamos|esta)|por donde (?:ir|seguir|bajar|salir|volver|regresar)|como (?:volver|regresar|bajar|salir))',
    ),
  },
  {
    name: 'lost',
    re: rx(
      '(?:se|me|nos) (?:separo|separaron|separe|separamos|alejo|alejamos) del (?:grupo|guia|sendero|camino)|desaparecid[oa]s?',
    ),
  },

  // Volcano: ash fall, gas, lahar, eruption or earthquake now.
  {
    name: 'volcano',
    re: rx(
      `(?:esta|estan|empezo a|sigue|siguen|nos esta|nos)? ?(?:cayendo|lloviendo|cayo|callo|cae encima|bajando)${G(2)} (?:ceniza|cenisa|seniza|piedras?|material volcanico)`,
    ),
  },
  {
    name: 'volcano',
    re: rx(
      '(?:me|nos|le|les) (?:arden|arde|pican|pica|lloran|quema|queman) (?:mucho |muchisimo )?(?:los ojos|la garganta|la nariz|el pecho)',
    ),
  },
  {
    name: 'volcano',
    weak: true,
    re: rx(`(?:huele|olor|hay olor|tufo)${G(3)} (?:azufre|huevo podrido|gas)`),
  },
  {
    name: 'volcano',
    re: rx(
      '(?:baja|bajan|bajando|viene|vienen|viniendo|se viene|se vino) (?:un |una |mucho |mucha )?(?:lodo|barro|lahar|avalancha|alud|creciente|corriente de lodo|piedras)|' +
        '(?:el rio|la quebrada) (?:esta )?(?:creciendo|crecio|se crecio|se esta creciendo|subio|sube)|' +
        `ruido (?:muy |super |bien )?(?:fuerte|raro|extrano)${G(3)} (?:rio|quebrada|montana|volcan|nevado)`,
    ),
  },
  {
    name: 'volcano',
    re: rx(
      '(?:esta|estan) (?:haciendo erupcion|erupcionando|en erupcion|explotando)|(?:acaba de|empezo a) (?:hacer erupcion|erupcionar|explotar)|' +
        '(?:el volcan|el nevado|el ruiz|el crater) (?:exploto|esta explotando|esta botando|boto|esta echando|hizo erupcion hoy)|' +
        '(?:esta|estan) (?:temblando|temblado) (?:la tierra|el piso|duro|fuerte|muy)|(?:hubo |hay |esta haciendo )?un (?:temblor|terremoto|sismo) (?:fuerte|duro|ahora|horrible)',
    ),
  },

  // Injury: falls, fractures, sprains, head trauma, bleeding.
  {
    name: 'fall',
    re: rx('(?:me|nos) (?:cai|caimos|resbale|resbalamos|rode|rodamos|desbarranque)(?! en cuenta)'),
  },
  {
    name: 'fall',
    re: rx(
      `${PERSON}${G(2)} se (?:cayo|callo|resbalo|rodo|desbarranco|fue de cara)|se (?:cayo|callo|resbalo|rodo|desbarranco) (?:de|por|en|a|al|contra|desde|y|feo|duro|muy|encima)`,
    ),
  },
  {
    name: 'fall',
    re: rx(
      'se (?:fue|cayo|callo|rodo) (?:al|por el|por un|a un|por la|a la|a una|por una) (?:abismo|barranco|precipicio|rio|hueco|voladero|quebrada|laguna|canada|ladera|grieta)',
    ),
  },
  {
    name: 'fracture',
    re: rx(
      '(?:me|se|le|nos) (?:fracture|fracturo|rompi|rompio|parti|partio|quebre|quebro|torci|torcio|doble|doblo|disloque|disloco|zafe|zafo|safe|safo|luxe|luxo|' +
        `lastime|lastimo|aporree|aporreo|jodi|jodio|tronche|troncho|reviente|revento|esguince)${G(2)} ${DET}${BODY}`,
    ),
  },
  {
    name: 'fracture',
    re: rx(
      `hueso (?:expuesto|salido|afuera|por fuera)|se le (?:salio|ve) el hueso|fracturad[oa]s?|${BODY} (?:rot[oa]s?|partid[oa]s?|quebrad[oa]s?|torcid[oa]s?|dislocad[oa]s?)`,
    ),
  },
  {
    name: 'head_injury',
    re: rx(
      `(?:se|me|le|nos) (?:golpeo|golpee|pego|pegue|dio|di|aporreo|aporree|rajo|raje|abrio|partio|revento)${G(3)} (?:la )?cabeza|golpe${G(2)} (?:en|de) la cabeza|(?:se|me) (?:descalabro|descalabre|esnuco|esnuque)`,
    ),
  },
  {
    name: 'cant_move',
    weak: true,
    re: rx(
      'no (?:puedo|puede|podemos|pueden|logra|logro) (?:caminar|moverme|moverse|movernos|mover (?:la|el|las|los|mi|su)|pararme|pararse|levantarme|levantarse|apoyar|pisar|seguir)' +
        '(?! (?:mucho|tanto|lejos|largo|largas|distancias|rapido|mas de|tan|por mucho|tantas|todo el dia|bien por))',
    ),
    unless: rx(
      'sendero(?:s)? (?:corto|cortos|facil|faciles|accesible|accesibles|suave)|accesib\\w*|silla de ruedas|movilidad reducida|discapacidad|caminata (?:corta|suave|facil)',
    ),
  },
  {
    name: 'bleeding',
    re: rx(
      '(?:estoy|esta|estamos|sigue|siguen) sangrando|sangr(?:a|ando|o)(?: la herida| harto)? (?:mucho|muchisimo|demasiado|harto|full|sin parar|a chorros|bastante|un monton)|mucha sangre|sangre a chorros|' +
        'no (?:para|deja|paramos|dejamos|puedo parar|podemos parar) de sangrar|(?:se|me|nos) (?:esta |estoy |estamos )?desangr\\w*|' +
        '(?:sale|saliendo|bota|botando|echando|pierde|perdiendo) (?:mucha |harta |demasiada )?sangre',
    ),
  },
  {
    name: 'bleeding',
    weak: true,
    re: rx(
      'hemorragia|herida (?:muy )?(?:profunda|grande|abierta|fea)|(?:tiene|tengo) (?:una )?(?:cortada|herida|corte) (?:profunda|grande|fea|abierta)',
    ),
  },
  {
    name: 'bleeding',
    re: rx(
      `(?:se|me|le) (?:corto|corte|rajo|raje|abrio|abri)${G(2)} (?:feo|profundo|duro|con (?:un|una|el|la) (?:machete|cuchillo|navaja|vidrio|piedra|hacha))`,
    ),
  },

  // Fire and burns.
  {
    name: 'fire',
    re: rx(
      '(?:se|se esta|esta|estan) (?:quemando|incendiando|prendiendo) (?:el|la|los|las) (?:monte|pasto|paramo|frailejon\\w*|carpa|bosque|vegetacion|cabana|refugio|carro|matorral)|' +
        'se (?:esta )?(?:quemando|incendiando)$|se prendio (?:el|la|un|una|fuego|candela)|(?:esta|estan) (?:en llamas|ardiendo)|' +
        'llamas (?:cerca|alrededor|encima)|humo (?:cerca|denso|negro|encima)|incendio (?:cerca|aqui|aca|ahora)',
    ),
  },
  {
    name: 'fire',
    weak: true,
    re: rx('h?ay (?:un |mucho )?(?:fuego|incendio|candela|llamas)'),
  },
  {
    name: 'burn',
    re: rx(
      '(?:me|se|le|nos) (?:queme|quemo|quemamos|escalde|escaldo|escaldamos)|(?:me|se|le) (?:cayo|callo|eche|echo|rego) (?:el |la )?(?:agua hirviendo|agua caliente|aceite|sopa hirviendo)',
    ),
  },
  {
    name: 'burn',
    weak: true,
    re: rx(
      'quemadura (?:grave|fuerte|grande|seria|de segundo|de tercer)|(?:tiene|tengo) (?:una )?quemadura',
    ),
  },

  // Lightning and storms in the open.
  {
    name: 'lightning',
    re: rx(
      '(?:le|nos|les|me|se) (?:cayo|callo|pego|dio|alcanzo|toco) (?:un )?(?:rayo|centella)|cayo un rayo|rayo (?:cayo|callo|nos cayo|le cayo|pego|nos pego)|(?:golpead|alcanzad|impactad)[oa]s? por un rayo',
    ),
  },
  {
    name: 'lightning',
    re: rx(
      `(?:estamos|estoy|quedamos|nos quedamos)${G(5)} sin (?:refugio|techo|donde (?:resguardarnos|protegernos|meternos|escondernos))|se (?:nos |me )?(?:eriza|erizo|para|paro) el pelo`,
    ),
  },
  {
    name: 'lightning',
    weak: true,
    re: rx(
      `(?:estamos|estoy|nos agarro|nos cogio|nos pillo|nos sorprendio|nos encontro|nos cayo|en medio de|hay)${G(2)} (?:una |la |plena |pleno |medio de |una gran )?(?:tormenta|tempestad|rayos|relampagos|truenos|granizada)|` +
        '(?:rayos|relampagos|truenos|tormenta) (?:muy )?(?:cerca|encima|alrededor|sobre nosotros|aqui)',
    ),
  },

  // Accidents and animal attacks.
  {
    name: 'accident',
    re: rx(
      '(?:tuvimos|tuve|tuvo|tuvieron|hubo|acaba de haber|acabamos de tener) un (?:accidente|choque|volcamiento)',
    ),
  },
  { name: 'accident', weak: true, re: rx('h?ay un (?:accidente|choque)') },
  {
    name: 'accident',
    re: rx(
      '(?:nos|se|me) (?:volcamos|volco|voltio|voltiamos|estrellamos|estrello|chocamos|choco|accidentamos|accidento|desbarrancamos|desbarranco)|' +
        '(?:lo|la|los|me|nos|le) (?:atropello|atropellaron|arrollo|arrollaron)|(?:salimos|se salio|nos salimos) de la via',
    ),
  },
  {
    name: 'animal',
    re: rx(
      '(?:nos|me|le|lo|la|les) (?:ataco|mordio|pico|embistio|esta persiguiendo|esta atacando) (?:un|una|el|la)',
    ),
  },
  {
    name: 'allergy',
    re: rx(
      '(?:reaccion alergica|alergia) (?:muy )?(?:fuerte|grave|severa)|se (?:le|me) (?:cerro|esta cerrando|hincho|esta hinchando) (?:la garganta|la cara|los ojos)',
    ),
  },
];

// Hypothetical or informational framing; disables weak rules only. "qué hago" alone is panic, not a
// hypothesis, so the frame needs "si"/"cuando"/"en caso".
const HYPOTHETICAL = rx(
  '(?:que|q|ke) (?:hago|hacer|hacemos|hace uno|debo hacer|debemos hacer|se hace|se debe hacer|pasa|ocurre|sucede|hay que hacer) (?:si|cuando|en caso)|' +
    'en caso de|por si|(?:^|como|que) si (?:alguien|uno|una persona|hay|me|nos|le|les|te|llega|llegara|un|una|mi|tu|algun|alguna)|' +
    'como (?:se )?(?:previene|prevenir|prevengo|evita|evitar|evito|reconoce|reconocer|reconozco|identifica|identificar|detecta|detectar|trata|tratar|actua|actuar|actuo|reporta|reportar|detiene|detener|controla|controlar|cura|curar)|' +
    '(?:que|cuales) (?:es|son|significa|significan|tan|sintomas|senales|signos|riesgos|causas)|(?:son|es) (?:peligros\\w*|normal|comun|frecuente|posible|verdad|cierto)|' +
    '(?:hay|existe|existen) (?:riesgo|peligro|probabilidad|posibilidad)|(?:se puede|se pueden|puedo|podemos|esta permitido|dejan|permiten) (?:hacer )?(?:fuego|fogata|candela)',
);

// --- live status -------------------------------------------------------------------------------

const ANCHOR =
  '(?:hoy|ahora|ahorita|ahoritica|ahora mismo|en este momento|en estos momentos|en el momento|actualmente|' +
  'esta (?:manana|tarde|noche)|este (?:fin de semana|finde|puente)|en estos dias|estos dias)';
const STATUS =
  '(?:abiert|cerrad|habilitad|ha[bv]ilitad|deshabilitad|bloquead|transitable|pasable|cierre|cierra|cerraron|abren|abre|abrieron|reabri|' +
  'funcionando|operando|atendiendo|alerta|clima|lluvia|llov|nevando|nieve|granizo|niebla|neblina|vias?|carretera|acceso|ingreso|' +
  'volcan|actividad|erupcion|ceniza|estado|cupos?|disponib|restriccion|pico y placa|derrumbe|' +
  '(?:se puede|puedo|podemos|dejan|permiten) (?:subir|entrar|ir|ingresar|pasar|visitar))';
// Schedule or audience qualifiers mark a static question ("¿abierto los lunes?", "¿a qué hora?").
const STATIC = rx(
  'los (?:lunes|martes|miercoles|jueves|viernes|sabados|domingos|fines de semana|festivos|feriados|puentes)|' +
    '(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo)s? (?:a|y|hasta)|fines de semana|festivos|todos los dias|todo el ano|' +
    'a que hora|que hora|horarios?|de [0-9]|desde las|hasta las|a las [0-9]|' +
    'para (?:turistas|visitantes|el publico|publico|ninos|menores|extranjeros|todos|nacionales|acampar)|al publico|' +
    'en (?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre|temporada|vacaciones|semana santa|navidad|ano nuevo|verano|invierno|epoca)|' +
    'normalmente|siempre|en general|cada (?:dia|ano|semana|mes)|durante|usualmente|por lo general|que dias|cuales dias|que meses|que temporada|permanentemente|todo el tiempo',
);

const LIVE_RULES: (Rule & { staticSuppresses?: boolean })[] = [
  {
    name: 'anchor',
    re: new RegExp(`\\b${ANCHOR}\\b.{0,60}\\b${STATUS}|\\b${STATUS}\\w*.{0,60}\\b${ANCHOR}\\b`),
  },
  {
    name: 'ya',
    re: rx(
      'ya (?:abrieron|reabrieron|abrio|reabrio|cerraron|cerro|habilitaron|habilito|deshabilitaron|levantaron (?:la|el)|quitaron (?:la|el))|' +
        'ya (?:e?stan?|sigue|siguen) (?:abiert|cerrad|habilitad|ha[bv]ilitad|bloquead|transitable|funcionando|operando|disponible)\\w*|' +
        'ya (?:se puede|puedo|podemos|dejan) (?:subir|entrar|ir|ingresar|pasar|visitar)',
    ),
  },
  {
    name: 'state',
    staticSuppresses: true,
    re: rx(
      '(?:e?stan?|ta|sigue|siguen|continua|continuan|quedo|quedaron) (?:abiert|cerrad|[cs]errad|habilitad|ha[bv]ilitad|deshabilitad|bloquead|clausurad|' +
        'suspendid|restringid|transitable|pasable|en alerta|funcionando|operando|activ)\\w*',
    ),
  },
  {
    name: 'phrase',
    staticSuppresses: true,
    re: rx(
      '(?:como|que tal) (?:esta|estan|sta|anda|va|amanecio) (?:el|la|los|las) (?:vias?|carretera|camino|clima|tiempo|volcan|nevado|ruiz|paramo|acceso|ingreso|sendero|nivel|alerta|actividad|situacion)|' +
        'estado (?:actual|de hoy|de la via|de las vias|de la carretera|del volcan|del clima|del sendero|del acceso|del nevado|del ruiz)',
    ),
  },
  {
    name: 'phrase',
    re: rx(
      'alerta (?:actual|vigente|de hoy|activa)|nivel de alerta (?:actual|vigente|de hoy)|(?:en que|que|cual es el) (?:alerta|nivel)(?: de alerta)? (?:esta|tiene|hay|va|es el actual)|' +
        'ultim[oa] (?:alerta|boletin|reporte|informe|actualizacion|comunicado)|(?:clima|pronostico|tiempo|temperatura) (?:de|para|para el dia de) (?:hoy|manana|esta semana|este fin)|' +
        '(?:esta|estan|sta) (?:lloviendo|nevando|granizando|haciendo (?:frio|sol|calor)|despejado|nublado|con niebla)|' +
        '(?:hay|habra) (?:cierres?|derrumbes?|bloqueos?|paro|trancon|cupos?|restricciones|restriccion) (?:hoy|ahora|en este momento|ahorita|en la via|en la carretera|en el ingreso)|' +
        '(?:sigue|siguen|continua) (?:la |el )?(?:alerta|cierre|restriccion|bloqueo|actividad)|reabrieron|reabrio|hay paro|' +
        '(?:estan|siguen|sigue|esta) dejando (?:subir|entrar|pasar|ingresar)',
    ),
  },
];

export function detectSafety(text: string): SafetyResult {
  const q = foldText(text);
  const matched: string[] = [];
  if (!q) return { urgent: false, liveStatus: false, matched };

  const hypothetical = HYPOTHETICAL.test(q);
  for (const r of EMERGENCY_RULES) {
    if (r.weak && hypothetical) continue;
    if (r.unless && r.unless.test(q)) continue;
    if (r.re.test(q)) {
      const name = `emergency:${r.name}`;
      if (!matched.includes(name)) matched.push(name);
    }
  }
  const urgent = matched.length > 0;

  const isStatic = STATIC.test(q);
  let liveStatus = false;
  for (const r of LIVE_RULES) {
    if (r.staticSuppresses && isStatic) continue;
    if (r.re.test(q)) {
      liveStatus = true;
      const name = `live:${r.name}`;
      if (!matched.includes(name)) matched.push(name);
    }
  }
  return { urgent, liveStatus, matched };
}
