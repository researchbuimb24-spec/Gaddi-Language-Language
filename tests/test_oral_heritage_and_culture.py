"""Comprehensive tests for Oral Heritage, Culture, and Research-Expanded Vocabulary."""

import json
from pathlib import Path

import pytest

import gaddi
from gaddi.cli import (
    cmd_culture,
    cmd_deities,
    cmd_festivals,
    cmd_proverbs,
    cmd_songs,
    cmd_stories,
    cmd_vocabulary,
)
from gaddi.culture import CultureRegistry, default_culture
from gaddi.dictionary import GaddiDictionary
from gaddi.oral_heritage import OralHeritageRegistry, default_oral_heritage
from gaddi.validator import GaddiValidator


def test_oral_heritage_registry_counts_and_genres():
    """Verify loading and integrity of stories, songs, proverbs, and oral histories."""
    registry = default_oral_heritage

    stories = registry.get_stories()
    assert len(stories) == 6
    for s in stories:
        assert s.id.startswith("gaddi-story-")
        assert len(s.title_en) > 0
        assert len(s.summary_en) > 0
        assert len(s.source_citation) > 0
        assert s.genre in {"folktale", "pastoral_narrative", "legend", "migration_tradition"}
        assert s.to_dict()["id"] == s.id

    songs = registry.get_songs()
    assert len(songs) == 6
    for s in songs:
        assert s.id.startswith("gaddi-song-")
        assert len(s.title_en) > 0
        assert len(s.source_citation) > 0
        assert s.genre in {"ainchali_ballad", "love_ballad", "pastoral_song", "wedding_song", "epic_ballad", "pastoral_narrative", "religious_song"}
        assert s.text_excerpt_gaddi is not None

    proverbs = registry.get_proverbs()
    assert len(proverbs) == 6
    for p in proverbs:
        assert p.id.startswith("gaddi-prov-")
        assert p.title_gaddi is not None
        assert len(p.title_en) > 0
        assert len(p.summary_en) > 0

    oral_histories = registry.get_oral_history()
    assert len(oral_histories) == 3
    for oh in oral_histories:
        assert oh.id.startswith("gaddi-oral-")
        assert len(oh.title_en) > 0


def test_oral_heritage_search():
    """Verify search across stories, songs, proverbs, and oral history."""
    # Search by text in story
    results = default_oral_heritage.search("prodigal")
    assert any(item.id == "gaddi-story-001" for item in results)

    # Search by genre in stories
    folktales = default_oral_heritage.get_stories(genre="folktale")
    assert len(folktales) >= 1
    assert folktales[0].id == "gaddi-story-001"

    # Search by song title
    kunjua = default_oral_heritage.search("Kunjua")
    assert any(item.id == "gaddi-song-002" for item in results or item.id == "gaddi-song-002" for item in kunjua)

    # Search proverb
    prov_results = default_oral_heritage.search("poverty")
    assert any("poverty" in p.summary_en.lower() for p in prov_results)


def test_culture_registry_counts_and_attributes():
    """Verify loading and integrity of deities, festivals, culture records, and media resources."""
    culture = default_culture

    deities = culture.get_deities()
    assert len(deities) == 8
    shiva = culture.get_deity_by_id("gaddi-deity-001")
    assert shiva is not None
    assert "शिव" in shiva.name_devanagari
    assert shiva.category == "supreme_deity"
    assert len(shiva.source_citation) > 0
    assert len(shiva.associated_locations) > 0

    kelang = culture.get_deity_by_id("gaddi-deity-002")
    assert kelang is not None
    assert "केलंग" in kelang.name_devanagari
    assert kelang.category == "shepherd_protector"

    festivals = culture.get_festivals()
    assert len(festivals) == 6
    nawala = culture.get_festival_by_id("gaddi-fest-001")
    assert nawala is not None
    assert "नवाला" in nawala.name_devanagari
    assert any("Shiva" in d for d in nawala.associated_deities)

    cultural_records = culture.get_cultural_records()
    assert len(cultural_records) == 7
    transhumance = culture.get_cultural_record_by_id("gaddi-cult-001")
    assert transhumance is not None
    assert transhumance.topic == "pastoral_migration"

    media_resources = culture.get_media_resources()
    assert len(media_resources) == 3
    assert all(m.media_type in {"audio_recording", "archival_text"} for m in media_resources)


def test_culture_search():
    """Verify search across deities, festivals, and cultural records."""
    deity_results = default_culture.search_deities("Kugti")
    assert any(d.id == "gaddi-deity-002" for d in deity_results)

    fest_results = default_culture.search_festivals("Manimahesh")
    assert any(f.id == "gaddi-fest-002" for f in fest_results)

    cult_results = default_culture.search_cultural_records("chola")
    assert any(c.id == "gaddi-cult-002" for c in cult_results)


