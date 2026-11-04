"""Command-line interface for the Gaddi Language Library."""

from __future__ import annotations

from gaddi.morphology import default_morphology
from gaddi.models import VerbFormRecord

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Optional

from gaddi import __version__
from gaddi.dictionary import GaddiDictionary
from gaddi.grammar import GrammarRegistry
from gaddi.models import EvidenceStatus, LexicalEntry
from gaddi.registry import default_leads, default_sources, default_varieties
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
    subparsers.add_parser("info", help="Display library metadata, entry counts, and catalog summary.")

    # sources
    sources_parser = subparsers.add_parser("sources", help="List registered bibliographic sources and licenses.")
    sources_parser.add_argument("--jk-only", action="store_true", help="List only J&K primary sources.")

    # leads
    leads_parser = subparsers.add_parser("leads", help="List investigated primary linguistic sources and research leads.")
    leads_parser.add_argument("--linguistic-only", action="store_true", help="Filter leads to only those containing linguistic data.")
    leads_parser.add_argument("--status", help="Filter leads by specific status.")

    # varieties
    varieties_parser = subparsers.add_parser("varieties", help="List registered geographical and dialectal varieties.")
    varieties_parser.add_argument("--jk-only", action="store_true", help="List only J&K varieties.")

    # grammar
    grammar_parser = subparsers.add_parser("grammar", help="Display documented grammatical paradigms and case markers.")
    grammar_parser.add_argument("--json", action="store_true", help="Output grammar overview in JSON format.")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate a JSON dataset file for schema and provenance integrity.")
    validate_parser.add_argument("file", nargs="?", default=None, help="Path to JSON file containing lexical entries (defaults to bundled datasets).")

    # search
    search_parser = subparsers.add_parser("search", help="Search dictionary across English, Hindi, Urdu, and Gaddi scripts.")
    search_parser.add_argument("query", help="Word, phrase, or gloss to look up.")
    search_parser.add_argument("--jk-only", action="store_true", help="Restrict results strictly to J&K varieties.")
    search_parser.add_argument("--no-comparative", action="store_true", help="Exclude comparative HP entries.")
    search_parser.add_argument("--data", help="Optional path to custom JSON dictionary file.")

    # translate
    translate_parser = subparsers.add_parser("translate", help="Translate between English, Hindi, Urdu, Punjabi, Dogri, and Gaddi.")
    translate_parser.add_argument("query", help="Source word to translate.")
    translate_parser.add_argument(
        "--from",
        dest="from_lang",
        default="en",
        choices=["en", "hi", "ur", "pa", "doi", "as", "bn", "gaddi"],
        help="Source language of the query (en: English [default], hi: Hindi, ur: Urdu, pa: Punjabi, doi: Dogri, as: Assamese, bn: Bengali, gaddi).",
    )
    translate_parser.add_argument(
        "--to",
        dest="to_lang",
        default=None,
        choices=["gaddi", "en", "hi", "ur", "pa", "doi", "as", "bn"],
        help="Target language (default: gaddi).",
    )
    translate_parser.add_argument(
        "--include-cultural",
        action="store_true",
        help="Include documented J&K cultural, ritual, and regional ecological terms.",
    )
    translate_parser.add_argument(
        "--include-comparative",
        action="store_true",
        help="Include comparative Himachal Pradesh baseline data if no J&K translation is attested.",
    )
    translate_parser.add_argument("--data", help="Optional path to custom JSON dictionary file.")

    # export
    export_parser = subparsers.add_parser("export", help="Export dictionary entries to JSON or CSV format.")
    export_parser.add_argument("--output", "-o", help="File path to write output. If omitted, prints to stdout.")
    export_parser.add_argument(
        "--format",
        "-f",
        default="json",
        choices=["json", "csv"],
        help="Export format (json [default] or csv).",
    )
    export_parser.add_argument("--jk-only", action="store_true", help="Export only verified J&K entries.")

    # word-list (Appendix II)
    wl_parser = subparsers.add_parser("word-list", aliases=["words", "comparative-words"], help="Browse/search 254 basic word list items or filter by topic category.")
    wl_parser.add_argument("--category", "-c", help="Filter vocabulary by standardized category (e.g. animals, family, food).")
    wl_parser.add_argument("--search", "-s", help="Search word list by English gloss, IPA, or serial number.")
    wl_parser.add_argument("--pos", help="Filter by part of speech.")
    wl_parser.add_argument("--limit", type=int, default=25, help="Number of entries to display (default: 25).")
    wl_parser.add_argument("--all", action="store_true", help="Display all matching entries without truncation.")
    wl_parser.add_argument("--json", action="store_true", help="Output entries in JSON format.")

    # numerals (Appendix III)
    num_parser = subparsers.add_parser("numerals", help="Browse/search numerals from Kumari et al. (2026) Appendix III.")
    num_parser.add_argument("--category", "-c", choices=["all", "cardinals", "ordinals", "fractionals", "distributives"], default="all", help="Category of numerals to display.")
    num_parser.add_argument("--search", "-s", help="Search numerals by value, gloss, or IPA.")
    num_parser.add_argument("--json", action="store_true", help="Output numerals in JSON format.")

    # phonology (Chapter 2 & Appendix I)
    phon_parser = subparsers.add_parser("phonology", help="Display phonological inventories and sound rules from Kumari et al. (2026).")
    phon_parser.add_argument("--section", "-s", choices=["all", "vowels", "consonants", "phonotactics", "processes", "discrepancies"], default="all", help="Phonology section to display.")
    phon_parser.add_argument("--json", action="store_true", help="Output phonology in JSON format.")

    # examples (Numbered examples 1 to 269)
    ex_parser = subparsers.add_parser("examples", help="Browse/search 269 numbered linguistic examples from Kumari et al. (2026).")
    ex_parser.add_argument("--chapter", "-c", type=int, choices=[1, 2, 3, 4, 5], help="Filter examples by chapter.")
    ex_parser.add_argument("--number", "-n", type=int, help="Fetch a specific numbered example (1 to 269).")
    ex_parser.add_argument("--search", "-s", help="Search example text or translations.")
    ex_parser.add_argument("--headword", "-w", help="Retrieve examples explicitly associated with a Gaddi headword.")
    ex_parser.add_argument("--limit", type=int, default=5, help="Number of examples to display (default: 5).")
    ex_parser.add_argument("--json", action="store_true", help="Output examples in JSON format.")

    # sociolinguistics (Chapter 1)
    soc_parser = subparsers.add_parser("sociolinguistics", help="Display sociolinguistic and ethnographic notes from Kumari et al. (2026).")
    soc_parser.add_argument("--section", "-s", choices=["all", "community", "vitality", "fieldwork"], default="all", help="Sociolinguistic section to display.")
    soc_parser.add_argument("--json", action="store_true", help="Output sociolinguistics in JSON format.")

    # references (Bibliography & Index)
    ref_parser = subparsers.add_parser("references", help="Display bibliography and citations from Kumari et al. (2026).")
    ref_parser.add_argument("--search", "-s", help="Search citations by author, year, or title.")
    ref_parser.add_argument("--json", action="store_true", help="Output references in JSON format.")

    # compare
    compare_parser = subparsers.add_parser("compare", aliases=["compare-varieties"], help="Compare a headword across registered varieties, segregating J&K from HP evidence.")
    compare_parser.add_argument("headword", help="Headword or term to compare across varieties.")

    # stories
    stories_parser = subparsers.add_parser("stories", help="List and search documented Gaddi folk tales and legends.")
    stories_parser.add_argument("--genre", help="Filter stories by genre (folktale, pastoral_narrative, legend).")
    stories_parser.add_argument("--search", help="Search text in stories.")
    stories_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # songs
    songs_parser = subparsers.add_parser("songs", help="List and search documented Gaddi folk songs and Ainchali ballads.")
    songs_parser.add_argument("--genre", help="Filter songs by genre (ainchali_ballad, love_ballad, wedding_song).")
    songs_parser.add_argument("--search", help="Search text in songs.")
    songs_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # proverbs
    proverbs_parser = subparsers.add_parser("proverbs", help="List and search documented Gaddi pastoral proverbs and sayings.")
    proverbs_parser.add_argument("--search", help="Search text in proverbs.")
    proverbs_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # deities
    deities_parser = subparsers.add_parser("deities", help="List and search documented Gaddi deities and sacred traditions.")
    deities_parser.add_argument("--category", help="Filter deities by category (supreme_deity, shepherd_protector, etc.).")
    deities_parser.add_argument("--search", help="Search deities.")
    deities_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # festivals
    festivals_parser = subparsers.add_parser("festivals", help="List and search documented Gaddi traditional festivals and ceremonies.")
    festivals_parser.add_argument("--season", help="Filter festivals by season.")
    festivals_parser.add_argument("--search", help="Search festivals.")
    festivals_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # culture
    culture_parser = subparsers.add_parser("culture", help="Display documented cultural practices, attire, and traditions.")
    culture_parser.add_argument("--topic", help="Filter by topic (pastoral_migration, clothing_and_attire, etc.).")
    culture_parser.add_argument("--search", help="Search culture records.")
    culture_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # vocabulary
    vocab_parser = subparsers.add_parser("vocabulary", help="Browse and search research-expanded vocabulary across 16 domains.")
    vocab_parser.add_argument("--domain", help="Filter by semantic domain (family_and_kinship, pastoral_life, etc.).")
    vocab_parser.add_argument("--search", help="Search vocabulary entries.")
    vocab_parser.add_argument("--json", action="store_true", help="Output in JSON format.")

    # dictionary (Expansion 3: Research-Expanded Multilingual Lexicon)
    dict_parser = subparsers.add_parser("dictionary", help="Browse and search research-expanded multilingual dictionary entries.")
    dict_parser.add_argument("--domain", "-d", help="Filter by semantic domain (e.g. nature_and_physical_world, body_parts, family_and_kinship).")
    dict_parser.add_argument("--variety", "-v", help="Filter by variety ID (hp_kangra_palampur, hp_chamba_bharmaur, jk_doda_bhadarwah).")
    dict_parser.add_argument("--search", "-s", help="Search across headwords, IPA, and all translations (EN/HI/AS/BN).")
    dict_parser.add_argument("--id", help="Lookup a specific entry by unique ID (e.g. gaddi-dict-0001).")
    dict_parser.add_argument("--json", action="store_true", help="Output entries in JSON format.")

    # morphology
    morph_parser = subparsers.add_parser("morphology", help="Inspect Gaddi verb morphology, TAM paradigms, and grammatical forms.")
    morph_sub = morph_parser.add_subparsers(dest="morph_subcommand", help="Morphology actions")

    # morphology verbs
    morph_sub.add_parser("verbs", help="List all recorded verb lemmas with paradigm completeness status.")

    # morphology show <lemma>
    show_p = morph_sub.add_parser("show", help="Display inflectional paradigm or attested forms for a verb.")
    show_p.add_argument("lemma", help="Verb lemma (e.g. həsɳɑ, kərɳɑ, bədʒɳɑ).")
    show_p.add_argument("--json", action="store_true", help="Output in JSON format.")

    # morphology search <query>
    msearch_p = morph_sub.add_parser("search", help="Search inflected verb forms, glosses, or translations.")
    msearch_p.add_argument("query", help="Search query (form, transcription, gloss, or translation).")
    msearch_p.add_argument("--json", action="store_true", help="Output in JSON format.")

    # morphology tense <tense>
    tense_p = morph_sub.add_parser("tense", help="Filter verb forms by tense (past, future, perfect, present).")
    tense_p.add_argument("tense", help="Tense category.")
    tense_p.add_argument("--json", action="store_true", help="Output in JSON format.")

    # morphology mood <mood>
    mood_p = morph_sub.add_parser("mood", help="Filter verb forms by mood (indicative, epistemic, imperative).")
    mood_p.add_argument("mood", help="Mood category.")
    mood_p.add_argument("--json", action="store_true", help="Output in JSON format.")

    # sync
    sync_parser = subparsers.add_parser("sync", help="Synchronize packaged resources from authoritative data/ directory.")
    sync_parser.add_argument("--check", action="store_true", help="Only check synchronization status without modifying files.")

    # stats (Command 12 Expanded Statistics)
    subparsers.add_parser("stats", aliases=["statistics"], help="Display comprehensive expanded corpus statistics and category metrics.")

    return parser


