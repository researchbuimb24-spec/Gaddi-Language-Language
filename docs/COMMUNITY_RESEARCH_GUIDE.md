# Community Research & Ethical Documentation Guide for J&K Gaddi

## 1. Introduction and Purpose

The Gaddi community in Jammu & Kashmir (numbering approximately 46,489 Scheduled Tribe members and over 24,000 mother-tongue speakers per the 2011 Census) possesses a unique linguistic and cultural heritage that remains severely underdocumented in academic linguistic literature. 

This guide sets forth the ethical framework, field recording procedures, data governance protocols, and quality control pipelines for community members, native speakers, linguists, and researchers contributing data to the **Gaddi Python Language Library (`gaddi`)**.

---

## 2. Ethical Principles and Data Governance

Documentation of an indigenous, vulnerable, and transhumant community requires strict adherence to international and community-rooted ethical standards:

### 2.1. CARE Principles for Indigenous Data Governance
The project strictly implements the **CARE Principles** (Global Indigenous Data Alliance):
- **Collective Benefit:** Data collection, analysis, and tools must directly benefit the Gaddi people of Jammu & Kashmir by supporting mother-tongue preservation, educational materials, and cultural recognition.
- **Authority to Control:** Gaddi speakers and community leaders retain ultimate authority over their linguistic heritage and traditional cultural expressions.
- **Responsibility:** Researchers and developers must uphold respectful relationships with community knowledge holders and accurately represent speakers' voices without distortion.
- **Ethics:** Harms must be minimized, privacy honored, and sacred, confidential, or ritual oral literature respected according to community customary norms.

### 2.2. FAIR Principles within Ethical Safeguards
Where consistent with community consent, linguistic data should be:
- **Findable:** Tagged with standard identifiers, ISO/glotto-codes, geographical coordinates, and standardized metadata.
- **Accessible:** Free and open for educational and non-commercial community access.
- **Interoperable:** Formatted in open, standard formats (UTF-8 JSON, CSV, Unicode Devanagari and Perso-Arabic).
- **Reusable:** Transparently licensed under permissive documentation standards with strict provenance and attribution.

### 2.3. Free, Prior, and Informed Consent (FPIC)
Every recording, transcription, or submission must be accompanied by explicit FPIC:
1. **Informed:** Contributors must understand how their words, audio recordings, and names will be used, stored, and shared.
2. **Prior:** Consent must be obtained before elicitation begins.
3. **Revocable:** Contributors may withdraw consent or request anonymization at any stage prior to final archival release.
4. **Attribution Preference:** Contributors may choose public attribution, community elder acknowledgment, or an anonymized contributor code (e.g., `CONTRIB_KTH_001`).

---

## 3. Data Collection Templates

Three standardized CSV templates are maintained in the repository under `docs/`:

1. **Word Collection Template** (`community_word_collection_template.csv`):
   - For collecting individual lexical items, nouns, verbs, tools, plants, animals, kinship terms, and material culture.
   - Fields: `contributor_code`, `consent_status`, `district`, `village_or_area`, `date`, `original_gaddi_script`, `gaddi_transcription`, `meaning_hi`, `meaning_en`, `meaning_ur`, `part_of_speech`, `semantic_domain`, `audio_filename`, `notes`, `reviewer_status`.

2. **Sentence Elicitation Template** (`community_sentence_elicitation_template.csv`):
   - For documenting natural conversational, narrative, and grammatical example sentences.
   - Fields: `contributor_code`, `consent_status`, `district`, `village_or_area`, `date`, `gaddi_sentence`, `sentence_transcription`, `meaning_hi`, `meaning_en`, `meaning_ur`, `elicitation_prompt`, `grammar_notes`, `audio_filename`, `reviewer_status`.

3. **Translation Review Template** (`community_translation_review_template.csv`):
   - For native speakers to verify, correct, or dispute existing dictionary entries and translations.
   - Fields: `entry_id`, `lemma_devanagari`, `current_meaning_en`, `current_meaning_hi`, `reviewer_code`, `reviewer_district`, `is_form_recognized`, `is_meaning_accurate`, `local_pronunciation_notes`, `disputed_meaning`, `suggested_correction`, `reviewer_decision`, `review_date`.

---

## 4. Elicitation and Recording Guidelines

### 4.1. Audio Recording Protocols
- **Equipment:** Record in quiet indoor settings whenever possible; avoid high wind noise common in high-altitude pastures (*dhars*).
- **Format:** Uncompressed WAV (44.1 kHz or 48 kHz, 16-bit or 24-bit, mono or stereo).
- **File Naming:** Follow `{district}_{tehsil}_{contributor_code}_{item_id}.wav` (e.g., `kth_bani_c001_pattu.wav`).

### 4.2. Elicitation Techniques
- **Semantic Field Probing:** Elicit vocabulary in thematic clusters (e.g., sheep herding, shearing, spinning, weaving, rituals, high-altitude plant names, pastoral topography) rather than isolated alphabetical lists.
- **Contextual Sentences:** Always elicit a natural sentence demonstrating how the word is used in daily speech.
- **Multiple Pronunciations:** If an elder pronounces a word with a retroflex flap or specific tone/aspiration, document the exact sound in IPA without standardizing it to Hindi or Dogri.

---

## 5. Verification Workflow & Anti-Conflation Pipeline

To preserve data integrity, the library enforces a rigorous 4-stage pipeline before any community submission enters the verified core:

```
[Community Field Submission]
          │
          ▼
Stage 1: Intake & Metadata Validation (Validator CLI)
         - Stored in data/community_unverified.json
         - Evidence status: 'community_submitted_unverified'
          │
          ▼
Stage 2: Peer Native-Speaker Review
         - Cross-checked by reviewers from Kathua, Udhampur, or Doda
         - Resolves lexical or semantic discrepancies
          │
          ▼
Stage 3: Linguistic Analysis
         - Phonological plausibility check
         - Disambiguation from neighbouring Dogri, Kashmiri, or Bhaderwahi
         - Verification against published comparative references (Kumari 2026, Grierson 1916)
          │
          ▼
Stage 4: Promotion to Core Lexicon
         - If verified in J&K field: Promoted to 'verified_jk' in lexicon_jk.json
         - If non-J&K form: Placed in 'comparative_only'
         - If disputed: Tagged as 'disputed' with editorial notes
```

---

## 6. Contact and Contributions

Contributions, audio files, and completed templates should be submitted via GitHub issues or pull requests to the canonical repository:
- **Repository:** `https://github.com/researchbuimb24-spec/Gaddi-Python-Language.git`
- **Maintainers:** Computational Linguistics & Language Documentation Working Group

