import json

with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

targets = ['कú', 'माबुरा', 'एज़िज़', 'गोबरू', 'कड़पा', 'ग्रोड्डु']
for t in targets:
    matches = [e for e in entries if t in e.get('lemma_devanagari', '') or any(t in a.get('transcription_raw', '') for a in e.get('attestations', [])) or t in str(e)]
    print(f"=== TARGET: {t} (Matches: {len(matches)}) ===")
    for m in matches:
        print(f"ID: {m['id']} | Lemma: {m['lemma_devanagari']} | Raw: {m.get('original_transcription')} | Variety: {m['variety_id']} | POS: {m['part_of_speech']}")
        for a in m.get('attestations', []):
            print(f"   Attestation: {a.get('source_id')} | Page: {a.get('page_or_section')} | Raw: {a.get('transcription_raw')}")
        for s in m.get('senses', []):
            print(f"   Sense: EN='{s.get('definition_en')}' | HI='{s.get('definition_hi')}'")