def test_research_expanded_vocabulary():
    """Verify the 101 research-expanded vocabulary entries across 16 domains."""
    d = GaddiDictionary()
    vocab = d.get_vocabulary_entries()
    assert len(vocab) == 101

    # Check kinship domain
    kinship = d.get_vocabulary_entries(domain="family_and_kinship")
    assert len(kinship) >= 25
    bapu = d.get_vocabulary_by_id("gaddi-voc-001")
    assert bapu is not None
    assert bapu.lemma_devanagari == "बापू"
    assert bapu.part_of_speech == "noun"
    assert bapu.senses[0].definition_en == "father"
    assert bapu.attestations[0].source_id == "dar_sheikh_2022"

    trinti = next((e for e in kinship if e.lemma_devanagari == "त्रिंती"), None)
    assert trinti is not None
    assert "wife" in trinti.senses[0].definition_en

    # Check pastoral domain
    pastoral = d.get_vocabulary_entries(domain="pastoral_life")
    assert len(pastoral) >= 8
    puhal = next((e for e in pastoral if e.lemma_devanagari == "पुहाल"), None)
    assert puhal is not None

    # Check numbers and measurements from Kumari et al. 2026
    fractions = d.get_vocabulary_entries(domain="numbers_and_measurements")
    assert len(fractions) >= 5
    pauna = next((e for e in fractions if e.lemma_devanagari == "पोणे"), None)
    assert pauna is not None
    assert "three-quarters" in pauna.senses[0].definition_en

    # Search functionality
    search_res = d.search_vocabulary("father")
    assert any(e.lemma_devanagari == "बापू" for e in search_res)


def test_validator_on_new_datasets():
    """Verify validation functions on oral traditions and culture collections."""
    validator = GaddiValidator()

    rep_stories = validator.validate_oral_heritage_collection(default_oral_heritage.get_stories())
    assert rep_stories.is_valid is True, f"Story validation errors: {rep_stories.errors}"

    rep_songs = validator.validate_oral_heritage_collection(default_oral_heritage.get_songs())
    assert rep_songs.is_valid is True, f"Song validation errors: {rep_songs.errors}"

    rep_proverbs = validator.validate_oral_heritage_collection(default_oral_heritage.get_proverbs())
    assert rep_proverbs.is_valid is True, f"Proverb validation errors: {rep_proverbs.errors}"

    rep_oh = validator.validate_oral_heritage_collection(default_oral_heritage.get_oral_history())
    assert rep_oh.is_valid is True, f"Oral history validation errors: {rep_oh.errors}"

    rep_deities = validator.validate_deities_collection(default_culture.get_deities())
    assert rep_deities.is_valid is True, f"Deities validation errors: {rep_deities.errors}"

    rep_festivals = validator.validate_festivals_collection(default_culture.get_festivals())
    assert rep_festivals.is_valid is True, f"Festivals validation errors: {rep_festivals.errors}"

    rep_culture = validator.validate_cultural_records_collection(default_culture.get_cultural_records())
    assert rep_culture.is_valid is True, f"Culture validation errors: {rep_culture.errors}"

    rep_media = validator.validate_media_resources_collection(default_culture.get_media_resources())
    assert rep_media.is_valid is True, f"Media validation errors: {rep_media.errors}"


def test_top_level_package_api():
    """Verify top-level module convenience exports in gaddi/__init__.py."""
    assert len(gaddi.get_stories()) == 6
    assert len(gaddi.get_songs()) == 6
    assert len(gaddi.get_proverbs()) == 6
    assert len(gaddi.get_oral_history()) == 3
    assert len(gaddi.get_deities()) == 8
    assert len(gaddi.get_festivals()) == 6
    assert len(gaddi.get_cultural_records()) == 7
    assert len(gaddi.get_media_resources()) == 3
    assert len(gaddi.get_vocabulary_entries()) == 101

    results = gaddi.search_vocabulary("ghee")
    assert len(results) >= 1
    assert any("ghee" in s.definition_en.lower() for e in results for s in e.senses)


def test_cli_new_commands(capsys):
    """Smoke test CLI subcommands for stories, songs, proverbs, deities, festivals, culture, vocabulary."""
    # Stories
    ret = cmd_stories(genre="folktale", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "gaddi-story-001" in cap.out

    ret = cmd_stories(as_json=True)
    assert ret == 0
    cap = capsys.readouterr()
    data = json.loads(cap.out)
    assert len(data) == 6

    # Songs
    ret = cmd_songs(genre="ainchali_ballad", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "Shiv Ainchali" in cap.out

    # Proverbs
    ret = cmd_proverbs(as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "Gaddi chare bhedan" in cap.out or "गद्दी" in cap.out

    # Deities
    ret = cmd_deities(category="supreme_deity", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "शिव" in cap.out

    # Festivals
    ret = cmd_festivals(season="August", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "मणिमहेश" in cap.out or "Manimahesh" in cap.out

    # Culture
    ret = cmd_culture(topic="pastoral_migration", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "Transhumance" in cap.out

    # Vocabulary
    ret = cmd_vocabulary(domain="family_and_kinship", as_json=False)
    assert ret == 0
    cap = capsys.readouterr()
    assert "बापू" in cap.out
