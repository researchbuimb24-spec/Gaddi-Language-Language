import json
from collections import defaultdict

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

dups = defaultdict(list)
for e in entries:
    key = (e.get('lemma_devanagari', '').strip(), e.get('variety_id', '').strip(), e.get('part_of_speech', '').strip())
    dups[key].append(e['id'])

exact_dups = {k: v for k, v in dups.items() if len(v) > 1}
print(f"Total duplicate keys in current database: {len(exact_dups)}")
for k, v in list(exact_dups.items())[:15]:
    print(f"  {k}: {v}")

