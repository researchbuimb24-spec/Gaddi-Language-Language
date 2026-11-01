import json
from collections import defaultdict

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

groups = defaultdict(list)
for e in entries:
    lemma = e.get("lemma_devanagari", "").strip()
    var = e.get("variety_id", "")
    pos = (e.get("part_of_speech") or "").lower()
    groups[(lemma, var, pos)].append(e)

for k, v in groups.items():
    if len(v) > 1:
        s = [it["senses"][0].get("definition_en") for it in v if it.get("senses")]
        print(f"{k[0]} ({k[1]}, {k[2]}): {s}")
