from simulate_expansion import all_entries

weather_entries = [e for e in all_entries if any('weather' in s['definition_en'].lower() for s in e['senses'])]
print(f"Total weather entries: {len(weather_entries)}")
for w in weather_entries:
    print(f"  ID: {w['id']} | Deva: {w['lemma_devanagari']} | Raw: {w['original_transcription']} | Gloss: {w['senses'][0]['definition_en']}")

