import json
import re
from pathlib import Path

data_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
with open(data_path, "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Initial entries: {len(entries)}")

# List of exact duplicate pairs to merge: (keep_id, merge_id)
# Only merge when clearly the exact same lexical item in the exact same variety and POS
merge_pairs = [
    ("gaddi-uni-00032", "gaddi-uni-00477"), # पाणी (water)
    ("gaddi-uni-00035", "gaddi-uni-00949"), # रात (night)
    ("gaddi-uni-00036", "gaddi-uni-00256"), # रुख (tree)
    ("gaddi-uni-00050", "gaddi-uni-00273"), # कुण (who)
    ("gaddi-uni-00072", "gaddi-uni-01011"), # खूण (blood)
    ("gaddi-uni-00075", "gaddi-uni-01014"), # हडड (bone)
    ("gaddi-uni-00106", "gaddi-uni-01033"), # मीँझ (fat, grease)
    ("gaddi-uni-00109", "gaddi-uni-01035"), # डर (fear)
    ("gaddi-uni-00113", "gaddi-uni-01040"), # मछलि (fish)
    ("gaddi-uni-00162", "gaddi-uni-01076"), # जूँ (louse)
    ("gaddi-uni-00165", "gaddi-uni-01079"), # मड़द (male)
    ("gaddi-uni-00168", "gaddi-uni-01082"), # चनदणि (moon)
    ("gaddi-uni-00170", "gaddi-uni-01084"), # हपपड़ (mountain)
    ("gaddi-uni-00176", "gaddi-uni-01089"), # कैड़ि (neck)
    ("gaddi-uni-00185", "gaddi-uni-01096"), # मणु (person)
    ("gaddi-uni-00195", "gaddi-uni-01103"), # सड़क (road)
    ("gaddi-uni-00196", "gaddi-uni-01104"), # जड़ (root)
    ("gaddi-uni-00201", "gaddi-uni-01108"), # लु:ण (salt)
    ("gaddi-uni-00215", "gaddi-uni-01115"), # चमड़ि (skin)
    ("gaddi-uni-00219", "gaddi-uni-01117"), # मुसक (smell)
    ("gaddi-uni-00235", "gaddi-uni-01129"), # नड़ (stone)
    ("gaddi-uni-00238", "gaddi-uni-01132"), # सुरज (sun)
    ("gaddi-uni-00260", "gaddi-uni-01142"), # उलटि (vomit)
    ("gaddi-uni-00284", "gaddi-uni-01158"), # बड़ि (year)
    ("gaddi-uni-00287", "gaddi-uni-01160"), # ओडण (clothing)
    ("gaddi-uni-00303", "gaddi-uni-01171"), # मिनडि (braid)
    ("gaddi-uni-00342", "gaddi-uni-00479"), # घोड़ा (horse)
    ("gaddi-uni-00637", "gaddi-uni-00790"), # गुगुन (bark)
    ("gaddi-uni-00065", "gaddi-uni-01006"), # कजोकि (because)
    ("gaddi-uni-00074", "gaddi-uni-01013"), # फुक (blow)
]

entries_by_id = {e["id"]: e for e in entries}
discard_ids = set()

for keep_id, merge_id in merge_pairs:
    if keep_id in entries_by_id and merge_id in entries_by_id:
        target = entries_by_id[keep_id]
        source = entries_by_id[merge_id]
        
        # Merge attestations
        existing_att = {(a["source_id"], a.get("page_or_section", ""), a.get("source_spelling", "")) for a in target.get("attestations", [])}
        for a in source.get("attestations", []):
            sig = (a["source_id"], a.get("page_or_section", ""), a.get("source_spelling", ""))
            if sig not in existing_att:
                target.setdefault("attestations", []).append(a)
                existing_att.add(sig)

        # Merge metadata
        t_meta = target.setdefault("metadata", {})
        s_meta = source.get("metadata", {})

        # Variants
        t_vars = set(t_meta.get("variants", []))
        for v in s_meta.get("variants", []):
            if v and v not in t_vars:
                t_meta.setdefault("variants", []).append(v)
                t_vars.add(v)

        # Example IDs
        t_ex = set(t_meta.get("example_ids", []))
        for ex in s_meta.get("example_ids", []):
            if ex and ex not in t_ex:
                t_meta.setdefault("example_ids", []).append(ex)
                t_ex.add(ex)

        # Categories
        t_cats = set(t_meta.get("categories", []))
        for c in s_meta.get("categories", []):
            if c and c not in t_cats:
                t_meta.setdefault("categories", []).append(c)
                t_cats.add(c)

        # Translations
        t_trans = t_meta.setdefault("translations", {})
        for lang_k, lang_v in s_meta.get("translations", {}).items():
            if lang_k not in t_trans or not t_trans[lang_k]:
                t_trans[lang_k] = lang_v

        # Senses definitions
        t_senses = target.setdefault("senses", [])
        if t_senses and source.get("senses"):
            s_first = source["senses"][0]
            if not t_senses[0].get("definition_hi") and s_first.get("definition_hi"):
                t_senses[0]["definition_hi"] = s_first["definition_hi"]
            if not t_senses[0].get("definition_ur") and s_first.get("definition_ur"):
                t_senses[0]["definition_ur"] = s_first["definition_ur"]

        # Preserve IPA if target missing
        if not target.get("lemma_ipa") and source.get("lemma_ipa"):
            target["lemma_ipa"] = source["lemma_ipa"]

        discard_ids.add(merge_id)

merged_entries = [e for e in entries if e["id"] not in discard_ids]
print(f"Entries after merging {len(discard_ids)} duplicates: {len(merged_entries)}")
