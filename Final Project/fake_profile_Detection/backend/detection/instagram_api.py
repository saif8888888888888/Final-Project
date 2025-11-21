import requests
import json
from datetime import datetime

class InstagramAPI:
    def __init__(self):
        self.api_key = "6916ee20fde0ac7ce6d2fe38"
        self.base_url = "https://api.scrapingdog.com/instagram/profile"
    
    def get_profile_info(self, username):
        """Get REAL Instagram profile information using ScrapingDog API"""
        if not username:
            return self.get_empty_profile_data(username)
        
        print(f"🔍 Fetching REAL Instagram data for: {username}")
        
        params = {
            "api_key": self.api_key,
            "username": username
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Raw API Response: {json.dumps(data, indent=2)[:500]}...")  # Print first 500 chars
                
                # Parse the real API data
                profile_data = self.parse_real_api_data(data, username)
                
                if profile_data and profile_data.get('followers_count', 0) > 0:  # Valid data check
                    print(f"✅ Successfully fetched REAL data for {username}")
                    return profile_data
                else:
                    print("❌ API returned incomplete data")
                    return self.get_empty_profile_data(username)
            else:
                print(f"❌ API request failed with status: {response.status_code}")
                return self.get_empty_profile_data(username)
                
        except Exception as e:
            print(f"❌ ScrapingDog API Error: {e}")
            return self.get_empty_profile_data(username)
    
    def parse_real_api_data(self, data, username):
        """Parse REAL ScrapingDog API response"""
        try:
            # The API response structure might vary - let's handle different possible structures
            profile_info = data
            
            # Common field mappings for Instagram profile data
            followers = (profile_info.get('followers') or 
                        profile_info.get('follower_count') or 
                        profile_info.get('followers_count') or 0)
            
            following = (profile_info.get('following') or 
                       profile_info.get('following_count') or 
                       profile_info.get('follows_count') or 0)
            
            posts = (profile_info.get('posts') or 
                    profile_info.get('post_count') or 
                    profile_info.get('posts_count') or 0)
            
            bio = (profile_info.get('bio') or 
                  profile_info.get('biography') or 
                  profile_info.get('description') or '')
            
            is_verified = (profile_info.get('verified') or 
                          profile_info.get('is_verified') or 
                          profile_info.get('is_verified_account') or False)
            
            profile_pic = (profile_info.get('profile_pic') or 
                          profile_info.get('profile_picture') or 
                          profile_info.get('profile_picture_url') or '')
            
            full_name = profile_info.get('full_name') or ''
            
            # Get recent posts
            recent_posts = self.extract_recent_posts(profile_info)
            
            profile_data = {
                'username': username,
                'bio': bio,
                'followers_count': int(followers) if followers else 0,
                'following_count': int(following) if following else 0,
                'posts_count': int(posts) if posts else 0,
                'is_verified': bool(is_verified),
                'profile_picture': bool(profile_pic),
                'full_name': full_name,
                'location': profile_info.get('location', ''),
                'account_age_days': self.calculate_account_age(profile_info.get('joined_date', '')),
                'recent_posts': recent_posts,
                'is_private': profile_info.get('is_private', False),
                'external_url': profile_info.get('external_url', ''),
            }
            
            print(f"📈 Parsed REAL data - Followers: {profile_data['followers_count']}, "
                  f"Following: {profile_data['following_count']}, Posts: {profile_data['posts_count']}")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Error parsing real API data: {e}")
            return None
    
    def extract_recent_posts(self, profile_info):
        """Extract recent posts from API response"""
        recent_posts = []
        
        # Try different possible keys for posts
        posts_data = (profile_info.get('recent_posts') or 
                     profile_info.get('posts') or 
                     profile_info.get('media') or [])
        
        if isinstance(posts_data, list):
            for post in posts_data[:5]:  # Get up to 5 recent posts
                if isinstance(post, dict):
                    post_text = (post.get('caption') or 
                                post.get('text') or 
                                post.get('description') or '')
                    
                    post_data = {
                        'text': post_text,
                        'likes': post.get('likes', 0) or post.get('like_count', 0),
                        'comments': post.get('comments', 0) or post.get('comment_count', 0),
                        'timestamp': post.get('timestamp', ''),
                    }
                    recent_posts.append(post_data)
        
        return recent_posts
    
    def calculate_account_age(self, join_date_str):
        """Calculate account age in days"""
        if not join_date_str:
            return 365  # Default
        
        try:
            # Try common date formats
            for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S', '%b %d, %Y'):
                try:
                    join_date = datetime.strptime(join_date_str, fmt)
                    current_date = datetime.now()
                    age_days = (current_date - join_date).days
                    return max(age_days, 1)
                except ValueError:
                    continue
            return 365
        except:
            return 365
    
    def get_empty_profile_data(self, username):
        """Return empty profile data when API fails"""
        print(f"⚠️ Using empty data for: {username} - API might be unavailable")
        return {
            'username': username,
            'bio': '',
            'followers_count': 0,
            'following_count': 0,
            'is_verified': False,
            'profile_picture': False,
            'location': '',
            'account_age_days': 365,
            'recent_posts': [],
            'is_private': False,
            'full_name': '',
        }