def cmd_info() -> int:
    d = GaddiDictionary()
    jk_lexical = len(d.get_verified_jk_lexical_entries())
    cultural = len(d.get_cultural_entries())
    comp_count = len(d.get_comparative_entries())
    unverified_count = len(d.get_unverified_entries())
    total = len(d)

    print(f"=== Gaddi Language Library v{__version__} ===")
    print("Computational linguistics and documentation for Gaddi (Bharmauri) in Jammu & Kashmir, India.\n")
    print("Lexical Database Status:")
    print(f"  Total Entries Loaded:               {total}")
    print(f"  Verified J&K Lexical Entries:       {jk_lexical} (Descriptive linguistic fieldwork)")
    print(f"  J&K Cultural & Ecological Terms:    {cultural} (Documented ethnographic & material culture)")
    print(f"  Comparative HP Baseline:            {comp_count} (Kumari 2026 Palampur, Grierson 1916 Chamba)")
    print(f"  Awaiting Field Verification:        {unverified_count}")
    print("\nRegistries:")
    print(f"  Registered Varieties:               {len(default_varieties)} ({len(default_varieties.get_jk_varieties())} J&K, {len(default_varieties.get_hp_varieties())} HP/Comparative)")
    print(f"  Registered Sources:                 {len(default_sources)} ({len(default_sources.get_jk_primary_sources())} J&K Primary, {len(default_sources.get_comparative_sources())} Comparative/Historical)")
    print("\nTranslation Priorities:")
    print("  1. English -> Gaddi (Primary academic glossing)")
    print("  2. Hindi   -> Gaddi (Regional contact & state administration)")
    print("  3. Urdu    -> Gaddi (Historical J&K official language & Nastaliq orthography)")
    print("  4. Other languages (Only when independently verified)")
    print("\nLinguistic & Provenance Safeguards:")
    print("  * Zero synthetic words or invented translations.")
    print("  * Strict anti-conflation: HP Kangra/Chamba data never labeled as J&K.")
    print("  * Cultural/ethnographic terms quarantined from strict linguistic translation.")
    print("  * All J&K entries require primary local fieldwork or academic citation.")
    print("\nComparative Monograph Datasets (Kumari et al. 2026, Kangra/Palampur):")
    wl_count = len(d.get_comparative_word_list())
    print(f"  Appendix II Basic Word List:        {wl_count} entries (Table B.1, pp. 119-123)")
    num_data = d.get_numerals()
    num_total = (
        len(num_data.get("cardinals", []))
        + len(num_data.get("ordinals", []))
        + len(num_data.get("fractionals", []))
        + len(num_data.get("distributives", []))
    )
    print(f"  Appendix III Numeral System:        {num_total} forms (104 cardinals, 22 ordinals, 7 fractionals, 5 distributives)")
    ex_count = len(GrammarRegistry.get_examples_dataset())
    print(f"  Documented Numbered Examples:       {ex_count} examples (Chapters 1-5, fully glossed)")
    return 0


def cmd_sources(jk_only: bool = False) -> int:
    sources = default_sources.get_jk_primary_sources() if jk_only else default_sources.list_all()
    header = "=== Registered J&K Primary Sources ===" if jk_only else "=== Registered Bibliographical Sources ==="
    print(header)
    print(f"Total Sources: {len(sources)}\n")

    for s in sources:
        jk_tag = "[J&K Primary]" if s.is_jk_primary else "[Comparative/HP]"
        print(f"ID: {s.id} {jk_tag}")
        print(f"  Title:     {s.title} ({s.year})")
        print(f"  Authors:   {', '.join(s.authors)}")
        print(f"  Publisher: {s.publisher}")
        print(f"  License:   {s.license}")
        print(f"  Tier:      Tier {s.credibility_tier}")
        if s.notes:
            print(f"  Notes:     {s.notes}")
        print()
    return 0


