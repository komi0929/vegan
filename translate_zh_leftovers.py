import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

zh_cn_translations = {
    # eat-in
    "Eat-in & Take-out available.": "提供堂食及外带服务。",
    "We have 4 seats inside our store for you to relax and enjoy your sweets.<br>All items are also available for take-out.<br>We highly recommend our soft serve and waffle for eat-in, and donuts or rice flour gelato for take-out.<br>Please feel free to drop by!": "店内设有4个座位，您可以放松享用甜点。<br>所有商品均可外带。<br>我们推荐您在店内享用冰淇淋和华夫饼，甜甜圈和米粉意式冰淇淋则适合外带。<br>欢迎随时光临！",
    # onlinestore
    "<h2>Online Store</h2>": "<h2>在线商店</h2>",
    "You can order our products<br>from the SoyStories Online Store.": "您可以在 SoyStories 在线商店<br>订购我们的产品。",
    "● For those living far away": "● 给居住较远的朋友",
    "● As a treat for yourself": "● 作为给自己的奖励",
    "● As a gift for your loved ones": "● 作为送给亲友的礼物",
    "Gift wrapping<br>is available": "提供精美<br>礼品包装",
    "Visit Online Store": "访问在线商店",
    # commitment
    "<h2>Our Commitment</h2>": "<h2>我们的坚持</h2>",
    "We use completely additive-free rich soy milk.<br>To maintain its freshness, we always finish processing it<br>within 2 days of squeezing. This temperature management is much<br>more difficult than dairy milk, requiring delicate skills.": "我们使用完全无添加的浓郁豆乳。<br>为了保持新鲜，我们坚持在鲜榨后<br>2天内完成加工。这种温度管理比牛奶要困难得多，<br>需要极其精湛的技艺。",
    "Okara (Soy Pulp)": "豆渣",
    "Rich in dietary fiber<br>and high-quality protein": "富含膳食纤维<br>与优质蛋白",
    "Rice Flour": "米粉",
    "Sweetened gently<br>with beet sugar": "使用甜菜糖<br>温和提甜",
    "Soy Milk": "豆乳",
    "Freshly squeezed<br>and exceptionally rich": "清晨鲜榨<br>口感极其浓郁"
}

zh_tw_translations = {
    # eat-in
    "Eat-in & Take-out available.": "提供內用及外帶服務。",
    "We have 4 seats inside our store for you to relax and enjoy your sweets.<br>All items are also available for take-out.<br>We highly recommend our soft serve and waffle for eat-in, and donuts or rice flour gelato for take-out.<br>Please feel free to drop by!": "店內設有4個座位，您可以放鬆享用甜點。<br>所有商品均可外帶。<br>我們推薦您在店內享用冰淇淋和鬆餅，甜甜圈和米粉義式冰淇淋則適合外帶。<br>歡迎隨時光臨！",
    # onlinestore
    "<h2>Online Store</h2>": "<h2>線上商店</h2>",
    "You can order our products<br>from the SoyStories Online Store.": "您可以在 SoyStories 線上商店<br>訂購我們的產品。",
    "● For those living far away": "● 給居住較遠的朋友",
    "● As a treat for yourself": "● 作為給自己的獎勵",
    "● As a gift for your loved ones": "● 作為送給親友的禮物",
    "Gift wrapping<br>is available": "提供精美<br>禮品包裝",
    "Visit Online Store": "訪問線上商店",
    # commitment
    "<h2>Our Commitment</h2>": "<h2>我們的堅持</h2>",
    "We use completely additive-free rich soy milk.<br>To maintain its freshness, we always finish processing it<br>within 2 days of squeezing. This temperature management is much<br>more difficult than dairy milk, requiring delicate skills.": "我們使用完全無添加的濃郁豆乳。<br>為了保持新鮮，我們堅持在鮮榨後<br>2天內完成加工。這種溫度管理比牛奶要困難得多，<br>需要極其精湛的技藝。",
    "Okara (Soy Pulp)": "豆渣",
    "Rich in dietary fiber<br>and high-quality protein": "富含膳食纖維<br>與優質蛋白",
    "Rice Flour": "米粉",
    "Sweetened gently<br>with beet sugar": "使用甜菜糖<br>溫和提甜",
    "Soy Milk": "豆乳",
    "Freshly squeezed<br>and exceptionally rich": "清晨鮮榨<br>口感極其濃郁"
}

def translate_file(file_path, translation_dict):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    for en_text, zh_text in translation_dict.items():
        html = html.replace(en_text, zh_text)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Translated leftovers in {file_path}")

translate_file(os.path.join(root_dir, 'zh-cn', 'index.html'), zh_cn_translations)
translate_file(os.path.join(root_dir, 'zh-tw', 'index.html'), zh_tw_translations)
