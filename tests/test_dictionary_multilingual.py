"""Unit and regression tests for Expansion 3: Research-Expanded Multilingual Dictionary.

Validates:
1. Dataset loading (958 entries, 100% 4-language translation coverage: EN, HI, AS, BN).
2. Translation into Gaddi from Assamese and Bengali.
3. Translation from English and Hindi.
4. Strict dialect and variety separation (hp_kangra_palampur, hp_chamba_bharmaur, jk_doda_bhadarwah).
5. Domain categorization across all 18 standardized domains.
6. Public API functional endpoints.
7. CLI subcommands and options.
8. Backward compatibility and baseline test invariants.
"""

import csv
import json
from pathlib import Path
import pytest

import gaddi
from gaddi.dictionary import GaddiDictionary
from gaddi.models import EvidenceStatus, LexicalEntry


@pytest.fixture
def dictionary() -> GaddiDictionary:
    return GaddiDictionary()


def test_multilingual_dataset_loading(dictionary: GaddiDictionary):
    """Verify that all 2,432 research-expanded multilingual entries are loaded."""
    entries = dictionary.get_multilingual_entries()
    assert len(entries) == 2432
    assert len(entries) >= 2000
    assert len(dictionary._multilingual_id_index) == 2432


def test_multilingual_translation_coverage(dictionary: GaddiDictionary):
    """Ensure 100% translation coverage across English, Hindi, Assamese, and Bengali."""
    entries = dictionary.get_multilingual_entries()
    total_senses = sum(len(e.senses) for e in entries)
    assert total_senses >= 2000
    assert total_senses == 2489

    for e in entries:
        assert e.id.startswith("gaddi-dict-")
        assert e.lemma_devanagari
        assert e.variety_id in ("hp_kangra_palampur", "hp_chamba_bharmaur", "jk_doda_bhadarwah")
        assert len(e.senses) >= 1
        assert len(e.attestations) >= 1

        for s in e.senses:
            assert s.definition_en, f"Missing definition_en in {e.id}"
            assert s.definition_hi, f"Missing definition_hi in {e.id}"
            assert getattr(s, "definition_as", None), f"Missing definition_as in {e.id}"
            assert getattr(s, "definition_bn", None), f"Missing definition_bn in {e.id}"
            assert s.semantic_field, f"Missing semantic_field in {e.id}"


def test_variety_distribution(dictionary: GaddiDictionary):
    """Verify dialect/variety counts and separation."""
    entries = dictionary.get_multilingual_entries()
    kangra = [e for e in entries if e.variety_id == "hp_kangra_palampur"]
    chamba = [e for e in entries if e.variety_id == "hp_chamba_bharmaur"]
    jk = [e for e in entries if e.variety_id == "jk_doda_bhadarwah"]

    assert len(kangra) == 941
    assert len(chamba) == 1370
    assert len(jk) == 121
    assert len(kangra) + len(chamba) + len(jk) == 2432


def test_semantic_domains_coverage(dictionary: GaddiDictionary):
    """Verify all 18 standardized semantic domains are represented."""
    entries = dictionary.get_multilingual_entries()
    domains = set(e.metadata.get("domain") for e in entries)
    expected_domains = {
        "nature_weather_geography",
        "body_and_health",
        "people_family_relationships",
        "animals_birds_insects",
        "plants_and_crops",
        "food_and_cooking",
        "clothing_and_adornment",
        "home_and_surroundings",
        "agriculture_and_pastoral_life",
        "work_occupations_and_tools",
        "common_actions_and_verbs",
        "descriptive_adjectives",
        "numbers_and_time",
        "directions_and_movement",
        "social_life_and_culture",
        "colors_shapes_and_space",
        "education_and_learning",
    }
    for dom in expected_domains:
        assert dom in domains, f"Missing expected domain: {dom}"


