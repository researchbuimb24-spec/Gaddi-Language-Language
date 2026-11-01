import json
import re
from pathlib import Path
from gloss_to_hindi import get_hindi_gloss
from lsi_to_devanagari import roman_to_devanagari
from prepare_all_lsi_entries import infer_category, infer_pos

# 1. Load existing database
data_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
with open(data_path, "r", encoding="utf-8") as f:
    existing_entries = json.load(f)

print(f"Starting unified entries count: {len(existing_entries)}")
initial_headwords = {e["lemma_devanagari"].strip() for e in existing_entries if e.get("lemma_devanagari")}
initial_records = sum(len(e["attestations"]) for e in existing_entries)
print(f"Starting unique headwords: {len(initial_headwords)}")
print(f"Starting total records: {initial_records}")

# Build multi-level lookup
entry_lookup = {}
raw_lookup = {}
for idx, e in enumerate(existing_entries):
    key = (e.get("lemma_devanagari", "").strip(), e.get("variety_id", "").strip(), e.get("part_of_speech", "").strip())
    if key not in entry_lookup:
        entry_lookup[key] = idx
    # Raw lookup
    raw_key = (e.get("original_transcription", "").strip().lower(), e.get("variety_id", "").strip())
    if raw_key not in raw_lookup and raw_key[0]:
        raw_lookup[raw_key] = idx

