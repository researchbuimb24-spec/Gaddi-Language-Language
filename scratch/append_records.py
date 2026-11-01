# Append cardinals, ordinals, kinship, and cultural terms

# --- 4. CARDINALS (Table 4, p. 249-250) ---
cardinals_data = [
    ("अकि", "akɨ", "akɨ", "one (cardinal numeral 1)", "एक (१)", "ایک (۱)", 1, "Table 4, p. 249"),
    ("दोय", "doːj", "doːj", "two (cardinal numeral 2)", "दो (२)", "دو (۲)", 2, "Table 4, p. 249"),
    ("त्रै", "trai", "trai", "three (cardinal numeral 3)", "तीन (३)", "تین (۳)", 3, "Table 4, p. 249"),
    ("चोर", "tʃoːr", "tʃoːr", "four (cardinal numeral 4)", "चार (४)", "چار (۴)", 4, "Table 4, p. 249"),
    ("पंजी", "pandʒi", "pandʒi", "five (cardinal numeral 5)", "पाँच (५)", "پانچ (۵)", 5, "Table 4, p. 249"),
    ("चे", "tʃeː", "tʃeː", "six (cardinal numeral 6)", "छह (६)", "چھ (۶)", 6, "Table 4, p. 249"),
    ("सति", "satɨ", "satɨ", "seven (cardinal numeral 7)", "सात (७)", "سات (۷)", 7, "Table 4, p. 249"),
    ("अठि", "aʈʰɨ", "aʈʰɨ", "eight (cardinal numeral 8)", "आठ (८)", "آٹھ (۸)", 8, "Table 4, p. 249"),
    ("नव", "nav", "nav", "nine (cardinal numeral 9)", "नौ (९)", "نو (۹)", 9, "Table 4, p. 249"),
    ("दश", "daʃ", "daʃ", "ten (cardinal numeral 10)", "दस (१०)", "دس (۱۰)", 10, "Table 4, p. 249"),
    ("ग्यारा", "ɡʲaːra", "ɡʲaːra", "eleven (cardinal numeral 11)", "ग्यारह (११)", "گیارہ (۱۱)", 11, "Table 4, p. 249"),
    ("बारा", "baːraː", "baːraː", "twelve (cardinal numeral 12)", "बारह (१२)", "بارہ (۱۲)", 12, "Table 4, p. 249"),
    ("तेरा", "teːraː", "teːraː", "thirteen (cardinal numeral 13)", "तेरह (१३)", "تیرہ (۱۳)", 13, "Table 4, p. 249"),
    ("चौदा", "tʃowda", "tʃowda", "fourteen (cardinal numeral 14)", "चौदह (१४)", "چودہ (۱۴)", 14, "Table 4, p. 249"),
    ("पन्द्रा", "pandra", "pandra", "fifteen (cardinal numeral 15)", "पंद्रह (१५)", "پندرہ (۱۵)", 15, "Table 4, p. 249"),
    ("शोला", "ʃola", "ʃola", "sixteen (cardinal numeral 16)", "सोलह (१६)", "سولہ (۱۶)", 16, "Table 4, p. 249"),
    ("सतारा", "sataːra", "sataːra", "seventeen (cardinal numeral 17)", "सत्रह (१७)", "سترہ (۱۷)", 17, "Table 4, p. 250"),
    ("अठारा", "aʈʰara", "aʈʰara", "eighteen (cardinal numeral 18)", "अठारह (१८)", "اٹھارہ (۱۸)", 18, "Table 4, p. 250"),
    ("उनी", "uniː", "uniː", "nineteen (cardinal numeral 19)", "उन्नीस (१९)", "انیس (۱۹)", 19, "Table 4, p. 250"),
    ("बी", "biː", "biː", "twenty (cardinal numeral 20)", "बीस (२०)", "بیس (۲۰)", 20, "Table 4, p. 250"),
    ("चाली", "tʃaliː", "tʃaliː", "forty (cardinal numeral 40)", "चालीस (४०)", "چالیس (۴۰)", 40, "Table 4, p. 250"),
    ("पंजा", "pandʒa", "pandʒa", "fifty (cardinal numeral 50)", "पचास (५०)", "پچاس (۵۰)", 50, "Table 4, p. 250"),
    ("शौव", "ʃov", "ʃov", "hundred (cardinal numeral 100)", "सौ (१००)", "سو (۱۰۰)", 100, "Table 4, p. 250"),
    ("अख हज़ार", "akʰ azaːr", "akʰ azaːr", "one thousand (cardinal numeral 1000)", "एक हज़ार (१०००)", "ایک ہزار (۱۰۰۰)", 1000, "Table 4, p. 250"),
]

for dev, ipa, orig, en, hi, ur, val, tbl in cardinals_data:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": "numeral",
        "gender": None,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "numbers",
                "table": tbl,
                "context": f"Cardinal number {val} in Bhaderwah Gaddi."
            }
        ],
        "cats": ["numbers"],
        "comp_notes": f"Bhaderwah Gaddi cardinal form for {val}.",
        "numeric_value": val
    })

