"""Complete Extraction and Dataset Builder for 'A Grammar of Gaddi' (Kumari et al. 2026).
Extracts all chapters, sections, tables, examples, appendices, references, and index terms.
Outputs 9 structured JSON datasets into data/ and src/gaddi/resources/.
"""

import json
import re
import sys
from pathlib import Path
import pypdf

PDF_PATH = Path(r"C:\Users\Hp\Documents\grammarOfGaddi.book.pdf")
DATA_DIR = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data")
RES_DIR = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources")

reader = pypdf.PdfReader(str(PDF_PATH))
print(f"Loaded PDF: {len(reader.pages)} pages")

def get_p(pno):
    """Return text of 1-indexed PDF page."""
    return reader.pages[pno - 1].extract_text()

# =========================================================================
# 1. gaddi_word_list.json (Appendix II: Basic Word List, Table B.1)
# =========================================================================
print("1. Building gaddi_word_list.json...")
app2_raw_lines = []
for pno in range(136, 142):
    t = get_p(pno)
    for line in t.splitlines():
        line = line.strip()
        if not line or "APP eNDI" in line or "A GRAMMAR" in line or "Table B.1" in line or "Serial No." in line or "List based on" in line or "Appendix II:" in line:
            continue
        app2_raw_lines.append((pno, line))

app2_combined = []
for pno, line in app2_raw_lines:
    if re.match(r"^\d+(\.\d+)?\b", line):
        app2_combined.append([pno, line])
    else:
        if app2_combined:
            app2_combined[-1][1] += " " + line

word_list_entries = []
for pno, text in app2_combined:
    m = re.match(r"^(\d+(\.\d+)?)\s*\[(.*?)\]\s*(.*)$", text)
    if not m:
        continue
    s_num, _, ipa_raw, gloss_raw = m.groups()
    clean_ipa = re.sub(r"\s+", "", ipa_raw)
    clean_gloss = re.sub(r"\s+", " ", gloss_raw).strip()
    
    if clean_gloss == "hear t":
        clean_gloss = "heart"
    
    base_num = int(s_num.split(".")[0])
    sub_num = int(s_num.split(".")[1]) if "." in s_num else None
    
    if sub_num is not None:
        entry_id = f"kumari-wlist-{base_num:03d}-{sub_num}"
    else:
        entry_id = f"kumari-wlist-{base_num:03d}"
    
    pos = "unspecified"
    if clean_gloss in ["all", "many (ma)", "many (fe)", "few", "some"]:
        pos = "quantifier"
    elif clean_gloss in ["and", "because", "if", "or"]:
        pos = "conjunction"
    elif clean_gloss in ["in", "near", "with", "there", "here"]:
        pos = "adposition_or_adverb"
    elif clean_gloss in ["I", "he/she", "thou", "they", "we", "what", "when", "where", "who", "this", "that"]:
        pos = "pronoun"
    elif " (verb)" in clean_gloss or clean_gloss in ["bite", "burn", "come", "count", "die", "dig", "drink", "eat", "fall", "fight", "float", "flow", "fly", "freeze", "give", "hear", "hit", "hold", "hunt", "kill", "know", "laugh", "lie", "live", "play", "pull", "push", "rain", "rub", "say", "scratch", "see", "sew", "sing", "sit", "sleep", "spit", "split", "squeeze", "stand", "suck", "swell", "swim", "think", "throw", "tie", "turn", "walk", "wash", "wipe", "cook", "dance", "shoot", "work"]:
        pos = "verb"
    elif clean_gloss in ["ashes", "back", "bark", "bark of a tree", "belly", "big vessel", "bird", "blood", "bone", "chest", "breast", "breath", "male child", "female child", "claw", "cloud", "day", "dog", "dust", "ear", "earth", "egg", "eye", "fat, grease", "father", "fear", "feather", "fish", "flower", "fog", "foot", "fruit", "grass", "guts", "hair", "hand", "head", "forehead", "heart", "horn", "husband", "ice", "knee", "leaf", "left side", "leg", "banana", "louse", "male", "meat (uncooked)", "meat (cooked)", "moon", "mother", "mountain", "mouth", "name", "neck", "night", "nose", "person", "pond", "river", "road", "root", "rope", "salt", "sand", "sea", "seed", "skin of animal", "skin", "sky", "smell (noun)", "smoke", "snake", "snow", "bangles", "star", "stick", "stone", "sun", "tail", "tongue", "tooth", "tree", "water", "wife", "wind", "wing", "woman", "woods", "worm", "year", "brother", "elder brother", "clothing", "male dancer", "female dancer", "sister", "spear", "bindi", "flour (kneaded)", "braid", "roti"]:
        pos = "noun"
    elif clean_gloss in ["bad", "big", "black", "cold", "dirty", "dry", "dull (colours)", "dull (lazy)", "far", "full", "good", "green", "heavy", "long", "narrow", "new (ma)", "new (fe)", "old", "other", "red", "correct", "right", "rotten", "round", "sharp", "short (young)", "short", "small", "smooth", "straight", "thick", "thin", "warm", "wet", "wet clothes", "white", "wide"]:
        pos = "adjective"
    elif clean_gloss in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "twenty", "hundred"]:
        pos = "numeral"

    word_list_entries.append({
        "entry_id": entry_id,
        "serial_number": s_num,
        "base_serial": base_num,
        "sub_serial": sub_num,
        "gaddi_ipa": clean_ipa,
        "gaddi_raw": f"[{clean_ipa}]",
        "english_gloss": clean_gloss,
        "part_of_speech": pos,
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "source_id": "kumari_2026",
        "source_citation": f"Kumari et al. (2026), Table B.1, p. {pno - 17}",
        "attribution": "List based on Abbi (2001, p. 244)",
        "printed_page": pno - 17,
        "pdf_page": pno,
        "table_id": "Table B.1",
        "extraction_method": "digital_pdf_with_visual_verification",
        "evidence_status": "comparative_only",
        "is_jk_verified": False,
        "license": "CC BY-NC 4.0 (Non-commercial research use only; third-party exclusions apply)"
    })

# =========================================================================
# 2. gaddi_numerals.json (Appendix III: Tables C.1-C.4 & Chapter 3.8)
# =========================================================================
print("2. Building gaddi_numerals.json...")
# (Using the complete verified list established earlier)
cardinals_data = [
    (1, "One", "əkʰ", "atom"), (2, "Two", "do", "atom"), (3, "Three", "trɛ", "atom"),
    (4, "Four", "tʃɑr", "atom"), (5, "Five", "pəndʒ", "atom"), (6, "Six", "tʃʰe", "atom"),
    (7, "Seven", "sət", "atom"), (8, "Eight", "əʈʰ", "atom"), (9, "Nine", "nɔ", "atom"),
    (10, "Ten", "dəs", "atom"), (11, "Eleven", "jɑrɑ̃", "derived"), (12, "Twelve", "bɑrɑ̃", "derived"),
    (13, "Thirteen", "terɑ̃", "derived"), (14, "Fourteen", "tʃodɑ̃", "derived"), (15, "Fifteen", "pəndrɑ̃", "derived"),
    (16, "Sixteen", "solɑ̃", "derived"), (17, "Seventeen", "sətɑrɑ̃", "derived"), (18, "Eighteen", "ʈʰɑrɑ̃", "derived"),
    (19, "Nineteen", "unni", "derived"), (20, "Twenty", "bi", "base_decade"),
    (21, "Twenty-one", "ikki", "derived"), (22, "Twenty-two", "bɑi", "derived"), (23, "Twenty-three", "trei", "derived"),
    (24, "Twenty-four", "tʃobbi", "derived"), (25, "Twenty-five", "pəndʒi", "derived"), (26, "Twenty-six", "tʃʰəbbi", "derived"),
    (27, "Twenty-seven", "sətɑi", "derived"), (28, "Twenty-eight", "ʈʰɑi", "derived"), (29, "Twenty-nine", "nəti", "derived_unit9"),
    (30, "Thirty", "tri", "base_decade"), (31, "Thirty-one", "kətti", "derived"), (32, "Thirty-two", "bətti", "derived"),
    (33, "Thirty-three", "tetti", "derived"), (34, "Thirty-four", "tʃotti", "derived"), (35, "Thirty-five", "pẽti", "derived"),
    (36, "Thirty-six", "tʃʰətti", "derived"), (37, "Thirty-seven", "sətətti", "derived"), (38, "Thirty-eight", "ʈʰətti", "derived"),
    (39, "Thirty-nine", "untɑli", "derived_unit9"), (40, "Forty", "tʃɑli", "base_decade"),
    (41, "Forty-one", "ektɑli", "derived"), (42, "Forty-two", "betɑli", "derived"), (43, "Forty-three", "tertɑli", "derived"),
    (44, "Forty-four", "tʃurtɑli", "derived"), (45, "Forty-five", "pɛ̃tɑli", "derived"), (46, "Forty-six", "tʃʰətɑli", "derived"),
    (47, "Forty-seven", "səntɑli", "derived"), (48, "Forty-eight", "əʈʰtɑli", "derived"), (49, "Forty-nine", "unundʒɑ", "derived_unit9"),
    (50, "Fifty", "pejɑ̃", "base_decade"), (51, "Fifty-one", "kundʒɑ", "derived"), (52, "Fifty-two", "bundʒɑ", "derived"),
    (53, "Fifty-three", "trundʒɑ", "derived"), (54, "Fifty-four", "tʃurundʒɑ", "derived"), (55, "Fifty-five", "pətʃundʒɑ", "derived"),
    (56, "Fifty-six", "tʃʰunɑ", "derived"), (57, "Fifty-seven", "sətunjɑ", "derived"), (58, "Fifty-eight", "ʈʰunjɑ", "derived"),
    (59, "Fifty-nine", "unɑʈʰ", "derived_unit9"), (60, "Sixty", "səʈʰ", "base_decade"),
    (61, "Sixty-one", "ekɑʈʰ", "derived"), (62, "Sixty-two", "bɑʈʰ", "derived"), (63, "Sixty-three", "treʈʰ", "derived"),
    (64, "Sixty-four", "tʃoʈʰ", "derived"), (65, "Sixty-five", "pɛ̃ʈʰ", "derived"), (66, "Sixty-six", "tʃʰijɑʈʰ", "derived"),
    (67, "Sixty-seven", "sətɑʈʰ", "derived"), (68, "Sixty-eight", "ʈʰɑʈʰ", "derived"), (69, "Sixty-nine", "unəttər", "derived_unit9"),
    (70, "Seventy", "səttər", "base_decade"), (71, "Seventy-one", "kəttər", "derived"), (72, "Seventy-two", "bəttər", "derived"),
    (73, "Seventy-three", "trettər", "derived"), (74, "Seventy-four", "tʃurəttər", "derived"), (75, "Seventy-five", "pətʃəttər", "derived"),
    (76, "Seventy-six", "tʃʰejəttər", "derived"), (77, "Seventy-seven", "sətəttər", "derived"), (78, "Seventy-eight", "ʈʰəttər", "derived"),
    (79, "Seventy-nine", "unɑsi", "derived_unit9"), (80, "Eighty", "əssi", "base_decade"),
    (81, "Eighty-one", "ekɑsi", "derived"), (82, "Eighty-two", "bejɑsi", "derived"), (83, "Eighty-three", "terɑsi", "derived"),
    (84, "Eighty-four", "tʃurɑsi", "derived"), (85, "Eighty-five", "pətʃɑsi", "derived"), (86, "Eighty-six", "tʃʰejɑsi", "derived"),
    (87, "Eighty-seven", "sətɑsi", "derived"), (88, "Eighty-eight", "ʈʰɑsi", "derived"), (89, "Eighty-nine", "nɑnʋe", "derived_unit9"),
    (90, "Ninety", "nəbbɛ", "base_decade"), (91, "Ninety-one", "kɑnʋe", "derived"), (92, "Ninety-two", "ʋənʋe", "derived"),
    (93, "Ninety-three", "terɑnʋe", "derived"), (94, "Ninety-four", "tʃurɑnʋe", "derived"), (95, "Ninety-five", "pətʃɑnʋe", "derived"),
    (96, "Ninety-six", "tʃʰijɑnʋe", "derived"), (97, "Ninety-seven", "sətɑnʋe", "derived"), (98, "Ninety-eight", "ʈʰɑnʋe", "derived"),
    (99, "Ninety-nine", "nəɽinʋe", "derived_unit9"),
    (100, "Hundred", "sɔ", "scale_base"), (1000, "Thousand", "jɑr", "scale_base"),
    (100000, "Lakh (100,000)", "ləkʰ", "scale_base"), (10000000, "Crore (10,000,000)", "kror", "scale_base"),
    (1000000000, "Billion (1,000,000,000)", "ərəb", "scale_base")
]

