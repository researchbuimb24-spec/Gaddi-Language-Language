"""Command-line interface for the Gaddi Language Library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gaddi import __version__
from gaddi.dictionary import GaddiDictionary
from gaddi.grammar import GrammarRegistry
from gaddi.models import LexicalEntry
from gaddi.registry import default_sources, default_varieties
from gaddi.validator import GaddiValidator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gaddi",
        description="Gaddi Language Library: Computational documentation of Gaddi (Bharmauri) as spoken in Jammu & Kashmir.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Display library metadata and registered catalog summary.")

    # sources
    subparsers.add_parser("sources", help="List registered bibliographic sources and licenses.")

    # varieties
    subparsers.add_parser("varieties", help="List registered geographical and dialectal varieties.")

    # grammar
    subparsers.add_parser("grammar", help="Display documented grammatical paradigms and case markers.")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate a JSON dataset file for schema and provenance integrity.")
    validate_parser.add_argument("file", help="Path to JSON file containing lexical entries.")

    # search
    search_parser = subparsers.add_parser("search", help="Search dictionary across English, Hindi, Urdu, and Gaddi.")
    search_parser.add_argument("query", help="Word, phrase, or gloss to look up.")
    search_parser.add_argument("--jk-only", action="store_true", help="Restrict results strictly to J&K varieties.")
    search_parser.add_argument("--data", help="Optional path to custom JSON dictionary file.")

    return parser


def cmd_info() -> int:
    print(f"=== Gaddi Language Library v{__version__} ===")
    print("Dedicated to the Gaddi language as spoken in Jammu & Kashmir, India.")
    print(f"Registered Varieties: {len(default_varieties)} ({len(default_varieties.get_jk_varieties())} J&K, {len(default_varieties.get_hp_varieties())} HP/Comparative)")
    print(f"Registered Sources:   {len(default_sources)} ({len(default_sources.get_jk_primary_sources())} J&K Primary, {len(default_sources.get_comparative_sources())} Comparative/Historical)")
    print("\nTranslation Pipeline Priority:")
    print("  1. English -> Gaddi")
    print("  2. Hindi   -> Gaddi")
    print("  3. Urdu    -> Gaddi")
    print("  4. Other source languages (only when verified)")
    print("\nLinguistic Policy: Zero synthetic or invented words. 100% traceable provenance.")
    return 0


def cmd_sources() -> int:
    print("=== Registered Bibliographical Sources ===")
    for s in default_sources.list_all():
        jk_flag = "[J&K Primary]" if s.is_jk_primary else "[Comparative/HP]"
        print(f"\nID: {s.id} {jk_flag}")
        print(f"  Title:     {s.title} ({s.year})")
        print(f"  Authors:   {', '.join(s.authors)}")
        print(f"  Publisher: {s.publisher}")
        print(f"  License:   {s.license}")
        print(f"  Tier:      Tier {s.credibility_tier}")
        if s.notes:
            print(f"  Notes:     {s.notes}")
    return 0


def cmd_varieties() -> int:
    print("=== Controlled Geographical Varieties ===")
    jk_vars = default_varieties.get_jk_varieties()
    hp_vars = default_varieties.get_hp_varieties()

    print("\n-- Jammu & Kashmir Varieties --")
    for v in jk_vars:
        print(f"ID: {v.id}")
        print(f"  Name:     {v.name}")
        print(f"  District: {v.district}")
        print(f"  Areas:    {', '.join(v.sub_areas)}")
        print(f"  Contacts: {', '.join(v.contact_languages)}")

    print("\n-- Himachal Pradesh & Comparative Varieties --")
    for v in hp_vars:
        print(f"ID: {v.id}")
        print(f"  Name:     {v.name} ({v.state_ut})")
        print(f"  District: {v.district}")
        print(f"  Notes:    {v.description}")
    return 0


def cmd_grammar() -> int:
    print("=== Baseline Grammatical Paradigms (Documented) ===")
    print("\nCase Markers & Postpositions:")
    for cm in GrammarRegistry.get_baseline_case_markers():
        jk_att = "Yes" if cm.is_jk_attested else "Unverified in J&K"
        print(f"  {cm.case_name:22} : {cm.form_devanagari:8} /{cm.form_ipa:12}/ | J&K Attested: {jk_att}")
        print(f"    Citation: {cm.source_citation}")

    print("\nPersonal Pronouns:")
    for pr in GrammarRegistry.get_personal_pronouns():
        print(f"  {pr.person} {pr.number:8} : {pr.form_devanagari:6} /{pr.form_ipa:8}/ ({pr.case}) | Citation: {pr.source_citation}")
    return 0


def cmd_validate(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = [LexicalEntry.from_dict(d) for d in data]
    except Exception as e:
        print(f"Error reading JSON entries: {e}", file=sys.stderr)
        return 1

    validator = GaddiValidator(default_sources, default_varieties)
    report = validator.validate_collection(entries)

    print(f"Validated {report.total_checked} entries:")
    print(f"  Errors:   {len(report.errors)}")
    print(f"  Warnings: {len(report.warnings)}")

    if report.errors:
        print("\nBlocking Errors:")
        for err in report.errors:
            print(f"  [ERROR] Entry '{err.entry_id}' field '{err.field_name}': {err.message}")

    if report.warnings:
        print("\nAdvisory Warnings:")
        for warn in report.warnings:
            print(f"  [WARN]  Entry '{warn.entry_id}' field '{warn.field_name}': {warn.message}")

    return 0 if report.is_valid else 1


def cmd_search(query: str, jk_only: bool, data_path: Optional[str]) -> int:
    d = GaddiDictionary()
    if data_path:
        count = d.load_from_json(data_path)
        print(f"Loaded {count} entries from {data_path}.")
    else:
        print("Note: No dictionary data loaded. Use '--data <path>' to query an ingested corpus.")

    results = d.search(query, jk_only=jk_only)
    print(f"Search query: '{query}' (Results: {len(results)})")
    for r in results:
        print(f"\n[{r.variety_id}] {r.lemma_devanagari} ({r.part_of_speech})")
        if r.lemma_ipa:
            print(f"  IPA: /{r.lemma_ipa}/")
        if r.lemma_perso_arabic:
            print(f"  Urdu/Perso-Arabic: {r.lemma_perso_arabic}")
        for s in r.senses:
            print(f"  Sense {s.sense_index}:")
            print(f"    EN: {s.definition_en}")
            if s.definition_hi:
                print(f"    HI: {s.definition_hi}")
            if s.definition_ur:
                print(f"    UR: {s.definition_ur}")
    return 0


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "info":
        sys.exit(cmd_info())
    elif args.command == "sources":
        sys.exit(cmd_sources())
    elif args.command == "varieties":
        sys.exit(cmd_varieties())
    elif args.command == "grammar":
        sys.exit(cmd_grammar())
    elif args.command == "validate":
        sys.exit(cmd_validate(args.file))
    elif args.command == "search":
        sys.exit(cmd_search(args.query, args.jk_only, args.data))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

