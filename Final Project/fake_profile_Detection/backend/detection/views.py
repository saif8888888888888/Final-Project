from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import traceback
from .models import ProfileScan, Report
from .rule_engine import RuleBasedDetectionEngine
from .instagram_api import InstagramAPI
from .twitter_api import TwitterAPI
from .facebook_api import FacebookAPI
from .utils import extract_platform_from_url, extract_username_from_url, validate_profile_url
from dashboard.models import UserStats

@login_required
def detect_profile(request):
    if request.method == 'POST':
        try:
            profile_url = request.POST.get('profile_url', '').strip()
            platform = request.POST.get('platform', '').strip()
            additional_context = request.POST.get('additional_context', '').strip()
            
            print(f"🎯 Starting REAL detection for: {profile_url}")
            
            # Validate inputs
            if not profile_url:
                messages.error(request, 'Please provide a profile URL.')
                return render(request, 'detection/detect.html')
            
            # Auto-detect platform if not provided
            if not platform or platform == 'auto':
                platform = extract_platform_from_url(profile_url)
                if platform == 'unknown':
                    messages.error(request, 'Could not detect platform from URL. Please select platform manually.')
                    return render(request, 'detection/detect.html')
            
            # Validate URL format
            if not validate_profile_url(profile_url, platform):
                messages.error(request, f'Invalid {platform} profile URL format.')
                return render(request, 'detection/detect.html')
            
            # Extract username from URL
            username = extract_username_from_url(profile_url, platform)
            if not username:
                messages.error(request, 'Could not extract username from the provided URL.')
                return render(request, 'detection/detect.html')
            
            print(f"🔍 Platform: {platform}, Username: {username}")
            
            # Get REAL profile data from ScrapingDog API
            profile_data = get_real_profile_data(platform, username, profile_url)
            
            # Analyze profile using rule-based engine with REAL data
            engine = RuleBasedDetectionEngine()
            analysis_result = engine.analyze_profile(profile_data)
            
            # Save scan result
            scan = ProfileScan.objects.create(
                user=request.user,
                profile_url=profile_url,
                platform=platform,
                additional_context=additional_context,
                risk_score=analysis_result['risk_score'],
                result=analysis_result['result'],
                risk_factors=analysis_result['risk_factors']
            )
            
            # Update user stats
            user_stats, created = UserStats.objects.get_or_create(user=request.user)
            user_stats.update_stats(analysis_result['result'])
            
            print(f"✅ Detection complete - Result: {analysis_result['result']}, Score: {analysis_result['risk_score']}%")
            
            return render(request, 'detection/result.html', {
                'scan': scan,
                'analysis_result': analysis_result,
                'profile_data': profile_data,
                'username': username
            })
            
        except Exception as e:
            print(f"❌ Error in detect_profile: {str(e)}")
            print(traceback.format_exc())
            messages.error(request, f'An error occurred during profile analysis: {str(e)}')
            return render(request, 'detection/detect.html')
    
    return render(request, 'detection/detect.html')

def get_real_profile_data(platform, username, profile_url):
    """Get REAL profile data from social media APIs"""
    print(f"🚀 Fetching REAL data for {platform} profile: {username}")
    
    try:
        if platform == 'instagram':
            api = InstagramAPI()
            profile_data = api.get_profile_info(username)
            
            # Add platform and URL info
            profile_data['platform'] = platform
            profile_data['profile_url'] = profile_url
            
            return profile_data
            
        elif platform == 'twitter':
            print(f"🐦 Calling Twitter API for username: {username}")
            api = TwitterAPI()
            profile_data = api.get_profile_info(username)
            profile_data['platform'] = platform
            profile_data['profile_url'] = profile_url
            
            # Debug: Check if we got real data
            if profile_data.get('followers_count', 0) == 0 and profile_data.get('following_count', 0) == 0:
                print("⚠️ WARNING: Twitter API returned zero data - profile might not exist or API issue")
            
            return profile_data
            
        elif platform == 'facebook':
            api = FacebookAPI()
            profile_data = api.get_profile_info(username)
            profile_data['platform'] = platform
            profile_data['profile_url'] = profile_url
            return profile_data
            
        else:
            # For unsupported platforms
            return {
                'username': username,
                'platform': platform,
                'profile_url': profile_url,
                'bio': '',
                'followers_count': 0,
                'following_count': 0,
                'posts_count': 0,
                'is_verified': False,
                'profile_picture': False,
                'location': '',
                'account_age_days': 365,
                'recent_posts': [],
                'api_success': False,
                'api_data_source': 'Platform not supported'
            }
            
    except Exception as e:
        print(f"❌ Error in get_real_profile_data: {str(e)}")
        return {
            'username': username,
            'platform': platform,
            'profile_url': profile_url,
            'bio': '',
            'followers_count': 0,
            'following_count': 0,
            'posts_count': 0,
            'is_verified': False,
            'profile_picture': False,
            'location': '',
            'account_age_days': 365,
            'recent_posts': [],
            'api_success': False,
            'api_data_source': 'Error fetching data'
        }

@login_required
@csrf_exempt
def report_profile(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                profile_url = data.get('profile_url')
                platform = data.get('platform')
                reason = data.get('reason')
            else:
                profile_url = request.POST.get('profile_url')
                platform = request.POST.get('platform')
                reason = request.POST.get('reason')
            
            if not profile_url or not reason:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
            
            if not platform:
                platform = extract_platform_from_url(profile_url)
            
            report = Report.objects.create(
                user=request.user,
                profile_url=profile_url,
                platform=platform,
                reason=reason
            )
            
            # Update user stats
            user_stats, created = UserStats.objects.get_or_create(user=request.user)
            user_stats.reports_filed += 1
            user_stats.save()
            
            return JsonResponse({'status': 'success', 'report_id': report.id})
            
        except Exception as e:
            print(f"❌ Error in report_profile: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})