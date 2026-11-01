import json
import re
from pathlib import Path
import pypdf

PDF_PATH = Path(r"C:\Users\Hp\Documents\grammarOfGaddi.book.pdf")
DATA_DIR = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\data")
RES_DIR = Path(r"C:\Users\Hp\Documents\Gaddi-Python-Language\src\gaddi\resources")

reader = pypdf.PdfReader(str(PDF_PATH))

pages_lines = []
for pno in range(18, 134):
    text = reader.pages[pno].extract_text()
    for line in text.splitlines():
        pages_lines.append((pno + 1, line))

# Match real example headers
real_ex = []
for idx, (pno, line) in enumerate(pages_lines):
    m = re.match(r'^\s*(?:\((\d+)\)|(\d+)\))(?:\s+(.*)|$)', line)
    if m:
        num = int(m.group(1) or m.group(2))
        rem = m.group(3) or ''
        if rem.startswith(',') or rem.startswith('.'):
            continue
        if 1 <= num <= 269:
            real_ex.append((num, pno, idx, rem, line))

real_ex.sort(key=lambda x: x[2])

def is_header(line):
    l = line.strip()
    if re.search(r'^\d+\s+A\s+GRAMMAR', l, re.I): return True
    if re.search(r'A\s+GRAMMAR\s+oF\s+GADDI', l, re.I): return True
    if re.search(r'tH\s*e\s+G\s*ADDIS\s+AND', l, re.I): return True
    if re.search(r'PHoNet\s*ICS\s+AND', l, re.I): return True
    if re.search(r'MAjo\s*R\s+w?\s*o?\s*RD\s+CL\s*A?\s*S', l, re.I): return True
    if re.search(r'Mo\s*RPH\s*oSYN\s*tA?\s*x', l, re.I): return True
    if re.search(r'CLAUS\s*e\s+t\s*YP\s*e\s*S', l, re.I): return True
    if re.search(r'APP\s*eNDI\s*x', l, re.I): return True
    return False

def clean_example_lines(num, pno, raw_lines):
    first = raw_lines[0]
    has_sub = bool(re.search(r'(?:^|\s)a\.\s+', first)) or (len(raw_lines) > 1 and bool(re.match(r'^\s*a\.\s+', raw_lines[1])))
    
    ex_lines = []
    prose_lines = []
    
    if not has_sub:
        in_ex = True
        for idx, line in enumerate(raw_lines):
            l = line.strip()
            if in_ex:
                ex_lines.append(line)
                if idx >= 1 and (re.search(r'[’\']\s*(?:\([^)]+\))?\s*$', l) or re.search(r'\([A-Za-z]+ \d{4}[^)]*\)\s*$', l)):
                    in_ex = False
            else:
                prose_lines.append(line)
    else:
        expected_letter_idx = 0
        in_ex = True
        for idx, line in enumerate(raw_lines):
            l = line.strip()
            if idx == 0:
                ex_lines.append(line)
                if re.search(r'(?:^|\s)a\.\s+', l):
                    expected_letter_idx = 1
                continue
            
            exp_letter = chr(ord('a') + expected_letter_idx)
            m_sub = re.match(r'^\s*' + exp_letter + r'\.\s+', l)
            if m_sub and in_ex:
                ex_lines.append(line)
                expected_letter_idx += 1
            elif in_ex:
                if re.match(r'^[A-Z][a-z]+ [a-z]+ [a-z]+', l) and len(l) > 50 and not ('[' in l or '‘' in l or '’' in l):
                    in_ex = False
                    prose_lines.append(line)
                elif l.startswith('Table ') or re.match(r'^\d+\.\d+', l):
                    in_ex = False
                    prose_lines.append(line)
                elif re.match(r'^\s*[a-z]\.\s+', l):
                    in_ex = False
                    prose_lines.append(line)
                else:
                    ex_lines.append(line)
            else:
                prose_lines.append(line)
                
    return ex_lines, prose_lines

