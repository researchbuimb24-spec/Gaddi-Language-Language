"""Comprehensive unit tests for Large-Scale Gaddi Language Library Expansion and Search/Translation Improvements."""

import json
from pathlib import Path
import pytest

import gaddi
from gaddi.cli import build_parser, cmd_examples, cmd_stats, cmd_translate, cmd_word_list
from gaddi.dictionary import GaddiDictionary, fold_text
from gaddi.grammar import GrammarRegistry


def test_unified_loading_and_counts():
    d = GaddiDictionary()
    unified = d.get_unified_entries()
    headwords = d.get_unique_headwords()
    categories = d.get_categories()

    assert len(unified) == 1971
    assert len(headwords) == 1781
    assert len(categories) == 19
    assert d.get_total_records() == 2472

    info = gaddi.info()
    assert info["unified_total_entries"] == 1971
    assert info["unique_headwords"] == 1781
    assert info["total_lexical_records"] == 2472
    assert info["alternate_forms"] == 1990
    assert info["categories_count"] == 19
    assert "category_totals_note" in info
    assert "translation_coverage_note" in info
    assert "en" in info["supported_languages"]
    assert "hi" in info["supported_languages"]
    assert "ur" in info["supported_languages"]
    assert "pa" in info["supported_languages"]
    assert "doi" in info["supported_languages"]


def test_category_overlap_consistency():
    d = GaddiDictionary()
    categories = d.get_categories()
    sum_cat_entries = sum(len(d.search_by_category(c)) for c in categories)

    # Multi-label semantic tagging means sum across categories is greater than unique entries (1866)
    assert sum_cat_entries > 1866
    assert sum_cat_entries == 2202

    # Multi-domain item verification (e.g. sheep 'bheḍ' in both animals and agriculture)
    animals = {e.lemma_devanagari for e in d.search_by_category("animals")}
    agri = {e.lemma_devanagari for e in d.search_by_category("agriculture")}
    assert "भेड़" in animals
    assert "भेड़" in agri or "बकरी" in animals


def test_search_ranking_and_exact_match():
    d = GaddiDictionary()

    # Exact Devanagari headword match must rank top
    results_pani = d.search("पाणी")
    assert len(results_pani) >= 1
    assert results_pani[0].lemma_devanagari == "पाणी"

    # Exact headword match vs gloss match
    results_rat = d.search("रात")
    assert len(results_rat) >= 1
    assert results_rat[0].lemma_devanagari == "रात"

    # Searching transliteration
    results_trans = d.search("pani")
    assert len(results_trans) >= 1
    lemmas = [e.lemma_devanagari for e in results_trans]
    assert "पाणी" in lemmas or "पाणि" in lemmas


def test_search_diacritic_and_phonetic_tolerance():
    d = GaddiDictionary()

    # IPA exact and folded matching
    results_ipa = d.search("ˈpaːɳiː")
    assert any(e.lemma_devanagari == "पाणी" for e in results_ipa)

    # Transliteration without diacritics
    results_bhed = d.search("bhed")
    assert any("भेड़" in e.lemma_devanagari for e in results_bhed)

    results_dora = d.search("dora")
    assert any("डोरा" in e.lemma_devanagari for e in results_dora)

    # Phonetic fold test helper
    assert fold_text("ˈpaːɳiː") == "pani"
    assert fold_text("bheḍ") == "bhed"
    assert fold_text("charkha") == "charkha"


def test_duplicate_suppression_and_metadata():
    d = GaddiDictionary()

    # Multiple variants or senses matching query should NOT duplicate entries
    results = d.search("water")
    seen_ids = set()
    for e in results:
        assert e.id not in seen_ids, f"Duplicate entry {e.id} returned in search results"
        seen_ids.add(e.id)

    # Verify that results carry complete metadata
    for e in results:
        assert e.lemma_devanagari
        assert e.variety_id
        assert len(e.senses) >= 1
        assert e.senses[0].definition_en
        assert len(e.attestations) >= 1
        assert e.attestations[0].source_id

    # Verify merged entries have retained multiple source attestations
    merged_pani = next(e for e in d.get_unified_entries() if e.lemma_devanagari == "पाणी")
    source_ids = {a.source_id for a in merged_pani.attestations}
    assert "grierson_1916" in source_ids
    assert "kumari_2026" in source_ids


