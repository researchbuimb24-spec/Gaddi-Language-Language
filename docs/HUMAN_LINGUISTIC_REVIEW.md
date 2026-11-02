# Gaddi Language Library — Human Linguistic Review Document

**Date:** 2026-11-02
**Repository:** `C:\Users\Hp\Documents\Gaddi-Language-Library`
**Dataset:** `data/dictionary_unified.json`
**Status:** Pending Human Review & Native Speaker Confirmation

---

## 1. Purpose & Scope

This document isolates and details the **seven uncertain lexical groups** identified during the deep audit of the 51 duplicate collision groups in `data/dictionary_unified.json`.

In accordance with strict linguistic documentation standards:
- **No speculative splits or merges have been applied.**
- All original field item numbers, raw source transcriptions, and glosses are preserved in the database.
- The evidence and alternatives for each group are presented neutrally below for field verification and human review.

---

## 2. Review Dossiers for the Seven Uncertain Groups

### Group 4: `करन` (karna)

- **Devanagari Form:** `करन`
- **Part of Speech:** `verb`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00729`: Census 2011/2023, p. 1094, Item 252 (Bharmauri/Gaddi). Raw transcription: `karna`. English gloss: `"do"`. Hindi gloss: `"करना"`.
  - Record `gaddi-uni-00796`: Census 2011/2023, p. 1096, Item 322 (Bharmauri/Gaddi). Raw transcription: `karna`. English gloss: `"swim"`. Metadata synonym: `["तर"]`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00729`
  - Lemma: `करन` (`part_of_speech: "verb"`, `homonym_index: null`)
  - Sense 1: `"to do"` (`definition_hi: "करना"`, `definition_ur: "کرنا"`)
  - Sense 2: `"to swim"` (`definition_hi: "तैरना"`, `definition_ur: "تیرنا"`)
  - Attestations Preserved: Census 2011 (Item 252, Item 322), Census 2023 LSI (p. 1094).
- **Reason for Uncertainty:**
  In Indo-Aryan, the primary root for "swim" is *tṛ-* / *tar-* (attested in Gaddi as `तर` / `तरन`, cf. Group 16). The appearance of `karna` for "swim" in Census Item 322 could represent:
  1. A light-verb verbal compound (e.g., *tarnā karnā* / *paunṛī karnā* contracted or incompletely transcribed).
  2. A field elicitation or typographic anomaly in the Census wordlist.
  3. A homophonous verbal idiom.
- **Evidence / Confirmation Needed:**
  Consultation with native Bharmauri Gaddi speakers to confirm the natural verb for "to swim" (e.g., *taraṇā* vs. *karna* / *karnā*).
- **Alternatives:**
  - *Alternative A (Current):* Retain as a multi-sense entry with an editorial note flagging Sense 2 ("to swim") as an unverified census elicitation.
  - *Alternative B:* Split into two distinct homonyms (`करन¹` "to do", `करन²` "to swim") using `homonym_index`.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 10: `गन` (gana)

- **Devanagari Form:** `गन`
- **Part of Speech:** `verb`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00747`: Census 2011/2023, p. 1095, Item 271 (Bharmauri/Gaddi). Raw transcription: `gana`. English gloss: `"sing"`. Hindi gloss: `"गाना"`.
  - Record `gaddi-uni-00754`: Census 2011/2023, p. 1095, Item 277 (Bharmauri/Gaddi). Raw transcription: `gana`. English gloss: `"go"`. Hindi gloss: `"जाना"`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00747`
  - Lemma: `गन` (`part_of_speech: "verb"`, `homonym_index: null`)
  - Sense 1: `"to sing"` (`definition_hi: "गाना"`, `definition_ur: "گانا"`)
  - Sense 2: `"to go"` (`definition_hi: "जाना"`, `definition_ur: "جانا"`)
  - Attestations Preserved: Census 2011 (Item 271, Item 277), Census 2023 LSI (pp. 58-119).
