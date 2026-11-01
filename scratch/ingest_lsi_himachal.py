import json
import re
from pathlib import Path
from gaddi.validator import GaddiValidator
from gaddi.models import LexicalEntry, Sense, Attestation
from gaddi.registry import default_sources, default_varieties

DATA_PATH = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
RES_PATH = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources\dictionary_unified.json")
SOURCES_PATH = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\sources.json")

# Ensure census_2023_lsi is loaded in default_sources
if not default_sources.contains("census_2023_lsi"):
    from gaddi.models import Source
    default_sources.register(Source(
        id="census_2023_lsi",
        title="Linguistic Survey of India: Himachal Pradesh",
        authors=["Office of the Registrar General, India", "Language Division", "N. Gopalakrishnan"],
        year=2023,
        publisher="Office of the Registrar General, India, New Delhi",
        license="Open Government Data (OGD) License India",
        credibility_tier=1,
        is_jk_primary=False
    ))

with open(DATA_PATH, "r", encoding="utf-8") as f:
    existing_entries = json.load(f)

print(f"Initial entries count: {len(existing_entries)}")
initial_entry_count = len(existing_entries)
initial_unique_headwords = len({e["lemma_devanagari"] for e in existing_entries if e.get("lemma_devanagari")})

# Build lookup by (lemma_devanagari, variety_id)
entry_index = {}
for idx, e in enumerate(existing_entries):
    key = (e["lemma_devanagari"].strip(), e["variety_id"].strip())
    entry_index[key] = idx

# Load extracted comparative lexicon data
with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\scratch\consolidated_comp_lex.json", "r", encoding="utf-8") as f:
    comp_lex = json.load(f)

