import json
import re
from collections import defaultdict

with open(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

# Find entries with identical lemma_devanagari, variety_id, and part_of_speech
candidates = defaultdict(list)
for e in entries:
    lemma = e.get("lemma_devanagari", "").strip()
    var = e.get("variety_id", "")
    pos = (e.get("part_of_speech") or "").lower()
    candidates[(lemma, var, pos)].append(e)

identical_pairs = []
for (lemma, var, pos), group in candidates.items():
    if len(group) > 1:
        # Check if glosses are identical or trivial variants
        glosses = [g["definition_en"].lower().strip(" .;,") for it in group for g in it.get("senses", [])]
        # Check if any two glosses are very close
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                g1 = group[i]["senses"][0]["definition_en"].lower().strip(" .;,")
                g2 = group[j]["senses"][0]["definition_en"].lower().strip(" .;,")
                # Normalize parentheticals
                g1_clean = re.sub(r"\(.*?\)", "", g1).strip()
                g2_clean = re.sub(r"\(.*?\)", "", g2).strip()
                if g1 == g2 or g1_clean == g2_clean or g1 in g2 or g2 in g1:
                    identical_pairs.append((lemma, var, pos, group[i]["id"], group[j]["id"], g1, g2))

print(f"Total candidate exact duplicate pairs: {len(identical_pairs)}")
for p in identical_pairs:
    print(f"  {p[0]} ({p[1]}, {p[2]}): {p[3]} vs {p[4]} -> '{p[5]}' vs '{p[6]}'")
