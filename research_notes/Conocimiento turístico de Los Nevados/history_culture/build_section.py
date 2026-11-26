#!/usr/bin/env python3
"""Retired builder. Running it would rewrite the corrected section with the pre-review entries."""

from __future__ import annotations

import sys

sys.exit(
    "Do not run. Superseded on 2026-11-21 by the correction pass. "
    "The section file is data/knowledge/sections/history_culture.json."
)

import json
from pathlib import Path

ROOT = Path("/home/cruz1122/dev/hacka-airplane")
OUT = ROOT / "data/knowledge/sections/history_culture.json"
DATE = "2026-11-21"

PNN = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
PNN_NORM = "https://old.parquesnacionales.gov.co/portal/es/normatividad/marco-normativo-areas-protegidas/dreccion-territorial-andes-occidentales/parque-nacional-natural-nevados/"
RES148 = "https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2022/01/148-de-1974.pdf"
LEY2 = "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=9021"
SGC_HIST = "https://historia-volcanes.sgc.gov.co/volcan-detalle?id=6"
SGC_TABLE = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/Actividad-historica.aspx"
SGC_SHEET = "https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf"
SGC_NOTE = "https://www2.sgc.gov.co/Noticias/Paginas/Nota-aclaratoria-sobre-el-t%C3%A9rmino-%E2%80%98lahares%E2%80%99-con-relaci%C3%B3n-a-las-recientes-alertas-anunciadas-por-el-IDEAM.aspx"
SGC_MAP = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/Mapa-amenaza.aspx"
SGC_MEM = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Documents/MemMapaAmenVNR.pdf"
SGC_TOL = "https://historia-volcanes.sgc.gov.co/volcan-detalle?id=5680"
CSJ = "https://cortesuprema.gov.co/corte/wp-content/uploads/2020/11/STL10716-2020.pdf"
LEY2505 = "http://www.secretariasenado.gov.co/senado/basedoc/ley_2505_2025.html"
IUGS = "https://iugs-geoheritage.org/geoheritage_sites/nevado-del-ruiz-quaternary-volcanic-complex/"
PCC = "https://paisajeculturalcafetero.org.co/preguntas-frecuentes/"
PLAN = "https://www.guao.org/sites/default/files/biblioteca/Los%20nevados.pdf"


def src(label: str, url: str) -> dict:
    return {"label": label, "url": url, "retrieved_at": DATE}


S = {
    "pnn": src("Parques Nacionales Naturales, ficha de Los Nevados", PNN),
    "norm": src("Parques Nacionales, índice normativo de Los Nevados", PNN_NORM),
    "res": src("Resolución Ejecutiva 148 de 1974 y Acuerdo 15 de 1973", RES148),
    "ley2": src("Función Pública, Ley 2 de 1959, artículo 13", LEY2),
    "hist": src("SGC, actividad histórica del Nevado del Ruiz", SGC_HIST),
    "table": src("SGC, tabla de actividad histórica del Ruiz", SGC_TABLE),
    "sheet": src("SGC, hoja informativa del Nevado del Ruiz, septiembre de 2024", SGC_SHEET),
    "note": src("SGC, nota sobre lahares del 28 de abril de 2023", SGC_NOTE),
    "map": src("SGC, conceptos del mapa de amenaza del Ruiz", SGC_MAP),
    "mem": src("SGC, memoria del mapa de amenaza del Ruiz, noviembre de 2015", SGC_MEM),
    "tol": src("SGC, actividad histórica del Nevado del Tolima", SGC_TOL),
    "csj": src("Corte Suprema de Justicia, STL10716-2020, 25 de noviembre de 2020", CSJ),
    "ley2505": src("Ley 2505 de 2025, Senado, Diario Oficial 53200", LEY2505),
    "iugs": src("IUGS, ficha del complejo volcánico del Nevado del Ruiz", IUGS),
    "pcc": src("Paisaje Cultural Cafetero, preguntas frecuentes", PCC),
    "plan": src("Documento ejecutivo del plan de manejo de Los Nevados, copia consultada", PLAN),
}


