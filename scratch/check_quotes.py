with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\b[a-zA-Zāīūēōḍṭṇṛṣśñŋ̃:/?\-]+\b[\s\t]+[‘\'"][^’\'"]+[’\'"])', text)
print("Matches with unicode quotes:", len(matches))
for m in matches[:40]:
    print("  ", m.strip())

