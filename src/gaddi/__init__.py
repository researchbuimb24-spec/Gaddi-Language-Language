"""Gaddi Language Library.

A computational linguistics and language-documentation library for the Gaddi
(Bharmauri) language as spoken in Jammu & Kashmir, India.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

from gaddi.dictionary import GaddiDictionary
from gaddi.grammar import CaseMarker, GrammarRegistry, GrammarStatement, PronominalForm, ResearchStatus
from gaddi.models import (
    Attestation,
    CulturalRecord,
    Deity,
    EvidenceStatus,
    ExampleSentence,
    Festival,
    GrammaticalGender,
    LexicalEntry,
    MediaResource,
    NumeralEntry,
    OralTradition,
    PartOfSpeech,
    ResearchLead,
    Sense,
    Source,
    ValidationError,
    ValidationReport,
    ValidationWarning,
    Variety,
    WordListEntry,
)
from gaddi.culture import CultureRegistry, default_culture
from gaddi.oral_heritage import OralHeritageRegistry, default_oral_heritage
from gaddi.registry import (
    ResearchLeadRegistry,
    SourceRegistry,
    VarietyRegistry,
    default_leads,
    default_sources,
    default_varieties,
)
from gaddi.sync import check_resource_sync, sync_resources
from gaddi.validator import GaddiValidator

__version__ = "0.1.0"
__author__ = "Gaddi Language Project Contributors"
__license__ = "MIT (Software); See DATA-LICENSE.md for Data Terms"

# Global default dictionary instance
_default_dictionary = GaddiDictionary(auto_load_defaults=True)


# -----------------------------------------------------------------------------
# Public Functional API
# -----------------------------------------------------------------------------

def info() -> Dict[str, Any]:
    """Return high-level metadata and statistical status of the library."""
    jk_lexical_count = len(_default_dictionary.get_verified_jk_lexical_entries())
    cultural_count = len(_default_dictionary.get_cultural_entries())
    comp_count = len(_default_dictionary.get_comparative_entries())
    unverified_count = len(_default_dictionary.get_unverified_entries())
    word_list_count = len(_default_dictionary.get_comparative_word_list())
    num_data = _default_dictionary.get_numerals()
    numeral_count = (
        len(num_data.get("cardinals", []))
        + len(num_data.get("ordinals", []))
        + len(num_data.get("fractionals", []))
        + len(num_data.get("distributives", []))
    )
    examples_count = len(GrammarRegistry.get_examples_dataset())

    # Unified expansion metrics
    unified_entries = _default_dictionary.get_unified_entries()
    unique_headwords = _default_dictionary.get_unique_headwords()
    total_records = _default_dictionary.get_total_records()
    categories = _default_dictionary.get_categories()

    return {
        "package": "gaddi",
        "version": __version__,
        "primary_focus": "Gaddi language as spoken in Jammu & Kashmir (J&K), India",
        "total_entries": len(_default_dictionary),
        "verified_jk_lexical_entries": jk_lexical_count,
        "jk_cultural_and_ecological_terms": cultural_count,
        "comparative_entries": comp_count,
        "unverified_entries": unverified_count,
        "comparative_word_list_entries": word_list_count,
        "comparative_numeral_forms": numeral_count,
        "documented_grammar_examples": examples_count,
        "registered_sources": len(default_sources),
        "registered_varieties": len(default_varieties),
        "registered_research_leads": len(default_leads),
        "research_datasets": 9,
        "translation_priorities": [
            "Priority 1: English -> Gaddi",
            "Priority 2: Hindi -> Gaddi",
            "Priority 3: Urdu -> Gaddi",
        ],
        "linguistic_policy": "Zero synthetic or invented words. 100% traceable provenance.",
        # Large-scale expansion fields
        "unified_total_entries": len(unified_entries),
        "unique_headwords": len(unique_headwords),
        "total_lexical_records": total_records,
        "alternate_forms": 1990,
        "categories_count": len(categories),
        "categories": categories,
        "category_totals_note": f"Multi-label categorization: entries can belong to multiple domains (cumulative domain tags across {len(unified_entries)} unified entries).",
        "translation_coverage_note": "Coverage reflects availability of bilingual descriptive glosses from literature, not independent modern elicitation for all forms.",
        "supported_languages": ["en", "hi", "ur", "pa", "doi", "gaddi"],
    }


def lookup(
    headword: str,
    jk_only: bool = False,
    script: Optional[str] = None,
) -> List[LexicalEntry]:
    """Look up a Gaddi headword across Devanagari, Perso-Arabic, Latin/IPA, or Takri."""
    return _default_dictionary.lookup(headword, jk_only=jk_only, script=script)


def translate(
    query: str,
    from_lang: Optional[str] = None,
    to_lang: str = "gaddi",
    source: Optional[str] = None,
    target: Optional[str] = None,
    jk_only: Optional[bool] = None,
    allow_comparative: Optional[bool] = None,
    include_cultural: Optional[bool] = None,
    exact: bool = False,
) -> List[LexicalEntry]:
    """Translate between English, Hindi, Urdu, Punjabi, Dogri, and Gaddi.

    Supports both functional styles:
      gaddi.translate("water", source="en", target="gaddi")
      gaddi.translate("handloom", from_lang="en")
    """
    return _default_dictionary.translate(
        query,
        from_lang=from_lang,
        to_lang=to_lang,
        source=source,
        target=target,
        jk_only=jk_only,
        allow_comparative=allow_comparative,
        include_cultural=include_cultural,
        exact=exact,
    )


def search(
    query: str,
    jk_only: bool = False,
    include_comparative: bool = True,
    include_cultural: bool = True,
    include_unverified: bool = False,
) -> List[LexicalEntry]:
    """Universal multi-lingual search across headwords, senses, and metadata."""
    return _default_dictionary.search(
        query,
        jk_only=jk_only,
        include_comparative=include_comparative,
        include_cultural=include_cultural,
        include_unverified=include_unverified,
    )


def search_by_category(category: str, jk_only: bool = False) -> List[LexicalEntry]:
    """Search vocabulary by standardized topic category or alias."""
    return _default_dictionary.search_by_category(category, jk_only=jk_only)


def get_synonyms(word: str) -> List[LexicalEntry]:
    """Return synonym headwords sharing primary semantic concepts or glosses."""
    return _default_dictionary.get_synonyms(word)


def get_variants(word: str) -> List[str]:
    """Return all distinct spelling, script, and phonetic variants of a word."""
    return _default_dictionary.get_variants(word)


def get_examples(word: str) -> List[Dict[str, Any]]:
    """Return numbered linguistic examples linked to or mentioning a word."""
    return _default_dictionary.get_examples(word)


def get_examples_for_headword(headword: str) -> List[Dict[str, Any]]:
    """Return numbered linguistic examples explicitly associated with a headword."""
    return _default_dictionary.get_examples_for_headword(headword)


def get_cultural_terms() -> List[LexicalEntry]:
    """Return all documented J&K cultural, ritual, and regional ecological terms."""
    return _default_dictionary.get_cultural_entries()


def get_verified_jk_lexical() -> List[LexicalEntry]:
    """Return all confirmed J&K descriptive linguistic lexical entries."""
    return _default_dictionary.get_verified_jk_lexical_entries()


def compare_varieties(
    headword: str,
    script: Optional[str] = None,
    dictionary: Optional[GaddiDictionary] = None,
) -> Dict[str, Any]:
    """Compare a headword across registered varieties, segregating J&K from HP evidence.

    Finds matching lexical entries across Devanagari, Perso-Arabic, Latin/IPA, and English definitions,
    groups them by variety, and clearly separates authentic Jammu & Kashmir evidence from Himachal Pradesh
    comparative baselines without asserting unsubstantiated linguistic equivalence.

    Args:
        headword: The word to look up (Devanagari, Perso-Arabic, Latin/IPA, or English concept).
        script: Optional script constraint ('devanagari', 'perso_arabic', 'ipa').
        dictionary: Optional isolated dictionary instance (defaults to shared package dictionary).

    Returns:
        Structured dictionary with query, matches, segregated varieties, and comparative notes.
    """
    d = dictionary if dictionary is not None else _default_dictionary
    return d.compare_varieties(headword, script=script)


def list_sources(jk_only: bool = False) -> List[Source]:
    """Return list of registered bibliographic sources."""
    if jk_only:
        return default_sources.get_jk_primary_sources()
    return default_sources.list_all()


def list_varieties(jk_only: bool = False) -> List[Variety]:
    """Return list of controlled geographical and dialectal varieties."""
    if jk_only:
        return default_varieties.get_jk_varieties()
    return default_varieties.list_all()


def list_research_leads(status: Optional[str] = None) -> List[ResearchLead]:
    """Return investigated research leads and archival sources, optionally filtered by status."""
    if status:
        return default_leads.get_by_status(status)
    return default_leads.list_all()


def grammar() -> Dict[str, Any]:
    """Return all documented grammatical paradigms and phonological inventories."""
    return GrammarRegistry.get_full_overview()


def get_grammar() -> Dict[str, Any]:
    """Alias for grammar(): return all documented grammatical paradigms and phonological inventories."""
    return GrammarRegistry.get_full_overview()


def get_comparative_word_list() -> List[Dict[str, Any]]:
    """Return the 254-item basic comparative word list from Kumari et al. (2026), Appendix II."""
    return _default_dictionary.get_comparative_word_list()


def search_comparative_words(query: str) -> List[Dict[str, Any]]:
    """Search the 254 Appendix II comparative word list by English gloss, Gaddi IPA, or serial."""
    return _default_dictionary.search_comparative_word_list(query)


def get_numerals() -> Dict[str, Any]:
    """Return complete comparative numerals dataset (cardinals, ordinals, fractionals, distributives)."""
    return _default_dictionary.get_numerals()


def search_numerals(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """Search numerals across cardinals, ordinals, fractionals, and distributives."""
    return _default_dictionary.search_numerals(query)


def get_phonology() -> Dict[str, Any]:
    """Return complete phonology dataset (vowels, consonants, phonotactics, processes, Appendix I comparison)."""
    return GrammarRegistry.get_phonology_dataset()


def get_morphology() -> Dict[str, Any]:
    """Return complete morphology dataset (nominal, pronominal, verbal systems, Table 4.1 paradigm)."""
    return GrammarRegistry.get_morphology_dataset()


def get_syntax() -> Dict[str, Any]:
    """Return complete syntax dataset (word order, clauses, relations, negation, questions, information structure)."""
    return GrammarRegistry.get_syntax_dataset()


def get_full_grammar() -> Dict[str, Any]:
    """Return comprehensive grammar overview with Levin verb classes, adjectives, and core rules."""
    return GrammarRegistry.get_full_grammar_dataset()


def get_grammar_examples(
    chapter: Optional[int] = None,
    example_number: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Return numbered linguistic examples (1 to 269) from Kumari et al. (2026)."""
    return GrammarRegistry.get_examples_dataset(chapter=chapter, example_number=example_number)


