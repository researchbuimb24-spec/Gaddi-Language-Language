with open('scratch/chapter2_bharmauri_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

snippets = [
    'connective',
    'India and Pakistan',
    'How can you ever fight him',
    'said the crow',
    'me apne larijo',
    'These two or three boys go into'
]

for s in snippets:
    pos = text.find(s)
    print(f"=== SNIPPET: {s} ===")
    if pos != -1:
        print(text[max(0, pos-150):min(len(text), pos+200)])
    else:
        print("Not found")

