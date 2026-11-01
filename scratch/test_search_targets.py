from gaddi.dictionary import GaddiDictionary

d = GaddiDictionary()
test_words = ['कू', 'माबुरा', 'एज़िज़', 'गोबरू', 'कड़पा', 'ग्रोड्डु', 'female dog', 'kú', 'eziz']
for tw in test_words:
    res = d.search(tw)
    print(f'Search "{tw}": {len(res)} result(s)')
    for r in res[:2]:
        orig = r.original_transcription or r.metadata.get('source_transcription', 'n/a')
        print(f"   [{r.id}] {r.lemma_devanagari} ({r.part_of_speech}) | Orig: {orig} | EN: {r.senses[0].definition_en}")

