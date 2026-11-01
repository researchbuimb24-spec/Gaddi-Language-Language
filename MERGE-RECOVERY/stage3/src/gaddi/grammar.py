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
                form_devanagari="αñ¿αÑç",
                form_ipa="ne",
                function="Marks the transitive subject in perfective aspect (split-ergativity)",
                source_citation="kumari_2026, p. 142",
                variety_id="hp_kangra_palampur",
                is_jk_attested=True,
                notes="Also widely used across Jammu Dogri and J&K Gaddi contact areas.",
            ),
            CaseMarker(
                case_name="Dative / Accusative",
                form_devanagari="αñ£αÑï",
                form_ipa="d╩Æo",
                function="Marks direct object and indirect object / recipient",
                source_citation="kumari_2026, p. 146; grierson_1916, p. 794",
                variety_id="hp_kangra_palampur",
                is_jk_attested=False,
                notes="Cognate with Western Pahari 'jo' / 'ko'. Needs specific verification in J&K tehsils.",
            ),
            CaseMarker(
                case_name="Ablative",
                form_devanagari="αññαÑç / αñÑαÑç",
                form_ipa="te / t╩░e",
                function="Marks source, origin, or separation ('from')",
                source_citation="kumari_2026, p. 150",
                variety_id="hp_kangra_palampur",
                is_jk_attested=False,
                notes="Compare with Dogri 'αñòαñ╢αñ╛' (k╔Ö╩âa╦É) and Punjabi 'αññαÑïαñé' (t├╡).",
            ),
            CaseMarker(
                case_name="Genitive (Possessive)",
                form_devanagari="αñ░αñ╛ / αñ░αÑÇ / αñ░αÑç",
                form_ipa="ra╦É / ri╦É / re╦É",
                function="Marks possession; inflects to agree in gender and number with possessed noun",
                source_citation="grierson_1916, p. 792; kumari_2026, p. 152",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Classic Western Pahari and Dogri genitive marker (-ra, -ri, -re), widely shared across J&K hills.",
            ),
            CaseMarker(
                case_name="Locative",
                form_devanagari="αñ«αñ¥ / αñ¬αñ░",
                form_ipa="m╔Öd╩Æ╩░ / p╔Ör",
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
                form_devanagari="αñåαñèαñé",
                form_ipa="a╦É┼⌐",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 112",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Shared across Chamba Gaddi, Kangra Gaddi, and Dogri (a┼⌐).",
            ),
            PronominalForm(
                person="1st",
                number="plural",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="αñàαñ╕αÑìαñ╕αÑç",
                form_ipa="╔Ös╦Ée",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 112",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Compare Dogri 'αñàαñ╕αÑìαñ╕' (╔Öss).",
            ),
            PronominalForm(
                person="2nd",
                number="singular",
                honorificity="familiar",
                proximity=None,
                case="direct",
                form_devanagari="αññαÑé",
                form_ipa="tu╦É",
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
                form_devanagari="αññαÑüαñ╕αÑìαñ╕αÑç",
                form_ipa="t╠¬╩ès╦Ée",
                source_citation="grierson_1916, p. 795; kumari_2026, p. 114",
                variety_id="hp_chamba_bharmaur",
                is_jk_attested=True,
                notes="Compare Dogri 'αññαÑüαñ╕αÑìαñ╕' (t╠¬╩èss).",
            ),
        ]
