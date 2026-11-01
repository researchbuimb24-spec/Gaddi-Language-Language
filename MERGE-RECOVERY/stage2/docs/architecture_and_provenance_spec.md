# Technical Architecture and Provenance Specification

This document details the software architecture, data provenance schema, and validation rules for the `gaddi` Python library.

---

## 1. Architectural Principles

1. **Linguistic Truthfulness Over Bulk Quantity:** No unverified, guessed, or synthetic words are allowed. Every entry must possess an unassailable audit trail back to a credible primary or academic source.
2. **Geographical Distinction:** Varieties from Jammu & Kashmir must be structurally separated from Himachal Pradesh varieties. Comparative forms from HP (e.g., Kumari et al. 2026 or Grierson 1916) must be labeled as `comparative_only` until verified in J&K.
3. **Multi-Script Fidelity:** Preserving original orthography across Devanagari (`Deva`), Perso-Arabic (`Arab`), Latin/IPA (`Latn`), and Takri (`Takr`), including original diacritics and source spellings.
4. **Minimal Runtime Dependencies:** Standard Python library only (`json`, `dataclasses`, `pathlib`, `typing`, `unicodedata`, `re`, `sqlite3`). `pytest` is reserved for development and verification.
5. **Hierarchical Translation Priority:**
   - 1. **English ΓåÆ Gaddi**
   - 2. **Hindi ΓåÆ Gaddi**
   - 3. **Urdu ΓåÆ Gaddi**
   - 4. Other source languages only when verified data is available.

---

## 2. Package Structure (`src/gaddi/`)

```text
src/gaddi/
Γö£ΓöÇΓöÇ __init__.py           # Package exports, version, and public functional API
Γö£ΓöÇΓöÇ models.py             # Strongly typed dataclasses for entries, senses, sources, varieties
Γö£ΓöÇΓöÇ registry.py           # Controlled registries for Sources and Varieties
Γö£ΓöÇΓöÇ validator.py          # Data audit and anti-conflation validation engine
Γö£ΓöÇΓöÇ dictionary.py         # Search engine and priority-based multi-language translation lookup
Γö£ΓöÇΓöÇ grammar.py            # Morphological paradigms, phonological inventory, and case markers
Γö£ΓöÇΓöÇ cli.py                # Command-line interface for dictionary queries, translations, validation
ΓööΓöÇΓöÇ resources/            # Embedded packaged resources
    Γö£ΓöÇΓöÇ sources.json              # Controlled source catalog
    Γö£ΓöÇΓöÇ varieties.json            # Controlled geographic variety registry
    Γö£ΓöÇΓöÇ lexicon_jk.json           # Verified J&K descriptive linguistic lexicon (strictly verified)
    Γö£ΓöÇΓöÇ cultural_terms_jk.json    # J&K cultural, ritual, and regional ecological terms (quarantined)
    ΓööΓöÇΓöÇ lexicon_comparative.json  # Quarantined comparative HP baseline entries
```

---

## 3. Data Provenance Schema

### 3.1 Controlled Varieties (`data/varieties.json`)
Every entry must reference a valid `variety_id` from the controlled variety registry:

```json
{
  "id": "jk_kathua_bani",
  "name": "Bani Gaddi",
  "state_ut": "Jammu and Kashmir",
  "district": "Kathua",
  "tehsil": "Bani",
  "is_jk_variety": true,
  "description": "Variety spoken in the high-altitude villages and migratory paths of Bani tehsil bordering Chamba."
}
```

### 3.2 Controlled Sources (`data/sources.json`)
Every entry must cite a valid `source_id` registered in the source catalog:

```json
{
  "id": "kumari_2026",
  "title": "A Grammar of Gaddi",
  "authors": ["Preeti Kumari", "Shreya Mehta", "Anjali Nair", "Anusuya Nayak", "Yangchen Roy", "Vyom Sharma"],
  "year": 2026,
  "publisher": "UCL Press, London",
  "variety_id": "hp_kangra_palampur",
  "credibility_tier": 1,
  "license": "CC BY-NC 4.0",
  "is_jk_primary": false,
  "evidence_type": "descriptive_grammar_phonology",
  "notes": "Valuable comparative grammar of Kangra/Palampur variety (CC BY-NC 4.0; non-commercial only). Explicitly states J&K requires fresh descriptions."
}
```

### 3.3 Lexical and Cultural Entry Schema
The unit of storage for dictionary entries:

