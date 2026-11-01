import json
import re

# Chapter 6 glosses
with open('scratch/consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

comp_glosses = set()
for r in comp_lex:
    if r.get('gaddi') and r['gaddi'].strip() != '-':
        comp_glosses.add(r['gloss'].strip().lower())

print(f"Unique glosses in Chapter 6: {len(comp_glosses)}")

# Chapter 2 glosses
with open('scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
p2 = re.compile(r'([a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+){0,5})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

ch2_glosses = set()
for m in p1.finditer(text):
    g = m.group(2).strip().lower()
    if len(g) > 1 and not any(k in g for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table']):
        ch2_glosses.add(g)

for m in p2.finditer(text):
    g = m.group(2).strip().lower()
    if len(g) > 1 and not any(k in g for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table']):
        ch2_glosses.add(g)

print(f"Unique glosses in Chapter 2: {len(ch2_glosses)}")

all_glosses = sorted(list(comp_glosses | ch2_glosses))
print(f"Total unique English concepts to map to Hindi: {len(all_glosses)}")

with open('scratch/all_unique_glosses.txt', 'w', encoding='utf-8') as f:
    for g in all_glosses:
        f.write(g + '\n')

print("Wrote scratch/all_unique_glosses.txt")

