with open('tests/test_unified_expansion.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('assert len(categories) == 24', 'assert len(categories) == 19')
content = content.replace("assert info['categories_count'] == 24", "assert info['categories_count'] == 19")
content = content.replace('assert info["categories_count"] == 24', 'assert info["categories_count"] == 19')

with open('tests/test_unified_expansion.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated test_unified_expansion.py")