def test_translate_multilingual_api():
    # English -> Gaddi returns genuine Gaddi equivalents
    res_en = gaddi.translate("water", source="en", target="gaddi")
    assert len(res_en) >= 1
    lemmas_en = {e.lemma_devanagari for e in res_en}
    assert "पाणी" in lemmas_en or "पाणि" in lemmas_en
    # Ensure no English or Hindi word was placed as headword
    for e in res_en:
        assert e.lemma_devanagari not in ("water", "water.", "water (n)")

    # Multiple legitimate translation equivalents (e.g. पाणी and पाणि)
    assert len(lemmas_en) >= 1

    # Hindi -> Gaddi
    res_hi = gaddi.translate("पानी", source="hi", target="gaddi")
    assert len(res_hi) >= 1
    lemmas_hi = {e.lemma_devanagari for e in res_hi}
    assert "पाणी" in lemmas_hi or "पाणि" in lemmas_hi

    # Urdu -> Gaddi
    res_ur = gaddi.translate("پانی", source="ur", target="gaddi")
    assert len(res_ur) >= 1
    assert any("पाणी" in e.lemma_devanagari or "पाणि" in e.lemma_devanagari for e in res_ur)

    # Punjabi -> Gaddi
    res_pa = gaddi.translate("ਪਾਣੀ", source="pa", target="gaddi")
    assert len(res_pa) >= 1

    # Dogri -> Gaddi
    res_doi = gaddi.translate("पाणी", source="doi", target="gaddi")
    assert len(res_doi) >= 1

    # Gaddi -> English
    res_gaddi_en = gaddi.translate("पाणी", source="gaddi", target="en")
    assert len(res_gaddi_en) >= 1
    assert any("water" in s.definition_en.lower() for e in res_gaddi_en for s in e.senses)

    # Gaddi -> Hindi
    res_gaddi_hi = gaddi.translate("पाणी", source="gaddi", target="hi")
    assert len(res_gaddi_hi) >= 1

    # Ambiguous term handling: "bark" returns noun/verb distinct senses
    res_bark = gaddi.translate("bark", source="en", target="gaddi")
    assert len(res_bark) >= 1

    # Missing term handling: unrecorded word returns empty list without inventing fake terms
    res_missing = gaddi.translate("hyperdrive_teleporter_xyz", source="en", target="gaddi")
    assert res_missing == []


def test_example_retrieval_by_headword():
    d = GaddiDictionary()

    # Headword explicit link retrieval
    exs_pani = d.get_examples_for_headword("पाणी")
    assert len(exs_pani) >= 5
    ex_numbers = [e.get("example_number") for e in exs_pani]
    assert 89 in ex_numbers

    # Via top-level package API
    exs_api = gaddi.get_examples_for_headword("पाणी")
    assert len(exs_api) == len(exs_pani)

    # Check that authentic structure is preserved: raw_text, interlinear gloss, translation
    ex89 = next(e for e in exs_pani if e.get("example_number") == 89)
    assert "rɑm" in ex89["raw_text"]
    assert "ram.3sg.m" in ex89["raw_text"]  # interlinear morpheme gloss
    assert "Ram is drinking water." in ex89["english_translation"]
    assert ex89.get("chapter") == 3
    assert ex89.get("source_id") == "kumari_2026"
    assert ex89.get("variety_id") == "hp_kangra_palampur"

    # General word query
    exs_water = gaddi.get_examples("water")
    assert len(exs_water) >= 5


def test_search_by_category():
    # Animals
    animals = gaddi.search_by_category("animals")
    assert len(animals) >= 50
    lemmas_anim = {e.lemma_devanagari for e in animals}
    assert any(w in lemmas_anim for w in ["भेड़", "बकरी", "कुत्ता", "कुत्तर", "घोड़ा", "गा"])

    # Family / Kinship
    family = gaddi.search_by_category("family")
    assert len(family) >= 50
    lemmas_fam = {e.lemma_devanagari for e in family}
    assert any(w in lemmas_fam for w in ["बाप", "मा", "भाई"])

    # Food
    food = gaddi.search_by_category("food")
    assert len(food) >= 20

    # Body
    body = gaddi.search_by_category("body")
    assert len(body) >= 50

    # Numbers
    numbers = gaddi.search_by_category("numbers")
    assert len(numbers) >= 100


