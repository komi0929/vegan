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

# Multilingual link blocks to inject
pc_lang_block = """
<style>
@media(min-width:768px) {
    .custom-sp-lang-block { display: none !important; }
}
@media(max-width:767px) {
    .custom-pc-lang-block { display: none !important; }
}
</style>
<div class="custom-pc-lang-block" style="display:flex; align-items:center; margin-left:16px; margin-right:16px; gap:8px; font-family:sans-serif; font-size:12px;">
    <a href="LANG_LINK_JP" style="JP_STYLE">JP</a><span style="color:#ccc;">|</span>
    <a href="LANG_LINK_EN" style="EN_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">EN</a><span style="color:#ccc;">|</span>
    <a href="LANG_LINK_KO" style="KO_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">KO</a><span style="color:#ccc;">|</span>
    <a href="LANG_LINK_ZH_TW" style="ZH_TW_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">繁</a><span style="color:#ccc;">|</span>
    <a href="LANG_LINK_ZH_CN" style="ZH_CN_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">簡</a>
</div>
"""

sp_lang_block = """
<div class="custom-sp-lang-block" style="margin-top:12px; display:flex; justify-content:center; gap:16px; font-family:sans-serif; font-size:14px; padding-bottom:12px;">
    <a href="LANG_LINK_JP" style="JP_STYLE">JP</a>
    <a href="LANG_LINK_EN" style="EN_STYLE">EN</a>
    <a href="LANG_LINK_KO" style="KO_STYLE">KO</a>
    <a href="LANG_LINK_ZH_TW" style="ZH_TW_STYLE">繁</a>
    <a href="LANG_LINK_ZH_CN" style="ZH_CN_STYLE">簡</a>
</div>
"""

langs = ['.', 'en', 'ko', 'zh-cn', 'zh-tw']
styles = {
    'active': 'color:#7C8A53; font-weight:bold;',
    'inactive': 'color:#999; transition:color 0.3s;'
}
sp_styles = {
    'active': 'color:#7C8A53; font-weight:bold;',
    'inactive': 'color:#999;'
}

for filename, url in urls.items():
    print(f"Fetching {filename}...")
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Extract the header block to process it carefully
    header_pattern = r'<header class="header">.*?</header>'
    header_match = re.search(header_pattern, html, flags=re.DOTALL)
    if not header_match:
        print(f"Skipping {filename}, no header found.")
        continue
    
    header_html = header_match.group(0)
    
    # Inject PC
    nav_pattern = r'<nav class="header__nav">\s*<a href="https://soystories\.com/".*?</a>\s*</nav>'
    def repl_nav(m):
        original = m.group(0)
        return original.replace('<a href="https://soystories.com/"', 'PC_LANG_BLOCK\n<a href="https://soystories.com/"')
    header_html = re.sub(nav_pattern, repl_nav, header_html)
    
    # Inject SP
    nav_sp_pattern = r'<div class="header__nav-sp">\s*<a href="https://soystories\.com/".*?</a>\s*</div>'
    def repl_nav_sp(m):
        original = m.group(0)
        return original.replace('</div>', '\nSP_LANG_BLOCK\n</div>')
    header_html = re.sub(nav_sp_pattern, repl_nav_sp, header_html)
    
    # Replace header in html
    html = html.replace(header_match.group(0), header_html)
    
    # Save it to all language directories
    for lang in langs:
        lang_dir = os.path.join(root_dir, lang)
        if not os.path.exists(lang_dir):
            continue
        filepath = os.path.join(lang_dir, filename)
        
        lang_html = html
        
        # Setup paths and styles based on language
        
        final_pc_block = pc_lang_block
        final_sp_block = sp_lang_block
        
        if lang == '.':
            final_pc_block = final_pc_block.replace('LANG_LINK_JP', 'index.html').replace('LANG_LINK_EN', 'en/index.html').replace('LANG_LINK_KO', 'ko/index.html').replace('LANG_LINK_ZH_TW', 'zh-tw/index.html').replace('LANG_LINK_ZH_CN', 'zh-cn/index.html')
            final_sp_block = final_sp_block.replace('LANG_LINK_JP', 'index.html').replace('LANG_LINK_EN', 'en/index.html').replace('LANG_LINK_KO', 'ko/index.html').replace('LANG_LINK_ZH_TW', 'zh-tw/index.html').replace('LANG_LINK_ZH_CN', 'zh-cn/index.html')
        else:
            final_pc_block = final_pc_block.replace('LANG_LINK_JP', '../index.html').replace('LANG_LINK_EN', '../en/index.html').replace('LANG_LINK_KO', '../ko/index.html').replace('LANG_LINK_ZH_TW', '../zh-tw/index.html').replace('LANG_LINK_ZH_CN', '../zh-cn/index.html')
            final_sp_block = final_sp_block.replace('LANG_LINK_JP', '../index.html').replace('LANG_LINK_EN', '../en/index.html').replace('LANG_LINK_KO', '../ko/index.html').replace('LANG_LINK_ZH_TW', '../zh-tw/index.html').replace('LANG_LINK_ZH_CN', '../zh-cn/index.html')
        if lang != '.':
            # Fix relative paths for subdirectories before injecting blocks
            lang_html = lang_html.replace('href="./css/', 'href="../css/')
            lang_html = lang_html.replace('href="css/', 'href="../css/')
            lang_html = lang_html.replace('src="./img/', 'src="../img/')
            lang_html = lang_html.replace('href="./img/', 'href="../img/')
            lang_html = lang_html.replace('href="./favicon.ico"', 'href="../favicon.ico"')
            # The top logo goes to the language's top page, which is index.html in the same subfolder
            lang_html = lang_html.replace('href="./index.html"', 'href="./index.html"')
            
            # Translate online store button
            if lang == 'en':
                lang_html = lang_html.replace('オンラインストアはこちら', 'Online Store')
            elif lang == 'ko':
                lang_html = lang_html.replace('オンラインストアはこちら', '온라인 스토어')
            elif lang == 'zh-cn':
                lang_html = lang_html.replace('オンラインストアはこちら', '在线商店')
            elif lang == 'zh-tw':
                lang_html = lang_html.replace('オンラインストアはこちら', '線上商店')
            
        for l_key, l_val in [('JP', '.'), ('EN', 'en'), ('KO', 'ko'), ('ZH_TW', 'zh-tw'), ('ZH_CN', 'zh-cn')]:
            if l_val == lang:
                pc_s = styles['active']
                sp_s = sp_styles['active']
            else:
                pc_s = styles['inactive']
                sp_s = sp_styles['inactive']
            
            final_pc_block = final_pc_block.replace(f'{l_key}_STYLE', pc_s)
            final_sp_block = final_sp_block.replace(f'{l_key}_STYLE', sp_s)

        lang_html = lang_html.replace('PC_LANG_BLOCK', final_pc_block)
        lang_html = lang_html.replace('SP_LANG_BLOCK', final_sp_block)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(lang_html)
            
print("Done restoring HTML files perfectly!")
