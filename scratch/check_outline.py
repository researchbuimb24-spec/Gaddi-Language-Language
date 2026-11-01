import pypdf
reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')
print("Num pages:", len(reader.pages))
try:
    outline = reader.outline
    print("Outline length:", len(outline) if outline else 0)
    for item in outline[:30]:
        if isinstance(item, list):
            print("  Sublist len:", len(item))
        else:
            print("  Title:", getattr(item, 'title', str(item)))
except Exception as e:
    print("Outline error:", e)

