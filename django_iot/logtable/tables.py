import django_tables2 as tables
from .models import Log, Sensor


class LogTableQuerySet(tables.Table):
    sensor_code_column = tables.Column(
        accessor='get_sensor_code', verbose_name='Sensor Code')
    sensor_name_column = tables.Column(
        accessor='get_sensor_name', verbose_name='Sensor Name')
    sensor_type_column = tables.Column(
        accessor='get_sensor_type', verbose_name='Sensor Type')
    sensor_status_column = tables.Column(
        accessor='get_sensor_status', verbose_name='Status')

    class Meta:
        fields = ['id', 'sensor_code_column', 'sensor_name_column',
                  'sensor_type_column', 'updated_time', 'sensor_status_column']
        model = Log
        order_by = 'sensor_code_column'
        template_name = "django_tables2/bootstrap.html"


class MonitoringTableQuerySet(tables.Table):
    checkbox_column = tables.columns.CheckBoxColumn(accessor='pk')

    class Meta:
        fields = ['checkbox_column', 'id', 'sensor_code', 'sensor_name',
                  'sensor_type', 'updated_time', 'sensor_status']
        model = Sensor
        template_name = "django_tables2/bootstrap.html"
