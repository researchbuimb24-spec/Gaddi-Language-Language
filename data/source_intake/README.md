# Source Intake Staging Directory (`data/source_intake/`)

This directory serves as the local staging area for lawful primary linguistic materials, consultation photographs, reprographic scans, and researcher field notes acquired during library visits or field documentation.

---

## 1. Legal and Copyright Guidelines

> [!CAUTION]
> **Do Not Commit or Distribute Copyrighted Materials:**
> - Under no circumstances should high-resolution scans, photocopies, or photographs of copyrighted published works (such as Dr. P. K. Kaul, *Pahāṛi and Other Tribal Dialects of Jammu*, 2006) be committed to the public Git repository or redistributed online without explicit copyright holder authorization.
> - While statutory fair dealing exceptions (such as Section 52(1)(a) of the Indian Copyright Act, 1957) apply to personal private study and non-commercial research, they do **not** grant an automatic, blanket right to photograph or scan library materials. All reproduction is subject to holding library regulations.
> - Lawful physical access or personal research photography does **not** confer redistribution rights.
> - Git is configured via `.gitignore` to recursively ignore all files in this directory (`data/source_intake/**`), exempting only `.gitkeep` and `README.md`.

---

## 2. Separation of Concerns: Source Images vs. Transcribed Lexical Data

To ensure both evidence transparency and copyright compliance, this project maintains a strict boundary between:

1. **Original Source Images (Private / Local Intake Only):**
   - High-resolution photographs of printed tables, pages, or manuscripts taken by visiting scholars during authorized reading-room consultation.
   - Staged locally in `data/source_intake/` and **never committed to public Git**.
   - Verified by computing SHA-256 cryptographic hashes for local bitstream integrity tracking (verifying file integrity, not proving linguistic authenticity).
2. **Factual Bibliographic Citations (Public / Open Access):**
   - Precise bibliographic citations (author, title, publisher, ISBN, volume, page numbers) are verifiable facts published openly.
3. **Transcribed Research Data (Public / Version-Controlled):**
   - Discrete linguistic transcriptions (Devanagari, Perso-Arabic, Latin/IPA), English glosses, grammatical categorizations, and exact page citations.
   - Recorded first in [`docs/physical_inspection_worksheet_template.csv`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/physical_inspection_worksheet_template.csv).
   - Once passing the Six-Point Lexical Extraction Gate, ingested into [`data/lexicon_jk.json`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/data/lexicon_jk.json).

---

## 3. Intake File Naming Convention

When staging newly acquired source photographs or scans, use the following standardized naming syntax:

```
SRC_{source_id}_{volume}_{page}_{descriptor}.{ext}
```

### Examples:
* `SRC_kaul_2006_vol1_p142_gaddi_nominal_table.jpg`
* `SRC_kaul_2006_vol1_p148_pastoral_vocabulary.png`
* `SRC_kaul_2006_vol1_toc_tribal_chapter.jpg`
* `SRC_sheeraza_1984_issue3_p45_anchli_ballad.pdf`

---

## 4. Associated Procedures and Templates

* **Evidence Intake Procedure:** Refer to [`docs/evidence_intake_procedure.md`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/evidence_intake_procedure.md) for step-by-step ingestion workflows.
* **On-Site Physical Inspection Worksheet:** Record lexical data in [`docs/physical_inspection_worksheet_template.csv`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/physical_inspection_worksheet_template.csv) following [`docs/physical_inspection_worksheet_guide.md`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/physical_inspection_worksheet_guide.md).
* **Source Acquisition Tracker:** Track institutional correspondence and physical copy status in [`docs/source_acquisition_tracker.csv`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/source_acquisition_tracker.csv).
