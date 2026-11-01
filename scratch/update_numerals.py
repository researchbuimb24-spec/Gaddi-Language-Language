import json

path_data = 'data/gaddi_numerals.json'
path_res = 'src/gaddi/resources/gaddi_numerals.json'

with open(path_data, 'r', encoding='utf-8') as f:
    num_data = json.load(f)

# 1. Update metadata
num_data['metadata']['third_party_attribution'] = {
    'collector': 'Kumari Mamta',
    'role': 'Doctoral research scholar, Centre for Linguistics, Jawaharlal Nehru University (JNU)',
    'source_note': "Appendix III footnote 1 (p. 125) states: 'The data in this appendix was collected by Kumari Mamta during her doctoral research at the Centre for Linguistics, Jawaharlal Nehru University, and shared with the authors for inclusion in this grammar.'",
    'applies_to': 'Appendix III (Tables C.1, C.2, C.3, C.4; pp. 125-128)'
}

# 2. Add unlexicalized_table_cells
num_data['unlexicalized_table_cells'] = [
    {
        'table_id': 'Table C.1',
        'printed_page': 127,
        'pdf_page': 144,
        'english_gloss': 'Million',
        'printed_cell': '–',
        'status': 'unlexicalized_dash_cell',
        'notes': 'No indigenous lexical numeral form provided in Table C.1 for Million; printed as an en/em dash cell indicating absence of a distinct native numeral atom in this base-10 system.'
    }
]

# 3. Update fractionals with printed_reading and resolved_reading
for frac in num_data['fractionals']:
    if frac['fraction'] == '1/10':
        frac['printed_reading'] = 'əkʰ bəʈɑ solɑ'
        frac['resolved_reading'] = 'əkʰ bəʈɑ dəs'
        frac['notes'] = "Printed as 'əkʰ bəʈɑ solɑ' in Table C.3 due to typographical inversion with sixteenth (1/16); resolved reading is 'əkʰ bəʈɑ dəs' based on numeral atom dəs (10)."
    elif frac['fraction'] == '1/16':
        frac['printed_reading'] = 'əkʰ bəʈɑ dəs'
        frac['resolved_reading'] = 'əkʰ bəʈɑ solɑ'
        frac['notes'] = "Printed as 'əkʰ bəʈɑ dəs' in Table C.3 due to typographical inversion with tenth (1/10); resolved reading is 'əkʰ bəʈɑ solɑ' based on numeral atom solɑ (16)."
    else:
        frac['printed_reading'] = frac['gaddi_ipa']
        frac['resolved_reading'] = frac['gaddi_ipa']

# 4. Clarify ordinals: printed_form vs feminine derivation
for ord_item in num_data['ordinals']:
    ord_item['printed_form'] = ord_item['masculine']
    ord_item['derivation_note'] = 'Table C.2 prints citation masculine forms. Feminine forms for ranks 1-5 documented in Section 3.8 Table 3.22 (p. 66); ranks 6-22 derived via regular -ɑ -> -i gender inflection.'

# 5. Ensure category: 'distributive' on all distributives
for dist in num_data['distributives']:
    dist['category'] = 'distributive'
    dist['table_id'] = 'Table C.4'
    dist['printed_page'] = 128
    dist['pdf_page'] = 145

with open(path_data, 'w', encoding='utf-8') as f:
    json.dump(num_data, f, ensure_ascii=False, indent=2)

with open(path_res, 'w', encoding='utf-8') as f:
    json.dump(num_data, f, ensure_ascii=False, indent=2)

print('Numerals dataset updated successfully.')
