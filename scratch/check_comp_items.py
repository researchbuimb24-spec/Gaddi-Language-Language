import json

with open('scratch/consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for sl in [38, 44, 48, 50, 53, 55, 146, 466]:
    matches = [it for it in items if it.get('sl_no') == sl]
    for m in matches:
        print(f"Sl: {m['sl_no']} | Gloss: {m['gloss']} | Gaddi: {m.get('gaddi')} | Printed p.: {m['printed_page']} | PDF p.: {m['pdf_page']}")

