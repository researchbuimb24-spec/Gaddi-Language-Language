import json
import re

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

print(f"Total entries loaded: {len(entries)}")

# 1. Non-Devanagari characters in lemma_devanagari
odd_devanagari = []
for e in entries:
    deva = e.get('lemma_devanagari', '')
    # Check for Latin characters, accents, question marks, brackets
    if re.search(r'[a-zA-Z\?!\(\)\[\]\{\}\<\>úíóéáàèìòùxţŢŗřḍṭṇṣśñŋ]', deva):
        odd_devanagari.append((e['id'], deva, e.get('original_transcription', ''), e['senses'][0].get('definition_en', '')))

print(f"\n--- 1. Odd/Mixed characters in lemma_devanagari: {len(odd_devanagari)} ---")
for o in odd_devanagari:
    print(f"  {o[0]}: Deva='{o[1]}' | Raw='{o[2]}' | Gloss='{o[3]}'")

# 2. Gloss check for non-neutral terms
non_neutral = []
for e in entries:
    for s in e.get('senses', []):
        en = s.get('definition_en', '').lower()
        if 'bitch' in en:
            non_neutral.append((e['id'], e.get('lemma_devanagari'), en))

print(f"\n--- 2. Non-neutral glosses (e.g., 'bitch'): {len(non_neutral)} ---")
for n in non_neutral:
    print(f"  {n[0]}: '{n[1]}' -> '{n[2]}'")

# 3. Check specific target entries
targets = ['00627', '01645', '00540', '01291', '01656', '01393', '01698', '00982', '00518', '00517']
print("\n--- 3. Specific target entries inspection ---")
for e in entries:
    if any(e['id'].endswith(t) for t in targets):
        print(f"ID: {e['id']} | Deva: {e['lemma_devanagari']} | Raw: {e.get('original_transcription')} | Variety: {e['variety_id']}")
        print(f"   Attestations: {[(a.get('source_id'), a.get('page_or_section'), a.get('transcription_raw')) for a in e.get('attestations', [])]}")
        print(f"   Senses: {[(s.get('definition_en'), s.get('definition_hi')) for s in e.get('senses', [])]}")
        print(f"   Metadata: {e.get('metadata')}")

