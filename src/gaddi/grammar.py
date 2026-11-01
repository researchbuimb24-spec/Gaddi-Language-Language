<<<<<<< HEAD
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
=======
"""Grammar resources and morphological paradigm specifications for Gaddi."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
>>>>>>> origin/main


@dataclass(frozen=True)
class CaseMarker:
<<<<<<< HEAD
    """Postposition or case affix with explicit variety and citation metadata."""
=======
    """Postposition or case affix in Gaddi."""
>>>>>>> origin/main
    case_name: str
    form_devanagari: str
    form_ipa: str
    function: str
    source_citation: str
    variety_id: str
<<<<<<< HEAD
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
=======
    is_jk_attested: bool = False
    notes: str = ""
    notes: str = ""
>>>>>>> origin/main


@dataclass(frozen=True)
class PronominalForm:
<<<<<<< HEAD
    """Pronoun form in direct or oblique case with dialectal provenance."""
    person: str  # '1st', '2nd', '3rd', 'interrogative', 'demonstrative'
    number: str  # 'singular', 'plural', 'both'
=======
    """Pronoun form in direct or oblique case."""
    person: str  # '1st', '2nd', '3rd'
    number: str  # 'singular', 'plural'
>>>>>>> origin/main
    honorificity: str  # 'intimate', 'familiar', 'honorific', 'neutral'
    proximity: Optional[str]  # 'proximal', 'distal', None
    case: str  # 'direct', 'oblique', 'ergative', 'genitive'
    form_devanagari: str
    form_ipa: str
    source_citation: str
    variety_id: str
<<<<<<< HEAD
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
                description="Kangra Gaddi possesses 10 oral vowel phonemes: /i, ɪ, e, ɛ, ə, aː, ɔ, o, ʊ, u/ along with contrastive nasalized counterparts.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, pp. 24-30",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="J&K Gaddi vowel inventory has not been mapped with acoustic phonetics.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Consonant Inventory",
                description="Standard Indo-Aryan places of articulation (bilabial, dental, retroflex, palatal, velar, glottal), including retroflex flap /ɽ/.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, pp. 31-38",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Chamba and Kangra share consonants; J&K requires instrumental phonetic documentation.",
            ),
            GrammarStatement(
                domain="Phonology",
                feature="Voiced Aspiration",
                description="Retains voiced aspirates /bʱ, d̪ʱ, ɖʱ, dʒʱ, ɡʱ/ in Kangra and Chamba. Whether J&K Gaddi retains these or de-aspirates with tone like Dogri is undocumented.",
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
                notes="Tr- clusters are also attested in historical Chamba records (trē = 3).",
            ),
        ]

    # -------------------------------------------------------------------------
    # 2. Nominal Morphology & Case Marking
    # -------------------------------------------------------------------------
    @staticmethod
    def get_baseline_case_markers() -> List[CaseMarker]:
=======
    is_jk_attested: bool = False
    notes: str = ""


class GrammarRegistry:
    """Documented grammatical paradigms with explicit geographic and source attribution."""

    @staticmethod
    def get_baseline_case_markers() -> List[CaseMarker]:
        """Return documented case markers and postpositions with source provenance."""
>>>>>>> origin/main
        return [
            CaseMarker(
                case_name="Agentive / Ergative",
                form_devanagari="ने",
                form_ipa="ne",
<<<<<<< HEAD
                function="Marks the transitive subject in perfective aspect (split-ergativity).",
                source_citation="kumari_2026, p. 142",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="Also widely shared across Jammu Dogri and J&K Gaddi contact areas.",
=======
                function="Marks the transitive subject in perfective aspect (split-ergativity)",
                source_citation="kumari_2026, p. 142",
                variety_id="hp_kangra_palampur",
                is_jk_attested=True,
                notes="Also widely used across Jammu Dogri and J&K Gaddi contact areas.",
>>>>>>> origin/main
            ),
            CaseMarker(
                case_name="Dative / Accusative",
                form_devanagari="जो",
                form_ipa="dʒo",
<<<<<<< HEAD
                function="Marks direct object and indirect recipient.",
                source_citation="kumari_2026, p. 146; grierson_1916, p. 794",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
=======
                function="Marks direct object and indirect object / recipient",
                source_citation="kumari_2026, p. 146; grierson_1916, p. 794",
                variety_id="hp_kangra_palampur",
>>>>>>> origin/main
                is_jk_attested=False,
                notes="Cognate with Western Pahari 'jo' / 'ko'. Needs specific verification in J&K tehsils.",
            ),
            CaseMarker(
                case_name="Ablative",
                form_devanagari="ते / थे",
                form_ipa="te / tʰe",
<<<<<<< HEAD
                function="Marks source, separation, or comparison ('from', 'than').",
                source_citation="kumari_2026, p. 150",
                variety_id="hp_kangra_palampur",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Compare with Dogri 'कशा' (kəʃaː).",
=======
                function="Marks source, origin, or separation ('from')",
                source_citation="kumari_2026, p. 150",
                variety_id="hp_kangra_palampur",
                is_jk_attested=False,
                notes="Compare with Dogri 'कशा' (kəʃaː) and Punjabi 'तों' (tõ).",
>>>>>>> origin/main
            ),
            CaseMarker(
                case_name="Genitive (Possessive)",
                form_devanagari="रा / री / रे",
                form_ipa="raː / riː / reː",
<<<<<<< HEAD
                function="Marks possession; inflects to agree in gender and number with possessed head noun.",
                source_citation="grierson_1916, p. 792; kumari_2026, p. 152",
                variety_id="hp_chamba_bharmaur",
                research_status=ResearchStatus.DOCUMENTED_JK.value,
=======
                function="Marks possession; inflects to agree in gender and number with possessed noun",
                source_citation="grierson_1916, p. 792; kumari_2026, p. 152",
                variety_id="hp_chamba_bharmaur",
>>>>>>> origin/main
                is_jk_attested=True,
                notes="Classic Western Pahari and Dogri genitive marker (-ra, -ri, -re), widely shared across J&K hills.",
            ),
            CaseMarker(
                case_name="Locative",
                form_devanagari="मझ / पर",
                form_ipa="mədʒʰ / pər",
<<<<<<< HEAD
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
=======
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
>>>>>>> origin/main
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
<<<<<<< HEAD
                research_status=ResearchStatus.DOCUMENTED_JK.value,
=======
>>>>>>> origin/main
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
<<<<<<< HEAD
                research_status=ResearchStatus.DOCUMENTED_JK.value,
=======
>>>>>>> origin/main
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
<<<<<<< HEAD
                research_status=ResearchStatus.DOCUMENTED_JK.value,
=======
>>>>>>> origin/main
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
<<<<<<< HEAD
                research_status=ResearchStatus.DOCUMENTED_JK.value,
                is_jk_attested=True,
                notes="Compare Dogri 'तुस्स' (t̪ʊss).",
            ),
            PronominalForm(
                person="interrogative",
                number="both",
                honorificity="neutral",
                proximity=None,
                case="direct",
                form_devanagari="कुण",
                form_ipa="kuɳ",
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
                form_devanagari="के",
                form_ipa="kɛ",
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
                feature="Sentential Negation (नी / ni)",
                description="Pre-verbal negative particle 'नी' (/niː/) used for declarative sentential negation.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 135",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
            ),
            GrammarStatement(
                domain="Negation",
                feature="Negative Copula (नथी / nətʰi)",
                description="Suppletive negative existential/indicative copula 'नथी' meaning 'is not / does not exist'.",
                variety_id="hp_kangra_palampur",
                source_citation="kumari_2026, p. 136",
                research_status=ResearchStatus.DOCUMENTED_COMPARATIVE_ONLY.value,
                is_jk_attested=False,
                notes="Cognate with Gujarati and Old Rajasthani negative copulas.",
            ),
            GrammarStatement(
                domain="Negation",
                feature="Prohibitive Imperative (मथ / matʰ)",
                description="Dedicated prohibitive particle 'मथ' used with imperative verb stems meaning 'do not / don't'.",
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
                    "particle_devanagari": "नी",
                    "particle_ipa": "niː",
                    "function": "Declarative sentential negation (pre-verbal)",
                    "context": "General negation (Kumari 2026, p. 135)",
                },
                {
                    "particle_devanagari": "नथी",
                    "particle_ipa": "nətʰi",
                    "function": "Negative existential / indicative copula ('is not')",
                    "context": "Suppletive negative copula (Kumari 2026, p. 136)",
                },
                {
                    "particle_devanagari": "मथ",
                    "particle_ipa": "matʰ",
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
                "direct_singular": "छोकरा (chokra = boy)",
                "direct_plural": "छोकरे (chokre = boys)",
                "oblique_singular": "छोकरे (chokre)",
                "oblique_plural": "छोकरियां / छोकरां (chokriyan / chokran)",
                "description": "Marked masculine nouns ending in -a; plural suffix -e.",
            },
            {
                "class_id": "class_II_masculine_consonant",
                "ending": "consonant-ending",
                "gender": "masculine",
                "direct_singular": "घर (ghar = house)",
                "direct_plural": "घर (ghar = houses)",
                "oblique_singular": "घर (ghar)",
                "oblique_plural": "घरां (gharan)",
                "description": "Unmarked masculine nouns ending in a consonant; direct plural is invariant.",
            },
            {
                "class_id": "class_III_feminine_vowel",
                "ending": "-i (vowel-ending)",
                "gender": "feminine",
                "direct_singular": "छोकरी (chokri = girl)",
                "direct_plural": "छोकरियाँ (chokriyan = girls)",
                "oblique_singular": "छोकरी (chokri)",
                "oblique_plural": "छोकरियां (chokriyan)",
                "description": "Marked feminine nouns ending in -i; plural suffix -an / -yan.",
            },
            {
                "class_id": "class_IV_feminine_consonant",
                "ending": "consonant-ending",
                "gender": "feminine",
                "direct_singular": "रात (raat = night)",
                "direct_plural": "रातां (raatan = nights)",
                "oblique_singular": "रात (raat)",
                "oblique_plural": "रातां (raatan)",
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
                "direct_singular": "ई (iː = this)",
                "direct_plural": "ए (eː = these)",
                "oblique_singular": "इस (ɪs = this)",
                "oblique_plural": "इन्हां (ɪnʱaː = these)",
                "source": "Kumari et al. (2026), p. 112",
            },
            {
                "type": "distal",
                "direct_singular": "ऊ (uː = that)",
                "direct_plural": "ओ (oː = those)",
                "oblique_singular": "उस (ʊs = that)",
                "oblique_plural": "उन्हों / उन्हान (ʊnʱoː = those)",
                "source": "Kumari et al. (2026), p. 113",
            },
            {
                "type": "relative",
                "direct_singular": "जो (dʒo = who/which)",
                "direct_plural": "जो (dʒo = who/which)",
                "oblique_singular": "जिस (dʒɪs)",
                "oblique_plural": "जिन्हां (dʒɪnʱaː)",
                "source": "Kumari et al. (2026), p. 114",
            },
        ]

    @staticmethod
    def get_adjectives_and_adverbs() -> Dict[str, Any]:
        """Return adjective inflection classes, comparison rules, and adverbs."""
        return {
            "inflecting_adjectives": {
                "pattern": "Suffix -a for MSG, -e for MPL/oblique, -i for FSG/FPL",
                "examples": ["काला / kale / kali (black)", "वडा / vadde / vaddi (big)", "छोटा / chhote / chhoti (small)"],
            },
            "uninflected_adjectives": {
                "pattern": "Invariant consonant- or short vowel-ending stems",
                "examples": ["शैल (ʃɛl = beautiful)", "साफ (saːpʰ = clean)", "लाल (laːl = red)"],
            },
            "comparison": {
                "method": "Periphrastic construction using ablative marker 'कन्हार / kanhār' or 'ते / te'",
                "comparative_example": "राम श्याम कन्हार वडा है (Ram is bigger than Shyam)",
                "superlative_example": "सब ते शैल (most beautiful of all)",
            },
            "adverbs": {
                "manner": ["झट / jhat (quickly)", "हौली / hauli (slowly)"],
                "place": ["इत्थी / itthi (here)", "तित्थी / titthi (there)", "कित्थी / kitthi (where)"],
                "time": ["अज / aj (today)", "कल / kal (yesterday/tomorrow)", "कद / kad (when)"],
            },
        }

    @staticmethod
    def get_verbal_system() -> Dict[str, Any]:
        """Return verb stem structure, TAM paradigms, copula forms, and alignment."""
        return {
            "stem_types": ["simple_root", "causative_stem (-al)", "second_causative (-wal)"],
            "tense_aspect_mood": {
                "present_imperfective": "root + -da + copula (e.g. खांदा है = is eating / eats)",
                "past_imperfective": "root + -da + past copula (e.g. खांदा था = was eating / used to eat)",
                "perfective": "root + -eya/-ya (e.g. खाया = ate; split-ergative subject with 'ne')",
                "future": "root + -ga / -la (e.g. खाएगा / खालो = will eat)",
            },
            "copula": {
                "present": {"singular": "है (hɛ)", "plural": "हन (hən)"},
                "past": {"masc_sg": "था (tʰaː)", "fem_sg": "थी (tʰiː)", "masc_pl": "थे (tʰeː)", "fem_pl": "थियाँ (tʰiːaː)"},
                "negative_copula": "नथी (nətʰi = is not / does not exist)",
            },
            "alignment": "Split ergativity: Ergative alignment with transitive verbs in perfective aspect; Nominative-Accusative alignment elsewhere.",
        }

    @staticmethod
    def get_imperatives() -> Dict[str, Any]:
        """Return imperative verb formations and prohibitive particles."""
        return {
            "affirmative": {
                "intimate_singular": "bare verb root (जा / dʒaː = go!, खा / kʰaː = eat!)",
                "honorific_plural": "root + -o / -a (जाओ / dʒaːo, खाओ / kʰaːo)",
            },
            "prohibitive": {
                "marker": "मथ (/matʰ/)",
                "position": "Immediately pre-verbal",
                "examples": ["मथ जा (matʰ dʒaː = do not go!)", "मथ बोल (matʰ बोल = don't speak!)"],
                "source": "Kumari et al. (2026), p. 137",
            },
        }

    @staticmethod
    def get_interrogatives() -> List[Dict[str, str]]:
        """Return interrogative pronouns and adverbs."""
        return [
            {"word_devanagari": "कुण", "ipa": "kuɳ", "meaning_en": "who", "category": "pronoun"},
            {"word_devanagari": "क्या / के", "ipa": "kjaː / kɛ", "meaning_en": "what", "category": "pronoun"},
            {"word_devanagari": "कित्थी", "ipa": "kɪt̪ʰiː", "meaning_en": "where", "category": "adverb"},
            {"word_devanagari": "कद", "ipa": "kəd̪", "meaning_en": "when", "category": "adverb"},
            {"word_devanagari": "की / किजो", "ipa": "kiː / kɪdʒoː", "meaning_en": "why", "category": "adverb"},
            {"word_devanagari": "किद्दां / कियाँ", "ipa": "kɪddaː / kɪjaː", "meaning_en": "how", "category": "adverb"},
            {"word_devanagari": "केत्ना", "ipa": "ket̪naː", "meaning_en": "how much / how many", "category": "quantifier"},
            {"word_devanagari": "केह्ड़ा", "ipa": "kehɽaː", "meaning_en": "which", "category": "determiner"},
        ]

    @staticmethod
    def get_clause_types() -> Dict[str, Any]:
        """Return simple, compound, and subordinate clause patterns."""
        return {
            "word_order": "SOV (Subject - Object - Verb)",
            "simple_clause": "Direct Subject + Direct/Indirect Object + Verb (+ Aux)",
            "compound_clause": {
                "coordination": ["ते / te (and)", "पर / pər (but)", "या / jaː (or)"],
                "example": "आऊं रोटी खांदा ते पाणी पींदा (I eat bread and drink water)",
            },
            "subordinate_clause": {
                "complementizer": "कि / kɪ (that)",
                "relative_correlative": "जो ... सो ... (who ... that ...)",
                "conditional": "जे ... तां ... (if ... then ...)",
                "temporal": "जद ... तद ... (when ... then ...)",
            },
        }

    @staticmethod
    def get_morphological_patterns() -> Dict[str, Any]:
        """Return causative and abstract morphological derivation patterns."""
        return {
            "causative_derivation": {
                "rule": "Root + -al (first causative) / -wal (second causative)",
                "examples": ["खा (eat) -> खवाल (feed)", "पी (drink) -> पवाल (make drink)"],
            },
            "abstract_nominalization": {
                "rule": "Adjective root + -ai / -i",
                "examples": ["शैल (beautiful) -> शैलाई (beauty)", "गरम (hot) -> गरमी (heat)"],
            },
            "agentive_derivation": {
                "rule": "Noun/verb stem + -वालू / -वाला",
                "examples": ["भेड़ (sheep) -> भेड़वालू (shepherd)"],
            },
        }

    @staticmethod
    def get_numeral_system_summary() -> Dict[str, Any]:
        """Return overview of numeral formation templates."""
        return {
            "base": "Decimal (base 10) with vigesimal (base 20) substrate traces",
            "cardinals_range": "1 to 100 documented with higher orders (1000, 100k, 10M, 1B)",
            "ordinals_formation": "Root + -वा / -वां / -था (e.g. पहला, दूजा, तीजा, चौथा)",
            "fractionals_formation": "अद्ध (1/2), पौणे (3/4), सवा (1 1/4), डेढ़ (1 1/2), ढाई (2 1/2)",
            "distributives_formation": "Reduplication: इक्क-इक्क (one each), दो-दो (two each)",
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

=======
                is_jk_attested=True,
                notes="Compare Dogri 'तुस्स' (t̪ʊss).",
            ),
        ]
>>>>>>> origin/main
