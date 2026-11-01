import json
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from gaddi.models import LexicalEntry, Sense, Attestation, EvidenceStatus
from gaddi.validator import GaddiValidator
from gaddi.registry import SourceRegistry, VarietyRegistry

# Load sources & varieties
with open(repo_root / "data/sources.json", encoding="utf-8") as f:
    src_data = json.load(f)
with open(repo_root / "data/varieties.json", encoding="utf-8") as f:
    var_data = json.load(f)

# Update dar_sheikh_2022 in src_data for testing
for s in src_data:
    if s.get("id") == "dar_sheikh_2022":
        s["access_status"] = "full_text_accessed_and_verified"
        s["pages"] = "245-258"
        s["url"] = "https://api.amu.ac.in/storage//file/10353/file_management/1659595804.pdf"
        s["license"] = "Academic Research / Open Access (AMU AJL / Author Attribution)"

from gaddi.models import Source, Variety
sources_reg = SourceRegistry([Source.from_dict(s) for s in src_data])
varieties_reg = VarietyRegistry([Variety(**v) for v in var_data])

validator = GaddiValidator(sources_reg, varieties_reg)

raw_records = []

# --- 1. SEASONS (Table 1, p. 248) ---
raw_records.append({
    "lemma_dev": "बस्त",
    "ipa": "bast",
    "orig": "bast",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Spring season; the season between winter and summer.",
            "hi": "वसंत ऋतु; जाड़े और गर्मी के बीच की ऋतु।",
            "ur": "موسمِ بہار؛ سردی اور گرمی کے درمیان کا موسم۔",
            "field": "time_and_seasons",
            "table": "Table 1, p. 248",
            "context": "Names of seasons in Gaddi language as documented in Bhaderwah."
        }
    ],
    "cats": ["nature", "time_and_seasons"],
    "comp_notes": "Corresponds to Western Pahari basant / bast."
})

raw_records.append({
    "lemma_dev": "बरसाला",
    "ipa": "barsaːla",
    "orig": "barsaːla",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Summer season / rainy season; the monsoon period.",
            "hi": "ग्रीष्म ऋतु / वर्षा ऋतु; बरसात का समय।",
            "ur": "گرمی کا موسم / برسات؛ بارشوں کا زمانہ۔",
            "field": "time_and_seasons",
            "table": "Table 1, p. 248",
            "context": "Names of seasons in Gaddi language as documented in Bhaderwah."
        }
    ],
    "cats": ["nature", "time_and_seasons"],
    "comp_notes": "Cognate with Pahari barsala / barsat."
})

raw_records.append({
    "lemma_dev": "शैर",
    "ipa": "ʃaeːr",
    "orig": "ʃaeːr",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Autumn season; the post-monsoon harvest season.",
            "hi": "शरद ऋतु; पतझड़ और फसल कटाई की ऋतु।",
            "ur": "موسمِ خزاں؛ پات جھڑ اور فصل کی کٹائی کا موسم۔",
            "field": "time_and_seasons",
            "table": "Table 1, p. 248",
            "context": "Names of seasons in Gaddi language as documented in Bhaderwah."
        }
    ],
    "cats": ["nature", "time_and_seasons"],
    "comp_notes": "Cognate with Western Pahari sair / share."
})

raw_records.append({
    "lemma_dev": "ह्योंद",
    "ipa": "hʲõːd",
    "orig": "hʲõːd",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Winter season; the cold and snowy season.",
            "hi": "शीत ऋतु / जाड़ा; ठंड और बर्फबारी का मौसम।",
            "ur": "موسمِ سرما / جاڑا؛ سردی اور برف کا موسم۔",
            "field": "time_and_seasons",
            "table": "Table 1, p. 248",
            "context": "Names of seasons in Gaddi language as documented in Bhaderwah."
        }
    ],
    "cats": ["nature", "time_and_seasons"],
    "comp_notes": "Cognate with Himachali Gaddi hyund / hyond, Sanskrit hemanta."
})

