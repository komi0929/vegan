import os
import urllib.request
import json
import urllib.parse

# Load .env file if it exists
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, val = line.partition("=")
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable is not set. Please set it or add it to a .env file (e.g., GOOGLE_API_KEY=your_key)")
    exit(1)
QUERY = "SoyStories 福岡 薬院"

url = f"https://places.googleapis.com/v1/places:searchText"
headers = {
    'X-Goog-Api-Key': API_KEY,
    'X-Goog-FieldMask': 'places.id,places.displayName',
    'Content-Type': 'application/json'
}
data = json.dumps({"textQuery": QUERY}).encode('utf-8')

try:
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result, indent=2))
except Exception as e:
    print(e)
