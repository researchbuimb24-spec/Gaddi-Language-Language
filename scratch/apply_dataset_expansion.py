import json
import shutil
from pathlib import Path
from simulate_expansion import all_entries

repo_root = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language")
data_path = repo_root / "data" / "dictionary_unified.json"
res_path = repo_root / "src" / "gaddi" / "resources" / "dictionary_unified.json"

print(f"Writing {len(all_entries)} unified entries to {data_path}...")
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(all_entries, f, ensure_ascii=False, indent=2)

print(f"Synchronizing {res_path}...")
shutil.copyfile(data_path, res_path)

# Byte verification
with open(data_path, "rb") as f1, open(res_path, "rb") as f2:
    b1 = f1.read()
    b2 = f2.read()
    assert b1 == b2, "Byte mismatch between data and resource dictionary_unified.json!"
print(f"SUCCESS: Synchronized dictionary_unified.json ({len(b1):,} bytes).")

# Ensure sources.json is synchronized
src_data = repo_root / "data" / "sources.json"
src_res = repo_root / "src" / "gaddi" / "resources" / "sources.json"
shutil.copyfile(src_data, src_res)
with open(src_data, "rb") as f1, open(src_res, "rb") as f2:
    assert f1.read() == f2.read()
print("SUCCESS: Synchronized sources.json.")

