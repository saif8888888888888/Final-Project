from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileScan(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
    ]
    
    RESULT_CHOICES = [
        ('fake', 'Fake'),
        ('genuine', 'Genuine'),
        ('suspicious', 'Suspicious'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_url = models.URLField(max_length=500)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    additional_context = models.TextField(blank=True)
    risk_score = models.IntegerField(default=0)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    risk_factors = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.profile_url} - {self.result}"

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('action_taken', 'Action Taken'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_url = models.URLField(max_length=500)
    platform = models.CharField(max_length=20)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.profile_url}"