import json
import re
from pathlib import Path
from gloss_to_hindi import get_hindi_gloss
from lsi_to_devanagari import roman_to_devanagari

# Load Chapter 6
with open('consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

# Load Chapter 2
with open('chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    ch2_text = f.read()

from prepare_all_lsi_entries import infer_category, infer_pos

extracted_items = []

# 1. Process Chapter 6
for r in comp_lex:
    gaddi_raw = r.get('gaddi', '').strip()
    gloss = r.get('gloss', '').strip()
    page = r.get('printed_page', 1089)
    if not gaddi_raw or gaddi_raw == '-':
        continue

    # Split sub-forms
    # Check for a) ... b) ...
    if 'a)' in gaddi_raw and 'b)' in gaddi_raw:
        parts = re.split(r'[ab]\)\s*', gaddi_raw)
        forms = [p.strip().rstrip(',') for p in parts if p.strip()]
    elif ',' in gaddi_raw:
        forms = [p.strip() for p in gaddi_raw.split(',') if p.strip()]
    elif '/' in gaddi_raw and not gaddi_raw.startswith('/'):
        forms = [p.strip() for p in gaddi_raw.split('/') if p.strip()]
    else:
        forms = [gaddi_raw]

    for f in forms:
        f_clean = f.strip().strip('-').strip()
        if not f_clean:
            continue
        extracted_items.append({
            'source_section': 'chapter_6_comparative_lexicon',
            'printed_page': f"p. {page}",
            'english_gloss': gloss,
            'source_form': f_clean,
            'is_multiword': ' ' in f_clean,
        })

print(f"Extracted from Chapter 6: {len(extracted_items)} raw forms")

# 2. Process Chapter 2 structured items
p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
p2 = re.compile(r'([a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+){0,5})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

seen_ch2 = set()

# Process p1 (/form/ 'gloss')
for m in p1.finditer(ch2_text):
    w = m.group(1).strip().strip('/')
    g = m.group(2).strip()
    if len(w) < 2 or len(g) < 2:
        continue
    if any(k in g.lower() for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table', 'building blocks']):
        continue
    key = (w.lower(), g.lower())
    if key not in seen_ch2:
        seen_ch2.add(key)
        extracted_items.append({
            'source_section': 'chapter_2_monograph',
            'printed_page': 'pp. 58-119',
            'english_gloss': g,
            'source_form': w,
            'is_multiword': ' ' in w,
        })

# Process p2 (form 'gloss')
for m in p2.finditer(ch2_text):
    w = m.group(1).strip().strip('/')
    g = m.group(2).strip()
    w_low = w.lower()
    if any(w_low.startswith(ex) for ex in ['the word', 'called', 'means', 'table', 'chapter', 'figure']):
        continue
    if w_low in ('means', 'called', 'that', 'with', 'which', 'and', 'also', 'the', 'is', 'for', 'this', 'in', 'it', 'there', 'who', 'how', 'when', 'where', 'some', 'they', 'you', 'she', 'him', 'her', 'we', 'i'):
        continue
    if len(w) < 2 or len(g) < 2:
        continue
    if any(k in g.lower() for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table', 'building blocks']):
        continue
    key = (w.lower(), g.lower())
    if key not in seen_ch2:
        seen_ch2.add(key)
        extracted_items.append({
            'source_section': 'chapter_2_monograph',
            'printed_page': 'pp. 58-119',
            'english_gloss': g,
            'source_form': w,
            'is_multiword': ' ' in w,
        })

print(f"Total raw extracted items (Ch6 + Ch2): {len(extracted_items)}")

