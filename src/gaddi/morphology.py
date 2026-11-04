"""Gaddi Verb Morphology & Grammatical Paradigms Registry.

Provides structured access to source-backed Gaddi verbal inflectional paradigms,
tense-aspect-mood (TAM) realizations, agreement morphology (PNGH), causatives,
and clausal negative verb constructions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from gaddi.models import VerbFormRecord, VerbParadigm


class VerbMorphologyRegistry:
    """Registry and query service for Gaddi verb morphology and paradigms."""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            # Look in repository data/ first, fallback to package resources/
            repo_root = Path(__file__).resolve().parents[2]
            cand = repo_root / "data" / "verb_paradigms.json"
            if cand.exists():
                data_path = cand
            else:
                data_path = Path(__file__).resolve().parent / "resources" / "verb_paradigms.json"
        self.data_path = data_path

        self._records: List[VerbFormRecord] = []
        self._by_id: Dict[str, VerbFormRecord] = {}
        self._by_lemma: Dict[str, List[VerbFormRecord]] = {}
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load verb morphology records from JSON file."""
        if not self.data_path or not self.data_path.exists():
            res_path = Path(__file__).resolve().parent / "resources" / "verb_paradigms.json"
            if res_path.exists():
                self.data_path = res_path
            else:
                return

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        for item in raw_data:
            rec = VerbFormRecord.from_dict(item)
            self._records.append(rec)
            self._by_id[rec.id] = rec

            # Normalize lemma keys for lookup
            norm_lemma = rec.verb_lemma.strip().lower()
            if norm_lemma not in self._by_lemma:
                self._by_lemma[norm_lemma] = []
            self._by_lemma[norm_lemma].append(rec)

            if rec.verb_lemma_devanagari:
                norm_dev = rec.verb_lemma_devanagari.strip()
                if norm_dev not in self._by_lemma:
                    self._by_lemma[norm_dev] = []
                self._by_lemma[norm_dev].append(rec)

    @property
    def total_forms(self) -> int:
        """Total number of inflected verbal form records."""
        return len(self._records)

    @property
    def total_verbs(self) -> int:
        """Total number of unique verb lemmas."""
        unique_lemmas = {r.verb_lemma for r in self._records}
        return len(unique_lemmas)

    def list_verbs(self) -> List[Dict[str, Any]]:
        """Return a structured summary list of all verbs in the registry."""
        lemmas_seen: Set[str] = set()
        result: List[Dict[str, Any]] = []

        for rec in self._records:
            if rec.verb_lemma in lemmas_seen:
                continue
            lemmas_seen.add(rec.verb_lemma)
            forms = [r for r in self._records if r.verb_lemma == rec.verb_lemma]
            has_complete = any(r.paradigm_type == "complete_paradigm_cell" for r in forms)
            sources = sorted(list({r.source_id for r in forms}))
            tenses = sorted(list({r.tense for r in forms if r.tense}))
            aspects = sorted(list({r.aspect for r in forms if r.aspect}))
            moods = sorted(list({r.mood for r in forms if r.mood}))

            result.append({
                "verb_lemma": rec.verb_lemma,
                "verb_lemma_devanagari": rec.verb_lemma_devanagari,
                "verb_meaning_en": rec.verb_meaning_en,
                "form_count": len(forms),
                "is_complete_paradigm": has_complete,
                "paradigm_type": "complete_paradigm" if has_complete else "isolated_attested_examples",
                "sources": sources,
                "tenses": tenses,
                "aspects": aspects,
                "moods": moods,
            })

        return sorted(result, key=lambda x: (not x["is_complete_paradigm"], x["verb_lemma"]))

    def get_verb(self, lemma: str) -> List[VerbFormRecord]:
        """Retrieve all recorded verbal forms for a given lemma.

        Does NOT invent missing paradigm cells; missing forms remain missing.
        """
        key = lemma.strip().lower()
        if key in self._by_lemma:
            # Deduplicate by ID
            seen_ids: Set[str] = set()
            forms: List[VerbFormRecord] = []
            for r in self._by_lemma[key]:
                if r.id not in seen_ids:
                    seen_ids.add(r.id)
                    forms.append(r)
            return forms

        # Partial fallback matching
        matches: List[VerbFormRecord] = []
        seen_ids = set()
        for rec in self._records:
            if key == rec.verb_lemma.lower() or (rec.verb_lemma_devanagari and key == rec.verb_lemma_devanagari):
                if rec.id not in seen_ids:
                    seen_ids.add(rec.id)
                    matches.append(rec)
        return matches

    def get_paradigm(self, lemma: str) -> Optional[VerbParadigm]:
        """Return a structured VerbParadigm grouping for a lemma.

        Clearly marks whether the paradigm is complete or consists of isolated attested forms.
        """
        forms = self.get_verb(lemma)
        if not forms:
            return None

        is_complete = any(f.paradigm_type == "complete_paradigm_cell" for f in forms)
        meaning = forms[0].verb_meaning_en
        devanagari = forms[0].verb_lemma_devanagari
        sources = sorted(list({f.source_id for f in forms}))
        notes = "Complete canonical inflectional paradigm" if is_complete else "Isolated attested examples only; complete paradigm not attested."

        return VerbParadigm(
            verb_lemma=forms[0].verb_lemma,
            verb_lemma_devanagari=devanagari,
            verb_meaning_en=meaning,
            forms=forms,
            is_complete=is_complete,
            source_ids=sources,
            notes=notes,
        )

    def search_forms(self, query: str) -> List[VerbFormRecord]:
        """Search across forms, transcription, gloss, meaning, and sentences."""
        q = query.strip().lower()
        if not q:
            return []

        results: List[VerbFormRecord] = []
        for rec in self._records:
            targets = [
                rec.inflected_form.lower(),
                rec.verb_lemma.lower(),
                rec.verb_meaning_en.lower(),
                rec.ipa_transcription.lower() if rec.ipa_transcription else "",
                rec.verb_lemma_devanagari or "",
                rec.form_devanagari or "",
                rec.interlinear_gloss.lower() if rec.interlinear_gloss else "",
                rec.morpheme_segmentation.lower() if rec.morpheme_segmentation else "",
                rec.english_translation.lower() if rec.english_translation else "",
                rec.metadata.get("example_sentence_gaddi", "").lower(),
            ]
            if any(q in t for t in targets):
                results.append(rec)
        return results

    def filter_by_tense(self, tense: str) -> List[VerbFormRecord]:
        """Filter forms by grammatical tense (past, future, perfect, present)."""
        t = tense.strip().lower()
        return [r for r in self._records if r.tense and r.tense.lower() == t]

    def filter_by_aspect(self, aspect: str) -> List[VerbFormRecord]:
        """Filter forms by grammatical aspect (imperfective, perfective, progressive, inchoative)."""
        a = aspect.strip().lower()
        return [r for r in self._records if r.aspect and r.aspect.lower() == a]

    def filter_by_mood(self, mood: str) -> List[VerbFormRecord]:
        """Filter forms by grammatical mood (indicative, epistemic, imperative)."""
        m = mood.strip().lower()
        return [r for r in self._records if r.mood and r.mood.lower() == m]

    def filter_by_variety(self, variety: str) -> List[VerbFormRecord]:
        """Filter forms by dialect variety ID."""
        v = variety.strip().lower()
        return [r for r in self._records if r.dialect_variety.lower() == v]

    def filter_by_source(self, source_id: str) -> List[VerbFormRecord]:
        """Filter forms by source ID."""
        s = source_id.strip().lower()
        return [r for r in self._records if r.source_id.lower() == s]

    def filter_by_paradigm_type(self, paradigm_type: str) -> List[VerbFormRecord]:
        """Filter by 'complete_paradigm_cell' or 'isolated_attested_example'."""
        pt = paradigm_type.strip().lower()
        return [r for r in self._records if r.paradigm_type.lower() == pt]

    def get_form_by_id(self, record_id: str) -> Optional[VerbFormRecord]:
        """Retrieve a specific form by its unique record ID."""
        return self._by_id.get(record_id.strip())

    def get_complete_paradigms(self) -> List[VerbParadigm]:
        """Return all complete paradigms in the registry."""
        complete_lemmas = {
            r.verb_lemma for r in self._records if r.paradigm_type == "complete_paradigm_cell"
        }
        res: List[VerbParadigm] = []
        for lem in sorted(list(complete_lemmas)):
            p = self.get_paradigm(lem)
            if p and p.is_complete:
                res.append(p)
        return res

    def get_isolated_examples(self) -> List[VerbFormRecord]:
        """Return all forms categorized as isolated attested examples."""
        return [r for r in self._records if r.paradigm_type == "isolated_attested_example"]


# Global default instance
default_morphology = VerbMorphologyRegistry()


def get_verb_morphology_registry() -> VerbMorphologyRegistry:
    """Return the global VerbMorphologyRegistry singleton."""
    return default_morphology