# 2. Collect candidate items from LSI HP (Chapter 6 + Chapter 2)
with open('consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

with open('chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    ch2_text = f.read()

candidates = []

# Ch 6
for r in comp_lex:
    g = r.get('gaddi', '').strip()
    gloss = r.get('gloss', '').strip()
    page = r.get('printed_page', 1089)
    if not g or g == '-':
        continue
    if 'a)' in g and 'b)' in g:
        parts = re.split(r'[ab]\)\s*', g)
        forms = [p.strip().rstrip(',') for p in parts if p.strip()]
    elif ',' in g:
        forms = [p.strip() for p in g.split(',') if p.strip()]
    elif '/' in g and not g.startswith('/'):
        forms = [p.strip() for p in g.split('/') if p.strip()]
    else:
        forms = [g]

    for f in forms:
        f_clean = f.strip().strip('-').strip()
        if f_clean:
            candidates.append({
                'source_id': 'census_2023_lsi',
                'page': f'p. {page}',
                'gloss_en': gloss,
                'form_raw': f_clean,
            })

# Ch 2
p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
p2 = re.compile(r'([a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+){0,5})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

seen_c2 = set()
for m in p1.finditer(ch2_text):
    w = m.group(1).strip().strip('/')
    gl = m.group(2).strip()
    if len(w) < 2 or len(gl) < 2:
        continue
    if any(k in gl.lower() for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table', 'building blocks']):
        continue
    k = (w.lower(), gl.lower())
    if k not in seen_c2:
        seen_c2.add(k)
        candidates.append({
            'source_id': 'census_2023_lsi',
            'page': 'pp. 58-119',
            'gloss_en': gl,
            'form_raw': w,
        })

for m in p2.finditer(ch2_text):
    w = m.group(1).strip().strip('/')
    gl = m.group(2).strip()
    w_low = w.lower()
    if any(w_low.startswith(ex) for ex in ['the word', 'called', 'means', 'table', 'chapter', 'figure']):
        continue
    if w_low in ('means', 'called', 'that', 'with', 'which', 'and', 'also', 'the', 'is', 'for', 'this', 'in', 'it', 'there', 'who', 'how', 'when', 'where', 'some', 'they', 'you', 'she', 'him', 'her', 'we', 'i'):
        continue
    if len(w) < 2 or len(gl) < 2:
        continue
    if any(k in gl.lower() for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table', 'building blocks']):
        continue
    k = (w.lower(), gl.lower())
    if k not in seen_c2:
        seen_c2.add(k)
        candidates.append({
            'source_id': 'census_2023_lsi',
            'page': 'pp. 58-119',
            'gloss_en': gl,
            'form_raw': w,
        })

print(f"Total candidate forms extracted: {len(candidates)}")

# 3. Execute Merge & Expansion
merged_existing_count = 0
new_entries = []
seen_new_keys = set()
new_multiword_count = 0

for item in candidates:
    w_raw = item['form_raw']
    gl_en = item['gloss_en']
    deva = roman_to_devanagari(w_raw).strip()
    if not deva or len(deva) < 2:
        continue

    gl_hi = get_hindi_gloss(gl_en)
    cat = infer_category(gl_en)
    pos = infer_pos(gl_en, w_raw)
    is_multi = (' ' in deva or ' ' in w_raw or pos == 'phrase')

    key = (deva, "hp_chamba_bharmaur", pos)
    raw_key = (w_raw.lower().strip(), "hp_chamba_bharmaur")

    attestation = {
        "source_id": "census_2023_lsi",
        "page_or_section": item['page'],
        "verified": True,
        "transcription_raw": w_raw
    }

    # Case A: Matches existing entry in dictionary
    target_idx = None
    if key in entry_lookup:
        target_idx = entry_lookup[key]
    elif raw_key in raw_lookup:
        target_idx = raw_lookup[raw_key]

    if target_idx is not None:
        target_entry = existing_entries[target_idx]
        # Normalize headword if existing had raw Latin/diacritics
        if re.search(r'[a-zA-ZţŢŗřḍṭṇṣśñŋːˑúíóéáàèìòù]', target_entry.get("lemma_devanagari", "")):
            target_entry["lemma_devanagari"] = deva

        # Check if already has census_2023_lsi attestation
        has_src = any(a.get("source_id") == "census_2023_lsi" for a in target_entry.get("attestations", []))
        if not has_src:
            target_entry["attestations"].append(attestation)
            merged_existing_count += 1
        # Enrich senses if missing Hindi
        for s in target_entry.get("senses", []):
            if not s.get("definition_hi"):
                s["definition_hi"] = gl_hi
        # Add variant
        variants = target_entry.get("metadata", {}).get("variants", [])
        if w_raw not in variants:
            variants.append(w_raw)
        # Add category
        cats = target_entry.get("metadata", {}).get("categories", [])
        if cat not in cats:
            cats.append(cat)
    # Case B: New entry
    else:
        if key in seen_new_keys:
            idx = next(i for i, e in enumerate(new_entries) if (e["lemma_devanagari"], e["variety_id"], e["part_of_speech"]) == key)
            target_entry = new_entries[idx]
            variants = target_entry["metadata"]["variants"]
            if w_raw not in variants:
                variants.append(w_raw)
            if cat not in target_entry["metadata"]["categories"]:
                target_entry["metadata"]["categories"].append(cat)
        else:
            seen_new_keys.add(key)
            if is_multi:
                new_multiword_count += 1
            new_id = f"gaddi-uni-{len(existing_entries) + len(new_entries) + 1:05d}"
            entry = {
                "id": new_id,
                "lemma_devanagari": deva,
                "variety_id": "hp_chamba_bharmaur",
                "senses": [
                    {
                        "sense_index": 1,
                        "definition_en": gl_en,
                        "definition_hi": gl_hi,
                        "definition_ur": None,
                        "semantic_field": cat,
                        "examples": []
                    }
                ],
                "attestations": [attestation],
                "lemma_ipa": w_raw,
                "lemma_perso_arabic": None,
                "lemma_takri": None,
                "original_transcription": w_raw,
                "normalized_headword": deva,
                "part_of_speech": pos,
                "gender": None,
                "evidence_status": "comparative_only",
                "comparative_notes": None,
                "editorial_notes": f"Extracted from 2023 Linguistic Survey of India (LSI): Himachal Pradesh (ORGI, New Delhi). Bharmauri/Gaddi dialect of Chamba.",
                "metadata": {
                    "categories": [cat],
                    "variants": [w_raw],
                    "phonemic_variants": [w_raw],
                    "synonyms": [],
                    "etymology": "",
                    "tags": ["lsi_2023", "bharmauri"],
                    "example_ids": [],
                    "is_multiword": is_multi
                }
            }
            new_entries.append(entry)

print("\n--- REFINED SIMULATION RESULTS ---")
print(f"Existing entries enriched with census_2023_lsi attestation: {merged_existing_count}")
print(f"New unique entries created: {len(new_entries)}")
print(f"New multiword expressions: {new_multiword_count}")

all_entries = existing_entries + new_entries
final_headwords = {e["lemma_devanagari"].strip() for e in all_entries if e.get("lemma_devanagari")}
final_records = sum(len(e["attestations"]) for e in all_entries)

print(f"Final Total Unified Entries: {len(all_entries)}")
print(f"Final Unique Headwords: {len(final_headwords)} (new: {len(final_headwords) - len(initial_headwords)})")
print(f"Final Total Records/Attestations: {final_records} (new: {final_records - initial_records})")

from collections import Counter
vars = Counter(e['variety_id'] for e in all_entries)
print("\nFinal Variety Breakdown:")
for v, c in vars.items():
    print(f"  {v}: {c}")

cats_cnt = Counter()
for e in all_entries:
    for c in e.get("metadata", {}).get("categories", []):
        cats_cnt[c] += 1

print("\nCategory Distribution:")
for c, cnt in sorted(cats_cnt.items()):
    print(f"  {c:15s}: {cnt}")
