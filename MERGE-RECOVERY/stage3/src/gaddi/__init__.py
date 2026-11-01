"""Gaddi Language Library.

A computational linguistics and language-documentation library for the Gaddi
(Bharmauri) language as spoken in Jammu & Kashmir, India.
"""

from __future__ import annotations

from gaddi.dictionary import GaddiDictionary
from gaddi.grammar import CaseMarker, GrammarRegistry, PronominalForm
from gaddi.models import (
    Attestation,
    ExampleSentence,
    GrammaticalGender,
    LexicalEntry,
    PartOfSpeech,
    Sense,
    Source,
    ValidationError,
    ValidationReport,
    ValidationWarning,
    Variety,
    VerificationStatus,
)
from gaddi.registry import (
    SourceRegistry,
    VarietyRegistry,
    default_sources,
    default_varieties,
)
from gaddi.validator import GaddiValidator

__version__ = "0.1.0"
__author__ = "Gaddi Language Project Contributors"
__license__ = "MIT (Software); See DATA-LICENSE.md for Data Terms"

__all__ = [
    "__version__",
    "GaddiDictionary",
    "GaddiValidator",
    "SourceRegistry",
    "VarietyRegistry",
    "default_sources",
    "default_varieties",
    "GrammarRegistry",
    "LexicalEntry",
    "Sense",
    "Source",
    "Variety",
    "Attestation",
    "ExampleSentence",
    "ValidationError",
    "ValidationWarning",
    "ValidationReport",
    "VerificationStatus",
    "PartOfSpeech",
    "GrammaticalGender",
    "CaseMarker",
    "PronominalForm",
]

