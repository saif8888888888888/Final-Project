import requests
import json
from datetime import datetime

class TwitterAPI:
    def __init__(self):
        self.api_key = "6914d3d71c1278811f5282bf"
        self.base_url = "https://api.scrapingdog.com/x/profile"
    
    def get_profile_info(self, username):
        """Get REAL Twitter profile information using ScrapingDog API"""
        if not username:
            return self.get_fallback_data(username)
        
        print(f"🔍 Fetching REAL Twitter data for: {username}")
        
        params = {
            "api_key": self.api_key,
            "profileId": username.strip(),
            "parsed": "true"
        }
        
        try:
            print(f"📡 Making API request to: {self.base_url}")
            print(f"📡 Request params: {params}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Raw API Response received")
                
                # Debug: Print the actual response structure
                print("🔍 Full API Response Structure:")
                print(json.dumps(data, indent=2)[:3000])  # Print first 3000 chars
                
                # Check if we got valid data
                if data and isinstance(data, dict):
                    # Check if API returned an error or empty data
                    if data.get('error') or data.get('message'):
                        print(f"❌ API Error: {data.get('error') or data.get('message')}")
                        return self.get_fallback_data(username)
                    
                    # Check if we have any meaningful data
                    if self.has_valid_data(data):
                        profile_data = self.parse_scrapingdog_response(data, username)
                        if profile_data:
                            print(f"✅ Successfully parsed real data for {username}")
                            return profile_data
                    else:
                        print("❌ API returned empty or invalid data")
                
                return self.get_fallback_data(username)
            else:
                print(f"❌ API request failed with status: {response.status_code}")
                return self.get_fallback_data(username)
                
        except Exception as e:
            print(f"❌ ScrapingDog API Error: {str(e)}")
            return self.get_fallback_data(username)
    
    def has_valid_data(self, data):
        """Check if the API response contains valid profile data"""
        # Check for common Twitter profile fields
        valid_fields = [
            'followers_count', 'following_count', 'tweets_count',
            'followers', 'following', 'tweets',
            'name', 'screen_name', 'description'
        ]
        
        for field in valid_fields:
            if field in data and data[field]:
                return True
        
        # Check nested structures
        if data.get('user'):
            return True
        if data.get('data'):
            return True
            
        return False
    
    def parse_scrapingdog_response(self, data, username):
        """Parse ScrapingDog API response for Twitter profiles"""
        try:
            print("🔧 Starting to parse Twitter API response...")
            
            profile_info = data
            
            # Extract data with multiple fallback options
            followers = self.extract_followers(profile_info)
            following = self.extract_following(profile_info)
            tweets = self.extract_tweets(profile_info)
            bio = self.extract_bio(profile_info)
            verified = self.extract_verified(profile_info)
            profile_pic = self.extract_profile_pic(profile_info)
            full_name = self.extract_full_name(profile_info)
            location = self.extract_location(profile_info)
            
            profile_data = {
                'username': username,
                'bio': bio,
                'followers_count': followers,
                'following_count': following,
                'posts_count': tweets,
                'is_verified': verified,
                'profile_picture': profile_pic,
                'full_name': full_name,
                'location': location,
                'account_age_days': 365,  # Default
                'recent_posts': self.extract_recent_tweets(profile_info),
                'api_success': True,
                'api_data_source': 'ScrapingDog API - Real-time Twitter Data'
            }
            
            print(f"📈 Parsed Twitter data:")
            print(f"   - Followers: {profile_data['followers_count']}")
            print(f"   - Following: {profile_data['following_count']}")
            print(f"   - Tweets: {profile_data['posts_count']}")
            print(f"   - Verified: {profile_data['is_verified']}")
            print(f"   - Recent Tweets: {len(profile_data['recent_posts'])}")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Error parsing Twitter API response: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def extract_followers(self, profile_info):
        """Extract followers count"""
        followers_sources = [
            profile_info.get('followers_count'),
            profile_info.get('followers'),
            profile_info.get('user', {}).get('followers_count'),
            profile_info.get('data', {}).get('followers_count'),
        ]
        
        for followers in followers_sources:
            if followers is not None:
                return self.safe_int(followers)
        return 0
    
    def extract_following(self, profile_info):
        """Extract following count"""
        following_sources = [
            profile_info.get('following_count'),
            profile_info.get('following'),
            profile_info.get('friends_count'),
            profile_info.get('user', {}).get('following_count'),
            profile_info.get('user', {}).get('friends_count'),
            profile_info.get('data', {}).get('following_count'),
        ]
        
        for following in following_sources:
            if following is not None:
                return self.safe_int(following)
        return 0
    
    def extract_tweets(self, profile_info):
        """Extract tweets count"""
        tweets_sources = [
            profile_info.get('tweets_count'),
            profile_info.get('statuses_count'),
            profile_info.get('posts_count'),
            profile_info.get('user', {}).get('statuses_count'),
            profile_info.get('data', {}).get('tweets_count'),
        ]
        
        for tweets in tweets_sources:
            if tweets is not None:
                return self.safe_int(tweets)
        return 0
    
    def extract_bio(self, profile_info):
        """Extract bio/description"""
        bio_sources = [
            profile_info.get('description'),
            profile_info.get('bio'),
            profile_info.get('user', {}).get('description'),
            profile_info.get('data', {}).get('description'),
        ]
        
        for bio in bio_sources:
            if bio:
                return str(bio)
        return ''
    
    def extract_verified(self, profile_info):
        """Extract verified status"""
        verified_sources = [
            profile_info.get('verified'),
            profile_info.get('is_verified'),
            profile_info.get('user', {}).get('verified'),
            profile_info.get('data', {}).get('verified'),
        ]
        
        for verified in verified_sources:
            if verified is not None:
                return self.safe_bool(verified)
        return False
    
    def extract_profile_pic(self, profile_info):
        """Extract profile picture status"""
        pic_sources = [
            profile_info.get('profile_image_url'),
            profile_info.get('profile_picture'),
            profile_info.get('user', {}).get('profile_image_url'),
            profile_info.get('data', {}).get('profile_image_url'),
        ]
        
        for pic in pic_sources:
            if pic:
                return True
        return False
    
    def extract_full_name(self, profile_info):
        """Extract full name"""
        name_sources = [
            profile_info.get('name'),
            profile_info.get('full_name'),
            profile_info.get('user', {}).get('name'),
            profile_info.get('data', {}).get('name'),
        ]
        
        for name in name_sources:
            if name:
                return str(name)
        return ''
    
    def extract_location(self, profile_info):
        """Extract location"""
        location_sources = [
            profile_info.get('location'),
            profile_info.get('user', {}).get('location'),
            profile_info.get('data', {}).get('location'),
        ]
        
        for location in location_sources:
            if location:
                return str(location)
        return ''
    
    def extract_recent_tweets(self, profile_info):
        """Extract recent tweets from API response"""
        recent_tweets = []
        
        # Try different possible tweet data structures
        tweets_data_sources = [
            profile_info.get('tweets'),
            profile_info.get('recent_tweets'),
            profile_info.get('posts'),
            profile_info.get('timeline'),
            profile_info.get('latest_tweets'),
            profile_info.get('data', {}).get('tweets'),
        ]
        
        tweets_data = None
        for data_source in tweets_data_sources:
            if data_source and isinstance(data_source, list) and len(data_source) > 0:
                tweets_data = data_source
                print(f"🐦 Found tweets data with {len(tweets_data)} items")
                break
        
        if not tweets_data:
            print("📭 No tweets data found in response")
            return recent_tweets
        
        for i, tweet in enumerate(tweets_data[:10]):  # Get up to 10 recent tweets
            try:
                if isinstance(tweet, dict):
                    # Extract tweet text
                    text = self.safe_get(tweet, ['text', 'content', 'body', 'full_text'])
                    
                    # Extract engagement metrics
                    likes = self.safe_int(self.safe_get(tweet, ['likes', 'like_count', 'favorite_count']))
                    retweets = self.safe_int(self.safe_get(tweet, ['retweets', 'retweet_count']))
                    replies = self.safe_int(self.safe_get(tweet, ['replies', 'reply_count']))
                    
                    tweet_data = {
                        'text': text if text else 'No text available',
                        'likes': likes,
                        'retweets': retweets,
                        'replies': replies,
                        'type': 'tweet'
                    }
                    
                    recent_tweets.append(tweet_data)
                    
            except Exception as e:
                print(f"⚠️ Error parsing tweet {i}: {e}")
                continue
        
        print(f"✅ Extracted {len(recent_tweets)} recent tweets")
        return recent_tweets
    
    def safe_get(self, data, keys, default=''):
        """Safely get nested value from dictionary"""
        if not isinstance(data, dict):
            return default
            
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current if current is not None else default
    
    def safe_int(self, value, default=0):
        """Safely convert to integer"""
        try:
            if value is None:
                return default
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def safe_bool(self, value, default=False):
        """Safely convert to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'y')
        return default
    
    def get_fallback_data(self, username):
        """Return fallback data when API fails"""
        print(f"⚠️ Using fallback data for Twitter: {username}")
        return {
            'username': username,
            'bio': '',
            'followers_count': 0,
            'following_count': 0,
            'posts_count': 0,
            'is_verified': False,
            'profile_picture': False,
            'full_name': '',
            'location': '',
            'account_age_days': 365,
            'recent_posts': [],
            'api_success': False,
            'api_data_source': 'Fallback Data (Twitter API Unavailable)'
        }