from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from detection.models import ProfileScan, Report
from .models import UserStats

@login_required
def dashboard_overview(request):
    # Get user's scan history
    user_scans = ProfileScan.objects.filter(user=request.user)
    user_reports = Report.objects.filter(user=request.user)
    
    # Get or create user stats
    user_stats, created = UserStats.objects.get_or_create(user=request.user)
    
    # Platform distribution
    platform_distribution = user_scans.values('platform').annotate(
        count=Count('platform')
    )
    
    # Result distribution
    result_distribution = user_scans.values('result').annotate(
        count=Count('result')
    )
    
    context = {
        'total_scans': user_scans.count(),
        'fake_profiles': user_scans.filter(result='fake').count(),
        'genuine_profiles': user_scans.filter(result='genuine').count(),
        'suspicious_profiles': user_scans.filter(result='suspicious').count(),
        'reports_filed': user_reports.count(),
        'recent_scans': user_scans[:10],
        'platform_distribution': list(platform_distribution),
        'result_distribution': list(result_distribution),
        'user_stats': user_stats,
    }
    
    return render(request, 'dashboard/overview.html', context)

@login_required
def scan_history(request):
    user_scans = ProfileScan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/scan_history.html', {'scans': user_scans})