from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max, Subquery, Value
from .models import *
from .tables import LogTableQuerySet, MonitoringTableQuerySet
import mimetypes
import json
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import UserForm, LoginForm, MonitoringProcessForm
from datetime import datetime, timedelta
import djqscsv.djqscsv as djqscsv  # NOQA
from djqscsv._csql import SELECT, EXCLUDE, AS, CONSTANT  # NOQA
from djqscsv import render_to_csv_response
import pandas as pd

def download_file(request, filepath, client_filename):
    # fill these variables with real values
    fl = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % client_filename
    return response

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
    # Export all Sensor datas to csv
    qs = Sensor.objects.all().values(
        'pk',
        'sensor_code',
        'sensor_model__name',
        'sensor_model__sensor_type',
        'updated_time',
        'sensor_status',
        'level__building_id__building_name',
        'level__level_num',
    )
    return render_to_csv_response(qs)

def get_sme20u_data_in_json_days(request, sensor_code, days):
    present_time = datetime.now()
    THRESHOLD_DAYS = days
    threshold_time = present_time - timedelta(days=THRESHOLD_DAYS)
    no_logs_in_ndays = False

    sme20u_qs = SME20U_Value.objects.filter(log_ptr__sensor__sensor_code=sensor_code).filter(log_ptr__updated_time__gte=threshold_time)
    if sme20u_qs.count() == 0:
        # no such value
        last_log_pk = SME20U_Value.objects.filter(log_ptr__sensor__sensor_code=sensor_code).latest('updated_time').pk
        sme20u_qs = SME20U_Value.objects.filter(pk=last_log_pk)
        no_logs_in_ndays = True
        

    sme20u_df = pd.DataFrame.from_records(sme20u_qs.values())
    print(sme20u_df)
    log_qs = Log.objects.filter(sensor__sensor_code=sensor_code).filter(updated_time__gte=threshold_time)
    if no_logs_in_ndays:
        last_log_pk = Log.objects.filter(sensor__sensor_code=sensor_code).latest('updated_time').pk
        log_qs = Log.objects.filter(pk=last_log_pk)
    log_df = pd.DataFrame.from_records(log_qs.values())
    merged_df = pd.merge(sme20u_df, log_df)
    
    json_data = merged_df.to_json(orient='records')
    return HttpResponse(json_data, content_type="text/json-comment-filtered")

def get_sme20u_data_in_json(request, sensor_code):
    data = SME20U_Value.objects.filter(log_ptr__sensor__sensor_code=sensor_code)
    all_objects = [*data, *Log.objects.filter(sensor__sensor_code=sensor_code)]
    json_data = serializers.serialize('json', data)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")

def monitoring(request):
    building = Building.objects.exclude(levels=0)
    level = Level.objects.all()
    logs_with_problems = FaultLog.objects.filter(is_handled=False)
    table = MonitoringTableQuerySet(
        logs_with_problems)  # make a table by sensor queryset
    # render table
    return render(request, 'logtable/monitoring.html', {
        'table': table,
        'building':building,
        'level':level,
    })

#method for crawling monitoring page
def monitoring_export(request):
    # Export all FaultLog datas to csv
    qs = FaultLog.objects.all().values(
        'log_ptr__sensor__level__building_id__building_name',
        'log_ptr__sensor__level__level_num',
        'log_ptr__sensor__sensor_code',
        'log_ptr__sensor__sensor_model__name',
        'log_ptr__sensor__sensor_model__sensor_type',
        'log_ptr__updated_time',
        'fault_status'
        )
    return render_to_csv_response(qs, filename="monitoring")

def monitoring_process_download_onerow(request, log_id):
    # Exported unreported FaultLog datas to csv
    qs = FaultLog.objects.filter(pk=log_id).values(
        'log_ptr__sensor__level__building_id__building_name',
        'log_ptr__sensor__level__level_num',
        'log_ptr__sensor__sensor_code',
        'log_ptr__sensor__sensor_model__name',
        'log_ptr__sensor__sensor_model__sensor_type',
        'log_ptr__updated_time',
        'fault_status'
        )
    return render_to_csv_response(qs, filename="faultlog_" + str(log_id))

def monitoring_process_download_all(request):
    # Exported unreported FaultLog datas to csv
    qs = FaultLog.objects.filter(is_handled='False').values(
        'log_ptr__sensor__level__building_id__building_name',
        'log_ptr__sensor__level__level_num',
        'log_ptr__sensor__sensor_code',
        'log_ptr__sensor__sensor_model__name',
        'log_ptr__sensor__sensor_model__sensor_type',
        'log_ptr__updated_time',
        'fault_status'
        )
    return render_to_csv_response(qs, filename="faultlogs_unreported")

def monitoring_process_get_check(request, log_id):
    json_data = serializers.serialize('json', FaultLog.objects.filter(pk=log_id), fields=('is_reported', 'is_handled'))
    return HttpResponse(json_data, content_type="text/json-comment-filtered")

def str_on_to_bool(result):
    if result == 'on':
        return 'True'
    else:
        return 'False'

def monitoring_process_update_all(request):
    if request.method == 'POST':
        form = MonitoringProcessForm(request.POST)
        if form.is_valid():
            reported = request.POST.get('reported', 'False')
            handled = request.POST.get('handled', 'False')
            updated_logs = FaultLog.objects.filter(is_handled='False')

            updated_logs.update(is_reported=str_on_to_bool(reported))
            updated_logs.update(is_handled=str_on_to_bool(handled))
            return redirect('monitoring')
    else:
        form = MonitoringProcessForm()
    return redirect('monitoring')

def monitoring_process_update_onerow(request, log_id):
    if request.method == 'POST':
        form = MonitoringProcessForm(request.POST)
        if form.is_valid():
            reported = request.POST.get('reported', 'False')
            handled = request.POST.get('handled', 'False')
            log = FaultLog.objects.get(pk=log_id)

            log.is_reported=str_on_to_bool(reported)
            log.is_handled = str_on_to_bool(handled)
            log.save()
            return redirect('monitoring')
    else:
        form = MonitoringProcessForm()
    return redirect('monitoring')

def monitoring_delete_one_row(request, log_id):
    # check is_handled of requested sensor
    deleting_log = FaultLog.objects.get(pk=log_id)
    deleting_log.is_handled = 'True'
    deleting_log.save()
    return redirect('monitoring')

def monitoring_delete_all_rows(request):
    # check is_handled of all sensors
    logs = FaultLog.objects.filter(is_handled='False')
    logs.update(is_handled='True')
    return redirect('monitoring')

def monitoring_delete_from_database(request):
    # check is_handled of all sensors
    logs = FaultLog.objects.filter(is_handled='False')
    logs.delete()
    return redirect('monitoring')

def floor(request,b_id,l_num):
    level_info = Level.objects.filter(building_id=b_id, level_num=l_num)
    sensor1 =Sensor.objects.filter(level__in=Subquery(Level.objects.filter(building_id=b_id, level_num=l_num).values('id')))
    building = Building.objects.exclude(levels=0)
    building_name= building.filter(id=b_id)
    levels = str(list(level_info.values())[0])#level_info JSON text
    sensor_infos = list(sensor1.values())
    for i in range(0,len(sensor_infos)):
        del sensor_infos[i]['updated_time']
        
    return render(request, 'logtable/floor.html', {
        'level_info':level_info,
        'levels':levels,#level_info JSON test
        'sensor':sensor1,
        'building':building,
        'bname':building_name,
        'sensor_info':sensor_infos,
    })
