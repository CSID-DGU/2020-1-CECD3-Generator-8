import django_tables2 as tables
from .models import Log, Sensor

# td tag에 chartDGU000n 형식으로 id를 달아줌
def chart_id(**kwargs):
    sensor_code = kwargs.get("record", None)
    return "chart" + str(sensor_code)

def monitoring_id(**kwargs):
    sensor_code = kwargs.get("record", None)
    return "monitor" + str(sensor_code)

class LogTableQuerySet(tables.Table):
    sensor_type_column = tables.Column(
        accessor='get_sensor_type', verbose_name='Sensor Type')
    action = tables.TemplateColumn(template_name='tables/dashboard_action_column.html', attrs={"td": {"id": chart_id}})

    class Meta:
        fields = ['id', 'sensor_code', 'sensor_model', 'sensor_type_column', 'updated_time', 'sensor_status', 'action']
        model = Sensor
        template_name = "django_tables2/bootstrap.html"


class MonitoringTableQuerySet(tables.Table):
    sensor_type_column = tables.Column(
        accessor='get_sensor_type', verbose_name='Sensor Type')
    action = tables.TemplateColumn(template_name='tables/monitoring_action_column.html', attrs={"td": {"id": monitoring_id}})

    class Meta:
        fields = ['id', 'sensor_code', 'sensor_model',
                  'sensor_type_column', 'updated_time', 'sensor_status', 'action']
        model = Sensor
        template_name = "django_tables2/bootstrap.html"