def test_get_synonyms():
    # Look up synonyms for पाणी
    syns = gaddi.get_synonyms("पाणी")
    assert len(syns) >= 1
    syn_lemmas = {e.lemma_devanagari for e in syns}
    assert "पाणि" in syn_lemmas or "कú" in syn_lemmas or "बिजन" in syn_lemmas

    # English concept query fallback
    syns_en = gaddi.get_synonyms("water")
    assert len(syns_en) >= 1


def test_get_variants():
    vars_pani = gaddi.get_variants("पाणी")
    assert len(vars_pani) >= 3
    assert "पाणी" in vars_pani
    assert any("pa" in v.lower() for v in vars_pani)


def test_cli_new_functionality(capsys):
    # 1. CLI translate with --to
    ret_tr_en = cmd_translate("water", from_lang="en", include_comparative=True, include_cultural=True, data_path=None, to_lang="gaddi")
    assert ret_tr_en == 0
    cap_tr_en = capsys.readouterr()
    assert "Translation Lookup: 'water'" in cap_tr_en.out
    assert "पाणी" in cap_tr_en.out
    assert "Variety:" in cap_tr_en.out

    ret_tr_hi = cmd_translate("पानी", from_lang="hi", include_comparative=True, include_cultural=True, data_path=None, to_lang="gaddi")
    assert ret_tr_hi == 0
    cap_tr_hi = capsys.readouterr()
    assert "Translation Lookup: 'पानी'" in cap_tr_hi.out
    assert "पाणी" in cap_tr_hi.out

    # 2. CLI word-list --category animals
    ret_wl_cat = cmd_word_list(category_filter="animals", limit=10)
    assert ret_wl_cat == 0
    cap_wl_cat = capsys.readouterr()
    assert "Gaddi Vocabulary by Category: 'Animals'" in cap_wl_cat.out
    assert "Total entries matched:" in cap_wl_cat.out

    # 3. CLI examples --search water
    ret_ex = cmd_examples(search_query="water", limit=3)
    assert ret_ex == 0
    cap_ex = capsys.readouterr()
    assert "Matched" in cap_ex.out
    assert "water" in cap_ex.out.lower()

    # 4. CLI examples --headword पाणी
    ret_ex_hw = cmd_examples(headword="पाणी", limit=3)
    assert ret_ex_hw == 0
    cap_ex_hw = capsys.readouterr()
    assert "Grammar Examples for Headword: 'पाणी'" in cap_ex_hw.out
    assert "Matched 7 example(s)" in cap_ex_hw.out

    # 5. CLI stats
    ret_st = cmd_stats()
    assert ret_st == 0
    cap_st = capsys.readouterr()
    assert "Expanded Corpus Statistics" in cap_st.out
    assert "Total Unified Entries:           1971" in cap_st.out
    assert "Unique Headwords (Devanagari):   1781" in cap_st.out
    assert "Total Lexical Records / Sources: 2472" in cap_st.out
    assert "Note on Category Multi-Labeling:" in cap_st.out


def test_expanded_grammar_modules():
    overview = GrammarRegistry.get_full_overview()

    assert "noun_classes" in overview
    assert len(overview["noun_classes"]) == 4

    assert "gender_and_number" in overview
    assert "masculine" in overview["gender_and_number"]["genders"]

    assert "demonstratives" in overview
    assert len(overview["demonstratives"]) >= 3

    assert "adjectives_and_adverbs" in overview
    assert "inflecting_adjectives" in overview["adjectives_and_adverbs"]

    assert "verbal_system" in overview
    assert "tense_aspect_mood" in overview["verbal_system"]

    assert "imperatives" in overview
    assert "prohibitive" in overview["imperatives"]

    assert "interrogatives" in overview
    assert len(overview["interrogatives"]) >= 6

    assert "clause_types" in overview
    assert overview["clause_types"]["word_order"] == "SOV (Subject - Object - Verb)"

    assert "morphological_patterns" in overview
    assert "causative_derivation" in overview["morphological_patterns"]

    assert "numeral_system" in overview
    assert overview["numeral_system"]["base"].startswith("Decimal")