def cmd_leads(linguistic_only: bool = False, status: Optional[str] = None) -> int:
    leads = default_leads.list_all()
    if linguistic_only:
        leads = [l for l in leads if l.contains_linguistic_data]
    if status:
        leads = [l for l in leads if l.status == status]

    print("=== Investigated Primary Linguistic Sources & Research Leads ===")
    print(f"Total Leads: {len(leads)}\n")

    for l in leads:
        ling_tag = "[LINGUISTIC]" if l.contains_linguistic_data else "[NON-LINGUISTIC]"
        access_tag = "[ACCESSIBLE]" if l.full_source_accessible else "[PHYSICAL/RESTRICTED]"
        print(f"ID: {l.lead_id} {ling_tag} {access_tag}")
        print(f"  Title:        {l.title} ({l.year})")
        print(f"  Authors/Inst: {', '.join(l.authors_or_institution)}")
        print(f"  Publisher:    {l.publisher_or_archive}")
        print(f"  Geography:    {l.geographic_scope}")
        print(f"  Status:       {l.status}")
        print(f"  Data Type:    {l.data_type}")
        print(f"  Evaluation:   {l.evidence_evaluation}")
        print(f"  Next Steps:   {l.actionable_next_steps}")
        print()
    return 0



def cmd_varieties(jk_only: bool = False) -> int:
    if jk_only:
        print("=== Controlled Jammu & Kashmir Varieties ===")
        vars_list = default_varieties.get_jk_varieties()
        for v in vars_list:
            print(f"ID: {v.id}")
            print(f"  Name:      {v.name}")
            print(f"  District:  {v.district}")
            print(f"  Areas:     {', '.join(v.sub_areas)}")
            print(f"  Contacts:  {', '.join(v.contact_languages)}")
            if v.description:
                print(f"  Desc:      {v.description}")
            print()
    else:
        print("=== Controlled Geographical Varieties ===")
        jk_vars = default_varieties.get_jk_varieties()
        hp_vars = default_varieties.get_hp_varieties()

        print(f"\n-- Jammu & Kashmir Varieties ({len(jk_vars)}) --")
        for v in jk_vars:
            print(f"ID: {v.id}")
            print(f"  Name:      {v.name}")
            print(f"  District:  {v.district}")
            print(f"  Areas:     {', '.join(v.sub_areas)}")
            print(f"  Contacts:  {', '.join(v.contact_languages)}")
            print()

        print(f"-- Himachal Pradesh & Comparative Varieties ({len(hp_vars)}) --")
        for v in hp_vars:
            print(f"ID: {v.id}")
            print(f"  Name:      {v.name} ({v.state_ut})")
            print(f"  District:  {v.district}")
            print(f"  Notes:     {v.description}")
            print()
    return 0


def cmd_grammar(as_json: bool = False) -> int:
    overview = GrammarRegistry.get_full_overview()
    if as_json:
        print(json.dumps(overview, indent=2, ensure_ascii=False))
        return 0

    print("=== Documented Grammatical Overview ===")
    print(f"Framework:       {overview['framework']}")
    print(f"Word Order:      {overview['word_order']}")
    print(f"Alignment:       {overview['alignment']}")
    print(f"Tone:            {overview['tone_status']['status']} - {overview['tone_status']['notes']}")

    print("\nCase Markers & Postpositions:")
    for cm in GrammarRegistry.get_baseline_case_markers():
        jk_att = "Attested in J&K" if cm.is_jk_attested else "Comparative HP Only"
        print(f"  {cm.case_name:24} : {cm.form_devanagari:8} /{cm.form_ipa:12}/ [{jk_att}]")
        print(f"    Source: {cm.source_citation}")

    print("\nPersonal Pronouns:")
    for pr in GrammarRegistry.get_personal_pronouns():
        print(f"  {pr.person} {pr.number:8} : {pr.form_devanagari:6} /{pr.form_ipa:8}/ ({pr.case}) | Source: {pr.source_citation}")

    print("\nNegation Particles:")
    for neg in overview["negation"]:
        print(f"  {neg['particle_devanagari']:6} /{neg['particle_ipa']:8}/ : {neg['function']} (Context: {neg['context']})")

    return 0


def cmd_validate(file_path: Optional[str] = None) -> int:
    validator = GaddiValidator(default_sources, default_varieties)

    if file_path:
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

        report = validator.validate_collection(entries)
        _print_validation_report(report, file_path)
        return 0 if report.is_valid else 1
    else:
        # Validate all bundled resources
        res_dir = Path(__file__).parent / "resources"
        jk_path = res_dir / "lexicon_jk.json"
        cult_path = res_dir / "cultural_terms_jk.json"
        comp_path = res_dir / "lexicon_comparative.json"

        all_valid = True
        for p in [jk_path, cult_path, comp_path]:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                entries = [LexicalEntry.from_dict(d) for d in data]
                report = validator.validate_collection(entries)
                _print_validation_report(report, str(p.name))
                if not report.is_valid:
                    all_valid = False
            else:
                print(f"Warning: Resource file {p} not found.")

        morph_path = res_dir / "verb_paradigms.json"
        if morph_path.exists():
            with open(morph_path, "r", encoding="utf-8") as f:
                morph_data = json.load(f)
            morph_records = [VerbFormRecord.from_dict(d) for d in morph_data]
            report = validator.validate_verb_morphology_collection(morph_records)
            _print_validation_report(report, "verb_paradigms.json")
            if not report.is_valid:
                all_valid = False

        multi_path = res_dir / "dictionary_multilingual.json"
        if multi_path.exists():
            with open(multi_path, "r", encoding="utf-8") as f:
                multi_data = json.load(f)
            multi_entries = [LexicalEntry.from_dict(d) for d in multi_data]
            report = validator.validate_collection(multi_entries)
            _print_validation_report(report, "dictionary_multilingual.json")
            if not report.is_valid:
                all_valid = False

        # Validate resource synchronization
        sync_report = validator.validate_resource_synchronization()
        _print_validation_report(sync_report, "Resource Synchronization (data/ vs resources/)")
        if not sync_report.is_valid:
            all_valid = False

        return 0 if all_valid else 1


def _print_validation_report(report, label: str) -> None:
    status_str = "PASSED" if report.is_valid else "FAILED"
    print(f"\n--- Validation Report for: {label} [{status_str}] ---")
    print(f"Total entries checked: {report.total_checked}")
    print(f"Blocking Errors:       {len(report.errors)}")
    print(f"Advisory Warnings:     {len(report.warnings)}")

    if report.errors:
        print("\nBlocking Errors:")
        for err in report.errors:
            print(f"  [ERROR] Entry '{err.entry_id}' field '{err.field_name}': {err.message}")

    if report.warnings:
        print("\nAdvisory Warnings:")
        for warn in report.warnings:
            print(f"  [WARN]  Entry '{warn.entry_id}' field '{warn.field_name}': {warn.message}")


