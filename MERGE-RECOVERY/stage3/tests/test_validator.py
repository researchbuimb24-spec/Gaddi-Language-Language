"""Tests for the linguistic validation engine."""

import pytest

from gaddi.models import Attestation, LexicalEntry, Sense
from gaddi.validator import GaddiValidator


@pytest.fixture
def validator():
    return GaddiValidator()


def test_valid_entry(validator):
    entry = LexicalEntry(
        id="test-001",
        lemma_devanagari="αñ¿αñ╡αñ╛αñ▓αñ╛",
        variety_id="jk_general",
        senses=[
            Sense(
                sense_index=1,
                definition_en="Thanksgiving ritual for Shiva",
                definition_hi="αñ╢αñ┐αñ╡ αñòαÑÇ αñ¬αÑéαñ£αñ╛",
                definition_ur="╪┤█î┘ê ┌⌐█î ┘╛┘ê╪¼╪º",
            )
        ],
        attestations=[
            Attestation(
                source_id="chakraborty_2024",
                page_or_section="p. 3",
            )
        ],
    )
    errors = validator.validate_entry(entry)
    assert len(errors) == 0


def test_missing_attestation_fails(validator):
    entry = LexicalEntry(
        id="test-002",
        lemma_devanagari="αñÜαÑïαñ▓αñ╛",
        variety_id="jk_kathua_bani",
        senses=[
            Sense(sense_index=1, definition_en="Woolen tunic")
        ],
        attestations=[],  # No source!
    )
    errors = validator.validate_entry(entry)
    assert any("attestations" in e.field_name for e in errors)


def test_unknown_variety_fails(validator):
    entry = LexicalEntry(
        id="test-003",
        lemma_devanagari="αñÜαÑïαñ▓αñ╛",
        variety_id="unknown_fictional_variety",
        senses=[Sense(sense_index=1, definition_en="Woolen coat")],
        attestations=[Attestation(source_id="kumar_2019")],
    )
    errors = validator.validate_entry(entry)
    assert any("variety_id" in e.field_name for e in errors)


def test_unknown_source_fails(validator):
    entry = LexicalEntry(
        id="test-004",
        lemma_devanagari="αñÜαÑïαñ▓αñ╛",
        variety_id="jk_kathua_bani",
        senses=[Sense(sense_index=1, definition_en="Woolen coat")],
        attestations=[Attestation(source_id="made_up_source_2099")],
    )
    errors = validator.validate_entry(entry)
    assert any("source_id" in e.field_name for e in errors)


def test_conflation_protection(validator):
    """Ensure that claiming a word is J&K Gaddi while citing only Kangra HP source fails."""
    entry = LexicalEntry(
        id="test-005",
        lemma_devanagari="αñòαÑüαñú",
        variety_id="jk_kathua_bani",  # Claims J&K variety
        status="verified",
        senses=[Sense(sense_index=1, definition_en="who")],
        attestations=[
            Attestation(source_id="kumari_2026", page_or_section="p. 119")  # Only Kangra source!
        ],
    )
    errors = validator.validate_entry(entry)
    assert any("claims J&K variety" in e.message for e in errors)


def test_duplicate_detection(validator):
    e1 = LexicalEntry(
        id="test-dup-1",
        lemma_devanagari="αñ¬αñƒαÑìαñƒαÑé",
        variety_id="jk_general",
        senses=[Sense(sense_index=1, definition_en="Woolen blanket")],
        attestations=[Attestation(source_id="chandar_2024")],
    )
    e2 = LexicalEntry(
        id="test-dup-2",
        lemma_devanagari="αñ¬αñƒαÑìαñƒαÑé",
        variety_id="jk_general",
        senses=[Sense(sense_index=1, definition_en="Duplicate item")],
        attestations=[Attestation(source_id="chandar_2024")],
    )
    report = validator.validate_collection([e1, e2])
    assert report.is_valid is False
    assert any("Duplicate entry" in e.message for e in report.errors)

