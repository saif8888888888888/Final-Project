from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_overview, name='dashboard'),
    path('history/', views.scan_history, name='scan_history'),
]