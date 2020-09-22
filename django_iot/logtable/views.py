from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max
from .models import Log, Sensor
from .tables import LogTableQuerySet, MonitoringTableQuerySet
from urllib.request import urlopen  # crawler
from bs4 import BeautifulSoup  # crawler


def dashboard(request):
    logs = Log.objects.raw(
        'SELECT "logtable_log"."id", "logtable_log"."sensor_id", "logtable_log"."updated_time" FROM "logtable_log" GROUP BY "sensor_id"')
    table = LogTableQuerySet(logs)  # make a table by logs
    # render table
    return render(request, 'logtable/dashboard.html', {'table': table})

def dashboard_export(request):
    logs = Log.objects.raw(
        'SELECT "logtable_log"."id", "logtable_log"."sensor_id", "logtable_log"."updated_time" FROM "logtable_log" GROUP BY "sensor_id"')
    table = LogTableQuerySet(logs)  # make a table by logs
    # render table
    print("Export it")
    html = urlopen("http://127.0.0.1:8000/dashboard")
    Datas = BeautifulSoup(html, 'html.parser')
    tb = Datas.find('div', {'class': 'table-responsive'})
    data = []
    for tr in tb.find_all('tr'):
        print("tr")
        tds = list(tr.find_all('td'))
        if not tds:
            pass
        else:
            ID = tds[0].text
            SCode = tds[1].text
            SName = tds[2].text
            SType = tds[3].text
            UpdatedTime = tds[4].text
            SStatus = tds[5].text

            data.append([ID, SCode, SName, SType, UpdatedTime, SStatus])
    with open('datas_dashboard.csv', 'w') as file:
        file.write(
            'ID,SensorCode,SensorName,SensorType,UpdatedTime0,SensorStatus\n')
        print("make file")
        for i in data:
            file.write('{0},{1},{2},{3},{4},{5}\n'.format(
                i[0], i[1], i[2], i[3], i[4], i[5]))

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


def monitoring_export(request):
    sensors_with_problems = Sensor.objects.filter(is_handled='False')
    table = MonitoringTableQuerySet(
        sensors_with_problems)  # make a table by sensor queryset
    # render table
    print("Export it")
    html = urlopen("http://127.0.0.1:8000/monitoring")
    Datas = BeautifulSoup(html, 'html.parser')
    tb = Datas.find('div', {'class': 'table-responsive'})
    data = []
    for tr in tb.find_all('tr'):
        print("tr")
        tds = list(tr.find_all('td'))
        if not tds:
            pass
        else:
            ID = tds[0].text
            SCode = tds[1].text
            SName = tds[2].text
            SType = tds[3].text
            UpdatedTime = tds[4].text
            SStatus = tds[5].text

            data.append([ID, SCode, SName, SType, UpdatedTime, SStatus])
    with open('datas_monitoring.csv', 'w') as file:
        file.write(
            'ID,SensorCode,SensorName,SensorType,UpdatedTime0,SensorStatus\n')
        print("make file")
        for i in data:
            file.write('{0},{1},{2},{3},{4},{5}\n'.format(
                i[0], i[1], i[2], i[3], i[4], i[5]))

    return render(request, 'logtable/monitoring.html', {'table': table})