# --- 5. ORDINALS (Table 5, p. 250) ---
ordinals_data = [
    ("पहला", "pehla", "pehla", "first (ordinal 1st)", "पहला (१ला)", "پہلا (۱لا)", 1, "Table 5, p. 250"),
    ("दुवा", "duwa", "duwa", "second (ordinal 2nd)", "दूसरा (२रा)", "دوسرا (۲را)", 2, "Table 5, p. 250"),
    ("त्रिया", "trija", "trija", "third (ordinal 3rd)", "तीसरा (३रा)", "تیسرا (۳را)", 3, "Table 5, p. 250"),
    ("चोथा", "tʃotʰa", "tʃotʰa", "fourth (ordinal 4th)", "चौथा (४था)", "چوتھا (۴تھا)", 4, "Table 5, p. 250"),
    ("पंज्वा", "pandʒwa", "pandʒwa", "fifth (ordinal 5th)", "पाँचवाँ (५वाँ)", "پانچواں (۵واں)", 5, "Table 5, p. 250"),
    ("छठ्वा", "tʃʰaʈʰwa", "tʃʰaʈʰwa", "sixth (ordinal 6th)", "छठा (६ठा)", "چھٹا (۶ٹا)", 6, "Table 5, p. 250"),
    ("सतिवा", "satɨwa", "satɨwa", "seventh (ordinal 7th)", "सातवाँ (७वाँ)", "ساتواں (۷واں)", 7, "Table 5, p. 250"),
    ("अठिवा", "aʈʰɨwa", "aʈʰɨwa", "eighth (ordinal 8th)", "आठवाँ (८वाँ)", "آٹھواں (۸واں)", 8, "Table 5, p. 250"),
    ("नववा", "nawwa", "nawwa", "ninth (ordinal 9th)", "नौवाँ (९वाँ)", "نواں (۹واں)", 9, "Table 5, p. 250"),
    ("दशवा", "daʃwa", "daʃwa", "tenth (ordinal 10th)", "दसवाँ (१०वाँ)", "دسواں (۱۰واں)", 10, "Table 5, p. 250"),
    ("बींवा", "bĩːwa", "bĩːwa", "twentieth (ordinal 20th)", "बीसवाँ (२०वाँ)", "بیسواں (۲۰واں)", 20, "Table 5, p. 250"),
    ("पजामा", "padʒama", "padʒama", "fiftieth (ordinal 50th)", "पचासवाँ (५०वाँ)", "پچاسواں (۵۰واں)", 50, "Table 5, p. 250"),
    ("शौमा", "ʃawma", "ʃawma", "hundredth (ordinal 100th)", "सौवाँ (१००वाँ)", "سوواں (۱۰۰واں)", 100, "Table 5, p. 250"),
]

for dev, ipa, orig, en, hi, ur, val, tbl in ordinals_data:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": "adjective",
        "gender": "masculine",
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "numbers",
                "table": tbl,
                "context": f"Ordinal numeral suffixing -wa/-ma for {val} in Bhaderwah Gaddi."
            }
        ],
        "cats": ["numbers"],
        "comp_notes": f"Bhaderwah Gaddi ordinal form for {val}.",
        "numeric_value": val
    })

# --- 6. KINSHIP TERMINOLOGY (Tables 6–13, pp. 252–255) ---

# बाजी (baːjiː) - Own Generation Male Relatives (Table 6, Table 12)
raw_records.append({
    "lemma_dev": "बाजी",
    "ipa": "baːjiː",
    "orig": "baːjiː",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Brother (elder or younger brother: B, B(e/y)); male sibling in own generation (G0). Addresser: Brother or Sister (B/Z).",
            "hi": "भाई (बड़ा या छोटा भाई: B); समकालीन पीढ़ी (G0) में सहोदर भाई। संबोधनकर्ता: भाई या बहन (B/Z)।",
            "ur": "بھائی (بڑا یا چھوٹا بھائی)؛ اپنی نسل (G0) میں سگا بھائی۔ مخاطِب: بھائی یا بہن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "B/Z -> B(e/y) Brother (elder/younger), M, G0."
        },
        {
            "en": "Paternal male parallel cousin (Father's Brother's Son: FBS); male cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "चचेरा भाई (चाचा का बेटा: FBS); समकालीन पीढ़ी (G0) में पितृपक्षीय भाई। संबोधनकर्ता: चचेरा/चचेरी भाई/बहन (C)।",
            "ur": "چچیرا بھائی (چچا کا بیٹا)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> FBS Father’s Brother’s Son, M, G0."
        },
        {
            "en": "Paternal male cross cousin (Father's Sister's Son: FZS); male cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "फुफेरा भाई (बुआ का बेटा: FZS); समकालीन पीढ़ी (G0) में बुआ का पुत्र। संबोधनकर्ता: फुफेरा/फुफेरी भाई/बहन (C)।",
            "ur": "پھپھیرا بھائی (پھپھی کا بیٹا)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> FZS Father’s Sister’s Son, M, G0."
        },
        {
            "en": "Maternal male cross cousin (Mother's Brother's Son: MBS); male cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "ममेरा भाई (मामा का बेटा: MBS); समकालीन पीढ़ी (G0) में मामा का पुत्र। संबोधनकर्ता: ममेरा/ममेरी भाई/बहन (C)।",
            "ur": "ممیرا بھائی (ماموں کا بیٹا)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> MBS Mother’s Brother’s Son, M, G0."
        },
        {
            "en": "Maternal male parallel cousin (Mother's Sister's Son: MZS); male cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "मौसेरा भाई (मौसी का बेटा: MZS); समकालीन पीढ़ी (G0) में मौसी का पुत्र। संबोधनकर्ता: मौसेरा/मौसेरी भाई/बहन (C)।",
            "ur": "موسیرا بھائی (خالہ کا بیٹا)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> MZS Mother’s Sister’s Son, M, G0."
        },
        {
            "en": "Husband's Sister's Husband (HZH); affinal male relative in own generation (G0). Addresser: Wife (W).",
            "hi": "ननदोई (पति की बहन का पति: HZH); समकालीन पीढ़ी (G0) में वैवाहिक संबंधी। संबोधनकर्ता: पत्नी (W)।",
            "ur": "نندوئی (شوہر کی بہن کا شوہر)؛ اپنی نسل (G0) میں سسرالی رشتہ۔ مخاطِب: بیوی (W)۔",
            "field": "kinship",
            "table": "Table 12, p. 255",
            "context": "W -> HZH Husband’s Sister’s Husband, M, G0."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "Key Gaddi kinship structural feature: /ba:ji/ functions as universal umbrella term for brother and all male first cousins, as well as husband's sister's husband.",
    "kinship_algebra": {"generation": "G0", "addresser": "B/Z, C, W", "addressee": "B, FBS, FZS, MBS, MZS, HZH", "sex": "M"}
})

