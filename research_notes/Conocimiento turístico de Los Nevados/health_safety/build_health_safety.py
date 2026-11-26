"""Generate data/knowledge/sections/health_safety.json from verified raw evidence."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SECTIONS = ROOT / "data/knowledge/sections"
OUT = SECTIONS / "health_safety.json"
TODAY = "2026-11-21"

PNN = {
    "label": "Parques Nacionales Naturales de Colombia: Parque Nacional Natural Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": TODAY,
}
RES207 = {
    "label": "Parques Nacionales Naturales de Colombia: Resolución 207 de 2023",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf",
    "retrieved_at": TODAY,
}
PNN_FIRST = {
    "label": "Parques Nacionales: recomendaciones para áreas protegidas",
    "url": "https://old.parquesnacionales.gov.co/portal/es/decalogo-de-recomendaciones-para-el-uso-de-areas-protegidas-en-parques-nacionales-naturales-de-colombia/",
    "retrieved_at": TODAY,
}
CDC_ALT = {
    "label": "CDC Yellow Book: High-Altitude Travel and Altitude Illness",
    "url": "https://www.cdc.gov/yellow-book/hcp/environmental-hazards-risks/high-altitude-travel-and-altitude-illness.html",
    "retrieved_at": TODAY,
}
CDC_TRAVEL_ALT = {
    "label": "CDC Travelers’ Health: Travel to High Altitudes",
    "url": "https://wwwnc.cdc.gov/travel/page/travel-to-high-altitudes",
    "retrieved_at": TODAY,
}
CDC_CHILD = {
    "label": "CDC Yellow Book: Traveling Safely with Infants and Children",
    "url": "https://www.cdc.gov/yellow-book/hcp/family-travel/traveling-safely-with-infants-and-children.html",
    "retrieved_at": TODAY,
}
CDC_COLD = {
    "label": "CDC Travelers’ Health: Cold Weather and Travel",
    "url": "https://wwwnc.cdc.gov/travel/page/travel-to-cold-climates/",
    "retrieved_at": TODAY,
}
CDC_NIOSH = {
    "label": "CDC NIOSH: Cold-related Illnesses",
    "url": "https://www.cdc.gov/niosh/cold-stress/about/related-illness.html",
    "retrieved_at": TODAY,
}
CDC_SUN = {
    "label": "CDC Travelers’ Health: Sun Exposure",
    "url": "https://wwwnc.cdc.gov/travel/page/sun-exposure",
    "retrieved_at": TODAY,
}
CDC_LIGHTNING = {
    "label": "CDC: Lightning Safety Tips",
    "url": "https://www.cdc.gov/lightning/safety/index.html",
    "retrieved_at": TODAY,
}
IDIGER = {
    "label": "Alcaldía de Bogotá / IDIGER: medidas ante tormentas eléctricas",
    "url": "https://bogota.gov.co/mi-ciudad/ambiente/medidas-ante-tormentas-electricas-vientos-fuertes-o-vendavales-bogota",
    "retrieved_at": TODAY,
}
POLICE = {
    "label": "Policía Nacional de Colombia: línea 123",
    "url": "https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155",
    "retrieved_at": TODAY,
}
MEDLINE_DEHYD = {
    "label": "MedlinePlus: Dehydration",
    "url": "https://medlineplus.gov/dehydration.html",
    "retrieved_at": TODAY,
}
MEDLINE_HYPO = {
    "label": "MedlinePlus Medical Encyclopedia: Hypothermia",
    "url": "https://medlineplus.gov/ency/article/000038.htm",
    "retrieved_at": TODAY,
}
MEDLINE_FROST = {
    "label": "MedlinePlus Medical Encyclopedia: Frostbite",
    "url": "https://medlineplus.gov/ency/article/000057.htm",
    "retrieved_at": TODAY,
}
MEDLINE_BLEED = {
    "label": "MedlinePlus Medical Encyclopedia: Bleeding",
    "url": "https://medlineplus.gov/ency/article/000045.htm",
    "retrieved_at": TODAY,
}
MEDLINE_CPR = {
    "label": "MedlinePlus: Cardiopulmonary Resuscitation (CPR)",
    "url": "https://medlineplus.gov/cpr.html",
    "retrieved_at": TODAY,
}
MEDLINE_SPRAIN = {
    "label": "MedlinePlus Medical Encyclopedia: Sprains",
    "url": "https://medlineplus.gov/ency/article/000041.htm",
    "retrieved_at": TODAY,
}
MEDLINE_NOSEBLEED = {
    "label": "MedlinePlus Medical Encyclopedia: Nosebleed",
    "url": "https://medlineplus.gov/ency/article/003106.htm",
    "retrieved_at": TODAY,
}
MEDLINE_FAINT = {
    "label": "MedlinePlus: Fainting",
    "url": "https://medlineplus.gov/fainting.html",
    "retrieved_at": TODAY,
}
MEDLINE_BLISTER = {
    "label": "MedlinePlus: Blisters",
    "url": "https://medlineplus.gov/blisters.html",
    "retrieved_at": TODAY,
}
PNN_OSO_HERMOSAS = {
    "label": "Parques Nacionales Naturales de Colombia: recomendaciones ante encuentro con oso andino",
    "url": "https://old.parquesnacionales.gov.co/portal/es/el-oso-andino-continua-dejandose-ver-en-esta-ocasion-en-el-parque-nacional-natural-las-hermosas/",
    "retrieved_at": TODAY,
}
PNN_OSO_HOMENAJE = {
    "label": "Parques Nacionales Naturales de Colombia: recomendaciones ante oso de anteojos con crías o en vías",
    "url": "https://old.parquesnacionales.gov.co/portal/es/este-domingo-21-de-febrero-pontelosanteojosporlavida-y-rinde-un-homenaje-al-gran-oso-de-anteojos/",
    "retrieved_at": TODAY,
}
PNN_OSO_SARAVENA = {
    "label": "Parques Nacionales Naturales de Colombia: comportamiento del oso de anteojos frente a humanos",
    "url": "https://old.parquesnacionales.gov.co/portal/es/parques-nacionales-naturales-de-colombia-rechaza-muerte-de-oso-de-anteojos-en-saravena/",
    "retrieved_at": TODAY,
}
CAR_PUMA = {
    "label": "Alcaldía de Bogotá / CAR Cundinamarca: protocolo ante encuentro con puma",
    "url": "https://bogota.gov.co/mi-ciudad/ambiente/registran-presencia-de-un-puma-en-la-calera-y-la-car-activa-protocolo",
    "retrieved_at": TODAY,
}
CVC_PUMA = {
    "label": "CVC: recomendaciones ante encuentros con pumas",
    "url": "https://www.cvc.gov.co/node/15874",
    "retrieved_at": TODAY,
}
CORTOLIMA_FELINOS = {
    "label": "Cortolima: atención y recomendaciones ante presencia de felinos en el Tolima",
    "url": "https://cortolima.gov.co/sala-de-prensa/noticias/1984-cortolima-atiende-preocupacion-de-comunidad-por-presencia-de-felinos-en-el-tolima",
    "retrieved_at": TODAY,
}
CORTOLIMA_FAUNA = {
    "label": "Cortolima: recomendaciones para respetar la fauna silvestre",
    "url": "https://cortolima.gov.co/sala-de-prensa/noticias/1567-en-el-tolima-se-trabaja-para-que-la-fauna-silvestre-se-respete",
    "retrieved_at": TODAY,
}
CARDER_PUMA = {
    "label": "CARDER: Día Internacional del Puma y línea para encuentros con fauna silvestre",
    "url": "https://www.carder.gov.co/dia-internacional-del-puma/",
    "retrieved_at": TODAY,
}
CARDER_DANTA = {
    "label": "CARDER: La jardinera de los bosques, la danta de montaña",
    "url": "https://www.carder.gov.co/la-jardinera-de-los-bosques-la-danta-de-montana/",
    "retrieved_at": TODAY,
}
MINAMBIENTE_132 = {
    "label": "Ministerio de Ambiente y Desarrollo Sostenible: líneas de emergencia 119, 132, 144 y 123",
    "url": "https://www.minambiente.gov.co/747-municipios-en-el-pais-en-alerta-por-amenaza-de-incendios-forestales/",
    "retrieved_at": TODAY,
}
DEFENSA_CIVIL = {
    "label": "Defensa Civil Colombiana: gestión operativa de emergencias y línea 144",
    "url": "https://www.defensacivil.gov.co/nuestra-institucion-1/gestion-operativa/emergencias",
    "retrieved_at": TODAY,
}
MINSALUD_ALT = {
    "label": "Hospital Civil E.S.E.: guía prehospitalaria de enfermedad por altura",
    "url": "https://hospitalcivilese.gov.co/site/images/guiasyprot/GUIASAMPH/33%20enfermedad%20por%20altura%20343%20a%20348.pdf",
    "retrieved_at": TODAY,
}
MINSALUD_FRIO = {
    "label": "Hospital Civil E.S.E.: guía prehospitalaria de lesiones por frío",
    "url": "https://web.hospitalcivilese.gov.co/wp-content/uploads/2025/09/28-lesiones-por-frio-293-a-300.pdf",
    "retrieved_at": TODAY,
}
MINSALUD_INMOV = {
    "label": "Hospital Civil E.S.E.: guía prehospitalaria de inmovilización",
    "url": "https://web.hospitalcivilese.gov.co/wp-content/uploads/2025/09/42-inmovilizacion-y-transporte-manual-de-pacientes-447-a-466.pdf",
    "retrieved_at": TODAY,
}
MINSALUD_QUEMADURAS = {
    "label": "Hospital Civil E.S.E.: guía prehospitalaria de quemaduras",
    "url": "https://web.hospitalcivilese.gov.co/wp-content/uploads/2025/09/27-quemaduras-283-a-292.pdf",
    "retrieved_at": TODAY,
}
MEDLINE_ALT = {
    "label": "MedlinePlus Medical Encyclopedia: Acute Mountain Sickness",
    "url": "https://medlineplus.gov/ency/article/000133.htm",
    "retrieved_at": TODAY,
}
MEDLINE_FRACTURES = {
    "label": "MedlinePlus Medical Encyclopedia: Fractures (First Aid)",
    "url": "https://medlineplus.gov/ency/article/000001.htm",
    "retrieved_at": TODAY,
}
MEDLINE_SUNBURN = {
    "label": "MedlinePlus Medical Encyclopedia: Sunburn",
    "url": "https://medlineplus.gov/ency/article/003227.htm",
    "retrieved_at": TODAY,
}
MEDLINE_BURNS = {
    "label": "MedlinePlus Medical Encyclopedia: Burns (First Aid)",
    "url": "https://medlineplus.gov/ency/article/000030.htm",
    "retrieved_at": TODAY,
}
MEDLINE_HEAD = {
    "label": "MedlinePlus Medical Encyclopedia: Head Injury (First Aid)",
    "url": "https://medlineplus.gov/ency/article/000028.htm",
    "retrieved_at": TODAY,
}
MEDLINE_CHOKING = {
    "label": "MedlinePlus Medical Encyclopedia: Choking / Abdominal Thrusts",
    "url": "https://medlineplus.gov/ency/article/000047.htm",
    "retrieved_at": TODAY,
}
MEDLINE_SHOCK = {
    "label": "MedlinePlus Medical Encyclopedia: Shock (First Aid)",
    "url": "https://medlineplus.gov/ency/article/000039.htm",
    "retrieved_at": TODAY,
}
MEDLINE_CUTS = {
    "label": "MedlinePlus Medical Encyclopedia: Cuts and Puncture Wounds",
    "url": "https://medlineplus.gov/ency/article/000043.htm",
    "retrieved_at": TODAY,
}


items = [
    (
        "high_altitude_health_risk",
        "riesgo de salud en altura",
        "safety",
        [
            "salud en altura",
            "qué riesgo tiene la altura",
            "me puede afectar la altura en Los Nevados",
            "es pesado para el cuerpo ir al parque",
            "alta montaña y salud",
            "me da algo por falta de oxígeno",
            "uno se puede enfermar por subir",
            "qué debo saber de salud antes de ir",
            "la altura afecta a cualquiera?",
            "is high altitude risky for visitors?",
            "que tan duro es para el cuerpo",
            "me preocupa la altura del parque",
        ],
        "Los Nevados es un destino de alta montaña donde el frío, la menor presión atmosférica y el esfuerzo físico pueden afectar tu salud. Revisa que tengas un estado de salud adecuado y avísale al guía cualquier condición previa antes de iniciar el recorrido.",
        [
            "La visita es de alta montaña: revisa cómo te sientes y coméntale al guía o a un profesional cualquier duda de salud antes de subir."
        ],
        ["Mal de altura", "alta montaña", "prevención"],
        ["altitude_sickness_symptoms", "pretrip_medical_advice"],
        [PNN, CDC_ALT],
        ["síntomas de soroche", "debo preguntarle al médico antes de ir"],
    ),
    (
        "altitude_sickness_symptoms",
        "síntomas del mal de altura",
        "safety",
        [
            "síntomas de soroche",
            "cómo sé si me dio mal de altura",
            "me duele la cabeza y tengo náuseas arriba",
            "mareo y cansancio después de subir",
            "el soroche da dolor de cabeza",
            "qué señales da la altura",
            "me siento como enguayabado en la montaña",
            "la altura puede dar vómito?",
            "poco apetito y dolor de cabeza al subir",
            "how do I recognize altitude sickness?",
            "me dio dolor de cabeza al llegar arriba",
            "que sintomas vigilo en altura",
        ],
        "Después de subir, el mal de altura suele sentirse como dolor de cabeza acompañado de mareo, cansancio, náuseas, vómito o falta de apetito. Si aparecen estos síntomas, avísale de inmediato al guía y no sigas subiendo mientras te sientas mal.",
        [
            "El soroche suele dar dolor de cabeza junto con malestar como náuseas, cansancio o mareo. Avisa al guía y detén el ascenso."
        ],
        ["soroche", "síntomas", "mal de montaña"],
        ["severe_altitude_warning_signs", "no_ascend_while_symptomatic"],
        [CDC_ALT, CDC_TRAVEL_ALT],
        ["confusión en altura", "me puedo quemar aunque esté nublado"],
    ),
    (
        "severe_altitude_warning_signs",
        "señales graves por altura",
        "safety",
        [
            "confusión en altura",
            "me cuesta coordinar al caminar arriba",
            "falta de aire en reposo en la montaña",
            "tos y ahogo después de subir",
            "cuándo el soroche es grave",
            "somnolencia y desorientación en altura",
            "no puedo respirar bien en altura",
            "debilidad y tos al subir",
            "mi compañero está confundido en el páramo",
            "what are danger signs of altitude illness?",
            "señales de emergencia por mal de altura",
            "se puso torpe y confundido al subir",
        ],
        "Confusión, pérdida de coordinación al caminar, somnolencia intensa o falta de aire en reposo son señales de alarma en altura. Pide ayuda urgente al guía o al personal del parque y desciende de inmediato con asistencia; no dejes sola a la persona.",
        [
            "Si hay confusión, mala coordinación o dificultad para respirar en reposo, trátalo como una urgencia: pide ayuda al guía y desciende con apoyo."
        ],
        ["mal de altura grave", "urgencia", "alarma"],
        ["altitude_sickness_symptoms", "descent_for_worsening_altitude"],
        [CDC_TRAVEL_ALT, CDC_ALT],
        ["me duele la cabeza y tengo náuseas arriba", "número para una emergencia en Colombia"],
    ),
    (
        "no_ascend_while_symptomatic",
        "no subir con síntomas",
        "safety",
        [
            "puedo seguir subiendo con dolor de cabeza",
            "me siento mal pero sigo al mirador",
            "si tengo soroche puedo subir más",
            "toca parar si me mareo",
            "puedo continuar con náuseas en altura",
            "es normal seguir caminando con malestar",
            "me dio soroche pero quiero llegar",
            "debo cancelar el ascenso si me duele la cabeza",
            "subir más ayuda a aclimatar",
            "should I keep climbing with symptoms?",
            "puedo avanzar aunque me sienta raro",
            "me aguanto el mareo y sigo?",
        ],
        "No continúes el ascenso ni subas a dormir a mayor altitud mientras tengas síntomas de mal de altura, por leves que parezcan. Quédate a la misma altura, avísale al guía para evaluar si suspenden la ruta y desciende si no mejoras.",
        [
            "Si te sientes mal por la altura, detén el ascenso: informa al guía y evalúen suspender el recorrido o bajar."
        ],
        ["ascenso", "síntomas", "prevención"],
        ["altitude_sickness_symptoms", "descent_for_worsening_altitude"],
        [CDC_TRAVEL_ALT, CDC_ALT, RES207],
        ["temblar mucho en el frío es peligroso", "cómo sé si me dio mal de altura"],
    ),
    (
        "descent_for_worsening_altitude",
        "descenso si empeoras en altura",
        "safety",
        [
            "empeoré descansando en altura",
            "qué hago si el soroche se pone peor",
            "debo bajar si sigo con síntomas",
            "mal de altura no mejora al parar",
            "cuándo hay que descender por soroche",
            "me siento cada vez peor arriba",
            "si descanso y no mejoro qué hago",
            "bajar de altura por malestar",
            "mi dolor de cabeza empeora en la montaña",
            "should I descend if symptoms get worse?",
            "empeora el mareo aunque pare",
            "me puse peor mientras descansaba",
        ],
        "Si tus síntomas empeoran aunque descanses a la misma altitud, debes descender a una cota más baja con ayuda del guía o del personal del parque. No intentes continuar hacia zonas más altas ni esperes a que se vuelva una urgencia grave.",
        [
            "El empeoramiento durante el descanso indica que debes bajar de altitud con apoyo del guía y solicitar atención."
        ],
        ["descenso", "empeoramiento", "mal de altura"],
        ["severe_altitude_warning_signs", "no_ascend_while_symptomatic"],
        [CDC_ALT, CDC_TRAVEL_ALT],
        ["me siento mal pero sigo al mirador", "a quién le digo que me siento mal"],
    ),
    (
        "pretrip_medical_advice",
        "consulta médica antes del viaje",
        "procedure",
        [
            "debo preguntarle al médico antes de ir",
            "tengo una condición de salud y quiero subir",
            "consulta médica para viajar a Los Nevados",
            "quién debe hablar con un doctor antes de ir",
            "es prudente ir con enfermedad previa",
            "llevo mis medicamentos formulados al parque",
            "medicina para prevenir soroche",
            "me automedico para el mal de altura?",
            "qué revisar con mi médico antes de viajar",
            "should I ask my doctor before a high-altitude trip?",
            "tengo una enfermedad crónica y voy al parque",
            "me recomienda un médico para subir",
        ],
        "Si tienes una condición médica previa o dudas sobre la altura, consulta antes del viaje con un médico familiarizado con medicina de montaña y lleva tus medicamentos formulados. No te automediques ni uses esta orientación como reemplazo de una consulta médica.",
        [
            "Habla con tu médico antes de viajar si tienes una condición previa y lleva contigo los medicamentos que tengas formulados."
        ],
        ["consulta médica", "condición previa", "medicación"],
        ["chronic_condition_altitude", "high_altitude_health_risk"],
        [PNN, PNN_FIRST, CDC_ALT],
        ["mi niño está irritable arriba", "me duele la cabeza y tengo náuseas arriba"],
    ),
    (
        "children_altitude_signs",
        "señales de altura en niños",
        "safety",
        [
            "cómo afecta la altura a los niños",
            "mi niño está irritable arriba",
            "mi bebé no quiere comer en altura",
            "niños también sufren soroche",
            "qué señales mirar en niños pequeños",
            "mi hijo está raro después de subir",
            "cambió el sueño de mi niño en la montaña",
            "niño con dolor de cabeza en altura",
            "cómo noto mal de altura si no habla",
            "can children get altitude sickness?",
            "mi hija está fastidiosa y cansada arriba",
            "se ve pálido mi hijo al subir",
        ],
        "Los niños son tan susceptibles al mal de altura como los adultos: en pequeños vigila irritabilidad inusual, falta de apetito o cambios de sueño y actividad, y en mayores dolor de cabeza o falta de aire. Si notas síntomas inexplicables tras subir, avisa al guía y desciende.",
        [
            "En niños, la irritabilidad, la falta de apetito o el dolor de cabeza después de subir pueden indicar mal de altura: avisa al guía para descender."
        ],
        ["niños", "altura", "síntomas"],
        ["altitude_sickness_symptoms", "pretrip_medical_advice"],
        [CDC_CHILD, CDC_TRAVEL_ALT],
        ["un niño llora sin lágrimas", "me duele la cabeza y tengo náuseas arriba"],
    ),
    (
        "tell_guide_about_health_change",
        "avisar al guía por malestar",
        "procedure",
        [
            "a quién le digo que me siento mal",
            "debo contarle al guía mis síntomas",
            "me dio mareo con quién hablo",
            "aviso al guardaparque si me duele la cabeza",
            "qué hago si me siento raro durante el recorrido",
            "puedo decirle al guía que estoy enfermo",
            "a quién notifico una anomalía de salud",
            "me da pena avisar que estoy mal",
            "el guía debe saber si me siento mal",
            "who should I tell if I feel unwell?",
            "me empezó un malestar caminando",
            "como le aviso al personal del parque",
        ],
        "Informa de inmediato a tu guía avalado o a los funcionarios del parque si sientes fatiga, dolor o cualquier malestar en la ruta, y reporta antes de salir si tienes alguna lesión o condición previa. Evalúa con el guía suspender el recorrido y sigue sus instrucciones.",
        [
            "Según la reglamentación del parque, debes avisar al guía sobre tu salud antes y durante la ruta para evaluar si es necesario suspenderla."
        ],
        ["guía", "síntomas", "apoyo"],
        ["altitude_sickness_symptoms", "national_emergency_number_123"],
        [RES207, PNN, PNN_FIRST],
        ["número para una emergencia en Colombia", "me duele la cabeza y tengo náuseas arriba"],
    ),
    (
        "hypothermia_warning_signs",
        "señales de hipotermia",
        "safety",
        [
            "cómo reconocer hipotermia",
            "temblar mucho en el frío es peligroso",
            "está confundido y tiene frío",
            "torpeza después de mojarse en la montaña",
            "cuáles son las señales de enfriamiento",
            "dejar de temblar es mala señal",
            "mi compañero está muy cansado y frío",
            "se le puso azul la piel por el frío",
            "hipotermia por lluvia y viento",
            "what are signs of hypothermia?",
            "me mojé y no paro de temblar",
            "tengo frío y me siento desorientado",
        ],
        "El temblor constante, el cansancio y la dificultad para pensar o moverse bien son señales de hipotermia; si el temblor se detiene por frío extremo o la persona pierde el conocimiento, es una urgencia grave. Busca resguardo, avisa al guía y solicita atención médica de inmediato.",
        [
            "Temblar sin control y perder coordinación o claridad mental con el frío indica hipotermia. Resguárdate y pide ayuda médica enseguida."
        ],
        ["frío", "hipotermia", "síntomas"],
        ["hypothermia_first_response", "frostbite_warning_signs"],
        [CDC_COLD, CDC_NIOSH, MEDLINE_HYPO],
        ["dedos entumecidos por el frío", "qué hago si alguien tiene hipotermia"],
    ),
    (
        "hypothermia_first_response",
        "primeros auxilios por hipotermia",
        "procedure",
        [
            "qué hago si alguien tiene hipotermia",
            "cómo ayudar a una persona muy fría",
            "mi amigo está mojado y tiembla mucho",
            "primeros auxilios por enfriamiento",
            "lo meto en una carpa si tiene hipotermia",
            "debo quitarle la ropa mojada",
            "persona confundida por frío qué hago",
            "cómo caliento a alguien con hipotermia",
            "le doy una bebida caliente si está inconsciente",
            "how do I help someone with hypothermia?",
            "necesito actuar por frío extremo",
            "se mojó y está perdiendo coordinación",
        ],
        "Pide ayuda médica al guía, lleva a la persona a un lugar protegido, quítale la ropa mojada y abrígala con capas secas priorizando pecho, cuello y cabeza. Solo dale una bebida tibia sin alcohol si está plenamente consciente, alerta y puede tragar con seguridad.",
        [
            "Resguarda a la persona del frío, retira la ropa húmeda y abrígala; ofrece bebida tibia sin alcohol únicamente si está alerta y traga bien."
        ],
        ["hipotermia", "primeros auxilios", "frío"],
        ["hypothermia_warning_signs", "national_emergency_number_123"],
        [CDC_COLD, CDC_NIOSH],
        ["cómo reconocer hipotermia", "dedos entumecidos por el frío"],
    ),
    (
        "frostbite_warning_signs",
        "señales de congelación",
        "safety",
        [
            "dedos entumecidos por el frío",
            "cómo saber si tengo congelación",
            "hormigueo y ardor en los dedos",
            "nariz dormida en la montaña",
            "piel pálida y cerosa por frío",
            "me duelen los dedos y no los siento",
            "qué señales da la congelación",
            "se me entumecieron las orejas en la nieve",
            "frostbite en los pies qué es",
            "how do I spot frostbite?",
            "tengo los dedos con hormigueo y dolor",
            "parte de la cara sin sensibilidad por frío",
        ],
        "El hormigueo, entumecimiento, dolor o pérdida de sensibilidad y color en dedos, nariz, orejas o mejillas son señales de congelación, junto con piel fría, pálida y dura. Avisa al guía, pasa a un lugar resguardado del frío y busca atención médica sin frotar la zona.",
        [
            "Si una zona expuesta al frío pierde sensibilidad, se pone pálida o siente hormigueo, resguárdate y busca atención médica sin frotarla."
        ],
        ["congelación", "entumecimiento", "frío"],
        ["frostbite_first_aid", "hypothermia_warning_signs"],
        [CDC_COLD, CDC_NIOSH, MEDLINE_FROST],
        ["cómo reconocer hipotermia", "qué hago con un dedo congelado"],
    ),
    (
        "sun_uv_protection",
        "protección solar en altura",
        "procedure",
        [
            "me puedo quemar aunque esté nublado",
            "el sol pega más en la montaña",
            "cómo evitar quemarme en Los Nevados",
            "protector solar para alta montaña",
            "la nieve refleja los rayos del sol",
            "necesito gafas aunque haga frío",
            "qué hago para cuidarme del sol arriba",
            "el clima frío protege de la radiación",
            "se puede quemar uno en el páramo",
            "how do I protect myself from UV at altitude?",
            "me quemé la cara en un día nublado",
            "como cuido los ojos del sol en altura",
        ],
        "En alta montaña y cerca del ecuador la radiación UV es más intensa, incluso en días fríos o nublados, y la nieve la refleja. Aplícate bloqueador solar de amplio espectro cada dos horas, usa gafas con protección UV y cubre la piel expuesta durante el recorrido.",
        [
            "Las nubes y el frío no frenan la radiación en altura: usa gafas con filtro UV y reaplica bloqueador solar cada dos horas."
        ],
        ["sol", "radiación UV", "protección"],
        ["dehydration_warning_signs", "high_altitude_health_risk"],
        [PNN, CDC_SUN],
        ["mucha sed y boca seca en el parque", "me dio dolor de cabeza al llegar arriba"],
    ),
    (
        "dehydration_warning_signs",
        "señales de deshidratación",
        "safety",
        [
            "cómo noto que estoy deshidratado",
            "orina oscura y mareo caminando",
            "mucha sed y boca seca en el parque",
            "me siento agotado por no tomar agua",
            "la altura me dio dolor de cabeza con náuseas",
            "un niño llora sin lágrimas",
            "cuándo la deshidratación es urgente",
            "tengo la boca seca y casi no orino",
            "deshidratación en caminata de montaña",
            "what are dehydration warning signs?",
            "mi hijo está muy dormido y no toma agua",
            "me mareo y tengo sed en el recorrido",
        ],
        "La sed intensa, la boca seca, orinar menos o con color oscuro, y en niños llorar sin lágrimas o estar muy somnolientos, son señales de deshidratación. Si hay falta de orina, latidos o respiración rápidos, busca atención médica inmediata y avisa al guía.",
        [
            "Sed intensa, boca seca y orina oscura indican deshidratación; si casi no orinas o respiras muy rápido, pide ayuda médica urgente."
        ],
        ["deshidratación", "sed", "mareo"],
        ["dehydration_response", "children_altitude_signs"],
        [MEDLINE_DEHYD, PNN],
        ["cómo evitar quemarme en Los Nevados", "qué tomo si estoy deshidratado"],
    ),
    (
        "national_emergency_number_123",
        "línea nacional de emergencias 123",
        "fact",
        [
            "número para una emergencia en Colombia",
            "a qué teléfono llamo si hay una urgencia",
            "línea de emergencia nacional",
            "cómo pido ayuda por teléfono en Colombia",
            "cuál es el número de emergencias",
            "llamar a la policía por una emergencia",
            "estoy en una emergencia cuál número marco",
            "teléfono de urgencias en Colombia",
            "número único para reportar una emergencia",
            "what number do I call for an emergency in Colombia?",
            "me pasó algo grave y necesito llamar",
            "como contacto emergencias si tengo señal",
        ],
        "En Colombia, el 123 es la línea única nacional de emergencias, gratuita y disponible las 24 horas; si tienes señal, llama e informa tu ubicación. Dentro del parque, avisa de inmediato a tu guía avalado, quien porta radio y botiquín para coordinar con las autoridades.",
        [
            "Si tienes señal móvil, marca el 123; en el sendero, acude enseguida a tu guía registrado para que active la comunicación por radio."
        ],
        ["emergencia", "teléfono", "Colombia"],
        ["tell_guide_about_health_change", "lost_person_protocol"],
        [POLICE, PNN, RES207],
        ["cómo noto que estoy deshidratado", "a quién le digo que me siento mal"],
    ),
    (
        "acclimatization_plan",
        "aclimatación gradual para la altura",
        "procedure",
        [
            "cómo me aclimato antes de subir",
            "cuántos días necesito para adaptarme a la altura",
            "subir rápido a Los Nevados es peligroso",
            "cómo evitar el mal de altura desde el primer día",
            "debo dormir en altura antes del ascenso",
            "es mejor subir despacio la primera vez",
            "rutina para acostumbrarme a la altura",
            "cada cuánto debo descansar al ascender",
            "llegué a Manizales y quiero subir mañana",
            "how do I acclimatize for high altitude?",
            "mejor subir en dos etapas al nevado",
            "qué hago la noche anterior para aclimatarme",
        ],
        "Asciende de forma gradual, evita el alcohol y el ejercicio intenso durante las primeras 48 horas en altura, y procura dormir a menor altitud de la que alcanzas en el día. Durante el ascenso en el parque, haz paradas periódicas de 10 minutos para aclimatarte.",
        [
            "Sube sin prisa, evita el alcohol las primeras 48 horas y realiza pausas de 10 minutos mientras asciendes para favorecer la aclimatación."
        ],
        ["aclimatación", "ascenso gradual", "prevención"],
        ["altitude_sickness_symptoms", "no_ascend_while_symptomatic"],
        [PNN, CDC_ALT, CDC_TRAVEL_ALT],
        ["síntomas de soroche", "puedo seguir subiendo con dolor de cabeza"],
    ),
    (
        "chronic_condition_altitude",
        "enfermedad cardíaca o pulmonar en altura",
        "safety",
        [
            "tengo una enfermedad del corazón puedo subir",
            "soy hipertenso y quiero ir al nevado",
            "tengo problemas pulmonares y me falta el aire",
            "mi médico me dijo que tengo arritmia",
            "puedo visitar la montaña si tengo asma",
            "tengo problema cardiovascular puedo entrar",
            "is altitude safe with a heart condition?",
            "tengo una condición cardíaca y me preocupa la altura",
            "mi presión alta me impide subir",
            "tengo enfisema puedo caminar en altura",
            "viajo con marcapasos al páramo",
            "tengo un soplo cardíaco y quiero subir al páramo",
        ],
        "La Resolución 207 de 2023 restringe el ingreso de personas con problemas cardiovasculares o pulmonares, y el CDC desaconseja viajar a gran altura con afecciones como hipertensión pulmonar severa o anemia falciforme. Consulta antes a tu médico e informa con anticipación al operador y al parque.",
        [
            "El reglamento del parque restringe el ingreso con problemas cardíacos o pulmonares; consulta a tu médico y avisa al operador antes de reservar."
        ],
        ["condición crónica", "corazón", "pulmón"],
        ["pretrip_medical_advice", "high_altitude_health_risk"],
        [RES207, PNN, CDC_ALT, CDC_TRAVEL_ALT],
        ["debo preguntarle al médico antes de ir", "estoy embarazada puedo subir a Los Nevados"],
    ),
    (
        "pregnancy_altitude",
        "embarazo y visita a gran altura",
        "safety",
        [
            "estoy embarazada puedo subir a Los Nevados",
            "viajar al páramo en embarazo es seguro",
            "qué riesgo tiene la altura para el bebé",
            "puedo caminar en altura si estoy gestando",
            "mi esposa está embarazada y quiere ir",
            "is high altitude safe during pregnancy?",
            "embarazo de pocas semanas y viaje a la montaña",
            "debo consultar al médico si estoy embarazada",
            "la altura afecta el embarazo",
            "puedo dormir arriba estando embarazada",
            "tengo embarazo y me da miedo la altura",
            "recomendaciones para gestantes en el parque",
        ],
        "La Resolución 207 de 2023 restringe el ingreso de mujeres embarazadas al Parque Nacional Natural Los Nevados, y el CDC advierte sobre el riesgo de complicaciones en terreno montañoso remoto y al dormir sobre 3.050 metros. No planees el ascenso en embarazo y consulta a tu médico.",
        [
            "El ingreso de mujeres embarazadas está restringido por la reglamentación del parque debido a los riesgos en alta montaña remota."
        ],
        ["embarazo", "altitud", "restricción"],
        ["pretrip_medical_advice", "chronic_condition_altitude"],
        [RES207, CDC_ALT, CDC_TRAVEL_ALT],
        ["tengo una enfermedad del corazón puedo subir", "cómo afecta la altura a los niños"],
    ),
    (
        "older_adults_altitude_health",
        "adultos mayores y salud en altura",
        "safety",
        [
            "cuidados de salud para adultos mayores en altura",
            "riesgo de deshidratación y frío en personas mayores",
            "mi papá es adulto mayor y quiere ir a la montaña",
            "cómo afecta el frío y la altura a la tercera edad",
            "precauciones médicas para mayores de sesenta años",
            "los adultos mayores sienten menos sed en la caminata",
            "is high altitude harder on older adults?",
            "salud de mis abuelos si subimos al páramo",
            "qué vigilar en un adulto mayor durante el recorrido",
            "mayor riesgo de enfriamiento en personas de edad",
            "recomendaciones de salud para viajeros mayores",
            "cuidados con la presión y el agua en adultos mayores",
        ],
        "En adultos mayores disminuye la sensación de sed y las afecciones crónicas o circulatorias aumentan el riesgo ante el frío y la altura. Además, el parque aplica límite máximo de edad (69 años en la ficha web y 70 en la Resolución 207): hidrátate con frecuencia y verifica con el operador antes de ir.",
        [
            "Las personas mayores pueden sentir menos sed y ser más vulnerables al frío; recuerda también confirmar el límite de edad vigente del parque antes de reservar."
        ],
        ["adulto mayor", "hidratación", "edad"],
        ["dehydration_warning_signs", "pretrip_medical_advice", "chronic_condition_altitude"],
        [MEDLINE_DEHYD, MEDLINE_HYPO, PNN, RES207],
        ["cómo noto que estoy deshidratado", "tengo una enfermedad del corazón puedo subir"],
    ),
    (
        "dehydration_response",
        "qué hacer ante la deshidratación",
        "procedure",
        [
            "qué tomo si estoy deshidratado",
            "cómo recuperarme de la deshidratación",
            "bebo agua a sorbos si tengo sed fuerte",
            "me mareé y creo que es por falta de agua",
            "qué hago si casi no he tomado líquido",
            "rehidratar a alguien que camina en altura",
            "how do I treat dehydration on a hike?",
            "tengo la boca seca y quiero mejorar",
            "sirve una bebida con electrolitos",
            "me siento débil por el calor y el esfuerzo",
            "mi compañero está deshidratado qué hago",
            "cómo repongo líquidos después del ascenso",
        ],
        "Para prevenir y tratar la deshidratación leve, hidrátate antes, durante y después de la caminata; bebe agua o soluciones de rehidratación oral, y toma pequeños sorbos si tienes náuseas. Si aparecen señales severas como falta de orina o respiración rápida, avisa al guía y busca atención médica.",
        [
            "Detente a descansar y repón líquidos con agua o sales de rehidratación a pequeños sorbos; si no mejoras, avisa al guía."
        ],
        ["rehidratación", "líquidos", "agua"],
        ["dehydration_warning_signs", "fainting_response"],
        [MEDLINE_DEHYD, PNN],
        ["cómo noto que estoy deshidratado", "alguien se desmayó en el sendero"],
    ),
    (
        "frostbite_first_aid",
        "primeros auxilios por congelación",
        "procedure",
        [
            "qué hago con un dedo congelado",
            "cómo caliento una zona congelada",
            "me puedo frotar los dedos si están entumecidos",
            "agua tibia para la congelación",
            "tratar la piel blanca y dura por frío",
            "first aid for frostbite",
            "mi nariz se congeló qué hago",
            "debo usar nieve para calentar la piel",
            "la piel se puso cerosa y sin sensibilidad",
            "cómo ayudar a alguien con los pies congelados",
            "me duelen los dedos y no siento la punta",
            "qué no hacer con una ampolla por congelación",
        ],
        "Lleva a la persona a un lugar resguardado, quita la ropa mojada o anillos ajustados, revisa si tiene hipotermia y calienta la zona en agua tibia (nunca caliente) o con calor corporal. No frotes ni masajees la piel, no toques las ampollas, evita caminar sobre pies congelados y busca atención médica.",
        [
            "Resguarda del frío y calienta con agua tibia o calor corporal sin frotar ni usar calor seco directo; pide ayuda médica al guía."
        ],
        ["congelación", "agua tibia", "primeros auxilios"],
        ["frostbite_warning_signs", "hypothermia_first_response"],
        [CDC_COLD, CDC_NIOSH, MEDLINE_FROST],
        ["dedos entumecidos por el frío", "qué hago si alguien tiene hipotermia"],
    ),
    (
        "lightning_storm_safety",
        "precaución ante tormenta eléctrica",
        "safety",
        [
            "qué hago si hay rayos durante la caminata",
            "me sorprendió una tormenta eléctrica",
            "es seguro quedarme en un claro",
            "dónde me refugio si hay truenos",
            "hay relámpagos cerca qué hago",
            "what to do in a thunderstorm on a hike?",
            "me refugio debajo de un árbol si llueve",
            "los rayos pueden caer en el páramo",
            "tormenta con viento y granizo en el recorrido",
            "debo soltar objetos metálicos si hay rayos",
            "cómo protegerme de una descarga eléctrica",
            "se oyen truenos y estamos lejos del refugio",
        ],
        "Si escuchas truenos o ves rayos, aléjate de zonas abiertas, de árboles aislados y de estructuras u objetos metálicos como bastones o cercas, y busca un lugar seguro. Sigue de inmediato las instrucciones del guía para resguardarte o evacuar la zona expuesta.",
        [
            "Ante tormenta eléctrica, evita campos abiertos, árboles solitarios y objetos metálicos; busca un sitio seguro junto a tu guía."
        ],
        ["rayos", "tormenta", "refugio"],
        ["hypothermia_warning_signs", "national_emergency_number_123"],
        [CDC_LIGHTNING, IDIGER],
        ["cómo reconocer hipotermia", "número para una emergencia en Colombia"],
    ),
    (
        "lost_person_protocol",
        "qué hacer si te pierdes",
        "procedure",
        [
            "me separé del grupo y no encuentro el sendero",
            "qué hago si me pierdo en la montaña",
            "cómo evitar perderme en la niebla",
            "me desorienté y no veo a nadie",
            "what should I do if I get lost on a hike?",
            "no encuentro el camino de regreso",
            "debo seguir caminando si me pierdo",
            "cómo actuar si alguien se rezaga en la ruta",
            "me alejé del sendero permitido",
            "estamos desorientados y baja la neblina",
            "qué dice el reglamento si alguien se extravía",
            "cómo mantenerme con el grupo en el sendero",
        ],
        "Para evitar extravíos, la Resolución 207 de 2023 exige caminar siempre junto al grupo y al guía avalado, sin salirte de los senderos establecidos ni dejar a nadie rezagado. Si alguien se extravía, no te disperses por tu cuenta: avisa de inmediato al guía y a las autoridades para que activen la respuesta con radio.",
        [
            "Mantente unido al grupo y dentro del sendero autorizado; ante cualquier extravío, informa de inmediato al guía y a las autoridades sin separarte."
        ],
        ["extraviado", "sendero", "grupo"],
        ["tell_guide_about_health_change", "national_emergency_number_123"],
        [RES207, PNN],
        ["a quién le digo que me siento mal", "número para una emergencia en Colombia"],
    ),
    (
        "bleeding_control",
        "controlar sangrado por herida",
        "procedure",
        [
            "cómo paro una hemorragia",
            "se cortó y sangra mucho",
            "presión directa en una herida",
            "sangrado que no se detiene qué hago",
            "how do I stop severe bleeding?",
            "mi compañero se hirió con una piedra",
            "cómo vendar una herida que sangra",
            "sangra la cabeza después de una caída",
            "debo lavar una herida grande antes de presionar",
            "se cortó la mano y sale mucha sangre",
            "hemorragia en la pierna durante la caminata",
            "qué hago si la sangre empapa la gasa",
        ],
        "Acuesta a la persona, eleva la parte que sangra si es posible y aplica presión directa y firme sobre la herida con una gasa o tela limpia. No retires un apósito empapado de sangre ni intentes limpiar una herida grande: pon otro paño encima y pide ayuda urgente al guía.",
        [
            "Haz presión directa con un paño limpio sin retirar la tela si se empapa; coloca otra encima y avisa de inmediato al guía."
        ],
        ["hemorragia", "presión directa", "herida"],
        ["sprain_first_aid", "national_emergency_number_123"],
        [MEDLINE_BLEED, RES207],
        ["me sangra la nariz en la montaña", "me torcí el tobillo en el sendero"],
    ),
    (
        "unresponsive_cpr",
        "persona inconsciente que no respira",
        "procedure",
        [
            "la persona no responde qué hago",
            "cómo hacer reanimación en la montaña",
            "mi compañero se desmayó y no despierta",
            "debo dar RCP si no respira",
            "how to do CPR if someone collapses?",
            "no respira normalmente qué hago",
            "empezar compresiones en el pecho",
            "persona inconsciente que no respira",
            "cómo pedir ayuda mientras hago RCP",
            "se desplomó y no responde al llamarlo",
            "reanimación mientras llega el rescate",
            "qué hago primero si alguien deja de respirar",
        ],
        "Toca su hombro, pregúntale en voz alta si está bien y mira si respira con normalidad; si no responde y no respira normalmente, pide a alguien que avise al guía y llame a emergencias mientras inicias compresiones firmes y rápidas en el centro del pecho si sabes hacer RCP.",
        [
            "Si la persona no responde ni respira con normalidad, pide ayuda urgente al guía y comienza compresiones en el centro del pecho."
        ],
        ["RCP", "inconsciente", "urgencia"],
        ["fainting_response", "national_emergency_number_123"],
        [MEDLINE_CPR, RES207],
        ["alguien se desmayó en el sendero", "número para una emergencia en Colombia"],
    ),
    (
        "sprain_first_aid",
        "primeros auxilios por esguince",
        "procedure",
        [
            "me torcí el tobillo en el sendero",
            "cómo tratar un esguince",
            "se me hinchó el tobillo después de caer",
            "puedo seguir caminando con el tobillo torcido",
            "first aid for a sprained ankle",
            "me duele la rodilla después de un mal paso",
            "hielo o calor para un esguince",
            "cómo vendar un tobillo lesionado",
            "me torcí la muñeca y se inflamó",
            "qué hacer con una articulación inflamada",
            "caí y me torcí el pie caminando",
            "debo apoyar el pie con un esguince",
        ],
        "Detén la caminata y evita apoyar peso sobre la articulación lesionada para no empeorar el daño; aplica frío envuelto en una tela (nunca directo en la piel), venda con firmeza sin apretar y mantén la zona elevada. Avisa al guía para evaluar la suspensión de la ruta y recibir asistencia.",
        [
            "No apoyes la articulación lesionada: aplica frío envuelto en tela, elévala y avisa al guía para suspender la marcha."
        ],
        ["esguince", "tobillo", "primeros auxilios"],
        ["tell_guide_about_health_change", "blister_care"],
        [MEDLINE_SPRAIN, RES207],
        ["cómo paro una hemorragia", "me salió una ampolla en el pie"],
    ),
    (
        "nosebleed_altitude",
        "sangrado nasal en la montaña",
        "procedure",
        [
            "me sangra la nariz en la montaña",
            "cómo parar un sangrado de nariz",
            "sangrado nasal por el aire seco",
            "me salió sangre de la nariz al subir",
            "nosebleed at high altitude what to do",
            "debo inclinar la cabeza hacia atrás",
            "sangra la nariz y no se detiene",
            "me duele la nariz y sangra",
            "cómo actuar si me sale sangre de la nariz",
            "sangrado nasal después de un golpe",
            "la nariz sangra por el frío y la altura",
            "qué hago si el sangrado nasal dura mucho",
        ],
        "El aire seco y frío irrita la nariz: si sangras, siéntate, inclínate hacia adelante para no tragar sangre, respira por la boca y presiona la parte blanda de la nariz por 10 minutos completos. No te acuestes ni metas gasas; si es tras un golpe en la cabeza o dura más de 20 minutos, busca atención médica.",
        [
            "Siéntate, inclina la cabeza hacia adelante y presiona la parte blanda de la nariz por 10 minutos; busca ayuda médica si no cede tras 20 minutos."
        ],
        ["sangrado nasal", "presión", "aire seco"],
        ["bleeding_control", "tell_guide_about_health_change"],
        [MEDLINE_NOSEBLEED, CDC_ALT],
        ["cómo paro una hemorragia", "me duele la cabeza y tengo náuseas arriba"],
    ),
    (
        "fainting_response",
        "qué hacer ante un desmayo",
        "procedure",
        [
            "alguien se desmayó en el sendero",
            "qué hago si una persona se desmaya",
            "me sentí mareado y perdí el conocimiento",
            "cómo ayudar a alguien que se desmayó",
            "what to do when someone faints?",
            "se cayó y quedó inconsciente un momento",
            "cuánto tiempo debe quedarse acostado tras desmayarse",
            "se puso pálido y se desplomó",
            "desmayo durante la caminata en altura",
            "cómo cuidar a una persona que se desmaya",
            "volvió en sí después del desmayo",
            "mi compañera se sintió mareada y se desmayó",
        ],
        "Si alguien se desmaya, verifica que sus vías respiratorias estén despejadas y que esté respirando, y haz que permanezca acostado durante 10 a 15 minutos. Avisa al guía y busca valoración médica para identificar la causa; si no responde o deja de respirar, trátalo como una emergencia.",
        [
            "Comprueba que respire con la vía aérea despejada y mantenlo acostado de 10 a 15 minutos mientras avisas al guía."
        ],
        ["desmayo", "inconsciencia", "primeros auxilios"],
        ["unresponsive_cpr", "dehydration_response"],
        [MEDLINE_FAINT, RES207],
        ["la persona no responde qué hago", "qué tomo si estoy deshidratado"],
    ),
    (
        "blister_care",
        "cuidado de ampollas al caminar",
        "procedure",
        [
            "me salió una ampolla en el pie",
            "cómo curar ampollas de la caminata",
            "debo reventar una ampolla",
            "ampolla en el talón por la bota",
            "how to treat a blister on a hike?",
            "me duele el pie por una ampolla",
            "cómo cubrir una ampolla para seguir",
            "ampollas por roce en el sendero",
            "se puso roja y caliente la ampolla",
            "qué poner en una ampolla del pie",
            "ampollas en los dedos después de caminar",
            "cómo proteger una ampolla del roce",
        ],
        "La piel sobre la ampolla ayuda a evitar infecciones: cúbrela con un vendaje limpio y asegúrate de que el calzado no siga rozando la zona. Si drena pus o el área se pone roja, hinchada, caliente o muy dolorosa, avisa al guía y consulta a un profesional de salud.",
        [
            "Cubre la ampolla con una vendita para mantenerla limpia y evitar más fricción; si ves signos de infección como pus o enrojecimiento, consulta a un médico."
        ],
        ["ampolla", "pie", "roce"],
        ["sprain_first_aid", "tell_guide_about_health_change"],
        [MEDLINE_BLISTER, RES207],
        ["me torcí el tobillo en el sendero", "a quién le digo que me siento mal"],
    ),
    (
        "no_published_wildlife_protocol",
        "no hay protocolo de encuentro con fauna",
        "safety",
        [
            "hay un protocolo si me encuentro un animal en Los Nevados",
            "qué hago si veo fauna silvestre en el sendero del parque",
            "el parque publicó cómo actuar ante un oso o un puma",
            "puedo acercarme a un animal silvestre en el nevado",
            "qué dice el reglamento si se cruza un animal",
            "me puedo llevar o mover un animal del camino",
            "is there an official wildlife encounter protocol in the park?",
            "no tocar ni correr animales del páramo",
            "qué está prohibido hacer con la fauna del parque",
            "vi un animal y no sé si alejarlo del sendero",
            "protocolo de Los Nevados para encuentros con fauna",
            "debo coger un animal herido o dejarlo quieto",
        ],
        "Los Nevados no publica un protocolo de encuentro con oso, puma o danta. La Resolución 207 de 2023 solo ordena evitar el contacto: no intentes coger, alimentar ni desplazar la fauna. Si ves un animal, no te acerques y avisa a tu guía.",
        [
            "No hay un protocolo publicado de encuentro con fauna en este parque: no cojas, no alimentes y no desplaces al animal, y avisa a tu guía."
        ],
        ["fauna", "encuentro", "reglamento"],
        ["rules.feed_wildlife", "fauna.injured_wildlife_protocol", "tell_guide_about_health_change"],
        [RES207],
        ["puedo darle comida a un venado", "número para una emergencia en Colombia"],
    ),
    (
        "ams_how_long_it_lasts",
        "cuánto dura el mal de altura",
        "safety",
        [
            "cuánto dura el mal de altura",
            "el soroche se quita solo o hay que bajar",
            "cuándo el mal de montaña se considera moderado",
            "si el dolor de cabeza de altura dura más de medio día",
            "el mal de altura pasa en dos días de aclimatación",
            "diferencia entre soroche leve y moderado por el tiempo",
            "how long does acute mountain sickness last?",
            "se me quita el soroche si espero en el mismo sitio",
            "más de 12 horas con síntomas de altura qué significa",
            "el mal de montaña cede con la aclimatación",
            "llevo un día con náuseas en el refugio",
            "cuánto tarda en mejorar el soroche si no subo más",
        ],
        "El mal agudo de montaña suele empezar 6 a 12 horas después de pasar los 2.500 m. Es leve si mejora antes de 12 horas y moderado si sigue más de 12 horas; muchas veces cede en las primeras 48 horas. Si no mejora o empeora, avisa al guía y desciende.",
        [
            "Si los síntomas de altura siguen más de 12 horas, trátalo como moderado: no sigas subiendo y avisa al guía para valorar el descenso."
        ],
        ["duración", "soroche", "48 horas"],
        ["altitude_sickness_symptoms", "altitude_classification_levels", "descent_for_worsening_altitude"],
        [MINSALUD_ALT],
        ["síntomas de soroche", "cómo me aclimato antes de subir"],
    ),
    (
        "hypothermia_body_temperature",
        "desde qué temperatura hay hipotermia",
        "safety",
        [
            "a partir de qué temperatura corporal hay hipotermia",
            "bajo cuántos grados es hipotermia leve o severa",
            "35 grados es el límite de la hipotermia",
            "qué es hipotermia moderada entre 32 y 28 grados",
            "cuándo la hipotermia ya es severa por la temperatura",
            "diferencia entre hipotermia leve moderada y grave",
            "at what body temperature does hypothermia start?",
            "si el cuerpo baja de 35 grados qué hago",
            "clasificación de hipotermia por temperatura central",
            "por debajo de 28 grados es hipotermia severa",
            "cómo saber si el enfriamiento ya es grave por los grados",
            "umbral de 35 grados para hipotermia en la montaña",
        ],
        "Hay hipotermia si la temperatura central baja de 35 °C sin quererlo: leve de 35 a 32 °C, moderada de 32 a 28 °C y severa por debajo de 28 °C. Si tiemblas mucho, te confundes o dejas de temblar, busca resguardo y avisa al guía.",
        [
            "Por debajo de 35 °C ya es hipotermia. Si dejas de temblar o te confundes, no esperes: abrígate y pide ayuda al guía."
        ],
        ["35 °C", "hipotermia", "temperatura"],
        ["hypothermia_warning_signs", "severe_hypothermia_signs_and_care"],
        [MINSALUD_FRIO],
        ["cómo reconocer hipotermia", "qué hago si alguien tiene hipotermia"],
    ),
    (
        "glucometer_at_high_altitude",
        "glucómetro poco fiable en altura",
        "safety",
        [
            "el glucómetro mide mal en la alta montaña",
            "puedo confiar en el medidor de azúcar arriba",
            "la altura altera la lectura de glucosa",
            "qué hago si el glucómetro da números raros en el páramo",
            "medidor de diabetes poco fiable en Los Nevados",
            "does a glucometer work at high altitude?",
            "llevar tiras de repuesto para la glucosa en el sendero",
            "el mal de altura puede disparar una cetoacidosis",
            "cómo vigilar el azúcar si subo al nevado",
            "mi glucómetro no coincide con cómo me siento arriba",
            "lectura de glucosa poco fiable por la altitud",
            "debo avisar al guía que mido el azúcar en ruta",
        ],
        "El CDC advierte que no todos los glucómetros leen bien en altura y que el mal de montaña puede desencadenar una cetoacidosis diabética. Sigue el plan de tu médico, lleva insumos de repuesto y avisa a tu guía antes de salir.",
        [
            "No te fíes de una sola lectura del glucómetro en altura: lleva repuestos, sigue lo que te indicó tu médico y dile al guía que tienes diabetes."
        ],
        ["glucómetro", "diabetes", "cetoacidosis"],
        ["diabetes_at_high_altitude", "pretrip_medical_advice"],
        [CDC_ALT],
        ["puedo ir a Los Nevados si tengo diabetes", "debo preguntarle al médico antes de ir"],
    ),
    (
        "hape_first_72_hours",
        "cuándo aparece el edema pulmonar",
        "safety",
        [
            "en cuántas horas aparece el edema pulmonar de altura",
            "el edema pulmonar sale en los primeros tres días",
            "cuándo es más probable el edema de pulmón tras subir",
            "por qué el edema pulmonar pesa tanto en escaladores novatos",
            "ventana de 72 horas del edema pulmonar",
            "when does high altitude pulmonary edema usually start?",
            "riesgo de mortalidad por edema pulmonar en montañistas",
            "las primeras 72 horas después de llegar arriba",
            "puede aparecer edema pulmonar al segundo día de altura",
            "tiempo de aparición del edema pulmonar en el páramo",
            "después de subir cuánto vigilo la tos y el ahogo",
            "el edema pulmonar tarda días o sale enseguida",
        ],
        "La guía prehospitalaria dice que el edema pulmonar de altura suele aparecer en las primeras 72 horas y es la principal causa de mortalidad en escaladores aficionados con poca experiencia y en profesionales por encima de 3.000 m. Si hay ahogo en reposo o tos, avisa al guía y desciende.",
        [
            "Vigila tos y ahogo durante las primeras 72 horas tras subir: si aparecen, avisa al guía y desciende sin esperar."
        ],
        ["72 horas", "edema pulmonar", "3.000 m"],
        ["high_altitude_pulmonary_edema_hape", "descent_for_worsening_altitude"],
        [MINSALUD_ALT],
        ["qué es el edema pulmonar de altura", "confusión en altura"],
    ),
    (
        "hace_may_appear_days_later",
        "el edema cerebral puede tardar días",
        "safety",
        [
            "el edema cerebral puede aparecer varios días después",
            "cuántos días después sale el edema cerebral de altura",
            "puede tardar una semana el edema cerebral",
            "ya bajó el soroche y días después me confundo",
            "el edema cerebral no siempre es inmediato",
            "can high altitude cerebral edema start days later?",
            "cinco a siete días después del mal de montaña",
            "síntomas neurológicos tardíos después de subir",
            "me sentí bien y al quinto día camino mal",
            "por qué vigilar varios días tras un ascenso alto",
            "el edema cerebral es tardío en la alta montaña",
            "días después del ascenso aparece confusión",
        ],
        "El edema cerebral de altura puede aparecer días después del mal de montaña, incluso 5 a 7 días más tarde, tras ascensos por encima de 3.500 m. Si hay confusión, somnolencia o pierdes la coordinación al caminar, avisa al guía y desciendan de inmediato.",
        [
            "No des por cerrado el mal de altura al primer día: el edema cerebral puede salir hasta 5 a 7 días después. Ante confusión o tambaleo, bajen con el guía."
        ],
        ["edema cerebral", "5 a 7 días", "3.500 m"],
        ["high_altitude_cerebral_edema_hace", "severe_altitude_warning_signs"],
        [MINSALUD_ALT],
        ["qué es el edema cerebral de altura", "síntomas de soroche"],
    ),
    (
        "red_cross_emergency_line_132",
        "línea 132 de la Cruz Roja",
        "procedure",
        [
            "cuál es el número de la Cruz Roja en Colombia",
            "línea 132 Cruz Roja emergencias",
            "llamar al 132 por una urgencia médica",
            "teléfono de ambulancia o Cruz Roja",
            "para qué sirve la línea 132",
            "puedo marcar 132 desde el celular en emergencia",
            "Red Cross emergency number in Colombia",
            "número de emergencia de la Cruz Roja Colombiana",
            "marcar 132 o 123 por accidente en montaña",
            "contacto de Cruz Roja para atención prehospitalaria",
            "cómo pedir apoyo a la Cruz Roja en ruta",
            "teléfono corto de la Cruz Roja",
        ],
        "El Ministerio de Ambiente publica el 132 como línea de la Cruz Roja y el 123 como línea de la Policía. Si tienes señal, marca uno de esos números; dentro del parque avisa primero a tu guía con radio.",
        [
            "Con señal puedes marcar el 132 o el 123. En el sendero, el primer aviso es a tu guía avalado, que lleva radio."
        ],
        ["Cruz Roja", "132", "emergencias"],
        ["national_emergency_number_123", "civil_defense_line_144"],
        [MINAMBIENTE_132, PNN, RES207],
        ["número para una emergencia en Colombia", "cuál es el número de la Defensa Civil"],
    ),
    (
        "civil_defense_line_144",
        "línea 144 de la Defensa Civil",
        "procedure",
        [
            "cuál es el número de la Defensa Civil",
            "línea 144 Defensa Civil Colombiana",
            "teléfono de emergencia de la Defensa Civil",
            "marcar 144 para búsqueda y rescate",
            "para qué sirve el número 144",
            "línea de rescate 144 en Colombia",
            "Civil Defense emergency number in Colombia",
            "cómo contactar a la Defensa Civil en una emergencia",
            "llamar al 144 por extravío o rescate",
            "número corto de la Defensa Civil",
            "apoyo de Defensa Civil 144 en montaña",
            "a qué línea llamo a la Defensa Civil",
        ],
        "La línea de emergencia de la Defensa Civil Colombiana es el 144 (y la línea nacional integrada es el 123). Si ocurre un accidente o extravío dentro del parque, notifícalo de inmediato a tu guía con radio y al personal de Parques Nacionales para que articulen el rescate con los organismos de socorro.",
        [
            "El número de emergencia de la Defensa Civil es el 144; en sectores sin señal, activa el reporte por medio del radio de tu guía."
        ],
        ["Defensa Civil", "144", "rescate"],
        ["national_emergency_number_123", "red_cross_emergency_line_132"],
        [DEFENSA_CIVIL, MINAMBIENTE_132, RES207],
        ["cuál es el número de la Cruz Roja en Colombia", "cuál es el teléfono de los bomberos"],
    ),
    (
        "firefighters_line_119",
        "línea 119 de Bomberos",
        "procedure",
        [
            "cuál es el teléfono de los bomberos",
            "línea 119 bomberos en Colombia",
            "a qué número llamo si veo humo o incendio en el parque",
            "marcar 119 por emergencia o incendio forestal",
            "número de emergencia de bomberos",
            "para qué sirve la línea 119",
            "firefighters emergency number in Colombia",
            "cómo reportar un conato de incendio en la montaña",
            "llamar al 119 o al 123 por fuego en el páramo",
            "teléfono corto de bomberos Colombia",
            "contacto de bomberos ante emergencia",
            "a quién llamo si veo fuego en el sendero",
        ],
        "La línea nacional de emergencia de Bomberos es el 119 (también puedes comunicarte al 123). Si detectas humo, fuego o una emergencia en el parque, avisa de inmediato a tu guía con radio y a los guardaparques, y marca el 119 o 123 en cuanto tengas cobertura móvil.",
        [
            "Para emergencias con bomberos o incendios forestales marca el 119 o el 123 si hay señal, y avisa enseguida al guía con radio y a los guardaparques."
        ],
        ["Bomberos", "119", "emergencias"],
        ["national_emergency_number_123", "civil_defense_line_144"],
        [MINAMBIENTE_132, RES207],
        ["cuál es el número de la Defensa Civil", "número para una emergencia en Colombia"],
    ),
    (
        "evacuation_and_rescue_reality",
        "evacuación y rescate en el parque",
        "safety",
        [
            "cómo me sacan del parque si me enfermo o me fracturo",
            "cuánto demora un rescate en Los Nevados",
            "hay helicóptero o ambulancia dentro del sendero",
            "cómo evacúan a un herido en la alta montaña",
            "se pueden usar mulas para sacar a un enfermo",
            "por qué es obligatorio el seguro de accidentes y rescate",
            "how does medical evacuation work in the park?",
            "evacuación en camilla por sendero de montaña",
            "qué pasa si no puedo seguir caminando en el páramo",
            "dificultad de evacuación médica en zonas remotas",
            "traslado de emergencia cuando no entra carro",
            "cómo es el rescate de un visitante lesionado",
        ],
        "En sitios remotos la evacuación puede retrasarse y, si no hay recurso aéreo, se hace por tierra con camillaje manual o con arrieros avalados para emergencias. Entra con el seguro obligatorio de accidentes y rescate y avisa a tu guía con radio.",
        [
            "Si no hay evacuación aérea, el descenso es por tierra, en camilla o con apoyo autorizado. Lleva el seguro obligatorio y avisa pronto al guía."
        ],
        ["evacuación", "rescate", "seguro obligatorio"],
        ["national_emergency_number_123", "tell_guide_about_health_change", "guide_first_aid_kit_and_certification"],
        [MINSALUD_ALT, MEDLINE_ALT, RES207],
        ["número para una emergencia en Colombia", "qué lleva el guía para primeros auxilios"],
    ),
    (
        "altitude_classification_levels",
        "altitud donde empieza el mal de montaña",
        "safety",
        [
            "a partir de qué altura da soroche",
            "desde cuántos metros empieza el mal de altura",
            "cuándo se considera alta o muy alta montaña",
            "en qué altitud aparecen los síntomas de montaña",
            "a las cuántas horas de subir da mal de altura",
            "entre 2500 y 5800 metros qué riesgo de altura hay",
            "at what elevation does altitude sickness start?",
            "por qué arriba de 2500 metros falta el aire",
            "cuánto tarda en aparecer el mal agudo de montaña",
            "clasificación médica de elevación alta y muy alta",
            "desde qué cota debo cuidar la aclimatación",
            "en cuánto tiempo se siente el soroche al subir",
        ],
        "La guía prehospitalaria llama elevación alta a 2.500–3.500 m y muy alta a 3.500–5.800 m. El mal agudo de montaña suele empezar 6 a 12 horas después de pasar los 2.500 m. Brisas y El Cisne están cerca de 4100 m: sube gradual y vigila cómo te sientes.",
        [
            "Tras pasar los 2.500 m, el mal de montaña suele empezar en 6 a 12 horas. Brisas y El Cisne rondan los 4100 m: asciende sin prisa y avisa al guía si te sientes mal."
        ],
        ["altitud", "2.500 metros", "3.500 metros"],
        ["high_altitude_health_risk", "altitude_sickness_symptoms", "acclimatization_plan"],
        [MINSALUD_ALT, CDC_ALT],
        ["salud en altura", "síntomas de soroche"],
    ),
    (
        "high_altitude_cerebral_edema_hace",
        "edema cerebral de altura (ECA)",
        "safety",
        [
            "qué es el edema cerebral de altura",
            "síntomas de edema cerebral por altura ECA",
            "alucinaciones y desorientación en la montaña",
            "qué significa ataxia o caminar tambaleando en altura",
            "por qué se inflama el cerebro con la altura",
            "complicación neurológica del mal de montaña",
            "what is high altitude cerebral edema HACE?",
            "mi compañero dice incoherencias y camina como borracho",
            "somnolencia extrema y confusión arriba de 3500 metros",
            "cómo reconocer un edema cerebral en el páramo",
            "peligro de coma por mal de altura",
            "diferencia entre soroche leve y edema cerebral",
        ],
        "El edema cerebral por altura (ECA) es una complicación grave tras ascensos sobre 3.500 metros y se reconoce por desorientación, confusión, alucinaciones, somnolencia intensa y ataxia (pérdida de coordinación al caminar, similar a estar ebrio). Es una emergencia vital: pide ayuda al guía y desciendan de inmediato.",
        [
            "Si alguien presenta confusión, alucinaciones, somnolencia o incapacidad para caminar coordinado en altura, puede ser edema cerebral de altura: pide rescate al guía y bajen de inmediato."
        ],
        ["edema cerebral", "ECA", "ataxia"],
        ["severe_altitude_warning_signs", "high_altitude_pulmonary_edema_hape", "descent_for_worsening_altitude"],
        [MINSALUD_ALT, CDC_ALT, MEDLINE_ALT],
        ["confusión en altura", "qué es el edema pulmonar de altura"],
    ),
    (
        "high_altitude_pulmonary_edema_hape",
        "edema pulmonar de altura (EPA)",
        "safety",
        [
            "qué es el edema pulmonar de altura",
            "síntomas de edema pulmonar por altura EPA",
            "líquido en los pulmones por subir a la montaña",
            "tos húmeda y labios morados en altura",
            "opresión en el pecho y ahogo sin caminar",
            "cuál es la principal causa de muerte por mal de altura",
            "what is high altitude pulmonary edema HAPE?",
            "se cansa demasiado y tiene tos con ahogo en el páramo",
            "labios azules y falta de aire sentado en la montaña",
            "cómo saber si es edema pulmonar de alta montaña",
            "ahogo progresivo y debilidad extrema al subir",
            "riesgo de asfixia por edema pulmonar en altura",
        ],
        "El edema pulmonar de altura combina síntomas como ahogo en reposo, tos, debilidad u opresión en el pecho con signos como cianosis central. Si los notas, avisa al guía y desciende de inmediato.",
        [
            "Ahogo en reposo, tos, debilidad, opresión en el pecho o cianosis central pueden ser edema pulmonar de altura: avisa al guía y desciende ya."
        ],
        ["edema pulmonar", "EPA", "cianosis"],
        ["severe_altitude_warning_signs", "high_altitude_cerebral_edema_hace", "descent_for_worsening_altitude"],
        [MINSALUD_ALT, CDC_ALT, MEDLINE_ALT],
        ["qué es el edema cerebral de altura", "falta de aire en reposo en la montaña"],
    ),
    (
        "altitude_sleep_disturbance",
        "insomnio y ahogo al dormir en altura",
        "safety",
        [
            "por qué cuesta dormir en la alta montaña",
            "insomnio por la altura en el refugio o campamento",
            "me despierto ahogado al dormir en altura",
            "baja más el oxígeno cuando uno duerme en el páramo",
            "puedo tomar pastillas para dormir en la montaña",
            "por qué es mejor bajar a dormir a menor altitud",
            "why is it hard to sleep at high altitude?",
            "respiración irregular al dormir en alta montaña",
            "sedantes o pastillas para el insomnio en altura",
            "dormir alto empeora el mal de montaña",
            "qué hacer si no puedo conciliar el sueño arriba",
            "consejos para dormir mejor en un viaje de altura",
        ],
        "Por encima de unos 2.700 m es frecuente una respiración periódica que corta el sueño, y la oxigenación baja más al dormir. No uses alcohol ni opiáceos para dormir; cualquier otro medicamento para el sueño, solo si te lo formula un médico. Si empeoras de noche, avisa al guía.",
        [
            "No uses alcohol ni opiáceos para conciliar el sueño en altura. Si te ahogas o empeoras de noche, avisa al guía y no subas a dormir más alto."
        ],
        ["sueño", "insomnio", "pernocta en altura"],
        ["acclimatization_plan", "alcohol_and_altitude_hypothermia", "no_ascend_while_symptomatic"],
        [CDC_ALT, MINSALUD_ALT],
        ["cómo me aclimato antes de subir", "por qué no se debe tomar alcohol en la montaña"],
    ),
    (
        "alcohol_and_altitude_hypothermia",
        "alcohol en altura y con frío",
        "safety",
        [
            "por qué no se debe tomar alcohol en la montaña",
            "un trago de aguardiente sirve para el frío del páramo",
            "el licor ayuda a calentar el cuerpo en el nevado",
            "puedo tomar cerveza o licor antes de subir",
            "cuántas horas debo evitar el alcohol en altura",
            "qué efecto tiene el alcohol en el soroche y la hipotermia",
            "should I avoid alcohol at high altitude and cold?",
            "darle licor a alguien que tiene mucho frío",
            "el alcohol empeora la aclimatación",
            "por qué prohíben bebidas alcohólicas en alta montaña",
            "tomar alcohol la noche anterior a la caminata",
            "riesgo de beber licor con frío y altura",
        ],
        "Evita el alcohol las primeras 48 horas en altura y no lo uses para dormir ni para calentar a alguien con frío o congelación. La Resolución 207 prohíbe ingresar o consumir bebidas alcohólicas en el parque; hidrátate con agua.",
        [
            "No lleves ni tomes alcohol en el parque: tampoco lo uses para dormir o para entrar en calor. Bebe agua y avisa al guía si alguien se enfría."
        ],
        ["alcohol", "aclimatación", "hipotermia"],
        ["altitude_sleep_disturbance", "hypothermia_first_response", "rules.intoxication"],
        [CDC_ALT, MEDLINE_ALT, MINSALUD_FRIO],
        ["por qué cuesta dormir en la alta montaña", "qué hago si alguien tiene hipotermia"],
    ),
    (
        "diabetes_at_high_altitude",
        "diabetes y visita a la alta montaña",
        "safety",
        [
            "puedo ir a Los Nevados si tengo diabetes",
            "precauciones para diabéticos en alta montaña",
            "la altura descontrola el azúcar o la diabetes",
            "riesgo de cetoacidosis diabética por mal de altura",
            "qué debe llevar una persona con diabetes al sendero",
            "soy diabético qué debo consultar antes de subir",
            "can people with diabetes travel to high altitude?",
            "control de glucosa en caminatas de páramo",
            "la diabetes es riesgosa a gran altitud",
            "recomendaciones médicas para visitantes con diabetes",
            "llevar insulina y medicamentos formulados al parque",
            "cómo afecta el soroche a una persona con diabetes",
        ],
        "Según el CDC, la diabetes puede ser difícil de controlar a gran altitud y el mal de montaña puede desencadenar complicaciones como cetoacidosis diabética. Consulta a tu médico antes de planear el ascenso, lleva tus medicamentos e insumos formulados y avisa a tu guía sobre tu condición antes de iniciar el recorrido.",
        [
            "Si tienes diabetes, consulta a tu médico antes de subir a alta montaña, porta tu medicación formulada e informa al guía antes de salir."
        ],
        ["diabetes", "condiciones previas", "glucosa"],
        ["pretrip_medical_advice", "tell_guide_about_health_change"],
        [CDC_TRAVEL_ALT, CDC_ALT, PNN_FIRST],
        ["debo preguntarle al médico antes de ir", "tengo anemia puedo subir a la montaña"],
    ),
    (
        "anemia_and_sickle_cell_altitude",
        "anemia o anemia falciforme en alta montaña",
        "safety",
        [
            "tengo anemia puedo subir a la montaña",
            "por qué la anemia aumenta el riesgo de soroche",
            "personas con anemia falciforme pueden ir al nevado",
            "hemoglobina baja y caminata en alta montaña",
            "qué dice el médico sobre subir con anemia",
            "falta de glóbulos rojos y mal de altura",
            "can I visit high altitude with anemia or sickle cell?",
            "la anemia disminuye el oxígeno en la sangre al subir",
            "contraindicación de gran altitud en anemia drepanocítica",
            "debo tratar la anemia antes de viajar a altura",
            "riesgo de subir al páramo con anemia",
            "anemia falciforme y viaje a gran altitud",
        ],
        "La anemia reduce la cantidad de oxígeno que transporta tu sangre y te hace más propenso a sufrir mal agudo de montaña; además, el CDC indica que las personas con anemia falciforme no deben viajar a grandes alturas bajo ninguna circunstancia. Consulta a tu médico antes del viaje para valorar si es seguro ascender.",
        [
            "Si tienes anemia, consulta a tu médico antes de subir porque aumenta el riesgo de mal de altura; si padeces anemia falciforme, evita viajar a gran altitud."
        ],
        ["anemia", "anemia falciforme", "oxígeno"],
        ["pretrip_medical_advice", "chronic_condition_altitude"],
        [MEDLINE_ALT, CDC_TRAVEL_ALT, CDC_ALT],
        ["puedo ir a Los Nevados si tengo diabetes", "tengo una enfermedad del corazón puedo subir"],
    ),
    (
        "recent_heart_attack_or_stroke_altitude",
        "infarto reciente, ACV o hipertensión pulmonar",
        "safety",
        [
            "tuve un infarto hace poco puedo subir al parque",
            "cuántos días después de un infarto o derrame no se debe subir",
            "hipertensión pulmonar severa en alta montaña",
            "puedo ir si tuve un accidente cerebrovascular reciente",
            "riesgo de subir con angina o EPOC a Los Nevados",
            "antecedente de infarto en los últimos 90 días y altura",
            "can I go to high altitude after a recent heart attack or stroke?",
            "quiénes tienen prohibido o contraindicado el ascenso por corazón",
            "problemas cardíacos o pulmonares severos en el páramo",
            "por qué la hipertensión pulmonar impide subir a gran altura",
            "la altura agrava la angina de pecho y el EPOC",
            "restricción médica tras infarto o trombosis cerebral",
        ],
        "El parque restringe el ingreso con problemas cardiovasculares o pulmonares; además, las guías médicas señalan que la angina o el EPOC se agravan con la altura y que no se debe ascender tras un infarto o ACV en los últimos 90 días ni con hipertensión pulmonar severa. Abstente de subir y consulta a tu médico.",
        [
            "Si sufriste un infarto o ACV en los últimos 90 días, tienes hipertensión pulmonar severa, angina o EPOC, no asciendas a la alta montaña y sigue el criterio de tu médico."
        ],
        ["infarto", "hipertensión pulmonar", "EPOC"],
        ["chronic_condition_altitude", "pretrip_medical_advice"],
        [RES207, CDC_ALT, CDC_TRAVEL_ALT, MINSALUD_ALT],
        ["tengo una enfermedad del corazón puedo subir", "debo preguntarle al médico antes de ir"],
    ),
    (
        "altitude_carbohydrates_and_exertion",
        "alimentación y ritmo de esfuerzo físico en altura",
        "safety",
        [
            "qué comer durante la caminata para prevenir el soroche",
            "por qué recomiendan carbohidratos en alta montaña",
            "qué tan rápido o fuerte puedo caminar en altura",
            "exigirse mucho físicamente da más mal de montaña",
            "debo hacer ejercicio suave los primeros días en altura",
            "alimentación rica en carbohidratos e hidratación al subir",
            "what food and pace help prevent altitude sickness?",
            "no esperar rendir igual que a nivel del mar",
            "cómo influye el esfuerzo físico en el mal de altura",
            "caminar despacio y comer carbohidratos en el páramo",
            "por qué me canso más rápido subiendo en Los Nevados",
            "ritmo de marcha y comidas para aguantar la altura",
        ],
        "En alta montaña no esperes rendir al mismo nivel físico que en tierras bajas, pues el mal de altura depende de la velocidad de ascenso y de cuánto te exijas. Mantén un ritmo suave durante las primeras 48 horas, haz paradas de 10 minutos al subir, hidrátate bien y consume comidas regulares ricas en carbohidratos.",
        [
            "Modera tu esfuerzo físico en altura, camina a paso suave con pausas de 10 minutos, hidrátate constantemente y prefiere alimentos ricos en carbohidratos."
        ],
        ["carbohidratos", "esfuerzo físico", "ritmo"],
        ["acclimatization_plan", "dehydration_response"],
        [MEDLINE_ALT, CDC_ALT, PNN],
        ["cómo me aclimato antes de subir", "qué tomo si estoy deshidratado"],
    ),
    (
        "altitude_preventive_medication_doctor",
        "medicamentos para prevenir el mal de altura",
        "safety",
        [
            "puedo tomar pastillas para prevenir el soroche",
            "qué medicamento sirve para el mal de altura",
            "se puede tomar acetazolamida sin receta médica",
            "debo automedicarme para no sentir la altura",
            "quién receta medicamentos para subir a la montaña",
            "sirve la acetazolamida o dexametasona para la altura",
            "should I take medicine like acetazolamide for altitude?",
            "consultar al médico sobre fármacos para el mal de montaña",
            "una pastilla reemplaza la aclimatación o el descenso",
            "medicación preventiva bajo fórmula médica para altura",
            "riesgo de tomar medicamentos para la altura por cuenta propia",
            "necesito autorización médica para profilaxis de altura",
        ],
        "Medicamentos como la acetazolamida o la dexametasona solo deben usarse con valoración y fórmula previa de un médico, pues tienen contraindicaciones y efectos adversos. Nunca te automediques y ten presente que ningún fármaco reemplaza el ascenso gradual ni el descenso inmediato si aparecen o empeoran los síntomas.",
        [
            "No te automediques para la altura: cualquier fármaco preventivo requiere consulta y fórmula médica previa, y nunca sustituye la aclimatación ni el descenso."
        ],
        ["medicamentos", "no automedicarse", "consulta médica"],
        ["pretrip_medical_advice", "acclimatization_plan", "descent_for_worsening_altitude"],
        [MEDLINE_ALT, MINSALUD_ALT, CDC_ALT],
        ["debo preguntarle al médico antes de ir", "cómo me aclimato antes de subir"],
    ),
    (
        "altitude_temperature_drop_rate",
        "cuánto baja la temperatura al subir de altitud",
        "safety",
        [
            "cuántos grados baja la temperatura al subir la montaña",
            "por qué hace tanto frío a medida que subimos",
            "cuánto disminuye la temperatura por cada 100 metros de altura",
            "cómo cambian el frío y la presión arriba de 3500 metros",
            "por qué las tormentas empeoran la falta de oxígeno arriba",
            "descenso térmico al ganar elevación en el parque",
            "how much does temperature drop as you gain altitude?",
            "cambio de temperatura por cada cien metros de ascenso",
            "baja presión y tormentas por encima de 3500 metros",
            "por qué se enfría tan rápido el ambiente al ascender",
            "relación entre ganar altura y pérdida de temperatura",
            "prepararse para la caída de temperatura en cotas altas",
        ],
        "En montaña la temperatura desciende aproximadamente entre 0,5 y 0,6 °C por cada 100 metros de elevación ganada; además, por encima de los 3.500 metros las tormentas y sistemas de baja presión reducen aún más la presión barométrica. Abrígate por capas antes de enfriarte y consulta al guía si el clima desmejora.",
        [
            "La temperatura cae cerca de 0,5 a 0,6 °C por cada 100 metros de ascenso y las tormentas sobre 3.500 m acentúan la hipoxia: ajusta tu abrigo a tiempo y sigue las indicaciones del guía."
        ],
        ["descenso térmico", "altitud", "presión barométrica"],
        ["hypothermia_first_response", "wind_and_wetness_heat_loss"],
        [MINSALUD_FRIO, MINSALUD_ALT],
        ["cómo reconocer hipotermia", "por qué el viento y la ropa mojada dan hipotermia"],
    ),
    (
        "wind_and_wetness_heat_loss",
        "viento y humedad aceleran la hipotermia",
        "safety",
        [
            "por qué el viento y la ropa mojada dan hipotermia",
            "cuánto multiplica el viento o la humedad el efecto del frío",
            "qué pasa si camino con la ropa sudada o mojada por lluvia",
            "cuánto más rápido se enfría el cuerpo mojado",
            "peligro de mojarse con lluvia y viento en el páramo",
            "por qué debo cambiarme la ropa húmeda de inmediato",
            "how fast do wind and wet clothes cause hypothermia?",
            "efecto del viento y del agua fría sobre el calor corporal",
            "pérdida de calor por contacto con agua fría en montaña",
            "protegerse del viento y la humedad para no sufrir hipotermia",
            "por qué la llovizna con viento enfría tanto en altura",
            "riesgo de enfriamiento rápido con prendas mojadas",
        ],
        "El viento multiplica por 10 la acción del frío, la humedad la multiplica por 14 y el contacto directo con agua fría hace perder calor hasta 32 veces más rápido que el aire seco. Protégete con chaqueta cortaviento e impermeable, retira de inmediato cualquier prenda húmeda o mojada y resguárdate si arrecia el viento.",
        [
            "El viento (10 veces), la humedad (14 veces) y el agua fría (32 veces) disparan la pérdida de calor: mantén tu ropa seca, corta el viento y busca abrigo a tiempo."
        ],
        ["viento", "humedad", "pérdida de calor"],
        ["hypothermia_first_response", "hypothermia_warning_signs", "trench_foot_wet_cold_feet"],
        [MINSALUD_FRIO, CDC_NIOSH],
        ["cómo reconocer hipotermia", "qué pasa si camino horas con las botas y medias mojadas"],
    ),
    (
        "severe_hypothermia_signs_and_care",
        "hipotermia moderada a severa y cuidado al mover",
        "safety",
        [
            "qué pasa cuando alguien con hipotermia deja de temblar",
            "por qué es peligroso que desaparezca el escalofrío en el frío",
            "por qué no se debe mover bruscamente a alguien con hipotermia",
            "señales de hipotermia severa bajo 32 grados",
            "rigidez muscular y estupor por frío extremo",
            "riesgo de arritmia cardíaca al mover a un hipotérmico",
            "what happens in severe hypothermia when shivering stops?",
            "mi compañero tiene mucho frío pero ya no tiembla y está letárgico",
            "cómo manejar con suavidad a una persona con hipotermia grave",
            "manta térmica y evitar movimientos bruscos en hipotermia",
            "cuándo la hipotermia se vuelve una emergencia crítica",
            "temperatura menor de 32 grados y pérdida de conciencia por frío",
        ],
        "La hipotermia moderada o severa es una persona fría con conciencia alterada, temperatura central bajo 32 °C o sin escalofrío; en la moderada hay rigidez y estupor. Quítale la ropa mojada, cúbrela con manta térmica, evita movimientos bruscos y pide evacuación al guía.",
        [
            "Si alguien muy frío deja de temblar, se pone rígido o somnoliento, abrígalo con manta térmica, no lo muevas de golpe y pide evacuación al guía."
        ],
        ["hipotermia severa", "32 °C", "movimientos bruscos"],
        ["hypothermia_warning_signs", "hypothermia_first_response", "unresponsive_cpr"],
        [MINSALUD_FRIO, MEDLINE_HYPO, CDC_NIOSH],
        ["cómo reconocer hipotermia", "qué hago si alguien tiene hipotermia"],
    ),
    (
        "frostbite_no_refreeze_or_walk",
        "no caminar con pies congelados ni recongelar",
        "safety",
        [
            "puedo seguir caminando si tengo los pies congelados",
            "qué pasa si una mano o pie congelado se calienta y vuelve a congelarse",
            "por qué es peligroso descongelar si aún falta caminar en el frío",
            "puedo caminar después de recalentar los pies congelados",
            "daño en los tejidos por descongelar y recongelar",
            "qué hacer si se me congelan los dedos de los pies en la ruta",
            "can I walk on frostbitten feet or let them refreeze?",
            "riesgo de recongelación en tejido congelado",
            "por qué prohibir que camine alguien con congelamiento en los pies",
            "proteger los pies congelados hasta la evacuación",
            "cuándo recalentar una extremidad congelada en montaña",
            "cuidado de los pies con congelación durante el rescate",
        ],
        "El tejido congelado que se descongela y vuelve a congelarse casi siempre muere; por eso no recalientes una zona en ruta si puede recongelarse. Tampoco camines sobre pies o dedos congelados —y menos tras recalentarlos—, pues causa lesiones graves: protege la extremidad sin apretarla y pide evacuación al guía.",
        [
            "No camines sobre pies congelados o recién recalentados ni descongeles una extremidad si puede volver a congelarse: protégela de golpes y frío y coordina la evacuación con el guía."
        ],
        ["congelamiento", "recongelación", "pies"],
        ["frostbite_warning_signs", "frostbite_no_direct_dry_heat"],
        [MINSALUD_FRIO, CDC_NIOSH],
        ["dedos entumecidos por el frío", "puedo calentar manos congeladas con una estufa o fogata"],
    ),
    (
        "frostbite_no_direct_dry_heat",
        "no uses calor directo en congelación",
        "safety",
        [
            "puedo calentar manos congeladas con una estufa o fogata",
            "por qué no acercar los dedos congelados al fuego",
            "se puede usar lámpara de calor o almohadilla eléctrica en congelamiento",
            "cómo recalentar dedos entumidos sin quemarlos",
            "peligro de quemadura al calentar piel congelada con estufa",
            "agua tibia o calor corporal para dedos congelados",
            "why shouldn't I warm frostbite with a stove or fire?",
            "por qué la piel congelada se quema fácil con calor seco",
            "recalentar dedos en la axila o con agua tibia",
            "errores al tratar manos o pies congelados en campamento",
            "no usar fuego ni agua hirviendo en partes congeladas",
            "temperatura segura para recalentar una zona congelada",
        ],
        "Nunca descongeles manos o pies con calor alto directo como estufas, fogatas, lámparas o almohadillas térmicas: como la piel congelada está entumecida, puede quemarse gravemente sin que lo sientas. Usa calor corporal (como abrigar los dedos en la axila) o agua tibia en un sitio seguro y busca atención médica.",
        [
            "No acerques zonas congeladas a estufas, fogatas ni calor seco directo porque están entumecidas y se queman con facilidad; usa calor corporal o agua tibia y consulta a un médico."
        ],
        ["congelamiento", "calor directo", "quemadura"],
        ["frostbite_warning_signs", "frostbite_no_refreeze_or_walk", "thermal_burn_first_aid_camp"],
        [CDC_NIOSH, MINSALUD_FRIO, MEDLINE_FROST],
        ["dedos entumecidos por el frío", "me quemé con la estufa o agua hirviendo en el campamento"],
    ),
    (
        "trench_foot_wet_cold_feet",
        "pie de trinchera por calzado mojado y frío",
        "safety",
        [
            "qué pasa si camino horas con las botas y medias mojadas",
            "qué es el pie de trinchera o pie de inmersión",
            "pies arrugados rojos y entumidos por humedad y frío",
            "cuánto más rápido pierden calor los pies mojados",
            "se me mojaron las botas en el páramo y me duelen los pies",
            "cómo tratar los pies después de caminar mojado en frío",
            "what is trench foot from wet cold boots?",
            "hinchazón calambres y ampollas por pies mojados en frío",
            "primeros auxilios si tengo los pies helados y húmedos",
            "por qué llevar medias secas de cambio previene lesiones por frío",
            "entumecimiento y dolor en los pies por botas húmedas",
            "cuidado de los pies expuestos al agua y al frío",
        ],
        "La exposición prolongada a humedad y frío produce el pie de trinchera: los pies mojados pierden calor 25 veces más rápido que los secos y presentan enrojecimiento, entumecimiento, calambres, hinchazón o ampollas. Quítate botas y medias mojadas, seca y abriga los pies, no camines si hay lesión y avisa al guía.",
        [
            "Si tus pies llevan horas mojados y fríos, retira botas y medias húmedas, sécalos y abrígalos de inmediato; si hay dolor, hinchazón o ampollas, no sigas caminando y avisa al guía."
        ],
        ["pie de trinchera", "botas mojadas", "frío"],
        ["wind_and_wetness_heat_loss", "frostbite_warning_signs", "blister_care"],
        [CDC_NIOSH, MINSALUD_FRIO],
        ["me salió una ampolla en el pie", "dedos entumecidos por el frío"],
    ),
    (
        "chilblains_cold_skin_itching",
        "sabañones o picazón y manchas rojas por frío",
        "safety",
        [
            "qué son los sabañones por el frío",
            "me salieron manchas rojas que pican en los dedos por el frío",
            "picazón e inflamación en orejas y mejillas tras el frío",
            "por qué me pican y se ponen rojos los dedos al calentarlos",
            "puedo rascarme la piel irritada por el frío",
            "cómo cuidar sabañones en manos u orejas",
            "what are chilblains from cold exposure?",
            "enrojecimiento y picazón en dedos y orejas en la montaña",
            "daño en los vasos pequeños de la piel por frío húmedo",
            "qué hacer si el frío me brotó y me inflamó los dedos",
            "calentar despacio la piel con sabañones",
            "lesiones leves de frío en mejillas orejas y dedos",
        ],
        "La exposición repetida al frío sobre cero daña pequeños vasos de la piel (sabañones), causando enrojecimiento, picazón, inflamación o ampollas en mejillas, orejas y dedos. Calienta la piel lentamente, evita rascarte, mantén cualquier ampolla o lesión limpia y cubierta y consulta a un médico si hay úlceras.",
        [
            "Si el frío te deja manchas rojas con picazón e inflamación en dedos, orejas o mejillas, abriga la piel poco a poco, no te rasques y mantén la zona limpia y protegida."
        ],
        ["sabañones", "picazón", "frío"],
        ["frostbite_warning_signs", "trench_foot_wet_cold_feet"],
        [CDC_NIOSH],
        ["dedos entumecidos por el frío", "qué pasa si camino horas con las botas y medias mojadas"],
    ),
    (
        "sunburn_first_aid_mountain",
        "cómo tratar una quemadura solar tras la caminata",
        "procedure",
        [
            "cómo aliviar una quemadura de sol después del sendero",
            "me quemé la cara con el sol del páramo qué me pongo",
            "puedo echarme vaselina o mantequilla en una quemadura solar",
            "por qué no usar cremas con benzocaína o lidocaína para el sol",
            "me salieron ampollas por el sol en la montaña",
            "cuándo ir al médico por una quemadura solar fuerte",
            "first aid and home care for sunburn at high altitude",
            "paños frescos y tomar agua para insolación o quemadura solar",
            "qué hacer si tengo fiebre y escalofríos tras quemarme con el sol",
            "debo reventar o pelar las ampollas del sol",
            "cuidados para la piel quemada por radiación UV en altura",
            "tratamiento básico si me insolé o quemé en el recorrido",
        ],
        "Para aliviar una quemadura solar, aplica paños limpios, húmedos y frescos, bebe abundante agua y no revientes ni peles las ampollas. No uses vaselina, mantequilla ni aceites (tapan los poros), ni productos con benzocaína o lidocaína; si presentas fiebre, escalofríos, mareo o ampollas extensas, consulta a un médico.",
        [
            "Enfría la quemadura solar con compresas húmedas frescas, hidrátate bien, no apliques aceites ni benzocaína/lidocaína y acude al médico si hay fiebre o mareo."
        ],
        ["quemadura solar", "radiación UV", "primeros auxilios"],
        ["sun_uv_protection", "sun_eye_pain_photophobia", "thermal_burn_first_aid_camp"],
        [MEDLINE_SUNBURN, CDC_SUN],
        ["cada cuánto aplicarse bloqueador en la montaña", "me duelen los ojos después de estar en el sol o la nieve"],
    ),
    (
        "sun_eye_pain_photophobia",
        "dolor de ojos por el sol en montaña",
        "safety",
        [
            "me duelen los ojos después de estar en el sol o la nieve",
            "por qué son obligatorias las gafas con filtro UV en el nevado",
            "el reflejo del sol en la nieve quema los ojos",
            "tengo los ojos irritados y me molesta la luz tras la caminata",
            "ceguera de la nieve o dolor ocular por radiación UV",
            "cómo proteger los ojos del sol en alta montaña",
            "eye pain and light sensitivity from high altitude sun",
            "riesgo en los ojos por no usar gafas de sol en el páramo",
            "fotofobia y ardor en los ojos después de subir",
            "cuándo consultar al médico por dolor en los ojos tras el sol",
            "radiación ultravioleta reflejada en nieve y agua",
            "gafas oscuras con protección UV para caminar en altura",
        ],
        "En alta montaña la radiación ultravioleta es muy intensa y se refleja en la nieve y el agua, por lo que siempre debes usar gafas con protección UV. Si tras la exposición solar sientes dolor en los ojos o sensibilidad a la luz, resguárdate del brillo, no te frotes los ojos y consulta de inmediato a un médico.",
        [
            "Usa siempre gafas con filtro UV en el parque; si tras la ruta te duelen los ojos o te molesta la luz, descansa de la claridad y busca valoración médica."
        ],
        ["ojos", "gafas UV", "sensibilidad a la luz"],
        ["sun_uv_protection", "sunburn_first_aid_mountain"],
        [MEDLINE_SUNBURN, CDC_SUN, PNN],
        ["cada cuánto aplicarse bloqueador en la montaña", "cómo aliviar una quemadura de sol después del sendero"],
    ),
    (
        "thermal_burn_first_aid_camp",
        "primeros auxilios por quemadura con estufa o líquido",
        "procedure",
        [
            "me quemé con la estufa o agua hirviendo en el campamento",
            "primeros auxilios para una quemadura con líquido caliente",
            "cuántos minutos debo poner agua fresca en una quemadura",
            "debo quitar la ropa pegada a una quemadura",
            "se puede poner hielo aceite o mantequilla en una quemadura",
            "cómo cubrir una quemadura para que no se infecte",
            "first aid for a stove or hot water burn on a trip",
            "qué hacer si alguien se quema cocinando en la montaña",
            "no reventar las ampollas de una quemadura térmica",
            "retirar anillos y prendas no adheridas tras una quemadura",
            "cuándo una quemadura requiere atención médica urgente",
            "enfriar quemadura con agua fresca y no helada",
        ],
        "Si sufres una quemadura térmica, enfría la zona con agua fresca (no helada) de 5 a 30 minutos y retira anillos o prendas no pegadas a la piel. No arranques ropa adherida, no rompas ampollas ni apliques aceite, mantequilla o remedios caseros; cúbrela con gasa limpia y seca y avisa al guía.",
        [
            "Enfría la quemadura con agua fresca de 5 a 30 minutos, no retires ropa adherida ni revientes ampollas, evita untar aceites o mantequilla, cubre con vendaje limpio y busca apoyo médico."
        ],
        ["quemadura", "primeros auxilios", "agua fresca"],
        ["sunburn_first_aid_mountain", "medical_shock_signs_and_response"],
        [MEDLINE_BURNS, MINSALUD_QUEMADURAS],
        ["cómo aliviar una quemadura de sol después del sendero", "puedo calentar manos congeladas con una estufa o fogata"],
    ),
    (
        "lightning_wait_30_minutes_and_shelters",
        "refugio y espera tras los rayos",
        "safety",
        [
            "una carpa protege contra los rayos en una tormenta",
            "cuánto tiempo debo esperar después del último trueno para salir",
            "dónde refugiarse de una tormenta eléctrica en la montaña",
            "sirve un kiosco o cobertizo abierto para protegerse de rayos",
            "es seguro meterse en un carro de techo duro durante rayos",
            "regla de los 30 minutos después de una tormenta eléctrica",
            "are tents safe from lightning and how long should I wait?",
            "por qué el final de la tormenta eléctrica sigue siendo peligroso",
            "qué refugios sí protegen de una descarga eléctrica",
            "puedo retomar la caminata apenas deje de llover si hubo truenos",
            "cerrar las ventanas del vehículo durante tormenta eléctrica",
            "esperar media hora tras el último trueno antes de caminar",
        ],
        "Las carpas y cobertizos abiertos no protegen contra los rayos: busca una edificación cerrada o un vehículo de techo rígido con ventanas subidas. No retomes la actividad al aire libre hasta que pasen al menos 30 minutos desde el último trueno, pues el inicio y el final de la tormenta son muy peligrosos.",
        [
            "Recuerda que las carpas no aíslan de los rayos: resguárdate en una construcción cerrada o vehículo de techo rígido y espera mínimo 30 minutos tras el último trueno antes de salir."
        ],
        ["tormenta eléctrica", "30 minutos", "refugio"],
        ["lightning_storm_safety", "lightning_caught_in_open_paramo", "lightning_strike_victim_first_aid"],
        [CDC_LIGHTNING, IDIGER],
        ["y si hay tormenta eléctrica, cierran?", "qué hago si me agarra una tormenta de rayos en campo abierto"],
    ),
    (
        "lightning_caught_in_open_paramo",
        "tormenta eléctrica en campo abierto",
        "safety",
        [
            "qué hago si me agarra una tormenta de rayos en campo abierto",
            "cómo actuar en el páramo si hay rayos y no hay refugio",
            "debo acostarme en el suelo durante una tormenta eléctrica",
            "por qué el grupo debe separarse si caen rayos en el sendero",
            "es peligroso refugiarse debajo de una roca o acantilado con rayos",
            "alejarse de lagunas cumbres y cercas de alambre en tormenta",
            "what to do if caught in the open during a lightning storm?",
            "bajar de los filos y cumbres cuando empieza a tronar",
            "por qué no ponerse bajo un árbol solitario en tormenta",
            "distancia entre compañeros durante tormenta eléctrica en ruta",
            "qué lugares abiertos son más peligrosos cuando caen rayos",
            "medidas de emergencia a cielo abierto con truenos",
        ],
        "Si una tormenta eléctrica te sorprende sin refugio, baja de inmediato de cumbres, filos y lomas, aléjate de lagunas, cercas y objetos metálicos, no te resguardes bajo árboles aislados ni cornisas de roca y nunca te acuestes plano en el suelo. Si vas en grupo, sepárense entre sí para reducir el riesgo de varios heridos.",
        [
            "A cielo abierto con rayos: desciende de cumbres y filos, aléjate del agua, rocas salientes, árboles aislados y metales, no te acuestes en el suelo y sepárate unos metros del resto del grupo."
        ],
        ["rayos", "campo abierto", "cumbre"],
        ["lightning_storm_safety", "lightning_wait_30_minutes_and_shelters", "lightning_strike_victim_first_aid"],
        [CDC_LIGHTNING, IDIGER],
        ["y si hay tormenta eléctrica, cierran?", "una carpa protege contra los rayos en una tormenta"],
    ),
    (
        "lightning_strike_victim_first_aid",
        "ayuda si un rayo alcanza a alguien",
        "procedure",
        [
            "es peligroso tocar a alguien que fue alcanzado por un rayo",
            "una persona impactada por un rayo queda con corriente",
            "primeros auxilios para una víctima de rayo",
            "qué hacer si un rayo golpea a un compañero en la montaña",
            "el rayo puede causar paro cardíaco qué hago",
            "cómo atender a un herido por descarga eléctrica de rayo",
            "is it safe to touch a lightning strike victim and give first aid?",
            "reanimación RCP a una persona alcanzada por un rayo",
            "aislar del suelo frío a un herido por rayo",
            "pasos de emergencia si cae un rayo cerca del grupo",
            "evaluar pulso y respiración tras impacto de rayo",
            "ayudar a víctima de rayo sin ponernos en riesgo",
        ],
        "Las personas alcanzadas por un rayo no retienen carga eléctrica y es seguro tocarlas. Verifica primero que el sitio sea seguro, pide ayuda urgente al guía y a emergencias, y revisa si respira y tiene pulso; si no tiene pulso, inicia compresiones de RCP de inmediato y aísla su cuerpo del suelo frío y húmedo.",
        [
            "Es seguro tocar a una víctima de rayo: pide ayuda urgente, verifica la seguridad del lugar y, si no respira o no tiene pulso, inicia RCP de inmediato."
        ],
        ["víctima de rayo", "RCP", "primeros auxilios"],
        ["lightning_storm_safety", "unresponsive_cpr", "thermal_burn_first_aid_camp"],
        [CDC_LIGHTNING, MEDLINE_CPR],
        ["y si hay tormenta eléctrica, cierran?", "la persona no responde qué hago"],
    ),
    (
        "suspected_fracture_first_aid",
        "primeros auxilios ante sospecha de fractura",
        "procedure",
        [
            "qué hago si alguien se fractura una pierna o brazo en el sendero",
            "cómo inmovilizar una posible fractura en la montaña",
            "debo intentar acomodar o enderezar un hueso roto",
            "cómo saber si una férula o vendaje quedó muy apretado",
            "primeros auxilios para hueso roto o fractura abierta",
            "qué hacer si el hueso asoma por la herida tras una caída",
            "first aid for a suspected broken bone on a trail",
            "inmovilizar por encima y por debajo de la fractura",
            "revisar circulación en los dedos después de entablillar",
            "diferencia de manejo si sospecho fractura en la ruta",
            "no apoyar ni mover una extremidad fracturada",
            "cómo improvisar una férula acolchada mientras llega ayuda",
        ],
        "Si sospechas una fractura, mantén quieta a la persona y nunca intentes enderezar el hueso. Si hay herida abierta, cúbrela con un apósito limpio sin presionar el hueso; inmoviliza por encima y por debajo con una férula acolchada sin apretar (vigila que los dedos no se pongan pálidos, azules o entumidos) y avisa al guía.",
        [
            "No muevas ni intentes alinear el hueso fracturado: inmoviliza la extremidad por encima y por debajo sin cortar la circulación, abrígala para prevenir shock y pide rescate al guía."
        ],
        ["fractura", "inmovilización", "férula"],
        ["sprain_first_aid", "head_or_spine_injury_fall", "medical_shock_signs_and_response"],
        [MEDLINE_FRACTURES, MINSALUD_INMOV, RES207],
        ["me torcí el tobillo en el sendero", "qué hacer si alguien se golpea fuerte la cabeza al caer"],
    ),
    (
        "head_or_spine_injury_fall",
        "golpe en la cabeza o la columna",
        "procedure",
        [
            "qué hacer si alguien se golpea fuerte la cabeza al caer",
            "primeros auxilios por trauma en la cabeza o columna",
            "debo quitarle el casco a un montañista o ciclista que cayó",
            "cómo actuar si alguien cae de altura y le duele el cuello",
            "qué hago si una persona con golpe en la cabeza va a vomitar",
            "señales de alarma después de un golpe en la cabeza",
            "first aid for a head or spinal injury after a fall",
            "no mover a un herido con posible lesión de columna",
            "sostener la cabeza alineada con el cuello tras una caída",
            "vómito somnolencia o pupilas desiguales tras golpe craneal",
            "por qué toda caída fuerte puede tener trauma cervical",
            "cuándo pedir rescate urgente por golpe en la cabeza",
        ],
        "Ante una caída fuerte o golpe en la cabeza, asume lesión de columna cervical: no muevas a la persona salvo peligro inminente, no le quites el casco y sostén su cabeza alineada con el cuello. Si vomita, giren cabeza, cuello y cuerpo en bloque de lado; pide rescate urgente al guía si hay somnolencia, confusión o vómito.",
        [
            "No muevas a quien sufrió un golpe craneal o caída fuerte ni le quites el casco: mantén su cabeza y cuello alineados sin movimiento y solicita ayuda médica urgente al guía."
        ],
        ["golpe en la cabeza", "columna cervical", "caída"],
        ["suspected_fracture_first_aid", "nosebleed_altitude", "unresponsive_cpr"],
        [MINSALUD_INMOV, MEDLINE_HEAD, RES207],
        ["qué hago si alguien se fractura una pierna o brazo en el sendero", "me sangra la nariz en la montaña"],
    ),
    (
        "minor_cuts_and_punctures_care",
        "cuidado de cortadas leves o heridas punzantes",
        "procedure",
        [
            "cómo limpiar una cortada o raspón en el sendero",
            "qué hago si me clavo una espina o astilla profunda",
            "debo sacar un objeto que quedó clavado en una herida",
            "primeros auxilios para heridas leves o punzantes",
            "cómo lavar una herida para que no se infecte en la ruta",
            "cuántos minutos enjuagar un pinchazo o herida punzante",
            "how to clean minor cuts and puncture wounds on a hike",
            "lavarse las manos y lavar el corte con agua y jabón suave",
            "qué hacer si se rompe una punta dentro de la herida",
            "cubrir un raspón o cortada con vendaje limpio",
            "riesgo de infección en heridas sucias o en los pies",
            "cuidados básicos de una herida leve en montaña",
        ],
        "Para cortadas leves, lávate las manos, lava bien la herida con agua limpia y jabón suave, haz presión directa si sangra y cúbrela con un vendaje limpio. Si es una herida punzante, enjuágala 5 minutos con agua; si hay un objeto clavado en la herida, no lo retires ni escarbes y busca atención médica.",
        [
            "Lava la cortada con agua limpia y jabón suave tras lavarte las manos y cúbrela con un apósito limpio; si hay un objeto incrustado en la herida, no lo saques y acude a urgencias."
        ],
        ["cortada", "herida punzante", "limpieza"],
        ["bleeding_control", "blister_care"],
        [MEDLINE_CUTS, RES207],
        ["cómo paro una hemorragia", "me salió una ampolla en el pie"],
    ),
    (
        "medical_shock_signs_and_response",
        "reconocer y actuar ante el shock",
        "procedure",
        [
            "cuáles son los síntomas de shock tras un accidente",
            "piel pálida fría y sudorosa después de una lesión",
            "qué hacer si un herido entra en estado de shock",
            "puedo darle agua o comida a una persona en shock",
            "posición para acostar a alguien en shock sin trauma de columna",
            "labios azules pulso rápido y debilidad tras hemorragia",
            "how to recognize and treat medical shock in first aid",
            "por qué abrigar y aflojar la ropa a una persona en shock",
            "elevar las piernas 30 centímetros si no hay fractura ni golpe espinal",
            "el shock médico es una urgencia que pone en riesgo la vida",
            "qué no hacer nunca cuando alguien presenta signos de shock",
            "cuidar a un lesionado pálido y frío mientras llega el rescate",
        ],
        "El shock por trauma o sangrado causa piel pálida, fría y húmeda, labios o uñas azulados, pulso débil y confusión. Pide ayuda urgente al guía, afloja su ropa, abrígalo para que no pierda calor, no le des nada de comer ni beber y, si no tiene lesión de cabeza, columna o piernas, acuéstalo elevando sus pies 30 cm.",
        [
            "Si un herido tiene piel pálida, fría y sudorosa, confusión o labios azulados, pide rescate urgente, abrígalo acostado, no lo muevas si sospechas trauma espinal y no le des nada por boca."
        ],
        ["shock", "piel fría y pálida", "urgencia"],
        ["bleeding_control", "suspected_fracture_first_aid", "fainting_response"],
        [MEDLINE_SHOCK, RES207],
        ["cómo paro una hemorragia", "alguien se desmayó en el sendero"],
    ),
    (
        "choking_first_aid_heimlich",
        "primeros auxilios por atragantamiento o asfixia",
        "procedure",
        [
            "qué hago si alguien se atraganta con comida en la ruta",
            "cómo hacer la maniobra de Heimlich en primeros auxilios",
            "debo golpear la espalda si la persona está tosiendo fuerte",
            "cómo ayudar a alguien que se ahoga con un bocado y no puede hablar",
            "compresiones abdominales para desobstruir la vía aérea",
            "ciclos de 5 golpes en la espalda y 5 compresiones abdominales",
            "first aid for a choking person who cannot breathe or speak",
            "dónde se pone el puño en la maniobra de Heimlich",
            "qué hacer si una embarazada se atraganta",
            "si la persona atragantada pierde el conocimiento qué hago",
            "primeros auxilios cuando un alimento bloquea la garganta",
            "actuar rápido ante asfixia por atragantamiento",
        ],
        "Si la persona tose con fuerza y puede hablar, no intervengas porque la tos suele expulsar el objeto. Si está consciente pero no puede hablar ni respirar, alterna ciclos de 5 golpes entre los omóplatos y 5 compresiones abdominales hacia adentro y arriba sobre el ombligo; si queda inconsciente, pide ayuda e inicia RCP.",
        [
            "No intervengas si tose con fuerza; si no puede hablar ni respirar, aplica ciclos de 5 golpes entre los omóplatos seguidos de 5 compresiones abdominales sobre el ombligo."
        ],
        ["atragantamiento", "Heimlich", "vía aérea"],
        ["unresponsive_cpr", "fainting_response"],
        [MEDLINE_CHOKING],
        ["la persona no responde qué hago", "alguien se desmayó en el sendero"],
    ),
    (
        "guide_first_aid_kit_and_certification",
        "botiquín y primeros auxilios del guía",
        "procedure",
        [
            "qué lleva el guía para primeros auxilios",
            "el guía del parque está capacitado en primeros auxilios y RCP",
            "es obligatorio que el guía lleve botiquín y radio",
            "qué certificación médica o de rescate tienen los guías avalados",
            "el guía lleva desfibrilador o curso de RCP vigente",
            "por qué exige el parque guías con radio y botiquín",
            "do park guides carry a first aid kit and CPR certification?",
            "requisitos de primeros auxilios para guías en Los Nevados",
            "dotación obligatoria de seguridad del guía o intérprete",
            "certificado presencial de 20 horas en primeros auxilios y RCP",
            "quién presta los primeros auxilios durante la caminata",
            "equipo médico y radio de comunicación del guía registrado",
        ],
        "Según la Resolución 207 de 2023, todo guía o intérprete autorizado en Los Nevados debe tener certificado presencial vigente de 20 horas en primeros auxilios (con RCP y DEA) y portar obligatoriamente botiquín de primeros auxilios, radio portable y filtro de agua. Acude siempre a tu guía ante cualquier síntoma o lesión.",
        [
            "Tu guía avalado cuenta con curso presencial vigente de 20 horas en primeros auxilios y RCP, y lleva botiquín y radio obligatorios para atender y reportar emergencias."
        ],
        ["botiquín", "guía avalado", "RCP"],
        ["tell_guide_about_health_change", "evacuation_and_rescue_reality", "services.first_aid_points"],
        [RES207, PNN],
        ["a quién le digo que me siento mal", "cómo me sacan del parque si me enfermo o me fracturo"],
    ),
    (
        "pre_hike_health_disclosure_and_induction",
        "inducción y aviso de tu estado de salud",
        "procedure",
        [
            "es obligatorio recibir la charla de inducción al entrar al parque",
            "debo avisar antes del recorrido si tengo una lesión o alergia",
            "qué explican en la charla de inducción de seguridad",
            "a quién informo si tengo un problema muscular o cardíaco previo",
            "por qué prestar atención a la inducción de Parques Nacionales",
            "llevar medicamentos formulados si sufro de una alergia",
            "is the safety induction talk mandatory before entering?",
            "informar con anterioridad lesiones o discapacidad al operador",
            "qué recomendaciones de emergencia dan en el punto de ingreso",
            "declarar condiciones médicas antes de empezar la caminata",
            "importancia de la charla preventiva antes de subir al páramo",
            "avisar al guía sobre medicamentos personales y lesiones previas",
        ],
        "Al ingresar al parque es obligatorio recibir la charla presencial de inducción sobre riesgos naturales y cómo actuar en emergencias. Además, debes informar antes de salir al operador, guía o guardaparques si tienes alguna lesión, alergia, problema cardíaco, muscular o discapacidad, y portar tus medicamentos formulados.",
        [
            "Asiste siempre a la charla presencial obligatoria de inducción al ingresar, lleva tus medicamentos formulados e informa al guía antes de salir cualquier lesión o condición de salud."
        ],
        ["charla de inducción", "lesiones previas", "prevención"],
        ["tell_guide_about_health_change", "pretrip_medical_advice", "guide_first_aid_kit_and_certification"],
        [RES207, PNN_FIRST],
        ["a quién le digo que me siento mal", "debo preguntarle al médico antes de ir"],
    ),
    (
        "stay_together_prevent_separation",
        "permanecer en grupo para evitar extravíos",
        "safety",
        [
            "cómo evitar que alguien se quede atrás o se pierda en el grupo",
            "por qué no debo adelantarme ni separarme del guía en el sendero",
            "qué significa mantener contacto visual y auditivo con el grupo",
            "es peligroso quedarse rezagado tomando fotos en la niebla",
            "cómo previene el guía que el grupo se fragmente",
            "regla de caminar unidos durante todo el recorrido",
            "how to prevent getting separated from the hiking group?",
            "no dejar a ningún compañero solo o rezagado en la montaña",
            "por qué el grupo no debe dividirse en el páramo",
            "avisar al guía si necesito parar para que el grupo no se separe",
            "riesgo de fragmentar el grupo en senderos de alta montaña",
            "caminar siempre a la vista del guía y de los compañeros",
        ],
        "Para prevenir extravíos en alta montaña, la reglamentación exige que el grupo camine unido sin fragmentarse y que el guía mantenga contacto visual y auditivo con todos. No te adelantes ni te quedes rezagado por tu cuenta; si alguien camina más lento o necesita parar, avisen de inmediato al guía para ajustar el ritmo.",
        [
            "Camina siempre unido al grupo manteniendo contacto visual y auditivo con el guía; nunca te adelantes ni dejes que un compañero quede rezagado."
        ],
        ["grupo unido", "prevención de extravío", "sendero"],
        ["lost_person_protocol", "tell_guide_about_health_change"],
        [RES207],
        ["qué hago si me pierdo en la montaña", "a quién le digo que me siento mal"],
    ),
    (
        "mountaineer_contingency_and_first_aid",
        "plan de contingencias y seguridad para montañistas",
        "procedure",
        [
            "qué es el plan de riesgos y contingencias para montañistas",
            "qué requisitos de seguridad médica piden para montañismo deportivo",
            "debo dejar un contacto de emergencia si voy a hacer montañismo",
            "quiénes deben presentar plan de contingencias en el centro de inducción",
            "seguro de rescate y contacto de emergencia para expediciones",
            "qué documento de riesgos presentan los deportistas de montaña",
            "what contingency plan is required for sport mountaineers?",
            "prevención y manejo de emergencias en montañismo y escalada",
            "datos de contacto en caso de emergencia para el itinerario",
            "obligaciones de seguridad para grupos expedicionarios en Los Nevados",
            "presentar plan de riesgos en la reserva y en la inducción",
            "preparación técnica y plan de emergencia para montañismo",
        ],
        "Si ingresas por montañismo deportivo, debes presentar en la reserva y en el centro de inducción un plan de riesgos y contingencias que evalúe los peligros de tu itinerario, describa el manejo de emergencias e incluya los datos de un contacto de emergencia, además de portar el seguro obligatorio de accidentes y rescate.",
        [
            "Los grupos de montañismo deportivo deben entregar su plan de riesgos y contingencias con contacto de emergencia, adquirir el seguro de rescate y asistir a la inducción obligatoria."
        ],
        ["montañismo", "plan de contingencias", "contacto de emergencia"],
        ["evacuation_and_rescue_reality", "pre_hike_health_disclosure_and_induction", "guide_first_aid_kit_and_certification"],
        [RES207, PNN_FIRST],
        ["cómo me sacan del parque si me enfermo o me fracturo", "es obligatorio recibir la charla de inducción al entrar al parque"],
    ),
]


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    return " ".join(re.findall(r"\w+", "".join(c for c in text if not unicodedata.combining(c))))


def main() -> None:
    entries = []
    for slug, label, kind, examples, short, variants, tags, related, sources, hard_negatives in items:
        if len(examples) < 12:
            raise ValueError(f"{slug} has fewer than 12 examples")
        if len(set(examples)) != len(examples):
            raise ValueError(f"{slug} has duplicate examples")
        if len(short) > 320:
            raise ValueError(f"{slug} answer.short exceeds 320 chars ({len(short)})")
        entry = {
            "id": f"health_safety.{slug}",
            "label": label,
            "kind": kind,
            "audience": "visitor",
            "lang": "es",
            "examples": examples,
            "hard_negatives": hard_negatives,
            "answer": {"short": short, "variants": variants},
            "sources": sources,
            "last_verified": TODAY,
            "related": [x if "." in x else f"health_safety.{x}" for x in related],
            "tags": tags,
        }
        entries.append(entry)

    # Check global uniqueness of examples across all sections
    other_examples: dict[str, str] = {}
    for path in sorted(SECTIONS.glob("*.json")):
        if path == OUT:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for e in data.get("entries", []):
            for ex in e.get("examples", []):
                other_examples[fold(ex)] = e["id"]

    seen_self: dict[str, str] = {}
    for e in entries:
        for ex in e["examples"]:
            key = fold(ex)
            if key in other_examples:
                raise ValueError(f"Cross-section collision: {ex!r} in {e['id']} and {other_examples[key]}")
            if key in seen_self:
                raise ValueError(f"Intra-section collision: {ex!r} in {e['id']} and {seen_self[key]}")
            seen_self[key] = e["id"]

    for e in entries:
        own_keys = {fold(ex) for ex in e["examples"]}
        for hn in e["hard_negatives"]:
            hkey = fold(hn)
            if hkey in own_keys:
                raise ValueError(f"hard_negative in own examples: {hn!r} in {e['id']}")
            if hkey not in seen_self and hkey not in other_examples:
                raise ValueError(f"hard_negative not found verbatim in any example: {hn!r} in {e['id']}")

    section = {
        "contract_version": 1,
        "id": "health_safety",
        "order": 2,
        "title": "Salud y seguridad en alta montaña",
        "description": "Orientación general para reconocer malestares de altura, frío, sol y deshidratación, primeros auxilios básicos, pedir ayuda y visitar Los Nevados con precaución.",
        "retrieval": {
            "profile": "safety",
            "bm25_weight": 0.25,
            "top_k": 3,
            "min_score": None,
        },
        "clarification": {
            "between_entries": "¿Te preocupa {label_a} o {label_b}?",
            "bank": [
                "¿Qué síntomas tienes y desde cuándo?",
                "¿La persona afectada es adulta, niña, gestante o adulta mayor?",
                "¿Estás con un guía avalado o personal del parque?",
                "¿La persona está consciente, alerta y respira con normalidad?",
                "¿Tu duda es sobre altura, frío, deshidratación o primeros auxilios por una lesión?",
                "¿Tienes señal para llamar al 123 o estás con un guía con radio?",
            ],
            "fallback": "Puedo orientarte sobre mal de altura, aclimatación, frío, radiación solar, deshidratación, primeros auxilios básicos y cómo pedir ayuda; si es urgente, avisa de inmediato a tu guía o al personal del parque.",
        },
        "featured": [
            "health_safety.altitude_sickness_symptoms",
            "health_safety.severe_altitude_warning_signs",
            "health_safety.hypothermia_warning_signs",
            "health_safety.acclimatization_plan",
            "health_safety.national_emergency_number_123",
        ],
        "entries": entries,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}: {len(entries)} entries, {sum(len(e['examples']) for e in entries)} examples")


if __name__ == "__main__":
    main()
