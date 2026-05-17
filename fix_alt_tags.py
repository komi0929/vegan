import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

def get_alt(src, lang):
    filename = os.path.basename(src).lower()
    
    if 'menu_photo1' in filename:
        return {'en': 'Signature Waffle & Soft Serve', 'ko': '시그니처 와플 & 소프트 아이스크림', 'zh-tw': '招牌華夫餅與霜淇淋', 'zh-cn': '招牌华夫饼与软冰淇淋'}[lang]
    if 'menu_photo2' in filename:
        return {'en': 'Gluten-Free Bubble Waffle', 'ko': '글루텐 프리 버블 와플', 'zh-tw': '無麩質泡泡華夫餅', 'zh-cn': '无麸质泡泡华夫饼'}[lang]
    if 'menu_photo3' in filename:
        return {'en': 'Artisan Soy Soft Serve', 'ko': '수제 두유 소프트 아이스크림', 'zh-tw': '手工豆奶霜淇淋', 'zh-cn': '手工豆奶软冰淇淋'}[lang]
    if 'menu_photo4' in filename:
        return {'en': 'Guilt-Free Soy Donuts', 'ko': '길트프리 두유 도넛', 'zh-tw': '無負擔豆奶甜甜圈', 'zh-cn': '无负担豆奶甜甜圈'}[lang]
    if 'menu_photo5' in filename:
        return {'en': 'Rice Flour Gelato', 'ko': '쌀가루 젤라또', 'zh-tw': '米粉義式冰淇淋', 'zh-cn': '米粉意式冰淇淋'}[lang]
    
    if 'waffle&soft' in filename or 'wafflesoft' in filename or 'wafflewhip' in filename:
        return {'en': 'Waffle & Soft Serve', 'ko': '와플 & 소프트 아이스크림', 'zh-tw': '華夫餅與霜淇淋', 'zh-cn': '华夫饼与软冰淇淋'}[lang]
    if 'waffle' in filename:
        return {'en': 'Bubble Waffle', 'ko': '버블 와플', 'zh-tw': '泡泡華夫餅', 'zh-cn': '泡泡华夫饼'}[lang]
    if 'soft' in filename:
        return {'en': 'Soy Soft Serve', 'ko': '두유 소프트 아이스크림', 'zh-tw': '豆奶霜淇淋', 'zh-cn': '豆奶软冰淇淋'}[lang]
    if 'donut' in filename:
        return {'en': 'Soy Donut', 'ko': '두유 도넛', 'zh-tw': '豆奶甜甜圈', 'zh-cn': '豆奶甜甜圈'}[lang]
    if 'ice' in filename:
        return {'en': 'Rice Flour Gelato', 'ko': '쌀가루 젤라또', 'zh-tw': '米粉義式冰淇淋', 'zh-cn': '米粉意式冰淇淋'}[lang]
    if 'butter_sand' in filename:
        return {'en': 'Vegan Butter Sandwich', 'ko': '비건 버터 샌드위치', 'zh-tw': '純素奶油夾心餅乾', 'zh-cn': '纯素奶油夹心饼干'}[lang]
    if 'tiramisu' in filename:
        return {'en': 'Vegan Tiramisu', 'ko': '비건 티라미수', 'zh-tw': '純素提拉米蘇', 'zh-cn': '纯素提拉米苏'}[lang]
    if 'store' in filename:
        return {'en': 'SoyStories Storefront', 'ko': 'SoyStories 매장 외관', 'zh-tw': 'SoyStories 店面', 'zh-cn': 'SoyStories 店面'}[lang]
    if 'concept_reef' in filename:
        return {'en': 'Leaf Shadow', 'ko': '나뭇잎 그림자', 'zh-tw': '樹葉剪影', 'zh-cn': '树叶剪影'}[lang]
    if 'qa' in filename:
        return {'en': 'Microwave 600W 1 minute', 'ko': '전자레인지 600W 1분', 'zh-tw': '微波爐 600W 1分鐘', 'zh-cn': '微波炉 600W 1分钟'}[lang]
    if 'soy-are' in filename or 'soypowder' in filename:
        return {'en': 'Contains Soy', 'ko': '대두 함유', 'zh-tw': '含大豆', 'zh-cn': '含大豆'}[lang]
    if 'almond' in filename:
        return {'en': 'Contains Almond', 'ko': '아몬드 함유', 'zh-tw': '含杏仁', 'zh-cn': '含杏仁'}[lang]
    if 'black_sesame' in filename:
        return {'en': 'Contains Black Sesame', 'ko': '검은깨 함유', 'zh-tw': '含黑芝麻', 'zh-cn': '含黑芝麻'}[lang]
    if 'potato' in filename:
        return {'en': 'Contains Yam', 'ko': '참마 함유', 'zh-tw': '含山藥', 'zh-cn': '含山药'}[lang]
    if 'apple' in filename:
        return {'en': 'Contains Apple', 'ko': '사과 함유', 'zh-tw': '含蘋果', 'zh-cn': '含苹果'}[lang]
    if 'allergens' in filename:
        return {'en': 'Free from Milk, Eggs, Wheat', 'ko': '우유, 계란, 밀 프리', 'zh-tw': '不含牛奶、雞蛋、小麥', 'zh-cn': '不含牛奶、鸡蛋、小麦'}[lang]
    if 'eat-in' in filename:
        return {'en': 'Store Interior', 'ko': '매장 내부', 'zh-tw': '店內環境', 'zh-cn': '店内环境'}[lang]
    if 'commitment' in filename or 'okara' in filename or 'greentea' in filename or 'houjicha' in filename:
        return {'en': 'Our Ingredients', 'ko': '우리의 재료', 'zh-tw': '我們的嚴選食材', 'zh-cn': '我们的严选食材'}[lang]
    if 'logo' in filename:
        return 'SoyStories'
    if 'icon' in filename:
        return 'Icon'
    if 'concept_waffle' in filename:
        return {'en': 'Waffle in hand', 'ko': '손에 든 와플', 'zh-tw': '手中的華夫餅', 'zh-cn': '手中的华夫饼'}[lang]
    if 'top_wafflesoft' in filename:
        return {'en': 'SoyStories Waffle & Soft Serve', 'ko': 'SoyStories 와플 & 소프트 아이스크림', 'zh-tw': 'SoyStories 華夫餅與霜淇淋', 'zh-cn': 'SoyStories 华夫饼与软冰淇淋'}[lang]
    if 'kuromitsu' in filename:
        return {'en': 'Brown Sugar Syrup', 'ko': '흑밀 시럽', 'zh-tw': '黑糖蜜', 'zh-cn': '黑糖蜜'}[lang]
    if 'chocosource' in filename:
        return {'en': 'Chocolate Source', 'ko': '초콜릿 소스', 'zh-tw': '巧克力醬', 'zh-cn': '巧克力酱'}[lang]
    
    return 'SoyStories Image'

def replace_alts_in_html(html, lang):
    # Regex to find img tags and replace alt based on src
    def replacer(match):
        img_tag = match.group(0)
        
        # Extract src
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        if not src_match:
            return img_tag
        src = src_match.group(1)
        
        # Get correct translation
        new_alt = get_alt(src, lang)
        
        # Replace existing alt or add one
        if re.search(r'alt=["\'][^"\']*["\']', img_tag):
            new_img_tag = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{new_alt}"', img_tag)
        else:
            new_img_tag = img_tag.replace('>', f' alt="{new_alt}">')
            
        return new_img_tag

    # Replace all img tags
    html = re.sub(r'<img[^>]+>', replacer, html)
    return html

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
            
        # 1. Fix angko typo in EN donuts
        if lang == 'en' and filename == 'dounuts.html':
            html = html.replace('angko', 'anko')
            
        # 2. Fix Alts
        html = replace_alts_in_html(html, lang)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

print("Alt attributes replaced successfully.")