cardinals_list = []
for val, gloss, ipa, struct in cardinals_data:
    cardinals_list.append({
        "value": val,
        "gloss": gloss,
        "gaddi_ipa": ipa,
        "category": "cardinal",
        "morpheme_structure": struct,
        "table_id": "Table C.1",
        "printed_page": 125 if val <= 37 else (126 if val <= 87 else 127),
        "pdf_page": 142 if val <= 37 else (143 if val <= 87 else 144)
    })

ordinals_data = [
    (1, "First", "pɛlɑ", "pɛli"), (2, "Second", "duɑ", "doi"), (3, "Third", "trijɑ", "trɛ"),
    (4, "Fourth", "tʃotʰɑ", "tʃotʰi"), (5, "Fifth", "pəimɑ", "pəimi"), (6, "Sixth", "tʃʰemmɑ", "tʃʰemmi"),
    (7, "Seventh", "sətuʋɑ", "sətuʋi"), (8, "Eighth", "əʈʰʋɑ", "əʈʰʋi"), (9, "Ninth", "nomɑ", "nomi"),
    (10, "Tenth", "dəsmɑ", "dəsmi"), (11, "Eleventh", "jɑrmɑ", "jɑrmi"), (12, "Twelfth", "bɑrmɑ", "bɑrmi"),
    (13, "Thirteenth", "termɑ", "termi"), (14, "Fourteenth", "tʃodmɑ", "tʃodmi"), (15, "Fifteenth", "pəndrəmɑ", "pəndrəmi"),
    (16, "Sixteenth", "solmɑ", "solmi"), (17, "Seventeenth", "sətɑrmɑ", "sətɑrmi"), (18, "Eighteenth", "ʈʰɑrmɑ", "ʈʰɑrmi"),
    (19, "Nineteenth", "unnimɑ", "unnimi"), (20, "Twentieth", "bimɑ", "bimi"), (21, "Twenty-first", "ikkimɑ", "ikkimi"),
    (22, "Twenty-second", "bɑimɑ", "bɑimi")
]
ordinals_list = []
for rank, gloss, masc, fem in ordinals_data:
    ordinals_list.append({
        "rank": rank,
        "gloss": gloss,
        "masculine": masc,
        "feminine": fem,
        "category": "ordinal",
        "agreement_type": "suppletive" if rank in [2, 3] else "vowel_alternation_a_vs_i",
        "table_id": "Table C.2",
        "printed_page": 127,
        "pdf_page": 144
    })

fractionals_list = [
    {"fraction": "1/4", "gloss": "Quarter", "gaddi_ipa": "pɔ:ni", "category": "fractional", "derivation_type": "lexical_atom", "printed_page": 128, "pdf_page": 145},
    {"fraction": "1/2", "gloss": "Half", "gaddi_ipa": "ɑddə", "category": "fractional", "derivation_type": "lexical_atom", "printed_page": 128, "pdf_page": 145},
    {"fraction": "1/3", "gloss": "Third (one-third)", "gaddi_ipa": "ɑkiɑ̃ trijɑ", "category": "fractional", "derivation_type": "derived_compound", "printed_page": 128, "pdf_page": 145},
    {"fraction": "2/3", "gloss": "Two-thirds", "gaddi_ipa": "doijɑ̃ trijɑ", "category": "fractional", "derivation_type": "derived_compound", "printed_page": 128, "pdf_page": 145},
    {"fraction": "3/4", "gloss": "Three-quarters", "gaddi_ipa": "trijɑ coutʰɑ", "category": "fractional", "derivation_type": "derived_compound", "printed_page": 128, "pdf_page": 145},
    {"fraction": "1/10", "gloss": "Tenth (one-tenth)", "gaddi_ipa": "əkʰ bəʈɑ dəs", "category": "fractional", "derivation_type": "mathematical_division", "notes": "Printed as 'əkʰ bəʈɑ solɑ' in Table C.3 due to typographical inversion with sixteenth", "printed_page": 128, "pdf_page": 145},
    {"fraction": "1/16", "gloss": "Sixteenth (one-sixteenth)", "gaddi_ipa": "əkʰ bəʈɑ solɑ", "category": "fractional", "derivation_type": "mathematical_division", "notes": "Printed as 'əkʰ bəʈɑ dəs' in Table C.3 due to typographical inversion with tenth", "printed_page": 128, "pdf_page": 145}
]

distributives_list = [
    {"gloss": "One each", "gaddi_ipa": "ək ək", "reading_type": "participant_key", "structure": "total_reduplication", "printed_page": 128, "pdf_page": 145},
    {"gloss": "Three each", "gaddi_ipa": "trɛ trɛ", "reading_type": "participant_key", "structure": "total_reduplication", "printed_page": 128, "pdf_page": 145},
    {"gloss": "Five each", "gaddi_ipa": "pəndʒ pəndʒ", "reading_type": "participant_key", "structure": "total_reduplication", "printed_page": 128, "pdf_page": 145},
    {"gloss": "One by one", "gaddi_ipa": "ək ək kəri kəre", "reading_type": "temporal_key", "structure": "reduplicated_cardinal_plus_reduplicated_verb_kare", "printed_page": 128, "pdf_page": 145},
    {"gloss": "Two by two", "gaddi_ipa": "do do kəri kəre", "reading_type": "temporal_key", "structure": "reduplicated_cardinal_plus_reduplicated_verb_kare", "printed_page": 128, "pdf_page": 145}
]

gaddi_numerals_dataset = {
    "metadata": {
        "title": "Comprehensive Gaddi Numeral System",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Section 3.8 (pp. 61-68) & Appendix III (pp. 125-128)",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "base_system": "decimal (base 10)",
        "attribution": "Appendix III data collected by Kumari Mamta; Section 3.8 analysis by Preeti Kumari (2016, 2021)",
        "license": "CC BY-NC 4.0",
        "is_jk_verified": False,
        "evidence_status": "comparative_only"
    },
    "cardinals": cardinals_list,
    "ordinals": ordinals_list,
    "fractionals": fractionals_list,
    "distributives": distributives_list,
    "prefix_templates_1_to_9": [
        {"digit": 1, "template": "/kk/"}, {"digit": 2, "template": "/b/"}, {"digit": 3, "template": "/tr/"},
        {"digit": 4, "template": "/tʃ/"}, {"digit": 5, "template": "/pẽ/"}, {"digit": 6, "template": "/tʃʰ/"},
        {"digit": 7, "template": "/sət/"}, {"digit": 8, "template": "/ʈʰ/"}, {"digit": 9, "template": "/n/"}
    ],
    "decade_templates": [
        {"decade": 20, "stem": "bi", "gloss": "twenty"}, {"decade": 30, "stem": "tri", "gloss": "thirty"},
        {"decade": 40, "stem": "tʃɑli", "gloss": "forty"}, {"decade": 50, "stem": "pejɑ̃", "gloss": "fifty"},
        {"decade": 60, "stem": "səʈʰ", "gloss": "sixty"}, {"decade": 70, "stem": "səttər", "gloss": "seventy"},
        {"decade": 80, "stem": "əssi", "gloss": "eighty"}, {"decade": 90, "stem": "nəbbɛ", "gloss": "ninety"}
    ],
    "unit_9_preceding_stems": [
        {"number": 29, "gaddi_ipa": "nəti", "gloss": "twenty-nine", "derived_from": "tri (30)"},
        {"number": 39, "gaddi_ipa": "untɑli", "gloss": "thirty-nine", "derived_from": "tʃɑli (40)"},
        {"number": 49, "gaddi_ipa": "unundʒɑ", "gloss": "forty-nine", "derived_from": "pejɑ̃ (50)"},
        {"number": 59, "gaddi_ipa": "unɑʈʰ", "gloss": "fifty-nine", "derived_from": "səʈʰ (60)"},
        {"number": 69, "gaddi_ipa": "unəttər", "gloss": "sixty-nine", "derived_from": "səttər (70)"},
        {"number": 79, "gaddi_ipa": "unɑsi", "gloss": "seventy-nine", "derived_from": "əssi (80)"},
        {"number": 89, "gaddi_ipa": "nɑnʋe", "gloss": "eighty-nine", "derived_from": "nəbbɛ (90)"},
        {"number": 99, "gaddi_ipa": "nəɽinʋe", "gloss": "ninety-nine", "derived_from": "irregular"}
    ]
}

