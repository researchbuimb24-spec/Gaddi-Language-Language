import pypdf

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

# Let's inspect page 1113 (index 1112)
page = reader.pages[1112]

elements = []
def visitor_body(text, cm, tm, font_dict, font_size):
    if text.strip():
        # tm[4] is x, tm[5] is y
        elements.append((tm[4], tm[5], text.strip()))

page.extract_text(visitor_text=visitor_body)
print(f"Extracted {len(elements)} positioned tokens from PDF page 1113")

# Print first 30 elements with coordinates
for elem in elements[:35]:
    print(f"x={elem[0]:6.1f}, y={elem[1]:6.1f}: {elem[2]}")

