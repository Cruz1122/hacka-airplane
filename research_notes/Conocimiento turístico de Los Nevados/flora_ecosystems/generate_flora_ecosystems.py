#!/usr/bin/env python3
"""Rebuild flora_ecosystems.json from the 22 verified entries plus sourced additions."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from entries_round3 import build_round3  # noqa: E402
SECTION_PATH = ROOT / "data/knowledge/sections/flora_ecosystems.json"
VERIFIED = HERE / "verified_22.json"
DATE = "2026-11-21"

PNN = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
IDEAM_PDF = (
    "https://ideam.gov.co/sites/default/files/prensa/boletines/2025-12-29/"
    "informe-del-estado-de-los-glaciares-colombianos-2024.pdf"
)
IDEAM_RUIZ = (
    "https://ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/"
    "glaciares/nevado-del-ruiz"
)
RAMSAR = "https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf"
ROMERALES = "https://www.parquesnacionales.gov.co/sala-prensa/incendio-romerales-parque-los-nevados/"
AFRICA = (
    "https://www.parquesnacionales.gov.co/sala-prensa/noticias/"
    "incendios-forestales-afectan-los-nevados-e-iguaque/"
)
VIVEROS = (
    "https://www.parquesnacionales.gov.co/sala-prensa/noticias/"
    "herencia-colombia-recorre-viveros-del-parque-los-nevados/"
)
POTOSI = (
    "https://www.parquesnacionales.gov.co/sala-prensa/noticias/"
    "asi-es-el-esfuerzo-inmenso-de-restaurar-areas-deforestadas/"
)

REJECTED = {
    "subparamo_transition",
    "frailejon_growth_and_longevity",
    "frailejon_necromass_thermal_jacket",
    "adaptation_leaf_pubescence",
    "puya_paramo_bromeliads",
    "sphagnum_peat_moss",
    "paramo_lichens_rocks",
    "turberas_bogs_peatlands",
    "cushion_bogs_damage_trampling",
    "volcanic_ash_on_glaciers",
    "glaciers_vs_paramo_water_role",
    "paramo_sponge_mechanism",
    "fog_interception_water_cycle",
    "urban_water_supply_cities",
    "nevado_del_ruiz_ice_cap",
    "nevado_del_tolima_glacier",
    "glacier_monitoring_ideam",
    "wildfire_impact_and_recovery",
    "restoration_nurseries_high_mountain",
    "sujeto_de_derechos_ruling",
}


def src(label: str, url: str) -> dict[str, str]:
    return {"label": label, "url": url, "retrieved_at": DATE}


def entry(
    suffix: str,
    label: str,
    kind: str,
    examples: list[str],
    short: str,
    variants: list[str],
    sources: list[dict[str, str]],
    hard_negatives: list[str],
    related: list[str],
    tags: list[str],
) -> dict:
    if suffix in REJECTED:
        raise ValueError(suffix)
    if not 3 <= len(label.split()) <= 8:
        raise ValueError(f"label words: {label}")
    if len(examples) < 12 or len(set(examples)) != len(examples):
        raise ValueError(f"examples: {suffix}")
    if not 2 <= len(hard_negatives) <= 4:
        raise ValueError(f"hard negatives: {suffix}")
    if not 1 <= len(variants) <= 2:
        raise ValueError(f"variants: {suffix}")
    if len(short) > 320:
        raise ValueError(f"short length {len(short)}: {suffix}")
    if not 1 <= len(related) <= 3:
        raise ValueError(f"related: {suffix}")
    return {
        "id": f"flora_ecosystems.{suffix}",
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "answer": {"short": short, "variants": variants},
        "sources": sources,
        "last_verified": DATE,
        "related": [f"flora_ecosystems.{item}" for item in related],
        "tags": tags,
    }


PNN_SRC = src("Parques Nacionales Naturales de Colombia", PNN)
IDEAM_SRC = src("IDEAM, Informe del estado de los glaciares colombianos 2024", IDEAM_PDF)
IDEAM_RUIZ_SRC = src("IDEAM, Nevado del Ruiz", IDEAM_RUIZ)
RAMSAR_SRC = src("Ficha Ramsar CO1781, Complejo de Humedales Laguna del Otún", RAMSAR)


def new_entries() -> list[dict]:
    return [
        entry(
            "subparamo_ruta_dulima",
            "subpáramo en la ruta del Tolima",
            "explanation",
            [
                "que es el subparamo en los nevados",
                "hay subparamo camino al nevado del tolima",
                "en la ruta del dulima se pasa por subparamo",
                "que vegetacion hay entre el bosque y el paramo",
                "como cambia el paisaje subiendo al tolima",
                "la transicion de bosque a glaciar en el sector sur",
                "pisos de vegetacion en la subida al tolima",
                "oiga en quindio-dulima se cruza el subparamo",
                "venga y antes del pajonal que zona hay hacia el tolima",
                "subparamo paramo y superparamo en el mismo recorrido",
                "desde el bosque altoandino hasta el hielo que franjas veo",
                "what vegetation belts are on the Tolima route",
                "is there a subparamo zone on the way to the glacier",
            ],
            "En el sector Quindío-Dulima recorres la transición desde el bosque altoandino hasta el glaciar, pasando por subpáramo, páramo y superpáramo. Prepárate para ese cambio de vegetación y confirma el recorrido con un operador registrado.",
            [
                "Hacia el Tolima, Parques Nacionales describe el paso de bosque altoandino a glaciar por subpáramo, páramo y superpáramo. Confirma esa ruta con un operador registrado."
            ],
            [PNN_SRC],
            ["qué es el páramo", "qué es el superpáramo", "a qué altura está el Ruiz"],
            ["high_andean_forest", "paramo_ecosystem", "superparamo_ecosystem"],
            ["subparamo", "tolima", "transicion"],
        ),
        entry(
            "ruiz_glacier_measured_2024",
            "hielo medido del volcán Ruiz",
            "fact",
            [
                "cuanto hielo le queda al nevado del ruiz",
                "de que tamano es el glaciar del ruiz",
                "area del casquete del ruiz en 2024",
                "el ruiz sigue siendo un nevado grande",
                "cuantos kilometros cuadrados de glaciar tiene el ruiz",
                "se ha encogido mucho el hielo del ruiz",
                "medicion del glaciar kumanday",
                "oiga el ruiz todavia tiene casquete de hielo",
                "comparado con 2022 cuanto hielo perdio el ruiz",
                "es el ruiz el segundo glaciar de colombia",
                "cifra oficial del hielo del nevado del ruiz",
                "how much glacier does Nevado del Ruiz still have",
                "what was the Ruiz ice area in 2024",
            ],
            "El IDEAM estimó el glaciar del Ruiz en 7,17 km² ± 0,30 km² el 20 de febrero de 2024, un 6,6 % menos que los 7,68 km² de 2022. Sigue siendo la segunda masa glaciar del país. Confirma la cifra vigente en el informe del IDEAM.",
            [
                "El 20 de febrero de 2024 el Ruiz tenía 7,17 km² ± 0,30 km² de glaciar, 6,6 % menos que los 7,68 km² de 2022, y sigue siendo la segunda masa del país. Mira el informe vigente del IDEAM."
            ],
            [IDEAM_SRC, IDEAM_RUIZ_SRC],
            ["a qué altura está el Ruiz", "qué nevados hay en el parque", "cómo es el clima en Los Nevados"],
            ["glaciers_snow_presence", "glacier_retreat_climate_change", "tolima_glacier_measured_2024"],
            ["ruiz", "glaciar", "ideam"],
        ),
        entry(
            "tolima_glacier_measured_2024",
            "hielo medido del volcán Tolima",
            "fact",
            [
                "cuanto hielo le queda al nevado del tolima",
                "el glaciar del tolima que tan pequeno quedo",
                "area de hielo del dulima en 2024",
                "el tolima todavia tiene glaciar",
                "cuantos kilometros de nieve tiene el tolima",
                "se derritio mucho el nevado del tolima",
                "medicion oficial del glaciar del tolima",
                "el nino le quito hielo al tolima",
                "oiga el dulima aun esta nevado",
                "comparado con 2022 cuanto perdio el tolima",
                "cifra del ideam para el glaciar del tolima",
                "how big is the Tolima glacier now",
                "did El Niño shrink the Tolima ice cap",
            ],
            "El IDEAM estimó el glaciar del Tolima en 0,45 km² ± 0,04 km² el 20 de febrero de 2024: 8,2 % menos que los 0,49 km² de 2022. Parte de ese retroceso se asocia a El Niño 2023-2024. Confirma la cifra vigente en el IDEAM.",
            [
                "El 20 de febrero de 2024 el Tolima tenía 0,45 km² ± 0,04 km² de glaciar, 8,2 % por debajo de los 0,49 km² de 2022, en parte por El Niño 2023-2024. Revisa el informe vigente del IDEAM."
            ],
            [IDEAM_SRC],
            ["qué nevados hay en el parque", "qué es el superpáramo", "cuándo llueve más en Los Nevados"],
            ["glaciers_snow_presence", "ruiz_glacier_measured_2024", "glacier_retreat_climate_change"],
            ["tolima", "glaciar", "nino"],
        ),
        entry(
            "conejeras_extinct_march_2024",
            "extinción del glaciar Conejeras",
            "fact",
            [
                "el glaciar conejeras todavia existe",
                "se acabo el hielo de conejeras",
                "cuando desaparecio el glaciar conejeras",
                "puedo ver nieve en el sendero conejeras",
                "el sector conejeras del santa isabel aun tiene glaciar",
                "parce el glaciar conejeras ya no existe",
                "el ideam cerro el monitoreo de conejeras",
                "cuantos anos midieron el glaciar conejeras",
                "la cumbre de conejeras sigue con hielo",
                "oiga conejeras se extingnio o queda un pedazo",
                "diferencia entre conejeras y el hielo que queda",
                "is the Conejeras glacier still there",
                "when did the Conejeras ice disappear",
            ],
            "El glaciar Conejeras, en el Santa Isabel, se extinguió en marzo de 2024, después de 18 años de monitoreo mensual del IDEAM. El hielo que aún queda en ese nevado no es Conejeras. Confirma con un operador registrado qué puedes ver en el recorrido.",
            [
                "Conejeras, un sector del Santa Isabel, se extinguió en marzo de 2024 tras 18 años de mediciones del IDEAM. Si buscas hielo, no es ese sector: confirma el recorrido con un operador registrado."
            ],
            [IDEAM_SRC],
            ["qué es el superpáramo", "cómo es el clima en Los Nevados", "puedo caminar por donde quiera"],
            ["santa_isabel_glacier_extinction", "santa_isabel_projection_three_years", "glaciers_snow_presence"],
            ["conejeras", "santa isabel", "extincion"],
        ),
        entry(
            "santa_isabel_projection_three_years",
            "proyección reciente del Santa Isabel",
            "explanation",
            [
                "cuando se acaba el glaciar del santa isabel",
                "cuanto hielo le queda al santa isabel",
                "el ideam dice que el santa isabel desaparece pronto",
                "es cierto que el poleka kasue se extingue en pocos anos",
                "la proyeccion de tres a cinco anos es fija",
                "por que la ficha dice 2028 y el ideam otra cosa",
                "el santa isabel se derrite por el nino",
                "medicion de febrero de 2024 del santa isabel",
                "oiga el santa isabel ya casi no tiene nieve",
                "esa fecha de extincion puede cambiar",
                "cuantos kilometros de glaciar tenia el santa isabel",
                "when might the Santa Isabel glacier disappear",
                "is the 2028 extinction date a forecast",
            ],
            "En febrero de 2024 el IDEAM midió el Santa Isabel en 0,16 km² ± 0,01 km², 44,8 % menos que los 0,29 km² de 2022, y proyecta su extinción en tres a cinco años. Esa proyección puede variar con El Niño o La Niña; la ficha del parque aún cita 2028. Confirma el dato vigente en el IDEAM.",
            [
                "El Santa Isabel medía 0,16 km² ± 0,01 km² en febrero de 2024, 44,8 % menos que los 0,29 km² de 2022. El IDEAM proyecta tres a cinco años y la ficha habla de 2028; ambas son proyecciones. Consulta el IDEAM."
            ],
            [IDEAM_SRC, PNN_SRC],
            ["qué nevados hay en el parque", "cómo es el clima en Los Nevados", "qué es el páramo"],
            ["santa_isabel_glacier_extinction", "conejeras_extinct_march_2024", "colombia_glacier_area_2024"],
            ["santa isabel", "proyeccion", "2028"],
        ),
        entry(
            "ruiz_ash_insulates_ice",
            "ceniza que cubre el hielo del Ruiz",
            "explanation",
            [
                "la ceniza del ruiz derrite el glaciar",
                "la ceniza volcanica acelera el deshielo",
                "por que el hielo del ruiz esta gris",
                "la capa de ceniza protege o dana el glaciar",
                "cuanta ceniza cubria el nevado del ruiz en 2024",
                "el cráter arenas ennegrece la nieve",
                "en el sur del ruiz se derrite mas el hielo",
                "una capa gruesa de ceniza aisla el glaciar",
                "oiga la ceniza quita el reflejo de la nieve",
                "no toda la ceniza derrite el hielo del ruiz",
                "efecto de la ceniza volcanica sobre el casquete",
                "does volcanic ash melt the Ruiz glacier",
                "why is the Ruiz ice covered in ash",
            ],
            "En 2024 cerca del 88 % del glaciar del Ruiz estaba cubierto de ceniza. El IDEAM vio que una capa de más de 5 cm aísla el hielo y reduce el derretimiento; al sur, con menos ceniza, el hielo se fundió más. No des por hecho que la ceniza siempre derrite la nieve: mira el informe 2024.",
            [
                "Cerca del 88 % del glaciar del Ruiz tuvo ceniza en 2024. Más de 5 cm actuaron como aislante; donde hubo menos ceniza, al sur, el hielo retrocedió más. Consulta el informe 2024 del IDEAM."
            ],
            [IDEAM_SRC],
            ["cómo es el clima en Los Nevados", "a qué altura está el Ruiz", "qué es el superpáramo"],
            ["ruiz_glacier_measured_2024", "glacier_retreat_climate_change", "glaciers_snow_presence"],
            ["ceniza", "ruiz", "albedo"],
        ),
        entry(
            "colombia_glacier_area_2024",
            "cobertura glaciar nacional en 2024",
            "fact",
            [
                "cuanto hielo queda en los glaciares de colombia",
                "cuantos kilometros de glaciar hay en el pais",
                "a que ritmo se derriten los nevados colombianos",
                "el retroceso glaciar de 2024 es una medicion o un pronostico",
                "porcentaje anual de perdida de glaciares",
                "cifra del ideam de glaciares a inicios de 2024",
                "se estan acabando las nieves de colombia",
                "oiga cuanto casquete glaciar queda en el pais",
                "la tasa de 3 a 5 por ciento es todos los anos",
                "informe de glaciares colombianos 2024",
                "el deshielo nacional medido por el ideam",
                "how much glacier ice remained in Colombia in 2024",
                "what annual glacier loss rate does IDEAM report",
            ],
            "Para inicios de 2024 el IDEAM estimó 30,83 km² ± 0,48 km² de glaciares en Colombia y una reducción del 6,84 %. El ritmo anual se ha mantenido entre el 3 y el 5 %. Es una medición del informe 2024, no un pronóstico: confirma la cifra en ideam.gov.co.",
            [
                "A inicios de 2024 había 30,83 km² ± 0,48 km² de glaciares en el país, un 6,84 % menos, con un ritmo anual de 3 a 5 %. Es medición, no pronóstico. Revisa el informe vigente del IDEAM."
            ],
            [IDEAM_SRC],
            ["qué nevados hay en el parque", "cómo es el clima en Los Nevados", "fauna de Los Nevados"],
            ["glacier_retreat_climate_change", "ruiz_glacier_measured_2024", "santa_isabel_projection_three_years"],
            ["glaciares", "colombia", "ideam"],
        ),
        entry(
            "romerales_fire_october_2024",
            "incendio de páramo en Romerales",
            "explanation",
            [
                "que paso con el incendio de romerales",
                "el fuego de octubre de 2024 dano los frailejones",
                "se quemo pajonal en el nevado del ruiz",
                "el incendio de romerales afecto el siete cueros",
                "los romeros de paramo se quemaron",
                "un incendio dana la regulacion del agua del paramo",
                "puedo visitar romerales despues del incendio",
                "oiga el fuego del ruiz quemo frailejones",
                "que plantas se afectaron en romerales",
                "el 12 de octubre de 2024 hubo incendio en el parque",
                "el paramo se recupera solo despues de un incendio",
                "what did the Romerales wildfire burn",
                "did the 2024 fire damage frailejones",
            ],
            "Desde el 12 de octubre de 2024 hubo un incendio en Romerales, en el Ruiz, que dañó frailejones, siete cueros, romeros y pajonal, plantas que regulan el agua. El estado de esa zona puede haber cambiado: pregunta al parque antes de visitar el sector.",
            [
                "El incendio de Romerales, desde el 12 de octubre de 2024, quemó frailejones, siete cueros, romeros y pajonal del Ruiz. Esas plantas regulan el agua. Pregunta al parque cómo está el sector ahora."
            ],
            [src("Parques Nacionales Naturales de Colombia", ROMERALES)],
            ["qué frailejones hay en el parque", "puedo caminar por donde quiera", "cómo es el clima en Los Nevados"],
            ["frailejones_overview", "pajonales_calamagrostis", "africa_paramo_fire_2026"],
            ["incendio", "romerales", "frailejon"],
        ),
        entry(
            "africa_paramo_fire_2026",
            "incendio de páramo en El África",
            "fact",
            [
                "hubo un incendio en el sector el africa",
                "se quemo paramo en santa isabel en 2026",
                "cuantas hectareas quemo el incendio de el africa",
                "el fuego de septiembre de 2026 ya se apago",
                "puedo subir a el africa despues del incendio",
                "incendio a 4200 metros en el parque",
                "los guardaparques controlaron un fuego en santa isabel",
                "la cifra de hectareas quemadas es preliminar",
                "oiga en el africa se quemo el paramo",
                "entre el 19 y el 20 de septiembre hubo fuego",
                "los incendios siguen amenazando el paramo",
                "was there a páramo fire at El África in 2026",
                "how many hectares burned at El África",
            ],
            "Entre el 19 y el 20 de septiembre de 2026 se liquidó un incendio en El África, Santa Isabel, a unos 4.200 m, con más de 20 hectáreas de páramo afectadas de forma preliminar. La cifra puede ajustarse: confirma el estado del sector con el parque.",
            [
                "Parques Nacionales liquidó el 19 y 20 de septiembre de 2026 un incendio en El África, cerca de 4.200 m, con más de 20 hectáreas de páramo en una cuenta preliminar. Pregunta al parque antes de ir a ese sector."
            ],
            [src("Parques Nacionales Naturales de Colombia", AFRICA)],
            ["qué es el páramo", "cómo es el clima en Los Nevados", "fauna de Los Nevados"],
            ["romerales_fire_october_2024", "paramo_ecosystem", "ecological_restoration_programs"],
            ["incendio", "africa", "paramo"],
        ),
        entry(
            "native_species_nurseries",
            "viveros de plantas nativas del parque",
            "explanation",
            [
                "donde reproducen los frailejones del parque",
                "hay viveros de paramo en los nevados",
                "que es el vivero de potosi",
                "a que altura esta el vivero de alta montana",
                "siembran especies nativas para restaurar",
                "torrecitas otun y brisas tienen vivero",
                "por que el frailejon del vivero crece lento",
                "puedo llevarme una planta del paramo",
                "oiga quien repone los frailejones danados",
                "el vivero de potosi solo usa plantas nativas",
                "restauracion activa con material de vivero",
                "where does the park grow native frailejones",
                "can I take a plant from the páramo",
            ],
            "Hay viveros de especies nativas en Torrecitas, Potosí, Laguna del Otún y Brisas para restaurar el páramo. En Potosí, a 3.850 m, propagan solo plantas nativas, incluido el frailejón, de crecimiento lento. No arranques plantas: la reposición la hace el parque.",
            [
                "El parque propaga plantas nativas en Torrecitas, Potosí, Laguna del Otún y Brisas. El vivero de Potosí está a 3.850 m y solo usa especies nativas, como el frailejón. Déjalas en el sitio."
            ],
            [
                src("Parques Nacionales Naturales de Colombia", VIVEROS),
                src("Parques Nacionales Naturales de Colombia", POTOSI),
            ],
            ["qué frailejones hay en el parque", "hay palmas de cera en los nevados", "puedo llevar a mi perro"],
            ["frailejones_overview", "ecological_restoration_programs", "romerales_fire_october_2024"],
            ["vivero", "restauracion", "frailejon"],
        ),
        entry(
            "otun_peatland_plants",
            "turberas vegetales de la laguna Otún",
            "explanation",
            [
                "que plantas forman las turberas del otun",
                "hay sphagnum en la laguna del otun",
                "distichia muscoides crece en el humedal",
                "las turberas regulan el agua del paramo",
                "cojines de plantago en la turbera",
                "puedo pisar la turbera del otun",
                "que es un pantano turboso en los nevados",
                "musgo de turbera junto a la laguna",
                "oiga esas almohadas verdes del camino al otun",
                "la ficha ramsar que plantas de turbera nombra",
                "por que no debo caminar sobre los cojines",
                "which plants build the Otún peatlands",
                "is sphagnum part of the Otún wetlands",
            ],
            "En el complejo Ramsar de la Laguna del Otún hay turberas con Plantago rigida, Distichia muscoides y musgo Sphagnum, que regulan el ciclo del agua. Camina por el sendero habilitado y no pises esos cojines.",
            [
                "La ficha Ramsar del Otún describe turberas de Plantago rigida, Distichia muscoides y Sphagnum, importantes para el ciclo del agua. Quédate en el sendero y no pises los cojines."
            ],
            [RAMSAR_SRC],
            ["qué es el páramo", "aves", "puedo caminar por donde quiera"],
            ["high_andean_wetlands", "cojines_plantago_rigida", "ramsar_otun_wetland_complex"],
            ["turbera", "sphagnum", "otun"],
        ),
        entry(
            "otun_mosses_and_lichens",
            "musgos y líquenes que retienen lluvia",
            "explanation",
            [
                "hay liquenes en la laguna del otun",
                "los musgos del paramo guardan el agua lluvia",
                "que funcion tienen los liquenes del humedal",
                "el suelo del otun retiene la lluvia",
                "gramineas musgos y liquenes de la laguna",
                "por que el suelo del humedal esta siempre humedo",
                "los liquenes ayudan a la cuenca del otun",
                "oiga esas costras y musgos del camino al otun",
                "puedo arrancar musgo para verlo de cerca",
                "la vegetacion baja controla el flujo del agua",
                "criptogamas que retienen agua en el otun",
                "do mosses and lichens hold rain at Otún",
                "why is the ground around Laguna del Otún so wet",
            ],
            "En los suelos de la Laguna del Otún, gramíneas, musgos, líquenes y algunos arbustos retienen grandes volúmenes de agua lluvia y ayudan a controlar el flujo de la cuenca. Míralos desde el sendero y evita pisar el suelo húmedo.",
            [
                "La ficha Ramsar recoge que en la Laguna del Otún gramíneas, musgos, líquenes y arbustos retienen mucha agua lluvia y regulan la cuenca. Obsérvalos sin salirte del sendero."
            ],
            [RAMSAR_SRC],
            ["qué es el superpáramo", "fauna de Los Nevados", "dónde boto la basura"],
            ["otun_peatland_plants", "laguna_del_otun_ecosystem", "water_cycle_basin_supply"],
            ["musgo", "liquen", "lluvia"],
        ),
        entry(
            "otun_river_supplies_pereira",
            "agua del río Otún para Pereira",
            "fact",
            [
                "de donde sale el agua de pereira",
                "el rio otun nace en la laguna del otun",
                "la laguna del otun abastece a dosquebradas",
                "cuantas personas tomaban agua del humedal del otun",
                "la cifra de 500 mil personas sigue vigente",
                "a que altura nace el rio otun",
                "el acueducto de pereira depende de la laguna",
                "oiga el agua de pereira baja del paramo",
                "ficha ramsar del otun y el abastecimiento",
                "esa cifra de 2006 puede haber cambiado",
                "dosquebradas tambien recibe agua del otun",
                "does the Otún river supply Pereira",
                "where does Pereira's Otún river begin",
            ],
            "La ficha Ramsar del 17 de julio de 2006 dice que el río Otún nace en la Laguna del Otún, a 4000 m, y que el humedal abastecía a más de 500 mil personas de Pereira y Dosquebradas. Esa cifra puede haber cambiado: confírmala con Aguas y Aguas de Pereira.",
            [
                "Según la ficha Ramsar del 17 de julio de 2006, el Otún nace en la laguna a 4000 m y el humedal abastecía a más de 500 mil personas de Pereira y Dosquebradas. Confirma el dato actual con Aguas y Aguas de Pereira."
            ],
            [RAMSAR_SRC],
            ["reservas para Los Nevados", "qué nevados hay en el parque", "qué es el páramo"],
            ["laguna_del_otun_ecosystem", "water_cycle_basin_supply", "coffee_region_water_reserve"],
            ["otun", "pereira", "agua"],
        ),
        entry(
            "coffee_region_water_reserve",
            "reserva de agua del Eje Cafetero",
            "explanation",
            [
                "a cuantos departamentos les da agua el parque",
                "el parque abastece a millones de personas",
                "los nevados son la reserva de agua del eje cafetero",
                "el agua llega a caldas risaralda quindio y tolima",
                "el paramo tambien riega cultivos del magdalena",
                "hay una cifra exacta de gente que bebe esa agua",
                "el parque regula agua para la agroindustria",
                "oiga de los nevados baja el agua del cafe",
                "millones de habitantes dependen del parque",
                "el valle del cauca recibe agua de los nevados",
                "no hay un numero oficial de usuarios del agua",
                "which departments get water from Los Nevados",
                "does the park supply the coffee region",
            ],
            "El parque es, según Parques Nacionales, la reserva de agua más importante para Tolima, Risaralda, Caldas y Quindío: abastece a millones de habitantes del Eje Cafetero y regula agua para agroindustrias del Magdalena y del Cauca. No hay una cifra exacta de personas; pregunta a tu acueducto.",
            [
                "Parques Nacionales llama al parque la reserva de agua de Tolima, Risaralda, Caldas y Quindío, útil para millones de personas y para agroindustrias del Magdalena y del Cauca. La cifra exacta la tiene tu acueducto."
            ],
            [PNN_SRC],
            ["qué ecosistemas hay en los nevados", "reservas para Los Nevados", "aves"],
            ["water_cycle_basin_supply", "otun_river_supplies_pereira", "glacier_melt_feeds_rivers"],
            ["agua", "eje cafetero", "cuenca"],
        ),
        entry(
            "conservation_target_values",
            "valores de conservación del parque",
            "explanation",
            [
                "que se conserva en los nevados",
                "cuales son los valores objeto de conservacion",
                "el parque monitorea paramos humedales y bosques",
                "las cuencas del chinchina y del otun son prioridad",
                "los glaciares tambien son un valor de conservacion",
                "que vigilan los guardaparques en el ecosistema",
                "por que cuidan el bosque altoandino",
                "oiga que objetivos de conservacion tiene el parque",
                "el humedal altoandino esta en la lista de conservacion",
                "donde leo el detalle de esos valores",
                "conservacion de cuencas altas y de los tres nevados",
                "what ecosystems does the park monitor for conservation",
                "are the glaciers a conservation target",
            ],
            "Parques Nacionales sigue como valores de conservación los páramos, humedales y bosques altoandinos, las cuencas altas del Chinchiná y del Otún, y los glaciares de los tres nevados. Si quieres el detalle de ese monitoreo, consúltalo en la ficha del parque.",
            [
                "Entre lo que el parque monitorea están páramos, humedales, bosques altoandinos, las cuencas del Chinchiná y del Otún, y los tres glaciares. El detalle está en la ficha de Parques Nacionales."
            ],
            [PNN_SRC],
            ["fauna de Los Nevados", "puedo llevar a mi perro", "qué frailejones hay en el parque"],
            ["park_ecosystems_overview", "ecological_restoration_programs", "high_andean_forest"],
            ["conservacion", "cuenca", "glaciar"],
        ),
        entry(
            "glacier_melt_feeds_rivers",
            "deshielo que alimenta los ríos",
            "explanation",
            [
                "el agua de la llave sale del deshielo",
                "el glaciar es el que produce toda el agua",
                "el derretimiento alimenta los rios del parque",
                "la nieve baja hacia el cauca y el magdalena",
                "que porcentaje del agua viene del glaciar",
                "el paramo aporta mas que el hielo",
                "no tengo el reparto entre nieve y paramo",
                "oiga sin el nevado se acaba el agua",
                "el deshielo del ruiz santa isabel y tolima",
                "el 84 por ciento de paramo tambien es agua",
                "debo preguntarle a mi acueducto el origen del agua",
                "does tap water come only from melting glaciers",
                "do the three ice caps feed the park rivers",
            ],
            "El deshielo del Ruiz, Santa Isabel y Tolima aporta agua a los ríos que nacen en el parque y siguen hacia el Cauca y el Magdalena. El páramo ocupa el 84 % del área. La ficha no reparte el caudal entre nieve y páramo: no atribuyas el agua del grifo solo al deshielo y pregunta a tu acueducto.",
            [
                "Parques Nacionales dice que el deshielo de los tres nevados alimenta ríos que van al Cauca y al Magdalena, y que el páramo es el 84 % del área. No publica el reparto del caudal: consúltalo con tu acueducto."
            ],
            [PNN_SRC],
            ["qué es el páramo", "qué nevados hay en el parque", "cuándo llueve más en Los Nevados"],
            ["water_cycle_basin_supply", "coffee_region_water_reserve", "glaciers_snow_presence"],
            ["deshielo", "rios", "paramo"],
        ),
    ]


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    return " ".join(re.findall(r"\w+", "".join(c for c in text if not unicodedata.combining(c))))


RETREAT_SHORT = (
    "En 2024 el IDEAM señaló un El Niño extremo en los primeros cuatro meses y un "
    "derretimiento intenso en las partes bajas de los glaciares por la falta de nieve. "
    "No lo tomes como pronóstico de tu día: revisa el informe de glaciares del IDEAM antes de subir."
)
RETREAT_VARIANT = (
    "El informe 2024 habla de un El Niño extremo al inicio del año y de derretimiento "
    "en las partes bajas por la ausencia de nieve. Consulta el informe del IDEAM: el hielo cambia."
)


def patch_verified(entries: list[dict]) -> list[dict]:
    """The old retreat answer blamed 'calentamiento global' without a contiguous quote."""
    for item in entries:
        if item["id"] != "flora_ecosystems.glacier_retreat_climate_change":
            continue
        item["answer"]["short"] = RETREAT_SHORT
        item["answer"]["variants"] = [RETREAT_VARIANT]
        item["sources"] = [IDEAM_SRC]
        item["last_verified"] = DATE
    return entries


def build() -> dict:
    verified = patch_verified(json.loads(VERIFIED.read_text(encoding="utf-8")))
    if len(verified) != 22:
        raise ValueError(f"expected 22 verified entries, got {len(verified)}")
    added = new_entries() + build_round3(entry)
    section = {
        "contract_version": 1,
        "id": "flora_ecosystems",
        "order": 12,
        "title": "Flora y ecosistemas de alta montaña",
        "description": (
            "Ecosistemas del parque, páramo, subpáramo, superpáramo, bosque altoandino, "
            "frailejones, turberas, glaciares, agua y conservación."
        ),
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.2,
            "top_k": 2,
            "min_score": None,
            "entity_filters": [],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Te interesa el subpáramo de la ruta del Tolima o el bosque altoandino?",
                "¿Preguntas por el hielo del Ruiz, del Tolima o del Santa Isabel?",
                "¿Quieres saber de la ceniza sobre el glaciar o del retroceso medido por el IDEAM?",
                "¿Tu duda es sobre turberas y musgos del Otún o sobre el agua que llega a Pereira?",
                "¿Buscas el incendio de Romerales o los viveros donde propagan frailejones?",
                "¿Quieres la cifra nacional de glaciares o la proyección del Santa Isabel?",
                "¿Preguntas por el agua del Eje Cafetero o por lo que aporta el deshielo a los ríos?",
                "¿Quieres datos del frailejón o de otras plantas del páramo?",
            ],
            "slot_questions": {},
            "fallback": (
                "No tengo ese dato de flora o ecosistemas. Puedo contarte de frailejones, "
                "páramo, turberas, glaciares o del agua que sale del parque."
            ),
        },
        "featured": [
            "flora_ecosystems.park_ecosystems_overview",
            "flora_ecosystems.frailejones_overview",
            "flora_ecosystems.high_andean_wetlands",
            "flora_ecosystems.glaciers_snow_presence",
            "flora_ecosystems.water_cycle_basin_supply",
        ],
        "entries": verified + added,
    }
    known = {item["id"] for item in section["entries"]}
    owners: dict[str, str] = {}
    for item in section["entries"]:
        for example in item["examples"]:
            key = fold(example)
            if key in owners:
                raise ValueError(f"duplicate example {example!r} in {owners[key]} and {item['id']}")
            owners[key] = item["id"]
        for related in item["related"]:
            if related not in known:
                raise ValueError(f"{item['id']} related missing {related}")
    sections = ROOT / "data/knowledge/sections"
    collisions = []
    for path in sections.glob("*.json"):
        if path.name == "flora_ecosystems.json":
            continue
        for other in json.loads(path.read_text(encoding="utf-8"))["entries"]:
            for example in other["examples"]:
                key = fold(example)
                if key in owners:
                    collisions.append(f"{example!r} :: {owners[key]} :: {other['id']}")
    if collisions:
        raise ValueError("example collisions:\n" + "\n".join(collisions))
    return section


def main() -> None:
    section = build()
    SECTION_PATH.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"entries {len(section['entries'])}")


if __name__ == "__main__":
    main()
