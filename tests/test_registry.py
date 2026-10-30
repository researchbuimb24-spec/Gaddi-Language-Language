"""Tests for controlled source and variety registries."""

from gaddi.registry import default_sources, default_varieties


def test_variety_registry_defaults():
    assert len(default_varieties) >= 7

    # Check J&K varieties
    jk_varieties = default_varieties.get_jk_varieties()
    assert len(jk_varieties) >= 4
    jk_ids = {v.id for v in jk_varieties}
    assert "jk_kathua_bani" in jk_ids
    assert "jk_udhampur_ramnagar" in jk_ids
    assert "jk_doda_bhadarwah" in jk_ids
    assert "jk_general" in jk_ids

    # Check HP varieties
    hp_varieties = default_varieties.get_hp_varieties()
    hp_ids = {v.id for v in hp_varieties}
    assert "hp_chamba_bharmaur" in hp_ids
    assert "hp_kangra_palampur" in hp_ids


def test_source_registry_defaults():
    assert len(default_sources) >= 10

    # Check Kumari et al. 2026 registration
    kumari = default_sources.get("kumari_2026")
    assert kumari is not None
    assert kumari.year == 2026
    assert kumari.publisher == "UCL Press"
    assert kumari.credibility_tier == 1
    assert kumari.is_jk_primary is False
    assert "CC BY 4.0" in kumari.license

    # Check Grierson 1916 registration
    grierson = default_sources.get("grierson_1916")
    assert grierson is not None
    assert grierson.license == "Public Domain"

    # Check J&K primary sources
    jk_sources = default_sources.get_jk_primary_sources()
    assert len(jk_sources) >= 5
    jk_source_ids = {s.id for s in jk_sources}
    assert "census_2011" in jk_source_ids
    assert "kumar_2019" in jk_source_ids
    assert "chandar_2024" in jk_source_ids
    assert "chakraborty_2024" in jk_source_ids