- **Reason for Uncertainty:**
  "To sing" (< OIA *gā-*, *gāyati*) and "to go" (< OIA *gam-*, *gacchati*) are etymologically distinct verbal roots across all Indo-Aryan languages. While both were transcribed as *gana* in the Census Roman wordlist (likely representing *gāṇā* "to sing" and a past/infinitival stem of *ga-* / *gacch-* "to go"), unifying them under one entry suggests semantic polysemy (that one Gaddi verb means both "sing" and "go"), which is linguistically implausible.
- **Evidence / Confirmation Needed:**
  Native speaker recording of the citation infinitives for "to sing" (typically *gāṇā*) and "to go" (typically *jāṇā* or *gachhṇā* / *gaṇā*).
- **Alternatives:**
  - *Alternative A (Current):* Retain as merged multi-sense entry with an editorial note documenting etymological convergence.
  - *Alternative B (Recommended upon review):* Disambiguate into two homonymous verb entries: `गन¹` (verb, "to sing") and `गन²` (verb, "to go") using `homonym_index`.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 15: `छाति` (chāti / chʰāti)

- **Devanagari Form:** `छाति`
- **Part of Speech:** `noun`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00591`: Census 2011/2023, p. 1091, Item 99 (Bharmauri/Gaddi); Kumari et al. 2026 Table B.1, Item 18.1. Raw transcriptions: `cʰāti`, `cʰati`, `chāti`. English gloss: `"chest"`. Hindi gloss: `"छाती / सीना"`.
  - Record `gaddi-uni-00626`: Census 2011/2023, p. 1092, Item 144 (Bharmauri/Gaddi). Raw transcription: `cʰāti`. English gloss: `"roof"`. Hindi gloss: `"छत"`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00591`
  - Lemma: `छाति` (`part_of_speech: "noun"`, `homonym_index: null`)
  - Sense 1: `"chest; breast"` (`definition_hi: "छाती / सीना"`, `definition_ur: "سینہ"`)
  - Sense 2: `"roof; terrace"` (`definition_hi: "छत"`, `definition_ur: "چھت"`)
  - Attestations Preserved: Census 2011 (Item 99, Item 144), Census 2023 LSI (p. 1091), Kumari 2026 (Table B.1, p. 119).
- **Reason for Uncertainty:**
  "Chest" (anatomical body part < OIA *chātti* / *vakṣas*) and "roof" (architectural structure < OIA *chattr-* / *chādayati* "to cover") belong to distinct semantic domains. While phonological erosion produced identical surface forms (*chāti*), they represent distinct lexical items rather than polysemy of a single concept.
- **Evidence / Confirmation Needed:**
  Field verification of grammatical gender (is "chest" feminine while "roof" is masculine or feminine in Bharmaur?) and tone/aspiration.
- **Alternatives:**
  - *Alternative A (Current):* Retain as merged multi-sense entry.
  - *Alternative B (Recommended upon review):* Disambiguate into two homonyms: `छाति¹` (noun, "chest; breast") and `छाति²` (noun, "roof; terrace") using `homonym_index`.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 17: `तुकन` (tukna)

- **Devanagari Form:** `तुकन`
- **Part of Speech:** `verb`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00737`: Census 2011/2023, p. 1095, Item 260 (Bharmauri/Gaddi). Raw transcription: `tukna`. English gloss: `"hit"`. Hindi gloss: `"मारना / ठोकना"`.
  - Record `gaddi-uni-00766`: Census 2011/2023, p. 1095, Item 289 (Bharmauri/Gaddi). Raw transcription: `tukna`. English gloss: `"spit"`. Hindi gloss: `"थूकना"`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00737`
  - Lemma: `तुकन` (`part_of_speech: "verb"`, `homonym_index: null`)
  - Sense 1: `"to hit; strike"` (`definition_hi: "मारना / ठोकना"`, `definition_ur: "मारना"`)
  - Sense 2: `"to spit"` (`definition_hi: "थूकना"`, `definition_ur: "تھوکना"`)
  - Attestations Preserved: Census 2011 (Item 260, Item 289), Census 2023 LSI (p. 1095).
