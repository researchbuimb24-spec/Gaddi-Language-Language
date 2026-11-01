import pypdf
import json

reader = pypdf.PdfReader('C:/Users/Hp/Documents/Gaddi-Python-Language/data/source_intake/LSI_HIMACHAL_PRADESH.pdf')

# Pages 1113 to 1124 (indices 1112 to 1123)
all_rows = []

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
    
    # Sort tokens by y descending (top to bottom), then x ascending
    # Group by y coordinate with a small tolerance (e.g. 4 points)
    # Filter out header elements (y > 720 or y < 60)
    body_tokens = [t for t in tokens if 60 <= t[1] <= 725]
    
    # Cluster into lines by y
    lines = []
    current_line = []
    current_y = None
    
    # Sort by y descending
    body_tokens.sort(key=lambda item: -item[1])
    
    for x, y, text in body_tokens:
        if current_y is None:
            current_y = y
            current_line.append((x, y, text))
        elif abs(current_y - y) <= 4.0:
            current_line.append((x, y, text))
        else:
            # Sort current line by x ascending
            current_line.sort(key=lambda item: item[0])
            lines.append(current_line)
            current_line = [(x, y, text)]
            current_y = y
            
    if current_line:
        current_line.sort(key=lambda item: item[0])
        lines.append(current_line)
        
    for line in lines:
        # Check if line has a Sl No (< 100) or is a continuation
        sl_tokens = [t[2] for t in line if t[0] < 100 and t[2].isdigit()]
        gloss_tokens = [t[2] for t in line if 95 <= t[0] < 190]
        gaddi_tokens = [t[2] for t in line if t[0] >= 415]
        
        all_rows.append({
            "pdf_page": pdf_p,
            "printed_page": printed_p,
            "y": line[0][1],
            "sl_no": sl_tokens[0] if sl_tokens else None,
            "gloss": " ".join(gloss_tokens).strip(),
            "gaddi": " ".join(gaddi_tokens).strip()
        })

print(f"Total line clusters: {len(all_rows)}")
# Print first 40 rows
for r in all_rows[:40]:
    if r['sl_no'] or r['gloss'] or r['gaddi']:
        print(f"p.{r['printed_page']:4d} | Sl {str(r['sl_no']):4s} | Gloss: {r['gloss']:25s} | Gaddi: {r['gaddi']}")

