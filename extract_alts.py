import os
import re

alts = set()
for lang in ['en', 'ko', 'zh-tw', 'zh-cn']:
    for root, dirs, files in os.walk(lang):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    alts.update(re.findall(r'alt=\'(.*?)\'', content))
                    alts.update(re.findall(r'alt="(.*?)"', content))

with open('extracted_alts.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(alts))
