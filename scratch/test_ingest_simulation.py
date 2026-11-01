import json
import re
from pathlib import Path

# Load existing database
with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    existing_entries = json.load(f)

print(f"Existing unified entries: {len(existing_entries)}")
existing_lemmas = {e["lemma_devanagari"] for e in existing_entries if e.get("lemma_devanagari")}
print(f"Existing unique Devanagari lemmas: {len(existing_lemmas)}")

# Load comparative lexicon
with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\scratch\consolidated_comp_lex.json", "r", encoding="utf-8") as f:
    comp_lex = json.load(f)

print(f"Loaded comp lex items: {len(comp_lex)}")

