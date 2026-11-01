import json
from pathlib import Path
from gaddi.dictionary import GaddiDictionary
from gaddi.models import LexicalEntry
from simulate_expansion import all_entries

# Test GaddiDictionary with simulated dataset
d = GaddiDictionary(entries=[], auto_load_defaults=False)
for e in all_entries:
    d._unified_entries.append(LexicalEntry.from_dict(e))

print("Total unified entries in dictionary:", len(d.get_unified_entries()))
print("Total unique headwords:", len(d.get_unique_headwords()))
print("Total records:", d.get_total_records())

# Test searches
res_weather = d.search("weather")
print(f"Search 'weather': {len(res_weather)} results")
for r in res_weather[:5]:
    print(f"  {r.lemma_devanagari} ({r.variety_id}) -> {r.senses[0].definition_en}")

res_bale = d.search("बले बले")
print(f"Search 'बले बले': {len(res_bale)} results")
for r in res_bale:
    print(f"  {r.lemma_devanagari} ({r.variety_id}) -> {r.senses[0].definition_en}")

res_snake = d.search("snake")
print(f"Search 'snake': {len(res_snake)} results")
for r in res_snake[:5]:
    print(f"  {r.lemma_devanagari} ({r.variety_id}) -> {r.senses[0].definition_en}")

res_hindi = d.search("हवा")
print(f"Search Hindi 'हवा': {len(res_hindi)} results")
for r in res_hindi[:5]:
    print(f"  {r.lemma_devanagari} ({r.variety_id}) -> {r.senses[0].definition_en}")

# Test Category Search
for cat in ["animals", "family", "food", "body", "mountains", "water", "household", "tools", "travel", "nature"]:
    cat_res = d.search_by_category(cat)
    print(f"Category '{cat}': {len(cat_res)} entries")