# दद्दा (daddaː) - Own Generation Female Relatives (Table 6, Table 12)
raw_records.append({
    "lemma_dev": "दद्दा",
    "ipa": "daddaː",
    "orig": "daddaː",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Sister (elder or younger sister: Z, Z(e/y)); female sibling in own generation (G0). Addresser: Brother or Sister (B/Z).",
            "hi": "बहन (बड़ी या छोटी बहन: Z); समकालीन पीढ़ी (G0) में सहोदरा बहन। संबोधनकर्ता: भाई या बहन (B/Z)।",
            "ur": "بہن (بڑی یا چھوٹی بہن)؛ اپنی نسل (G0) میں سگی بہن۔ مخاطِب: بھائی یا بہن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "B/Z -> Z(e/y) Sister (elder/younger), F, G0."
        },
        {
            "en": "Paternal female parallel cousin (Father's Brother's Daughter: FBD); female cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "चचेरी बहन (चाचा की बेटी: FBD); समकालीन पीढ़ी (G0) में पितृपक्षीय बहन। संबोधनकर्ता: चचेरा/चचेरी भाई/बहन (C)।",
            "ur": "چچیری بہن (چچا کی بیٹی)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> FBD Father’s Brother’s Daughter, F, G0."
        },
        {
            "en": "Paternal female cross cousin (Father's Sister's Daughter: FZD); female cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "फुफेरी बहन (बुआ की बेटी: FZD); समकालीन पीढ़ी (G0) में बुआ की पुत्री। संबोधनकर्ता: फुफेरा/फुफेरी भाई/बहन (C)।",
            "ur": "پھپھیری بہن (پھپھی کی بیٹی)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> FZD Father’s Sister’s Daughter, F, G0."
        },
        {
            "en": "Maternal female cross cousin (Mother's Brother's Daughter: MBD); female cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "ममेरी बहन (मामा की बेटी: MBD); समकालीन पीढ़ी (G0) में मामा की पुत्री। संबोधनकर्ता: ममेरा/ममेरी भाई/बहन (C)।",
            "ur": "ممیری بہن (ماموں کی بیٹی)؛ اپنی نسل (G0) में کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> MBD Mother’s Brother’s Daughter, F, G0."
        },
        {
            "en": "Maternal female parallel cousin (Mother's Sister's Daughter: MZD); female cousin in own generation (G0). Addresser: Cousin (C(M/F)).",
            "hi": "मौसेरी बहन (मौसी की बेटी: MZD); समकालीन पीढ़ी (G0) में मौसी की पुत्री। संबोधनकर्ता: मौसेरा/मौसेरी भाई/बहन (C)।",
            "ur": "موسیری بہن (خالہ کی بیٹی)؛ اپنی نسل (G0) میں کزن۔ مخاطِب: کزن۔",
            "field": "kinship",
            "table": "Table 6, p. 252",
            "context": "C(M/F) -> MZD Mother’s Sister’s Daughter, F, G0."
        },
        {
            "en": "Wife's Brother's Wife (WBW); affinal female relative in own generation (G0). Addresser: Husband (H).",
            "hi": "सलहज (पत्नी के भाई की पत्नी: WBW); समकालीन पीढ़ी (G0) में वैवाहिक संबंधी। संबोधनकर्ता: पति (H)।",
            "ur": "سلہج (بیوی کے بھائی کی بیوی)؛ اپنی نسل (G0) میں سسرالی رشتہ۔ مخاطِب: شوہر (H)۔",
            "field": "kinship",
            "table": "Table 12, p. 255",
            "context": "H -> WBW Wife’s Brother’s Wife, F, G0."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "Key Gaddi kinship structural feature: /dadda:/ functions as universal umbrella term for sister and all female first cousins, as well as wife's brother's wife.",
    "kinship_algebra": {"generation": "G0", "addresser": "B/Z, C, H", "addressee": "Z, FBD, FZD, MBD, MZD, WBW", "sex": "F"}
})

# Partial-blood kinship (Table 7, p. 252)
partial_kin = [
    ("सोतेला बापू", "sotelaː baːpuː", "sotelaː baːpuː", "Step Father (XF, G+1, Sex: M); male step-parent. Addresser: Step-Son or Step-Daughter (S/D).", "सौतेला पिता (XF); समकालीन पीढ़ी से ऊपर (G+1)। संबोधनकर्ता: बेटा या बेटी (S/D)।", "سوتیلا باپ؛ سوتیلا والد۔ مخاطِب: بیٹا یا بیٹی۔", "noun", "masculine", "XF", "G+1", "S/D", "M", "Table 7, p. 252"),
    ("सोतेली अम्मा", "soteli amma", "soteli amma", "Step Mother (XM, G+1, Sex: F); female step-parent. Addresser: Step-Son or Step-Daughter (S/D).", "सौतेली माँ (XM); समकालीन पीढ़ी से ऊपर (G+1)। संबोधनकर्ता: बेटा या बेटी (S/D)।", "سوتیلی ماں؛ سوتیلی والدہ۔ مخاطِب: بیٹا یا بیٹی۔", "noun", "feminine", "XM", "G+1", "S/D", "F", "Table 7, p. 252"),
    ("सोतेला बाज", "sotela baːj", "sotela baːj", "Step Brother (XB, G0, Sex: M); male step-sibling. Addresser: Step-Sibling (C).", "सौतेला भाई (XB); समकालीन पीढ़ी (G0)। संबोधनकर्ता: भाई या बहन (C)।", "سوتیلا بھائی۔ مخاطِب: بھائی یا بہن۔", "noun", "masculine", "XB", "G0", "C", "M", "Table 7, p. 252"),
    ("सोतेली ददा", "soteliː dada", "soteliː dada", "Step Sister (XZ, G0, Sex: F); female step-sibling. Addresser: Step-Sibling (C).", "सौतेली बहन (XZ); समकालीन पीढ़ी (G0)। संबोधनकर्ता: भाई या बहन (C)।", "سوتیلی بہن۔ مخاطِب: بھائی یا بہن۔", "noun", "feminine", "XZ", "G0", "C", "F", "Table 7, p. 252"),
    ("सोतेली कोडे", "soteli koɖeː", "soteli koɖeː", "Step Daughter (XD, G-1, Sex: F); female child through spouse's previous marriage. Addresser: Step-Parent (C).", "सौतेली बेटी (XD); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: माता या पिता (C)।", "سوتیلی بیٹی۔ مخاطِب: سوتیلا والد یا والدہ۔", "noun", "feminine", "XD", "G-1", "C", "F", "Table 7, p. 252"),
    ("सोतेला गोगरू", "sotelaː ɡoɡruː", "sotelaː ɡoɡruː", "Step Son (XS, G-1, Sex: M); male child through spouse's previous marriage. Addresser: Step-Parent (S/C).", "सौतेला बेटा (XS); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: माता या पिता (S/C)।", "سوتیلا بیٹا / سوتیلا پتر۔ مخاطِب: سوتیلا والد یا والدہ۔", "noun", "masculine", "XS", "G-1", "S", "M", "Table 7, p. 252"),
]

