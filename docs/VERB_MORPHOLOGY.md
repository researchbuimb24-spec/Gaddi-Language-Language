# Gaddi Verb Morphology & Grammatical Paradigms

## 1. Overview & Linguistic Scope

This module provides structured, source-backed computational representations of Gaddi verbal inflection, tense-aspect-mood (TAM) realization, agreement morphology (person-number-gender-honorificity / PNGH), causative alternations, and clausal negation.

All data in this module is extracted strictly from peer-reviewed descriptive linguistics and published technical grammars:
1. **Mehta, Shreya (2019)**, *"The Morphological Realization of Tense, Aspect and Mood in Gaddi"*, *Smart Moves Journal IJELLH*, Vol. 7, Issue 7, pp. 927–943. Licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
2. **Kumari, P., Mehta, S., Nair, A., Nayak, A., Roy, Y., & Sharma, V. (2026)**, *A Grammar of Gaddi*, UCL Press, London. DOI: `10.14324/111.9781800089938`. Licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

### Strict Anti-Fabrication Rule
A central scientific commitment of the Gaddi Language Library is that **no verbal paradigms are fabricated to fill empty cells**. If a grammatical category or inflected form is not explicitly printed in primary fieldwork data, it remains unrecorded.
- **Complete Canonical Paradigm:** Exactly one verb in the current corpus has a complete 96-cell canonical paradigm table verified from fieldwork: **`həsɳɑ`** (*to laugh*), published in Mehta (2019, p. 941).
- **Isolated Attested Examples:** All other 34 recorded verbs (such as *kərɳɑ*, *ɡətʃɳɑ*, *bədʒɳɑ*, *dʒəmɳɑ*, *muɭɭɳɑ*, *likʰɳɑ*, *kʰəridɳɑ*) consist solely of isolated sentence examples, causative pairs, or negative constructions attested in the literature. They are explicitly marked as `isolated_attested_example` and `is_complete: false`.

### Variety & Locality Notice
All verbal morphology data currently documented in this module reflects the **Kangra Gaddi** variety spoken around **Palampur, Kangra District, Himachal Pradesh** (`hp_kangra_palampur`). In accordance with project safety rules, **Kangra Gaddi verbal forms must never be labeled or assumed to be identical to Jammu & Kashmir Gaddi**. They serve as an empirical comparative baseline pending dedicated fieldwork in J&K.

---

## 2. Morphological Categories & Exponents

In Gaddi, verbal inflections are formed using three distinct morphological strategies (Kumari et al. 2026, Table 3.13):
1. **Direct affixation** onto the verbal base.
2. **Auxiliary verbs** following the lexical verb.
3. **Periphrastic constructions** combining a participial form of the main verb with an auxiliary verb (*kərɳɑ* or *ləɡɳɑ*).

### A. Tense

| Tense Category | Morphological Strategy | Exponent | Agreement & Notes |
| :--- | :--- | :--- | :--- |
| **Past** | Auxiliary | `tʰ-` + agreement (`-u` M.SG, `-i` F.SG, `-ijɛ` PL/HON) | Forms: `tʰu` (M.SG), `tʰi` (F.SG), `tʰijɛ` (PL/HON). Agrees in gender, number, honorificity. |
| **Future** | Affixation | `-ɳ-` + agreement (`-ɑ` M.SG, `-i` F.SG, `-ɛ` PL/HON) | Homophonous with infinitival marker `-ɳɑ`. Agrees with subject/object. |
| **Perfect** | Affixation | `-ur-` + agreement (`-ɑ` M.SG, `-i` F.SG, `-ɛ` PL/HON) | Denotes a past event with present relevance; focuses on resultant state. |
| **Present** | Auxiliary | `h-` + agreement (`-ɑ` SG, `-in` PL/HON) | Formed with present indicative auxiliary `hɑ` (SG) / `hin` (PL/HON). |

### B. Aspect

| Aspect Category | Morphological Strategy | Exponent | Notes & Syntax |
| :--- | :--- | :--- | :--- |
| **Imperfective** | Affixation | `-d-` + agreement (`-ɑ`, `-i`, `-ɛ`) | Attention on internal structure; situation is unbounded. Also forms habitual. |
| **Perfective** | Affixation | `-u` (M.SG/MA), `-i` (F.SG/FE), `-ɛ` (PL/HON) | Event viewed as an indivisible whole. Gender agreement is labeled `gend` (MA/FE). |
| **Progressive** | Periphrastic | Main verb in PFV (`-u`/`-i`) + AUX `kər-d-` + AGR (`-ɑ`/`-i`/`-ɛ`) | Main verb carries perfective `-u`/`-i` agreeing in `gend`; auxiliary is imperfective of *kərɳɑ*. |
| **Inchoative** | Periphrastic | Main verb in INF (`-ɳ-` + AGR) + AUX `ləɡ-ur-` + AGR | Indicates inception or beginning of state change; auxiliary is perfect form of *ləɡɳɑ*. |

### C. Mood

