import json
import re
from pathlib import Path

# Load multilingual definitions
with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\scratch\consolidated_comp_lex.json", "r", encoding="utf-8") as f:
    comp_lex = json.load(f)

# Load existing database to index by (lemma, variety)
with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    existing_entries = json.load(f)

lemma_map = {}
for e in existing_entries:
    key = (e.get("lemma_devanagari", "").strip(), e.get("variety_id", "").strip())
    lemma_map[key] = e

print(f"Existing entries: {len(existing_entries)}, unique (lemma, variety) keys: {len(lemma_map)}")

