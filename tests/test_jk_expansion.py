"""Comprehensive test suite for Jammu & Kashmir (Bhaderwah/Doda) Gaddi expansion (Command 16).

Validates:
1. 105 verified J&K lexical entries loaded into GaddiDictionary and unified dictionary.
2. Regional variety assignment to 'jk_bhaderwah_doda'.
3. Linguistic integrity of kinship terminology (systematic classificatory merger in G0).
4. Numerals (cardinals 1-20, tens, thousand; ordinals 1st-10th, 20th, 50th, 100th).
5. Seasons and lunar-solar months with IPA transcriptions and Western Pahari features.
6. Strict provenance tracking to Hilal Ahmad Dar & Aejaz Mohammed Sheikh (2022).
"""

from pathlib import Path
import pytest

import gaddi
from gaddi.dictionary import GaddiDictionary
from gaddi.models import EvidenceStatus


@pytest.fixture
def dictionary():
    return GaddiDictionary()


def test_jk_lexical_count_and_status(dictionary):
    """Verify that exactly 105 verified J&K lexical entries are loaded and tracked."""
    verified_jk = dictionary.get_verified_jk_lexical_entries()
    assert len(verified_jk) == 105

    for entry in verified_jk:
        assert entry.variety_id == "jk_bhaderwah_doda"
        assert entry.evidence_status == EvidenceStatus.VERIFIED_JK_LEXICAL.value
        assert entry.id.startswith("jk-lex-")
        assert len(entry.attestations) >= 1
        assert entry.attestations[0].source_id == "dar_sheikh_2022"
        assert entry.lemma_ipa is not None
        assert entry.lemma_devanagari is not None


def test_unified_dictionary_includes_jk(dictionary):
    """Verify that unified dictionary contains the 105 J&K entries (total: 1971)."""
    unified = dictionary.get_unified_entries()
    assert len(unified) == 1971

    # Check for presence of verified J&K attestations in unified dictionary
    jk_in_unified = [
        e for e in unified
        if any(a.source_id == "dar_sheikh_2022" for a in e.attestations)
    ]
    assert len(jk_in_unified) == 105


def test_jk_seasons(dictionary):
    """Test seasonal cycle documented in Table 1 (p. 248)."""
    seasons = [
        ("बस्त", "bast", "Spring"),
        ("बरसाला", "barsaːla", "Rainy season"),
        ("शैर", "ʃaeːr", "Autumn"),
        ("ह्योंद", "hʲõːd", "Winter"),
    ]
    for dev, ipa, gloss in seasons:
        results = dictionary.lookup(dev, jk_only=True)
        assert len(results) >= 1, f"Failed lookup for season {dev}"
        match = next((e for e in results if e.lemma_devanagari == dev), None)
        assert match is not None, f"Exact entry for season {dev} not found"
        assert match.lemma_ipa == ipa
        assert any(gloss.lower() in s.definition_en.lower() for s in match.senses)
        assert "time_and_seasons" in match.metadata.get("categories", [])


def test_jk_months(dictionary):
    """Test 12 traditional Pahari solar-lunar months documented in Table 2 (p. 248)."""
    expected_months = [
        ("चेतर", "tʃetar"),
        ("बिसाक", "bisaːk"),
        ("जेठ", "dʒeːʈʰ"),
        ("हाड़", "haːɖ"),
        ("सवनी", "sawni"),
        ("भादू", "bʰadu"),
        ("असोझ", "asoːdʒ"),
        ("कतिक", "katɨk"),
        ("मघर", "maɡʰar"),
        ("पौह", "pɔw"),
        ("माग", "maːɡ"),
        ("फागण", "pʰaɡən"),
    ]
    for dev, ipa in expected_months:
        res = dictionary.lookup(dev, jk_only=True)
        assert len(res) >= 1, f"Month {dev} not found in J&K entries"
        match = next((e for e in res if e.lemma_devanagari == dev), None)
        assert match is not None, f"Exact entry for month {dev} not found"
        assert match.lemma_ipa == ipa


def test_jk_cardinal_numerals(dictionary):
    """Test cardinal numerals from Table 4 (pp. 249-250)."""
    sample_cardinals = [
        ("अकि", "akɨ", 1),
        ("दोय", "doːj", 2),
        ("त्रै", "trai", 3),
        ("चोर", "tʃoːr", 4),
        ("पंजी", "pandʒi", 5),
        ("चे", "tʃeː", 6),
        ("सति", "satɨ", 7),
        ("अठि", "aʈʰɨ", 8),
        ("नव", "nav", 9),
        ("दश", "daʃ", 10),
        ("बी", "biː", 20),
        ("चाली", "tʃaliː", 40),
        ("पंजा", "pandʒa", 50),
        ("शौव", "ʃov", 100),
        ("अख हज़ार", "akʰ azaːr", 1000),
    ]
    for dev, ipa, val in sample_cardinals:
        res = dictionary.lookup(dev, jk_only=True)
        assert len(res) >= 1, f"Cardinal numeral {dev} lookup failed"
        match = next((e for e in res if e.lemma_devanagari == dev), None)
        assert match is not None, f"Exact cardinal {dev} not found"
        assert match.lemma_ipa == ipa
        assert match.metadata.get("numeric_value") == val