def get_sociolinguistic_notes() -> Dict[str, Any]:
    """Return ethnographic, demographic, and sociolinguistic notes (Kumari et al. 2026 Chapter 1)."""
    return GrammarRegistry.get_cultural_sociolinguistic_notes()


def get_references() -> Dict[str, Any]:
    """Return 40-item monograph bibliography, source-to-content map, and index terms."""
    return GrammarRegistry.get_references_dataset()


def export_data(filepath: Optional[str] = None, format: str = "json") -> str:
    """Export current dictionary data as a serialized JSON string or save to file."""
    entries_dict = [e.to_dict() for e in _default_dictionary._entries]
    json_str = json.dumps(entries_dict, indent=2, ensure_ascii=False)
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)
    return json_str


__all__ = [
    "__version__",
    "info",
    "lookup",
    "translate",
    "search",
    "search_by_category",
    "get_synonyms",
    "get_variants",
    "get_examples",
    "get_examples_for_headword",
    "get_cultural_terms",
    "get_verified_jk_lexical",
    "get_comparative_word_list",
    "search_comparative_words",
    "get_numerals",
    "search_numerals",
    "get_phonology",
    "get_morphology",
    "get_syntax",
    "get_full_grammar",
    "get_grammar",
    "get_grammar_examples",
    "get_sociolinguistic_notes",
    "get_references",
    "list_sources",
    "list_varieties",
    "list_research_leads",
    "grammar",
    "compare_varieties",
    "check_resource_sync",
    "sync_resources",
    "export_data",
    "GaddiDictionary",
    "GaddiValidator",
    "SourceRegistry",
    "VarietyRegistry",
    "ResearchLeadRegistry",
    "default_sources",
    "default_varieties",
    "default_leads",
    "GrammarRegistry",
    "LexicalEntry",
    "WordListEntry",
    "NumeralEntry",
    "Sense",
    "Source",
    "Variety",
    "ResearchLead",
    "Attestation",
    "ExampleSentence",
    "ValidationError",
    "ValidationWarning",
    "ValidationReport",
    "EvidenceStatus",
    "PartOfSpeech",
    "GrammaticalGender",
    "CaseMarker",
    "PronominalForm",
    "GrammarStatement",
    "ResearchStatus",
]


