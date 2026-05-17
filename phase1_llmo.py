import os
from bs4 import BeautifulSoup

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# --- Content Dictionaries ---
meta_data = {
    'waffle.html': {
        'en': {'title': 'Gluten-Free Bubble Waffle | SoyStories', 'desc': 'Enjoy our freshly baked gluten-free and plant-based bubble waffle. Warm, crispy on the outside, and chewy on the inside.'},
        'ko': {'title': '글루텐 프리 버블 와플 | SoyStories', 'desc': '갓 구운 글루텐 프리 및 100% 식물성 버블 와플. 겉은 바삭하고 속은 쫀득한 식감을 즐겨보세요.'},
        'zh-tw': {'title': '無麩質泡泡鬆餅 | SoyStories', 'desc': '現烤無麩質及100%植物性泡泡鬆餅。享受外酥內軟Ｑ的美味口感。'},
        'zh-cn': {'title': '无麸质泡泡华夫饼 | SoyStories', 'desc': '现烤无麸质及100%植物性泡泡华夫饼。享受外酥内软Ｑ的美味口感。'}
    },
    'soft.html': {
        'en': {'title': 'Rich Soy Soft Serve Ice Cream | SoyStories', 'desc': 'A creamy and rich soft serve ice cream made entirely from premium soy milk. 100% vegan and gluten-free.'},
        'ko': {'title': '진한 소이 소프트 아이스크림 | SoyStories', 'desc': '고급 두유로 만든 크리미하고 진한 소프트 아이스크림. 100% 비건 및 글루텐 프리 디저트입니다.'},
        'zh-tw': {'title': '極濃純豆乳霜淇淋 | SoyStories', 'desc': '使用特級豆乳製成的極濃霜淇淋。100%純素與無麩質的安心甜點。'},
        'zh-cn': {'title': '极浓纯豆乳冰淇淋 | SoyStories', 'desc': '使用特级豆乳制成的极浓冰淇淋。100%纯素与无麸质的安心甜点。'}
    },
    'waffle&soft.html': {
        'en': {'title': 'Bubble Waffle & Soy Soft Serve | SoyStories', 'desc': 'Our signature menu item: a perfect combination of our freshly baked bubble waffle and rich soy soft serve.'},
        'ko': {'title': '버블 와플 & 소이 소프트 | SoyStories', 'desc': 'SoyStories의 간판 메뉴: 갓 구운 버블 와플과 진한 소이 소프트 아이스크림의 완벽한 조화.'},
        'zh-tw': {'title': '泡泡鬆餅 & 豆乳霜淇淋 | SoyStories', 'desc': 'SoyStories的招牌餐點：現烤泡泡鬆餅與極濃豆乳霜淇淋的完美結合。'},
        'zh-cn': {'title': '泡泡华夫饼 & 豆乳冰淇淋 | SoyStories', 'desc': 'SoyStories的招牌餐点：现烤泡泡华夫饼与极浓豆乳冰淇淋的完美结合。'}
    },
    'dounuts.html': {
        'en': {'title': 'Baked Soy Donuts | SoyStories', 'desc': 'Healthy baked donuts made with rich soy milk, okara, and rice flour. 100% vegan and gluten-free.'},
        'ko': {'title': '구운 소이 도넛 | SoyStories', 'desc': '진한 두유, 비지, 쌀가루로 만든 건강한 구운 도넛. 100% 비건 및 글루텐 프리입니다.'},
        'zh-tw': {'title': '無負擔豆乳烤甜甜圈 | SoyStories', 'desc': '使用濃郁豆乳、豆渣與米粉製成的健康烤甜甜圈。100%純素與無麩質。'},
        'zh-cn': {'title': '零负担豆乳烤甜甜圈 | SoyStories', 'desc': '使用浓郁豆乳、豆渣与米粉制成的健康烤甜甜圈。100%纯素与无麸质。'}
    },
    'ice.html': {
        'en': {'title': 'Rice Flour Gelato | SoyStories', 'desc': 'Creamy and smooth gelato made with domestic rice flour. Available in a variety of rich, plant-based flavors.'},
        'ko': {'title': '쌀가루 젤라또 | SoyStories', 'desc': '국내산 쌀가루로 만든 크리미하고 부드러운 젤라또. 100% 식물성 재료로 만든 깊은 맛을 즐겨보세요.'},
        'zh-tw': {'title': '米粉義式冰淇淋 | SoyStories', 'desc': '使用日本國產米粉製成的滑順義式冰淇淋。100%植物性成分，擁有多種豐富口味。'},
        'zh-cn': {'title': '米粉意式冰淇淋 | SoyStories', 'desc': '使用日本国产米粉制成的滑顺意式冰淇淋。100%植物性成分，拥有多种丰富口味。'}
    }
}

