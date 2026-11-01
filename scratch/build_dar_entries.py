import json
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from gaddi.models import LexicalEntry, Sense, Attestation, EvidenceStatus
from gaddi.validator import GaddiValidator

# 1. Seasons
raw_seasons = [
    ("bast", "बस्त", "bast", "Spring season", "वसंत ऋतु", "noun", "masculine", "Table 1, p. 248", ["nature", "time_and_seasons"]),
    ("barsaːla", "बरसाला", "barsaːla", "Summer / rainy season", "ग्रीष्म ऋतु / वर्षा ऋतु", "noun", "masculine", "Table 1, p. 248", ["nature", "time_and_seasons"]),
    ("ʃaeːr", "शैर", "ʃaeːr", "Autumn season", "शरद ऋतु / पतझड़", "noun", "masculine", "Table 1, p. 248", ["nature", "time_and_seasons"]),
    ("hʲõːd", "ह्योंद", "hʲõːd", "Winter season", "शीत ऋतु / जाड़ा", "noun", "masculine", "Table 1, p. 248", ["nature", "time_and_seasons"]),
]

# 2. Months
raw_months = [
    ("tʃetar", "चेतर", "tʃetar", "Chaitra month (approx. February–March / March–April)", "चैत्र मास", "Table 2, p. 248"),
    ("bisaːk", "बिसाक", "bisaːk", "Vaisakha month (approx. March–April / April–May)", "वैशाख मास", "Table 2, p. 248"),
    ("dʒeːʈʰ", "जेठ", "dʒeːʈʰ", "Jyeshtha month (approx. April–May / May–June)", "ज्येष्ठ मास", "Table 2, p. 248"),
    ("haːɖ", "हाड़", "haːɖ", "Ashadha month (approx. May–June / June–July)", "आषाढ़ मास", "Table 2, p. 248"),
    ("Sawni", "सवनी", "sawni", "Shravana month (approx. June–July / July–August)", "श्रावण मास / सावन", "Table 2, p. 248"),
    ("Badu", "भादू", "bʰadu", "Bhadrapada month (approx. July–August / August–September)", "भाद्रपद मास / भादों", "Table 2, p. 248"),
    ("asoːdʒ", "असोझ", "asoːdʒ", "Ashvina month (approx. August–September / September–October)", "आश्विन मास / आसोज", "Table 2, p. 248"),
    ("katɨk", "कतिक", "katɨk", "Kartika month (approx. September–October / October–November)", "कार्तिक मास", "Table 2, p. 248"),
    ("maɡʰar", "मघर", "maɡʰar", "Margashirsha month (approx. October–November / November–December)", "मार्गशीर्ष मास / अगहन", "Table 2, p. 248"),
    ("Pow", "पौह", "pɔw", "Pausha month (approx. November–December / December–January)", "पौष मास / पूस", "Table 2, p. 248"),
    ("maːɡ", "माग", "maːɡ", "Magha month (approx. December–January / January–February)", "माघ मास", "Table 2, p. 248"),
    ("pʰaɡən", "फागण", "pʰaɡən", "Phalguna month (approx. January–February / February–March)", "फाल्गुन मास / फागुन", "Table 2, p. 248"),
]

# 3. Days
raw_days = [
    ("somwaːr", "सोमवार", "somwaːr", "Monday", "सोमवार", "Table 3, p. 249"),
    ("maŋalwar", "मंगलवार", "maŋalwar", "Tuesday", "मंगलवार", "Table 3, p. 249"),
    ("budʰwar", "बुधवार", "budʰwar", "Wednesday", "बुधवार", "Table 3, p. 249"),
    ("brestwar", "ब्रेस्तवार", "brestwar", "Thursday", "बृहस्पतिवार / गुरुवार", "Table 3, p. 249"),
    ("ʃukurwar", "शुक्रवार", "ʃukurwar", "Friday", "शुक्रवार", "Table 3, p. 249"),
    ("ʃaniwar", "शनिवार", "ʃaniwar", "Saturday", "शनिवार", "Table 3, p. 249"),
    ("eːtwar", "एतवार", "eːtwar", "Sunday", "रविवार / इतवार", "Table 3, p. 249"),
]

