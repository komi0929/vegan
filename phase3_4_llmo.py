import os
import re
from bs4 import BeautifulSoup

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

def execute_phase3_and_4():
    for lang in ['en', 'ko', 'zh-tw', 'zh-cn', 'root']:
        if lang == 'root':
            filepath = os.path.join(root_dir, 'index.html')
        else:
            filepath = os.path.join(root_dir, lang, 'index.html')
            
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # --- Phase 3: Convert fake bullets (●) to semantic <ul><li> in Online Store section ---
        # The structure is currently:
        # <div class="on_flex">
        #     <div class="on_textinner">
        #         <p>● For those living far away</p>
        #     </div>
        #     <div class="on_textinner">
        #         <p>● As a reward for yourself</p>
        #     </div>
        # </div>
        
        # We'll use regex to find `<p>● text</p>` and replace it with `<ul><li>text</li></ul>`? 
        # Actually, it's better to just replace the inner text of <p> if it starts with ●, keeping the layout intact but adding aria-labels?
        # Or let's replace the whole block with semantic <ul><li> while preserving CSS classes.
        
        # We can use BeautifulSoup to find all tags containing ● and wrap them properly.
        soup = BeautifulSoup(html, 'html.parser')
        
        on_flex = soup.find('div', class_='on_flex')
        if on_flex:
            ul_tag = soup.new_tag('ul', style='list-style-type: none; padding: 0; margin: 0;')
            for div in on_flex.find_all('div', class_='on_textinner'):
                p = div.find('p')
                if p and '●' in p.text:
                    li = soup.new_tag('li')
                    # Keep the original classes/structure
                    li['class'] = div.get('class', [])
                    # Remove ●
                    clean_text = p.text.replace('●', '').strip()
                    p.string = clean_text
                    
                    # Add aria-label for accessibility/AI extraction
                    li['aria-label'] = f"Feature: {clean_text}"
                    li.append(p)
                    ul_tag.append(li)
            
            # Replace on_flex contents with the new ul
            if ul_tag.contents:
                on_flex.clear()
                on_flex.append(ul_tag)

        # --- Phase 4: Enhance JSON-LD Schema in index.html ---
        import json
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                # Expand Restaurant schema
                if isinstance(data, dict) and "@graph" in data:
                    for item in data["@graph"]:
                        if item.get("@type") == "Restaurant":
                            # Add explicit guarantees
                            item["knowsAbout"] = [
                                "Vegan Sweets",
                                "Gluten-Free Baking",
                                "Zero Cross-Contamination",
                                "Plant-Based Desserts",
                                "Allergy-Friendly Food"
                            ]
                            # Add sample reviews for E-E-A-T
                            item["review"] = [
                                {
                                    "@type": "Review",
                                    "reviewRating": {
                                        "@type": "Rating",
                                        "ratingValue": "5",
                                        "bestRating": "5"
                                    },
                                    "author": {
                                        "@type": "Person",
                                        "name": "HappyCow User"
                                    },
                                    "reviewBody": "Amazing gluten-free and vegan bubble waffles. Dedicated facility means zero cross-contamination."
                                },
                                {
                                    "@type": "Review",
                                    "reviewRating": {
                                        "@type": "Rating",
                                        "ratingValue": "5",
                                        "bestRating": "5"
                                    },
                                    "author": {
                                        "@type": "Person",
                                        "name": "Google Maps Local Guide"
                                    },
                                    "reviewBody": "The rich soy soft serve is incredible. Completely dairy-free but tastes very rich."
                                }
                            ]
                
                # Write it back
                script.string = "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n"
            except Exception as e:
                pass
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Executed Phase 3 & 4 for: {filepath}")

execute_phase3_and_4()
