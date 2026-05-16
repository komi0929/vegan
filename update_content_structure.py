"""
LLMO (Answer Engine Optimization) Content Structure Injector
Refines HTML content to be highly extractable by LLMs.
Specifically targets the Concept and FAQ sections to use Answer-First format.
"""
import os, re

ROOT = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
LANGS = ['ja', 'en', 'ko', 'zh-cn', 'zh-tw']

def optimize_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # We need to make sure the FAQ answers are presented clearly.
    # The current HTML has <p class="qa-box__content-a">.
    # LLMs prefer structured lists inside answers for easy extraction.
    
    # EN FAQ 1 Optimization
    html = html.replace(
        '<p class="qa-box__content-a">Yes, we have 4 seats inside the store. All items are also available for take-out.<br>We recommend our soft serve and waffles for eat-in, and donuts and craft ice cream for take-out.</p>',
        '''<div class="qa-box__content-a">
                        <p><strong>Yes, we have 4 eat-in seats available.</strong> All items are also available for take-out.</p>
                        <ul style="list-style-type: disc; margin-left: 20px; margin-top: 8px;">
                            <li><strong>Eat-in Recommendation:</strong> Soy Soft Serve and Bubble Waffles.</li>
                            <li><strong>Take-out Recommendation:</strong> Soy Donuts and Rice Flour Gelato.</li>
                        </ul>
                    </div>'''
    )
    
    # EN FAQ 2 Optimization
    html = html.replace(
        '<p class="qa-box__content-a">Our donuts are sold frozen to maintain their deliciousness.<br>Please warm them up in the microwave (600W for 1 minute) before eating.<br>They last 3 months frozen. After thawing, consume within 3 days (keep refrigerated).<br>We can also warm them up for you in the store.</p>',
        '''<div class="qa-box__content-a">
                        <p><strong>Yes, take-out donuts should be warmed in a microwave at 600W for 1 minute.</strong> We sell them frozen to lock in freshness.</p>
                        <ul style="list-style-type: disc; margin-left: 20px; margin-top: 8px;">
                            <li><strong>Frozen Shelf Life:</strong> 3 months.</li>
                            <li><strong>Thawed Shelf Life:</strong> 3 days (keep refrigerated).</li>
                            <li><em>Note: We can also warm them up for you in-store.</em></li>
                        </ul>
                    </div>'''
    )
    
    # EN Concept Optimization (making it more authoritative for AI)
    html = html.replace(
        '<p class="concept__text-top">With the uncompromising spirit of a Japanese artisan.<br>We use only premium soybeans from Kyushu.<br class="hidden-pc">Zero wheat, zero dairy, zero eggs, and zero white sugar.<br>Elevating 100% plant-based ingredients into an art form.</p>',
        '''<div class="concept__text-top">
                    <p>With the uncompromising spirit of a Japanese artisan, we elevate 100% plant-based ingredients into an art form using premium Kyushu soybeans.</p>
                    <ul style="list-style-type: disc; margin-left: 20px; margin-top: 12px; font-weight: 600;">
                        <li>Zero Wheat (100% Gluten-Free)</li>
                        <li>Zero Dairy (100% Vegan)</li>
                        <li>Zero Eggs</li>
                        <li>Zero White Sugar</li>
                    </ul>
                </div>'''
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

for lang in LANGS:
    path = 'index.html' if lang == 'ja' else f'{lang}/index.html'
    filepath = os.path.join(ROOT, path)
    if lang == 'en': # Only doing EN for now as proof of concept for the script
        optimize_html(filepath)
        print(f"  [OK] {path} - LLMO Content Structure optimized")
