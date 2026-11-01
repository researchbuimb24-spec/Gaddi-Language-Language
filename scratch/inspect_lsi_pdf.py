import pypdf
import re

pdf_path = 'C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf'
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# Search for Bharmauri / Gaddi across pages
bharmauri_pages = []
gaddi_pages = []

for idx, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    if re.search(r'bharmauri', text, re.IGNORECASE):
        bharmauri_pages.append(idx + 1)
    if re.search(r'\bgaddi\b', text, re.IGNORECASE):
        gaddi_pages.append(idx + 1)

print(f"Pages mentioning Bharmauri ({len(bharmauri_pages)}): {bharmauri_pages[:50]}")
print(f"Pages mentioning Gaddi ({len(gaddi_pages)}): {gaddi_pages[:50]}")

