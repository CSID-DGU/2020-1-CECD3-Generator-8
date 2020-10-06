from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Building, Level, Log, Sensor, DeviceModel

# Register your models here.
@admin.register(Log)
class LogAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Building)
admin.site.register(Level)
admin.site.register(Sensor)
admin.site.register(DeviceModel)