import json
import re
from gloss_to_hindi import get_hindi_gloss
from lsi_to_devanagari import roman_to_devanagari
from prepare_all_lsi_entries import infer_category, infer_pos

# Load raw items
with open('consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

with open('chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    ch2_text = f.read()

items = []

# Process Ch6
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
            items.append({
                'source': f'census_2023_lsi',
                'page': f'p. {page}',
                'gloss_en': gloss,
                'form_raw': f_clean,
            })

# Process Ch2
p1 = re.compile(r'/([^/\n\r]+)/\s*[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')
p2 = re.compile(r'([a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+(?:[\s\-][a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-~]+){0,5})\s+[‘\'"“]([^’\'"”\n\r]+)[’\'"”]')

seen = set()
for m in p1.finditer(ch2_text):
    w = m.group(1).strip().strip('/')
    gl = m.group(2).strip()
    if len(w) < 2 or len(gl) < 2:
        continue
    if any(k in gl.lower() for k in ['phoneme', 'vowel', 'consonant', 'chapter', 'table', 'building blocks']):
        continue
    k = (w.lower(), gl.lower())
    if k not in seen:
        seen.add(k)
        items.append({
            'source': 'census_2023_lsi',
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
    if k not in seen:
        seen.add(k)
        items.append({
            'source': 'census_2023_lsi',
            'page': 'pp. 58-119',
            'gloss_en': gl,
            'form_raw': w,
        })

print(f"Total candidate items: {len(items)}")

# Test normalization and transliteration
processed = []
for it in items:
    w = it['form_raw']
    gl = it['gloss_en']
    deva = roman_to_devanagari(w)
    hi = get_hindi_gloss(gl)
    cat = infer_category(gl)
    pos = infer_pos(gl, w)
    processed.append({
        'deva': deva,
        'raw': w,
        'gl_en': gl,
        'gl_hi': hi,
        'cat': cat,
        'pos': pos,
        'page': it['page'],
    })

print(f"Successfully processed {len(processed)} items.")
print("Sample processed items:")
for p in processed[450:475]:
    print(f"  {p['deva']:18s} | {p['raw']:20s} | {p['pos']:8s} | {p['gl_en']:25s} -> {p['gl_hi']}")

