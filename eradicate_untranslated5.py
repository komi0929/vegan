import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

translations = {
    r'純豆乳ソフト.*Large': {
        'en': 'Soy Soft Serve Large', 'ko': '소이 소프트 라지', 'zh-tw': '純豆乳霜淇淋 大杯', 'zh-cn': '纯豆乳冰淇淋 大杯'
    },
    r'純豆乳ソフト.*Medium': {
        'en': 'Soy Soft Serve Medium', 'ko': '소이 소프트 미디엄', 'zh-tw': '純豆乳霜淇淋 中杯', 'zh-cn': '纯豆乳冰淇淋 中杯'
    },
    r'トッピング.*topping': {
        'en': 'Toppings', 'ko': '토핑', 'zh-tw': '配料', 'zh-cn': '配料'
    },
}

def translate_all_subpages():
    for lang in ['en', 'ko', 'zh-tw', 'zh-cn']:
        lang_dir = os.path.join(root_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        for filename in os.listdir(lang_dir):
            if not filename.endswith('.html'):
                continue
                
            filepath = os.path.join(lang_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            modified = False
            for pattern, lang_dict in translations.items():
                replacement = lang_dict.get(lang)
                if not replacement:
                    continue
                
                new_html = re.sub(pattern, replacement, html)
                if new_html != html:
                    html = new_html
                    modified = True
                    
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"Fixed translations in {lang}/{filename}")

translate_all_subpages()
