import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

fixes = {
    'en': {
        'Plainドーナツ': 'Plain Donuts',
        'Black sesameグレーズ': 'Black Sesame Glaze',
        'Matchaグレーズ': 'Matcha Glaze',
        'Soybean flourグレーズ': 'Kinako Glaze',
        '【公式】SoyStories | グルテンフリー＆プラントベーススイーツ': '【Official】SoyStories | Gluten-Free & Plant-Based Sweets',
        '本格派Matchaスイーツ': 'authentic matcha sweet',
        'Plainフレイバー': 'Plain flavored',
        'Matchaドーナツ': 'matcha donut',
    },
    'ko': {
        '플레인ドーナツ': '플레인 도넛',
        '검은깨グレーズ': '검은깨 글레이즈',
        '말차グレーズ': '말차 글레이즈',
        '콩가루グレーズ': '콩가루 글레이즈',
        '【公式】SoyStories | グルテンフリー＆プラントベーススイーツ': '【공식】SoyStories | 글루텐 프리 & 플랜트 베이스 스위츠',
    },
    'zh-cn': {
        '原味ドーナツ': '原味甜甜圈',
        '黑芝麻グレーズ': '黑芝麻糖霜',
        '抹茶グレーズ': '抹茶糖霜',
        '黄豆粉グレーズ': '黄豆粉糖霜',
        '【公式】SoyStories | グルテンフリー＆プラントベーススイーツ': '【官方】SoyStories | 无麸质 & 植物性甜点',
    },
    'zh-tw': {
        '原味ドーナツ': '原味甜甜圈',
        '黑芝麻グレーズ': '黑芝麻糖霜',
        '抹茶グレーズ': '抹茶糖霜',
        '黄豆粉グレーズ': '黃豆粉糖霜',
        '【公式】SoyStories | グルテンフリー＆プラントベーススイーツ': '【官方】SoyStories | 無麩質 & 植物性甜點',
    }
}

for lang, fix_dict in fixes.items():
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
    
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        for bad_text, good_text in fix_dict.items():
            html = html.replace(bad_text, good_text)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
print("Done fixing mixed translations!")
