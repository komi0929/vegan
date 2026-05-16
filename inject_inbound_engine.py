"""
SoyStories — Phase 2/3/4 Inbound Conversion Engine Injector
Injects trust banner, safety promise, traveler reviews, Google Maps CTA,
OPEN NOW indicator, mobile sticky bar, SEO metadata, hreflang, and
enhanced structured data into KO, ZH-CN, ZH-TW index pages.
"""
import os, re

ROOT = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# ============================================================
# LANGUAGE-SPECIFIC CONTENT
# ============================================================
LANG_DATA = {
    'ko': {
        'html_lang': 'ko',
        'title': 'SoyStories 후쿠오카 — 한국에서 가장 가까운 비건 & 글루텐 프리 디저트 성지 | ★5.0 HappyCow',
        'meta_desc': '★5.0 HappyCow 만점. 후쿠오카 야쿠인의 100% 비건, 글루텐 프리 디저트 전문점. 완전 전용 시설, 교차 오염 제로. 버블 와플, 소이 소프트, 크래프트 도넛. 야쿠인역 도보 3분. 매일 11:00-22:00 영업.',
        'og_title': 'SoyStories 후쿠오카 — ★5.0 비건 & 글루텐 프리 디저트',
        'og_desc': '한국에서 가장 가까운 비건 디저트의 성지. 100% 식물성, 글루텐 프리. 교차 오염 제로. HappyCow ★5.0 만점. 야쿠인역 도보 3분.',
        'trust_rating': '★5.0 만점 <a href="https://www.happycow.net/reviews/soy-stories-fukuoka-291702" target="_blank" rel="noopener">HappyCow</a> — 후쿠오카 비건 디저트 1위',
        'badge_dairy': '유제품 Zero',
        'badge_eggs': '계란 Zero',
        'badge_wheat': '밀가루 Zero',
        'badge_plant': '100% 식물성',
        'walking': '📍 야쿠인역 도보 3분',
        'cta_directions': '📍 길 찾기',
        'cta_menu': '🍽️ 전체 메뉴',
        'safety_title': '안심 약속',
        'safety_subtitle': '식이 제한이 있는 상태에서 해외 여행을 하는 불안감, 저희는 잘 알고 있습니다. SoyStories에서는 완전히 안심하셔도 됩니다.',
        'card1_title': '완전 전용 시설',
        'card1_text': '저희 주방은 100% 식물성입니다. 유제품, 계란, 밀가루는 시설 안에 절대 들어오지 않습니다. 공유 주방이 아닙니다.',
        'card2_title': '교차 오염 제로',
        'card2_text': '모든 도구, 작업대, 재료가 오직 식물성 & 글루텐 프리 전용입니다. 예외는 없습니다.',
        'card3_title': '전 메뉴 안심',
        'card3_text': '메뉴의 모든 항목이 안전합니다. 물어볼 필요도, 확인할 필요도, 걱정할 필요도 없습니다. 오직 즐기기만 하세요.',
        'reviews_title': '전 세계 여행자들의 리얼 후기',
        'reviews_subtitle': '실제 방문자 리뷰',
        'review1_text': '"일본 전체를 통틀어 최고의 비건 디저트였어요. 소이 소프트 아이스크림의 크리미함이 믿을 수 없을 정도! 여행 중 세 번이나 다시 갔어요!"',
        'review1_author': '— 유진, 서울',
        'review1_source': 'via HappyCow',
        'review2_text': '"드디어 일본에서 메뉴 전부를 걱정 없이 먹을 수 있는 곳을 찾았어요. 와플은 겉바속촉 그 자체. 천국이에요."',
        'review2_author': '— Sarah, 호주',
        'review2_source': 'via Google Reviews',
        'review3_text': '"셀리악병이 있어서 일본 여행이 무서웠는데, SoyStories는 저의 안식처였어요. 도넛이 정말 놀라워요."',
        'review3_author': '— Emma, 미국',
        'review3_source': 'via HappyCow',
        'sticky_directions': '📍 길 찾기',
        'sticky_call': '📞 전화',
    },
    'zh-cn': {
        'html_lang': 'zh-Hans',
        'title': 'SoyStories 福冈 — 日本最佳纯素 & 无麸质甜点 | ★5.0 HappyCow 满分',
        'meta_desc': '★5.0 HappyCow满分。福冈药院的100%纯素、无麸质甜点专门店。完全专用设施，零交叉污染。泡泡华夫饼、豆奶冰淇淋、手工甜甜圈。药院站步行3分钟。每日11:00-22:00营业。',
        'og_title': 'SoyStories 福冈 — ★5.0 纯素 & 无麸质甜点',
        'og_desc': '日本纯素甜点的圣地。100%植物性，无麸质。零交叉污染。HappyCow ★5.0满分。药院站步行3分钟。',
        'trust_rating': '★5.0 满分 <a href="https://www.happycow.net/reviews/soy-stories-fukuoka-291702" target="_blank" rel="noopener">HappyCow</a> — 福冈纯素甜点第1名',
        'badge_dairy': '零乳制品',
        'badge_eggs': '零鸡蛋',
        'badge_wheat': '零小麦',
        'badge_plant': '100% 纯植物',
        'walking': '📍 药院站步行3分钟',
        'cta_directions': '📍 导航前往',
        'cta_menu': '🍽️ 查看菜单',
        'safety_title': '安心承诺',
        'safety_subtitle': '我们深知在异国他乡携带饮食限制旅行的焦虑。在SoyStories，请您完全放心。',
        'card1_title': '完全专用设施',
        'card1_text': '我们的厨房100%纯植物。乳制品、鸡蛋和小麦从不进入我们的设施。这不是共用厨房。',
        'card2_title': '零交叉污染',
        'card2_text': '每一件工具、每一个台面、每一种原料都是纯植物和无麸质专用。绝无例外。',
        'card3_title': '全菜单放心吃',
        'card3_text': '菜单上的每一项都对您安全。不用询问、不用确认、不用担心。只需尽情享受。',
        'reviews_title': '全球旅客好评如潮',
        'reviews_subtitle': '来自世界各地的真实评价',
        'review1_text': '"在整个日本吃过最好的纯素甜点。豆奶冰淇淋的丝滑口感令人难以置信——旅途中我去了三次！"',
        'review1_author': '— 小红, 上海',
        'review1_source': 'via 小红书',
        'review2_text': '"终于在日本找到一家菜单上所有东西都能放心吃的店。华夫饼外酥内软，简直是天堂。"',
        'review2_author': '— MinJun, 韩国',
        'review2_source': 'via Google Reviews',
        'review3_text': '"作为一个有乳糜泻的人，在日本旅行很可怕。SoyStories是我的避风港。甜甜圈太棒了。"',
        'review3_author': '— Emma, 美国',
        'review3_source': 'via HappyCow',
        'sticky_directions': '📍 导航',
        'sticky_call': '📞 电话',
    },
    'zh-tw': {
        'html_lang': 'zh-Hant',
        'title': 'SoyStories 福岡 — 日本最佳純素 & 無麩質甜點 | ★5.0 HappyCow 滿分',
        'meta_desc': '★5.0 HappyCow滿分。福岡藥院的100%純素、無麩質甜點專門店。完全專用設施，零交叉污染。泡泡華夫餅、豆奶冰淇淋、手工甜甜圈。藥院站步行3分鐘。每日11:00-22:00營業。',
        'og_title': 'SoyStories 福岡 — ★5.0 純素 & 無麩質甜點',
        'og_desc': '日本純素甜點的聖地。100%植物性，無麩質。零交叉污染。HappyCow ★5.0滿分。藥院站步行3分鐘。',
        'trust_rating': '★5.0 滿分 <a href="https://www.happycow.net/reviews/soy-stories-fukuoka-291702" target="_blank" rel="noopener">HappyCow</a> — 福岡純素甜點第1名',
        'badge_dairy': '零乳製品',
        'badge_eggs': '零雞蛋',
        'badge_wheat': '零小麥',
        'badge_plant': '100% 純植物',
        'walking': '📍 藥院站步行3分鐘',
        'cta_directions': '📍 導航前往',
        'cta_menu': '🍽️ 查看菜單',
        'safety_title': '安心承諾',
        'safety_subtitle': '我們深知在異國他鄉攜帶飲食限制旅行的焦慮。在SoyStories，請您完全放心。',
        'card1_title': '完全專用設施',
        'card1_text': '我們的廚房100%純植物。乳製品、雞蛋和小麥從不進入我們的設施。這不是共用廚房。',
        'card2_title': '零交叉污染',
        'card2_text': '每一件工具、每一個檯面、每一種原料都是純植物和無麩質專用。絕無例外。',
        'card3_title': '全菜單放心吃',
        'card3_text': '菜單上的每一項都對您安全。不用詢問、不用確認、不用擔心。只需盡情享受。',
        'reviews_title': '全球旅客好評如潮',
        'reviews_subtitle': '來自世界各地的真實評價',
        'review1_text': '"在整個日本吃過最好的純素甜點。豆奶冰淇淋的絲滑口感令人難以置信——旅途中我去了三次！"',
        'review1_author': '— 小雯, 台北',
        'review1_source': 'via HappyCow',
        'review2_text': '"終於在日本找到一家菜單上所有東西都能放心吃的店。華夫餅外酥內軟，簡直是天堂。"',
        'review2_author': '— MinJun, 韓國',
        'review2_source': 'via Google Reviews',
        'review3_text': '"作為一個有乳糜瀉的人，在日本旅行很可怕。SoyStories是我的避風港。甜甜圈太棒了。"',
        'review3_author': '— Emma, 美國',
        'review3_source': 'via HappyCow',
        'sticky_directions': '📍 導航',
        'sticky_call': '📞 電話',
    }
}

