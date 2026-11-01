import json
from pathlib import Path
from gaddi.models import LexicalEntry

uni_path = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data\dictionary_unified.json")
with open(uni_path, "r", encoding="utf-8") as f:
    raw = json.load(f)

entries = [LexicalEntry.from_dict(d) for d in raw]
print(f"Loaded {len(entries)} LexicalEntry objects successfully.")