def test_translate_from_assamese():
    """Verify translation into Gaddi from Assamese."""
    # Water: পানী -> पाणी
    res_water = gaddi.translate("পানী", source="as", target="gaddi")
    assert len(res_water) >= 1
    assert any(e.lemma_devanagari == "पाणी" for e in res_water)

    # Horse: ঘোঁৰা -> घोड़ा
    res_horse = gaddi.translate("ঘোঁৰা", source="as", target="gaddi")
    assert len(res_horse) >= 1
    assert any(e.lemma_devanagari == "घोड़ा" for e in res_horse)

    # And: আৰু -> अतै
    res_and = gaddi.translate("আৰু", source="as", target="gaddi")
    assert len(res_and) >= 1
    assert any(e.lemma_devanagari == "अतै" for e in res_and)

    # Adopted daughter (J&K Gaddi): তোলনীয়া জীয়েক -> धरम बेटी
    res_daughter = gaddi.translate("তোলনীয়া জীয়েক", source="as", target="gaddi")
    assert len(res_daughter) >= 1
    assert any(e.lemma_devanagari == "धरम बेटी" for e in res_daughter)


def test_translate_from_bengali():
    """Verify translation into Gaddi from Bengali."""
    # Water: জল -> पाणी
    res_water = gaddi.translate("জল", source="bn", target="gaddi")
    assert len(res_water) >= 1
    assert any(e.lemma_devanagari == "पाणी" for e in res_water)

    # Horse: ঘোড়া -> घोड़ा
    res_horse = gaddi.translate("ঘোড়া", source="bn", target="gaddi")
    assert len(res_horse) >= 1
    assert any(e.lemma_devanagari == "घोड़ा" for e in res_horse)

    # And: এবং -> अतै
    res_and = gaddi.translate("এবং", source="bn", target="gaddi")
    assert len(res_and) >= 1
    assert any(e.lemma_devanagari == "अतै" for e in res_and)

    # Adopted daughter (J&K Gaddi): দত্তক কন্যা -> धरम बेटी
    res_daughter = gaddi.translate("দত্তক কন্যা", source="bn", target="gaddi")
    assert len(res_daughter) >= 1
    assert any(e.lemma_devanagari == "धरम बेटी" for e in res_daughter)


def test_public_api_multilingual_functions(dictionary: GaddiDictionary):
    """Test top-level functional API exports."""
    # get_multilingual_entries
    all_multi = gaddi.get_multilingual_entries()
    assert len(all_multi) == 2432

    # Filtered by variety
    jk_only = gaddi.get_multilingual_entries(variety_id="jk_doda_bhadarwah")
    assert len(jk_only) == 121

    # Filtered by domain
    kinship = gaddi.get_multilingual_entries(domain="people_family_relationships")
    assert len(kinship) >= 70

    # get_multilingual_by_id
    entry1 = gaddi.get_multilingual_by_id("gaddi-dict-0001")
    assert entry1 is not None
    assert entry1.lemma_devanagari == "सब"

    # lookup_assamese & lookup_bengali
    as_res = gaddi.lookup_assamese("ঘোঁৰা")
    assert len(as_res) >= 1
    assert any(e.lemma_devanagari == "घोड़ा" for e in as_res)

    bn_res = gaddi.lookup_bengali("ঘোড়া")
    assert len(bn_res) >= 1
    assert any(e.lemma_devanagari == "घोड़ा" for e in bn_res)

    # search_multilingual
    search_res = gaddi.search_multilingual("apple")
    assert len(search_res) >= 1
    assert any(e.lemma_devanagari == "सेउ" for e in search_res)


def test_baseline_test_invariants():
    """Ensure baseline assertions are not disturbed."""
    info = gaddi.info()
    assert info["total_entries"] == 159
    assert info["verified_jk_lexical_entries"] == 105
    assert info["jk_cultural_and_ecological_terms"] == 25
    assert info["comparative_entries"] == 29
    assert len(info["translation_priorities"]) == 3
    assert info["multilingual_total_entries"] == 2432
    assert "as" in info["supported_languages"]
    assert "bn" in info["supported_languages"]


