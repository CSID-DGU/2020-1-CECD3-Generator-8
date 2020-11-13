'''
File: analyzer.py
Project: 2020-1-CECD3-GENERATOR-8
File Created: Tuesday, 6th October 2020 1:03:23 am
Author: Jongyeon Yoon (0417yjy@naver.com)
-----
Last Modified: Wednesday, 14th October 2020 12:53:18 am
Modified By: Jongyeon Yoon (0417yjy@naver.com>)
-----
Copyright 2020 Jongyeon Yoon
'''

from abc import ABC, abstractmethod
from logtable.models import Log, Sensor, SME20U_Value
from decimal import Decimal
from numpy import *
from django.db.models import Value
import scipy.stats as stats


class Analyzer(ABC):
    @abstractmethod
    def update(self, log, time):
        pass

class SimpleAnalyzer(Analyzer):
    def update(self, log, time):
        logtime = log.updated_time
        sensor = log.sensor
        operational_period = sensor.sensor_model.period

        
        elapsed_time = time - logtime
        diff = elapsed_time.total_seconds()
        if diff <= operational_period + 3:
            # 정상 작동
            sensor.sensor_status = 'OP'
        elif diff <= operational_period * 3:
            sensor.sensor_status = 'TE'
        else:
            sensor.sensor_status = 'BR'
        sensor.save()

class N_Sigma_Analyzer(Analyzer):
    sigma_value = 2  # default value is 2 (95%)
    
    def __init__(self, v):
        self.sigma_value = v

    def update(self, log, time, device):
        logtime = log.updated_time
        sensor = log.sensor
        operational_period = sensor.sensor_model.period
        faulty_flag = False
        
        elapsed_time = time - logtime
        diff = elapsed_time.total_seconds()
        if diff <= operational_period + 3:
            if self.StateAnalysis(sensor,device):
                sensor.sensor_status = 'OP'
                print(sensor.sensor_code,':',sensor.sensor_status)
            else:
                sensor.sensor_status = 'WN'
                print(sensor.sensor_code, ':', sensor.sensor_status)
                faulty_flag = True
            
        elif diff <= operational_period * 3:
            sensor.sensor_status = 'TE'
            faulty_flag = True
        else:
            sensor.sensor_status = 'BR'
            faulty_flag = True
        sensor.save()
    
    def StateAnalysis(self, sensor, device):
        sensor_values = SME20U_Value.objects.filter(sensor_id=sensor.id)
        sensor_values = list(sensor_values.values())

        # 각 값을 저장할 리스트
        temp_list = []
        humid_list = []
        co2_list = []
        tvoc_list = []
        
        # 각 값을 sensor_values에서 받아옴
        for log in sensor_values:
            temp_list.append(float(log['temp']))
            humid_list.append(float(log['humid']))
            co2_list.append(int(log['co2']))
            tvoc_list.append(int(log['tvoc']))
        #정렬(안해도 될지도?)
        temp_list.sort()
        humid_list.sort()
        co2_list.sort()
        tvoc_list.sort()
        
        #정규화를 하기 위해 numpy array에 담음
        data = array([temp_list,humid_list,co2_list,tvoc_list])
        #정규화를 할array 생성 위해 data copy
        normed_data = data.copy()

        #정규화 과정(x-mean())/std()
        for i in range(0,4):
            normed_data[i] = (normed_data[i]-mean(normed_data[i]))/std(normed_data[i])
        
        #device로 부터 측정 값 가져옴
        temp = round(float(Decimal(device['DEVICE_FIELD01'])),2)
        humid = round(float(Decimal(device['DEVICE_FIELD02'])),2)
        co2 = int(device['DEVICE_FIELD10'])
        tvoc = int(device['DEVICE_FIELD11'])
        #리스트에 담음
        device_values = [temp,humid,co2,tvoc]
        
        #이상값이 있는지 탐지할 flag
        flag = True

        #각 값에 대한 검사 결과를 저장 위해 bool곱셈을 함
        for i in range(0,4):
            flag*=self.is_normal_state(device_values[i],data[i],mean(normed_data[i]),std(normed_data[i]))
        # True면 이상값 없음
        if flag:
            return True
        else:
            return False

    # 상태를 판별하는 메서드
    # value : 상태를 검사할 측정한 값. data : 측정된 값의 집합. mean_normed : 정규화된 값의 mean값. std_normed : 정규화된 값의 표준편차 
    def is_normal_state(self,value,data,mean_normed,std_normed):
        normed_value = (value-mean(data))/std(data) # 측정한 값을 정규화 한다.
        
        #3-sigma 방법 사용. 입력한 n 값으로 sigma 계수 지정
        #정규화 된 값이 n-sigma 범위 밖이면 False, 아니면 True
        if (normed_value < mean_normed - self.sigma_value*std_normed) or ( normed_value > mean_normed + self.sigma_value*std_normed):
            return False
        else:
            return True










            


