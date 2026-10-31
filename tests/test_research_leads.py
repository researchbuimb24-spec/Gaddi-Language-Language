"""Tests for primary linguistic research leads and archival source discovery."""

import json
from pathlib import Path
import pytest

import gaddi
from gaddi.models import ResearchLead
from gaddi.registry import default_leads


def test_research_leads_json_files_exist_and_match():
    """Verify data/research_leads.json and packaged resources are present and identical."""
    root = Path(__file__).parents[1]
    data_file = root / "data" / "research_leads.json"
    res_file = root / "src" / "gaddi" / "resources" / "research_leads.json"

    assert data_file.exists(), f"Missing {data_file}"
    assert res_file.exists(), f"Missing {res_file}"

    with open(data_file, "r", encoding="utf-8") as f1, open(res_file, "r", encoding="utf-8") as f2:
        d1 = json.load(f1)
        d2 = json.load(f2)

    assert d1 == d2, "data/research_leads.json and resources/research_leads.json must be identical"


def test_research_lead_registry_defaults():
    """Verify that default_leads registry loads all leads properly."""
    assert len(default_leads) >= 15

    lead_ids = {l.lead_id for l in default_leads.list_all()}
    assert "lead-kaul-2006" in lead_ids
    assert "lead-plsi-vol12-jk" in lead_ids
    assert "lead-plsi-vol11-hp" in lead_ids
    assert "lead-ucl-grammar-2026" in lead_ids
    assert "lead-grierson-lsi-1916" in lead_ids
    assert "lead-shodhganga-ashwani-2014" in lead_ids
    assert "lead-shodhganga-linguistics-survey" in lead_ids
    assert "lead-ciil-ldcil-bharmauri" in lead_ids
    assert "lead-jkaacl-sheeraza-archives" in lead_ids
    assert "lead-univ-jammu-dogri-ling" in lead_ids


def test_lead_schema_and_types():
    """Verify every registered research lead adheres to required schema fields and types."""
    leads = default_leads.list_all()
    required_fields = [
        "lead_id",
        "title",
        "authors_or_institution",
        "year",
        "publisher_or_archive",
        "geographic_scope",
        "variety_coverage",
        "contains_linguistic_data",
        "data_type",
        "lexical_content_type",
        "status",
        "full_source_accessible",
        "evidence_evaluation",
        "actionable_next_steps",
    ]

    for lead in leads:
        lead_dict = lead.to_dict()
        for field_name in required_fields:
            assert field_name in lead_dict, f"Missing field '{field_name}' in lead {lead.lead_id}"
            assert lead_dict[field_name] is not None, f"Field '{field_name}' is None in lead {lead.lead_id}"

        assert isinstance(lead.lead_id, str) and lead.lead_id.startswith("lead-")
        assert isinstance(lead.title, str) and len(lead.title) > 0
        assert isinstance(lead.authors_or_institution, list) and len(lead.authors_or_institution) > 0
        assert isinstance(lead.contains_linguistic_data, bool)
        assert isinstance(lead.full_source_accessible, bool)
        assert isinstance(lead.evidence_evaluation, str) and len(lead.evidence_evaluation) > 10
        assert isinstance(lead.actionable_next_steps, str) and len(lead.actionable_next_steps) > 5


def test_anti_conflation_and_negative_findings():
    """Verify key negative findings and anti-conflation safeguards in research leads."""
    # 1. P. K. Kaul (2006) requires physical library inspection; cannot be claimed as accessible
    kaul = default_leads.get("lead-kaul-2006")
    assert kaul is not None
    assert kaul.contains_linguistic_data is True
    assert kaul.full_source_accessible is False
    assert kaul.status == "inaccessible_requires_physical_library_inspection"
    assert "University of Jammu" in kaul.actionable_next_steps or "Sahitya Akademi" in kaul.actionable_next_steps

    # 2. PLSI Volume 12 (J&K) must record the negative finding: Gaddi was omitted from J&K volume
    plsi12 = default_leads.get("lead-plsi-vol12-jk")
    assert plsi12 is not None
    assert plsi12.contains_linguistic_data is False
    assert "omitted" in plsi12.evidence_evaluation.lower()

    # 3. UCL Press 2026 grammar must be comparative only
    ucl = default_leads.get("lead-ucl-grammar-2026")
    assert ucl is not None
    assert ucl.status == "accessible_comparative_only"
    assert "CC BY-NC 4.0" in ucl.license_or_rights

    # 4. Ashwani Kumar 2014 thesis must be marked non-linguistic (sociological)
    ashwani = default_leads.get("lead-shodhganga-ashwani-2014")
    assert ashwani is not None
    assert ashwani.contains_linguistic_data is False
    assert ashwani.status == "evaluated_non_linguistic"

    # 5. Shodhganga Linguistics Survey confirms 0 linguistic dissertations on J&K Gaddi
    survey = default_leads.get("lead-shodhganga-linguistics-survey")
    assert survey is not None
    assert "zero" in survey.evidence_evaluation.lower()


