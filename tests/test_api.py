"""Unit tests for the top-level public functional API of the gaddi package."""

import json
import pytest

import gaddi


def test_api_info():
    info = gaddi.info()
    assert isinstance(info, dict)
    assert info["package"] == "gaddi"
    assert info["version"] == gaddi.__version__
    assert info["total_entries"] == 159
    assert info["verified_jk_lexical_entries"] == 105
    assert info["jk_cultural_and_ecological_terms"] == 25
    assert info["comparative_entries"] == 29
    assert info["registered_sources"] >= 12
    assert info["registered_varieties"] >= 8
    assert len(info["translation_priorities"]) == 3


def test_api_lookup_multi_script():
    # Devanagari lookup
    res_deva = gaddi.lookup("नवाला")
    assert len(res_deva) >= 1
    assert res_deva[0].lemma_devanagari == "नवाला"
    assert res_deva[0].evidence_status == "jk_cultural_term"

    # Perso-Arabic lookup
    res_perso = gaddi.lookup("نوالہ")
    assert len(res_perso) >= 1
    assert res_perso[0].lemma_devanagari == "नवाला"

    # Latin / IPA lookup
    res_ipa = gaddi.lookup("nəˈwaːlaː")
    assert len(res_ipa) >= 1
    assert res_ipa[0].lemma_devanagari == "नवाला"


def test_api_translate_strict_lexical_policy():
    # Strict default translation (jk_only=True, include_cultural=False):
    # Must return [] because no descriptive linguistic lexicon for J&K Gaddi has verified 'handloom'
    res_strict = gaddi.translate("handloom", from_lang="en")
    assert res_strict == []

    # With include_cultural=True, returns documented J&K cultural term
    res_cult = gaddi.translate("handloom", from_lang="en", include_cultural=True)
    assert len(res_cult) >= 1
    assert any(e.lemma_devanagari == "खडे" for e in res_cult)
    assert any(e.evidence_status == "jk_cultural_term" for e in res_cult)

    # Comparative only term (water -> पाणी): must return [] by default (jk_only=True)
    res_water = gaddi.translate("water", from_lang="en")
    assert res_water == []

    # With allow_comparative=True, must return comparative entry
    res_comp = gaddi.translate("water", from_lang="en", jk_only=False, allow_comparative=True)
    assert len(res_comp) >= 1
    assert any(e.lemma_devanagari == "पाणी" for e in res_comp)
    assert any(e.evidence_status == "comparative_only" for e in res_comp)


def test_api_translate_priority2_hindi():
    # Strict returns []
    assert gaddi.translate("चोगा", from_lang="hi") == []
    # Cultural opt-in returns चोला
    res = gaddi.translate("चोगा", from_lang="hi", include_cultural=True)
    assert len(res) >= 1
    assert any(e.lemma_devanagari == "चोला" for e in res)


def test_api_translate_priority3_urdu():
    # Strict returns []
    assert gaddi.translate("ہتھ کرگھی", from_lang="ur") == []
    # Cultural opt-in returns खडे
    res = gaddi.translate("ہتھ کرگھی", from_lang="ur", include_cultural=True)
    assert len(res) >= 1
    assert any(e.lemma_devanagari == "खडे" for e in res)


def test_api_cultural_and_lexical_accessors():
    cult_terms = gaddi.get_cultural_terms()
    assert len(cult_terms) == 25
    assert all(e.evidence_status in ("jk_cultural_term", "jk_place_or_ecological_term") for e in cult_terms)

    verified_jk = gaddi.get_verified_jk_lexical()
    assert len(verified_jk) == 105


def test_api_search():
    # Search across Roman/English
    res_dora = gaddi.search("Dora")
    assert len(res_dora) >= 1
    assert any(e.lemma_devanagari == "डोरा" for e in res_dora)

    # Search with jk_only restriction
    res_jk = gaddi.search("water", jk_only=True)
    assert not any(e.lemma_devanagari == "पाणी" for e in res_jk)

    # Search with comparative included
    res_comp = gaddi.search("water", jk_only=False, include_comparative=True)
    assert any(e.lemma_devanagari == "पाणी" for e in res_comp)


def test_api_list_sources():
    all_sources = gaddi.list_sources()
    assert len(all_sources) >= 10

    jk_sources = gaddi.list_sources(jk_only=True)
    assert len(jk_sources) >= 5
    assert all(s.is_jk_primary for s in jk_sources)


def test_api_list_varieties():
    all_vars = gaddi.list_varieties()
    assert len(all_vars) >= 8

    jk_vars = gaddi.list_varieties(jk_only=True)
    assert len(jk_vars) >= 4
    assert all(v.is_jk_variety for v in jk_vars)


def test_api_grammar():
    overview = gaddi.grammar()
    assert isinstance(overview, dict)
    assert "framework" in overview
    assert "word_order" in overview
    assert "alignment" in overview
    assert "case_markers" in overview
    assert "personal_pronouns" in overview
    assert "negation" in overview
    assert len(overview["case_markers"]) >= 5
    assert len(overview["personal_pronouns"]) >= 6


def test_api_export_data():
    exported_json = gaddi.export_data()
    assert isinstance(exported_json, str)
    data = json.loads(exported_json)
    assert isinstance(data, list)
    assert len(data) >= 50
    assert any(item["id"] == "jk-cult-00001" for item in data)
