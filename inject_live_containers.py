"""
Inject live-reviews and instagram-feed containers + live-content.js
into all language index pages.
Replaces the old static traveler-reviews section with a dynamic container.
"""
import os, re

ROOT = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
LANGS = ['en', 'ko', 'zh-cn', 'zh-tw']

LIVE_CONTAINER = '''    <!-- LIVE REVIEWS (dynamically populated by live-content.js) -->
    <section id="live-reviews"></section>
    <!-- INSTAGRAM FEED -->
    <section id="instagram-feed"></section>'''

for lang in LANGS:
    filepath = os.path.join(ROOT, lang, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add live-reviews container after the static traveler-reviews section
    #    (or after safety-promise if no traveler-reviews)
    if 'id="live-reviews"' not in html:
        # Insert before Q&A section
        for marker in ['<!-- Q&A -->', '<!-- Q&amp;A -->']:
            if marker in html:
                html = html.replace(marker, LIVE_CONTAINER + '\n    ' + marker)
                break

    # 2. Add live-content.js (after inbound.js)
    if 'live-content.js' not in html:
        html = html.replace(
            '<script src="../js/inbound.js"></script>',
            '<script src="../js/inbound.js"></script>\n    <script src="../js/live-content.js"></script>'
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  [OK] {lang}/index.html - live containers injected")

# Also update JP index (root)
jp_path = os.path.join(ROOT, 'index.html')
with open(jp_path, 'r', encoding='utf-8') as f:
    jp_html = f.read()

# Add inbound.css to JP
if 'inbound.css' not in jp_html:
    jp_html = jp_html.replace(
        '<link rel="stylesheet" href="./css/style.css">',
        '<link rel="stylesheet" href="./css/style.css">\n    <link rel="stylesheet" href="./css/inbound.css">'
    )

# Add live-reviews container to JP
if 'id="live-reviews"' not in jp_html:
    jp_live = LIVE_CONTAINER.replace('../data/', './data/')
    for marker in ['<!-- Q&A -->', '<!-- Q&amp;A -->']:
        if marker in jp_html:
            jp_html = jp_html.replace(marker, jp_live + '\n    ' + marker)
            break

# Add JS to JP
if 'inbound.js' not in jp_html:
    jp_html = jp_html.replace(
        '<script src="./js/script.js"></script>',
        '<script src="./js/script.js"></script>\n    <script src="./js/inbound.js"></script>'
    )
if 'live-content.js' not in jp_html:
    if 'inbound.js' in jp_html:
        jp_html = jp_html.replace(
            '<script src="./js/inbound.js"></script>',
            '<script src="./js/inbound.js"></script>\n    <script src="./js/live-content.js"></script>'
        )

with open(jp_path, 'w', encoding='utf-8') as f:
    f.write(jp_html)
print("  [OK] index.html (JP) - live containers injected")
print("\nDone! All pages now have live review containers.")
