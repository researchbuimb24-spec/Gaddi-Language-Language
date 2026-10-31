"""Comprehensive test suite for the linguistic extraction and research integration
of 'A Grammar of Gaddi' (Kumari, Mehta, Nair, Nayak, Roy, & Sharma 2026; UCL Press).

Verifies dataset integrity, serial numbers, phonetic representations, grammatical rules,
examples, numerals, sociolinguistic notes, API exposure, and strict anti-conflation safeguards.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

import gaddi
from gaddi.cli import (
    cmd_examples,
    cmd_numerals,
    cmd_phonology,
    cmd_references,
    cmd_sociolinguistics,
    cmd_word_list,
)
from gaddi.grammar import GrammarRegistry
from gaddi.models import EvidenceStatus, NumeralEntry, WordListEntry


REPO_ROOT = Path(__file__).parents[1]
DATA_DIR = REPO_ROOT / "data"
RES_DIR = REPO_ROOT / "src" / "gaddi" / "resources"

DATASET_NAMES = [
    "gaddi_word_list.json",
    "gaddi_numerals.json",
    "gaddi_phonology.json",
    "gaddi_grammar.json",
    "gaddi_examples.json",
    "gaddi_morphology.json",
    "gaddi_syntax.json",
    "gaddi_cultural_sociolinguistic_notes.json",
    "gaddi_references.json",
]


# =============================================================================
# 1. Dataset Presence & Synchronization Tests
# =============================================================================

@pytest.mark.parametrize("filename", DATASET_NAMES)
def test_dataset_exists_and_synchronized(filename: str):
    """Ensure every dataset exists in both data/ and src/gaddi/resources/ and is byte-identical."""
    data_file = DATA_DIR / filename
    res_file = RES_DIR / filename

    assert data_file.exists(), f"Missing dataset in data/: {filename}"
    assert res_file.exists(), f"Missing dataset in src/gaddi/resources/: {filename}"

    with open(data_file, "rb") as f1, open(res_file, "rb") as f2:
        assert f1.read() == f2.read(), f"Datasets out of sync: {filename}"


# =============================================================================
# 2. Appendix II: Basic Word List (Table B.1) Tests
# =============================================================================

def test_appendix_ii_word_list_completeness_and_schema():
    """Verify Appendix II Table B.1 basic word list extraction."""
    word_list = gaddi.get_comparative_word_list()
    assert len(word_list) == 254, f"Expected exactly 254 entries, got {len(word_list)}"

    # Check serial coverage: spans 1.1 to 221
    serials = [w["serial_number"] for w in word_list]
    assert serials[0] == "1.1"
    assert serials[1] == "1.2"
    assert serials[-1] == "221"
    assert "25.1" in serials
    assert "25.2" in serials
    assert "25.3" in serials
    assert "210.1" in serials
    assert "210.2" in serials
    assert "210.3" in serials

    # Verify every entry satisfies strict metadata and anti-conflation rules
    for item in word_list:
        entry = WordListEntry.from_dict(item)
        assert entry.evidence_status == EvidenceStatus.COMPARATIVE_ONLY.value
        assert entry.is_jk_verified is False
        assert entry.variety_id == "hp_kangra_palampur"
        assert entry.source_id == "kumari_2026"
        assert entry.table_id == "Table B.1"
        assert entry.printed_page in range(119, 125)
        assert entry.pdf_page == entry.printed_page + 17
        assert entry.gaddi_ipa, f"Entry {entry.serial_number} missing IPA"
        assert entry.english_gloss, f"Entry {entry.serial_number} missing gloss"
        assert "CC BY-NC 4.0" in entry.license

    # Verify spot check entries
    w_all = [w for w in word_list if w["serial_number"] == "1.1"][0]
    assert w_all["gaddi_ipa"] == "səb"
    assert w_all["english_gloss"] == "all"

    w_heart = [w for w in word_list if w["serial_number"] == "73"][0]
    assert w_heart["gaddi_ipa"] == "dil"
    assert w_heart["english_gloss"] == "heart"

    w_bangles = [w for w in word_list if w["serial_number"] == "157"][0]
    assert w_bangles["gaddi_ipa"] == "boŋɡɽi"
    assert w_bangles["english_gloss"] == "bangles"


# =============================================================================
# 3. Appendix III: Numerals System Tests
# =============================================================================

def test_appendix_iii_numerals_completeness():
    """Verify numerals extracted from Appendix III (Tables C.1, C.2, C.3, C.4) and Ch 3.8."""
    num_data = gaddi.get_numerals()
    assert isinstance(num_data, dict)

    # Cardinals: 1 to 100, plus 1000, 100000, 10000000, 1000000000 (104 total)
    cardinals = num_data["cardinals"]
    assert len(cardinals) == 104
    assert cardinals[0]["value"] == 1
    assert cardinals[0]["gaddi_ipa"] == "əkʰ"
    assert cardinals[99]["value"] == 100
    assert cardinals[99]["gaddi_ipa"] == "sɔ"
    assert cardinals[100]["value"] == 1000
    assert cardinals[100]["gaddi_ipa"] == "jɑr"
    assert cardinals[101]["value"] == 100000
    assert cardinals[101]["gaddi_ipa"] == "ləkʰ"
    assert cardinals[102]["value"] == 10000000
    assert cardinals[102]["gaddi_ipa"] == "kror"
    assert cardinals[103]["value"] == 1000000000
    assert cardinals[103]["gaddi_ipa"] == "ərəb"

    # Spot-check tricky cardinal 65 (pɛ̃ʈʰ)
    c65 = [c for c in cardinals if c["value"] == 65][0]
    assert c65["gaddi_ipa"] == "pɛ̃ʈʰ"

    # Ordinals: 1st through 22nd (22 total)
    ordinals = num_data["ordinals"]
    assert len(ordinals) == 22
    assert ordinals[0]["rank"] == 1
    assert ordinals[0]["gloss"] == "First"
    assert ordinals[21]["rank"] == 22
    assert ordinals[21]["gloss"] == "Twenty-second"

    # Fractionals: 7 total with printed inversion note for 1/10 and 1/16
    fractionals = num_data["fractionals"]
    assert len(fractionals) == 7
    tenth = [f for f in fractionals if f["fraction"] == "1/10"][0]
    sixteenth = [f for f in fractionals if f["fraction"] == "1/16"][0]
    assert "inversion" in tenth["notes"].lower()
    assert "inversion" in sixteenth["notes"].lower()

    # Distributives: 5 total
    distributives = num_data["distributives"]
    assert len(distributives) == 5

    # Prefix and decade templates
    assert len(num_data["prefix_templates_1_to_9"]) == 9
    assert len(num_data["decade_templates"]) == 8


# =============================================================================
# 4. Chapters 1-5 Numbered Examples Tests
# =============================================================================

def test_numbered_examples_completeness_and_range():
    """Verify that all 269 numbered examples from Chapters 1-5 are cleanly parsed."""
    examples = gaddi.get_grammar_examples()
    assert len(examples) == 269, f"Expected exactly 269 examples, got {len(examples)}"

    # Ensure complete 1..269 sequence with zero gaps or duplicates
    example_nums = [e["example_number"] for e in examples]
    assert example_nums == list(range(1, 270))

    # Check chapter coverage
    chapters = {e["chapter"] for e in examples}
    assert chapters == {1, 2, 3, 4, 5}

    # Verify example 1 and example 269
    ex1 = examples[0]
    assert ex1["example_number"] == 1
    assert ex1["chapter"] == 1
    assert ex1["printed_page"] == 6
    assert ex1["pdf_page"] == 23
    assert "gʰooɽee" in ex1["raw_text"]

    ex269 = examples[-1]
    assert ex269["example_number"] == 269
    assert ex269["chapter"] == 5
    assert ex269["printed_page"] == 115
    assert ex269["pdf_page"] == 132
    assert "lɑll-ɛ" in ex269["raw_text"]

    # Filter by chapter test
    ch4_exs = gaddi.get_grammar_examples(chapter=4)
    assert len(ch4_exs) == 78
    assert all(e["chapter"] == 4 for e in ch4_exs)

    # Specific example lookup
    ex22 = gaddi.get_grammar_examples(example_number=22)
    assert len(ex22) == 1
    assert ex22[0]["example_number"] == 22


# =============================================================================
# 5. Phonology Dataset & Appendix I Discrepancies Tests
# =============================================================================

def test_phonology_dataset_and_discrepancies():
    """Verify phonology dataset, vowel/consonant charts, and documentation of App I differences."""
    phon = gaddi.get_phonology()
    assert isinstance(phon, dict)

    # Vowels
    vowels = phon["vowel_system"]
    assert vowels["total_oral_monophthongs"] == 8
    assert len(vowels["oral_monophthongs"]) == 8
    assert "/i/" in [f"/{v['ipa']}/" for v in vowels["oral_monophthongs"]]
    assert len(vowels["nasal_vowels_chapter2"]) == 3
    assert len(vowels["diphthongs"]) == 2

    # Consonants
    consonants = phon["consonant_system"]
    places = [c["place"] for c in consonants["consonants"]]
    assert "bilabial" in places
    assert "retroflex" in places

    # Discrepancies documentation
    disc = phon["appendix_i_discrepancies"]
    assert "vowels" in disc
    assert "consonants" in disc
    assert "Appendix I Table A.2" in disc["vowels"]
    assert "Chapter 2 Table 2.4" in disc["consonants"]


# =============================================================================
# 6. Sociolinguistic, Ethnographic & Fieldwork Boundary Tests
# =============================================================================

def test_sociolinguistic_notes_and_boundary():
    """Verify sociolinguistic documentation and authors' explicit variety boundary statement."""
    notes = gaddi.get_sociolinguistic_notes()
    assert isinstance(notes, dict)

    community = notes["community_profile"]
    assert community["name"] == "Gaddi"
    assert "pastoralists" in community["pastoral_identity"].lower()

    fw = notes["fieldwork_methodology"]
    villages = " ".join(fw["fieldwork_villages"])
    assert "Palampur" in villages
    assert "Saperu" in villages
    assert "Banuri" in villages
    assert "Kandbari" in villages

    # Explicit variety boundary statement
    boundary = notes["dialectological_isolation_warning"]["authors_statement_p5"]
    assert "Jammu and Kashmir" in boundary
    assert "require fresh descriptions" in boundary


