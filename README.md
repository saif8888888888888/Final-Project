Fake Profile Detection System

A powerful Django-based web application that detects fake social media profiles in real-time using advanced rule-based analysis and ScrapingDog API integration.
https://img.shields.io/badge/Fake-Profile%2520Detection-red
https://img.shields.io/badge/Django-4.2-green
https://img.shields.io/badge/Python-3.8+-blue
https://img.shields.io/badge/Real--time-Analysis-orange

🚀 Overview
The Fake Profile Detection System is an intelligent web application that analyzes social media profiles across multiple platforms (Instagram, Twitter, Facebook, TikTok) to identify fake or artificial accounts. Using real-time data from ScrapingDog API and advanced rule-based algorithms, it provides accurate detection of suspicious patterns and fake engagement.

✨ Key Features
🔥 Real-time Detection
Live API Integration: Uses ScrapingDog API for real-time profile data
Multi-Platform Support: Instagram, Twitter, Facebook, TikTok
Instant Analysis: Get results in seconds with detailed risk factors

🎯 Advanced Detection Algorithms
Follower/Following Ratio Analysis: Detects unnatural growth patterns
Username Pattern Recognition: Identifies auto-generated and suspicious usernames
Engagement Analysis: Analyzes likes, comments, and posting patterns
Content Similarity Detection: Finds duplicate or automated content
Growth Pattern Analysis: Identifies purchased followers and artificial growth

📊 Smart Risk Assessment
Binary Classification: Clear "Fake" or "Genuine" results
Detailed Risk Factors: Specific reasons why a profile is flagged
Confidence Scoring: Percentage-based confidence in detection
Real-time Data: Always uses current profile information

🛡️ User-Friendly Interface
Modern Cyber Theme: Clean, professional design
Responsive Design: Works on all devices
Interactive Dashboard: Track scan history and analytics
Easy Reporting: Simple profile reporting system

🛠️ Technologies Used
Backend
Django 4.2: Python web framework
SQLite: Database (can be upgraded to PostgreSQL)
Requests: API communication
Python 3.8+: Core programming language

Frontend
HTML5/CSS3: Modern web standards
JavaScript: Interactive functionality
Bootstrap: Responsive design framework
Chart.js: Analytics and visualization
Font Awesome: Icons and UI elements

APIs & Services
ScrapingDog API: Real-time social media data
RESTful Architecture: Clean API design
JSON Processing: Efficient data handling

📦 Installation
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Git

Step-by-Step Setup
Clone the Repository
bash
git clone https://github.com/yourusername/fake-profile-detection.git
cd fake-profile-detection/backend
Create Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
pip install -r requirements.txt
Configure Environment Variables

bash
cp .env.example .env
# Edit .env with your API keys and settings
Database Setup

bash
python manage.py migrate
python manage.py createsuperuser
Run Development Server

bash
python manage.py runserver

Access Application
Open http://localhost:8000 in your browser

⚙️ Configuration
Environment Variables
Create a .env file in the backend directory:
env
# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
SCRAPINGDOG_API_KEY=your-scrapingdog-api-key
TWITTER_API_KEY=your-twitter-api-key
INSTAGRAM_ACCESS_TOKEN=your-instagram-token
FACEBOOK_APP_ID=your-facebook-app-id

# Database
DATABASE_URL=sqlite:///db.sqlite3

API Configuration
ScrapingDog API: Get your API key from scrapingdog.com
Social Media APIs: Configure additional API keys for enhanced functionality

🎮 Usage Guide
1. Profile Detection
Navigate to Detection Page: Click "Detect" in navigation
Select Platform: Choose Instagram, Twitter, Facebook, or TikTok
Enter Profile URL: Paste the full profile URL
Analyze: Click "Analyze Profile with Real-time API"
View Results: Get instant fake/genuine classification

2. Understanding Results
🟢 Genuine Profile
Green confirmation banner
No risk factors detected
Profile appears authentic

