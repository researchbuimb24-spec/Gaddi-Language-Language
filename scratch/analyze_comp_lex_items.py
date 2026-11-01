import json

with open('scratch/consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

empty = [it for it in items if not it.get('gaddi') or it['gaddi'].strip() in ('-', '')]
print(f"Total: {len(items)}, Empty: {len(empty)}, Valid: {len(items) - len(empty)}")

multi = [it for it in items if any(sep in it.get('gaddi', '') for sep in [',', '/', ';', 'a)', 'b)'])]
print(f"Items with multiple forms: {len(multi)}")
for m in multi[:15]:
    print(f"  {m['gloss']:20s}: {m['gaddi']}")

