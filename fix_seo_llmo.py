import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

def fix_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    html = f.read()
                
                original_html = html
                
                # 1. Fix noindex, nofollow
                html = html.replace('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="index, follow">')
                
                # 2. Check if <meta name="revised" is present, if not add it below the description
                if '<meta name="revised"' not in html:
                    # Find description meta tag
                    desc_match = re.search(r'(<meta\s+name="description".*?>)', html, re.IGNORECASE)
                    if desc_match:
                        revised_tag = '\n    <meta name="revised" content="2026-05-17T14:15:00+09:00">'
                        html = html.replace(desc_match.group(1), desc_match.group(1) + revised_tag)

                if html != original_html:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html)
                    print(f"Optimized LLMO/SEO for: {filepath}")

fix_html_files(root_dir)