# =========================================================================
# 3. gaddi_phonology.json (Chapter 2 & Appendix I)
# =========================================================================
print("3. Building gaddi_phonology.json...")
gaddi_phonology_dataset = {
    "metadata": {
        "title": "Phonetics and Phonology of Kangra Gaddi",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Chapter 2 (pp. 11-37) & Appendix I (pp. 117-118)",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "license": "CC BY-NC 4.0",
        "is_jk_verified": False,
        "evidence_status": "comparative_only"
    },
    "vowel_system": {
        "total_oral_monophthongs": 8,
        "oral_monophthongs": [
            {"ipa": "i", "height": "close", "frontness": "front", "rounding": "unrounded", "features": {"high": True, "mid": False, "low": False, "front": True, "back": False, "round": False}},
            {"ipa": "e", "height": "close-mid", "frontness": "front", "rounding": "unrounded", "features": {"high": True, "mid": True, "low": False, "front": True, "back": False, "round": False}},
            {"ipa": "ɛ", "height": "open-mid", "frontness": "front", "rounding": "unrounded", "features": {"high": False, "mid": True, "low": True, "front": True, "back": False, "round": False}},
            {"ipa": "ə", "height": "mid", "frontness": "central", "rounding": "unrounded", "features": {"high": False, "mid": True, "low": False, "front": False, "back": False, "round": False}},
            {"ipa": "ɑ", "height": "open", "frontness": "central_back", "rounding": "unrounded", "features": {"high": False, "mid": False, "low": True, "front": False, "back": True, "round": False}},
            {"ipa": "u", "height": "close", "frontness": "back", "rounding": "rounded", "features": {"high": True, "mid": False, "low": False, "front": False, "back": True, "round": True}},
            {"ipa": "o", "height": "close-mid", "frontness": "back", "rounding": "rounded", "features": {"high": True, "mid": True, "low": False, "front": False, "back": True, "round": True}},
            {"ipa": "ɔ", "height": "open-mid", "frontness": "back", "rounding": "rounded", "features": {"high": False, "mid": True, "low": True, "front": False, "back": True, "round": True}}
        ],
        "nasal_vowels_chapter2": [
            {"ipa": "ũ", "nature": "inherent_lexical", "examples": [{"word": "kjũ", "gloss": "fava beans"}, {"word": "ijũ", "gloss": "snow"}, {"word": "dʰũː", "gloss": "smoke"}]},
            {"ipa": "ɑ̃", "nature": "inherent_lexical", "examples": [{"word": "bɑ̃", "gloss": "pond"}, {"word": "ɡɾɑ̃ː", "gloss": "village"}]},
            {"ipa": "ɛ̃", "nature": "inherent_lexical", "examples": [{"word": "pɛ͂tɑli", "gloss": "forty-five"}, {"word": "cɛ͂ː", "gloss": "root"}]}
        ],
        "diphthongs": {
            "oral": [
                {"ipa": "oi", "type": "raising", "example": "bʰənoi", "gloss": "brother-in-law"},
                {"ipa": "ei", "type": "raising", "example": "peinnɑ", "gloss": "sharp"},
                {"ipa": "ɑi", "type": "raising", "example": "bʰɑi", "gloss": "brother"},
                {"ipa": "əu", "type": "raising", "example": "tʃəuɾə", "gloss": "four"},
                {"ipa": "eo", "type": "raising", "example": "keolɑ", "gloss": "coal"}
            ],
            "nasal": [
                {"ipa": "əũ", "type": "raising", "example": "bəũkʰɾi", "gloss": "broom"},
                {"ipa": "ɛ̃i", "type": "raising", "example": "d̪ɛ̃i", "gloss": "curd"},
                {"ipa": "iũ", "type": "raising", "example": "piũɭɑ", "gloss": "yellow"},
                {"ipa": "aũ", "type": "raising", "example": "aũ", "gloss": "I"}
            ]
        },
        "length_distinction": {
            "status": "phonetically_long_not_phonemically_contrastive",
            "pairs_table_2_3": [
                {"vowel": "i", "short": "sinnɑ (wet)", "long": "siːɳɑ (to sew)"},
                {"vowel": "e", "short": "sere (their)", "long": "heːɭə (slate on roof)"},
                {"vowel": "ɛ", "short": "bɛɡə (morning)", "long": "bɛːɳə (sister)"},
                {"vowel": "u", "short": "pʰulə (flower)", "long": "luːɳə (salt)"},
                {"vowel": "o", "short": "boli (language)", "long": "koːlə (big bowl)"},
                {"vowel": "ɔ", "short": "ʈɔɳɑ (deaf)", "long": "t̪ɔːlə (hammer)"},
                {"vowel": "ɑ", "short": "kɑɭɑ (black)", "long": "bɑːli (earring)"},
                {"vowel": "ũ", "short": "kjũ (fava beans)", "long": "dʰũː (smoke)"},
                {"vowel": "ɑ̃", "short": "bɑ̃ (pond)", "long": "ɡɾɑ̃ː (village)"},
                {"vowel": "ɛ̃", "short": "pɛ͂t̪ɑli (forty-five)", "long": "cɛ͂ː (root)"}
            ]
        }
    },
    "consonant_system": {
        "total_consonants": 31,
        "consonants": [
            {"ipa": "p", "manner": "plosive", "place": "bilabial", "voiced": False, "aspirated": False},
            {"ipa": "pʰ", "manner": "plosive", "place": "bilabial", "voiced": False, "aspirated": True},
            {"ipa": "b", "manner": "plosive", "place": "bilabial", "voiced": True, "aspirated": False},
            {"ipa": "bʰ", "manner": "plosive", "place": "bilabial", "voiced": True, "aspirated": True},
            {"ipa": "t̪", "manner": "plosive", "place": "dental", "voiced": False, "aspirated": False},
            {"ipa": "t̪ʰ", "manner": "plosive", "place": "dental", "voiced": False, "aspirated": True},
            {"ipa": "d̪", "manner": "plosive", "place": "dental", "voiced": True, "aspirated": False},
            {"ipa": "d̪ʰ", "manner": "plosive", "place": "dental", "voiced": True, "aspirated": True},
            {"ipa": "ʈ", "manner": "plosive", "place": "retroflex", "voiced": False, "aspirated": False},
            {"ipa": "ʈʰ", "manner": "plosive", "place": "retroflex", "voiced": False, "aspirated": True},
            {"ipa": "ɖ", "manner": "plosive", "place": "retroflex", "voiced": True, "aspirated": False},
            {"ipa": "ɖʰ", "manner": "plosive", "place": "retroflex", "voiced": True, "aspirated": True},
            {"ipa": "k", "manner": "plosive", "place": "velar", "voiced": False, "aspirated": False},
            {"ipa": "kʰ", "manner": "plosive", "place": "velar", "voiced": False, "aspirated": True},
            {"ipa": "ɡ", "manner": "plosive", "place": "velar", "voiced": True, "aspirated": False},
            {"ipa": "ɡʰ", "manner": "plosive", "place": "velar", "voiced": True, "aspirated": True},
            {"ipa": "tʃ", "manner": "affricate", "place": "palato-alveolar", "voiced": False, "aspirated": False},
            {"ipa": "tʃʰ", "manner": "affricate", "place": "palato-alveolar", "voiced": False, "aspirated": True},
            {"ipa": "dʒ", "manner": "affricate", "place": "palato-alveolar", "voiced": True, "aspirated": False},
            {"ipa": "dʒʰ", "manner": "affricate", "place": "palato-alveolar", "voiced": True, "aspirated": True},
            {"ipa": "s", "manner": "fricative", "place": "alveolar", "voiced": False, "aspirated": False},
            {"ipa": "h", "manner": "fricative", "place": "glottal", "voiced": False, "aspirated": False},
            {"ipa": "m", "manner": "nasal", "place": "bilabial", "voiced": True, "aspirated": False},
            {"ipa": "n", "manner": "nasal", "place": "alveolar", "voiced": True, "aspirated": False},
            {"ipa": "ɳ", "manner": "nasal", "place": "retroflex", "voiced": True, "aspirated": False},
            {"ipa": "ɾ", "manner": "flap", "place": "alveolar", "voiced": True, "aspirated": False},
            {"ipa": "ɽ", "manner": "flap", "place": "retroflex", "voiced": True, "aspirated": False},
            {"ipa": "l", "manner": "lateral_approximant", "place": "alveolar", "voiced": True, "aspirated": False},
            {"ipa": "ɭ", "manner": "lateral_approximant", "place": "retroflex", "voiced": True, "aspirated": False},
            {"ipa": "ʋ", "manner": "approximant", "place": "labiodental", "voiced": True, "aspirated": False},
            {"ipa": "j", "manner": "approximant", "place": "palatal", "voiced": True, "aspirated": False}
        ],
        "allophones": [
            {"ipa": "ŋ", "phoneme": "n", "context": "before velar plosives", "examples": ["lɔ͂ŋɡ (nose ring)", "pʰə͂ŋɡ (feather)", "kɑ̃ŋɡi (comb)", "si͂ŋkʰə (meat)"]}
        ],
        "retroflex_series": {
            "total": 7,
            "inventory": ["ʈ", "ɖ", "ʈʰ", "ɖʰ", "ɳ", "ɽ", "ɭ"],
            "features": "apicality, posteriority, sublingual cavity, retraction (Hamann 2003)",
            "initial_restriction": "/ɽ/, /ɭ/, /ɳ/ never occur word-initially"
        }
    },
    "phonotactics_and_syllable": {
        "canonical_syllable": "(C)(C)(V)(C)",
        "sonority_hierarchy": "Plosives < Fricatives < Nasals < Laterals < Flaps < Vowels",
        "syllable_principles": [
            "Onset Maximisation Principle (Kahn 1980): Intervocalic single consonants assigned to following onset",
            "Geminates split across coda and onset: sut.tu.rɑ, tʃiʈ.ʈʰi, bər.kkʰɑ",
            "Homorganic oral plosive clusters (unaspirated + aspirated) syllabify as geminates"
        ],
        "word_initial_clusters": ["/br/", "/dr/", "/ɡr/", "/kr/", "/ɡl/", "/pj/", "/sʋ/"],
        "word_final_codas": "Rare due to excrescent schwa /ə/ release; only /ɾ/, /m/, /s/ occur word-finally without schwa"
    },
    "phonological_processes": [
        {"name": "Regressive Nasal Spread", "rule": "V -> Ṽ / __ [+nasal]", "direction": "right to left", "examples": ["lɔŋɡ -> lɔ̃ŋɡ", "tʃɛnʈe -> tʃɛ̃nʈe", "kɑŋɡi -> kɑ̃ŋɡi", "mɑndʒ -> mɑ̃ndʒ"]},
        {"name": "Prenasalisation", "environment": "word-initially before voiced plosives", "examples": ["[ᵐbinnɑ] (mattress)", "[ᵐbəsəndə] (summer)", "[ᵐbɑːldə] (bull)", "[ᵐbəɾkʰɑ] (rain)", "[ⁿɖəkka] (push)", "[ⁿda:rə] (door)", "[ᵑgəttə] (big flower)", "[ᵑgirka] (heavy)"]},
        {"name": "Gemination", "types": "derived (across morpheme boundary with ergative -ɛ on sonorants) vs underived", "examples": ["ɾɑm + ɛ -> ɾɑmmɛ", "sjɑm + ɛ -> sjɑmmɛ", "nikkɑ (child)", "buʈʈɑ (tree)", "dʒɑnnu (knee)"]},
        {"name": "Loanword Schwa Epenthesis", "purpose": "break illegal clusters in borrowings", "examples": ["/skuːl/ -> [səkul]", "/pʌrs/ -> [pərəs]", "/film/ -> [pʰiləm]", "/bʌlb/ -> [bələb]"]},
        {"name": "Glide Epenthesis", "rule": "Ø -> [j] / V1_V2", "purpose": "hiatus resolution across vowel collocation", "examples": ["[ijũ] (snow)", "[tʃəlijɑ] (come)", "[sejɑu] (apple)", "post-lexical before mood marker: dʒərurijɑ, indi(j)ɑ"]},
        {"name": "Lyman's Law / OCP Retroflex Dissimilation", "rule": "Prohibits two adjacent aspirated retroflex consonants", "examples": ["[piʈʈʰi] (back)", "[piʈʈʰɑ] (dough)", "[miʈʈʰe] (sweet)"]}
    ],
    "appendix_i_discrepancies": {
        "vowels": "Appendix I Table A.2 lists 5 nasal vowels (ĩ, ũ, ẽ, ə̃, ɑ̃), whereas Chapter 2 Section 2.2.2 establishes exactly 3 lexical nasal vowels (/ũ/, /ɑ̃/, /ɛ̃/).",
        "consonants": "Appendix I Table A.3 includes fricatives /f/ and /ʃ/, velar nasal /ŋ/ as a full phoneme, and trill /r/ alongside flap /ɽ/, whereas Chapter 2 Table 2.4 restricts fricatives to /s, h/, treats [ŋ] as an allophone of /n/ before velars, and lists only flap /ɾ/."
    }
}

