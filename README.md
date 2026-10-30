# Gaddi Language Library (`gaddi`)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Software%20License-MIT-green.svg)](LICENSE)
[![Data Terms: Audited Provenance](https://img.shields.io/badge/Data%20Terms-Audited%20Provenance-orange.svg)](DATA-LICENSE.md)
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

```bash
git clone https://github.com/researchbuimb24-spec/Gaddi-Python-Language.git
cd Gaddi-Python-Language
pip install -e .
```

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
```

---

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
```

---

## 7. Running Tests

```bash
pytest -v
```

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

