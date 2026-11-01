import json

path_data = "data/sources.json"
path_res = "src/gaddi/resources/sources.json"

with open(path_data, "r", encoding="utf-8") as f:
    sources = json.load(f)

existing_ids = {s.get("id") for s in sources}

new_sources = [
    {
        "id": "dar_sheikh_2022",
        "title": "Gaddi Speech Community of Jammu and Kashmir: The Self-Claimed Descendants of Lord Shiva",
        "authors": [
            "Hilal Ahmad Dar",
            "Aejaz Mohammed Sheikh"
        ],
        "year": 2022,
        "journal": "Aligarh Journal of Linguistics",
        "volume": "11 (2021-2022)",
        "publisher": "Department of Linguistics, Aligarh Muslim University, Aligarh",
        "issn": "2249-1511",
        "variety_id": "jk_bhaderwah_doda",
        "credibility_tier": 1,
        "is_jk_primary": True,
        "evidence_type": "fieldwork_sociolinguistic_vocabulary",
        "access_status": "source_metadata_only",
        "notes": "Fieldwork-based sociolinguistic and lexical survey in Bhaderwah and Assar (Doda district, J&K), documenting community folklore, basic vocabulary, and kinship terminology. Print journal issue; full text not exposed in open-access PDF; acquisition requires institutional request to AMU Department of Linguistics."
    },
    {
        "id": "dar_2022_thesis",
        "title": "Phonological and Morphological Analysis of Gaddi Language: A Descriptive Study",
        "authors": [
            "Hilal Ahmad Dar"
        ],
        "supervisor": "Prof. Aejaz Mohammed Sheikh",
        "year": 2022,
        "publisher": "Department of Linguistics, University of Kashmir, Srinagar",
        "degree": "Ph.D. Dissertation (142 pp.)",
        "glottolog_id": "dar2022phonological",
        "variety_id": "jk_bhaderwah_doda",
        "locality": "Assar and Bhaderwah tehsils, District Doda, Jammu and Kashmir",
        "credibility_tier": 1,
        "is_jk_primary": True,
        "evidence_type": "descriptive_grammar_phonology_morphology",
        "access_status": "institutional_thesis_repository",
        "notes": "First dedicated descriptive linguistic dissertation on Jammu & Kashmir Gaddi as spoken in Doda district (Assar and Bhaderwah). Cataloged on Glottolog. Departmental holding at University of Kashmir."
    },
    {
        "id": "jambu_cdial_gaddi",
        "title": "Jambu: A Digital Comparative Dictionary of the Indo-Aryan Languages (Gaddi Reflexes)",
        "authors": [
            "Sir Ralph Lilley Turner",
            "Jambu Project (moli-mandala)"
        ],
        "year": 2024,
        "original_publication_year": 1966,
        "publisher": "Digital CLDF database (moli-mandala / Oxford University Press)",
        "url": "https://neojambu.herokuapp.com/languages/ga",
        "variety_id": "comparative_historical",
        "credibility_tier": 1,
        "is_jk_primary": False,
        "evidence_status": "comparative_only",
        "evidence_type": "etymological_dictionary_reflexes",
        "forms_count": 1118,
        "geographic_coordinates": "32.36, 76.57 (Bharmaur, Chamba, Himachal Pradesh)",
        "underlying_sources": [
            "T. Grahame Bailey (1908), The Languages of the Northern Himalayas",
            "Sir George A. Grierson (1916), Linguistic Survey of India, Vol. IX, Part IV"
        ],
        "license": "Database code MIT; source dictionary text subject to copyright (OUP / SOAS)",
        "notes": "Reports 1,118 historical Indo-Aryan etymological reflexes for Gaddi (code ga). Audit confirms coordinates map to Bharmaur, Himachal Pradesh, and underlying data derives from Bailey (1908) and Grierson (1916). Exactly zero forms originate from Jammu & Kashmir. Quarantined as comparative_only."
    }
]

for ns in new_sources:
    if ns["id"] not in existing_ids:
        sources.append(ns)

with open(path_data, "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

with open(path_res, "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

print(f"Updated sources. Total: {len(sources)}")
