import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# --- Master Replace Dictionary ---
# Regex pattern -> { 'en': replacement, 'ko': replacement, 'zh-tw': replacement, 'zh-cn': replacement }

translations = {
    # --- soft.html & waffle&soft.html ---
    r'純豆乳ソフト\s*Large': {
        'en': 'Soy Soft Serve Large', 'ko': '소이 소프트 라지', 'zh-tw': '純豆乳霜淇淋 大杯', 'zh-cn': '纯豆乳冰淇淋 大杯'
    },
    r'濃厚豆乳を使ったソフトクリームです。': {
        'en': 'A soft serve ice cream made with rich soy milk.', 'ko': '진한 두유로 만든 소프트 아이스크림입니다.', 'zh-tw': '使用濃郁豆乳製成的霜淇淋。', 'zh-cn': '使用浓郁豆乳制成的冰淇淋。'
    },
    r'アレルギーをお持ちの方でも': {
        'en': 'Even those with allergies', 'ko': '알레르기가 있으신 분들도', 'zh-tw': '即使是過敏體質的顧客', 'zh-cn': '即使是过敏体质的顾客'
    },
    r'美味しく召し上がれます。': {
        'en': 'can enjoy it safely.', 'ko': '안심하고 맛있게 드실 수 있습니다.', 'zh-tw': '也能安心享用美味。', 'zh-cn': '也能安心享用美味。'
    },
    r'純豆乳ソフト\s*Medium': {
        'en': 'Soy Soft Serve Medium', 'ko': '소이 소프트 미디엄', 'zh-tw': '純豆乳霜淇淋 中杯', 'zh-cn': '纯豆乳冰淇淋 中杯'
    },
    r'濃厚豆乳を使ったソフトクリームを': {
        'en': 'Our rich soy milk soft serve', 'ko': '진한 두유로 만든 소프트 아이스크림을', 'zh-tw': '將濃郁的豆乳霜淇淋', 'zh-cn': '将浓郁的豆乳冰淇淋'
    },
    r'食べやすい(Half|하프|半尺寸)サイズにしました。': {
        'en': 'in an easy-to-eat half size.', 'ko': '먹기 편한 하프 사이즈로 제공합니다.', 'zh-tw': '做成方便享用的半杯尺寸。', 'zh-cn': '做成方便享用的半杯尺寸。'
    },
    r'ワッ(Full|풀|全尺寸)豆乳ホイップクリーム': {
        'en': 'Bubble Waffle & Soy Whip', 'ko': '버블 와플 & 소이 휩', 'zh-tw': '泡泡鬆餅 & 豆乳鮮奶油', 'zh-cn': '泡泡华夫饼 & 豆乳鲜奶油'
    },
    r'濃厚豆乳を使ったホイップに、': {
        'en': 'A combination of our rich soy milk whip', 'ko': '진한 두유로 만든 휩 크림과', 'zh-tw': '濃郁豆乳製成的鮮奶油，', 'zh-cn': '浓郁豆乳制成的鲜奶油，'
    },
    r'当店自慢のワッ(Full|풀|全尺寸)を組み合わせた商品です。': {
        'en': 'and our signature bubble waffle.', 'ko': '자랑거리인 버블 와플을 조합한 상품입니다.', 'zh-tw': '搭配招牌泡泡鬆餅的完美組合。', 'zh-cn': '搭配招牌泡泡华夫饼的完美组合。'
    },
    
    # --- Toppings ---
    r'^きな粉$': {
        'en': 'Soybean flour', 'ko': '콩가루', 'zh-tw': '黃豆粉', 'zh-cn': '黄豆粉'
    },
    r'^ほうじ茶$': {
        'en': 'Roasted green tea', 'ko': '호지차', 'zh-tw': '焙茶', 'zh-cn': '焙茶'
    },
    r'^おから$': {
        'en': 'Okara (Soy pulp)', 'ko': '비지', 'zh-tw': '豆渣', 'zh-cn': '豆渣'
    },
    r'^クッキー$': {
        'en': 'Cookie', 'ko': '쿠키', 'zh-tw': '餅乾', 'zh-cn': '饼干'
    },
    r'^チョコソース$': {
        'en': 'Chocolate sauce', 'ko': '초코 소스', 'zh-tw': '巧克力醬', 'zh-cn': '巧克力酱'
    },
    r'トッピング\s*topping': {
        'en': 'Toppings', 'ko': '토핑', 'zh-tw': '配料', 'zh-cn': '配料'
    },
    r'ワッ(Full|풀|全尺寸)ソフトクリーム＆(Waffle Whip|와플 휩|華夫餅打發奶油|华夫饼打发奶油)には': {
        'en': 'You can add toppings to the Bubble Waffle Soft Serve & Whip.', 'ko': '버블 와플 소프트 & 와플 휩에는', 'zh-tw': '您可以為泡泡鬆餅霜淇淋及打發奶油', 'zh-cn': '您可以为泡泡华夫饼冰淇淋及打发奶油'
    },
    r'トッピングを追加することができます。': {
        'en': ' ', 'ko': '토핑을 추가할 수 있습니다.', 'zh-tw': '追加喜歡的配料。', 'zh-cn': '追加喜欢的配料。'
    },
    r'ぜひあなた好みにカスタマイズしてお召し上がりください。': {
        'en': 'Customize it to your liking and enjoy!', 'ko': '취향에 맞게 커스터마이즈해서 즐겨보세요.', 'zh-tw': '請隨心所欲地客製化您的專屬美味。', 'zh-cn': '请随心所欲地定制您的专属美味。'
    },
    
    # --- waffle.html (Only translate in non-EN) ---
    r'Freshly Baked Domestic Rice Flour Waffle': {
        'en': 'Freshly Baked Domestic Rice Flour Waffle', 'ko': '갓 구운 국내산 쌀가루 와플', 'zh-tw': '現烤日本國產米粉鬆餅', 'zh-cn': '现烤日本国产米粉华夫饼'
    },
    r'Warm, crispy on the outside, and chewy on the inside, shaped like bubbles.': {
        'en': 'Warm, crispy on the outside, and chewy on the inside, shaped like bubbles.', 'ko': '따뜻하고 겉은 바삭, 속은 쫀득한 버블 모양의 와플입니다.', 'zh-tw': '熱騰騰、外酥內軟Ｑ的泡泡造型鬆餅。', 'zh-cn': '热腾腾、外酥内软Ｑ的泡泡造型华夫饼。'
    },

    # --- ice.html (Only translate in non-EN) ---
    r'^Melting\s*chocolate$': {
        'en': 'Melting chocolate', 'ko': '사르르 녹는 초콜릿', 'zh-tw': '入口即化的巧克力', 'zh-cn': '入口即化的巧克力'
    },
    r'^Refreshing\s*apple$': {
        'en': 'Refreshing apple', 'ko': '상큼한 사과', 'zh-tw': '清爽蘋果', 'zh-cn': '清爽苹果'
    },
    r'^Supreme\s*rich\s*matcha$': {
        'en': 'Supreme rich matcha', 'ko': '궁극의 진한 말차', 'zh-tw': '極致濃郁抹茶', 'zh-cn': '极致浓郁抹茶'
    },
    r'^Fragrant\s*hojicha$': {
        'en': 'Fragrant hojicha', 'ko': '향긋한 호지차', 'zh-tw': '香醇焙茶', 'zh-cn': '香醇焙茶'
    },
    r'^Juicy\s*dragon\s*fruit$': {
        'en': 'Juicy dragon fruit', 'ko': '과즙 가득 용과', 'zh-tw': '多汁火龍果', 'zh-cn': '多汁火龙果'
    },

    # --- dounuts.html (Only translate in non-EN) ---
    r'^Lemon\s*Earl\s*Grey$': {
        'en': 'Lemon Earl Grey', 'ko': '레몬 얼그레이', 'zh-tw': '檸檬伯爵茶', 'zh-cn': '柠檬伯爵茶'
    },
    r'^Soybean\s*flour\s*glaze$': {
        'en': 'Soybean flour glaze', 'ko': '콩가루 글레이즈', 'zh-tw': '黃豆粉糖霜', 'zh-cn': '黄豆粉糖霜'
    },
    r'^Black\s*sesame\s*glaze$': {
        'en': 'Black sesame glaze', 'ko': '검은깨 글레이즈', 'zh-tw': '黑芝麻糖霜', 'zh-cn': '黑芝麻糖霜'
    },
    r'^Couvert\s*chocolate\s*nuts$': {
        'en': 'Couvert chocolate nuts', 'ko': '쿠버춰 초콜릿 넛츠', 'zh-tw': '調溫巧克力堅果', 'zh-cn': '调温巧克力坚果'
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
                
                # Replace exact matches with regex
                # We need to preserve HTML tags if the text is inside them
                # But since our patterns are exact strings, we can just use re.sub
                new_html = re.sub(pattern, replacement, html, flags=re.MULTILINE)
                if new_html != html:
                    html = new_html
                    modified = True
                    
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"Fixed translations in {lang}/{filename}")

translate_all_subpages()
