import json
import unicodedata

def fold_text(text: str) -> str:
    if not text:
        return ""
    s = unicodedata.normalize("NFD", text.lower().strip())
    s = "".join(c for c in s if not unicodedata.combining(c))
    subs = {
        "tʃ": "ch", "dʒ": "j",
        "ɑ": "a", "ʌ": "a", "ə": "a", "ä": "a", "ā": "a", "á": "a",
        "ɪ": "i", "ī": "i", "í": "i",
        "ʊ": "u", "ū": "u", "ú": "u",
        "ɛ": "e", "ē": "e", "é": "e",
        "ɔ": "o", "ō": "o", "ó": "o",
        "ʈ": "t", "ṭ": "t",
        "ɖ": "d", "ḍ": "d", "ɽ": "r", "ṛ": "r",
        "ɳ": "n", "ṇ": "n", "ñ": "n", "ɲ": "n", "ŋ": "n",
        "ʃ": "s", "ś": "s", "ṣ": "s",
        "ɭ": "l", "ḷ": "l",
        "ʱ": "h", "ʰ": "h",
        "ː": "", "ˑ": "", "'": "", "ˈ": "", "ˌ": "", "̃": "", "~": "",
    }
    for k, v in subs.items():
        s = s.replace(k, v)
    return s.replace("़", "")

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

def test_search(query):
    clean_q = query.strip()
    q_lower = clean_q.lower()
    q_folded = fold_text(clean_q)
    scored = []
    for e in entries:
        score = 0
        lemma_d = e.get("lemma_devanagari", "")
        lemma_ipa = e.get("lemma_ipa", "") or ""
        norm_h = e.get("normalized_headword", "") or ""
        variants = e.get("metadata", {}).get("variants", [])
        senses = e.get("senses", [])
        
        # 1. Exact Devanagari
        if clean_q == lemma_d:
            score = 1000
        elif clean_q == lemma_d.replace("़", ""):
            score = 950
        # 2. Exact IPA / Roman
        elif q_lower == lemma_ipa.lower():
            score = 900
        elif q_folded == fold_text(lemma_ipa) or (norm_h and q_folded == fold_text(norm_h)):
            score = 850
        # 3. Exact variant
        elif any(q_lower == (v or "").lower() for v in variants):
            score = 800
        elif any(q_folded == fold_text(v or "") for v in variants):
            score = 770
        # 4. Prefix match
        elif lemma_d.startswith(clean_q):
            score = 700
        elif lemma_ipa and fold_text(lemma_ipa).startswith(q_folded):
            score = 670
        elif norm_h and fold_text(norm_h).startswith(q_folded):
            score = 650
        # 5. Exact word in definition
        elif any(clean_q == (s.get("definition_hi") or "").strip("।,;()\"' ") for s in senses):
            score = 600
        elif any(q_lower == (s.get("definition_en") or "").lower().strip(",.()[]{}:;\"' ") for s in senses):
            score = 590
        elif any(q_lower in [t.strip(",.()[]{}:;\"' ") for t in (s.get("definition_en") or "").lower().split()] for s in senses):
            score = 580
        # 6. Substring in lemma/ipa/variants
        elif clean_q in lemma_d:
            score = 500
        elif lemma_ipa and q_folded in fold_text(lemma_ipa):
            score = 480
        elif norm_h and q_folded in fold_text(norm_h):
            score = 460
        # 7. Substring in glosses
        elif any(clean_q in (s.get("definition_hi") or "") for s in senses):
            score = 400
        elif any(q_lower in (s.get("definition_en") or "").lower() for s in senses):
            score = 380
        # 8. Category
        elif any(q_lower == c.lower() for c in e.get("metadata", {}).get("categories", [])):
            score = 300
            
        if score > 0:
            scored.append((score, e))
            
    scored.sort(key=lambda x: -x[0])
    return scored

for q in ["water", "पानी", "pani", "पाणी", "bhed", "dora", "nawala"]:
    res = test_search(q)
    print(f"\nQuery '{q}' -> {len(res)} matches. Top 3:")
    for score, item in res[:3]:
        print(f"  [score={score}] {item['lemma_devanagari']} /{item.get('lemma_ipa')}/: {item['senses'][0].get('definition_en')}")
