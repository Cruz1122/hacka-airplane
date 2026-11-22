"""Shared constants for the corrected history_culture section. Not the retired builder."""

from __future__ import annotations

DATE = "2026-11-21"

PNN = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
PNN_NORM = "https://old.parquesnacionales.gov.co/portal/es/normatividad/marco-normativo-areas-protegidas/dreccion-territorial-andes-occidentales/parque-nacional-natural-nevados/"
RES148 = "https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2022/01/148-de-1974.pdf"
SGC_HIST = "https://historia-volcanes.sgc.gov.co/volcan-detalle?id=6"
SGC_TABLE = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/Actividad-historica.aspx"
SGC_SHEET = "https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf"
SGC_NOTE = "https://www2.sgc.gov.co/Noticias/Paginas/Nota-aclaratoria-sobre-el-t%C3%A9rmino-%E2%80%98lahares%E2%80%99-con-relaci%C3%B3n-a-las-recientes-alertas-anunciadas-por-el-IDEAM.aspx"
SGC_MAP = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/Mapa-amenaza.aspx"
SGC_MEM = "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Documents/MemMapaAmenVNR.pdf"
SGC_TOL = "https://historia-volcanes.sgc.gov.co/volcan-detalle?id=5680"
CSJ = "https://cortesuprema.gov.co/corte/wp-content/uploads/2020/11/STL10716-2020.pdf"
LEY2505 = "http://www.secretariasenado.gov.co/senado/basedoc/ley_2505_2025.html"
UNESCO = "https://whc.unesco.org/en/list/1121"
IUGS = "https://iugs-geoheritage.org/geoheritage_sites/nevado-del-ruiz-quaternary-volcanic-complex/"


def src(*pairs: tuple[str, str]) -> list[dict]:
    return [{"label": label, "url": url, "retrieved_at": DATE} for label, url in pairs]


def entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    hard_negatives: list[str],
    short: str,
    variants: list[str],
    sources: list[dict],
    related: list[str],
    tags: list[str],
    detail: str | None = None,
    steps: list | None = None,
    reflection: str | None = None,
    entities: dict | None = None,
) -> dict:
    answer: dict = {
        "short": short,
        "variants": variants,
        "detail": detail,
        "reflection": reflection,
    }
    if steps is not None:
        answer["steps"] = steps
    item = {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "needs": [],
        "answer": answer,
        "sources": sources,
        "last_verified": DATE,
        "valid_until": None,
        "related": related,
        "tags": tags,
    }
    if entities:
        item["entities"] = entities
    return item
