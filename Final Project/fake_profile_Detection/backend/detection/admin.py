from django.contrib import admin
from .models import ProfileScan, Report

@admin.register(ProfileScan)
class ProfileScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_url', 'platform', 'risk_score', 'result', 'created_at')
    list_filter = ('platform', 'result', 'created_at')
    search_fields = ('profile_url', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_url', 'platform', 'status', 'created_at')
    list_filter = ('platform', 'status', 'created_at')
    search_fields = ('profile_url', 'user__username', 'reason')
    readonly_fields = ('created_at',)