# =========================================================================
# 4. gaddi_cultural_sociolinguistic_notes.json (Chapter 1)
# =========================================================================
print("4. Building gaddi_cultural_sociolinguistic_notes.json...")
gaddi_cultural_dataset = {
    "metadata": {
        "title": "Gaddi Ethnography, Sociolinguistics, and Vitality Profile",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Chapter 1 (pp. 1-10)",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "license": "CC BY-NC 4.0",
        "is_jk_verified": False,
        "evidence_status": "comparative_only"
    },
    "community_profile": {
        "name": "Gaddi",
        "endonym_pronunciation_ipa": "/ɡəd̪d̪i/",
        "mythical_homeland": "Bharmaur region of Chamba in Himachal Pradesh, on the river basins of the Ravi and Budhil (Kapila 2008)",
        "pastoral_identity": "Traditional migratory pastoralists owning sheep and goats. Self-conception as 'ghomtus' (people born with moving feet)",
        "herding_cycle": "Year-round seasonal transhumance across Himalayan grazing corridors; shearing, slaughtering, penning",
        "herding_roles": "Large flock owners (>200) hold community leadership; 'puhal' are herding assistants regarded as lower socio-economic status",
        "women_roles": "Farming, animal husbandry, woollen blanket and clothes weaving, domestic water and fuel collection",
        "social_structure": "Patriarchal lineage; preference for male offspring for shepherding continuity; gotra exogamy (father's clan); parallel and cross-cousin marriage permitted",
        "customary_divorce": "Decided by family elders; husband provides 'kharcha' (living allowance), legally fixed at 50% of income for government servants",
        "polygyny": "Known as 'sɒkəɳ' or 'sɒkəɳi', permitted if first wife unable to bear a male heir"
    },
    "geographic_distribution": {
        "himachal_pradesh": ["Chamba (Bharmaur, Budhil, Ravi)", "Kangra (Palampur, Dharamshala)", "Mandi", "Kullu (outer foothills of Dhauladhar, fringes of Pir-Panjal)"],
        "jammu_and_kashmir": ["Badherwah", "Basoli", "Ram Nagar", "Udhampur", "Bilawar", "Ramban", "Batot (Government of J&K n.d.)"],
        "other_states": ["Punjab", "Haryana"]
    },
    "demographics": {
        "census_2011_mother_tongue": 181069,
        "scheduled_tribe_population_2013": {
            "himachal_pradesh": 178130,
            "jammu_and_kashmir": 46489
        },
        "census_classification_note": "Grouped as a mother tongue under Hindi in Census 2011; Scheduled Tribe figures represent constitutional ST category"
    },
    "language_vitality": {
        "unesco_classification": "Definitely endangered (under name 'Bharmauri', UNESCO Atlas of World's Languages in Danger, 3rd ed.)",
        "authors_field_assessment": "Fieldwork in Kangra did not reveal severe endangerment or active language loss; intergenerational transmission remains active; used in elementary classrooms",
        "vulnerabilities": "Attrition of native-stock vocabulary (especially kinship terms, Sharma 2016); rapid encroachment and lexical replacement by Hindi-Urdu",
        "language_planning_needs": "Need for extensive documentation, orthographic standardization/script development, and mother-tongue educational materials"
    },
    "fieldwork_methodology": {
        "institution": "Centre for Linguistics (CLIN), Jawaharlal Nehru University (JNU), New Delhi",
        "initiator_and_mentors": "Field methods course instituted by Prof. Anvita Abbi, mentored by Prof. Ayesha Kidwai and Dr. Hari Madhav Ray",
        "field_cohorts": "2013 and 2015 MA Linguistics batches; follow-up online elicitation in February 2022",
        "fieldwork_villages": ["Palampur", "Saperu", "Banuri", "Kandbari (Kangra District, HP)"],
        "language_consultants": ["Tek Chand Sharma", "Urmila Rana", "Ratan Pahl (and others unnamed)"],
        "elicitation_instruments": "Modified Morris Swadesh word list (Abbi 2001, p. 248) and Abbi's basic sentence list",
        "digital_tools": "FieldWorks Language Explorer™ (FLEx) and Fling@JNU archive"
    },
    "dialectological_isolation_warning": {
        "authors_statement_p5": "Gaddi has varieties apart from the one described in this book, which is the variety spoken in and around Palampur. The varieties spoken in the districts of Chamba, Mandi, Kullu, and the state of Punjab and the Union Territory of Jammu and Kashmir require fresh descriptions.",
        "project_implication": "Kumari et al. (2026) cannot be cited as direct primary evidence for J&K Gaddi lexical usage. Its entries serve strictly as high-credibility comparative Western Pahari baseline data."
    }
}

# =========================================================================
# 5. gaddi_references.json (References pp. 129-130 & Index pp. 131-133)
# =========================================================================
print("5. Building gaddi_references.json...")
ref_raw_lines = []
for pno in range(146, 148):
    for line in get_p(pno).splitlines():
        line = line.strip()
        if not line or "Re FeReNC eS" in line or "References" in line:
            continue
        ref_raw_lines.append(line)

# Join multi-line references
bib_entries = []
current_entry = ""
for line in ref_raw_lines:
    if re.match(r"^[A-Z][a-zA-Z\s\.,\-]+?\(\d{4}[a-z]?\)", line):
        if current_entry:
            bib_entries.append(current_entry)
        current_entry = line
    else:
        if current_entry:
            current_entry += " " + line
        else:
            current_entry = line
if current_entry:
    bib_entries.append(current_entry)

