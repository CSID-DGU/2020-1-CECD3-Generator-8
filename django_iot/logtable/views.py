from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max
from .models import Log, Sensor
from .tables import LogTableQuerySet, MonitoringTableQuerySet


def dashboard(request):
    logs = Log.objects.raw(
        'SELECT "logtable_log"."id", "logtable_log"."sensor_id", "logtable_log"."updated_time" FROM "logtable_log" GROUP BY "sensor_id"')
    table = LogTableQuerySet(logs)  # make a table by logs
    # render table
    return render(request, 'logtable/dashboard.html', {'table': table})


def json(request):
    logs = Log.objects.all()  # get all logs
    log_list = serializers.serialize('json', logs)
    return HttpResponse(log_list, content_type="text/json-comment-filtered")


def monitoring(request):
    sensors_with_problems = Sensor.objects.filter(is_handled='False')
    table = MonitoringTableQuerySet(
        sensors_with_problems)  # make a table by sensor queryset
    # render table
    return render(request, 'logtable/monitoring.html', {'table': table})
