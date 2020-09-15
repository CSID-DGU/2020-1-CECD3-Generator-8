from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('json', views.json, name='json'),
]
