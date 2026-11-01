with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find words with glosses: e.g. /word/ 'gloss' or word 'gloss' or word “gloss” or word ‘gloss’
pattern = re.compile(r'(?:/(?P<ipa>[^/]+)/)?\s*(?P<word>[a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-]+)\s+[‘\'"“](?P<gloss>[^’\'"”\n\r]+)[’\'"”]')

entries = []
for m in pattern.finditer(text):
    w = m.group('word').strip()
    g = m.group('gloss').strip()
    ipa = m.group('ipa').strip() if m.group('ipa') else None
    
    # Filter out English words or header words
    if w.lower() in ('means', 'called', 'that', 'with', 'which', 'and', 'also', 'the', 'is', 'for', 'this', 'in', 'it'):
        continue
    if len(w) <= 1 and w not in ('e', 'o'):
        continue
        
    entries.append({
        'word': w,
        'ipa': ipa,
        'gloss': g
    })

print(f"Extracted {len(entries)} glossed items from Chapter 2")
for e in entries[:50]:
    ipa_str = f"/{e['ipa']}/" if e['ipa'] else ""
    print(f"  {e['word']:20s} {ipa_str:15s} '{e['gloss']}'")

