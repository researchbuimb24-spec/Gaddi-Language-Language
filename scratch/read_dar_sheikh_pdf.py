from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
pdf_path = repo_root / "data/source_intake/dar_sheikh_2022.pdf"

try:
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    print("Total pages:", len(reader.pages))
    for i, page in enumerate(reader.pages):
        print(f"\n--- PAGE {i+1} ---")
        text = page.extract_text()
        print(text[:400])
        print(f"Page text length: {len(text)}")
except Exception as e:
    print("pypdf error:", e)
    # try other packages or pypdf / pdfminer

