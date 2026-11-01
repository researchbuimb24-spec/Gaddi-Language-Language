import pypdf
import re

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

for p in range(50, 90):
    text = reader.pages[p - 1].extract_text() or ""
    if "BHARMAURI" in text.upper() or "GADDI" in text.upper():
        first_line = text.strip().splitlines()[0] if text.strip().splitlines() else ""
        print(f"PDF Page {p}: {first_line[:80]}")

print("\n--- Check Comparative Lexicon around page 1080-1120 ---")
for p in range(1080, 1120):
    text = reader.pages[p - 1].extract_text() or ""
    if "BHARMAURI" in text.upper() or "COMPARATIVE" in text.upper():
        first_line = text.strip().splitlines()[0] if text.strip().splitlines() else ""
        print(f"PDF Page {p}: {first_line[:80]}")

