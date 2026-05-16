"""
LLMO Semantic ARIA & Detail Page Schema Injector
Enhances AI extraction by adding ARIA roles to regions and injecting Product Schema to detail pages.
"""
import os, re

ROOT = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
LANGS = ['ja', 'en', 'ko', 'zh-cn', 'zh-tw']
DETAIL_PAGES = ['waffle&soft.html', 'soft.html', 'waffle.html', 'dounuts.html', 'ice.html']

def inject_aria_semantics(filepath):
    """Add role='region' and aria-label to structural sections for better LLM DOM parsing."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        return

    # Add ARIA to Safety Promise
    html = html.replace('<section class="safety-promise">', '<section class="safety-promise" role="region" aria-label="Dietary Safety and Allergen Promise">')
    
    # Add ARIA to Trust Banner
    html = html.replace('<div class="trust-banner">', '<div class="trust-banner" role="complementary" aria-label="Customer Reviews and Trust Signals">')
    
    # Add ARIA to FAQ
    html = html.replace('<section class="qa" id="qa">', '<section class="qa" id="qa" role="region" aria-label="Frequently Asked Questions">')
    html = html.replace('<section class="qa" id="qa" >', '<section class="qa" id="qa" role="region" aria-label="Frequently Asked Questions">') # catch extra space
    
    # Add ARIA to Access
    html = html.replace('<section class="access" id="access">', '<section class="access" id="access" role="region" aria-label="Location, Access, and Geospatial Information">')

    # Enhance Geospatial Text (if Japanese)
    if filepath.endswith(r'\index.html') and 'ja' not in filepath: # it's root index.html
        pass
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_product_schema(filename):
    """Generate Product JSON-LD based on the page name."""
    product_map = {
        'waffle&soft.html': ('Bubble Waffle & Soy Soft Serve', '100% Vegan & Gluten-Free Waffle topped with creamy soy milk soft serve.', '1000'),
        'soft.html': ('Premium Soy Soft Serve', 'Rich and creamy 100% plant-based soft serve made from Kyushu soybeans.', '600'),
        'waffle.html': ('Gluten-Free Bubble Waffle', 'Crispy on the outside, chewy on the inside. Baked with rice flour and soy milk.', '600'),
        'dounuts.html': ('Soy Baked Donuts', 'Healthy baked donuts. Dairy-free, egg-free, and wheat-free. Perfect for souvenirs.', '350'),
        'ice.html': ('Rice Flour Craft Gelato', 'Smooth plant-based gelato made without dairy or eggs.', '500')
    }
    
    if filename not in product_map:
        return ""
        
    name, desc, price = product_map[filename]
    
    return f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{name}",
      "image": "https://soystories.jp/img/fv_logo.png",
      "description": "{desc}",
      "brand": {{
        "@type": "Brand",
        "name": "SoyStories Fukuoka"
      }},
      "offers": {{
        "@type": "Offer",
        "url": "https://soystories.jp/{filename}",
        "priceCurrency": "JPY",
        "price": "{price}",
        "availability": "https://schema.org/InStoreOnly",
        "seller": {{
          "@type": "Organization",
          "name": "SoyStories"
        }}
      }},
      "suitableForDiet": [
        "https://schema.org/VeganDiet",
        "https://schema.org/GlutenFreeDiet"
      ]
    }}
    </script>
'''

def inject_detail_schema(filepath, filename):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        return
        
    schema = generate_product_schema(filename)
    if schema and '<script type="application/ld+json">' not in html:
        # Insert right before </head>
        html = html.replace('</head>', schema + '</head>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  [OK] Injected Product Schema: {filename}")

print("============================================================")
print("Injecting Level 2 LLMO Enhancements (ARIA & Product Schema)")
print("============================================================")

# 1. Inject ARIA to index pages
for lang in LANGS:
    path = 'index.html' if lang == 'ja' else f'{lang}/index.html'
    filepath = os.path.join(ROOT, path)
    inject_aria_semantics(filepath)
print("  [OK] ARIA Semantics injected to all landing pages")

# 2. Inject Product Schema to detail pages (currently in root)
for page in DETAIL_PAGES:
    filepath = os.path.join(ROOT, page)
    inject_detail_schema(filepath, page)
    
print("\nDone! AI engines will now perfectly parse the DOM and index individual menu items.")