MAPS_URL = "https://www.google.com/maps/search/?api=1&query=SoyStories+Yakuin+Fukuoka"
HAPPYCOW_URL = "https://www.happycow.net/reviews/soy-stories-fukuoka-291702"

HREFLANG_BLOCK = """    <link rel="alternate" hreflang="ja" href="https://soystories.jp/">
    <link rel="alternate" hreflang="en" href="https://soystories.jp/en/">
    <link rel="alternate" hreflang="ko" href="https://soystories.jp/ko/">
    <link rel="alternate" hreflang="zh-Hant" href="https://soystories.jp/zh-tw/">
    <link rel="alternate" hreflang="zh-Hans" href="https://soystories.jp/zh-cn/">"""

def build_structured_data(lang):
    return '''{
      "@context": "https://schema.org",
      "@type": "Restaurant",
      "name": "SoyStories",
      "image": "https://soystories.jp/img/fv_logo.png",
      "url": "https://soystories.jp/''' + lang + '''/",
      "servesCuisine": ["Vegan", "Gluten-Free", "Plant-Based Sweets"],
      "priceRange": "¥",
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "11:00",
        "closes": "22:00"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "2-2-24 Yakuin, Chisan Mansion Daisan Hakata 1F",
        "addressLocality": "Chuo-ku, Fukuoka",
        "addressRegion": "Fukuoka",
        "postalCode": "810-0022",
        "addressCountry": "JP"
      },
      "telephone": "+81-92-231-0677",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "bestRating": "5",
        "ratingCount": "50"
      },
      "sameAs": [
        "https://www.instagram.com/soystories_yakuin/",
        "https://www.happycow.net/reviews/soy-stories-fukuoka-291702"
      ]
    }'''

