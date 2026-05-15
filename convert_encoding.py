import os

def check_and_convert(filepath):
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
            
        if raw.startswith(b'\xef\xbb\xbf'):
            # Already UTF-8 with BOM, or corrupted. Let's see if we can read it.
            return "UTF-8 BOM"
            
        try:
            # Try to decode as UTF-8
            raw.decode('utf-8')
            return "UTF-8"
        except UnicodeDecodeError:
            pass
            
        try:
            # Try to decode as Shift-JIS
            text = raw.decode('shift_jis')
            # If successful, rewrite as UTF-8
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            return "Converted from Shift-JIS"
        except UnicodeDecodeError:
            return "Unknown"
    except Exception as e:
        return str(e)

root = r"c:\Users\soyst\OneDrive\デスクトップ\vegan"
html_files = []
for path, subdirs, files in os.walk(root):
    for name in files:
        if name.endswith(".html"):
            html_files.append(os.path.join(path, name))

for f in html_files:
    print(f"{os.path.relpath(f, root)}: {check_and_convert(f)}")