parsed_refs = []
for b in bib_entries:
    b_clean = re.sub(r"\s+", " ", b).strip()
    m = re.match(r"^(.*?)\s*\((\d{4}[a-z]?|[a-z\.]+)\)\.\s*(.*)$", b_clean)
    if m:
        authors, year, rest = m.groups()
        parsed_refs.append({
            "citation_key": f"{authors.split(',')[0].strip().lower()}_{year}",
            "authors": authors.strip(),
            "year": year.strip(),
            "details": rest.strip(),
            "full_citation": b_clean
        })
    else:
        parsed_refs.append({
            "citation_key": "ref_misc",
            "authors": "Various",
            "year": "n.d.",
            "details": b_clean,
            "full_citation": b_clean
        })

# Index terms extraction from pp. 148-150 (PDF pp. 148-150)
index_terms = [
    {"term": "adjectives", "printed_pages": "39–41, 56–61, 76–8", "subcategories": ["attributive (57, 77, 78)", "predicative (57, 77)"]},
    {"term": "adpositions", "printed_pages": "58"},
    {"term": "adverbs", "printed_pages": "59–61", "subcategories": ["intensifiers (61)", "spatial (60)", "temporal (60)"]},
    {"term": "agreement", "printed_pages": "76–97", "subcategories": ["agreement blocking (73, 94–8)", "controller of agreement (79–94)", "object–verb (80)", "person agreement (81)", "subject–verb (80)"]},
    {"term": "aspect", "printed_pages": "86–91", "subcategories": ["imperfective (86)", "inchoative (90)", "perfective (87–9)", "progressive (89–90)"]},
    {"term": "aspiration", "printed_pages": "15, 20, 26, 30–4"},
    {"term": "auxiliaries", "printed_pages": "7, 52, 81–98"},
    {"term": "Bharmauri", "printed_pages": "1, 8, 71"},
    {"term": "case", "printed_pages": "35, 36, 39–47, 58, 69–80, 94–8", "subcategories": ["ablative (74)", "accusative (58, 69, 71, 72, 96, 97)", "case-marking inflection (35–7)", "dative (58, 71–2, 94–8)", "locative (6, 75)", "nominative (5, 6, 45, 46, 47, 58, 70, 75)", "oblique (44–5)", "split-case pattern (75–6)", "subject-oblique (69, 97)"]},
    {"term": "causatives", "printed_pages": "50–4"},
    {"term": "cleft", "printed_pages": "108"},
    {"term": "community", "printed_pages": "1–5, 8, 9"},
    {"term": "consonants", "printed_pages": "9–35, 80", "subcategories": ["approximants (30, 118)", "aspirated (17, 18, 26, 28, 35, 40, 41, 42)", "consonant clusters (22, 28, 31, 38, 40)", "coronal (30)", "geminate (26, 27, 28, 29, 30, 31, 38, 40, 42)", "glide (32, 33, 35, 46, 47)", "intervocalic (20, 21)", "nasal consonant (14, 30, 31, 24, 26)", "plosive (8, 26, 28, 35, 38)", "retroflex (35, 37, 38, 40, 42)"]},
    {"term": "coordination", "printed_pages": "106", "subcategories": ["adjectival (106)", "nominal (106)"]},
    {"term": "declension", "printed_pages": "5, 6, 35"},
    {"term": "diachronic", "printed_pages": "16"},
    {"term": "discourse", "printed_pages": "113–16"},
    {"term": "distinctive features", "printed_pages": "9, 15, 13, 14"},
    {"term": "endangerment", "printed_pages": "8"},
    {"term": "extraction", "printed_pages": "109"},
    {"term": "fieldwork", "printed_pages": "1, 6, 7, 8, 9, 11"},
    {"term": "focus", "printed_pages": "114–15", "subcategories": ["additive focus (115)", "emphasis (115)", "focus-marked nominals (115)"]},
    {"term": "gender", "printed_pages": "39–45, 76–89", "subcategories": ["grammatical (39–42)", "natural (41, 89)"]},
    {"term": "Grierson", "printed_pages": "5–8"},
    {"term": "Himachal Pradesh", "printed_pages": "1, 3, 9"},
    {"term": "honorificity", "printed_pages": "39, 49, 55, 81, 94"},
    {"term": "interjections", "printed_pages": "104"},
    {"term": "Jammu", "printed_pages": "1, 4, 7, 129"},
    {"term": "main clause, types of", "printed_pages": "101–6", "subcategories": ["declarative (101)", "exclamatives (104)", "imperative (103)", "interrogative (101)"]},
    {"term": "minimal pair", "printed_pages": "11"},
    {"term": "mood", "printed_pages": "91–4", "subcategories": ["epistemic (92)", "imperative (94)", "indicative (92)", "irrealis (45, 73, 97)"]},
    {"term": "morphology", "printed_pages": "9, 35, 40, 42, 69, 79, 82, 83"},
    {"term": "morphophonological", "printed_pages": "9, 11, 27, 34"},
    {"term": "negation", "printed_pages": "109–12", "subcategories": ["negation marker (109–12)", "negative polarity items (112)"]},
    {"term": "nouns", "printed_pages": "35–6, 40–5, 69–79, 94–6", "subcategories": ["plural (41, 42, 47, 68, 76–96)", "singular (42, 46, 76–97)"]},
    {"term": "numerals", "printed_pages": "61–8", "subcategories": ["cardinal (61–8)", "distributive (68)", "fractional (66–7)", "multiplicative (67)", "ordinal (66)"]},
    {"term": "oblique stems", "printed_pages": "44, 73"},
    {"term": "pastoralist", "printed_pages": "3, 4"},
    {"term": "phonological processes", "printed_pages": "22–35", "subcategories": ["nasalisation (22–5)", "prenasalisation (25–7)", "gemination (27–8)", "schwa epenthesis (28)", "glide formation (28–30)", "retroflexion (30–4)"]},
    {"term": "pronouns", "printed_pages": "45–9"},
    {"term": "questions", "printed_pages": "101–3, 107–9", "subcategories": ["content-word question (109)", "direct question (108)", "indirect question (108)", "polar question (101)", "question formation (107)", "wh-questions (102)", "wh-scope marking (108)"]},
    {"term": "subordinate clauses", "printed_pages": "105–7", "subcategories": ["coordinate clause (106)", "non-finite clause (105)", "relative clause (105)"]},
    {"term": "syllables", "printed_pages": "11, 15, 18–22, 34–7", "subcategories": ["canonical (19, 22)", "codas (18–21, 28, 35)", "nucleus (15, 18–22)", "onset (19–22, 28, 35)"]},
    {"term": "TAM", "printed_pages": "81–98"},
    {"term": "tense", "printed_pages": "81–5", "subcategories": ["future (73, 84)", "past (83)", "perfect (85–6)", "present (83, 92)"]},
    {"term": "verbs", "printed_pages": "49–55, 79–98", "subcategories": ["classification of Gaddi verbs (52–5)", "ditransitive (50)", "intransitive (50, 70)", "transitive (50–1, 70, 72, 75)", "verb root (79–94)", "verb morphology (79–94)"]},
    {"term": "vowels", "printed_pages": "11–36", "subcategories": ["diphthongs (12–16, 24, 28–9)", "hiatus (28–30, 36)", "monophthong (12–13)", "nasal vowels (12–15, 24)", "schwa (17, 18, 28)", "sonority (15, 19)", "vowel length (13, 22)"]}
]

