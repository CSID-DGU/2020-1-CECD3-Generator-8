from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_list, name='log_list'),
]