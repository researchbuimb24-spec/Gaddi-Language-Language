"""Gaddi Cultural Knowledge Registry: Deities, Festivals, Cultural Practices, and Media Resources."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from gaddi.models import CulturalRecord, Deity, Festival, MediaResource


class CultureRegistry:
    """Registry and search service for Gaddi cultural, sacred, and ethnographic knowledge."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            repo_root = Path(__file__).resolve().parents[2]
            cand = repo_root / "data"
            if cand.exists():
                data_dir = cand
            else:
                data_dir = Path(__file__).resolve().parent / "resources"
        self.data_dir = data_dir

        self._deities: List[Deity] = []
        self._festivals: List[Festival] = []
        self._cultural_records: List[CulturalRecord] = []
        self._media_resources: List[MediaResource] = []
        self._load_datasets()

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        fpath = self.data_dir / filename
        if not fpath.exists():
            res_path = Path(__file__).resolve().parent / "resources" / filename
            if res_path.exists():
                fpath = res_path
            else:
                return []
        with open(fpath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_datasets(self) -> None:
        self._deities = [Deity.from_dict(d) for d in self._load_json("deities.json")]
        self._festivals = [Festival.from_dict(f) for f in self._load_json("festivals.json")]
        self._cultural_records = [CulturalRecord.from_dict(c) for c in self._load_json("culture.json")]
        self._media_resources = [MediaResource.from_dict(m) for m in self._load_json("media_resources.json")]

    def get_deities(self, category: Optional[str] = None) -> List[Deity]:
        """Return documented Gaddi deities and sacred figures."""
        if category:
            return [d for d in self._deities if d.category.lower() == category.lower()]
        return list(self._deities)

    def get_deity_by_id(self, deity_id: str) -> Optional[Deity]:
        """Lookup a deity by unique ID."""
        for d in self._deities:
            if d.id == deity_id:
                return d
        return None

    def get_festivals(self, season: Optional[str] = None) -> List[Festival]:
        """Return documented Gaddi festivals and ceremonies."""
        if season:
            return [f for f in self._festivals if season.lower() in f.timing_lunar_solar.lower()]
        return list(self._festivals)

    def get_festival_by_id(self, fest_id: str) -> Optional[Festival]:
        """Lookup a festival by unique ID."""
        for f in self._festivals:
            if f.id == fest_id:
                return f
        return None

    def get_cultural_records(self, topic: Optional[str] = None) -> List[CulturalRecord]:
        """Return documented cultural, pastoral, material, and social records."""
        if topic:
            return [c for c in self._cultural_records if c.topic.lower() == topic.lower()]
        return list(self._cultural_records)

    def get_cultural_record_by_id(self, record_id: str) -> Optional[CulturalRecord]:
        """Lookup a cultural record by ID."""
        for c in self._cultural_records:
            if c.id == record_id:
                return c
        return None

    def get_media_resource_by_id(self, resource_id: str) -> Optional[MediaResource]:
        """Lookup a media resource by ID."""
        for m in self._media_resources:
            if m.id == resource_id:
                return m
        return None

    def get_media_resources(self, media_type: Optional[str] = None) -> List[MediaResource]:
        """Return documented audio recordings, archival texts, and photographs."""
        if media_type:
            return [m for m in self._media_resources if m.media_type.lower() == media_type.lower()]
        return list(self._media_resources)

    def search_culture(self, query: str) -> Dict[str, List[Any]]:
        """Search across deities, festivals, cultural records, and media resources."""
        q = query.lower().strip()
        results: Dict[str, List[Any]] = {
            "deities": [],
            "festivals": [],
            "cultural_records": [],
            "media_resources": [],
        }
        if not q:
            return {
                "deities": list(self._deities),
                "festivals": list(self._festivals),
                "cultural_records": list(self._cultural_records),
                "media_resources": list(self._media_resources),
            }

        # Deities
        for d in self._deities:
            haystack = " ".join([
                d.name_devanagari,
                d.name_ipa or "",
                " ".join(d.alternate_names),
                d.description,
                d.ritual_roles,
                " ".join(d.associated_locations),
            ]).lower()
            if q in haystack:
                results["deities"].append(d)

        # Festivals
        for f in self._festivals:
            haystack = " ".join([
                f.name_devanagari,
                f.name_en,
                f.purpose_and_significance,
                f.timing_lunar_solar,
                " ".join(f.associated_rituals),
                " ".join(f.associated_deities),
            ]).lower()
            if q in haystack:
                results["festivals"].append(f)

        # Cultural records
        for c in self._cultural_records:
            haystack = " ".join([
                c.title,
                c.topic,
                c.term_devanagari or "",
                c.term_ipa or "",
                c.description,
            ]).lower()
            if q in haystack:
                results["cultural_records"].append(c)

        # Media resources
        for m in self._media_resources:
            haystack = " ".join([
                m.title,
                m.media_type,
                m.description,
                m.creator_or_collector,
                m.holding_institution,
            ]).lower()
            if q in haystack:
                results["media_resources"].append(m)

        return results

    def search_deities(self, query: str) -> List[Deity]:
        """Search deities matching query string."""
        return self.search_culture(query)["deities"]

    def search_festivals(self, query: str) -> List[Festival]:
        """Search festivals matching query string."""
        return self.search_culture(query)["festivals"]

    def search_cultural_records(self, query: str) -> List[CulturalRecord]:
        """Search cultural records matching query string."""
        return self.search_culture(query)["cultural_records"]


# Global singleton instance
default_culture = CultureRegistry()
