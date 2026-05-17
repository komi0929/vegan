import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

nav_translations = {
    'ko': {
        'Concept': '콘셉트',
        'Menu': '메뉴',
        'Q&amp;A': '자주 묻는 질문',
        'Q&A': '자주 묻는 질문',
        'Access': '오시는 길'
    },
    'zh-tw': {
        'Concept': '品牌理念',
        'Menu': '菜單',
        'Q&amp;A': '常見問題',
        'Q&A': '常見問題',
        'Access': '交通指南'
    },
    'zh-cn': {
        'Concept': '品牌理念',
        'Menu': '菜单',
        'Q&amp;A': '常见问题',
        'Q&A': '常见问题',
        'Access': '交通指南'
    }
}

# 1. Translate Navigation in ko, zh-tw, zh-cn
for lang, trans in nav_translations.items():
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
        
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        # Replace in header nav and drawer nav
        for en_word, local_word in trans.items():
            # Specifically target the <a> tags to avoid accidental replacements in other text
            content = re.sub(rf'(<a[^>]*class="(?:header|drawer-content)__link"[^>]*>)\s*{en_word}\s*(</a>)', rf'\g<1>{local_word}\g<2>', content)
            
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated Navigation for: {filepath}")

# 2. Inject Trust Banner into Japanese index.html
ja_index_path = os.path.join(root_dir, 'index.html')
with open(ja_index_path, 'r', encoding='utf-8') as f:
    ja_html = f.read()

trust_banner_ja = """    <!-- TRUST BANNER: HappyCow 5.0 -->
    <div aria-label="カスタマーレビューと信頼の証" class="trust-banner" role="complementary">
        <div class="trust-banner__inner">
            <div class="trust-banner__stars">★★★★★</div>
            <div class="trust-banner__rating"><a href="https://www.happycow.net/reviews/soy-stories-fukuoka-291702" rel="noopener" target="_blank">HappyCow</a> 評価 <strong>5.0</strong> — 福岡のヴィーガンスイーツ #1</div>
            <div class="allergen-badges">
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> 乳製品不使用</span>
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> 卵不使用</span>
                <span class="allergen-badge"><span class="allergen-badge__icon">🚫</span> 小麦不使用</span>
            </div>
            <div class="trust-banner__subtext">専用施設による <strong>交差汚染ゼロ</strong> の完全保証。安心してご来店ください。</div>
        </div>
    </div>
"""

# Insert right after the FV closing div.
# Pattern to find the end of fv__inner in index.html
if "<!-- TRUST BANNER: HappyCow 5.0 -->" not in ja_html:
    fv_end_pattern = r'(</div>\s*<!-- コンセプト -->)'
    ja_html = re.sub(fv_end_pattern, rf'    </div>\n{trust_banner_ja}    <!-- コンセプト -->', ja_html, count=1)
    
    with open(ja_index_path, 'w', encoding='utf-8') as f:
        f.write(ja_html)
    print("Injected Trust Banner into Japanese index.html")
else:
    print("Trust Banner already exists in Japanese index.html")

