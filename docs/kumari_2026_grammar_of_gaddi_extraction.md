# Linguistic Extraction and Research Integration: *A Grammar of Gaddi* (Kumari et al. 2026)

## Executive Summary

This document records the comprehensive linguistic extraction, empirical dataset construction, and research integration of the open-access monograph:

> **Kumari, Preeti; Mehta, Shreya; Nair, Anjali; Nayak, Anusuya; Roy, Yangchen; and Sharma, Vyom.** (2026).  
> *A Grammar of Gaddi*.  
> Series: *Grammars of World and Minority Languages*, Volume 5.  
> London: **UCL Press**.  
> DOI: [`10.14324/111.9781800089938`](https://doi.org/10.14324/111.9781800089938)  
> ISBNs: `978-1-80008-993-8` (PDF Open Access) | `978-1-73935-428-2` (Hardback) | `978-1-73935-429-9` (Paperback)  
> License: **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

The entire 150-page open-access monograph has been systematically analyzed and converted into **9 structured, auditable JSON research datasets**, fully synchronized across `data/` and `src/gaddi/resources/`, integrated into the Python package (`gaddi`), exposed via CLI subcommands, and verified with automated test suites.

---

## 1. Variety Boundary & Linguistic Policy

> [!IMPORTANT]
> **Strict Variety Boundary: Kangra Gaddi vs. Jammu & Kashmir Gaddi**  
> On page 5 of *A Grammar of Gaddi*, the authors state explicitly:  
> *"Gaddi has varieties apart from the one described in this book, which is the variety spoken in and around Palampur. The varieties spoken in the districts of Chamba, Mandi, Kullu, and the state of Punjab and the Union Territory of Jammu and Kashmir require fresh descriptions."*

In accordance with our strict zero-hallucination and anti-conflation policy:
1. **Zero J&K Contamination:** All lexical and grammatical data extracted from Kumari et al. (2026) is strictly classified as variety `hp_kangra_palampur` with evidence status `comparative_only`.
2. **`verified_jk_lexical_entries` remains strictly 0:** The presence of 254 basic word list entries and 138 numeral forms in this comparative dataset does not alter the count of verified Jammu & Kashmir lexical entries.
3. **Strict Translation Safety:** `gaddi.translate()` by default returns only verified J&K lexical entries (`jk_only=True`). Comparative data from Kumari et al. requires explicit opt-in (`allow_comparative=True, jk_only=False`) or access via dedicated comparative accessors (`gaddi.get_comparative_word_list()`, `gaddi.search_comparative_words()`).

---

## 2. Inventory of Generated Research Datasets

All datasets are validated, formatted with two-space indentation, and synchronized identically between `data/` and `src/gaddi/resources/`:

| Dataset Filename | Scope & Source Location | Record Count / Structural Details |
| :--- | :--- | :--- |
| `gaddi_word_list.json` | Appendix II, Table B.1 (pp. 119–124) | **254 entries** (serials 1.1 to 221; includes 33 sub-entries; full IPA, raw forms, English glosses, parts of speech, printed & PDF page mappings). |
| `gaddi_numerals.json` | Appendix III, Tables C.1–C.4 & Ch 3.8 (pp. 125–128) | **138 total numeral forms**: 104 cardinals (1–100, 1000, 100k, 10M, 1B), 22 ordinals (1st–22nd with m/f agreement), 7 fractionals (with printed inversion note), 5 distributives, 9 prefix templates, 8 decade templates. |
| `gaddi_phonology.json` | Chapter 2 (pp. 11–26) & Appendix I (pp. 117–118) | Complete sound system: 8 oral monophthongs, 2 diphthongs, 3 lexical nasal vowels, 31 consonants, retroflex series, syllable templates, phonotactics, and an audited catalogue of Chapter 2 vs. Appendix I discrepancies. |
| `gaddi_grammar.json` | Chapters 3, 4, 5 (pp. 27–116) | Comprehensive grammatical rules, 10 Levin verb classes (Table 3.16), 14 adjective forms (Table 3.14), verbal paradigm for `həsɳɑ` (Table 4.1), and core syntactic relations. |
| `gaddi_examples.json` | Chapters 1 through 5 (pp. 6–116) | **269 numbered linguistic examples** (complete sequence 1 to 269 without gaps; Gaddi text, morpheme-by-morpheme glosses, English translations, printed & PDF page mapping). |
| `gaddi_morphology.json` | Chapters 3 & 4 (pp. 27–84) | Nominal morphology (gender, number, case markers), pronominal systems (personal, demonstrative, interrogative), verbal morphology (TAM suffixes, verbal templates, Mehta's 'Gend' feature). |
| `gaddi_syntax.json` | Chapter 5 (pp. 85–116) | Canonical SOV word order, main clause types, subordinate clauses, sentential negation (`/niː/`), negative copula (`/nətʰi/`), prohibitive (`/matʰ/`), interrogatives, wh-scope marking (`/kɛ/`), and information structure focus particles (`/bʱi/`, `/hi/`). |
| `gaddi_cultural_sociolinguistic_notes.json` | Chapter 1 (pp. 1–10) | Community ethnography, autonym/exonym, transhumant pastoralism, herding cycles, gotra exogamy, demographic vitality (Census 2011), and CLIN JNU fieldwork methodology in Palampur villages (Saperu, Banuri, Kandbari). |
| `gaddi_references.json` | References & Index (pp. 129–135) | **43 bibliographical citations**, 38 source-to-content mappings, and 47 index terms with printed page references. |

---

## 3. Detailed Chapter-by-Chapter Extraction

### Chapter 1: The Gaddi Community and Their Language (pp. 1–10)
- **Ethnographic Profile:** Autonym *Gaddi* (IPA: `/gəd̪ːi/`), endonym self-conception as *ghomtus* ("people born with moving feet"). Traditional transhumant sheep and goat pastoralists migrating between winter lowlands (Kangra/Punjab) and alpine summer pastures (Bharmaur/Lahaul/Pangi).
- **Social Structure:** Patriarchal lineage, preference for male offspring for pastoral continuation, *gotra* exogamy (father's clan), permits cross-cousin and parallel-cousin marriage.
- **Demographics & Vitality:** Census 2011 records 181,089 speakers under mother tongue Gaddi/Pahari; Himachal Pradesh Scheduled Tribe population recorded at 277,417 (2013). Vitality assessed as vulnerable due to expanding Hindi/English school education and sedentarization.
- **Fieldwork Methodology:** Field methods cohorts from the Centre for Linguistics (CLIN), Jawaharlal Nehru University (JNU), New Delhi (cohorts of 2013 and 2015, online follow-up February 2022). Consulted native speakers: Tek Chand Sharma, Urmila Rana, Ratan Pahl. Fieldwork sites: Palampur, Saperu, Banuri, and Kandbari.

### Chapter 2: Phonetics and Phonology (pp. 11–26)
- **Oral Monophthongs (8):** `/i/` (close front), `/e/` (close-mid front), `/ɛ/` (open-mid front), `/ə/` (mid central), `/ɑ/` (open central-back), `/u/` (close back), `/o/` (close-mid back), `/ɔ/` (open-mid back).
- **Diphthongs (2):** `/əi/` (e.g. `bəiʈʰɳɑ` 'to sit') and `/əu/` (e.g. `bəũkʰɾi` 'broom').
- **Nasal Vowels:**
  - Chapter 2 Section 2.2.2 establishes **3 lexical nasal vowels**: `/ũ/` (e.g. `kũɑ` 'dove'), `/ɑ̃/` (e.g. `tʃɑ̃` 'tea'), `/ɛ̃/` (e.g. `d̪ɛ̃i` 'curd').
  - Discrepancy Note: Appendix I (Table A.2) lists 5 nasal vowels (`ĩ, ũ, ẽ, ə̃, ɑ̃`). This discrepancy is formally documented in `gaddi_phonology.json`.
- **Consonants (31):**
  - Plosives: Voiceless unaspirated, voiceless aspirated, voiced unaspirated, and voiced aspirated series at bilabial (`p, pʰ, b, bʰ`), dental (`t̪, t̪ʰ, d̪, d̪ʰ`), retroflex (`ʈ, ʈʰ, ɖ, ɖʰ`), palatal affricates (`tʃ, tʃʰ, dʒ, dʒʰ`), and velar (`k, kʰ, g, gʰ`).
  - Nasals: Bilabial `/m/`, dental `/n/`, retroflex `/ɳ/`. Velar `[ŋ]` is analyzed in Ch 2 as an allophone before velars (though listed independently in Table A.3).
  - Rhotics: Alveolar flap `/ɾ/` and retroflex flap `/ɽ/`. Trill `[r]` appears in Table A.3 but is not established as contrastive in Ch 2.
  - Laterals: Alveolar `/l/` and retroflex lateral `/ɭ/`.
  - Fricatives: Alveolar `/s/`, glottal `/h/`. Table A.3 lists `/f/` and `/ʃ/`, which Ch 2 treats as marginal loan phonemes.
  - Glides: Labio-velar `/w/` and palatal `/j/`.
- **Phonotactics:** Canonical syllable shape `(C)(C)V(C)(C)`. Word-initial complex onsets include `/pr-, tr-, br-, kr-, gr-, dr-, mr-`.

### Chapter 3: Major Word Classes (pp. 27–66)
- **Nominal Gender:** Two grammatical genders (masculine and feminine). Marked masculine nouns typically end in `-ɑ` or `-u`; feminine in `-i` or consonant.
- **Adjectives:** 14 marked adjective forms documented in Table 3.14 (e.g. `kɑlɑ/kɑli` 'black', `baɽɑ/baɽi` 'big').
- **Levin Verb Classes:** Chapter 3.7.2 classifies Gaddi verbs into 10 semantic classes based on Levin (1993):
  1. Verbs of Change of State (e.g. `kʰilɳɑ` 'to blossom')
  2. Verbs of Contact (e.g. `tʃʰuɳɑ` 'to touch')
  3. Verbs of Ingestion (e.g. `kʰɑɳɑ` 'to eat')
  4. Verbs of Movement (e.g. `nəsɳɑ` 'to run')
  5. Verbs of Perception (e.g. `sunɳɑ` 'to hear')
  6. Verbs of Social Interaction (e.g. `milɳɑ` 'to meet')
  7. Verbs of Transfer (e.g. `d̪eɳɑ` 'to give')
  8. Verbs of Creation (e.g. `bəɳɑɳɑ` 'to make')
  9. Weather Verbs (e.g. `bərəf pɛɳi` 'to snow')
  10. Psych Verbs (e.g. `dərɳɑ` 'to fear')
- **Numerals Morphology (Ch 3.8 & Appendix III):**
  - Prefix templates for digits 1–9 (`/kk-/, /b-/, /tr-/, /tʃəʊ-/, /pəɲ-/, /tʃʰi-/, /sət-/, /əʈʰ-/, /nəʊ-/`).
  - Decade stems for 20 (`bi`), 30 (`tri`), 40 (`tʃɑli`), 50 (`pəndʒɑ`), 60 (`səʈʰ`), 70 (`sətːər`), 80 (`əsi`), 90 (`nəbːe`).
  - Unit 9 prefixation: Numbers 19, 29, 39, 49, 59, 69, 79 use the subtractive/anticipatory stem `un-` or `una-` preceding the upcoming decade.

### Chapter 4: Morphosyntax (pp. 67–84)
- **Complete Verbal Paradigm (Table 4.1, p. 75):**  
  Full conjugation matrix for the verb `həsɳɑ` ('to laugh') across 3 persons, singular and plural, masculine and feminine:
  - Present Habitual: Stem + `-d-` + Agreement (e.g. 1sg.m `həsdɑ hɑ̃`, 1sg.f `həsdi hɑ̃`).
  - Present Continuous: Stem + `kər-d-` + Agreement (e.g. `həs kərdɑ hɑ̃`).
  - Past Continuous: Stem + `kər-d-` + Past copula (e.g. `həs kərdɑ tʰu`).
  - Future: Stem + `-g-` + Agreement (e.g. 1sg.m `həsgɑ`, 1pl `həsgɛ`).
  - Perfective Aspect: Demonstrates split ergativity. Intransitive verbs agree with the subject; transitive verbs agree with the object.
- **The Mehta 'Gend' Feature Discovery:**  
  Citing Shreya Mehta (2016, 2021), Chapter 4 establishes that in perfective forms, suffixes `-u` and `-i` often show a specialized agreement pattern (termed `Gend` with values `ma` and `fe`) that can operate independently of canonical noun class gender.

### Chapter 5: Clause Types and Syntax (pp. 85–116)
- **Word Order:** Strict canonical Subject-Object-Verb (SOV) order with head-final postpositions.
- **Tripartite Negation System:**
  1. Declarative sentential negation: Pre-verbal particle **`नी`** (`/niː/`).
  2. Suppletive negative copula: **`नथी`** (`/nətʰi/`) ('is not / does not exist').
  3. Prohibitive particle: **`मथ`** (`/matʰ/`) ('do not'), used exclusively with imperative verb stems.
- **Interrogatives & Scope Marking:**
  - Wh-in-situ: Interrogative words (`kuɳ` 'who', `kɛ` 'what', `kəre` 'where', `kəd̪` 'when') remain in situ.
  - Wh-scope marking: Long-distance interrogatives in complex matrix clauses use the scope marker **`kɛ`** in the matrix clause paired with the embedded wh-element.
- **Focus Particles:** Additive focus marked by **`bʰi`** ('also/too'); exclusive/contrastive focus marked by **`hi`** ('only').

---

## 4. Appendices Extraction Details

### Appendix I: Phonemic Inventory (pp. 117–118)
- Tables A.1, A.2, and A.3 provide the initial summary phoneme inventory.
- Documented in `gaddi_phonology.json` alongside an audited list of discrepancies with Chapter 2 (e.g., 5 vs. 3 nasal vowels, inclusion of `/f, ʃ, r, ŋ/`).

### Appendix II: Basic Word List (Table B.1, pp. 119–124)
- Based on Anvita Abbi's (2001, p. 244) modified Swadesh list.
- **254 total items**, covering base serials 1 to 221 with 33 decimal sub-entries (e.g. `1.1` [səb] all, `1.2` [sɑɾe] all; `25.1` [ɑɳɑ] come, `25.2` [oɳɑ] come, `25.3` [illɑ] come).
- Digitally extracted and verified against visual screenshots for hyphenation and diacritic consistency.

### Appendix III: Numerals (Tables C.1–C.4, pp. 125–128)
- **Cardinals (Table C.1):** Complete inventory 1 to 100, plus higher powers (`1000: jɑr`, `100,000: ləkʰ`, `10,000,000: kror`, `1,000,000,000: ərəb`).
- **Ordinals (Table C.2):** 1st (`pɛlɑ / pɛli`) through 22nd (`bɑibɑ̃`).
- **Fractionals (Table C.3):** 7 fractional forms (`1/4: pɔ:ni`, `1/2: əddɑ`, `3/4: pɔɳe`, `1 1/4: səwɑ`, `1 1/2: ɖeɖʰ`, `1/10: əkʰ bəʈɑ solɑ` [inversion note], `1/16: əkʰ bəʈɑ dəs` [inversion note]).
- **Distributives (Table C.4):** 5 reduplicated distributive forms (`1 each: əkʰ-əkʰ`, `2 each: do-do`, `3 each: trɛ-trɛ`, `4 each: tʃɑr-tʃɑr`, `5 each: pəndʒ-pəndʒ`).

---

## 5. Python API & Command-Line Interface

### Public Python API (`import gaddi`)
```python
import gaddi

# 1. Inspect metadata and comparative dataset counts
info = gaddi.info()
print(info["comparative_word_list_entries"])   # 254
print(info["comparative_numeral_forms"])       # 138
print(info["documented_grammar_examples"])     # 269
print(info["verified_jk_lexical_entries"])     # 0 (strictly preserved!)

# 2. Access Appendix II basic word list
words = gaddi.get_comparative_word_list()      # List of 254 entries
results = gaddi.search_comparative_words("all")

# 3. Access Appendix III numerals
numerals = gaddi.get_numerals()               # Dict of cardinals, ordinals, fractionals, distributives
found = gaddi.search_numerals("1")             # Finds cardinal 1, ordinal 1st, fractional 1/4, distributive 1 each

# 4. Access Chapters 1-5 Numbered Examples (1 to 269)
all_exs = gaddi.get_grammar_examples()         # All 269 examples
ch4_exs = gaddi.get_grammar_examples(chapter=4) # Filter by chapter
ex22 = gaddi.get_grammar_examples(example_number=22)

# 5. Access Sound System, Grammar, and Sociolinguistics
phon = gaddi.get_phonology()
grammar = gaddi.get_full_grammar()
soc = gaddi.get_sociolinguistic_notes()
refs = gaddi.get_references()
```

### CLI Subcommands (`python -m gaddi.cli <command>`)
- `gaddi word-list [--search <query>] [--pos <pos>] [--limit <n>] [--all] [--json]`
- `gaddi numerals [--category {cardinals,ordinals,fractionals,distributives}] [--search <query>] [--json]`
- `gaddi phonology [--section {vowels,consonants,phonotactics,processes,discrepancies}] [--json]`
- `gaddi examples [--chapter <1-5>] [--number <n>] [--search <query>] [--limit <n>] [--json]`
- `gaddi sociolinguistics [--section {community,vitality,fieldwork,all}] [--json]`
- `gaddi references [--search <query>] [--json]`

---

## 6. Verification and Test Results

The integration is verified by an automated test suite (`tests/test_kumari_2026_extraction.py`) comprising 17 dedicated unit tests, in addition to the 69 existing library tests:

- **Total Test Suite:** **86 passed** in 0.44s.
- **Data Integrity:** All 9 JSON datasets confirmed byte-identical between `data/` and `src/gaddi/resources/`.
- **Lexical Isolation:** Confirmed that `verified_jk_lexical_entries` remains strictly 0 and default English/Hindi/Urdu translation returns `[]` without leaking Palampur comparative data.
- **Validation Report:** `gaddi validate` reports **PASSED** with 0 errors across all datasets.