# Semantic category mapper
def infer_category(gloss):
    g = gloss.lower()
    if any(k in g for k in ["father", "mother", "son", "daughter", "brother", "sister", "wife", "husband", "uncle", "aunt", "nephew", "niece", "bride", "widow", "ancestor", "parent", "baby", "boy", "girl", "child", "friend"]):
        return "family"
    if any(k in g for k in ["head", "hair", "eye", "ear", "nose", "mouth", "lip", "tooth", "tongue", "neck", "hand", "arm", "finger", "foot", "leg", "belly", "heart", "blood", "bone", "skin", "lung", "liver", "spine", "waist", "breast", "chest", "claw", "navel", "moustache", "beard", "fever", "pain", "flesh"]):
        return "body"
    if any(k in g for k in ["cow", "bull", "ox", "calf", "goat", "sheep", "dog", "cat", "horse", "lion", "tiger", "bear", "monkey", "fox", "jackal", "bird", "cock", "hen", "crow", "fish", "frog", "snake", "ant", "fly", "spider", "mouse", "rat", "crab", "tortoise", "cuckoo", "feather", "wing", "tail", "horn", "egg"]):
        return "animals"
    if any(k in g for k in ["tree", "leaf", "root", "flower", "fruit", "grass", "bamboo", "plant", "creeper", "forest", "wood", "seed", "banana", "mango", "apple", "jack fruit", "guava", "melon", "ground nut", "lily"]):
        return "plants"
    if any(k in g for k in ["water", "rain", "river", "stream", "lake", "pond", "sea", "wave", "fog", "cloud", "snow", "ice", "well", "storm", "flood"]):
        return "water"
    if any(k in g for k in ["mountain", "hill", "ridge", "pass", "rock", "stone", "sand", "landscape"]):
        return "mountains"
    if any(k in g for k in ["sky", "sun", "moon", "star", "fire", "smoke", "ashes", "earth", "darkness", "light", "eclipse", "wind", "air", "weather", "season"]):
        return "nature"
    if any(k in g for k in ["food", "rice", "bread", "milk", "salt", "sweet", "ghee", "liquor", "sour", "bitter", "chilly", "brinjal", "potato", "paddy", "garlic", "vegetable"]):
        return "food"
    if any(k in g for k in ["plough", "cultivate", "sow", "reap", "harvest", "field", "graze", "crop", "farm"]):
        return "agriculture"
    if any(k in g for k in ["house", "wall", "door", "window", "roof", "room", "bed", "cloth", "blanket", "tunic", "cord", "shoe", "jar", "frock", "curtain", "furniture", "banian", "cotton"]):
        return "household"
    if any(k in g for k in ["loom", "wheel", "axe", "sickle", "net", "mirror", "stick", "rope", "knife", "potter", "weaver", "moneylender", "labourer", "tool", "trade", "occupation"]):
        return "tools"
    if any(k in g for k in ["road", "path", "walk", "run", "climb", "arrive", "go", "come", "travel", "direction", "east", "north", "south", "far", "near", "out", "down", "bus"]):
        return "travel"
    if any(k in g for k in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "sixteen", "twenty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "first", "second", "third", "half", "quarter", "many", "some", "all", "few", "more"]):
        return "numbers"
    if any(k in g for k in ["black", "white", "red", "green", "yellow", "blue", "brown", "bright", "color"]):
        return "colors"
    if any(k in g for k in ["god", "worship", "temple", "festival", "heaven", "hell", "sacred", "prayer", "shiva"]):
        return "religion"
    if any(k in g for k in ["school", "teacher", "student", "book", "read", "write", "learn", "study"]):
        return "education"
    if any(k in g for k in ["what", "when", "where", "who", "why", "how", "this", "that", "these", "those", "here", "there", "i", "we", "you", "he", "she", "they", "not", "if", "and", "or", "say", "ask", "speak", "call", "shout", "hear"]):
        return "expressions"
    return "general"

def infer_pos(gloss):
    g = gloss.lower()
    if any(g.startswith(v) for v in ["to ", "blow", "break", "burn", "carry", "catch", "clean", "fall", "hold", "lick", "make", "mix", "open", "pick", "hit", "arrive", "play", "pull", "flow", "push", "put", "kill", "sing", "bring", "climb", "come", "drag", "get", "go", "jump", "move", "stand", "take", "walk", "rub", "sell", "shut", "sink", "sprinkle", "squeeze", "spit", "shoot", "split", "fight", "quarrel", "enter", "escape", "fly", "give", "tear", "stab", "throw", "dance", "wash", "wipe", "cut", "dig", "milk", "bark", "drink", "eat", "feed", "write", "run", "send", "slip", "swing", "swim", "vomit", "cultivate", "comb", "graze", "harvest", "lend", "plant", "reap", "sow", "bite", "suck", "tie", "wear", "answer", "hide", "turn", "stop", "swell", "die", "earn", "sit", "change", "freeze", "wet", "know", "think", "cry", "fear", "laugh", "taste", "annoy", "kiss", "love", "bathe", "smell", "touch", "wake", "meet", "repay", "show", "scratch"]):
        return "verb"
    if any(g == adj for adj in ["good", "bad", "tall", "lean", "fat", "dumb", "blind", "thick", "thin", "narrow", "wide", "short", "long", "new", "old", "straight", "smooth", "smart", "far", "near", "wild", "wise", "raw", "rotten", "right", "dull", "sharp", "soft", "ugly", "fast", "black", "blind", "blue", "green", "brown", "bright", "sour", "sweet", "white", "yellow", "hungry", "rich", "miser"]):
        return "adjective"
    if any(g in num for num in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "sixteen", "twenty", "forty", "first", "second", "third", "half", "quarter"]):
        return "numeral"
    if any(g == p for p in ["i", "we", "you", "he", "she", "they", "who", "what", "where", "when", "how", "this", "that", "these", "those"]):
        return "pronoun"
    if any(g == adv for adv in ["daily", "always", "today", "tomorrow", "yesterday", "before", "behind", "after", "again", "loudly", "slowly", "here", "there"]):
        return "adverb"
    if any(g == c for c in ["and", "or", "if", "but"]):
        return "conjunction"
    if any(g == pp for pp in ["in", "at", "for", "from", "between", "down", "out"]):
        return "postposition"
    return "noun"

print("Compiling curated LSI Himachal Pradesh Lexical Entries...")

