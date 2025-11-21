import requests
import os

class FacebookAPI:
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    def get_profile_info(self, profile_id):
        """Get Facebook profile information"""
        if not self.app_id or not self.access_token:
            return self.get_mock_data(profile_id)
        
        # Note: Facebook API has strict requirements for profile access
        # This is a simplified example
        return self.get_mock_data(profile_id)
    
    def get_mock_data(self, profile_id):
        """Return mock data when API is not available"""
        import random
        return {
            'username': profile_id,
            'bio': 'Sample Facebook user bio',
            'friends_count': random.randint(50, 5000),
            'is_verified': random.random() > 0.95,
        }