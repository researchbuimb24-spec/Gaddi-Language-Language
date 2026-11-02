# Gaddi Language Library (`gaddi`)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Software%20License-MIT-green.svg)](LICENSE)
[![Data Terms: Audited Provenance](https://img.shields.io/badge/Data%20Terms-Audited%20Provenance-orange.svg)](DATA-LICENSE.md)
[![Tests](https://img.shields.io/badge/tests-133%20passed-brightgreen.svg)]()

A computational linguistics and language-documentation Python library for the **Gaddi language (*Bharmauri / Gaddiyali*) as spoken in Jammu & Kashmir (J&K), India**, with rigorously quarantined comparative baselines from Himachal Pradesh.

---

## 1. Mission and Core Linguistic Principles

The primary objective of this project is to build an accurate, searchable, and auditable digital dictionary and linguistic resource for **Jammu & Kashmir Gaddi**.

### Core Tenets:
1. **Accuracy Over Bulk Volume:** A dictionary of verified, authentic words with documented provenance is vastly superior to thousands of unverified or scraped entries.
2. **Geographical Distinction:** Gaddi spoken in Jammu & Kashmir (Kathua, Udhampur, Doda, Kishtwar, Ramban) is geographically, historically, and sociolinguistically distinct from varieties spoken in Himachal Pradesh (Bharmaur/Chamba, Kangra/Palampur, Mandi, Kullu). **Varieties are never merged without empirical evidence.**
3. **Comparative Sources as References, Not Automatic Proof:**
   - The landmark 2026 open-access book *A Grammar of Gaddi* by Kumari et al. (UCL Press) documents the Kangra/Palampur variety (HP). The authors explicitly note that varieties in Chamba, Mandi, Kullu, Punjab, and **Jammu & Kashmir require fresh, dedicated descriptions**.
   - In this library, HP materials (Kumari et al. 2026, Grierson 1916, Census 2023 LSI) serve as valuable **comparative baselines**, but are **never** treated as automatic evidence for J&K vocabulary or grammar.
4. **Strict Traceability & Zero Invention:** Every lexical entry and grammatical rule cites a verifiable primary source. Words, pronunciations, meanings, and examples are **never invented**.
5. **Multi-Script Preservation:** Preserving authentic orthography across **Devanagari**, **Perso-Arabic** (Urdu script), **Latin/IPA**, and historical **Takri**.

---

## 2. Dataset Scale & Inventory

The repository maintains **27 fully synchronized datasets** between `data/` and `src/gaddi/resources/`:

| Dataset | Scope / Description | Entries / Scale | Provenance & Source |
| :--- | :--- | :---: | :--- |
| `data/dictionary_unified.json` | Unified multi-script search database | **1,925 records** | Multi-source (J&K field + comparative HP; 2,470 citations) |
| `data/vocabulary.json` | Research-expanded vocabulary across 16 domains | **101 records** | Dar & Sheikh (2022), Kumari et al. (2026) |
| `data/lexicon_jk.json` | Primary J&K descriptive linguistic lexicon | **105 records** | Hilal Ahmad Dar & Aejaz Mohammed Sheikh (2022) |
| `data/cultural_terms_jk.json` | Traditional material & ecological culture | **25 records** | Kumar (2019), Chandar (2024), Chakraborty (2024) |
| `data/stories.json` | Documented folk tales, legends, and pastoral narratives | **6 records** | Grierson (1916), Kumari et al. (2026), Shashi (1977) |
| `data/songs.json` | Documented folk songs and Ainchali ballads | **6 records** | JKAACL Archive, PLSI (2014), Dar & Sheikh (2022) |
| `data/proverbs.json` | Pastoral proverbs and oral sayings | **6 records** | PLSI (2014), Verma (2014), Shashi (1977) |
| `data/deities.json` | Community pantheon and protector deities | **8 records** | Shashi (1977), Nirmohi, Chakraborty (2024) |
| `data/festivals.json` | Seasonal festivals and sacred cycles (Nawala, Yatra) | **6 records** | Shashi (1977), Chakraborty (2024), Kumar (2019) |
| `data/culture.json` | Pastoral transhumance, attire, looms, and cuisine | **7 records** | Kumari et al. (2026), Shashi (1977), Chandar (2024) |
| `data/oral_history.json` | Historical transhumance accounts & oral testimonies | **3 records** | Dar & Sheikh (2022), Field Informant Testimonies |
| `data/media_resources.json` | Archival recordings and open-access corpus metadata | **3 records** | JKAACL Archives, Grierson LSI, UCL Press OA |
| `data/gaddi_examples.json` | Numbered, interlinear glossed grammar examples | **269 examples** | Kumari et al. (2026), Chapters 1–5 |
| `data/gaddi_word_list.json` | Comparative basic word list (Appendix II) | **254 entries** | Kumari et al. (2026), Table B.1 |
| `data/gaddi_numerals.json` | Numeral system (cardinals, ordinals, fractions) | **138 forms** | Kumari et al. (2026), Appendix III |
| `data/gaddi_grammar.json` | Documented paradigms, affixes, and markers | 7 sections | Kumari et al. (2026), Mehta (2016, 2021) |
| `data/gaddi_phonology.json` | Phonemic inventories & tonal descriptions | 6 sections | Kumari et al. (2026), Bailey (1908) |
| `data/research_leads.json` | Cataloged academic research leads & trackers | **20 leads** | J&K archives, census monographs, field surveys |
| `data/sources.json` | Controlled bibliographic source registry | **21 sources** | 12 J&K primary, 9 comparative/historical |
| `data/varieties.json` | Controlled geographic variety catalog | **11 varieties** | 5 J&K varieties, 6 comparative varieties |

---

## 3. Package Architecture

```text
Gaddi-Language-Library/
├── pyproject.toml              # Packaging configuration (pure standard library dependencies)
├── LICENSE                     # MIT Software License
├── DATA-LICENSE.md             # Data governance, provenance, and cultural heritage terms
├── README.md                   # Project documentation and quickstart
├── data/                       # Authoritative primary JSON datasets (27 datasets)
│   ├── dictionary_unified.json # 1,925-record unified dictionary with audited item-level provenance
│   ├── vocabulary.json         # 101-record research-expanded vocabulary across 16 domains
│   ├── stories.json            # 6 documented folk tales & pastoral narratives
│   ├── songs.json              # 6 documented folk songs & Ainchali ballads
│   ├── proverbs.json           # 6 pastoral proverbs & sayings
│   ├── deities.json            # 8 documented deities & protector traditions
│   ├── festivals.json          # 6 traditional seasonal festivals
│   ├── culture.json            # 7 cultural practices, attire, and crafts records
│   ├── oral_history.json       # 3 oral history and transhumance memory testimonies
│   ├── media_resources.json    # 3 archival audio and corpus metadata records
│   ├── lexicon_jk.json         # 105 authenticated J&K field records
│   ├── cultural_terms_jk.json  # 25 documented cultural/ethnographic terms
│   ├── gaddi_examples.json     # 269 numbered linguistic examples
│   ├── gaddi_word_list.json    # 254 comparative lexical items
│   ├── gaddi_numerals.json     # 138 documented numeral forms
│   ├── gaddi_phonology.json    # Phoneme inventory & contrastive pairs
│   ├── gaddi_grammar.json      # Grammatical paradigms & affix systems
│   ├── research_leads.json     # Cataloged research leads
│   ├── sources.json            # 21 registered bibliographic sources
│   ├── varieties.json          # 11 registered geographical varieties
│   ├── seed_corpus.json        # Curated seed corpus
│   └── source_intake/          # Primary research PDFs (Dar & Sheikh 2022, Grierson LSI, etc.)
├── docs/
│   ├── PROJECT_AUDIT.md        # Comprehensive technical & linguistic audit
│   ├── EXPANSION_RESEARCH_REPORT.md # Provenance remediation and major expansion report
│   ├── DEDUPLICATION_REVIEW.md # Collision-group and attestation preservation audit
│   ├── sources_and_bibliography.md     # Bibliographical survey and reliability assessment
│   ├── jk_gaddi_linguistic_profile.md  # Detailed profile of J&K Gaddi & research gaps
│   ├── jk_gaddi_primary_linguistic_sources.md # Source analysis & citations
│   ├── architecture_and_provenance_spec.md # Technical schema and validation engine specs
│   └── dataset_strategy_and_roadmap.md # Phased acquisition and field validation plan
├── scratch/                    # Data extraction, audit, and verification scripts
├── src/
│   └── gaddi/
│       ├── __init__.py         # Package exports & public API
│       ├── models.py           # Dataclasses (LexicalEntry, OralTradition, Deity, Festival, etc.)
│       ├── registry.py         # Controlled SourceRegistry and VarietyRegistry
│       ├── validator.py        # Strict provenance and anti-conflation validation engine
│       ├── dictionary.py       # Multi-script search & priority translation engine
│       ├── oral_heritage.py    # Stories, songs, proverbs, and oral history registry
│       ├── culture.py          # Deities, festivals, cultural heritage, and media registry
│       ├── grammar.py          # Documented grammatical paradigms & case markers
│       ├── sync.py             # Authoritative data/ vs packaged resources/ synchronization
│       ├── cli.py              # Command-line interface with 28 subcommands
│       └── resources/          # 27 packaged internal synchronized JSON datasets
└── tests/
    ├── test_api.py             # Public API integration tests
    ├── test_audit.py           # Evidence quarantine & census distinction tests
    ├── test_cli.py             # CLI command suite tests
    ├── test_dictionary.py      # Multi-language translation & search tests
    ├── test_grammar.py         # Grammatical paradigm and citation tests
    ├── test_jk_expansion.py    # J&K field lexicon & kinship tests
    ├── test_kumari_2026_extraction.py # Monograph datasets & synchronization tests
    ├── test_models.py          # Data model serialization and immutability tests
    ├── test_oral_heritage_and_culture.py # Oral heritage, deities, and culture tests
    ├── test_quality_and_regression.py # Synchronization, homonym, and Group 19 item tests
    ├── test_registry.py        # Source & variety registry integrity tests
    ├── test_research_leads.py  # Research leads & intake safeguard tests
    ├── test_unified_expansion.py # Search ranking & diacritic tolerance tests
    └── test_validator.py       # Validation engine & conflation-rejection tests
```

---

## 4. Controlled Varieties

| Variety ID | State/UT | District / Region | Primary Sub-Areas | Status in Library |
| :--- | :--- | :--- | :--- | :--- |
| `jk_kathua_bani` | J&K | Kathua | Bani, Duggan, Dhaggar, Billawar, Basohli | **Primary J&K Target** |
| `jk_udhampur_ramnagar`| J&K | Udhampur | Ramnagar, Dudu-Basantgarh, Chenani, Pachound | **Primary J&K Target** |
| `jk_doda_bhadarwah` | J&K | Doda / Kishtwar | Bhadarwah, Assar, Saraj (Chenab valley) | **Primary J&K Target** |
| `jk_bhaderwah_doda` | J&K | Doda | Bhaderwah valley settlements | **Primary J&K Target** |
| `jk_general` | J&K | State-wide | All J&K Gaddi settlements | **General J&K Anchor** |
| `hp_chamba_bharmaur` | HP | Chamba | Bharmaur (Gaderan), Budhil valley | Comparative Baseline |
| `hp_kangra_palampur` | HP | Kangra | Palampur (Saperu, Banuri, Kandbari) | Comparative Baseline |
| `hp_mandi_kullu` | HP | Mandi / Kullu | Peripheral HP settlements | Comparative Reference |
| `historical_gaddi_unspecified_locality` | Historical | Unspecified | LSI / Grierson historical attestations | Historical Reference |

---

## 5. Quickstart & Python API

### Installation
The library uses the Python Standard Library for its core runtime (requires Python >= 3.10):

```bash
git clone https://github.com/researchbuimb24-spec/Gaddi-Language-Language.git
cd Gaddi-Language-Language
pip install -e .
```

### Basic Usage

```python
import gaddi

# 1. Access documented stories and Ainchali ballads
stories = gaddi.get_stories(genre="folktale")
print(stories[0].title_en, stories[0].source_citation)

songs = gaddi.get_songs(genre="ainchali_ballad")
print(songs[0].title_en, songs[0].text_excerpt_gaddi)

# 2. Access deities, festivals, and cultural traditions
deities = gaddi.get_deities()
for deity in deities:
    print(f"[{deity.category}] {deity.name_devanagari} ({deity.name_ipa}): {deity.ritual_roles}")

festivals = gaddi.get_festivals()
for fest in festivals:
    print(f"{fest.name_devanagari}: {fest.timing_lunar_solar}")

# 3. Research-expanded vocabulary across 16 domains
kinship_terms = gaddi.get_vocabulary_entries(domain="family_and_kinship")
print(f"Loaded {len(kinship_terms)} kinship terms from Dar & Sheikh (2022).")
bapu = kinship_terms[0]
print(f"{bapu.lemma_devanagari} [{bapu.lemma_ipa}]: {bapu.senses[0].definition_en}")

# 4. Multi-script search across the unified dictionary
dictionary = gaddi.GaddiDictionary()
results = dictionary.search("handloom")
for entry in results:
    print(f"{entry.lemma_devanagari} ({entry.variety_id}): {entry.senses[0].definition_en}")

# 5. Cross-Variety Comparison (segregating J&K from HP comparative baselines)
comparison = gaddi.compare_varieties("पाणी")
print(comparison["has_jk_evidence"])      # False
print(comparison["has_hp_comparative"])  # True (hp_chamba_bharmaur)
print(comparison["comparative_summary"])  # Explains geographic quarantine
```

---

## 6. Command-Line Interface (CLI)

The library provides 28 specialized CLI subcommands:

```bash
# Display project overview, dataset status, and metrics
gaddi info
gaddi stats

# Stories, ballads, and proverbs
gaddi stories --genre folktale
gaddi songs --genre ainchali_ballad
gaddi proverbs

# Sacred pantheon, festivals, and culture
gaddi deities --category supreme_deity
gaddi festivals --season August
gaddi culture --topic pastoral_migration

# Research-expanded vocabulary
gaddi vocabulary --domain family_and_kinship
gaddi vocabulary --search father

# Universal multi-script dictionary search
gaddi search blanket
gaddi search पाणी

# Cross-variety comparison (segregating J&K from HP baselines)
gaddi compare पाणी
gaddi compare खडे

# Check resource synchronization between authoritative data/ and packaged src/
gaddi sync --check

# Validate a JSON dataset file for provenance and schema integrity
gaddi validate data/lexicon_jk.json
```

---

## 7. Running Tests

```bash
pytest -v
```

All **133 automated tests** pass across 14 test suites (0 failures, 0 errors, 100% green), verifying:
- Serialization, schema immutability, and registry lookups.
- Group 19 item-level provenance preservation (`dʰuːɽ` with item 36 'dust' and item 57 'fog; haze').
- Strict anti-conflation guardrails (preventing labeling an entry as J&K if it only cites HP works).
- Diacritic-tolerant, multi-script search across Devanagari, Perso-Arabic, Latin/IPA, and English/Hindi glosses.
- 100% identical synchronization between all 27 authoritative `data/` files and packaged `src/gaddi/resources/`.
- Provenance tracking, copyright safeguards, and academic licensing distinctions.

---

## 8. Licensing and Data Terms

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Data, Provenance, and Cultural Knowledge:** Governed by [DATA-LICENSE.md](DATA-LICENSE.md) in accordance with the CARE and FAIR Principles for Indigenous Data Governance.
- **Third-Party Academic Citations:**
  - Kumari et al. (*A Grammar of Gaddi*, UCL Press, 2026): Open Access under **CC BY-NC 4.0**.
  - Grierson (LSI, 1916) & Bailey (1908): **Public Domain**.
  - Census of India (2011, 2023): Open Government Data (OGD) India.
  - J&K Academic Publications (Hilal Ahmad Dar & Aejaz Mohammed Sheikh 2022, Banti Kumar 2019, Subhash Chandar 2024, Arka Chakraborty 2024, Prof. Shiv Nirmohi): Fair dealing academic indexing, summary, and excerpt citation.
