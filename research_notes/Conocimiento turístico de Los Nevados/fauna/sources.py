"""Builder for fauna knowledge section of PNN Los Nevados."""
import json
import re
from pathlib import Path

# Common sources
SOURCE_PNN_PORTAL = {
    "label": "Parques Nacionales Naturales de Colombia - PNN Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21"
}
SOURCE_PNN_PLAN = {
    "label": "Plan de Manejo Parque Nacional Natural Los Nevados (PNN)",
    "url": "https://www.parquesnacionales.gov.co/gestion-del-conocimiento/planes-de-manejo/pnn-los-nevados/",
    "retrieved_at": "2026-11-21"
}
SOURCE_SIB_COLOMBIA = {
    "label": "SiB Colombia - Biodiversidad Parque Nacional Natural Nevados",
    "url": "https://doi.org/10.15472/r0e1u9",
    "retrieved_at": "2026-11-21"
}
SOURCE_HUMBOLDT = {
    "label": "Instituto de Investigación de Recursos Biológicos Alexander von Humboldt",
    "url": "http://www.humboldt.org.co/",
    "retrieved_at": "2026-11-21"
}
SOURCE_CARDER = {
    "label": "Corporación Autónoma Regional de Risaralda (CARDER) - Fauna Altoandina",
    "url": "https://www.carder.gov.co/",
    "retrieved_at": "2026-11-21"
}
SOURCE_CORPOCALDAS = {
    "label": "Corporación Autónoma Regional de Caldas (Corpocaldas) - Biodiversidad",
    "url": "https://www.corpocaldas.gov.co/",
    "retrieved_at": "2026-11-21"
}
SOURCE_CORTOLIMA = {
    "label": "Corporación Autónoma Regional del Tolima (Cortolima) - Especies Focales",
    "url": "https://www.cortolima.gov.co/",
    "retrieved_at": "2026-11-21"
}
SOURCE_EBIRD = {
    "label": "eBird - Hotspot Parque Nacional Natural Los Nevados",
    "url": "https://ebird.org/hotspot/L1142279",
    "retrieved_at": "2026-11-21"
}
