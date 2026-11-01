import json

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

multiwords = [e for e in entries if e.get('part_of_speech') == 'phrase' or e.get('metadata', {}).get('is_multiword') or ' ' in e.get('lemma_devanagari', '')]

print(f"Total multiword expressions: {len(multiwords)}")
print("\nSample multiword expressions (first 30):")
for m in multiwords[:30]:
    print(f"ID: {m['id']} | Deva: {m['lemma_devanagari']:25s} | Raw: {m.get('original_transcription', ''):25s} | EN: {m['senses'][0].get('definition_en')}")

print("\nSample multiword expressions (last 30):")
for m in multiwords[-30:]:
    print(f"ID: {m['id']} | Deva: {m['lemma_devanagari']:25s} | Raw: {m.get('original_transcription', ''):25s} | EN: {m['senses'][0].get('definition_en')}")

