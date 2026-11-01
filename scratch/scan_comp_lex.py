import pypdf

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/comp_lex_outline.txt', 'w', encoding='utf-8') as f:
    for pdf_p in range(1100, 1158):
        text = reader.pages[pdf_p - 1].extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        f.write(f"PDF {pdf_p} (Printed {pdf_p - 23}): {lines[:3]}\n")

print("Wrote comparative lexicon outline.")

