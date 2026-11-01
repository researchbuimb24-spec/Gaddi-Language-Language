import json
import re

with open(r'C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

unusual = []
for e in entries:
    deva = e.get('lemma_devanagari', '')
    if re.search(r'[a-zA-ZţŢŗřḍṭṇṣśñŋːˑúíóéáàèìòù]', deva):
        unusual.append((e['id'], deva, e.get('original_transcription', '')))

print(f"Total entries with Latin/diacritic chars in lemma_devanagari: {len(unusual)}")
for u in unusual[:20]:
    print(f"  {u[0]}: {u[1]} (raw: {u[2]})")

