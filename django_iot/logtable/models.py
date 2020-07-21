from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Log(models.Model):
    STATUS_CHOICES = (
        ('OP', 'Operational'),
        ('TE', 'Temporary Error'),
        ('BR', 'Broken'),
        ('ND', 'Not Defined')
    )

    sensor_name = models.CharField(max_length=10, db_index=True, primary_key=True)
    updated_time = models.DateTimeField(default=timezone.now)
    status=models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='ND'
    )