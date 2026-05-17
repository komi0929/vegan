import os

filepath = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\css\inbound.css"
with open(filepath, 'r', encoding='utf-8') as f:
    css = f.read()

# Add z-index to trust-banner and hero-cta to prevent overlap from fv__inner
if 'z-index: 20;' not in css:
    css = css.replace('.trust-banner {', '.trust-banner {\n  z-index: 20;\n  position: relative;')
    css = css.replace('.hero-cta {', '.hero-cta {\n  position: relative;\n  z-index: 20;')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated inbound.css")