# =============================================================================
# 7. References and Bibliography Tests
# =============================================================================

def test_references_and_bibliography():
    """Verify 40-item monograph bibliography and source map."""
    refs = gaddi.get_references()
    assert isinstance(refs, dict)

    bib = refs["bibliography"]
    assert len(bib) >= 40
    keys = [b["citation_key"] for b in bib]
    assert "abbi_2001" in keys
    assert "grierson_1916" in keys
    assert "mehta_2016" in keys
    assert "mehta_2021" in keys
    assert "masica_1991" in keys

    # Index terms
    index_terms = refs["index"]
    assert len(index_terms) >= 40


# =============================================================================
# 8. Strict Anti-Conflation & Zero J&K Contamination Tests
# =============================================================================

def test_strict_zero_jk_contamination():
    """CRITICAL SAFETY TEST:
    Under no circumstances should the 254 comparative entries from Kangra Gaddi
    contaminate the verified J&K lexical count or default J&K translation.
    """
    # 1. Total verified J&K lexical entries (Command 16 field documentation)
    info = gaddi.info()
    assert info["verified_jk_lexical_entries"] == 105

    # 2. Strict translation of English concepts into Gaddi must return [] by default
    # Even if 'all' or 'heart' exists in Kumari (2026), default jk_only=True returns []
    res_all_strict = gaddi.translate("all", from_lang="en", jk_only=True)
    assert res_all_strict == []

    res_heart_strict = gaddi.translate("heart", from_lang="en", jk_only=True)
    assert res_heart_strict == []

    # 3. Dedicated comparative search works cleanly and returns the Palampur comparative entry
    comp_all = gaddi.search_comparative_words("all")
    assert len(comp_all) >= 1
    assert comp_all[0]["gaddi_ipa"] == "səb"
    assert comp_all[0]["variety_id"] == "hp_kangra_palampur"
    assert comp_all[0]["evidence_status"] == "comparative_only"
    assert comp_all[0]["is_jk_verified"] is False