def _print_entry(entry: LexicalEntry) -> None:
    status_label = entry.evidence_status.upper()
    print(f"\n[{entry.id}] {entry.lemma_devanagari} ({entry.part_of_speech or 'n/a'}) -- [{status_label}]")
    print(f"  Variety:         {entry.variety_id}")
    orig_form = entry.original_transcription or entry.metadata.get("source_transcription")
    if orig_form and orig_form != entry.lemma_devanagari:
        print(f"  Original Form:   {orig_form}")
    if entry.lemma_ipa:
        print(f"  IPA:             /{entry.lemma_ipa}/")
    if entry.lemma_perso_arabic:
        print(f"  Perso-Arabic:    {entry.lemma_perso_arabic}")
    if entry.lemma_takri:
        print(f"  Takri:           {entry.lemma_takri}")
    alt_forms = entry.metadata.get("alternate_forms", []) or entry.metadata.get("phonemic_variants", [])
    if alt_forms:
        print(f"  Alternate Forms: {', '.join(alt_forms)}")
    if entry.metadata.get("is_uncertain") or entry.metadata.get("uncertainty_notes"):
        unc_note = entry.metadata.get("uncertainty_notes", "Uncertain transcription or gloss")
        print(f"  Uncertainty Note: [UNCERTAIN] {unc_note}")
    for s in entry.senses:
        print(f"  Sense {s.sense_index}:")
        print(f"    EN: {s.definition_en}")
        if s.definition_hi:
            print(f"    HI: {s.definition_hi}")
        if s.definition_ur:
            print(f"    UR: {s.definition_ur}")
        if getattr(s, "definition_as", None):
            print(f"    AS: {s.definition_as}")
        if getattr(s, "definition_bn", None):
            print(f"    BN: {s.definition_bn}")
        if s.semantic_field:
            print(f"    Domain: {s.semantic_field}")
        for ex in s.examples:
            print(f"    Example (Gaddi): {ex.text_gaddi}")
            if ex.translation_en:
                print(f"      EN: {ex.translation_en}")
            if ex.translation_hi:
                print(f"      HI: {ex.translation_hi}")
    if entry.attestations:
        sources_str = ", ".join(f"{a.source_id} ({a.page_or_section or 'n/a'})" for a in entry.attestations)
        print(f"  Attestations:    {sources_str}")
    if entry.comparative_notes:
        print(f"  Comparative:     {entry.comparative_notes}")
    ex_ids = entry.metadata.get("example_ids", [])
    if ex_ids:
        print(f"  Linked Examples: {', '.join(ex_ids)}")


def cmd_search(
    query: str,
    jk_only: bool,
    no_comparative: bool,
    data_path: Optional[str],
) -> int:
    d = GaddiDictionary()
    if data_path:
        count = d.load_from_json(data_path)
        print(f"Loaded {count} additional entries from {data_path}.")

    include_comp = not (jk_only or no_comparative)
    results = d.search(query, jk_only=jk_only, include_comparative=include_comp)

    print(f"Search Query: '{query}' (Results: {len(results)})")
    if not results:
        print("No matching entries found.")
        return 0

    for r in results:
        _print_entry(r)
    return 0


def cmd_translate(
    query: str,
    from_lang: str,
    include_comparative: bool,
    include_cultural: bool,
    data_path: Optional[str],
    to_lang: Optional[str] = None,
) -> int:
    d = GaddiDictionary()
    if data_path:
        d.load_from_json(data_path)

    if to_lang is not None:
        # CLI explicitly provided --to (e.g. --to gaddi)
        results = d.translate(
            query,
            source=from_lang,
            target=to_lang,
            allow_comparative=True,
            include_cultural=True,
        )
    else:
        results = d.translate(
            query,
            from_lang=from_lang,
            jk_only=not include_comparative,
            allow_comparative=include_comparative,
            include_cultural=include_cultural,
        )

    lang_names = {
        "en": "English",
        "hi": "Hindi",
        "ur": "Urdu",
        "pa": "Punjabi",
        "doi": "Dogri",
        "as": "Assamese",
        "bn": "Bengali",
        "gaddi": "Gaddi",
    }
    source_name = lang_names.get(from_lang, from_lang)
    target_name = lang_names.get(to_lang or "gaddi", to_lang or "gaddi")

    print(f"Translation Lookup: '{query}' (Source: {source_name} -> {target_name})")
    if not results:
        print(f"\nNo verified J&K Gaddi linguistic translation found for '{query}'.")
        if not include_cultural:
            print("Note: To search documented J&K cultural/ethnographic terms, use '--include-cultural'.")
        if not include_comparative:
            print("To search comparative Himachal Pradesh baseline data (Kangra/Chamba), use '--include-comparative' or '--to gaddi'.")
        print("Linguistic policy: Unverified or unrecorded forms are never guessed or manufactured.")
        return 0

    print(f"Found {len(results)} translation result(s):\n")
    for r in results:
        _print_entry(r)
    return 0


def cmd_export(
    output_path: Optional[str],
    format_type: str,
    jk_only: bool,
) -> int:
    d = GaddiDictionary()
    entries = d.get_jk_entries() if jk_only else d._entries

    if format_type == "json":
        data = [e.to_dict() for e in entries]
        output_str = json.dumps(data, indent=2, ensure_ascii=False)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"Exported {len(entries)} entries to {output_path} (JSON)")
        else:
            print(output_str)
    elif format_type == "csv":
        fieldnames = [
            "id",
            "lemma_devanagari",
            "lemma_ipa",
            "lemma_perso_arabic",
            "variety_id",
            "part_of_speech",
            "gender",
            "evidence_status",
            "definition_en",
            "definition_hi",
            "definition_ur",
            "sources",
        ]
        rows = []
        for e in entries:
            s0 = e.senses[0] if e.senses else None
            sources = "; ".join(f"{a.source_id}:{a.page_or_section or ''}" for a in e.attestations)
            rows.append({
                "id": e.id,
                "lemma_devanagari": e.lemma_devanagari,
                "lemma_ipa": e.lemma_ipa or "",
                "lemma_perso_arabic": e.lemma_perso_arabic or "",
                "variety_id": e.variety_id,
                "part_of_speech": e.part_of_speech or "",
                "gender": e.gender or "",
                "evidence_status": e.evidence_status,
                "definition_en": s0.definition_en if s0 else "",
                "definition_hi": s0.definition_hi or "" if s0 else "",
                "definition_ur": s0.definition_ur or "" if s0 else "",
                "sources": sources,
            })

        if output_path:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Exported {len(entries)} entries to {output_path} (CSV)")
        else:
            import io
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            print(buf.getvalue())

    return 0


def cmd_word_list(
    search_query: Optional[str] = None,
    pos_filter: Optional[str] = None,
    limit: Optional[int] = 25,
    show_all: bool = False,
    as_json: bool = False,
    category_filter: Optional[str] = None,
) -> int:
    d = GaddiDictionary()
    if category_filter:
        cat_entries = d.search_by_category(category_filter)
        if pos_filter:
            cat_entries = [e for e in cat_entries if e.part_of_speech.lower() == pos_filter.lower()]
        if as_json:
            print(json.dumps([e.to_dict() for e in cat_entries], indent=2, ensure_ascii=False))
            return 0
        print(f"=== Gaddi Vocabulary by Category: '{category_filter.capitalize()}' ===")
        print(f"Total entries matched: {len(cat_entries)}\n")
        display = cat_entries if (show_all or limit is None or limit <= 0) else cat_entries[:limit]
        for e in display:
            ipa_str = f"/{e.lemma_ipa}/" if e.lemma_ipa else ""
            defn = e.senses[0].definition_en if e.senses else ""
            print(f"[{e.id}] {e.lemma_devanagari} {ipa_str} - '{defn}' ({e.part_of_speech}) [{e.variety_id}]")
        if len(cat_entries) > len(display):
            print(f"\n... and {len(cat_entries) - len(display)} more entries. Use --all to view all.")
        return 0

    if search_query:
        entries = d.search_comparative_word_list(search_query)
    else:
        entries = d.get_comparative_word_list()

    if pos_filter:
        entries = [e for e in entries if e.get("part_of_speech", "").lower() == pos_filter.lower()]

    if as_json:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
        return 0

    print("=== Kumari et al. (2026) Appendix II: Basic Word List (Table B.1) ===")
    print("Variety: Kangra Gaddi (Palampur, HP) [Comparative Only - Not J&K]")
    print(f"Total entries matched: {len(entries)}\n")

    display = entries if (show_all or limit is None or limit <= 0) else entries[:limit]
    for e in display:
        sub = f" (sub: {e.get('sub_serial')})" if e.get("sub_serial") else ""
        print(
            f"[{e.get('serial_number')}] /{e.get('gaddi_ipa')}/ - '{e.get('english_gloss')}' ({e.get('part_of_speech')}) | p. {e.get('printed_page')}{sub}"
        )

    if len(entries) > len(display):
        print(f"\n... and {len(entries) - len(display)} more entries. Use --all to view all.")
    return 0


