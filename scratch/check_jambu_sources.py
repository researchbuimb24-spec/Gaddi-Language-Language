import json
from pathlib import Path
from collections import Counter

repo_root = Path(__file__).resolve().parent.parent
with open(repo_root / 'data/source_intake/jambu_gaddi_raw.json', encoding='utf-8') as f:
    jambu = json.load(f)

sources = Counter()
tags = Counter()
for item in jambu:
    s = item.get('Source', '')
    sources[s.split(';')[0].split('[')[0]] += 1
    t = item.get('Tags', '')
    if t:
        tags[t] += 1

print("Sources:")
for s, c in sources.most_common(15):
    print(f"  {s}: {c}")

print("\nTags:")
for t, c in tags.most_common(15):
    print(f"  {t}: {c}")
