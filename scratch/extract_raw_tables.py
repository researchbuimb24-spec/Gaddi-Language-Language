from pathlib import Path
import re

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect sections 4.1.1 to 4.1.5
for sec in [
    ("Table 1", "Seasons", r'4\.1\.1\s+Seasons.*?Table 1\.[^\n]*'),
    ("Table 2", "Months", r'4\.1\.2\s+Months.*?Table 2\.[^\n]*'),
    ("Table 3", "Days", r'4\.1\.3\s+Days.*?Table 3\.[^\n]*'),
    ("Table 4", "Cardinals", r'Cardinals\s*\n\s*Gaddi.*?Table 4\.[^\n]*'),
    ("Table 5", "Ordinals", r'Ordinals\s*\n\s*Gaddi.*?Table 5\.[^\n]*'),
    ("Table 6", "Own Gen", r'Gaddi Addresser→ Addressee.*?Table 6\.[^\n]*'),
    ("Table 7", "Partial", r'b\.\s+Partial-Blood Relationship.*?Table 7\.[^\n]*'),
    ("Table 8", "1st Asc", r'c\.\s+First Ascending Generation.*?Table 8\.[^\n]*'),
    ("Table 9", "2nd Asc", r'd\.\s+Second Ascending Generation.*?Table 9\.[^\n]*'),
    ("Table 10", "1st Desc", r'e\.\s+First Descending Generation.*?Table 10\.[^\n]*'),
    ("Table 11", "2nd Desc", r'f\.\s+Second Descending Generation.*?Table 11\.[^\n]*'),
    ("Table 12", "Affinal", r'II\.\s+Affinal Relationships:.*?Table 12\.[^\n]*'),
    ("Table 13", "Adoption", r'III\.\s+Kinship by Adoption/Affiliation:.*?Table 13\.[^\n]*'),
]:
    m = re.search(sec[2], text, re.DOTALL)
    if m:
        print(f"=== {sec[0]}: {sec[1]} ===")
        print(m.group(0).strip())
        print("=" * 50)
    else:
        print(f"FAILED to match {sec[0]}")