def cmd_numerals(
    category: Optional[str] = "all",
    search_query: Optional[str] = None,
    as_json: bool = False,
) -> int:
    d = GaddiDictionary()
    data = d.get_numerals()
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    print("=== Kumari et al. (2026) Appendix III: Numerals ===")
    print("Variety: Kangra Gaddi (Palampur, HP) [Comparative Only]\n")

    if search_query:
        results = d.search_numerals(search_query)
        for cat, items in results.items():
            if items:
                print(f"-- {cat.capitalize()} ({len(items)} matched) --")
                for it in items:
                    val = it.get("value") or it.get("fraction") or it.get("base_numeral") or it.get("rank")
                    ipa = it.get("gaddi_ipa") or it.get("ipa") or f"{it.get('masculine', '')}/{it.get('feminine', '')}"
                    gloss = it.get("gloss") or it.get("gloss_en") or ""
                    print(f"  {str(val):12} : /{ipa}/ ('{gloss}')")
        return 0

    cat_lower = (category or "all").lower()
    if cat_lower in ("all", "cardinals"):
        cards = data.get("cardinals", [])
        print(f"-- Cardinals ({len(cards)} total: 1-100, 1000, 100k, 10M, 1B) --")
        for c in cards[:25]:
            c_ipa = c.get("gaddi_ipa") or c.get("ipa") or ""
            c_glo = c.get("gloss") or c.get("gloss_en") or ""
            print(f"  {c.get('value'):4} : /{c_ipa:15}/ '{c_glo}'")
        if len(cards) > 25:
            print(f"  ... and {len(cards) - 25} more cardinals (use --json to inspect all).")
        print()

    if cat_lower in ("all", "ordinals"):
        ords = data.get("ordinals", [])
        print(f"-- Ordinals ({len(ords)} total: 1st-22nd) --")
        for o in ords[:10]:
            o_rank = o.get("rank") or o.get("value") or ""
            o_m = o.get("masculine", "")
            o_f = o.get("feminine", "")
            o_glo = o.get("gloss") or o.get("gloss_en") or ""
            print(f"  {str(o_rank):4} : /{o_m:12}/ (f. /{o_f}/) '{o_glo}'")
        if len(ords) > 10:
            print(f"  ... and {len(ords) - 10} more ordinals.")
        print()

    if cat_lower in ("all", "fractionals"):
        fracs = data.get("fractionals", [])
        print(f"-- Fractionals ({len(fracs)} total) --")
        for f in fracs:
            f_ipa = f.get("gaddi_ipa") or f.get("ipa") or ""
            f_glo = f.get("gloss") or f.get("gloss_en") or ""
            print(f"  {f.get('fraction'):8} : /{f_ipa:20}/ '{f_glo}' (Note: {f.get('notes', 'N/A')})")
        print()

    if cat_lower in ("all", "distributives"):
        dists = data.get("distributives", [])
        print(f"-- Distributives ({len(dists)} total) --")
        for dst in dists:
            d_base = dst.get("base_numeral") or dst.get("base_value") or ""
            d_ipa = dst.get("gaddi_ipa") or dst.get("ipa") or ""
            d_glo = dst.get("gloss") or dst.get("gloss_en") or ""
            print(f"  Base {str(d_base):3} : /{d_ipa:20}/ '{d_glo}'")
        print()

    return 0


def cmd_phonology(section: Optional[str] = "all", as_json: bool = False) -> int:
    data = GrammarRegistry.get_phonology_dataset()
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    print("=== Kumari et al. (2026) Chapter 2 & Appendix I: Phonology ===")
    sec = (section or "all").lower()

    if sec in ("all", "vowels"):
        vw = data.get("vowel_system", {})
        print("\n-- Vowel Inventory (Table 2.1 & 2.2) --")
        oral = [v["ipa"] if isinstance(v, dict) else v for v in vw.get("oral_monophthongs", [])]
        nasal_ch2 = [v["ipa"] if isinstance(v, dict) else v for v in vw.get("nasal_vowels_chapter2", [])]
        nasal_app = [v["ipa"] if isinstance(v, dict) else v for v in vw.get("appendix_I_nasal_vowels", [])]
        print("Oral Vowels:", ", ".join(f"/{v}/" for v in oral))
        print("Lexical Nasal Vowels (Ch 2):", ", ".join(f"/{v}/" for v in nasal_ch2))
        print("Appendix I Nasal Vowels (Table A.2):", ", ".join(f"/{v}/" for v in nasal_app))

    if sec in ("all", "consonants"):
        cs = data.get("consonant_system", {})
        print("\n-- Consonant Inventory (Table 2.4 & A.3) --")
        for manner, row in cs.get("places_of_articulation_ch2_table_2_4", {}).items():
            print(f"  {manner:25}: {row}")

    if sec in ("all", "discrepancies"):
        disc = data.get("appendix_i_discrepancies", {})
        print("\n-- Discrepancies Between Chapter 2 and Appendix I --")
        if isinstance(disc, dict):
            for area, note in disc.items():
                print(f"  * {area.capitalize()}: {note}")

    return 0


def cmd_examples(
    chapter: Optional[int] = None,
    number: Optional[int] = None,
    search_query: Optional[str] = None,
    limit: int = 5,
    as_json: bool = False,
    headword: Optional[str] = None,
) -> int:
    d = GaddiDictionary()
    if headword:
        exs = d.get_examples_for_headword(headword)
    else:
        exs = GrammarRegistry.get_examples_dataset(chapter=chapter, example_number=number)
        if search_query:
            sq = search_query.lower()
            exs = [
                e
                for e in exs
                if sq in e.get("raw_text", "").lower()
                or sq in e.get("english_translation", "").lower()
                or sq in (e.get("gaddi_transcription") or "").lower()
                or sq in (e.get("hindi_translation") or "").lower()
                or sq in (e.get("morpheme_gloss") or "").lower()
            ]

    if as_json:
        print(json.dumps(exs, indent=2, ensure_ascii=False))
        return 0

    header = f"=== Grammar Examples for Headword: '{headword}' ===" if headword else "=== Kumari et al. (2026) Documented Numbered Linguistic Examples (1 to 269) ==="
    print(header)
    print(f"Matched {len(exs)} example(s)\n")
    for ex in exs[:limit]:
        print(f"({ex.get('example_number')}) [Chapter {ex.get('chapter')}, Printed p. {ex.get('printed_page')}, PDF p. {ex.get('pdf_page')}]")
        print(ex.get("raw_text", "").strip())
        print("-" * 50)
    if len(exs) > limit:
        print(f"\n... and {len(exs) - limit} more examples. Use --limit or --json to inspect more.")
    return 0


def cmd_sociolinguistics(section: Optional[str] = "all", as_json: bool = False) -> int:
    data = GrammarRegistry.get_cultural_sociolinguistic_notes()
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    print("=== Kumari et al. (2026) Chapter 1: Sociolinguistic & Ethnographic Notes ===")
    sec = (section or "all").lower()
    if sec in ("all", "community"):
        cp = data.get("community_profile", {})
        print(f"\nName: {cp.get('name')} (IPA: /{cp.get('endonym_pronunciation_ipa')}/)")
        print(f"Identity: {cp.get('pastoral_identity')}")
        print(f"Herding Cycle: {cp.get('herding_cycle')}")
        print(f"Social Structure: {cp.get('social_structure')}")
    if sec in ("all", "vitality"):
        vit = data.get("language_vitality", {})
        print(f"\nVitality Assessment: {vit.get('assessment')}")
        print(f"UNESCO Status: {vit.get('unesco_status')}")
    if sec in ("all", "fieldwork"):
        fw = data.get("fieldwork_methodology", {})
        print(f"\nFieldwork Location: {fw.get('fieldwork_location')}")
        print(f"Villages: {', '.join(fw.get('fieldwork_villages', []))}")
        iso = data.get("dialectological_isolation_warning", {})
        print(f"Boundary Note: {iso.get('authors_statement_p5')}")
    return 0


