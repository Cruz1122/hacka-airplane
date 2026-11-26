"""Round-2 audit overrides for the `preparation` section.

Applied by build_preparation.py after the entry modules are built, so the original
generator modules stay intact and every change is listed here.

Rules used for each entry (see evidence/quotes.md for the verbatim support):
- Every published entry names the source whose raw file states its advice. No entry is
  published on a generic page: a source that does not state the advice is a false attribution.
- Keep and rewrite the answer to what the quoted source says, with no added figures or claims.
- Remove an entry when no downloaded source states its advice (REMOVED, with the reason).
- Merge an entry into a survivor when the same quote covers both (MERGED): examples move to the
  survivor, which keeps its id. LABELS renames a survivor whose id is kept.

Raw files (paths relative to the research notes folder):
- activities/evidence/resolucion-207-2023.txt          Res. 207 de 2023 (park regulation)
- preparation/evidence/raw/pnn_nevados_ficha_2026-11-21.txt  PNN Los Nevados official page
- preparation/evidence/raw/pnn_semana_santa_2018_2026-11-21.txt  PNN advisory, Semana Santa 2018 (dated)
- preparation/evidence/raw/res098_2021_cumbres_2026-11-21.txt   Res. 098 de 2021, event permit at Santa Isabel (dated, event-specific)
- preparation/evidence/raw/lineamientos_montana_2018_2026-11-21.txt  PNN mountain sports guidelines, 2018 (national)
- preparation/evidence/raw/colombia_travel_paramos_2026-11-21.txt  Colombia.travel páramo page (tourism portal)
"""

import copy

RETRIEVED = "2026-11-21"

