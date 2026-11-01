import re

def clean_source_text(text):
    t = text.strip()
    # Remove parenthetical comments or split them
    t = re.sub(r'\(.*?\)', '', t).strip()
    # Remove question marks and odd OCR symbols
    t = t.replace('?', '').replace('!', '').replace('“', '').replace('”', '')
    t = t.replace('‘', '').replace('’', '').replace("'", "")
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def roman_to_devanagari(text):
    t = clean_source_text(text)
    if not t:
        return ""

    # Specific authentic Bharmauri lemmas and multiword overrides
    OVERRIDES = {
        # Core nature & elements
        "biar": "ब्यार", "biyari": "ब्यारी", "biyar": "ब्यार",
        "halkibiyari": "हलकी ब्यारी", "halki biyari": "हलकी ब्यारी",
        "mottibiyari": "मोटी ब्यारी", "moţţibiyari": "मोटी ब्यारी", "motti biyari": "मोटी ब्यारी",
        "hura biyari": "हुरा ब्यारी",
        "dhodu": "धोदु", "badalu": "बादलु", "baddal": "बद्दर",
        "hi:th": "हीथ", "hith": "हीथ", "hi:t": "हीत", "hit": "हीत",
        "nhe:ra": "न्हेरा", "nhera": "न्हेरा",
        "dhart": "धर्त", "dharat": "धरत",
        "gra:n": "ग्राह्ण", "grĕn": "ग्रेन", "gran": "ग्राह्ण",
        "a:g": "आग", "ag": "आग", "aag": "आग",
        "dundu": "धुंदु", "banu": "बनु", "heu": "हेउ", "heũ": "हेउँ", "hiyu": "हियु", "hiyũ": "हियुँ",
        "chanani": "चानणी", "angãri": "अंगारी", "ankari": "अणकारी",
        "barkha": "बर्खा", "samundar": "समुंदर", "ambar": "अंबर",
        "sta:re": "स्तारे", "stare": "स्तारे", "na: r": "नार", "nar": "नार", "gholē": "घोले", "ghole": "घोले",
        "pani": "पाणी", "pa:ni": "पाणी",
        
        # Family & kinship
        "mabura": "माबुरा", "ma-bura": "माबुरा", "ma-bure": "माबुरा", "ma bura": "माबुरा",
        "dharam puttar": "धरम पुत्तर", "dharm puttar": "धरम पुत्तर",
        "gobru": "गोबरू", "gobro": "गोबरो", "abbi gobru": "अब्बी गोबरू",
        "lada": "लाड़ा", "lāRa": "लाड़ा", "lara": "लाड़ा", "lare": "लाड़े",
        "ladi": "लाड़ी", "lāRi": "लाड़ी", "lari": "लाड़ी",
        "buŗa": "बुड़ा", "bura": "बुरा", "budda": "बुड्ढा", "sena": "सेणा",
        "kuri": "कुड़ी", "kuDi": "कुड़ी",
        "bhenu": "भेणु", "bheni": "भेणी",
        "baroji": "बरोजी", "barki": "बड़की", "shalanu": "शलानु",
        "janani": "जनानी", "betari": "बेतरी", "tirmbath": "तिरम्बथ",
        "nikka": "निक्का", "bacha": "बच्छा", "bachhe": "बच्छे",
        "amma": "अम्मा", "eziz": "एज़िज़",
        "batija": "भतीजा", "bandri - yar": "बंद्री-यार", "badri - ja": "बद्री-जा",
        "banji": "भांजी", "bhareyi": "भरयी",
        "mama": "मामा", "mola": "मोला",
        "sala": "साला", "jija": "जीजा", "sali": "साली", "daroji": "दरोजी",
        "petaru": "पेतरु", "kaka": "काका", "kawi": "कवी",

        # Body parts
        "dãnd": "दाँद", "dand": "दंद",
        "jibh": "जीभ", "jib": "जीभ",
        "hath": "हत्थ", "ha:t": "हाथ", "khabi hatte": "खाबी हत्थे",
        "múndu": "मुंडु", "mundu": "मुंडु",
        "dhidh": "ढिढ", "didh": "दिध",
        "gaDi": "गाडी", "múcha": "मूँछ", "mucha": "मूँछ",
        "neynu": "नेयनु", "nẽynu": "नेयनु",
        "pãnku": "पांकु", "panku": "पांकु",
        "nẽh": "नेह", "neh": "नेह",
        "brũa": "ब्रुँआ", "brua": "ब्रुँआ",
        "ãkhri ghuadna": "आँखरी घुआड़ना",

        # Animals & birds
        "kala kaRpa": "काला कड़पा", "kala khaRpa": "काला खड़पा", "kaRpa": "कड़पा", "khaRpa": "खड़पा",
        "kutar-u": "कुत्तरु", "kutta": "कुत्ता", "kutter": "कुत्तर", "kutti": "कुत्ती", "kuttti": "कुत्ती",
        "machi": "माछी", "macchi": "मच्छी",
        "bakri": "बकरी", "bhed": "भेड़",
        "gora": "घोड़ा", "ghoRa": "घोड़ा", "ghoRi": "घोड़ी", "ghori": "घोड़ी",
        "alla": "अल्ला",
        "pakru": "पखरू", "pakhru": "पखरू",
        "muha": "मूह", "groDDu": "ग्रोड्डु", "giddal": "गिद्दड़", "gidhhat": "गिद्दड़",

        # Food & plants
        "dūdh": "दूध", "dud": "दूध", "dudu": "दूध",
        "loon": "लूण", "lūn": "लूण",
        "challi": "छल्ली",
        "barghat": "बरघट", "bhuttar": "भुत्तर", "bhutta": "भुट्टा", "dali": "डाली",
        "ghĩu ra diya": "घीउ रा दीआ", "ghiu ra diya": "घीउ रा दीआ",
        "gaira mans": "गायरा माँस", "gayra maans": "गायरा माँस",

        # Expressions, verbs & phrases
        "bale bale": "बले बले", "jore jore": "जोरे जोरे",
        "bale bale kane": "बले बले काणे", "jore jore kane": "जोरे जोरे काणे", "jore mat kane": "जोरे मत काणे",
        "tunda na ke": "तुंदा ना के", "tu teri renden": "तू तेरी रेंदेन",
        "khabi kanare": "खाबी कणारे", "undi payi": "उंदी पई",
        "undẽ janu": "उंदे जाणू", "unde janu": "उंदे जाणू",
        "jhola kholu": "झोला खोलू", "pani ciRkna": "पाणी चिड़कणा",
        "dasna wala": "दसणा वाला", "kapRa banana": "कपड़ा बणाणा",
        "so munjo tale kam kanta": "सो मुंजो तले कम कांता",
        "skula taun gach": "स्कुला तौन गच्छ", "re-da-re skula taun-ai": "रे-दा-रे स्कुला तौन-आई",
        "mari-ditta": "मारी-दित्ता", "mari ditta": "मारी-दित्ता",
        "phãy manj phasana": "फाँय मंज फसाणा", "phũnjna": "फुंजणा", "pũnniya": "पुँनिया",
        "kuãna": "कुआणा", "hãna": "हाणा", "ĩna": "ईणा", "ina": "औणा",
        "sarak": "सड़क", "rasta": "रास्ता", "sisa": "सीसा",
        "sunnu": "सुन्नु", "loha": "लोहा", "chandi": "चांदी", "puja": "पूजा", "chori": "चोरी",
        "khelha": "खेलहा", "kheldna": "खेल्दणा", "nacna": "नचना", "karna": "करणा",
        "kana": "खाणा", "pīna": "पीणा", "pina": "पीणा", "gana": "जाणा", "dina": "देणा", "lina": "लैणा",
        "behna": "बहणा", "sona": "सौणा", "suna": "सौणा", "marna": "मारणा",
        "sidda": "सिद्धा", "mugda": "मुगदा", "jagna": "जगणा", "anDa": "आँडा", "dusman": "दुश्मन",
        "stara": "सतारा", "aTTaran": "अठारह", "pantra": "पंदरा", "chour": "चौर", "due": "दुए", "thray": "त्रै",
    }

    clean_k = t.lower().replace(":", "").replace("-", "")
    for k, v in OVERRIDES.items():
        if clean_k == k.lower().replace(":", "").replace("-", ""):
            return v

    # Fallback systematic transliteration
    # Replace pre-composed accented vowels
    t = t.replace("ã", "a~").replace("ẽ", "e~").replace("ĩ", "i~").replace("õ", "o~").replace("ũ", "u~")
    t = t.replace("à", "a").replace("á", "a").replace("ā", "a:")
    t = t.replace("è", "e").replace("é", "e").replace("ē", "e:")
    t = t.replace("ì", "i").replace("í", "i").replace("ī", "i:")
    t = t.replace("ò", "o").replace("ó", "o").replace("ō", "o:")
    t = t.replace("ù", "u").replace("ú", "u").replace("ū", "u:")
    t = t.replace("ţ", "T").replace("ţţ", "TT").replace("Ţ", "T")
    t = t.replace("ŗ", "R").replace("ř", "R").replace("ṛ", "R")
    t = t.replace("ḍ", "D").replace("ṭ", "T").replace("ṇ", "N").replace("ṣ", "sh").replace("ś", "sh")
    t = t.replace("ñ", "ny").replace("ŋ", "ng")

    V_MAP = {
        'a:': 'ा', 'aa': 'ा',
        'i:': 'ी', 'ii': 'ी',
        'u:': 'ू', 'uu': 'ू',
        'e:': 'े', 'ee': 'े',
        'o:': 'ो', 'oo': 'ो',
        'ai': 'ै', 'au': 'ौ',
        'a': '', 'i': 'ि', 'u': 'ु', 'e': 'े', 'o': 'ो'
    }
    V_INIT = {
        'a:': 'आ', 'aa': 'आ',
        'i:': 'ई', 'ii': 'ई',
        'u:': 'ऊ', 'uu': 'ऊ',
        'e:': 'ए', 'ee': 'ए',
        'o:': 'ओ', 'oo': 'ओ',
        'ai': 'ऐ', 'au': 'औ',
        'a': 'अ', 'i': 'इ', 'u': 'उ', 'e': 'ए', 'o': 'ओ'
    }
    C_MAP = [
        ('kh', 'ख'), ('gh', 'घ'), ('ch', 'छ'), ('jh', 'झ'),
        ('Th', 'ठ'), ('Dh', 'ढ'), ('th', 'थ'), ('dh', 'ध'),
        ('ph', 'फ'), ('bh', 'भ'), ('sh', 'श'), ('Rh', 'ढ़'),
        ('k', 'क'), ('g', 'ग'), ('c', 'च'), ('j', 'ज'),
        ('T', 'ट'), ('D', 'ड'), ('N', 'ण'), ('t', 'त'),
        ('d', 'द'), ('n', 'न'), ('p', 'प'), ('b', 'ब'),
        ('m', 'म'), ('y', 'य'), ('r', 'र'), ('l', 'ल'),
        ('v', 'व'), ('w', 'व'), ('s', 'स'), ('h', 'ह'),
        ('R', 'ड़'), ('f', 'फ'), ('z', 'ज़')
    ]

    tokens = re.findall(r'(kh|gh|ch|jh|Th|Dh|th|dh|ph|bh|sh|Rh|[kgcjTDNtdnpbmyrlvwshRfz]|[aA]:|[iI]:|[uU]:|[eE]:|[oO]:|ai|au|[aiueoAIUEO]|.)', t)
    
    out = []
    is_start = True
    prev_was_c = False

    for tok in tokens:
        tok_low = tok.lower()
        if tok in [c[0] for c in C_MAP] or tok_low in [c[0] for c in C_MAP]:
            c_char = next(c[1] for c in C_MAP if c[0] == tok or c[0] == tok_low)
            if prev_was_c:
                out.append('्')
            out.append(c_char)
            prev_was_c = True
            is_start = False
        elif tok_low in V_MAP:
            if is_start or not prev_was_c:
                out.append(V_INIT[tok_low])
            else:
                out.append(V_MAP[tok_low])
            prev_was_c = False
            is_start = False
        elif tok in [' ', '-', '_']:
            out.append(tok)
            prev_was_c = False
            is_start = True
        elif tok in ['~', '̃']:
            out.append('ँ')
        else:
            out.append(tok)
            prev_was_c = False
            is_start = False

    res = "".join(out)
    return res

if __name__ == "__main__":
    test_words = ["biar", "dhodu", "badalu", "hi:th", "nhe:ra", "gobru", "lada", "ladi", "bhenu", "pakru", "ãkhri ghuadna", "ghĩu ra diya", "pũnniya", "bale bale kane"]
    for w in test_words:
        print(f"  {w:22s} -> {roman_to_devanagari(w)}")
