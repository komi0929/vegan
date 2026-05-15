import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['ko', 'zh-cn', 'zh-tw']
files_to_fix = ['dounuts.html', 'soft.html', 'waffle.html', 'ice.html', 'waffle&soft.html']

for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    index_path = os.path.join(lang_dir, "index.html")
    
    if not os.path.exists(index_path):
        continue
        
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    header_match = re.search(r'<header class="header">.*?</header>', index_content, re.DOTALL)
    footer_match = re.search(r'<footer class="footer">.*?</div>', index_content, re.DOTALL)
    
    if not header_match or not footer_match:
        continue
        
    new_header = header_match.group(0)
    new_footer = footer_match.group(0)

    for filename in files_to_fix:
        filepath = os.path.join(lang_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace header, footer, remove menu-nav
        content = re.sub(r'<header class="header">.*?</header>', new_header, content, flags=re.DOTALL)
        content = re.sub(r'<footer class="footer">.*</div>', new_footer, content, flags=re.DOTALL)
        content = re.sub(r'<nav class="menu-nav">.*?</nav>', '', content, flags=re.DOTALL)
        
        # Update CSS links
        content = re.sub(r'<link rel="stylesheet" href="https://unpkg.com/ress.*?">', '', content, flags=re.DOTALL)
        content = re.sub(r'<link rel="stylesheet" href="\.\./css/reset.css">', '<link rel="stylesheet" href="../css/reset.css">', content, flags=re.DOTALL)
        content = re.sub(r'<link rel="stylesheet" href="css/style\d*\.css">', '<link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">', content, flags=re.DOTALL)
        content = re.sub(r'<link rel="stylesheet" href="\.\./css/style\d*\.css">', '<link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">', content, flags=re.DOTALL)
        
        if content.count('href="../css/style.css"') == 0:
            content = content.replace('</head>', '    <link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">\n</head>')
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Fixed {lang}/{filename}")
