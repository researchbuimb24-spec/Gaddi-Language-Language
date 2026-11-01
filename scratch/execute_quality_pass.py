import json
import re
from pathlib import Path
import shutil

repo_root = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language")
data_path = repo_root / "data" / "dictionary_unified.json"
res_path = repo_root / "src" / "gaddi" / "resources" / "dictionary_unified.json"

with open(data_path, "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Total entries before quality pass: {len(entries)}")

corrected_count = 0
enriched_count = 0
marked_uncertain_count = 0
unchanged_count = 0
suspicious_for_review = []

# Specific corrections and metadata for the 39 mixed-script entries and questionable items
CLEANUP_MAP = {
    "gaddi-uni-00222": {"deva": "चिफला", "uncertain": False, "notes": "Romanized tʃiflɑ normalized to Devanagari चिफला (smooth). Source form preserved."},
    "gaddi-uni-00310": {"deva": "दश", "uncertain": True, "notes": "Source Bailey/Jambu records phonetic 'dax' for numeral ten (standard दस/दश). Phonetic -x preserved in original transcription."},
    "gaddi-uni-00380": {"deva": "बेख", "uncertain": True, "notes": "Source Bailey/Jambu records 'bēx' for sit (standard बहणा/बैसणा). Phonetic -x preserved."},
    "gaddi-uni-00384": {"deva": "खौ", "uncertain": True, "notes": "Source Bailey/Jambu records 'xau' for hundred (standard सौ/सोह). Phonetic x- preserved."},
    "gaddi-uni-00461": {"deva": "खराळ", "uncertain": True, "notes": "Source Bailey/Jambu records 'xarāḷ' for hair (standard वाल/केस). Phonetic x- preserved."},
    "gaddi-uni-00526": {"deva": "मोटी भियालु", "uncertain": False, "notes": "Compound moţţabʰiyalu normalized to मोटी भियालु (elder brother: moţţa 'big' + bhiyalu 'brother')."},
    "gaddi-uni-00530": {"deva": "बुड़ा", "uncertain": False, "notes": "Source buŗa normalized to Devanagari बुड़ा (father / old man)."},
    "gaddi-uni-00537": {"deva": "ब्याह", "uncertain": True, "notes": "Source prints 'biy?a' with OCR/phonetic glottal stop artifact; represents byah/byaha (marriage)."},
    "gaddi-uni-00540": {"deva": "एज़िज़", "uncertain": True, "notes": "Source LSI 2023 p. 1090 item 50 prints 'amma/eziz' for 'mother'. 'eziz' is an idiosyncratic phonetic transcription of Bharmauri/Western Pahari vocative/diminutive ijji/ijei (mother). Preserved exactly as printed."},
    "gaddi-uni-00552": {"deva": "गूंगा (तत्ता)", "uncertain": False, "notes": "Formatted parenthetical variant from source gunga(tatta)."},
    "gaddi-uni-00563": {"deva": "काखी (छाछी)", "uncertain": False, "notes": "Formatted parenthetical variant from source kakʰi(cʰācʰi) (ant)."},
    "gaddi-uni-00600": {"deva": "मुंडु", "uncertain": False, "notes": "Stripped acute accent from múndu to clean Devanagari मुंडु (head)."},
    "gaddi-uni-00604": {"deva": "फीफेरु", "uncertain": False, "notes": "Transliterated fiipʰeru to Devanagari फीफेरु (lung)."},
    "gaddi-uni-00625": {"deva": "दार (बिधु)", "uncertain": False, "notes": "Formatted parenthetical variant from source dār(bidʰu) (door)."},
    "gaddi-uni-00627": {"deva": "कू", "uncertain": True, "notes": "Source LSI 2023 p. 1092 item 146 prints 'kú' for 'well water' with acute accent marking pitch/stress. Likely represents Western Pahari kū̃ / kuā (well/well-water). Kept source transcription with uncertainty flag."},
    "gaddi-uni-00636": {"deva": "फ्हल", "uncertain": True, "notes": "Source LSI 2023 p. 1092 prints 'fhal' for coconut. Preserved with uncertainty note."},
    "gaddi-uni-00656": {"deva": "कुम्हारे", "uncertain": False, "notes": "Normalized kumàre to Devanagari कुम्हारे (potter)."},
    "gaddi-uni-00660": {"deva": "फल", "uncertain": False, "notes": "Normalized fal to Devanagari फल (fruit)."},
    "gaddi-uni-00720": {"deva": "छारे", "uncertain": False, "notes": "Normalized cʰáre to Devanagari छारे (forty)."},
    "gaddi-uni-00728": {"deva": "साफ-सुथरा", "uncertain": False, "notes": "Normalized sāfcʰudra to Devanagari साफ-सुथरा (clean)."},
    "gaddi-uni-00744": {"deva": "धक्का देणा", "uncertain": False, "notes": "Normalized dakkʰadéna to Devanagari धक्का देणा (push)."},
    "gaddi-uni-00750": {"deva": "कुआणा", "uncertain": True, "notes": "Source prints 'ku?ana' for climb with OCR artifact question mark."},
    "gaddi-uni-00752": {"deva": "आगु-पिछु", "uncertain": False, "notes": "Normalized àgupicʰu to Devanagari आगु-पिछु (drag forward/backward)."},
    "gaddi-uni-00764": {"deva": "कुआरा", "uncertain": True, "notes": "Source prints 'ku? ara' for sprinkle with OCR artifact question mark."},
    "gaddi-uni-00798": {"deva": "भाणा", "uncertain": False, "notes": "Normalized bʰána to Devanagari भाणा (cultivate)."},
    "gaddi-uni-00805": {"deva": "बिआणा", "uncertain": True, "notes": "Source prints 'bi?ana' for sow with OCR artifact question mark."},
    "gaddi-uni-00818": {"deva": "थेणा", "uncertain": False, "notes": "Normalized tʰéna to Devanagari थेणा (keep/place)."},
    "gaddi-uni-00844": {"deva": "पोक्का", "uncertain": True, "notes": "Source prints 'pokka?a' for annoy with OCR artifact question mark."},
    "gaddi-uni-00865": {"deva": "रोजे", "uncertain": False, "notes": "Normalized róje to Devanagari रोजे (again)."},
    "gaddi-uni-00866": {"deva": "पेहले", "uncertain": False, "notes": "Normalized pehlé to Devanagari पेहले (always/before)."},
    "gaddi-uni-00883": {"deva": "कुसेरा (सेरा)", "uncertain": False, "notes": "Formatted parenthetical variant from kusera(sĕra) (it/this)."},
    "gaddi-uni-00884": {"deva": "मुंजू (मेरताँये)", "uncertain": False, "notes": "Formatted parenthetical variant from munju (meratãye) (like/for me)."},
    "gaddi-uni-00931": {"deva": "खूना", "uncertain": False, "notes": "Normalized kʰúna to Devanagari खूना (soft)."},
    "gaddi-uni-00938": {"deva": "बकार (बार)", "uncertain": True, "notes": "Source prints 'bakar (ba? r)' for out with OCR artifact question mark."},
    "gaddi-uni-00946": {"deva": "बुईया", "uncertain": True, "notes": "Source prints 'bu? ya' (likely bui/buiya or buṭṭa 'below/down') with OCR artifact question mark."},
    "gaddi-uni-00956": {"deva": "साला (जीजा)", "uncertain": False, "notes": "Formatted parenthetical variant from salā (jija) (brother-in-law)."},
    "gaddi-uni-00957": {"deva": "साली (दरोजी)", "uncertain": False, "notes": "Formatted parenthetical variant from sali(daroji) (sister-in-law)."},
    "gaddi-uni-00959": {"deva": "मूछा", "uncertain": False, "notes": "Normalized múcʰa to Devanagari मूछा (moustache)."},
    "gaddi-uni-00962": {"deva": "किन्ना (इन्ना)", "uncertain": False, "notes": "Formatted parenthetical variant from kinna(inna) (to me)."},
    "gaddi-uni-00965": {"deva": "अखो", "uncertain": True, "notes": "Source prints 'axō' for this year with phonetic -x-."},
    "gaddi-uni-00966": {"deva": "अखोका", "uncertain": True, "notes": "Source prints 'axokā' for of this year with phonetic -x-."},
    "gaddi-uni-01095": {"deva": "चिफला", "uncertain": False, "notes": "Normalized cifla to Devanagari चिफला (smooth)."},
    "gaddi-uni-01291": {"deva": "गोबरू", "uncertain": False, "notes": "Authentic Western Pahari go:bru (boy/son)."},
    "gaddi-uni-01393": {"deva": "ग्रोड्डु", "uncertain": False, "notes": "Authentic Bharmauri initial-cluster groDDu (spider)."},
    "gaddi-uni-01645": {"deva": "माबुरा", "uncertain": False, "notes": "Authentic Bharmauri dvandva compound ma+bura > mabura (parents)."},
}

