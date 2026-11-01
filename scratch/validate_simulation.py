import json
from pathlib import Path
from gaddi.validator import GaddiValidator
from gaddi.registry import default_sources, default_varieties
from gaddi.models import LexicalEntry

# Ensure census_2023_lsi is registered
if not default_sources.contains("census_2023_lsi"):
    from gaddi.models import Source
    default_sources.register(Source(
        id="census_2023_lsi",
        title="Linguistic Survey of India: Himachal Pradesh",
        authors=["Language Division, Office of the Registrar General, India", "N. Gopalakrishnan", "Ranjita Pattanaik"],
        year=2023,
        publisher="Office of the Registrar General, India (ORGI), Ministry of Home Affairs, Government of India, New Delhi",
        license="Open Government Data (OGD) License India",
        credibility_tier=1,
        is_jk_primary=False
    ))

from simulate_expansion import all_entries

validator = GaddiValidator(default_sources, default_varieties)

converted_new = []
for e in all_entries[1274:]: # Check all 761 new entries
    converted_new.append(LexicalEntry.from_dict(e))

rep = validator.validate_collection(converted_new)
print(f"Validation of new entries: Valid={rep.is_valid}, Errors={len(rep.errors)}, Warnings={len(rep.warnings)}")
if rep.errors:
    print("First 10 errors:")
    for err in rep.errors[:10]:
        print(err)

