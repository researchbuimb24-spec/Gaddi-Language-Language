"""Gaddi Oral Heritage Registry: Stories, Songs, Proverbs, and Oral History."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from gaddi.models import OralTradition


class OralHeritageRegistry:
    """Registry and search service for Gaddi oral traditions."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # Look in data/ first, fallback to package resources
            repo_root = Path(__file__).resolve().parents[2]
            cand = repo_root / "data"
            if cand.exists():
                data_dir = cand
            else:
                data_dir = Path(__file__).resolve().parent / "resources"
        self.data_dir = data_dir

        self._stories: List[OralTradition] = []
        self._songs: List[OralTradition] = []
        self._proverbs: List[OralTradition] = []
        self._oral_history: List[OralTradition] = []
        self._load_datasets()

    def _load_file(self, filename: str) -> List[OralTradition]:
        fpath = self.data_dir / filename
        if not fpath.exists():
            res_path = Path(__file__).resolve().parent / "resources" / filename
            if res_path.exists():
                fpath = res_path
            else:
                return []
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [OralTradition.from_dict(item) for item in data]

    def _load_datasets(self) -> None:
        self._stories = self._load_file("stories.json")
        self._songs = self._load_file("songs.json")
        self._proverbs = self._load_file("proverbs.json")
        self._oral_history = self._load_file("oral_history.json")

    def get_stories(self, genre: Optional[str] = None, variety_id: Optional[str] = None) -> List[OralTradition]:
        """Return list of documented Gaddi stories and legends."""
        results = self._stories
        if genre:
            results = [s for s in results if s.genre.lower() == genre.lower()]
        if variety_id:
            results = [s for s in results if s.variety_id == variety_id]
        return results

    def get_songs(self, genre: Optional[str] = None, variety_id: Optional[str] = None) -> List[OralTradition]:
        """Return list of documented Gaddi songs and musical traditions."""
        results = self._songs
        if genre:
            results = [s for s in results if s.genre.lower() == genre.lower()]
        if variety_id:
            results = [s for s in results if s.variety_id == variety_id]
        return results

    def get_proverbs(self) -> List[OralTradition]:
        """Return list of documented Gaddi proverbs and sayings."""
        return list(self._proverbs)

    def get_oral_history(self) -> List[OralTradition]:
        """Return list of documented oral history testimonies."""
        return list(self._oral_history)

    def get_all(self) -> List[OralTradition]:
        """Return all oral heritage items across all categories."""
        return self._stories + self._songs + self._proverbs + self._oral_history

    def get_by_id(self, item_id: str) -> Optional[OralTradition]:
        """Lookup an oral tradition item by unique ID."""
        for item in self.get_all():
            if item.id == item_id:
                return item
        return None

    def search(self, query: str, genre: Optional[str] = None) -> List[OralTradition]:
        """Search across titles, summaries, excerpts, and performers."""
        q = query.lower().strip()
        if not q:
            return self.get_all()

        results = []
        for item in self.get_all():
            if genre and item.genre.lower() != genre.lower():
                continue
            haystack = " ".join([
                item.title_en,
                item.title_gaddi or "",
                item.summary_en,
                item.community_locality,
                item.performer_or_collector,
                item.text_excerpt_gaddi or "",
                item.text_excerpt_en or "",
            ]).lower()
            if q in haystack:
                results.append(item)
        return results


# Global singleton instance
default_oral_heritage = OralHeritageRegistry()
