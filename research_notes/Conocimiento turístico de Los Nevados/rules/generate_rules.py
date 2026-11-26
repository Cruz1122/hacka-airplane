"""Build data/knowledge/sections/rules.json from the reviewed entries below.

Single source of truth for section `rules`. Every claim is backed by a verbatim quote in
rules/evidence/quotes.md (checked by rules/check_quotes.py).

Excluded on purpose (owned by other sections or without verified text):
- bathing in lagoons, tourist horseback, human waste on the trail, bicycles, motorcycles and parking
  (activities, preparation, access); age, guides and insurance (booking_fees); the 15-day
  mountaineering headline (activities.sport_mountaineering); staying with the group (health_safety);
  tent specs and camp stoves (preparation); vehicle routes and parking (access, hours_status).
- burying trash is folded into `leave_no_waste`; production lights into `audiovisual_permits`.
- smoking, speed limits, assistance dogs: no verified text in the sources read on 2026-11-21.
- `rules.no_hunting`: injected by coordination/coordinator_fixes.py, do not add it here.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research_notes/Conocimiento turístico de Los Nevados"
OUT = ROOT / "data/knowledge/sections/rules.json"
TODAY = "2026-11-21"

RES207 = {
    "label": "Parques Nacionales Naturales de Colombia · Resolución 207 de 2023 (reglamentación PNN Los Nevados)",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf",
    "retrieved_at": TODAY,
}
DEC = {
    "label": "Función Pública · Decreto 1076 de 2015, arts. 2.2.2.1.15.1, 2.2.2.1.15.2 y 2.2.2.1.16",
    "url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=78153",
    "retrieved_at": TODAY,
}
PNN = {
    "label": "Parques Nacionales Naturales de Colombia · Ficha oficial PNN Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": TODAY,
}
FAQ = {
    "label": "Parques Nacionales Naturales de Colombia · Preguntas frecuentes (pregunta 29)",
    "url": "https://www.parquesnacionales.gov.co/atencion-al-ciudadano/",
    "retrieved_at": TODAY,
}
LEY2387 = {
    "label": "Cancillería · Ley 2387 de 2024 (modifica el procedimiento sancionatorio ambiental)",
    "url": "https://cancilleria.gov.co/sites/default/files/Normograma/docs/ley_2387_2024.htm",
    "retrieved_at": TODAY,
}
LEY1333 = {
    "label": "Función Pública · Ley 1333 de 2009 (procedimiento sancionatorio ambiental)",
    "url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=36879",
    "retrieved_at": TODAY,
}
CARTA2026 = {
    "label": "Parques Nacionales Naturales de Colombia · Respuesta oficial Radicado 20266200003411 del 11 de mayo de 2026",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf",
    "retrieved_at": TODAY,
}
POE2026 = {
    "label": "Parques Nacionales Naturales de Colombia · Plan de Ordenamiento Ecoturístico PNN Los Nevados 2026-2030 (versión corta)",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
    "retrieved_at": TODAY,
}


def E(eid, label, examples, short, variants, sources, related, tags):
    return {
        "id": "rules." + eid,
        "label": label,
        "kind": "rule",
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": [],  # filled by build() from other entries (always real examples)
        "entities": {},
        "needs": [],
        "answer": {"short": short, "variants": variants},
        "sources": sources,
        "related": ["rules." + r for r in related],
        "tags": tags,
    }


entries = [
    # ---- existing entries kept and corrected ------------------------------------------------
    E("pets", "ingreso de mascotas", [
        "puedo llevar a mi perro", "dejan entrar mascotas al parque", "mascotas",
        "voy con mi gato, ¿puede entrar?", "se permite llevar un perrito a Los Nevados",
        "toca dejar al perro en casa?", "puedo subir con mi mascota", "¿reciben animales domésticos en Brisas?",
        "llevar perro al nevado", "mi perra puede acompañarme en el recorrido",
        "can I bring my dog to the park?", "dejan pasar mascotas o no",
        "se puede entrar con animales de compañía", "voy con el firulais, ¿lo dejan pasar?",
    ], "No puedes ingresar con mascotas al Parque Nacional Natural Los Nevados: el reglamento lo prohíbe. Antes de viajar, organiza quién la cuide durante tu visita.",
        ["Parques Nacionales indica que no está permitido el ingreso de mascotas a sus áreas protegidas; busca con anticipación quién pueda cuidarla mientras visitas Los Nevados."],
        [RES207, FAQ], ["stay_on_routes", "leave_no_waste"], ["mascotas", "perros", "animales domésticos"]),

    E("stay_on_routes", "permanecer en recorridos habilitados", [
        "puedo caminar por donde quiera", "me salgo del sendero para tomar fotos?", "hay que seguir el camino marcado",
        "puedo cortar camino por el páramo", "se puede explorar fuera de la ruta", "toca quedarse en el sendero habilitado",
        "quiero acercarme por fuera al glaciar", "¿está bien salirse de la ruta para ver mejor?",
        "puedo andar libre por el parque", "por dónde sí puedo caminar", "can I leave the marked trail?",
        "¿puedo abrir un atajo por el monte?", "me meto un poquito fuera del camino para una foto",
        "hay zonas donde no debo pasar",
    ], "Quédate en los senderos autorizados. El reglamento solo permite los senderos del mapa oficial, y tomar rutas alternas está prohibido. Recorre el sendero a pie y sin salirte de él.",
        ["Si te sales del sendero o tomas un atajo, incumples el reglamento. Si tienes dudas sobre la ruta permitida, pregunta al personal del parque antes de salir."],
        [RES207], ["leave_no_waste", "leave_natural_objects"], ["senderos", "rutas autorizadas", "cuidado del páramo"]),

    E("leave_no_waste", "manejo de residuos", [
        "dónde boto la basura", "me llevo los empaques de vuelta?", "qué hago con mis residuos en el recorrido",
        "puedo dejar la cáscara ahí", "basura en el parque", "toca cargar la basura hasta la salida",
        "dónde hay canecas en el páramo", "¿dejo la botella al lado del camino?", "qué hago con el papelito del snack",
        "qué hago con la basura que produzco en la caminata", "should I pack out my trash?", "no encuentro caneca, ¿qué hago?",
        "los residuos orgánicos también me los llevo?", "dónde dejo el empaque del almuerzo",
    ], "Llévate tus residuos de regreso: no los dejes, no los entierres ni los escondas bajo rocas. Guarda envoltorios, pilas y bolsas en el morral hasta salir.",
        ["Cada visitante debe retomar sus propios residuos y basuras al lugar de origen. No dejes nada en el sendero, ni siquiera cáscaras o envoltorios."],
        [RES207], ["stay_on_routes", "leave_natural_objects"], ["basura", "residuos", "no dejar rastro"]),

    E("leave_natural_objects", "no retirar elementos naturales", [
        "puedo arrancar un frailejón", "me puedo llevar una piedra de recuerdo", "está bien recoger flores del páramo",
        "puedo sacar una planta para mi casa", "se permite llevarse rocas del sendero", "quiero guardar una flor que encontré",
        "puedo recoger semillas en el parque", "me llevo un pedacito de musgo?", "puedo coger una planta sin dañarla",
        "se pueden coleccionar piedras de Los Nevados", "can I take a flower home?", "no pasa nada si recojo una piedrita?",
        "puedo arrancar una ramita como recuerdo", "es permitido recolectar plantas para mí",
    ], "No te lleves plantas, rocas ni otros elementos naturales. El reglamento prohíbe extraer material del suelo, vegetal, fauna o rocas. Fotografíalos sin retirarlos.",
        ["Recolectar flora o extraer rocas y animales está prohibido; la única excepción es la colecta autorizada con fines científicos o de investigación."],
        [RES207, DEC], ["leave_no_waste", "research_permissions"], ["plantas", "rocas", "recolección", "frailejón"]),

    E("no_introduce_species", "no traer animales, semillas ni plantas", [
        "puedo soltar peces en una laguna", "llevo semillas de afuera para sembrar?", "se permite traer plantas para plantar",
        "puedo liberar un conejo en el parque", "introducir especies al páramo", "está bien dejar renacuajos en una charca",
        "puedo traer flores de otro lugar para el páramo", "quiero llevar peces a la laguna",
        "se pueden llevar animales para soltarlos", "¿puedo repoblar una zona con plantas?",
        "may I release a pet fish in the lake?", "puedo dejar unas semillas por el camino",
        "puedo traer un arbolito de la casa para plantarlo", "llevar una especie de otra región al parque",
    ], "No traigas ni sueltes animales, semillas, flores ni propágulos en el parque, de ninguna especie. El reglamento lo prohíbe, sea de forma transitoria o permanente.",
        ["Introducir animales o material vegetal en el parque está prohibido, aunque sea transitorio. Antes de cualquier siembra o liberación, consulta con Parques Nacionales."],
        [RES207, DEC], ["leave_natural_objects", "avoid_pollutants"], ["especies", "semillas", "liberar animales"]),

    E("avoid_pollutants", "no contaminar el entorno", [
        "puedo botar aceite en el suelo", "dónde vacío el agua jabonosa", "se puede echar detergente a la quebrada",
        "qué hago con el combustible que sobró", "puedo tirar pintura en un hueco", "está bien dejar químicos en la laguna",
        "dónde descarto una sustancia contaminante", "verter residuos al agua del parque", "puedo lavar cosas en la quebrada",
        "¿puedo botar una pila usada en el páramo?", "can I dump soap water in the stream?", "dónde boto aceite de cocina acá",
        "puedo dejar un envase con químico", "se permite descargar aguas sucias al río",
    ], "No viertas ni dejes sustancias contaminantes o tóxicas en el suelo, el agua o el aire. Si llevas un producto que pueda derramarse, ciérralo y sácalo contigo.",
        ["Utilizar sustancias contaminantes o productos químicos en grandes cantidades que puedan causar derrames está prohibido en el parque; consérvalos cerrados y retíralos contigo."],
        [RES207, DEC], ["avoid_chemicals", "leave_no_waste"], ["contaminación", "químicos", "quebradas", "residuos peligrosos"]),

    E("avoid_chemicals", "uso de químicos y explosivos", [
        "puedo usar pólvora en el parque", "se permiten explosivos para una actividad", "puedo fumigar una planta",
        "llevo pesticida para los mosquitos?", "está permitido usar químicos en el páramo", "puedo prender un artefacto pirotécnico",
        "usar explosivos en Los Nevados", "¿puedo aplicar herbicida en un campamento?", "se pueden llevar químicos para una demostración",
        "puedo hacer una detonación pequeña", "are fireworks allowed in the park?", "sirve llevar insecticida para rociar el área",
        "puedo usar fertilizante en el recorrido", "qué regla hay sobre sustancias químicas",
    ], "No lleves ni uses pólvora, juegos pirotécnicos, explosivos ni productos químicos de efectos residuales. Solo una obra autorizada puede usar explosivos. Si es tu caso, confírmalo con el parque.",
        ["El reglamento prohíbe llevar y usar juegos pirotécnicos y sustancias explosivas, y usar productos químicos de efectos residuales. Consulta con el parque si tienes una actividad autorizada."],
        [DEC, RES207], ["avoid_pollutants", "open_fires"], ["químicos", "explosivos", "pólvora", "pesticidas"]),

    E("commercial_photography", "fotografía con fines comerciales", [
        "puedo hacer fotos para una marca", "necesito permiso para una sesión paga", "voy a fotografiar para publicidad",
        "puedo grabar un catálogo en el parque", "fotografía comercial en Los Nevados", "cómo pido autorización para fotos profesionales",
        "puedo hacer una sesión de producto en Brisas", "se permiten fotos de stock con fines comerciales",
        "voy a cobrar por las imágenes, ¿debo avisar?", "permiso para fotos con patrocinador", "can I shoot a commercial photo campaign?",
        "puedo hacer fotos para venderlas después", "tengo una producción fotográfica, qué permiso necesito",
        "una sesión para una empresa requiere autorización",
    ], "Las fotos con fines comerciales o publicitarios necesitan autorización previa de Parques Nacionales. Las fotos y videos aficionados sí están permitidos en el parque.",
        ["Para uso comercial, consulta el trámite de permisos y licencias con Parques Nacionales antes de tomar las imágenes. La foto de turista no requiere ese trámite."],
        [PNN, RES207, DEC], ["audiovisual_permits", "sell_advertise"], ["fotografía comercial", "permisos", "producción"]),

    E("audiovisual_permits", "filmación y tomas audiovisuales", [
        "puedo grabar un documental", "permiso para filmar en el parque", "voy a hacer un video comercial en el páramo",
        "cómo autorizan una producción audiovisual", "se puede grabar con equipo profesional", "necesito permiso para rodar una película",
        "tomas audiovisuales en Los Nevados", "quiero filmar un anuncio en la montaña", "puedo grabar para una serie",
        "dónde se solicita permiso de filmación", "how can I get permission to film here?", "voy a grabar un video para una marca, qué hago",
        "se requiere autorización para grabar un documental", "puedo llevar equipo de rodaje al parque",
    ], "Para tomas audiovisuales debes solicitar autorización a Parques Nacionales, y el requisito aplica a todos los sectores del parque. Luces, pantallas, telones o estudios temporales también necesitan permisos.",
        ["Confirma con Parques Nacionales qué autorización corresponde a tu proyecto y sector antes de planear la grabación."],
        [PNN, RES207], ["commercial_photography", "event_permits"], ["filmación", "video", "audiovisual", "autorización"]),

    E("event_permits", "eventos dentro del parque", [
        "puedo organizar un evento en Los Nevados", "permiso para hacer una actividad grupal", "quiero hacer un evento en el páramo",
        "se puede hacer un encuentro de marca", "cómo tramito un evento en el área protegida", "puedo celebrar una reunión en la montaña",
        "evento privado dentro del parque", "necesito autorización para una actividad especial", "se permiten eventos en los senderos",
        "voy a convocar gente al parque, qué permiso pido", "can I host an event in the park?", "puedo hacer una activación de marca en Brisas",
        "organizar una actividad pública en el parque", "dónde consulto el permiso para eventos",
    ], "Para organizar un evento dentro del parque necesitas autorización de Parques Nacionales, en todos los sectores. Las reuniones no autorizadas por el parque no están permitidas. Pide el trámite antes de convocar a la gente.",
        ["Pide orientación a Parques Nacionales y espera la autorización antes de anunciar o programar el evento."],
        [PNN, DEC], ["audiovisual_permits", "organized_sports"], ["eventos", "permisos", "actividades especiales"]),

    E("organized_sports", "actividades deportivas organizadas", [
        "puedo hacer una carrera en el parque", "permiso para una competencia de montaña", "se puede organizar una carrera de trail",
        "voy a hacer una carrera ciclística en Los Nevados", "autorización para un evento deportivo", "puedo convocar una competencia en el páramo",
        "organizar una caminata deportiva grupal", "se permiten carreras con participantes",
        "necesito permiso para hacer una travesía deportiva organizada", "cómo tramito una actividad deportiva en el parque",
        "can I organize a trail race here?", "puedo montar una competencia en los senderos",
        "actividad deportiva con inscripción, qué autorización necesita", "quiero hacer una prueba deportiva en el parque",
    ], "Las actividades deportivas organizadas, como una carrera, necesitan autorización de Parques Nacionales; el montañismo de clubes sigue la Resolución 474 de 2018. Pide el permiso antes de convocar.",
        ["Consulta el trámite y las condiciones con Parques Nacionales antes de convocar participantes a una actividad deportiva."],
        [PNN, RES207], ["event_permits", "audiovisual_permits"], ["deportes", "competencias", "autorización"]),

    E("research_permissions", "investigación y recolección científica", [
        "puedo hacer una investigación en Los Nevados", "permiso para tomar muestras científicas", "voy a recolectar plantas para un estudio",
        "cómo solicitar permiso de investigación", "se puede hacer trabajo de campo en el parque", "autorización para estudiar aves en el área",
        "necesito ingresar para una tesis", "puedo recolectar muestras de agua para un proyecto", "qué trámite hay para una investigación ambiental",
        "permiso científico PNN Los Nevados", "how do I apply for a research permit?", "voy a muestrear insectos, qué autorización necesito",
        "puedo hacer investigación universitaria sin permiso", "se requiere permiso para investigación biológica",
    ], "Los proyectos de investigación o académicos necesitan permiso previo de Parques Nacionales, y la colecta de especímenes solo se permite con fines científicos autorizados. Confirma qué permiso aplica a tu proyecto.",
        ["La ficha del parque pide autorización para las actividades de investigación; consulta con Parques Nacionales el trámite que corresponde antes de ingresar o recolectar muestras."],
        [RES207, DEC, PNN], ["leave_natural_objects", "fishing"], ["investigación", "permisos", "recolección científica"]),

    E("drones", "uso de drones", [
        "se puede volar dron en Los Nevados", "puedo usar mi drone para unas fotos", "dejan entrar drones al parque",
        "dron recreativo en Brisas", "quiero grabar desde el aire, está permitido?", "se puede volar un cuadricóptero en el páramo",
        "toca pedir permiso para volar dron?", "puedo sacar el dron un momento", "qué norma hay para drones en el parque",
        "are drones allowed in the park?", "puedo hacer tomas aéreas con drone", "dejan usar dron para un video familiar",
    ], "El reglamento prohíbe utilizar drones en el parque. Deja el dron guardado durante toda la visita.",
        ["No uses el dron en el parque. Si tienes una duda sobre la norma vigente, confirma con Parques Nacionales."],
        [RES207], ["audiovisual_permits", "commercial_photography"], ["drones", "vuelo", "tomas aéreas"]),

    E("open_fires", "fogatas y fuego abierto", [
        "puedo prender una fogata", "se permiten fogatas en el parque", "hacer una fogata para calentar comida",
        "toca llevar leña para cocinar", "puedo encender fuego en el páramo", "nos dejan hacer una fogata pequeña",
        "qué pasa si prendo una fogata en el campamento", "puedo prender una fogata con ramas secas", "fuego abierto en Los Nevados",
        "can we make a campfire here?", "se puede hacer una fogata de noche", "hay alguna regla sobre fuego en el parque",
    ], "No hagas fogatas: el reglamento del parque las prohíbe por el riesgo de incendios forestales. Para cocinar, el reglamento indica llevar camping gas.",
        ["Las fogatas están prohibidas en el parque por riesgo de incendios forestales. Para cocinar, lleva camping gas y consulta con el personal cualquier duda."],
        [RES207, DEC], ["camping", "leave_no_waste"], ["fuego", "fogatas", "incendios"]),
    E("noise", "ruido y equipos de sonido", [
        "puedo poner música con un parlante", "se permiten bafles en el sendero", "puedo llevar un altavoz bluetooth",
        "poner música duro en el parque", "toca caminar en silencio?", "hay regla sobre hacer ruido",
        "puedo usar una bocina para llamar al grupo", "can I play music on a speaker?", "se puede poner música en el campamento",
        "qué pasa si hago mucho ruido", "dejan llevar parlante portátil", "cómo debo comportarme con el ruido en el páramo",
    ], "No produzcas ruidos ni uses parlantes u otros equipos sonoros que perturben el ambiente natural o incomoden a otros visitantes. El reglamento lo prohíbe.",
        ["Usar equipos sonoros que incomoden a los visitantes está prohibido en el parque; confirma cualquier actividad especial con Parques Nacionales."],
        [RES207, DEC], ["playback", "drones"], ["ruido", "parlantes", "equipos de sonido"]),

    E("feed_wildlife", "alimentar fauna silvestre", [
        "puedo darle comida a un venado", "está bien alimentar aves del parque", "puedo dejarle fruta a un animal",
        "cómo atraigo un oso para verlo", "les puedo dar migas a los pájaros", "puedo cebar animales para tomarles fotos",
        "se puede alimentar fauna silvestre", "dejo comida para los animales?", "qué comida les gusta a las aves del páramo",
        "can I feed the wildlife here?", "puedo dejar sal para los venados?", "alimentar animales en Los Nevados",
    ], "No des de comer a la fauna silvestre: el reglamento prohíbe alimentarla para atraerla o capturarla y también suministrar alimentos a los animales. Obsérvala sin ofrecerle nada.",
        ["Dar de comer a los animales silvestres está prohibido en el parque; obsérvalos sin ofrecerles nada."],
        [RES207, DEC], ["playback", "leave_no_waste"], ["alimentación", "fauna", "atraer animales"]),

    E("playback", "audios para atraer aves", [
        "puedo poner cantos de aves en el celular", "se puede usar playback para ver colibríes", "audio para atraer pájaros",
        "reproducir sonidos de aves en el sendero", "cómo hago que se acerquen las aves", "puedo usar un parlante con cantos de aves",
        "playback en Los Nevados", "dejan usar grabaciones para observar fauna", "can I use bird calls to attract birds?",
        "sirve poner cantos para fotografiar pájaros", "usar sonidos de fauna en el páramo", "se permite atraer aves con una grabación",
    ], "No uses playback: el reglamento prohíbe reproducir audios de fauna silvestre con un dispositivo electrónico, incluso para observar aves. Obsérvalas sin audios.",
        ["El reglamento prohíbe el playback durante la observación de aves en el parque; si quieres verlas, espera a que aparezcan sin grabaciones."],
        [RES207], ["feed_wildlife", "noise"], ["playback", "aves", "audios de fauna"]),

    E("camping", "acampar dentro del parque", [
        "puedo montar carpa en cualquier parte", "dónde se puede acampar en Los Nevados", "acampar fuera del sendero está permitido?",
        "puedo dormir en la montaña sin reserva", "camping en zona no autorizada", "se puede pasar la noche en el páramo",
        "dónde consulto si dejan acampar", "puedo armar carpa en un claro que no está marcado?", "can I camp anywhere in the park?",
        "acampar en un sitio que no tiene zona marcada", "puedo hacer vivac donde me coja la noche", "acampar donde no hay zona habilitada está prohibido?",
    ], "No armes la carpa fuera de una zona de camping habilitada: acampar en otro sitio está prohibido. Pregunta al personal del parque cuál zona está abierta para tu fecha.",
        ["El reglamento prohíbe el camping en zonas no permitidas; no montes carpa en otro lugar y confirma la disponibilidad antes de tu visita."],
        [RES207], ["open_fires", "leave_no_waste"], ["camping", "pernocte", "zonas permitidas"]),
    E("fishing", "pesca en el parque", [
        "se puede pescar en la Laguna del Otún", "dejan llevar caña de pescar", "puedo pescar truchas en el parque",
        "pesca recreativa en Los Nevados", "está permitida la pesca deportiva", "puedo lanzar una línea desde la orilla",
        "se puede pescar para comer", "pescar en los ríos del parque", "qué regla hay para la pesca",
        "can I fish in the park?", "puedo usar anzuelo en la laguna", "dejan hacer pesca con devolución",
    ], "No puedes pescar en el parque, salvo un proyecto científico autorizado por la autoridad ambiental. Si es tu caso, pide ese permiso antes de entrar.",
        ["La pesca recreativa está prohibida en el parque; si tu proyecto requiere pescar, pide la autorización a la autoridad ambiental antes de ingresar."],
        [RES207], ["research_permissions", "leave_natural_objects"], ["pesca", "caña", "laguna"]),

    E("intoxication", "alcohol y sustancias psicoactivas", [
        "puedo entrar si estoy borracho", "dejan ingresar después de tomar", "se puede visitar el parque con tragos encima",
        "puedo ir al sendero bajo efectos de drogas", "qué pasa si llego alicorado", "se puede consumir y luego entrar al parque",
        "puedo entrar tomado a Los Nevados", "hay control si uno va borracho", "visitar el parque después de beber",
        "can I enter the park while intoxicated?", "toca estar sobrio para ingresar", "me dejan pasar si estoy enguayabado y aún tomado",
        "puedo tomar una cerveza en la laguna?", "¿puedo llevar una botella de licor cerrada?",
    ], "No puedes ingresar ni consumir alcohol ni sustancias psicoactivas en el parque, y tampoco entrar embriagado o bajo sus efectos. Si ya estás bajo sus efectos, no inicies la visita.",
        ["El reglamento prohíbe entrar en estado de alicoramiento o bajo sustancias psicoactivas, y embriagarse dentro del parque. Espera a estar en condiciones para empezar."],
        [RES207, DEC], ["entry_bag_checks", "weapons"], ["alcohol", "sustancias psicoactivas", "embriaguez"]),

    # ---- new entries (verified in quotes.md) ------------------------------------------------
    E("weapons", "armas y objetos cortopunzantes", [
        "puedo llevar un cuchillo para cortar comida", "se permite llevar armas para protegerse", "puedo entrar con una pistola de defensa?",
        "llevo un machete para abrir camino", "dejan entrar navaja o cuchillo de bolsillo?", "puedo llevar un arma de fuego en el recorrido",
        "puedo cargar un arma con permiso de porte?", "mi hermano va armado, ¿puede entrar?",
        "cuchillo suizo o navaja multiusos, ¿lo puedo llevar?", "is it allowed to bring a knife to the park?",
        "me revisan las armas en el control?", "se puede llevar una escopeta al parque?",
    ], "No puedes ingresar ni usar armas de fuego ni elementos cortopunzantes en el parque. Los controles de ingreso los buscan; déjalos fuera antes de llegar al puesto de control.",
        ["El reglamento prohíbe portar armas de fuego en las áreas del Sistema de Parques Nacionales y el ingreso y uso de armas o elementos cortopunzantes en Los Nevados."],
        [RES207, DEC], ["entry_bag_checks", "intoxication", "preventive_measures"], ["armas", "cortopunzantes", "control de ingreso"]),

    E("entry_bag_checks", "controles de ingreso y salida", [
        "me van a revisar el morral al entrar?", "hay requisa de maletas en el parque", "revisan lo que llevo en los controles?",
        "control de salida, también revisan?", "qué revisan en la caseta de ingreso", "revisan el morral en los puestos de control?",
        "me pueden pedir que abra el bolso?", "they search bags at the entrance?", "revisan si llevo algo prohibido antes de subir",
        "toca mostrar el equipaje en el puesto de control", "en la portería revisan la mochila o no?", "revisan los equipos de pesca en la entrada?",
    ], "Sí, en los controles de ingreso y salida pueden revisar tu equipaje. Buscan sustancias psicoactivas, elementos embriagantes, armas, cortopunzantes y equipos de pesca. Déjalos fuera antes de llegar al control.",
        ["Debes participar en los controles de ingreso y salida. Si encuentran algo prohibido, se implementarán las medidas a las que haya lugar; pregunta al personal qué procede."],
        [RES207], ["weapons", "intoxication", "preventive_measures"], ["control", "requisa", "equipaje"]),
    E("minors_protection", "protección de niños y adolescentes", [
        "turismo sexual con menores está prohibido aquí?", "qué pasa si alguien explota sexualmente a un menor en un tour",
        "la explotación infantil se castiga en Los Nevados?", "hay ley contra la explotación sexual de niños en el parque",
        "¿qué norma protege a los niños del turismo sexual?", "explotación sexual infantil en el turismo, está permitido?",
        "is child sexual exploitation banned in the park?", "si veo a un adulto abusando de un menor, a quién aviso aquí?",
        "¿qué pasa si veo un caso de explotación infantil en el parque?", "dónde denuncio la explotación sexual de menores en el parque?",
        "abuso de menores en un tour, qué hago?", "está penalizado el turismo sexual con niños?",
    ], "No participes en turismo sexual ni en ninguna explotación de niños o adolescentes: es un delito. Si ves un caso, denúncialo de inmediato al personal del parque o a las autoridades.",
        ["Si ves turismo sexual o explotación de un menor, denúncialo al personal del parque o a las autoridades. No te quedes callado."],
        [RES207], ["follow_park_staff", "respect_communities"], ["menores", "explotación sexual", "protección infantil"]),
    E("follow_park_staff", "obedecer al personal del parque", [
        "tengo que hacer caso a los guardaparques?", "y si no quiero seguir las indicaciones del personal?",
        "tengo que obedecer al guía o al ranger?", "debo acatar lo que diga el personal de Parques",
        "do I have to follow the rangers' instructions?", "el guardaparque me pide salir, ¿tengo que irme?",
        "si el personal me dice que me devuelva, ¿qué hago?", "puedo discutir con el ranger si me pide algo?",
        "las recomendaciones del guía son obligatorias?", "qué hago si un funcionario me llama la atención",
        "tengo que seguir al guía en la ruta?", "¿los guías del parque mandan en el recorrido?",
    ], "Sigue las indicaciones de los funcionarios del parque y de los guías autorizados. El personal de vigilancia tiene funciones de control. Cumple lo que te indiquen en el recorrido.",
        ["Si una indicación te parece injusta, consúltala después por los canales oficiales de Parques Nacionales, sin desobedecerla en el momento."],
        [RES207, DEC], ["entry_bag_checks", "sanctions_penalties"], ["personal del parque", "guardaparques", "autoridad"]),
    E("sell_advertise", "vender o hacer publicidad en el parque", [
        "puedo vender agua o snacks en el sendero?", "se puede vender artesanías en Brisas", "puedo repartir volantes de mi negocio",
        "hacer publicidad de mi marca en el parque está permitido?", "vender cosas a los turistas en la laguna",
        "puedo poner un puesto de comida en el páramo", "dejo un aviso publicitario en el camino, ¿sí?",
        "can I sell souvenirs in the park?", "puedo distribuir folletos de mi tienda en las rutas",
        "pongo un stand para vender en Los Nevados?", "poner pancartas de mi empresa en el sendero",
        "puedo vender algo de comer al grupo en la ruta", "vender ropa o gorras a los visitantes, ¿se puede?",
    ], "No puedes vender, comerciar ni distribuir productos en el parque, salvo los que estén autorizados expresamente. Tampoco hagas propaganda no prevista en la regulación. Consulta primero con Parques Nacionales.",
        ["Vender agua, comida o artesanías, repartir folletos o poner avisos publicitarios requiere autorización expresa; sin ella, está prohibido en el parque."],
        [DEC], ["commercial_photography", "event_permits"], ["venta", "comercio", "publicidad", "propaganda"]),

    E("single_use_plastics", "plásticos de un solo uso", [
        "puedo llevar botellas de plástico al parque?", "las bolsas plásticas están prohibidas?",
        "llevo pitillos de plástico para el jugo, pasa?", "se pueden ingresar vasos desechables", "pitillos plásticos prohibidos en el parque?",
        "is it allowed to bring single-use plastic bottles?", "los platos desechables están permitidos?",
        "hay que llevar recipiente reutilizable en vez de plástico?", "cubiertos de plástico para el almuerzo, ¿sí o no?",
        "reemplazo las botellas de plástico por una reutilizable, sirve?", "bolsas de mercado plásticas, ¿entran?",
        "¿puedo llevar un termo en lugar de botellas plásticas?", "is plastic cutlery allowed in the park?",
    ], "No ingreses plásticos de un solo uso al parque: el reglamento los prohíbe por la Resolución 1558 de 2019. Lleva una botella y recipientes reutilizables en su lugar.",
        ["No lleves plásticos de un solo uso. Revisa el morral antes del control y cambia botellas y empaques por algo reutilizable."],
        [RES207], ["leave_no_waste", "avoid_pollutants"], ["plásticos", "un solo uso", "reutilizables"]),
    E("graffiti_signage", "rayar, pintar o mover señales", [
        "puedo escribir mi nombre en una roca del sendero?", "dejar mi firma pintada en un árbol", "se puede pintar un grafiti en la valla?",
        "puedo quitar un letrero que estorba en el camino?", "rayar las piedras con un marcador, ¿hay problema?",
        "me llevo la señal de la ruta de recuerdo", "puedo hacer marcas con pintura en el sendero para no perderme",
        "dejar un mensaje escrito en una piedra del páramo", "is graffiti allowed on the rocks?", "puedo mover la valla que tapa el paso?",
        "escribir con un cuchillo en un árbol del sendero", "puedo dibujar un corazón en una roca con tiza?",
        "qué pasa si rayo una señal del parque",
    ], "No rayes ni pintes rocas, árboles ni estructuras, y no quites ni muevas señales, avisos o vallas. Si una señal está dañada, avísale al personal del parque.",
        ["Causar daño a las instalaciones o remover señalización y vallas en los senderos está prohibido; si una señal está dañada, avisa al personal del parque."],
        [RES207, DEC], ["leave_natural_objects", "stay_on_routes"], ["grafitis", "rayar", "señales", "vallas"]),

    E("respect_communities", "respeto a comunidades y cultura", [
        "tengo que respetar a los campesinos que viven en el parque?", "puedo hacer chistes sobre las costumbres de la gente de la zona?",
        "hay reglas para tratar a las comunidades del parque?", "debemos respetar las tradiciones de los habitantes locales?",
        "los habitantes de la zona tienen costumbres que debo respetar?", "is it required to respect local culture?",
        "cómo debo tratar a los habitantes de la vereda?", "cómo portarse con las familias campesinas del páramo?",
        "tengo que respetar las costumbres de los indígenas de la zona?", "qué norma hay sobre el trato a las comunidades?",
        "puedo burlarme de la forma de hablar de los arrieros?", "respetar la cultura local es obligatorio aquí?",
    ], "Respeta la cultura y las costumbres de los habitantes del lugar. El reglamento también prohíbe hacer discriminaciones de cualquier índole en el parque.",
        ["Trata con respeto a las comunidades de la zona; discriminar a alguien por cualquier motivo está prohibido en el área protegida."],
        [RES207, DEC], ["minors_protection", "follow_park_staff"], ["comunidades", "cultura", "costumbres"]),

    E("sanctions_penalties", "sanciones y multas por infringir", [
        "cuánto es la multa si rompo una regla del parque?", "qué pasa si incumplo el reglamento de Los Nevados?",
        "me pueden multar por dejar basura?", "cuál es la sanción por hacer fogata", "hasta cuánto pueden cobrar de multa en el parque?",
        "cómo funciona el proceso sancionatorio ambiental en el parque", "qué castigo hay por entrar con armas?",
        "cuánto pagaría por pisar un sendero no autorizado", "what happens if I break the park rules?", "pagar multa por llevar mascota al parque?",
        "se pueden imponer sanciones a turistas por ruido?", "hay multas por tirar basura en el parque?",
        "es grave dejar basura en el páramo, cuánto pagan?",
    ], "Si incumples una norma del parque, pueden abrirte un proceso sancionatorio: desde una amonestación pública o servicio comunitario hasta una multa de hasta 100.000 salarios mínimos legales vigentes. El valor en pesos cambia cada año; confirma la duda con Parques Nacionales.",
        ["La multa se liquida con el salario mínimo vigente a la fecha de la decisión, así que su valor en pesos cambia cada año. Confirma el monto con Parques Nacionales."],
        [RES207, LEY2387, LEY1333], ["preventive_measures", "follow_park_staff"], ["sanción", "multa", "proceso sancionatorio"]),
    E("preventive_measures", "decomiso de lo que llevas", [
        "me pueden quitar lo que llevo si está prohibido?", "decomisan la pólvora si la traigo al parque?",
        "qué pasa con las cosas que me confisquen en el control", "si me encuentran algo prohibido, ¿se lo quedan?",
        "pueden llevarse mis implementos de pesca?", "me cobran el parqueadero si retienen mi carro",
        "los costos del decomiso los paga el turista?", "can they confiscate my gear at the entrance?",
        "se pueden retener mis cosas por una infracción?", "si llevo pólvora, me la quitan?",
        "decomiso preventivo en el parque, ¿qué es?", "me pueden retener el equipo mientras se resuelve el caso?",
        "me quitan el alcohol si lo llevo al parque?",
    ], "Si llevas algo prohibido, te lo pueden quitar hasta que decidan el caso. Lo que cueste guardar, transportar o vigilar eso, incluido el parqueadero, lo pagas tú. Pregunta en el control cómo sigue el trámite.",
        ["Si el decomiso se mantiene, los costos de conservar lo retenido corren a tu cargo; consulta el caso con Parques Nacionales."],
        [LEY2387], ["sanctions_penalties", "entry_bag_checks"], ["decomiso", "medidas preventivas", "costos"]),

    # ---- Round 2 expansion: 49 concrete visitor rules and sanctions (total 80 with no_hunting) ----
    E("excavations_prohibited", "Prohibición de excavaciones y remoción de tierra", [
        "puedo cavar una zanja alrededor de la carpa?", "se permite hacer huecos en el suelo del páramo?",
        "puedo hacer una excavación pequeña en el campamento?", "está prohibido remover tierra en Los Nevados?",
        "hacer zanjas para el agua de lluvia junto a la carpa", "puedo abrir una calicata en el sendero?",
        "se puede escarbar la tierra del parque?", "can I dig a trench around my tent?",
        "qué dice el reglamento sobre hacer excavaciones?", "puedo cavar un hoyo en el piso para nivelar la carpa?",
        "remoción de tierras en el parque nacional", "autorizan hacer excavaciones sin permiso científico?",
    ], "No caves ni remuevas tierra, ni hagas calicatas. El reglamento solo deja, de forma excepcional, el hoyo de gato para excretas; cualquier otra excavación necesita autorización de Parques Nacionales.",
        ["El reglamento solo contempla de forma excepcional el hoyo de gato para excretas; cualquier otra excavación o remoción de tierra está prohibida."],
        [RES207, DEC], ["leave_natural_objects", "geological_soil_samples"], ["excavaciones", "calicatas", "remoción de tierra", "zanjas"]),

    E("rock_bolting_prohibited", "Prohibición de instalar chapas en la roca", [
        "puedo instalar chapas de seguridad en la roca?", "se permite taladrar la roca para poner anclajes?",
        "poner chapas de escalada en las paredes del parque", "está permitido equipar rutas con pernos en la roca?",
        "puedo clavar chapas metálicas para escalar en Los Nevados?", "instalación de chapas de seguridad en paredes rocosas",
        "can I bolt climbing routes on the park rocks?", "se puede perforar la roca para asegurar cuerdas?",
        "qué regla hay sobre poner chapas en las peñas del parque?", "dejan instalar anclajes fijos en la piedra?",
        "dejan clavar chapas en la piedra para escalar?", "puedo abrir una vía de escalada poniendo chapas?",
    ], "No instales chapas ni anclajes fijos en la roca, ni perfores las paredes. Pregunta a Parques Nacionales qué equipo de montaña sí puedes llevar.",
        ["No instales chapas ni anclajes fijos en la roca. Pregunta a Parques Nacionales qué equipo de montaña sí puedes llevar."],
        [RES207], ["geological_soil_samples", "organized_sports"], ["chapas", "roca", "escalada", "anclajes"]),

    E("geological_soil_samples", "Prohibición de tomar muestras geológicas y edafológicas", [
        "puedo tomar muestras de suelo o ceniza volcánica?", "se permite recolectar muestras geológicas en el parque?",
        "puedo picar una roca con martillo geológico?", "tomar muestras edafológicas en Los Nevados está permitido?",
        "quiero llevar una muestra de tierra del páramo para analizar", "se puede fracturar material rocoso para ver minerales?",
        "can I collect geological or soil samples in the park?", "puedo partir una piedra para ver cómo es por dentro?",
        "puedo recoger muestras de suelo sin permiso de investigación?", "qué norma rige la toma de muestras geológicas?",
        "dejan partir piedras para estudiar la geología?", "sacar muestras de tierra o roca del volcán",
    ], "No tomes muestras de roca ni de suelo, ni piques o fractures la piedra. Si tu visita es una investigación, pide el permiso a Parques Nacionales antes de entrar.",
        ["Durante la observación geológica no puedes picar rocas ni extraer muestras de suelo; solicita autorización previa si se trata de una investigación formal."],
        [RES207], ["leave_natural_objects", "research_permissions", "excavations_prohibited"], ["muestras geológicas", "suelo", "rocas", "edafología"]),

    E("wildlife_traps_prohibited", "Prohibición de instalar trampas para fauna silvestre", [
        "puedo poner una trampa para capturar animales?", "se permite instalar trampas o conductores de fauna?",
        "puedo usar una jaula o red para atrapar aves?", "está prohibido poner trampas de fauna en el páramo?",
        "instalar conductores de fauna para fotografiar animales", "puedo armar una trampa casera para ver roedores?",
        "are wildlife traps allowed in the park?", "dejan poner una trampa para mirar roedores?",
        "se pueden colocar trampas de captura en Los Nevados?", "puedo poner un cebo para que se acerque un animal?",
        "dejan poner redes de niebla o trampas sin permiso?", "capturar fauna con trampas en el área protegida",
    ], "No pongas trampas ni conductores para atraer o capturar animales. Si ves una, no la toques y avísale al personal del parque.",
        ["No pongas trampas ni conductores para atraer o capturar animales. Si ves una, avísale al personal del parque."],
        [RES207], ["feed_wildlife", "research_permissions"], ["trampas", "conductores de fauna", "captura", "fauna silvestre"]),

    E("wildlife_contact_displacement", "Prohibición de tocar o desplazar fauna silvestre", [
        "puedo tocar o acariciar un animal silvestre si se acerca?", "qué hago si veo un animal en el camino, lo puedo mover?",
        "se puede coger un animalito del páramo para una foto?", "está prohibido desplazar animales de donde están?",
        "puedo agarrar una rana o lagartija para mirarla de cerca?", "intentar coger fauna silvestre en el sendero",
        "can I touch or move wild animals on the trail?", "puedo correr un ave o mamífero para que salga en el video?",
        "me puedo acercar a tocar un colibrí?", "se permite alzar o tocar animales del parque?",
        "puedo alzar un conejo del páramo para la foto?", "qué debo hacer para no incomodar a un animal en la ruta?",
    ], "No cojas, no alimentes y no muevas a los animales silvestres: déjalos donde están. Obsérvalos desde el sendero y sigue de largo.",
        ["No toques ni muevas ningún animal silvestre del sitio donde lo encuentres; obsérvalo en silencio desde el sendero autorizado."],
        [RES207], ["feed_wildlife", "earth_tone_clothing_wildlife"], ["contacto con fauna", "tocar animales", "desplazar fauna"]),

    E("earth_tone_clothing_wildlife", "Ropa de colores tierra para observar fauna", [
        "qué colores de ropa debo usar para no espantar la fauna?", "hay regla sobre evitar ropa de colores muy vivos al ver aves?",
        "recomiendan vestir colores tierra para observar fauna?", "por qué piden evitar colores chillones o fluorescentes en el sendero?",
        "vestir con colores tierra durante la observación de animales", "puedo perturbar a las aves si llevo chaqueta neón muy viva?",
        "should I wear earth-tone clothes for wildlife watching?", "qué dice el reglamento sobre el color de la ropa y la fauna?",
        "la chaqueta fosforescente espanta a los animales?", "evitar colores muy vivos para no perturbar la fauna del parque",
        "cómo vestirse para observar aves sin alterarlas en Los Nevados?", "regla de colores discretos en observación de fauna",
    ], "Para ver fauna o aves, procura ropa de colores tierra y evita prendas muy vivas, para no espantar a los animales. Escoge tonos discretos al alistar la ropa.",
        ["Para no espantar a la fauna, prefiere ropa de colores tierra y evita prendas muy vivas. Escoge tonos discretos antes de salir."],
        [RES207], ["playback", "wildlife_contact_displacement"], ["colores tierra", "observación de fauna", "vestimenta", "aves"]),

    E("aerosols_sprays_prohibited", "Prohibición de usar aerosoles en el parque", [
        "puedo llevar desodorante o bloqueador en aerosol?", "el desodorante en spray me lo dejan entrar?",
        "se pueden usar sprays o aerosoles en Los Nevados?", "qué regla hay sobre llevar productos en aerosol?",
        "puedo aplicar pintura o spray en aerosol sobre una piedra?", "uso de aerosoles o agentes contaminantes en el páramo",
        "are aerosol sprays prohibited in the park?", "dejan usar repelente o pintura en lata de aerosol?",
        "por qué no se permiten aerosoles en el área protegida?", "puedo usar químicos en aerosol durante la caminata?",
        "puedo pintar una piedra con spray?", "prefiero crema o aerosol para subir al parque?",
    ], "No uses aerosoles ni pintes rocas o suelo con spray u otras sustancias. Lleva el protector y el desodorante en crema o barra. Revisa el morral antes de salir.",
        ["Tampoco se permite usar productos químicos en aerosoles que puedan contaminar el suelo, el aire o el agua; empaca alternativas sin spray."],
        [RES207], ["avoid_pollutants", "avoid_chemicals", "graffiti_signage"], ["aerosoles", "sprays", "contaminantes"]),

    E("burning_trash_prohibited", "Prohibición de quemar o incinerar basuras", [
        "puedo quemar el papel higiénico usado en el páramo?", "se permite incinerar la basura en el campamento?",
        "está prohibido quemar desechos o empaques en el parque?", "puedo quemar los papeles de comida para no cargarlos?",
        "incinerar residuos o basuras dentro del área protegida", "puedo prenderle fuego al papel higiénico para no bajarlo?",
        "can I burn my toilet paper or trash at camp?", "se vale prenderle fuego a la basura en la montaña?",
        "quemar la basura del campamento se puede?", "puedo quemar cartón o papel en la zona de camping?",
        "es legal quemar residuos sólidos durante la travesía?", "qué hago con el papel sucio si está prohibido quemarlo?",
    ], "No quemes papel, empaques ni ningún residuo: incinerar basura en el parque está prohibido. Guárdala y sácala contigo.",
        ["Incinerar papel higiénico o empaques está prohibido y además genera riesgo de incendio en el páramo; empaca todos tus desechos de regreso."],
        [DEC, RES207], ["leave_no_waste", "open_fires", "single_use_plastics"], ["incinerar basura", "quemar residuos", "papel higiénico"]),

    E("pick_up_trail_litter", "Deber de recoger residuos hallados en senderos", [
        "qué debo hacer si veo basura tirada en el sendero?", "me llevo la basura ajena que vea tirada?",
        "si encuentro una envoltura en la ruta, ¿debo recogerla?", "qué dice el reglamento si observo basura durante el recorrido?",
        "recoger residuos observados en el sendero para sacarlos", "debo ayudar a sacar basura que otros dejaron en el páramo?",
        "should I pick up litter I see on the trail?", "recojo la basura que otros dejaron en la ruta?",
        "si veo plásticos abandonados en la montaña, qué hago?", "sacar a disposición final la basura encontrada en la ruta",
        "llevo una bolsa extra por si veo basura de otros?", "llevar bolsa para recoger residuos que vea en el camino",
    ], "Si ves basura en el camino, recógela y llévala con la tuya hasta donde se pueda disponer. Lleva una bolsa extra en el morral.",
        ["Si encuentras envolturas en el camino, recógelas y llévalas con tus residuos."],
        [RES207], ["leave_no_waste", "single_use_plastics"], ["recoger basura", "limpieza de senderos", "disposición final"]),

    E("biodegradable_packaging_food", "Uso de materiales biodegradables y mínimo residuo", [
        "qué regla hay sobre los empaques de comida y refrigerios?", "es obligatorio usar materiales biodegradables para los alimentos?",
        "cómo debo llevar los refrigerios para generar el mínimo de residuos?", "reglamentación sobre alimentación e hidratación en senderos",
        "piden usar materiales biodegradables en las zonas de camping?", "cómo empacar la comida para cumplir las normas del parque?",
        "do I need to use biodegradable materials for food packaging?", "generar el mínimo de residuos posible con los refrigerios",
        "los refrigerios tienen que ir en empaque biodegradable?", "debo reempacar mis snacks antes de entrar al parque?",
        "uso de materiales biodegradables en alimentación de montaña", "regla de mínimo residuo en refrigerios del parque",
    ], "Para la comida del sendero o del campamento, usa materiales biodegradables y genera la menor basura posible. Reempaca antes de entrar y saca contigo lo que sobre.",
        ["Lleva la comida en materiales biodegradables y saca contigo lo que sobre."],
        [RES207], ["single_use_plastics", "leave_no_waste"], ["materiales biodegradables", "refrigerios", "mínimo residuo"]),

    E("logging_clearing_vegetation", "Prohibición de talar o cortar vegetación", [
        "puedo cortar ramas para despejar el sitio de la carpa?", "está prohibido talar o hacer rocerías en el parque?",
        "se puede cortar leña o arbustos en el páramo?", "puedo machetear o podar plantas que estorben en el sendero?",
        "abrir monte con machete en el páramo se puede?", "puedo cortar un frailejón que estorba la foto?",
        "is cutting branches or clearing vegetation prohibited?", "puedo llevar implementos para tala de bosques?",
        "hacer rocería o limpiar maleza para acampar está permitido?", "puedo cortar palos del páramo para armar un toldo?",
        "puedo cortar varas de madera en el bosque altoandino?", "se permite socolar o entresacar plantas del parque?",
    ], "No cortes ni despejes vegetación: está prohibido talar, entresacar o hacer rocerías, y tampoco lleves herramientas para talar. Arma la carpa solo donde ya está habilitado, sin tocar las plantas.",
        ["Extraer o dañar material vegetal está prohibido en toda el área protegida; instala tu carpa únicamente en las zonas ya habilitadas sin alterar la vegetación."],
        [DEC, RES207], ["leave_natural_objects", "weapons", "open_fires"], ["tala", "rocería", "vegetación", "bosques"]),

    E("abandoning_gear_objects", "Prohibición de abandonar equipos, carpas u objetos", [
        "qué pasa si se me rompe la carpa, la puedo dejar allá?", "está prohibido abandonar equipos o ropa en la montaña?",
        "puedo dejar abandonado un objeto o equipo dañado en el parque?", "se permite dejar carpas o equipo instalado sin dueño?",
        "puedo dejar el morral dañado escondido en el campamento?", "si mis botas o morral se dañan en la ruta, ¿los puedo dejar?",
        "is it illegal to abandon damaged camping gear in the park?", "debo bajar hasta la ropa o carpa rota de la expedición?",
        "si se me vara el carro, lo puedo dejar ahí?", "la carpa rota también me la tengo que bajar?",
        "puedo dejar equipo guardado y abandonado en el campamento?", "no abandonar objetos de ninguna clase en Los Nevados",
    ], "No dejes equipos, carpas, ropa ni otros objetos en el parque, aunque se hayan dañado. Antes de irte, revisa el sitio y bájalos todos.",
        ["Revisa tu zona de descanso o campamento antes de partir y baja contigo todo tu equipo y prendas sin excepción."],
        [DEC, RES207], ["leave_no_waste", "camping"], ["abandonar equipos", "carpas", "objetos", "retiro"]),

    E("damage_park_infrastructure", "Prohibición de dañar instalaciones o infraestructura", [
        "qué pasa si alguien daña una cabaña o refugio del parque?", "está prohibido causar daño a las instalaciones de Los Nevados?",
        "cuidado de los equipos, miradores y casetas del parque", "se sanciona dañar las instalaciones o bienes del área protegida?",
        "puedo desarmar una cerca o estructura del centro de visitantes?", "romper una banca o una puerta del refugio está prohibido?",
        "is damaging park facilities or infrastructure a violation?", "qué dice el reglamento sobre dañar la infraestructura del parque?",
        "romper puertas, bancas o techos en los puntos de control", "puedo recostarme o subirme a un mirador del parque?",
        "dañar cercas, puentes o miradores en los senderos del parque", "respetar los equipos e instalaciones de Parques Nacionales",
    ], "No dañes las instalaciones, los equipos ni las estructuras del parque. Si ves algo roto, avísale al personal y no lo manipules.",
        ["Si observas una instalación o estructura averiada en el sendero, repórtala al personal del Parque sin manipularla."],
        [RES207, DEC], ["graffiti_signage", "sanctions_penalties"], ["instalaciones", "infraestructura", "daños", "cabañas"]),

    E("agro_industrial_mining_ban", "Prohibición de actividades agropecuarias, hoteleras o mineras", [
        "se pueden hacer actividades agropecuarias o ganaderas en el parque?", "está prohibida la minería y la industria dentro de Los Nevados?",
        "pueden construir hoteles o industrias dentro del parque nacional?", "puedo meter ganado o sembrar dentro del parque?",
        "puedo montar un cultivo o una mina en el páramo?", "se permite meter ganado o cultivos nuevos al área protegida?",
        "are mining, hotel, or agricultural activities banned in the park?", "por qué no se permiten desarrollos hoteleros ni mineros en el parque?",
        "regla contra actividades petroleras, mineras o agropecuarias", "es legal abrir una explotación agrícola o minera en el páramo del parque?",
        "prohibición legal de industria y hotelería en parques nacionales", "se puede abrir un hotel o una mina dentro del parque?",
    ], "No puedes hacer ganadería, agricultura, hotelería, minería ni actividad petrolera dentro del parque. Si quieres ofrecer un servicio a visitantes, pregunta primero a Parques Nacionales.",
        ["Dentro del área protegida no se autorizan explotaciones agropecuarias, mineras, petroleras ni hoteleras; consulta con Parques Nacionales los servicios ecoturísticos permitidos."],
        [DEC], ["sell_advertise", "sanctions_penalties"], ["minería", "actividades agropecuarias", "hotelería", "industria"]),

    E("authorized_stay_duration", "Permanecer solo durante el tiempo autorizado", [
        "puedo quedarme más días de los que dice mi permiso de ingreso?", "qué pasa si me quedo en el parque más tiempo del autorizado?",
        "solo puedo permanecer en el parque el tiempo de mi autorización?", "puedo alargar mi estadía o acampar una noche extra sin permiso?",
        "regla sobre el tiempo máximo de permanencia autorizado", "tengo que salir del parque dentro del tiempo que me aprobaron?",
        "can I stay in the park longer than my permit allows?", "temporalidad de las autorizaciones de ingreso al parque",
        "se permite quedarse más horas o días de los especificados en el permiso?", "me puedo quedar una noche más de la que dice el permiso?",
        "qué dice el reglamento sobre el tiempo de permanencia en el área?", "puedo extender mi travesía dentro del parque por mi cuenta?",
    ], "Quédate solo el tiempo que dice tu permiso de ingreso. No alargues la caminata ni sumes noches de campamento sin una autorización nueva del parque.",
        ["Sal del parque dentro del tiempo que dice tu permiso. Si necesitas más, pide otra autorización antes."],
        [RES207, DEC], ["show_entry_permit_on_request", "camping"], ["tiempo autorizado", "permanencia", "permiso de ingreso"]),

    E("show_entry_permit_on_request", "Obligación de portar y exhibir el permiso", [
        "tengo que llevar el permiso de ingreso durante toda la caminata?", "me pueden pedir la autorización de ingreso en mitad del sendero?",
        "es obligatorio exhibir el permiso ante los funcionarios del parque?", "debo identificarme y mostrar el permiso cuando me lo pidan?",
        "tengo que cargar el permiso de entrada todo el camino?", "qué pasa si un guardaparque me pide el permiso y no lo llevo?",
        "do I have to carry and show my entry permit inside the park?", "si un guardaparque me pide el permiso, se lo muestro?",
        "toca cargar el comprobante de derecho de ingreso todo el tiempo?", "quién me puede exigir mostrar el permiso dentro de Los Nevados?",
        "regla sobre identificarse debidamente ante funcionarios de Parques", "mostrar autorización de ingreso cuando se requiera en la ruta",
    ], "Lleva siempre el permiso de ingreso y tu documento, y muéstralos cuando el personal o una autoridad te los pidan. Tenlos a la mano durante todo el recorrido.",
        ["Los guardaparques y autoridades pueden solicitarte la autorización de ingreso en cualquier punto del recorrido; consérvala protegida durante toda la visita."],
        [RES207, DEC], ["authorized_stay_duration", "tent_permit_display", "follow_park_staff"], ["exhibir permiso", "autorización de ingreso", "identificación"]),

    E("tent_permit_display", "Copia del permiso visible en la carpa", [
        "tengo que pegar una copia del permiso en mi carpa?", "es obligatorio poner el derecho de ingreso visible en la carpa?",
        "dónde debo colocar la copia del permiso cuando acampo?", "regla de adherir copia del derecho de ingreso a la carpa",
        "cómo revisan los guardaparques que mi carpa tiene permiso?", "al hacer camping toca dejar visible la autorización en la carpa?",
        "do I need to attach a copy of my entry permit to my tent?", "qué documento hay que fijar por fuera de la carpa en el campamento?",
        "pego el permiso por fuera de la carpa cuando acampo?", "si acampo en Arenales o Termales Cañón, ¿pego el permiso en la carpa?",
        "para qué piden llevar una copia extra del derecho de ingreso al acampar?", "permiso visible en la carpa durante campamentos",
    ], "Si acampas, pega una copia de tu permiso de ingreso en un lugar visible de la carpa. Lleva esa copia impresa y protégela de la lluvia al armar el campamento.",
        ["Pega la copia del permiso donde se vea en la carpa, además de llevar el original contigo."],
        [RES207], ["camping", "show_entry_permit_on_request", "authorized_stay_duration"], ["permiso en la carpa", "camping", "derecho de ingreso"]),

    E("respect_carrying_capacity_limits", "Deber de respetar la capacidad de carga", [
        "es obligatorio respetar la capacidad de carga de cada sendero?", "qué dice el reglamento sobre el número máximo de personas por grupo?",
        "se puede superar el cupo diario o el tamaño máximo de grupo?", "puedo entrar si el sendero ya está lleno?",
        "qué pasa si un grupo lleva más personas de las permitidas por sendero?", "por qué el reglamento limita los visitantes diarios por atractivo?",
        "must visitors respect the trail carrying capacity and group size limits?", "si el cupo del día ya se llenó, igual entro?",
        "puedo sumarme a un sendero si ya se llenó la capacidad de carga?", "nos dejan pasar si el grupo es más grande de la cuenta?",
        "incumplir el número máximo de personas por grupo es una infracción?", "regla de capacidad de carga en los senderos de Los Nevados",
    ], "Respeta el cupo del sendero y el máximo de personas de tu grupo. No entres sin cupo ni armes un grupo más grande que el autorizado. Confirma el cupo con tu operador antes de salir.",
        ["No pases el cupo del sendero ni el tamaño de grupo que te autorizaron. Confírmalo con tu operador antes de salir."],
        [RES207, POE2026], ["show_entry_permit_on_request", "stay_on_routes"], ["capacidad de carga", "tamaño de grupo", "cupos"]),

    E("visitor_risk_assumption", "Asunción de riesgos y cuidado de pertenencias", [
        "quién asume los riesgos legales durante la visita al parque?", "Parques Nacionales responde si se me pierde algo o tengo un accidente?",
        "quién es responsable de los objetos personales extraviados en el parque?", "si me pasa algo en la ruta, el parque responde?",
        "los funcionarios del parque se responsabilizan por cosas perdidas?", "asunción de riesgos por el visitante en áreas protegidas",
        "does the park assume liability for lost items or visitor accidents?", "cada persona es responsable de sus objetos personales en el recorrido?",
        "exención de responsabilidad de Parques Nacionales por pérdidas o daños", "qué norma establece que el visitante ingresa bajo su propio riesgo?",
        "si pierdo mi cámara o equipo en el sendero, ¿el parque me paga?", "responsabilidad por accidentes y pertenencias dentro del parque",
    ], "Los riesgos de la visita los asumes tú, y cada quien responde por sus cosas. El parque no responde si se te pierde algo. No sueltes el equipaje ni lo dejes solo.",
        ["Entrar no hace responsable al parque por los riesgos de la visita ni por lo que se te extravíe. Cuida tu equipo."],
        [RES207, DEC], ["follow_park_staff", "show_entry_permit_on_request"], ["asunción de riesgos", "objetos personales", "responsabilidad"]),

    E("report_environmental_infractions", "Obligación de denunciar infracciones en el parque", [
        "si veo a alguien dañando el páramo, aviso?", "a quién debo denunciar una infracción contra el reglamento?",
        "es un deber del visitante reportar delitos o infracciones ambientales?", "qué hago si veo a otro turista arrancando plantas o dejando basura?",
        "a quién le cuento si veo una fogata prohibida?", "tengo que reportar si alguien se sale del sendero?",
        "am I required to report rule violations I witness in the park?", "ante quién se denuncian las infracciones cometidas dentro de Los Nevados?",
        "aviso en el control si veo a alguien con dron?", "si veo que alguien vuela un dron o hace fogata, ¿debo avisar?",
        "cómo reportar una infracción ambiental vista durante el recorrido?", "denunciar ante funcionarios de Parques Nacionales y autoridades",
    ], "Si ves que alguien incumple las normas, denúncialo a los funcionarios del parque o a la autoridad. Anota el lugar y avisa en el control.",
        ["Anota el lugar y avísale a tu guía o a los funcionarios del parque."],
        [RES207, DEC], ["follow_park_staff", "sanctions_penalties", "social_media_unauthorized_routes"], ["denunciar infracciones", "delitos ambientales", "deber ciudadano"]),

    E("ecological_customs_checkpoints", "Obligación de someterse a aduanas ecológicas", [
        "qué son las aduanas ecológicas en el acceso al parque?", "es obligatorio pasar por las aduanas ecológicas del sector?",
        "quién realiza las aduanas ecológicas camino a Los Nevados?", "puedo negarme a pasar por una aduana ecológica en la vía?",
        "me puedo saltar la aduana ecológica de la vía?", "para qué sirven las aduanas ecológicas en el manejo del turismo?",
        "what are the ecological customs checkpoints at the park?", "debo detenerme en las aduanas ecológicas antes de ingresar?",
        "qué revisan las autoridades en las aduanas ecológicas del sector?", "en la aduana ecológica me revisan el morral?",
        "las aduanas ecológicas son obligatorias para todos los turistas?", "control ambiental en aduanas ecológicas del área protegida",
    ], "En las aduanas ecológicas del sector debes dejarte revisar por quien maneja el turismo ahí. Quita antes los plásticos de un solo uso y lo que no puedas ingresar.",
        ["Las aduanas ecológicas complementan los controles de ingreso y salida del Parque; colabora con el personal encargado durante la verificación."],
        [RES207], ["entry_bag_checks", "single_use_plastics", "follow_park_staff"], ["aduanas ecológicas", "control ambiental", "autoridades"]),

    E("no_discrimination_scandals", "Prohibición de escándalos y actos de discriminación", [
        "está prohibido provocar o participar en escándalos en el parque?", "qué pasa si alguien arma una pelea o escándalo en el sendero?",
        "puedo poner una bronca en el mirador?", "me pueden echar si armo un escándalo en el sendero?",
        "qué pasa si se arma una pelea en el mirador?", "pueden sancionarme por armar un escándalo en el centro de visitantes?",
        "are public disturbances and discrimination prohibited in the park?", "gritar y pelear en el páramo está prohibido?",
        "alterar el orden o participar en escándalos dentro del área protegida", "si hay una bronca en el grupo, qué hago?",
        "conductas prohibidas por alteración de la organización: escándalos", "se puede hacer una fiesta con pelea en el campamento?",
    ], "No armes escándalos ni te metas en peleas dentro del parque. Si hay un conflicto, aléjate y avísale al personal.",
        ["Si se arma una pelea, aléjate y avísale al personal del parque. No te metas en el escándalo."],
        [DEC, RES207], ["respect_communities", "intoxication", "follow_park_staff"], ["escándalos", "discriminación", "convivencia"]),

    E("park_closure_no_compensation", "Cierre de atractivos sin derecho a indemnización", [
        "si el parque cierra un sendero por riesgo volcánico, ¿tiene que indemnizarme?", "Parques Nacionales paga indemnización si restringe el ingreso por clima o emergencia?",
        "pueden cerrar un atractivo en cualquier momento aunque yo haya pedido entrada antes?", "si cierran por el volcán, me indemnizan el viaje?",
        "facultad del parque para cerrar atractivos sin comprometerse a indemnizar", "si cierran el parque por amenaza natural, ¿indemnizan a la agencia o al turista?",
        "does the park pay compensation if trails close due to natural hazards?", "puede el jefe del parque limitar la entrada o cerrar un atractivo por seguridad?",
        "derecho a indemnización cuando Parques Nacionales cierra por gestión del riesgo", "cierres intempestivos por actividad volcánica o amenazas naturales",
        "compromete a la entidad a indemnizar un cierre preventivo del parque?", "regla sobre restricción de ingreso por recomendaciones de gestión del riesgo",
    ], "El parque puede cerrar un atractivo por seguridad, riesgo, investigación o protección ecológica. Eso no lo obliga a indemnizarte aunque ya hubieras pedido la entrada. Revisa el estado oficial antes de viajar y acata el cierre.",
        ["Revisa si el sector está abierto antes de viajar y cumple el cierre."],
        [RES207], ["follow_park_staff", "authorized_stay_duration"], ["cierre de atractivos", "indemnización", "gestión del riesgo"]),

    E("pack_animals_weight_overnight", "Límite de peso y pernocta de mulas", [
        "cuántos kilos máximo puede cargar una mula de porteo en el parque?", "pueden las mulas o caballos quedarse a dormir dentro del parque?",
        "cuántos animales de carga puede llevar como máximo cada arriero?", "qué reglas tienen los equinos y mulares de porteo en Los Nevados?",
        "es cierto que ningún animal de carga puede llevar más de 80 kg?", "el caballo de carga puede pasar la noche adentro?",
        "what is the maximum weight limit for pack mules in the park?", "máximo cinco animales de carga por arriero o porteador",
        "pueden las mulas salirse del camino o tomar atajos por el páramo?", "las mulas pueden dormir en el parque después del porteo?",
        "por qué las mulas no pueden pasar la noche dentro del parque nacional?", "límite de 80 kilogramos y 5 semovientes por arriero",
    ], "Si contratas porteo, ningún animal puede cargar más de 80 kg, van máximo 5 por arriero, no duermen en el parque y solo transitan por las vías autorizadas, sin atajos. Revisa el peso antes de cargar las maletas.",
        ["Si contratas porteo con animales de carga en un sector habilitado, verifica que el peso de tus maletas respete el tope de 80 kg por animal y que los semovientes no pernocten en el Parque."],
        [RES207], ["no_mules_arenales_calvito", "stay_on_routes"], ["mulas", "animales de carga", "80 kilogramos", "pernocta de equinos"]),

    E("no_mules_arenales_calvito", "Prohibición de mulas en Arenales y Calvito", [
        "pueden subir mulas de carga hasta los campamentos de Arenales o El Calvito?", "está prohibido el porteo con mulas hacia Arenales y Calvito?",
        "hasta dónde pueden llegar las mulas de carga en el sector sur del Tolima?", "cómo se debe entrar a los campamentos de Arenales y Calvito?",
        "la mula puede llegar hasta la carpa en Calvito?", "se permite llevar equipaje en mula desde Termales de Cañón hasta Arenales?",
        "are pack mules allowed up to Arenales and El Calvito camps?", "ingreso exclusivamente a pie a los campamentos temporales de Calvito y Arenales",
        "por qué prohibieron el porteo de maletas con mulas a Arenales y Calvito?", "pueden entrar mulas desde La Primavera o La Playa hacia El Calvito?",
        "cuál es la única excepción para que entren mulas a Arenales o Calvito?", "regla sobre aproximación a pie a los campamentos altos del Tolima",
    ], "No entran mulas ni porteo de maletas a Arenales ni a Calvito: desde Termales del Cañón, La Primavera o La Playa se sigue a pie. Solo pueden entrar mulas si hay un rescate o una emergencia. Haz ese tramo caminando.",
        ["En el sur el porteo solo llega hasta El Berlín, La Argentina o Buenos Aires, La Primavera o La Playa, y Termales del Cañón. Desde ahí cargas tu equipo a pie."],
        [RES207], ["pack_animals_weight_overnight", "camping"], ["Arenales", "El Calvito", "prohibición de mulas", "porteo"]),

    E("commercial_sound_recording", "Permiso para grabaciones de sonido comerciales", [
        "necesito permiso para hacer grabaciones de sonido con fines comerciales?", "está prohibido grabar audio de la naturaleza para uso comercial sin aprobación?",
        "puedo grabar el sonido del páramo para venderlo?", "puedo grabar sonidos del páramo para venderlos en un banco de audio?",
        "autorización previa para grabaciones de sonido con fines comerciales", "capturar audio profesional para una producción comercial en el parque",
        "do I need approval for commercial sound recordings in the park?", "tomar fotografías, películas o grabaciones de sonido para fines comerciales",
        "se requiere permiso de Parques Nacionales para grabación sonora comercial?", "grabar paisajes sonoros de Los Nevados para un proyecto comercial",
        "grabar el viento del páramo para un disco comercial necesita permiso?", "diferencia entre grabar audio personal y grabación sonora comercial",
    ], "Si vas a grabar sonidos del parque para venderlos o usarlos comercialmente, necesitas aprobación previa. Pide el permiso a Parques Nacionales antes de la visita.",
        ["Si la grabación es solo un recuerdo y no la vas a usar comercialmente, esa prohibición no te cubre. Evita el playback y el ruido."],
        [DEC], ["audiovisual_permits", "commercial_photography", "playback"], ["grabaciones de sonido", "audio comercial", "permiso previo"]),

    E("researcher_deliverables_obligation", "Obligaciones de entrega tras investigaciones científicas", [
        "qué debo entregar a Parques Nacionales cuando termine mi investigación autorizada?", "cuáles son las obligaciones de quien obtiene permiso de investigación en el parque?",
        "tengo que entregar informe, publicaciones y duplicados de muestras recolectadas?", "después de investigar, qué le tengo que entregar al parque?",
        "tengo que dejar una muestra de lo que recolecté?", "el paper que saque del estudio se lo mando a Parques?",
        "what must researchers submit to the park after completing a study?", "informe detallado de actividades y resultados tras investigación en el parque",
        "qué pasa con los ejemplares o muestras obtenidas en un estudio científico?", "deberes posteriores al permiso de investigación o estudio en parques nacionales",
        "entregar al menos un ejemplar de cada especie o muestra obtenida", "compromisos legales del investigador autorizado con Parques Nacionales",
    ], "Si te autorizan una investigación, entrega un informe de lo que hiciste y de los resultados, una copia de lo que publiques y al menos un ejemplar de cada muestra. Haz esa entrega a Parques Nacionales.",
        ["Entrega el informe, las publicaciones y los duplicados de las muestras, como quedó en tu permiso."],
        [DEC, RES207], ["research_permissions", "leave_natural_objects", "geological_soil_samples"], ["informe de investigación", "duplicados de muestras", "publicaciones científicas"]),

    E("sport_mountaineers_advance_request", "plan de riesgos del montañismo", [
        "toca adjuntar plan de contingencia y coordenadas de campamento en montañismo deportivo?",
        "el plan de riesgos va en la solicitud de montañismo?",
        "si el campamento es avanzado, pongo las coordenadas?",
        "qué adjunto además del itinerario para escalar en el parque?",
        "el club me pidió un plan de contingencia, eso va en el permiso?",
        "las coordenadas del vivac las pide el parque?",
        "can the mountaineering request include camp coordinates and a risk plan?",
        "mando la solicitud de escalada sin el plan de riesgos?",
        "el itinerario del club lleva el punto del campamento avanzado?",
        "para el permiso de montaña deportiva, el plan de contingencia es aparte?",
        "si no mando las coordenadas del campamento avanzado, me niegan la entrada?",
        "qué papel de riesgos piden en el montañismo deportivo?",
    ], "Si el campamento del montañismo deportivo es avanzado, el itinerario lleva las coordenadas, y la solicitud incluye un plan de riesgos y contingencias. Adjúntalos y espera la autorización del parque antes de salir.",
        ["Sin coordenadas del campamento avanzado ni plan de riesgos, la solicitud queda incompleta. Complétala y espera el permiso."],
        [RES207], ["organized_sports", "sport_mountaineers_schedule_exit_report", "authorized_stay_duration"], ["montañismo deportivo", "plan de riesgos", "coordenadas"]),

    E("sport_mountaineers_schedule_exit_report", "Aviso de cambios y salida de montañistas", [
        "con cuántas horas de anticipación debe avisar un montañista si cambia su cronograma?", "qué pasa si un club de montañismo no avisa un cambio de fecha 24 horas antes?",
        "cuándo deben reportar su salida del parque los montañistas deportivos?", "es obligatorio reportar el fin de la expedición el mismo día o máximo un día después?",
        "pérdida del derecho de ingreso por no informar cambios 24 horas antes", "cuando baje de la expedición, aviso que ya salí?",
        "when must sport mountaineers report schedule changes or expedition exit?", "avisar cambios en el cronograma 24 horas antes de la fecha de ingreso establecida",
        "plazo máximo de un día después para reportar la salida de la expedición", "qué ocurre si los deportistas modifican su itinerario sin avisar 24 horas antes?",
        "reporte obligatorio de finalización de expedición de montañismo en Los Nevados", "reglas sobre ajuste de cronograma y aviso de salida para montañistas deportivos",
    ], "Si cambia tu fecha de ingreso, avísale al parque al menos 24 horas antes; si no avisas, pierdes el derecho a entrar. Cuando termines, reporta la salida el mismo día o, como tarde, al día siguiente.",
        ["Avisa cualquier cambio de fecha al menos 24 horas antes y reporta la salida el mismo día o, como tarde, al día siguiente. Si no avisas el cambio, pierdes el ingreso."],
        [RES207], ["sport_mountaineers_advance_request", "organized_sports", "authorized_stay_duration"], ["cambio de cronograma", "24 horas antes", "reporte de salida", "expedición"]),

    E("guide_operator_misconduct_ban", "Sanciones y prohibiciones para guías y operadores", [
        "qué sanción recibe un guía u operador turístico que incumpla las normas del parque?", "pueden expulsar del registro REPSE a un prestador que viole el reglamento?",
        "cuántas horas antes de trabajar tiene prohibido tomar alcohol un guía?", "es cierto que el guía que incumpla la normatividad no puede seguir operando?",
        "prohibición para guías de consumir bebidas embriagantes 24 horas antes", "expulsión definitiva del registro de prestadores REPSE por faltas graves",
        "what happens if a registered guide or operator breaks park rules?", "si el guía llega con guayabo, puede trabajar?",
        "puede un guía seguir prestando servicios si incumple la reglamentación del parque?", "régimen de sanciones para guías, intérpretes y agencias operadoras",
        "consecuencias para operadores turísticos que violen las reglas de Los Nevados", "regla de cero alcohol 24 horas antes de la labor para guías e intérpretes",
    ], "Un guía no puede tomar alcohol en las 24 horas anteriores a la salida. Si un prestador incumple las normas, puede quedar por fuera del parque y del registro de prestadores. Contrata solo gente avalada y reporta la irregularidad a Parques Nacionales.",
        ["Contrata siempre guías y agencias avaladas que cumplan el reglamento, y reporta al Parque cualquier irregularidad del prestador."],
        [RES207, POE2026], ["follow_park_staff", "sanctions_penalties", "intoxication"], ["guías", "operadores", "REPSE", "sanción a prestadores"]),

    E("social_media_unauthorized_routes", "Sanciones por publicar ascensos a zonas prohibidas", [
        "me pueden sancionar si subo una foto o video en Instagram en el cráter del Ruiz?", "qué hace Parques Nacionales si alguien publica en redes sociales un ascenso no autorizado?",
        "inician proceso sancionatorio por divulgar en Instagram incursiones al glaciar del Ruiz?", "está prohibido ascender a la cima y al cráter del Volcán Nevado del Ruiz?",
        "qué pasó con la denuncia por videos en Instagram subiendo al glaciar del Ruiz?", "usan las publicaciones de redes sociales como evidencia de infracción ambiental?",
        "can I be fined for posting an unauthorized climb to Nevado del Ruiz on Instagram?", "subo la foto del cráter del Ruiz y me pueden sancionar?",
        "investigan a turistas y guías que publican rutas prohibidas en redes sociales?", "consecuencias legales de subir sin permiso al glaciar del Ruiz y publicarlo",
        "cómo actúa el parque ante videos en redes sociales dentro de sectores cerrados?", "incursión no autorizada al cráter del Ruiz divulgada en redes sociales",
    ], "Si publicas en Instagram un ingreso al glaciar o al cráter del Ruiz, Parques Nacionales puede abrir un proceso sancionatorio si hay mérito. No hagas ese ascenso y avisa al parque si alguien lo ofrece.",
        ["No subas al cráter del Ruiz y avísale a Parques Nacionales si alguien ofrece ese recorrido."],
        [CARTA2026, RES207, LEY2387], ["stay_on_routes", "sanctions_penalties", "report_environmental_infractions"], ["Instagram", "redes sociales", "cráter del Ruiz", "incursión no autorizada"]),

    E("written_reprimand_mandatory_course", "Amonestación pública escrita y curso ambiental obligatorio", [
        "en qué consiste la sanción de amonestación pública escrita?", "dónde se publica la amonestación escrita por una infracción ambiental leve?",
        "es cierto que la amonestación obliga a asistir a un curso o servicio comunitario?", "cuánto es la multa si no asisto al curso ambiental de una amonestación?",
        "multa de hasta 5 salarios mínimos por incumplir el curso o servicio comunitario", "si me amonestan por escrito, tengo que ir a un curso?",
        "what is a public written reprimand and mandatory environmental course?", "publicación de la amonestación en la página web de la autoridad y en la alcaldía",
        "sanción por incumplir la asistencia al curso obligatorio o servicio comunitario", "cuándo se aplica la amonestación pública escrita en vez de una multa alta?",
        "la amonestación escrita obliga a tomar cursos de educación ambiental?", "qué pasa si me imponen una amonestación y no voy a la capacitación?",
    ], "La amonestación es un llamado de atención por escrito: la publican en la web de la autoridad y en la alcaldía, y te manda a un curso ambiental o a servicio comunitario. Si no cumples, la multa puede llegar a 5 salarios mínimos mensuales. Asiste a lo que te asignen.",
        ["Si te amonestan por escrito, asiste al curso o a la jornada. Si no vas, la multa puede llegar a 5 salarios mínimos mensuales."],
        [LEY2387], ["sanctions_penalties", "community_service_sanction", "ruia_offender_registry"], ["amonestación pública escrita", "curso ambiental", "5 SMMLV"]),

    E("community_service_sanction", "Servicio comunitario en materia ambiental como sanción", [
        "pueden sancionarme con servicio comunitario ambiental por una falta en el parque?", "cuándo se impone el servicio comunitario en vez de una multa ambiental?",
        "me pueden poner a trabajar por la comunidad en vez de multarme?", "si no tengo dinero para pagar una multa ambiental, ¿pueden ponerme servicio comunitario?",
        "si no tengo plata para la multa, hay otra opción?", "en qué casos reemplaza el servicio comunitario a la multa pecuniaria?",
        "can the environmental authority impose community service as a penalty?", "servicio comunitario ambiental por capacidad socioeconómica insuficiente",
        "el servicio comunitario reemplaza la multa o se suma?", "se puede cumplir servicio comunitario en materias ambientales por infringir normas?",
        "el servicio comunitario aplica junto con la amonestación o en reemplazo de multa?", "reglamentación del servicio comunitario ambiental para infractores",
    ], "Te pueden poner servicio comunitario ambiental o un curso, también junto con la amonestación. Eso reemplaza la multa solo si no puedes pagarla; si no, puede sumarse. Pregunta el trámite a Parques Nacionales.",
        ["El servicio comunitario busca promover la conservación y el cumplimiento de las normas ambientales; consulta con Parques Nacionales los detalles del procedimiento."],
        [LEY2387], ["written_reprimand_mandatory_course", "sanctions_penalties"], ["servicio comunitario", "capacidad socioeconómica", "Ley 2387 de 2024"]),

    E("confiscation_restitution_specimens", "Decomiso y restitución de flora y fauna", [
        "qué hacen con las plantas o animales que le decomisan a un infractor en el parque?", "pueden devolverle al infractor la flora o fauna silvestre que le decomisaron?",
        "qué es la aprehensión preventiva y la restitución de especímenes silvestres?", "si me quitan una planta, me la devuelven después?",
        "prohibición legal de devolver al infractor fauna o flora decomisada", "decomiso definitivo y restitución de especies de flora y fauna silvestres",
        "what happens to wildlife or plants confiscated from rulebreakers?", "si me decomisan un frailejón o animal extraído, ¿nunca me lo devuelven?",
        "aprehensión preventiva de especímenes, productos y subproductos de flora y fauna", "diferencia entre decomiso de implementos y restitución de fauna y flora",
        "la ley prohíbe en todos los casos devolver recursos naturales extraídos ilegalmente?", "se quedan con el animal que saqué del parque?",
    ], "Si sacas plantas o animales sin permiso, te los pueden quitar y no te los devuelven. No te lleves nada del parque.",
        ["Nunca extraigas plantas, semillas ni animales del Parque: además del decomiso definitivo sin devolución, enfrentarás el proceso sancionatorio ambiental."],
        [LEY2387, LEY1333], ["leave_natural_objects", "preventive_measures", "sanctions_penalties"], ["aprehensión preventiva", "restitución de especímenes", "prohibición de devolución"]),

    E("presumption_of_fault_burden_proof", "Presunción de culpa o dolo del infractor", [
        "en una infracción ambiental dentro del parque se presume la culpa o el dolo?", "quién tiene la carga de la prueba en un proceso sancionatorio ambiental?",
        "es cierto que el presunto infractor debe probar que no tuvo culpa ni dolo?", "si me abren un proceso, tengo que probar que no fui yo?",
        "presunción legal de culpa o dolo en infracciones ambientales", "cómo se desvirtúa la presunción de culpa en un proceso con Parques Nacionales?",
        "is fault or intent presumed in Colombian environmental infractions?", "por qué el infractor ambiental tiene a su cargo desvirtuar la culpa o el dolo?",
        "me presumen culpable si hay una infracción ambiental?", "me toca a mí demostrar que no tuve la culpa?",
        "qué significa que en derecho sancionatorio ambiental se presume la culpa?", "regla sobre presunción de culpa o dolo al incumplir normas del parque",
    ], "Si hay una infracción ambiental, se presume que hubo culpa o dolo, y te toca demostrar lo contrario. Cumple las normas y guarda tu permiso de ingreso.",
        ["Para evitar procesos sancionatorios donde opera la presunción de culpa o dolo, cumple estrictamente todas las normas del área protegida y conserva tus soportes de ingreso autorizado."],
        [LEY2387], ["sanctions_penalties", "liability_exemptions_force_majeure"], ["presunción de culpa", "dolo", "carga de la prueba"]),

    E("confession_fine_reduction", "Reducción de multa por confesión de infracción", [
        "hay descuento o reducción en la multa ambiental si confieso la infracción?", "de cuánto es la reducción de la multa si confieso antes del proceso o de los cargos?",
        "aplica la reducción del 30% o 15% por confesión si me sorprenden en flagrancia?", "si confieso antes de que me abran el proceso, me bajan la multa?",
        "reducción del 30% de la multa por confesar antes del inicio del proceso sancionatorio", "reducción del 15% de la multa si confieso antes del auto de formulación de cargos",
        "does confessing an environmental violation reduce the fine in Colombia?", "por qué no procede el descuento por confesión en casos de flagrancia?",
        "beneficio de atenuación por confesión en el procedimiento sancionatorio ambiental", "diferencia entre confesar antes de iniciar el proceso y antes del pliego de cargos",
        "confesar después de que me pillen en el acto también descuenta?", "excepción de flagrancia en la reducción de multa por confesar",
    ], "Si confiesas antes de que abran el proceso, la multa puede bajar un 30%; si confiesas antes de que formulen cargos, un 15%. Si te pillan en el acto, esa rebaja no aplica. Habla con Parques Nacionales antes de que formalicen el caso.",
        ["La rebaja es del 30% o del 15% según el momento, y no aplica si te encontraron en el acto. Confiesa antes de que abran el expediente."],
        [LEY2387], ["sanctions_penalties", "flagrancy_foreign_tourists_procedure"], ["confesión", "reducción de multa", "30%", "15%", "flagrancia"]),

    E("early_termination_correction_plan", "Suspensión y terminación anticipada por corrección ambiental", [
        "se puede suspender y terminar anticipadamente un proceso sancionatorio ambiental?", "puedo parar el proceso si me ofrezco a reparar el daño?",
        "cómo puede un presunto infractor pedir la suspensión del proceso presentando medidas de corrección?", "si cumplo el plan de corrección o compensación ambiental, ¿archivan el proceso sin antecedente?",
        "suspensión del procedimiento sancionatorio por propuesta técnica de corrección o compensación", "hasta cuándo puedo pedir que pausen el proceso para corregir?",
        "can an environmental sanction process be terminated early by correcting the damage?", "la terminación anticipada por corrección ambiental deja antecedente sancionatorio?",
        "si reparo el daño, el proceso queda como antecedente?", "qué tengo que proponer para que cierren el proceso antes del fallo?",
        "presentar medidas técnicamente soportadas y viables para corregir o compensar daño ambiental", "me dejan arreglar el daño yo mismo y cerrar el caso?",
    ], "Antes del fallo puedes pedir que pausen el proceso si propones medidas técnicas para corregir o compensar el daño y las haces tú. Si comprueban que quedó corregido, cierran el caso y no queda como antecedente. Presenta la propuesta a Parques Nacionales.",
        ["Las medidas para corregir o compensar el daño las haces tú. Si las aprueban y verifican el arreglo, cierran el caso."],
        [LEY2387], ["sanctions_penalties", "restoration_duty_civil_criminal"], ["terminación anticipada", "artículo 18A", "corrección ambiental", "compensación"]),

    E("ruia_offender_registry", "Registro Único de Infractores Ambientales (RUIA)", [
        "qué es el RUIA o Registro Único de Infractores Ambientales?", "si me sancionan en el parque, ¿mi nombre queda publicado en el RUIA?",
        "la información del Registro Único de Infractores Ambientales es pública?", "para qué sirve el RUIA en casos de reincidencia en sanciones ambientales?",
        "si me multan, mi nombre queda en un registro público?", "quién administra el Registro Único de Infractores Ambientales en Colombia?",
        "what is the RUIA environmental offender registry in Colombia?", "cualquier persona puede consultar quién está inscrito en el RUIA?",
        "el RUIA es prueba suficiente para demostrar la reincidencia ambiental?", "qué datos del infractor y de la sanción se publican en el RUIA?",
        "inscripción en el RUIA por multas o sanciones en parques nacionales", "consecuencias de quedar reportado en el Registro Único de Infractores Ambientales",
    ], "Si te sancionan, puedes quedar en el registro público de infractores ambientales (RUIA), con la falta, el lugar y la sanción. Lo consulta cualquiera y sirve para probar reincidencia. Evita la falta: ese dato queda visible.",
        ["Evita conductas que den lugar a sanciones ambientales, pues el reporte en el RUIA es de consulta pública y agrava cualquier falta futura."],
        [LEY1333, LEY2387], ["sanctions_penalties", "written_reprimand_mandatory_course", "aggravating_factors_protected_area"], ["RUIA", "registro de infractores", "reincidencia", "acceso público"]),

    E("aggravating_factors_protected_area", "Agravantes por infracciones dentro de áreas protegidas", [
        "es más grave una infracción ambiental si se comete dentro de un parque nacional?", "es peor la falta si la hago dentro del parque?",
        "atentar contra recursos en áreas protegidas o especies amenazadas agrava la sanción?", "obstaculizar la acción de las autoridades o incumplir medidas preventivas es un agravante?",
        "si no dejo que el guardaparque me revise, la sanción sube?", "por qué cometer una falta en Los Nevados tiene agravante legal?",
        "are penalties higher when an environmental infraction occurs inside a national park?", "agravantes por realizar la acción en áreas de especial importancia ecológica",
        "qué pasa si además de cometer la infracción obstaculizo a los guardaparques o incumplo una medida?", "afectar especies en peligro de extinción o bajo veda como causal agravante",
        "factores que aumentan la sanción ambiental en el Parque Nacional Natural Los Nevados", "causales 6, 7, 9 y 10 de agravación en el régimen sancionatorio ambiental",
    ], "Dentro del parque la falta pesa más: dañar recursos de un área protegida o de importancia ecológica, estorbar a la autoridad o incumplir una medida preventiva agrava la sanción. Sigue las indicaciones del personal y no te opongas a un control.",
        ["Respeta las indicaciones de los guardaparques y las medidas preventivas, ya que obstaculizar a la autoridad o reincidir agrava aún más la sanción."],
        [LEY1333], ["sanctions_penalties", "ruia_offender_registry", "follow_park_staff"], ["agravantes", "áreas protegidas", "especies amenazadas", "obstaculizar autoridad"]),

    E("liability_exemptions_force_majeure", "Eximentes de responsabilidad en infracciones ambientales", [
        "cuáles son los únicos eximentes de responsabilidad en una infracción ambiental?", "me salvo de la multa si digo que no sabía la regla?",
        "en qué casos no me sancionan por una infracción ambiental?", "la fuerza mayor, el caso fortuito y el hecho de un tercero eximen de responsabilidad ambiental?",
        "si nadie me explicó la regla al entrar, igual me sancionan?", "un derrumbe que me saca del sendero cuenta como caso fortuito?",
        "what are the legal exemptions from environmental liability in Colombia?", "si alguien más causó el daño, yo respondo igual?",
        "qué causas exoneran a un presunto infractor en un proceso sancionatorio ambiental?", "si un evento de fuerza mayor me obliga a salirme del sendero, ¿es eximente?",
        "un derrumbe o un caso fortuito me exime de la sanción?", "cómo demostrar un eximente de responsabilidad ante la autoridad ambiental",
    ], "Solo pueden eximirte la fuerza mayor o el caso fortuito, o el hecho de un tercero, un sabotaje o un acto terrorista. Si crees que te aplica, explícalo en el proceso ante Parques Nacionales.",
        ["Si alegas fuerza mayor o que el daño lo causó otra persona, explícalo en el proceso ante Parques Nacionales."],
        [LEY1333], ["presumption_of_fault_burden_proof", "sanctions_penalties"], ["eximentes de responsabilidad", "fuerza mayor", "caso fortuito", "hecho de un tercero"]),

    E("restoration_duty_civil_criminal", "Obligación de restaurar el daño ambiental causado", [
        "si pago la multa ambiental, ¿quedo libre de restaurar el daño que hice en el parque?", "la sanción administrativa reemplaza la responsabilidad penal o civil por daño ambiental?",
        "si pago la multa, igual tengo que reparar el páramo?", "pueden abrirme también un proceso penal o civil además de la multa de Parques Nacionales?",
        "la imposición de sanciones no exime al infractor de restaurar el ecosistema o paisaje", "sanciones ambientales sin perjuicio de las acciones civiles, penales, fiscales y disciplinarias",
        "does paying an environmental fine exempt me from restoring the damaged area?", "me pueden obligar a restaurar lo que dañé además de la multa?",
        "responsabilidad en materia penal y civil por daños dentro del Parque Los Nevados", "qué pasa con el daño al páramo después de que imponen la multa sancionatoria?",
        "pagar la sanción me libra del daño que dejé?", "además de la multa, me pueden abrir un proceso penal?",
    ], "Pagar la multa no te libra de reparar el daño: te pueden ordenar obras para restaurar el ecosistema o el paisaje, y además puede haber un proceso civil o penal. Atiende lo que te ordene la autoridad.",
        ["Un incendio, sacar plantas o dañar el páramo puede traerte multa, la orden de reparar y hasta un proceso penal. Atiende lo que te ordene la autoridad."],
        [LEY2387, RES207], ["sanctions_penalties", "early_termination_correction_plan"], ["restauración ambiental", "responsabilidad penal", "acciones civiles", "daño ecológico"]),

    E("flagrancy_foreign_tourists_procedure", "Procedimiento en flagrancia y para turistas extranjeros", [
        "qué procedimiento siguen si sorprenden a un visitante en flagrancia dentro del parque?", "las sanciones y medidas preventivas también se aplican a turistas extranjeros?",
        "cómo notifican a un turista extranjero que vive en otro país si comete una infracción en el parque?", "si me pillan en el momento, me hacen firmar un acta ahí mismo?",
        "soy extranjero, me aplica el mismo proceso si cometo una falta?", "si un extranjero se niega a firmar el acta de flagrancia en el sendero, ¿qué pasa?",
        "how are environmental infractions handled for foreign tourists or in flagrancy?", "envío del auto de inicio y terminación a través de la Cancillería colombiana al país de residencia",
        "levantamiento de acta en el sitio cuando sorprenden a alguien infringiendo normas en flagrancia", "si vivo fuera de Colombia, cómo me notifican la sanción?",
        "procedimiento en el lugar de los hechos cuando hay flagrancia ambiental", "pueden imponer medidas preventivas a ciudadanos extranjeros y sus bienes en el parque?",
    ], "Si te encuentran en el momento, levantan un acta en el sitio y te la hacen firmar; si no firmas, firma un testigo. El proceso también vale si eres extranjero, y si vives en otro país envían los documentos por la Cancillería. Quédate y atiende al funcionario.",
        ["El mismo trámite vale si vienes de otro país. Si vives fuera, los documentos del proceso pueden salir por la Cancillería. Atiende el acta en el sitio."],
        [LEY1333], ["preventive_measures", "confession_fine_reduction", "sanctions_penalties"], ["flagrancia", "acta en el sitio", "turistas extranjeros", "Cancillería"]),
]


def pick_examples(entry, pool):
    """Hard negatives: real examples (3+ words) of other rules entries, related ones first."""
    candidates = []
    for other in entry["related"]:
        if other != entry["id"]:
            candidates.append(other)
    for other in pool:
        if other["id"] != entry["id"] and other["id"] not in candidates:
            candidates.append(other["id"])
    chosen = []
    by_id = {e["id"]: e for e in pool}
    for cid in candidates:
        for text in by_id[cid]["examples"]:
            if len(text.split()) >= 3 and text not in chosen:
                chosen.append(text)
                break
        if len(chosen) == 2:
            break
    return chosen


def build():
    ids = [e["id"] for e in entries]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate rules ids in generator")
    if "rules.no_hunting" in ids:
        raise SystemExit("rules.no_hunting is injected by coordinator_fixes.py; remove it here")
    for entry in entries:
        for ref in entry["related"]:
            if ref not in ids:
                raise SystemExit(f"{entry['id']} related points to unknown id {ref}")
        if len(entry["examples"]) < 12:
            raise SystemExit(f"{entry['id']} has {len(entry['examples'])} examples; need >= 12")
        if len(entry["answer"]["short"]) > 330:
            raise SystemExit(f"{entry['id']} short answer too long ({len(entry['answer']['short'])} chars)")
        if re.search(r"\d", entry["answer"]["short"] + " ".join(entry["answer"]["variants"])):
            entry["last_verified"] = TODAY
        entry["hard_negatives"] = pick_examples(entry, entries)
    section = {
        "contract_version": 1,
        "id": "rules",
        "order": 9,
        "title": "Normas para visitar Los Nevados",
        "description": "Reglas de cuidado y autorizaciones para visitantes: mascotas, residuos, elementos naturales, sustancias, armas, fuego, ruido, fauna, sanciones y actividades especiales en el Parque Nacional Natural Los Nevados.",
        "retrieval": {"profile": "rules", "bm25_weight": 0.25, "top_k": 2, "min_score": None, "entity_filters": []},
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Tu duda es sobre una mascota, residuos o el cuidado del entorno?",
                "¿Quieres saber qué debes dejar en su lugar durante el recorrido?",
                "¿Preguntas por una actividad personal o por una producción organizada?",
                "¿La actividad sería comercial, deportiva, un evento o una investigación?",
                "¿Necesitas una regla general o el permiso para una actividad especial?",
                "¿Tu pregunta es sobre sustancias, plantas u otros elementos naturales?",
            ],
            "slot_questions": {},
            "fallback": "No encontré una regla específica para esa consulta. Para confirmar una norma vigente, pregunta a Parques Nacionales antes de tu visita.",
        },
        "featured": ["rules.pets", "rules.stay_on_routes", "rules.leave_no_waste", "rules.drones", "rules.open_fires"],
        "entries": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}: {len(entries)} entries, {sum(len(e['examples']) for e in entries)} examples")


if __name__ == "__main__":
    build()
