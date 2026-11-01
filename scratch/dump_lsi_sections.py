import pypdf

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

def dump_pages(page_nums, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        for p in page_nums:
            f.write(f"\n{'='*30} PAGE {p} {'='*30}\n")
            text = reader.pages[p - 1].extract_text() or ""
            f.write(text)

dump_pages(range(1, 15), 'C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/toc_pages.txt')
print("TOC pages dumped.")

