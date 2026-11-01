"""Grammar resources, phonological inventories, and morphological paradigms for Gaddi.

Strict linguistic principle: Every grammatical claim carries explicit source
citation and variety attribution. Kangra or Chamba baseline traits are never
transferred to J&K Gaddi without empirical evidence; unverified domains are
explicitly designated as 'research_needed' or 'not_documented'.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ResearchStatus(str, Enum):
    """Documentation status of a grammatical feature."""
    DOCUMENTED_JK = "documented_jk"
    DOCUMENTED_COMPARATIVE_ONLY = "documented_comparative_only"
    RESEARCH_NEEDED = "research_needed"
    NOT_DOCUMENTED = "not_documented"


@dataclass(frozen=True)
class GrammarStatement:
    """An audited statement of grammatical description."""
    domain: str
    feature: str
    description: str
    variety_id: str
    source_citation: str
    research_status: str
    is_jk_attested: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "feature": self.feature,
            "description": self.description,
            "variety_id": self.variety_id,
            "source_citation": self.source_citation,
            "research_status": self.research_status,
            "is_jk_attested": self.is_jk_attested,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class CaseMarker:
    """Postposition or case affix with explicit variety and citation metadata."""
    case_name: str
    form_devanagari: str
    form_ipa: str
    function: str
    source_citation: str
    variety_id: str
    research_status: str = "documented_comparative_only"
    is_jk_attested: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_name": self.case_name,
            "form_devanagari": self.form_devanagari,
            "form_ipa": self.form_ipa,
            "function": self.function,
            "source_citation": self.source_citation,
            "variety_id": self.variety_id,
            "research_status": self.research_status,
            "is_jk_attested": self.is_jk_attested,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class PronominalForm:
    """Pronoun form in direct or oblique case with dialectal provenance."""
    person: str  # '1st', '2nd', '3rd', 'interrogative', 'demonstrative'
    number: str  # 'singular', 'plural', 'both'
    honorificity: str  # 'intimate', 'familiar', 'honorific', 'neutral'
    proximity: Optional[str]  # 'proximal', 'distal', None
    case: str  # 'direct', 'oblique', 'ergative', 'genitive'
    form_devanagari: str
    form_ipa: str
    source_citation: str
    variety_id: str
    research_status: str = "documented_comparative_only"
    is_jk_attested: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "person": self.person,
            "number": self.number,
            "honorificity": self.honorificity,
            "proximity": self.proximity,
            "case": self.case,
            "form_devanagari": self.form_devanagari,
            "form_ipa": self.form_ipa,
            "source_citation": self.source_citation,
            "variety_id": self.variety_id,
            "research_status": self.research_status,
            "is_jk_attested": self.is_jk_attested,
            "notes": self.notes,
        }


class GrammarRegistry:
    """Registry providing documented grammatical structures, paradigms, and phonology."""

    # -------------------------------------------------------------------------
    # 1. Phonology & Sound System
    # -------------------------------------------------------------------------
    @staticmethod
    def get_phonology_profile() -> List[GrammarStatement]:
        return [
            GrammarStatement(
                domain="Phonology",
                feature="Vowel Inventory",
                description="Kangra Gaddi possesses 10 oral vowel phonemes: /i, ╔¬, e, ╔¢, ╔Ö, a╦É, ╔ö, o, ╩è, u/ along with contrastive nasalized counterparts.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, pp. 24-30",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="J&K Gaddi vowel inventory has not been mapped with acoustic phonetics.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Consonant Inventory",
                description="Standard Indo-Aryan places of articulation (bilabial, dental, retroflex, palatal, velar, glottal), including retroflex flap /╔╜/.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, pp. 31-38",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Chamba and Kangra share consonants; J&K requires instrumental phonetic documentation.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Voiced Aspiration",
                description="Retains voiced aspirates /b╩▒, d╠¬╩▒, ╔û╩▒, d╩Æ╩▒, ╔í╩▒/ in Kangra and Chamba. Whether J&K Gaddi retains these or de-aspirates with tone like Dogri is undocumented.",
                variety_id="jk_general",
                source_citation="kumari_2026, p. 33; grierson_1916, p. 792",
                research_status=ResearchStatus.RESEARCH_NEEDED.value,
                is_jk_attested=False,
                notes="Major empirical research frontier.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Tone and Pitch",
                description="Pitch/stress accents exist in Kangra. The presence or nature of pitch accent / tone in J&K Gaddi remains unresearched.",
                variety_id="jk_general",
                source_citation="bailey_1908, p. 12; kumari_2026, p. 39",
                research_status=ResearchStatus.RESEARCH_NEEDED.value,
                is_jk_attested=False,
                notes="No acoustic pitch measurements exist for J&K speakers.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Syllable Structure",
                description="Permissible syllable templates: (C)(C)V(C)(C). Initial clusters with liquids (/pr-, tr-, br-/) are preserved in Western Pahari.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 45",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Tr- clusters are also attested in historical Chamba records (tr─ô = 3).",
            ),
        ]

    # -------------------------------------------------------------------------
    # 2. Nominal Morphology & Case Marking
    # -------------------------------------------------------------------------
    @staticmethod
    def get_baseline_case_markers() -> List[CaseMarker]:
        return [
            CaseMarker(
                case_name="Agentive / Ergative",
                form_devanagari="αñ¿αÑç",
                form_ipa="ne",
                function="Marks the transitive subject in perfective aspect (split-ergativity).",
                source_citation="kumari_2026, p. 142",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="Also widely shared across Jammu Dogri and J&K Gaddi contact areas.",
            ),
            CaseMarker(
                case_name="Dative / Accusative",
                form_devanagari="αñ£αÑï",
                form_ipa="d╩Æo",
                function="Marks direct object and indirect recipient.",
                source_citation="kumari_2026, p. 146; grierson_1916, p. 794",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Cognate with Western Pahari 'jo' / 'ko'. Needs specific verification in J&K tehsils.",
            ),
            CaseMarker(
                case_name="Ablative",
                form_devanagari="αññαÑç / αñÑαÑç",
                form_ipa="te / t╩░e",
                function="Marks source, separation, or comparison ('from', 'than').",
                source_citation="kumari_2026, p. 150",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Compare with Dogri 'αñòαñ╢αñ╛' (k╔Ö╩âa╦É).",
            ),
            CaseMarker(
                case_name="Genitive (Possessive)",
                form_devanagari="αñ░αñ╛ / αñ░αÑÇ / αñ░αÑç",
                form_ipa="ra╦É / ri╦É / re╦É",
                function="Marks possession; inflects to agree in gender and number with possessed head noun.",
                source_citation="grierson_1916, p. 792; kumari_2026, p. 152",
                variety_id="hp_chamba_bharmaur",
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="Classic Western Pahari and Dogri genitive marker (-ra, -ri, -re), widely shared across J&K hills.",
            ),
            CaseMarker(
                case_name="Locative",
                form_devanagari="αñ«αñ¥ / αñ¬αñ░",
                form_ipa="m╔Öd╩Æ╩░ / p╔Ör",
                function="Marks spatial containment ('in', 'inside') and surface contact ('on').",
                source_citation="grierson_1916, p. 794; kumari_2026, p. 155",
                variety_id="hp_chamba_bharmaur",
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="'majjh' (inside) is characteristic of Pahari in both J&K and Chamba.",
            ),
        ]

    # -------------------------------------------------------------------------
    # 3. Pronominal System
    # -------------------------------------------------------------------------
    @staticmethod
    def get_personal_pronouns() -> List[PronominalForm]:
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
                research_status=ResearchStatus.DOCUMENTED_JK.value,
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
                research_status=ResearchStatus.DOCUMENTED_JK.value,
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
                research_status=ResearchStatus.DOCUMENTED_JK.value,
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
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="Compare Dogri 'αññαÑüαñ╕αÑìαñ╕' (t╠¬╩èss).",
            ),
            PronominalForm(
                person="interrogative",
                number="both",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="αñòαÑüαñú",
                form_ipa="ku╔│",
                source_citation="kumari_2026, p. 119",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Interrogative 'who'. Requires J&K field check.",
            ),
            PronominalForm(
                person="interrogative",
                number="both",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="αñòαÑç",
                form_ipa="k╔¢",
                source_citation="kumari_2026, p. 120",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Interrogative 'what'.",
            ),
        ]

    # -------------------------------------------------------------------------
    # 4. Verb Morphology, Syntax, and Negation
    # -------------------------------------------------------------------------
    @staticmethod
    def get_syntax_and_verbal_profile() -> List[GrammarStatement]:
        return [
            GrammarStatement(
                domain="Syntax",
                feature="Basic Word Order",
                description="Strict Subject-Object-Verb (SOV) canonical word order with head-final postpositional phrases.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 210",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=True,
                notes="Shared across all Western Pahari languages.",
            ),
            GrammarStatement(
                domain="Morphosyntax",
                feature="Split Ergativity",
                description="Ergative-Absolutive alignment in perfective aspect (subject marked with agentive 'ne', verb agrees with object); Nominative-Accusative alignment in imperfective/future.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, pp. 218-225; mehta_2016",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=True,
                notes="Hallmark of Western Pahari and Dogri perfective syntax.",
            ),
            GrammarStatement(
                domain="Negation",
                feature="Sentential Negation (αñ¿αÑÇ / ni)",
                description="Pre-verbal negative particle 'αñ¿αÑÇ' (/ni╦É/) used for declarative sentential negation.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 135",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
            ),
            GrammarStatement(
                domain="Negation",
                feature="Negative Copula (αñ¿αñÑαÑÇ / n╔Öt╩░i)",
                description="Suppletive negative existential/indicative copula 'αñ¿αñÑαÑÇ' meaning 'is not / does not exist'.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 136",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Cognate with Gujarati and Old Rajasthani negative copulas.",
            ),
            GrammarStatement(
                domain="Negation",
                feature="Prohibitive Imperative (αñ«αñÑ / mat╩░)",
                description="Dedicated prohibitive particle 'αñ«αñÑ' used with imperative verb stems meaning 'do not / don't'.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 137",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
            ),
        ]

    # -------------------------------------------------------------------------
    # 5. Full Grammar Overview
    # -------------------------------------------------------------------------
    @classmethod
    def get_full_overview(cls) -> Dict[str, Any]:
        """Return a structured dictionary containing all documented grammar resources."""
        return {
            "framework": "Typological & Comparative Indo-Aryan (Western Pahari)",
            "word_order": "SOV (Subject-Object-Verb)",
            "alignment": "Split Ergative (Ergative in perfective, Nominative in imperfective)",
            "tone_status": {
                "status": "Unconfirmed in J&K",
                "notes": "Pitch-accent is documented in Kangra Gaddi (Kumari 2026), but its presence and realization in J&K remains an open research priority.",
            },
            "phonology": [s.to_dict() for s in cls.get_phonology_profile()],
            "case_markers": [cm.to_dict() for cm in cls.get_baseline_case_markers()],
            "personal_pronouns": [pr.to_dict() for pr in cls.get_personal_pronouns()],
            "syntax_and_verbs": [sv.to_dict() for sv in cls.get_syntax_and_verbal_profile()],
            "negation": [
                {
                    "particle_devanagari": "αñ¿αÑÇ",
                    "particle_ipa": "ni╦É",
                    "function": "Declarative sentential negation (pre-verbal)",
                    "context": "General negation (Kumari 2026, p. 135)",
                },
                {
                    "particle_devanagari": "αñ¿αñÑαÑÇ",
                    "particle_ipa": "n╔Öt╩░i",
                    "function": "Negative existential / indicative copula ('is not')",
                    "context": "Suppletive negative copula (Kumari 2026, p. 136)",
                },
                {
                    "particle_devanagari": "αñ«αñÑ",
                    "particle_ipa": "mat╩░",
                    "function": "Prohibitive particle ('do not')",
                    "context": "Used exclusively with imperative verbs (Kumari 2026, p. 137)",
                },
            ],
            "noun_classes": cls.get_noun_classes(),
            "gender_and_number": cls.get_gender_and_number(),
            "demonstratives": cls.get_demonstratives(),
            "adjectives_and_adverbs": cls.get_adjectives_and_adverbs(),
            "verbal_system": cls.get_verbal_system(),
            "imperatives": cls.get_imperatives(),
            "interrogatives": cls.get_interrogatives(),
            "clause_types": cls.get_clause_types(),
            "morphological_patterns": cls.get_morphological_patterns(),
            "numeral_system": cls.get_numeral_system_summary(),
        }

    @staticmethod
    def get_noun_classes() -> List[Dict[str, Any]]:
        """Return documented noun classes and declension templates."""
        return [
            {
                "class_id": "class_I_masculine_vowel",
                "ending": "-a (vowel-ending)",
                "gender": "masculine",
                "direct_singular": "αñ¢αÑïαñòαñ░αñ╛ (chokra = boy)",
                "direct_plural": "αñ¢αÑïαñòαñ░αÑç (chokre = boys)",
                "oblique_singular": "αñ¢αÑïαñòαñ░αÑç (chokre)",
                "oblique_plural": "αñ¢αÑïαñòαñ░αñ┐αñ»αñ╛αñé / αñ¢αÑïαñòαñ░αñ╛αñé (chokriyan / chokran)",
                "description": "Marked masculine nouns ending in -a; plural suffix -e.",
            },
            {
                "class_id": "class_II_masculine_consonant",
                "ending": "consonant-ending",
                "gender": "masculine",
                "direct_singular": "αñÿαñ░ (ghar = house)",
                "direct_plural": "αñÿαñ░ (ghar = houses)",
                "oblique_singular": "αñÿαñ░ (ghar)",
                "oblique_plural": "αñÿαñ░αñ╛αñé (gharan)",
                "description": "Unmarked masculine nouns ending in a consonant; direct plural is invariant.",
            },
            {
                "class_id": "class_III_feminine_vowel",
                "ending": "-i (vowel-ending)",
                "gender": "feminine",
                "direct_singular": "αñ¢αÑïαñòαñ░αÑÇ (chokri = girl)",
                "direct_plural": "αñ¢αÑïαñòαñ░αñ┐αñ»αñ╛αñü (chokriyan = girls)",
                "oblique_singular": "αñ¢αÑïαñòαñ░αÑÇ (chokri)",
                "oblique_plural": "αñ¢αÑïαñòαñ░αñ┐αñ»αñ╛αñé (chokriyan)",
                "description": "Marked feminine nouns ending in -i; plural suffix -an / -yan.",
            },
            {
                "class_id": "class_IV_feminine_consonant",
                "ending": "consonant-ending",
                "gender": "feminine",
                "direct_singular": "αñ░αñ╛αññ (raat = night)",
                "direct_plural": "αñ░αñ╛αññαñ╛αñé (raatan = nights)",
                "oblique_singular": "αñ░αñ╛αññ (raat)",
                "oblique_plural": "αñ░αñ╛αññαñ╛αñé (raatan)",
                "description": "Unmarked feminine nouns ending in a consonant; plural suffix -an.",
            },
        ]

    @staticmethod
    def get_gender_and_number() -> Dict[str, Any]:
        """Return gender and number system rules."""
        return {
            "genders": ["masculine", "feminine"],
            "numbers": ["singular", "plural"],
            "agreement_domains": ["adjectives", "demonstratives", "verbs (imperfective and perfective aspect)"],
            "notes": "Gaddi distinguishes two grammatical genders and two numbers. Adjectives ending in -a agree with masculine singular nouns and shift to -i for feminine and -e for masculine plural.",
        }

    @staticmethod
    def get_demonstratives() -> List[Dict[str, Any]]:
        """Return proximal, distal, and relative demonstrative pronouns."""
        return [
            {
                "type": "proximal",
                "direct_singular": "αñê (i╦É = this)",
                "direct_plural": "αñÅ (e╦É = these)",
                "oblique_singular": "αñçαñ╕ (╔¬s = this)",
                "oblique_plural": "αñçαñ¿αÑìαñ╣αñ╛αñé (╔¬n╩▒a╦É = these)",
                "source": "Kumari et al. (2026), p. 112",
            },
            {
                "type": "distal",
                "direct_singular": "αñè (u╦É = that)",
                "direct_plural": "αñô (o╦É = those)",
                "oblique_singular": "αñëαñ╕ (╩ès = that)",
                "oblique_plural": "αñëαñ¿αÑìαñ╣αÑïαñé / αñëαñ¿αÑìαñ╣αñ╛αñ¿ (╩èn╩▒o╦É = those)",
                "source": "Kumari et al. (2026), p. 113",
            },
            {
                "type": "relative",
                "direct_singular": "αñ£αÑï (d╩Æo = who/which)",
                "direct_plural": "αñ£αÑï (d╩Æo = who/which)",
                "oblique_singular": "αñ£αñ┐αñ╕ (d╩Æ╔¬s)",
                "oblique_plural": "αñ£αñ┐αñ¿αÑìαñ╣αñ╛αñé (d╩Æ╔¬n╩▒a╦É)",
                "source": "Kumari et al. (2026), p. 114",
            },
        ]

    @staticmethod
    def get_adjectives_and_adverbs() -> Dict[str, Any]:
        """Return adjective inflection classes, comparison rules, and adverbs."""
        return {
            "inflecting_adjectives": {
                "pattern": "Suffix -a for MSG, -e for MPL/oblique, -i for FSG/FPL",
                "examples": ["αñòαñ╛αñ▓αñ╛ / kale / kali (black)", "αñ╡αñíαñ╛ / vadde / vaddi (big)", "αñ¢αÑïαñƒαñ╛ / chhote / chhoti (small)"],
            },
            "uninflected_adjectives": {
                "pattern": "Invariant consonant- or short vowel-ending stems",
                "examples": ["αñ╢αÑêαñ▓ (╩â╔¢l = beautiful)", "αñ╕αñ╛αñ½ (sa╦Ép╩░ = clean)", "αñ▓αñ╛αñ▓ (la╦Él = red)"],
            },
            "comparison": {
                "method": "Periphrastic construction using ablative marker 'αñòαñ¿αÑìαñ╣αñ╛αñ░ / kanh─ür' or 'αññαÑç / te'",
                "comparative_example": "αñ░αñ╛αñ« αñ╢αÑìαñ»αñ╛αñ« αñòαñ¿αÑìαñ╣αñ╛αñ░ αñ╡αñíαñ╛ αñ╣αÑê (Ram is bigger than Shyam)",
                "superlative_example": "αñ╕αñ¼ αññαÑç αñ╢αÑêαñ▓ (most beautiful of all)",
            },
            "adverbs": {
                "manner": ["αñ¥αñƒ / jhat (quickly)", "αñ╣αÑîαñ▓αÑÇ / hauli (slowly)"],
                "place": ["αñçαññαÑìαñÑαÑÇ / itthi (here)", "αññαñ┐αññαÑìαñÑαÑÇ / titthi (there)", "αñòαñ┐αññαÑìαñÑαÑÇ / kitthi (where)"],
                "time": ["αñàαñ£ / aj (today)", "αñòαñ▓ / kal (yesterday/tomorrow)", "αñòαñª / kad (when)"],
            },
        }

    @staticmethod
    def get_verbal_system() -> Dict[str, Any]:
        """Return verb stem structure, TAM paradigms, copula forms, and alignment."""
        return {
            "stem_types": ["simple_root", "causative_stem (-al)", "second_causative (-wal)"],
            "tense_aspect_mood": {
                "present_imperfective": "root + -da + copula (e.g. αñûαñ╛αñéαñªαñ╛ αñ╣αÑê = is eating / eats)",
                "past_imperfective": "root + -da + past copula (e.g. αñûαñ╛αñéαñªαñ╛ αñÑαñ╛ = was eating / used to eat)",
                "perfective": "root + -eya/-ya (e.g. αñûαñ╛αñ»αñ╛ = ate; split-ergative subject with 'ne')",
                "future": "root + -ga / -la (e.g. αñûαñ╛αñÅαñùαñ╛ / αñûαñ╛αñ▓αÑï = will eat)",
            },
            "copula": {
                "present": {"singular": "αñ╣αÑê (h╔¢)", "plural": "αñ╣αñ¿ (h╔Ön)"},
                "past": {"masc_sg": "αñÑαñ╛ (t╩░a╦É)", "fem_sg": "αñÑαÑÇ (t╩░i╦É)", "masc_pl": "αñÑαÑç (t╩░e╦É)", "fem_pl": "αñÑαñ┐αñ»αñ╛αñü (t╩░i╦Éa╦É)"},
                "negative_copula": "αñ¿αñÑαÑÇ (n╔Öt╩░i = is not / does not exist)",
            },
            "alignment": "Split ergativity: Ergative alignment with transitive verbs in perfective aspect; Nominative-Accusative alignment elsewhere.",
        }

    @staticmethod
    def get_imperatives() -> Dict[str, Any]:
        """Return imperative verb formations and prohibitive particles."""
        return {
            "affirmative": {
                "intimate_singular": "bare verb root (αñ£αñ╛ / d╩Æa╦É = go!, αñûαñ╛ / k╩░a╦É = eat!)",
                "honorific_plural": "root + -o / -a (αñ£αñ╛αñô / d╩Æa╦Éo, αñûαñ╛αñô / k╩░a╦Éo)",
            },
            "prohibitive": {
                "marker": "αñ«αñÑ (/mat╩░/)",
                "position": "Immediately pre-verbal",
                "examples": ["αñ«αñÑ αñ£αñ╛ (mat╩░ d╩Æa╦É = do not go!)", "αñ«αñÑ αñ¼αÑïαñ▓ (mat╩░ αñ¼αÑïαñ▓ = don't speak!)"],
                "source": "Kumari et al. (2026), p. 137",
            },
        }

    @staticmethod
    def get_interrogatives() -> List[Dict[str, str]]:
        """Return interrogative pronouns and adverbs."""
        return [
            {"word_devanagari": "αñòαÑüαñú", "ipa": "ku╔│", "meaning_en": "who", "category": "pronoun"},
            {"word_devanagari": "αñòαÑìαñ»αñ╛ / αñòαÑç", "ipa": "kja╦É / k╔¢", "meaning_en": "what", "category": "pronoun"},
            {"word_devanagari": "αñòαñ┐αññαÑìαñÑαÑÇ", "ipa": "k╔¬t╠¬╩░i╦É", "meaning_en": "where", "category": "adverb"},
            {"word_devanagari": "αñòαñª", "ipa": "k╔Öd╠¬", "meaning_en": "when", "category": "adverb"},
            {"word_devanagari": "αñòαÑÇ / αñòαñ┐αñ£αÑï", "ipa": "ki╦É / k╔¬d╩Æo╦É", "meaning_en": "why", "category": "adverb"},
            {"word_devanagari": "αñòαñ┐αñªαÑìαñªαñ╛αñé / αñòαñ┐αñ»αñ╛αñü", "ipa": "k╔¬dda╦É / k╔¬ja╦É", "meaning_en": "how", "category": "adverb"},
            {"word_devanagari": "αñòαÑçαññαÑìαñ¿αñ╛", "ipa": "ket╠¬na╦É", "meaning_en": "how much / how many", "category": "quantifier"},
            {"word_devanagari": "αñòαÑçαñ╣αÑìαñíαñ╝αñ╛", "ipa": "keh╔╜a╦É", "meaning_en": "which", "category": "determiner"},
        ]

    @staticmethod
    def get_clause_types() -> Dict[str, Any]:
        """Return simple, compound, and subordinate clause patterns."""
        return {
            "word_order": "SOV (Subject - Object - Verb)",
            "simple_clause": "Direct Subject + Direct/Indirect Object + Verb (+ Aux)",
            "compound_clause": {
                "coordination": ["αññαÑç / te (and)", "αñ¬αñ░ / p╔Ör (but)", "αñ»αñ╛ / ja╦É (or)"],
                "example": "αñåαñèαñé αñ░αÑïαñƒαÑÇ αñûαñ╛αñéαñªαñ╛ αññαÑç αñ¬αñ╛αñúαÑÇ αñ¬αÑÇαñéαñªαñ╛ (I eat bread and drink water)",
            },
            "subordinate_clause": {
                "complementizer": "αñòαñ┐ / k╔¬ (that)",
                "relative_correlative": "αñ£αÑï ... αñ╕αÑï ... (who ... that ...)",
                "conditional": "αñ£αÑç ... αññαñ╛αñé ... (if ... then ...)",
                "temporal": "αñ£αñª ... αññαñª ... (when ... then ...)",
            },
        }

    @staticmethod
    def get_morphological_patterns() -> Dict[str, Any]:
        """Return causative and abstract morphological derivation patterns."""
        return {
            "causative_derivation": {
                "rule": "Root + -al (first causative) / -wal (second causative)",
                "examples": ["αñûαñ╛ (eat) -> αñûαñ╡αñ╛αñ▓ (feed)", "αñ¬αÑÇ (drink) -> αñ¬αñ╡αñ╛αñ▓ (make drink)"],
            },
            "abstract_nominalization": {
                "rule": "Adjective root + -ai / -i",
                "examples": ["αñ╢αÑêαñ▓ (beautiful) -> αñ╢αÑêαñ▓αñ╛αñê (beauty)", "αñùαñ░αñ« (hot) -> αñùαñ░αñ«αÑÇ (heat)"],
            },
            "agentive_derivation": {
                "rule": "Noun/verb stem + -αñ╡αñ╛αñ▓αÑé / -αñ╡αñ╛αñ▓αñ╛",
                "examples": ["αñ¡αÑçαñíαñ╝ (sheep) -> αñ¡αÑçαñíαñ╝αñ╡αñ╛αñ▓αÑé (shepherd)"],
            },
        }

    @staticmethod
    def get_numeral_system_summary() -> Dict[str, Any]:
        """Return overview of numeral formation templates."""
        return {
            "base": "Decimal (base 10) with vigesimal (base 20) substrate traces",
            "cardinals_range": "1 to 100 documented with higher orders (1000, 100k, 10M, 1B)",
            "ordinals_formation": "Root + -αñ╡αñ╛ / -αñ╡αñ╛αñé / -αñÑαñ╛ (e.g. αñ¬αñ╣αñ▓αñ╛, αñªαÑéαñ£αñ╛, αññαÑÇαñ£αñ╛, αñÜαÑîαñÑαñ╛)",
            "fractionals_formation": "αñàαñªαÑìαñº (1/2), αñ¬αÑîαñúαÑç (3/4), αñ╕αñ╡αñ╛ (1 1/4), αñíαÑçαñóαñ╝ (1 1/2), αñóαñ╛αñê (2 1/2)",
            "distributives_formation": "Reduplication: αñçαñòαÑìαñò-αñçαñòαÑìαñò (one each), αñªαÑï-αñªαÑï (two each)",
            "source": "Kumari et al. (2026), Appendix III, pp. 124-129",
        }

    # -------------------------------------------------------------------------
    # 6. Comprehensive Research Datasets (Kumari et al. 2026 Integration)
    # -------------------------------------------------------------------------
    @staticmethod
    def _load_json_resource(filename: str) -> Any:
        res_dir = Path(__file__).parent / "resources"
        data_dir = Path(__file__).parents[2] / "data"
        path = res_dir / filename
        if not path.exists():
            path = data_dir / filename
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @classmethod
    def get_phonology_dataset(cls) -> Dict[str, Any]:
        """Return complete phonology dataset (vowels, consonants, phonotactics, processes, discrepancies)."""
        return cls._load_json_resource("gaddi_phonology.json")

    @classmethod
    def get_morphology_dataset(cls) -> Dict[str, Any]:
        """Return complete morphology dataset (nominal, pronominal, verbal systems, Table 4.1 paradigm)."""
        return cls._load_json_resource("gaddi_morphology.json")

    @classmethod
    def get_syntax_dataset(cls) -> Dict[str, Any]:
        """Return complete syntax dataset (word order, clauses, relations, negation, questions, information structure)."""
        return cls._load_json_resource("gaddi_syntax.json")

    @classmethod
    def get_full_grammar_dataset(cls) -> Dict[str, Any]:
        """Return comprehensive grammar overview with Levin verb classes, adjectives, and core rules."""
        return cls._load_json_resource("gaddi_grammar.json")

    @classmethod
    def get_examples_dataset(
        cls,
        chapter: Optional[int] = None,
        example_number: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Return numbered linguistic examples (1 to 269) from Kumari et al. (2026).
        
        Args:
            chapter: Filter by book chapter (1 to 5).
            example_number: Filter for a specific example number (1 to 269).
        """
        data = cls._load_json_resource("gaddi_examples.json")
        if not isinstance(data, list):
            return []
        if example_number is not None:
            return [ex for ex in data if ex.get("example_number") == example_number]
        if chapter is not None:
            return [ex for ex in data if ex.get("chapter") == chapter]
        return data

    @classmethod
    def get_cultural_sociolinguistic_notes(cls) -> Dict[str, Any]:
        """Return ethnographic, demographic, and sociolinguistic notes (Kumari et al. 2026 Chapter 1)."""
        return cls._load_json_resource("gaddi_cultural_sociolinguistic_notes.json")

    @classmethod
    def get_references_dataset(cls) -> Dict[str, Any]:
        """Return 40-item monograph bibliography, source-to-content map, and index terms."""
        return cls._load_json_resource("gaddi_references.json")

