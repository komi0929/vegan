import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# Since we translated partial matches, we have some weird left-over strings.
fixes = {
    'en': {
        '濃厚焙煎Black sesameグレーズソース': 'Rich roasted black sesame glaze source',
        '香味豊かな八女Matchaドーナツに、<br>あんこをトッピングした和ドーナツ': 'A Japanese donut with fragrant Yame matcha dough,<br>topped with red bean paste',
        'Plainフレイバーの<br class="phonebr">ドーナツに<br class="pcbr">甘酸っぱい<br class="phonebr">Cranberryをトッピング': 'Plain flavored<br class="phonebr">donut<br class="pcbr">topped with<br class="phonebr">sweet and sour cranberries',
        '国産Black sesameを１００％<br class="phonebr">使用した、<br class="pcbr">プチプチとした<br class="phonebr">食感が楽しい和ドーナツ': 'Uses 100% domestic black sesame.<br class="phonebr">A Japanese-style donut<br class="pcbr">with a fun,<br class="phonebr">crunchy texture',
        '香味豊かな石臼引きのMatchaを<br class="phonebr">使用した、<br class="pcbr">香料、着色料不使用の<br class="phonebr">本格派Matchaスイーツ': 'Made with fragrant stone-milled matcha.<br class="phonebr">An authentic matcha sweet<br class="pcbr">made without<br class="phonebr">artificial flavors or colors',
        'もちもちドーナツにRoasted Soy Flourを<br class="phonebr">たっぷりかけた、<br class="pcbr">お子様、<br class="phonebr">女性に大人気の和ドーナツ': 'Chewy donut generously coated<br class="phonebr">with roasted soy flour.<br class="pcbr">A very popular Japanese donut<br class="phonebr">among women and children',
        'ベルガモットが香る<br class="phonebr">Earl Greyの紅茶を<br class="phonebr">練り込んだ、大人のドーナッツ': 'An adult donut<br class="phonebr">kneaded with Earl Grey tea<br class="phonebr">fragrant with bergamot',
        '子供から大人まで<br class="phonebr">幅広く愛される、<br class="pcbr">ビターな<br class="phonebr">甘さのチョコレートドーナツ': 'Loved by everyone from children to adults,<br class="phonebr">a chocolate donut<br class="pcbr">with a slightly bitter<br class="phonebr">sweetness',
        '温めるとAmaou Framboiseの香りが<br class="phonebr">いっぱい広がる<br>人気ナンバーワンドーナツ': 'When warmed, the scent of Amaou strawberries<br class="phonebr">spreads fully.<br>Our most popular donut',
        'イタリアBABBI社の<br class="phonebr">100％ピスタチオ<br class="pcbr">ペーストを<br class="phonebr">贅沢に使用': 'Luxuriously uses<br class="phonebr">100% pistachio<br class="pcbr">paste from<br class="phonebr">Italy\'s BABBI',
        'ベルガモット香るEarl Grey<br class="phonebr">生地に<br class="pcbr">有機無農薬Lemonグレーズを<br class="phonebr">トッピング': 'Earl Grey dough<br class="phonebr">fragrant with bergamot<br class="pcbr">topped with organic,<br class="phonebr">pesticide-free lemon glaze',
        'Roasted Soy Flourドーナツにグレーズ<br class="phonebr">ソースをたっぷり。<br class="pcbr">さらに甘さ<br class="phonebr">控えめの小豆をトッピング': 'Kinako donut generously topped with glaze.<br class="phonebr"><br class="pcbr">Further topped with<br class="phonebr">mildly sweet red beans',
        '国産Black sesameをじっくりと<br class="phonebr">皮ごと練り上げた<br>濃厚焙煎Black sesameグレーズソース': 'A rich roasted black sesame glaze source<br class="phonebr">made by carefully kneading<br>domestic black sesame whole with skin',
        'ビターな甘さの自家製クーベル<br class="phonebr">チュールチョコレートを<br class="phonebr">Chocolatドーナツにトッピング': 'Homemade couverture chocolate<br class="phonebr">with a bitter sweetness<br class="phonebr">topped on a chocolat donut',
        'いちごの優しい香りと甘み<br>見た目も可愛いいので、<br class="phonebr">お持たせにもおすすめです！': 'Gentle scent and sweetness of strawberries.<br>It looks cute too,<br class="phonebr">so it is highly recommended as a gift!',
        'ホロ苦いMatchaと、<br class="phonebr">甘い生地がぴったり<br>お子様も食べやすいお味です': 'The slightly bitter matcha and<br class="phonebr">sweet dough are a perfect match.<br>A flavor that is easy for children to eat',
        'チョコ好きさん大満足！<br>とにかく甘いものが食べたいときに<br>お子様も大好きな味': 'Highly satisfying for chocolate lovers!<br>When you just want to eat something sweet.<br>A flavor that children also love',
        'Lemonの爽やかな香りと甘さ<br>さっぱりとした甘さを楽しめます': 'Refreshing scent and sweetness of lemon.<br>You can enjoy a refreshing sweetness',
        '上にはチョコチップのトッピング<br>チョコミン党はぜひ！': 'Topped with chocolate chips on top.<br>A must-try for chocolate mint lovers!',
        'Coconutの優しい香りと甘さが<br>しっとり生地にぴったり<br>コーヒーと一緒に': 'The gentle scent and sweetness of coconut<br>is perfect for the moist dough.<br>Enjoy with coffee',
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
            
print("Done fixing English mixed translations!")
