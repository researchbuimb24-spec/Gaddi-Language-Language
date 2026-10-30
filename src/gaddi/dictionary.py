"""Searchable dictionary and multi-language translation engine for Gaddi."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from gaddi.models import LexicalEntry
from gaddi.registry import VarietyRegistry, default_varieties


def normalize_text(text: str) -> str:
    """Normalize text using Unicode NFC form and strip surrounding whitespace."""
    if not text:
        return ""
    return unicodedata.normalize("NFC", text).strip()


class GaddiDictionary:
    """In-memory searchable dictionary with multi-script and multi-language support."""

    def __init__(
        self,
        entries: Optional[List[LexicalEntry]] = None,
        variety_registry: Optional[VarietyRegistry] = None,
    ):
        self.varieties = variety_registry or default_varieties
        self._entries: List[LexicalEntry] = []
        self._id_index: Dict[str, LexicalEntry] = {}

        if entries:
            for entry in entries:
                self.add_entry(entry)

    def add_entry(self, entry: LexicalEntry) -> None:
        """Add a lexical entry to the dictionary and update internal indices."""
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
        return self._id_index.get(entry_id)

    # -------------------------------------------------------------------------
    # Priority 1: English -> Gaddi Lookup
    # -------------------------------------------------------------------------
    def lookup_english(
        self,
        query: str,
        jk_only: bool = False,
        exact: bool = False,
    ) -> List[LexicalEntry]:
        """Search English definitions and semantic glosses for matching Gaddi entries.

        Args:
            query: English search term or phrase.
            jk_only: If True, restricts results strictly to Jammu & Kashmir varieties.
            exact: If True, matches exact word/definition, else substring/token match.
        """
        clean_q = normalize_text(query).lower()
        if not clean_q:
            return []

        results: List[LexicalEntry] = []
        for entry in self._entries:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                defn = normalize_text(sense.definition_en).lower()
                if exact:
                    if clean_q == defn or clean_q in defn.split():
                        matched = True
                        break
                else:
                    if clean_q in defn:
                        matched = True
                        break

            if matched:
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
    ) -> List[LexicalEntry]:
        """Search Hindi definitions and glosses for matching Gaddi entries."""
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        results: List[LexicalEntry] = []
        for entry in self._entries:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                if not sense.definition_hi:
                    continue
                defn = normalize_text(sense.definition_hi)
                if exact:
                    if clean_q == defn or clean_q in defn.split():
                        matched = True
                        break
                else:
                    if clean_q in defn:
                        matched = True
                        break

            if matched:
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
    ) -> List[LexicalEntry]:
        """Search Urdu definitions and glosses for matching Gaddi entries."""
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        results: List[LexicalEntry] = []
        for entry in self._entries:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False
            for sense in entry.senses:
                if not sense.definition_ur:
                    continue
                defn = normalize_text(sense.definition_ur)
                if exact:
                    if clean_q == defn or clean_q in defn.split():
                        matched = True
                        break
                else:
                    if clean_q in defn:
                        matched = True
                        break

            if matched:
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Gaddi Headword Lookup (Multi-Script)
    # -------------------------------------------------------------------------
    def lookup_gaddi(
        self,
        query: str,
        jk_only: bool = False,
        script: Optional[str] = None,
    ) -> List[LexicalEntry]:
        """Look up Gaddi headwords across Devanagari, Perso-Arabic, Latin/IPA, and Takri.

        Args:
            query: Headword string in any supported script.
            jk_only: Restrict to J&K varieties.
            script: Optional filter ('deva', 'arab', 'latn', 'takr').
        """
        clean_q = normalize_text(query)
        clean_q_lower = clean_q.lower()
        if not clean_q:
            return []

        results: List[LexicalEntry] = []
        for entry in self._entries:
            if jk_only and not self._is_jk_variety(entry.variety_id):
                continue

            matched = False

            # Check Devanagari
            if (not script or script.lower() in ("deva", "devanagari")) and entry.lemma_devanagari:
                lemma = normalize_text(entry.lemma_devanagari)
                if clean_q == lemma or clean_q in lemma:
                    matched = True

            # Check Perso-Arabic
            if not matched and (not script or script.lower() in ("arab", "urdu", "arabic")) and entry.lemma_perso_arabic:
                lemma = normalize_text(entry.lemma_perso_arabic)
                if clean_q == lemma or clean_q in lemma:
                    matched = True

            # Check IPA / Latin
            if not matched and (not script or script.lower() in ("latn", "latin", "ipa")) and entry.lemma_ipa:
                lemma = normalize_text(entry.lemma_ipa).lower()
                if clean_q_lower == lemma or clean_q_lower in lemma:
                    matched = True

            # Check Attestation Source Spellings (Romanized / original source spellings)
            if not matched and (not script or script.lower() in ("latn", "latin")):
                for att in entry.attestations:
                    if att.source_spelling:
                        spelling = normalize_text(att.source_spelling).lower()
                        if clean_q_lower == spelling or clean_q_lower in spelling.split():
                            matched = True
                            break

            # Check Takri
            if not matched and (not script or script.lower() in ("takr", "takri")) and entry.lemma_takri:
                lemma = normalize_text(entry.lemma_takri)
                if clean_q == lemma or clean_q in lemma:
                    matched = True

            if matched:
                results.append(entry)

        return self._sort_results(results)

    # -------------------------------------------------------------------------
    # Universal Search
    # -------------------------------------------------------------------------
    def search(self, query: str, jk_only: bool = False) -> List[LexicalEntry]:
        """Universal multi-lingual and multi-script search across headwords and definitions."""
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        # Combine results from all search channels with deduplication
        seen: Set[str] = set()
        combined: List[LexicalEntry] = []

        for fn in (
            lambda: self.lookup_gaddi(clean_q, jk_only=jk_only),
            lambda: self.lookup_english(clean_q, jk_only=jk_only),
            lambda: self.lookup_hindi(clean_q, jk_only=jk_only),
            lambda: self.lookup_urdu(clean_q, jk_only=jk_only),
        ):
            for entry in fn():
                if entry.id not in seen:
                    seen.add(entry.id)
                    combined.append(entry)

        return self._sort_results(combined)

    # -------------------------------------------------------------------------
    # Filtering & Analytics
    # -------------------------------------------------------------------------
    def filter_by_variety(self, variety_id: str) -> List[LexicalEntry]:
        return [e for e in self._entries if e.variety_id == variety_id]

    def filter_by_pos(self, part_of_speech: str) -> List[LexicalEntry]:
        pos_clean = part_of_speech.lower().strip()
        return [e for e in self._entries if e.part_of_speech.lower() == pos_clean]

    def get_jk_entries(self) -> List[LexicalEntry]:
        return [e for e in self._entries if self._is_jk_variety(e.variety_id)]

    def get_comparative_entries(self) -> List[LexicalEntry]:
        return [e for e in self._entries if not self._is_jk_variety(e.variety_id)]

    def count_by_variety(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for e in self._entries:
            counts[e.variety_id] = counts.get(e.variety_id, 0) + 1
        return counts

    def count_by_status(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for e in self._entries:
            counts[e.status] = counts.get(e.status, 0) + 1
        return counts

    def __len__(self) -> int:
        return len(self._entries)

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
            is_verified = e.status == "verified"
            return (
                0 if is_jk else 1,          # J&K varieties first
                0 if is_verified else 1,    # Verified before provisional
                e.lemma_devanagari,
            )
        return sorted(entries, key=sort_key)
