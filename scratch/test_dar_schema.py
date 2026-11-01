# Build and verify all entries from Dar & Sheikh (2022)
entries = []

# Table 1: Seasons of the Year (p. 248)
# Gaddi | Gloss
# bast Spring
# barsaːla Summer
# ʃaeːr Autumn
# hʲõːd Winter

seasons = [
    {"source": "bast", "devanagari": "बस्त", "ipa": "bast", "gloss_en": "Spring (season)", "gloss_hi": "वसंत ऋतु", "pos": "noun", "gender": "masculine", "table": "Table 1, p. 248", "cat": ["nature", "time_and_seasons"]},
    {"source": "barsaːla", "devanagari": "बरसाला", "ipa": "barsaːla", "gloss_en": "Summer / rainy season", "gloss_hi": "ग्रीष्म ऋतु / वर्षा ऋतु", "pos": "noun", "gender": "masculine", "table": "Table 1, p. 248", "cat": ["nature", "time_and_seasons"]},
    {"source": "ʃaeːr", "devanagari": "शैर", "ipa": "ʃaeːr", "gloss_en": "Autumn (season)", "gloss_hi": "शरद ऋतु / पतझड़", "pos": "noun", "gender": "masculine", "table": "Table 1, p. 248", "cat": ["nature", "time_and_seasons"]},
    {"source": "hʲõːd", "devanagari": "ह्योंद", "ipa": "hʲõːd", "gloss_en": "Winter (season)", "gloss_hi": "शीत ऋतु / जाड़ा", "pos": "noun", "gender": "masculine", "table": "Table 1, p. 248", "cat": ["nature", "time_and_seasons"]},
]

# Table 2: Months of the Year (p. 248)
# tʃetar February-March
# bisaːk March-April
# dʒeːʈʰ April-May
# haːɖ May-June
# Sawni June-July
# Badu July-August
# asoːdʒ August-September
# katɨk September-October
# maɡʰar October-November
# Pow November-December
# maːɡ December-January
# pʰaɡən January- February

