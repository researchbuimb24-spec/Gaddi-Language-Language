"""Validation engine for linguistic integrity, provenance, and anti-conflation rules."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from gaddi.models import EvidenceStatus, LexicalEntry, ValidationError, ValidationReport, ValidationWarning
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
                            "Entry is marked as verified J&K lexical but lacks any J&K primary source attestation. "
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

            # Global duplicate check: same lemma in Devanagari + same variety + same POS
            dup_key = f"{entry.lemma_devanagari.strip()}::{entry.variety_id}::{entry.part_of_speech}"
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
