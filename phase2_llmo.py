import os
import json
from bs4 import BeautifulSoup

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

schema_data = {
    'waffle.html': {
        "name": "Bubble Waffle",
        "description": "Gluten-Free and Plant-Based Bubble Waffle",
        "image": "https://soystories.jp/img/waffle_plain.png",
        "price": "600",
        "url_suffix": "waffle.html"
    },
    'soft.html': {
        "name": "Rich Soy Soft Serve Ice Cream",
        "description": "100% Vegan and Gluten-Free Soy Soft Serve Ice Cream",
        "image": "https://soystories.jp/img/softcream_large.png",
        "price": "690",
        "url_suffix": "soft.html"
    },
    'waffle&soft.html': {
        "name": "Bubble Waffle & Soy Soft Serve",
        "description": "Freshly baked bubble waffle combined with rich soy soft serve. 100% Vegan and Gluten-Free.",
        "image": "https://soystories.jp/img/wafflesoft.png",
        "price": "980",
        "url_suffix": "waffle&soft.html"
    },
    'dounuts.html': {
        "name": "Baked Soy Donuts",
        "description": "Healthy baked donuts made with rich soy milk, okara, and rice flour. 100% vegan and gluten-free.",
        "image": "https://soystories.jp/img/donuts_lemon.png",
        "price": "430",
        "url_suffix": "dounuts.html"
    },
    'ice.html': {
        "name": "Rice Flour Gelato",
        "description": "Creamy and smooth gelato made with domestic rice flour. 100% plant-based.",
        "image": "https://soystories.jp/img/ice_berry-mix.png",
        "price": "490",
        "url_suffix": "ice.html"
    }
}

def inject_product_schema():
    for lang in ['en', 'ko', 'zh-tw', 'zh-cn', 'root']:
        if lang == 'root':
            lang_dir = root_dir
            prefix = ""
        else:
            lang_dir = os.path.join(root_dir, lang)
            prefix = f"{lang}/"
            
        if not os.path.exists(lang_dir):
            continue
            
        for filename, data in schema_data.items():
            filepath = os.path.join(lang_dir, filename)
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            # Remove any existing ld+json to prevent duplicates
            for script in soup.find_all('script', type='application/ld+json'):
                script.decompose()
                
            # Build new JSON-LD
            schema = {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": data['name'],
                "image": data['image'],
                "description": data['description'],
                "brand": {
                    "@type": "Brand",
                    "name": "SoyStories"
                },
                "offers": {
                    "@type": "Offer",
                    "url": f"https://soystories.jp/{prefix}{data['url_suffix']}",
                    "priceCurrency": "JPY",
                    "price": data['price'],
                    "availability": "https://schema.org/InStock"
                },
                "audience": {
                    "@type": "Audience",
                    "healthCondition": {
                        "@type": "MedicalCondition",
                        "name": ["Vegan", "Gluten-Free", "Plant-Based", "Dairy-Free", "Egg-Free", "Wheat-Free"]
                    }
                }
            }
            
            script_tag = soup.new_tag("script", type="application/ld+json")
            script_tag.string = "\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
            
            if soup.head:
                soup.head.append(script_tag)
                soup.head.append('\n')
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Injected Phase 2 Product Schema for: {lang}/{filename}")

inject_product_schema()
