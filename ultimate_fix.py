import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['.', 'en', 'ko', 'zh-cn', 'zh-tw']
files_to_fix = ['dounuts.html', 'soft.html', 'waffle.html', 'ice.html', 'waffle&soft.html']

for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    index_path = os.path.join(lang_dir, "index.html")
    
    if not os.path.exists(index_path):
        continue
        
    with open(index_path, "r", encoding="utf-8", errors='ignore') as f:
        index_content = f.read()

    # Extract clean blocks from index.html
    head_match = re.search(r'<head.*?</head>', index_content, re.DOTALL | re.IGNORECASE)
    header_match = re.search(r'<header class="header">.*?</header>', index_content, re.DOTALL | re.IGNORECASE)
    footer_match = re.search(r'<footer class="footer">.*?</html>', index_content, re.DOTALL | re.IGNORECASE)
    
    if not head_match or not header_match or not footer_match:
        print(f"Failed to find blocks in {index_path}")
        continue
        
    new_head = head_match.group(0)
    # inject detail.css into new_head
    if 'detail.css' not in new_head:
        css_path = "./css/detail.css" if lang == '.' else "../css/detail.css"
        new_head = new_head.replace('</head>', f'    <link rel="stylesheet" href="{css_path}">\n</head>')
        
    new_header = header_match.group(0)
    new_footer = footer_match.group(0)

    for filename in files_to_fix:
        filepath = os.path.join(lang_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
            content = f.read()
            
        # 1. Replace entire <head>
        content = re.sub(r'<head.*?</head>', new_head, content, flags=re.DOTALL | re.IGNORECASE)
        # fallback if <head> is corrupted (like missing < or >)
        if '<head' not in content:
            # this shouldn't happen, but just in case
            pass
            
        # 2. Replace entire <header>
        content = re.sub(r'<header.*?</header>', new_header, content, flags=re.DOTALL | re.IGNORECASE)
        
        # 3. Replace entire footer to EOF
        content = re.sub(r'<footer.*', new_footer, content, flags=re.DOTALL | re.IGNORECASE)
        
        # 4. Remove old menu-nav
        content = re.sub(r'<nav class="menu-nav">.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 5. Fix broken alt attributes that swallowed the closing quote and bracket.
        # Find alt="[no quotes here]> and replace with alt="">
        # Be careful not to replace valid alt="...". Valid ones end with ".
        # So if alt starts with " but the next quote is AFTER a >, it means the tag's closing > was swallowed by the text before the next quote, OR the quote was swallowed before the >.
        # Actually, the simplest fix is to just forcefully close any img tag that has alt="[text without quotes]>
        content = re.sub(r'alt="([^">]*?)>', r'alt="">', content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Perfected {lang}/{filename}")
