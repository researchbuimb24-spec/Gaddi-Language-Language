# Gaddi Language Library (`gaddi`)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Software%20License-MIT-green.svg)](LICENSE)
[![Data Terms: Audited Provenance](https://img.shields.io/badge/Data%20Terms-Audited%20Provenance-orange.svg)](DATA-LICENSE.md)
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
- **Multi-Lingual Translation Support** across **6 Languages**: English Γåö Gaddi, Hindi Γåö Gaddi, Urdu Γåö Gaddi, Punjabi Γåö Gaddi, and Dogri Γåö Gaddi.
- **Comprehensive Grammar Engine**: Noun declensions, gender/number agreement, demonstratives, inflecting adjectives, postpositions, TAM verbal paradigms, copula systems, split-ergativity, prohibitive imperatives, interrogatives, clause types, and morphological derivations.
- **Complete Numeral System**: 138 forms (104 cardinals 1ΓÇô100+, 22 ordinals 1stΓÇô22nd, 7 fractionals, 5 distributives).
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
> **Category Multi-Labeling**: The sum of category entries (2,202) exceeds the number of unique lexical entries (1,971) because culturally multifaceted words are assigned to multiple relevant domains (e.g., *bheß╕ì* 'sheep' belongs to both *animals* and *agriculture*; *charkha* belongs to *tools*, *household*, and *animals*).

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
| **Numbers & Quantities** | 247 | αñçαñòαÑìαñò (1), αñªαÑï (2), αññαÑìαñ░αÑê (3), αñ¼αÑÇαñ╣ (20), αñ╕αÑïαñ╣ (100), αñàαñªαÑìαñº (1/2), αñ¬αñ╣αñ▓αñ╛ (1st) |
| **Expressions & Discourse** | 240 | αñòαÑüαñú (who), αñòαÑìαñ»αñ╛ / αñòαÑç (what), αñòαñ┐αññαÑìαñÑαÑÇ (where), αñ£αñª (when), αñ¼αñ▓αÑç αñ¼αñ▓αÑç (slowly), αñ£αÑïαñ░αÑç αñ£αÑïαñ░αÑç (loudly) |
| **Family & Kinship** | 148 | αñ¼αñ╛αñ¬ (father), αñ«αñ╛ (mother), αñ«αñ╛αñ¼αÑüαñ░αñ╛ (parents), αñ¡αñ╛αñê (brother), αñºαÑÇ (daughter), αñ¬αÑüαññαÑìαññ (son) |
| **Body Parts & Health** | 137 | αñ╕αñ┐αñ░ (head), αñàαñòαÑìαñû / αñåαñüαñû (eye), αñªαñ╛αñüαñª (tooth), αñ£αÑÇαñ¡ (tongue), αñ╣αññαÑìαñÑ (hand), αñ¬αÑêαñ░ (foot) |
| **Animals & Pastoral Life** | 122 | αñ¡αÑçαñíαñ╝ (sheep), αñ¼αñòαñ░αÑÇ (goat), αñùαñ╛ (cow), αñÿαÑïαñíαñ╝αñ╛ (horse), αñòαÑüαññαÑìαññαñ░ (dog), αñòαñíαñ╝αñ¬αñ╛ (snake) |
| **Actions & Verbs** | 108 | αñûαñ╛αñúαñ╛ (eat), αñ¬αÑÇαñúαñ╛ (drink), αñ£αñ╛αñúαñ╛ (go), αñöαñúαñ╛ (come), αñ¼αÑïαñ▓αñúαñ╛ (speak), αñªαñ┐αñûαñúαñ╛ (see) |
| **Travel & Directions** | 87 | αñ░αñ╛αñ╣ (path), αñ╕αñíαñ╝αñò (road), αñçαññαÑìαñÑαÑÇ (here), αññαñ┐αññαÑìαñÑαÑÇ (there), αñûαñ╛αñ¼αÑÇ αñòαñúαñ╛αñ░αÑç (left bank) |
| **Colors & Qualities** | 76 | αñòαñ╛αñ▓αñ╛ (black), αñÜαñ┐αñƒαÑìαñƒαñ╛ (white), αñ▓αñ╛αñ▓ (red), αñ¬αÑÇαñ│αñ╛ (yellow), αñ╢αÑêαñ▓ (beautiful) |
| **Nature & Environment** | 53 | αñºαñ░αññαÑÇ (earth), αñàαñ«αÑìαñ¼αñ░ (sky), αñ╕αÑéαñ░αñ£ (sun), αñÜαñ╛αñ¿αñúαÑÇ (moon), αññαñ╛αñ░αñ╛ (star), αñåαñù (fire) |
| **Water, Weather & Seasons** | 52 | αñ¬αñ╛αñúαÑÇ (water), αñ¼αÑìαñ»αñ╛αñ░αÑÇ (wind), αñ¼αñ░αñûαñ╛ (rain), αñ╣αÑçαñëαñü / αñ╣αñ┐αñ»αÑüαñü (snow), αñ¢αñéαñ¼ (lake) |
| **Food & Cooking** | 51 | αñ░αÑïαñƒαÑÇ (bread), αñ¡αñ╛αññ (rice), αñªαÑüαñªαÑìαñº (milk), αñÿαÑìαñ»αÑï / αñÿαÑÇαñë (ghee), αñ▓αÑéαñú (salt) |
| **Household & Clothing** | 39 | αñÜαÑïαñ▓αñ╛ (tunic), αñíαÑïαñ░αñ╛ (cord), αñ¬αñƒαÑìαñƒαÑé (blanket), αñûαñíαÑç (loom), αñÿαñ░ (house) |
| **Plants & Trees** | 39 | αñ¼αÑéαñƒαñ╛ / αñ¬αÑçαñíαñ╝ (tree), αñ¬αññαÑìαññαñ░ (leaf), αñ¼αñ░αñÿαñƒ (banyan), αñ½αÑüαñ▓αÑìαñ▓ (flower), αñùαñ╛αñ╣ (grass) |
| **Mountains & Landscapes** | 31 | αñºαñ╛αñ░ (ridge), αñàαñéαñùαñ╛αñ░αÑÇ (mountain), αñ¿αñªαÑìαñªαÑÇ (river), αñ£αÑïαññ (high pass) |
| **Education & Technology** | 30 | αñòαñ┐αññαñ╛αñ¼ (book), αñ╕αÑìαñòαÑéαñ▓ (school), αñ¬αñóαñ╝αñ╛αñê (study), αñ«αñ╛αñ╕αÑìαñƒαñ░ (teacher) |
| **Tools & Trades** | 26 | αñòαÑüαñ▓αÑìαñ╣αñ╛αñíαñ╝αÑÇ (axe), αñûαñíαÑç (handloom), αñíαñ╛αñÜαÑÇ (sickle), αñ½αÑüαñƒαÑìαñƒαÑÇ (club) |
| **Agriculture & Herding** | 22 | αñ¼αñ▓αÑìαñª (ox), αñûαÑçαññαñ░ (field), αñ«αñ╛αñ▓ (flock/livestock), αñÜαñ░αñ╛αñê (grazing) |
| **Religion & Traditions** | 15 | αñ¿αñ╡αñ╛αñ▓αñ╛ (Shiva worship), αñàαñéαñÜαñ▓αÑÇ (hymn), αñ¬αÑéαñ£αñ╛ (worship), αñòαÑêαñ▓αñ╛αñ╢ (sacred peak) |

---

## 3. Installation

The library requires Python >= 3.10 and relies exclusively on the Python standard library for runtime execution:

```bash
git clone https://github.com/researchbuimb24-spec/Gaddi-Python-Language.git
cd Gaddi-Python-Language
pip install -e .
```

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
print([e.lemma_devanagari for e in res_en])  # ['αñ¬αñ╛αñúαÑÇ', 'αñ¬αñ╛αñúαñ┐', 'αñò├║', 'αñ¼αñ┐αñ£αñ¿']

# Hindi -> Gaddi
res_hi = gaddi.translate("αñ¬αñ╛αñ¿αÑÇ", source="hi", target="gaddi")
print([e.lemma_devanagari for e in res_hi])  # ['αñ¬αñ╛αñúαÑÇ', 'αñ¬αñ╛αñúαñ┐', 'αñò├║', 'αñ¼αñ┐αñ£αñ¿']

# Regional languages (Urdu, Punjabi, Dogri) -> Gaddi
res_ur = gaddi.translate("┘╛╪º┘å█î", source="ur", target="gaddi")
res_pa = gaddi.translate("α¿¬α¿╛α¿úα⌐Ç", source="pa", target="gaddi")
res_doi = gaddi.translate("αñ¬αñ╛αñúαÑÇ", source="doi", target="gaddi")

# Gaddi -> English / Hindi
res_to_en = gaddi.translate("αñ¬αñ╛αñúαÑÇ", source="gaddi", target="en")

# 3. Topic Category Search
animals = gaddi.search_by_category("animals")
family = gaddi.search_by_category("family")
food = gaddi.search_by_category("food")
print(f"Found {len(animals)} animals, {len(family)} kinship terms, {len(food)} food items")

# 4. Synonyms, Variants, and Linked Examples
synonyms = gaddi.get_synonyms("αñ¬αñ╛αñúαÑÇ")
variants = gaddi.get_variants("αñ¬αñ╛αñúαÑÇ")
print(f"Variants: {variants}")  # ['αñ¬αñ╛αñúαÑÇ', '╦êpa╦É╔│i╦É', 'p╩î╦É╔│i╦É', 'p─üß╣ç─½', 'pani', 'paß╣çi']

# Retrieve numbered grammar examples linked directly to a headword
exs_pani = gaddi.get_examples_for_headword("αñ¬αñ╛αñúαÑÇ")
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
res_cult = gaddi.translate("handloom", from_lang="en", include_cultural=True)  # [αñûαñíαÑç]
```

---

## 5. Command-Line Interface (CLI)

The library provides the `gaddi` command (or `python -m gaddi.cli`):

```powershell
# Display comprehensive corpus statistics and category breakdown
python -m gaddi.cli stats

# Search dictionary across all scripts and definitions
python -m gaddi.cli search water

# Multi-lingual translations
python -m gaddi.cli translate "water" --from en --to gaddi
python -m gaddi.cli translate "αñ¬αñ╛αñ¿αÑÇ" --from hi --to gaddi
python -m gaddi.cli translate "αñÿαÑïαñíαñ╝αñ╛" --from hi --to gaddi

# Browse vocabulary by category
python -m gaddi.cli word-list --category animals
python -m gaddi.cli word-list --category family
python -m gaddi.cli word-list --category food

# Search numbered linguistic examples
python -m gaddi.cli examples --search water
python -m gaddi.cli examples --headword αñ¬αñ╛αñúαÑÇ
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
```

---

## 6. Grammar & Linguistic Architecture

The grammar engine (`src/gaddi/grammar.py`) incorporates structured analyses extracted from descriptive fieldwork and literature:

1. **Noun Classes & Declensions**:
   - Class I: Masculine nouns ending in *-a* (αñ¢αÑïαñòαñ░αñ╛ / *chokra* = boy), direct plural in *-e* (αñ¢αÑïαñòαñ░αÑç / *chokre*).
   - Class II: Masculine consonant-ending nouns (αñÿαñ░ / *ghar* = house), direct plural invariant.
   - Class III: Feminine nouns ending in *-i* (αñ¢αÑïαñòαñ░αÑÇ / *chokri* = girl), plural in *-iyan*.
   - Class IV: Feminine consonant-ending nouns (αñ░αñ╛αññ / *raat* = night), plural in *-an* (αñ░αñ╛αññαñ╛αñé).
   - Oblique Case: Singular masculine *-a* shifts to *-e* before postpositions; plural nouns take oblique suffix *-an*.
2. **Gender & Number**:
   - Two grammatical genders (Masculine, Feminine) and two numbers (Singular, Plural). Adjectives and verbs agree in gender and number.
3. **Pronominal & Demonstrative System**:
   - Proximal: Direct SG αñê (*i╦É*), Direct PL αñÅ (*e╦É*), Oblique SG αñçαñ╕ (*╔¬s*), Oblique PL αñçαñ¿αÑìαñ╣αñ╛αñé (*╔¬n╩▒a╦É*).
   - Distal: Direct SG αñè (*u╦É*), Direct PL αñô (*o╦É*), Oblique SG αñëαñ╕ (*╩ès*), Oblique PL αñëαñ¿αÑìαñ╣αÑïαñé (*╩èn╩▒o╦É*).
   - Relative: Direct αñ£αÑï (*d╩Æo*), Oblique αñ£αñ┐αñ╕ (*d╩Æ╔¬s*).
4. **Adjectives & Comparison**:
   - Inflecting adjectives ending in *-a* (αñòαñ╛αñ▓αñ╛ / *kale* / *kali*).
   - Non-inflecting invariant adjectives (αñ╢αÑêαñ▓ / *╩â╔¢l* = beautiful, αñ╕αñ╛αñ½ / *sa╦Ép╩░* = clean).
   - Periphrastic comparison using ablative marker αñòαñ¿αÑìαñ╣αñ╛αñ░ (*kanh─ür*) or αññαÑç (*te*) (e.g. *αñ╕αñ¼ αññαÑç αñ╢αÑêαñ▓* = most beautiful).
5. **Verbal System & TAM**:
   - Present Imperfective: stem + *-da* + copula αñ╣αÑê (*h╔¢*) (e.g. αñûαñ╛αñéαñªαñ╛ αñ╣αÑê = eats).
   - Past Imperfective: stem + *-da* + past copula αñÑαñ╛ (*t╩░a╦É*) (e.g. αñûαñ╛αñéαñªαñ╛ αñÑαñ╛ = was eating).
   - Perfective: stem + *-eya/-ya* (e.g. αñûαñ╛αñ»αñ╛ = ate).
   - Future: stem + *-ga / -la* (e.g. αñûαñ╛αñÅαñùαñ╛ / αñûαñ╛αñ▓αÑï = will eat).
   - Copula forms: Indicative SG αñ╣αÑê, PL αñ╣αñ¿; Past MSG αñÑαñ╛, FSG αñÑαÑÇ, MPL αñÑαÑç, FPL αñÑαñ┐αñ»αñ╛αñü.
   - Negative copula: Suppletive invariant αñ¿αñÑαÑÇ (*n╔Öt╩░i* = is not / does not exist).
6. **Split Ergativity**:
   - Ergative-Absolutive alignment in perfective aspect (transitive subjects marked with agentive postposition αñ¿αÑç *ne*; verb agrees with object).
   - Nominative-Accusative alignment in imperfective and future aspects.
7. **Negation & Imperatives**:
   - Sentential declarative negation: Pre-verbal particle αñ¿αÑÇ (*ni╦É*).
   - Negative copula: αñ¿αñÑαÑÇ (*n╔Öt╩░i*).
   - Dedicated prohibitive particle: αñ«αñÑ (*mat╩░*) used exclusively with imperative verb stems (e.g. *αñ«αñÑ αñ£αñ╛* = do not go!, *αñ«αñÑ αñ¼αÑïαñ▓* = don't speak!).
8. **Word Order & Clauses**:
   - Strict canonical Subject-Object-Verb (SOV) order.
   - Coordination: αññαÑç (*te* = and), αñ¬αñ░ (*p╔Ör* = but), αñ»αñ╛ (*ja╦É* = or).
   - Subordination: Complementizer αñòαñ┐ (*k╔¬*), Relative-correlative αñ£αÑï...αñ╕αÑï... (*jo...so...*), Conditionals αñ£αÑç...αññαñ╛αñé... (*je...taan...*).

---

## 7. Data Sources & Licensing Attribution

- **Software Code**: Licensed under the [MIT License](LICENSE).
- **Data & Provenance Governance**: Governed by [DATA-LICENSE.md](DATA-LICENSE.md) in accordance with the **CARE Principles** (Collective Benefit, Authority to Control, Responsibility, Ethics) and **FAIR Principles** for Indigenous Data.
- **Core Integrated Datasets**:
  - **Aryaman Arora & CLDF Jambu Collection (2023ΓÇô2026)**: 1,118 comparative Gaddi forms aggregated from the Census 2023 Mother Tongue Survey of Himachal Pradesh, Kumari et al. 2026, Grierson 1928, Zoller 2023, and CDIAL.
  - **Kumari et al. (UCL Press, 2026)**: *A Grammar of Gaddi*, Open Access under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Extracted across 9 structured datasets: Appendix II basic word list (254 items), Appendix III numerals (138 forms), 269 numbered examples, phonetics, and morphosyntax.
  - **Sir George A. Grierson (LSI, 1916ΓÇô1928)** & **Rev. T. Grahame Bailey (1908)**: Public Domain historical Western Pahari dialect surveys.
  - **Jammu & Kashmir Field & Academic Sources**: Dr. Banti Kumar (2019), Subhash Chandar (2024), and Arka Chakraborty (2024) for authentic J&K cultural realia, ritual vocabulary, and toponyms.
  - **Census of India (2011)**: Open Government Data (OGD) License India.

---

## 8. Automated Verification Suite

Run the full automated test suite (107 tests):

```bash
pytest -v
```

The test suite validates:
- Multi-lingual translation accuracy across English, Hindi, Urdu, Punjabi, Dogri, and Gaddi.
- Strict anti-conflation policies (separating J&K fieldwork from HP comparative data).
- Topic categorization across all 19 standardized domains.
- Numeral and grammar paradigm completeness.
- Numbered example indexing and text search.
- Backward compatibility of the legacy strict lookup engine.
- Byte-synchronization between `data/` and packaged resources `src/gaddi/resources/`.
