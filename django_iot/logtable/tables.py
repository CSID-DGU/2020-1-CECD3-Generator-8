import django_tables2 as tables
from .models import LogView

class LogTable(tables.Table):
    class Meta:
        model = LogView
        template_name = "django_tables2/bootstrap.html"

"""
class Log(models.Model): # Model for Logs displayed in main page.
    STATUS_CHOICES = (
        ('OP', 'Operational'),
        ('TE', 'Temporary Error'),
        ('BR', 'Broken'),
        ('ND', 'Not Defined')
    ) # Has 4 sensor status choices
    sensor_name = models.CharField(max_length=10, db_index=True, primary_key=True)
    updated_time = models.DateTimeField(default=timezone.now)
    sensor_id = models.ForeignKey('Sensor',on_delete=models.CASCADE)
    status=models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='ND'
    )
"""