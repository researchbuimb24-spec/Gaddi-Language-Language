import re

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/comp_lex_bharmauri_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
parsed = []
for line in lines:
    line_str = line.strip()
    if not line_str or line_str.startswith("PDF") or line_str.startswith("Comparative") or line_str.startswith("Sl.") or line_str.isdigit():
        continue
    m = re.match(r'^(\d{1,3})\s+(.*)$', line_str)
    if m:
        num = int(m.group(1))
        rest = m.group(2).strip()
        parsed.append((num, rest))
    else:
        if parsed:
            prev_num, prev_rest = parsed[-1]
            parsed[-1] = (prev_num, prev_rest + " " + line_str)

# Let's write out all rows with parsed tokens
with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/all_parsed_rows.txt', 'w', encoding='utf-8') as out:
    for num, rest in parsed:
        out.write(f"{num:3d} | {rest}\n")

print(f"Wrote {len(parsed)} rows to all_parsed_rows.txt")

