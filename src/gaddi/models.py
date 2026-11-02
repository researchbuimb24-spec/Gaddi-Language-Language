"""Core data models, schemas, and evidence classifications for Gaddi."""

from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EvidenceStatus(str, Enum):
    """Rigorous evidence classification for lexical items and linguistic claims.

    Guarantees that comparative, cultural, ecological, or unverified data is never
    conflated with empirically verified Jammu & Kashmir Gaddi lexical data.
    """
    VERIFIED_JK_LEXICAL = "verified_jk_lexical"
    JK_CULTURAL_TERM = "jk_cultural_term"
    JK_PLACE_OR_ECOLOGICAL_TERM = "jk_place_or_ecological_term"
    DOCUMENTED_OTHER_VARIETY = "documented_other_variety"
    COMPARATIVE_ONLY = "comparative_only"
    COMMUNITY_SUBMITTED_UNVERIFIED = "community_submitted_unverified"
    UNVERIFIED_LEAD = "unverified_lead"
    DISPUTED = "disputed"

    # Command 11 & J&K primary source evidence statuses
    JK_FIELD_ATTESTED = "jk_field_attested"
    JK_SOURCE_ATTESTED = "jk_source_attested"
    HISTORICAL_ATTESTED = "historical_attested"
    LOCATION_UNVERIFIED = "location_unverified"
    SOURCE_METADATA_ONLY = "source_metadata_only"
    NEEDS_MANUAL_REVIEW = "needs_manual_review"

    # Backwards-compatibility alias
    VERIFIED_JK = "verified_jk_lexical"


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
    NEUTER = "neuter"
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
    """Bibliographic source with licensing, verification, and geographic scope metadata."""
    id: str
    title: str
    authors: List[str]
    year: int
    publisher: str
    series: Optional[str] = None
    volume: Optional[int] = None
    doi: Optional[str] = None
    isbn: Optional[str] = None
    url: Optional[str] = None
    license: str = "Unspecified"
    variety_id: str = "jk_general"
    credibility_tier: int = 3
    is_jk_primary: bool = False
    evidence_type: str = "academic_fieldwork"
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
            isbn=data.get("isbn"),
            url=data.get("url"),
            license=data.get("license", "Unspecified"),
            variety_id=data.get("variety_id", "jk_general"),
            credibility_tier=int(data.get("credibility_tier", 3)),
            is_jk_primary=bool(data.get("is_jk_primary", False)),
            evidence_type=data.get("evidence_type", "academic_fieldwork"),
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
            "isbn": self.isbn,
            "url": self.url,
            "license": self.license,
            "variety_id": self.variety_id,
            "credibility_tier": self.credibility_tier,
            "is_jk_primary": self.is_jk_primary,
            "evidence_type": self.evidence_type,
            "notes": self.notes,
        }


@dataclass
class Attestation:
    """Exact attestation of an entry in an underlying source."""
    source_id: str
    page_or_section: str = ""
    source_spelling: str = ""
    context: str = ""
    transcription_raw: Optional[str] = None
    verified: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Attestation:
        return cls(
            source_id=data["source_id"],
            page_or_section=data.get("page_or_section", ""),
            source_spelling=data.get("source_spelling", ""),
            context=data.get("context", ""),
            transcription_raw=data.get("transcription_raw"),
            verified=data.get("verified"),
        )

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "source_id": self.source_id,
            "page_or_section": self.page_or_section,
            "source_spelling": self.source_spelling,
            "context": self.context,
        }
        if self.transcription_raw is not None:
            d["transcription_raw"] = self.transcription_raw
        if self.verified is not None:
            d["verified"] = self.verified
        return d


