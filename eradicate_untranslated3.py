import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

translations = {
    # --- ice.html ---
    r'Melting(?:&ensp;|\s)*chocolate': {
        'en': 'Melting chocolate', 'ko': '사르르 녹는 초콜릿', 'zh-tw': '入口即化的巧克力', 'zh-cn': '入口即化的巧克力'
    },
    r'Refreshing(?:&ensp;|\s)*apple': {
        'en': 'Refreshing apple', 'ko': '상큼한 사과', 'zh-tw': '清爽蘋果', 'zh-cn': '清爽苹果'
    },
    r'Supreme(?:&ensp;|\s)*rich(?:&ensp;|\s)*matcha': {
        'en': 'Supreme rich matcha', 'ko': '궁극의 진한 말차', 'zh-tw': '極致濃郁抹茶', 'zh-cn': '极致浓郁抹茶'
    },
    r'Fragrant(?:&ensp;|\s)*hojicha': {
        'en': 'Fragrant hojicha', 'ko': '향긋한 호지차', 'zh-tw': '香醇焙茶', 'zh-cn': '香醇焙茶'
    },
    r'Juicy(?:&ensp;|\s)*dragon(?:&ensp;|\s)*fruit': {
        'en': 'Juicy dragon fruit', 'ko': '과즙 가득 용과', 'zh-tw': '多汁火龍果', 'zh-cn': '多汁火龙果'
    },

    # --- dounuts.html ---
    r'Lemon(?:&ensp;|\s)*Earl(?:&ensp;|\s)*Grey': {
        'en': 'Lemon Earl Grey', 'ko': '레몬 얼그레이', 'zh-tw': '檸檬伯爵茶', 'zh-cn': '柠檬伯爵茶'
    },
    r'Soybean(?:&ensp;|\s)*flour(?:&ensp;|\s)*glaze': {
        'en': 'Soybean flour glaze', 'ko': '콩가루 글레이즈', 'zh-tw': '黃豆粉糖霜', 'zh-cn': '黄豆粉糖霜'
    },
    r'Black(?:&ensp;|\s)*sesame(?:&ensp;|\s)*glaze': {
        'en': 'Black sesame glaze', 'ko': '검은깨 글레이즈', 'zh-tw': '黑芝麻糖霜', 'zh-cn': '黑芝麻糖霜'
    },
    r'Couvert(?:&ensp;|\s)*chocolate(?:&ensp;|\s)*nuts': {
        'en': 'Couvert chocolate nuts', 'ko': '쿠버춰 초콜릿 넛츠', 'zh-tw': '調溫巧克力堅果', 'zh-cn': '调温巧克力坚果'
    }
}

def translate_all_subpages():
    for lang in ['ko', 'zh-tw', 'zh-cn']: # En isn't needed here as it's already english
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
