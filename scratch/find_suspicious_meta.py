import json
import re

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

suspicious = []
for e in entries:
    raw = e.get('original_transcription', '').strip().lower()
    gl = e['senses'][0].get('definition_en', '').strip().lower()
    
    # Check if raw transcription contains English commentary words
    if any(w in raw.split() for w in ['the', 'and', 'said', 'crow', 'connective', 'used', 'by', 'wars', 'black', 'near', 'go', 'into', 'when', 'did', 'he']):
        suspicious.append(e)
    # Check if raw is identical to an English phrase
    elif raw in ['said the crow', 'connective generally used by a kane', 'wars', 'black', 'near', 'go into']:
        suspicious.append(e)
    # Check if gloss is inverted (Gaddi in gloss, English in raw)
    elif any(k in gl for k in ['me apne larijo', 'so munjo tale', 'so kaRpẽjo', 'kiya kawi']):
        suspicious.append(e)

print(f"Total suspicious English/meta entries found: {len(suspicious)}")
for s in suspicious:
    print(f"ID: {s['id']} | Deva: {s['lemma_devanagari']} | Raw: '{s.get('original_transcription')}' | EN: '{s['senses'][0].get('definition_en')}'")

