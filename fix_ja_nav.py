import re

filepath = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

ja_trans = {
    'Concept': 'コンセプト',
    'Menu': 'メニュー',
    'Access': 'アクセス'
}

for en_word, jp_word in ja_trans.items():
    content = re.sub(rf'(<a[^>]*class="(?:header|drawer-content)__link"[^>]*>)\s*{en_word}\s*(</a>)', rf'\g<1>{jp_word}\g<2>', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Japanese Navigation")