# The 6 English/commentary entries to correct
COMMENTARY_CORRECTIONS = {
    "gaddi-uni-01848": {
        "lemma": "ए दुई और त्रै गोबरू घरा मंज कुसुदिन्दे",
        "raw": "e dui aur thray gobru ghara manj kusudinde",
        "en": "These two or three boys go into the house",
        "hi": "ये दो या तीन लड़के घर में जाते हैं",
        "pos": "phrase"
    },
    "gaddi-uni-01853": {
        "lemma": "में अपने लाड़ीजो हवा गहणे आन्देन्",
        "raw": "me apne larijo howa gane anden",
        "en": "I have brought new ornaments for my wife",
        "hi": "मैंने अपनी पत्नी (लाड़ी) के लिए नए गहने लाए हैं",
        "pos": "phrase"
    },
    "gaddi-uni-01862": {
        "lemma": "कने",
        "raw": "kane",
        "en": "and (coordinating conjunction)",
        "hi": "और (संयोजक)",
        "pos": "conjunction"
    },
    "gaddi-uni-01863": {
        "lemma": "भारत कने पाकिस्तान मंज युद्ध-भुआ-तू",
        "raw": "bharat kane pakistan manj yud-bhua-tu",
        "en": "There was a war between India and Pakistan",
        "hi": "भारत और पाकिस्तान के बीच युद्ध हुआ था",
        "pos": "phrase"
    },
    "gaddi-uni-01864": {
        "lemma": "तसरी लाड़ी दुक्की बियी करे बल्लू",
        "raw": "tasari lari dukki biyi kare ballu",
        "en": "said his wife in despair",
        "hi": "उसकी पत्नी ने दुखी होकर कहा",
        "pos": "phrase"
    },
    "gaddi-uni-01865": {
        "lemma": "काए बल्लू",
        "raw": "kaye ballu",
        "en": "the crow said",
        "hi": "कौवे ने कहा",
        "pos": "phrase"
    },
    "gaddi-uni-01698": {
        "lemma": "सो कड़पेंजो मारी दित्ता",
        "raw": "so kaRpẽjo maridtta",
        "en": "She killed the snake",
        "hi": "उसने साँप को मार दिया",
        "pos": "phrase"
    }
}

