with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split("==============================")

def inspect_range(start_pdf, end_pdf):
    print(f"\n================ INSPECTING PDF {start_pdf} to {end_pdf} ================")
    for p in range(start_pdf, end_pdf + 1):
        # find page in pages
        p_text = ""
        for page_block in pages:
            if f"PDF {p} " in page_block:
                p_text = page_block
                break
        if not p_text:
            continue
        lines = [l.strip() for l in p_text.splitlines() if l.strip()]
        print(f"\n--- PDF {p} ({len(lines)} lines) ---")
        for l in lines:
            if any(c in l for c in ['‘', '’', "'", '"', '–', '>']):
                print(" ", l)

inspect_range(88, 105)

