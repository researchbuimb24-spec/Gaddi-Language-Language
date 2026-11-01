import json

path_data = "data/varieties.json"
path_res = "src/gaddi/resources/varieties.json"

with open(path_data, "r", encoding="utf-8") as f:
    varieties = json.load(f)

existing_ids = {v["id"] for v in varieties}

new_varieties = [
    {
        "id": "jk_bhaderwah_doda",
        "name": "Bhaderwah Gaddi (Doda)",
        "region_type": "tehsil_cluster",
        "state_ut": "Jammu and Kashmir",
        "district": "Doda",
        "sub_areas": ["Bhaderwah", "Assar", "Saraj", "Haddal", "Bharei", "Kansar"],
        "is_jk_variety": True,
        "description": "Gaddi variety spoken in Bhaderwah and Assar tehsils of Doda district, documented by Hilal Ahmad Dar and Aejaz Mohammed Sheikh (2022).",
        "contact_languages": ["Bhaderwahi", "Sarazi", "Kashmiri", "Urdu"]
    },
    {
        "id": "historical_gaddi_unspecified_locality",
        "name": "Historical Gaddi (Unspecified Locality)",
        "region_type": "historical",
        "state_ut": "Pan-Regional",
        "district": "Unspecified",
        "sub_areas": ["Western Himalayas"],
        "is_jk_variety": False,
        "description": "Historical Gaddi records and early survey forms lacking specific village or tehsil attribution.",
        "contact_languages": ["Western Pahari", "Prakrit"]
    },
    {
        "id": "comparative_unlocated",
        "name": "Comparative Gaddi (Unlocated / Mixed)",
        "region_type": "comparative",
        "state_ut": "Pan-Regional",
        "district": "Unlocated",
        "sub_areas": ["Western Pahari belt"],
        "is_jk_variety": False,
        "description": "Comparative lexical items, etymological roots, or pan-regional cognates without specific locality attestation.",
        "contact_languages": ["Western Pahari", "Indo-Aryan"]
    }
]

for nv in new_varieties:
    if nv["id"] not in existing_ids:
        varieties.append(nv)

with open(path_data, "w", encoding="utf-8") as f:
    json.dump(varieties, f, ensure_ascii=False, indent=2)

with open(path_res, "w", encoding="utf-8") as f:
    json.dump(varieties, f, ensure_ascii=False, indent=2)

print(f"Updated varieties. Total: {len(varieties)}")