SOURCES = {
    "R207": {
        "label": "Parques Nacionales Naturales de Colombia · Resolución 207 de 2023",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf",
    },
    "FICHA": {
        "label": "Parques Nacionales Naturales de Colombia · Los Nevados",
        "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    },
    "SS2018": {
        "label": "Parques Nacionales Naturales de Colombia · Recomendaciones Semana Santa 2018 (Los Nevados, dato de 2018)",
        "url": "https://old.parquesnacionales.gov.co/portal/es/recomendaciones-para-ingresar-al-pnn-los-nevados-esta-temporada-de-semana-santa-2018/",
    },
    "R098": {
        "label": "Parques Nacionales Naturales de Colombia · Resolución 098 de 2021 (evento en Santa Isabel, dato de 2021)",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2021/08/resolucion-no-098-del-10-de-agosto-de-2021.pdf",
    },
    "LIN2018": {
        "label": "Parques Nacionales Naturales de Colombia · Lineamientos de actividades deportivas de montaña y escalada (2018, nacional, no específico de Los Nevados)",
        "url": "https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2018/08/Documento-Lineamientos-Deportes-de-Montan%CC%83a-en-PNN-2018-1.pdf",
    },
    "CT": {
        "label": "Colombia.travel · Páramos en Colombia: planes de turismo de altura (portal oficial de turismo)",
        "url": "https://colombia.travel/es/blog/paramos-en-colombia-planes-imperdibles-de-turismo-de-altura",
    },
}

# Raw file behind each source key, used by check_quotes.py to verify digits.
RAW_FILES = {
    "R207": "activities/evidence/resolucion-207-2023.txt",
    "FICHA": "preparation/evidence/raw/pnn_nevados_ficha_2026-11-21.txt",
    "SS2018": "preparation/evidence/raw/pnn_semana_santa_2018_2026-11-21.txt",
    "R098": "preparation/evidence/raw/res098_2021_cumbres_2026-11-21.txt",
    "LIN2018": "preparation/evidence/raw/lineamientos_montana_2018_2026-11-21.txt",
    "CT": "preparation/evidence/raw/colombia_travel_paramos_2026-11-21.txt",
}

# Entries removed from the section, with the reason logged in the research log.
REMOVED = {
    "cotton_risk": "safety claim (hypothermia, cotton) without an official source",
    "hydration_bladder_freeze": "freezing claim without an official source",
    "cold_battery_drain": "battery-cold claim without an official source",
    "whistle_emergency": "emergency safety claim without an official source",
    "electrolytes": "medical-adjacent claim, belongs to health_safety and has no source",
    "children_snacks_hydration": "child hydration instruction without an official source; health overlap",
    "trekking_pants": "no downloaded source names pants or their fabric; advice without source",
    "rubber_boots": "rubber boots for mud have no source; the volunteer sheet only lists 'botas plásticas' without use or context for visitors",
    "break_in_boots": "advice to break in boots before the trip has no source",
    "gaiters": "gaiters (polainas) do not appear in any downloaded source",
    "thermal_socks": "thermal socks do not appear in any downloaded source",
    "lip_balm": "lip balm does not appear in any downloaded source; the sunscreen quotes name sunscreen only",
    "skin_moisturizer": "moisturizer does not appear in any downloaded source",
    "trekking_backpack": "multi-day trekking backpack does not appear in any downloaded source; the only 'morral' in official text is a small or short-trip pack",
    "backpack_rain_cover": "pack rain cover does not appear in any downloaded source; 'funda de vivac' is a bivy sack, not a pack cover",
    "trekking_poles": "'bastones telescópicos' appear only in the gear list of a 2021 summit event permit at Santa Isabel, not as general advice",
    "thermal_flask": "thermal flask with hot drink does not appear in any downloaded source",
}

# Entries merged into a survivor because one quote covers them (same quote => one entry).
# Examples move to the survivor; the survivor keeps its id. The survivor's label is set in LABELS.
MERGED = {
    "first_layer_thermal": ["insulation_jacket", "waterproof_overpants", "spare_clothing"],
}
ABSORBED = {part for parts in MERGED.values() for part in parts}

LABELS = {
    "first_layer_thermal": "ropa térmica, impermeable y de repuesto",
}

# id -> (source keys, answer dict). Answers carry only quoted facts or general advice.
REWRITTEN = {
    "layering_system": (["R207", "FICHA"], {
        "short": "Para Los Nevados lleva ropa abrigada e impermeable. La Resolución 207 de 2023 la pide para senderismo, y el parque advierte de climas fríos inferiores a 0 ºC y lluviosos. Vístete en capas para quitarte o ponerte prendas según el clima.",
        "variants": ["Lleva ropa abrigada e impermeable para el frío y la lluvia del parque. Empaca en capas para regular el calor."],
        "detail": "Resolución 207 de 2023, numeral 6.1: ropa impermeable y ropa abrigada. Ficha oficial: ropa y calzado apropiado para climas fríos inferiores a 0 ºC y lluviosos.",
    }),
    "first_layer_thermal": (["SS2018", "LIN2018", "CT"], {
        "short": "Lleva ropa térmica, impermeable y un cambio extra por si llueve. Según la guía de Semana Santa 2018 del PNN, la ropa debe ser adecuada para clima frío e impermeable.",
        "variants": ["Empaca ropa térmica y un cambio extra por si llueve: así lo recomienda Colombia.travel para los páramos."],
        "detail": "Guía de Semana Santa 2018 del PNN (dato de 2018): ropa adecuada para clima frío, impermeable. Lineamientos PNN de montaña (2018, nacional): vestimenta térmica e impermeable. Colombia.travel: ropa térmica y un cambio extra por si llueve.",
    }),
    "second_layer_fleece": (["R207"], {
        "short": "Como segunda capa, usa un buzo o chaqueta de forro polar o micropolar que abrigue sin ser muy pesado para caminar.",
        "variants": ["Un forro polar o una chaqueta liviana sirve de capa de abrigo intermedia."],
        "detail": "Resolución 207 de 2023, numeral 6.1: ropa abrigada para soportar temperaturas extremas de frío en cabeza, tórax y extremidades.",
    }),
    "third_layer_waterproof": (["R207"], {
        "short": "Como capa exterior, lleva una chaqueta impermeable y cortavientos con capucha. La Resolución 207 de 2023 exige ropa impermeable en el equipo mínimo para recorrer los senderos.",
        "variants": ["Lleva chaqueta impermeable con capucha por si llueve en el sendero: la Resolución 207 la incluye en el equipo mínimo."],
        "detail": None,
    }),
    "rain_poncho": (["R207"], {
        "short": "Lleva chaqueta impermeable, que la Resolución 207 de 2023 pide. Si usas poncho, que sea reutilizable: el parque prohíbe los plásticos de un solo uso.",
        "variants": ["Para la lluvia, usa chaqueta impermeable. Un poncho desechable de plástico no es admitido en el parque."],
        "detail": "Resolución 207 de 2023 sobre plásticos: no ingresar plásticos de un solo uso, prohibido de acuerdo a la Resolución 1558 de 2019.",
    }),
    "hiking_boots": (["R207", "FICHA"], {
        "short": "Usa zapatos cómodos y preferiblemente impermeables, con suela que agarre bien. La Resolución 207 de 2023 los incluye en el equipo mínimo para los senderos del parque.",
        "variants": ["Lleva zapatos cómodos, preferiblemente impermeables, para caminar. Evita los tenis de suela lisa."],
        "detail": "Resolución 207 de 2023, numeral 6.1: zapatos cómodos preferiblemente impermeables. Ficha oficial: calzado apropiado para climas fríos inferiores a 0 ºC y lluviosos.",
    }),
    "thermal_gloves": (["R207"], {
        "short": "La Resolución 207 de 2023 incluye guantes en el equipo mínimo para los senderos. Lleva guantes que abriguen para el frío del páramo.",
        "variants": ["Para el páramo, lleva guantes que abriguen: la resolución los incluye en el equipo mínimo."],
        "detail": "Resolución 207 de 2023, numeral 6.1: guantes.",
    }),
    "thermal_hat": (["R207"], {
        "short": "La Resolución 207 de 2023 pide ropa abrigada para soportar temperaturas extremas de frío en cabeza, tórax y extremidades. Lleva un gorro que abrigue la cabeza.",
        "variants": ["Protege la cabeza con un gorro abrigado: la resolución pide ropa abrigada también para la cabeza."],
        "detail": None,
    }),
    "neck_gaiter": (["R207"], {
        "short": "La Resolución 207 de 2023 incluye el pasa montañas en el equipo mínimo para senderismo. Lleva un pasamontañas o cuello térmico para cubrirte el cuello y la cara del viento.",
        "variants": ["Lleva pasa montañas o cuello térmico: la resolución lo incluye en el equipo mínimo para los senderos."],
        "detail": None,
    }),
    "sunglasses_uv": (["R207", "FICHA"], {
        "short": "Lleva gafas con protección ultravioleta 100% (UV). La Resolución 207 de 2023 las exige en el equipo mínimo de senderismo.",
        "variants": ["Usa gafas UV 100% para caminar en los senderos autorizados: el parque las exige."],
        "detail": "Ficha oficial: usa gafas con protección UV. Resolución 207 de 2023, numeral 6.1: gafas con protección ultravioleta 100% (UV).",
    }),
    "sunscreen": (["R207", "FICHA"], {
        "short": "Lleva bloqueador solar con factor 50 como mínimo, que pide la Resolución 207 de 2023. Aplícatelo cada dos horas, antes y durante la caminata.",
        "variants": ["Usa bloqueador factor 50 o más y reaplícalo cada dos horas: el parque lo pide para el sol de altura."],
        "detail": "Ficha oficial: aplícate bloqueador solar cada dos horas (antes y durante).",
    }),
    "sun_hat": (["R207"], {
        "short": "Una gorra o sombrero ayuda a cubrir la cara del sol, pero no reemplaza el bloqueador ni las gafas UV que pide la Resolución 207 de 2023.",
        "variants": ["Lleva gorra o sombrero como complemento; el bloqueador y las gafas UV siguen siendo obligatorios."],
        "detail": None,
    }),
    "daypack_size": (["R207"], {
        "short": "La Resolución 207 de 2023 exige un morral pequeño en el equipo mínimo para los senderos autorizados. Lleva uno cómodo para tus prendas, agua y snacks.",
        "variants": ["Para el sendero, lleva un morral pequeño: es parte del equipo mínimo que pide la resolución."],
        "detail": "Resolución 207 de 2023, numeral 6.1: morral pequeño.",
    }),
    "dry_bags": (["LIN2018"], {
        "short": "Usa una bolsa seca con cierre estanco para guardar lo que debe quedar totalmente seco durante la caminata.",
        "variants": ["Para que nada se moje, guarda tus objetos en una bolsa seca con cierre estanco."],
        "detail": "Lineamientos PNN de montaña (2018), glosario: bolsa seca con cierre estanco, bolsa que permite guardar objetos que se mantendrán totalmente secos.",
    }),
    "water_quantity": (["FICHA", "R207"], {
        "short": "El PNN recomienda hidratarte antes, durante y después de la actividad, y la Resolución 207 pide llevar cantimplora. Bebe pequeños sorbos durante todo el recorrido.",
        "variants": ["Hidrátate antes, durante y después de caminar, como indica el parque. Lleva cantimplora."],
        "detail": "Ficha oficial: ten una buena hidratación antes, durante y después de la actividad.",
    }),
    "reusable_bottles": (["R207"], {
        "short": "Lleva cantimplora o botella reutilizable, que pide la Resolución 207 de 2023. Los plásticos de un solo uso no pueden ingresar al parque.",
        "variants": ["Usa cantimplora reutilizable: la resolución prohíbe ingresar plásticos de un solo uso."],
        "detail": "Resolución 207 de 2023: no ingresar plásticos de un solo uso, prohibido de acuerdo a la Resolución 1558 de 2019.",
    }),
    "trail_snacks": (["R207", "FICHA"], {
        "short": "La Resolución 207 de 2023 exige alimentos ligeros, listos para consumir y ricos en calorías. Lleva snacks energéticos para la caminata.",
        "variants": ["Empaca snacks energéticos listos para comer: la resolución los incluye en el equipo mínimo para senderismo."],
        "detail": "Resolución 207 de 2023, numeral 6.1: alimentos ligeros listos para consumir y ricos en calorías. Ficha oficial: aliméntate bien y come snacks energéticos.",
    }),
    "pre_hike_meal": (["SS2018", "FICHA"], {
        "short": "Según la guía oficial de Semana Santa 2018, consume carbohidratos y líquido antes de la visita. Durante el recorrido, come snacks energéticos.",
        "variants": ["Antes de la visita, come carbohidratos y bebe líquido: así lo recomendó el PNN en su guía de 2018."],
        "detail": None,
    }),
    "trail_meals_multiday": (["FICHA", "SS2018"], {
        "short": "Al acampar, lleva alimentación apropiada para bajas temperaturas, según la ficha oficial del parque, y una estufa portátil de gas para preparar los alimentos.",
        "variants": ["Para dormir en el parque, lleva comida apropiada para bajas temperaturas y una estufa de gas."],
        "detail": "Guía de Semana Santa 2018: lleve estufa portable para acampar de gas para la preparación de alimentos.",
    }),
    "mountain_tent": (["R207"], {
        "short": "La Resolución 207 de 2023 exige carpas técnicas de alta montaña, de tres o cuatro estaciones, para temperaturas menores a cero grados centígrados.",
        "variants": ["Para acampar, lleva carpa de tres o cuatro estaciones: la resolución la exige para temperaturas bajo cero."],
        "detail": None,
    }),
    "sleeping_bag": (["FICHA", "SS2018"], {
        "short": "Si vas a acampar en las zonas permitidas, lleva carpa y saco de dormir para bajas temperaturas, como indica la ficha oficial del parque.",
        "variants": ["Para acampar, el PNN pide llevar saco de dormir apropiado para bajas temperaturas."],
        "detail": "Guía de Semana Santa 2018: lleve equipos, carpa y sleeping especial para alta montaña y bajas temperaturas.",
    }),
    "sleeping_pad": (["LIN2018"], {
        "short": "Para acampar en montaña, lleva un aislante térmico: está en el equipo mínimo de campamento que pide el PNN.",
        "variants": ["Si acampas, empaca un aislante térmico: el PNN lo lista en el equipo mínimo de campamento para montaña."],
        "detail": "Lineamientos PNN de montaña (2018), numeral 2.8.1, equipo mínimo para campamento: aislante térmico. Documento nacional para deportistas de montaña, no específico de Los Nevados.",
    }),
    "camp_stove": (["FICHA", "SS2018", "R207"], {
        "short": "Para cocinar en campamento, lleva estufa portátil de gas y material de cocina. La Resolución 207 de 2023 prohíbe las fogatas en el parque.",
        "variants": ["No hagas fogatas en el parque: la Resolución 207 las prohíbe. Para cocinar, usa una estufa portátil de gas."],
        "detail": "Ficha oficial: lleva carpa, sleeping, material de cocina y alimentación apropiada para bajas temperaturas. Guía de Semana Santa 2018: lleve estufa portable para acampar de gas.",
    }),
    "cookware_utensils": (["R207"], {
        "short": "Lleva menaje reutilizable para cocinar y comer. La Resolución 1558 de 2019 prohíbe los plásticos de un solo uso en el parque.",
        "variants": ["Usa menaje reutilizable en el campamento: los plásticos de un solo uso no pueden ingresar."],
        "detail": None,
    }),
    "camp_hygiene": (["R207"], {
        "short": "Las excretas se evacúan en cacatubo o en hoyo de gato con la pala que lleva el guía. Cada visitante debe retomar sus residuos, y no está permitido enterrar basura.",
        "variants": ["En campamento, usa cacatubo o hoyo de gato con la pala del guía, y lleva de vuelta tus residuos."],
        "detail": "Resolución 207 de 2023, numeral 6.2: cada visitante deberá retomar sus propios residuos y basuras al lugar de origen.",
    }),
    "headlamp": (["R207"], {
        "short": "La Resolución 207 de 2023 exige linterna frontal y baterías de repuesto en el equipo mínimo para senderismo. Revisa que funcione antes de salir.",
        "variants": ["Lleva linterna frontal con pilas de repuesto: la resolución lo exige para caminar en los senderos."],
        "detail": "Resolución 207 de 2023, numeral 6.1: linterna frontal y baterías de repuesto.",
    }),
    "technical_glacier_gear": (["R207", "R098"], {
        "short": "Para borde de glaciar, ascenso a cumbre o travesía, la Resolución 207 de 2023 exige contratar un guía de turismo o un intérprete del patrimonio. Pregunta a tu guía qué equipo técnico lleva.",
        "variants": ["En glaciar o cumbre, el guía de turismo o intérprete es obligatorio. Pregúntale qué equipo técnico se necesita."],
        "detail": "Resolución 098 de 2021 (evento en Santa Isabel): equipo mínimo para cada 5 personas: cuerda de mínimo 40 metros, arnés, casco.",
    }),
    "fitness_training": (["FICHA"], {
        "short": "El PNN recomienda hacer paradas periódicas de 10 minutos mientras asciendes. Camina a paso pausado y ten buena hidratación.",
        "variants": ["Sube a paso pausado y haz paradas periódicas de 10 minutos, como indica el parque."],
        "detail": None,
    }),
    "children_gear": (["R207", "FICHA"], {
        "short": "Para el niño, empaca ropa abrigada e impermeable, calzado cómodo y ropa de repuesto. La Resolución 207 de 2023 pide esa misma ropa a los visitantes en los senderos.",
        "variants": ["Lleva al niño ropa abrigada, impermeable y una muda de repuesto, como pide la resolución para los senderos."],
        "detail": None,
    }),
    "what_not_to_pack": (["R207"], {
        "short": "No ingreses bebidas alcohólicas, sustancias psicoactivas, plásticos de un solo uso, leña para fogatas, ni equipos de sonido que perturben el ambiente. La Resolución 207 de 2023 lo prohíbe.",
        "variants": ["Evita empacar alcohol, plásticos desechables, parlantes o leña: la resolución prohíbe esas prácticas en el parque."],
        "detail": "Resolución 207 de 2023 prohíbe el ingreso de turistas en estado de alicoramiento o bajo sustancias psicoactivas, hacer fogatas y producir ruidos o utilizar equipos que puedan perturbar el ambiente natural.",
    }),
    "checklist_brisas_day": (["R207", "FICHA"], {
        "short": "Para un pasadía, lleva lo que pide la Resolución 207 de 2023: gafas UV 100%, bloqueador factor 50 como mínimo, linterna frontal con pilas de repuesto, cantimplora, guantes, pasa montañas y morral pequeño.",
        "variants": ["Checklist de pasadía: morral pequeño, ropa impermeable y abrigada, gafas UV 100%, bloqueador factor 50, linterna frontal, cantimplora, guantes y pasa montañas."],
        "detail": "Resolución 207 de 2023, numeral 6.1, equipo mínimo para senderismo, también incluye ropa impermeable y ropa abrigada, y alimentos ligeros listos para consumir y ricos en calorías.",
    }),
    "checklist_glacier_day": (["R207", "R098"], {
        "short": "Para borde de glaciar, la Resolución 207 de 2023 exige guía de turismo o intérprete del patrimonio. Lleva ropa abrigada e impermeable, gafas UV, guantes, pasa montañas y calzado de buen agarre.",
        "variants": ["Antes de subir al glaciar, confirma con tu guía el equipo técnico. El guía de turismo o intérprete es obligatorio."],
        "detail": "Resolución 098 de 2021, evento en Santa Isabel: ropa adecuada para alta montaña, preferiblemente segunda y tercera capa térmica impermeable y/o rompevientos, guantes, gafas con filtro UV, pasamontañas o gorro, calzado de buen agarre y suela gruesa.",
    }),
    "checklist_multiday_trek": (["R207", "SS2018"], {
        "short": "Para acampar varios días, lleva carpa de tres o cuatro estaciones, saco para bajas temperaturas, estufa de gas, linterna frontal, cantimplora y bolsa para retornar la basura.",
        "variants": ["Checklist de campamento: carpa de tres o cuatro estaciones, saco, estufa de gas, linterna, cantimplora y bolsa para la basura."],
        "detail": "Guía de Semana Santa 2018: lleve equipos, carpa y sleeping especial para alta montaña y bajas temperaturas.",
    }),
}

NEW = {
    "navigation_map_gps": {
        "label": "mapa, GPS o brújula para orientarte",
        "sources": ["SS2018"],
        "answer": {
            "short": "Según la guía oficial de Semana Santa 2018, lleva mapa, GPS o brújula, linterna con pilas de repuesto y celular con batería suficiente. Avisa tu ruta a un familiar antes de salir.",
            "variants": ["Para orientarte en el páramo, lleva mapa, GPS o brújula, y deja tu ruta anotada con alguien antes de salir."],
            "detail": None,
        },
        "related": ["preparation.headlamp", "preparation.daypack_size"],
        "hard_negatives": [
            "qué síntomas produce el mal de altura",
            "cuánto cuesta la entrada al parque",
            "a qué hora abren el sector brisas",
        ],
        "examples": [
            "necesito mapa o gps para caminar?",
            "toca llevar brújula al parque",
            "qué llevo para orientarme en el páramo",
            "hay que llevar mapa impreso o con el celular basta",
            "se puede ir sin gps",
            "llevo brujula o no",
            "celular y gps para la ruta, qué me recomiendan",
            "what do I need to navigate the trail",
            "should I bring a compass or a map",
            "cómo me oriento si hay niebla en el sendero",
            "con qué me ubico en la montaña",
            "qué tengo que empacar para no perderme",
        ],
    },
}


def _official_sources(keys):
    # Every entry must name the source whose raw file states its advice. An empty list is refused:
    # falling back to a generic park page is the false attribution this audit removes.
    if not keys:
        raise ValueError("entry without a source: remove it, or name the raw file that states its advice")
    return [
        {"label": SOURCES[k]["label"], "url": SOURCES[k]["url"], "retrieved_at": RETRIEVED}
        for k in keys
    ]


def apply(entries, valid_examples_elsewhere):
    """Return the section entries after the audit overrides.

    valid_examples_elsewhere: examples of the other sections (kept for the caller's signature;
    hard negatives no longer depend on it, so the build does not depend on corpus state).
    """
    by_id = {e["id"]: e for e in entries}
    for survivor, parts in MERGED.items():
        target = by_id[f"preparation.{survivor}"]
        seen = {x.strip().lower() for x in target["examples"]}
        for part in parts:
            for example in by_id[f"preparation.{part}"]["examples"]:
                if example.strip().lower() not in seen:
                    target["examples"].append(example)
                    seen.add(example.strip().lower())

    kept_ids = set()
    out = []
    for entry in entries:
        short_id = entry["id"].split(".", 1)[1]
        if short_id in REMOVED or short_id in ABSORBED:
            continue
        if short_id in REWRITTEN:
            keys, answer = REWRITTEN[short_id]
            entry["answer"] = copy.deepcopy(answer)
            entry["sources"] = _official_sources(keys)
        if short_id in LABELS:
            entry["label"] = LABELS[short_id]
        out.append(entry)
        kept_ids.add(entry["id"])

    template = next(e for e in entries if e["id"] == "preparation.headlamp")
    for short_id, spec in NEW.items():
        new_entry = copy.deepcopy(template)
        new_entry["id"] = f"preparation.{short_id}"
        new_entry["label"] = spec["label"]
        new_entry["examples"] = list(spec["examples"])
        new_entry["hard_negatives"] = list(spec["hard_negatives"])
        new_entry["answer"] = copy.deepcopy(spec["answer"])
        new_entry["sources"] = _official_sources(spec["sources"])
        new_entry["related"] = list(spec["related"])
        out.append(new_entry)
        kept_ids.add(new_entry["id"])

    by_out = {e["id"]: e for e in out}
    for entry in out:
        # Related: keep only ids that still exist in this section, fall back to layering_system.
        related = [r for r in entry.get("related", []) if r in kept_ids and r != entry["id"]]
        entry["related"] = related[:3] or ["preparation.layering_system"]
        # Hard negatives: keep the authored ones (independent of the rest of the corpus, so the
        # build is reproducible); coordinator_fixes maps any that are not real examples elsewhere
        # through hard_negative_map.json. Only an entry left with fewer than 2 is topped up, from
        # the first examples of its related entries in this section.
        own = {x.casefold() for x in entry["examples"]}
        hn = list(dict.fromkeys(h for h in entry.get("hard_negatives", []) if h.casefold() not in own))
        for rid in entry["related"]:
            if len(hn) >= 2:
                break
            candidate = by_out[rid]["examples"][0]
            if candidate not in hn and candidate.casefold() not in own:
                hn.append(candidate)
        entry["hard_negatives"] = hn[:4]
    return out
