"""Tests for Gaddi Verb Morphology, Grammatical Paradigms, and Provenance Integrity."""

import json
from pathlib import Path
import pytest

import gaddi
from gaddi.cli import cmd_morphology, cmd_validate
from gaddi.models import VerbFormRecord, VerbParadigm
from gaddi.morphology import VerbMorphologyRegistry, default_morphology
from gaddi.registry import default_sources, default_varieties
from gaddi.validator import GaddiValidator


class TestVerbMorphologyRegistry:
    """Test registry initialization, dataset loading, and stats."""

    def test_registry_loaded_and_counts(self):
        """Verify that the registry loads all 160 attested verb forms across 35 lemmas."""
        assert default_morphology.total_forms == 160
        assert default_morphology.total_verbs == 35

    def test_complete_canonical_paradigm_hasna(self):
        """Verify the 96-cell canonical paradigm of həsɳɑ from Mehta (2019) p. 941."""
        paradigm = default_morphology.get_paradigm("həsɳɑ")
        assert paradigm is not None
        assert paradigm.verb_lemma == "həsɳɑ"
        assert paradigm.is_complete is True
        assert len(paradigm.forms) == 96
        assert "mehta_2019" in paradigm.source_ids

        # Verify all 12 rows are present
        row_names = {f.metadata.get("paradigm_row") for f in paradigm.forms}
        expected_rows = {
            "PASTAUX", "PERFECT", "FUTURE", "IMPERATIVE", "EPISTEMIC",
            "INDICATIVEAUX", "IMPERFECTIVE", "PERFECTIVE", "PROG",
            "PROGAUX", "INCHO", "INCHOAUX"
        }
        assert row_names == expected_rows

        # Verify all 8 PNGH columns are present
        col_names = {f.metadata.get("paradigm_column") for f in paradigm.forms}
        expected_cols = {
            "M.SG", "F.SG", "M.SG.HON", "F.SG.HON",
            "M.PL", "F.PL", "M.PL.HON", "F.PL.HON"
        }
        assert col_names == expected_cols

        # Spot-check specific attested forms in the table
        m_sg_perf = next(f for f in paradigm.forms if f.metadata.get("paradigm_row") == "PERFECT" and f.metadata.get("paradigm_column") == "M.SG")
        assert m_sg_perf.inflected_form == "həsurɑ"
        assert m_sg_perf.morpheme_segmentation == "həs-ur-ɑ"

        f_sg_perf = next(f for f in paradigm.forms if f.metadata.get("paradigm_row") == "PERFECT" and f.metadata.get("paradigm_column") == "F.SG")
        assert f_sg_perf.inflected_form == "həsuri"

        m_sg_fut = next(f for f in paradigm.forms if f.metadata.get("paradigm_row") == "FUTURE" and f.metadata.get("paradigm_column") == "M.SG")
        assert m_sg_fut.inflected_form == "həsɳɑ"

        m_sg_pastaux = next(f for f in paradigm.forms if f.metadata.get("paradigm_row") == "PASTAUX" and f.metadata.get("paradigm_column") == "M.SG")
        assert m_sg_pastaux.inflected_form == "tʰu"

        f_sg_pastaux = next(f for f in paradigm.forms if f.metadata.get("paradigm_row") == "PASTAUX" and f.metadata.get("paradigm_column") == "F.SG")
        assert f_sg_pastaux.inflected_form == "tʰi"

    def test_missing_forms_remain_missing_zero_gap_fabrication(self):
        """Crucial requirement: Verify that missing forms are NEVER fabricated to fill paradigms.

        Verbs with isolated examples must remain incomplete (is_complete == False)
        and contain only their explicitly attested forms.
        """
        # kərɳɑ has only 1 attested isolated sentence example (kər-d-ɑ)
        kar_paradigm = default_morphology.get_paradigm("kərɳɑ")
        assert kar_paradigm is not None
        assert kar_paradigm.is_complete is False
        assert len(kar_paradigm.forms) == 1
        assert kar_paradigm.forms[0].inflected_form == "kər-d-ɑ"
        assert kar_paradigm.forms[0].paradigm_type == "isolated_attested_example"

        # bədʒɳɑ has only 2 causative forms in perfective aspect (bədʒ-ɑ-i, bədʒ-ʋɑ-i)
        badj_paradigm = default_morphology.get_paradigm("bədʒɳɑ")
        assert badj_paradigm is not None
        assert badj_paradigm.is_complete is False
        assert len(badj_paradigm.forms) == 2
        for f in badj_paradigm.forms:
            assert f.paradigm_type == "isolated_attested_example"

        # Check total complete paradigms in library: strictly 1 (həsɳɑ)
        complete_paradigms = default_morphology.get_complete_paradigms()
        assert len(complete_paradigms) == 1
        assert complete_paradigms[0].verb_lemma == "həsɳɑ"

    def test_causative_morphology_extraction(self):
        """Verify the 18 causative verbal forms from Kumari et al. (2026) Table 3.12."""
        caus_forms = [
            r for r in default_morphology._records
            if r.source_id == "kumari_2026" and r.form_type in ("causative_transitive", "causative_secondary")
        ]
        assert len(caus_forms) == 18

        # 9 transitive causatives and 9 secondary causatives
        trans = [f for f in caus_forms if f.form_type == "causative_transitive"]
        sec = [f for f in caus_forms if f.form_type == "causative_secondary"]
        assert len(trans) == 9
        assert len(sec) == 9

        # Spot-check specific attested pairs
        badj_tr = next(f for f in trans if f.verb_lemma == "bədʒɳɑ")
        badj_sec = next(f for f in sec if f.verb_lemma == "bədʒɳɑ")
        assert badj_tr.inflected_form == "bədʒ-ɑ-i"
        assert badj_sec.inflected_form == "bədʒ-ʋɑ-i"

        ghum_tr = next(f for f in trans if f.verb_lemma == "ɡʰumɳɑ")
        ghum_sec = next(f for f in sec if f.verb_lemma == "ɡʰumɳɑ")
        assert ghum_tr.inflected_form == "ɡʰum-ɑ-u"
        assert ghum_sec.inflected_form == "ɡʰum-ʋɑ-u"

    def test_negative_verb_constructions_extraction(self):
        """Verify the 15 clausal negative verb constructions from Kumari et al. (2026) Section 5.5.2."""
        neg_forms = [
            r for r in default_morphology._records
            if r.source_id == "kumari_2026" and r.form_type == "negative_construction"
        ]
        assert len(neg_forms) == 15

        forms_text = {f.inflected_form for f in neg_forms}
        assert "nɑ i-ɳ-ɑ" in forms_text
        assert "ni hɑ" in forms_text
        assert "nətʰi" in forms_text
        assert "mətʰ ɡətʃtʃʰ" in forms_text
        assert "nɑ ɡətʃʰ-ur-ɑ tʰ-u" in forms_text
        assert "ɡəcʰ-ur-ɑ nɑ tʰ-u" in forms_text
        assert "nɑ ɡən-d-ɑ" in forms_text
        assert "nɑ tʃəl-u kər-d-ɑ" in forms_text
        assert "nɑ ɡətʃʰ-i sək-d-ɑ" in forms_text
        assert "nɑ tʃʰəɖɖ-i ditʰ-ur-ɑ" in forms_text

    def test_filtering_by_tam_categories(self):
        """Test filtering by tense, aspect, and mood."""
        # Tense
        past_forms = default_morphology.filter_by_tense("past")
        assert len(past_forms) == 10
        fut_forms = default_morphology.filter_by_tense("future")
        assert len(fut_forms) == 15
        perf_forms = default_morphology.filter_by_tense("perfect")
        assert len(perf_forms) == 14

        # Aspect
        ipfv_forms = default_morphology.filter_by_aspect("imperfective")
        assert len(ipfv_forms) == 15
        pfv_forms = default_morphology.filter_by_aspect("perfective")
        assert len(pfv_forms) == 36
        prog_forms = default_morphology.filter_by_aspect("progressive")
        assert len(prog_forms) == 20
        incho_forms = default_morphology.filter_by_aspect("inchoative")
        assert len(incho_forms) == 21

        # Mood
        imp_forms = default_morphology.filter_by_mood("imperative")
        assert len(imp_forms) == 13
        em_forms = default_morphology.filter_by_mood("epistemic")
        assert len(em_forms) == 12
        ind_forms = default_morphology.filter_by_mood("indicative")
        assert len(ind_forms) == 10

    def test_search_forms(self):
        """Test searching forms across surface text, segmentation, and glosses."""
        res_prohibitive = default_morphology.search_forms("prohibitive")
        assert len(res_prohibitive) >= 1
        assert any(f.inflected_form == "mətʰ ɡətʃtʃʰ" for f in res_prohibitive)

        res_laugh = default_morphology.search_forms("həsurɑ")
        assert len(res_laugh) == 1
        assert res_laugh[0].verb_lemma == "həsɳɑ"

        res_dev = default_morphology.search_forms("हसणा")
        assert len(res_dev) == 96


