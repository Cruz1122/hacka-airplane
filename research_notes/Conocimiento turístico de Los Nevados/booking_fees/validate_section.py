import json
import re
from pathlib import Path

BASE = Path('/home/cruz1122/dev/hacka-airplane')
section_path = BASE / 'data/knowledge/sections/booking_fees.json'
schema_path = BASE / 'research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json'
section = json.loads(section_path.read_text(encoding='utf-8'))
schema = json.loads(schema_path.read_text(encoding='utf-8'))
try:
    import jsonschema
    jsonschema.Draft202012Validator(schema).validate(section)
    schema_result = 'valid (jsonschema Draft 2020-12)'
except ImportError:
    # The schema is restricted to structural/type/enum/pattern/min-max/required rules.
    def check(value, spec, path='$'):
        errs=[]
        typ=spec.get('type')
        allowed={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'null':type(None),'boolean':bool}
        types=[typ] if isinstance(typ,str) else typ or []
        if types and not any(isinstance(value,allowed[t]) and not (t=='integer' and isinstance(value,bool)) for t in types):
            return [f'{path}: expected {types}']
        if 'const' in spec and value != spec['const']: errs.append(f'{path}: const mismatch')
        if 'enum' in spec and value not in spec['enum']: errs.append(f'{path}: enum mismatch')
        if isinstance(value,dict):
            for k in spec.get('required',[]):
                if k not in value: errs.append(f'{path}: missing {k}')
            props=spec.get('properties',{})
            if spec.get('additionalProperties') is False:
                for k in value.keys()-props.keys(): errs.append(f'{path}: unexpected {k}')
            for k,v in value.items():
                if k in props: errs += check(v,props[k],f'{path}.{k}')
                elif isinstance(spec.get('additionalProperties'),dict): errs += check(v,spec['additionalProperties'],f'{path}.{k}')
        if isinstance(value,list):
            if spec.get('uniqueItems') and len(value)!=len({json.dumps(v,sort_keys=True,ensure_ascii=False) for v in value}): errs.append(f'{path}: duplicates')
            for i,v in enumerate(value): errs += check(v,spec.get('items',{}),f'{path}[{i}]')
        if isinstance(value,str):
            if len(value)<spec.get('minLength',0): errs.append(f'{path}: too short')
            if len(value)>spec.get('maxLength',10**9): errs.append(f'{path}: too long')
            if 'pattern' in spec and not re.search(spec['pattern'],value): errs.append(f'{path}: pattern mismatch')
        if isinstance(value,(int,float)) and not isinstance(value,bool):
            if value<spec.get('minimum',float('-inf')) or value>spec.get('maximum',float('inf')): errs.append(f'{path}: number out of range')
        if isinstance(value,list):
            if len(value)<spec.get('minItems',0) or len(value)>spec.get('maxItems',10**9): errs.append(f'{path}: item count out of range')
        return errs
    errors=check(section,schema)
    if errors: raise SystemExit('Schema errors:\n'+'\n'.join(errors))
    schema_result='valid (local equivalent structural schema checker; jsonschema unavailable)'

entries=section['entries']; ids={e['id'] for e in entries}; problems=[]; all_examples={}
for e in entries:
    words=e['label'].split()
    if not 3<=len(words)<=8: problems.append(f"{e['id']}: label has {len(words)} words")
    if len(e['examples'])<12: problems.append(f"{e['id']}: fewer than 12 examples")
    if any(ch.isdigit() for ch in e['answer']['short']) and not e.get('last_verified'):
        problems.append(f"{e['id']}: numeric answer lacks last_verified")
    if not 2<=len(e.get('hard_negatives',[]))<=4: problems.append(f"{e['id']}: negatives outside 2-4")
    for x in e['examples']:
        if x in all_examples: problems.append(f"duplicate example: {all_examples[x]} and {e['id']}: {x}")
        all_examples[x]=e['id']
    for ref in e.get('related',[]):
        if ref not in ids: problems.append(f"{e['id']}: related id unresolved: {ref}")
    for need in e.get('needs',[]):
        if need not in section['clarification'].get('slot_questions',{}): problems.append(f"{e['id']}: missing slot question for {need}")
for ref in section.get('featured',[]):
    if ref not in ids: problems.append(f'featured id unresolved: {ref}')
for e in entries:
    for negative in e.get('hard_negatives',[]):
        if negative not in all_examples or all_examples.get(negative)==e['id']:
            problems.append(f"{e['id']}: hard negative does not match another entry's example: {negative}")
for key in section['retrieval'].get('entity_filters',[]):
    if key not in section['clarification'].get('slot_questions',{}): problems.append(f'missing slot question for entity filter {key}')
if problems: raise SystemExit('Contract checks failed:\n'+'\n'.join(problems))
print(f'Schema: {schema_result}')
print(f'Contract checks: valid; {len(entries)} entries, {sum(len(e["examples"]) for e in entries)} examples, {sum(len(e.get("hard_negatives",[])) for e in entries)} hard negatives; no exact local duplicate examples; hard negatives map to other in-section intents; references and slots resolve.')
