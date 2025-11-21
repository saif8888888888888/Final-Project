// API integration functions
class FakeProfileAPI {
    static async detectProfile(profileUrl, platform, additionalContext = '') {
        try {
            const response = await fetch('/detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: new URLSearchParams({
                    'profile_url': profileUrl,
                    'platform': platform,
                    'additional_context': additionalContext
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            return await response.text(); // For HTML response
        } catch (error) {
            console.error('Error detecting profile:', error);
            throw error;
        }
    }
    
    static async reportProfile(profileUrl, platform, reason) {
        try {
            const response = await fetch('/detect/report/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: new URLSearchParams({
                    'profile_url': profileUrl,
                    'platform': platform,
                    'reason': reason
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error reporting profile:', error);
            throw error;
        }
    }
    
    static async getScanHistory() {
        try {
            const response = await fetch('/dashboard/history/');
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            return await response.text(); // For HTML response
        } catch (error) {
            console.error('Error fetching scan history:', error);
            throw error;
        }
    }
    
    static getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Utility functions for API interactions
const APIUtils = {
    // Format platform for display
    formatPlatform(platform) {
        const platformMap = {
            'instagram': 'Instagram',
            'facebook': 'Facebook',
            'twitter': 'Twitter',
            'tiktok': 'TikTok'
        };
        return platformMap[platform] || platform;
    },
    
    // Get platform icon class
    getPlatformIcon(platform) {
        const iconMap = {
            'instagram': 'fab fa-instagram',
            'facebook': 'fab fa-facebook-f',
            'twitter': 'fab fa-twitter',
            'tiktok': 'fab fa-tiktok'
        };
        return iconMap[platform] || 'fas fa-globe';
    },
    
    // Format risk score for display
    formatRiskScore(score) {
        if (score >= 70) {
            return { text: 'High Risk', class: 'score-high' };
        } else if (score >= 40) {
            return { text: 'Medium Risk', class: 'score-medium' };
        } else {
            return { text: 'Low Risk', class: 'score-low' };
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FakeProfileAPI, APIUtils };
}