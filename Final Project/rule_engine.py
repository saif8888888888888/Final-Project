import re
import math
from collections import Counter
from datetime import datetime

class RuleBasedDetectionEngine:
    def __init__(self):
        self.rules = {
            'extreme_ratio': self.check_extreme_ratio,
            'suspicious_growth': self.check_suspicious_growth,
            'fake_username_patterns': self.check_fake_username_patterns,
            'automated_behavior': self.check_automated_behavior,
            'spam_content': self.check_spam_content,
            'engagement_anomalies': self.check_engagement_anomalies,
        }
    
    def analyze_profile(self, profile_data):
        risk_factors = []
        total_score = 0
        max_score = len(self.rules) * 15  # Higher max score for stronger detection
        
        print("🔍 Starting real-time fake profile detection...")
        print(f"📊 Profile data: {profile_data.get('followers_count', 0)} followers, "
              f"{profile_data.get('following_count', 0)} following")
        
        for rule_name, rule_func in self.rules.items():
            score, factors = rule_func(profile_data)
            total_score += score
            if factors:
                if isinstance(factors, list):
                    risk_factors.extend(factors)
                else:
                    risk_factors.append(factors)
        
        risk_percentage = (total_score / max_score) * 100
        
        # Binary classification: Either Fake or Genuine
        # Higher threshold to avoid false positives
        if risk_percentage >= 40:  # 40% risk score means fake
            result = 'fake'
        else:
            result = 'genuine'
        
        print(f"🎯 Detection Complete: {risk_percentage:.1f}% risk score")
        print(f"📋 Result: {result.upper()}")
        print(f"🚨 Risk factors found: {len(risk_factors)}")
        
        return {
            'risk_score': int(risk_percentage),
            'result': result,
            'risk_factors': risk_factors
        }
    
    def check_extreme_ratio(self, profile_data):
        """Check for extreme follower/following ratios that indicate fake accounts"""
        followers = profile_data.get('followers_count', 0)
        following = profile_data.get('following_count', 0)
        
        if following == 0:
            return 0, None
        
        ratio = followers / following
        
        # Only flag extreme patterns that are strong fake indicators
        if ratio < 0.01 and following > 500:  # Following 100x more than followers
            score = 15
            factor = f"🚩 EXTREME RATIO: Following {following} accounts but only {followers} followers (1:{int(1/ratio)}) - Massive follow/unfollow scheme detected"
            return score, factor
        elif ratio < 0.05 and followers > 1000:
            score = 12
            factor = f"📊 SUSPICIOUS RATIO: {followers} followers vs {following} following - Fake engagement pattern"
            return score, factor
        elif ratio > 100 and followers > 5000:  # Mass followers, almost no following
            score = 10
            factor = f"📈 UNNATURAL RATIO: {followers} followers but only following {following} - Likely purchased followers"
            return score, factor
        
        return 0, None
    
    def check_suspicious_growth(self, profile_data):
        """Check for unnatural growth patterns"""
        followers_count = profile_data.get('followers_count', 0)
        account_age_days = profile_data.get('account_age_days', 1)
        
        factors = []
        score = 0
        
        # Check for impossible growth rates
        if account_age_days > 0:
            followers_per_day = followers_count / account_age_days
            
            # Impossible growth for new accounts
            if account_age_days < 7 and followers_count > 5000:
                score += 15
                factors.append(f"🚀 IMPOSSIBLE GROWTH: Gained {followers_count} followers in {account_age_days} days - Definitely fake")
            
            # Unnatural growth for medium-aged accounts
            elif account_age_days < 30 and followers_count > 10000:
                score += 12
                factors.append(f"📈 UNNATURAL GROWTH: {followers_count} followers in {account_age_days} days - Purchased followers")
            
            # High growth with no engagement
            elif followers_per_day > 100 and account_age_days > 30:
                score += 10
                factors.append(f"⚡ RAPID GROWTH: {followers_per_day:.0f} followers/day - Inconsistent with organic growth")
        
        return min(score, 15), factors if factors else None
    
    def check_fake_username_patterns(self, profile_data):
        """Check for username patterns common in fake accounts"""
        username = profile_data.get('username', '')
        
        if len(username) < 3:
            return 0, None
        
        # High entropy detection (very random usernames)
        prob = [float(username.count(c)) / len(username) for c in set(username)]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
        
        # Only flag very high entropy with length
        if entropy > 4.2 and len(username) > 10:
            score = 12
            factor = f"🔢 RANDOM USERNAME: '{username}' appears auto-generated - Common in bot accounts"
            return score, factor
        
        # Specific fake account patterns
        fake_patterns = [
            (r'^[a-z]+[0-9]{8,}$', "Random letters + 8+ numbers"),
            (r'^user_[0-9]{6,}$', "Generic user_123456 pattern"),
            (r'^insta_[0-9]{5,}$', "Insta_12345 pattern"),
            (r'^followers?_[0-9]+$', "Follower_123 pattern"),
            (r'^[0-9]{10,}$', "All numbers (10+ digits)"),
            (r'^.*[0-9]{6,}.*$', "6+ consecutive numbers in username"),
        ]
        
        for pattern, description in fake_patterns:
            if re.match(pattern, username, re.IGNORECASE):
                score = 10
                factor = f"🔄 FAKE PATTERN: Username '{username}' matches known fake account format"
                return score, factor
        
        return 0, None
    
    def check_automated_behavior(self, profile_data):
        """Check for patterns of automated/bot behavior"""
        posts_count = profile_data.get('posts_count', 0)
        account_age_days = max(profile_data.get('account_age_days', 1), 1)
        
        factors = []
        score = 0
        
        posts_per_day = posts_count / account_age_days
        
        # Impossible posting frequency
        if posts_per_day > 100:
            score += 15
            factors.append(f"🤖 IMPOSSIBLE FREQUENCY: {posts_per_day:.0f} posts/day - Clearly automated")
        elif posts_per_day > 50:
            score += 12
            factors.append(f"⚡ EXTREME FREQUENCY: {posts_per_day:.0f} posts/day - Likely bot account")
        elif posts_per_day > 20 and account_age_days > 30:
            score += 8
            factors.append(f"📱 HIGH FREQUENCY: {posts_per_day:.0f} posts/day - Unnatural for human")
        
        # Check for private account with massive following (common in fake accounts)
        is_private = profile_data.get('is_private', False)
        following_count = profile_data.get('following_count', 0)
        
        if is_private and following_count > 2000:
            score += 10
            factors.append(f"🔒 PRIVATE MASS-FOLLOWING: Private account following {following_count} users - Fake account strategy")
        
        return min(score, 15), factors if factors else None
    
    def check_spam_content(self, profile_data):
        """Check for spam content patterns"""
        bio = profile_data.get('bio', '')
        posts = profile_data.get('recent_posts', [])
        
        factors = []
        score = 0
        
        # Spam bio patterns
        if bio:
            spam_indicators = [
                'follow for follow',
                'f4f',
                'l4l',  # like for like
                'dm for promotion',
                'buy followers',
                'cheap followers',
                'instant followers',
                'get rich quick',
                'bitcoin investment',
                'passive income',
                'dm to promote',
                'promotion page'
            ]
            
            bio_lower = bio.lower()
            for indicator in spam_indicators:
                if indicator in bio_lower:
                    score += 12
                    factors.append(f"📝 SPAM BIO: Contains spam phrase '{indicator}'")
                    break
        
        # Check for duplicate content in posts (bot behavior)
        if len(posts) >= 3:
            content_texts = [post.get('text', '') for post in posts[:5] if post.get('text')]
            if len(content_texts) >= 3:
                duplicate_count = 0
                for i in range(len(content_texts)):
                    for j in range(i + 1, len(content_texts)):
                        if self.calculate_similarity(content_texts[i], content_texts[j]) > 0.95:  # Very high similarity
                            duplicate_count += 1
                
                if duplicate_count >= 2:
                    score += 10
                    factors.append(f"🔄 DUPLICATE CONTENT: {duplicate_count} nearly identical posts - Automated posting")
        
        return min(score, 15), factors if factors else None
    
    def check_engagement_anomalies(self, profile_data):
        """Check for engagement patterns that indicate fake accounts"""
        posts = profile_data.get('recent_posts', [])
        followers_count = profile_data.get('followers_count', 0)
        
        if followers_count == 0 or len(posts) == 0:
            return 0, None
        
        # Analyze engagement patterns
        total_likes = 0
        posts_with_engagement = 0
        
        for post in posts[:10]:
            likes = post.get('likes', 0)
            if likes > 0:
                total_likes += likes
                posts_with_engagement += 1
        
        if posts_with_engagement > 0:
            avg_likes = total_likes / posts_with_engagement
            engagement_ratio = avg_likes / followers_count if followers_count > 0 else 0
            
            # Suspicious: High followers but almost no engagement
            if engagement_ratio < 0.001 and followers_count > 10000:
                score = 12
                factor = f"📉 NO ENGAGEMENT: {followers_count} followers but almost zero likes - Fake followers"
                return score, factor
            
            # Suspicious: Too perfect engagement for large following
            if engagement_ratio > 0.8 and followers_count > 5000:
                score = 10
                factor = f"📊 PERFECT ENGAGEMENT: {engagement_ratio:.1%} engagement rate - Artificially inflated"
                return score, factor
        
        return 0, None
    
    def calculate_similarity(self, text1, text2):
        """Calculate Jaccard similarity between two texts"""
        if not text1 or not text2:
            return 0
            
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return 0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0