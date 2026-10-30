"""Tests for grammar paradigms and rules."""

from gaddi.grammar import GrammarRegistry


def test_baseline_case_markers():
    markers = GrammarRegistry.get_baseline_case_markers()
    assert len(markers) >= 5
    case_names = {m.case_name for m in markers}
    assert "Agentive / Ergative" in case_names
    assert "Genitive (Possessive)" in case_names

    # Check J&K attestation flag
    erg = next(m for m in markers if "Agentive" in m.case_name)
    assert erg.is_jk_attested is True
    assert erg.form_devanagari == "ने"


def test_personal_pronouns():
    pronouns = GrammarRegistry.get_personal_pronouns()
    assert len(pronouns) >= 4
    first_sing = next(p for p in pronouns if p.person == "1st" and p.number == "singular")
    assert first_sing.form_devanagari == "आऊं"
    assert first_sing.is_jk_attested is True

