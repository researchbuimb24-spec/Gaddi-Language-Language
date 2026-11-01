from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("=== PAGE ")
for i in range(1, 4):
    print(f"=== PAGE {i} ===")
    print(pages[i])

