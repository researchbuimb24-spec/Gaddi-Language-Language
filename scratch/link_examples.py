import json
import re
from pathlib import Path

data_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
res_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources\dictionary_unified.json")
ex_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\gaddi_examples.json")

with open(data_path, "r", encoding="utf-8") as f:
    entries = json.load(f)

with open(ex_path, "r", encoding="utf-8") as f:
    examples = json.load(f)

print(f"Indexing {len(examples)} examples across {len(entries)} entries...")

total_links = 0
entries_with_links = 0

for entry in entries:
    meta = entry.setdefault("metadata", {})
    existing_ex = set(meta.get("example_ids", []))
    
    # Target tokens
    lemma_d = entry.get("lemma_devanagari", "").strip()
    lemma_ipa = (entry.get("lemma_ipa") or "").strip().lower()
    norm_h = (entry.get("normalized_headword") or "").strip().lower()
    
    # English keywords from senses
    en_keywords = set()
    for s in entry.get("senses", []):
        en_def = s.get("definition_en", "").lower()
        for tok in en_def.split():
            tok = tok.strip(",.()[]{}:;\"' /")
            if len(tok) > 3 and tok not in ("with", "from", "that", "this", "also", "have", "been", "used", "into"):
                en_keywords.add(tok)
                
    # Search each example
    for ex in examples:
        ex_id = ex.get("example_id") or ex.get("id")
        if not ex_id or ex_id in existing_ex:
            continue
            
        raw = ex.get("raw_text", "").lower()
        trans = (ex.get("gaddi_transcription") or "").lower()
        trans_en = (ex.get("english_translation") or "").lower()
        gloss = (ex.get("morpheme_gloss") or "").lower()
        
        matched = False
        # Match Devanagari
        if lemma_d and lemma_d in raw:
            matched = True
        # Match IPA
        elif lemma_ipa and len(lemma_ipa) >= 3 and (lemma_ipa in trans or lemma_ipa in raw):
            matched = True
        # Match primary English keyword if exact standalone word in English translation
        elif en_keywords:
            ex_words = set(re.findall(r"\b[a-z]{3,}\b", trans_en))
            if en_keywords & ex_words:
                matched = True
                
        if matched:
            existing_ex.add(ex_id)
            total_links += 1

    meta["example_ids"] = sorted(list(existing_ex))
    if meta["example_ids"]:
        entries_with_links += 1

print(f"Total entries now linked to examples: {entries_with_links} / {len(entries)}")
print(f"Total example links: {total_links}")

# Verify पाणी
pani = next(e for e in entries if e["lemma_devanagari"] == "पाणी")
print(f"पाणी linked examples: {pani['metadata']['example_ids']}")

# Save back
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

with open(res_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print("Saved updated dictionary_unified.json to data/ and src/gaddi/resources/")
