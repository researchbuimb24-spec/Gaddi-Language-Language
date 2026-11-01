import json
from pathlib import Path
from gaddi.models import LexicalEntry

uni_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
with open(uni_path, "r", encoding="utf-8") as f:
    raw = json.load(f)

entries = [LexicalEntry.from_dict(d) for d in raw]

# Test finding water in English
water_matches = [e for e in entries if any("water" in (s.definition_en or "").lower().split() for s in e.senses)]
print("Water matches:", len(water_matches), [e.lemma_devanagari for e in water_matches])

# Test finding animals
animal_matches = [e for e in entries if "animals" in e.metadata.get("categories", [])]
print("Animal matches:", len(animal_matches), [e.lemma_devanagari for e in animal_matches[:5]])

# Test finding family
family_matches = [e for e in entries if "family" in e.metadata.get("categories", [])]
print("Family matches:", len(family_matches), [e.lemma_devanagari for e in family_matches[:5]])