def entry(
    eid: str,
    label: str,
    kind: str,
    examples: list[str],
    negatives: list[str],
    short: str,
    variants: list[str],
    sources: list[dict],
    related: list[str],
    tags: list[str],
    volcano: list[str] | None = None,
    needs: list[str] | None = None,
    steps: list[list[str]] | None = None,
    detail: str | None = None,
    reflection: str | None = None,
) -> dict:
    answer: dict = {"short": short, "variants": variants}
    if steps:
        answer["steps"] = steps
    if detail is not None:
        answer["detail"] = detail
    if reflection is not None:
        answer["reflection"] = reflection
    item = {
        "id": eid,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "answer": answer,
        "sources": sources,
        "last_verified": DATE,
        "related": related,
        "tags": tags,
    }
    if volcano:
        item["entities"] = {"volcano": volcano}
    if needs:
        item["needs"] = needs
    return item


ENTRIES: list[dict] = []


def add(item: dict) -> None:
    ENTRIES.append(item)


add(entry(
    "history_culture.kumanday_name",
    "nombre indígena Kumanday",
    "fact",
    [
        "qué significa Kumanday",
        "qué es Kumanday",
        "cómo se llama el Nevado del Ruiz",
        "cuál es el otro nombre del Ruiz",
        "nombre ancestral del nevado",
        "kumanday es el ruiz o es otra montaña",
        "oiga y kumanday qué quiere decir",
        "que significa kumanday",
        "kumandai como se escribe",
        "me dijeron que el Ruiz tiene nombre quimbaya",
        "what does Kumanday mean",
        "is Kumanday the same as Nevado del Ruiz",
    ],
    [
        "qué alerta tiene hoy el Ruiz",
        "cuántos metros tiene el Nevado del Ruiz",
        "puedo subir hoy al cráter Arenas",
    ],
    "Kumanday es el nombre que, según Parques Nacionales, los quimbaya dieron al Nevado del Ruiz y significa «cerro blanco». La misma ficha llama Poleka Kasue al Nevado de Santa Isabel y Dulima al Nevado del Tolima. El Servicio Geológico Colombiano también escribe Cumanday, así que vas a ver las dos grafías.",
    [
        "Si oyes Kumanday, te están hablando del Nevado del Ruiz. Parques Nacionales lo traduce como «cerro blanco», nombre quimbaya, y usa Poleka Kasue y Dulima para Santa Isabel y el Tolima.",
        "Kumanday y Cumanday apuntan al mismo nevado, el Ruiz. La ficha del parque explica el primer nombre como «cerro blanco».",
    ],
    [S["pnn"], S["sheet"]],
    ["history_culture.poleka_kasue", "history_culture.dulima", "history_culture.ruiz_other_ancestral_names"],
    ["kumanday", "cumanday", "quimbaya", "ruiz"],
    ["ruiz"],
    steps=[
        ["Parques Nacionales atribuye Kumanday a los quimbaya y lo traduce como «cerro blanco». No es un nevado distinto del Ruiz."],
        ["En señales del sector norte también verás Brisas-Kumanday: es el nombre del recorrido asociado a ese volcán, no otro sitio."],
    ],
    reflection="Cuando preguntes por un nevado, el nombre indígena y el nombre del mapa suelen ser la misma cumbre.",
))

add(entry(
    "history_culture.ruiz_other_ancestral_names",
    "otros nombres ancestrales del Ruiz",
    "fact",
    [
        "qué es Tabuchía",
        "el Ruiz también se llamaba Tama",
        "cumanday y kumanday son lo mismo",
        "nombres precolombinos del volcán Ruiz",
        "tabuchia significa fuego",
        "tama padre mayor del nevado",
        "cuál otro nombre ancestral tiene el Ruiz además de Kumanday",
        "el sgc dice cumanday o kumanday",
        "como se escribia el ruiz antes",
        "me sonó Tabuchía en una guía, qué es",
        "what other indigenous names does Ruiz have",
        "is Cumanday a different spelling of Kumanday",
    ],
    [
        "cómo reservo Brisas Kumanday",
        "está activo el Nevado del Ruiz",
        "qué ropa llevo al Ruiz",
    ],
    "Además de Kumanday, la hoja del SGC de septiembre de 2024 recuerda que en época precolombina al Ruiz lo llamaron Cumanday, «cerro blanco», Tabuchía, «candela o fuego», y Tama, «padre mayor o grande». Cumanday y Kumanday son dos escrituras del mismo nombre en fuentes oficiales distintas. No cambian cuál es la montaña.",
    [
        "El SGC lista tres nombres de antes de la Colonia para el Ruiz: Cumanday o cerro blanco, Tabuchía o fuego, y Tama o padre mayor. Parques escribe Kumanday.",
    ],
    [S["sheet"], S["pnn"]],
    ["history_culture.kumanday_name", "history_culture.indigenous_peoples"],
    ["tabuchia", "tama", "cumanday"],
    ["ruiz"],
))

