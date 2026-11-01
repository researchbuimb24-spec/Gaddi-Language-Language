from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent

with open(repo_root / "scratch/build_and_verify_jk_dataset.py", "r", encoding="utf-8") as f:
    part1 = f.read()

with open(repo_root / "scratch/append_records.py", "r", encoding="utf-8") as f:
    part2 = f.read()

trailer = """
# Convert raw_records into LexicalEntry objects
entries = []
for i, r in enumerate(raw_records):
    eid = f"jk-lex-{i+1:05d}"
    senses = []
    for s_idx, s in enumerate(r["senses"]):
        senses.append(Sense(
            sense_index=s_idx + 1,
            definition_en=s["en"],
            definition_hi=s["hi"],
            definition_ur=s.get("ur"),
            semantic_field=s.get("field", "general"),
            examples=[]
        ))
    
    attestations = []
    for s in r["senses"]:
        attestations.append(Attestation(
            source_id="dar_sheikh_2022",
            page_or_section=s.get("table", "Aligarh Journal of Linguistics 11: 245-258"),
            source_spelling=r["orig"],
            context=s.get("context", "")
        ))

    entry = make_entry(
        eid=eid,
        lemma_dev=r["lemma_dev"],
        ipa=r["ipa"],
        orig_trans=r["orig"],
        pos=r["pos"],
        gender=r["gender"],
        senses=senses,
        attestations=attestations,
        categories=r["cats"],
        extra_meta={
            "comparative_notes": r.get("comp_notes"),
            "kinship_algebra": r.get("kinship_algebra"),
            "numeric_value": r.get("numeric_value"),
            "etymology": r.get("etymology", "")
        }
    )
    entries.append(entry)

print(f"Total entries created: {len(entries)}")

# Validate each entry individually
all_errors = []
all_warnings = []
for entry in entries:
    errs = validator.validate_entry(entry)
    warns = validator.check_warnings(entry)
    if errs:
        all_errors.extend(errs)
        print(f"ERROR in {entry.id} ({entry.lemma_devanagari}): {errs}")
    if warns:
        all_warnings.extend(warns)
        print(f"WARNING in {entry.id} ({entry.lemma_devanagari}): {warns}")

print(f"Individual validation: {len(all_errors)} errors, {len(all_warnings)} warnings.")

# Validate whole collection
report = validator.validate_collection(entries)
print(f"Collection validation: valid={report.is_valid}, {len(report.errors)} errors, {len(report.warnings)} warnings.")
if report.errors:
    for e in report.errors:
        print("  Coll error:", e.message)
"""

with open(repo_root / "scratch/run_full_validation_test.py", "w", encoding="utf-8") as f:
    f.write(part1 + "\n\n" + part2 + "\n\n" + trailer)

print("Regenerated scratch/run_full_validation_test.py")
