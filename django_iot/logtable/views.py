from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Max, Subquery, Value
from .models import *
from .tables import LogTableQuerySet, MonitoringTableQuerySet
from urllib.request import urlopen  # crawler
from bs4 import BeautifulSoup  # crawler
import mimetypes
import json
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import UserForm, LoginForm
from datetime import datetime, timedelta

def signout(request):
    logout(request)
    return redirect('dashboard')

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request,'logtable/login_failed.html')
            #return HttpResponse('Login failed. Try again.')
    else:
        form = LoginForm()
        return render(request, 'logtable/user_login.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('dashboard')
    else:
        form = UserForm()
        return render(request, 'user_new.html')

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
    url = 'http://'+request.get_host() + '/dashboard'
    html = urlopen(url)
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
            'ID,SensorCode,SensorName,SensorType,UpdatedTime,SensorStatus\n')
        #print("make file")
        for i in data:
            file.write('{0},{1},{2},{3},{4},{5}\n'.format(
                i[0], i[1], i[2], i[3], i[4], i[5]))
    return redirect('datas_dashboard/download')

def get_sme20u_data_in_json_days(request, sensor_code, days):
    present_time = datetime.now()
    THRESHOLD_DAYS = days
    threshold_time = present_time - timedelta(days=THRESHOLD_DAYS)

    data = SME20U_Value.objects.filter(log_ptr__sensor__sensor_code=sensor_code).filter(log_ptr__updated_time__gte=threshold_time)
    all_objects = [*data, *Log.objects.filter(sensor__sensor_code=sensor_code).filter(updated_time__gte=threshold_time)]
    json_data = serializers.serialize('json', all_objects)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")

def get_sme20u_data_in_json(request, sensor_code):
    data = SME20U_Value.objects.filter(log_ptr__sensor__sensor_code=sensor_code)
    all_objects = [*data, *Log.objects.filter(sensor__sensor_code=sensor_code)]
    json_data = serializers.serialize('json', data)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")

def monitoring(request):
    building = Building.objects.exclude(levels=0)
    level = Level.objects.all()
    # sensors_with_problems = Sensor.objects.all() # 수정 필요
    # sensor_list = list(sensors_with_problems.values())
    # for i in range(0,len(sensor_list)):
    #     del sensor_list[i]['is_handled']
    #     del sensor_list[i]['updated_time']
    logs_with_problems = FaultLog.objects.all()
    table = MonitoringTableQuerySet(
        logs_with_problems)  # make a table by sensor queryset
    user_email = request.user.email
    # render table
    return render(request, 'logtable/monitoring.html', {
        'table': table,
        'building':building,
        'level':level,
        #'sensor_list': sensor_list,
        'to_email': user_email
    })

#method for crawling monitoring page
def monitoring_export(request):
    print("Export it")
    url = 'http://'+request.get_host() + '/monitoring'
    html = urlopen(url)
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
            'ID,SensorCode,SensorName,SensorType,UpdatedTime,SensorStatus\n')
        #print("make file")
        for i in data:
            file.write('{0},{1},{2},{3},{4},{5}\n'.format(
                i[0], i[1], i[2], i[3], i[4], i[5]))
    return redirect('datas_monitoring/download')


def monitoring_download_file(request,filepath):
    # fill these variables with real values
    fl_path = filepath + '.csv'
    filename = 'monitoring.csv'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def dashboard_download_file(request,filepath):
    # fill these variables with real values
    fl_path = filepath + '.csv'
    filename = 'dashboard.csv'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def monitoring_delete_one_row(request, d_sensor_code):
    # check is_handled of requested sensor
    deleting_sensor = Sensor.objects.get(sensor_code=d_sensor_code)
    deleting_sensor.is_handled = 'True'
    deleting_sensor.save()
    return redirect('monitoring')

def monitoring_delete_all_rows(request):
    # check is_handled of all sensors
    sensors_with_problems = Sensor.objects.filter(is_handled='False')
    sensors_with_problems.update(is_handled='True')
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
