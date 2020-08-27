from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max
from .models import Log
from .tables import LogTableQuerySet

def dashboard(request):
    logs = Log.objects.raw('SELECT "logtable_log"."id", "logtable_log"."sensor_id", "logtable_log"."updated_time" FROM "logtable_log" GROUP BY "sensor_id"')
    table = LogTableQuerySet(logs) # make a table by logs
    return render(request, 'logtable/dashboard.html', {'table':table}) # render table

def json(request):
    logs = Log.objects.all() # get all logs
    log_list = serializers.serialize('json', logs)
    return HttpResponse(log_list, content_type="text/json-comment-filtered")