from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
txt_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's see pages 4, 5, 6, 7, 8, 9, 10, 11
pages = text.split("=== PAGE ")
for p in pages[1:]:
    header = p.split("\n")[0]
    print(f"=== {header} ===")
    print(p[:1500])
    print("=" * 60)