🔴 Fake Profile Detected
Red warning banner
Specific risk factors listed
Confidence percentage
Clear reasons for detection

3. Dashboard Features
Scan History: View all previous scans
Analytics: Visual charts of detection results
User Statistics: Track your detection activity
Export Reports: Download scan results

🔍 Detection Rules
The system uses multiple rule-based checks:
1. Extreme Ratio Detection
Following 100x more accounts than followers
Massive follower counts with minimal following
Unnatural engagement patterns

2. Suspicious Growth Patterns
Impossible growth rates (5000+ followers in 7 days)
Rapid follower acquisition
Inconsistent growth timelines

3. Username Analysis
Auto-generated patterns (user_123456, insta_829472)
High entropy random usernames
Known fake account naming conventions

4. Automated Behavior
Impossible posting frequency (100+ posts/day)
Duplicate content across posts
Private accounts with massive following

5. Spam Content Detection
"Follow for follow" phrases
Promotion and buying followers content
Generic template bios

📊 API Integration
Supported Platforms
Instagram: Full profile analysis with posts, followers, engagement
Twitter: Follower analysis, tweet patterns, verification status
Facebook: Basic profile information and friend counts

API Endpoints
python
# Profile Detection
POST /detect/
# Parameters: profile_url, platform, additional_context

# Report Profile
POST /detect/report/
# Parameters: profile_url, platform, reason

# Scan History
GET /dashboard/history/
🗄️ Database Schema
Core Models
python
class ProfileScan:
    user, profile_url, platform, risk_score, result, risk_factors, created_at

class Report:
    user, profile_url, platform, reason, status, created_at

class UserStats:
    user, total_scans, fake_profiles, genuine_profiles, reports_filed

🚀 Deployment
Production Deployment
Set DEBUG=False in settings
Configure production database (PostgreSQL recommended)
Set up static files with WhiteNoise
Configure ALLOWED_HOSTS
Set up SSL certificate
Configure web server (Nginx + Gunicorn)

Docker Deployment
dockerfile

# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "fake_detect.wsgi:application", "--bind", "0.0.0.0:8000"]

🤝 Contributing
We welcome contributions! Please see our Contributing Guidelines for details.
Development Setup
Fork the repository
Create a feature branch
Make your changes
Add tests
Submit a pull request
Code Style
Follow PEP 8 guidelines
Use meaningful variable names
Add docstrings for functions
Include tests for new features

🐛 Troubleshooting
Common Issues
API Connection Errors
Check internet connection
Verify API keys in .env file
Ensure ScrapingDog account is active
Database Issues
Run python manage.py migrate
Check database permissions
Verify database URL in settings
Static Files Not Loading
Run python manage.py collectstatic
Check WhiteNoise configuration
Verify static file paths
Getting Help
Create an issue on GitHub
Check existing issues for solutions
Contact support via email

🔮 Future Enhancements
Planned Features
Machine Learning integration for improved detection
Additional social media platforms (LinkedIn, YouTube)
Advanced analytics and reporting
Browser extension for quick detection
Mobile application
Batch profile scanning
API rate limiting and caching
Advanced user roles and permissions

Roadmap
Phase 1: Core detection engine ✅
Phase 2: Multi-platform support ✅
Phase 3: User dashboard and analytics ✅
Phase 4: Machine learning integration 🚧
Phase 5: Mobile app and extensions 📅

📞 Support & Contact
Project Maintainer
Saif
Email: hsaifullasaif@gmail.com
Phone: 8123769345
Support Channels
GitHub Issues: Project Issues

Email Support: hsaifullasaif@gmail.com

Documentation: Final Project
🙏 Acknowledgments
ScrapingDog for providing reliable social media APIs
Django Community for the excellent web framework
Contributors who helped improve this project
Testers who provided valuable feedback

⭐ Star this repository if you find it helpful!

https://img.shields.io/github/stars/yourusername/fake-profile-detection?style=social
https://img.shields.io/github/forks/yourusername/fake-profile-detection?style=social

Built By ❤️ Saif





