import os

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['en', 'ko', 'zh-tw', 'zh-cn']

# 1. Fix .../ to ../
for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
    
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        if '.../' in html:
            html = html.replace('.../', '../')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Fixed .../ in {filepath}")

# 2. Fix English hero text layout
en_index = os.path.join(root_dir, 'en', 'index.html')
if os.path.exists(en_index):
    with open(en_index, 'r', encoding='utf-8') as f:
        html = f.read()
        
    old_hero = '''        <div class="fv__content">
            <p class="fv__text-left" style="letter-spacing:0.1em; font-family:var(--ff-serif-en);">The Holy Land of</p>
            <p class="fv__text-right" style="letter-spacing:0.1em; font-family:var(--ff-serif-en);">Vegan Sweets in Japan</p>
        </div>'''
        
    new_hero = '''        <div class="fv__content fv__content--en">
            <p class="fv__text-en" style="font-family:var(--ff-serif-en);">The Holy Land of Vegan Sweets in Japan</p>
        </div>'''
        
    if old_hero in html:
        html = html.replace(old_hero, new_hero)
        with open(en_index, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Replaced English hero text in en/index.html")
    else:
        print("Could not find old hero text in en/index.html")

# 3. Append CSS to inbound.css
css_append = '''
/* ============================================
   ENGLISH HERO TEXT OVERRIDES
   ============================================ */
.fv__content--en {
  top: auto !important;
  bottom: -40px !important;
  width: 100%;
  display: flex !important;
  justify-content: center !important;
  gap: 0 !important;
  transform: translateX(-50%) !important;
}

.fv__text-en {
  writing-mode: horizontal-tb !important;
  font-size: 16px !important;
  letter-spacing: 2px !important;
  text-align: center;
  color: #333;
  font-weight: 600;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.8);
  padding: 8px 24px;
  border-radius: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

@media(min-width: 768px) {
  .fv__content--en {
    bottom: -60px !important;
  }
  .fv__text-en {
    font-size: 22px !important;
    letter-spacing: 4px !important;
    padding: 12px 36px;
  }
}
'''

inbound_css = os.path.join(root_dir, 'css', 'inbound.css')
if os.path.exists(inbound_css):
    with open(inbound_css, 'a', encoding='utf-8') as f:
        f.write(css_append)
    print("Appended CSS to inbound.css")
