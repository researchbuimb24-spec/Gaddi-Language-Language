"""Tests for the dictionary and search engine."""

from pathlib import Path
import pytest

from gaddi.dictionary import GaddiDictionary


@pytest.fixture
def dictionary():
    d = GaddiDictionary()
    seed_path = Path(__file__).parents[1] / "data" / "seed_corpus.json"
    d.load_from_json(seed_path)
    return d


def test_seed_corpus_loading(dictionary):
    assert len(dictionary) == 9
    jk_entries = dictionary.get_jk_entries()
    comp_entries = dictionary.get_comparative_entries()
    assert len(jk_entries) == 7
    assert len(comp_entries) == 2


def test_priority1_english_lookup(dictionary):
    # Search for handloom
    results = dictionary.lookup_english("handloom")
    assert len(results) >= 1
    assert results[0].lemma_devanagari == "खडे"
    assert results[0].variety_id == "jk_doda_bhadarwah"

    # Search for blanket
    results = dictionary.lookup_english("blanket")
    lemmas = {r.lemma_devanagari for r in results}
    assert "पट्टू" in lemmas


def test_priority2_hindi_lookup(dictionary):
    # Search for हथकरघा
    results = dictionary.lookup_hindi("हथकरघा")
    assert len(results) >= 1
    assert results[0].lemma_devanagari == "खडे"

    # Search for शिव
    results = dictionary.lookup_hindi("शिव")
    lemmas = {r.lemma_devanagari for r in results}
    assert "नवाला" in lemmas
    assert "अंचली" in lemmas


def test_priority3_urdu_lookup(dictionary):
    # Search for ہتھ کرگھی (handloom)
    results = dictionary.lookup_urdu("ہتھ کرگھی")
    assert len(results) >= 1
    assert results[0].lemma_devanagari == "खडे"

    # Search for چوغہ (robe/tunic)
    results = dictionary.lookup_urdu("چوغہ")
    assert len(results) >= 1
    assert results[0].lemma_devanagari == "चोला"


def test_gaddi_headword_lookup_multi_script(dictionary):
    # Devanagari lookup
    res_deva = dictionary.lookup_gaddi("नवाला")
    assert len(res_deva) == 1
    assert res_deva[0].id == "entry-jk-00001"

    # Perso-Arabic lookup
    res_arab = dictionary.lookup_gaddi("نوالہ")
    assert len(res_arab) == 1
    assert res_arab[0].id == "entry-jk-00001"

    # Latin / IPA lookup
    res_ipa = dictionary.lookup_gaddi("nəˈwaːlaː")
    assert len(res_ipa) == 1
    assert res_ipa[0].id == "entry-jk-00001"


def test_jk_only_filtering(dictionary):
    # "who" exists as comparative entry 'कुण' (Kangra)
    all_results = dictionary.lookup_english("who", jk_only=False)
    assert any(r.lemma_devanagari == "कुण" for r in all_results)

    # With jk_only=True, comparative entries must be filtered out
    jk_results = dictionary.lookup_english("who", jk_only=True)
    assert not any(r.lemma_devanagari == "कुण" for r in jk_results)


def test_universal_search(dictionary):
    res = dictionary.search("Dora")
    assert any(r.lemma_devanagari == "डोरा" for r in res)

