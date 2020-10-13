'''
File: valuesaver.py
Project: 2020-1-CECD3-GENERATOR-8
File Created: Wednesday, 14th October 2020 12:48:57 am
Author: Jongyeon Yoon (0417yjy@naver.com)
-----
Last Modified: Wednesday, 14th October 2020 12:53:36 am
Modified By: Jongyeon Yoon (0417yjy@naver.com>)
-----
Copyright 2020 Jongyeon Yoon
'''

from abc import ABC, abstractmethod
from logtable.models import Sensor, SME20U_Value
from datetime import datetime
from decimal import Decimal

class ValueSaver(ABC):
    @abstractmethod
    def store_to_db(self, device):
        pass

class IntegratedSensorSaver(ValueSaver):
    @staticmethod
    def store_to_db(device):
        scode = device['DEVICE_SCODE']
        try:
            current_sensor = Sensor.objects.get(sensor_code=scode)
        except Sensor.DoesNotExist:
           print('Failed to get sensor: doesn\'t exist')
           return
        send_time = datetime.strptime(device['DEVICE_DATA_REG_DTM'], '%Y-%m-%d %H:%M:%S')
        new_values = SME20U_Value(
            sensor=current_sensor,
            updated_time=send_time, 
            temp = Decimal(device['DEVICE_FIELD01']),
            humid = Decimal(device['DEVICE_FIELD02']),
            illum = Decimal(device['DEVICE_FIELD03']),
            rador = int(device['DEVICE_FIELD04']),
            last_movement_time = device['DEVICE_FIELD05'],
            co2 = int(device['DEVICE_FIELD10']),
            tvoc = int(device['DEVICE_FIELD11']),
            )
        new_values.save()