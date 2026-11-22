import json, re, sys, difflib, glob, os
SEC = "/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/services.json"
SCHEMA = "/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json"
OTHERS = "/home/cruz1122/dev/hacka-airplane/data/knowledge/sections"
d = json.load(open(SEC, encoding="utf-8"))
errs, warns = [], []
try:
    import jsonschema
    jsonschema.validate(d, json.load(open(SCHEMA, encoding="utf-8")))
    print("SCHEMA: OK (jsonschema)")
except ImportError:
    print("SCHEMA: jsonschema no disponible; validación estructural manual")
except jsonschema.ValidationError as e:
    errs.append("SCHEMA: " + e.message[:300])
entries = d["entries"]
ids = {e["id"] for e in entries}
print("entries:", len(entries))
ex_all = {}
for e in entries:
    ex = e["examples"]
    if len(ex) < 12: errs.append(f"{e['id']}: solo {len(ex)} ejemplos")
    if len(set(x.lower() for x in ex)) != len(ex): errs.append(f"{e['id']}: ejemplos repetidos internos")
    nw = len(e["label"].split())
    if not (3 <= nw <= 8): errs.append(f"{e['id']}: label de {nw} palabras")
    hn = e.get("hard_negatives", [])
    if not (2 <= len(hn) <= 4): errs.append(f"{e['id']}: hard_negatives={len(hn)}")
    for x in ex:
        ex_all.setdefault(x.strip().lower(), []).append(e["id"])
    for r in e.get("related", []):
        if r not in ids: errs.append(f"{e['id']}: related no resuelve {r}")
    if not (1 <= len(e.get("related", [])) <= 3): errs.append(f"{e['id']}: related={len(e.get('related',[]))}")
    for n in e.get("needs", []):
        if n not in d["clarification"].get("slot_questions", {}): errs.append(f"{e['id']}: need sin slot {n}")
    for k in e.get("entities", {}):
        if k not in d["retrieval"].get("entity_filters", []): errs.append(f"{e['id']}: entidad fuera de filters {k}")
    txt = e["answer"]["short"] + " " + " ".join(e["answer"].get("variants", []))
    if re.search(r"\d", txt) and not e.get("last_verified"): errs.append(f"{e['id']}: cifra sin last_verified")
    if not (1 <= len(e["answer"].get("variants", [])) <= 2): warns.append(f"{e['id']}: variants={len(e['answer'].get('variants',[]))}")
    sents = len([s for s in re.split(r"[.!?]+\s", e["answer"]["short"]) if s.strip()])
    if sents > 3: warns.append(f"{e['id']}: short con {sents} frases")
for f in d["featured"]:
    if f not in ids: errs.append(f"featured no resuelve {f}")
print("featured:", len(d["featured"]), "(3-5 requerido)")
dups = {k: v for k, v in ex_all.items() if len(v) > 1}
if dups: errs.append(f"ejemplos duplicados en entradas: {dups}")
# colisiones exactas con otras secciones
other_ex = {}
for f in glob.glob(os.path.join(OTHERS, "*.json")):
    if os.path.abspath(f) == os.path.abspath(SEC): continue
    try:
        od = json.load(open(f, encoding="utf-8"))
    except Exception as ex:
        warns.append(f"no pude leer {os.path.basename(f)}: {ex}"); continue
    for oe in od.get("entries", []):
        for x in oe.get("examples", []):
            other_ex.setdefault(x.strip().lower(), []).append(oe["id"])
col = {k: (v, other_ex[k]) for k, v in ex_all.items() if k in other_ex}
if col: errs.append(f"ejemplos idénticos a otras secciones: {col}")
# casi duplicados internos (ratio >= 0.9)
flat = [(x, e["id"]) for e in entries for x in e["examples"]]
near = []
for i in range(len(flat)):
    for j in range(i + 1, len(flat)):
        if flat[i][1] == flat[j][1]: continue
        r = difflib.SequenceMatcher(None, flat[i][0].lower(), flat[j][0].lower()).ratio()
        if r >= 0.9: near.append((round(r, 2), flat[i], flat[j]))
print("casi duplicados (ratio>=0.9) entre entradas:", len(near))
for n in near[:20]: print("  ", n)
# hard negatives: deben ser ejemplos de otra entrada (sección o global)
hn_unres = []
all_known = set(ex_all) | set(other_ex)
for e in entries:
    for h in e.get("hard_negatives", []):
        if h.strip().lower() not in all_known: hn_unres.append((e["id"], h))
        elif e["id"] in ex_all.get(h.strip().lower(), []): errs.append(f"{e['id']}: hard negative igual a un ejemplo propio: {h}")
print("hard_negatives no encontrados como ejemplo de otra entrada:", len(hn_unres))
for h in hn_unres: print("  ", h)
total = sum(len(e["examples"]) for e in entries)
print("total ejemplos:", total, "| min por entrada:", min(len(e["examples"]) for e in entries))
print("entradas por kind:", {k: sum(1 for e in entries if e["kind"] == k) for k in set(e["kind"] for e in entries)})
print("WARN:", *warns, sep="\n  ") if warns else print("WARN: ninguna")
print("ERRORES:", len(errs))
for er in errs: print("  -", er)
sys.exit(1 if errs else 0)