# =============================================================================
# 9. CLI Subcommands Tests
# =============================================================================

def test_cli_subcommands_execution(capsys):
    """Test that all newly added CLI subcommands execute cleanly and output expected markers."""
    # word-list
    ret_wl = cmd_word_list(search_query="heart", pos_filter=None, limit=5, show_all=False, as_json=False)
    assert ret_wl == 0
    out_wl = capsys.readouterr().out
    assert "dil" in out_wl
    assert "heart" in out_wl

    # numerals
    ret_num = cmd_numerals(category="cardinals", search_query=None, as_json=False)
    assert ret_num == 0
    out_num = capsys.readouterr().out
    assert "əkʰ" in out_num

    # phonology
    ret_phon = cmd_phonology(section="vowels", as_json=False)
    assert ret_phon == 0
    out_phon = capsys.readouterr().out
    assert "Oral Vowels" in out_phon

    # examples
    ret_ex = cmd_examples(chapter=1, number=1, search_query=None, limit=1, as_json=False)
    assert ret_ex == 0
    out_ex = capsys.readouterr().out
    assert "gʰooɽee" in out_ex

    # sociolinguistics
    ret_soc = cmd_sociolinguistics(section="community", as_json=False)
    assert ret_soc == 0
    out_soc = capsys.readouterr().out
    assert "pastoralists" in out_soc.lower()

    # references
    ret_ref = cmd_references(search_query="Grierson", as_json=False)
    assert ret_ref == 0
    out_ref = capsys.readouterr().out
    assert "Linguistic Survey of India" in out_ref


