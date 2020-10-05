from abc import ABC, abstractmethod
from logtable.models import Log, Sensor

class Analyzer(ABC):
    @abstractmethod
    def update(self, log):
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
        elif diff <= operational_period * 3:
            sensor.sensor_status = 'TE'
        else:
            sensor.sensor_status = 'BR'
        sensor.save()