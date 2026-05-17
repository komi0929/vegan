import os
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"

def fix_errors():
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(('.html', '.js')):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original = content
            
            # 1. Fix HappyCow URL globally
            content = content.replace('soy-stories-fukuoka-291702', 'soy-stories-fukuoka-311234')
            
            # 2. Fix Japanese "Cross-Contamination" phrasing in index.html (and any others)
            # The original phrase: 専用施設による 交差汚染ゼロ の完全保証。安心してご来店ください。
            if '交差汚染ゼロ' in content:
                content = content.replace(
                    '専用施設による 交差汚染ゼロ の完全保証。安心してご来店ください。',
                    '専用工場による <strong>コンタミネーション（アレルゲン混入）ゼロ</strong> を完全保証。安心してお召し上がりください。'
                )
                # Catch variations where tags might be inside
                content = re.sub(
                    r'専用施設による\s*<strong>交差汚染ゼロ</strong>\s*の完全保証。安心してご来店ください。',
                    r'専用工場による <strong>コンタミネーション（アレルゲン混入）ゼロ</strong> を完全保証。安心してお召し上がりください。',
                    content
                )
                
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed errors in: {filepath}")

fix_errors()
