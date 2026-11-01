import re
import json

with open('scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern 1: /ipa_or_word/ 'gloss'
p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
# Pattern 2: word 'gloss' (single word or phrase)
p2 = re.compile(r'([a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+){0,5})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

all_extracted = []
seen = set()

for m in p1.finditer(text):
    w = m.group(1).strip()
    g = m.group(2).strip()
    if w and g and len(w) > 1 and len(g) > 1:
        key = (w.lower(), g.lower())
        if key not in seen:
            seen.add(key)
            all_extracted.append({'word': w, 'gloss': g, 'type': 'slash_delimited'})

for m in p2.finditer(text):
    w = m.group(1).strip()
    g = m.group(2).strip()
    # Filter non-Gaddi words
    w_low = w.lower()
    if any(w_low.startswith(ex) for ex in ['the word', 'called', 'means', 'table', 'chapter', 'figure']):
        continue
    if w_low in ('means', 'called', 'that', 'with', 'which', 'and', 'also', 'the', 'is', 'for', 'this', 'in', 'it', 'there', 'who', 'how', 'when', 'where', 'some', 'they', 'you', 'she', 'him', 'her', 'we', 'i'):
        continue
    if len(w) > 1 and len(g) > 1:
        key = (w.lower(), g.lower())
        if key not in seen:
            seen.add(key)
            all_extracted.append({'word': w, 'gloss': g, 'type': 'space_delimited'})

print(f"Total extracted items from Chapter 2: {len(all_extracted)}")

single_words = [it for it in all_extracted if ' ' not in it['word']]
multi_words = [it for it in all_extracted if ' ' in it['word']]

print(f"Single words: {len(single_words)}")
print(f"Multiword expressions: {len(multi_words)}")

print("\nSample multiword expressions:")
for m in multi_words[:25]:
    print(f"  {m['word']:30s} -> '{m['gloss']}'")

print("\nSample single words:")
for s in single_words[:25]:
    print(f"  {s['word']:30s} -> '{s['gloss']}'")

