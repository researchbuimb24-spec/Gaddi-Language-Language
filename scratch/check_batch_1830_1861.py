import json

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

for e in entries:
    num = int(e['id'].split('-')[-1])
    if 1830 <= num <= 1861:
        print(f"ID: {e['id']} | Deva: {e['lemma_devanagari']} | Raw: '{e.get('original_transcription')}' | POS: {e['part_of_speech']} | Gloss: '{e['senses'][0]['definition_en']}'")

