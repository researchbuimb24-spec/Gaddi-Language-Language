import json
import re
from pathlib import Path
from gloss_to_hindi import get_hindi_gloss
from lsi_to_devanagari import roman_to_devanagari

# Load Chapter 6 comparative lexicon
with open('consolidated_comp_lex.json', 'r', encoding='utf-8') as f:
    comp_lex = json.load(f)

# Load Chapter 2 full text
with open('chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    ch2_text = f.read()

# Category inference function
def infer_category(gloss):
    g = gloss.lower()
    if any(k in g for k in ["father", "mother", "son", "daughter", "brother", "sister", "wife", "husband", "uncle", "aunt", "nephew", "niece", "bride", "widow", "ancestor", "parent", "baby", "boy", "girl", "child", "friend", "man", "woman", "people"]):
        return "family"
    if any(k in g for k in ["head", "hair", "eye", "ear", "nose", "mouth", "lip", "tooth", "tongue", "neck", "hand", "arm", "finger", "foot", "leg", "belly", "heart", "blood", "bone", "skin", "lung", "liver", "spine", "waist", "breast", "chest", "claw", "navel", "moustache", "beard", "fever", "pain", "flesh", "chin", "elbow", "face", "jaw", "knee", "rib", "shoulder", "sweat", "tears", "thigh", "throat", "thumb", "toe"]):
        return "body"
    if any(k in g for k in ["cow", "bull", "ox", "calf", "goat", "sheep", "dog", "cat", "horse", "lion", "tiger", "bear", "monkey", "fox", "jackal", "bird", "cock", "hen", "crow", "fish", "frog", "snake", "ant", "fly", "spider", "mouse", "rat", "crab", "tortoise", "cuckoo", "feather", "wing", "tail", "horn", "egg", "mosquito", "pig", "wolf"]):
        return "animals"
    if any(k in g for k in ["tree", "leaf", "leaves", "root", "flower", "fruit", "grass", "bamboo", "plant", "creeper", "forest", "wood", "seed", "banana", "mango", "apple", "jack fruit", "guava", "melon", "ground nut", "lily", "thorn", "grape", "coconut"]):
        return "plants"
    if any(k in g for k in ["water", "rain", "river", "stream", "lake", "pond", "sea", "wave", "fog", "cloud", "snow", "ice", "well", "storm", "flood"]):
        return "water"
    if any(k in g for k in ["mountain", "hill", "ridge", "pass", "rock", "stone", "sand", "landscape"]):
        return "mountains"
    if any(k in g for k in ["sky", "sun", "moon", "star", "fire", "smoke", "ashes", "earth", "darkness", "light", "eclipse", "wind", "air", "weather", "season", "flame", "lightning", "shade", "shadow", "thunder"]):
        return "nature"
    if any(k in g for k in ["food", "rice", "bread", "milk", "salt", "sweet", "ghee", "liquor", "sour", "bitter", "chilly", "brinjal", "potato", "paddy", "garlic", "vegetable", "butter", "honey", "meat", "flour", "onion", "oil", "pea", "tea", "wheat"]):
        return "food"
    if any(k in g for k in ["plough", "cultivate", "sow", "reap", "harvest", "field", "graze", "crop", "farm", "barn"]):
        return "agriculture"
    if any(k in g for k in ["house", "wall", "door", "window", "roof", "room", "bed", "cloth", "clothing", "blanket", "tunic", "cord", "shoe", "jar", "frock", "curtain", "furniture", "banian", "cotton", "pot", "ring", "shirt", "wool"]):
        return "household"
    if any(k in g for k in ["loom", "wheel", "axe", "sickle", "net", "mirror", "stick", "rope", "knife", "potter", "weaver", "moneylender", "labourer", "tool", "trade", "occupation", "cart", "flute", "needle", "club"]):
        return "tools"
    if any(k in g for k in ["road", "path", "walk", "run", "climb", "arrive", "go", "come", "travel", "direction", "east", "north", "south", "west", "far", "near", "out", "down", "bus", "move", "journey", "village", "town"]):
        return "travel"
    if any(k in g for k in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "first", "second", "third", "half", "quarter", "many", "some", "all", "few", "more", "hour", "day", "night", "month", "year", "week", "noon", "today", "tomorrow", "yesterday"]):
        return "numbers"
    if any(k in g for k in ["black", "white", "red", "green", "yellow", "blue", "brown", "bright", "color", "round"]):
        return "colors"
    if any(k in g for k in ["god", "worship", "temple", "festival", "heaven", "hell", "sacred", "prayer", "shiva"]):
        return "religion"
    if any(k in g for k in ["school", "teacher", "student", "book", "read", "write", "learn", "study"]):
        return "education"
    if any(k in g for k in ["what", "when", "where", "who", "why", "how", "this", "that", "these", "those", "here", "there", "i", "we", "you", "he", "she", "they", "not", "if", "and", "or", "say", "ask", "speak", "call", "shout", "hear"]):
        return "expressions"
    return "general"

