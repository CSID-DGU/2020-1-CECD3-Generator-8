from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from .models import Log, Sensor,Building,Level, SME20U_Value
from .tables import LogTableQuerySet, MonitoringTableQuerySet
from urllib.request import urlopen  # crawler
from bs4 import BeautifulSoup  # crawler
from django.db.models import Subquery
from django.db.models import Value
import json


def dashboard(request):
    building = Building.objects.exclude(levels=0)
    level = Level.objects.all()
    #logs = Log.objects.raw(
    #    'SELECT "logtable_log"."id", "logtable_log"."sensor_id", "logtable_log"."updated_time" FROM "logtable_log" GROUP BY "sensor_id"')
    sensors = Sensor.objects.order_by('sensor_code')
    table = LogTableQuerySet(sensors)  # make a table by logs
    # render table
    return render(request, 'logtable/dashboard.html',{
        'table': table,
        'building':building,
        'level':level,
    })

#method for crawling dashboard page
def dashboard_export(request):
    print("Export it")
    html = urlopen("http://127.0.0.1:8000/dashboard")
    Datas = BeautifulSoup(html, 'html.parser')
    tb = Datas.find('div', {'class': 'table-responsive'})
    data = []
    for tr in tb.find_all('tr'):
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

    return redirect('dashboard')

def get_sme20u_data_in_json(request, sensor_code):
    data = SME20U_Value.objects.filter(sensor__sensor_code=sensor_code)
    json_data = serializers.serialize('json', data)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")


def monitoring(request):
    building = Building.objects.exclude(levels=0)
    level = Level.objects.all()
    sensors_with_problems = Sensor.objects.filter(is_handled='False')
    table = MonitoringTableQuerySet(
        sensors_with_problems)  # make a table by sensor queryset
    # render table
    return render(request, 'logtable/monitoring.html', {
        'table': table,
        'building':building,
        'level':level,
    })

#method for crawling monitoring page
def monitoring_export(request):
    print("Export it")
    html = urlopen("http://127.0.0.1:8000/monitoring")
    Datas = BeautifulSoup(html, 'html.parser')
    tb = Datas.find('div', {'class': 'table-responsive'})
    data = []
    for tr in tb.find_all('tr'):
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

    return redirect('monitoring')

def floor(request,b_id,l_num):
    level_info = Level.objects.filter(building_id=b_id, level_num=l_num)
    sensor1 =Sensor.objects.filter(level__in=Subquery(Level.objects.filter(building_id=b_id, level_num=l_num).values('id')))
    building = Building.objects.exclude(levels=0)
    building_name= building.filter(id=b_id)
    levels = str(list(level_info.values())[0])#level_info JSON text
    sensor_infos = list(sensor1.values())
    for i in range(0,len(sensor_infos)):
        del sensor_infos[i]['is_handled']
        del sensor_infos[i]['updated_time']
        
    return render(request, 'logtable/floor.html', {
        'level_info':level_info,
        'levels':levels,#level_info JSON test
        'sensor':sensor1,
        'building':building,
        'bname':building_name,
        'sensor_info':sensor_infos,
    })
