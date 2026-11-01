import pypdf

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'w', encoding='utf-8') as f:
    for pdf_p in range(78, 140):
        text = reader.pages[pdf_p - 1].extract_text() or ""
        f.write(f"\n{'='*30} PDF {pdf_p} (Printed {pdf_p - 20}) {'='*30}\n")
        f.write(text)

print("Dumped Chapter 2 Bharmauri full text.")

