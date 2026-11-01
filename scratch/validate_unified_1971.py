import json
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from gaddi.models import LexicalEntry, Source, Variety
from gaddi.validator import GaddiValidator
from gaddi.registry import SourceRegistry, VarietyRegistry

with open(repo_root / "data/sources.json", encoding="utf-8") as f:
    s_data = json.load(f)
with open(repo_root / "data/varieties.json", encoding="utf-8") as f:
    v_data = json.load(f)
with open(repo_root / "data/dictionary_unified.json", encoding="utf-8") as f:
    dict_data = json.load(f)

sources = SourceRegistry([Source.from_dict(s) for s in s_data])
varieties = VarietyRegistry([Variety(**v) for v in v_data])
validator = GaddiValidator(sources, varieties)

print(f"Validating {len(dict_data)} entries in dictionary_unified.json...")
entries = [LexicalEntry.from_dict(d) for d in dict_data]

blocking_errors = []
for e in entries:
    errs = validator.validate_entry(e)
    if errs:
        blocking_errors.extend(errs)
        print(f"Error in {e.id}: {[err.message for err in errs]}")

print(f"Individual validation complete: {len(blocking_errors)} blocking errors across {len(entries)} entries.")

# Variety distribution
from collections import Counter
var_counts = Counter(e.variety_id for e in entries)
print("Varieties breakdown in unified dictionary:")
for v, c in var_counts.most_common():
    print(f"  {v}: {c}")

ev_counts = Counter(e.evidence_status for e in entries)
print("Evidence status breakdown in unified dictionary:")
for ev, c in ev_counts.most_common():
    print(f"  {ev}: {c}")

