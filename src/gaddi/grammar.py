"""Grammar resources and morphological paradigm specifications for Gaddi."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class CaseMarker:
    """Postposition or case affix in Gaddi."""
    case_name: str
    form_devanagari: str
    form_ipa: str
    function: str
    source_citation: str
    variety_id: str
    is_jk_attested: bool = False
    notes: str = ""
    notes: str = ""


@dataclass(frozen=True)
class PronominalForm:
    """Pronoun form in direct or oblique case."""
    person: str  # '1st', '2nd', '3rd'
    number: str  # 'singular', 'plural'
    honorificity: str  # 'intimate', 'familiar', 'honorific', 'neutral'
    proximity: Optional[str]  # 'proximal', 'distal', None
    case: str  # 'direct', 'oblique', 'ergative', 'genitive'
    form_devanagari: str
    form_ipa: str
    source_citation: str
    variety_id: str
    is_jk_attested: bool = False
    notes: str = ""


class GrammarRegistry:
    """Documented grammatical paradigms with explicit geographic and source attribution."""

    @staticmethod
    def get_baseline_case_markers() -> List[CaseMarker]:
        """Return documented case markers and postpositions with source provenance."""
        return [
            CaseMarker(
                case_name="Agentive / Ergative",
                form_devanagari="ने",
                form_ipa="ne",
                function="Marks the transitive subject in perfective aspect (split-ergativity)",
                source_citation="kumari_2026, p. 142",
                variety_id="hp_kangra_palampur",
                is_jk_attested=True,
                notes="Also widely used across Jammu Dogri and J&K Gaddi contact areas.",
            ),
            CaseMarker(
                case_name="Dative / Accusative",
                form_devanagari="जो",
                form_ipa="dʒo",
                function="Marks direct object and indirect object / recipient",
                source_citation="kumari_2026, p. 146; grierson_1916, p. 794",
                variety_id="hp_kangra_palampur",
                is_jk_attested=False,
                notes="Cognate with Western Pahari 'jo' / 'ko'. Needs specific verification in J&K tehsils.",
            ),
            CaseMarker(
                case_name="Ablative",
                form_devanagari="ते / थे",
                form_ipa="te / tʰe",
                function="Marks source, origin, or separation ('from')",
                source_citation="kumari_2026, p. 150",
                variety_id="hp_kangra_palampur",
                is_jk_attested=False,
                notes="Compare with Dogri 'कशा' (kəʃaː) and Punjabi 'तों' (tõ).",
            ),
            CaseMarker(
                case_name="Genitive (Possessive)",
                form_devanagari="रा / री / रे",
                form_ipa="raː / riː / reː",
                function="Marks possession; inflects to agree in gender and number with possessed noun",
                source_citation="grierson_1916, p. 792; kumari_2026, p. 152",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Classic Western Pahari and Dogri genitive marker (-ra, -ri, -re), widely shared across J&K hills.",
            ),
            CaseMarker(
                case_name="Locative",
                form_devanagari="मझ / पर",
                form_ipa="mədʒʰ / pər",
                function="Marks spatial containment ('in', 'inside') and contact ('on')",
                source_citation="grierson_1916, p. 794; kumari_2026, p. 155",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="'majjh' (inside) is characteristic of Pahari and Gaddi in both J&K and Chamba.",
            ),
        ]

    @staticmethod
    def get_personal_pronouns() -> List[PronominalForm]:
        """Return baseline personal pronoun paradigms with variety tracking."""
        return [
            PronominalForm(
                person="1st",
                number="singular",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="आऊं",
                form_ipa="aːũ",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 112",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Shared across Chamba Gaddi, Kangra Gaddi, and Dogri (aũ).",
            ),
            PronominalForm(
                person="1st",
                number="plural",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="अस्से",
                form_ipa="əsːe",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 112",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Compare Dogri 'अस्स' (əss).",
            ),
            PronominalForm(
                person="2nd",
                number="singular",
                honorificity="familiar",
                proximity=None,
                case="direct",
                form_devanagari="तू",
                form_ipa="tuː",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 114",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
            ),
            PronominalForm(
                person="2nd",
                number="plural",
                honorificity="familiar",
                proximity=None,
                case="direct",
                form_devanagari="तुस्से",
                form_ipa="t̪ʊsːe",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 114",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Compare Dogri 'तुस्स' (t̪ʊss).",
            ),
        ]
