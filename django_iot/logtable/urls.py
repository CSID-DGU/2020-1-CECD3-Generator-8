from django.urls import path
from django.shortcuts import redirect
from django.conf.urls.static import static 
from django.conf import settings
from . import views

urlpatterns = [
    path('', lambda request: redirect('dashboard', permanent=True)),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/export', views.dashboard_export, name='export_file_dashboard'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('monitoring/export', views.monitoring_export,name='export_file_monitoring'),
    path('json', views.json, name='json'),
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
