import json
import shutil
from pathlib import Path

repo_root = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language")
data_path = repo_root / "data" / "dictionary_unified.json"
res_path = repo_root / "src" / "gaddi" / "resources" / "dictionary_unified.json"

with open(data_path, "r", encoding="utf-8") as f:
    entries = json.load(f)

for e in entries:
    if e["id"] == "gaddi-uni-01698":
        e["lemma_devanagari"] = "कड़पा"
        e["original_transcription"] = "kaRpa"
        e["part_of_speech"] = "noun"
        e["metadata"]["source_transcription"] = "kaRpa"
        e["metadata"]["is_multiword"] = False
        e["metadata"]["notes"] = "Authentic Bharmauri noun for snake (kaṛpa / khaṛpa), documented in LSI 2023 Chapter 2, p. 93 and Section 6 narrative text (pp. 113-118)."
        e["metadata"]["variants"] = ["kaRpa", "kala kaRpa", "khaRpa", "काला कड़पा", "सो कड़पेंजो मारी दित्ता", "so kaRpẽjo maridtta"]
        e["senses"] = [
            {
                "sense_index": 1,
                "definition_en": "snake; black snake",
                "definition_hi": "साँप / सर्प (कड़पा / काला कड़पा)",
                "definition_ur": None,
                "semantic_field": "animals",
                "examples": [
                    {
                        "text_gaddi": "so kaRpẽjo maridtta",
                        "translation_en": "She killed the snake",
                        "translation_hi": "उसने साँप को मार दिया"
                    }
                ]
            }
        ]

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

shutil.copyfile(data_path, res_path)
print("Updated gaddi-uni-01698 to कड़पा successfully.")

