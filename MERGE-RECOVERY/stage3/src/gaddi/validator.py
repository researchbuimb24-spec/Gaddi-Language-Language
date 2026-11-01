"""Validation engine for data integrity and linguistic provenance."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Set

from gaddi.models import LexicalEntry, ValidationError, ValidationReport, ValidationWarning
from gaddi.registry import SourceRegistry, VarietyRegistry, default_sources, default_varieties


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

        # 2. Variety validation
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

        # 3. Headword presence
        if not entry.lemma_devanagari or not entry.lemma_devanagari.strip():
            errors.append(
                ValidationError(
                    entry.id,
                    "lemma_devanagari",
                    "Headword in Devanagari script is mandatory.",
                )
            )

        # 4. Senses validation
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

        # 5. Attestation and Source Traceability
        if not entry.attestations:
            errors.append(
                ValidationError(
                    entry.id,
                    "attestations",
                    "Entry has zero source attestations. Every item must have traceable provenance.",
                )
            )
        else:
            variety = self.varieties.get(entry.variety_id)
            has_jk_source = False
            has_valid_source = False

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
                    has_valid_source = True
                    if source.is_jk_primary:
                        has_jk_source = True

            # Critical rule: Prevent claiming a word is J&K Gaddi if it only cites an HP Kangra source
            if variety and variety.is_jk_variety and has_valid_source and not has_jk_source:
                # Unless status explicitly says comparative_only or provisional with comparative notes
                if entry.status not in ("provisional", "comparative_only"):
                    errors.append(
                        ValidationError(
                            entry.id,
                            "variety_id",
                            f"Entry claims J&K variety '{entry.variety_id}' but only cites non-J&K comparative sources. "
                            "Local J&K attestation is required to assert J&K status.",
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

        # Check status
        if entry.status in ("provisional", "disputed"):
            warnings.append(
                ValidationWarning(
                    entry.id,
                    "status",
                    f"Entry is marked as '{entry.status}'. Requires further field verification.",
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

            # Global duplicate check: same lemma in Devanagari + same variety
            dup_key = f"{entry.lemma_devanagari.strip()}::{entry.variety_id}"
            if dup_key in seen_keys:
                report.errors.append(
                    ValidationError(
                        entry.id,
                        "lemma_devanagari",
                        f"Duplicate entry found for '{entry.lemma_devanagari}' in variety '{entry.variety_id}'.",
                    )
                )
            else:
                seen_keys.add(dup_key)

        return report

