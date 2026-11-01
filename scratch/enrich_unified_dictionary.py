import json
import re
from pathlib import Path
from gaddi.validator import GaddiValidator
from gaddi.models import LexicalEntry

data_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
res_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources\dictionary_unified.json")

with open(data_path, "r", encoding="utf-8") as f:
    entries = json.load(f)

# Filter out empty lemmas
entries = [e for e in entries if e.get("lemma_devanagari", "").strip()]

# Expanded multilingual dictionary for common English terms
MULTILINGUAL_GLOSSES = {
    "water": {"hi": "पानी", "ur": "پانی", "pa": "ਪਾਣੀ", "doi": "पाणी"},
    "fire": {"hi": "आग", "ur": "آگ", "pa": "ਅੱਗ", "doi": "अग्ग"},
    "sun": {"hi": "सूरज", "ur": "سورج", "pa": "ਸੂਰਜ", "doi": "सूरज"},
    "moon": {"hi": "चाँद", "ur": "چاند", "pa": "ਚੰਨ", "doi": "चन्न"},
    "star": {"hi": "तारा", "ur": "تارہ", "pa": "ਤਾਰਾ", "doi": "तारा"},
    "earth": {"hi": "धरती", "ur": "زمین", "pa": "ਧਰਤੀ", "doi": "धरती"},
    "sky": {"hi": "आसमान", "ur": "آسمان", "pa": "ਅਸਮਾਨ", "doi": "अम्बर"},
    "cloud": {"hi": "बादल", "ur": "بادل", "pa": "ਬੱਦਲ", "doi": "बदल"},
    "rain": {"hi": "बारिश", "ur": "بارش", "pa": "ਮੀਂਹ", "doi": "बरखा"},
    "wind": {"hi": "हवा", "ur": "ہوا", "pa": "ਹਵਾ", "doi": "हवा"},
    "tree": {"hi": "पेड़", "ur": "درخت", "pa": "ਰੁੱਖ", "doi": "बूटा"},
    "leaf": {"hi": "पत्ता", "ur": "پتا", "pa": "ਪੱਤਾ", "doi": "पत्तर"},
    "root": {"hi": "जड़", "ur": "جڑ", "pa": "ਜੜ੍ਹ", "doi": "जड़"},
    "flower": {"hi": "फूल", "ur": "پھول", "pa": "ਫੁੱਲ", "doi": "फुल्ल"},
    "fruit": {"hi": "फल", "ur": "پھਲ", "pa": "ਫਲ", "doi": "फल"},
    "grass": {"hi": "घास", "ur": "گھاس", "pa": "ਘਾਹ", "doi": "गाह"},
    "wood": {"hi": "लकड़ी", "ur": "لکڑی", "pa": "ਲੱਕੜ", "doi": "लट्ठ"},
    "stone": {"hi": "पत्थर", "ur": "پتھر", "pa": "ਪੱਥਰ", "doi": "पत्थर"},
    "mountain": {"hi": "पहाड़", "ur": "پہاڑ", "pa": "ਪਹਾੜ", "doi": "धार"},
    "river": {"hi": "नदी", "ur": "دریا", "pa": "ਨਦੀ", "doi": "नद्दी"},
    "lake": {"hi": "झील", "ur": "جھيل", "pa": "ਝੀਲ", "doi": "छंब"},
    "sea": {"hi": "समुद्र", "ur": "سمندر", "pa": "ਸਮੁੰਦਰ", "doi": "समुन्दर"},
    "path": {"hi": "रास्ता", "ur": "راستہ", "pa": "ਰਾਹ", "doi": "राह"},
    "road": {"hi": "सड़क", "ur": "سڑک", "pa": "ਸੜਕ", "doi": "सड़क"},
    "house": {"hi": "घर", "ur": "گھر", "pa": "ਘਰ", "doi": "घर"},
    "door": {"hi": "दरवाज़ा", "ur": "دروازہ", "pa": "ਬੂਹਾ", "doi": "बूहा"},
    "window": {"hi": "खिड़की", "ur": "کھڑکی", "pa": "ਖਿੜਕੀ", "doi": "खिड़की"},
    "room": {"hi": "कमरा", "ur": "کمرہ", "pa": "ਕਮਰਾ", "doi": "कमरा"},
    "village": {"hi": "गाँव", "ur": "گاؤں", "pa": "ਪਿੰਡ", "doi": "गराँ"},
    "city": {"hi": "शहर", "ur": "شہر", "pa": "ਸ਼ਹਿਰ", "doi": "शहर"},
    "country": {"hi": "देश", "ur": "ملک", "pa": "ਦੇਸ਼", "doi": "देस"},
    "man": {"hi": "पुरुष / आदमी", "ur": "مرد / آدمی", "pa": "ਆਦਮੀ / ਬੰਦਾ", "doi": "मणु / बंदा"},
    "woman": {"hi": "औरत / महिला", "ur": "عورت", "pa": "ਔਰਤ / ਤੀਵੀਂ", "doi": "जनानी"},
    "boy": {"hi": "लड़का", "ur": "لڑکا", "pa": "ਮੁੰਡਾ", "doi": "छोकरा / मुंडा"},
    "girl": {"hi": "लड़की", "ur": "لڑکی", "pa": "ਕੁੜੀ", "doi": "कुड़ी / छोकरी"},
    "child": {"hi": "बच्चा", "ur": "بچہ", "pa": "ਬੱਚਾ / ਨਿਆਣਾ", "doi": "बच्चा / श्वाला"},
    "mother": {"hi": "माँ / माता", "ur": "ماں", "pa": "ਮਾਂ", "doi": "मई / माँ"},
    "father": {"hi": "पिता / बाप", "ur": "باپ", "pa": "ਪਿਓ / ਪਿਤਾ", "doi": "बप्पू / पिता"},
    "brother": {"hi": "भाई", "ur": "بھائی", "pa": "ਭਰਾ", "doi": "भ्रा"},
    "sister": {"hi": "बहन", "ur": "بہن", "pa": "ਭੈਣ", "doi": "ਭੈਣ / भैण"},
    "son": {"hi": "बेटा / पुत्र", "ur": "بیٹا", "pa": "ਪੁੱਤ", "doi": "पुत्त"},
    "daughter": {"hi": "बेटी / पुत्री", "ur": "بیਟੀ", "pa": "ਧੀ", "doi": "धी"},
    "husband": {"hi": "पति", "ur": "شوہر", "pa": "ਘਰਵਾਲਾ / ਪਤੀ", "doi": "खसम / पति"},
    "wife": {"hi": "पत्नी", "ur": "بیوی", "pa": "ਘਰਵਾਲੀ / ਪਤਨੀ", "doi": "जनानी / पत्नी"},
    "friend": {"hi": "मित्र / दोस्त", "ur": "دوست", "pa": "ਮਿੱਤਰ / ਦੋਸਤ", "doi": "संगी / दोस्त"},
    "head": {"hi": "सिर", "ur": "سر", "pa": "ਸਿਰ", "doi": "सिर"},
    "hair": {"hi": "बाल", "ur": "بال", "pa": "ਵਾਲ", "doi": "बाल / रुंड"},
    "eye": {"hi": "आँख", "ur": "آنکھ", "pa": "ਅੱਖ", "doi": "अक्ख"},
    "ear": {"hi": "कान", "ur": "کان", "pa": "ਕੰਨ", "doi": "कन्न"},
    "nose": {"hi": "नाक", "ur": "ناک", "pa": "ਨੱਕ", "doi": "नक्क"},
    "mouth": {"hi": "मुँह", "ur": "منہ", "pa": "ਮੂੰਹ", "doi": "मुँह"},
    "tooth": {"hi": "दाँत", "ur": "دانت", "pa": "ਦੰਦ", "doi": "दंद"},
    "tongue": {"hi": "जीभ", "ur": "زبان", "pa": "ਜੀਭ", "doi": "जीभ"},
    "hand": {"hi": "हाथ", "ur": "ہاتھ", "pa": "ਹੱਥ", "doi": "हत्थ"},
    "arm": {"hi": "बाँह", "ur": "بازو", "pa": "ਬਾਂਹ", "doi": "बाँह"},
    "foot": {"hi": "पैर", "ur": "پیر", "pa": "ਪੈਰ", "doi": "पैर"},
    "leg": {"hi": "टाँग", "ur": "ٹانگ", "pa": "ਲੱਤ", "doi": "जंघ / लत्त"},
    "belly": {"hi": "पेट", "ur": "پیٹ", "pa": "ਢਿੱਡ / ਪੇਟ", "doi": "ढिड्ड"},
    "heart": {"hi": "दिल / हृदय", "ur": "دل", "pa": "ਦਿਲ", "doi": "हिया / दिल"},
    "blood": {"hi": "खून / रक्त", "ur": "خون", "pa": "ਖੂਨ / ਲਹੂ", "doi": "लहू"},
    "bone": {"hi": "हड्डी", "ur": "ہڈی", "pa": "ਹੱਡੀ", "doi": "हड्डी"},
    "skin": {"hi": "त्वचा / चमड़ी", "ur": "جلد", "pa": "ਚਮੜੀ", "doi": "चमड़ी"},
    "meat": {"hi": "माँस", "ur": "گوشت", "pa": "ਮਾਸ", "doi": "मास"},
    "milk": {"hi": "दूध", "ur": "دودھ", "pa": "ਦੁੱਧ", "doi": "दुद्ध"},
    "butter": {"hi": "मक्खन", "ur": "مکھن", "pa": "ਮੱਖਣ", "doi": "मक्खण"},
    "ghee": {"hi": "घी", "ur": "گھی", "pa": "ਘਿਓ", "doi": "घ्यो"},
    "bread": {"hi": "रोटी", "ur": "روٹی", "pa": "ਰੋਟੀ", "doi": "रोटी / फुलका"},
    "rice": {"hi": "चावल / भात", "ur": "چاول", "pa": "ਚੌਲ", "doi": "चौळ / भात"},
    "salt": {"hi": "नमक", "ur": "نمک", "pa": "ਲੂਣ", "doi": "लूण"},
    "oil": {"hi": "तेल", "ur": "تیل", "pa": "ਤੇਲ", "doi": "तेल"},
    "honey": {"hi": "शहद", "ur": "شہد", "pa": "ਸ਼ਹਿਦ", "doi": "माख्यों"},
    "dog": {"hi": "कुत्ता", "ur": "کتا", "pa": "ਕੁੱਤਾ", "doi": "कुत्ता"},
    "cat": {"hi": "बिल्ली", "ur": "بلی", "pa": "ਬਿੱਲੀ", "doi": "बिल्ली"},
    "cow": {"hi": "गाय", "ur": "گائے", "pa": "ਗਾਂ", "doi": "गौ / गां"},
    "bull": {"hi": "बैल", "ur": "بیل", "pa": "ਬਲਦ", "doi": "बल्द"},
    "ox": {"hi": "बैल", "ur": "بیل", "pa": "ਬਲਦ", "doi": "बल्द"},
    "buffalo": {"hi": "भैंस", "ur": "بھینس", "pa": "ਮੱਝ", "doi": "मझ"},
    "sheep": {"hi": "भेड़", "ur": "بھیڑ", "pa": "ਭੇਡ", "doi": "भेड"},
    "goat": {"hi": "बकरी", "ur": "بکری", "pa": "ਬੱਕਰੀ", "doi": "बकरी"},
    "horse": {"hi": "घोड़ा", "ur": "گھوڑا", "pa": "ਘੋੜਾ", "doi": "घोड़ा"},
    "bird": {"hi": "पक्षी / चिड़िया", "ur": "پرندہ", "pa": "ਪੰਛੀ", "doi": "पंछी / पंखेरू"},
    "fish": {"hi": "मछली", "ur": "مچھلی", "pa": "ਮੱਛੀ", "doi": "मच्छी"},
    "snake": {"hi": "साँप", "ur": "سانپ", "pa": "ਸੱਪ", "doi": "सप्प"},
    "bear": {"hi": "भालू", "ur": "ریچھ", "pa": "ਭਾਲੂ / ਰਿੱਛ", "doi": "रिच्छ"},
    "wolf": {"hi": "भेड़िया", "ur": "بھیڑیا", "pa": "ਬਘਿਆੜ", "doi": "बघ्याड़"},
    "fox": {"hi": "लोमड़ी", "ur": "لومڑی", "pa": "ਲੂੰਬੜੀ", "doi": "लूंबड़ी"},
    "day": {"hi": "दिन", "ur": "دن", "pa": "ਦਿਨ / ਦਿਹਾੜਾ", "doi": "दिहाड़ा"},
    "night": {"hi": "रात", "ur": "رات", "pa": "ਰਾਤ", "doi": "रात"},
    "morning": {"hi": "सुबह / प्रातः", "ur": "صبح", "pa": "ਸਵੇਰ", "doi": "सवेरे"},
    "evening": {"hi": "शाम / संध्या", "ur": "شام", "pa": "ਸ਼ਾਮ / ਤ੍ਰਿਕਾਲਾਂ", "doi": "संज"},
    "year": {"hi": "साल / वर्ष", "ur": "سال", "pa": "ਸਾਲ / ਵਰ੍ਹਾ", "doi": "साल / ब्ह्रा"},
    "month": {"hi": "महीना", "ur": "مہینہ", "pa": "ਮਹੀਨਾ", "doi": "म्हीना"},
    "summer": {"hi": "गर्मी / ग्रीष्म", "ur": "گرمی", "pa": "ਗਰਮੀ", "doi": "गर्मी"},
    "winter": {"hi": "सर्दी / शीतकाल", "ur": "سردی", "pa": "ਸਰਦੀ / ਸਿਆਲ", "doi": "स्याल"},
    "snow": {"hi": "बर्फ़ / हिम", "ur": "برف", "pa": "ਬਰਫ਼", "doi": "बरफ"},
    "white": {"hi": "सफ़ेद / श्वेत", "ur": "سفید", "pa": "ਚਿੱਟਾ", "doi": "चिट्टा"},
    "black": {"hi": "काला", "ur": "کالا", "pa": "ਕਾਲਾ", "doi": "काला"},
    "red": {"hi": "लाल", "ur": "سرخ / لال", "pa": "ਲਾਲ", "doi": "लाल / रत्ता"},
    "green": {"hi": "हरा", "ur": "سبز / ہرا", "pa": "ਹਰਾ", "doi": "सब्ज / हरा"},
    "yellow": {"hi": "पीला", "ur": "پیلا", "pa": "ਪੀਲਾ", "doi": "पीळा"},
    "blue": {"hi": "नीला", "ur": "نیلا", "pa": "ਨੀਲਾ", "doi": "नीला"},
    "good": {"hi": "अच्छा / भला", "ur": "اچھا / عمدہ", "pa": "ਚੰਗਾ", "doi": "शैल / चंगा"},
    "bad": {"hi": "बुरा / ख़राब", "ur": "برا / خراب", "pa": "ਮਾੜਾ / ਬੁਰਾ", "doi": "माड़ा / बुरा"},
    "big": {"hi": "बड़ा", "ur": "بڑا", "pa": "ਵੱਡਾ", "doi": "वड्डा"},
    "small": {"hi": "छोटा", "ur": "چھوٹਾ", "pa": "ਛੋਟਾ", "doi": "निक्का / छोटा"},
    "hot": {"hi": "गर्म", "ur": "گرم", "pa": "ਗਰਮ / ਤੱਤਾ", "doi": "तत्ता / गर्म"},
    "cold": {"hi": "ठंडा / शीतल", "ur": "ٹھنڈا", "pa": "ਠੰਢਾ", "doi": "ठंडा"},
    "to eat": {"hi": "खाना", "ur": "کھانا", "pa": "ਖਾਣਾ", "doi": "खाणा"},
    "to drink": {"hi": "पीना", "ur": "پینا", "pa": "ਪੀਣਾ", "doi": "पीणा"},
    "to go": {"hi": "जाना", "ur": "جانا", "pa": "ਜਾਣਾ", "doi": "जाणा"},
    "to come": {"hi": "आना", "ur": "آنا", "pa": "ਆਉਣਾ", "doi": "औणा"},
    "to see": {"hi": "देखना", "ur": "دیکھنا", "pa": "ਵੇਖਣਾ", "doi": "दिखणा"},
    "to hear": {"hi": "सुनना", "ur": "سننا", "pa": "ਸੁਣਨਾ", "doi": "सुणना"},
    "to speak": {"hi": "बोलना", "ur": "بولنا", "pa": "ਬੋਲਣਾ", "doi": "बोलणा"},
    "to sleep": {"hi": "सोना", "ur": "سونا", "pa": "ਸੌਣਾ", "doi": "सौणा"},
    "to sit": {"hi": "बैठना", "ur": "بیٹھنا", "pa": "ਬੈਠਣਾ", "doi": "बैहणा"},
    "to stand": {"hi": "खड़ा होना", "ur": "کھڑا ہونا", "pa": "ਖੜੋਣਾ", "doi": "ख्लोणा"},
    "to give": {"hi": "देना", "ur": "دینا", "pa": "ਦੇਣਾ", "doi": "देणा"},
    "to take": {"hi": "लेना", "ur": "لینا", "pa": "ਲੈਣਾ", "doi": "लैणा"},
    "to do": {"hi": "करना", "ur": "کرنا", "pa": "ਕਰਨਾ", "doi": "करना / करणा"},
    "who": {"hi": "कौन", "ur": "کون", "pa": "ਕੌਣ", "doi": "कुण"},
    "what": {"hi": "क्या", "ur": "کیا", "pa": "ਕੀ", "doi": "क्या / केह"},
    "where": {"hi": "कहाँ", "ur": "کہاں", "pa": "ਕਿੱਥੇ", "doi": "कुत्थे / कित्थी"},
    "when": {"hi": "कब", "ur": "کب", "pa": "ਕਦੋਂ", "doi": "कद"},
    "why": {"hi": "क्यों", "ur": "کیوں", "pa": "ਕਿਉਂ", "doi": "की जे"},
    "how": {"hi": "कैसे", "ur": "کیسے", "pa": "ਕਿਵੇਂ", "doi": "कियाँ"},
}