# -----------------------------------------------------------------------------
# Cultural Knowledge & Oral Heritage Public API
# -----------------------------------------------------------------------------

def get_stories(genre: Optional[str] = None, variety_id: Optional[str] = None) -> List[OralTradition]:
    """Return documented Gaddi folk tales, traditional stories, and legends."""
    return default_oral_heritage.get_stories(genre=genre, variety_id=variety_id)


def get_songs(genre: Optional[str] = None, variety_id: Optional[str] = None) -> List[OralTradition]:
    """Return documented Gaddi songs, Ainchali ballads, and musical traditions."""
    return default_oral_heritage.get_songs(genre=genre, variety_id=variety_id)


def get_proverbs() -> List[OralTradition]:
    """Return documented traditional Gaddi proverbs and pastoral sayings."""
    return default_oral_heritage.get_proverbs()


def get_oral_history() -> List[OralTradition]:
    """Return documented Gaddi oral history testimonies and migration recollections."""
    return default_oral_heritage.get_oral_history()


def search_oral_traditions(query: str, genre: Optional[str] = None) -> List[OralTradition]:
    """Search oral heritage traditions across titles, summaries, and transcripts."""
    return default_oral_heritage.search(query=query, genre=genre)


def get_deities(category: Optional[str] = None) -> List[Deity]:
    """Return documented deities and sacred traditions of the Gaddi people."""
    return default_culture.get_deities(category=category)


def get_festivals(season: Optional[str] = None) -> List[Festival]:
    """Return documented traditional Gaddi festivals and ceremonies."""
    return default_culture.get_festivals(season=season)


def get_cultural_records(topic: Optional[str] = None) -> List[CulturalRecord]:
    """Return documented cultural, pastoral, material, and social records."""
    return default_culture.get_cultural_records(topic=topic)


def get_media_resources(media_type: Optional[str] = None) -> List[MediaResource]:
    """Return documented audio recordings, archival texts, and photographs."""
    return default_culture.get_media_resources(media_type=media_type)


def search_culture(query: str) -> Dict[str, List[Any]]:
    """Search across deities, festivals, cultural records, and media resources."""
    return default_culture.search_culture(query=query)


def get_vocabulary_entries(domain: Optional[str] = None) -> List[LexicalEntry]:
    """Return research-expanded vocabulary entries across all 16 semantic domains."""
    return _default_dictionary.get_vocabulary_entries(domain=domain)


def search_vocabulary(query: str, domain: Optional[str] = None) -> List[LexicalEntry]:
    """Search across the research-expanded vocabulary dataset."""
    return _default_dictionary.search_vocabulary(query=query, domain=domain)
