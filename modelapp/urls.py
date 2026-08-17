from django.urls import path
from . import views

app_name = 'modelapp'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
    path('growth/', views.growth, name='growth'),

    path('scans/save/', views.api_save_scan, name='api_save_scan'),
    path('scans/summary/', views.api_summary, name='api_summary'),
    path('scans/recent/', views.api_recent, name='api_recent'),
    path('scans/history/', views.api_history, name='api_history'),
    path('scans/trend/', views.api_trend, name='api_trend'),
    path('scans/class-distribution/', views.api_class_distribution, name='api_class_distribution'),

    path('fields/save/', views.api_save_field, name='api_save_field'),
    path('fields/', views.api_fields, name='api_fields'),
    path('fields/<int:field_id>/', views.api_field_detail, name='api_field_detail'),
    path('fields/latest/', views.api_latest_field, name='api_latest_field'),
]