def test_jk_ordinal_numerals(dictionary):
    """Test ordinal numerals from Table 5 (p. 250)."""
    sample_ordinals = [
        ("पहला", "pehla", 1),
        ("दुवा", "duwa", 2),
        ("त्रिया", "trija", 3),
        ("चोथा", "tʃotʰa", 4),
        ("पंज्वा", "pandʒwa", 5),
        ("छठ्वा", "tʃʰaʈʰwa", 6),
        ("सतिवा", "satɨwa", 7),
        ("अठिवा", "aʈʰɨwa", 8),
        ("नववा", "nawwa", 9),
        ("दशवा", "daʃwa", 10),
        ("बींवा", "bĩːwa", 20),
        ("पजामा", "padʒama", 50),
        ("शौमा", "ʃawma", 100),
    ]
    for dev, ipa, val in sample_ordinals:
        res = dictionary.lookup(dev, jk_only=True)
        assert len(res) >= 1, f"Ordinal numeral {dev} lookup failed"
        match = next((e for e in res if e.lemma_devanagari == dev), None)
        assert match is not None, f"Exact ordinal {dev} not found"
        assert match.lemma_ipa == ipa
        assert match.metadata.get("numeric_value") == val


def test_jk_kinship_classificatory_merger(dictionary):
    """Test the fundamental classificatory kinship mergers in Bhaderwah Gaddi.

    Dar & Sheikh (2022) document that:
    1. /ba:ji:/ merges Brother (elder/younger), FBS, FZS, MBS, MZS, and HZH.
    2. /dadda:/ merges Sister (elder/younger), FBD, FZD, MBD, MZD, and WBW.
    """
    # Male G0 umbrella
    res_baji = dictionary.lookup("बाजी", jk_only=True)
    assert len(res_baji) >= 1
    e_baji = res_baji[0]
    assert e_baji.lemma_ipa == "baːjiː"
    assert len(e_baji.senses) == 6  # 6 senses merged under single lexeme
    assert e_baji.metadata["kinship_algebra"]["generation"] == "G0"
    assert e_baji.metadata["kinship_algebra"]["sex"] == "M"

    # Female G0 umbrella
    res_dadda = dictionary.lookup("दद्दा", jk_only=True)
    assert len(res_dadda) >= 1
    e_dadda = res_dadda[0]
    assert e_dadda.lemma_ipa == "daddaː"
    assert len(e_dadda.senses) == 6
    assert e_dadda.metadata["kinship_algebra"]["generation"] == "G0"
    assert e_dadda.metadata["kinship_algebra"]["sex"] == "F"


def test_jk_kinship_cross_generation_terms(dictionary):
    """Test ascending, descending, affinal, and adoptive kinship terms."""
    key_terms = [
        ("बापू", "baːpuː", "father"),
        ("अम्मा", "ammaː", "mother"),
        ("दादा", "daːdaː", "grandfather"),
        ("दादी", "daːdiː", "grandmother"),
        ("गगरू", "ɡaɡruː", "son"),
        ("कोडे", "koɖeː", "daughter"),
        ("लाड़ा", "laːɖaː", "husband"),
        ("लाड़े", "laːɖe", "wife"),
        ("त्रिन्ति", "trintɨ", "wife"),
        ("देवर", "deːwar", "husband's younger brother"),
        ("सड़िबाइज", "saɖɨbaːj", "co-brother-in-law"),
        ("खोखलेरू गगरू", "kʰokʰaleruː ɡaɡru", "adopted son"),
        ("खोखलेरू कोडे", "kʰokʰaleruː koɖeː", "adopted daughter"),
    ]
    for dev, ipa, concept in key_terms:
        res = dictionary.lookup(dev, jk_only=True)
        assert len(res) >= 1, f"Kinship term {dev} ({concept}) not found"
        match = next((e for e in res if e.lemma_devanagari == dev), None)
        assert match is not None, f"Exact entry for kinship term {dev} not found"
        assert match.lemma_ipa == ipa
        assert any(concept.lower() in s.definition_en.lower() for s in match.senses), (
            f"Concept {concept} not in senses for {dev}"
        )


def test_jk_homograph_resolution(dictionary):
    """Test that homograph 'जेठ' (month vs husband's elder brother) is resolved gracefully."""
    res = dictionary.lookup("जेठ", jk_only=True)
    assert len(res) >= 1
    entry = res[0]
    # In unified and JK dictionary, homograph is handled with multi-sense representation
    senses_en = [s.definition_en for s in entry.senses]
    assert any("month" in s.lower() for s in senses_en)
    assert any("brother" in s.lower() for s in senses_en)