# 4. Cardinals
raw_cardinals = [
    ("akɨ", "अकि", "akɨ", "one (cardinal numeral 1)", "एक (१)", 1, "Table 4, p. 249"),
    ("doːj", "दोय", "doːj", "two (cardinal numeral 2)", "दो (२)", 2, "Table 4, p. 249"),
    ("trai", "त्रै", "trai", "three (cardinal numeral 3)", "तीन (३)", 3, "Table 4, p. 249"),
    ("tʃoːr", "चोर", "tʃoːr", "four (cardinal numeral 4)", "चार (४)", 4, "Table 4, p. 249"),
    ("pandʒi", "पंजी", "pandʒi", "five (cardinal numeral 5)", "पाँच (५)", 5, "Table 4, p. 249"),
    ("tʃeː", "चे", "tʃeː", "six (cardinal numeral 6)", "छह (६)", 6, "Table 4, p. 249"),
    ("satɨ", "सति", "satɨ", "seven (cardinal numeral 7)", "सात (७)", 7, "Table 4, p. 249"),
    ("aʈʰɨ", "अठि", "aʈʰɨ", "eight (cardinal numeral 8)", "आठ (८)", 8, "Table 4, p. 249"),
    ("nav", "नव", "nav", "nine (cardinal numeral 9)", "नौ (९)", 9, "Table 4, p. 249"),
    ("daʃ", "दश", "daʃ", "ten (cardinal numeral 10)", "दस (१०)", 10, "Table 4, p. 249"),
    ("ɡʲaːra", "ग्यारा", "ɡʲaːra", "eleven (cardinal numeral 11)", "ग्यारह (११)", 11, "Table 4, p. 249"),
    ("baːraː", "बारा", "baːraː", "twelve (cardinal numeral 12)", "बारह (१२)", 12, "Table 4, p. 249"),
    ("teːraː", "तेरा", "teːraː", "thirteen (cardinal numeral 13)", "तेरह (१३)", 13, "Table 4, p. 249"),
    ("tʃowda", "चौदा", "tʃowda", "fourteen (cardinal numeral 14)", "चौदह (१४)", 14, "Table 4, p. 249"),
    ("pandra", "पन्द्रा", "pandra", "fifteen (cardinal numeral 15)", "पंद्रह (१५)", 15, "Table 4, p. 249"),
    ("ʃola", "शोला", "ʃola", "sixteen (cardinal numeral 16)", "सोलह (१६)", 16, "Table 4, p. 249"),
    ("sataːra", "सतारा", "sataːra", "seventeen (cardinal numeral 17)", "सत्रह (१७)", 17, "Table 4, p. 250"),
    ("aʈʰara", "अठारा", "aʈʰara", "eighteen (cardinal numeral 18)", "अठारह (१८)", 18, "Table 4, p. 250"),
    ("uniː", "उनी", "uniː", "nineteen (cardinal numeral 19)", "उन्नीस (१९)", 19, "Table 4, p. 250"),
    ("biː", "बी", "biː", "twenty (cardinal numeral 20)", "बीस (२०)", 20, "Table 4, p. 250"),
    ("tʃaliː", "चाली", "tʃaliː", "forty (cardinal numeral 40)", "चालीस (४०)", 40, "Table 4, p. 250"),
    ("pandʒa", "पंजा", "pandʒa", "fifty (cardinal numeral 50)", "पचास (५०)", 50, "Table 4, p. 250"),
    ("ʃov", "शौव", "ʃov", "hundred (cardinal numeral 100)", "सौ (१००)", 100, "Table 4, p. 250"),
    ("akʰ azaːr", "अख हज़ार", "akʰ azaːr", "one thousand (cardinal numeral 1000)", "एक हज़ार (१०००)", 1000, "Table 4, p. 250"),
]

# 5. Ordinals
raw_ordinals = [
    ("pehla", "पहला", "pehla", "first (ordinal 1st)", "पहला (१ला)", "Table 5, p. 250"),
    ("duwa", "दुवा", "duwa", "second (ordinal 2nd)", "दूसरा (२रा)", "Table 5, p. 250"),
    ("trija", "त्रिया", "trija", "third (ordinal 3rd)", "तीसरा (३रा)", "Table 5, p. 250"),
    ("tʃotʰa", "चोथा", "tʃotʰa", "fourth (ordinal 4th)", "चौथा (४था)", "Table 5, p. 250"),
    ("pandʒwa", "पंज्वा", "pandʒwa", "fifth (ordinal 5th)", "पाँचवाँ (५वाँ)", "Table 5, p. 250"),
    ("tʃʰaʈʰwa", "छठ्वा", "tʃʰaʈʰwa", "sixth (ordinal 6th)", "छठा (६ठा)", "Table 5, p. 250"),
    ("satɨwa", "सतिवा", "satɨwa", "seventh (ordinal 7th)", "सातवाँ (७वाँ)", "Table 5, p. 250"),
    ("aʈʰɨwa", "अठिवा", "aʈʰɨwa", "eighth (ordinal 8th)", "आठवाँ (८वाँ)", "Table 5, p. 250"),
    ("nawwa", "नववा", "nawwa", "ninth (ordinal 9th)", "नौवाँ (९वाँ)", "Table 5, p. 250"),
    ("daʃwa", "दशवा", "daʃwa", "tenth (ordinal 10th)", "दसवाँ (१०वाँ)", "Table 5, p. 250"),
    ("bĩːwa", "बींवा", "bĩːwa", "twentieth (ordinal 20th)", "बीसवाँ (२०वाँ)", "Table 5, p. 250"),
    ("padʒama", "पजामा", "padʒama", "fiftieth (ordinal 50th)", "पचासवाँ (५०वाँ)", "Table 5, p. 250"),
    ("ʃawma", "शौमा", "ʃawma", "hundredth (ordinal 100th)", "सौवाँ (१००वाँ)", "Table 5, p. 250"),
]

print("Setup completed successfully.")
