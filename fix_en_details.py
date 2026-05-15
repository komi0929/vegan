import os
import re

en_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\en"
index_path = os.path.join(en_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract header
header_match = re.search(r'<header class="header">.*?</header>', index_content, re.DOTALL)
if header_match:
    new_header = header_match.group(0)
else:
    print("Header not found in index.html")
    exit(1)

# Extract footer
footer_match = re.search(r'<footer class="footer">.*?</div>', index_content, re.DOTALL) # matches footer and copylight
if footer_match:
    new_footer = footer_match.group(0)
else:
    print("Footer not found in index.html")
    exit(1)

files_to_fix = ['dounuts.html', 'soft.html', 'waffle.html', 'ice.html', 'waffle&soft.html']

for filename in files_to_fix:
    filepath = os.path.join(en_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace header
    content = re.sub(r'<header class="header">.*?</header>', new_header, content, flags=re.DOTALL)
    
    # Replace footer & copylight
    content = re.sub(r'<footer class="footer">.*</div>', new_footer, content, flags=re.DOTALL)
    
    # Remove menu-nav
    content = re.sub(r'<nav class="menu-nav">.*?</nav>', '', content, flags=re.DOTALL)
    
    # Update CSS links
    # remove old ress and style*.css
    content = re.sub(r'<link rel="stylesheet" href="https://unpkg.com/ress.*?">', '', content, flags=re.DOTALL)
    content = re.sub(r'<link rel="stylesheet" href="\.\./css/reset.css">', '<link rel="stylesheet" href="../css/reset.css">', content, flags=re.DOTALL)
    content = re.sub(r'<link rel="stylesheet" href="css/style\d*\.css">', '<link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">', content, flags=re.DOTALL)
    content = re.sub(r'<link rel="stylesheet" href="\.\./css/style\d*\.css">', '<link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">', content, flags=re.DOTALL)

    # Make sure we don't have duplicate style.css
    if content.count('href="../css/style.css"') == 0:
        content = content.replace('</head>', '    <link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/detail.css">\n</head>')
    
    # Localization fixes
    content = content.replace('円（税込）', ' JPY (Tax incl.)')
    content = content.replace('円', ' JPY')
    content = content.replace('価格', 'Price: ')
    content = content.replace('プレーン', 'Plain ')
    content = content.replace('その他', 'Others ')
    content = content.replace('含まれているアレルギー食品', 'Allergen Information')
    content = content.replace('大豆を使用しています', 'Contains Soy')
    content = content.replace('大豆', 'Soy')
    content = content.replace('アーモンド', 'Almond')
    content = content.replace('黒ごま', 'Black Sesame')
    content = content.replace('やまいも', 'Yam')
    content = content.replace('プレーンドーナツ', 'Plain Donuts')
    content = content.replace('グレーズドーナツ', 'Glazed Donuts')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed {filename}")
