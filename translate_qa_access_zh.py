import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

replacements_zh_tw = {
    'Frequently Asked Questions': '常見問題',
    'Do you have eat-in space?': '有內用座位嗎？',
    'Yes, we have 4 seats inside the store. All items are also available for take-out.<br>We recommend soft serve and waffles for eat-in, and donuts and craft ice cream for take-out.': '是的，店內設有4個座位。所有商品均可外帶。<br>我們推薦在店享用霜淇淋和華夫餅，外帶則推薦甜甜圈和手工冰淇淋。',
    'How should I eat<br class="hidden-pc">the take-out donuts?': '外帶的甜甜圈<br class="hidden-pc">應該怎麼吃？',
    'Our donuts are sold frozen to maintain their deliciousness.<br>Please warm them up in the microwave (600W for 1 minute) before eating.<br>The expiration date is 3 months when frozen. After thawing, please consume within 3 days (keep refrigerated).<br>We can also warm them up for you in the store.': '為了保持最佳口感，我們的甜甜圈是冷凍銷售的。<br>請用微波爐加熱（600W加熱1分鐘）後食用。<br>冷凍保存期限為3個月。解凍後請冷藏，並在3天內食用。<br>我們也可以在店內為您加熱。',
    '600W / 1minute': '600W / 1分鐘',
    'Is there a parking lot?': '有停車場嗎？',
    'We do not have a private parking lot.<br>Please use a nearby coin parking area.': '我們沒有專用停車場。<br>請使用附近的收費停車場。',
    'Address: 1F Chisan Mansion Daisan Hakata,<br>2-2-24 Yakuin, Chuo-ku, Fukuoka-shi, Fukuoka 810-0022': '地址：福岡縣福岡市中央區藥院2-2-24<br>智山第3博多公寓 1F 郵編 810-0022',
    'Opening Hours: 11:00 ~ 22:00<br>Closed: Open every day': '營業時間：11:00 ~ 22:00<br>公休日：無休（每天營業）'
}

replacements_zh_cn = {
    'Frequently Asked Questions': '常见问题',
    'Do you have eat-in space?': '有堂食座位吗？',
    'Yes, we have 4 seats inside the store. All items are also available for take-out.<br>We recommend soft serve and waffles for eat-in, and donuts and craft ice cream for take-out.': '是的，店内设有4个座位。所有商品均可外带。<br>我们推荐在店享用软冰淇淋和华夫饼，外带则推荐甜甜圈和手工冰淇淋。',
    'How should I eat<br class="hidden-pc">the take-out donuts?': '外带的甜甜圈<br class="hidden-pc">应该怎么吃？',
    'Our donuts are sold frozen to maintain their deliciousness.<br>Please warm them up in the microwave (600W for 1 minute) before eating.<br>The expiration date is 3 months when frozen. After thawing, please consume within 3 days (keep refrigerated).<br>We can also warm them up for you in the store.': '为了保持最佳口感，我们的甜甜圈是冷冻销售的。<br>请用微波炉加热（600W加热1分钟）后食用。<br>冷冻保存期限为3个月。解冻后请冷藏，并在3天内食用。<br>我们也可以在店内为您加热。',
    '600W / 1minute': '600W / 1分钟',
    'Is there a parking lot?': '有停车场吗？',
    'We do not have a private parking lot.<br>Please use a nearby coin parking area.': '我们没有专用停车场。<br>请使用附近的收费停车场。',
    'Address: 1F Chisan Mansion Daisan Hakata,<br>2-2-24 Yakuin, Chuo-ku, Fukuoka-shi, Fukuoka 810-0022': '地址：福冈县福冈市中央区药院2-2-24<br>智山第3博多公寓 1F 邮编 810-0022',
    'Opening Hours: 11:00 ~ 22:00<br>Closed: Open every day': '营业时间：11:00 ~ 22:00<br>休息日：无休（每天营业）'
}

for lang, replacements in [('zh-tw', replacements_zh_tw), ('zh-cn', replacements_zh_cn)]:
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
    
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        for old_str, new_str in replacements.items():
            html = html.replace(old_str, new_str)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

print("Q&A and Access sections translated for Chinese pages.")
