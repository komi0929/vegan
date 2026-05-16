import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
files = ['waffle.html', 'waffle&soft.html', 'soft.html', 'dounuts.html', 'ice.html']
langs = ['en', 'ko', 'zh-cn', 'zh-tw']

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

styles = {
    'active': 'color:#7C8A53; font-weight:bold;',
    'inactive': 'color:#999; transition:color 0.3s;'
}
sp_styles = {
    'active': 'color:#7C8A53; font-weight:bold;',
    'inactive': 'color:#999;'
}

for lang in langs:
    for filename in files:
        filepath = os.path.join(root_dir, lang, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Check if already injected
        if "custom-pc-lang-block" in html:
            continue
            
        # The 11109df header:
        # <div class="header__nav-sp">
        #     <a href="https://soystories.com/" class="header__button-sp" target="_blank">Online Store</a>
        # </div>
        # <nav class="header__nav">
        #     <a href="https://soystories.com/" class="header__button" target="_blank">Online Store</a>
        # </nav>
        
        # Inject SP block into header__nav-sp
        nav_sp_pattern = r'<div class="header__nav-sp">\s*<a href="https://soystories\.com/".*?</a>\s*</div>'
        def repl_nav_sp(m):
            original = m.group(0)
            return original.replace('</div>', '\nSP_LANG_BLOCK\n</div>')
        html = re.sub(nav_sp_pattern, repl_nav_sp, html)
        
        # Inject PC block into header__nav
        nav_pattern = r'<nav class="header__nav">\s*<a href="https://soystories\.com/".*?</a>\s*</nav>'
        def repl_nav(m):
            original = m.group(0)
            return original.replace('<a href="https://soystories.com/"', 'PC_LANG_BLOCK\n<a href="https://soystories.com/"')
        html = re.sub(nav_pattern, repl_nav, html)
        
        # Replace language links
        final_pc_block = pc_lang_block
        final_sp_block = sp_lang_block
        
        final_pc_block = final_pc_block.replace('LANG_LINK_JP', '../index.html').replace('LANG_LINK_EN', '../en/index.html').replace('LANG_LINK_KO', '../ko/index.html').replace('LANG_LINK_ZH_TW', '../zh-tw/index.html').replace('LANG_LINK_ZH_CN', '../zh-cn/index.html')
        final_sp_block = final_sp_block.replace('LANG_LINK_JP', '../index.html').replace('LANG_LINK_EN', '../en/index.html').replace('LANG_LINK_KO', '../ko/index.html').replace('LANG_LINK_ZH_TW', '../zh-tw/index.html').replace('LANG_LINK_ZH_CN', '../zh-cn/index.html')
            
        for l_key, l_val in [('JP', '.'), ('EN', 'en'), ('KO', 'ko'), ('ZH_TW', 'zh-tw'), ('ZH_CN', 'zh-cn')]:
            if l_val == lang:
                pc_s = styles['active']
                sp_s = sp_styles['active']
            else:
                pc_s = styles['inactive']
                sp_s = sp_styles['inactive']
            
            final_pc_block = final_pc_block.replace(f'{l_key}_STYLE', pc_s)
            final_sp_block = final_sp_block.replace(f'{l_key}_STYLE', sp_s)

        html = html.replace('PC_LANG_BLOCK', final_pc_block)
        html = html.replace('SP_LANG_BLOCK', final_sp_block)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
print("Done injecting language blocks and fixing CSS links in localized detail pages!")
