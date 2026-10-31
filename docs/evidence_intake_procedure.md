# Evidence Intake Procedure: Primary Source Management and Citation Standards

**Document Purpose:** Defines standard operating procedures for lawful evidence intake, provenance tracking, page-level citation recording, and strict separation between private raw media and public research datasets in the Gaddi Language Library.

---

## 1. Principles of Lawful Evidence Intake

1. **Copyright Compliance & Statutory Limits of Fair Dealing:**  
   Published works (such as Dr. P. K. Kaul, *Pahāṛi and Other Tribal Dialects of Jammu*, 2006) are protected by copyright under the Indian Copyright Act, 1957. While Section 52(1)(a) provides exceptions for private or personal use including research, statutory fair dealing does **not** grant an automatic, unlimited right to photograph or scan library materials. Any reproduction is governed by the specific holding institution's reading-room regulations, terms of admission, and reprographic permissions. Crucially, lawful physical access to a library copy or the authorized capture of a private research photograph does **not** confer any copyright or redistribution rights. Raw photographic reproductions, scans, or third-party digital surrogates must **never** be committed to public version control, pushed to remote repositories, or redistributed online.

2. **Separation of Media and Data (Private Media vs. Public Research Data):**  
   To respect copyright boundaries while upholding scientific transparency, this project enforces strict separation across three categories:
   * **Private Raw Media (Local Only):** High-resolution scans and photographs of original source pages are stored exclusively in the local staging folder `data/source_intake/` (recursively excluded from Git tracking via `.gitignore`). These binary files are strictly private to the researcher and never committed or redistributed.
   * **Public Factual Metadata (Version-Controlled):** Factual bibliographic citations (author, title, publisher, ISBN, volume, page numbers, section headers) are non-copyrightable verifiable facts published openly in documentation and registries.
   * **Public Transcribed Linguistic Data (Version-Controlled):** Discrete linguistic extractions (lemmas, phonetic notations, IPA renderings, English glosses, grammatical categorizations) are non-copyrightable factual data excerpted for lexicographical research. They are committed to version-controlled JSON datasets only when legally, ethically, and academically verified.

3. **Bitstream Integrity vs. Linguistic Authenticity:**  
   Every ingested source image must have its SHA-256 cryptographic hash calculated locally and logged in the researcher's intake register. This hash records and confirms **bitstream integrity** (verifying that the local image file has not suffered truncation, file corruption, or alteration). A cryptographic checksum does not prove linguistic authenticity, dialect accuracy, geographic origin, or the factual truth of any claim made in the source. Establishing linguistic authenticity requires rigorous philological evaluation and satisfaction of the Six-Point Lexical Extraction Gate.

4. **Zero Speculative Ingestion:**  
   No lemma or paradigm may be added to `data/lexicon_jk.json` unless it has passed every check of the Six-Point Lexical Extraction Gate. Until primary J&K Gaddi linguistic evidence is directly inspected and verified at the page level, the verified J&K lexical count remains strictly zero (`verified_jk_lexical_entries = 0`).

---

## 2. Step-by-Step Evidence Intake Workflow

```
+-----------------------------------------------------------------------------------------------+
|                               PRIMARY EVIDENCE INTAKE WORKFLOW                                |
+-----------------------------------------------------------------------------------------------+
| Step 1: On-Site Inspection & Lawful Consultation                                              |
|         - Visit holding library or publisher office with photo ID and institutional credentials.|
|         - Request permission from reference staff according to library regulations.            |
|         - Do not assume photography is automatically authorized by fair dealing.              |
|         - If authorized, capture personal research photographs of title page, TOC, and text.  |
|         - Note: Lawful physical access or photography does NOT grant redistribution rights.   |
+-----------------------------------------------------------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
| Step 2: Local Staging in data/source_intake/                                                 |
|         - Transfer image files to data/source_intake/ (recursively gitignored).               |
|         - Rename according to standard: SRC_{source_id}_{volume}_{page}_{descriptor}.ext.    |
|         - Compute SHA-256 hash for local bitstream integrity tracking (not authenticity).    |
+-----------------------------------------------------------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
| Step 3: Transcription into Physical Inspection Worksheet                                     |
|         - Open docs/physical_inspection_worksheet_template.csv.                               |
|         - Record exact page number, running header, lemma, script, IPA, gloss, and label.     |
|         - Mark direct_jk_attribution_flag: direct_jk_attributed vs general_gaddi.             |
+-----------------------------------------------------------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
| Step 4: Verification Gate Audit & Schema Ingestion                                           |
|         - Audit entry against the Six-Point Lexical Extraction Gate.                         |
|         - If verified: Ingest into data/lexicon_jk.json with full page citation.              |
|         - If cultural term lacking unique dialect form: Stage in cultural_terms_jk.json.     |
|         - Synchronize data/ with src/gaddi/resources/ and run pytest & gaddi validate.       |
+-----------------------------------------------------------------------------------------------+
```

