"""Comprehensive regression, synchronization, multi-sense, and variety-comparison tests."""

from pathlib import Path
import pytest

import gaddi
from gaddi.cli import cmd_compare, cmd_sync
from gaddi.dictionary import GaddiDictionary
from gaddi.models import Attestation, EvidenceStatus, LexicalEntry, Sense
from gaddi.registry import default_sources, default_varieties
from gaddi.sync import check_resource_sync, sync_resources
from gaddi.validator import GaddiValidator


def test_compare_varieties_hp_baseline():
    """Verify that compare_varieties identifies HP comparative forms and isolates them from J&K."""
    res = gaddi.compare_varieties("पाणी")

    assert res["query"] == "पाणी"
    assert res["total_matches"] >= 1
    assert res["has_hp_comparative"] is True
    assert res["has_jk_evidence"] is False
    assert "hp_chamba_bharmaur" in res["hp_varieties"]
    assert "HP comparative baseline only" in res["comparative_summary"]

    hp_entry = res["hp_varieties"]["hp_chamba_bharmaur"][0]
    assert hp_entry["lemma_devanagari"] == "पाणी"
    assert hp_entry["evidence_status"] == "comparative_only"
    assert hp_entry["is_jk_variety"] is False
    assert any(a["source_id"] == "grierson_1916" for a in hp_entry["attestations"])


def test_compare_varieties_jk_cultural_term():
    """Verify that compare_varieties identifies authentic J&K field terms."""
    res = gaddi.compare_varieties("खडे")

    assert res["query"] == "खडे"
    assert res["total_matches"] >= 1
    assert res["has_jk_evidence"] is True
    assert "jk_doda_bhadarwah" in res["jk_varieties"]
    assert "J&K specific" in res["comparative_summary"]

    jk_entry = res["jk_varieties"]["jk_doda_bhadarwah"][0]
    assert jk_entry["lemma_devanagari"] == "खडे"
    assert jk_entry["evidence_status"] == "jk_cultural_term"
    assert jk_entry["is_jk_variety"] is True
    assert any(a["source_id"] in ("kumar_2019", "chandar_2024") for a in jk_entry["attestations"])


def test_compare_varieties_empty_result():
    """Verify that non-existent queries return a structured, clean empty response."""
    res = gaddi.compare_varieties("nonexistent_term_9999")

    assert res["query"] == "nonexistent_term_9999"
    assert res["total_matches"] == 0
    assert res["has_jk_evidence"] is False
    assert res["has_hp_comparative"] is False
    assert res["jk_varieties"] == {}
    assert res["hp_varieties"] == {}
    assert "No documented lexical entries found" in res["comparative_summary"]

    res_empty_str = gaddi.compare_varieties("")
    assert res_empty_str["total_matches"] == 0
    assert "Empty headword query" in res_empty_str["comparative_summary"]


def test_multisense_entries_preserved():
    """Verify that polysemous words are unified into multi-sense entries with intact definitions."""
    d = GaddiDictionary()

    # 'खा' (verb) has 2 senses: bite & eat
    kha_entries = d.search("खा", jk_only=False)
    kha = [e for e in kha_entries if e.lemma_devanagari == "खा" and e.part_of_speech == "verb"]
    assert len(kha) == 1
    assert len(kha[0].senses) == 2
    sense_defs = {s.definition_en for s in kha[0].senses}
    assert any("bite" in d for d in sense_defs)
    assert any("eat" in d for d in sense_defs)

    # 'तर' (verb) has 2 senses: float & swim
    tar_entries = d.search("तर", jk_only=False)
    tar = [e for e in tar_entries if e.lemma_devanagari == "तर" and e.part_of_speech == "verb"]
    assert len(tar) == 1
    assert len(tar[0].senses) == 2
    tar_defs = {s.definition_en for s in tar[0].senses}
    assert any("float" in d for d in tar_defs)
    assert any("swim" in d for d in tar_defs)

    # 'हिउँ' (noun) has 2 senses: ice & snow
    hiu_entries = d.search("हिउँ", jk_only=False)
    hiu = [e for e in hiu_entries if e.lemma_devanagari == "हिउँ"]
    assert len(hiu) == 1
    assert len(hiu[0].senses) == 2
    hiu_defs = {s.definition_en for s in hiu[0].senses}
    assert any("ice" in d for d in hiu_defs)
    assert any("snow" in d for d in hiu_defs)