for idx, entry in enumerate(entries):
    entry["id"] = f"gaddi-uni-{idx+1:05d}"
    senses = entry.get("senses", [])
    if not senses:
        continue
    
    first_sense = senses[0]
    en_def = (first_sense.get("definition_en") or "").lower()
    
    # Try exact or token matching with multilingual table
    for term, tr in MULTILINGUAL_GLOSSES.items():
        if term in en_def.split() or term == en_def:
            if not first_sense.get("definition_hi"):
                first_sense["definition_hi"] = tr["hi"]
            if not first_sense.get("definition_ur"):
                first_sense["definition_ur"] = tr["ur"]
            
            # Store pa and doi in metadata
            entry_meta = entry.setdefault("metadata", {})
            translations = entry_meta.setdefault("translations", {})
            translations["pa"] = tr["pa"]
            translations["doi"] = tr["doi"]
            break

# Re-validate all entries
validator = GaddiValidator()
valid_count = 0
for entry_dict in entries:
    e = LexicalEntry.from_dict(entry_dict)
    errs = validator.validate_entry(e)
    if errs:
        print(f"Error on {e.id}: {errs}")
    else:
        valid_count += 1

print(f"All validated: {valid_count} / {len(entries)}")

# Write to both paths
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

with open(res_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print("Saved byte-identical unified dictionaries to data and src resources.")
