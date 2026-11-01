import re

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern 1: /ipa_or_word/ 'gloss'
# Pattern 2: word 'gloss'
p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
p2 = re.compile(r'([^\s/\n\r]+(?:[\s\-][^\s/\n\r]+){0,4})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

items1 = p1.findall(text)
print("Pattern 1 (/.../ 'gloss'):", len(items1))
for w, g in items1[:20]:
    print(f"  /{w}/ -> '{g}'")

items2 = p2.findall(text)
print("\nPattern 2 (word 'gloss'):", len(items2))
for w, g in items2[:20]:
    print(f"  {w} -> '{g}'")

