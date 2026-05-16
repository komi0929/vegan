import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# Target languages and their translation dictionaries for donuts
translations = {
    'en': {
        'プレーンドーナツ': 'Plain Donuts',
        'プレーンフレイバーの<br class="phonebr">ドーナツに<br class="pcbr">甘酸っぱい<br class="phonebr">クランベリーをトッピング': 'Plain flavored<br class="phonebr">donut<br class="pcbr">topped with<br class="phonebr">sweet and sour cranberries',
        '国産黒ごまを１００％<br class="phonebr">使用した、<br class="pcbr">プチプチとした<br class="phonebr">食感が楽しい和ドーナツ': 'Uses 100% domestic black sesame.<br class="phonebr">A Japanese-style donut<br class="pcbr">with a fun,<br class="phonebr">crunchy texture',
        '香味豊かな石臼引きの抹茶を<br class="phonebr">使用した、<br class="pcbr">香料、着色料不使用の<br class="phonebr">本格派抹茶スイーツ': 'Made with fragrant stone-milled matcha.<br class="phonebr">An authentic matcha sweet<br class="pcbr">made without<br class="phonebr">artificial flavors or colors',
        'もちもちドーナツにきなこを<br class="phonebr">たっぷりかけた、<br class="pcbr">お子様、<br class="phonebr">女性に大人気の和ドーナツ': 'Chewy donut generously coated<br class="phonebr">with roasted soy flour.<br class="pcbr">A very popular Japanese donut<br class="phonebr">among women and children',
        'ベルガモットが香る<br class="phonebr">アールグレイの紅茶を<br class="phonebr">練り込んだ、大人のドーナッツ': 'An adult donut<br class="phonebr">kneaded with Earl Grey tea<br class="phonebr">fragrant with bergamot',
        '子供から大人まで<br class="phonebr">幅広く愛される、<br class="pcbr">ビターな<br class="phonebr">甘さのチョコレートドーナツ': 'Loved by everyone from children to adults,<br class="phonebr">a chocolate donut<br class="pcbr">with a slightly bitter<br class="phonebr">sweetness',
        'グレーズドーナツ': 'Glazed Donuts',
        '温めるとあまおうの香りが<br class="phonebr">いっぱい広がる<br>人気ナンバーワンドーナツ': 'When warmed, the scent of Amaou strawberries<br class="phonebr">spreads fully.<br>Our most popular donut',
        'イタリアBABBI社の<br class="phonebr">100％ピスタチオ<br class="pcbr">ペーストを<br class="phonebr">贅沢に使用': 'Luxuriously uses<br class="phonebr">100% pistachio<br class="pcbr">paste from<br class="phonebr">Italy\'s BABBI',
        'ベルガモット香るアールグレイ<br class="phonebr">生地に<br class="pcbr">有機無農薬レモングレーズを<br class="phonebr">トッピング': 'Earl Grey dough<br class="phonebr">fragrant with bergamot<br class="pcbr">topped with organic,<br class="phonebr">pesticide-free lemon glaze',
        'きなこドーナツにグレーズ<br class="phonebr">ソースをたっぷり。<br class="pcbr">さらに甘さ<br class="phonebr">控えめの小豆をトッピング': 'Kinako donut generously topped with glaze.<br class="phonebr"><br class="pcbr">Further topped with<br class="phonebr">mildly sweet red beans',
        '国産黒ごまをじっくりと<br class="phonebr">皮ごと練り上げた<br>濃厚焙煎黒ごまグレーズソース': 'A rich roasted black sesame glaze source<br class="phonebr">made by carefully kneading<br>domestic black sesame whole with skin',
        'ビターな甘さの自家製クーベル<br class="phonebr">チュールチョコレートを<br class="phonebr">ショコラドーナツにトッピング': 'Homemade couverture chocolate<br class="phonebr">with a bitter sweetness<br class="phonebr">topped on a chocolat donut',
        '香味豊かな八女抹茶ドーナツに、<br>あんこをトッピングした和ドーナツ': 'A Japanese donut with fragrant Yame matcha dough,<br>topped with red bean paste',
        'ケーキドーナツ': 'Cake Donuts',
        'いちごの優しい香りと甘み<br>見た目も可愛いいので、<br class="phonebr">お持たせにもおすすめです！': 'Gentle scent and sweetness of strawberries.<br>It looks cute too,<br class="phonebr">so it is highly recommended as a gift!',
        'ホロ苦い抹茶と、<br class="phonebr">甘い生地がぴったり<br>お子様も食べやすいお味です': 'The slightly bitter matcha and<br class="phonebr">sweet dough are a perfect match.<br>A flavor that is easy for children to eat',
        'チョコ好きさん大満足！<br>とにかく甘いものが食べたいときに<br>お子様も大好きな味': 'Highly satisfying for chocolate lovers!<br>When you just want to eat something sweet.<br>A flavor that children also love',
        'レモンの爽やかな香りと甘さ<br>さっぱりとした甘さを楽しめます': 'Refreshing scent and sweetness of lemon.<br>You can enjoy a refreshing sweetness',
        '上にはチョコチップのトッピング<br>チョコミン党はぜひ！': 'Topped with chocolate chips on top.<br>A must-try for chocolate mint lovers!',
        'ココナッツの優しい香りと甘さが<br>しっとり生地にぴったり<br>コーヒーと一緒に': 'The gentle scent and sweetness of coconut<br>is perfect for the moist dough.<br>Enjoy with coffee',
        'クランベリー': 'Cranberry',
        '黒ごま': 'Black Sesame',
        '抹茶': 'Matcha',
        'きなこ': 'Roasted Soy Flour',
        'アールグレイ': 'Earl Grey',
        'ショコラ': 'Chocolat',
        'あまおうフランボワーズ': 'Amaou Framboise',
        'ピュアピスタチオ': 'Pure Pistachio',
        'レモンアールグレイ': 'Lemon Earl Grey',
        'きなこグレーズ': 'Kinako Glaze',
        '黒ごまグレーズ': 'Black Sesame Glaze',
        'クーベルチョコナッツ': 'Couverture Chocolate Nuts',
        'モリンガあんこ': 'Moringa Red Bean',
        'いちご': 'Strawberry',
        'ダブルチョコ': 'Double Chocolate',
        'レモン': 'Lemon',
        'チョコミント': 'Chocolate Mint',
        'ココナッツ': 'Coconut'
    },
    'ko': {
        'プレーンドーナツ': '플레인 도넛',
        'プレーンフレイバーの<br class="phonebr">ドーナツに<br class="pcbr">甘酸っぱい<br class="phonebr">クランベリーをトッピング': '플레인 맛의<br class="phonebr">도넛에<br class="pcbr">새콤달콤한<br class="phonebr">크랜베리 토핑',
        '国産黒ごまを１００％<br class="phonebr">使用した、<br class="pcbr">プチプチとした<br class="phonebr">食感が楽しい和ドーナツ': '국산 검은깨를 100%<br class="phonebr">사용한,<br class="pcbr">톡톡 터지는<br class="phonebr">식감이 즐거운 일본식 도넛',
        '香味豊かな石臼引きの抹茶を<br class="phonebr">使用した、<br class="pcbr">香料、着色料不使用の<br class="phonebr">本格派抹茶スイーツ': '향이 풍부한 맷돌 말차를<br class="phonebr">사용한,<br class="pcbr">향료 및 착색료 무첨가의<br class="phonebr">본격 말차 스위츠',
        'もちもちドーナツにきなこを<br class="phonebr">たっぷりかけた、<br class="pcbr">お子様、<br class="phonebr">女性に大人気の和ドーナツ': '쫄깃한 도넛에 콩가루를<br class="phonebr">듬뿍 뿌린,<br class="pcbr">어린이와<br class="phonebr">여성에게 인기 있는 일본식 도넛',
        'ベルガモットが香る<br class="phonebr">アールグレイの紅茶を<br class="phonebr">練り込んだ、大人のドーナッツ': '베르가못 향이 나는<br class="phonebr">얼그레이 홍차를<br class="phonebr">반죽한 어른의 도넛',
        '子供から大人まで<br class="phonebr">幅広く愛される、<br class="pcbr">ビターな<br class="phonebr">甘さのチョコレートドーナツ': '어린이부터 어른까지<br class="phonebr">폭넓게 사랑받는,<br class="pcbr">쌉쌀한<br class="phonebr">단맛의 초콜릿 도넛',
        'グレーズドーナツ': '글레이즈 도넛',
        '温めるとあまおうの香りが<br class="phonebr">いっぱい広がる<br>人気ナンバーワンドーナツ': '따뜻하게 데우면 아마오우 딸기 향이<br class="phonebr">가득 퍼지는<br>인기 넘버원 도넛',
        'イタリアBABBI社の<br class="phonebr">100％ピスタチオ<br class="pcbr">ペーストを<br class="phonebr">贅沢に使用': '이탈리아 BABBI사의<br class="phonebr">100% 피스타치오<br class="pcbr">페이스트를<br class="phonebr">아낌없이 사용',
        'ベルガモット香るアールグレイ<br class="phonebr">生地に<br class="pcbr">有機無農薬レモングレーズを<br class="phonebr">トッピング': '베르가못 향의 얼그레이<br class="phonebr">반죽에<br class="pcbr">유기농 무농약 레몬 글레이즈를<br class="phonebr">토핑',
        'きなこドーナツにグレーズ<br class="phonebr">ソースをたっぷり。<br class="pcbr">さらに甘さ<br class="phonebr">控えめの小豆をトッピング': '콩가루 도넛에 글레이즈<br class="phonebr">소스를 듬뿍.<br class="pcbr">여기에 단맛을<br class="phonebr">줄인 팥을 토핑',
        '国産黒ごまをじっくりと<br class="phonebr">皮ごと練り上げた<br>濃厚焙煎黒ごまグレーズソース': '국산 검은깨를 정성껏<br class="phonebr">껍질째 갈아 만든<br>진한 로스팅 검은깨 글레이즈 소스',
        'ビターな甘さの自家製クーベル<br class="phonebr">チュールチョコレートを<br class="phonebr">ショコラドーナツにトッピング': '쌉쌀한 단맛의 수제 쿠베르<br class="phonebr">튀르 초콜릿을<br class="phonebr">쇼콜라 도넛에 토핑',
        '香味豊かな八女抹茶ドーナツに、<br>あんこをトッピングした和ドーナツ': '향이 풍부한 야메 말차 도넛에,<br>팥을 토핑한 일본식 도넛',
        'ケーキドーナツ': '케이크 도넛',
        'いちごの優しい香りと甘み<br>見た目も可愛いいので、<br class="phonebr">お持たせにもおすすめです！': '딸기의 부드러운 향과 단맛<br>모양도 귀여워서,<br class="phonebr">선물용으로도 추천합니다!',
        'ホロ苦い抹茶と、<br class="phonebr">甘い生地がぴったり<br>お子様も食べやすいお味です': '쌉싸름한 말차와,<br class="phonebr">달콤한 반죽이 찰떡궁합<br>어린이도 먹기 좋은 맛입니다',
        'チョコ好きさん大満足！<br>とにかく甘いものが食べたいときに<br>お子様も大好きな味': '초코 마니아 대만족!<br>어쨌든 단 것이 먹고 싶을 때<br>어린이도 아주 좋아하는 맛',
        'レモンの爽やかな香りと甘さ<br>さっぱりとした甘さを楽しめます': '레몬의 상쾌한 향과 단맛<br>깔끔한 단맛을 즐길 수 있습니다',
        '上にはチョコチップのトッピング<br>チョコミン党はぜひ！': '위에는 초코칩 토핑<br>민트 초코파는 꼭 드셔보세요!',
        'ココナッツの優しい香りと甘さが<br>しっとり生地にぴったり<br>コーヒーと一緒に': '코코넛의 부드러운 향과 단맛이<br>촉촉한 반죽에 딱<br>커피와 함께 즐기세요',
        'クランベリー': '크랜베리',
        '黒ごま': '검은깨',
        '抹茶': '말차',
        'きなこ': '콩가루',
        'アールグレイ': '얼그레이',
        'ショコラ': '쇼콜라',
        'あまおうフランボワーズ': '아마오우 프랑부아즈',
        'ピュアピスタチオ': '퓨어 피스타치오',
        'レモンアールグレイ': '레몬 얼그레이',
        'きなこグレーズ': '콩가루 글레이즈',
        '黒ごまグレーズ': '검은깨 글레이즈',
        'クーベルチョコナッツ': '쿠베르 초코 너츠',
        'モリンガあんこ': '모링가 팥',
        'いちご': '딸기',
        'ダブルチョコ': '더블 초코',
        'レモン': '레몬',
        'チョコミント': '초코 민트',
        'ココナッツ': '코코넛'
    },
    'zh-cn': {
        'プレーンドーナツ': '原味甜甜圈',
        'プレーンフレイバーの<br class="phonebr">ドーナツに<br class="pcbr">甘酸っぱい<br class="phonebr">クランベリーをトッピング': '原味甜甜圈<br class="phonebr">配上<br class="pcbr">酸甜可口的<br class="phonebr">蔓越莓点缀',
        '国産黒ごまを１００％<br class="phonebr">使用した、<br class="pcbr">プチプチとした<br class="phonebr">食感が楽しい和ドーナツ': '使用100%日本国产黑芝麻，<br class="phonebr">口感<br class="pcbr">层次分明，<br class="phonebr">充满趣味的日式甜甜圈',
        '香味豊かな石臼引きの抹茶を<br class="phonebr">使用した、<br class="pcbr">香料、着色料不使用の<br class="phonebr">本格派抹茶スイーツ': '使用香气四溢的石磨抹茶，<br class="phonebr">不含<br class="pcbr">香料和色素的<br class="phonebr">正宗抹茶甜点',
        'もちもちドーナツにきなこを<br class="phonebr">たっぷりかけた、<br class="pcbr">お子様、<br class="phonebr">女性に大人気の和ドーナツ': '软糯的甜甜圈撒上<br class="phonebr">大量黄豆粉，<br class="pcbr">深受儿童<br class="phonebr">和女性喜爱的日式甜甜圈',
        'ベルガモットが香る<br class="phonebr">アールグレイの紅茶を<br class="phonebr">練り込んだ、大人のドーナッツ': '揉入散发佛手柑香气的<br class="phonebr">伯爵红茶的<br class="phonebr">成熟风味甜甜圈',
        '子供から大人まで<br class="phonebr">幅広く愛される、<br class="pcbr">ビターな<br class="phonebr">甘さのチョコレートドーナツ': '从儿童到成人<br class="phonebr">都广泛喜爱的，<br class="pcbr">带有微苦<br class="phonebr">甜味的巧克力甜甜圈',
        'グレーズドーナツ': '糖霜甜甜圈',
        '温めるとあまおうの香りが<br class="phonebr">いっぱい広がる<br>人気ナンバーワンドーナツ': '加热后甘王草莓的香气<br class="phonebr">会完全散发出来<br>人气第一的甜甜圈',
        'イタリアBABBI社の<br class="phonebr">100％ピスタチオ<br class="pcbr">ペーストを<br class="phonebr">贅沢に使用': '奢侈地使用<br class="phonebr">意大利BABBI公司的<br class="pcbr">100%开心果<br class="phonebr">酱',
        'ベルガモット香るアールグレイ<br class="phonebr">生地に<br class="pcbr">有機無農薬レモングレーズを<br class="phonebr">トッピング': '在散发佛手柑香气的伯爵茶<br class="phonebr">面团上<br class="pcbr">点缀有机无农药柠檬糖霜<br class="phonebr">',
        'きなこドーナツにグレーズ<br class="phonebr">ソースをたっぷり。<br class="pcbr">さらに甘さ<br class="phonebr">控えめの小豆をトッピング': '黄豆粉甜甜圈淋上充足的糖霜<br class="phonebr">。<br class="pcbr">再配上甜度<br class="phonebr">适中的红豆点缀',
        '国産黒ごまをじっくりと<br class="phonebr">皮ごと練り上げた<br>濃厚焙煎黒ごまグレーズソース': '将日本国产黑芝麻带皮<br class="phonebr">精心揉制而成的<br>浓郁烘焙黑芝麻糖霜',
        'ビターな甘さの自家製クーベル<br class="phonebr">チュールチョコレートを<br class="phonebr">ショコラドーナツにトッピング': '将带有微苦甜味的自制调温<br class="phonebr">巧克力<br class="phonebr">点缀在巧克力甜甜圈上',
        '香味豊かな八女抹茶ドーナツに、<br>あんこをトッピングした和ドーナツ': '在香气四溢的八女抹茶甜甜圈上，<br>点缀红豆泥的日式甜甜圈',
        'ケーキドーナツ': '蛋糕甜甜圈',
        'いちごの優しい香りと甘み<br>見た目も可愛いいので、<br class="phonebr">お持たせにもおすすめです！': '草莓柔和的香气和甜味<br>外观也非常可爱，<br class="phonebr">作为伴手礼也很推荐！',
        'ホロ苦い抹茶と、<br class="phonebr">甘い生地がぴったり<br>お子様も食べやすいお味です': '微苦的抹茶与<br class="phonebr">香甜的面团完美契合<br>儿童也很容易接受的口味',
        'チョコ好きさん大満足！<br>とにかく甘いものが食べたいときに<br>お子様も大好きな味': '巧克力爱好者大满足！<br>无论如何想吃甜食的时候<br>儿童也非常喜欢的味道',
        'レモンの爽やかな香りと甘さ<br>さっぱりとした甘さを楽しめます': '柠檬清爽的香气和甜味<br>可以享受清爽的甜度',
        '上にはチョコチップのトッピング<br>チョコミン党はぜひ！': '上面点缀有巧克力片<br>薄荷巧克力爱好者一定要尝试！',
        'ココナッツの優しい香りと甘さが<br>しっとり生地にぴったり<br>コーヒーと一緒に': '椰子柔和的香气和甜味<br>与湿润的面团完美契合<br>适合搭配咖啡',
        'クランベリー': '蔓越莓',
        '黒ごま': '黑芝麻',
        '抹茶': '抹茶',
        'きなこ': '黄豆粉',
        'アールグレイ': '伯爵红茶',
        'ショコラ': '巧克力',
        'あまおうフランボワーズ': '甘王覆盆子',
        'ピュアピスタチオ': '纯正开心果',
        'レモンアールグレイ': '柠檬伯爵茶',
        'きなこグレーズ': '黄豆粉糖霜',
        '黒ごまグレーズ': '黑芝麻糖霜',
        'クーベルチョコナッツ': '调温巧克力坚果',
        'モリンガあんこ': '辣木红豆',
        'いちご': '草莓',
        'ダブルチョコ': '双重巧克力',
        'レモン': '柠檬',
        'チョコミント': '薄荷巧克力',
        'ココナッツ': '椰子'
    },
    'zh-tw': {
        'プレーンドーナツ': '原味甜甜圈',
        'プレーンフレイバーの<br class="phonebr">ドーナツに<br class="pcbr">甘酸っぱい<br class="phonebr">クランベリーをトッピング': '原味甜甜圈<br class="phonebr">配上<br class="pcbr">酸甜可口的<br class="phonebr">蔓越莓點綴',
        '国産黒ごまを１００％<br class="phonebr">使用した、<br class="pcbr">プチプチとした<br class="phonebr">食感が楽しい和ドーナツ': '使用100%日本國產黑芝麻，<br class="phonebr">口感<br class="pcbr">層次分明，<br class="phonebr">充滿趣味的日式甜甜圈',
        '香味豊かな石臼引きの抹茶を<br class="phonebr">使用した、<br class="pcbr">香料、着色料不使用の<br class="phonebr">本格派抹茶スイーツ': '使用香氣四溢的石磨抹茶，<br class="phonebr">不含<br class="pcbr">香料和色素的<br class="phonebr">正宗抹茶甜點',
        'もちもちドーナツにきなこを<br class="phonebr">たっぷりかけた、<br class="pcbr">お子様、<br class="phonebr">女性に大人気の和ドーナツ': '軟糯的甜甜圈撒上<br class="phonebr">大量黃豆粉，<br class="pcbr">深受兒童<br class="phonebr">和女性喜愛的日式甜甜圈',
        'ベルガモットが香る<br class="phonebr">アールグレイの紅茶を<br class="phonebr">練り込んだ、大人のドーナッツ': '揉入散發佛手柑香氣的<br class="phonebr">伯爵紅茶的<br class="phonebr">成熟風味甜甜圈',
        '子供から大人まで<br class="phonebr">幅広く愛される、<br class="pcbr">ビターな<br class="phonebr">甘さのチョコレートドーナツ': '從兒童到成人都<br class="phonebr">廣泛喜愛的，<br class="pcbr">帶有微苦<br class="phonebr">甜味的巧克力甜甜圈',
        'グレーズドーナツ': '糖霜甜甜圈',
        '温めるとあまおうの香りが<br class="phonebr">いっぱい広がる<br>人気ナンバーワンドーナツ': '加熱後甘王草莓的香氣<br class="phonebr">會完全散發出來<br>人氣第一的甜甜圈',
        'イタリアBABBI社の<br class="phonebr">100％ピスタチオ<br class="pcbr">ペーストを<br class="phonebr">贅沢に使用': '奢侈地使用<br class="phonebr">義大利BABBI公司的<br class="pcbr">100%開心果<br class="phonebr">醬',
        'ベルガモット香るアールグレイ<br class="phonebr">生地に<br class="pcbr">有機無農薬レモングレーズを<br class="phonebr">トッピング': '在散發佛手柑香氣的伯爵茶<br class="phonebr">麵團上<br class="pcbr">點綴有機無農藥檸檬糖霜<br class="phonebr">',
        'きなこドーナツにグレーズ<br class="phonebr">ソースをたっぷり。<br class="pcbr">さらに甘さ<br class="phonebr">控えめの小豆をトッピング': '黃豆粉甜甜圈淋上充足的糖霜<br class="phonebr">。<br class="pcbr">再配上甜度<br class="phonebr">適中的紅豆點綴',
        '国産黒ごまをじっくりと<br class="phonebr">皮ごと練り上げた<br>濃厚焙煎黒ごまグレーズソース': '將日本國產黑芝麻帶皮<br class="phonebr">精心揉製而成的<br>濃郁烘焙黑芝麻糖霜',
        'ビターな甘さの自家製クーベル<br class="phonebr">チュールチョコレートを<br class="phonebr">ショコラドーナツにトッピング': '將帶有微苦甜味的自製調溫<br class="phonebr">巧克力<br class="phonebr">點綴在巧克力甜甜圈上',
        '香味豊かな八女抹茶ドーナツに、<br>あんこをトッピングした和ドーナツ': '在香氣四溢的八女抹茶甜甜圈上，<br>點綴紅豆泥的日式甜甜圈',
        'ケーキドーナツ': '蛋糕甜甜圈',
        'いちごの優しい香りと甘み<br>見た目も可愛いいので、<br class="phonebr">お持たせにもおすすめです！': '草莓柔和的香氣和甜味<br>外觀也非常可愛，<br class="phonebr">作為伴手禮也很推薦！',
        'ホロ苦い抹茶と、<br class="phonebr">甘い生地がぴったり<br>お子様も食べやすいお味です': '微苦的抹茶與<br class="phonebr">香甜的麵團完美契合<br>兒童也很容易接受的口味',
        'チョコ好きさん大満足！<br>とにかく甘いものが食べたいときに<br>お子様も大好きな味': '巧克力愛好者大滿足！<br>無論如何想吃甜食的時候<br>兒童也非常喜歡的味道',
        'レモンの爽やかな香りと甘さ<br>さっぱりとした甘さを楽しめます': '檸檬清爽的香氣和甜味<br>可以享受清爽的甜度',
        '上にはチョコチップのトッピング<br>チョコミン党はぜひ！': '上面點綴有巧克力片<br>薄荷巧克力愛好者一定要嘗試！',
        'ココナッツの優しい香りと甘さが<br>しっとり生地にぴったり<br>コーヒーと一緒に': '椰子柔和的香氣和甜味<br>與濕潤的麵團完美契合<br>適合搭配咖啡',
        'クランベリー': '蔓越莓',
        '黒ごま': '黑芝麻',
        '抹茶': '抹茶',
        'きなこ': '黃豆粉',
        'アールグレイ': '伯爵紅茶',
        'ショコラ': '巧克力',
        'あまおうフランボワーズ': '甘王覆盆子',
        'ピュアピスタチオ': '純正開心果',
        'レモンアールグレイ': '檸檬伯爵茶',
        'きなこグレーズ': '黃豆粉糖霜',
        '黒ごまグレーズ': '黑芝麻糖霜',
        'クーベルチョコナッツ': '調溫巧克力堅果',
        'モリンガあんこ': '辣木紅豆',
        'いちご': '草莓',
        'ダブルチョコ': '雙重巧克力',
        'レモン': '檸檬',
        'チョコミント': '薄荷巧克力',
        'ココナッツ': '椰子'
    }
}

for lang, translation_dict in translations.items():
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
    
    # Process all HTML files in the lang directory
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Apply translations
        # Sort keys by length descending to prevent partial replacements
        for jp_text in sorted(translation_dict.keys(), key=len, reverse=True):
            html = html.replace(jp_text, translation_dict[jp_text])
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
print("Done translating all missing donut text across all files!")
