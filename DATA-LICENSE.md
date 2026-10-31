# Data and Cultural Heritage Terms Notice (`DATA-LICENSE.md`)

**Date:** 2026-10-30  
**Repository:** `Gaddi-Python-Language` / `Gaddi-Language-Library`  
**Applies to:** All linguistic datasets, source registries (`data/sources.json`), variety registries (`data/varieties.json`), lexical records (`data/lexicon/`), cultural annotations, grammatical paradigms, and phonetic transcriptions.

---

## 1. Separation of Software and Data Licensing

The original software code in this repository (Python modules, command-line interfaces, validation algorithms, testing suites, and schema definitions) is licensed under the **MIT License** (see [`LICENSE`](LICENSE)).

**The MIT License applies strictly to the software code and does not govern or grant unrestricted rights to third-party academic source material, historical texts, indigenous cultural expressions, or lexical datasets.**

Rights, licenses, and ethical reuse permissions for data, citations, and cultural assets must be assessed individually and independently of the codebase.

---

## 2. Status of Sources and Data Assets

### 2.1 Academic Open-Access Sources
- **UCL Press — *A Grammar of Gaddi* (Kumari et al., 2026):**
  - **Mandatory Attribution String:**
    > Kumari, P., Mehta, S., Nair, A., Nayak, A., Roy, Y., and Sharma, V. (2026). *A Grammar of Gaddi*. London: UCL Press. https://doi.org/10.14324/111.9781800089938
  - Published open-access under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.
  - **Non-Commercial Restriction:** Any reuse, sharing, adaptation, or comparative analysis of this work must be strictly non-commercial.
  - **Non-Endorsement Disclaimer:** This library is an independent computational linguistic and research project and is not affiliated with, endorsed by, or sponsored by UCL Press or the authors of *A Grammar of Gaddi*.
  - **Indication of Adaptations and Derivative Structuring:**
    In accordance with Section 3(a)(1)(B) of CC BY-NC 4.0, the following adaptations were made to the source text during extraction and integration:
    1. Structuring and parsing unstructured print text from the digital PDF into machine-readable JSON datasets.
    2. Documentation and resolution of typographical inversion in Appendix III Table C.3 fractionals (tenth `1/10` vs. sixteenth `1/16`), preserving both printed and resolved readings.
    3. Systematic grammatical and part-of-speech (POS) classification of Appendix II lexical items.
    4. Extraction and separation of numbered linguistic examples (1 to 269) from surrounding analytical prose, moving explanatory context to dedicated notes fields.
    5. Removal of PDF running page headers and footers from example text blocks.
    6. Restoration of word-internal whitespace in compound IPA entries (serials 214.1, 214.2, and 220).
  - **Third-Party Copyright Materials Excluded from CC BY-NC 4.0 Licence:**
    As noted in UCL Press copyright terms, third-party materials embedded within the work do not fall under the CC licence and are used under fair dealing / academic citation:
    1. *Appendix III Numerals:* Collected by **Kumari Mamta** during doctoral research at the Centre for Linguistics, Jawaharlal Nehru University (JNU), and shared with the authors (p. 125, footnote 1).
    2. *Appendix II Word List Structure:* Elicitation list structured after **Anvita Abbi (2001, p. 244)**, *A Manual of Linguistic Field Work and Indian Language Structures*.
    3. *Historical Comparative Examples:* Examples (1) and (2) cite data from **Sir George A. Grierson (LSI 1916, Vol. IX, Part IV)**.
    4. *Grammatical Frameworks:* Categorization schemas adapted from **R.M.W. Dixon (1977)** (adjective classes) and **Beth Levin (1993)** (verb classifications).
  - **Linguistic Scope & Strict Dialect Boundary:**
    Describes the Kangra/Palampur variety (Himachal Pradesh). It is treated in this library as a **comparative reference only** (`hp_kangra_palampur`), and not as automatic proof of Jammu & Kashmir Gaddi features. The authors explicitly note (p. 5) that Jammu & Kashmir varieties require fresh, independent descriptions.

