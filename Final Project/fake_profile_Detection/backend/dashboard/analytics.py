import json
from datetime import datetime, timedelta
from django.db.models import Count
from detection.models import ProfileScan

class DashboardAnalytics:
    @staticmethod
    def get_user_stats(user):
        """Get comprehensive stats for a user"""
        scans = ProfileScan.objects.filter(user=user)
        
        return {
            'total_scans': scans.count(),
            'fake_count': scans.filter(result='fake').count(),
            'genuine_count': scans.filter(result='genuine').count(),
            'suspicious_count': scans.filter(result='suspicious').count(),
            'platform_breakdown': list(scans.values('platform').annotate(count=Count('platform'))),
            'weekly_activity': DashboardAnalytics.get_weekly_activity(user),
        }
    
    @staticmethod
    def get_weekly_activity(user):
        """Get user activity for the past week"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        daily_counts = []
        for i in range(7):
            day = start_date + timedelta(days=i)
            count = ProfileScan.objects.filter(
                user=user,
                created_at__date=day.date()
            ).count()
            daily_counts.append({
                'date': day.strftime('%Y-%m-%d'),
                'count': count
            })
        
        return daily_counts
    
    @staticmethod
    def get_platform_insights(user):
        """Get insights about different platforms"""
        scans = ProfileScan.objects.filter(user=user)
        platform_data = {}
        
        for platform in ['instagram', 'facebook', 'twitter', 'tiktok']:
            platform_scans = scans.filter(platform=platform)
            total = platform_scans.count()
            if total > 0:
                fake_percentage = (platform_scans.filter(result='fake').count() / total) * 100
                platform_data[platform] = {
                    'total': total,
                    'fake_percentage': round(fake_percentage, 2),
                    'genuine_percentage': round((platform_scans.filter(result='genuine').count() / total) * 100, 2)
                }
        
        return platform_data