- **Reason for Uncertainty:**
  "To hit" (Hindi *ṭhoknā* / *ṭhuknā*, with retroflex unaspirated/aspirated stop) and "to spit" (Hindi *thūknā*, with dental aspirated stop) are etymologically distinct. The Census wordlist de-aspirated or collapsed the dental/retroflex contrast in Roman transcription (*tukna*). Unifying them into one polysemous verb conflates spitting with striking.
- **Evidence / Confirmation Needed:**
  Native speaker audio recording to determine the phonetic initial consonant (dental [t̪ʰ] vs retroflex [ʈʰ] / [ʈ]) and vowel length.
- **Alternatives:**
  - *Alternative A (Current):* Retain as merged multi-sense entry with an editorial note documenting transcription convergence.
  - *Alternative B (Recommended upon review):* Disambiguate into `तुकन¹` (verb, "to hit; strike") and `तुकन²` (verb, "to spit") using `homonym_index`.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 27: `बदन` (badna / badana)

- **Devanagari Form:** `बदन`
- **Part of Speech:** `verb`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00784`: Census 2011/2023, p. 1096, Item 309 (Bharmauri/Gaddi). Raw transcription: `badna`. English gloss: `"cut"`. Hindi gloss: `"काटना"`.
  - Record `gaddi-uni-00789`: Census 2011/2023, p. 1096, Item 316 (Bharmauri/Gaddi). Raw transcription: `badana`. English gloss: `"call"`. Hindi gloss: `"बुलाना / सादना"`.
  - Record `gaddi-uni-00801`: Census 2011/2023, p. 1096, Item 327 (Bharmauri/Gaddi). Raw transcription: `badna`. English gloss: `"harvest"`. Hindi gloss: `"फसल काटना"`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00784`
  - Lemma: `बदन` (`part_of_speech: "verb"`, `homonym_index: null`)
  - Sense 1: `"to cut"` (`definition_hi: "काटना"`, `definition_ur: "کاٹنا"`)
  - Sense 2: `"to call; shout"` (`definition_hi: "बुलाना / सादना"`, `definition_ur: "بلانا"`)
  - Sense 3: `"to harvest; reap"` (`definition_hi: "फसल काटना"`, `definition_ur: "فصل کاٹنا"`)
  - Attestations Preserved: Census 2011 (Items 309, 316, 327), Census 2023 LSI (p. 1096).
- **Reason for Uncertainty:**
  Sense 1 ("to cut") and Sense 3 ("to harvest") represent genuine polysemy (agricultural harvesting is crop-cutting < OIA *vardh-* / *badh-*). However, Sense 2 ("to call; shout" < OIA *vad-*, *vadana* "to speak, utter") is an unrelated verbal root.
- **Evidence / Confirmation Needed:**
  Native speaker elicitation of the verbal paradigms for "to call/shout" (cf. Pahari *saddṇā* vs *badṇā*) versus "to reap/cut" (*bāḍhṇā* / *badṇā*).
- **Alternatives:**
  - *Alternative A (Current):* Retain all 3 senses on `00784` with an editorial note distinguishing the calling root from the cutting root.
  - *Alternative B (Recommended upon review):* Keep Senses 1 & 3 under `बदन¹` ("to cut; harvest") and split Sense 2 into a distinct entry `बदन²` ("to call; shout") using `homonym_index`.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 37: `मरन` (marna)

- **Devanagari Form:** `मरन`
- **Part of Speech:** `verb`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00736`: Census 2011/2023, p. 1095, Item 260. Raw transcription: `marna`. English gloss: `"hit"`.
  - Record `gaddi-uni-00746`: Census 2011/2023, p. 1095, Item 270. Raw transcription: `marna`. English gloss: `"kill"`.
  - Record `gaddi-uni-00778`: Census 2011/2023, p. 1095, Item 301. Raw transcription: `marna`. English gloss: `"stab"`.
  - Record `gaddi-uni-00828`: Census 2011/2023, p. 1097, Item 352. Raw transcription: `marna`. English gloss: `"choose"`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00736`
  - Lemma: `मरन` (`part_of_speech: "verb"`, `homonym_index: null`)
  - Sense 1: `"to hit; strike"` (`definition_hi: "मारना"`)
  - Sense 2: `"to kill"` (`definition_hi: "मार डालना / वध करना"`)
  - Sense 3: `"to stab; pierce"` (`definition_hi: "भोंकना / चुभोना"`)
  - Sense 4: `"to choose; select"` (`definition_hi: "चुनना"`)
  - Attestations Preserved: Census 2011 (Items 260, 270, 301, 352), Census 2023 LSI (p. 1095).
