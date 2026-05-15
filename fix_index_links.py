import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['en', 'ko', 'zh-cn', 'zh-tw']

for lang in langs:
    filepath = os.path.join(root_dir, lang, 'index.html')
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # The PC switcher
    pc_nav_pattern = r'<div style="display:flex; align-items:center; margin-left:16px; margin-right:16px; gap:8px; font-family:sans-serif; font-size:12px;">.*?</div>'
    
    # The SP switcher
    sp_nav_pattern = r'<div style="margin-top:24px; display:flex; justify-content:center; gap:16px; font-family:sans-serif; font-size:14px; padding-bottom:24px;">.*?</div>'

    # New PC block
    pc_lang_block = """<div style="display:flex; align-items:center; margin-left:16px; margin-right:16px; gap:8px; font-family:sans-serif; font-size:12px;">
                    <a href="../index.html" style="JP_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">JP</a><span style="color:#ccc;">|</span>
                    <a href="../en/index.html" style="EN_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">EN</a><span style="color:#ccc;">|</span>
                    <a href="../ko/index.html" style="KO_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">KO</a><span style="color:#ccc;">|</span>
                    <a href="../zh-tw/index.html" style="ZH_TW_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">繁</a><span style="color:#ccc;">|</span>
                    <a href="../zh-cn/index.html" style="ZH_CN_STYLE" onmouseover="this.style.color='#7C8A53'" onmouseout="this.style.color='#999'">簡</a>
                </div>"""

    # New SP block
    sp_lang_block = """<div style="margin-top:24px; display:flex; justify-content:center; gap:16px; font-family:sans-serif; font-size:14px; padding-bottom:24px;">
                    <a href="../index.html" style="JP_STYLE">JP</a>
                    <a href="../en/index.html" style="EN_STYLE">EN</a>
                    <a href="../ko/index.html" style="KO_STYLE">KO</a>
                    <a href="../zh-tw/index.html" style="ZH_TW_STYLE">繁</a>
                    <a href="../zh-cn/index.html" style="ZH_CN_STYLE">簡</a>
                </div>"""

    styles = {
        'active': 'color:#7C8A53; font-weight:bold;',
        'inactive': 'color:#999; transition:color 0.3s;'
    }
    sp_styles = {
        'active': 'color:#7C8A53; font-weight:bold;',
        'inactive': 'color:#999;'
    }

    # Apply styles
    for l_key, l_val in [('JP', '.'), ('EN', 'en'), ('KO', 'ko'), ('ZH_TW', 'zh-tw'), ('ZH_CN', 'zh-cn')]:
        if l_val == lang:
            pc_s = styles['active']
            sp_s = sp_styles['active']
            # Remove hover effects from active link
            pc_lang_block = pc_lang_block.replace(f'style="{l_key}_STYLE" onmouseover="this.style.color=\'#7C8A53\'" onmouseout="this.style.color=\'#999\'"', f'style="{l_key}_STYLE"')
        else:
            pc_s = styles['inactive']
            sp_s = sp_styles['inactive']
        
        pc_lang_block = pc_lang_block.replace(f'{l_key}_STYLE', pc_s)
        sp_lang_block = sp_lang_block.replace(f'{l_key}_STYLE', sp_s)
        
    html = re.sub(pc_nav_pattern, pc_lang_block, html, flags=re.DOTALL)
    html = re.sub(sp_nav_pattern, sp_lang_block, html, flags=re.DOTALL)

    # Also make sure the logo link goes to the correct top page for that language
    # Currently it says <a href="../index.html"> which means if they click the logo from en/index.html, they go to JP index.
    # It should be <a href="./index.html">
    html = re.sub(r'<h1 class="header__logo">\s*<a href="\.\./index\.html">', r'<h1 class="header__logo">\n                <a href="./index.html">', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Done fixing index.html language switchers!")
