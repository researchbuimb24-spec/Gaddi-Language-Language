"""Core data models and schemas for the Gaddi Language Library."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class VerificationStatus(str, Enum):
    """Status of verification for an entry or linguistic assertion."""
    VERIFIED = "verified"
    PROVISIONAL = "provisional"
    DISPUTED = "disputed"
    COMPARATIVE_ONLY = "comparative_only"


class PartOfSpeech(str, Enum):
    """Standardized grammatical parts of speech."""
    NOUN = "noun"
    PROPER_NOUN = "proper_noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    POSTPOSITION = "postposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    PARTICLE = "particle"
    NUMERAL = "numeral"
    PHRASE = "phrase"
    OTHER = "other"


class GrammaticalGender(str, Enum):
    """Grammatical gender in Gaddi."""
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTER = "neuter"  # rarely used in Western Pahari, but available for comparative notes
    COMMON = "common"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class Variety:
    """Geographical or dialectal variety of Gaddi."""
    id: str
    name: str
    region_type: str
    state_ut: str
    district: str
    sub_areas: List[str] = field(default_factory=list)
    is_jk_variety: bool = False
    description: str = ""
    contact_languages: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Variety:
        return cls(
            id=data["id"],
            name=data["name"],
            region_type=data.get("region_type", "regional"),
            state_ut=data.get("state_ut", ""),
            district=data.get("district", ""),
            sub_areas=data.get("sub_areas", []),
            is_jk_variety=bool(data.get("is_jk_variety", False)),
            description=data.get("description", ""),
            contact_languages=data.get("contact_languages", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "region_type": self.region_type,
            "state_ut": self.state_ut,
            "district": self.district,
            "sub_areas": self.sub_areas,
            "is_jk_variety": self.is_jk_variety,
            "description": self.description,
            "contact_languages": self.contact_languages,
        }


@dataclass(frozen=True)
class Source:
    """Bibliographic source with licensing and geographic scope metadata."""
    id: str
    title: str
    authors: List[str]
    year: int
    publisher: str
    series: Optional[str] = None
    volume: Optional[int] = None
    doi: Optional[str] = None
    oapen_id: Optional[str] = None
    license: str = "Unspecified"
    variety_id: str = "jk_general"
    credibility_tier: int = 3
    is_jk_primary: bool = False
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Source:
        return cls(
            id=data["id"],
            title=data["title"],
            authors=data.get("authors", []),
            year=int(data["year"]),
            publisher=data.get("publisher", ""),
            series=data.get("series"),
            volume=data.get("volume"),
            doi=data.get("doi"),
            oapen_id=data.get("oapen_id"),
            license=data.get("license", "Unspecified"),
            variety_id=data.get("variety_id", "jk_general"),
            credibility_tier=int(data.get("credibility_tier", 3)),
            is_jk_primary=bool(data.get("is_jk_primary", False)),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "publisher": self.publisher,
            "series": self.series,
            "volume": self.volume,
            "doi": self.doi,
            "oapen_id": self.oapen_id,
            "license": self.license,
            "variety_id": self.variety_id,
            "credibility_tier": self.credibility_tier,
            "is_jk_primary": self.is_jk_primary,
            "notes": self.notes,
        }


@dataclass
class Attestation:
    """Exact attestation of an entry in an underlying source."""
    source_id: str
    page_or_section: str = ""
    source_spelling: str = ""
    context: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Attestation:
        return cls(
            source_id=data["source_id"],
            page_or_section=data.get("page_or_section", ""),
            source_spelling=data.get("source_spelling", ""),
            context=data.get("context", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "page_or_section": self.page_or_section,
            "source_spelling": self.source_spelling,
            "context": self.context,
        }


@dataclass
class ExampleSentence:
    """Documented example sentence with multi-lingual translations."""
    text_gaddi: str
    translation_en: str
    translation_hi: Optional[str] = None
    translation_ur: Optional[str] = None
    source_citation: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExampleSentence:
        return cls(
            text_gaddi=data["text_gaddi"],
            translation_en=data["translation_en"],
            translation_hi=data.get("translation_hi"),
            translation_ur=data.get("translation_ur"),
            source_citation=data.get("source_citation"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text_gaddi": self.text_gaddi,
            "translation_en": self.translation_en,
            "translation_hi": self.translation_hi,
            "translation_ur": self.translation_ur,
            "source_citation": self.source_citation,
        }


@dataclass
class Sense:
    """Word sense with definitions in priority languages."""
    sense_index: int
    definition_en: str
    definition_hi: Optional[str] = None
    definition_ur: Optional[str] = None
    semantic_field: Optional[str] = None
    examples: List[ExampleSentence] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Sense:
        examples = [
            ExampleSentence.from_dict(ex)
            for ex in data.get("examples", [])
        ]
        return cls(
            sense_index=int(data.get("sense_index", 1)),
            definition_en=data["definition_en"],
            definition_hi=data.get("definition_hi"),
            definition_ur=data.get("definition_ur"),
            semantic_field=data.get("semantic_field"),
            examples=examples,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sense_index": self.sense_index,
            "definition_en": self.definition_en,
            "definition_hi": self.definition_hi,
            "definition_ur": self.definition_ur,
            "semantic_field": self.semantic_field,
            "examples": [ex.to_dict() for ex in self.examples],
        }


@dataclass
class LexicalEntry:
    """Primary unit of lexical documentation in the Gaddi language."""
    id: str
    lemma_devanagari: str
    variety_id: str
    senses: List[Sense]
    attestations: List[Attestation]
    lemma_ipa: Optional[str] = None
    lemma_perso_arabic: Optional[str] = None
    lemma_takri: Optional[str] = None
    part_of_speech: str = "noun"
    gender: Optional[str] = None
    status: str = "verified"
    comparative_notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LexicalEntry:
        senses = [Sense.from_dict(s) for s in data.get("senses", [])]
        attestations = [Attestation.from_dict(a) for a in data.get("attestations", [])]
        return cls(
            id=data["id"],
            lemma_devanagari=data["lemma_devanagari"],
            variety_id=data["variety_id"],
            senses=senses,
            attestations=attestations,
            lemma_ipa=data.get("lemma_ipa"),
            lemma_perso_arabic=data.get("lemma_perso_arabic"),
            lemma_takri=data.get("lemma_takri"),
            part_of_speech=data.get("part_of_speech", "noun"),
            gender=data.get("gender"),
            status=data.get("status", "verified"),
            comparative_notes=data.get("comparative_notes"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "lemma_devanagari": self.lemma_devanagari,
            "lemma_ipa": self.lemma_ipa,
            "lemma_perso_arabic": self.lemma_perso_arabic,
            "lemma_takri": self.lemma_takri,
            "variety_id": self.variety_id,
            "part_of_speech": self.part_of_speech,
            "gender": self.gender,
            "status": self.status,
            "senses": [s.to_dict() for s in self.senses],
            "attestations": [a.to_dict() for a in self.attestations],
            "comparative_notes": self.comparative_notes,
            "metadata": self.metadata,
        }


@dataclass
class ValidationError:
    """A blocking schema or provenance validation failure."""
    entry_id: str
    field_name: str
    message: str


@dataclass
class ValidationWarning:
    """A non-blocking advisory note on data completeness."""
    entry_id: str
    field_name: str
    message: str


@dataclass
class ValidationReport:
    """Aggregated results of data validation checks."""
    total_checked: int = 0
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationWarning] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

