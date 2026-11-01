from gloss_to_hindi import get_hindi_gloss
from pathlib import Path

path = Path(__file__).parent / "all_unique_glosses.txt"
with open(path, 'r', encoding='utf-8') as f:
    glosses = [l.strip() for l in f if l.strip()]

unmapped = [g for g in glosses if get_hindi_gloss(g) == g]
print(f"Total unmapped: {len(unmapped)}")
for u in unmapped:
    print(f"    '{u}': '',")

