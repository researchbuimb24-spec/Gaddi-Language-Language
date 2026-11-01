import pypdf
import json

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

raw_lines = []

for page_idx in range(1112, 1124):
    pdf_p = page_idx + 1
    printed_p = pdf_p - 24
    page = reader.pages[page_idx]
    
    tokens = []
    def visitor(text, cm, tm, font_dict, font_size):
        t = text.strip()
        if t:
            tokens.append((tm[4], tm[5], t))
            
    page.extract_text(visitor_text=visitor)
    body_tokens = [t for t in tokens if 60 <= t[1] <= 725]
    body_tokens.sort(key=lambda item: -item[1])
    
    lines = []
    current_line = []
    current_y = None
    
    for x, y, text in body_tokens:
        if current_y is None:
            current_y = y
            current_line.append((x, y, text))
        elif abs(current_y - y) <= 4.0:
            current_line.append((x, y, text))
        else:
            current_line.sort(key=lambda item: item[0])
            lines.append(current_line)
            current_line = [(x, y, text)]
            current_y = y
            
    if current_line:
        current_line.sort(key=lambda item: item[0])
        lines.append(current_line)
        
    for line in lines:
        sl_tokens = [t[2] for t in line if t[0] < 100 and t[2].isdigit()]
        gloss_tokens = [t[2] for t in line if 95 <= t[0] < 190]
        gaddi_tokens = [t[2] for t in line if t[0] >= 415]
        
        raw_lines.append({
            "pdf_page": pdf_p,
            "printed_page": printed_p,
            "sl_no": int(sl_tokens[0]) if sl_tokens else None,
            "gloss": " ".join(gloss_tokens).strip(),
            "gaddi": " ".join(gaddi_tokens).strip()
        })

# Consolidate continuation lines
consolidated = []
for row in raw_lines:
    if row["sl_no"] is not None:
        consolidated.append(dict(row))
    else:
        if consolidated:
            prev = consolidated[-1]
            if row["gloss"]:
                prev["gloss"] = (prev["gloss"] + " " + row["gloss"]).strip()
            if row["gaddi"]:
                prev["gaddi"] = (prev["gaddi"] + " " + row["gaddi"]).strip()

print(f"Consolidated rows: {len(consolidated)}")
valid_gaddi = [r for r in consolidated if r["gaddi"] and r["gaddi"] != "-"]
print(f"Rows with non-empty Gaddi form: {len(valid_gaddi)}")

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/consolidated_comp_lex.json', 'w', encoding='utf-8') as f:
    json.dump(consolidated, f, indent=2, ensure_ascii=False)

# Show rows 40 to 80
for r in consolidated[40:80]:
    print(f"Sl {r['sl_no']:3d} | Gloss: {r['gloss']:30s} | Gaddi: {r['gaddi']}")