def test_public_api_list_research_leads():
    """Verify gaddi.list_research_leads() functional API."""
    all_leads = gaddi.list_research_leads()
    assert len(all_leads) == len(default_leads)

    # Filter by status
    comp_leads = gaddi.list_research_leads(status="accessible_comparative_only")
    assert len(comp_leads) >= 4
    for l in comp_leads:
        assert l.status == "accessible_comparative_only"

    # Leads with linguistic data
    ling_leads = default_leads.get_with_linguistic_data()
    assert len(ling_leads) >= 5
    for l in ling_leads:
        assert l.contains_linguistic_data is True


def test_command_5_enhanced_verification_fields():
    """Verify that all leads possess Command 5 enhanced verification fields."""
    leads = default_leads.list_all()
    for lead in leads:
        assert isinstance(lead.bibliographic_verified, bool)
        assert isinstance(lead.contents_verified, bool)
        assert isinstance(lead.full_text_accessible, bool)
        assert isinstance(lead.varieties_documented, list)
        assert isinstance(lead.relevant_pages, str) and len(lead.relevant_pages) > 0
        assert isinstance(lead.linguistic_data_type, str) and len(lead.linguistic_data_type) > 0
        assert isinstance(lead.access_status, str) and len(lead.access_status) > 0
        assert isinstance(lead.verification_notes, str) and len(lead.verification_notes) > 0


def test_kaul_2006_detailed_bibliographic_verification():
    """Verify exact bibliographic and contents findings for Dr. P. K. Kaul (2006)."""
    kaul = default_leads.get("lead-kaul-2006")
    assert kaul is not None
    assert kaul.bibliographic_verified is True
    assert kaul.contents_verified is True
    assert kaul.full_text_accessible is False
    assert "9788178541006" in kaul.identifier_or_url or "978-81-7854-100-6" in kaul.identifier_or_url
    assert "Padri" in kaul.varieties_documented
    assert "Cinali" in kaul.varieties_documented or "Cinali (Chinali)" in kaul.varieties_documented
    # Volume 2 must be documented as containing Cinali glossary and Padri/Bhalesi texts, NOT Gaddi dictionary
    assert "Cinali" in kaul.verification_notes
    assert "NOT a standalone Gaddi dictionary" in kaul.verification_notes or "not a standalone gaddi dictionary" in kaul.verification_notes.lower()


def test_ucl_press_2026_doi_and_license_verification():
    """Verify that UCL Press 2026 grammar has the corrected official DOI and CC BY-NC 4.0 license."""
    ucl = default_leads.get("lead-ucl-grammar-2026")
    assert ucl is not None
    assert ucl.bibliographic_verified is True
    assert ucl.contents_verified is True
    assert ucl.full_text_accessible is True
    assert "10.14324/111.9781800089938" in ucl.identifier_or_url
    assert "CC BY-NC 4.0" in ucl.license_or_rights
    assert "Third-party" in ucl.license_or_rights or "third-party" in ucl.license_or_rights.lower()


def test_plsi_vol12_comparative_contact_coverage():
    """Verify that PLSI Volume 12 is verified with Orient Blackswan TOC and contact languages."""
    plsi12 = default_leads.get("lead-plsi-vol12-jk")
    assert plsi12 is not None
    assert plsi12.bibliographic_verified is True
    assert plsi12.contents_verified is True
    assert plsi12.full_text_accessible is False
    assert "9788125055174" in plsi12.identifier_or_url
    # Verifies presence of neighboring Western Pahari contact varieties
    assert "Bhadrawahi" in plsi12.varieties_documented
    assert "Siraji" in plsi12.varieties_documented
    assert "Dogri" in plsi12.varieties_documented
    # Confirms Gaddi omission from J&K volume is recorded
    assert "omitted" in plsi12.evidence_evaluation.lower()
    # Confirms comparative value is recognized
    assert "comparative" in plsi12.evidence_evaluation.lower()


