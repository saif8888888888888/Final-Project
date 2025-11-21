from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_scans = models.IntegerField(default=0)
    fake_profiles_detected = models.IntegerField(default=0)
    genuine_profiles = models.IntegerField(default=0)
    reports_filed = models.IntegerField(default=0)
    last_scan_date = models.DateTimeField(null=True, blank=True)
    
    def update_stats(self, scan_result):
        self.total_scans += 1
        if scan_result == 'fake':
            self.fake_profiles_detected += 1
        elif scan_result == 'genuine':
            self.genuine_profiles += 1
        self.last_scan_date = timezone.now()
        self.save()
    
    def __str__(self):
        return f"Stats for {self.user.username}"