class TestVerbMorphologyValidation:
    """Test validation engine rules and anti-fabrication enforcement."""

    def test_all_attested_records_pass_validation(self):
        """Verify that all 160 packaged verb morphology records pass validation with 0 errors."""
        validator = GaddiValidator(default_sources, default_varieties)
        report = validator.validate_verb_morphology_collection(default_morphology._records)
        assert report.is_valid is True
        assert len(report.errors) == 0

    def test_duplicate_id_triggers_validation_error(self):
        """Verify that duplicate record IDs are caught by the validator."""
        validator = GaddiValidator(default_sources, default_varieties)
        rec1 = default_morphology._records[0]
        # Duplicate rec1
        report = validator.validate_verb_morphology_collection([rec1, rec1])
        assert report.is_valid is False
        assert any(e.field_name == "id" and "Duplicate" in e.message for e in report.errors)

    def test_fabricated_complete_paradigm_triggers_error(self):
        """Verify that asserting a complete paradigm for an unverified verb triggers a validation error."""
        validator = GaddiValidator(default_sources, default_varieties)
        fake_rec = VerbFormRecord(
            id="fake_verb_perf_m_sg",
            verb_lemma="fake_verb",
            verb_meaning_en="to fake",
            paradigm_type="complete_paradigm_cell",  # Not allowed for non-həsɳɑ without documentation
            inflected_form="fake_form",
            source_id="mehta_2019",
            source_reference="Fabricated test",
            evidence_status="verified_field_attestation",
            dialect_variety="hp_kangra_palampur",
            collection_locality="Palampur",
            tense="past"
        )
        errors = validator.validate_verb_form(fake_rec)
        assert any("Fabricated complete paradigm detected" in e.message for e in errors)

    def test_invalid_grammatical_categories_trigger_error(self):
        """Verify that invalid tense or aspect strings trigger validation errors."""
        validator = GaddiValidator(default_sources, default_varieties)
        invalid_rec = VerbFormRecord(
            id="test_invalid_tense",
            verb_lemma="həsɳɑ",
            verb_meaning_en="to laugh",
            paradigm_type="isolated_attested_example",
            inflected_form="həs-x",
            source_id="mehta_2019",
            source_reference="Test",
            evidence_status="verified_field_attestation",
            dialect_variety="hp_kangra_palampur",
            collection_locality="Palampur",
            tense="past_anterior_imaginary"  # Invalid tense
        )
        errors = validator.validate_verb_form(invalid_rec)
        assert any(e.field_name == "tense" and "Invalid grammatical tense" in e.message for e in errors)