def test_kaul_2006_library_holdings_and_identifiers():
    """Command 7-8: Verify Kaul (2006) identifiers, Google Books snippet access, and unconfirmed shelf status."""
    kaul = default_leads.get("lead-kaul-2006")
    assert kaul is not None
    assert "2006448331" in kaul.identifier_or_url
    assert "77713834" in kaul.identifier_or_url
    assert "PK2610.J35 K38 2006" in kaul.identifier_or_url
    assert "pHZOAQAAIAAJ" in kaul.identifier_or_url
    assert "snippet" in kaul.access_status.lower() and ("pages_unverified" in kaul.access_status.lower() or "inaccessible" in kaul.access_status.lower())
    assert kaul.digitized_record_found is True
    assert kaul.preview_available is True
    assert kaul.relevant_pages_accessible is False
    assert kaul.full_text_accessible is False
    assert kaul.evidence_claim_tier == "publisher_or_catalogue_verified"

    notes = kaul.verification_notes
    assert "Dhanvantri Central Library" in notes or "University of Jammu" in notes
    assert "Sahitya Akademi Library" in notes
    assert "National Library of India" in notes
    assert "Library of Congress" in notes
    # Unconfirmed physical holdings must be classified as requiring institutional confirmation
    assert "institutional_confirmation_required" in notes or "institutional confirmation required" in notes.lower()
    # Digital access audit notes must record snippet view and lack of full page access
    assert "Snippet view" in notes or "snippet view" in notes.lower()


def test_kaul_2006_volume_1_and_inspection_checklist():
    """Command 7: Verify Volume 1 specific targeting and proposed inspection procedure."""
    kaul = default_leads.get("lead-kaul-2006")
    assert kaul is not None
    assert "Vol. 1" in kaul.relevant_pages
    assert "Vol. 2" in kaul.relevant_pages
    # Volume 1 cannot be inferred from Volume 2
    assert "cannot be inferred" in kaul.evidence_evaluation.lower()

    steps = kaul.actionable_next_steps
    assert "Dhanvantri Central Library" in steps or "Sahitya Akademi" in steps
    assert "Vol. 1" in steps
    assert "6-point extraction gate" in steps
    assert "fair dealing" in steps.lower()


def test_institutional_leads_demarcation_of_confirmed_vs_inquiry():
    """Command 7: Verify strict demarcation between confirmed holdings and suggestions for inquiry."""
    target_ids = ["lead-ciil-ldcil-bharmauri", "lead-jkaacl-sheeraza-archives", "lead-univ-jammu-dogri-ling"]
    for lead_id in target_ids:
        lead = default_leads.get(lead_id)
        assert lead is not None, f"Missing {lead_id}"
        eval_text = lead.evidence_evaluation
        assert "CONFIRMED" in eval_text or "VERIFIED" in eval_text, f"Missing CONFIRMED in {lead_id}"
        assert "INSTITUTIONAL CONFIRMATION REQUIRED" in eval_text or "SUGGESTIONS FOR INQUIRY" in eval_text, f"Missing INQUIRY in {lead_id}"


def test_evidence_claim_tiers_and_downgrades():
    """Command 7: Verify evidence claim tier vocabulary and downgraded claims."""
    valid_tiers = {
        "primary_source_verified",
        "publisher_or_catalogue_verified",
        "secondary_source_reported",
        "institutional_confirmation_required",
        "not_located_in_search",
        "unverified_or_removed",
    }
    leads = default_leads.list_all()
    for lead in leads:
        assert hasattr(lead, "evidence_claim_tier"), f"Missing evidence_claim_tier on {lead.lead_id}"
        assert lead.evidence_claim_tier in valid_tiers, f"Invalid tier '{lead.evidence_claim_tier}' on {lead.lead_id}"

    # Shodhganga Linguistics Survey must be classified as not_located_in_search
    shodh = default_leads.get("lead-shodhganga-linguistics-survey")
    assert shodh is not None
    assert shodh.evidence_claim_tier == "not_located_in_search"

    # Univ Jammu Dogri theses must be classified as institutional_confirmation_required
    uj = default_leads.get("lead-univ-jammu-dogri-ling")
    assert uj is not None
    assert uj.evidence_claim_tier == "institutional_confirmation_required"

    # UCL Press grammar is primary_source_verified
    ucl = default_leads.get("lead-ucl-grammar-2026")
    assert ucl is not None
    assert ucl.evidence_claim_tier == "primary_source_verified"