- **Reason for Uncertainty:**
  Senses 1, 2, and 3 ("hit", "kill", "stab") are classic polysemes of the transitive/causative verb *mārnā* (*māran*). However, Sense 4 ("choose; select") from Census Item 352 is highly anomalous. It is likely:
  1. An informant misunderstanding of Hindi *mānnā* (to accept/agree/choose) or *varaṇ* (to choose/elect).
  2. A field interviewer transcription error in the census questionnaire.
- **Evidence / Confirmation Needed:**
  Native speaker elicitation for "to choose / select" in Bharmauri Gaddi (e.g., *chuṇnā*, *chʰāṅṭnā*).
- **Alternatives:**
  - *Alternative A (Current):* Retain Sense 4 with an explicit editorial flag marking "choose" as a doubtful census elicitation gloss.
  - *Alternative B:* Quarantine Sense 4 into editorial notes while keeping Senses 1–3 on the main lemma.
- **Status:** **PENDING HUMAN REVIEW**

---

### Group 42: `लमम` (lamma)

- **Devanagari Form:** `लमम`
- **Part of Speech:** `adjective`
- **Dialect / Variety:** `hp_chamba_bharmaur` (Bharmauri / Chamba Gaddi)
- **Original Source Items & Transcriptions:**
  - Record `gaddi-uni-00549`: Census 2011/2023, p. 1090, Item 55. Raw transcription: `lamma`. English gloss: `"tall"`. Hindi gloss: `"लंबा / ऊँचा"`.
  - Record `gaddi-uni-00855`: Census 2011/2023, p. 1097, Item 378. Raw transcription: `lamma`. English gloss: `"good"`. Hindi gloss: `"अच्छा"`. Recorded synonyms: `["छैɭ", "छैḷ"]`.
- **Current Database Representation:**
  - Entry ID: `gaddi-uni-00549`
  - Lemma: `लमम` (`part_of_speech: "adjective"`, `homonym_index: null`)
  - Sense 1: `"tall; long"` (`definition_hi: "लंबा / ऊँचा"`, `definition_ur: "لمبا"`)
  - Sense 2: `"good; fine"` (`definition_hi: "अच्छा / भला"`, `definition_ur: "اچھا"`)
  - Attestations Preserved: Census 2011 (Items 55, 378), Census 2023 LSI (p. 1090).
- **Reason for Uncertainty:**
  *Lammā* regularly means "long / tall" across Western Pahari and Punjabi (< OIA *lamba-*). In Gaddi and Dogri, the standard words for "good / fine" are *chhaiḷ* (`छैळ` / `शैल`) or *bhalā* (`भला`). The gloss "good" in Item 378 may represent:
  1. A metaphorical extension ("fine / grand / noble / upstanding").
  2. An informant elicitation anomaly where *lamma* was given in response to an ambiguous prompt.
- **Evidence / Confirmation Needed:**
  Native speaker verification of whether *lammā* can idiomatically mean "good / fine" in Bharmauri Gaddi expressions.
- **Alternatives:**
  - *Alternative A (Current):* Retain both senses, explicitly flagging Sense 2 with an editorial note.
  - *Alternative B:* Relegate Sense 2 to an editorial field note pending speaker confirmation.
- **Status:** **PENDING HUMAN REVIEW**

---

## 3. Summary of Status & Next Steps

All seven dossiers remain strictly preserved in their current state in `data/dictionary_unified.json` and `src/gaddi/resources/dictionary_unified.json`. No unverified changes will be applied until human review and native-speaker field feedback are received.