# =============================================================================
# 10. Audit Verification Tests: Spacing, POS, Dash Cells, Cleaning & Licensing
# =============================================================================

def test_appendix_ii_ipa_spacing_and_pos_resolution():
    """Verify that multi-word compound IPA forms preserve spacing and POS is fully resolved."""
    words = gaddi.get_comparative_word_list()
    word_map = {w["serial_number"]: w for w in words}

    # Spacing in multi-word IPA forms
    assert word_map["214.1"]["gaddi_ipa"] == "bənduk mɑrɳɑ"
    assert word_map["214.2"]["gaddi_ipa"] == "tupk mɑrɳɑ"
    assert word_map["220"]["gaddi_ipa"] == "bəʈurɑ piʈʈʰɑ"

    # Resolved parts of speech
    assert word_map["3"]["part_of_speech"] == "noun"
    assert word_map["16.1"]["part_of_speech"] == "verb"
    assert word_map["50"]["part_of_speech"] == "noun"
    assert word_map["79.1"]["part_of_speech"] == "adverb"
    assert word_map["79.2"]["part_of_speech"] == "adverb"
    assert word_map["113"]["part_of_speech"] == "particle"
    assert word_map["184.1"]["part_of_speech"] == "noun"
    assert word_map["184.2"]["part_of_speech"] == "noun"

    # Zero unspecified POS entries remaining
    unspecified = [w for w in words if w.get("part_of_speech") == "unspecified"]
    assert len(unspecified) == 0, f"Found entries with unspecified POS: {unspecified}"


