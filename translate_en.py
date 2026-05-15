import os
import re

en_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\en"
files_to_fix = ['dounuts.html', 'soft.html', 'waffle.html', 'ice.html', 'waffle&soft.html']

for filename in files_to_fix:
    filepath = os.path.join(en_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Localization fixes
    content = content.replace('円（税込）', ' JPY (Tax incl.)')
    content = content.replace('円', ' JPY')
    content = content.replace('価格', 'Price: ')
    content = content.replace('プレーン', 'Plain ')
    content = content.replace('その他', 'Others ')
    content = content.replace('含まれているアレルギー食品', 'Allergen Information')
    content = content.replace('大豆を使用しています', 'Contains Soy')
    content = content.replace('大豆', 'Soy')
    content = content.replace('アーモンド', 'Almond')
    content = content.replace('黒ごま', 'Black Sesame')
    content = content.replace('やまいも', 'Yam')
    content = content.replace('プレーンドーナツ', 'Plain Donuts')
    content = content.replace('グレーズドーナツ', 'Glazed Donuts')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Translated {filename}")
