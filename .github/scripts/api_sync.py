import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------
# CONFIGURATION & SECRETS
# ---------------------------------------------------------
GOOGLE_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
GOOGLE_PLACE_ID = os.environ.get('GOOGLE_PLACE_ID')
INSTAGRAM_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN')

REVIEWS_JSON_PATH = 'data/reviews.json'
INSTAGRAM_JSON_PATH = 'data/instagram.json'

def fetch_google_reviews():
    if not GOOGLE_API_KEY or not GOOGLE_PLACE_ID:
        print("Skipping Google Reviews: API Key or Place ID not provided.")
        return False
        
    print("Fetching Google Reviews using Places API (New)...")
    url = f"https://places.googleapis.com/v1/places/{GOOGLE_PLACE_ID}"
    
    headers = {
        'X-Goog-Api-Key': GOOGLE_API_KEY,
        'X-Goog-FieldMask': 'id,displayName,rating,userRatingCount,reviews',
        'Accept-Language': 'en'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        rating = data.get('rating')
        review_count = data.get('userRatingCount')
        reviews = data.get('reviews', [])
        
        # Format for our frontend
        formatted_reviews = []
        for r in reviews:
            r_rating = r.get('rating', 0)
            if r_rating >= 4:
                publish_time = r.get('publishTime', '')
                try:
                    date_str = publish_time.split('T')[0] if 'T' in publish_time else publish_time
                except Exception:
                    date_str = publish_time

                author = r.get('authorAttribution', {})
                text_obj = r.get('text', r.get('originalText', {}))
                
                formatted_reviews.append({
                    "id": f"g-{r.get('name', '').split('/')[-1]}",
                    "source": "Google",
                    "author": author.get('displayName', 'Google User'),
                    "rating": r_rating,
                    "date": date_str,
                    "text": {
                        "en": text_obj.get('text', ''),
                        "ko": "",
                        "zh-cn": "",
                        "zh-tw": ""
                    },
                    "photoUrl": author.get('photoUri')
                })
        
        # Load existing reviews
        existing_data = {}
        if os.path.exists(REVIEWS_JSON_PATH):
            with open(REVIEWS_JSON_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                
        existing_data['lastUpdated'] = datetime.now(timezone.utc).isoformat()
        if 'sources' not in existing_data:
            existing_data['sources'] = {}
        if 'google' not in existing_data['sources']:
            existing_data['sources']['google'] = {}
            
        existing_data['sources']['google']['rating'] = rating
        existing_data['sources']['google']['reviewCount'] = review_count
        
        current_featured = existing_data.get('featured', [])
        kept_reviews = [r for r in current_featured if r.get('source') != 'Google']
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
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink&access_token={INSTAGRAM_TOKEN}&limit=6"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        posts = data.get('data', [])
        formatted_posts = []
        
        for p in posts:
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
        
        refresh_url = f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={INSTAGRAM_TOKEN}"
        try:
            urllib.request.urlopen(urllib.request.Request(refresh_url))
            print("Successfully refreshed Instagram access token.")
        except Exception:
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
