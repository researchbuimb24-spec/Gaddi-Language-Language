import json
import unicodedata
from collections import defaultdict

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFC", text).strip().lower()

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Total entries before duplicate merge: {len(entries)}")

# Key for exact duplicate: (lemma_devanagari, variety_id, evidence_status, pos, main_concept)
def get_main_concept(e):
    senses = e.get("senses", [])
    if not senses:
        return ""
    en = senses[0].get("definition_en", "").lower()
    # simplify: strip punctuation and parentheticals
    import re
    en = re.sub(r"\(.*?\)", "", en)
    words = [w.strip(".,;:!?\"'") for w in en.split() if len(w) > 2]
    # return first 2 significant words
    return " ".join(words[:2])

# Group by lemma + variety + status
groups = defaultdict(list)
for e in entries:
    lemma = e.get("lemma_devanagari", "").strip()
    var = e.get("variety_id", "")
    status = e.get("evidence_status", "")
    pos = (e.get("part_of_speech") or "").lower()
    concept = get_main_concept(e)
    # If concept matches or is identical
    key = (lemma, var, status, pos, concept)
    groups[key].append(e)

mergeable = {k: v for k, v in groups.items() if len(v) > 1}
print(f"Mergeable duplicate groups found: {len(mergeable)}")
for k, v in list(mergeable.items())[:10]:
    print(f"Group: {k[0]} ({k[1]}, {k[3]}, '{k[4]}') -> {len(v)} records")
