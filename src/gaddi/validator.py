"""Validation engine for linguistic integrity, provenance, and anti-conflation rules."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from gaddi.models import (
    CulturalRecord,
    Deity,
    EvidenceStatus,
    Festival,
    LexicalEntry,
    MediaResource,
    OralTradition,
    ValidationError,
    ValidationReport,
    ValidationWarning,
)
from gaddi.registry import SourceRegistry, VarietyRegistry, default_sources, default_varieties

VALID_EVIDENCE_STATUSES = {s.value for s in EvidenceStatus} | {"verified_jk"}

LINGUISTIC_EVIDENCE_TYPES = {
    "linguistic_grammar",
    "descriptive_grammar_phonology",
    "historical_linguistic_lexical",
    "linguistic_fieldwork",
    "fieldwork_sociolinguistic_vocabulary",
}


class GaddiValidator:
    """Validator enforcing strict linguistic and provenance rules for Gaddi data."""

    def __init__(
        self,
        source_registry: Optional[SourceRegistry] = None,
        variety_registry: Optional[VarietyRegistry] = None,
    ):
        self.sources = source_registry or default_sources
        self.varieties = variety_registry or default_varieties

    def validate_entry(self, entry: LexicalEntry) -> List[ValidationError]:
        """Validate a single entry and return all blocking errors."""
        errors: List[ValidationError] = []

        # 1. Entry ID check
        if not entry.id or not entry.id.strip():
            errors.append(ValidationError("", "id", "Entry ID cannot be empty."))

        # 2. Evidence status validation
        if not entry.evidence_status:
            errors.append(
                ValidationError(entry.id, "evidence_status", "Evidence status is mandatory.")
            )
        elif entry.evidence_status not in VALID_EVIDENCE_STATUSES:
            errors.append(
                ValidationError(
                    entry.id,
                    "evidence_status",
                    f"Invalid evidence status '{entry.evidence_status}'. "
                    f"Must be one of: {sorted(VALID_EVIDENCE_STATUSES)}",
                )
            )

        # 3. Variety validation
        variety = None
        if not entry.variety_id:
            errors.append(ValidationError(entry.id, "variety_id", "Variety ID is missing."))
        elif not self.varieties.contains(entry.variety_id):
            errors.append(
                ValidationError(
                    entry.id,
                    "variety_id",
                    f"Unknown variety ID '{entry.variety_id}'. Must be registered in varieties catalog.",
                )
            )
        else:
            variety = self.varieties.get(entry.variety_id)

        # 4. Headword presence
        if not entry.lemma_devanagari or not entry.lemma_devanagari.strip():
            errors.append(
                ValidationError(
                    entry.id,
                    "lemma_devanagari",
                    "Headword in Devanagari script is mandatory.",
                )
            )

        # 5. Senses validation
        if not entry.senses:
            errors.append(
                ValidationError(
                    entry.id,
                    "senses",
                    "Entry must contain at least one sense definition.",
                )
            )
        else:
            for i, sense in enumerate(entry.senses):
                if not sense.definition_en or not sense.definition_en.strip():
                    errors.append(
                        ValidationError(
                            entry.id,
                            f"senses[{i}].definition_en",
                            "English definition (Priority 1) is mandatory for every sense.",
                        )
                    )

        # 6. Attestation and Source Traceability
        if not entry.attestations:
            errors.append(
                ValidationError(
                    entry.id,
                    "attestations",
                    "Entry has zero source attestations. Every item must have traceable provenance.",
                )
            )
        else:
            has_jk_source = False
            has_jk_linguistic_source = False

            for j, attestation in enumerate(entry.attestations):
                if not attestation.source_id:
                    errors.append(
                        ValidationError(
                            entry.id,
                            f"attestations[{j}].source_id",
                            "Source ID is empty.",
                        )
                    )
                    continue

                source = self.sources.get(attestation.source_id)
                if not source:
                    errors.append(
                        ValidationError(
                            entry.id,
                            f"attestations[{j}].source_id",
                            f"Unregistered source ID '{attestation.source_id}'. Must exist in sources catalog.",
                        )
                    )
                else:
                    if source.is_jk_primary:
                        has_jk_source = True
                        if source.evidence_type in LINGUISTIC_EVIDENCE_TYPES:
                            has_jk_linguistic_source = True

                # Check page/section or context presence
                if not attestation.page_or_section and not attestation.context:
                    errors.append(
                        ValidationError(
                            entry.id,
                            f"attestations[{j}]",
                            f"Attestation for source '{attestation.source_id}' lacks page/section or context.",
                        )
                    )

            # Strict anti-conflation guardrail 1:
            # Cannot claim verified J&K lexical status without a J&K source providing linguistic lexical evidence
            is_claimed_jk_lexical = entry.evidence_status in (
                EvidenceStatus.VERIFIED_JK_LEXICAL.value,
                "verified_jk",
            )
            if is_claimed_jk_lexical:
                if not has_jk_source:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "evidence_status",
                            "Entry claims J&K variety but lacks any J&K primary source attestation. "
                            "A non-J&K source (such as Kumari et al. 2026 or Grierson 1916) cannot validate J&K status.",
                        )
                    )
                elif not has_jk_linguistic_source:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "evidence_status",
                            "Entry is marked as verified J&K lexical, but its cited J&K source(s) only provide "
                            "ethnographic/cultural/demographic evidence, not descriptive linguistic lexical documentation. "
                            "Reclassify as 'jk_cultural_term' or 'jk_place_or_ecological_term'.",
                        )
                    )
                if variety and not variety.is_jk_variety:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "variety_id",
                            f"Entry has evidence_status '{entry.evidence_status}' but variety '{entry.variety_id}' is not in J&K.",
                        )
                    )

            # Strict anti-conflation guardrail 2:
            # Cultural or ecological term must be from a J&K primary source and J&K variety
            is_cultural_or_eco = entry.evidence_status in (
                EvidenceStatus.JK_CULTURAL_TERM.value,
                EvidenceStatus.JK_PLACE_OR_ECOLOGICAL_TERM.value,
            )
            if is_cultural_or_eco:
                if not has_jk_source:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "evidence_status",
                            f"Entry is marked as '{entry.evidence_status}' but lacks a J&K primary source attestation.",
                        )
                    )
                if variety and not variety.is_jk_variety:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "variety_id",
                            f"Cultural/ecological term '{entry.id}' must be assigned a J&K variety, not '{entry.variety_id}'.",
                        )
                    )

            # Strict anti-conflation guardrail 3:
            # Comparative-only entry must NOT be assigned a J&K variety
            is_comparative = entry.evidence_status in (
                EvidenceStatus.COMPARATIVE_ONLY.value,
                EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value,
            )
            if is_comparative:
                if variety and variety.is_jk_variety:
                    errors.append(
                        ValidationError(
                            entry.id,
                            "variety_id",
                            f"Comparative-only entry cannot be assigned J&K variety '{entry.variety_id}'. "
                            "Use 'hp_kangra_palampur', 'hp_chamba_bharmaur', or 'comparative_historical'.",
                        )
                    )

        return errors

    def check_warnings(self, entry: LexicalEntry) -> List[ValidationWarning]:
        """Check for non-blocking data completeness advisories."""
        warnings: List[ValidationWarning] = []

        # Check for IPA transcription
        if not entry.lemma_ipa:
            warnings.append(
                ValidationWarning(
                    entry.id,
                    "lemma_ipa",
                    "IPA phonetic transcription is missing.",
                )
            )

        # Check for priority translations in senses
        for i, sense in enumerate(entry.senses):
            if not sense.definition_hi:
                warnings.append(
                    ValidationWarning(
                        entry.id,
                        f"senses[{i}].definition_hi",
                        "Hindi definition (Priority 2) is missing.",
                    )
                )
            if not sense.definition_ur:
                warnings.append(
                    ValidationWarning(
                        entry.id,
                        f"senses[{i}].definition_ur",
                        "Urdu definition (Priority 3) is missing.",
                    )
                )

            # Check example sentence citations
            for k, ex in enumerate(sense.examples):
                if not ex.source_citation:
                    warnings.append(
                        ValidationWarning(
                            entry.id,
                            f"senses[{i}].examples[{k}].source_citation",
                            "Example sentence lacks an explicit source citation.",
                        )
                    )

        # Warning for unverified leads or community submissions
        if entry.evidence_status in (
            EvidenceStatus.COMMUNITY_SUBMITTED_UNVERIFIED.value,
            EvidenceStatus.UNVERIFIED_LEAD.value,
            EvidenceStatus.DISPUTED.value,
        ):
            warnings.append(
                ValidationWarning(
                    entry.id,
                    "evidence_status",
                    f"Entry has unverified or provisional status: '{entry.evidence_status}'.",
                )
            )

        return warnings

    def validate_collection(self, entries: List[LexicalEntry]) -> ValidationReport:
        """Validate a collection of entries, checking individual entries and global duplicates."""
        report = ValidationReport(total_checked=len(entries))
        seen_keys: Set[str] = set()

        for entry in entries:
            # Individual entry checks
            errors = self.validate_entry(entry)
            warnings = self.check_warnings(entry)

            report.errors.extend(errors)
            report.warnings.extend(warnings)

            # Global duplicate check: same lemma in Devanagari + same variety + same POS (+ optional homonym_index)
            dup_key = f"{entry.lemma_devanagari.strip()}::{entry.variety_id}::{entry.part_of_speech}"
            if entry.homonym_index is not None:
                dup_key += f"::homonym_{entry.homonym_index}"
            if dup_key in seen_keys:
                report.errors.append(
                    ValidationError(
                        entry.id,
                        "lemma_devanagari",
                        f"Duplicate entry found for '{entry.lemma_devanagari}' in variety '{entry.variety_id}' "
                        f"with part of speech '{entry.part_of_speech}'.",
                    )
                )
            else:
                seen_keys.add(dup_key)

        return report

    # -------------------------------------------------------------------------
    # Oral Heritage, Cultural Knowledge, and Media Validation
    # -------------------------------------------------------------------------
    def validate_oral_tradition(self, item: OralTradition) -> List[ValidationError]:
        """Validate an oral tradition (story, song, proverb, oral history)."""
        errors: List[ValidationError] = []
        if not item.id or not item.id.strip():
            errors.append(ValidationError("", "id", "Oral tradition ID is mandatory."))
        if not item.title_en or not item.title_en.strip():
            errors.append(ValidationError(item.id, "title_en", "English title is mandatory."))
        if not item.genre or not item.genre.strip():
            errors.append(ValidationError(item.id, "genre", "Genre is mandatory."))
        if item.source_id and not self.sources.contains(item.source_id):
            errors.append(ValidationError(item.id, "source_id", f"Unknown source '{item.source_id}'. Must be in sources registry."))
        if item.variety_id and not self.varieties.contains(item.variety_id):
            errors.append(ValidationError(item.id, "variety_id", f"Unknown variety '{item.variety_id}'."))
        return errors

    def validate_deity(self, deity: Deity) -> List[ValidationError]:
        """Validate a documented Gaddi deity record."""
        errors: List[ValidationError] = []
        if not deity.id or not deity.id.strip():
            errors.append(ValidationError("", "id", "Deity ID is mandatory."))
        if not deity.name_devanagari or not deity.name_devanagari.strip():
            errors.append(ValidationError(deity.id, "name_devanagari", "Deity Devanagari name is mandatory."))
        if deity.source_id and not self.sources.contains(deity.source_id):
            errors.append(ValidationError(deity.id, "source_id", f"Unknown source '{deity.source_id}'."))
        return errors

    def validate_festival(self, fest: Festival) -> List[ValidationError]:
        """Validate a documented Gaddi festival or ceremony."""
        errors: List[ValidationError] = []
        if not fest.id or not fest.id.strip():
            errors.append(ValidationError("", "id", "Festival ID is mandatory."))
        if not fest.name_devanagari or not fest.name_devanagari.strip():
            errors.append(ValidationError(fest.id, "name_devanagari", "Festival Devanagari name is mandatory."))
        if not fest.name_en or not fest.name_en.strip():
            errors.append(ValidationError(fest.id, "name_en", "Festival English name is mandatory."))
        if fest.source_id and not self.sources.contains(fest.source_id):
            errors.append(ValidationError(fest.id, "source_id", f"Unknown source '{fest.source_id}'."))
        return errors

    def validate_cultural_record(self, record: CulturalRecord) -> List[ValidationError]:
        """Validate a documented cultural, pastoral, or social practice record."""
        errors: List[ValidationError] = []
        if not record.id or not record.id.strip():
            errors.append(ValidationError("", "id", "Cultural record ID is mandatory."))
        if not record.title or not record.title.strip():
            errors.append(ValidationError(record.id, "title", "Title is mandatory."))
        if not record.topic or not record.topic.strip():
            errors.append(ValidationError(record.id, "topic", "Topic is mandatory."))
        if record.source_id and not self.sources.contains(record.source_id):
            errors.append(ValidationError(record.id, "source_id", f"Unknown source '{record.source_id}'."))
        return errors

    def validate_media_resource(self, media: MediaResource) -> List[ValidationError]:
        """Validate an archival audio, manuscript, or photographic media resource."""
        errors: List[ValidationError] = []
        if not media.id or not media.id.strip():
            errors.append(ValidationError("", "id", "Media resource ID is mandatory."))
        if not media.title or not media.title.strip():
            errors.append(ValidationError(media.id, "title", "Title is mandatory."))
        if not media.media_type or not media.media_type.strip():
            errors.append(ValidationError(media.id, "media_type", "Media type is mandatory."))
        if media.source_id and not self.sources.contains(media.source_id):
            errors.append(ValidationError(media.id, "source_id", f"Unknown source '{media.source_id}'."))
        return errors

    def validate_oral_heritage_collection(self, items: List[OralTradition]) -> ValidationReport:
        """Validate a collection of oral traditions."""
        report = ValidationReport(total_checked=len(items))
        seen_ids: Set[str] = set()
        for item in items:
            errors = self.validate_oral_tradition(item)
            report.errors.extend(errors)
            if item.id in seen_ids:
                report.errors.append(ValidationError(item.id, "id", f"Duplicate oral tradition ID '{item.id}'."))
            else:
                seen_ids.add(item.id)
        return report

    def validate_deities_collection(self, items: List[Deity]) -> ValidationReport:
        """Validate a collection of deity records."""
        report = ValidationReport(total_checked=len(items))
        seen_ids: Set[str] = set()
        for item in items:
            errors = self.validate_deity(item)
            report.errors.extend(errors)
            if item.id in seen_ids:
                report.errors.append(ValidationError(item.id, "id", f"Duplicate deity ID '{item.id}'."))
            else:
                seen_ids.add(item.id)
        return report

    def validate_festivals_collection(self, items: List[Festival]) -> ValidationReport:
        """Validate a collection of festival records."""
        report = ValidationReport(total_checked=len(items))
        seen_ids: Set[str] = set()
        for item in items:
            errors = self.validate_festival(item)
            report.errors.extend(errors)
            if item.id in seen_ids:
                report.errors.append(ValidationError(item.id, "id", f"Duplicate festival ID '{item.id}'."))
            else:
                seen_ids.add(item.id)
        return report

    def validate_cultural_records_collection(self, items: List[CulturalRecord]) -> ValidationReport:
        """Validate a collection of cultural practice records."""
        report = ValidationReport(total_checked=len(items))
        seen_ids: Set[str] = set()
        for item in items:
            errors = self.validate_cultural_record(item)
            report.errors.extend(errors)
            if item.id in seen_ids:
                report.errors.append(ValidationError(item.id, "id", f"Duplicate cultural record ID '{item.id}'."))
            else:
                seen_ids.add(item.id)
        return report

    def validate_media_resources_collection(self, items: List[MediaResource]) -> ValidationReport:
        """Validate a collection of media resources."""
        report = ValidationReport(total_checked=len(items))
        seen_ids: Set[str] = set()
        for item in items:
            errors = self.validate_media_resource(item)
            report.errors.extend(errors)
            if item.id in seen_ids:
                report.errors.append(ValidationError(item.id, "id", f"Duplicate media resource ID '{item.id}'."))
            else:
                seen_ids.add(item.id)
        return report
