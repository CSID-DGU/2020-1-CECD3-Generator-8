from django.urls import path
from django.shortcuts import redirect
from django.conf.urls.static import static 
from django.conf import settings
from . import views

urlpatterns = [
    path('', lambda request: redirect('dashboard', permanent=True)),
    path('signup', views.signup, name='user_signup'),
    path('login', views.signin, name='user_login'),
    path('logout', views.signout, name='user_logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/export', views.dashboard_export, name='export_file_dashboard'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('monitoring/export', views.monitoring_export, name='export_file_monitoring'),
    path('monitoring/process/getcheckinfo/<int:log_id>', views.monitoring_process_get_check, name='monitoring_process_get_check'),
    path('monitoring/process/download/all', views.monitoring_process_download_all, name='monitoring_process_download_all'),
    path('monitoring/process/download/<int:log_id>', views.monitoring_process_download_onerow, name='monitoring_process_download_onerow'),
    path('monitoring/process/update/all', views.monitoring_process_update_all, name='monitoring_process_update_all'),
    path('monitoring/process/update/<int:log_id>', views.monitoring_process_update_onerow, name='monitoring_process_update_onerow'),
    path('monitoring/delete/all', views.monitoring_delete_all_rows, name='monitoring_delete_allrows'),
    path('monitoring/delete/<int:log_id>', views.monitoring_delete_one_row, name='monitoring_delete_onerow'),  # delete monitoring row
    path('monitoring/delete/from_database', views.monitoring_delete_from_database,name='delete_from_database'), #delete from database
    path('<int:b_id>/<slug:l_num>/', views.floor, name='floor'),
    path('sme20u/<slug:sensor_code>/json', views.get_sme20u_data_in_json, name='json'),  # http response url (센서의 전체 데이터 제공)
    path('sme20u/<slug:sensor_code>/json/days/<int:days>', views.get_sme20u_data_in_json_days, name='json'),  # http response url (센서의 특정 일까지의 데이터 제공)
    path('download/<str:filepath>/as/<str:client_filename>', views.download_file),
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
