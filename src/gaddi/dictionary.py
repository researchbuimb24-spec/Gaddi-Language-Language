"""Searchable dictionary and multi-language translation engine for Gaddi."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

try:
    import importlib.resources as pkg_resources
except ImportError:
    pkg_resources = None  # type: ignore

from gaddi.models import EvidenceStatus, LexicalEntry
from gaddi.registry import VarietyRegistry, default_varieties


def normalize_text(text: str) -> str:
    """Normalize text using Unicode NFC form and strip surrounding whitespace."""
    if not text:
        return ""
    return unicodedata.normalize("NFC", text).strip()


def fold_text(text: str) -> str:
    """Normalize and fold diacritics and phonetics for tolerant fuzzy matching.

    Folds IPA symbols, macrons, retroflex dots, and special diacritics into plain ASCII:
      - ╔æ, ╩î, ╔Ö, ├ñ, ─ü, ├í, a╦É -> a
      - ─½, ╔¬, ├¡, i╦É -> i
      - ┼½, ╩è, ├║, u╦É -> u
      - ─ô, ╔¢, ├⌐, e╦É -> e
      - ┼ì, ╔ö, ├│, o╦É -> o
      - ╩ê, ß╣¡ -> t; ╔û, ß╕ì, ╔╜, ß╣¢ -> d / r
      - ╔│, ß╣ç, ├▒, ╔▓, ┼ï -> n
      - ╩â, ┼¢, ß╣ú -> s
      - t╩â -> ch; d╩Æ -> j
      - ╔¡, ß╕╖ -> l
      - ╩▒, ╩░ -> h
      - removes length marks ╦É, stress ╦ê, tone marks, and combining diacritics
    """
    if not text:
        return ""
    s = unicodedata.normalize("NFD", text.lower().strip())
    s = "".join(c for c in s if not unicodedata.combining(c))

    subs = {
        "t╩â": "ch",
        "d╩Æ": "j",
        "╔æ": "a", "╩î": "a", "╔Ö": "a", "├ñ": "a", "─ü": "a", "├í": "a",
        "╔¬": "i", "─½": "i", "├¡": "i",
        "╩è": "u", "┼½": "u", "├║": "u",
        "╔¢": "e", "─ô": "e", "├⌐": "e",
        "╔ö": "o", "┼ì": "o", "├│": "o",
        "╩ê": "t", "ß╣¡": "t",
        "╔û": "d", "ß╕ì": "d", "╔╜": "r", "ß╣¢": "r",
        "╔│": "n", "ß╣ç": "n", "├▒": "n", "╔▓": "n", "┼ï": "n",
        "╩â": "s", "┼¢": "s", "ß╣ú": "s",
        "╔¡": "l", "ß╕╖": "l",
        "╩▒": "h", "╩░": "h",
        "╦É": "", "╦æ": "", "'": "", "╦ê": "", "╦î": "", "╠â": "", "~": "",
    }
    for k, v in subs.items():
        s = s.replace(k, v)

    # Devanagari folding: normalize nukta
    s = s.replace("αñ╝", "")
    return s


CATEGORY_ALIASES: Dict[str, str] = {
    "animals": "animals",
    "animal": "animals",
    "bird": "animals",
    "birds": "animals",
    "fauna": "animals",
    "insect": "animals",
    "insects": "animals",
    "family": "family",
    "kinship": "family",
    "people": "family",
    "relationship": "family",
    "relationships": "family",
    "relatives": "family",
    "body": "body",
    "health": "body",
    "anatomy": "body",
    "body_parts": "body",
    "feelings": "body",
    "plants": "plants",
    "plant": "plants",
    "flora": "plants",
    "trees": "plants",
    "tree": "plants",
    "crops": "plants",
    "flowers": "plants",
    "food": "food",
    "cooking": "food",
    "drink": "food",
    "drinks": "food",
    "meal": "food",
    "meals": "food",
    "eating": "food",
    "water": "water",
    "weather": "water",
    "seasons": "water",
    "hydrology": "water",
    "rain": "water",
    "snow": "water",
    "mountains": "mountains",
    "mountain": "mountains",
    "river": "mountains",
    "rivers": "mountains",
    "landscape": "mountains",
    "geography": "mountains",
    "forests": "mountains",
    "agriculture": "agriculture",
    "farming": "agriculture",
    "livestock": "agriculture",
    "herding": "agriculture",
    "household": "household",
    "furniture": "household",
    "clothing": "household",
    "ornaments": "household",
    "house": "household",
    "home": "household",
    "tools": "tools",
    "tool": "tools",
    "occupations": "tools",
    "trades": "tools",
    "utensils": "tools",
    "travel": "travel",
    "transport": "travel",
    "direction": "travel",
    "directions": "travel",
    "movement": "travel",
    "numbers": "numbers",
    "number": "numbers",
    "numeral": "numbers",
    "numerals": "numbers",
    "quantities": "numbers",
    "time": "numbers",
    "colors": "colors",
    "color": "colors",
    "colour": "colors",
    "colours": "colors",
    "shapes": "colors",
    "qualities": "colors",
    "actions": "actions",
    "action": "actions",
    "verbs": "actions",
    "activity": "actions",
    "nature": "nature",
    "environment": "nature",
    "ecology": "nature",
    "religion": "religion",
    "festivals": "religion",
    "traditions": "religion",
    "folklore": "religion",
    "spiritual": "religion",
    "ritual": "religion",
    "education": "education",
    "school": "education",
    "technology": "education",
    "modern": "education",
    "expressions": "expressions",
    "expression": "expressions",
    "greetings": "expressions",
    "questions": "expressions",
    "phrases": "expressions",
    "general": "general",
    "misc": "general",
    "other": "general",
}


class GaddiDictionary:
    """In-memory searchable dictionary with multi-script, multi-language, and topic support."""

    def __init__(
        self,
        entries: Optional[List[LexicalEntry]] = None,
        variety_registry: Optional[VarietyRegistry] = None,
        auto_load_defaults: bool = True,
        include_unified: bool = False,
    ):
        self.varieties = variety_registry or default_varieties
        self._entries: List[LexicalEntry] = []
        self._id_index: Dict[str, LexicalEntry] = {}
        self._unified_entries: List[LexicalEntry] = []
        self._unified_id_index: Dict[str, LexicalEntry] = {}

        if entries:
            for entry in entries:
                self.add_entry(entry)
        elif auto_load_defaults:
            self._load_packaged_resources(include_unified=include_unified)

    def _load_packaged_resources(self, include_unified: bool = False) -> None:
        """Load bundled verified J&K, cultural, comparative, and unified lexicons."""
        res_dir = Path(__file__).parent / "resources"
        data_dir = Path(__file__).parents[2] / "data"

        # 1. Load verified J&K lexical database
        jk_path = res_dir / "lexicon_jk.json"
        if not jk_path.exists():
            jk_path = data_dir / "lexicon_jk.json"
        if jk_path.exists():
            self.load_from_json(jk_path)

        # 2. Load J&K cultural & regional ecological terms
        cult_path = res_dir / "cultural_terms_jk.json"
        if not cult_path.exists():
            cult_path = data_dir / "cultural_terms_jk.json"
        if cult_path.exists():
            self.load_from_json(cult_path)

        # 3. Load comparative baseline lexicon
        comp_path = res_dir / "lexicon_comparative.json"
        if not comp_path.exists():
            comp_path = data_dir / "lexicon_comparative.json"
        if comp_path.exists():
            self.load_from_json(comp_path)

        # Fallback to legacy seed_corpus.json if individual files missing
        if len(self._entries) == 0:
            seed_path = data_dir / "seed_corpus.json"
            if seed_path.exists():
                self.load_from_json(seed_path)

        # 4. Load large-scale unified lexical database (Command 12)
        uni_path = res_dir / "dictionary_unified.json"
        if not uni_path.exists():
            uni_path = data_dir / "dictionary_unified.json"
        if uni_path.exists():
            with open(uni_path, "r", encoding="utf-8") as f:
                uni_raw = json.load(f)
            for item in uni_raw:
                e = LexicalEntry.from_dict(item)
                self._unified_entries.append(e)
                self._unified_id_index[e.id] = e
                if include_unified:
                    self.add_entry(e)

    def add_entry(self, entry: LexicalEntry) -> None:
        """Add a lexical entry to the dictionary and update internal indices."""
        if entry.id in self._id_index:
            idx = next(i for i, e in enumerate(self._entries) if e.id == entry.id)
            self._entries[idx] = entry
        else:
            self._entries.append(entry)
        self._id_index[entry.id] = entry

    def load_from_json(self, path: Union[str, Path]) -> int:
        """Load entries from a JSON file. Returns count of entries loaded."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for item in data:
            entry = LexicalEntry.from_dict(item)
            self.add_entry(entry)
            count += 1
        return count

    def get_by_id(self, entry_id: str) -> Optional[LexicalEntry]:
        """Look up an entry by its unique identifier."""
        return self._id_index.get(entry_id) or self._unified_id_index.get(entry_id)

    # -------------------------------------------------------------------------
    # Core Translation Engine: translate()
    # -------------------------------------------------------------------------
    def translate(
        self,
        query: str,
        from_lang: Optional[str] = None,
        to_lang: str = "gaddi",
        source: Optional[str] = None,
        target: Optional[str] = None,
        jk_only: Optional[bool] = None,
        allow_comparative: Optional[bool] = None,
        include_cultural: Optional[bool] = None,
        exact: bool = False,
    ) -> List[LexicalEntry]:
        """Translate between English, Hindi, Urdu, Punjabi, Dogri, and Gaddi.

        Supports both functional signatures:
          gaddi.translate("water", source="en", target="gaddi")
          gaddi.translate("handloom", from_lang="en")

        EVIDENCE POLICIES:
        - When using `source` and `target` (Command 12 API), translates across the
          complete unified database including comparative and cultural material.
        - When using legacy `from_lang` without explicit `source`, preserves the
          strict verification baseline (jk_only=True by default).
        """
        is_modern_call = source is not None or target is not None
        src_lang = (source or from_lang or "en").lower().strip()
        tgt_lang = (target or to_lang or "gaddi").lower().strip()

        if is_modern_call:
            effective_jk_only = False if jk_only is None else bool(jk_only)
            effective_allow_comp = True if allow_comparative is None else bool(allow_comparative)
            effective_inc_cult = True if include_cultural is None else bool(include_cultural)
            active_pool = self._unified_entries if self._unified_entries else self._entries
        else:
            effective_jk_only = True if jk_only is None else bool(jk_only)
            effective_allow_comp = False if allow_comparative is None else bool(allow_comparative)
            effective_inc_cult = False if include_cultural is None else bool(include_cultural)
            active_pool = self._entries

        # Handle reverse direction: Gaddi -> Other language
        if src_lang in ("gaddi", "gad") and tgt_lang not in ("gaddi", "gad"):
            # Lookup Gaddi query in unified entries
            return self.lookup(query, jk_only=effective_jk_only)

        # Lookup in source language
        if src_lang in ("en", "eng", "english"):
            raw_results = self.lookup_english(query, jk_only=False, exact=exact, pool=active_pool)
        elif src_lang in ("hi", "hin", "hindi"):
            raw_results = self.lookup_hindi(query, jk_only=False, exact=exact, pool=active_pool)
        elif src_lang in ("ur", "urd", "urdu"):
            raw_results = self.lookup_urdu(query, jk_only=False, exact=exact, pool=active_pool)
        elif src_lang in ("pa", "pan", "punjabi"):
            raw_results = self.lookup_punjabi(query, jk_only=False, exact=exact, pool=active_pool)
        elif src_lang in ("doi", "dog", "dogri"):
            raw_results = self.lookup_dogri(query, jk_only=False, exact=exact, pool=active_pool)
        else:
            raise ValueError(
                f"Unsupported source language: '{src_lang}'. "
                f"Supported: 'en', 'hi', 'ur', 'pa', 'doi', 'gaddi'."
            )

        filtered: List[LexicalEntry] = []
        seen_ids: Set[str] = set()

        for entry in raw_results:
            if entry.id in seen_ids:
                continue

            is_jk = self._is_jk_variety(entry.variety_id)
            is_verified_lexical = entry.evidence_status in (
                EvidenceStatus.VERIFIED_JK_LEXICAL.value,
                "verified_jk",
            )
            is_cultural = entry.evidence_status in (
                EvidenceStatus.JK_CULTURAL_TERM.value,
                EvidenceStatus.JK_PLACE_OR_ECOLOGICAL_TERM.value,
            )
            is_comparative = entry.evidence_status in (
                EvidenceStatus.COMPARATIVE_ONLY.value,
                EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value,
            )

            if effective_jk_only:
                if is_jk and is_verified_lexical:
                    filtered.append(entry)
                    seen_ids.add(entry.id)
                elif is_jk and is_cultural and effective_inc_cult:
                    filtered.append(entry)
                    seen_ids.add(entry.id)
            else:
                if is_comparative and not effective_allow_comp:
                    continue
                if is_cultural and not effective_inc_cult:
                    continue
                filtered.append(entry)
                seen_ids.add(entry.id)

        # Sort translation results: exact gloss match first, then J&K priority
        clean_q_lower = normalize_text(query).lower()

        def trans_sort_key(e: LexicalEntry) -> Tuple:
            # Check if any definition is an exact whole word or exact definition
            is_exact_def = False
            for s in e.senses:
                d_en = (s.definition_en or "").lower().strip(" .,;()")
                d_hi = (s.definition_hi or "").strip(" αÑñ;,()")
                if clean_q_lower in (d_en, d_hi) or clean_q_lower in d_en.split():
                    is_exact_def = True
                    break
            is_jk = self._is_jk_variety(e.variety_id)
            is_verified = e.evidence_status == EvidenceStatus.VERIFIED_JK.value
            return (
                0 if is_exact_def else 1,
                0 if is_jk else 1,
                0 if is_verified else 1,
                e.lemma_devanagari,
            )

        return sorted(filtered, key=trans_sort_key)

    # -------------------------------------------------------------------------
    # Priority 1: English -> Gaddi Lookup
    # -------------------------------------------------------------------------
    def lookup_english(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Search English definitions and semantic glosses for matching Gaddi entries."""
        clean_q = normalize_text(query).lower()
        if not clean_q:
            return []

        search_pool = pool if pool is not None else self._entries
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        # Prepare regex pattern supporting singular/plural inflection
        base_q = clean_q.rstrip('s') if len(clean_q) > 3 and clean_q.endswith('s') else clean_q
        q_pattern = r'\b' + re.escape(base_q) + r'(?:s|es)?\b'

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                defn = normalize_text(sense.definition_en).lower()
                tokens = [t.strip(",.()[]{}:;\"' /") for t in defn.split()]
                if exact:
                    if clean_q == defn or clean_q in tokens:
                        matched = True
                        break
                else:
                    if clean_q == defn or clean_q in tokens or bool(re.search(q_pattern, defn)):
                        matched = True
                        break

            if matched and entry.id not in seen:
                seen.add(entry.id)
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Priority 2: Hindi -> Gaddi Lookup
    # -------------------------------------------------------------------------
    def lookup_hindi(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Search Hindi definitions and glosses for matching Gaddi entries."""
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        search_pool = pool if pool is not None else self._entries
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                if not sense.definition_hi:
                    continue
                defn = normalize_text(sense.definition_hi)
                tokens = [t.strip("αÑñ,;()\"' /") for t in defn.split()]
                if exact:
                    if clean_q == defn or clean_q in tokens:
                        matched = True
                        break
                else:
                    if clean_q in defn or clean_q in tokens:
                        matched = True
                        break

            if matched and entry.id not in seen:
                seen.add(entry.id)
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Priority 3: Urdu -> Gaddi Lookup
    # -------------------------------------------------------------------------
    def lookup_urdu(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Search Urdu definitions and glosses for matching Gaddi entries."""
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        search_pool = pool if pool is not None else self._entries
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                if not sense.definition_ur:
                    continue
                defn = normalize_text(sense.definition_ur)
                tokens = [t.strip("╪î╪¢█ö()\"' /") for t in defn.split()]
                if exact:
                    if clean_q == defn or clean_q in tokens:
                        matched = True
                        break
                else:
                    if clean_q in defn or clean_q in tokens:
                        matched = True
                        break

            if matched and entry.id not in seen:
                seen.add(entry.id)
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Additional Regional Languages: Punjabi & Dogri
    # -------------------------------------------------------------------------
    def lookup_punjabi(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Search Punjabi translations for matching Gaddi entries."""
        clean_q = normalize_text(query).lower()
        if not clean_q:
            return []

        search_pool = pool if pool is not None else (self._unified_entries or self._entries)
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            pa_val = entry.metadata.get("translations", {}).get("pa", "")
            if pa_val:
                pa_clean = normalize_text(pa_val).lower()
                tokens = [t.strip("αÑñ,;()\"' /") for t in pa_clean.split()]
                matched = False
                if exact:
                    if clean_q == pa_clean or clean_q in tokens:
                        matched = True
                else:
                    if clean_q in pa_clean or clean_q in tokens:
                        matched = True

                if matched and entry.id not in seen:
                    seen.add(entry.id)
                    results.append(entry)

        return self._sort_results(results)

    def lookup_dogri(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Search Dogri translations for matching Gaddi entries."""
        clean_q = normalize_text(query).lower()
        if not clean_q:
            return []

        search_pool = pool if pool is not None else (self._unified_entries or self._entries)
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            doi_val = entry.metadata.get("translations", {}).get("doi", "")
            if doi_val:
                doi_clean = normalize_text(doi_val).lower()
                tokens = [t.strip("αÑñ,;()\"' /") for t in doi_clean.split()]
                matched = False
                if exact:
                    if clean_q == doi_clean or clean_q in tokens:
                        matched = True
                else:
                    if clean_q in doi_clean or clean_q in tokens:
                        matched = True

                if matched and entry.id not in seen:
                    seen.add(entry.id)
                    results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Gaddi Headword Lookup: lookup()
    # -------------------------------------------------------------------------
    def lookup(
        self,
        query: str,
        jk_only: bool = False,
        script: Optional[str] = None,
    ) -> List[LexicalEntry]:
        """Look up Gaddi headwords across Devanagari, Perso-Arabic, Latin/IPA, and Takri."""
        res = self.lookup_gaddi(query, jk_only=jk_only, script=script)
        if not res and self._unified_entries:
            res = self.lookup_gaddi(query, jk_only=jk_only, script=script, pool=self._unified_entries)
        return res

    def lookup_gaddi(
        self,
        query: str,
        jk_only: bool = False,
        script: Optional[str] = None,
        pool: Optional[List[LexicalEntry]] = None,
    ) -> List[LexicalEntry]:
        """Internal multi-script Gaddi headword matching with diacritic and phonetic tolerance."""
        clean_q = normalize_text(query)
        clean_q_lower = clean_q.lower()
        q_folded = fold_text(clean_q)
        if not clean_q:
            return []

        search_pool = pool if pool is not None else self._entries
        results: List[LexicalEntry] = []
        seen: Set[str] = set()

        for entry in search_pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False

            # Check Devanagari
            if (not script or script.lower() in ("deva", "devanagari")) and entry.lemma_devanagari:
                lemma = normalize_text(entry.lemma_devanagari)
                if clean_q == lemma or clean_q in lemma:
                    matched = True
                elif clean_q.replace("αñ╝", "") == lemma.replace("αñ╝", ""):
                    matched = True

            # Check Perso-Arabic
            if not matched and (not script or script.lower() in ("arab", "urdu", "arabic")) and entry.lemma_perso_arabic:
                lemma = normalize_text(entry.lemma_perso_arabic)
                if clean_q == lemma or clean_q in lemma:
                    matched = True

            # Check IPA / Latin (with phonetic folding)
            if not matched and (not script or script.lower() in ("latn", "latin", "ipa")) and entry.lemma_ipa:
                lemma = normalize_text(entry.lemma_ipa).lower()
                lemma_f = fold_text(lemma)
                if clean_q_lower == lemma or clean_q_lower in lemma:
                    matched = True
                elif q_folded == lemma_f or q_folded in lemma_f:
                    matched = True

            # Check Attestation Source Spellings & Transliteration
            if not matched and (not script or script.lower() in ("latn", "latin")):
                if entry.normalized_headword and q_folded == fold_text(entry.normalized_headword):
                    matched = True
                if not matched:
                    for att in entry.attestations:
                        if att.source_spelling:
                            spelling = normalize_text(att.source_spelling).lower()
                            sp_folded = fold_text(spelling)
                            if clean_q_lower == spelling or clean_q_lower in spelling.split():
                                matched = True
                                break
                            elif q_folded == sp_folded or q_folded in sp_folded.split():
                                matched = True
                                break

            # Check Takri
            if not matched and (not script or script.lower() in ("takr", "takri")) and entry.lemma_takri:
                lemma = normalize_text(entry.lemma_takri)
                if clean_q == lemma or clean_q in lemma:
                    matched = True

            if matched and entry.id not in seen:
                seen.add(entry.id)
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Universal Search: search() with Relevance Ranking
    # -------------------------------------------------------------------------
    def search(
        self,
        query: str,
        jk_only: bool = False,
        include_comparative: bool = True,
        include_cultural: bool = True,
        include_unverified: bool = False,
    ) -> List[LexicalEntry]:
        """Universal multi-lingual, multi-script search with relevance ranking.

        Ranks exact headwords above transliterations, variants, and glosses.
        Tolerant of partial words, case variations, and diacritics. Suppresses duplicate entries.
        """
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        q_lower = clean_q.lower()
        q_folded = fold_text(clean_q)

        # Build candidate pool
        seen_ids: Set[str] = set()
        pool: List[LexicalEntry] = []

        # Add baseline entries
        for e in self._entries:
            if e.id not in seen_ids:
                seen_ids.add(e.id)
                pool.append(e)

        # Add unified entries if comparative enabled
        if include_comparative and self._unified_entries:
            for e in self._unified_entries:
                if e.id not in seen_ids:
                    seen_ids.add(e.id)
                    pool.append(e)

        scored_results: List[Tuple[int, LexicalEntry]] = []

        for entry in pool:
            # Filter checks
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            if not include_comparative and entry.evidence_status in (
                EvidenceStatus.COMPARATIVE_ONLY.value,
                EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value,
            ):
                continue

            if not include_cultural and entry.evidence_status in (
                EvidenceStatus.JK_CULTURAL_TERM.value,
                EvidenceStatus.JK_PLACE_OR_ECOLOGICAL_TERM.value,
            ):
                continue

            if not include_unverified and entry.evidence_status in (
                EvidenceStatus.COMMUNITY_SUBMITTED_UNVERIFIED.value,
                EvidenceStatus.UNVERIFIED_LEAD.value,
            ):
                continue

            score = 0
            lemma_d = entry.lemma_devanagari or ""
            lemma_ipa = entry.lemma_ipa or ""
            norm_h = entry.normalized_headword or ""
            variants = entry.metadata.get("variants", [])
            senses = entry.senses or []

            # 1. Exact Devanagari headword match
            if clean_q == lemma_d:
                score = 1000
            elif clean_q == lemma_d.replace("αñ╝", ""):
                score = 950
            # 2. Exact IPA / Roman transliteration match
            elif lemma_ipa and q_lower == lemma_ipa.lower():
                score = 900
            elif (lemma_ipa and q_folded == fold_text(lemma_ipa)) or (norm_h and q_folded == fold_text(norm_h)):
                score = 850
            # 3. Exact variant or attestation spelling match
            elif any(q_lower == (v or "").lower() for v in variants):
                score = 800
            elif any(q_folded == fold_text(v or "") for v in variants):
                score = 770
            elif any(q_lower == (a.source_spelling or "").lower() for a in entry.attestations if a.source_spelling):
                score = 750
            elif any(q_folded == fold_text(a.source_spelling or "") for a in entry.attestations if a.source_spelling):
                score = 740
            # 4. Prefix match on headword
            elif lemma_d.startswith(clean_q):
                score = 700
            elif lemma_ipa and fold_text(lemma_ipa).startswith(q_folded):
                score = 670
            elif norm_h and fold_text(norm_h).startswith(q_folded):
                score = 650
            # 5. Exact word match in definitions / glosses
            elif any(clean_q == (s.definition_hi or "").strip("αÑñ,;()\"' ") for s in senses):
                score = 600
            elif any(q_lower == (s.definition_en or "").lower().strip(",.()[]{}:;\"' ") for s in senses):
                score = 590
            elif any(q_lower in [t.strip(",.()[]{}:;\"' ") for t in (s.definition_en or "").lower().split()] for s in senses):
                score = 580
            # 6. Substring in headword, IPA, or variants
            elif clean_q in lemma_d:
                score = 500
            elif lemma_ipa and q_folded in fold_text(lemma_ipa):
                score = 480
            elif norm_h and q_folded in fold_text(norm_h):
                score = 460
            elif any(q_folded in fold_text(v or "") for v in variants):
                score = 450
            # 7. Substring in definitions
            elif any(clean_q in (s.definition_hi or "") for s in senses):
                score = 400
            elif any(q_lower in (s.definition_en or "").lower() for s in senses):
                score = 380
            elif any(clean_q in (s.definition_ur or "") for s in senses):
                score = 350
            # 8. Category / semantic field match
            elif any(q_lower == c.lower() for c in entry.metadata.get("categories", [])):
                score = 300
            elif any(q_lower in c.lower() for c in entry.metadata.get("categories", [])):
                score = 250

            if score > 0:
                scored_results.append((score, entry))

        # Sort: score descending, J&K first, verified first, then lemma
        def rank_sort_key(item: Tuple[int, LexicalEntry]) -> Tuple:
            sc, e = item
            is_jk = self._is_jk_variety(e.variety_id)
            is_verified = e.evidence_status == EvidenceStatus.VERIFIED_JK.value
            return (
                -sc,
                0 if is_jk else 1,
                0 if is_verified else 1,
                e.lemma_devanagari,
            )

        scored_results.sort(key=rank_sort_key)
        return [e for _, e in scored_results]

    # -------------------------------------------------------------------------
    # Topic & Categorization API (Command 12)
    # -------------------------------------------------------------------------
    def get_categories(self) -> List[str]:
        """Return all 19 standardized lexical categories."""
        return [
            "family",
            "body",
            "animals",
            "plants",
            "food",
            "water",
            "mountains",
            "agriculture",
            "household",
            "tools",
            "travel",
            "numbers",
            "colors",
            "actions",
            "nature",
            "religion",
            "education",
            "expressions",
            "general",
        ]

    def search_by_category(self, category: str, jk_only: bool = False) -> List[LexicalEntry]:
        """Search vocabulary by standardized topic category or alias."""
        cat_key = category.lower().strip()
        norm_cat = CATEGORY_ALIASES.get(cat_key, cat_key)

        pool = self._unified_entries if self._unified_entries else self._entries
        results: List[LexicalEntry] = []
        for entry in pool:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue
            entry_cats = [c.lower() for c in entry.metadata.get("categories", [])]
            if norm_cat in entry_cats or any(norm_cat in c for c in entry_cats):
                results.append(entry)

        return self._sort_results(results)

    def get_synonyms(self, word: str) -> List[LexicalEntry]:
        """Return synonym headwords sharing primary semantic concepts or glosses."""
        clean_w = normalize_text(word).lower()
        if not clean_w:
            return []

        pool = self._unified_entries if self._unified_entries else self._entries
        targets: List[LexicalEntry] = []
        for entry in pool:
            lemma_d = normalize_text(entry.lemma_devanagari or "").lower()
            lemma_i = normalize_text(entry.lemma_ipa or "").lower()
            norm_h = normalize_text(entry.normalized_headword or "").lower()
            if clean_w in (lemma_d, lemma_i, norm_h):
                targets.append(entry)

        target_defs: Set[str] = set()
        target_cats: Set[str] = set()
        for t in targets:
            for s in t.senses:
                if s.definition_en:
                    for token in s.definition_en.lower().split():
                        token = token.strip(",.()[]{}:;\"'")
                        if len(token) > 3 and token not in ("with", "from", "that", "this", "also", "used"):
                            target_defs.add(token)
            for c in t.metadata.get("categories", []):
                target_cats.add(c)

        results: List[LexicalEntry] = []
        seen = {t.id for t in targets}
        for entry in pool:
            if entry.id in seen:
                continue

            entry_syns = [normalize_text(s).lower() for s in entry.metadata.get("synonyms", [])]
            if clean_w in entry_syns:
                results.append(entry)
                seen.add(entry.id)
                continue

            matched_tokens = 0
            for s in entry.senses:
                if s.definition_en:
                    for token in s.definition_en.lower().split():
                        token = token.strip(",.()[]{}:;\"'")
                        if token in target_defs:
                            matched_tokens += 1
            if matched_tokens >= 1 and any(c in target_cats for c in entry.metadata.get("categories", [])):
                results.append(entry)
                seen.add(entry.id)

        # Concept fallback: if word is an English gloss keyword
        if not results and not targets:
            for entry in pool:
                for s in entry.senses:
                    defn = (s.definition_en or "").lower()
                    tokens = [t.strip(",.()[]{}:;\"'") for t in defn.split()]
                    if clean_w == defn or clean_w in tokens:
                        if entry.id not in seen:
                            results.append(entry)
                            seen.add(entry.id)

        return self._sort_results(results)

    def get_variants(self, word: str) -> List[str]:
        """Return all distinct spelling, script, and phonetic variants of a word."""
        clean_w = normalize_text(word).lower()
        if not clean_w:
            return []

        pool = self._unified_entries if self._unified_entries else self._entries
        variants: List[str] = []
        seen: Set[str] = set()

        def add_var(v: Optional[str]) -> None:
            if v:
                v_clean = normalize_text(v)
                if v_clean and v_clean not in seen:
                    seen.add(v_clean)
                    variants.append(v_clean)

        for entry in pool:
            lemma_d = normalize_text(entry.lemma_devanagari or "").lower()
            lemma_i = normalize_text(entry.lemma_ipa or "").lower()
            norm_h = normalize_text(entry.normalized_headword or "").lower()

            matched = clean_w in (lemma_d, lemma_i, norm_h)
            if not matched:
                for att in entry.attestations:
                    if att.source_spelling and clean_w == normalize_text(att.source_spelling).lower():
                        matched = True
                        break
            if not matched:
                for s in entry.senses:
                    if s.definition_en and clean_w in [t.strip(",.()[]{}:;\"'") for t in s.definition_en.lower().split()]:
                        matched = True
                        break

            if matched:
                add_var(entry.lemma_devanagari)
                add_var(entry.lemma_ipa)
                add_var(entry.lemma_perso_arabic)
                add_var(entry.lemma_takri)
                add_var(entry.original_transcription)
                for v in entry.metadata.get("variants", []):
                    add_var(v)
                for v in entry.metadata.get("phonemic_variants", []):
                    add_var(v)
                for att in entry.attestations:
                    add_var(att.source_spelling)
                    add_var(att.context)

        return variants

    def get_examples_for_headword(self, headword: str) -> List[Dict[str, Any]]:
        """Retrieve numbered grammar examples explicitly associated with a headword."""
        return self.get_examples(headword)

    def get_examples(self, word: str) -> List[Dict[str, Any]]:
        """Return numbered grammar examples linked to or mentioning a word."""
        clean_w = normalize_text(word)
        if not clean_w:
            return []

        w_lower = clean_w.lower()
        w_folded = fold_text(clean_w)

        from gaddi.grammar import GrammarRegistry
        all_examples = GrammarRegistry.get_examples_dataset()
        if not all_examples:
            return []

        # 1. Check dictionary entries to collect linked example IDs
        linked_ids: Set[str] = set()
        pool = self._unified_entries if self._unified_entries else self._entries
        for entry in pool:
            lemma_d = normalize_text(entry.lemma_devanagari or "")
            lemma_i = normalize_text(entry.lemma_ipa or "").lower()
            if (
                clean_w == lemma_d
                or w_lower == lemma_i
                or w_folded == fold_text(lemma_i)
                or clean_w == entry.id
            ):
                for ex_id in entry.metadata.get("example_ids", []):
                    linked_ids.add(ex_id)

        results: List[Dict[str, Any]] = []
        seen: Set[str] = set()

        # Add explicitly linked examples first
        if linked_ids:
            for ex in all_examples:
                ex_id = ex.get("example_id") or ex.get("id")
                if ex_id in linked_ids and ex_id not in seen:
                    seen.add(ex_id)
                    results.append(ex)

        # 2. Text search across examples
        for ex in all_examples:
            ex_id = ex.get("example_id") or ex.get("id")
            if ex_id in seen:
                continue

            raw = normalize_text(ex.get("raw_text") or "").lower()
            g_trans = normalize_text(ex.get("gaddi_transcription") or "").lower()
            en_trans = normalize_text(ex.get("english_translation") or "").lower()
            hi_trans = normalize_text(ex.get("hindi_translation") or "").lower()
            m_gloss = normalize_text(ex.get("morpheme_gloss") or "").lower()

            en_tokens = [t.strip(",.()[]{}:;\"' /") for t in en_trans.split()]

            matched = False
            if clean_w in raw or clean_w in hi_trans:
                matched = True
            elif w_lower in g_trans or w_folded in fold_text(g_trans):
                matched = True
            elif w_lower in en_tokens or w_lower in en_trans:
                matched = True
            elif w_lower in m_gloss:
                matched = True

            if matched:
                seen.add(ex_id)
                results.append(ex)

        return results

    def get_unified_entries(self) -> List[LexicalEntry]:
        """Return all entries in the expanded unified database."""
        return list(self._unified_entries)

    def get_unique_headwords(self) -> List[str]:
        """Return list of distinct headword lemmas across the unified database."""
        pool = self._unified_entries if self._unified_entries else self._entries
        return sorted(list({e.lemma_devanagari for e in pool if e.lemma_devanagari}))

    def get_total_records(self) -> int:
        """Return total source attestation records in the unified database."""
        pool = self._unified_entries if self._unified_entries else self._entries
        return sum(len(e.attestations) for e in pool)

    # -------------------------------------------------------------------------
    # Filtering & Analytics
    # -------------------------------------------------------------------------
    def filter_by_variety(self, variety_id: str) -> List[LexicalEntry]:
        return [e for e in self._entries if e.variety_id == variety_id]

    def filter_by_pos(self, part_of_speech: str) -> List[LexicalEntry]:
        pos_clean = part_of_speech.lower().strip()
        return [e for e in self._entries if e.part_of_speech.lower() == pos_clean]

    def filter_by_evidence_status(self, status: Union[str, EvidenceStatus]) -> List[LexicalEntry]:
        stat_val = status.value if isinstance(status, EvidenceStatus) else str(status)
        return [e for e in self._entries if e.evidence_status == stat_val]

    def get_verified_jk_lexical_entries(self) -> List[LexicalEntry]:
        """Return all entries that are verified J&K linguistic lexical items."""
        return [
            e for e in self._entries
            if self._is_jk_variety(e.variety_id)
            and e.evidence_status in (EvidenceStatus.VERIFIED_JK_LEXICAL.value, "verified_jk")
        ]

    def get_cultural_entries(self) -> List[LexicalEntry]:
        """Return all entries categorized as cultural, ethnographic, or regional ecological terms."""
        return [
            e for e in self._entries
            if e.evidence_status in (
                EvidenceStatus.JK_CULTURAL_TERM.value,
                EvidenceStatus.JK_PLACE_OR_ECOLOGICAL_TERM.value,
            )
        ]

    def get_jk_entries(self) -> List[LexicalEntry]:
        """Return all entries belonging to Jammu & Kashmir varieties (lexical, cultural, ecological)."""
        return [e for e in self._entries if self._is_jk_variety(e.variety_id)]

    def get_comparative_entries(self) -> List[LexicalEntry]:
        """Return all entries designated as comparative baselines."""
        return [
            e for e in self._entries
            if e.evidence_status in (
                EvidenceStatus.COMPARATIVE_ONLY.value,
                EvidenceStatus.DOCUMENTED_OTHER_VARIETY.value,
            )
            or not self._is_jk_variety(e.variety_id)
        ]

    def get_unverified_entries(self) -> List[LexicalEntry]:
        """Return entries requiring community or academic verification."""
        return [
            e for e in self._entries
            if e.evidence_status in (
                EvidenceStatus.COMMUNITY_SUBMITTED_UNVERIFIED.value,
                EvidenceStatus.UNVERIFIED_LEAD.value,
                EvidenceStatus.DISPUTED.value,
            )
        ]

    def count_by_variety(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for e in self._entries:
            counts[e.variety_id] = counts.get(e.variety_id, 0) + 1
        return counts

    def count_by_evidence_status(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for e in self._entries:
            counts[e.evidence_status] = counts.get(e.evidence_status, 0) + 1
        return counts

    def __len__(self) -> int:
        return len(self._entries)

    # -------------------------------------------------------------------------
    # Comparative Research Datasets (Kumari et al. 2026 Integration)
    # -------------------------------------------------------------------------
    def get_comparative_word_list(self) -> List[Dict[str, Any]]:
        """Return all 254 entries from Appendix II (Table B.1) of Kumari et al. (2026)."""
        res_dir = Path(__file__).parent / "resources"
        data_dir = Path(__file__).parents[2] / "data"
        path = res_dir / "gaddi_word_list.json"
        if not path.exists():
            path = data_dir / "gaddi_word_list.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_numerals(self) -> Dict[str, Any]:
        """Return complete numeral dataset from Appendix III of Kumari et al. (2026)."""
        res_dir = Path(__file__).parent / "resources"
        data_dir = Path(__file__).parents[2] / "data"
        path = res_dir / "gaddi_numerals.json"
        if not path.exists():
            path = data_dir / "gaddi_numerals.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def search_comparative_word_list(self, query: str) -> List[Dict[str, Any]]:
        """Search the 254 Appendix II comparative word list by English gloss, Gaddi IPA, or serial number."""
        clean_q = normalize_text(query).lower()
        if not clean_q:
            return []
        results = []
        for item in self.get_comparative_word_list():
            gloss = normalize_text(item.get("english_gloss", "")).lower()
            ipa = normalize_text(item.get("gaddi_ipa", "")).lower()
            serial = str(item.get("serial_number", ""))
            tokens = [t.strip(",.()[]{}:;\"'") for t in gloss.split()]
            if clean_q == gloss or clean_q in tokens or clean_q in gloss:
                results.append(item)
            elif clean_q == ipa or clean_q in ipa:
                results.append(item)
            elif clean_q == serial:
                results.append(item)
        return results

    def search_numerals(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """Search numerals across cardinals, ordinals, fractionals, and distributives."""
        data = self.get_numerals()
        clean_q = normalize_text(query).lower()
        matched: Dict[str, List[Dict[str, Any]]] = {
            "cardinals": [],
            "ordinals": [],
            "fractionals": [],
            "distributives": [],
        }
        if not clean_q or not data:
            return matched

        for card in data.get("cardinals", []):
            c_val = str(card.get("value", ""))
            c_ipa = normalize_text(card.get("gaddi_ipa") or card.get("ipa", "")).lower()
            c_glo = normalize_text(card.get("gloss") or card.get("gloss_en", "")).lower()
            if clean_q == c_val or clean_q in c_ipa or clean_q in c_glo:
                matched["cardinals"].append(card)

        for ord_item in data.get("ordinals", []):
            o_rank = str(ord_item.get("rank") or ord_item.get("value", ""))
            o_m = normalize_text(ord_item.get("masculine", "")).lower()
            o_f = normalize_text(ord_item.get("feminine", "")).lower()
            o_ipa = normalize_text(ord_item.get("gaddi_ipa") or ord_item.get("ipa", "")).lower()
            o_glo = normalize_text(ord_item.get("gloss") or ord_item.get("gloss_en", "")).lower()
            if clean_q == o_rank or clean_q in o_m or clean_q in o_f or clean_q in o_ipa or clean_q in o_glo:
                matched["ordinals"].append(ord_item)

        for frac in data.get("fractionals", []):
            f_val = str(frac.get("fraction", ""))
            f_ipa = normalize_text(frac.get("gaddi_ipa") or frac.get("ipa", "")).lower()
            f_glo = normalize_text(frac.get("gloss") or frac.get("gloss_en", "")).lower()
            if clean_q == f_val or clean_q in f_ipa or clean_q in f_glo:
                matched["fractionals"].append(frac)

        for dist in data.get("distributives", []):
            d_val = str(dist.get("base_numeral") or dist.get("base_value", ""))
            d_ipa = normalize_text(dist.get("gaddi_ipa") or dist.get("ipa", "")).lower()
            d_glo = normalize_text(dist.get("gloss") or dist.get("gloss_en", "")).lower()
            if clean_q == d_val or clean_q in d_ipa or clean_q in d_glo:
                matched["distributives"].append(dist)

        return matched

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------
    def _is_jk_variety(self, variety_id: str) -> bool:
        v = self.varieties.get(variety_id)
        if v:
            return v.is_jk_variety
        return variety_id.startswith("jk_")

    def _sort_results(self, entries: List[LexicalEntry]) -> List[LexicalEntry]:
        """Sort results prioritizing J&K varieties first, then verified status."""
        def sort_key(e: LexicalEntry) -> tuple:
            is_jk = self._is_jk_variety(e.variety_id)
            is_verified = e.evidence_status == EvidenceStatus.VERIFIED_JK.value
            return (
                0 if is_jk else 1,
                0 if is_verified else 1,
                e.lemma_devanagari,
            )
        return sorted(entries, key=sort_key)