gaddi_references_dataset = {
    "metadata": {
        "title": "A Grammar of Gaddi: Bibliography, Source-to-Content Map, and Index",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), References (pp. 129-130) & Index (pp. 131-133)",
        "license": "CC BY-NC 4.0",
        "total_references": len(parsed_refs),
        "total_index_terms": len(index_terms)
    },
    "bibliography": parsed_refs,
    "source_to_content_map": [
        {"source": "Abbi (2001)", "role": "Fieldwork methodology, Swadesh wordlist, basic sentence elicitation, causative classification (p. 9, 50, 80, 119)"},
        {"source": "Al-Haj Badran (2015)", "role": "Gaddi Lexicography Semantic Domains, Perso-Arabic loanwords (p. 43)"},
        {"source": "Anand (2013)", "role": "Causatives and Passives in Gaddi Language, causative elicitation (p. 51)"},
        {"source": "Asher & Kumari (1997)", "role": "Methodological model for consonant classes and syllable division (p. 20)"},
        {"source": "Bhatt (2007)", "role": "Indo-Aryan aspect-based split ergativity theoretical framework (p. 75)"},
        {"source": "Blake (2001)", "role": "Typology of case systems and morphological case (p. 70)"},
        {"source": "Brockhaus-Grand (1999)", "role": "Sonority Sequencing Principle and syllable sonority profile (p. 19)"},
        {"source": "Chatterji (1926)", "role": "Historical background on South Asian compound verbs (p. 8)"},
        {"source": "Comrie (1999)", "role": "Typology of numeral base systems (quinary, decimal, vigesimal) (p. 62)"},
        {"source": "Dixon (1977)", "role": "Semantic classification of adjectives (dimension, physical properties, value, etc.) (p. 56)"},
        {"source": "Fallows (1981)", "role": "Ambisyllabicity and coda doubling experiments (p. 36)"},
        {"source": "Ferguson (1963, 1975)", "role": "Phonological universals of nasal vowels and regressive nasal spread (p. 24, 25)"},
        {"source": "Government of India (2011, 2013)", "role": "Census mother-tongue counts (181,069) and Scheduled Tribe population statistics (p. 1)"},
        {"source": "Greenberg (1978)", "role": "Generalizations about numeral systems (atoms vs. syntagms) (p. 62)"},
        {"source": "Grierson (1916, 1922)", "role": "Historical baseline in LSI IX(I), Western Pahari classification, phonological comparisons (ś->kh), verb roots, declensions (p. 5-8)"},
        {"source": "Hall (2006)", "role": "Excrescent vowels and vocalic release vs. epenthesis (p. 17, 18)"},
        {"source": "Hamann (2003)", "role": "Articulatory characteristics of retroflex consonants (p. 30)"},
        {"source": "Itô & Mester (1986)", "role": "Obligatory Contour Principle (OCP) and Lyman's law for aspiration dissimilation (p. 33)"},
        {"source": "Kachru (1966)", "role": "Hindi syntactic comparisons, mass/abstract nouns, causatives (p. 42, 50)"},
        {"source": "Kahn (1980)", "role": "Onset Maximisation Principle in generative phonology (p. 21)"},
        {"source": "Kapila (2008)", "role": "Anthropological profile of Gaddis in Chamba, ghomtus pastoral self-identity (p. 1, 2)"},
        {"source": "Kumari, Mamta (2016, 2021)", "role": "Doctoral research on numeral typology; provided all Appendix III numeral data (p. 61, 125)"},
        {"source": "Levin (1993) & Levin & Rappaport Hovav (1995)", "role": "10 semantic verb classes and unaccusativity framework (p. 52-54)"},
        {"source": "Masica (1976, 1991)", "role": "South Asian linguistic area features, Indo-Aryan verb morphology, tense-aspect-mood, split ergativity (p. 8, 27, 50, 71, 72, 80, 82, 83, 86)"},
        {"source": "Mehta, Shreya (2016, 2021)", "role": "Primary empirical source for Gaddi verbal inflection, 'Gend' feature in perfective, TAM templates, 150+ sentence examples (p. 51, 52, 70, 80-97)"},
        {"source": "Mondal (2013)", "role": "Field methods report on noun-to-noun derivation (p. 42)"},
        {"source": "Naik (2015)", "role": "Gaddi lexicography and natural gender pairs of animates (Table 3.1) and count nouns (Table 3.2) (p. 41, 42)"},
        {"source": "Pandey (2014)", "role": "Vowel length neutralization in Indic languages (p. 13)"},
        {"source": "Prasad, Vishnu (2015)", "role": "Word formation processes and compound nouns (p. 43)"},
        {"source": "Reichenbach (1947)", "role": "Theoretical model of tense: Point of Event (E), Speech (S), Reference (R) (p. 83-85)"},
        {"source": "Richa (2008)", "role": "Hindi unaccusative/unergative verb classifications applied to Gaddi (p. 54)"},
        {"source": "Riemsdijk (1982)", "role": "Wh-scope marking in finite embedded clauses (p. 108)"},
        {"source": "Sharma, Shilpi (2016)", "role": "Sociolinguistic profile, kinship terminology, intra-caste marriage, gotra exogamy (p. 4, 8)"},
        {"source": "Spencer (2009) & Malchukov & Spencer (2009)", "role": "Theoretical definitions of morphological and syntactic case (p. 69, 70)"},
        {"source": "Steele (1978)", "role": "Cross-linguistic definition of agreement as systematic covariance (p. 79)"},
        {"source": "Trubetzkoy (1969)", "role": "Phonological theory of vowel length (p. 13)"},
        {"source": "Turner (1966)", "role": "Comparative Dictionary of the Indo-Aryan Languages (CDIAL), native-stock lexical identification (p. 43)"},
        {"source": "Winter (1992)", "role": "Indo-European numeral structure (atoms vs. syntagms) (p. 62)"}
    ],
    "index": index_terms
}

# =========================================================================
# 6. gaddi_morphology.json & 7. gaddi_syntax.json & 8. gaddi_grammar.json
# =========================================================================
print("6. Building gaddi_morphology.json, gaddi_syntax.json, and gaddi_grammar.json...")

gaddi_morphology_dataset = {
    "metadata": {
        "title": "Morphological System of Kangra Gaddi",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Chapters 2, 3, 4 (pp. 35-98)",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "license": "CC BY-NC 4.0",
        "evidence_status": "comparative_only"
    },
    "nominal_morphology": {
        "gender_system": {
            "type": "two_way",
            "values": ["masculine", "feminine"],
            "phonological_tendencies": "Vowel /u/ typically masculine; vowel /i/ typically feminine; consonant-final variable",
            "natural_gender_overrides": True,
            "semantic_classes": {
                "ornaments": "all feminine (matika, bɑ:li, kəɖoɭi)",
                "days_of_week": "all masculine (tuɑr, suɑr, breb)"
            }
        },
        "number_system": {
            "values": ["singular", "plural"],
            "count_nouns": "Inflect for plural: -ɑ stems change to -e (nikkɑ -> nikke, buɖʰɑ -> buɖʰe); consonant stems add -ɑ (pɑɽ -> pɑɽɑ, kətɑb -> kətɑbɑ̃); zero inflection (urnu sg/pl)",
            "mass_nouns": "Do not manifest plural number (teɭi 'oil', čəuɭ 'rice', kʰənɖ 'sugar', kʰɑɳɑ 'food', tɔ:dʒurbɑ: 'experience')"
        },
        "case_markers_and_adpositions": [
            {"case": "nominative", "marker": "Ø (zero marked)", "type": "noun_dependent", "function": "Subject of intransitives, and transitive subjects in imperfective/progressive"},
            {"case": "accusative", "marker": "-dʒo / -o", "type": "noun_dependent", "function": "Direct object marking; -o is only used on direct objects, never on indirect objects"},
            {"case": "dative", "marker": "-dʒo", "type": "noun_dependent", "function": "Indirect objects (goals/beneficiaries) and experiencer subjects (pəŋkədʒɑ-dʒo bʰukə ləɡ-ur-i hɑ)"},
            {"case": "ergative", "marker": "-ɛ (with sonorant gemination on stems) or suppletive oblique", "type": "noun_dependent", "function": "Subject of transitive verbs in perfect tense and perfective aspect (aspect-based split)"},
            {"case": "oblique", "marker": "stem suppletion: vowel stems unchanged; consonant stems undergo gemination + -ɑ (bisɑl -> bisɑllɑ, rɑm -> rəmmɑ)", "type": "noun_dependent", "function": "Required base for all postpositions and case markers"},
            {"case": "subject_oblique", "marker": "suppletive oblique stem without overt case suffix", "type": "noun_dependent", "function": "Marks subjects of irrealis mood (future/unrealized events); blocks subject agreement"},
            {"case": "ablative", "marker": "tʰaũ / hɔ / haũ", "type": "noun_independent_adposition", "function": "Movement away from source, temporal origin, standard of comparison"},
            {"case": "instrumental", "marker": "-te / -hoɡɡi / -sɔɡi", "type": "noun_independent_adposition", "function": "Instrument of action or comitative accompaniment"},
            {"case": "locative", "marker": "pur / məndʒ", "type": "noun_independent_adposition", "function": "Spatial/temporal location ('on' = pur, 'in/inside' = məndʒ)"}
        ]
    },
    "pronominal_morphology": {
        "nominative": {"1sg": "ɑũ / əũ", "1pl": "əsɛ", "2sg": "tu", "2pl": "tussɛ", "3sg_prox": "e", "3sg_dist": "so", "3pl_prox": "e", "3pl_dist": "ɑho"},
        "accusative": {"1sg": "mindʒo", "1pl": "əsudʒo", "2sg": "tidʒdʒo", "2pl": "tusidʒo", "3sg_prox": "tessijo", "3sg_dist": "tijɑ̃", "3pl_prox": "ijẽdʒo", "3pl_dist": "tijẽdʒo"},
        "dative": {"1sg": "mindʒo, mu", "1pl": "əsudʒo", "2sg": "tidʒdʒo", "2pl": "tusijo", "3sg_prox": "tessijo", "3sg_dist": "tessijo", "3pl_prox": "ij˜edʒo", "3pl_dist": "tij˜edʒo"},
        "genitive": {"1sg": "merɑ / meri / mere", "1pl": "indɑ / indi / indɛ", "2sg": "terɑ / teri / tere", "2pl": "təjɑrɑ / təjɑre, tinj̃ɛ", "3sg": "serɑ / seri / serɛ", "3pl": "userɑ / useri, uʋɛrɑ"},
        "ergative": {"1sg": "mei", "1pl": "ahɛ", "2sg": "tei / tẽi", "2pl": "tussɛ", "3sg": "tinni", "3pl": "tiɳje"},
        "subject_oblique": {"1sg": "mu", "1pl": "su, əsu", "2sg": "unrecorded", "2pl": "tussu", "3sg": "tessə", "3pl": "unrecorded"},
        "honorific": {"2nd_person": {"nom": "tussɛ", "acc": "tusijo", "dat": "unrecorded", "gen": "tundɛ", "erg": "tussɛ"}, "3rd_person": {"nom": "uɳi", "acc": "tijẽdʒo", "dat": "ijẽdʒo", "gen": "unrecorded", "erg": "unrecorded"}},
        "reflexive": "ɑpɳ-X (inflects for gender and number: ɑpɳɑ, ɑpɳi, ɑpɳe)",
        "neutral_pronoun": "ta (words for 'it')"
    },
    "verbal_morphology": {
        "verb_templates": {
            "template_1": "Verb_Root + TAM_suffix + AGR_suffix",
            "template_2": "Verb_Root-TAM_suffix.Gend + Auxiliary + AGR_suffix"
        },
        "inflectional_affixes": {
            "infinitive": "-ɳɑ (after vowels) / -nɑ (after liquids /ɾ, ɭ/)",
            "first_causative_transitiviser": "-ɑ (e.g. kʰil-ɑ-u)",
            "second_causative_causativiser": "-ʋɑ (e.g. pil-ʋɑ-u, kʰil-ʋɑ-u)",
            "past_tense_auxiliary": "tʰ-u (masc.sg), tʰ-i (fem.sg), tʰi-jɛ (plural/honorific)",
            "future_tense_suffix": "-ɳ + agreement (-ɑ/-i/-ɛ)",
            "perfect_tense_suffix": "-ur + agreement (-ɑ/-i/-ɛ)",
            "imperfective_aspect_suffix": "-d (after closed stems) / -nd (after open stems) + agreement (-ɑ/-i/-ɛ)",
            "perfective_aspect_suffix": "-u (masc.sg) / -i (fem.sg) / -ɛ (plural/honorific) - encodes 'Gend' feature (ma/fe)",
            "indicative_mood_auxiliary": "h-ɑ (singular) / h-in (plural/honorific)",
            "epistemic_mood_suffix": "-ɭɭ + agreement (-ɑ/-i/-ɛ)",
            "imperative_mood_suffix": "-ɑ (masc.sg), -i (fem.sg), -ɛ (plural/honorific)"
        },
        "agreement_hierarchy": "Honorificity > Number > Gender (Steele 1978; Masica 1991)",
        "case_blocking_rule": "Case marking on an NP blocks that NP from controlling agreement on the verb. If subject is ergative/dative, agreement falls to direct object. If direct object is also case marked (-dʒo or -o), verb takes default agreement (3sg.m)."
    }
}