for e in entries:
    eid = e["id"]
    was_modified = False

    # 1. Base metadata enrichment: source form preservation & transliteration provenance
    orig = e.get("original_transcription", "").strip()
    if "metadata" not in e:
        e["metadata"] = {}
    
    if orig and not e["metadata"].get("source_transcription"):
        e["metadata"]["source_transcription"] = orig

    # Determine transliteration source
    if not e["metadata"].get("transliteration_source"):
        has_kumari = any(a.get("source_id") == "kumari_2026" for a in e.get("attestations", []))
        has_cultural = e.get("evidence_status") in ("jk_cultural_term", "jk_place_or_ecological_term")
        if (has_kumari or has_cultural) and not any(a.get("source_id") == "census_2023_lsi" for a in e.get("attestations", [])):
            e["metadata"]["transliteration_source"] = "source_devanagari"
            e["metadata"]["source_attested_spelling"] = True
        else:
            e["metadata"]["transliteration_source"] = "derived_transliteration"
            e["metadata"]["source_attested_spelling"] = False
        enriched_count += 1
        was_modified = True

    # 2. Check neutral glosses (female dog vs bitch)
    for s in e.get("senses", []):
        en_gloss = s.get("definition_en", "")
        if "bitch" in en_gloss.lower():
            if en_gloss.lower().strip() == "bitch":
                s["definition_en"] = "female dog"
                s["definition_hi"] = "कुतिया (मादा कुत्ता)"
            elif en_gloss.lower().strip() == "bitches":
                s["definition_en"] = "female dogs"
                s["definition_hi"] = "कुतियाँ (मादा कुत्ते)"
            else:
                s["definition_en"] = re.sub(r'\bbitches\b', 'female dogs', s["definition_en"], flags=re.I)
                s["definition_en"] = re.sub(r'\bbitch\b', 'female dog', s["definition_en"], flags=re.I)
            corrected_count += 1
            was_modified = True

    # 3. Check Commentary corrections
    if eid in COMMENTARY_CORRECTIONS:
        c = COMMENTARY_CORRECTIONS[eid]
        e["lemma_devanagari"] = c["lemma"]
        e["original_transcription"] = c["raw"]
        e["metadata"]["source_transcription"] = c["raw"]
        e["part_of_speech"] = c["pos"]
        e["senses"][0]["definition_en"] = c["en"]
        e["senses"][0]["definition_hi"] = c["hi"]
        e["metadata"]["is_multiword"] = (" " in c["lemma"] or c["pos"] == "phrase")
        corrected_count += 1
        was_modified = True

    # 4. Check Cleanup Map (Devanagari normalization & uncertainty notes)
    if eid in CLEANUP_MAP:
        cl = CLEANUP_MAP[eid]
        e["lemma_devanagari"] = cl["deva"]
        if cl.get("uncertain"):
            e["metadata"]["is_uncertain"] = True
            e["metadata"]["uncertainty_notes"] = cl["notes"]
            marked_uncertain_count += 1
            suspicious_for_review.append({"id": eid, "deva": cl["deva"], "raw": orig, "notes": cl["notes"]})
        else:
            e["metadata"]["is_uncertain"] = False
            if cl.get("notes"):
                e["metadata"]["notes"] = cl["notes"]
        corrected_count += 1
        was_modified = True

    # 5. Check other uncertain forms (containing '?' in raw transcription)
    if "?" in orig and eid not in CLEANUP_MAP:
        e["metadata"]["is_uncertain"] = True
        e["metadata"]["uncertainty_notes"] = f"Raw source transcription '{orig}' contains OCR or phonetic question mark."
        marked_uncertain_count += 1
        suspicious_for_review.append({"id": eid, "deva": e["lemma_devanagari"], "raw": orig, "notes": e["metadata"]["uncertainty_notes"]})
        was_modified = True

    if not was_modified:
        unchanged_count += 1

print(f"\n--- Quality Pass Execution Summary ---")
print(f"Corrected entries: {corrected_count}")
print(f"Enriched entries (metadata/provenance/neutral): {enriched_count}")
print(f"Marked uncertain entries: {marked_uncertain_count}")
print(f"Unchanged core entries: {unchanged_count}")
print(f"Suspicious entries flagged for human review: {len(suspicious_for_review)}")

# Save updated dataset
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

shutil.copyfile(data_path, res_path)

with open(data_path, "rb") as f1, open(res_path, "rb") as f2:
    assert f1.read() == f2.read()

print("Synchronized data/dictionary_unified.json and src/gaddi/resources/dictionary_unified.json successfully.")

