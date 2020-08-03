from django.contrib import admin
from .models import Building, Level, Log, Sensor

# Register your models here.
admin.site.register(Log)
admin.site.register(Building)
admin.site.register(Level)
admin.site.register(Sensor)