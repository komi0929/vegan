"""
Autonomous LLMO (AEO) Freshness Engine
This script runs automatically via GitHub Actions to continuously optimize the site for AI crawlers.
Tasks:
1. Update <meta name="revised"> tags across all pages to keep content "fresh" for recency-biased AI.
2. (Future) Can be expanded to auto-fetch Google Reviews API and write to data/reviews.json
"""
import os, re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def refresh_meta_tags():
    today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
    print(f"Refreshing LLMO Freshness Tags to: {today}")
    
    html_files = []
    for dirpath, _, filenames in os.walk(ROOT):
        # Ignore .git and node_modules
        if '.git' in dirpath or 'node_modules' in dirpath:
            continue
        for f in filenames:
            if f.endswith('.html'):
                html_files.append(os.path.join(dirpath, f))
                
    updated_count = 0
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find and replace the revised meta tag
        pattern = r'<meta name="revised" content="[^"]*">'
        new_tag = f'<meta name="revised" content="{today}">'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, new_tag, content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                
    print(f"Successfully refreshed freshness tags on {updated_count} pages.")

if __name__ == "__main__":
    print("Starting Autonomous LLMO Engine...")
    refresh_meta_tags()
    print("Done!")