| Mood Category | Morphological Strategy | Exponent | Notes & Usage |
| :--- | :--- | :--- | :--- |
| **Indicative** | Auxiliary | `h-` + agreement (`-ɑ` SG, `-in` PL/HON) | Asserts real, factual state. Present tense copula is obligatory; optional in some futures. |
| **Epistemic** | Affixation | `-ɭɭ-` + agreement (`-ɑ`, `-i`, `-ɛ`) | Expresses speaker confidence, conviction, or deduction ("would be / must have"). |
| **Imperative** | Affixation | `-ɑ` (M.SG), `-i` (F.SG), `-ɛ` (PL/HON) | Command, injunction, or request agreeing with addressee or object. |

---

## 3. The Canonical Paradigm of *həsɳɑ* (*to laugh*)

The table below reproduces the full canonical 96-cell paradigm printed in **Mehta (2019, p. 941)** (also reproduced in Kumari et al. 2026, Table 4.1):

| Row / Category | M.SG | F.SG | M.SG.HON | F.SG.HON | M.PL | F.PL | M.PL.HON | F.PL.HON |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PASTAUX** | `tʰu` | `tʰi` | `tʰijɛ` | `tʰijɛ` | `tʰijɛ` | `tʰijɛ` | `tʰijɛ` | `tʰijɛ` |
| **PERFECT** | `həsurɑ` | `həsuri` | `həsurɛ` | `həsurɛ` | `həsurɛ` | `həsurɛ` | `həsurɛ` | `həsurɛ` |
| **FUTURE** | `həsɳɑ` | `həsɳi` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` |
| **IMPERATIVE** | `həsɑ` | `həsi` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` |
| **EPISTEMIC** | `həsɭɭɑ` | `həsɭɭi` | `həsɭɭɛ` | `həsɭɭɛ` | `həsɭɭɛ` | `həsɭɭɛ` | `həsɭɭɛ` | `həsɭɭɛ` |
| **INDICATIVEAUX** | `hɑ` | `hɑ` | `hin` | `hin` | `hin` | `hin` | `hin` | `hin` |
| **IMPERFECTIVE** | `həsdɑ` | `həsdi` | `həsdɛ` | `həsdɛ` | `həsdɛ` | `həsdɛ` | `həsdɛ` | `həsdɛ` |
| **PERFECTIVE** | `həsu` | `həsi` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` | `həsɛ` |
| **PROG** | `həsu` | `həsi` | `həsu` | `həsi` | `həsu` | `həsi` | `həsu` | `həsi` |
| **PROGAUX** | `kərdɑ` | `kərdi` | `kərdɛ` | `kərdɛ` | `kərdɛ` | `kərdɛ` | `kərdɛ` | `kərdɛ` |
| **INCHO** | `həsɳɑ` | `həsɳi` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` | `həsɳɛ` |
| **INCHOAUX** | `ləɡurɑ` | `ləɡuri` | `ləɡurɛ` | `ləɡurɛ` | `ləɡurɛ` | `ləɡurɛ` | `ləɡurɛ` | `ləɡurɛ` |

All 96 cells are stored with full morpheme segmentation (`həs-ur-ɑ`, `həs-d-i`, `həs-ɭɭ-ɛ`, etc.), interlinear glosses (`laugh-PRF-M.SG`, `laugh-IPFV-F.SG`, etc.), and provenance metadata referencing Mehta (2019, p. 941).

---

## 4. Causative Morphology (Kumari et al. 2026, Table 3.12)

Gaddi displays morphological causative formation in the perfective aspect, distinguishing direct/transitive causatives (suffix `-ɑ-`) from secondary/indirect causatives (suffix `-ʋɑ-`):