lang_codes = {
    'en': 'en',
    'ko': 'ko',
    'zh-tw': 'zh-Hant',
    'zh-cn': 'zh-Hans'
}

def inject_hreflang_and_meta():
    # Process en, ko, zh-tw, zh-cn
    for lang, html_lang_code in lang_codes.items():
        lang_dir = os.path.join(root_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        for filename in os.listdir(lang_dir):
            if not filename.endswith('.html'):
                continue
                
            filepath = os.path.join(lang_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            # 1. Update <html lang="...">
            html_tag = soup.find('html')
            if html_tag:
                html_tag['lang'] = html_lang_code
                
            # 2. Update title, desc, og for subpages
            if filename in meta_data:
                data = meta_data[filename].get(lang)
                if data:
                    if soup.title:
                        soup.title.string = data['title']
                    desc_tag = soup.find('meta', attrs={'name': 'description'})
                    if desc_tag:
                        desc_tag['content'] = data['desc']
                    og_title = soup.find('meta', attrs={'property': 'og:title'})
                    if og_title:
                        og_title['content'] = data['title']
                    og_desc = soup.find('meta', attrs={'property': 'og:description'})
                    if og_desc:
                        og_desc['content'] = data['desc']
                        
            # 3. Clear existing hreflang tags to avoid duplicates
            for link in soup.find_all('link', attrs={'rel': 'alternate'}):
                if link.get('hreflang'):
                    link.decompose()
                    
            # 4. Inject new hreflang tags at the end of head
            if soup.head:
                prefix = "" if filename == "index.html" else filename
                hreflangs = [
                    f'<link rel="alternate" hreflang="ja" href="https://soystories.jp/{prefix}">',
                    f'<link rel="alternate" hreflang="en" href="https://soystories.jp/en/{prefix}">',
                    f'<link rel="alternate" hreflang="ko" href="https://soystories.jp/ko/{prefix}">',
                    f'<link rel="alternate" hreflang="zh-Hant" href="https://soystories.jp/zh-tw/{prefix}">',
                    f'<link rel="alternate" hreflang="zh-Hans" href="https://soystories.jp/zh-cn/{prefix}">',
                    f'<link rel="alternate" hreflang="x-default" href="https://soystories.jp/{prefix}">'
                ]
                
                # Append them to the head
                # We use beautifulsoup append
                for h_tag in hreflangs:
                    soup.head.append(BeautifulSoup(h_tag, 'html.parser'))
                    soup.head.append('\n')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated LLMO Phase 1 for: {lang}/{filename}")
            
    # Process Japanese (root) separately for hreflang only
    for filename in os.listdir(root_dir):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        for link in soup.find_all('link', attrs={'rel': 'alternate'}):
            if link.get('hreflang'):
                link.decompose()
                
        if soup.head:
            prefix = "" if filename == "index.html" else filename
            hreflangs = [
                f'<link rel="alternate" hreflang="ja" href="https://soystories.jp/{prefix}">',
                f'<link rel="alternate" hreflang="en" href="https://soystories.jp/en/{prefix}">',
                f'<link rel="alternate" hreflang="ko" href="https://soystories.jp/ko/{prefix}">',
                f'<link rel="alternate" hreflang="zh-Hant" href="https://soystories.jp/zh-tw/{prefix}">',
                f'<link rel="alternate" hreflang="zh-Hans" href="https://soystories.jp/zh-cn/{prefix}">',
                f'<link rel="alternate" hreflang="x-default" href="https://soystories.jp/{prefix}">'
            ]
            
            for h_tag in hreflangs:
                soup.head.append(BeautifulSoup(h_tag, 'html.parser'))
                soup.head.append('\n')
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated LLMO Phase 1 for: root/{filename}")

inject_hreflang_and_meta()