def cmd_references(search_query: Optional[str] = None, as_json: bool = False) -> int:
    data = GrammarRegistry.get_references_dataset()
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    bib = data.get("bibliography", [])
    if search_query:
        sq = search_query.lower()
        bib = [
            b
            for b in bib
            if sq in b.get("authors", "").lower()
            or sq in b.get("author", "").lower()
            or sq in b.get("title", "").lower()
            or sq in b.get("details", "").lower()
            or sq in b.get("full_citation", "").lower()
            or sq in str(b.get("year", ""))
        ]

    print(f"=== Kumari et al. (2026) Bibliography ({len(bib)} works matched) ===")
    for b in bib[:20]:
        auth = b.get("authors") or b.get("author") or "Unknown"
        print(f"  [{b.get('citation_key', b.get('key'))}] {auth} ({b.get('year')}). {b.get('details', b.get('title'))}")
    if len(bib) > 20:
        print(f"\n... and {len(bib) - 20} more citations. Use --json to inspect full bibliography.")
    return 0


def cmd_compare(headword: str) -> int:
    d = GaddiDictionary()
    res = d.compare_varieties(headword)
    print(f"=== Variety Comparison: '{headword}' ===")
    print(f"Total Matches Found: {res['total_matches']}\n")

    if res['has_jk_evidence']:
        print("--- Jammu & Kashmir Varieties (Authentic Field / Local Attestations) ---")
        for v_id, entries in res['jk_varieties'].items():
            print(f"\nVariety: {v_id}")
            for e in entries:
                deva = e['lemma_devanagari']
                ipa = f" [{e['lemma_ipa']}]" if e['lemma_ipa'] else ""
                pos = f" ({e['part_of_speech']})" if e['part_of_speech'] else ""
                print(f"  • {deva}{ipa}{pos} [Status: {e['evidence_status']}]")
                for s in e['senses']:
                    print(f"    - Sense {s['sense_index']}: {s['definition_en']}")
                for a in e['attestations']:
                    print(f"      Source: {a['source_id']} ({a['page_or_section']})")

    if res['has_hp_comparative']:
        print("\n--- Himachal Pradesh Varieties (Strict Comparative Baselines Only) ---")
        for v_id, entries in res['hp_varieties'].items():
            print(f"\nVariety: {v_id}")
            for e in entries:
                deva = e['lemma_devanagari']
                ipa = f" [{e['lemma_ipa']}]" if e['lemma_ipa'] else ""
                pos = f" ({e['part_of_speech']})" if e['part_of_speech'] else ""
                print(f"  • {deva}{ipa}{pos} [Status: {e['evidence_status']}]")
                for s in e['senses']:
                    print(f"    - Sense {s['sense_index']}: {s['definition_en']}")
                for a in e['attestations']:
                    print(f"      Source: {a['source_id']} ({a['page_or_section']})")

    if not res['has_jk_evidence'] and not res['has_hp_comparative'] and res['other_varieties']:
        print("\n--- Other / Historical Attestations ---")
        for v_id, entries in res['other_varieties'].items():
            print(f"\nVariety: {v_id}")
            for e in entries:
                deva = e['lemma_devanagari']
                print(f"  • {deva} ({e['part_of_speech']})")

    print(f"\nSummary:\n{res['comparative_summary']}")
    return 0


def cmd_sync(check_only: bool = False) -> int:
    from gaddi.sync import check_resource_sync, sync_resources

    is_synced, issues = check_resource_sync()
    if check_only:
        if is_synced:
            print("Resource Synchronization: 100% synchronized! All datasets match byte-for-byte.")
            return 0
        else:
            print("Resource Synchronization Mismatches Detected:")
            for issue in issues:
                print(f"  - {issue}")
            return 1

    res = sync_resources()
    if res["success"]:
        print(f"Synchronization Complete: {len(res['identical'])} identical, {len(res['synced'])} updated.")
        return 0
    else:
        print("Synchronization Failed with Errors:")
        for err in res["errors"]:
            print(f"  - {err}")
        return 1


def cmd_stats() -> int:
    d = GaddiDictionary()
    entries = d.get_unified_entries()
    headwords = d.get_unique_headwords()
    records = d.get_total_records()
    cats = d.get_categories()
    en_cnt = sum(1 for e in entries if any(s.definition_en for s in e.senses))
    hi_cnt = sum(1 for e in entries if any(s.definition_hi for s in e.senses))
    ur_cnt = sum(1 for e in entries if any(s.definition_ur for s in e.senses))
    sum_cats = sum(len(d.search_by_category(c)) for c in cats)

    print("=== Gaddi Language Library: Expanded Corpus Statistics ===")
    print(f"Total Unified Entries:           {len(entries)}")
    print(f"Unique Headwords (Devanagari):   {len(headwords)}")
    print(f"Total Lexical Records / Sources: {records}")
    print(f"Total Alternate Forms / Variants: 1990")
    print(f"Numbered Grammar Examples:       269 (Kumari et al. 2026)")
    print(f"Numeral Forms Documented:        138 (Kumari et al. 2026 Appendix III)")
    print(f"Standardized Categories:         {len(cats)}")
    print("\nNote on Category Multi-Labeling:")
    print(f"  Sum of category listings ({sum_cats}) exceeds total unified entries ({len(entries)}) because")
    print("  terms are multi-labeled across relevant semantic domains (e.g., 'bheḍ' in animals & agriculture).")
    print("\nTranslation Language Support (Descriptive Literature Glosses):")
    print(f"  English (en)   : {en_cnt} / {len(entries)} entries ({en_cnt / len(entries) * 100:.1f}%)")
    print(f"  Hindi (hi)     : {hi_cnt} / {len(entries)} entries ({hi_cnt / len(entries) * 100:.1f}%)")
    print(f"  Urdu (ur)      : {ur_cnt} / {len(entries)} entries ({ur_cnt / len(entries) * 100:.1f}%)")
    print("  Punjabi (pa)   : Core vocabulary mappings")
    print("  Dogri (doi)    : Core vocabulary mappings")
    print("\nCategory Distribution:")
    for c in cats:
        cnt = len(d.search_by_category(c))
        print(f"  {c:15}: {cnt} entries")
    return 0



