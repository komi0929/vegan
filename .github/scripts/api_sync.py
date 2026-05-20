import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------
# CONFIGURATION & SECRETS
# ---------------------------------------------------------
# These are pulled from GitHub Actions Secrets
GOOGLE_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
GOOGLE_PLACE_ID = os.environ.get('GOOGLE_PLACE_ID')
INSTAGRAM_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN')

# File paths (relative to repo root)
REVIEWS_JSON_PATH = 'data/reviews.json'
INSTAGRAM_JSON_PATH = 'data/instagram.json'

def fetch_google_reviews():
    if not GOOGLE_API_KEY or not GOOGLE_PLACE_ID:
        print("Skipping Google Reviews: API Key or Place ID not provided.")
        return False
        
    print("Fetching Google Reviews...")
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=name,rating,user_ratings_total,reviews&key={GOOGLE_API_KEY}&language=en"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data.get('status') != 'OK':
            print(f"Google API Error: {data.get('status')}")
            return False
            
        result = data.get('result', {})
        reviews = result.get('reviews', [])
        
        # Format for our frontend
        formatted_reviews = []
        for r in reviews:
            # Only include 4 and 5 star reviews for the website
            if r.get('rating', 0) >= 4:
                formatted_reviews.append({
                    "id": f"g-{r.get('time')}",
                    "source": "Google",
                    "author": r.get('author_name'),
                    "rating": r.get('rating'),
                    "date": datetime.fromtimestamp(r.get('time')).strftime('%Y-%m-%d'),
                    "text": {
                        "en": r.get('text'),
                        "ko": "", # Optional: Can integrate DeepL API here later
                        "zh-cn": "",
                        "zh-tw": ""
                    },
                    "photoUrl": r.get('profile_photo_url')
                })
        
        # Load existing reviews to keep HappyCow/manual structure intact, just update Google part
        existing_data = {}
        if os.path.exists(REVIEWS_JSON_PATH):
            with open(REVIEWS_JSON_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                
        # Update fields
        existing_data['lastUpdated'] = datetime.now(timezone.utc).isoformat()
        if 'sources' not in existing_data:
            existing_data['sources'] = {}
        if 'google' not in existing_data['sources']:
            existing_data['sources']['google'] = {}
            
        existing_data['sources']['google']['rating'] = result.get('rating')
        existing_data['sources']['google']['reviewCount'] = result.get('user_ratings_total')
        
        # Merge reviews (keep HappyCow, replace Google)
        current_featured = existing_data.get('featured', [])
        kept_reviews = [r for r in current_featured if r.get('source') != 'Google']
        
        # Add new top 5 Google reviews
        existing_data['featured'] = kept_reviews + formatted_reviews[:5]
        
        with open(REVIEWS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
        print("Successfully updated Google Reviews!")
        return True
        
    except Exception as e:
        print(f"Failed to fetch Google Reviews: {e}")
        return False

def fetch_instagram_posts():
    if not INSTAGRAM_TOKEN:
        print("Skipping Instagram: Access token not provided.")
        return False
        
    print("Fetching Instagram Posts...")
    # Instagram Graph API or Basic Display API endpoint
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink&access_token={INSTAGRAM_TOKEN}&limit=6"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        posts = data.get('data', [])
        formatted_posts = []
        
        for p in posts:
            # Use thumbnail for videos, otherwise media_url
            img_url = p.get('thumbnail_url') if p.get('media_type') == 'VIDEO' else p.get('media_url')
            
            formatted_posts.append({
                "id": p.get('id'),
                "imageUrl": img_url,
                "link": p.get('permalink'),
                "caption": p.get('caption', '')
            })
            
        output = {"posts": formatted_posts}
        
        with open(INSTAGRAM_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        print("Successfully updated Instagram feed!")
        
        # Note: If using Basic Display API, the token needs to be refreshed every 60 days.
        # We can trigger the refresh endpoint here as well.
        refresh_url = f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={INSTAGRAM_TOKEN}"
        try:
            urllib.request.urlopen(urllib.request.Request(refresh_url))
            print("Successfully refreshed Instagram access token.")
        except Exception:
            # Silent fail for refresh, it might just be a non-expiring page token
            pass
            
        return True
        
    except Exception as e:
        print(f"Failed to fetch Instagram posts: {e}")
        return False

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    google_success = fetch_google_reviews()
    insta_success = fetch_instagram_posts()
    
    if not google_success and not insta_success:
        print("No APIs were successfully updated. Please check your GitHub Secrets.")
