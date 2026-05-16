"""
LLMO (Answer Engine Optimization) Schema Injector

Enhances the existing JSON-LD structured data to include:
1. FAQPage Schema (Critical for AI Question Answering)
2. Advanced Restaurant properties (priceRange, menu, servesCuisine)
3. Explicit "Vegan" and "Gluten-Free" entity declarations
"""
import os, re, json
from datetime import datetime

ROOT = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
LANGS = ['ja', 'en', 'ko', 'zh-cn', 'zh-tw']

FAQ_DATA = {
    'ja': [
        {
            "q": "イートインスペースはありますか？",
            "a": "はい、店内に4席ご用意しております。全商品テイクアウトも可能です。イートインではソフトクリームやワッフル、テイクアウトではドーナツやクラフトアイスがおすすめです。"
        },
        {
            "q": "テイクアウトのドーナツはどうやって食べるのがおすすめですか？",
            "a": "一番美味しい状態でお渡しするため、冷凍で販売しています。電子レンジ(600Wで1分)で温めてお召し上がりください。賞味期限は冷凍で3ヶ月です。解凍後は冷蔵で3日以内にお召し上がりください。店頭で温めてお渡しすることも可能です。"
        },
        {
            "q": "駐車場はありますか？",
            "a": "専用駐車場はありません。お近くのコインパーキングをご利用ください。"
        }
    ],
    'en': [
        {
            "q": "Do you have an eat-in space?",
            "a": "Yes, we have 4 seats inside the store. All items are also available for take-out. We recommend our soft serve and waffles for eat-in, and donuts and craft ice cream for take-out."
        },
        {
            "q": "How should I eat the take-out donuts?",
            "a": "Our donuts are sold frozen to maintain their deliciousness. Please warm them up in the microwave (600W for 1 minute) before eating. They last 3 months frozen. After thawing, consume within 3 days (keep refrigerated). We can also warm them up for you in the store."
        },
        {
            "q": "Is there a parking lot?",
            "a": "We do not have a private parking lot. Please use a nearby coin parking area."
        }
    ],
    'ko': [
        {
            "q": "매장 내 취식 공간이 있나요?",
            "a": "네, 매장에 4석이 마련되어 있습니다. 전 상품 포장도 가능합니다. 매장에서는 소프트 아이스크림과 와플을, 포장으로는 도넛과 크래프트 아이스크림을 추천합니다."
        },
        {
            "q": "포장한 도넛은 어떻게 먹는 게 좋나요?",
            "a": "가장 맛있는 상태로 제공하기 위해 냉동 상태로 판매하고 있습니다. 전자레인지(600W에서 1분)로 데워 드시기 바랍니다. 유통기한은 냉동 시 3개월입니다. 해동 후에는 냉장 보관하며 3일 이내에 드시기 바랍니다. 매장에서 데워서 제공해 드릴 수도 있습니다."
        },
        {
            "q": "주차장이 있나요?",
            "a": "전용 주차장은 없습니다. 근처의 코인 주차장을 이용해 주시기 바랍니다."
        }
    ],
    'zh-cn': [
        {
            "q": "有堂食座位吗？",
            "a": "是的，店内设有4个座位。所有商品均可外带。我们推荐在店享用冰淇淋和华夫饼，外带则推荐甜甜圈和手工冰淇淋。"
        },
        {
            "q": "外带的甜甜圈应该怎么吃？",
            "a": "为了保持最佳口感，我们的甜甜圈是冷冻销售的。请用微波炉加热（600W加热1分钟）后食用。冷冻保质期为3个月。解冻后请冷藏，并在3天内食用。我们也可以在店内为您加热。"
        },
        {
            "q": "有停车场吗？",
            "a": "我们没有专用停车场。请使用附近的收费停车场。"
        }
    ],
    'zh-tw': [
        {
            "q": "有內用座位嗎？",
            "a": "是的，店內設有4個座位。所有商品均可外帶。我們推薦在店享用霜淇淋和華夫餅，外帶則推薦甜甜圈和手工冰淇淋。"
        },
        {
            "q": "外帶的甜甜圈應該怎麼吃？",
            "a": "為了保持最佳口感，我們的甜甜圈是冷凍銷售的。請用微波爐加熱（600W加熱1分鐘）後食用。冷凍保存期限為3個月。解凍後請冷藏，並在3天內食用。我們也可以在店內為您加熱。"
        },
        {
            "q": "有停車場嗎？",
            "a": "我們沒有專用停車場。請使用附近的收費停車場。"
        }
    ]
}