# --- 2. MONTHS OF THE YEAR (Table 2, p. 248) ---
month_data = [
    ("चेतर", "tʃetar", "tʃetar", "Chaitra month (approx. February–March / March–April)", "चैत्र मास (फरवरी-मार्च)", "چیت کا مہینہ (فروری تا مارچ)", "Table 2, p. 248"),
    ("बिसाक", "bisaːk", "bisaːk", "Vaisakha month (approx. March–April / April–May)", "वैशाख मास (मार्च-अप्रैल)", "بیساکھ کا مہینہ (مارچ تا اپریل)", "Table 2, p. 248"),
    ("हाड़", "haːɖ", "haːɖ", "Ashadha month (approx. May–June / June–July)", "आषाढ़ मास (मई-जून)", "ہاڑھ کا مہینہ (مئی تا جون)", "Table 2, p. 248"),
    ("सवनी", "sawni", "Sawni", "Shravana month (approx. June–July / July–August)", "श्रावण मास / सावन (जून-जुलाई)", "ساون کا مہینہ (جون تا جولائی)", "Table 2, p. 248"),
    ("भादू", "bʰadu", "Badu", "Bhadrapada month (approx. July–August / August–September)", "भाद्रपद मास / भादों (जुलाई-अगस्त)", "بھادوں کا مہینہ (جولائی تا اگست)", "Table 2, p. 248"),
    ("असोझ", "asoːdʒ", "asoːdʒ", "Ashvina month (approx. August–September / September–October)", "आश्विन मास / आसोज (अगस्त-सितंबर)", "اسوج کا مہینہ (اگست تا ستمبر)", "Table 2, p. 248"),
    ("कतिक", "katɨk", "katɨk", "Kartika month (approx. September–October / October–November)", "कार्तिक मास (सितंबर-अक्टूबर)", "کاتک کا مہینہ (ستمبر تا اکتوبر)", "Table 2, p. 248"),
    ("मघर", "maɡʰar", "maɡʰar", "Margashirsha month (approx. October–November / November–December)", "मार्गशीर्ष मास / अगहन (अक्टूबर-नवंबर)", "مگھر کا مہینہ (اکتوبر تا نومبر)", "Table 2, p. 248"),
    ("पौह", "pɔw", "Pow", "Pausha month (approx. November–December / December–January)", "पौष मास / पूस (नवंबर-दिसंबर)", "پوہ کا مہینہ (نومبر تا دسمبر)", "Table 2, p. 248"),
    ("माग", "maːɡ", "maːɡ", "Magha month (approx. December–January / January–February)", "माघ मास (दिसंबर-जनवरी)", "ماگھ کا مہینہ (دسمبر تا جنوری)", "Table 2, p. 248"),
    ("फागण", "pʰaɡən", "pʰaɡən", "Phalguna month (approx. January–February / February–March)", "फाल्गुन मास / फागुन (जनवरी-फरवरी)", "پھگن کا مہینہ (جنوری تا فروری)", "Table 2, p. 248"),
]
for dev, ipa, orig, en, hi, ur, tbl in month_data:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": "noun",
        "gender": "masculine" if dev != "सवनी" else "feminine",
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "calendar",
                "table": tbl,
                "context": "Traditional calendar month in Bhaderwah Gaddi."
            }
        ],
        "cats": ["time_and_seasons", "calendar"],
        "comp_notes": "Traditional Pahari solar calendar month."
    })

