import os
from bs4 import BeautifulSoup
import re

root_dir = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
langs = ['en', 'ko', 'zh-tw', 'zh-cn']

def contains_hiragana_katakana(text):
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text))

def is_mostly_english(text):
    cleaned = re.sub(r'[^a-zA-Z]', '', text)
    if len(cleaned) > 10:
        return True
    return False

allowed_en = ['Concept', 'Menu', 'Q&A', 'Access', 'SoyStories', 'Waffle', 'Soft Serve', 'Donut', 'rice flour gelato', 'OPEN NOW', 'Eat-in & Take-out available.', 'Signature Item', 'Eat-in', 'Take-out', 'Online Store', 'Visit Online Store', 'Gift wrapping', 'Our Commitment', 'Okara (Soy Pulp)', 'Rice Flour', 'Soy Milk', 'HappyCow', 'Instagram', 'Waffle Soft Serve']

results = []

for lang in langs:
    lang_dir = os.path.join(root_dir, lang)
    if not os.path.exists(lang_dir):
        continue
        
    results.append(f"\n--- Auditing Language: {lang} ---")
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        for script in soup(["script", "style"]):
            script.decompose()
            
        texts = soup.stripped_strings
        
        for text in texts:
            if text in allowed_en:
                continue
                
            # Special case to ignore pure English/Numbers/Punctuation in EN files
            
            if contains_hiragana_katakana(text):
                results.append(f"[{filename}] Found Japanese: {text}")
                
            if lang != 'en':
                if len(text) > 15 and re.match(r'^[a-zA-Z0-9\s.,!?\'"()-]+$', text):
                    results.append(f"[{filename}] Found English: {text}")

with open(os.path.join(root_dir, 'audit_results.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