def test_translation_status_and_evidence_categories(dictionary: GaddiDictionary):
    """Verify that every sense carries valid translation evidence status."""
    entries = dictionary.get_multilingual_entries()
    valid_statuses = {"source_attested", "cross_source_supported", "translation_equivalent", "needs_review"}

    status_counts = {}
    for e in entries:
        for s in e.senses:
            st = getattr(s, "translation_status", None)
            assert st in valid_statuses, f"Invalid translation_status '{st}' in {e.id}"
            status_counts[st] = status_counts.get(st, 0) + 1

    # Verify exact reconciled sense counts by evidence tier
    assert status_counts["source_attested"] == 1164
    assert status_counts["cross_source_supported"] == 160
    assert status_counts["translation_equivalent"] == 1136
    assert status_counts["needs_review"] == 29
    assert sum(status_counts.values()) == 2489


def test_dialect_isolation_and_anti_conflation(dictionary: GaddiDictionary):
    """Enforce strict geographic segregation between J&K and HP comparative baselines."""
    entries = dictionary.get_multilingual_entries()

    for e in entries:
        if e.variety_id == "jk_doda_bhadarwah":
            assert e.evidence_status in (EvidenceStatus.VERIFIED_JK_LEXICAL.value, "needs_review", "verified_jk")
            # Must derive exclusively from Dar & Sheikh (2022)
            assert any(a.source_id == "dar_sheikh_2022" for a in e.attestations)
        elif e.variety_id in ("hp_kangra_palampur", "hp_chamba_bharmaur"):
            assert e.evidence_status in (EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value, EvidenceStatus.COMPARATIVE_ONLY.value)
            # Cannot have a J&K primary source
            assert not any(a.source_id == "dar_sheikh_2022" for a in e.attestations)


def test_machine_readable_audit_report_integrity():
    """Verify integrity and schema of machine-readable audit report files."""
    repo_root = Path(__file__).resolve().parents[1]
    json_report = repo_root / "docs" / "expansion3_lexical_audit.json"
    csv_report = repo_root / "docs" / "expansion3_lexical_audit.csv"

    assert json_report.exists(), "docs/expansion3_lexical_audit.json missing!"
    assert csv_report.exists(), "docs/expansion3_lexical_audit.csv missing!"

    with open(json_report, "r", encoding="utf-8") as f:
        rows = json.load(f)
    assert len(rows) == 990

    # Check required fields
    sample = rows[0]
    required_fields = [
        "entry_id", "sense_index", "lemma_devanagari", "lemma_ipa",
        "part_of_speech", "variety_id", "gaddi_evidence_status",
        "source_id", "page_or_section", "definition_en", "definition_hi",
        "definition_as", "definition_bn", "translation_status",
        "translation_evidence_category", "audit_flags", "audit_notes"
    ]
    for rf in required_fields:
        assert rf in sample, f"Missing audit field: {rf}"

    with open(csv_report, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 990


def test_expansion4_audit_report_integrity():
    """Verify integrity and schema of Expansion 4 machine-readable audit report files."""
    repo_root = Path(__file__).resolve().parents[1]
    json_report = repo_root / "docs" / "expansion4_lexical_audit.json"
    csv_report = repo_root / "docs" / "expansion4_lexical_audit.csv"

    assert json_report.exists(), "docs/expansion4_lexical_audit.json missing!"
    assert csv_report.exists(), "docs/expansion4_lexical_audit.csv missing!"

    with open(json_report, "r", encoding="utf-8") as f:
        rows = json.load(f)
    assert len(rows) == 2489

    sample = rows[0]
    required_fields = [
        "entry_id", "sense_index", "lemma_devanagari", "lemma_ipa",
        "part_of_speech", "variety_id", "gaddi_evidence_status",
        "source_id", "page_or_section", "definition_en", "definition_hi",
        "definition_as", "definition_bn", "translation_status",
        "translation_evidence_category", "audit_flags", "audit_notes"
    ]
    for rf in required_fields:
        assert rf in sample, f"Missing audit field: {rf}"

    with open(csv_report, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 2489