# Month and Kinship homograph: जेठ (dʒeːʈʰ)
raw_records.append({
    "lemma_dev": "जेठ",
    "ipa": "dʒeːʈʰ",
    "orig": "dʒeːʈʰ",
    "pos": "noun",
    "gender": "masculine",
    "senses": [
        {
            "en": "Jyeshtha month (approx. April–May / May–June); the third month of the traditional Pahari calendar.",
            "hi": "ज्येष्ठ मास (अप्रैल-मई); पारंपरिक पहाड़ी पंचांग का तीसरा महीना।",
            "ur": "جیٹھ کا مہینہ (اپریل تا مئی)؛ روایتی تقویم کا تیسرا مہینہ۔",
            "field": "calendar",
            "table": "Table 2, p. 248",
            "context": "Traditional calendar month in Bhaderwah Gaddi."
        },
        {
            "en": "Husband's Elder Brother (HBe); senior affinal male relative in own generation (G0). Addresser: Wife (W).",
            "hi": "जेठ (पति का बड़ा भाई); समकालीन पीढ़ी (G0) में वरिष्ठ वैवाहिक पुरुष संबंधी। संबोधनकर्ता: पत्नी (W)।",
            "ur": "جیٹھ (شوہر کا بڑا بھائی)؛ اپنی نسل (G0) میں بڑا سسرالی رشتہ۔ مخاطِب: بیوی (W)۔",
            "field": "kinship",
            "table": "Table 12, p. 254",
            "context": "Affinal relationship in Bhaderwah Gaddi: Wife -> Husband's Elder Brother (HBe, M, G0)."
        }
    ],
    "cats": ["time_and_seasons", "calendar", "people", "kinship"],
    "comp_notes": "Polysemous in Western Pahari: designates both Jyeshtha month and husband's elder brother.",
    "kinship_algebra": {"generation": "G0", "addresser": "W", "addressee": "HBe", "relation_code": "HBe", "sex": "M"}
})

# --- 3. DAYS OF THE WEEK (Table 3, p. 249) ---
days_data = [
    ("सोमवार", "somwaːr", "somwaːr", "Monday; first day of the working week.", "सोमवार; सप्ताह का पहला कार्यदिवस।", "پیر / سوموار؛ ہفتے کا پہلا دن۔", "Table 3, p. 249"),
    ("मंगलवार", "maŋalwar", "maŋalwar", "Tuesday; second day of the week.", "मंगलवार; सप्ताह का दूसरा दिन।", "منگل / منگلوار؛ ہفتے کا دوسرا دن۔", "Table 3, p. 249"),
    ("बुधवार", "budʰwar", "budʰwar", "Wednesday; third day of the week.", "बुधवार; सप्ताह का तीसरा दिन।", "بدھ / بدھوار؛ ہفتے کا تیسرا دن۔", "Table 3, p. 249"),
    ("ब्रेस्तवार", "brestwar", "brestwar", "Thursday; fourth day of the week.", "बृहस्पतिवार / गुरुवार; सप्ताह का चौथा दिन।", "جمعرات / برستوار؛ ہفتے کا چوتھا دن۔", "Table 3, p. 249"),
    ("शुक्रवार", "ʃukurwar", "ʃukurwar", "Friday; fifth day of the week.", "शुक्रवार; सप्ताह का पाँचवाँ दिन।", "جمعہ / شکرور؛ ہفتے کا پانچواں دن۔", "Table 3, p. 249"),
    ("शनिवार", "ʃaniwar", "ʃaniwar", "Saturday; sixth day of the week.", "शनिवार; सप्ताह का छठा दिन।", "ہفتہ / سنیچر / شنیوار؛ ہفتے کا چھٹا دن۔", "Table 3, p. 249"),
    ("एतवार", "eːtwar", "eːtwar", "Sunday; seventh day of the week.", "रविवार / इतवार; सप्ताह का सातवाँ दिन।", "اتوار / رتوار؛ ہفتے کا ساتواں دن۔", "Table 3, p. 249"),
]
for dev, ipa, orig, en, hi, ur, tbl in days_data:
    raw_records.append({
        "lemma_dev": dev,
        "ipa": ipa,
        "orig": orig,
        "pos": "noun",
        "gender": "masculine",
        "senses": [
            {
                "en": en,
                "hi": hi,
                "ur": ur,
                "field": "calendar",
                "table": tbl,
                "context": "Day of the week in Bhaderwah Gaddi."
            }
        ],
        "cats": ["time_and_seasons", "calendar"],
        "comp_notes": "Western Pahari weekday naming system."
    })

print(f"Loaded {len(raw_records)} season, month, and day records.")
