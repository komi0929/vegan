import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

def inject_script():
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original = content
                
                # Check if the script tag actually exists
                if '<script src="' not in content or 'live-content.js' not in content.split('<script')[-1]:
                    # Make doubly sure
                    if not re.search(r'<script[^>]*src="[^"]*live-content\.js"[^>]*>', content):
                        # Determine correct path relative to root
                        if root == root_dir:
                            script_tag = '<script src="./js/live-content.js"></script>\n'
                        else:
                            script_tag = '<script src="../js/live-content.js"></script>\n'
                            
                        # Inject right before </body>
                        content = content.replace('</body>', script_tag + '</body>')
                    
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Injected live-content.js into: {filepath}")

inject_script()
