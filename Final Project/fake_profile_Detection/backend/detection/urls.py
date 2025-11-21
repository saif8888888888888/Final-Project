from django.urls import path
from . import views

urlpatterns = [
    path('', views.detect_profile, name='detect_profile'),
    path('report/', views.report_profile, name='report_profile'),
]