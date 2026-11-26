import json, re
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path('/home/cruz1122/dev/hacka-airplane')
base=root/'research_notes/Conocimiento turístico de Los Nevados'
schema=json.loads((base/'inputs/knowledge-section.schema.json').read_text())
data=json.loads((root/'data/knowledge/sections/rules.json').read_text())
errors=list(Draft202012Validator(schema).iter_errors(data))
for e in errors: print('SCHEMA', '/'.join(map(str,e.absolute_path)),e.message)
ids={e['id'] for f in (root/'data/knowledge/sections').glob('*.json') for e in json.loads(f.read_text())['entries']}  # refs may cross sections
examples=[]
for e in data['entries']:
 label_words=re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b",e['label'])
 if not 3<=len(label_words)<=8: print('LABEL_WORDS',e['id'],len(label_words),e['label'])
 if len(e['examples'])<12: print('EXAMPLE_COUNT',e['id'],len(e['examples']))
 if not 2<=len(e.get('hard_negatives',[]))<=4: print('NEG_COUNT',e['id'],len(e.get('hard_negatives',[])))
 examples += [(s.casefold().strip(),e['id']) for s in e['examples']]
 for n in e.get('needs',[]):
  if n not in data['clarification'].get('slot_questions',{}): print('MISSING_SLOT',e['id'],n)
 for ref in e.get('related',[]):
  if ref not in ids: print('BAD_RELATED',e['id'],ref)
for ref in data.get('featured',[]):
 if ref not in ids: print('BAD_FEATURED',ref)
for s,n in Counter(x[0] for x in examples).items():
 if n>1: print('DUP_EXAMPLE',s,[e for x,e in examples if x==s])
print('SCHEMA_ERRORS',len(errors),'ENTRIES',len(data['entries']),'EXAMPLES',sum(len(e['examples']) for e in data['entries']),'LOCAL_EXAMPLE_DUPLICATES',sum(n-1 for n in Counter(x[0] for x in examples).values() if n>1),'REFERENCES_OK')
