from gaddi.validator import GaddiValidator
from gaddi.registry import default_sources, default_varieties
from gaddi.models import LexicalEntry
import json

v = GaddiValidator(default_sources, default_varieties)
with open('data/dictionary_unified.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

entries = [LexicalEntry.from_dict(d) for d in raw]
errors = []
warnings = []
for idx, entry in enumerate(entries):
    errs = v.validate_entry(entry)
    warns = v.check_warnings(entry)
    if errs:
        errors.extend([(entry.id, e) for e in errs])
    if warns:
        warnings.extend([(entry.id, w) for w in warns])

print(f"Total entries validated: {len(entries)}")
print(f"Total individual entry errors: {len(errors)}")
print(f"Total individual entry warnings: {len(warnings)}")
if errors:
    print("Errors:")
    for eid, err in errors[:10]:
        print(f"  {eid}: {err}")

