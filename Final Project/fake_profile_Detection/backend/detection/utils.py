import re
from urllib.parse import urlparse

def extract_platform_from_url(url):
    """Extract platform from profile URL"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    if 'instagram.com' in domain:
        return 'instagram'
    elif 'facebook.com' in domain:
        return 'facebook'
    elif 'twitter.com' in domain or 'x.com' in domain:
        return 'twitter'
    elif 'tiktok.com' in domain:
        return 'tiktok'
    else:
        return 'unknown'

def extract_username_from_url(url, platform):
    """Extract username from profile URL"""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    
    if platform == 'instagram':
        return path.split('/')[0] if path else None
    elif platform == 'facebook':
        return path.split('/')[-1] if path else None
    elif platform == 'twitter':
        # Handle both twitter.com and x.com URLs
        username = path.split('/')[0] if path else None
        # Remove @ symbol if present and any query parameters
        if username:
            if username.startswith('@'):
                username = username[1:]
            # Remove any query parameters
            username = username.split('?')[0]
        return username
    elif platform == 'tiktok':
        if '@' in path:
            return path.split('@')[-1]
        return path.split('/')[-1] if path else None
    else:
        return None

def validate_profile_url(url, platform):
    """Validate if the URL matches the expected platform format"""
    if platform == 'instagram':
        pattern = r'^https?://(www\.)?instagram\.com/[\w\.]+/?$'
    elif platform == 'facebook':
        pattern = r'^https?://(www\.)?facebook\.com/[\w\.]+/?$'
    elif platform == 'twitter':
        pattern = r'^https?://(www\.)?(twitter|x)\.com/[\w]+/?$'
    elif platform == 'tiktok':
        pattern = r'^https?://(www\.)?tiktok\.com/@?[\w\.]+/?$'
    else:
        return False
    
    return bool(re.match(pattern, url))

def extract_twitter_username(url):
    """Specialized function to extract Twitter username from URL"""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    
    if path:
        username = path.split('/')[0]
        # Remove @ symbol if present
        if username.startswith('@'):
            username = username[1:]
        return username
    return None