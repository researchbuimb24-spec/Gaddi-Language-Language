import json

path_data = "data/gaddi_phonology.json"
path_res = "src/gaddi/resources/gaddi_phonology.json"

with open(path_data, "r", encoding="utf-8") as f:
    ph = json.load(f)

ph["appendix_i_discrepancies"] = {
    "vowels": "Appendix I Table A.2 lists 5 nasal vowels (ĩ, ũ, ẽ, ə̃, ɑ̃), whereas Chapter 2 Section 2.2.2 establishes exactly 3 lexical nasal vowels (/ũ/, /ɑ̃/, /ɛ̃/).",
    "consonants": "Appendix I Table A.1 (and Table A.3) includes fricatives /f/ and /ʃ/, velar nasal /ŋ/ as an independent phoneme, and trill /r/ alongside flap /ɽ/, whereas Chapter 2 Table 2.4 restricts native fricatives to /s, h/, treats [ŋ] as an assimilatory allophone before velars, and lists flap /ɾ/.",
    "four_audited_discrepancies": [
        {
            "category": "nasal_vowels",
            "chapter_2_analysis": "3 lexical nasal vowels (/ũ/, /ɑ̃/, /ɛ̃/) in Section 2.2.2 (p. 13)",
            "appendix_i_analysis": "5 nasal vowels (/ĩ/, /ũ/, /ẽ/, /ə̃/, /ɑ̃/) in Table A.2 (p. 118)",
            "reconciliation": "Chapter 2 reflects phonemic contrast established through minimal/sub-minimal pairs; Appendix I represents surface phonetic inventory."
        },
        {
            "category": "fricatives",
            "chapter_2_analysis": "Fricatives restricted to /s, h/ in Table 2.4 (p. 14); /f/ and /ʃ/ treated as marginal loan phonemes",
            "appendix_i_analysis": "Includes /f/ and /ʃ/ directly in the primary consonant inventory in Table A.1 (p. 117)",
            "reconciliation": "Appendix I includes contact/borrowed segments from Hindi/English; Chapter 2 isolates indigenous phonemic core."
        },
        {
            "category": "rhotics",
            "chapter_2_analysis": "Alveolar liquid described as flap /ɾ/ or trill /r/ in Table 2.4 (p. 14)",
            "appendix_i_analysis": "Table A.1 lists alveolar trill /r/ and retroflex flap /ɽ/",
            "reconciliation": "Phonetic variation between tapped [ɾ] and trilled [r] realizations depending on speaker and syllable position."
        },
        {
            "category": "approximants_and_glides",
            "chapter_2_analysis": "Charts labio-dental approximant /ʋ/; velar nasal [ŋ] is contextual allophone before velars",
            "appendix_i_analysis": "Charts labio-velar glide /w/ and lists velar nasal /ŋ/ as distinct phoneme",
            "reconciliation": "Surface phonetic charting in Appendix I vs phonological economy in Chapter 2."
        }
    ]
}

with open(path_data, "w", encoding="utf-8") as f:
    json.dump(ph, f, ensure_ascii=False, indent=2)

with open(path_res, "w", encoding="utf-8") as f:
    json.dump(ph, f, ensure_ascii=False, indent=2)

print("Phonology discrepancies updated successfully.")