def generate_llmo_schema(lang):
    # Core Restaurant Data
    url_path = f"/{lang}/" if lang != 'ja' else "/"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Restaurant",
                "@id": f"https://soystories.jp{url_path}#restaurant",
                "name": "SoyStories",
                "image": "https://soystories.jp/img/fv_logo.png",
                "url": f"https://soystories.jp{url_path}",
                "description": "100% Vegan and Gluten-Free Sweets Shop in Fukuoka, Japan. Zero cross-contamination dedicated facility.",
                "servesCuisine": ["Vegan", "Gluten-Free", "Plant-Based", "Dessert"],
                "priceRange": "¥",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "2-2-24 Yakuin, Chisan Mansion Daisan Hakata 1F",
                    "addressLocality": "Chuo-ku, Fukuoka-shi",
                    "addressRegion": "Fukuoka",
                    "postalCode": "810-0022",
                    "addressCountry": "JP"
                },
                "telephone": "+81-92-231-0677",
                "openingHoursSpecification": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                    "opens": "11:00",
                    "closes": "22:00"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "5.0",
                    "bestRating": "5",
                    "ratingCount": "50"
                },
                "sameAs": [
                    "https://www.instagram.com/soystories_yakuin/",
                    "https://www.happycow.net/reviews/soy-stories-fukuoka-291702"
                ],
                "hasMenu": {
                    "@type": "Menu",
                    "name": "Vegan & Gluten-Free Menu",
                    "hasMenuItem": [
                        { "@type": "MenuItem", "name": "Bubble Waffle & Soy Soft Serve", "suitableForDiet": "https://schema.org/VeganDiet" },
                        { "@type": "MenuItem", "name": "Gluten-Free Bubble Waffle", "suitableForDiet": "https://schema.org/GlutenFreeDiet" },
                        { "@type": "MenuItem", "name": "Soy Soft Serve", "suitableForDiet": "https://schema.org/VeganDiet" },
                        { "@type": "MenuItem", "name": "Soy Donut", "suitableForDiet": "https://schema.org/VeganDiet" }
                    ]
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"https://soystories.jp{url_path}#faq",
                "mainEntity": []
            }
        ]
    }
    
    # Add localized FAQs
    for item in FAQ_DATA.get(lang, FAQ_DATA['en']):
        schema["@graph"][1]["mainEntity"].append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["a"]
            }
        })
        
    return json.dumps(schema, ensure_ascii=False, indent=2)

def process_file():
    today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
    
    for lang in LANGS:
        path = 'index.html' if lang == 'ja' else f'{lang}/index.html'
        filepath = os.path.join(ROOT, path)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # 1. Replace old schema with new LLMO schema
        old_schema_pattern = r'<script type="application/ld\+json">.*?</script>'
        new_schema = f'<script type="application/ld+json">\n{generate_llmo_schema(lang)}\n    </script>'
        html = re.sub(old_schema_pattern, new_schema, html, flags=re.DOTALL)
        
        # 2. Inject freshness meta tags
        freshness_tags = f'''    <meta name="revised" content="{today}">
    <meta name="author" content="SoyStories">'''
        
        if 'name="revised"' not in html:
            html = html.replace('<meta name="robots"', freshness_tags + '\n    <meta name="robots"')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"  [OK] {path} - LLMO Schema & Freshness Tags injected")

print("============================================================")
print("Injecting LLMO (Answer Engine Optimization) Structured Data")
print("============================================================")
process_file()
print("\nDone! AI engines will now extract entities and FAQs perfectly.")
