import json
import re
from pathlib import Path

# Load consolidated comparative lexicon
with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

print(f"Loaded {len(comp_lex)} comparative lexicon rows")

# Filter rows that have Gaddi forms
gaddi_rows = [r for r in comp_lex if r.get('gaddi') and r['gaddi'].strip() != '-']
print(f"Non-empty Gaddi rows: {len(gaddi_rows)}")

# Sample inspection
for r in gaddi_rows[:15]:
    print(f"  {r['sl_no']:3d}: Gloss='{r['gloss']}' | Gaddi='{r['gaddi']}' (Printed p. {r['printed_page']})")

