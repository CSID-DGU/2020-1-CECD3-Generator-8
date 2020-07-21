from django.shortcuts import render
from .models import Log
import django_tables2 as tables

class LogTable(tables.Table):
    class Meta:
        model = Log

# Create your views here.
def log_list(request):
    logs = Log.objects.all()
    table = LogTable(logs)
    return render(request, 'logtable/log_list.html', {'table':table})