### 2.2 Academic Fieldwork Documentation — Aligarh Journal of Linguistics (Dar & Sheikh, 2022)
- **Primary Source:**
  - Hilal Ahmad Dar and Aejaz Mohammed Sheikh (2022). "Gaddi Speech Community of Jammu and Kashmir: The Self-Claimed Descendants of Lord Shiva." *Aligarh Journal of Linguistics*, Volume 11 (2021–2022), pp. 245–258. Department of Linguistics, Aligarh Muslim University (AMU), Aligarh, India.
  - Open-access academic publication accessed via AMU Academic Portal: `https://api.amu.ac.in/storage//file/10353/file_management/1659595804.pdf`.
- **Licensing & Fair Academic Use:**
  - Published open access by Aligarh Muslim University Department of Linguistics for non-commercial educational and linguistic research purposes.
  - Used strictly in accordance with fair dealing for non-commercial scholarly research and linguistic preservation under Section 52(1)(a) of the Indian Copyright Act, 1957.
  - Attribution: Full academic citation and tabular provenance are recorded for all 105 extracted lexical items (Tables 1–13, pp. 248–255).
- **Linguistic Focus:**
  - Provides primary descriptive linguistic field documentation of Gaddi as spoken in 10 villages of Bhaderwah (Doda district, Jammu & Kashmir).
  - Categorized under variety ID `jk_bhaderwah_doda`.

### 2.3 Historical Public Domain Sources
- **Linguistic Survey of India (Grierson, 1916, Vol. IX, Part IV):**
  - In the public domain globally.
  - Represents historical data collected in the late 19th and early 20th centuries, chiefly representing the Bharmaur (Chamba) variety.
- **T. Grahame Bailey (1908, *The Languages of the Northern Himalayas*):**
  - In the public domain globally.

### 2.4 Regional Academic Papers and Fieldwork in Jammu & Kashmir
- Research articles, book chapters, and dissertations documenting the Gaddi community in Jammu & Kashmir (e.g., Dr. Banti Kumar et al. 2019, Subhash Chandar 2024, Arka Chakraborty 2024, Prof. Shiv Nirmohi):
  - Used strictly under the principles of academic fair dealing, non-commercial research, citation, and factual indexing.
  - Full bibliographic traceability is maintained for every factual statement and cultural item.
  - These sociological/ethnographic studies are classified as cultural and ethnographic records; they are not cited as linguistic descriptive dictionaries.

### 2.5 Official Government Demographic Data
- **Census of India (Office of the Registrar General & Census Commissioner, India):**
  - Used under the **Open Government Data (OGD) License India**.
  - Distinct datasets:
    - **Table C-16 (2011/2018):** Mother-tongue language reporting (24,161 Gaddi speakers in J&K).
    - **Table ST-14 / PCA ST (2011/2013):** Scheduled Tribe population enumeration (46,489 Gaddi ST population in J&K).
  - ST population is strictly maintained as an ethnic/administrative demographic category and never conflated with mother-tongue speaker counts.

---

## 3. Indigenous Cultural Heritage and Data Sovereignty

### 3.1 Non-Assertion of Community Representation
This library is a computational linguistic and language-documentation research tool. It does **not** claim official community representation, collective ownership, or political mandate on behalf of the Gaddi people of Jammu & Kashmir or Himachal Pradesh.

### 3.2 Respect for Traditional Cultural Expressions
The Gaddi people hold rich, sacred, and customary oral traditions, including *Ainchali* / *Anchli* hymns, *Shiv Nuala* rites, and pastoral lore (*Hadwari*). This project commits to:
- Recording provenance and geographical variety with high fidelity.
- Avoiding the trivialization, decontextualization, or commercial exploitation of sacred cultural expressions.
- Adhering to the **CARE Principles for Indigenous Data Governance** (Collective benefit, Authority to control, Responsibility, Ethics) alongside FAIR data principles (Findable, Accessible, Interoperable, Reusable).

---

## 4. Verification Status and Research Transparency

To ensure intellectual and linguistic honesty:
1. Every lexical entry must indicate its exact source ID and geographic variety.
2. Unverified or candidate entries are strictly labeled as `provisional` or `comparative_only`.
3. No entry is marked `verified` without explicit citation from a documented primary source or verified native speaker attestation.
4. No synthetic, hallucinated, or guessed words are permitted in this repository.

---

## 5. Contact and Contribution Protocols

Researchers, native speakers, and community members wishing to suggest corrections, contribute dialectal data, or clarify cultural provenance are warmly invited to engage through the project's documentation review guidelines and issue tracker.

