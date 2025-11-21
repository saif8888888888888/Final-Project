import re
import math
from collections import Counter

class RuleBasedDetectionEngine:
    def __init__(self):
        self.rules = {
            'profile_completeness': self.check_profile_completeness,
            'follower_following_ratio': self.check_follower_following_ratio,
            'username_entropy': self.check_username_entropy,
            'posting_frequency': self.check_posting_frequency,
            'content_similarity': self.check_content_similarity,
            'account_age_activity': self.check_account_age_activity,
            'verification_status': self.check_verification_status,
        }
    
    def analyze_profile(self, profile_data):
        risk_factors = []
        total_score = 0
        max_score = len(self.rules) * 10
        
        for rule_name, rule_func in self.rules.items():
            score, factor = rule_func(profile_data)
            total_score += score
            if factor:
                risk_factors.append(factor)
        
        risk_percentage = (total_score / max_score) * 100
        
        # Determine result based on risk percentage
        if risk_percentage >= 25:
            result = 'fake'
        elif risk_percentage >= 40:
            result = 'suspicious'
        else:
            result = 'genuine'
        
        return {
            'risk_score': int(risk_percentage),
            'result': result,
            'risk_factors': risk_factors
        }
    
    def check_profile_completeness(self, profile_data):
        score = 0
        factors = []
        
        if not profile_data.get('bio') or len(profile_data.get('bio', '')) < 10:
            score += 6
            factors.append("Profile bio is empty or very short")
        
        if not profile_data.get('location'):
            score += 4
            factors.append("No location information provided")
        
        factor = "; ".join(factors) if factors else None
        return min(score, 10), factor
    
    def check_follower_following_ratio(self, profile_data):
        followers = profile_data.get('followers_count', 0) or profile_data.get('friends_count', 0)
        following = profile_data.get('following_count', 0)
        
        if following == 0:
            return 0, None
        
        ratio = followers / following
        
        if ratio < 0.1:  # Following many but few followers
            return 10, "Extremely low follower-to-following ratio (potential follow-back scheme)"
        elif ratio < 0.5:
            return 7, "Low follower-to-following ratio"
        elif ratio > 10:  # Many followers but following few
            return 5, "Very high follower-to-following ratio (potential purchased followers)"
        
        return 0, None
    
    def check_username_entropy(self, profile_data):
        username = profile_data.get('username', '')
        
        # Calculate Shannon entropy
        if len(username) == 0:
            return 0, None
        
        prob = [float(username.count(c)) / len(username) for c in set(username)]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
        
        # High entropy often indicates random username generation
        if entropy > 3.5:
            return 8, "Username appears randomly generated (high entropy)"
        
        # Check for patterns common in fake accounts
        fake_patterns = [
            r'.*\d{4,}.*',  # Many numbers
            r'user_\d+',    # user_12345 pattern
            r'.*fake.*',    # Contains 'fake'
            r'.*bot.*',     # Contains 'bot'
            r'^[a-z]+\d+$', # alphabets followed by numbers
        ]
        
        for pattern in fake_patterns:
            if re.match(pattern, username, re.IGNORECASE):
                return 6, "Username matches common fake account patterns"
        
        return 0, None
    
    def check_posting_frequency(self, profile_data):
        posts_count = profile_data.get('posts_count', 0)
        account_age_days = profile_data.get('account_age_days', 1)
        
        if account_age_days == 0:
            return 0, None
        
        posts_per_day = posts_count / account_age_days
        
        if posts_per_day > 50:
            return 9, "Extremely high posting frequency (potential automation)"
        elif posts_per_day > 20:
            return 7, "Very high posting frequency"
        elif posts_per_day < 0.1 and posts_count > 0:
            return 5, "Very low posting frequency with existing posts"
        
        return 0, None
    
    def check_content_similarity(self, profile_data):
        posts = profile_data.get('recent_posts', [])
        
        if len(posts) < 2:
            return 0, None
        
        # Simple content similarity check
        content_texts = [post.get('text', '') for post in posts[:5]]
        similarity_count = 0
        
        for i in range(len(content_texts)):
            for j in range(i + 1, len(content_texts)):
                if self.calculate_similarity(content_texts[i], content_texts[j]) > 0.8:
                    similarity_count += 1
        
        if similarity_count > len(posts) * 0.3:
            return 8, "High content similarity detected across multiple posts"
        
        return 0, None
    
    def check_account_age_activity(self, profile_data):
        account_age_days = profile_data.get('account_age_days', 0)
        posts_count = profile_data.get('posts_count', 0)
        
        if account_age_days < 30 and posts_count > 100:
            return 8, "Very high activity for a new account"
        elif account_age_days < 7:
            return 5, "Very new account (less than 1 week old)"
        
        return 0, None
    
    def check_verification_status(self, profile_data):
        is_verified = profile_data.get('is_verified', False)
        
        if not is_verified:
            # Being unverified is normal, but combined with other factors it adds risk
            return 2, "Account is not verified"
        
        return 0, None
    
    def calculate_similarity(self, text1, text2):
        """Calculate Jaccard similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0