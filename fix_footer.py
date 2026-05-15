import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['.', 'en', 'ko', 'zh-cn', 'zh-tw']
files_to_fix = ['dounuts.html', 'soft.html', 'waffle.html', 'ice.html', 'waffle&soft.html']

for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    index_path = os.path.join(lang_dir, "index.html")
    
    if not os.path.exists(index_path):
        continue
        
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Extract footer until </body>
    footer_match = re.search(r'<footer class="footer">.*?</body>', index_content, re.DOTALL)
    
    if not footer_match:
        print(f"Could not find footer in {index_path}")
        continue
        
    new_footer_to_body = footer_match.group(0)

    for filename in files_to_fix:
        filepath = os.path.join(lang_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace broken footer to end of file with new footer
        content = re.sub(r'<footer class="footer">.*', new_footer_to_body + '\n</html>\n', content, flags=re.DOTALL)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Fixed footer in {lang}/{filename}")
