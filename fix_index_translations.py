import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# We will replace the Japanese ice cream block with the translated versions.
jap_ice_cream = """                        <p class="menu__title-ja">米粉ジェラート</p>
                        <p class="menu__title-en hidden-sp">rice flour gelato</p>
                        <p class="menu__text">クリーミーな口溶けが魅力的なアイスクリーム。</p>
                        <a href="./ice.html">>>もっと見る</a>"""

translations = {
    'en': """                        <p class="menu__title-ja" style="font-family:var(--ff-serif-en);">Rice Flour Gelato</p>
                        <p class="menu__title-en hidden-sp">rice flour gelato</p>
                        <p class="menu__text" style="font-family:var(--ff-serif-en);">A masterpiece of creaminess. You will not believe it is 100% dairy-free.</p>
                        <a href="./ice.html">>>View more</a>""",
    'ko': """                        <p class="menu__title-ja">쌀가루 젤라또</p>
                        <p class="menu__title-en hidden-sp">rice flour gelato</p>
                        <p class="menu__text">크리미하게 입안에서 녹아내리는 매력적인 아이스크림.</p>
                        <a href="./ice.html">>>더 보기</a>""",
    'zh-cn': """                        <p class="menu__title-ja">米粉意式冰淇淋</p>
                        <p class="menu__title-en hidden-sp">rice flour gelato</p>
                        <p class="menu__text">口感绵密、入口即化的迷人冰淇淋。</p>
                        <a href="./ice.html">>>查看更多</a>""",
    'zh-tw': """                        <p class="menu__title-ja">米粉義式冰淇淋</p>
                        <p class="menu__title-en hidden-sp">rice flour gelato</p>
                        <p class="menu__text">口感綿密、入口即化的迷人冰淇淋。</p>
                        <a href="./ice.html">>>查看更多</a>"""
}

for lang, translated_block in translations.items():
    filepath = os.path.join(root_dir, lang, 'index.html')
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace(jap_ice_cream, translated_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Done translating index.html ice cream blocks!")
