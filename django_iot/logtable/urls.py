from django.urls import path
from django.shortcuts import redirect
from django.conf.urls.static import static 
from django.conf import settings
from . import views

urlpatterns = [
    path('', lambda request: redirect('dashboard', permanent=True)),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/sme20u/<slug:sensor_code>', views.get_sme20u_data_in_json, name='json'), # http response url (센서 데이터 제공)
    path('dashboard/export', views.dashboard_export, name='export_file_dashboard'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('monitoring/export', views.monitoring_export,name='export_file_monitoring'),
    path('<int:b_id>/<slug:l_num>/', views.floor, name='floor'),
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
