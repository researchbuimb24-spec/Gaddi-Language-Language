import json

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

glosses = [r['gloss'].lower().strip() for r in comp_lex if r.get('gaddi') and r['gaddi'] != '-']
print(f"Total non-empty Gaddi rows: {len(glosses)}")
print(f"Unique English glosses: {len(set(glosses))}")

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/comp_glosses.txt', 'w', encoding='utf-8') as f:
    for g in sorted(list(set(glosses))):
        f.write(g + "\n")

