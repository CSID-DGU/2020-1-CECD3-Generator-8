from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import LogView
from .tables import LogTable

def dashboard(request):
    logs = LogView.objects.all() # get all logs
    table = LogTable(logs) # make a table by logs
    return render(request, 'logtable/dashboard.html', {'table':table}) # render table

def json(request):
    logs = LogView.objects.all() # get all logs
    log_list = serializers.serialize('json', logs)
    return HttpResponse(log_list, content_type="text/json-comment-filtered")