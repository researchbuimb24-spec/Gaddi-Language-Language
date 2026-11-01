import json
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

with open(repo_root / "data/dictionary_unified.json", encoding="utf-8") as f:
    uni = json.load(f)

lemmas = set(e["lemma_devanagari"] for e in uni if e.get("lemma_devanagari"))
print("Total unified entries:", len(uni))
print("Total unique Devanagari headwords:", len(lemmas))

# Source records count
total_attestations = sum(len(e.get("attestations", [])) for e in uni)
print("Total source attestations:", total_attestations)

# Categories count
from collections import Counter
cats = Counter()
for e in uni:
    for c in e.get("metadata", {}).get("categories", []):
        cats[c] += 1
print("Categories count:", len(cats))
print("Categories sum:", sum(cats.values()))
for c, count in cats.most_common():
    print(f"  {c}: {count}")