def test_homonym_index_model_and_validation():
    """Verify that homonym_index supports distinct entries with same lemma and POS."""
    validator = GaddiValidator(default_sources, default_varieties)

    # Two homonyms with homonym_index 1 and 2
    h1 = LexicalEntry(
        id="hom-001",
        lemma_devanagari="बरख",
        variety_id="hp_kangra_palampur",
        part_of_speech="noun",
        evidence_status="comparative_only",
        senses=[Sense(sense_index=1, definition_en="rain")],
        attestations=[Attestation(source_id="kumari_2026", page_or_section="p. 122")],
        homonym_index=1,
    )
    h2 = LexicalEntry(
        id="hom-002",
        lemma_devanagari="बरख",
        variety_id="hp_kangra_palampur",
        part_of_speech="noun",
        evidence_status="comparative_only",
        senses=[Sense(sense_index=1, definition_en="elder brother")],
        attestations=[Attestation(source_id="kumari_2026", page_or_section="p. 124")],
        homonym_index=2,
    )

    # Serializing and deserializing preserves homonym_index
    d1 = h1.to_dict()
    assert d1["homonym_index"] == 1
    recovered1 = LexicalEntry.from_dict(d1)
    assert recovered1.homonym_index == 1

    # Both homonyms together pass validation with 0 duplicate errors
    report = validator.validate_collection([h1, h2])
    assert report.is_valid
    assert len(report.errors) == 0

    # Two homonyms with duplicate homonym_index trigger ValidationError
    h2_collision = LexicalEntry(
        id="hom-003",
        lemma_devanagari="बरख",
        variety_id="hp_kangra_palampur",
        part_of_speech="noun",
        evidence_status="comparative_only",
        senses=[Sense(sense_index=1, definition_en="elder brother")],
        attestations=[Attestation(source_id="kumari_2026", page_or_section="p. 124")],
        homonym_index=1,  # Same homonym_index!
    )
    report_collision = validator.validate_collection([h1, h2_collision])
    assert not report_collision.is_valid
    assert any("Duplicate entry" in e.message for e in report_collision.errors)


def test_all_27_packaged_resources_synchronized():
    """Verify that authoritative data/ and packaged src/gaddi/resources/ are 100% synchronized across all 27 managed datasets."""
    is_synced, issues = check_resource_sync()
    assert is_synced is True, f"Resource synchronization issues: {issues}"
    assert len(issues) == 0

    sync_result = sync_resources(dry_run=True)
    assert sync_result["success"] is True
    assert sync_result["total_datasets"] == 27
    assert len(sync_result["identical"]) == 27
    assert len(sync_result["synced"]) == 0
    assert len(sync_result["errors"]) == 0


def test_zero_mojibake_in_source_code():
    """Regression check: verify that no CP437 mojibake or corrupt box characters exist in Python sources."""
    src_dir = Path(__file__).resolve().parents[1] / "src" / "gaddi"
    corrupt_chars = ["α", "ß╣", "┬⌐", "╪î", "╪¢", "█ö"]

    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for bad in corrupt_chars:
            assert bad not in content, f"Mojibake artifact '{bad}' found in {py_file.name}"


def test_urdu_punctuation_in_search():
    """Verify that Urdu definitions with Arabic punctuation (،؛۔) are cleanly searchable."""
    d = GaddiDictionary()
    res = d.lookup_urdu("شیو")
    assert len(res) >= 1
    assert any(e.lemma_devanagari in ("नवाला", "अंचली") for e in res)


def test_cli_compare_and_sync_commands(capsys):
    """Test the CLI 'compare' and 'sync --check' commands."""
    ret_comp_hp = cmd_compare("पाणी")
    assert ret_comp_hp == 0
    cap_hp = capsys.readouterr()
    assert "Variety Comparison: 'पाणी'" in cap_hp.out
    assert "Himachal Pradesh Varieties" in cap_hp.out

    ret_comp_jk = cmd_compare("खडे")
    assert ret_comp_jk == 0
    cap_jk = capsys.readouterr()
    assert "Variety Comparison: 'खडे'" in cap_jk.out
    assert "Jammu & Kashmir Varieties" in cap_jk.out

    ret_sync = cmd_sync(check_only=True)
    assert ret_sync == 0
    cap_sync = capsys.readouterr()
    assert "100% synchronized" in cap_sync.out


