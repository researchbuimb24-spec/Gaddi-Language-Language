import json

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

print("--- Searching for ú or similar characters ---")
for e in entries:
    if 'ú' in e.get('lemma_devanagari', '') or 'ú' in e.get('original_transcription', '') or 'ú' in str(e):
        print(f"ID: {e['id']} | Deva: {e['lemma_devanagari']} | Raw: {e.get('original_transcription')}")

print("\n--- Searching for kaRpa or snake ---")
for e in entries:
    raw = e.get('original_transcription', '').lower()
    gl = str(e.get('senses', [])).lower()
    if 'karpa' in raw or 'kaṛpa' in raw or 'kaRpa' in e.get('original_transcription', '') or 'snake' in gl:
        print(f"ID: {e['id']} | Deva: {e['lemma_devanagari']} | Raw: {e.get('original_transcription')} | Gloss: {e['senses'][0]['definition_en']}")

