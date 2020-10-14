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
from logtable.models import Log, Sensor

class Analyzer(ABC):
    @abstractmethod
    def update(self, log, time):
        pass

class SimpleAnalyzer(Analyzer):
    def update(self, log, time):
        logtime = log.updated_time
        sensor = log.sensor
        operational_period = sensor.sensor_model.period

        
        elapsed_time = time - logtime;
        diff = elapsed_time.total_seconds()
        if diff <= operational_period + 3:
            # 정상 작동
            sensor.sensor_status = 'OP'
            sensor.is_handled = True
        elif diff <= operational_period * 3:
            sensor.sensor_status = 'TE'
        else:
            sensor.sensor_status = 'BR'
        sensor.save()