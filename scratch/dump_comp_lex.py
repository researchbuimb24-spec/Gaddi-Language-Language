import pypdf

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/comp_lex_bharmauri_raw.txt', 'w', encoding='utf-8') as f:
    for pdf_p in range(1113, 1125):
        text = reader.pages[pdf_p - 1].extract_text() or ""
        f.write(f"\n{'='*30} PDF {pdf_p} (Printed {pdf_p - 24}) {'='*30}\n")
        f.write(text)

print("Dumped comparative lexicon pages.")

