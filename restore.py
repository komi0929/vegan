import urllib.request
import os
import re

urls = {
    'waffle.html': 'https://soystories.jp/waffle.html',
    'waffle&soft.html': 'https://soystories.jp/waffle&soft.html',
    'soft.html': 'https://soystories.jp/soft.html',
    'dounuts.html': 'https://soystories.jp/dounuts.html',
    'ice.html': 'https://soystories.jp/ice.html'
}

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# Read the multilingual header from index.html
with open(os.path.join(root_dir, 'index.html'), 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract header from index.html
header_match = re.search(r'<header class="header">.*?</header>', index_html, re.DOTALL)
index_header = header_match.group(0)

# Process each file
langs = ['.', 'en', 'ko', 'zh-cn', 'zh-tw']

for filename, url in urls.items():
    print(f"Fetching {filename}...")
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # The fetched HTML has its own <header class="header">
    # It contains <div class="header__inner inner"> and <nav class="menu-nav">
    # We want to replace its <div class="header__inner inner">...</div> with index.html's
    # AND add the drawer content.
    
    # Extract menu-nav from the fetched HTML
    menu_nav_match = re.search(r'<nav class="menu-nav">.*?</nav>', html, re.DOTALL)
    menu_nav = menu_nav_match.group(0) if menu_nav_match else ""
    
    # Construct the new header: index_header + menu_nav (inserted before </header>)
    new_header = index_header.replace('</header>', f'    {menu_nav}\n</header>')
    
    # Replace the fetched header with the new header
    html = re.sub(r'<header class="header">.*?</header>', new_header, html, flags=re.DOTALL)
    
    # Replace the footer with index footer to have consistent links
    footer_match = re.search(r'<footer class="footer">.*?</footer>', index_html, re.DOTALL)
    index_footer = footer_match.group(0)
    
    # The fetched HTML has <footer class="footer">...</footer>
    # And maybe <p id="line">...</p> after it.
    html = re.sub(r'<footer class="footer">.*?</footer>', index_footer, html, flags=re.DOTALL)
    
    # Save it to all language directories
    for lang in langs:
        lang_dir = os.path.join(root_dir, lang)
        if not os.path.exists(lang_dir):
            continue
        filepath = os.path.join(lang_dir, filename)
        
        # If it's a subfolder, we need to adjust the relative paths for href and src
        # from "./img" to "../img" and so on.
        lang_html = html
        if lang != '.':
            # Adjust paths for subdirectories
            lang_html = lang_html.replace('href="./', 'href="../')
            lang_html = lang_html.replace('src="./', 'src="../')
            lang_html = lang_html.replace('href="css/', 'href="../css/')
            lang_html = lang_html.replace('href="index.html"', 'href="../index.html"')
            
            # The multi-links in index_header need adjustment too, but they are hardcoded as "en/index.html".
            # In a subdirectory like "en", the link to JP should be "../index.html", 
            # EN should be "./index.html", etc.
            # For simplicity, we just use absolute-like relative paths from the subfolder.
            lang_html = lang_html.replace('href="index.html"', 'href="../index.html"')
            lang_html = lang_html.replace('href="en/index.html"', 'href="../en/index.html"')
            lang_html = lang_html.replace('href="ko/index.html"', 'href="../ko/index.html"')
            lang_html = lang_html.replace('href="zh-tw/index.html"', 'href="../zh-tw/index.html"')
            lang_html = lang_html.replace('href="zh-cn/index.html"', 'href="../zh-cn/index.html"')
            
            # We don't translate the text for now, but we fix the mojibake and layout.
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(lang_html)
            
print("Done restoring HTML files!")