def test_deduplication_provenance_and_homonyms_in_unified():
    """Verify that unified dictionary preserves all homonym pairs and retains 100% provenance."""
    d = GaddiDictionary(include_unified=True)
    unified = d.get_unified_entries()
    assert len(unified) == 1925

    # 1. Verify all 5 genuine homonym groups exist and have homonym_index
    homonym_checks = {
        "घोड़ी": [1, 2],
        "बरख": [1, 2],
        "मामा": [1, 2],
        "मुह": [1, 2],
        "हिङग": [1, 2],
    }

    for lemma, indices in homonym_checks.items():
        matches = [e for e in unified if e.lemma_devanagari == lemma]
        found_indices = sorted([e.homonym_index for e in matches if e.homonym_index is not None])
        for idx in indices:
            assert idx in found_indices, f"Homonym index {idx} missing for lemma '{lemma}'"

    # 2. Verify 100% of unified entries have non-empty attestations with registered source IDs
    valid_source_ids = set(default_sources._sources.keys())
    for e in unified:
        assert len(e.attestations) > 0, f"Entry {e.id} has no attestations!"
        for a in e.attestations:
            assert a.source_id in valid_source_ids, f"Entry {e.id} has invalid source {a.source_id}!"

    # 3. Verify that GaddiValidator reports exactly 0 errors on unified entries
    validator = GaddiValidator(default_sources, default_varieties)
    report = validator.validate_collection(unified)
    assert report.is_valid, f"Validation errors on unified: {report.errors}"
    assert len(report.errors) == 0


def test_group_19_item_level_provenance_and_sense_associations():
    """Regression test for Part 1: verify Group 19 (धौड़) item-level provenance and sense associations."""
    d = GaddiDictionary(include_unified=True)
    unified = d.get_unified_entries()
    entry = next((e for e in unified if e.id == "gaddi-uni-00059"), None)
    assert entry is not None, "Entry gaddi-uni-00059 missing from unified dictionary"

    # 1. Basic properties preserved
    assert entry.lemma_devanagari == "धौड़"
    assert entry.part_of_speech == "noun"
    assert entry.variety_id == "hp_kangra_palampur"
    assert entry.original_transcription == "dʰuːɽ"

    # 2. Exactly 2 attestations preserved (no duplicate citations created)
    assert len(entry.attestations) == 2, f"Expected exactly 2 attestations, got {len(entry.attestations)}"
    p119 = next((a for a in entry.attestations if "p. 119" in a.page_or_section), None)
    p120 = next((a for a in entry.attestations if "p. 120" in a.page_or_section), None)
    assert p119 is not None, "Attestation for p. 119 missing"
    assert p120 is not None, "Attestation for p. 120 missing"
    assert p119.source_id == "kumari_2026"
    assert p120.source_id == "kumari_2026"
    assert p120.transcription_raw == "dʰuːɽ"
    assert "36" in p120.context and "57" in p120.context

    # 3. Exactly 3 senses preserved with explicit item-level provenance
    assert len(entry.senses) == 3
    s1, s2, s3 = entry.senses[0], entry.senses[1], entry.senses[2]

    # Sense 1: ashes
    assert s1.definition_en == "ashes"
    assert s1.source_item is not None and "item 4" in s1.source_item.lower()

    # Sense 2: dust (Item 36, p. 120)
    assert s2.definition_en == "dust"
    assert s2.source_item is not None
    assert "item 36" in s2.source_item.lower()
    assert "120" in s2.source_item

    # Sense 3: fog; haze (Item 57, p. 120)
    assert "fog" in s2.definition_en.lower() or "fog" in s3.definition_en.lower()
    assert s3.source_item is not None
    assert "item 57" in s3.source_item.lower()
    assert "120" in s3.source_item

    # 4. Editorial notes and metadata trace
    assert "36" in entry.editorial_notes and "57" in entry.editorial_notes
    assert "sense_provenance" in entry.metadata
    assert entry.metadata["sense_provenance"]["2"]["item"] == 36
    assert entry.metadata["sense_provenance"]["3"]["item"] == 57
