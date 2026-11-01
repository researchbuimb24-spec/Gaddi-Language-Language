import json
from pathlib import Path

# Load unified
uni_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
with open(uni_path, "r", encoding="utf-8") as f:
    unified = json.load(f)

# Load examples
ex_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\gaddi_examples.json")
with open(ex_path, "r", encoding="utf-8") as f:
    examples = json.load(f)

print(f"Loaded {len(unified)} unified entries and {len(examples)} examples.")

# Test finding examples for "water" or "पाणी"
matches = [ex for ex in examples if "water" in ex.get("english_translation", "").lower() or "paːɳi" in ex.get("gaddi_transcription", "").lower()]
print(f"Examples for water: {len(matches)}")
for m in matches[:2]:
    print(f"  Ex #{m.get('example_number')}: {m.get('gaddi_transcription')} -> {m.get('english_translation')}")
