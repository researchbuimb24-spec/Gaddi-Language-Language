import json

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

for e in entries:
    deva = e.get('lemma_devanagari', '')
    raw = e.get('original_transcription', '')
    if 'कड़प' in deva or 'kaRpa' in raw or 'kaṛpa' in raw or 'kala kaRpa' in raw:
        print(f"ID: {e['id']} | Deva: {deva} | Raw: {raw} | POS: {e['part_of_speech']} | Gloss: {e['senses'][0]['definition_en']}")