```json
{
  "id": "jk-cult-00001",
  "lemma_devanagari": "αñ¿αñ╡αñ╛αñ▓αñ╛",
  "lemma_ipa": "n╔Ö╦êwa╦Éla╦É",
  "lemma_perso_arabic": "┘å┘ê╪º┘ä█ü",
  "lemma_takri": null,
  "part_of_speech": "noun",
  "gender": "masculine",
  "variety_id": "jk_general",
  "evidence_status": "jk_cultural_term",
  "senses": [
    {
      "sense_index": 1,
      "definition_en": "An all-night thanksgiving ritual ceremony and sacrifice dedicated to Lord Shiva",
      "definition_hi": "αñ¡αñùαñ╡αñ╛αñ¿ αñ╢αñ┐αñ╡ αñòαÑï αñ╕αñ«αñ░αÑìαñ¬αñ┐αññ αñ░αñ╛αññ αñ¡αñ░ αñÜαñ▓αñ¿αÑç αñ╡αñ╛αñ▓αñ╛ αñºαñ¿αÑìαñ»αñ╡αñ╛αñª αñöαñ░ αñ¬αÑéαñ£αñ╛ αñàαñ¿αÑüαñ╖αÑìαñáαñ╛αñ¿",
      "definition_ur": "╪¿┌╛┌»┘ê╪º┘å ╪┤█î┘ê ┌⌐█î ┘å╪░╪▒ ┌⌐█î ╪¼╪º┘å█Æ ┘ê╪º┘ä█î ╪▒╪º╪¬ ╪¿┌╛╪▒ ┌⌐█î ┘à╪«╪╡┘ê╪╡ ┘╛┘ê╪¼╪º ┌⌐█î ╪▒╪│┘à",
      "semantic_field": "religion_and_ritual",
      "examples": [
        {
          "text_gaddi": "αñ╢αñ┐αñ╡ αñ¿αñ╡αñ╛αñ▓αÑç αñªαÑÇ αñ░αñ╛αññ αñàαñéαñÜαñ▓αÑÇ αñùαñ╛αñ»αÑÇ αñ£αñ╛αñéαñªαÑÇ αñ╣αÑçαÑñ",
          "translation_en": "On the night of Shiv Nawala, Ainchali hymns are sung.",
          "translation_hi": "αñ╢αñ┐αñ╡ αñ¿αñ╡αñ╛αñ▓αÑç αñòαÑÇ αñ░αñ╛αññ αñàαñéαñÜαñ▓αÑÇ αñùαñ╛αñê αñ£αñ╛αññαÑÇ αñ╣αÑêαÑñ",
          "translation_ur": "╪┤█î┘ê ┘å┘ê╪º┘ä█Æ ┌⌐█î ╪▒╪º╪¬ ╪ó┘å┌å┘ä█î ┌»╪º╪ª█î ╪¼╪º╪¬█î █ü█Æ█ö",
          "source_citation": "nirmohi_duggar, p. 112"
        }
      ]
    }
  ],
  "attestations": [
    {
      "source_id": "chakraborty_2024",
      "page_or_section": "p. 3",
      "source_spelling": "Nawala",
      "context": "Traditional thanksgiving ritual dedicated to Lord Shiva performed across Gaddi households in J&K."
    }
  ],
  "comparative_notes": "Cognate with Chamba Gaddi 'nuala' / 'nawala' documented in Grierson (1916).",
  "metadata": {
    "created_at": "2026-10-30",
    "compiler": "Gaddi Language Project",
    "confidence_score": 1.0
  }
}
```

---

## 4. Strict Validation Engine Rules

The validation engine (`gaddi.validator`) enforces linguistic integrity by raising hard failures or warnings:

### Hard Failures (Rejects Entry)
1. **Missing Source ID:** Any entry lacking `attestations` or citing an unregistered `source_id`.
2. **Missing or Invalid Variety:** Any entry without a `variety_id` or with a variety not in `data/varieties.json`.
3. **Missing Headword Representation:** Entry missing both Devanagari and Latin/IPA representations.
4. **Empty Senses:** Entry lacking at least one valid sense definition.
5. **Duplicate Conflict:** Multiple entries with identical headword and identical variety unless explicitly differentiated by homonym indices.
6. **Conflated Provenance:** An entry labeled `is_jk_variety: true` whose only source is an HP-specific source (e.g. `kumari_2026` or `mehta_2016`) without local verification.

### Warnings (Requires Attention)
1. Missing IPA transcription when Devanagari is provided.
2. Missing Urdu definition (Urdu is Priority 3).
3. Missing Hindi definition (Hindi is Priority 2).
4. Unattested example sentence (example without explicit source citation).
5. Status labeled `provisional` or `disputed`.

---

## 5. Search Engine and Translation Lookup Logic

The `gaddi.dictionary` engine implements:
1. **Targeted Script Matching:** Supports queries in English, Hindi (Devanagari), Urdu (Perso-Arabic), Gaddi (Devanagari, Perso-Arabic, Latin, Takri).
2. **Variety Filtering:**
   - Default behavior: Queries return J&K varieties first.
   - Explicit flag: `jk_only=True` strictly excludes comparative HP entries.
   - Comparative mode: `include_comparative=True` allows viewing Kangra/Chamba cognates clearly segregated under a comparative badge.
3. **Exact & Prefix Matching:** Normalizes Unicode (NFC), strips combining accents where appropriate for fuzzy search while preserving them for display.

