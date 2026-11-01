import json
from pathlib import Path

source_entry = {
    "id": "census_2023_lsi",
    "title": "Linguistic Survey of India: Himachal Pradesh",
    "authors": [
        "Language Division, Office of the Registrar General, India",
        "N. Gopalakrishnan",
        "Ranjita Pattanaik"
    ],
    "year": 2023,
    "original_publication_year": 2023,
    "publisher": "Office of the Registrar General, India (ORGI), Ministry of Home Affairs, Government of India, New Delhi",
    "url": "https://censusindia.gov.in/nada/index.php/catalog/45246/download/48953/LSI_HIMACHAL_PRADESH.pdf",
    "variety_id": "hp_chamba_bharmaur",
    "credibility_tier": 1,
    "is_jk_primary": False,
    "evidence_status": "comparative_only",
    "evidence_type": "government_linguistic_survey",
    "forms_count": 500,
    "geographic_coordinates": "32.44, 76.53 (Bharmaur Tehsil, Chamba District, Himachal Pradesh)",
    "underlying_sources": [
        "Fieldwork in B.P.O. Bharmaur Tehsil, District Chamba (Informant: Shri O.P. Verma)"
    ],
    "license": "Open Government Data (OGD) License India",
    "notes": "Official post-independence Linguistic Survey of India (LSI) report for Himachal Pradesh containing Chapter 2 (Bharmauri/Gaddi descriptive grammar, phonology, morphology, syntax, and narrative text, pp. 58-119) and Chapter 6 (Comparative Lexicon across 17 mother tongues including Bharmauri/Gaddi, pp. 1077-1134)."
}

for path in [
    Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\sources.json"),
    Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources\sources.json")
]:
    with open(path, "r", encoding="utf-8") as f:
        sources = json.load(f)
    if not any(s["id"] == "census_2023_lsi" for s in sources):
        sources.append(source_entry)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sources, f, indent=2, ensure_ascii=False)
        print(f"Added census_2023_lsi to {path}")
    else:
        print(f"census_2023_lsi already in {path}")