gaddi_syntax_dataset = {
    "metadata": {
        "title": "Syntactic System and Clause Typology of Kangra Gaddi",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Chapter 5 (pp. 99-116)",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "license": "CC BY-NC 4.0",
        "evidence_status": "comparative_only"
    },
    "word_order": {
        "canonical": "SOV (Subject - Object - Verb)",
        "with_adjuncts": "Subject - Indirect Object - Direct Object - Verb",
        "modifiers": "Preverbal and prenominal (modifiers precede nouns and verbs)",
        "adpositions": "Postpositional (nouns precede adpositions)",
        "scrambling": "Freely permitted for discourse functions; fronted object encodes contrastive focus"
    },
    "main_clause_types": [
        {"type": "declarative", "structure": "SOV canonical; unmarked declarative statements"},
        {"type": "polar_interrogative", "structure": "Formed by inserting question particle 'kɛ' clause-initially or clause-finally (e.g. 'kɛ tusɛ ədʒ əkhbɑr pəɽ-i' / 'tusɛ ədʒ əkhbɑr pəɽ-i kɛ')"},
        {"type": "wh_interrogative", "structure": "Wh-in-situ (wh-word replaces questioned constituent without fronting)", "wh_words": {"kɛ": "what", "kuɳ": "who", "kəs": "which", "kijẽ": "how", "kəɖi": "where", "kəjo": "why", "kəɳe": "when"}},
        {"type": "imperative", "structure": "Second-person subject typically dropped; verb inflects with -ɑ (m), -i (f), -ɛ (pl/hon)", "examples": ["əmb bəɖɖ-ɑ (Cut the mango)", "əndrɑǰo əij-ɑ (Come in)", "behi (Please sit down)"]},
        {"type": "exclamative", "structure": "Formed with emotive interjections: 'vah!', 'hɛ bʰəgvan!', 'ərɛ!', 'ərɑ!', 'o:!', 'ʃɑbɑʃ!'"}
    ],
    "subordinate_clause_types": [
        {"type": "relative_clause", "structure": "Correlative construction: relative pronoun 'dʒes' / 'dʒəs' in relative clause + correlative pronoun 'so' / 'təssɑ' in main clause", "reduced_form": "Relative clause directly precedes modified noun without pronouns"},
        {"type": "non_finite_clause", "structure": "Marked with infinitival suffix -nɑ / -ɳɑ (e.g. 'rəso kər-n-ɑ pəsənd hɑ')"},
        {"type": "coordinate_clause", "structure": "Nominal or verbal coordination with conjunctions 'tɛ' / 'ətɛ' ('and'), 'pər' ('but')"}
    ],
    "core_syntactic_relations": {
        "wh_in_situ": "Wh-words remain in base structural position; fronting is scrambling for focus, not syntactic movement",
        "wh_scope_marking": "Direct question reading out of finite complement clauses requires scope marker 'kɛ' in matrix clause (Riemsdijk 1982); single scope marker used for multiple embedded wh-words",
        "wh_extraction_prohibition": "Syntactic wh-extraction out of finite complement clauses is strictly ungrammatical (*kɛ rɑm dʒɑɳ-d-ɑ hɑ dʒe sitɛ khə-u?)"
    },
    "negation_system": {
        "negation_markers": [
            {"marker": "/nɑ/", "distribution": "General preverbal negative marker"},
            {"marker": "/ni/", "distribution": "Preverbal negative marker, interchangeable with /nətʰi/"},
            {"marker": "/nətʰi/", "distribution": "Negative copular marker, interchangeable with /ni/"},
            {"marker": "/mət/ or /mətʰ/", "distribution": "Prohibitive marker used in negative imperatives"}
        ],
        "tam_interactions": {
            "perfective": "Negative marker either precedes main verb or intervenes between main verb and past auxiliary",
            "imperfective": "Negative marker always precedes main verb; indicative copula 'hɑ' is barred when negated",
            "progressive": "Negative marker precedes main verb or precedes progressive auxiliary 'kər-'",
            "modals": "Negative marker can precede or follow main verb with modal 'səkɳɑ' ('can')",
            "complex_predicates": "Negative marker can precede either main verb or light verb"
        },
        "negative_polarity_items": [
            {"npi": "koi bʰi", "meaning": "anyone"},
            {"npi": "kəddi bʰi", "meaning": "never"},
            {"npi": "əkkə bʰi", "meaning": "even one"},
            {"npi": "həlli təkər", "meaning": "until now"}
        ]
    },
    "information_structure": {
        "topic": "Sentence-initial position; marked by fronting",
        "contrastive_topic": "Marked by postposed particle 'tɑ'",
        "focus": "Immediate preverbal position in canonical order",
        "focus_particles": [
            {"particle": "hi", "function": "Restrictive focus ('only') / emphasis; attaches to any category"},
            {"particle": "sirf", "function": "Pre-nominal restrictive focus ('only')"},
            {"particle": "bʰi", "function": "Additive focus ('even' / 'also')"}
        ]
    }
}

