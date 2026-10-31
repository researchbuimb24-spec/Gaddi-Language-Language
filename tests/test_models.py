"""Tests for data models and schemas."""

from gaddi.models import (
    Attestation,
    ExampleSentence,
    LexicalEntry,
    Sense,
    Source,
    Variety,
)


def test_variety_creation_and_dict_roundtrip():
    v = Variety(
        id="jk_kathua_bani",
        name="Bani Gaddi",
        region_type="tehsil_cluster",
        state_ut="Jammu and Kashmir",
        district="Kathua",
        sub_areas=["Bani", "Duggan"],
        is_jk_variety=True,
        description="High altitude test",
        contact_languages=["Dogri"],
    )
    assert v.is_jk_variety is True
    d = v.to_dict()
    assert d["id"] == "jk_kathua_bani"
    v2 = Variety.from_dict(d)
    assert v == v2


def test_source_creation_and_dict_roundtrip():
    s = Source(
        id="kumari_2026",
        title="A Grammar of Gaddi",
        authors=["Preeti Kumari", "Shreya Mehta"],
        year=2026,
        publisher="UCL Press",
        license="CC BY-NC 4.0",
        credibility_tier=1,
        is_jk_primary=False,
    )
    assert s.is_jk_primary is False
    assert s.credibility_tier == 1
    d = s.to_dict()
    s2 = Source.from_dict(d)
    assert s == s2


def test_lexical_entry_serialization():
    ex = ExampleSentence(
        text_gaddi="शिव नवाले दी रात",
        translation_en="On the night of Shiv Nawala",
        translation_hi="शिव नवाले की रात",
        translation_ur="شیو نوالے کی رات",
        source_citation="nirmohi_duggar, p. 112",
    )
    sense = Sense(
        sense_index=1,
        definition_en="A thanksgiving ceremony dedicated to Shiva",
        definition_hi="शिव को समर्पित पूजा अनुष्ठान",
        definition_ur="شیو کی پوجا",
        examples=[ex],
    )
    att = Attestation(
        source_id="chakraborty_2024",
        page_or_section="p. 3",
        source_spelling="Nawala",
    )
    entry = LexicalEntry(
        id="entry-001",
        lemma_devanagari="नवाला",
        lemma_ipa="nəˈwaːlaː",
        lemma_perso_arabic="نوالہ",
        variety_id="jk_general",
        senses=[sense],
        attestations=[att],
    )
    d = entry.to_dict()
    assert d["id"] == "entry-001"
    assert d["lemma_devanagari"] == "नवाला"
    assert len(d["senses"]) == 1
    assert len(d["attestations"]) == 1

    entry2 = LexicalEntry.from_dict(d)
    assert entry2.id == entry.id
    assert entry2.senses[0].definition_en == entry.senses[0].definition_en
    assert entry2.senses[0].examples[0].text_gaddi == "शिव नवाले दी रात"

