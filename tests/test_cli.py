"""Tests for the command-line interface of the gaddi library."""

import json
from pathlib import Path
import pytest

from gaddi.cli import (
    build_parser,
    cmd_export,
    cmd_grammar,
    cmd_info,
    cmd_search,
    cmd_sources,
    cmd_translate,
    cmd_validate,
    cmd_varieties,
)


def test_cli_parser_build():
    parser = build_parser()
    assert parser.prog == "gaddi"

    # Test argument parsing
    args_info = parser.parse_args(["info"])
    assert args_info.command == "info"

    args_trans = parser.parse_args(["translate", "handloom", "--from", "en", "--include-comparative"])
    assert args_trans.command == "translate"
    assert args_trans.query == "handloom"
    assert args_trans.from_lang == "en"
    assert args_trans.include_comparative is True

    args_export = parser.parse_args(["export", "--format", "csv", "--jk-only"])
    assert args_export.format == "csv"
    assert args_export.jk_only is True


def test_cli_cmd_info(capsys):
    ret = cmd_info()
    assert ret == 0
    captured = capsys.readouterr()
    assert "Gaddi Language Library" in captured.out
    assert "Verified J&K Lexical Entries" in captured.out
    assert "J&K Cultural & Ecological Terms" in captured.out
    assert "Comparative HP Baseline" in captured.out


def test_cli_cmd_sources(capsys):
    # All sources
    ret = cmd_sources(jk_only=False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Registered Bibliographical Sources" in captured.out
    assert "kumari_2026" in captured.out
    assert "kumar_2019" in captured.out

    # J&K primary only
    ret_jk = cmd_sources(jk_only=True)
    assert ret_jk == 0
    captured_jk = capsys.readouterr()
    assert "Registered J&K Primary Sources" in captured_jk.out
    assert "kumar_2019" in captured_jk.out
    assert "kumari_2026" not in captured_jk.out


def test_cli_cmd_varieties(capsys):
    # All varieties
    ret = cmd_varieties(jk_only=False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Jammu & Kashmir Varieties" in captured.out
    assert "Himachal Pradesh & Comparative Varieties" in captured.out

    # J&K only
    ret_jk = cmd_varieties(jk_only=True)
    assert ret_jk == 0
    captured_jk = capsys.readouterr()
    assert "Controlled Jammu & Kashmir Varieties" in captured_jk.out
    assert "jk_kathua_bani" in captured_jk.out
    assert "hp_kangra_palampur" not in captured_jk.out


def test_cli_cmd_grammar(capsys):
    # Text output
    ret = cmd_grammar(as_json=False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Documented Grammatical Overview" in captured.out
    assert "Case Markers & Postpositions" in captured.out

    # JSON output
    ret_json = cmd_grammar(as_json=True)
    assert ret_json == 0
    captured_json = capsys.readouterr()
    data = json.loads(captured_json.out)
    assert "case_markers" in data
    assert "personal_pronouns" in data


def test_cli_cmd_validate_defaults(capsys):
    ret = cmd_validate(file_path=None)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Validation Report for: lexicon_jk.json [PASSED]" in captured.out
    assert "Validation Report for: cultural_terms_jk.json [PASSED]" in captured.out
    assert "Validation Report for: lexicon_comparative.json [PASSED]" in captured.out


def test_cli_cmd_search(capsys):
    ret = cmd_search("handloom", jk_only=False, no_comparative=False, data_path=None)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Search Query: 'handloom'" in captured.out
    assert "खडे" in captured.out


def test_cli_cmd_translate(capsys):
    # Strict J&K translation without flags -> should return no verified J&K lexical item
    ret_strict = cmd_translate("handloom", from_lang="en", include_comparative=False, include_cultural=False, data_path=None)
    assert ret_strict == 0
    captured_strict = capsys.readouterr()
    assert "No verified J&K Gaddi linguistic translation found" in captured_strict.out

    # Translation with --include-cultural flag -> surfaces cultural term
    ret_cult = cmd_translate("handloom", from_lang="en", include_comparative=False, include_cultural=True, data_path=None)
    assert ret_cult == 0
    captured_cult = capsys.readouterr()
    assert "Found 2 translation result(s)" in captured_cult.out
    assert "खडे" in captured_cult.out
    assert "JK_CULTURAL_TERM" in captured_cult.out

    # Comparative only query without flag -> should report no verified J&K
    ret_comp_no = cmd_translate("water", from_lang="en", include_comparative=False, include_cultural=False, data_path=None)
    assert ret_comp_no == 0
    captured_comp_no = capsys.readouterr()
    assert "No verified J&K Gaddi linguistic translation found" in captured_comp_no.out

    # Comparative only query with flag -> should return comparative result
    ret_comp_yes = cmd_translate("water", from_lang="en", include_comparative=True, include_cultural=False, data_path=None)
    assert ret_comp_yes == 0
    captured_comp_yes = capsys.readouterr()
    assert "Found 1 translation result(s)" in captured_comp_yes.out
    assert "पाणी" in captured_comp_yes.out


def test_cli_cmd_export(tmp_path, capsys):
    # Test JSON export to file
    out_json = tmp_path / "export.json"
    ret = cmd_export(output_path=str(out_json), format_type="json", jk_only=True)
    assert ret == 0
    assert out_json.exists()
    with open(out_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 130

    # Test CSV export to file
    out_csv = tmp_path / "export.csv"
    ret_csv = cmd_export(output_path=str(out_csv), format_type="csv", jk_only=False)
    assert ret_csv == 0
    assert out_csv.exists()
    content = out_csv.read_text(encoding="utf-8")
    assert "lemma_devanagari" in content
    assert "नवाला" in content

