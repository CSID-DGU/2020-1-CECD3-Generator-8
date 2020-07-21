from django.shortcuts import render
from .models import Log
from .tables import LogTable

# Create your views here.
def log_list(request):
    logs = Log.objects.all() # get all logs
    table = LogTable(logs) # make a table by logs
    return render(request, 'logtable/log_list.html', {'table':table}) # render table