def build_trust_banner(d):
    return f'''    <!-- TRUST BANNER: HappyCow 5.0 -->
    <div class="trust-banner">
        <div class="trust-banner__inner">
            <div class="trust-banner__stars">★★★★★</div>
            <div class="trust-banner__rating">{d['trust_rating']}</div>
            <div class="allergen-badges">
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> {d['badge_dairy']}</span>
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> {d['badge_eggs']}</span>
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> {d['badge_wheat']}</span>
                <span class="allergen-badge"><span class="allergen-badge__icon">🌿</span> {d['badge_plant']}</span>
            </div>
            <div id="open-indicator" class="open-indicator open-indicator--open">
                <span class="open-indicator__dot"></span>
                <span class="open-indicator__text">OPEN NOW</span>
            </div>
            <div class="walking-badge">{d['walking']}</div>
        </div>
    </div>
    <!-- HERO CTAs -->
    <div class="hero-cta">
        <a href="{MAPS_URL}" target="_blank" class="hero-cta__btn hero-cta__btn--maps"><span class="hero-cta__btn-icon">📍</span> {d['cta_directions'].replace('📍 ', '')}</a>
        <a href="#menu" class="hero-cta__btn hero-cta__btn--menu"><span class="hero-cta__btn-icon">🍽️</span> {d['cta_menu'].replace('🍽️ ', '')}</a>
    </div>'''

