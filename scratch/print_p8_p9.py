from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("=== PAGE ")
print("=== PAGE 8 ===")
print(pages[8])
print("=== PAGE 9 ===")
print(pages[9])

