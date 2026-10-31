"""Strict linguistic evidence audit and integrity tests (Command 3)."""

import json
from pathlib import Path
import pytest

import gaddi
from gaddi.dictionary import GaddiDictionary
from gaddi.models import EvidenceStatus
from gaddi.registry import default_sources, default_varieties
from gaddi.validator import GaddiValidator


def test_cultural_terms_quarantined_from_strict_translate():
    """Verify that cultural and ethnographic terms NEVER appear in strict J&K translation."""
    d = GaddiDictionary()

    # Strict translation (default) must return empty list for cultural words
    assert d.translate("handloom", from_lang="en") == []
    assert d.translate("blanket", from_lang="en") == []
    assert d.translate("चोला", from_lang="hi") == []
    assert d.translate("ہتھ کرگھی", from_lang="ur") == []

    # When explicitly opted into cultural search, they appear with transparent status
    cult_res = d.translate("handloom", from_lang="en", include_cultural=True)
    assert len(cult_res) >= 1
    assert any(e.lemma_devanagari == "खडे" for e in cult_res)
    assert all(e.evidence_status in ("jk_cultural_term", "jk_place_or_ecological_term") for e in cult_res)


def test_comparative_entries_quarantined_from_jk_translate():
    """Verify that comparative HP entries never leak into J&K translation."""
    d = GaddiDictionary()

    # "water" is attested only in Chamba Bharmauri ('पाणी', Grierson 1916)
    assert d.translate("water", from_lang="en", jk_only=True) == []

    # Opting in with allow_comparative=True returns it, explicitly flagged
    comp_res = d.translate("water", from_lang="en", jk_only=False, allow_comparative=True)
    assert len(comp_res) >= 1
    assert any(e.lemma_devanagari == "पाणी" for e in comp_res)
    assert any(e.evidence_status == "comparative_only" for e in comp_res)


def test_census_population_distinction():
    """Verify that Scheduled Tribe population and Mother Tongue speaker counts are distinct."""
    c16 = default_sources.get("census_2011_c16")
    st14 = default_sources.get("census_2011_st14")

    assert c16 is not None
    assert st14 is not None

    # Table C-16 is language mother tongue (24,161)
    assert "24,161" in c16.notes
    assert c16.evidence_type == "demographic_mother_tongue"

    # Table ST-14 is Scheduled Tribe population (46,489)
    assert "46,489" in st14.notes
    assert st14.evidence_type == "demographic_scheduled_tribe"

    # Must explicitly state that ST population does not equal mother-tongue speaker count
    assert "not mother-tongue speaker counts" in st14.notes


def test_kumari_license_is_cc_by_nc_4():
    """Audit check: UCL Press 2026 grammar is CC BY-NC 4.0, not CC BY 4.0."""
    kumari = default_sources.get("kumari_2026")
    assert kumari is not None
    assert kumari.license == "CC BY-NC 4.0"
    assert "CC BY-NC 4.0" in kumari.notes
    assert "non-commercial" in kumari.notes.lower()
    assert "third-party" in kumari.notes.lower()


def test_source_evidence_classifications():
    """Verify that sources do not claim linguistic evidence when providing only culture or demography."""
    # Banti Kumar 2019 is ethnographic, NOT linguistic descriptive grammar
    kumar = default_sources.get("kumar_2019")
    assert kumar.evidence_type == "ethnographic_evidence"
    assert "NOT provide descriptive linguistic lexicon" in kumar.notes

    # Subhash Chandar 2024 is ethnographic
    chandar = default_sources.get("chandar_2024")
    assert chandar.evidence_type == "ethnographic_evidence"
    assert "NOT provide descriptive linguistic lexicon" in chandar.notes

    # Arka Chakraborty 2024 is cultural documentation
    chakraborty = default_sources.get("chakraborty_2024")
    assert chakraborty.evidence_type == "cultural_documentation"
    assert "NOT provide descriptive linguistic lexicon" in chakraborty.notes

    # Grierson 1916 provides historical linguistic lexical data for Chamba
    grierson = default_sources.get("grierson_1916")
    assert grierson.evidence_type == "historical_linguistic_lexical"


def test_packaged_datasets_match_data_files():
    """Ensure data/ and src/gaddi/resources/ datasets are completely synchronized."""
    root = Path(__file__).parents[1]
    data_dir = root / "data"
    res_dir = root / "src" / "gaddi" / "resources"

    for filename in ["sources.json", "varieties.json", "lexicon_jk.json", "cultural_terms_jk.json", "lexicon_comparative.json", "research_leads.json"]:
        p1 = data_dir / filename
        p2 = res_dir / filename
        assert p1.exists(), f"Missing {p1}"
        assert p2.exists(), f"Missing {p2}"

        with open(p1, encoding="utf-8") as f1, open(p2, encoding="utf-8") as f2:
            d1 = json.load(f1)
            d2 = json.load(f2)
        assert d1 == d2, f"Mismatch between data/{filename} and resources/{filename}"


def test_cultural_terms_all_have_attestations_and_provenance():
    """Verify that every entry in cultural_terms_jk.json has traceable sources and sections."""
    d = GaddiDictionary()
    cultural_entries = d.get_cultural_entries()
    assert len(cultural_entries) == 25

    validator = GaddiValidator(default_sources, default_varieties)
    report = validator.validate_collection(cultural_entries)
    assert report.is_valid, f"Validation errors in cultural terms: {report.errors}"

    for e in cultural_entries:
        assert e.evidence_status in ("jk_cultural_term", "jk_place_or_ecological_term")
        assert len(e.attestations) >= 1
        for a in e.attestations:
            assert a.page_or_section != "" or a.context != ""

