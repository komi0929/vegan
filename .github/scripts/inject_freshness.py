import os
import re
from datetime import datetime, timezone, timedelta

# Japan Standard Time (JST) is UTC+9
jst = timezone(timedelta(hours=9))
current_time = datetime.now(jst).strftime('%Y-%m-%dT%H:%M:%S+09:00')

root_dir = "."

def update_freshness():
    updated_count = 0
    # Walk through all directories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(subdir, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to match the revised meta tag
                pattern = r'(<meta\s+name="revised"\s+content=")[^"]+(")'
                new_content = re.sub(pattern, rf'\g<1>{current_time}\g<2>', content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_count += 1
                    print(f"Updated freshness for: {filepath}")

    print(f"Total files updated: {updated_count}")

if __name__ == "__main__":
    update_freshness()
