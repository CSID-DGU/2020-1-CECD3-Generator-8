from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Log(models.Model): # Model for Logs displayed in main page.
    STATUS_CHOICES = (
        ('OP', 'Operational'),
        ('TE', 'Temporary Error'),
        ('BR', 'Broken'),
        ('ND', 'Not Defined')
    ) # Has 4 sensor status choices

    sensor_name = models.CharField(max_length=10, db_index=True, primary_key=True)
    updated_time = models.DateTimeField(default=timezone.now)
    status=models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='ND'
    )

class Building(models.Model): # Model for Building list displayed in main page.
    building_name = models.CharField(max_length=15, primary_key=True)
    levels = models.IntegerField()
"""
class Level(models.Model):
    level_id = models.CharField(max_length=10, db_index=True, primary_key=True)
    level_num = models.IntegerField()
    img_file_path = models.CharField(max_length=200)

class Sensor(models.Model):
    sensor_id = models.CharField(max_length=10, db_index=True, primary_key=True)
    sensor_type = models.CharField(max_length=2, choice = TYPE_CHOICES)
    TYPE_CHOICES = (
        ('IG','Intergration'),
        ('RD','Radar'),
        ('RF','RF')
    )
"""