add(entry(
    "history_culture.poleka_kasue",
    "nombre Poleka Kasue",
    "fact",
    [
        "qué significa Poleka Kasue",
        "cómo llamaban a Santa Isabel",
        "poleka kasue es el nevado de santa isabel",
        "doncella de la montaña cuál nevado es",
        "nombre indígena de santa isabel",
        "poleka kasue quien lo puso",
        "que es poleka kasue",
        "poleka kazue como se escribe",
        "el sector del cisne por qué dice poleka",
        "los quimbaya también nombraron a santa isabel",
        "what does Poleka Kasue mean",
        "which peak is the maiden of the mountain",
    ],
    [
        "cómo llego al sector del Cisne",
        "puedo hacer cumbre en Santa Isabel",
        "hay glaciar todavía en Santa Isabel",
    ],
    "Parques Nacionales dice que los quimbaya llamaron Poleka Kasue al Nevado de Santa Isabel, «doncella de la montaña». Es un nombre del mismo nevado, no de una laguna ni de un pueblo. El sector turístico Cisne-Poleka Kasue usa esa palabra para orientar la visita cerca de Santa Isabel y del paramillo del Cisne.",
    [
        "Poleka Kasue es el nombre quimbaya de Santa Isabel según la ficha del parque, y se traduce como «doncella de la montaña».",
    ],
    [S["pnn"]],
    ["history_culture.kumanday_name", "history_culture.santa_isabel_record", "history_culture.sector_indigenous_names"],
    ["poleka", "santa isabel", "quimbaya"],
    ["santa_isabel"],
))

add(entry(
    "history_culture.dulima",
    "nombre indígena Dulima",
    "fact",
    [
        "qué significa Dulima",
        "cómo llamaban los pijaos al Tolima",
        "dulima es el nevado del tolima",
        "río de nieve qué montaña es",
        "nombre pijao del tolima",
        "dulima también quiere decir nube",
        "que significa dulima",
        "dulima o nevado del tolima",
        "por qué el sector se llama quindío dulima",
        "los pijaos le decían dulima al tolima",
        "what does Dulima mean",
        "is Dulima the Nevado del Tolima",
    ],
    [
        "reserva Quindío Dulima",
        "qué hay en el sector Dulima",
        "sendero para el Nevado del Tolima",
    ],
    "Parques Nacionales cuenta que los pijaos llamaban Dulima al Nevado del Tolima. La ficha interpreta esa voz como «río de nieve» o «nube», y también como expresión de la resistencia de ese pueblo. El sector Quindío-Dulima toma de ahí el nombre del volcán, no es otro nevado.",
    [
        "Dulima es el nombre pijao del Nevado del Tolima. En la ficha del parque se lee como «río de nieve» o «nube».",
    ],
    [S["pnn"]],
    ["history_culture.tolima_history", "history_culture.indigenous_peoples", "history_culture.sector_indigenous_names"],
    ["dulima", "pijao", "tolima"],
    ["tolima"],
))

