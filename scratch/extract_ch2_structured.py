import re
import json

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for /word/ 'gloss' or word 'gloss'
p_gloss = re.compile(r'(?:/(?P<ipa>[^/\n\r]+)/)?\s*(?P<word>[a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+)*)\s+[‘\'"“](?P<gloss>[^’\'"”\n\r]+)[’\'"”]')

ch2_items = []
seen = set()

for m in p_gloss.finditer(text):
    w = m.group('word').strip()
    g = m.group('gloss').strip()
    ipa = m.group('ipa').strip() if m.group('ipa') else None
    
    # Filter non-words and meta terms
    if not w or len(w) < 2:
        continue
    w_clean = re.sub(r'[\s\-]+', ' ', w)
    if w_clean.lower() in ('means', 'called', 'that', 'with', 'which', 'and', 'also', 'the', 'is', 'for', 'this', 'in', 'it', 'there', 'who', 'how', 'when', 'where', 'some', 'they', 'you', 'she', 'him', 'her', 'we', 'i'):
        continue
    if any(k in g.lower() for k in ['building blocks', 'table', 'phoneme', 'vowel', 'consonant', 'chapter']):
        continue
    if len(g) < 2:
        continue
        
    key = (w_clean.lower(), g.lower())
    if key not in seen:
        seen.add(key)
        ch2_items.append({
            'word': w_clean,
            'ipa': ipa,
            'gloss': g
        })

print(f"Extracted {len(ch2_items)} distinct lexical items from Chapter 2")
for item in ch2_items[:30]:
    print(f"  {item['word']:25s} -> '{item['gloss']}' (ipa: {item['ipa']})")