@dataclass
class ExampleSentence:
    """Documented example sentence with multi-lingual translations and citation."""
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
    """Word sense with definitions in priority languages (EN, HI, UR)."""
    sense_index: int
    definition_en: str
    definition_hi: Optional[str] = None
    definition_ur: Optional[str] = None
    semantic_field: Optional[str] = None
    examples: List[ExampleSentence] = field(default_factory=list)
    source_item: Optional[str] = None

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
            source_item=data.get("source_item"),
        )

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "sense_index": self.sense_index,
            "definition_en": self.definition_en,
            "definition_hi": self.definition_hi,
            "definition_ur": self.definition_ur,
            "semantic_field": self.semantic_field,
            "examples": [ex.to_dict() for ex in self.examples],
        }
        if self.source_item is not None:
            res["source_item"] = self.source_item
        return res


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
    original_transcription: Optional[str] = None
    normalized_headword: Optional[str] = None
    part_of_speech: str = "noun"
    gender: Optional[str] = None
    evidence_status: str = "jk_cultural_term"
    status: InitVar[Optional[str]] = None
    comparative_notes: Optional[str] = None
    editorial_notes: Optional[str] = None
    homonym_index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self, status):
        if status is None:
            return
        if status == "verified":
            self.evidence_status = "verified_jk_lexical" if self.variety_id.startswith("jk_") else "documented_other_variety"
        elif status == "comparative_only":
            self.evidence_status = "comparative_only"
        else:
            self.evidence_status = status

    @property
    def is_verified_jk_lexical(self) -> bool:
        """Whether this entry is a verified Gaddi linguistic lexical item from J&K."""
        return self.evidence_status in (EvidenceStatus.VERIFIED_JK_LEXICAL.value, "verified_jk")

    @property
    def is_cultural_or_ecological_term(self) -> bool:
        """Whether this entry is a cultural, ethnographic, or regional ecological term."""
        return self.evidence_status in (
            EvidenceStatus.JK_CULTURAL_TERM.value,
            EvidenceStatus.JK_PLACE_OR_ECOLOGICAL_TERM.value,
        )

    @property
    def is_comparative(self) -> bool:
        """Whether this entry is comparative/non-J&K material."""
        return self.evidence_status in (
            EvidenceStatus.COMPARATIVE_ONLY.value,
            EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LexicalEntry:
        senses = [Sense.from_dict(s) for s in data.get("senses", [])]
        attestations = [Attestation.from_dict(a) for a in data.get("attestations", [])]
        
        # Support backwards-compat with legacy 'status' field
        evidence_status = data.get("evidence_status")
        if not evidence_status:
            legacy_status = data.get("status", "verified_jk")
            if legacy_status == "verified":
                evidence_status = "verified_jk" if data.get("variety_id", "").startswith("jk_") else "documented_other_variety"
            elif legacy_status == "comparative_only":
                evidence_status = "comparative_only"
            else:
                evidence_status = legacy_status

        return cls(
            id=data["id"],
            lemma_devanagari=data["lemma_devanagari"],
            variety_id=data["variety_id"],
            senses=senses,
            attestations=attestations,
            lemma_ipa=data.get("lemma_ipa"),
            lemma_perso_arabic=data.get("lemma_perso_arabic"),
            lemma_takri=data.get("lemma_takri"),
            original_transcription=data.get("original_transcription"),
            normalized_headword=data.get("normalized_headword"),
            part_of_speech=data.get("part_of_speech", "noun"),
            gender=data.get("gender"),
            evidence_status=evidence_status,
            comparative_notes=data.get("comparative_notes"),
            editorial_notes=data.get("editorial_notes"),
            homonym_index=data.get("homonym_index"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "id": self.id,
            "lemma_devanagari": self.lemma_devanagari,
            "lemma_ipa": self.lemma_ipa,
            "lemma_perso_arabic": self.lemma_perso_arabic,
            "lemma_takri": self.lemma_takri,
            "original_transcription": self.original_transcription,
            "normalized_headword": self.normalized_headword,
            "variety_id": self.variety_id,
            "part_of_speech": self.part_of_speech,
            "gender": self.gender,
            "evidence_status": self.evidence_status,
            "senses": [s.to_dict() for s in self.senses],
            "attestations": [a.to_dict() for a in self.attestations],
            "comparative_notes": self.comparative_notes,
            "editorial_notes": self.editorial_notes,
            "metadata": self.metadata,
        }
        if self.homonym_index is not None:
            res["homonym_index"] = self.homonym_index
        return res


@dataclass
class ValidationError:
    """A blocking schema, provenance, or linguistic integrity failure."""
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


@dataclass(frozen=True)
class ResearchLead:
    """Documented research lead or archive evaluated for J&K Gaddi linguistic evidence."""
    lead_id: str
    title: str
    authors_or_institution: List[str]
    year: Union[int, str]
    publisher_or_archive: str
    geographic_scope: str
    variety_coverage: str
    contains_linguistic_data: bool
    data_type: str
    lexical_content_type: str
    status: str
    full_source_accessible: bool
    page_or_section: str = ""
    identifier_or_url: str = ""
    license_or_rights: str = "Unspecified"
    evidence_evaluation: str = ""
    actionable_next_steps: str = ""
    # Command 5 Enhanced Verification Fields
    bibliographic_verified: bool = False
    contents_verified: bool = False
    full_text_accessible: bool = False
    varieties_documented: List[str] = field(default_factory=list)
    relevant_pages: str = ""
    linguistic_data_type: str = ""
    access_status: str = ""
    verification_notes: str = ""
    # Command 7 Audit and Digital Access Verification Fields
    digitized_record_found: bool = False
    preview_available: bool = False
    relevant_pages_accessible: bool = False
    evidence_claim_tier: str = "unverified_or_removed"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ResearchLead:
        full_accessible = bool(data.get("full_text_accessible", data.get("full_source_accessible", False)))
        return cls(
            lead_id=data["lead_id"],
            title=data["title"],
            authors_or_institution=data.get("authors_or_institution", []),
            year=data.get("year", ""),
            publisher_or_archive=data.get("publisher_or_archive", ""),
            geographic_scope=data.get("geographic_scope", ""),
            variety_coverage=data.get("variety_coverage", ""),
            contains_linguistic_data=bool(data.get("contains_linguistic_data", False)),
            data_type=data.get("data_type", "unverified"),
            lexical_content_type=data.get("lexical_content_type", "none"),
            status=data.get("status", "unverified_lead"),
            full_source_accessible=full_accessible,
            page_or_section=data.get("page_or_section", ""),
            identifier_or_url=data.get("identifier_or_url", ""),
            license_or_rights=data.get("license_or_rights", "Unspecified"),
            evidence_evaluation=data.get("evidence_evaluation", ""),
            actionable_next_steps=data.get("actionable_next_steps", ""),
            bibliographic_verified=bool(data.get("bibliographic_verified", False)),
            contents_verified=bool(data.get("contents_verified", False)),
            full_text_accessible=full_accessible,
            varieties_documented=data.get("varieties_documented", []),
            relevant_pages=data.get("relevant_pages", data.get("page_or_section", "")),
            linguistic_data_type=data.get("linguistic_data_type", data.get("data_type", "")),
            access_status=data.get("access_status", data.get("status", "")),
            verification_notes=data.get("verification_notes", ""),
            digitized_record_found=bool(data.get("digitized_record_found", False)),
            preview_available=bool(data.get("preview_available", False)),
            relevant_pages_accessible=bool(data.get("relevant_pages_accessible", False)),
            evidence_claim_tier=data.get("evidence_claim_tier", "unverified_or_removed"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lead_id": self.lead_id,
            "title": self.title,
            "authors_or_institution": self.authors_or_institution,
            "year": self.year,
            "publisher_or_archive": self.publisher_or_archive,
            "geographic_scope": self.geographic_scope,
            "variety_coverage": self.variety_coverage,
            "contains_linguistic_data": self.contains_linguistic_data,
            "data_type": self.data_type,
            "lexical_content_type": self.lexical_content_type,
            "status": self.status,
            "full_source_accessible": self.full_source_accessible,
            "page_or_section": self.page_or_section,
            "identifier_or_url": self.identifier_or_url,
            "license_or_rights": self.license_or_rights,
            "evidence_evaluation": self.evidence_evaluation,
            "actionable_next_steps": self.actionable_next_steps,
            "bibliographic_verified": self.bibliographic_verified,
            "contents_verified": self.contents_verified,
            "full_text_accessible": self.full_text_accessible,
            "varieties_documented": self.varieties_documented,
            "relevant_pages": self.relevant_pages,
            "linguistic_data_type": self.linguistic_data_type,
            "access_status": self.access_status,
            "verification_notes": self.verification_notes,
            "digitized_record_found": self.digitized_record_found,
            "preview_available": self.preview_available,
            "relevant_pages_accessible": self.relevant_pages_accessible,
            "evidence_claim_tier": self.evidence_claim_tier,
        }


@dataclass(frozen=True)
class WordListEntry:
    """An entry from the basic comparative word list (Kumari et al. 2026, Appendix II)."""
    entry_id: str
    serial_number: str
    gaddi_ipa: str
    english_gloss: str
    part_of_speech: str
    gaddi_raw: str = ""
    base_serial: int = 0
    sub_serial: Optional[int] = None
    variety_id: str = "hp_kangra_palampur"
    variety_name: str = "Kangra Gaddi (Palampur)"
    source_id: str = "kumari_2026"
    source_citation: str = "Kumari et al. (2026), Table B.1, p. 119"
    attribution: str = "List based on Abbi (2001, p. 244)"
    printed_page: int = 119
    pdf_page: int = 136
    table_id: str = "Table B.1"
    evidence_status: str = "comparative_only"
    is_jk_verified: bool = False
    license: str = "CC BY-NC 4.0 (Non-commercial research use only; third-party exclusions apply)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WordListEntry:
        return cls(
            entry_id=data["entry_id"],
            serial_number=str(data["serial_number"]),
            gaddi_ipa=data["gaddi_ipa"],
            english_gloss=data["english_gloss"],
            part_of_speech=data.get("part_of_speech", ""),
            gaddi_raw=data.get("gaddi_raw", ""),
            base_serial=int(data.get("base_serial", 0)),
            sub_serial=data.get("sub_serial"),
            variety_id=data.get("variety_id", "hp_kangra_palampur"),
            variety_name=data.get("variety_name", "Kangra Gaddi (Palampur)"),
            source_id=data.get("source_id", "kumari_2026"),
            source_citation=data.get("source_citation", "Kumari et al. (2026), Table B.1"),
            attribution=data.get("attribution", "List based on Abbi (2001, p. 244)"),
            printed_page=int(data.get("printed_page", 119)),
            pdf_page=int(data.get("pdf_page", 136)),
            table_id=data.get("table_id", "Table B.1"),
            evidence_status=data.get("evidence_status", "comparative_only"),
            is_jk_verified=bool(data.get("is_jk_verified", False)),
            license=data.get("license", "CC BY-NC 4.0"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "serial_number": self.serial_number,
            "base_serial": self.base_serial,
            "sub_serial": self.sub_serial,
            "gaddi_ipa": self.gaddi_ipa,
            "gaddi_raw": self.gaddi_raw,
            "english_gloss": self.english_gloss,
            "part_of_speech": self.part_of_speech,
            "variety_id": self.variety_id,
            "variety_name": self.variety_name,
            "source_id": self.source_id,
            "source_citation": self.source_citation,
            "attribution": self.attribution,
            "printed_page": self.printed_page,
            "pdf_page": self.pdf_page,
            "table_id": self.table_id,
            "evidence_status": self.evidence_status,
            "is_jk_verified": self.is_jk_verified,
            "license": self.license,
        }


@dataclass(frozen=True)
class NumeralEntry:
    """A numeral form (cardinal, ordinal, fractional, distributive) from Appendix III."""
    value: Any
    ipa: str
    gloss_en: str
    category: str  # 'cardinal', 'ordinal', 'fractional', 'distributive'
    variety_id: str = "hp_kangra_palampur"
    source_id: str = "kumari_2026"
    table_id: str = "Table C.1"
    printed_page: int = 124
    pdf_page: int = 141
    evidence_status: str = "comparative_only"
    is_jk_verified: bool = False
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any], category: str = "cardinal") -> NumeralEntry:
        return cls(
            value=data.get("value", data.get("fraction", data.get("base_value", ""))),
            ipa=data.get("ipa", ""),
            gloss_en=data.get("gloss_en", ""),
            category=data.get("category", category),
            variety_id=data.get("variety_id", "hp_kangra_palampur"),
            source_id=data.get("source_id", "kumari_2026"),
            table_id=data.get("table_id", "Table C.1"),
            printed_page=int(data.get("printed_page", 124)),
            pdf_page=int(data.get("pdf_page", 141)),
            evidence_status=data.get("evidence_status", "comparative_only"),
            is_jk_verified=bool(data.get("is_jk_verified", False)),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "ipa": self.ipa,
            "gloss_en": self.gloss_en,
            "category": self.category,
            "variety_id": self.variety_id,
            "source_id": self.source_id,
            "table_id": self.table_id,
            "printed_page": self.printed_page,
            "pdf_page": self.pdf_page,
            "evidence_status": self.evidence_status,
            "is_jk_verified": self.is_jk_verified,
            "notes": self.notes,
        }


@dataclass
class OralTradition:
    """Documented Gaddi oral tradition: folktale, legend, song, ballad, or proverb."""
    id: str
    title_en: str
    title_gaddi: Optional[str] = None
    genre: str = "folktale"  # folktale, pastoral_narrative, ainchali_ballad, love_ballad, wedding_song, proverb, seasonal_song, oral_history
    variety_id: str = "hp_chamba_bharmaur"
    community_locality: str = ""
    performer_or_collector: str = ""
    source_id: str = ""
    source_citation: str = ""
    summary_en: str = ""
    text_excerpt_gaddi: Optional[str] = None
    text_excerpt_en: Optional[str] = None
    recording_or_transcript_url: Optional[str] = None
    copyright_status: str = "Public Domain"
    evidence_status: str = "verified_traditional"  # verified_traditional, documented_academic, collection_target
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OralTradition:
        return cls(
            id=data["id"],
            title_en=data["title_en"],
            title_gaddi=data.get("title_gaddi"),
            genre=data.get("genre", "folktale"),
            variety_id=data.get("variety_id", "hp_chamba_bharmaur"),
            community_locality=data.get("community_locality", ""),
            performer_or_collector=data.get("performer_or_collector", ""),
            source_id=data.get("source_id", ""),
            source_citation=data.get("source_citation", ""),
            summary_en=data.get("summary_en", ""),
            text_excerpt_gaddi=data.get("text_excerpt_gaddi"),
            text_excerpt_en=data.get("text_excerpt_en"),
            recording_or_transcript_url=data.get("recording_or_transcript_url"),
            copyright_status=data.get("copyright_status", "Public Domain"),
            evidence_status=data.get("evidence_status", "verified_traditional"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title_en": self.title_en,
            "title_gaddi": self.title_gaddi,
            "genre": self.genre,
            "variety_id": self.variety_id,
            "community_locality": self.community_locality,
            "performer_or_collector": self.performer_or_collector,
            "source_id": self.source_id,
            "source_citation": self.source_citation,
            "summary_en": self.summary_en,
            "text_excerpt_gaddi": self.text_excerpt_gaddi,
            "text_excerpt_en": self.text_excerpt_en,
            "recording_or_transcript_url": self.recording_or_transcript_url,
            "copyright_status": self.copyright_status,
            "evidence_status": self.evidence_status,
            "metadata": self.metadata,
        }


@dataclass
class Deity:
    """Documented deity or sacred figure in Gaddi religious and ritual life."""
    id: str
    name_devanagari: str
    name_ipa: Optional[str] = None
    alternate_names: List[str] = field(default_factory=list)
    category: str = "supreme_deity"  # supreme_deity, shepherd_protector, village_patron, devi_form, ancestral_spirit
    associated_locations: List[str] = field(default_factory=list)
    ritual_roles: str = ""
    associated_festivals: List[str] = field(default_factory=list)
    traditional_offerings: Optional[str] = None
    source_id: str = ""
    source_citation: str = ""
    description: str = ""
    is_community_specific: bool = True
    regional_distinctions: Optional[str] = None
    evidence_status: str = "verified_traditional"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Deity:
        return cls(
            id=data["id"],
            name_devanagari=data["name_devanagari"],
            name_ipa=data.get("name_ipa"),
            alternate_names=data.get("alternate_names", []),
            category=data.get("category", "supreme_deity"),
            associated_locations=data.get("associated_locations", []),
            ritual_roles=data.get("ritual_roles", ""),
            associated_festivals=data.get("associated_festivals", []),
            traditional_offerings=data.get("traditional_offerings"),
            source_id=data.get("source_id", ""),
            source_citation=data.get("source_citation", ""),
            description=data.get("description", ""),
            is_community_specific=bool(data.get("is_community_specific", True)),
            regional_distinctions=data.get("regional_distinctions"),
            evidence_status=data.get("evidence_status", "verified_traditional"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name_devanagari": self.name_devanagari,
            "name_ipa": self.name_ipa,
            "alternate_names": self.alternate_names,
            "category": self.category,
            "associated_locations": self.associated_locations,
            "ritual_roles": self.ritual_roles,
            "associated_festivals": self.associated_festivals,
            "traditional_offerings": self.traditional_offerings,
            "source_id": self.source_id,
            "source_citation": self.source_citation,
            "description": self.description,
            "is_community_specific": self.is_community_specific,
            "regional_distinctions": self.regional_distinctions,
            "evidence_status": self.evidence_status,
            "metadata": self.metadata,
        }


@dataclass
class Festival:
    """Documented traditional festival or seasonal ceremony of the Gaddi community."""
    id: str
    name_devanagari: str
    name_en: str
    timing_lunar_solar: str = ""
    variety_or_region: str = ""
    purpose_and_significance: str = ""
    associated_rituals: List[str] = field(default_factory=list)
    associated_deities: List[str] = field(default_factory=list)
    source_id: str = ""
    source_citation: str = ""
    evidence_status: str = "verified_traditional"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Festival:
        return cls(
            id=data["id"],
            name_devanagari=data["name_devanagari"],
            name_en=data["name_en"],
            timing_lunar_solar=data.get("timing_lunar_solar", ""),
            variety_or_region=data.get("variety_or_region", ""),
            purpose_and_significance=data.get("purpose_and_significance", ""),
            associated_rituals=data.get("associated_rituals", []),
            associated_deities=data.get("associated_deities", []),
            source_id=data.get("source_id", ""),
            source_citation=data.get("source_citation", ""),
            evidence_status=data.get("evidence_status", "verified_traditional"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name_devanagari": self.name_devanagari,
            "name_en": self.name_en,
            "timing_lunar_solar": self.timing_lunar_solar,
            "variety_or_region": self.variety_or_region,
            "purpose_and_significance": self.purpose_and_significance,
            "associated_rituals": self.associated_rituals,
            "associated_deities": self.associated_deities,
            "source_id": self.source_id,
            "source_citation": self.source_citation,
            "evidence_status": self.evidence_status,
            "metadata": self.metadata,
        }


@dataclass
class CulturalRecord:
    """Documented cultural, pastoral, material, or social practice of the Gaddis."""
    id: str
    topic: str  # pastoral_migration, clothing_and_attire, music_and_dance, crafts_and_wool, social_organization, food_and_cuisine, village_institutions
    title: str
    term_devanagari: Optional[str] = None
    term_ipa: Optional[str] = None
    description: str = ""
    varieties: List[str] = field(default_factory=list)
    source_id: str = ""
    source_citation: str = ""
    evidence_status: str = "documented_academic"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CulturalRecord:
        return cls(
            id=data["id"],
            topic=data.get("topic", "general_culture"),
            title=data["title"],
            term_devanagari=data.get("term_devanagari"),
            term_ipa=data.get("term_ipa"),
            description=data.get("description", ""),
            varieties=data.get("varieties", []),
            source_id=data.get("source_id", ""),
            source_citation=data.get("source_citation", ""),
            evidence_status=data.get("evidence_status", "documented_academic"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "title": self.title,
            "term_devanagari": self.term_devanagari,
            "term_ipa": self.term_ipa,
            "description": self.description,
            "varieties": self.varieties,
            "source_id": self.source_id,
            "source_citation": self.source_citation,
            "evidence_status": self.evidence_status,
            "metadata": self.metadata,
        }


@dataclass
class MediaResource:
    """Documented audio recording, manuscript scan, archive entry, or photographic record."""
    id: str
    title: str
    media_type: str = "audio_recording"  # audio_recording, archival_text, manuscript_scan, photograph, map
    description: str = ""
    creator_or_collector: str = ""
    year: Optional[int] = None
    source_id: str = ""
    holding_institution: str = ""
    url_or_locator: Optional[str] = None
    license: str = "Fair Dealing / Research Consultation"
    access_status: str = "documented_archive"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MediaResource:
        return cls(
            id=data["id"],
            title=data["title"],
            media_type=data.get("media_type", "audio_recording"),
            description=data.get("description", ""),
            creator_or_collector=data.get("creator_or_collector", ""),
            year=int(data["year"]) if data.get("year") is not None else None,
            source_id=data.get("source_id", ""),
            holding_institution=data.get("holding_institution", ""),
            url_or_locator=data.get("url_or_locator"),
            license=data.get("license", "Fair Dealing / Research Consultation"),
            access_status=data.get("access_status", "documented_archive"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "description": self.description,
            "creator_or_collector": self.creator_or_collector,
            "year": self.year,
            "source_id": self.source_id,
            "holding_institution": self.holding_institution,
            "url_or_locator": self.url_or_locator,
            "license": self.license,
            "access_status": self.access_status,
            "metadata": self.metadata,
        }

