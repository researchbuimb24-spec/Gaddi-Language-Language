from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("=== PAGE ")
for p_num in range(4, 12):
    p = pages[p_num]
    print(f"\n******************* PAGE {p_num} *******************")
    print(p)

