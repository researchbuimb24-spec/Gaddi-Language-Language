import re
import json

with open('scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect sections by finding headers and content
headers = re.findall(r'(\d+\.[\d\.]*\s+[A-Z\s]+)', text)
print("Headers in Chapter 2:")
for h in headers[:30]:
    print(" ", h.strip())

