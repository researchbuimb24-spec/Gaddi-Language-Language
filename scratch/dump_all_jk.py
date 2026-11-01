import json

data = json.load(open('data/lexicon_jk.json', encoding='utf-8'))
for i, e in enumerate(data):
    print(f"{i+1:3d}. id={e['id']}: dev={e['lemma_devanagari']!r}, ipa={e['lemma_ipa']!r}, orig={e['original_transcription']!r}, cats={e['metadata'].get('categories')}")

