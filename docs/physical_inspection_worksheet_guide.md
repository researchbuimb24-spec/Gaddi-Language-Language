# Physical Inspection Worksheet Guide: On-Site Lexical Elicitation Protocol

**Document Purpose:** Standard operating procedure and column definitions for [`docs/physical_inspection_worksheet_template.csv`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/physical_inspection_worksheet_template.csv) during on-site library collation of Dr. Pritam Krishen Kaul (2006), *Pahāṛi and Other Tribal Dialects of Jammu*, Volume 1.

---

## 1. Core Verification Principles

Before any lexical item recorded on this worksheet is eligible for migration into `data/lexicon_jk.json`, it must strictly pass the **Six-Point Lexical Extraction Gate**:

1. **Direct Primary Attestation:** The item must appear printed on a physical page of Volume 1 that has been inspected in person. No conjecture, extrapolation, or snippet-based inference is permitted.
2. **Explicit Linguistic Label:** The printed text must explicitly designate the form as *Gaddi* (or *Bharmauri / Gaddiyali*), distinct from neighboring Dogri, Bhaderwahi, Siraji, or generic Western Pahari.
3. **J&K Geographical Localization:** The informant or speech variety must be explicitly localized to a district, tehsil, or settlement in Jammu & Kashmir (e.g., Doda, Bhaderwah, Kishtwar, Ramban, Udhampur, Ramnagar, Kathua, Bani).
4. **Exact Page Citation:** The exact volume, chapter, section, and page number must be recorded.
5. **Faithful Transcription:** Transcribe the exact characters printed (Devanagari, Perso-Arabic, Latin transliteration, IPA diacritics, tone markers) without editorial normalization.
6. **Anti-Conflation Isolation:** Pan-Pahari cultural terms, religious terms, or garments shared across Jammu hill communities must not be classified as distinctive Gaddi language vocabulary unless documented as specific dialect forms.

---

## 2. Worksheet Column Definitions

| Column Name | Type | Description & Allowed Values | Verification Requirement |
| :--- | :--- | :--- | :--- |
| `entry_id` | String | Unique inspection identifier, formatted as `INSP-KAUL06-XXX` (e.g., `INSP-KAUL06-001`). | Mandatory. Sequential identifier. |
| `page_number` | Integer | Exact printed page number in Volume 1. | Mandatory. Verified from running header/footer. |
| `chapter_and_section` | String | Exact title of chapter and subsection where the term appears (e.g., `Chapter 4: Tribal Dialects, Section 4.2: Gaddi`). | Mandatory. Preserves macro-structural context. |
| `lemma_original_script` | String | Word form printed in the original script (typically Devanagari or Perso-Arabic). | Mandatory. Transcribe verbatim. |
| `phonetic_transcription_or_ipa` | String | Phonetic transcription, Latin transliteration, or IPA as printed by Dr. Kaul. | Optional/Mandatory if present in source. |
| `meaning_as_printed` | String | The gloss or definition provided in the printed text (often in Hindi or Urdu). | Mandatory. Record exact words of author. |
| `meaning_english_gloss` | String | Clear English gloss/translation of the primary word sense. | Mandatory for dictionary indexing. |
| `explicit_variety_label` | String | Exact label used by Dr. Kaul (e.g., `Gaddi`, `Bharmauri`, `Gaddiyali`, `Doda Gaddi`, `Pahari`). | Mandatory. Must NOT be assumed. |
| `direct_jk_attribution_flag` | Enum | Classification of geographic attribution:<br>• `direct_jk_attributed`: Specifically stated as J&K Gaddi speech.<br>• `general_gaddi_unspecified_locality`: Labeled Gaddi without specific geographic locality. | **Critical Anti-Conflation Field.** Only `direct_jk_attributed` can enter `lexicon_jk.json`. |
| `district` | String | District of origin in J&K (e.g., `Doda`, `Kathua`, `Udhampur`, `Kishtwar`, or `Unspecified`). | Mandatory if provided in text. |
| `tehsil_or_area` | String | Tehsil or local valley (e.g., `Bhaderwah`, `Bani`, `Ramnagar`, `Dudu-Basantgarh`). | Record exact local jurisdiction. |
| `village_or_informant_location` | String | Village or settlement of the consultant (e.g., `Assar`, `Sarthal`, `Dhaggar`). | High-precision provenance tracking. |
| `informant_details` | String | Consultant metadata if noted (age, gender, clan/caste, bilingualism, occupation). | Records sociolinguistic parameters. |
| `grammatical_category` | Enum | Part of speech (`noun`, `verb`, `adjective`, `pronoun`, `postposition`, `adverb`, `conjunction`, `interjection`). | Grammatical classification. |
| `grammatical_context_or_paradigm` | String | Case marking, gender/number inflections, verbal conjugations, or auxiliary endings. | Records morphological data. |
| `example_phrase_or_sentence` | String | Example phrase, sentence, or proverb cited in the text containing the lemma. | Verbatim contextual citation. |
| `source_citation` | String | Standard citation string (e.g., `Kaul (2006) Vol. 1 p. 142`). | Bibliographic linkage. |
| `researcher_confidence_tier` | Enum | Confidence tier:<br>• `high_direct_evidence`: Clear J&K Gaddi dialect attestation.<br>• `medium_needs_field_check`: Form attested but phonetic or regional status requires verification.<br>• `low_uncertain_conflation`: Potential pan-Pahari loan or ambiguous attribution. | Self-audit confidence score. |
| `anti_conflation_notes` | String | Comparative observations against neighboring Dogri, Bhaderwahi, or HP Gaddi. | Isolation from contact languages. |
| `unresolved_questions` | String | Open questions, phonetic ambiguities, or verification needs for field consultants. | Flags for subsequent community verification. |

---

## 3. Post-Inspection Workflow

1. **Digital Transcoding:** Enter handwritten field notes into [`docs/physical_inspection_worksheet_template.csv`](file:///C:/Users/Hp/Documents/Gaddi-Python-Language/docs/physical_inspection_worksheet_template.csv).
2. **Double Verification:** Verify that entries marked `direct_jk_attributed` have verifiable page citations and exact printed labels.
3. **Quarantine Check:** Ensure cultural terms lacking unique dialect forms are categorized for `data/cultural_terms_jk.json` rather than direct lexical translation.
4. **Schema Ingestion:** Ingest verified records into `data/lexicon_jk.json` and synchronize with packaged resources.