for dev, ipa, orig, en, hi, ur, pos, gen, rel, gen_lvl, addr, sex, tbl in partial_kin:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": pos,
        "gender": gen,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "kinship",
                "table": tbl,
                "context": f"Partial-blood relationship: {addr} -> {rel} ({gen_lvl}, {sex})."
            }
        ],
        "cats": ["people", "kinship"],
        "comp_notes": "Compound kinship term formed with modifier sotela / soteli.",
        "kinship_algebra": {"generation": gen_lvl, "addresser": addr, "addressee": rel, "relation_code": rel, "sex": sex}
    })

# First Ascending Generation (Table 8, p. 253)
asc_1_kin = [
    ("बापू", "baːpuː", "baːpuː", "Father (Fa, G+1, Sex: M); male biological parent. Addresser: Son or Daughter (S/D).", "पिता / बापू (Fa); प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: बेटा या बेटी (S/D)।", "باپ / والد (Fa)؛ پہلی بالائی نسل (G+1)۔ مخاطِب: بیٹا یا بیٹی۔", "noun", "masculine", "Fa", "G+1", "S/D", "M", "Table 8, p. 253"),
    ("चाचा", "tʃaːtʃaː", "tʃaːtʃaː", "Father's Brother (FB, paternal uncle, G+1, Sex: M). Addresser: Child (C).", "चाचा (FB); पिता का भाई, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भतीजा या भतीजी (C)।", "چچا (FB)؛ والد کا بھائی۔ مخاطِب: بھتیجا یا بھتیجی۔", "noun", "masculine", "FB", "G+1", "C", "M", "Table 8, p. 253"),
    ("चाची", "tʃaːtʃi", "tʃaːtʃi", "Father's Brother's Wife (FBW, paternal aunt, G+1, Sex: F). Addresser: Child (C).", "चाची (FBW); चाचा की पत्नी, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भतीजा या भतीजी (C)।", "چچی (FBW)؛ چچا کی بیوی۔ مخاطِب: بھتیجا یا بھتیجی۔", "noun", "feminine", "FBW", "G+1", "C", "F", "Table 8, p. 253"),
    ("बुब्बे", "bubbeː", "bubbeː", "Father's Sister (FZ, paternal aunt / bua, G+1, Sex: F). Addresser: Child (C).", "बुआ / बुब्बे (FZ); पिता की बहन, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भतीजा या भतीजी (C)।", "پھپھی / پھوپھو (FZ)؛ والد کی بہن۔ مخاطِب: بھتیجا یا بھتیجی۔", "noun", "feminine", "FZ", "G+1", "C", "F", "Table 8, p. 253"),
    ("बुब्बा", "bubbaː", "bubbaː", "Father's Sister's Husband (FZH / fufa, G+1, Sex: M). Addresser: Child (C).", "फूफा / बुब्बा (FZH); बुआ का पति, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भतीजा या भतीजी (C)।", "پھوپھا (FZH)؛ پھپھی کا شوہر۔ مخاطِب: بھتیجا یا بھتیجی۔", "noun", "masculine", "FZH", "G+1", "C", "M", "Table 8, p. 253"),
    ("अम्मा", "ammaː", "ammaː", "Mother (Mo, G+1, Sex: F); female biological parent. Addresser: Son or Daughter (S/D).", "माँ / अम्मा (Mo); प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: बेटा या बेटी (S/D)।", "ماں / والدہ (Mo)؛ پہلی بالائی نسل (G+1)۔ مخاطِب: بیٹا یا بیٹی۔", "noun", "feminine", "Mo", "G+1", "S/D", "F", "Table 8, p. 253"),
    ("माम", "maːm", "maːm", "Mother's Brother (MB, maternal uncle / mama, G+1, Sex: M). Addresser: Child (C).", "मामा / माम (MB); माँ का भाई, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भांजा या भांजी (C)।", "ماموں (MB)؛ والدہ کا بھائی۔ مخاطِب: بھانجا یا بھانجی۔", "noun", "masculine", "MB", "G+1", "C", "M", "Table 8, p. 253"),
    ("मामी", "maːmiː", "maːmiː", "Mother's Brother's Wife (MBW, maternal aunt / mami, G+1, Sex: F). Addresser: Child (C).", "मामी (MBW); मामा की पत्नी, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भांजा या भांजी (C)।", "ممانی (MBW)؛ ماموں کی بیوی۔ مخاطِب: بھانجا یا بھانجی۔", "noun", "feminine", "MBW", "G+1", "C", "F", "Table 8, p. 253"),
    ("मासी", "maːsiː", "maːsiː", "Mother's Sister (MZ, maternal aunt / masi, G+1, Sex: F). Addresser: Child (C).", "मौसी (MZ); माँ की बहन, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भांजा या भांजी (C)।", "خالہ / ماسی (MZ)؛ والدہ کی بہن۔ مخاطِب: بھانجا یا بھانجی۔", "noun", "feminine", "MZ", "G+1", "C", "F", "Table 8, p. 253"),
    ("मोसाजी", "mosajiː", "mosajiː", "Mother's Sister's Husband (MZH / mausa, G+1, Sex: M). Addresser: Child (C).", "मौसा / मोसाजी (MZH); मौसी का पति, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: भांजा या भांजी (C)।", "خالو / موساجی (MZH)؛ خالہ کا شوہر۔ مخاطِب: بھانجا یا بھانجی۔", "noun", "masculine", "MZH", "G+1", "C", "M", "Table 8, p. 253"),
]

