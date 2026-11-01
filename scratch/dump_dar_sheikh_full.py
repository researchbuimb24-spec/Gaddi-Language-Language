from pathlib import Path
import pypdf

repo_root = Path(__file__).resolve().parent.parent
pdf_path = repo_root / "data/source_intake/dar_sheikh_2022.pdf"
out_path = repo_root / "scratch/dar_sheikh_2022_full_text.txt"

reader = pypdf.PdfReader(str(pdf_path))
with open(out_path, "w", encoding="utf-8") as f:
    for i, page in enumerate(reader.pages):
        f.write(f"=== PAGE {i+1} (Printed Page {244+i+1}) ===\n")
        f.write(page.extract_text() or "")
        f.write("\n\n")

print(f"Dumped {len(reader.pages)} pages to {out_path}")