def test_digital_access_status_vocabulary():
    """Command 7: Verify digital access status flags and precise definitions."""
    leads = default_leads.list_all()
    for lead in leads:
        assert isinstance(lead.digitized_record_found, bool)
        assert isinstance(lead.preview_available, bool)
        assert isinstance(lead.relevant_pages_accessible, bool)
        assert isinstance(lead.full_text_accessible, bool)

    # Kaul 2006 has digitized record and snippet preview, but pages and full text are inaccessible
    kaul = default_leads.get("lead-kaul-2006")
    assert kaul is not None
    assert kaul.digitized_record_found is True
    assert kaul.preview_available is True
    assert kaul.relevant_pages_accessible is False
    assert kaul.full_text_accessible is False

    # UCL Press 2026 is fully accessible
    ucl = default_leads.get("lead-ucl-grammar-2026")
    assert ucl is not None
    assert ucl.digitized_record_found is True
    assert ucl.preview_available is True
    assert ucl.relevant_pages_accessible is True
    assert ucl.full_text_accessible is True

    # PLSI Vol 12 has no digitized open access record
    plsi = default_leads.get("lead-plsi-vol12-jk")
    assert plsi is not None
    assert plsi.digitized_record_found is False
    assert plsi.preview_available is False
    assert plsi.relevant_pages_accessible is False
    assert plsi.full_text_accessible is False


def test_command_8_acquisition_artifacts_and_enquiry_drafts():
    """Command 8: Verify acquisition worksheet templates and institutional enquiry drafts."""
    root = Path(__file__).parents[1]
    csv_template = root / "docs" / "physical_inspection_worksheet_template.csv"
    guide_doc = root / "docs" / "physical_inspection_worksheet_guide.md"
    drafts_doc = root / "docs" / "institutional_enquiry_drafts.md"

    assert csv_template.exists(), f"Missing {csv_template}"
    assert guide_doc.exists(), f"Missing {guide_doc}"
    assert drafts_doc.exists(), f"Missing {drafts_doc}"

    # Verify CSV template header columns
    with open(csv_template, "r", encoding="utf-8") as f:
        header_line = f.readline().strip()
    headers = [h.strip() for h in header_line.split(",")]

    required_columns = [
        "entry_id",
        "page_number",
        "chapter_and_section",
        "lemma_original_script",
        "phonetic_transcription_or_ipa",
        "meaning_as_printed",
        "explicit_variety_label",
        "direct_jk_attribution_flag",
        "district",
        "tehsil_or_area",
        "village_or_informant_location",
        "informant_details",
        "grammatical_category",
        "grammatical_context_or_paradigm",
        "source_citation",
        "researcher_confidence_tier",
        "anti_conflation_notes",
        "unresolved_questions",
    ]
    for col in required_columns:
        assert col in headers, f"Missing column '{col}' in inspection worksheet template"

    # Verify enquiry drafts document content
    with open(drafts_doc, "r", encoding="utf-8") as f:
        drafts_text = f.read()

    # All 4 institutions must have prepared drafts with official contact info
    assert "dhanvantrilibraryju@jammuuniversity.ac.in" in drafts_text
    assert "librarian@sahitya-akademi.gov.in" in drafts_text
    assert "sivaprasad.s77@gov.in" in drafts_text
    assert "eblindology@gmail.com" in drafts_text

    # All 5 mandatory inquiries must be addressed in drafts
    assert "Physical Holding Confirmation" in drafts_text or "physically held" in drafts_text.lower()
    assert "External Researcher Consultation" in drafts_text or "consulted" in drafts_text.lower()
    assert "Contents & Page Range" in drafts_text or "page range" in drafts_text.lower()
    assert "Document Delivery" in drafts_text or "chapter-level" in drafts_text.lower()
    assert "Photography" in drafts_text or "photography" in drafts_text.lower()


