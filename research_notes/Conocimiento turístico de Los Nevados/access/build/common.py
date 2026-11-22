"""Shared builders for the access knowledge section. Content lives in part files."""

from __future__ import annotations

FICHA = {
    "label": "Parques Nacionales Naturales de Colombia — Parque Nacional Natural Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21",
}
ANEXO = {
    "label": "Parques Nacionales Naturales — Reglamentación transitoria de ecoturismo, PNN Los Nevados, diciembre de 2023",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf",
    "retrieved_at": "2026-11-21",
}
SGC = {
    "label": "Servicio Geológico Colombiano — Generalidades del volcán Nevado del Ruiz",
    "url": "https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/generalidades-volcan-nevado-ruiz.aspx",
    "retrieved_at": "2026-11-21",
}
GUIDE_2016 = {
    "label": "Parques Nacionales Naturales — How to get there, Los Nevados, version 1, April 2016",
    "url": "https://old.parquesnacionales.gov.co/portal/en/ecotourism/andean-region/los-nevados-national-natural-park/how-to-get-there/",
    "retrieved_at": "2026-11-21",
}
TRIP_2026 = {
    "label": "Parques Nacionales Naturales — Organiza tu viaje al Parque Nacional Natural Los Nevados (PDF, 2026)",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
    "retrieved_at": "2026-11-21",
}
GPS_2013 = {
    "label": "Parques Nacionales Naturales — Guía complementaria del mapa ecoturístico de Los Nevados",
    "url": "https://old.parquesnacionales.gov.co/portal/wp-content/uploads/2013/10/Guia_compl_mapa_Parq_Nevados.pdf",
    "retrieved_at": "2026-11-21",
}


def entry(
    *,
    id: str,
    label: str,
    kind: str,
    examples: list[str],
    hard_negatives: list[str],
    short: str,
    variants: list[str],
    sources: list[dict],
    related: list[str],
    tags: list[str],
    steps: list[list[str]] | None = None,
    detail: str | None = None,
    reflection: str | None = None,
    entities: dict | None = None,
    needs: list[str] | None = None,
) -> dict:
    answer: dict = {"short": short, "variants": variants}
    if steps is not None:
        answer["steps"] = steps
    if detail is not None:
        answer["detail"] = detail
    if reflection is not None:
        answer["reflection"] = reflection
    item: dict = {
        "id": id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "answer": answer,
        "sources": sources,
        "last_verified": "2026-11-21",
        "related": related,
        "tags": tags,
    }
    if entities is not None:
        item["entities"] = entities
    if needs is not None:
        item["needs"] = needs
    return item
