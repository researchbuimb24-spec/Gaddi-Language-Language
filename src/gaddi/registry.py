"""Registries for controlled sources and geographical varieties."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from gaddi.models import Source, Variety


class VarietyRegistry:
    """Registry managing controlled geographic and dialectal varieties."""

    def __init__(self, varieties: Optional[List[Variety]] = None):
        self._varieties: Dict[str, Variety] = {}
        if varieties:
            for v in varieties:
                self.register(v)
        else:
            self._load_default_varieties()

    def _load_default_varieties(self) -> None:
        resource_path = Path(__file__).parent / "resources" / "varieties.json"
        if not resource_path.exists():
            # Fallback to repo data dir
            resource_path = Path(__file__).parents[2] / "data" / "varieties.json"

        if resource_path.exists():
            with open(resource_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self.register(Variety.from_dict(item))

    def register(self, variety: Variety) -> None:
        self._varieties[variety.id] = variety

    def get(self, variety_id: str) -> Optional[Variety]:
        return self._varieties.get(variety_id)

    def contains(self, variety_id: str) -> bool:
        return variety_id in self._varieties

    def list_all(self) -> List[Variety]:
        return list(self._varieties.values())

    def get_jk_varieties(self) -> List[Variety]:
        """Return all varieties specific to Jammu & Kashmir."""
        return [v for v in self._varieties.values() if v.is_jk_variety]

    def get_hp_varieties(self) -> List[Variety]:
        """Return all varieties specific to Himachal Pradesh."""
        return [v for v in self._varieties.values() if not v.is_jk_variety]

    def __len__(self) -> int:
        return len(self._varieties)


class SourceRegistry:
    """Registry managing bibliographic sources and citations."""

    def __init__(self, sources: Optional[List[Source]] = None):
        self._sources: Dict[str, Source] = {}
        if sources:
            for s in sources:
                self.register(s)
        else:
            self._load_default_sources()

    def _load_default_sources(self) -> None:
        resource_path = Path(__file__).parent / "resources" / "sources.json"
        if not resource_path.exists():
            resource_path = Path(__file__).parents[2] / "data" / "sources.json"

        if resource_path.exists():
            with open(resource_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self.register(Source.from_dict(item))

    def register(self, source: Source) -> None:
        self._sources[source.id] = source

    def get(self, source_id: str) -> Optional[Source]:
        return self._sources.get(source_id)

    def contains(self, source_id: str) -> bool:
        return source_id in self._sources

    def list_all(self) -> List[Source]:
        return list(self._sources.values())

    def get_jk_primary_sources(self) -> List[Source]:
        """Return sources directly documenting Gaddi in J&K."""
        return [s for s in self._sources.values() if s.is_jk_primary]

    def get_comparative_sources(self) -> List[Source]:
        """Return sources providing comparative baseline data (e.g. Kangra/Chamba)."""
        return [s for s in self._sources.values() if not s.is_jk_primary]

    def __len__(self) -> int:
        return len(self._sources)


# Global singleton instances for direct import
default_varieties = VarietyRegistry()
default_sources = SourceRegistry()

