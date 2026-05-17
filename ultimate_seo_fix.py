import os
from bs4 import BeautifulSoup

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

og_images = {
    'index.html': 'https://soystories.jp/img/fv_logo.png',
    'waffle.html': 'https://soystories.jp/img/waffle_plain.png',
    'soft.html': 'https://soystories.jp/img/softcream_large.png',
    'waffle&soft.html': 'https://soystories.jp/img/wafflesoft.png',
    'dounuts.html': 'https://soystories.jp/img/donuts_lemon.png',
    'ice.html': 'https://soystories.jp/img/ice_berry-mix.png'
}

def execute_ultimate_seo_fix():
    for lang in ['en', 'ko', 'zh-tw', 'zh-cn', 'root']:
        if lang == 'root':
            lang_dir = root_dir
            url_prefix = "https://soystories.jp/"
        else:
            lang_dir = os.path.join(root_dir, lang)
            url_prefix = f"https://soystories.jp/{lang}/"
            
        if not os.path.exists(lang_dir):
            continue
            
        for filename in os.listdir(lang_dir):
            if not filename.endswith('.html'):
                continue
                
            filepath = os.path.join(lang_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            # 1. Update Canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if canonical:
                target_url = f"{url_prefix}{filename}" if filename != "index.html" else url_prefix
                canonical['href'] = target_url
                
            # 2. Update og:url
            og_url = soup.find('meta', attrs={'property': 'og:url'})
            if og_url:
                target_url = f"{url_prefix}{filename}" if filename != "index.html" else url_prefix
                og_url['content'] = target_url
                
            # 3. Update og:image
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image:
                image_url = og_images.get(filename, 'https://soystories.jp/img/fv_logo.png')
                og_image['content'] = image_url
                
            # 4. Add loading="lazy" to images (except those in header or fv)
            for img in soup.find_all('img'):
                # Skip header logo or FV images for LCP optimization
                parent_classes = []
                p = img.parent
                while p and p.name != 'body':
                    if p.get('class'):
                        parent_classes.extend(p.get('class'))
                    p = p.parent
                    
                if 'header' in parent_classes or 'fv__inner' in parent_classes or 'header__logo' in parent_classes:
                    continue
                    
                if not img.get('loading'):
                    img['loading'] = 'lazy'
                    
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Executed Ultimate SEO Fix for: {lang}/{filename}")

execute_ultimate_seo_fix()
