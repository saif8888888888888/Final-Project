from django.contrib import admin
from .models import UserStats

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_scans', 'fake_profiles_detected', 'genuine_profiles', 'reports_filed')
    list_filter = ('user',)
    search_fields = ('user__username',)