def test_appendix_iii_unlexicalized_dash_cell_and_attribution():
    """Verify dash cell for Million, third-party attribution for Kumari Mamta, and fractionals."""
    num_data = gaddi.get_numerals()

    # Unlexicalized dash cell
    dash_cells = num_data.get("unlexicalized_table_cells", [])
    assert len(dash_cells) == 1
    assert dash_cells[0]["english_gloss"] == "Million"
    assert dash_cells[0]["printed_cell"] == "–"

    # Third-party attribution for Kumari Mamta
    meta = num_data.get("metadata", {})
    assert "third_party_attribution" in meta
    tpa = meta["third_party_attribution"]
    assert "Kumari Mamta" in tpa["collector"]
    assert "Jawaharlal Nehru University" in tpa["role"]

    # Fractionals printed vs resolved readings
    fractionals = num_data["fractionals"]
    tenth = [f for f in fractionals if f["fraction"] == "1/10"][0]
    sixteenth = [f for f in fractionals if f["fraction"] == "1/16"][0]
    assert tenth["printed_reading"] == "əkʰ bəʈɑ solɑ"
    assert tenth["resolved_reading"] == "əkʰ bəʈɑ dəs"
    assert sixteenth["printed_reading"] == "əkʰ bəʈɑ dəs"
    assert sixteenth["resolved_reading"] == "əkʰ bəʈɑ solɑ"

    # Ordinals printed form and derivation note
    ordinals = num_data["ordinals"]
    assert all("printed_form" in o for o in ordinals)
    assert all("derivation_note" in o for o in ordinals)

    # Distributives category tag
    distributives = num_data["distributives"]
    assert all(d.get("category") == "distributive" for d in distributives)


def test_examples_cleaning_and_header_removal():
    """Verify that numbered examples are stripped of running headers and trailing prose."""
    examples = gaddi.get_grammar_examples()
    ex_map = {e["example_number"]: e for e in examples}

    # Ex 269: clean translation without trailing prose words
    ex269 = ex_map[269]
    assert ex269["english_translation"] == "Lala too bought a book."
    assert "Ram" not in ex269["english_translation"]
    assert ex269["context_notes"] is not None

    # Ex 200: clean translation without trailing prose words
    ex200 = ex_map[200]
    assert ex200["english_translation"] == "No, cats meow."
    assert "brother" not in ex200["english_translation"]
    assert "be" not in ex200["english_translation"].split()

    # Ex 4: clean translation without analytical paragraph
    ex4 = ex_map[4]
    assert ex4["english_translation"] == "striking; striking; striking"
    assert "static past" not in ex4["english_translation"]

    # Ex 5: clean translation without vitality text
    ex5 = ex_map[5]
    assert "Bharmauri" not in ex5["english_translation"]
    assert "definitely endangered" not in ex5["english_translation"]

    # Zero running headers in raw_text of any example
    header_patterns = ["A GRAMMAR oF GADDI", "Mo RPH oSYN tAx", "MAjo R wo RD  CLA SS eS", "PHoNet ICS"]
    for ex in examples:
        raw = ex["raw_text"]
        for pat in header_patterns:
            assert pat not in raw, f"Example {ex['example_number']} contains running header: {pat}"


def test_licensing_and_provenance_metadata():
    """Verify that sources metadata and licensing terms are strictly recorded."""
    res_sources = json.loads((RES_DIR / "sources.json").read_text(encoding="utf-8"))
    k_src = [s for s in res_sources if s.get("id") == "kumari_2026"][0]

    assert "UCL Press" in k_src["required_attribution"]
    assert "10.14324/111.9781800089938" in k_src["required_attribution"]
    assert "not affiliated with, endorsed by" in k_src["non_endorsement_disclaimer"]
    assert len(k_src["adaptations_made"]) >= 5
    assert len(k_src["third_party_materials_excluded_from_cc"]) >= 4