gaddi_grammar_dataset = {
    "metadata": {
        "title": "Descriptive Grammar of Kangra Gaddi (Palampur)",
        "source_id": "kumari_2026",
        "source_citation": "Kumari et al. (2026), Chapters 3, 4, 5",
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "license": "CC BY-NC 4.0",
        "evidence_status": "comparative_only"
    },
    "phonology_summary": gaddi_phonology_dataset,
    "morphology_summary": gaddi_morphology_dataset,
    "syntax_summary": gaddi_syntax_dataset,
    "adjectives_table_3_14": {
        "dimension": ["bəɽɑ (big)", "hɑlkɑ (small)", "pɑtəɭə (thin)", "ləmmɑ (long)", "tʃɔɖi (wide)", "ɡehro (deep)", "untʃɑ (high)", "muʈʈɑ (big)"],
        "physical_properties": ["mitthɑ (sweet)", "sɑf (clean)", "kũɭɑ (soft)", "kʰudrɑ (hard)", "dʒəilɑ (hard)", "kɑtʃtʃɑ (raw)", "məiljɛ (dirty)", "tədi (sharp)", "kʰurdur (rough)", "tʃipʰlɑ (smooth)", "mәʈәmɛlɑ (soiled)", "hiɭɭɑ (cold)", "dʰudʰlɑ (blur)", "tətti (hot)", "trit (sour)", "ɡoɭ (round)", "kәudɑ (bitter)", "luɳkɑ (salty)", "pʰikɑ (tasteless)", "bʰɑddɑ (ugly)", "tʃɛɭ (beautiful)", "kɑ:ɭɑ (black)", "hukke (dry)", "sidʒi (wet)", "bʰədʒuri (broken)", "swɑdi (tasty)", "pʰuki (burnt)"],
        "value": ["kʰərɑ (good)", "burɑ (bad)", "mehengɑ (expensive)", "sәstɑ (cheap)", "dʒɑruri (important)"],
        "human_propensity": ["takatwar (strong)", "tʰɛɭ (healthy)", "kәmzor (weak)", "udɑːs (sad)", "kʰuʃ (happy)", "tedʒ (sharp)", "ɡʰәmәnɖi (proud)", "duʃʈә (cruel)", "kʰidʒi (tired)", "bimɑr (sick)", "trihəɳɑ (thirsty)", "bukkʰɑ (hungry)", "bədtəmiːz (arrogant)", "bʰoɭɑ (innocent)", "bədmɑʃ (naughty)"],
        "speed": ["bəlɛ (slow)", "təũɭɛ (fast)", "dʒəldi (quick)", "dʒɑt (early)"],
        "age": ["buɖɖɑ (old)", "dʒəwɑn (young)", "bәtʃtʃɑ (childish)"]
    },
    "levin_verb_classes": {
        "verbs_of_motion": ["uɖɳɑ (fly)", "tʃəlɳɑ (walk)", "ɡʰumɳɑ (turn/roam)", "peɳɳɑ (put)", "tʃəɭəɳɑ (drive)", "terɳɑ (swim)", "bəɖɳɑ (enter)", "tʃukɳɑ (lift)", "tʃʰɑdɳɑ (quit)", "bəɖəlɳɑ (turn)", "bʰədʒɳɑ (transfer)", "dəŋɡɳɑ (strike)", "bəhɳɑ (flow)", "kʰəɳɳɑ (dig)", "peiɳɑ (fall)", "leɳɑ (take)"],
        "verbs_of_change_of_state": ["kʰilɳɑ/kʰidɳɑ (bloom)", "həkɳɑ (dry)", "dʒəmɳɑ (freeze)", "truʈɳɑ/bʰədʒɳɑ (break)", "bənɑɳɑ (make/cook)", "bədəlɳɑ (change)", "ɡʰuhɑɖɳɑ/kholɳɑ (open)", "uʈʰɳɑ (wake)", "muskurana (smile)", "ʃərmɑnɑ (be shy)"],
        "verbs_of_perception": ["sunɳɑ (listen)", "dekʰɳɑ/herɳɑ (see)", "huɳɳɑ (listen)", "bəlɳɑ (speak)", "dʒɑnaɳɑ (know)", "ləɡɳɑ (feel)", "tʃəkʰɳɑ (taste)", "tʃɑɳɑ (want)", "tʃuɳɑ (touch)"],
        "verbs_of_consumption": ["kʰɑɳɑ (eat)", "piɳɑ (drink)", "kʰilɑɳɑ (feed)", "niɡəlɳɑ (swallow)", "leɳɑ (have/take)", "pəɳɳɑ (put)", "tʃɑɳɑ (want)"],
        "verbs_of_image_impression": ["rəŋɡɳɑ (paint)", "pəɽɳɑ (read)", "likʰɳɑ (write)"],
        "verbs_of_bodily_processes": ["tʰukɳɑ (spit)", "kʰɑŋɡɳɑ (cough)", "roɳɑ (cry)", "həsɳɑ (laugh)", "uʈʰɳɑ (wake)", "ʃərmɑnɑ (be shy)", "muskurana (smile)", "dekʰɳɑ/herɳɑ (see)", "huɳɳɑ (listen)", "dəŋɡɳɑ (stink)", "bəlɳɑ (speak)", "ləɡɳɑ (feel)", "tʃəkʰɳɑ (taste)", "tʃɑɳɑ (want)"],
        "verbs_of_spatial_configuration": ["ləʈəkɳɑ (hang)", "beʃɳɑ (sit)", "kʰədɳɑ (stand)"],
        "verbs_of_existence_appearance_disappearance": ["rɛɳɑ (live/stay)", "mərɳɑ (die)", "uʈʰɳɑ (wake)", "hoɳɑ (be)", "bʰuɳɑ (happen)", "tʃəlɳɑ (walk)", "kʰolɳɑ (open)"],
        "verbs_of_emission": ["roɳɑ (cry)", "ɡurrana (roar)", "kəɽəkɳɑ (thunder)", "bədʒɳa (ring)", "dəŋɡɳɑ (stink)"],
        "verbs_of_contact_attachment": ["tʃipakɳɑ (stick)", "ləɡɑɳɑ (put/attach)", "mɑrɳɑ (beat)", "ləɡɳɑ (feel)"]
    },
    "verbal_paradigm_hasna_table_4_1": {
        "verb_root": "həs- (to laugh)",
        "categories": {
            "PAST_AUX": {"SGM": "tʰu", "SGF": "tʰi", "SGM_HON": "tʰijɛ", "SGF_HON": "tʰijɛ", "PLM": "tʰijɛ", "PLF": "tʰijɛ", "PLM_HON": "tʰijɛ", "PLF_HON": "tʰijɛ"},
            "FUTURE": {"SGM": "həsɳɑ", "SGF": "həsɳi", "SGM_HON": "həsɳɛ", "SGF_HON": "həsɳɛ", "PLM": "həsɳɛ", "PLF": "həsɳɛ", "PLM_HON": "həsɳɛ", "PLF_HON": "həsɳɛ"},
            "PERFECT": {"SGM": "həsurɑ", "SGF": "həsuri", "SGM_HON": "həsurɛ", "SGF_HON": "həsurɛ", "PLM": "həsurɛ", "PLF": "həsurɛ", "PLM_HON": "həsurɛ", "PLF_HON": "həsurɛ"},
            "IMPERATIVE": {"SGM": "həs", "SGF": "həsi", "SGM_HON": "həsɛ", "SGF_HON": "həsɛ", "PLM": "həsɛ", "PLF": "həsɛ", "PLM_HON": "həsɛ", "PLF_HON": "həsɛ"},
            "EPISTEMIC": {"SGM": "həsɭɭɑ", "SGF": "həsɭɭi", "SGM_HON": "həsɭɭɛ", "SGF_HON": "həsɭɭɛ", "PLM": "həsɭɭɛ", "PLF": "həsɭɭɛ", "PLM_HON": "həsɭɭɛ", "PLF_HON": "həsɭɭɛ"},
            "INDICATIVE_AUX": {"SGM": "hɑ", "SGF": "hɑ", "SGM_HON": "hin", "SGF_HON": "hin", "PLM": "hin", "PLF": "hin", "PLM_HON": "hin", "PLF_HON": "hin"},
            "IMPERFECTIVE": {"SGM": "həsdɑ", "SGF": "həsdi", "SGM_HON": "həsdɛ", "SGF_HON": "həsdɛ", "PLM": "həsdɛ", "PLF": "həsdɛ", "PLM_HON": "həsdɛ", "PLF_HON": "həsdɛ"},
            "PERFECTIVE": {"SGM": "həsu", "SGF": "həsi", "SGM_HON": "həsɛ", "SGF_HON": "həsɛ", "PLM": "həsɛ", "PLF": "həsɛ", "PLM_HON": "həsɛ", "PLF_HON": "həsɛ"},
            "PROG_V": {"SGM": "həsu", "SGF": "həsi", "SGM_HON": "həsu", "SGF_HON": "həsi", "PLM": "həsu", "PLF": "həsi", "PLM_HON": "həsu", "PLF_HON": "həsi"},
            "PROG_AUX": {"SGM": "kərdɑ", "SGF": "kərdi", "SGM_HON": "kərdɛ", "SGF_HON": "kərdɛ", "PLM": "kərdɛ", "PLF": "kərdɛ", "PLM_HON": "kərdɛ", "PLF_HON": "kərdɛ"},
            "INCHO_V": {"SGM": "həsɳɑ", "SGF": "həsɳi", "SGM_HON": "həsɳɛ", "SGF_HON": "həsɳɛ", "PLM": "həsɳɛ", "PLF": "həsɳɛ", "PLM_HON": "həsɳɛ", "PLF_HON": "həsɳɛ"},
            "INCHO_AUX": {"SGM": "ləɡurɑ", "SGF": "ləɡuri", "SGM_HON": "ləɡurɛ", "SGF_HON": "ləɡurɛ", "PLM": "ləɡurɛ", "PLF": "ləɡurɛ", "PLM_HON": "ləɡurɛ", "PLF_HON": "ləɡurɛ"}
        }
    }
}

# =========================================================================
# 7. gaddi_examples.json (Examples 1 to 269)
# =========================================================================
print("7. Building gaddi_examples.json...")

# We will extract all numbered examples by regex across pages 23 to 133
raw_examples = []
current_num = None
current_lines = []
current_pno = None

# Scan pages sequentially
for pno in range(18, 134):
    lines = get_p(pno).splitlines()
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        # Match example number start e.g. (1), (22), or 22)
        m = re.match(r"^(?:\((\d+)\)|(\d+)\))\s*(.*)$", line_str)
        if m:
            num = int(m.group(1) or m.group(2))
            # Store previous
            if current_num is not None:
                raw_examples.append({
                    "number": current_num,
                    "text": "\n".join(current_lines),
                    "pdf_page": current_pno,
                    "printed_page": current_pno - 17
                })
            current_num = num
            current_pno = pno
            current_lines = [m.group(3)] if m.group(3) else []
        else:
            if current_num is not None:
                # Stop if hitting major heading or footer
                if "A GRAMMAR OF GADDI" in line_str or "PHONETICS AND PHONOLOGY" in line_str or "MAJOR WORD CLASSES" in line_str or "MORPHOSYNTAX" in line_str or "CLAUSE TYPES" in line_str:
                    continue
                current_lines.append(line_str)

if current_num is not None:
    raw_examples.append({
        "number": current_num,
        "text": "\n".join(current_lines),
        "pdf_page": current_pno,
        "printed_page": current_pno - 17
    })

print(f"Extracted {len(raw_examples)} numbered example blocks.")

# Process each example block into clean structured format
processed_examples = []
for ex in raw_examples:
    num = ex["number"]
    txt = ex["text"].strip()
    pno = ex["pdf_page"]
    ch = 1 if pno <= 27 else (2 if pno <= 54 else (3 if pno <= 85 else (4 if pno <= 115 else 5)))
    
    # Extract attribution if present at end e.g. (Mehta 2016, ex. 1.3)
    attr = "Kumari et al. (2026)"
    m_attr = re.search(r"\((Mehta|Grierson|Anand|Sharma|Naik|Prasad)[^)]+\)", txt)
    if m_attr:
        attr = m_attr.group(0).strip("()")
    
    # Extract translation in single quotes
    translations = re.findall(r"[‘']([^'’]+)[’']", txt)
    clean_trans = "; ".join(translations) if translations else ""
    
    processed_examples.append({
        "example_id": f"kumari-ex-{num:03d}",
        "example_number": num,
        "chapter": ch,
        "printed_page": ex["printed_page"],
        "pdf_page": pno,
        "raw_text": txt,
        "english_translation": clean_trans,
        "attribution": attr,
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "source_id": "kumari_2026",
        "evidence_status": "comparative_only",
        "is_jk_verified": False,
        "license": "CC BY-NC 4.0"
    })

# =========================================================================
# Write all datasets to data/ and src/gaddi/resources/
# =========================================================================
datasets = {
    "gaddi_word_list.json": word_list_entries,
    "gaddi_numerals.json": gaddi_numerals_dataset,
    "gaddi_phonology.json": gaddi_phonology_dataset,
    "gaddi_cultural_sociolinguistic_notes.json": gaddi_cultural_dataset,
    "gaddi_references.json": gaddi_references_dataset,
    "gaddi_morphology.json": gaddi_morphology_dataset,
    "gaddi_syntax.json": gaddi_syntax_dataset,
    "gaddi_grammar.json": gaddi_grammar_dataset,
    "gaddi_examples.json": processed_examples
}

for fname, d in datasets.items():
    p1 = DATA_DIR / fname
    p2 = RES_DIR / fname
    with open(p1, "w", encoding="utf-8") as f1:
        json.dump(d, f1, ensure_ascii=False, indent=2)
    with open(p2, "w", encoding="utf-8") as f2:
        json.dump(d, f2, ensure_ascii=False, indent=2)
    print(f"Saved and synchronized: {fname} (Size: {p1.stat().st_size} bytes)")

print("All 9 datasets generated and synchronized successfully!")