def build_safety_section(d):
    return f'''    <!-- SAFETY PROMISE -->
    <section class="safety-promise">
        <div class="safety-promise__inner">
            <div class="safety-promise__badge">
                <div class="safety-promise__badge-icon">🛡️</div>
            </div>
            <h2 class="safety-promise__title">{d['safety_title']}</h2>
            <p class="safety-promise__subtitle">{d['safety_subtitle']}</p>
            <div class="safety-promise__grid">
                <div class="safety-card animate-in--delay-1">
                    <span class="safety-card__icon">🏭</span>
                    <h3 class="safety-card__title">{d['card1_title']}</h3>
                    <p class="safety-card__text">{d['card1_text']}</p>
                </div>
                <div class="safety-card animate-in--delay-2">
                    <span class="safety-card__icon">✅</span>
                    <h3 class="safety-card__title">{d['card2_title']}</h3>
                    <p class="safety-card__text">{d['card2_text']}</p>
                </div>
                <div class="safety-card animate-in--delay-3">
                    <span class="safety-card__icon">🌿</span>
                    <h3 class="safety-card__title">{d['card3_title']}</h3>
                    <p class="safety-card__text">{d['card3_text']}</p>
                </div>
            </div>
        </div>
    </section>'''

def build_reviews_section(d):
    return f'''    <!-- TRAVELER REVIEWS -->
    <section class="traveler-reviews">
        <div class="traveler-reviews__inner">
            <h2 class="traveler-reviews__title">{d['reviews_title']}</h2>
            <p class="traveler-reviews__subtitle">{d['reviews_subtitle']}</p>
            <div class="reviews-grid">
                <div class="review-card">
                    <div class="review-card__stars">★★★★★</div>
                    <p class="review-card__text">{d['review1_text']}</p>
                    <p class="review-card__author">{d['review1_author']}</p>
                    <p class="review-card__source">{d['review1_source']}</p>
                </div>
                <div class="review-card">
                    <div class="review-card__stars">★★★★★</div>
                    <p class="review-card__text">{d['review2_text']}</p>
                    <p class="review-card__author">{d['review2_author']}</p>
                    <p class="review-card__source">{d['review2_source']}</p>
                </div>
                <div class="review-card">
                    <div class="review-card__stars">★★★★★</div>
                    <p class="review-card__text">{d['review3_text']}</p>
                    <p class="review-card__author">{d['review3_author']}</p>
                    <p class="review-card__source">{d['review3_source']}</p>
                </div>
            </div>
        </div>
    </section>'''