for dev, ipa, orig, en, hi, ur, pos, gen, rel, gen_lvl, addr, sex, tbl in asc_1_kin:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": pos,
        "gender": gen,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "kinship",
                "table": tbl,
                "context": f"First ascending generation kinship: {addr} -> {rel} ({gen_lvl}, {sex})."
            }
        ],
        "cats": ["people", "kinship"],
        "comp_notes": f"Primary Gaddi kinship term for {rel}.",
        "kinship_algebra": {"generation": gen_lvl, "addresser": addr, "addressee": rel, "relation_code": rel, "sex": sex}
    })

# Second Ascending Generation (Table 9, p. 253)
raw_records.append({
    "lemma_dev": "दादा",
    "ipa": "daːdaː",
    "orig": "daːdaː",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Father's Father (FF, paternal grandfather, G+2, Sex: M). Addresser: Grandchild (C).",
            "hi": "दादा (FF); पिता के पिता, द्वितीय आरोही पीढ़ी (G+2)। संबोधनकर्ता: पोता या पोती (C)।",
            "ur": "دادا (FF)؛ والد کے والد۔ مخاطِب: پوتا یا پوتی۔",
            "field": "kinship",
            "table": "Table 9, p. 253",
            "context": "C -> FF Father’s father, M, G+2."
        },
        {
            "en": "Mother's Father (MF, maternal grandfather, G+2, Sex: M). Addresser: Grandchild (C).",
            "hi": "नाना / दादा (MF); माँ के पिता, द्वितीय आरोही पीढ़ी (G+2)। संबोधनकर्ता: नाती या नातिन (C)।",
            "ur": "نانا (MF)؛ والدہ کے والد۔ مخاطِب: نواسا یا نواسی۔",
            "field": "kinship",
            "table": "Table 9, p. 253",
            "context": "C -> MF Mother’s father, M, G+2."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /da:da:/ merges both paternal and maternal grandfathers (FF and MF).",
    "kinship_algebra": {"generation": "G+2", "addresser": "C", "addressee": "FF, MF", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "दादी",
    "ipa": "daːdiː",
    "orig": "daːdiː",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Father's Mother (FM, paternal grandmother, G+2, Sex: F). Addresser: Grandchild (C).",
            "hi": "दादी (FM); पिता की माँ, द्वितीय आरोही पीढ़ी (G+2)। संबोधनकर्ता: पोता या पोती (C)।",
            "ur": "دادی (FM)؛ والد کی والدہ۔ مخاطِب: پوتا یا پوتی۔",
            "field": "kinship",
            "table": "Table 9, p. 253",
            "context": "C -> FM Father’s mother, F, G+2."
        },
        {
            "en": "Mother's Mother (MM, maternal grandmother, G+2, Sex: F). Addresser: Grandchild (C).",
            "hi": "नानी / दादी (MM); माँ की माँ, द्वितीय आरोही पीढ़ी (G+2)। संबोधनकर्ता: नाती या नातिन (C)।",
            "ur": "نانی (MM)؛ والدہ کی والدہ۔ مخاطِب: نواسا یا نواسی۔",
            "field": "kinship",
            "table": "Table 9, p. 253",
            "context": "C -> MM Mother’s mother, F, G+2."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /da:di:/ merges both paternal and maternal grandmothers (FM and MM).",
    "kinship_algebra": {"generation": "G+2", "addresser": "C", "addressee": "FM, MM", "sex": "F"}
})

# First Descending Generation (Table 10, p. 254)
raw_records.append({
    "lemma_dev": "गगरू",
    "ipa": "ɡaɡruː",
    "orig": "ɡaɡruː",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Son (S, G-1, Sex: M); male biological offspring. Addresser: Father or Mother (Fa/Mo).",
            "hi": "बेटा / पुत्र (S); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: पिता या माँ (Fa/Mo)।",
            "ur": "بیٹا / فرزند (S)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: والد یا والدہ۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "Fa/Mo -> S Son, M, G-1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "Gaddi specific descendant term gagru / gogru.",
    "kinship_algebra": {"generation": "G-1", "addresser": "Fa/Mo", "addressee": "S", "relation_code": "S", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "कोडे",
    "ipa": "koɖeː",
    "orig": "koɖeː",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Daughter (D, G-1, Sex: F); female biological offspring. Addresser: Father or Mother (Fa/Mo).",
            "hi": "बेटी / पुत्री / कन्या (D); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: पिता या माँ (Fa/Mo)।",
            "ur": "بیٹی / دختر (D)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: والد یا والدہ۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "Fa/Mo -> D Daughter, F, G-1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "Gaddi specific descendant term kode / kudi.",
    "kinship_algebra": {"generation": "G-1", "addresser": "Fa/Mo", "addressee": "D", "relation_code": "D", "sex": "F"}
})

raw_records.append({
    "lemma_dev": "भांज",
    "ipa": "bʰaːndʒ",
    "orig": "bʰaːndʒ",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Brother's Son (BS, nephew, G-1, Sex: M). Addresser: Uncle or Aunt (C).",
            "hi": "भतीजा (भाई का बेटा: BS); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: चाचा/ताऊ/बुआ (C)।",
            "ur": "بھتیجا (بھائی کا بیٹا)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: چچا یا پھپھی۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "C -> BS Brother’s Son, M, G-1."
        },
        {
            "en": "Sister's Son (ZS, nephew, G-1, Sex: M). Addresser: Uncle or Aunt (C).",
            "hi": "भांजा (बहन का बेटा: ZS); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: मामा या मौसी (C)।",
            "ur": "بھانجا (بہن کا بیٹا)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: ماموں یا خالہ۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "C -> ZS Sister’s Son, M, G-1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /bha:ndz/ covers both brother's son (BS) and sister's son (ZS).",
    "kinship_algebra": {"generation": "G-1", "addresser": "C", "addressee": "BS, ZS", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "भांजी",
    "ipa": "bʰaːndʒi",
    "orig": "bʰaːndʒi",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Brother's Daughter (BD, niece, G-1, Sex: F). Addresser: Uncle or Aunt (C).",
            "hi": "भतीजी (भाई की बेटी: BD); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: चाचा/ताऊ/बुआ (C)।",
            "ur": "بھتیجی (بھائی کی بیٹی)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: چچا یا پھپھی۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "C -> BD Brother’s Daughter, F, G-1."
        },
        {
            "en": "Sister's Daughter (ZD, niece, G-1, Sex: F). Addresser: Uncle or Aunt (C).",
            "hi": "भांजी (बहन की बेटी: ZD); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: मामा या मौसी (C)।",
            "ur": "بھانجی (بہن کی بیٹی)؛ پہلی زیریں نسل (G-1)۔ مخاطِب: ماموں یا خالہ۔",
            "field": "kinship",
            "table": "Table 10, p. 254",
            "context": "C -> ZD Sister’s Daughter, F, G-1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /bha:ndzi/ covers both brother's daughter (BD) and sister's daughter (ZD).",
    "kinship_algebra": {"generation": "G-1", "addresser": "C", "addressee": "BD, ZD", "sex": "F"}
})

# Second Descending Generation (Table 11, p. 254)
raw_records.append({
    "lemma_dev": "पोत्रू",
    "ipa": "potruː",
    "orig": "potruː",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Son's Son (SS, grandson, G-2, Sex: M). Addresser: Grandparent (C).",
            "hi": "पोता (बेटे का बेटा: SS); द्वितीय अवरोही पीढ़ी (G-2)। संबोधनकर्ता: दादा या दादी (C)।",
            "ur": "پوتا (بیٹے کا بیٹا)؛ دوسری زیریں نسل (G-2)۔ مخاطِب: دادا یا دادی۔",
            "field": "kinship",
            "table": "Table 11, p. 254",
            "context": "C -> SS Son’s son, M, G-2."
        },
        {
            "en": "Daughter's Son (DS, maternal grandson, G-2, Sex: M). Addresser: Grandparent (C).",
            "hi": "नाती / नवासा (बेटी का बेटा: DS); द्वितीय अवरोही पीढ़ी (G-2)। संबोधनकर्ता: नाना या नानी (C)।",
            "ur": "نواسا (بیٹی کا بیٹا)؛ دوسری زیریں نسل (G-2)۔ مخاطِب: نانا یا نانی۔",
            "field": "kinship",
            "table": "Table 11, p. 254",
            "context": "C -> DS daughter’s son, M, G-2."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /potru:/ covers both son's son (SS) and daughter's son (DS).",
    "kinship_algebra": {"generation": "G-2", "addresser": "C", "addressee": "SS, DS", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "पोत्री",
    "ipa": "potri",
    "orig": "potri",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Son's Daughter (SD, granddaughter, G-2, Sex: F). Addresser: Grandparent (C).",
            "hi": "पोती (बेटे की बेटी: SD); द्वितीय अवरोही पीढ़ी (G-2)। संबोधनकर्ता: दादा या दादी (C)।",
            "ur": "پوتی (بیٹے کی بیٹی)؛ دوسری زیریں نسل (G-2)۔ مخاطِب: دادا یا دادی۔",
            "field": "kinship",
            "table": "Table 11, p. 254",
            "context": "C -> SD Son’s daughter, F, G-2."
        },
        {
            "en": "Daughter's Daughter (DD, maternal granddaughter, G-2, Sex: F). Addresser: Grandparent (C).",
            "hi": "नातिन / नवासी (बेटी की बेटी: DD); द्वितीय अवरोही पीढ़ी (G-2)। संबोधनकर्ता: नाना या नानी (C)।",
            "ur": "نواسی (بیٹی کی بیٹی)؛ دوسری زیریں نسل (G-2)۔ مخاطِب: نانا یا نانی۔",
            "field": "kinship",
            "table": "Table 11, p. 254",
            "context": "C -> DD Daughter’s daughter, F, G-2."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /potri/ covers both son's daughter (SD) and daughter's daughter (DD).",
    "kinship_algebra": {"generation": "G-2", "addresser": "C", "addressee": "SD, DD", "sex": "F"}
})

# Affinal Relationships (Table 12, pp. 254-255)
raw_records.append({
    "lemma_dev": "लाड़ा",
    "ipa": "laːɖaː",
    "orig": "laːɖaː",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Husband (H, G0, Sex: M); male marital spouse. Addresser: Wife (W).",
            "hi": "पति / दूल्हा (H); समकालीन पीढ़ी (G0)। संबोधनकर्ता: पत्नी (W)।",
            "ur": "شوہر / خاوند (H)؛ اپنی نسل (G0)۔ مخاطِب: بیوی (W)۔",
            "field": "kinship",
            "table": "Table 12, p. 254",
            "context": "W -> H Husband, M, G0."
        },
        {
            "en": "Son-in-law (SL, G-1, Sex: M); daughter's husband. Addresser: Parents-in-law (C).",
            "hi": "दामाद (SL); पुत्री का पति, प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: सास या ससुर (C)।",
            "ur": "داماد (SL)؛ بیٹی کا شوہر۔ مخاطِب: ساس یا سسر۔",
            "field": "kinship",
            "table": "Table 12, p. 255",
            "context": "C -> SL Son-in-law, M, G-1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /la:da:/ designates both bridegroom/husband and daughter's husband (son-in-law).",
    "kinship_algebra": {"generation": "G0 / G-1", "addresser": "W, C", "addressee": "H, SL", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "शौवरा",
    "ipa": "ʃovra",
    "orig": "ʃovra",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Husband's Father (HF, father-in-law, G+1, Sex: M). Addresser: Wife (W).",
            "hi": "ससुर (HF); पति का पिता, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: पत्नी (W)।",
            "ur": "سسر (HF)؛ شوہر کا والد۔ مخاطِب: بیوی (W)۔",
            "field": "kinship",
            "table": "Table 12, p. 254",
            "context": "W -> HF Husband’s Father, M, G+1."
        },
        {
            "en": "Wife's Father (WF, father-in-law, G+1, Sex: M). Addresser: Husband (H).",
            "hi": "ससुर (WF); पत्नी का पिता, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: पति (H)।",
            "ur": "سسر (WF)؛ بیوی کا والد۔ مخاطِب: شوہر (H)۔",
            "field": "kinship",
            "table": "Table 12, p. 255",
            "context": "H -> WF Wife’s Father, M, G+1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /shovra/ designates father-in-law from both wife's and husband's perspective.",
    "kinship_algebra": {"generation": "G+1", "addresser": "W, H", "addressee": "HF, WF", "sex": "M"}
})

raw_records.append({
    "lemma_dev": "शशू",
    "ipa": "ʃaʃuː",
    "orig": "ʃaʃuː",
    "pos": "noun",
    "gender": "feminine",
    "senses": [
        {
            "en": "Husband's Mother (HM, mother-in-law, G+1, Sex: F). Addresser: Wife (W).",
            "hi": "सास (HM); पति की माँ, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: पत्नी (W)।",
            "ur": "ساس (HM)؛ شوہر کی والدہ۔ مخاطِب: بیوی (W)۔",
            "field": "kinship",
            "table": "Table 12, p. 254",
            "context": "W -> HM Husband’s Mother, F, G+1."
        },
        {
            "en": "Wife's Mother (WM, mother-in-law, G+1, Sex: F). Addresser: Husband (H).",
            "hi": "सास (WM); पत्नी की माँ, प्रथम आरोही पीढ़ी (G+1)। संबोधनकर्ता: पति (H)।",
            "ur": "ساس (WM)؛ بیوی کی والدہ۔ مخاطِب: شوہر (H)۔",
            "field": "kinship",
            "table": "Table 12, p. 255",
            "context": "H -> WM Wife’s Mother, F, G+1."
        }
    ],
    "cats": ["people", "kinship"],
    "comp_notes": "In Gaddi, /shashu:/ designates mother-in-law from both wife's and husband's perspective.",
    "kinship_algebra": {"generation": "G+1", "addresser": "W, H", "addressee": "HM, WM", "sex": "F"}
})

other_affinal = [
    ("देवर", "deːwar", "deːwar", "Husband's Younger Brother (HBy, G0, Sex: M). Addresser: Wife (W).", "देवर (HBy); पति का छोटा भाई, समकालीन पीढ़ी (G0)। संबोधनकर्ता: भाभी / पत्नी (W)।", "دیور (HBy)؛ شوہر کا چھوٹا بھائی۔ مخاطِب: بھابھی (W)۔", "noun", "masculine", "HBy", "G0", "W", "M", "Table 12, p. 254"),
    ("जठान", "dʒəʈʰaːn", "dʒəʈʰaːn", "Husband's Elder Brother's Wife (HBWe, G0, Sex: F). Addresser: Wife (W).", "जेठानी / जठान (HBWe); जेठ की पत्नी, समकालीन पीढ़ी (G0)। संबोधनकर्ता: देवरानी (W)।", "جٹھانی (HBWe)؛ جیٹھ کی بیوی۔ مخاطِب: دیورانی (W)۔", "noun", "feminine", "HBWe", "G0", "W", "F", "Table 12, p. 254"),
    ("देवराँ", "dewraːn", "dewraːn", "Husband's Younger Brother's Wife (HBWy, G0, Sex: F). Addresser: Wife (W).", "देवरानी / देवराँ (HBWy); देवर की पत्नी, समकालीन पीढ़ी (G0)। संबोधनकर्ता: जेठानी (W)।", "دیورانی (HBWy)؛ دیور کی بیوی۔ مخاطِب: جٹھانی (W)۔", "noun", "feminine", "HBWy", "G0", "W", "F", "Table 12, p. 254"),
    ("नन्द", "nand", "nand", "Husband's Sister (HZ, sister-in-law, G0, Sex: F). Addresser: Wife (W).", "ननद (HZ); पति की बहन, समकालीन पीढ़ी (G0)। संबोधनकर्ता: भाभी (W)।", "نند (HZ)؛ شوہر کی بہن۔ مخاطِب: بھابھی (W)۔", "noun", "feminine", "HZ", "G0", "W", "F", "Table 12, p. 255"),
    ("त्रिन्ति", "trintɨ", "trintɨ", "Wife (W, G0, Sex: F); female marital partner / householder. Addresser: Husband (H).", "पत्नी / घरवाली (W); समकालीन पीढ़ी (G0)। संबोधनकर्ता: पति (H)।", "بیوی / گھر والی (W)؛ اپنی نسل (G0)۔ مخاطِب: شوہر (H)۔", "noun", "feminine", "W", "G0", "H", "F", "Table 12, p. 255"),
    ("लाड़े", "laːɖe", "laːɖe", "Wife (W, G0, Sex: F); bride / female marital spouse. Addresser: Husband (H).", "पत्नी / दुल्हन / वधू (W); समकालीन पीढ़ी (G0)। संबोधनकर्ता: पति (H)।", "بیوی / دلہن (W)؛ اپنی نسل (G0)۔ مخاطِب: شوہر (H)۔", "noun", "feminine", "W", "G0", "H", "F", "Table 12, p. 255"),
    ("साला", "saːlaː", "saːlaː", "Wife's Brother (WB, brother-in-law, G0, Sex: M). Addresser: Husband (H).", "साला (WB); पत्नी का भाई, समकालीन पीढ़ी (G0)। संबोधनकर्ता: जीजा (H)।", "سالا (WB)؛ بیوی کا بھائی۔ مخاطِب: بہنوئی (H)۔", "noun", "masculine", "WB", "G0", "H", "M", "Table 12, p. 255"),
    ("साली", "sa:li:", "sa:li:", "Wife's Sister (WZ, sister-in-law, G0, Sex: F). Addresser: Husband (H).", "साली (WZ); पत्नी की बहन, समकालीन पीढ़ी (G0)। संबोधनकर्ता: जीजा (H)।", "سالی (WZ)؛ بیوی کی بہن۔ مخاطِب: بہنوئی (H)۔", "noun", "feminine", "WZ", "G0", "H", "F", "Table 12, p. 255"),
    ("सड़िबाइज", "saɖɨbaːj", "saɖɨbaːj", "Wife's Sister's Husband (WZH, co-brother-in-law / sadhu bhai, G0, Sex: M). Addresser: Husband (H).", "साढ़ू भाई (WZH); पत्नी की बहन का पति, समकालीन पीढ़ी (G0)। संबोधनकर्ता: साढ़ू भाई (H)।", "ہم زلف / ساڑھو بھائی (WZH)؛ بیوی کی بہن کا شوہر۔ مخاطِب: ہم زلف (H)۔", "noun", "masculine", "WZH", "G0", "H", "M", "Table 12, p. 255"),
    ("नुश", "nuʃ", "nuʃ", "Daughter-in-law (DL, G-1, Sex: F); son's wife. Addresser: Parents-in-law (C).", "बहू / पुत्रवधू (DL); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: सास या ससुर (C)।", "بہو (DL)؛ بیٹے کی بیوی۔ مخاطِب: ساس یا سسر۔", "noun", "feminine", "DL", "G-1", "C", "F", "Table 12, p. 255"),
]

for dev, ipa, orig, en, hi, ur, pos, gen, rel, gen_lvl, addr, sex, tbl in other_affinal:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": pos,
        "gender": gen,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "kinship",
                "table": tbl,
                "context": f"Affinal relationship: {addr} -> {rel} ({gen_lvl}, {sex})."
            }
        ],
        "cats": ["people", "kinship"],
        "comp_notes": f"Affinal kinship term for {rel}.",
        "kinship_algebra": {"generation": gen_lvl, "addresser": addr, "addressee": rel, "relation_code": rel, "sex": sex}
    })

# Kinship by Adoption (Table 13, p. 255)
adoptive_kin = [
    ("खोखलेरू गगरू", "kʰokʰaleruː ɡaɡru", "kʰokʰaleruː ɡaɡru", "Adopted Son (AS, G-1, Sex: M); child adopted through community custom. Addresser: Adoptive Parent (C).", "दत्तक पुत्र / गोद लिया बेटा (AS); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: माता या पिता (C)।", "لے پالک بیٹا / متبنیٰ (AS)۔ مخاطِب: گود لینے والے والدین۔", "noun", "masculine", "AS", "G-1", "C", "M", "Table 13, p. 255"),
    ("खोखलेरू कोडे", "kʰokʰaleruː koɖeː", "kʰokʰaleruː koɖeː", "Adopted Daughter (AD, G-1, Sex: F); female child adopted through community custom. Addresser: Adoptive Parent (C).", "दत्तक पुत्री / गोद ली बेटी (AD); प्रथम अवरोही पीढ़ी (G-1)। संबोधनकर्ता: माता या पिता (C)।", "لے پالک بیٹی (AD)۔ مخاطِب: گود لینے والے والدین۔", "noun", "feminine", "AD", "G-1", "C", "F", "Table 13, p. 255"),
]

for dev, ipa, orig, en, hi, ur, pos, gen, rel, gen_lvl, addr, sex, tbl in adoptive_kin:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": pos,
        "gender": gen,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "kinship",
                "table": tbl,
                "context": f"Adoptive relationship: {addr} -> {rel} ({gen_lvl}, {sex})."
            }
        ],
        "cats": ["people", "kinship"],
        "comp_notes": "Adoptive kinship compound with khokhaleru.",
        "kinship_algebra": {"generation": gen_lvl, "addresser": addr, "addressee": rel, "relation_code": rel, "sex": sex}
    })