def test_strict_linguistic_safeguards_zero_jk_entries():
    """Verify that verified J&K lexical entries count matches authenticated field extractions."""
    from gaddi.dictionary import GaddiDictionary
    d = GaddiDictionary()
    assert len(d.get_verified_jk_lexical_entries()) == 105
    # Strict translation returns nothing for unverified English queries
    assert d.translate("sheep", from_lang="en", jk_only=True) == []
    assert d.translate("goat", from_lang="en", jk_only=True) == []


def test_command_9_source_acquisition_tracker():
    """Command 9: Verify acquisition tracker schema, status vocabulary, and initial not_contacted states."""
    import csv
    root = Path(__file__).parents[1]
    tracker_file = root / "docs" / "source_acquisition_tracker.csv"
    assert tracker_file.exists(), f"Missing {tracker_file}"

    valid_statuses = {
        "not_contacted",
        "contacted",
        "awaiting_response",
        "response_received",
        "holding_confirmed",
        "copy_obtained",
        "pages_inspected",
        "unavailable",
    }

    required_columns = [
        "institution_or_publisher",
        "official_contact_source",
        "contact_email_or_channel",
        "status",
        "date_contacted",
        "response_received",
        "physical_copy_confirmed",
        "consultation_permission",
        "reproduction_permission",
        "gaddi_section_confirmed",
        "follow_up_date",
        "notes_and_evidence_reference",
    ]

    with open(tracker_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for col in required_columns:
            assert col in headers, f"Missing column '{col}' in acquisition tracker"

        rows = list(reader)
        assert len(rows) >= 6, "Tracker must record all major target institutions and publishers"

        for row in rows:
            # All statuses must be in the valid vocabulary
            status = row["status"].strip()
            assert status in valid_statuses, f"Invalid status '{status}' in row {row}"
            # Command 9 constraint: No emails sent; initial status must be not_contacted
            assert status == "not_contacted", f"Row should be not_contacted initially: {row}"
            # Official source must be a valid URL
            assert row["official_contact_source"].startswith("http"), f"Missing official URL for {row['institution_or_publisher']}"
            assert row["response_received"].strip().lower() == "no"


def test_command_9_evidence_intake_and_copyright_safeguards():
    """Command 9: Verify evidence intake directory, documentation, and gitignore safeguards."""
    root = Path(__file__).parents[1]
    intake_dir = root / "data" / "source_intake"
    intake_readme = intake_dir / "README.md"
    intake_keep = intake_dir / ".gitkeep"
    proc_doc = root / "docs" / "evidence_intake_procedure.md"
    gitignore_file = root / ".gitignore"

    assert intake_dir.is_dir(), f"Missing intake directory {intake_dir}"
    assert intake_readme.exists(), f"Missing {intake_readme}"
    assert intake_keep.exists(), f"Missing {intake_keep}"
    assert proc_doc.exists(), f"Missing {proc_doc}"

    # Verify intake procedure documentation contents
    with open(proc_doc, "r", encoding="utf-8") as f:
        proc_text = f.read()

    assert "Separation of Media and Data" in proc_text or "Separation of Concerns" in proc_text
    assert "SRC_{source_id}_{volume}_{page}_{descriptor}" in proc_text
    assert "SHA-256" in proc_text
    assert "Six-Point" in proc_text or "6-Point" in proc_text
    assert "Section 52(1)(a)" in proc_text

    # Verify .gitignore safeguards raw intake binaries
    with open(gitignore_file, "r", encoding="utf-8") as f:
        git_ignore_text = f.read()

    assert "data/source_intake/**" in git_ignore_text or "data/source_intake/*" in git_ignore_text
    assert "!data/source_intake/README.md" in git_ignore_text
    assert "!data/source_intake/.gitkeep" in git_ignore_text


def test_command_10_recursive_intake_exclusion_and_safeguards():
    """Command 10: Verify recursive raw-source exclusion and intake procedure legal framing."""
    root = Path(__file__).parents[1]
    gitignore_file = root / ".gitignore"
    proc_doc = root / "docs" / "evidence_intake_procedure.md"
    readme_doc = root / "data" / "source_intake" / "README.md"

    # 1. Verify recursive exclusion in .gitignore
    with open(gitignore_file, "r", encoding="utf-8") as f:
        git_ignore_text = f.read()
    assert "data/source_intake/**" in git_ignore_text
    assert "!data/source_intake/README.md" in git_ignore_text
    assert "!data/source_intake/.gitkeep" in git_ignore_text

    # 2. Verify evidence intake procedure does not overstate fair dealing or checksums
    with open(proc_doc, "r", encoding="utf-8") as f:
        proc_raw = f.read()

    proc_text = proc_raw.lower().replace("*", "").replace("_", "")

    # Must clarify bitstream integrity vs linguistic authenticity
    assert "bitstream integrity" in proc_text
    assert "linguistic authenticity" in proc_text
    assert "not prove linguistic authenticity" in proc_text or "not constitute proof" in proc_text

    # Must clarify photography does not grant redistribution rights
    assert "redistribution rights" in proc_text
    assert "not grant" in proc_text or "never be committed" in proc_text

    # Must clarify fair dealing statutory limits
    assert "fair dealing" in proc_text
    assert "not grant an automatic" in proc_text or "does not grant an automatic" in proc_text

    # 3. Verify README in source_intake also enforces these safeguards
    with open(readme_doc, "r", encoding="utf-8") as f:
        readme_raw = f.read()
    readme_text = readme_raw.lower().replace("*", "").replace("_", "")
    assert "bitstream integrity" in readme_text
    assert "redistribution rights" in readme_text


def test_command_10_contact_provenance_and_verification_tiers():
    """Command 10: Verify contact provenance tiers, time-sensitive staff records, and CIIL distinction."""
    import csv
    root = Path(__file__).parents[1]
    tracker_file = root / "docs" / "source_acquisition_tracker.csv"
    assert tracker_file.exists(), f"Missing {tracker_file}"

    with open(tracker_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        assert "contact_verification_tier" in headers
        assert "staff_name_and_role" in headers

        rows = {r["institution_or_publisher"]: r for r in reader}

    # All rows must be not_contacted and no correspondence sent
    for inst, r in rows.items():
        assert r["status"] == "not_contacted"
        assert r["date_contacted"] == ""
        assert r["response_received"].lower() == "no"
        assert "unconfirmed" in r["physical_copy_confirmed"].lower() or "institutional_confirmation_required" in r["physical_copy_confirmed"].lower()
        assert "pending_enquiry" in r["consultation_permission"].lower() or "unverified" in r["consultation_permission"].lower()
        assert "pending_enquiry" in r["reproduction_permission"].lower() or "unverified" in r["reproduction_permission"].lower()
        assert "unconfirmed" in r["gaddi_section_confirmed"].lower() or "institutional_confirmation_required" in r["gaddi_section_confirmed"].lower()

    # Check University of Jammu personnel & notes
    ju = [r for inst, r in rows.items() if "Dhanvantri" in inst][0]
    assert "Rakesh Kumar" in ju["staff_name_and_role"]
    assert "Vikram Sahi" in ju["staff_name_and_role"]
    assert "time-sensitive" in ju["staff_name_and_role"].lower()
    assert "official_contact_page_verified" in ju["contact_verification_tier"]
    assert "official_email_verified" in ju["contact_verification_tier"]

    # Check Sahitya Akademi personnel
    sa = [r for inst, r in rows.items() if "Sahitya Akademi" in inst][0]
    assert "Avinash Bansode" in sa["staff_name_and_role"]
    assert "time-sensitive" in sa["staff_name_and_role"].lower()

    # Check National Library personnel
    nl = [r for inst, r in rows.items() if "National Library" in inst][0]
    assert "Siva Prasad Senapatdi" in nl["staff_name_and_role"]
    assert "time-sensitive" in nl["staff_name_and_role"].lower()

    # Check CIIL distinction between Director email and general portal
    ciil = [r for inst, r in rows.items() if "CIIL" in inst][0]
    assert "director-ciil@gov.in" in ciil["contact_email_or_channel"]
    assert "ciil.org" in ciil["contact_email_or_channel"]
    assert "Director" in ciil["contact_email_or_channel"] or "Director" in ciil["staff_name_and_role"]
    assert "time-sensitive" in ciil["staff_name_and_role"].lower()








def test_command_11_dar_sheikh_2022_lead_and_thesis_connection():
    """Command 11: Verify Dar & Sheikh 2022 research lead, J&K primary status, and doctoral thesis link."""
    from gaddi.registry import default_sources

    lead = default_leads.get("lead-dar-sheikh-2022")
    assert lead is not None
    assert lead.lead_id == "lead-dar-sheikh-2022"
    assert "Hilal Ahmad Dar" in lead.authors_or_institution[0]
    assert "Aejaz Mohammed Sheikh" in lead.authors_or_institution[1]
    assert "Doda" in lead.geographic_scope
    assert "Bhaderwah" in lead.variety_coverage or "Assar" in lead.variety_coverage
    assert lead.contains_linguistic_data is True
    assert lead.full_source_accessible is True
    assert lead.full_text_accessible is True
    assert lead.status == "acquired_and_extracted"
    assert lead.access_status == "open_access_pdf_downloaded"
    assert "jk_bhaderwah_doda" in lead.varieties_documented
    assert "Aligarh Muslim University" in lead.publisher_or_archive

    # Verify sources.json entries
    s_paper = default_sources.get("dar_sheikh_2022")
    assert s_paper is not None
    assert s_paper.is_jk_primary is True
    assert s_paper.credibility_tier == 1
    assert s_paper.variety_id == "jk_bhaderwah_doda"

    s_thesis = default_sources.get("dar_2022_thesis")
    assert s_thesis is not None
    assert s_thesis.is_jk_primary is True
    assert s_thesis.credibility_tier == 1
    assert s_thesis.variety_id == "jk_bhaderwah_doda"
    assert "University of Kashmir" in s_thesis.publisher


def test_command_11_jambu_cdial_provenance_audit():
    """Command 11: Verify Jambu 1,118 forms provenance audit, coordinates, and strict comparative quarantine."""
    from gaddi.registry import default_sources

    lead = default_leads.get("lead-jambu-gaddi-cdial")
    assert lead is not None
    assert lead.lead_id == "lead-jambu-gaddi-cdial"
    assert lead.contains_linguistic_data is True
    assert lead.status == "accessible_comparative_only"
    assert lead.evidence_claim_tier == "primary_source_verified"
    assert "32.36, 76.57" in lead.geographic_scope or "Bharmaur" in lead.geographic_scope
    assert "ZERO" in lead.evidence_evaluation or "zero" in lead.evidence_evaluation
    assert "comparative_historical" in lead.varieties_documented

    # Verify sources.json entry
    s_jambu = default_sources.get("jambu_cdial_gaddi")
    assert s_jambu is not None
    assert s_jambu.is_jk_primary is False
    assert "1118" in s_jambu.notes or "Bharmaur" in s_jambu.notes


def test_command_11_grierson_lsi_exact_pages_and_chamba_provenance():
    """Command 11: Verify Grierson LSI exact page citations, volumes, and Brahmaur elicitation."""
    lead = default_leads.get("lead-grierson-lsi-1916")
    assert lead is not None
    # Check that relevant_pages or notes mention pp. 790-833 or similar
    assert "790" in lead.relevant_pages or "791" in lead.relevant_pages
    assert "Chamba" in lead.geographic_scope or "Bharmaur" in lead.geographic_scope


def test_command_11_variety_registry_expansion():
    """Command 11: Verify new variety IDs in registry: jk_bhaderwah_doda, historical, and comparative."""
    from gaddi.registry import default_varieties

    v_doda = default_varieties.get("jk_bhaderwah_doda")
    assert v_doda is not None
    assert v_doda.is_jk_variety is True
    assert v_doda.district == "Doda"
    assert "Bhaderwah" in v_doda.sub_areas

    v_hist = default_varieties.get("historical_gaddi_unspecified_locality")
    assert v_hist is not None
    assert v_hist.is_jk_variety is False

    v_comp = default_varieties.get("comparative_unlocated")
    assert v_comp is not None
    assert v_comp.is_jk_variety is False


def test_command_11_zero_jk_lexical_count_integrity():
    """Command 16: Assertion that verified_jk_lexical_entries reflects authentic field extractions."""
    info = gaddi.info()
    assert info["verified_jk_lexical_entries"] == 105
    assert info["jk_cultural_and_ecological_terms"] == 25
    assert info["comparative_word_list_entries"] >= 250
