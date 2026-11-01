from pathlib import Path
import re

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract the tables systematically
print("--- Parsing Dar & Sheikh 2022 tables ---")
lines = text.splitlines()

current_table = None
table_lines = {}

for line in lines:
    m = re.search(r'Table\s+(\d+)\.\s*(.*)', line)
    if m:
        t_num = int(m.group(1))
        t_title = m.group(2).strip()
        print(f"Found Table {t_num}: {t_title}")