| Verb Root | Gloss | Transitive Perfective Form | Secondary Causative Form | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `bədʒɳɑ` | *to ring* | `bədʒ-ɑ-i` | `bədʒ-ʋɑ-i` | Kumari et al. (2026), p. 51, Table 3.12 |
| `dʒəmɳɑ` | *to freeze* | `dʒəm-ɑ-jɑ` | `dʒəm-ʋɑ-jɑ` | Kumari et al. (2026), p. 51, Table 3.12 |
| `ɡʰumɳɑ` | *to revolve/roam* | `ɡʰum-ɑ-u` | `ɡʰum-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |
| `nipiɳɑ` | *to bend/squeeze* | `nipi-ɑ-i` | `nipi-ʋɑ-i` | Kumari et al. (2026), p. 51, Table 3.12 |
| `uɽɳɑ` | *to fly* | `uɽ-ɑ-u` | `uɽ-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |
| `tʃipkɳɑ` | *to stick* | `tʃipk-ɑ-u` | `tʃipək-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |
| `kʰilɑɳɑ` | *to feed/eat* | `kʰil-ɑ-u` | `kʰil-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |
| `huɳɑɳɑ` | *to tell/listen* | `huɳ-ɑ-u` | `huɳ-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |
| `pəɽɑɳɑ` | *to read/teach* | `pəɽ-ɑ-u` | `pəɽ-ʋɑ-u` | Kumari et al. (2026), p. 51, Table 3.12 |

---

## 5. Clausal Negation & Negative Verb Constructions (Section 5.5.2)

Gaddi employs four distinct negation particles: `/nɑ/`, `/ni/`, `/nətʰi/`, and prohibitive `/mətʰ/`:

1. **Standard Future Negation:** Precedes the verb:
   - `rɑm pɑləmpuro nɑ i-ɳ-ɑ` (*Ram will not come to Palampur*, ex. 251a).
2. **Present Indicative Negation:**
   - With auxiliary: `rɑm kʰərɑ ɡobru ni hɑ` (*Ram is not a good boy*, ex. 251b).
   - Negative copula: `rɑm kʰərɑ ɡobru nətʰi` (*Ram is not a good boy*, ex. 251c).
3. **Prohibitive Imperative:** Uses `mətʰ` preceding the imperative verb:
   - `ɑːndər-ɔu mətʰ ɡətʃtʃʰ` (*Don't go inside!*, ex. 251d, 255).
4. **Perfective Aspect Negation:** Either precedes main verb or intervenes between verb and past auxiliary:
   - `rɑm ʃimlɑ-dʒo nɑ ɡətʃʰ-ur-ɑ tʰ-u` (*Ram had not gone to Shimla*, ex. 252a).
   - `rɑm ʃimlɑ-dʒo ɡəcʰ-ur-ɑ nɑ tʰ-u` (inter-verbal negation, ex. 252b).
5. **Imperfective Aspect Negation:** Precedes main verb; indicative `hɑ` is ungrammatical when negated:
   - `rɑm ʃimlɑ-dʒo nɑ ɡən-d-ɑ` (*Ram does not go to Shimla*, ex. 253).
6. **Progressive Aspect Negation:**
   - Pre-verbal: `rɑm ʃimlɑ-dʒo nɑ tʃəl-u kər-d-ɑ` (*Ram is not going to Shimla*, ex. 254a).
   - Inter-verbal: `rɑm ʃimlɑ-dʒo tʃəl-u nɑ kər-d-ɑ` (ex. 254b).
7. **Modal Verb Negation:**
   - `rɑm ʃimlɛ-dʒo nɑ ɡətʃʰ-i sək-d-ɑ` (*Ram cannot go to Shimla*, ex. 256a).
   - `rɑm ʃimlɛ-dʒo ɡətʃʰ-i nɑ sək-d-ɑ` (ex. 256b).
8. **Complex Predicate Negation:**
   - `rəmmɛ ɡʰər nɑ tʃʰəɖɖ-i ditʰ-ur-ɑ` (*Ram did not leave the house*, ex. 257a).
   - `rəmmɛ ɡʰər tʃʰəɖɖ-i nɑ ditʰ-ur-ɑ` (ex. 257b).
9. **Negative Polarity Items (NPIs):**
   - With `muɭɳɑ`: `tɛs kəsi sitʰɛ bʰi nɑ muɭ-n-ɑ` (*She/He will not meet anyone*, ex. 259).

---

## 6. Python API Reference

```python
import gaddi

# 1. Retrieve all complete paradigms (e.g. həsɳɑ)
paradigms = gaddi.get_verb_paradigms()
for p in paradigms:
    print(f"Verb: {p.verb_lemma} ({p.verb_meaning_en}) - {len(p.forms)} cells")

# 2. Retrieve forms for a specific lemma
forms = gaddi.get_verb_forms("həsɳɑ")
print(f"Total forms for həsɳɑ: {len(forms)}")

# 3. Get structured paradigm grouping (distinguishes complete vs isolated)
kar_paradigm = gaddi.get_verb_paradigm("kərɳɑ")
print(f"Is complete: {kar_paradigm.is_complete}")  # False (isolated example)
print(f"Attested forms: {[f.inflected_form for f in kar_paradigm.forms]}")

# 4. Search across forms, transcription, and glosses
matches = gaddi.search_verb_forms("prohibitive")
for m in matches:
    print(f"Form: {m.inflected_form} | Ref: {m.source_reference}")

# 5. Filter by TAM category
past_forms = gaddi.default_morphology.filter_by_tense("past")
imp_forms = gaddi.default_morphology.filter_by_mood("imperative")
caus_forms = [f for f in gaddi.default_morphology._records if "causative" in (f.form_type or "")]
```

---

## 7. CLI Reference

```bash
# List all recorded verbs with paradigm status
python -m gaddi.cli morphology verbs

# Show paradigm or attested forms for a verb
python -m gaddi.cli morphology show həsɳɑ
python -m gaddi.cli morphology show bədʒɳɑ

# Filter by tense (past, future, perfect, present)
python -m gaddi.cli morphology tense past
python -m gaddi.cli morphology tense future

# Filter by mood (indicative, epistemic, imperative)
python -m gaddi.cli morphology mood imperative
python -m gaddi.cli morphology mood epistemic

# Search across inflected forms, morphemes, and glosses
python -m gaddi.cli morphology search "mətʰ"
python -m gaddi.cli morphology search "causative"

# Validate verb morphology dataset schema and integrity
python -m gaddi.cli validate
```
