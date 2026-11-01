import re

with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/comp_lex_bharmauri_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect pages and extract entries
pages = text.split("==============================")
print("Pages count:", len(pages))

# Each entry starts with a number (1 to 500)
# Let's write a parser that identifies Sl. No. and tokens
lines = text.splitlines()
entry_pattern = re.compile(r'^\s*(\d{1,3})\s+([a-zA-Z\(\)\s/,-]+?)\s+([^\t\n\r]+)$')

parsed = []
current_entry = None

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
        # continuation line
        if parsed:
            prev_num, prev_rest = parsed[-1]
            parsed[-1] = (prev_num, prev_rest + " " + line_str)

print("Parsed numbered rows count:", len(parsed))
for p in parsed[:25]:
    print(f"Row {p[0]}: {p[1]}")

