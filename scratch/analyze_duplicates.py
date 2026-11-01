import json
from collections import defaultdict

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Total entries: {len(entries)}")

by_lemma = defaultdict(list)
for e in entries:
    by_lemma[e["lemma_devanagari"]].append(e)

dups = {k: v for k, v in by_lemma.items() if len(v) > 1}
print(f"Lemmas with multiple entries: {len(dups)}")
for k, v in list(dups.items())[:15]:
    print(f"\nLemma: {k} ({len(v)} entries)")
    for item in v:
        senses = [s.get("definition_en", "")[:40] for s in item.get("senses", [])]
        sources = [a.get("source_id") for a in item.get("attestations", [])]
        print(f"  [{item['id']}] variety: {item['variety_id']}, senses: {senses}, sources: {sources}")
