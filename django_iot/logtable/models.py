from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


# Create your models here.

class Building(models.Model): # Model for Building list displayed in main page.
    building_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    building_name = models.CharField(max_length=15)
    levels = models.IntegerField()

class Level(models.Model):
    level_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    level_num = models.IntegerField()
    img_file_path = models.CharField(max_length=200)
    building_id = models.ForeignKey('Building', on_delete=models.CASCADE)

class Sensor(models.Model):
    TYPE_CHOICES = (
        ('IG','Intergration'),
        ('RD','Radar'),
        ('RF','RF')
    )
    STATUS_CHOICES = (
        ('OP', 'Operational'),
        ('TE', 'Temporary Error'),
        ('BR', 'Broken'),
        ('ND', 'Not Defined')
    ) # Has 4 sensor status choices
    sensor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    sensor_type = models.CharField(max_length=2, choices = TYPE_CHOICES)
    sensor_status=models.CharField(max_length=2, choices=STATUS_CHOICES, default='ND')
    level_id = models.ForeignKey('Level', on_delete=models.CASCADE)
    #position = models.CommaSeparatedIntegerField(max_length=10)

# class recent_Log(Log):
#     pass

class Log(models.Model): # Model for Logs displayed in main page.
    log_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=10, db_index=True )
    updated_time = models.DateTimeField(default=timezone.now)
    sensor_id = models.ForeignKey('Sensor',on_delete=models.CASCADE)
    
