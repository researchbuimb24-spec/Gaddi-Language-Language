with open('C:/Users/Hp/Documents/Gaddi-Python-Language/scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split("==============================")
print("Pages in ch2:", len(pages))

# Inspect printed pages 65 to 76 (indices around 7 to 18)
for i in range(7, 20):
    lines = pages[i].splitlines()
    print(f"\n--- {lines[0] if lines else 'empty'} ---")
    for l in lines[1:25]:
        if any(c in l for c in ['‘', '’', "'", '"']):
            print(" ", l.strip())

