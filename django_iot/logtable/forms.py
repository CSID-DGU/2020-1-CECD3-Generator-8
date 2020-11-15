from django import forms
from django.contrib.auth.models import User
from .models import FaultLog

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class MonitoringProcessForm(forms.ModelForm):
    class Meta:
        model = FaultLog
        fields = ['is_handled', 'is_reported']