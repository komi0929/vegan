import os, re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['en', 'ko', 'zh-cn', 'zh-tw']
pattern = re.compile(r'alt="([^"]+)"')
jp_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

alts = set()
for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir): continue
    for file in os.listdir(lang_dir):
        if not file.endswith('.html'): continue
        filepath = os.path.join(lang_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = pattern.findall(content)
        for m in matches:
            if jp_pattern.search(m):
                alts.add(m)

with open("alts.txt", "w", encoding="utf-8") as f:
    for a in sorted(alts):
        f.write(a + "\n")
