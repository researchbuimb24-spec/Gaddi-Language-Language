# Gaddi Language Library (`gaddi`)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Software%20License-MIT-green.svg)](LICENSE)
[![Data Terms: Audited Provenance](https://img.shields.io/badge/Data%20Terms-Audited%20Provenance-orange.svg)](DATA-LICENSE.md)
<<<<<<< HEAD
[![Tests](https://img.shields.io/badge/tests-116%20passed-brightgreen.svg)]()

A comprehensive computational linguistics, multi-lingual dictionary, and language-documentation library for the **Gaddi language (*Bharmauri / Gaddiyali*)**, spoken across Jammu & Kashmir and Himachal Pradesh, India.

---

## 1. Overview & Core Features

The `gaddi` library provides an expanded, fully validated, and multi-script digital language resource containing:

- **1,971 Unified Lexical Entries** covering **1,781 Unique Devanagari Headwords** (deduplicated with 100% preservation of distinct varieties, pronunciations, historical forms, and attestations).
- **105 Verified J&K Fieldwork Lexical Entries** documenting the Bhaderwah (Doda district, Jammu & Kashmir) speech community (Dar & Sheikh 2022).
- **2,472 Source Attestation Records** with exact bibliographic and fieldwork provenance.
- **1,990 Distinct Alternate Forms and Phonetic Variants** across Devanagari, IPA, Romanized spellings, Perso-Arabic, and Takri.
- **19 Standardized Topic Categories** (Family, Body, Animals, Plants, Food, Water, Mountains, Agriculture, Household, Tools, Travel, Numbers, Colors, Actions, Nature, Religion, Education, Expressions, General).
- **Multi-Lingual Translation Support** across **6 Languages**: English ↔ Gaddi, Hindi ↔ Gaddi, Urdu ↔ Gaddi, Punjabi ↔ Gaddi, and Dogri ↔ Gaddi.
- **Comprehensive Grammar Engine**: Noun declensions, gender/number agreement, demonstratives, inflecting adjectives, postpositions, TAM verbal paradigms, copula systems, split-ergativity, prohibitive imperatives, interrogatives, clause types, and morphological derivations.
- **Complete Numeral System**: 138 forms (104 cardinals 1–100+, 22 ordinals 1st–22nd, 7 fractionals, 5 distributives).
- **269 Numbered Linguistic Examples** with interlinear morpheme glosses explicitly cross-referenced to dictionary entries.
- **Rigorous Provenance & Anti-Conflation Safeguards**: Clear geographical separation between Jammu & Kashmir varieties (`jk_bhaderwah_doda`, `jk_doda_bhadarwah`, `jk_kathua_bani`, `jk_general`) and Himachal Pradesh baselines (`hp_chamba_bharmaur`, `hp_kangra_palampur`). Zero manufactured or hallucinated words.

---

## 2. Corpus Statistics

All statistics are computed directly from the verified underlying datasets (`data/dictionary_unified.json`, `data/lexicon_jk.json`, `data/gaddi_examples.json`, `data/gaddi_numerals.json`):

| Metric | Count | Details / Authority |
| :--- | :--- | :--- |
| **Total Unified Entries** | **1,971** | Deduplicated across Jambu, Kumari 2026, Grierson, Bailey, Census 2023, and Dar & Sheikh 2022 J&K field realia |
| **Unique Headwords (Devanagari)** | **1,781** | Distinct lemmatized headwords |
| **Verified J&K Field Lexical Entries** | **105** | Primary field documentation from Bhaderwah, Doda, J&K (Dar & Sheikh 2022) |
| **Total Lexical Attestations** | **2,472** | Traceable bibliographic and fieldwork citations |
| **Alternate Forms & Variants** | **1,990** | Spelling, historical, script, and phonemic variants |
| **Linked Example References** | **1,211** | Direct links from 583 entries to authentic grammar sentences |
| **Standardized Topic Categories** | **19** | Domain classifications covering material and daily life |
| **Category Assignment Total** | **2,202** | Multi-label domain assignments across entries (see note below) |
| **Documented Numbered Examples** | **269** | Interlinear morpheme-by-morpheme parsed sentences |
| **Documented Numeral Forms** | **138** | Cardinals (104), Ordinals (22), Fractionals (7), Distributives (5) |
| **Controlled Varieties** | **8** | 4 Jammu & Kashmir, 4 Himachal Pradesh / Historical |
| **Automated Tests** | **116** | 100% passing test suite across models, dictionary, API, CLI, grammar, and J&K expansion |

> [!NOTE]
> **Category Multi-Labeling**: The sum of category entries (2,202) exceeds the number of unique lexical entries (1,971) because culturally multifaceted words are assigned to multiple relevant domains (e.g., *bheḍ* 'sheep' belongs to both *animals* and *agriculture*; *charkha* belongs to *tools*, *household*, and *animals*).

### Descriptive Translation Coverage
Translation coverage reflects authentic descriptive literature gloss availability, not synthetic generation:
- **English (`en`)**: 1,971 / 1,971 entries (100.0%)
- **Hindi (`hi`)**: 1,489 / 1,971 entries (75.5%)
- **Urdu (`ur`)**: 431 / 1,971 entries (21.9%)
- **Punjabi (`pa`) & Dogri (`doi`)**: Core shared Western Pahari lexical mappings

### Topic Category Distribution

| Category | Entries | Representative Words |
| :--- | :--- | :--- |
| **General & Descriptive** | 631 | Core modifiers, pronouns, conjunctions, and root forms |
| **Numbers & Quantities** | 247 | इक्क (1), दो (2), त्रै (3), बीह (20), सोह (100), अद्ध (1/2), पहला (1st) |
| **Expressions & Discourse** | 240 | कुण (who), क्या / के (what), कित्थी (where), जद (when), बले बले (slowly), जोरे जोरे (loudly) |
| **Family & Kinship** | 148 | बाप (father), मा (mother), माबुरा (parents), भाई (brother), धी (daughter), पुत्त (son) |
| **Body Parts & Health** | 137 | सिर (head), अक्ख / आँख (eye), दाँद (tooth), जीभ (tongue), हत्थ (hand), पैर (foot) |
| **Animals & Pastoral Life** | 122 | भेड़ (sheep), बकरी (goat), गा (cow), घोड़ा (horse), कुत्तर (dog), कड़पा (snake) |
| **Actions & Verbs** | 108 | खाणा (eat), पीणा (drink), जाणा (go), औणा (come), बोलणा (speak), दिखणा (see) |
| **Travel & Directions** | 87 | राह (path), सड़क (road), इत्थी (here), तित्थी (there), खाबी कणारे (left bank) |
| **Colors & Qualities** | 76 | काला (black), चिट्टा (white), लाल (red), पीळा (yellow), शैल (beautiful) |
| **Nature & Environment** | 53 | धरती (earth), अम्बर (sky), सूरज (sun), चानणी (moon), तारा (star), आग (fire) |
| **Water, Weather & Seasons** | 52 | पाणी (water), ब्यारी (wind), बरखा (rain), हेउँ / हियुँ (snow), छंब (lake) |
| **Food & Cooking** | 51 | रोटी (bread), भात (rice), दुद्ध (milk), घ्यो / घीउ (ghee), लूण (salt) |
| **Household & Clothing** | 39 | चोला (tunic), डोरा (cord), पट्टू (blanket), खडे (loom), घर (house) |
| **Plants & Trees** | 39 | बूटा / पेड़ (tree), पत्तर (leaf), बरघट (banyan), फुल्ल (flower), गाह (grass) |
| **Mountains & Landscapes** | 31 | धार (ridge), अंगारी (mountain), नद्दी (river), जोत (high pass) |
| **Education & Technology** | 30 | किताब (book), स्कूल (school), पढ़ाई (study), मास्टर (teacher) |
| **Tools & Trades** | 26 | कुल्हाड़ी (axe), खडे (handloom), डाची (sickle), फुट्टी (club) |
| **Agriculture & Herding** | 22 | बल्द (ox), खेतर (field), माल (flock/livestock), चराई (grazing) |
| **Religion & Traditions** | 15 | नवाला (Shiva worship), अंचली (hymn), पूजा (worship), कैलाश (sacred peak) |

---

## 3. Installation

The library requires Python >= 3.10 and relies exclusively on the Python standard library for runtime execution:
=======
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)]()

A computational linguistics and language-documentation Python library for the **Gaddi language (*Bharmauri / Gaddiyali*) as spoken in Jammu & Kashmir (J&K), India**.

---

## 1. Mission and Core Linguistic Principles

The primary objective of this project is to build an accurate, searchable, and auditable digital dictionary and linguistic resource for **Jammu & Kashmir Gaddi**.

### Core Tenets:
1. **Accuracy Over Bulk Volume:** A dictionary of 100 fully verified, authentic words is vastly superior to thousands of guessed or scraped entries.
2. **Geographical Distinction:** Gaddi spoken in Jammu & Kashmir (Kathua, Udhampur, Doda, Kishtwar, Ramban) is geographically, historically, and sociolinguistically distinct from varieties spoken in Himachal Pradesh (Bharmaur/Chamba, Kangra/Palampur, Mandi, Kullu). **Varieties are never merged without empirical evidence.**
3. **Comparative Sources as References, Not Automatic Proof:**
   - The landmark 2026 open-access book *A Grammar of Gaddi* by Kumari et al. (UCL Press) documents the Kangra/Palampur variety (HP). The authors explicitly note that varieties in Chamba, Mandi, Kullu, Punjab, and **Jammu & Kashmir require fresh, dedicated descriptions**.
   - In this library, HP materials (Kumari et al. 2026, Grierson 1916) serve as valuable **comparative baselines**, but are **never** treated as automatic evidence for J&K vocabulary or grammar.
4. **Strict Traceability & Zero Invention:** Every lexical entry and grammatical rule must cite a verifiable primary source. Words, pronunciations, meanings, and examples are **never invented**.
5. **Multi-Script Preservation:** Preserving original orthography across **Devanagari**, **Perso-Arabic** (Urdu script), **Latin/IPA**, and historical **Takri**.

---

## 2. Translation Pipeline Priority

Entries in the dictionary are indexed and translated according to the following strict priority:

```text
Priority 1: English  (International accessibility & scientific documentation)
    ↓
Priority 2: Hindi    (National and regional educational lingua franca)
    ↓
Priority 3: Urdu     (Historical and administrative state language of J&K)
    ↓
Priority 4: Other    (Dogri, Gojri, Kashmiri contact glosses where documented)
```

---

## 3. Package Architecture

```text
Gaddi-Language-Library/
├── pyproject.toml              # Packaging configuration (pure standard library dependencies)
├── LICENSE                     # MIT Software License
├── DATA-LICENSE.md             # Data governance, provenance, and cultural heritage terms
├── README.md                   # Project documentation and quickstart
├── data/
│   ├── sources.json            # Controlled bibliographic source catalog
│   ├── varieties.json          # Controlled geographical variety registry
│   └── seed_corpus.json        # Curated, source-verified seed corpus (zero synthetic words)
├── docs/
│   ├── sources_and_bibliography.md     # Bibliographical survey and reliability assessment
│   ├── jk_gaddi_linguistic_profile.md  # Detailed profile of J&K Gaddi & research gaps
│   ├── architecture_and_provenance_spec.md # Technical schema and validation engine specs
│   └── dataset_strategy_and_roadmap.md # Phased acquisition and field validation plan
├── src/
│   └── gaddi/
│       ├── __init__.py         # Package exports & version
│       ├── models.py           # Dataclasses (LexicalEntry, Sense, Source, Variety, etc.)
│       ├── registry.py         # Controlled SourceRegistry and VarietyRegistry
│       ├── validator.py        # Strict provenance and anti-conflation validation engine
│       ├── dictionary.py       # Multi-script search & priority translation engine
│       ├── grammar.py          # Documented grammatical paradigms & case markers
│       ├── cli.py              # Command-line interface
│       └── resources/          # Packaged internal registry JSON files
└── tests/
    ├── test_models.py          # Data model serialization and immutability tests
    ├── test_registry.py        # Source & variety registry integrity tests
    ├── test_validator.py       # Validation engine & conflation-rejection tests
    ├── test_dictionary.py      # Multi-language translation & search tests
    └── test_grammar.py         # Grammatical paradigm and citation tests
```

---

## 4. Controlled Varieties

| Variety ID | State/UT | District / Region | Primary Sub-Areas | Status in Library |
| :--- | :--- | :--- | :--- | :--- |
| `jk_kathua_bani` | J&K | Kathua | Bani, Duggan, Dhaggar, Billawar, Basohli | **Primary J&K Target** |
| `jk_udhampur_ramnagar`| J&K | Udhampur | Ramnagar, Dudu-Basantgarh, Chenani, Pachound | **Primary J&K Target** |
| `jk_doda_bhadarwah` | J&K | Doda / Kishtwar | Bhadarwah, Assar, Saraj (Chenab valley) | **Primary J&K Target** |
| `jk_general` | J&K | State-wide | All J&K Gaddi settlements | **General J&K Anchor** |
| `hp_chamba_bharmaur` | HP | Chamba | Bharmaur (Gaderan), Budhil valley | Comparative Baseline |
| `hp_kangra_palampur` | HP | Kangra | Palampur (Saperu, Banuri, Kandbari) | Comparative Baseline |
| `hp_mandi_kullu` | HP | Mandi / Kullu | Peripheral HP settlements | Comparative Reference |

---

## 5. Quickstart & Python API

### Installation
The library uses the Python Standard Library for its core runtime (requires Python >= 3.10):
>>>>>>> origin/main

```bash
git clone https://github.com/researchbuimb24-spec/Gaddi-Python-Language.git
cd Gaddi-Python-Language
pip install -e .
```

<<<<<<< HEAD
---

## 4. Python API Usage

The high-level `gaddi` module provides convenient, consistent functions:

```python
import gaddi

# 1. High-level library metadata and counts
info = gaddi.info()
print(f"Unified entries:   {info['unified_total_entries']}")  # 1866
print(f"Unique headwords:  {info['unique_headwords']}")       # 1682
print(f"Categories:        {info['categories_count']}")        # 19

# 2. Multi-Lingual Translation (Command 12 API)
# English -> Gaddi
res_en = gaddi.translate("water", source="en", target="gaddi")
print([e.lemma_devanagari for e in res_en])  # ['पाणी', 'पाणि', 'कú', 'बिजन']

# Hindi -> Gaddi
res_hi = gaddi.translate("पानी", source="hi", target="gaddi")
print([e.lemma_devanagari for e in res_hi])  # ['पाणी', 'पाणि', 'कú', 'बिजन']

# Regional languages (Urdu, Punjabi, Dogri) -> Gaddi
res_ur = gaddi.translate("پانی", source="ur", target="gaddi")
res_pa = gaddi.translate("ਪਾਣੀ", source="pa", target="gaddi")
res_doi = gaddi.translate("पाणी", source="doi", target="gaddi")

# Gaddi -> English / Hindi
res_to_en = gaddi.translate("पाणी", source="gaddi", target="en")

# 3. Topic Category Search
animals = gaddi.search_by_category("animals")
family = gaddi.search_by_category("family")
food = gaddi.search_by_category("food")
print(f"Found {len(animals)} animals, {len(family)} kinship terms, {len(food)} food items")

# 4. Synonyms, Variants, and Linked Examples
synonyms = gaddi.get_synonyms("पाणी")
variants = gaddi.get_variants("पाणी")
print(f"Variants: {variants}")  # ['पाणी', 'ˈpaːɳiː', 'pʌːɳiː', 'pāṇī', 'pani', 'paṇi']

# Retrieve numbered grammar examples linked directly to a headword
exs_pani = gaddi.get_examples_for_headword("पाणी")
for ex in exs_pani[:2]:
    print(f"Ex #{ex['example_number']}: {ex['raw_text']}")

examples = gaddi.get_examples("water")
for ex in examples[:2]:
    print(f"Ex #{ex['example_number']}: {ex['raw_text']}")

# 5. Numerals, Phonology, Morphology, and Grammar Overview
numerals = gaddi.get_numerals()
grammar = gaddi.get_grammar()
morphology = gaddi.get_morphology()
phonology = gaddi.get_phonology()

# 6. Registries and Variety Listings
varieties = gaddi.list_varieties()
sources = gaddi.list_sources()

# 7. Backward-compatible strict J&K lookup
res_strict = gaddi.translate("handloom", from_lang="en")  # [] (truthful zero-guess)
res_cult = gaddi.translate("handloom", from_lang="en", include_cultural=True)  # [खडे]
=======
### Basic Usage

```python
from gaddi import GaddiDictionary

# Initialize dictionary and load verified dataset
dictionary = GaddiDictionary()
dictionary.load_from_json("data/seed_corpus.json")

# 1. Priority 1: English -> Gaddi Lookup
results = dictionary.lookup_english("handloom")
for entry in results:
    print(f"{entry.lemma_devanagari} ({entry.variety_id}): {entry.senses[0].definition_en}")
# Output: खडे (jk_doda_bhadarwah): Traditional wooden handloom...

# 2. Priority 2: Hindi -> Gaddi Lookup
results = dictionary.lookup_hindi("हथकरघा")
print(results[0].lemma_devanagari)  # खडे

# 3. Priority 3: Urdu -> Gaddi Lookup
results = dictionary.lookup_urdu("چوغہ")
print(results[0].lemma_devanagari)  # चोला

# 4. Multi-script Gaddi Headword Lookup
by_deva = dictionary.lookup_gaddi("नवाला")
by_urdu = dictionary.lookup_gaddi("نوالہ")
by_ipa  = dictionary.lookup_gaddi("nəˈwaːlaː")

# 5. Strict J&K Filtering (Excluding comparative HP entries)
jk_only_results = dictionary.lookup_english("who", jk_only=True)
print(len(jk_only_results))  # 0 (Kumari et al. Kangra entry 'कुण' is excluded)
```

### Running Validation on Datasets

```python
from gaddi import GaddiValidator, LexicalEntry

validator = GaddiValidator()
# Validate any custom entry or file
report = validator.validate_collection(my_entries)
if not report.is_valid:
    for error in report.errors:
        print(f"Error in {error.entry_id}: {error.message}")
>>>>>>> origin/main
```

---

<<<<<<< HEAD
## 5. Command-Line Interface (CLI)

The library provides the `gaddi` command (or `python -m gaddi.cli`):

```powershell
# Display comprehensive corpus statistics and category breakdown
python -m gaddi.cli stats

# Search dictionary across all scripts and definitions
python -m gaddi.cli search water

# Multi-lingual translations
python -m gaddi.cli translate "water" --from en --to gaddi
python -m gaddi.cli translate "पानी" --from hi --to gaddi
python -m gaddi.cli translate "घोड़ा" --from hi --to gaddi

# Browse vocabulary by category
python -m gaddi.cli word-list --category animals
python -m gaddi.cli word-list --category family
python -m gaddi.cli word-list --category food

# Search numbered linguistic examples
python -m gaddi.cli examples --search water
python -m gaddi.cli examples --headword पाणी
python -m gaddi.cli examples --chapter 3 --limit 5

# Inspect documented grammar paradigms and rules
python -m gaddi.cli grammar
python -m gaddi.cli grammar --json

# Browse numeral paradigms (cardinals, ordinals, fractionals, distributives)
python -m gaddi.cli numerals
python -m gaddi.cli numerals --category cardinals
python -m gaddi.cli numerals --search "1"

# Inspect phonology inventory and sound discrepancies
python -m gaddi.cli phonology --section vowels

# Validate dataset files for schema and provenance integrity
python -m gaddi.cli validate

# Export dictionary to JSON or CSV
python -m gaddi.cli export --format json -o gaddi_export.json
python -m gaddi.cli export --format csv -o gaddi_export.csv
=======
## 6. Command-Line Interface (CLI)

The package provides a built-in command-line tool `gaddi`:

```bash
# Display project information and catalog status
gaddi info

# List registered bibliographic sources and licenses
gaddi sources

# List registered geographic varieties (J&K vs HP)
gaddi varieties

# View documented grammatical paradigms and case markers
gaddi grammar

# Validate a JSON dataset file for provenance and schema integrity
gaddi validate data/seed_corpus.json

# Search dictionary across English, Hindi, Urdu, and Gaddi
gaddi search "blanket" --data data/seed_corpus.json
>>>>>>> origin/main
```

---

<<<<<<< HEAD
## 6. Grammar & Linguistic Architecture

The grammar engine (`src/gaddi/grammar.py`) incorporates structured analyses extracted from descriptive fieldwork and literature:

1. **Noun Classes & Declensions**:
   - Class I: Masculine nouns ending in *-a* (छोकरा / *chokra* = boy), direct plural in *-e* (छोकरे / *chokre*).
   - Class II: Masculine consonant-ending nouns (घर / *ghar* = house), direct plural invariant.
   - Class III: Feminine nouns ending in *-i* (छोकरी / *chokri* = girl), plural in *-iyan*.
   - Class IV: Feminine consonant-ending nouns (रात / *raat* = night), plural in *-an* (रातां).
   - Oblique Case: Singular masculine *-a* shifts to *-e* before postpositions; plural nouns take oblique suffix *-an*.
2. **Gender & Number**:
   - Two grammatical genders (Masculine, Feminine) and two numbers (Singular, Plural). Adjectives and verbs agree in gender and number.
3. **Pronominal & Demonstrative System**:
   - Proximal: Direct SG ई (*iː*), Direct PL ए (*eː*), Oblique SG इस (*ɪs*), Oblique PL इन्हां (*ɪnʱaː*).
   - Distal: Direct SG ऊ (*uː*), Direct PL ओ (*oː*), Oblique SG उस (*ʊs*), Oblique PL उन्हों (*ʊnʱoː*).
   - Relative: Direct जो (*dʒo*), Oblique जिस (*dʒɪs*).
4. **Adjectives & Comparison**:
   - Inflecting adjectives ending in *-a* (काला / *kale* / *kali*).
   - Non-inflecting invariant adjectives (शैल / *ʃɛl* = beautiful, साफ / *saːpʰ* = clean).
   - Periphrastic comparison using ablative marker कन्हार (*kanhār*) or ते (*te*) (e.g. *सब ते शैल* = most beautiful).
5. **Verbal System & TAM**:
   - Present Imperfective: stem + *-da* + copula है (*hɛ*) (e.g. खांदा है = eats).
   - Past Imperfective: stem + *-da* + past copula था (*tʰaː*) (e.g. खांदा था = was eating).
   - Perfective: stem + *-eya/-ya* (e.g. खाया = ate).
   - Future: stem + *-ga / -la* (e.g. खाएगा / खालो = will eat).
   - Copula forms: Indicative SG है, PL हन; Past MSG था, FSG थी, MPL थे, FPL थियाँ.
   - Negative copula: Suppletive invariant नथी (*nətʰi* = is not / does not exist).
6. **Split Ergativity**:
   - Ergative-Absolutive alignment in perfective aspect (transitive subjects marked with agentive postposition ने *ne*; verb agrees with object).
   - Nominative-Accusative alignment in imperfective and future aspects.
7. **Negation & Imperatives**:
   - Sentential declarative negation: Pre-verbal particle नी (*niː*).
   - Negative copula: नथी (*nətʰi*).
   - Dedicated prohibitive particle: मथ (*matʰ*) used exclusively with imperative verb stems (e.g. *मथ जा* = do not go!, *मथ बोल* = don't speak!).
8. **Word Order & Clauses**:
   - Strict canonical Subject-Object-Verb (SOV) order.
   - Coordination: ते (*te* = and), पर (*pər* = but), या (*jaː* = or).
   - Subordination: Complementizer कि (*kɪ*), Relative-correlative जो...सो... (*jo...so...*), Conditionals जे...तां... (*je...taan...*).

---

## 7. Data Sources & Licensing Attribution

- **Software Code**: Licensed under the [MIT License](LICENSE).
- **Data & Provenance Governance**: Governed by [DATA-LICENSE.md](DATA-LICENSE.md) in accordance with the **CARE Principles** (Collective Benefit, Authority to Control, Responsibility, Ethics) and **FAIR Principles** for Indigenous Data.
- **Core Integrated Datasets**:
  - **Aryaman Arora & CLDF Jambu Collection (2023–2026)**: 1,118 comparative Gaddi forms aggregated from the Census 2023 Mother Tongue Survey of Himachal Pradesh, Kumari et al. 2026, Grierson 1928, Zoller 2023, and CDIAL.
  - **Kumari et al. (UCL Press, 2026)**: *A Grammar of Gaddi*, Open Access under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Extracted across 9 structured datasets: Appendix II basic word list (254 items), Appendix III numerals (138 forms), 269 numbered examples, phonetics, and morphosyntax.
  - **Sir George A. Grierson (LSI, 1916–1928)** & **Rev. T. Grahame Bailey (1908)**: Public Domain historical Western Pahari dialect surveys.
  - **Jammu & Kashmir Field & Academic Sources**: Dr. Banti Kumar (2019), Subhash Chandar (2024), and Arka Chakraborty (2024) for authentic J&K cultural realia, ritual vocabulary, and toponyms.
  - **Census of India (2011)**: Open Government Data (OGD) License India.

---

## 8. Automated Verification Suite

Run the full automated test suite (107 tests):
=======
## 7. Running Tests
>>>>>>> origin/main

```bash
pytest -v
```

<<<<<<< HEAD
The test suite validates:
- Multi-lingual translation accuracy across English, Hindi, Urdu, Punjabi, Dogri, and Gaddi.
- Strict anti-conflation policies (separating J&K fieldwork from HP comparative data).
- Topic categorization across all 19 standardized domains.
- Numeral and grammar paradigm completeness.
- Numbered example indexing and text search.
- Backward compatibility of the legacy strict lookup engine.
- Byte-synchronization between `data/` and packaged resources `src/gaddi/resources/`.
=======
All 20 test cases verify:
- Complete roundtrip serialization of models.
- Controlled variety and source registries.
- Strict anti-conflation guardrails (preventing labeling an entry as J&K if it only cites non-J&K comparative works).
- Multi-script search accuracy across English, Hindi, Urdu, and Gaddi.

---

## 8. Licensing and Data Terms

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Data, Provenance, and Cultural Knowledge:** Governed by [DATA-LICENSE.md](DATA-LICENSE.md) in accordance with the CARE and FAIR Principles for Indigenous Data Governance.
- **Third-Party Academic Citations:**
  - Kumari et al. (UCL Press, 2026): Open Access under **CC BY 4.0**.
  - Grierson (LSI, 1916) & Bailey (1908): **Public Domain**.
  - J&K Academic Papers (Banti Kumar 2019, Subhash Chandar 2024, Chakraborty 2024, Shiv Nirmohi): Fair dealing academic indexing and citation.

>>>>>>> origin/main