add(entry(
    "history_culture.indigenous_peoples",
    "pueblos indígenas de los nevados",
    "explanation",
    [
        "qué indígenas vivían en los nevados",
        "los quimbaya tenían que ver con el ruiz",
        "pijaos y el nevado del tolima",
        "pantágoras y muiscas en esta montaña",
        "pueblos originarios del parque los nevados",
        "había resguardo indígena dentro del parque",
        "que indigenas nombraron los nevados",
        "los muiscas vivian en el ruiz o solo lo nombraban",
        "cultura indígena de kumanday",
        "quiénes veían sagrados estos volcanes",
        "which indigenous peoples are linked to Los Nevados",
        "did the Quimbaya name the Ruiz",
    ],
    [
        "puedo ver cóndores en el parque",
        "hay frailejones en el páramo",
        "está permitido llevar ofrendas al cráter",
    ],
    "La ficha de Parques Nacionales dice que los tres volcanes nevados fueron símbolo cultural y espiritual para pueblos que habitaron el territorio, y nombra a quimbayas, pijaos, pantágoras y muiscas. Atribuye Kumanday y Poleka Kasue a los quimbaya, y Dulima a los pijaos. No publica un mapa de resguardos actuales dentro del parque: si buscas eso, no lo inventes a partir de esta guía.",
    [
        "Parques relaciona los nevados con quimbayas, pijaos, pantágoras y muiscas como símbolo espiritual. Los nombres Kumanday, Poleka Kasue y Dulima vienen de esa memoria, no de un censo de hoy.",
    ],
    [S["pnn"]],
    ["history_culture.kumanday_name", "history_culture.dulima", "history_culture.campesino_communities"],
    ["quimbaya", "pijao", "pantagora", "muisca"],
    ["park"],
    reflection="Habla de esos pueblos como parte de la memoria del territorio, sin asumir rituales o permisos que la ficha no describe.",
))

add(entry(
    "history_culture.sector_indigenous_names",
    "nombres indígenas en los sectores",
    "explanation",
    [
        "por qué el sector se llama Kumanday",
        "brisas kumanday qué significa el segundo nombre",
        "cisne poleka kasue es un nombre turístico",
        "quindío dulima de dónde sale",
        "los sectores usan nombres indígenas",
        "el letrero dice kumanday y yo busco el ruiz",
        "por que brisas se llama kumanday",
        "poleka en el nombre del sector cisne",
        "no entiendo los nombres de los cuatro sectores",
        "el parque rebautizó los nevados",
        "why is the north sector called Kumanday",
        "what do the sector names Poleka and Dulima refer to",
    ],
    [
        "cómo llego a Brisas desde Manizales",
        "horario de ingreso por Brisas",
        "cuánto cuesta la entrada a Brisas",
    ],
    "Los cuatro sectores de la ficha se llaman Brisas-Kumanday, Cisne-Poleka Kasue, Laguna del Otún y Quindío-Dulima. Kumanday, Poleka Kasue y Dulima son los nombres indígenas que Parques Nacionales da al Ruiz, a Santa Isabel y al Tolima. Sirven para reconocer la montaña del recorrido, no reemplazan el mapa de acceso ni el horario.",
    [
        "Si el letrero dice Kumanday, Poleka Kasue o Dulima, está nombrando el Ruiz, Santa Isabel o el Tolima con el nombre que usa la ficha del parque.",
    ],
    [S["pnn"]],
    ["history_culture.kumanday_name", "history_culture.poleka_kasue", "history_culture.dulima"],
    ["sectores", "brisas", "cisne", "dulima"],
    ["park"],
))


def dump() -> None:
    section = {
        "contract_version": 1,
        "id": "history_culture",
        "order": 14,
        "title": "Historia y cultura",
        "description": "Nombres indígenas, creación del parque, erupciones históricas, memoria de Armero y la cultura campesina y cafetera ligada a Los Nevados.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.35,
            "top_k": 3,
            "min_score": None,
            "entity_filters": ["volcano"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Preguntas por la tragedia de 1985, por una erupción más antigua o por el nombre de un nevado?",
                "¿Hablas del Ruiz, de Santa Isabel, del Tolima o del parque en general?",
                "¿Quieres saber cuándo se creó el parque o qué pasó en Armero?",
                "¿Buscas el significado de Kumanday, de Poleka Kasue o de Dulima?",
                "¿La pregunta es sobre la historia de 1985 o sobre el estado del volcán hoy?",
                "¿Te interesa la cultura cafetera de la región o las comunidades del páramo?",
            ],
            "slot_questions": {
                "volcano": "¿Sobre cuál nevado preguntas: el Ruiz, Santa Isabel o el Tolima?",
            },
            "fallback": "Puedo contarte los nombres indígenas, la creación del parque o la memoria de Armero. Si necesitas el estado del volcán hoy, míralo en el Servicio Geológico Colombiano antes de salir o cuando vuelvas a tener señal.",
        },
        "featured": [
            "history_culture.armero_1985",
            "history_culture.what_is_a_lahar",
            "history_culture.kumanday_name",
            "history_culture.park_creation_1974",
            "history_culture.coffee_landscape",
        ],
        "entries": ENTRIES,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"entries={len(ENTRIES)} path={OUT}")
