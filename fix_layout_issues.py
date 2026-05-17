import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

# 1. Fix .one-nav, .two-nav width in all style*.css
css_dir = os.path.join(root_dir, 'css')
for i in range(1, 6):
    style_file = os.path.join(css_dir, f'style{i}.css')
    if os.path.exists(style_file):
        with open(style_file, 'r', encoding='utf-8') as f:
            css = f.read()
        
        # Replace fixed width with flexible width
        css = re.sub(r'\.one-nav\s*,\s*\.two-nav\s*\{\s*width:\s*112px;', 
                     '.one-nav ,.two-nav {\n    min-width: 112px;\n    width: auto;\n    padding: 0 12px;', css)
        
        with open(style_file, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"Fixed navigation width in {style_file}")

# 2. Fix English hero text visibility in inbound.css
inbound_css_path = os.path.join(css_dir, 'inbound.css')
if os.path.exists(inbound_css_path):
    with open(inbound_css_path, 'r', encoding='utf-8') as f:
        inbound_css = f.read()

    # We need to replace the .fv__content--en rules
    # It was previously:
    # .fv__content--en {
    #   top: auto !important;
    #   bottom: -40px !important;
    #   width: 100%;
    #   display: flex !important;
    #   justify-content: center !important;
    #   gap: 0 !important;
    #   transform: translateX(-50%) !important;
    # }
    
    # We will redefine it to be static so it flows naturally, and add margin to clear the absolute logo.
    new_fv_css = '''
.fv__content--en {
  position: relative !important;
  top: auto !important;
  bottom: auto !important;
  left: auto !important;
  transform: none !important;
  width: 100%;
  display: flex !important;
  justify-content: center !important;
  gap: 0 !important;
  margin-top: 70px !important;
  z-index: 20 !important;
}

.fv__text-en {
  writing-mode: horizontal-tb !important;
  font-size: 16px !important;
  letter-spacing: 2px !important;
  text-align: center;
  color: #333;
  font-weight: 600;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px 24px;
  border-radius: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

@media(min-width: 768px) {
  .fv__content--en {
    margin-top: 130px !important;
  }
  .fv__text-en {
    font-size: 22px !important;
    letter-spacing: 4px !important;
    padding: 16px 36px;
  }
}
'''
    
    # Let's just append an override at the end of the file, which will take precedence.
    with open(inbound_css_path, 'a', encoding='utf-8') as f:
        f.write("\n/* --- FIX FOR HERO TEXT VISIBILITY --- */\n" + new_fv_css)
    print("Appended visibility fix to inbound.css")