def infer_pos(gloss, word=""):
    g = gloss.lower().strip()
    if ' ' in word.strip() or ' ' in g or any(g.startswith(p) for p in ["come from", "do not", "be silent", "open eyes", "kneel down", "he stays"]):
        return "phrase"
    if any(g.startswith(v) for v in ["to ", "blow", "break", "burn", "carry", "catch", "clean", "fall", "hold", "lick", "make", "mix", "open", "pick", "hit", "arrive", "play", "pull", "flow", "push", "put", "kill", "sing", "bring", "climb", "come", "drag", "get", "go", "jump", "move", "stand", "take", "walk", "rub", "sell", "shut", "sink", "sprinkle", "squeeze", "spit", "shoot", "split", "fight", "quarrel", "enter", "escape", "fly", "give", "tear", "stab", "throw", "dance", "wash", "wipe", "cut", "dig", "milk", "bark", "drink", "eat", "feed", "write", "run", "send", "slip", "swing", "swim", "vomit", "cultivate", "comb", "graze", "harvest", "lend", "plant", "reap", "sow", "bite", "suck", "tie", "wear", "answer", "hide", "turn", "stop", "swell", "die", "earn", "sit", "change", "freeze", "wet", "know", "think", "cry", "fear", "laugh", "taste", "annoy", "kiss", "love", "bathe", "smell", "touch", "wake", "meet", "repay", "show", "scratch", "act", "believe", "choose", "cook", "count", "drop", "follow", "hang", "keep", "mend", "pound", "refuse", "say", "see", "sleep", "swallow", "wait"]):
        return "verb"
    if any(g == adj for adj in ["good", "bad", "tall", "lean", "fat", "dumb", "blind", "thick", "thin", "narrow", "wide", "short", "long", "new", "old", "straight", "smooth", "smart", "far", "near", "wild", "wise", "raw", "rotten", "right", "dull", "sharp", "soft", "ugly", "fast", "black", "blind", "blue", "green", "brown", "bright", "sour", "sweet", "white", "yellow", "hungry", "rich", "miser", "cold", "hot", "dry", "dirty", "empty", "heavy", "little", "quick", "ripe", "round", "shy", "strong", "true", "young"]):
        return "adjective"
    if any(g in num for num in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "first", "second", "third", "half", "quarter"]):
        return "numeral"
    if any(g == p for p in ["i", "we", "you", "he", "she", "they", "who", "what", "where", "when", "how", "this", "that", "these", "those", "self", "some"]):
        return "pronoun"
    if any(g == adv for adv in ["daily", "always", "today", "tomorrow", "yesterday", "before", "behind", "after", "again", "loudly", "slowly", "here", "there", "early", "now", "sharply", "yet"]):
        return "adverb"
    if any(g == c for c in ["and", "or", "if", "but"]):
        return "conjunction"
    if any(g == pp for pp in ["in", "at", "for", "from", "between", "down", "out", "under", "up"]):
        return "postposition"
    return "noun"

print("Helper functions ready.")