months = [
    {"source": "tʃetar", "devanagari": "चेतर", "ipa": "tʃetar", "gloss_en": "Chaitra month (approx. February–March / March–April)", "gloss_hi": "चैत्र मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "bisaːk", "devanagari": "बिसाक", "ipa": "bisaːk", "gloss_en": "Vaisakha month (approx. March–April / April–May)", "gloss_hi": "वैशाख मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "dʒeːʈʰ", "devanagari": "जेठ", "ipa": "dʒeːʈʰ", "gloss_en": "Jyeshtha month (approx. April–May / May–June)", "gloss_hi": "ज्येष्ठ मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "haːɖ", "devanagari": "हाड़", "ipa": "haːɖ", "gloss_en": "Ashadha month (approx. May–June / June–July)", "gloss_hi": "आषाढ़ मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "Sawni", "devanagari": "सवनी", "ipa": "sawni", "gloss_en": "Shravana month (approx. June–July / July–August)", "gloss_hi": "श्रावण मास / सावन", "pos": "noun", "gender": "feminine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "Badu", "devanagari": "भादू", "ipa": "bʰadu", "gloss_en": "Bhadrapada month (approx. July–August / August–September)", "gloss_hi": "भाद्रपद मास / भादों", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "asoːdʒ", "devanagari": "असोझ", "ipa": "asoːdʒ", "gloss_en": "Ashvina month (approx. August–September / September–October)", "gloss_hi": "आश्विन मास / आसोज", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "katɨk", "devanagari": "कतिक", "ipa": "katɨk", "gloss_en": "Kartika month (approx. September–October / October–November)", "gloss_hi": "कार्तिक मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "maɡʰar", "devanagari": "मघर", "ipa": "maɡʰar", "gloss_en": "Margashirsha month (approx. October–November / November–December)", "gloss_hi": "मार्गशीर्ष मास / मंगसिर", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "Pow", "devanagari": "पौह", "ipa": "pɔw", "gloss_en": "Pausha month (approx. November–December / December–January)", "gloss_hi": "पौष मास / पूस", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "maːɡ", "devanagari": "माग", "ipa": "maːɡ", "gloss_en": "Magha month (approx. December–January / January–February)", "gloss_hi": "माघ मास", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
    {"source": "pʰaɡən", "devanagari": "फागण", "ipa": "pʰaɡən", "gloss_en": "Phalguna month (approx. January–February / February–March)", "gloss_hi": "फाल्गुन मास / फागुन", "pos": "noun", "gender": "masculine", "table": "Table 2, p. 248", "cat": ["time_and_seasons", "calendar"]},
]

# Table 3: Days of the Week (p. 249)
# somwaːr Monday
# maŋalwar Tuesday
# budʰwar Wednesday
# brestwar Thursday
# ʃukurwar Friday
# ʃaniwar Saturday
# eːtwar Sunday

days = [
    {"source": "somwaːr", "devanagari": "सोमवार", "ipa": "somwaːr", "gloss_en": "Monday", "gloss_hi": "सोमवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "maŋalwar", "devanagari": "मंगलवार", "ipa": "maŋalwar", "gloss_en": "Tuesday", "gloss_hi": "मंगलवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "budʰwar", "devanagari": "बुधवार", "ipa": "budʰwar", "gloss_en": "Wednesday", "gloss_hi": "बुधवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "brestwar", "devanagari": "ब्रेस्तवार", "ipa": "brestwar", "gloss_en": "Thursday", "gloss_hi": "गुरुवार / बृहस्पतिवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "ʃukurwar", "devanagari": "शुक्रवार", "ipa": "ʃukurwar", "gloss_en": "Friday", "gloss_hi": "शुक्रवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "ʃaniwar", "devanagari": "शनिवार", "ipa": "ʃaniwar", "gloss_en": "Saturday", "gloss_hi": "शनिवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
    {"source": "eːtwar", "devanagari": "एतवार", "ipa": "eːtwar", "gloss_en": "Sunday", "gloss_hi": "रविवार / इतवार", "pos": "noun", "gender": "masculine", "table": "Table 3, p. 249", "cat": ["time_and_seasons", "calendar"]},
]

# Table 4: Cardinals in Gaddi (p. 249-250)
cardinals = [
    {"source": "akɨ", "devanagari": "अकि", "ipa": "akɨ", "gloss_en": "one (1)", "gloss_hi": "एक (१)", "pos": "numeral", "num_val": 1, "table": "Table 4, p. 249"},
    {"source": "doːj", "devanagari": "दोय", "ipa": "doːj", "gloss_en": "two (2)", "gloss_hi": "दो (२)", "pos": "numeral", "num_val": 2, "table": "Table 4, p. 249"},
    {"source": "trai", "devanagari": "त्रै", "ipa": "trai", "gloss_en": "three (3)", "gloss_hi": "तीन (३)", "pos": "numeral", "num_val": 3, "table": "Table 4, p. 249"},
    {"source": "tʃoːr", "devanagari": "चोर", "ipa": "tʃoːr", "gloss_en": "four (4)", "gloss_hi": "चार (४)", "pos": "numeral", "num_val": 4, "table": "Table 4, p. 249"},
    {"source": "pandʒi", "devanagari": "पंजी", "ipa": "pandʒi", "gloss_en": "five (5)", "gloss_hi": "पाँच (५)", "pos": "numeral", "num_val": 5, "table": "Table 4, p. 249"},
    {"source": "tʃeː", "devanagari": "चे", "ipa": "tʃeː", "gloss_en": "six (6)", "gloss_hi": "छह (६)", "pos": "numeral", "num_val": 6, "table": "Table 4, p. 249"},
    {"source": "satɨ", "devanagari": "सति", "ipa": "satɨ", "gloss_en": "seven (7)", "gloss_hi": "सात (७)", "pos": "numeral", "num_val": 7, "table": "Table 4, p. 249"},
    {"source": "aʈʰɨ", "devanagari": "अठि", "ipa": "aʈʰɨ", "gloss_en": "eight (8)", "gloss_hi": "आठ (८)", "pos": "numeral", "num_val": 8, "table": "Table 4, p. 249"},
    {"source": "nav", "devanagari": "नव", "ipa": "nav", "gloss_en": "nine (9)", "gloss_hi": "नौ (९)", "pos": "numeral", "num_val": 9, "table": "Table 4, p. 249"},
    {"source": "daʃ", "devanagari": "दश", "ipa": "daʃ", "gloss_en": "ten (10)", "gloss_hi": "दस (१०)", "pos": "numeral", "num_val": 10, "table": "Table 4, p. 249"},
    {"source": "ɡʲaːra", "devanagari": "ग्यारा", "ipa": "ɡʲaːra", "gloss_en": "eleven (11)", "gloss_hi": "ग्यारह (११)", "pos": "numeral", "num_val": 11, "table": "Table 4, p. 249"},
    {"source": "baːraː", "devanagari": "बारा", "ipa": "baːraː", "gloss_en": "twelve (12)", "gloss_hi": "बारह (१२)", "pos": "numeral", "num_val": 12, "table": "Table 4, p. 249"},
    {"source": "teːraː", "devanagari": "तेरा", "ipa": "teːraː", "gloss_en": "thirteen (13)", "gloss_hi": "तेरह (१३)", "pos": "numeral", "num_val": 13, "table": "Table 4, p. 249"},
    {"source": "tʃowda", "devanagari": "चौदा", "ipa": "tʃowda", "gloss_en": "fourteen (14)", "gloss_hi": "चौदह (१४)", "pos": "numeral", "num_val": 14, "table": "Table 4, p. 249"},
    {"source": "pandra", "devanagari": "पन्द्रा", "ipa": "pandra", "gloss_en": "fifteen (15)", "gloss_hi": "पंद्रह (१५)", "pos": "numeral", "num_val": 15, "table": "Table 4, p. 249"},
    {"source": "ʃola", "devanagari": "शोला", "ipa": "ʃola", "gloss_en": "sixteen (16)", "gloss_hi": "सोलह (१६)", "pos": "numeral", "num_val": 16, "table": "Table 4, p. 249"},
    {"source": "sataːra", "devanagari": "सतारा", "ipa": "sataːra", "gloss_en": "seventeen (17)", "gloss_hi": "सत्रह (१७)", "pos": "numeral", "num_val": 17, "table": "Table 4, p. 250"},
    {"source": "aʈʰara", "devanagari": "अठारा", "ipa": "aʈʰara", "gloss_en": "eighteen (18)", "gloss_hi": "अठारह (१८)", "pos": "numeral", "num_val": 18, "table": "Table 4, p. 250"},
    {"source": "uniː", "devanagari": "उनी", "ipa": "uniː", "gloss_en": "nineteen (19)", "gloss_hi": "उन्नीस (१९)", "pos": "numeral", "num_val": 19, "table": "Table 4, p. 250"},
    {"source": "biː", "devanagari": "बी", "ipa": "biː", "gloss_en": "twenty (20)", "gloss_hi": "बीस (२०)", "pos": "numeral", "num_val": 20, "table": "Table 4, p. 250"},
    {"source": "tʃaliː", "devanagari": "चाली", "ipa": "tʃaliː", "gloss_en": "forty (40)", "gloss_hi": "चालीस (४०)", "pos": "numeral", "num_val": 40, "table": "Table 4, p. 250"},
    {"source": "pandʒa", "devanagari": "पंजा", "ipa": "pandʒa", "gloss_en": "fifty (50)", "gloss_hi": "पचास (५०)", "pos": "numeral", "num_val": 50, "table": "Table 4, p. 250"},
    {"source": "ʃov", "devanagari": "शौव", "ipa": "ʃov", "gloss_en": "hundred (100)", "gloss_hi": "सौ (१००)", "pos": "numeral", "num_val": 100, "table": "Table 4, p. 250"},
    {"source": "akʰ azaːr", "devanagari": "अख हज़ार", "ipa": "akʰ azaːr", "gloss_en": "one thousand (1000)", "gloss_hi": "एक हज़ार (१०००)", "pos": "numeral", "num_val": 1000, "table": "Table 4, p. 250"},
]

# Table 5: Ordinals in Gaddi (p. 250)
ordinals = [
    {"source": "pehla", "devanagari": "पहला", "ipa": "pehla", "gloss_en": "first (1st)", "gloss_hi": "पहला", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "duwa", "devanagari": "दुवा", "ipa": "duwa", "gloss_en": "second (2nd)", "gloss_hi": "दूसरा", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "trija", "devanagari": "त्रिया", "ipa": "trija", "gloss_en": "third (3rd)", "gloss_hi": "तीसरा", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "tʃotʰa", "devanagari": "चोथा", "ipa": "tʃotʰa", "gloss_en": "fourth (4th)", "gloss_hi": "चौथा", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "pandʒwa", "devanagari": "पंज्वा", "ipa": "pandʒwa", "gloss_en": "fifth (5th)", "gloss_hi": "पाँचवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "tʃʰaʈʰwa", "devanagari": "छठ्वा", "ipa": "tʃʰaʈʰwa", "gloss_en": "sixth (6th)", "gloss_hi": "छठा", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "satɨwa", "devanagari": "सतिवा", "ipa": "satɨwa", "gloss_en": "seventh (7th)", "gloss_hi": "सातवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "aʈʰɨwa", "devanagari": "अठिवा", "ipa": "aʈʰɨwa", "gloss_en": "eighth (8th)", "gloss_hi": "आठवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "nawwa", "devanagari": "नववा", "ipa": "nawwa", "gloss_en": "ninth (9th)", "gloss_hi": "नौवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "daʃwa", "devanagari": "दशवा", "ipa": "daʃwa", "gloss_en": "tenth (10th)", "gloss_hi": "दसवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "bĩːwa", "devanagari": "बींवा", "ipa": "bĩːwa", "gloss_en": "twentieth (20th)", "gloss_hi": "बीसवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "padʒama", "devanagari": "पजामा", "ipa": "padʒama", "gloss_en": "fiftieth (50th)", "gloss_hi": "पचासवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
    {"source": "ʃawma", "devanagari": "शौमा", "ipa": "ʃawma", "gloss_en": "hundredth (100th)", "gloss_hi": "सौवाँ", "pos": "adjective", "table": "Table 5, p. 250"},
]

print(f"Seasons: {len(seasons)}, Months: {len(months)}, Days: {len(days)}, Cardinals: {len(cardinals)}, Ordinals: {len(ordinals)}")

