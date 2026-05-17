import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

translations = {
    # Fix the ones missed due to unicode em-space (\u2003)
    r'純豆乳ソフト(?:\u2003|\s)*Large': {
        'en': 'Soy Soft Serve Large', 'ko': '소이 소프트 라지', 'zh-tw': '純豆乳霜淇淋 大杯', 'zh-cn': '纯豆乳冰淇淋 大杯'
    },
    r'純豆乳ソフト(?:\u2003|\s)*Medium': {
        'en': 'Soy Soft Serve Medium', 'ko': '소이 소프트 미디엄', 'zh-tw': '純豆乳霜淇淋 中杯', 'zh-cn': '纯豆乳冰淇淋 中杯'
    },
    r'トッピング(?:\u2003|\s)*topping': {
        'en': 'Toppings', 'ko': '토핑', 'zh-tw': '配料', 'zh-cn': '配料'
    },
    
    # Navigation titles that were missed (only target kind-jp or main titles, not kind-en)
    r'<div class="kind-jp">Rice Flour Gelato</div>': {
        'en': '<div class="kind-jp">Rice Flour Gelato</div>', 'ko': '<div class="kind-jp">쌀가루 젤라또</div>', 'zh-tw': '<div class="kind-jp">米粉義式冰淇淋</div>', 'zh-cn': '<div class="kind-jp">米粉意式冰淇淋</div>'
    },
    r'<span id="title-sub">Rice Flour Gelato</span>': {
        'en': '<span id="title-sub">Rice Flour Gelato</span>', 'ko': '<span id="title-sub">쌀가루 젤라또</span>', 'zh-tw': '<span id="title-sub">米粉義式冰淇淋</span>', 'zh-cn': '<span id="title-sub">米粉意式冰淇淋</span>'
    },

    # Fix typo Chocolate source -> Chocolate sauce
    r'Chocolate\s*source': {
        'en': 'Chocolate sauce', 'ko': 'Chocolate sauce', 'zh-tw': 'Chocolate sauce', 'zh-cn': 'Chocolate sauce'
    },

    # Fix ko index.html leftover
    r'You can order our products<br>\s*from the SoyStories 온라인 스토어.': {
        'ko': 'SoyStories 온라인 스토어에서<br>주문하실 수 있습니다.'
    },

    # Fix via Google reviews
    r'via Google Reviews': {
        'ko': '출처: Google Reviews', 'zh-tw': '來自 Google Reviews', 'zh-cn': '来自 Google Reviews'
    }
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