processed_examples = []
for i in range(len(real_ex)):
    num, pno, start_idx, rem, first_line = real_ex[i]
    end_idx = real_ex[i+1][2] if i + 1 < len(real_ex) else len(pages_lines)
    raw = [l for _, l in pages_lines[start_idx:end_idx] if not is_header(l) and l.strip()]
    ex_l, pr_l = clean_example_lines(num, pno, raw)
    
    txt = "\n".join(ex_l)
    prose_txt = "\n".join(pr_l).strip() if pr_l else None
    
    ch = 1 if pno <= 27 else (2 if pno <= 54 else (3 if pno <= 85 else (4 if pno <= 115 else 5)))
    
    # Extract attribution if present at end e.g. (Mehta 2016, ex. 1.3)
    attr = "Kumari et al. (2026)"
    m_attr = re.search(r"\((Mehta|Grierson|Anand|Sharma|Naik|Prasad)[^)]+\)", txt)
    if m_attr:
        attr = m_attr.group(0).strip("()")
    elif num in [1, 2, 3, 4, 5]:
        attr = "Grierson (1916)"
    
    # Extract translation in single quotes from the example text ONLY
    translations = re.findall(r"[‘']([^'’]+)[’']", txt)
    clean_trans = "; ".join(translations) if translations else ""
    
    # Special cleanups for edge cases:
    # Ex 1: uses comma after Gaddi word
    if num == 1:
        clean_trans = "by/in a horse or horses; by/in a house or houses; by/in a young man or young men; by/in a girl; by/in girls; by/in daughter or daughters"
    elif num == 2:
        clean_trans = "to/for; with/by means of; from; from/in; with/together with; of; in; near"
    elif num == 73:
        clean_trans = "He saw a donkey."
    elif num == 74:
        clean_trans = "The donkey saw him."
    elif num == 123:
        clean_trans = "1, 2, 3, 4, 5, 6, 7...; one, two, three, four, five, six, seven..."
    elif num == 124:
        clean_trans = "Forty-seven: Forty + Seven = 47; Three hundred: Three * Hundred = 300; Two hundred and thirty: Two * Hundred + Thirty = 230"
    elif num == 126:
        clean_trans = "Who is the first girl on the left?; *Who is the one girl on the left?"
    elif num == 127:
        clean_trans = "I will take a half of that cake.; It cost me a quarter of my salary."
    elif num == 128:
        clean_trans = "I gave him one-third of all the profits.; My family owns four-sevenths of the property."
    elif num == 130:
        clean_trans = "I called her once.; I called her *one/*first."
    elif num == 132:
        clean_trans = "We gave two apples each to seven kids.; Everyone in the class must board the bus one-by-one."
    elif num == 243:
        clean_trans = "I bought a car.; What did you buy ____?"
    elif num == 249:
        clean_trans = "What does Ram know [Sita ate ___]?"

    processed_examples.append({
        "example_id": f"kumari-ex-{num:03d}",
        "example_number": num,
        "chapter": ch,
        "printed_page": pno - 17,
        "pdf_page": pno,
        "raw_text": txt,
        "english_translation": clean_trans,
        "context_notes": prose_txt,
        "attribution": attr,
        "variety_id": "hp_kangra_palampur",
        "variety_name": "Kangra Gaddi (Palampur)",
        "source_id": "kumari_2026",
        "evidence_status": "comparative_only",
        "is_jk_verified": False,
        "license": "CC BY-NC 4.0"
    })

print(f"Processed {len(processed_examples)} examples.")

# Save to data and resources
with open(DATA_DIR / "gaddi_examples.json", "w", encoding="utf-8") as f:
    json.dump(processed_examples, f, ensure_ascii=False, indent=2)

with open(RES_DIR / "gaddi_examples.json", "w", encoding="utf-8") as f:
    json.dump(processed_examples, f, ensure_ascii=False, indent=2)

print("Saved cleanly to data/gaddi_examples.json and src/gaddi/resources/gaddi_examples.json")
