import django_tables2 as tables
from .models import Log

class LogTable(tables.Table):
    class Meta:
        model = Log
        template_name = "django_tables2/bootstrap.html"