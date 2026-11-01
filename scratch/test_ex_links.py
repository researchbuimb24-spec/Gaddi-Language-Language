import json
from pathlib import Path

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\gaddi_examples.json", "r", encoding="utf-8") as f:
    examples = json.load(f)

ex_map = {e.get("example_id") or e.get("id"): e for e in examples}

# Test finding examples for "के"
ke_entry = next((e for e in entries if e["lemma_devanagari"] == "के"), None)
if ke_entry:
    linked = [ex_map[ex_id] for ex_id in ke_entry.get("metadata", {}).get("example_ids", []) if ex_id in ex_map]
    print(f"Linked examples for 'के': {len(linked)}")

# Test finding examples for "पाणी"
pani_entry = next((e for e in entries if e["lemma_devanagari"] == "पाणी"), None)
if pani_entry:
    linked = [ex_map[ex_id] for ex_id in pani_entry.get("metadata", {}).get("example_ids", []) if ex_id in ex_map]
    print(f"Linked examples for 'पाणी': {len(linked)}")
