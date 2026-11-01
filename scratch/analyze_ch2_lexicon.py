with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of Chapter 2:", len(text))
# Let's find sections with single quotes (glosses) like /word/ 'gloss' or word 'gloss'
gloss_matches = re.findall(r'(/[a-zA-Z:̃ŋñʈɖɽɳʃɭʰʱ\s\.\-?]+/\s*[\'"][^\'"]+[\'"]|[a-zA-Z:̃ŋñʈɖɽɳʃɭʰʱ\-?]+[\s\t]+[\'"][^\'"]+[\'"])', text)
print("Potential lexical tokens with glosses:", len(gloss_matches))
for m in gloss_matches[:30]:
    print("  ", m.strip())

