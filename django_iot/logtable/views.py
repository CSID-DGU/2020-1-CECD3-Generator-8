from django.shortcuts import render
from .models import Log
from .tables import LogTable

def dashboard(request):
    logs = Log.objects.all() # get all logs
    table = LogTable(logs) # make a table by logs
    return render(request, 'logtable/dashboard.html', {'table':table}) # render table