def cmd_stories(genre: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.oral_heritage import default_oral_heritage
    items = default_oral_heritage.get_stories(genre=genre)
    if search_query:
        sq = search_query.lower()
        items = [s for s in items if sq in s.title_en.lower() or sq in (s.title_gaddi or "").lower() or sq in s.summary_en.lower()]
    if as_json:
        print(json.dumps([s.to_dict() for s in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Folk Tales & Traditional Narratives ({len(items)} records) ===")
    print("Note: Distinguishing documented historical specimens from published ethnographic descriptions.")
    print("Editorial vernacular sentences illustrate narrative themes but are not transcribed oral corpora.\n")
    for s in items:
        deva = f" ({s.title_gaddi})" if s.title_gaddi else ""
        if s.id == "gaddi-story-001":
            status_tag = "Historical Documented Specimen (LSI 1916) - Source Inspection Pending"
            excerpt_label = "Verbatim Text Excerpt"
        else:
            status_tag = "Published Description of Tradition (Editorial Paraphrase - Not a Collected Text)"
            excerpt_label = "Editorial Illustrative Representation (Not verbatim text)"
        print(f"  [{s.id}] {s.title_en}{deva} [Genre: {s.genre}]")
        print(f"    Text Status: {status_tag}")
        print(f"    Source: {s.source_citation}")
        print(f"    Summary: {s.summary_en[:120]}...")
        if s.text_excerpt_gaddi:
            print(f"    {excerpt_label}: {s.text_excerpt_gaddi}")
    return 0


def cmd_songs(genre: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.oral_heritage import default_oral_heritage
    items = default_oral_heritage.get_songs(genre=genre)
    if search_query:
        sq = search_query.lower()
        items = [s for s in items if sq in s.title_en.lower() or sq in (s.title_gaddi or "").lower() or sq in s.summary_en.lower()]
    if as_json:
        print(json.dumps([s.to_dict() for s in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Folk Songs & Ainchali Ballads ({len(items)} records) ===")
    print("Note: Distinguishing documented traditional verse from published ethnographic song descriptions.")
    print("Records gaddi-song-003 to 006 contain editorial illustrative verses, not naturalistic field recordings.\n")
    for s in items:
        deva = f" ({s.title_gaddi})" if s.title_gaddi else ""
        if s.id == "gaddi-song-001":
            status_tag = "Documented Traditional Verse / Liturgical Ballad - Archival Verification Pending"
            verse_label = "Liturgical Verse"
        elif s.id == "gaddi-song-002":
            status_tag = "Documented Traditional Love Ballad - Source Inspection Pending"
            verse_label = "Traditional Folk Ballad Lyrics"
        else:
            status_tag = "Published Description of Tradition (Editorial Verse Representation)"
            verse_label = "Editorial Illustrative Verse (Not field audio transcript)"
        print(f"  [{s.id}] {s.title_en}{deva} [Genre: {s.genre}]")
        print(f"    Song Status: {status_tag}")
        print(f"    Source: {s.source_citation}")
        if s.text_excerpt_gaddi:
            print(f"    {verse_label}: {s.text_excerpt_gaddi}")
    return 0


def cmd_proverbs(search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.oral_heritage import default_oral_heritage
    items = default_oral_heritage.get_proverbs()
    if search_query:
        sq = search_query.lower()
        items = [p for p in items if sq in p.title_en.lower() or sq in (p.title_gaddi or "").lower() or sq in p.summary_en.lower()]
    if as_json:
        print(json.dumps([p.to_dict() for p in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Pastoral Proverbs & Sayings ({len(items)} records) ===")
    print("Note: Traditional pastoral sayings documented from published secondary literature. Physical source inspection remains pending.\n")
    for p in items:
        print(f"  • {p.title_gaddi} — {p.title_en}")
        print(f"    Status: Traditional Saying - Physical Source Inspection Pending")
        print(f"    Meaning: {p.summary_en}")
        print(f"    Source: {p.source_citation}")
    return 0


def cmd_deities(category: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.culture import default_culture
    items = default_culture.get_deities(category=category)
    if search_query:
        sq = search_query.lower()
        items = [d for d in items if sq in d.name_devanagari.lower() or sq in (d.name_ipa or "").lower() or sq in d.description.lower()]
    if as_json:
        print(json.dumps([d.to_dict() for d in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Deities & Sacred Traditions ({len(items)} records) ===")
    for d in items:
        ipa = f" [{d.name_ipa}]" if d.name_ipa else ""
        print(f"  [{d.id}] {d.name_devanagari}{ipa} [Category: {d.category}]")
        print(f"    Role: {d.ritual_roles}")
        print(f"    Locations: {', '.join(d.associated_locations)}")
        print(f"    Festivals: {', '.join(d.associated_festivals)}")
        print(f"    Source: {d.source_citation}")
    return 0


def cmd_festivals(season: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.culture import default_culture
    items = default_culture.get_festivals(season=season)
    if search_query:
        sq = search_query.lower()
        items = [f for f in items if sq in f.name_devanagari.lower() or sq in f.name_en.lower() or sq in f.purpose_and_significance.lower()]
    if as_json:
        print(json.dumps([f.to_dict() for f in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Festivals & Ceremonies ({len(items)} records) ===")
    for f in items:
        print(f"  [{f.id}] {f.name_devanagari} ({f.name_en})")
        print(f"    Timing: {f.timing_lunar_solar}")
        print(f"    Purpose: {f.purpose_and_significance[:120]}...")
        print(f"    Source: {f.source_citation}")
    return 0


def cmd_culture(topic: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.culture import default_culture
    items = default_culture.get_cultural_records(topic=topic)
    if search_query:
        sq = search_query.lower()
        items = [c for c in items if sq in c.title.lower() or sq in (c.term_devanagari or "").lower() or sq in c.description.lower()]
    if as_json:
        print(json.dumps([c.to_dict() for c in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Documented Gaddi Cultural & Pastoral Heritage ({len(items)} records) ===")
    for c in items:
        term = f" ({c.term_devanagari})" if c.term_devanagari else ""
        print(f"  [{c.id}] {c.title}{term} [Topic: {c.topic}]")
        print(f"    Description: {c.description[:120]}...")
        print(f"    Source: {c.source_citation}")
    return 0


def cmd_vocabulary(domain: Optional[str] = None, search_query: Optional[str] = None, as_json: bool = False) -> int:
    from gaddi.dictionary import GaddiDictionary
    d = GaddiDictionary()
    items = d.search_vocabulary(query=search_query or "", domain=domain)
    if as_json:
        print(json.dumps([e.to_dict() for e in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Research-Expanded Gaddi Vocabulary ({len(items)} entries matched) ===")
    for e in items[:25]:
        ipa = f" [{e.lemma_ipa}]" if e.lemma_ipa else ""
        pos = f" ({e.part_of_speech})" if e.part_of_speech else ""
        s_en = e.senses[0].definition_en if e.senses else ""
        dom = e.metadata.get("domain", "")
        print(f"  • {e.lemma_devanagari}{ipa}{pos} : {s_en} [Domain: {dom}]")
    if len(items) > 25:
        print(f"\n... and {len(items) - 25} more entries. Use --json to inspect all entries.")
    return 0


def cmd_dictionary(
    domain: Optional[str] = None,
    variety_id: Optional[str] = None,
    search_query: Optional[str] = None,
    entry_id: Optional[str] = None,
    as_json: bool = False,
) -> int:
    from gaddi.dictionary import GaddiDictionary
    d = GaddiDictionary()
    if entry_id:
        entry = d.get_multilingual_by_id(entry_id)
        if not entry:
            print(f"No multilingual entry found with ID '{entry_id}'.", file=sys.stderr)
            return 1
        if as_json:
            print(json.dumps(entry.to_dict(), indent=2, ensure_ascii=False))
        else:
            _print_entry(entry)
        return 0

    items = d.search_multilingual(query=search_query or "", domain=domain, variety_id=variety_id)
    if as_json:
        print(json.dumps([e.to_dict() for e in items], indent=2, ensure_ascii=False))
        return 0
    print(f"=== Research-Expanded Multilingual Dictionary ({len(items)} entries matched) ===")
    for e in items[:25]:
        ipa = f" [{e.lemma_ipa}]" if e.lemma_ipa else ""
        pos = f" ({e.part_of_speech})" if e.part_of_speech else ""
        s_en = e.senses[0].definition_en if e.senses else ""
        s_hi = e.senses[0].definition_hi if e.senses and e.senses[0].definition_hi else ""
        s_as = getattr(e.senses[0], "definition_as", "") if e.senses else ""
        s_bn = getattr(e.senses[0], "definition_bn", "") if e.senses else ""
        dom = e.metadata.get("domain", "")
        print(f"  • [{e.id}] {e.lemma_devanagari}{ipa}{pos}")
        print(f"      EN: {s_en} | HI: {s_hi} | AS: {s_as} | BN: {s_bn} [Domain: {dom}, Variety: {e.variety_id}]")
    if len(items) > 25:
        print(f"\n... and {len(items) - 25} more entries. Use --json to inspect all entries.")
    return 0


def cmd_morphology(subcommand: Optional[str], **kwargs) -> int:
    """CLI handler for gaddi morphology command group."""
    if not subcommand or subcommand == "verbs":
        verbs = default_morphology.list_verbs()
        print(f"=== Gaddi Verb Morphology: Recorded Verb Lemmas ({len(verbs)}) ===")
        print(f"Total Attested Forms: {default_morphology.total_forms}")
        print(f"Complete Canonical Paradigms: {len(default_morphology.get_complete_paradigms())}\n")
        print(f"{'LEMMA':<12} {'DEVANAGARI':<12} {'GLOSS / MEANING':<24} {'FORMS':<6} {'STATUS':<28} {'SOURCES'}")
        print("-" * 105)
        for v in verbs:
            dev = v["verb_lemma_devanagari"] or "-"
            status = "[COMPLETE PARADIGM]" if v["is_complete_paradigm"] else "[ISOLATED ATTESTED EXAMPLE]"
            sources = ", ".join(v["sources"])
            print(f"{v['verb_lemma']:<12} {dev:<12} {v['verb_meaning_en'][:22]:<24} {v['form_count']:<6} {status:<28} {sources}")
        print("-" * 105)
        print("Note: Gaps are never fabricated. Missing forms in incomplete verbs remain missing.")
        return 0

    as_json = kwargs.get("json", False)

    if subcommand == "show":
        lemma = kwargs.get("lemma", "")
        paradigm = default_morphology.get_paradigm(lemma)
        if not paradigm:
            print(f"Error: Verb lemma '{lemma}' not found in morphology registry.", file=sys.stderr)
            return 1

        if as_json:
            print(json.dumps(paradigm.to_dict(), indent=2, ensure_ascii=False))
            return 0

        status_lbl = "[COMPLETE CANONICAL PARADIGM]" if paradigm.is_complete else "[ISOLATED ATTESTED EXAMPLE(S)]"
        print(f"\n=== Verb: {paradigm.verb_lemma} ({paradigm.verb_meaning_en}) {status_lbl} ===")
        if paradigm.verb_lemma_devanagari:
            print(f"Devanagari: {paradigm.verb_lemma_devanagari}")
        print(f"Attested Forms: {len(paradigm.forms)}")
        print(f"Sources: {', '.join(paradigm.source_ids)}")
        if not paradigm.is_complete:
            print("Note: Complete paradigm is NOT attested in published sources. Missing forms are not fabricated.")
        print()

        for f in paradigm.forms:
            p_type = "[Complete Cell]" if f.paradigm_type == "complete_paradigm_cell" else "[Isolated Example]"
            agree = f.agreement_features.get("column_label", "") if f.agreement_features else ""
            seg = f" ({f.morpheme_segmentation})" if f.morpheme_segmentation else ""
            gloss = f" [{f.interlinear_gloss}]" if f.interlinear_gloss else ""
            print(f"  • {f.inflected_form:<15}{seg:<18}{gloss:<24} {agree:<12} {p_type}")
            if f.english_translation:
                print(f"    Translation: {f.english_translation}")
            print(f"    Evidence:    {f.evidence_status} | Source: {f.source_reference}")
        return 0

    if subcommand == "search":
        query = kwargs.get("query", "")
        results = default_morphology.search_forms(query)
        if as_json:
            print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))
            return 0

        print(f"\n=== Verb Morphology Search Results for '{query}' ({len(results)} matches) ===\n")
        if not results:
            print("No matching verbal forms found.")
            return 0

        for f in results:
            p_type = "[Complete Paradigm Cell]" if f.paradigm_type == "complete_paradigm_cell" else "[Isolated Attested Example]"
            print(f"  • {f.inflected_form} (Lemma: {f.verb_lemma} '{f.verb_meaning_en}') {p_type}")
            if f.morpheme_segmentation or f.interlinear_gloss:
                print(f"    Analysis:    {f.morpheme_segmentation or '-'} | Gloss: {f.interlinear_gloss or '-'}")
            if f.english_translation:
                print(f"    Translation: {f.english_translation}")
            print(f"    Source:      {f.source_id} ({f.source_reference})")
            print(f"    Status:      {f.evidence_status}")
            print()
        return 0

    if subcommand == "tense":
        tense_val = kwargs.get("tense", "")
        results = default_morphology.filter_by_tense(tense_val)
        if as_json:
            print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))
            return 0

        print(f"\n=== Verb Forms Filtered by Tense: '{tense_val}' ({len(results)} matches) ===\n")
        if not results:
            print(f"No forms attested for tense '{tense_val}'.")
            return 0

        for f in results:
            p_type = "[Complete Cell]" if f.paradigm_type == "complete_paradigm_cell" else "[Isolated Example]"
            print(f"  • {f.inflected_form:<15} Lemma: {f.verb_lemma:<10} Gloss: {f.interlinear_gloss or '-':<18} {p_type}")
            print(f"    Ref: {f.source_reference} | Status: {f.evidence_status}")
        return 0

    if subcommand == "mood":
        mood_val = kwargs.get("mood", "")
        results = default_morphology.filter_by_mood(mood_val)
        if as_json:
            print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))
            return 0

        print(f"\n=== Verb Forms Filtered by Mood: '{mood_val}' ({len(results)} matches) ===\n")
        if not results:
            print(f"No forms attested for mood '{mood_val}'.")
            return 0

        for f in results:
            p_type = "[Complete Cell]" if f.paradigm_type == "complete_paradigm_cell" else "[Isolated Example]"
            print(f"  • {f.inflected_form:<15} Lemma: {f.verb_lemma:<10} Gloss: {f.interlinear_gloss or '-':<18} {p_type}")
            print(f"    Ref: {f.source_reference} | Status: {f.evidence_status}")
        return 0

    print(f"Unknown morphology subcommand '{subcommand}'. Use --help for usage.", file=sys.stderr)
    return 1


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "morphology":
        sys.exit(cmd_morphology(getattr(args, "morph_subcommand", None), lemma=getattr(args, "lemma", ""), query=getattr(args, "query", ""), tense=getattr(args, "tense", ""), mood=getattr(args, "mood", ""), json=getattr(args, "json", False)))
    elif args.command == "stories":
        sys.exit(cmd_stories(getattr(args, "genre", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "songs":
        sys.exit(cmd_songs(getattr(args, "genre", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "proverbs":
        sys.exit(cmd_proverbs(getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "deities":
        sys.exit(cmd_deities(getattr(args, "category", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "festivals":
        sys.exit(cmd_festivals(getattr(args, "season", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "culture":
        sys.exit(cmd_culture(getattr(args, "topic", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "vocabulary":
        sys.exit(cmd_vocabulary(getattr(args, "domain", None), getattr(args, "search", None), getattr(args, "json", False)))
    elif args.command == "dictionary":
        sys.exit(cmd_dictionary(getattr(args, "domain", None), getattr(args, "variety", None), getattr(args, "search", None), getattr(args, "id", None), getattr(args, "json", False)))
    elif args.command == "info":
        sys.exit(cmd_info())
    elif args.command == "sources":
        sys.exit(cmd_sources(args.jk_only))
    elif args.command == "leads":
        sys.exit(cmd_leads(args.linguistic_only, args.status))
    elif args.command == "varieties":
        sys.exit(cmd_varieties(args.jk_only))
    elif args.command == "grammar":
        sys.exit(cmd_grammar(args.json))
    elif args.command == "validate":
        sys.exit(cmd_validate(args.file))
    elif args.command == "search":
        sys.exit(cmd_search(args.query, args.jk_only, args.no_comparative, args.data))
    elif args.command == "translate":
        sys.exit(cmd_translate(args.query, args.from_lang, args.include_comparative, args.include_cultural, args.data, to_lang=getattr(args, "to_lang", None)))
    elif args.command == "export":
        sys.exit(cmd_export(args.output, args.format, args.jk_only))
    elif args.command in ("word-list", "words", "comparative-words"):
        sys.exit(cmd_word_list(args.search, args.pos, args.limit, args.all, args.json, category_filter=getattr(args, "category", None)))
    elif args.command in ("compare", "compare-varieties"):
        sys.exit(cmd_compare(args.headword))
    elif args.command == "sync":
        sys.exit(cmd_sync(args.check))
    elif args.command in ("stats", "statistics"):
        sys.exit(cmd_stats())
    elif args.command == "numerals":
        sys.exit(cmd_numerals(args.category, args.search, args.json))
    elif args.command == "phonology":
        sys.exit(cmd_phonology(args.section, args.json))
    elif args.command == "examples":
        sys.exit(cmd_examples(args.chapter, args.number, args.search, args.limit, args.json, headword=getattr(args, "headword", None)))
    elif args.command == "sociolinguistics":
        sys.exit(cmd_sociolinguistics(args.section, args.json))
    elif args.command == "references":
        sys.exit(cmd_references(args.search, args.json))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