---

## 3. How to Record Page-Level Citations

Every citation recorded in the worksheet and the dictionary must adhere to the following standard:

### Citation Format Syntax
```
{source_id}, Vol. {volume_number}, p. {page_number}[, {section_or_table}]
```

### Examples
* `kaul_2006, Vol. 1, p. 142, Table 4.2`
* `kaul_2006, Vol. 1, p. 148, Section 4.2.3`
* `kumari_2026, p. 74, Table 3.5`
* `grierson_1916, Vol. IX, Pt. IV, p. 794`

### Mandatory Citation Elements
1. **Source Identifier:** Matches an entry registered in [`src/gaddi/registry.py`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/src/gaddi/registry.py) (e.g., `kaul_2006`, `kumari_2026`).
2. **Volume Designation:** Explicitly distinguishes Volume 1 (*Survey & Analysis*) from Volume 2 (*Reference Compendium*).
3. **Exact Page Number:** The printed page number where the lexical item, paradigm, or example sentence appears.
4. **Locational Sub-Identifier:** If multiple tables or wordlists exist on the page, record the specific table number or line.

---

## 4. File Naming Conventions for Intake Artifacts

To prevent file collision and maintain clear traceability, files placed in `data/source_intake/` must follow this naming schema:

```
SRC_{source_id}_{volume}_{page}_{descriptor}.{ext}
```

* `{source_id}`: Registered source ID (e.g., `kaul_2006`, `sheeraza_1984`).
* `{volume}`: Volume number formatted as `vol1` or `vol2` (omit if single-volume work).
* `{page}`: Page number formatted as `p142`, `p148-149`, or `toc_p1-4`.
* `{descriptor}`: Short snake_case summary (e.g., `gaddi_case_markers`, `pastoral_nouns`, `title_page`).
* `{ext}`: File extension (`jpg`, `png`, `pdf`, `tiff`).

### Example File Names
* `SRC_kaul_2006_vol1_p142_nominal_declensions.jpg`
* `SRC_kaul_2006_vol1_p148_gaddi_lexicon_extract.png`
* `SRC_kaul_2006_vol1_toc_tribal_dialects_chapter.jpg`
* `SRC_kaul_2006_vol1_frontmatter_methodology.pdf`

---

## 5. Local Bitstream Integrity Logging & Checksum Generation

To establish an audit trail of staged research files without committing or redistributing copyrighted images, researchers should generate and record SHA-256 hashes of all staged files in a local, uncommitted log.

> [!NOTE]
> **Integrity vs Authenticity Distinction:** SHA-256 checksums verify local **bitstream integrity** (proving that the staged file has not been altered, truncated, or replaced since hashing). Checksums do **not** verify the historical, linguistic, or factual authenticity of the content, which must be independently evaluated by linguists.

### Generating SHA-256 in PowerShell:
```powershell
Get-FileHash -Algorithm SHA256 data/source_intake/SRC_kaul_2006_vol1_p142_nominal_declensions.jpg
```

### Logging Format:
Record in a local text file `data/source_intake/intake_checksums.txt`:
```
[SHA-256 HASH]  SRC_kaul_2006_vol1_p142_nominal_declensions.jpg  [Date: YYYY-MM-DD]  [Location: Dhanvantri Library]
```

---

## 6. Verification Against the Six-Point Extraction Gate

Before adding any lexical entry from the physical inspection worksheet to `data/lexicon_jk.json`, confirm that all six criteria are satisfied:

1. **Direct Primary Attestation:** Verified directly from staged photo or physical consultation.
2. **Explicit Linguistic Label:** Explicitly labeled *Gaddi*, *Bharmauri*, or *Gaddiyali* in text.
3. **J&K Geographical Localization:** Provenance traced to a specific district or locality in Jammu & Kashmir (Doda, Bhaderwah, Kishtwar, Ramban, Udhampur, Ramnagar, Kathua, Bani).
4. **Exact Page Citation:** Full page citation recorded as `{source_id}, Vol. {vol}, p. {page}`.
5. **Faithful Transcription:** Exact spelling, diacritics, and tone marks recorded without normalization.
6. **Anti-Conflation Isolation:** Pan-Pahari cultural terms quarantined unless documented as distinct dialect vocabulary.

If any criterion fails, the entry must **NOT** be added to `data/lexicon_jk.json`.