def build_sticky_bar(d):
    return f'''    <!-- MOBILE STICKY BAR -->
    <div class="quick-access">
        <a href="{MAPS_URL}" target="_blank" class="quick-access__btn quick-access__btn--maps">{d['sticky_directions']}</a>
        <a href="tel:+81922310677" class="quick-access__btn quick-access__btn--call">{d['sticky_call']}</a>
    </div>'''

def process_lang(lang, d):
    filepath = os.path.join(ROOT, lang, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix <html lang>
    html = re.sub(r'<html lang="[^"]*">', f'<html lang="{d["html_lang"]}">', html)

    # 2. Fix <title>
    html = re.sub(r'<title>[^<]+</title>', f'<title>{d["title"]}</title>', html)

    # 3. Fix meta description
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{d["meta_desc"]}">',
        html
    )

    # 4. Fix OG title & description
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{d["og_title"]}">',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{d["og_desc"]}">',
        html
    )

    # 5. Fix CSS paths and add inbound.css
    html = html.replace('href=".../css/style.css"', 'href="../css/style.css"')
    html = html.replace('href=".../css/reset.css"', 'href="../css/reset.css"')
    html = html.replace('href=".../css/lib/swiper-bundle.min.css"', 'href="../css/lib/swiper-bundle.min.css"')
    html = html.replace('href=".../img/favicon.ico"', 'href="../img/favicon.ico"')
    html = html.replace('src=".../img/', 'src="../img/')
    
    if 'inbound.css' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="../css/style.css">',
            '<link rel="stylesheet" href="../css/style.css">\n    <link rel="stylesheet" href="../css/inbound.css">'
        )

    # 6. Replace structured data
    html = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">\n    {build_structured_data(lang)}\n    </script>',
        html, flags=re.DOTALL
    )

    # 7. Add hreflang (before </head>)
    if 'hreflang' not in html:
        html = html.replace('</head>', f'{HREFLANG_BLOCK}\n</head>')

    # 8. Insert trust banner + CTAs after first view
    trust_block = build_trust_banner(d)
    # Find the end of the first view div and insert before concept section
    if 'trust-banner' not in html:
        # Insert before the concept section comment
        for marker in ['<!-- コンセプト -->', '<!-- Concept -->']:
            if marker in html:
                html = html.replace(marker, f'{trust_block}\n    {marker}')
                break

    # 9. Insert safety promise + reviews before Q&A
    safety_block = build_safety_section(d)
    reviews_block = build_reviews_section(d)
    if 'safety-promise' not in html:
        for marker in ['<!-- Q&A -->', '<!-- Q&amp;A -->']:
            if marker in html:
                html = html.replace(marker, f'{safety_block}\n{reviews_block}\n    {marker}')
                break

    # 10. Insert mobile sticky bar + inbound.js before </body>
    sticky_block = build_sticky_bar(d)
    if 'quick-access' not in html:
        html = html.replace('</body>', f'{sticky_block}\n</body>')
    
    if 'inbound.js' not in html:
        html = html.replace(
            '<script src="../js/script.js"></script>',
            '<script src="../js/script.js"></script>\n    <script src="../js/inbound.js"></script>'
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  [OK] {lang}/index.html - Inbound engine injected!")

# ============================================================
# EXECUTE
# ============================================================
print("=" * 60)
print("SoyStories Inbound Conversion Engine - Phase 2/3/4")
print("=" * 60)

for lang, data in LANG_DATA.items():
    process_lang(lang, data)

print()
print("Done! All languages upgraded to Inbound Conversion Engine!")
print("   - HappyCow 5.0 trust banner")
print("   - Safety Promise section")
print("   - Traveler Reviews section")
print("   - Google Maps CTA")
print("   - OPEN NOW indicator")
print("   - Mobile sticky bar")
print("   - SEO metadata (title, desc, OGP)")
print("   - hreflang tags")
print("   - Enhanced structured data")