class TestVerbMorphologyProvenanceAndLicensing:
    """Test bibliographic provenance and licensing distinctions."""

    def test_mehta_2019_registered_and_cc_by_4(self):
        """Verify Mehta (2019) source metadata under CC BY 4.0."""
        source = default_sources.get("mehta_2019")
        assert source is not None
        assert "Shreya Mehta" in source.authors
        assert source.year == 2019
        assert source.license == "CC BY 4.0"
        assert "ijellh.com" in (source.url or "") or "Smart Moves Journal" in source.publisher

    def test_source_separation_kangra_only_not_jk(self):
        """Verify that all extracted forms are marked as Kangra variety, never falsely as J&K."""
        for rec in default_morphology._records:
            assert rec.dialect_variety == "hp_kangra_palampur"
            assert "Jammu" not in rec.collection_locality
            assert "Kashmir" not in rec.collection_locality


class TestVerbMorphologyCLI:
    """Test CLI commands for verb morphology."""

    def test_cli_verbs_command(self, capsys):
        """Test 'gaddi morphology verbs' output."""
        ret = cmd_morphology("verbs")
        assert ret == 0
        captured = capsys.readouterr()
        assert "Gaddi Verb Morphology: Recorded Verb Lemmas (35)" in captured.out
        assert "həsɳɑ" in captured.out
        assert "[COMPLETE PARADIGM]" in captured.out
        assert "bədʒɳɑ" in captured.out
        assert "[ISOLATED ATTESTED EXAMPLE]" in captured.out

    def test_cli_show_command(self, capsys):
        """Test 'gaddi morphology show həsɳɑ' output."""
        ret = cmd_morphology("show", lemma="həsɳɑ")
        assert ret == 0
        captured = capsys.readouterr()
        assert "=== Verb: həsɳɑ (to laugh) [COMPLETE CANONICAL PARADIGM] ===" in captured.out
        assert "Attested Forms: 96" in captured.out

    def test_cli_tense_command(self, capsys):
        """Test 'gaddi morphology tense past' output."""
        ret = cmd_morphology("tense", tense="past")
        assert ret == 0
        captured = capsys.readouterr()
        assert "Verb Forms Filtered by Tense: 'past'" in captured.out
        assert "tʰu" in captured.out

    def test_cli_mood_command(self, capsys):
        """Test 'gaddi morphology mood imperative' output."""
        ret = cmd_morphology("mood", mood="imperative")
        assert ret == 0
        captured = capsys.readouterr()
        assert "Verb Forms Filtered by Mood: 'imperative'" in captured.out
        assert "həsɑ" in captured.out

    def test_cli_search_command(self, capsys):
        """Test 'gaddi morphology search' output."""
        ret = cmd_morphology("search", query="prohibitive")
        assert ret == 0
        captured = capsys.readouterr()
        assert "prohibitive" in captured.out
        assert "mətʰ ɡətʃtʃʰ" in captured.out