# --- 7. ETHNONYMS AND CULTURAL REALIA (pp. 246–247) ---
ethno_terms = [
    ("घदेशी", "ɡʰəɖeːʃiː", "Ghadeshi", "Gaddi people / folk from the country of shepherds; local endonym used in Bhaderwah.", "घदेशी (चरवाहों के देश के लोग); भद्रवाह में गद्दी समुदाय के लिए प्रयुक्त स्थानीय नाम।", "گھدیشی؛ چرواہوں کے ملک کے لوگ، بھدرواہ میں گدی لوگوں کا مقامی نام۔", "noun", "masculine", ["people", "culture"], "Section 2. Background, p. 246", "Locally called by the name Ghadeshi which means 'the people from the country of shepherds'."),
    ("गद्दर", "ɡəddər", "Gaddar", "Sheep; Sanskrit etymological root of the tribal name Gaddi.", "गद्दर (भेड़); गद्दी शब्द का संस्कृत व्युत्पत्तिपरक मूल शब्द।", "گدر (بھیڑ)؛ لفظ گدی کا سنسکرت ماخذ۔", "noun", "masculine", ["animals", "culture"], "Section 2. Background, p. 246", "Derived from the Sanskrit word Gaddar which means sheep."),
    ("गद्दी", "ɡəddiː", "Gaddi", "Gaddi person / community member; shepherd; also sacred throne or seat of Lord Shiva.", "गद्दी; गद्दी समुदाय का व्यक्ति, चरवाहा; भगवान शिव का आसन।", "گدی؛ گدی قبیلے کا فرد، چرواہا، بھگوان شیو کا تخت / آسن۔", "noun", "masculine", ["people", "culture", "religion"], "Section 2. Background & Section 3. Religion, p. 246", "Self-claimed descendants and special disciples of Lord Shiva."),
    ("शिवरात्रि", "ʃɪv raːtri", "Shiv Ratri", "Shivratri; festival celebrating Lord Shiva, principal religious festival of Gaddi community.", "शिवरात्रि; भगवान शिव का मुख्य पर्व, भद्रवाह में गद्दी समुदाय का सर्वोच्च त्योहार।", "شیو راتری؛ بھگوان شیو کا بڑا تہوار، گدی برادری کا خاص مذہبی پرب۔", "noun", "feminine", ["culture", "religion"], "Section 3. Religion, p. 247", "Shiv Ratri is their main festival celebrated with communal harmony."),
]

for dev, ipa, orig, en, hi, ur, pos, gen, cats, tbl, ctx in ethno_terms:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": pos,
        "gender": gen,
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "culture",
                "table": tbl,
                "context": ctx
            }
        ],
        "cats": cats,
        "comp_notes": "Socio-cultural and religious term of Bhaderwah Gaddi.",
        "etymology": ctx
    })

print(f"Total raw records compiled: {len(raw_records)}")

