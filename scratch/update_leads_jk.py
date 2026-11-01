import json

path_data = "data/research_leads.json"
path_res = "src/gaddi/resources/research_leads.json"

with open(path_data, "r", encoding="utf-8") as f:
    leads = json.load(f)

lead_map = {l.get("lead_id"): l for l in leads}

# Update lead-grierson-lsi-1916
if "lead-grierson-lsi-1916" in lead_map:
    l_grier = lead_map["lead-grierson-lsi-1916"]
    l_grier["lsi_exact_pages"] = "Vol. IX, Part IV, pp. 790-833 (Gadi or Bharmauri); Vol. I, Part II (1928, Comparative Vocabulary, 168 standard words); Vol. XI (1922, Gipsy Languages)"
    l_grier["elicitation_locality"] = "Brahmaur, Chamba State, Himachal Pradesh"
    l_grier["jammu_relevance_audit"] = "Documents the border transhumance zone between Chamba/Kangra and the Jammu hills (Bhadarwah, Padar, Kathua). All linguistic text specimens (Prodigal Son, folktale, wordlist) were collected in Brahmaur (Chamba). Quarantined as comparative_historical."

# Update lead-kaul-2006
if "lead-kaul-2006" in lead_map:
    l_kaul = lead_map["lead-kaul-2006"]
    l_kaul["volume_1_vs_volume_2_audit"] = {
        "volume_1_linguistic_survey": "Contains UGC research project fieldwork, classification of Jammu mountain speech, and chapters on tribal dialects (Gojri, Bakerwali, Gaddi, Watali, Cinnali). Systematic lexical wordlist vs narrative survey remains open until physical inspection.",
        "volume_2_reference_compendium": "Contains monographs on Padri, Bhalesi, and a Glossary of Cinali (Chinali). Confirmed: Volume 2 contains ZERO Gaddi vocabulary.",
        "digital_access_audit": "Google Books ID pHZOAQAAIAAJ is restricted snippet view; zero readable scans exposed.",
        "physical_inspection_routes": "Dhanvantri Library (University of Jammu), National Library of India (Kolkata), Library of Congress."
    }

# New lead 1: Dar and Sheikh (2022) / Dar (2022 dissertation)
new_lead_dar = {
    "lead_id": "lead-dar-sheikh-2022",
    "title": "Gaddi Speech Community of Jammu and Kashmir: The Self-Claimed Descendants of Lord Shiva",
    "authors": [
        "Hilal Ahmad Dar",
        "Aejaz Mohammed Sheikh"
    ],
    "year": 2022,
    "institution_or_publisher": "Department of Linguistics, Aligarh Muslim University (Aligarh Journal of Linguistics, Vol. 11, 2021-2022)",
    "thesis_connection": "Ph.D. Dissertation: 'Phonological and Morphological Analysis of Gaddi Language: A Descriptive Study' (142 pp., Department of Linguistics, University of Kashmir, 2022; Supervised by Prof. Aejaz Mohammed Sheikh; Glottolog: spoken in Assar and Bhaderwah areas of District Doda)",
    "geographical_coverage": "Assar and Bhaderwah tehsils, District Doda, Jammu & Kashmir",
    "variety_id": "jk_bhaderwah_doda",
    "is_jk_primary": True,
    "evidence_type": "fieldwork_sociolinguistic_vocabulary",
    "status": "institutional_archive_inquiry_needed",
    "digital_access_status": "source_metadata_only",
    "priority_level": "Tier 1 (Highest Priority J&K Primary Source)",
    "linguistic_value": "First modern descriptive linguistic and sociolinguistic field study dedicated specifically to the Gaddi speech community in Jammu & Kashmir (Doda district). Documents community folklore of Shaivite descent, basic vocabulary, and kinship terminology.",
    "access_reality": "Published in print (ISSN: 2249-1511). AMU portal indexes Volume 11 (2021-2022) in its journal archives but does not provide an open-access full-text PDF download. The 142-page Kashmir University dissertation is cataloged on Glottolog and NDLI but not yet public on Shodhganga. Full text not accessible on open web; zero guessed entries permitted.",
    "actionable_acquisition_plan": "1. Submit formal article reprint request to Editor-in-Chief, Aligarh Journal of Linguistics, AMU. 2. Submit dissertation access request to Department of Linguistics / Allama Iqbal Library, University of Kashmir. 3. Direct academic correspondence with authors Dr. Hilal Ahmad Dar (SPPEL/CIIL Mysuru) and Prof. Aejaz Mohammed Sheikh (University of Kashmir)."
}

# New lead 2: Jambu Gaddi Lexicon (1,118 forms)
new_lead_jambu = {
    "lead_id": "lead-jambu-gaddi-cdial",
    "title": "Jambu Gaddi Lexical Dataset (1,118 Forms)",
    "authors": [
        "Sir Ralph Lilley Turner",
        "Jambu Project (moli-mandala)"
    ],
    "year": 2024,
    "institution_or_publisher": "Digital CLDF database (https://neojambu.herokuapp.com/languages/ga)",
    "underlying_source": "Sir Ralph Lilley Turner (1966), Comparative Dictionary of the Indo-Aryan Languages (CDIAL), Oxford University Press",
    "geographical_provenance": "Coordinates: 32.36, 76.57 (Bharmaur, Chamba, Himachal Pradesh)",
    "variety_id": "comparative_historical",
    "is_jk_primary": False,
    "status": "accessible_comparative_only",
    "digital_access_status": "fully_accessible_comparative",
    "provenance_audit_finding": "The 1,118 forms indexed under Gaddi in Jambu derive strictly from British colonial surveys: Rev. T. Grahame Bailey (1908, The Languages of the Northern Himalayas, Chamba and Kangra Gaddi) and Sir George A. Grierson (1916, LSI Vol. IX, Part IV, Brahmaur Gadi). EXACTLY ZERO of the 1,118 forms originate from Jammu & Kashmir. Quarantined as comparative_only to prevent conflation.",
    "licensing": "Application code open-source MIT; underlying CDIAL etymological text subject to copyright (OUP / SOAS London)."
}

if "lead-dar-sheikh-2022" not in lead_map:
    leads.append(new_lead_dar)
else:
    lead_map["lead-dar-sheikh-2022"].update(new_lead_dar)

if "lead-jambu-gaddi-cdial" not in lead_map:
    leads.append(new_lead_jambu)
else:
    lead_map["lead-jambu-gaddi-cdial"].update(new_lead_jambu)

with open(path_data, "w", encoding="utf-8") as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)

with open(path_res, "w", encoding="utf-8") as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)

print(f"Updated research_leads. Total: {len(leads)}")
