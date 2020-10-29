from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


# Create your models here.

# Model for Building list displayed in main page.
class Building(models.Model):
    # Fields
    building_name = models.CharField(max_length=15,default="신공학관") # Name of Building.
    levels = models.IntegerField()  # Number of floors in the building.
    # Metadata

    class Meta:
        #ordering = ['building_id']
        ordering = ['building_name']

    # Methods
    # basic methods
    def __str__(self):
        return self.building_name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])


# Model for  floor of Buildings list diplayed in main mage.
class Level(models.Model):
    # Fields
    level_num = models.CharField(max_length=10,default="1F")  # Number of floor(level).
    # Path of blueprint image of the floor.
    img_file_path = models.CharField(max_length=200,default="/static/img/map_img/default.png")
    # Foreign key. Building ID that floor is placed at(?).
    building_id = models.ForeignKey(
        'Building', on_delete=models.CASCADE, default=uuid.uuid4)
    # Metadata

    class Meta:
        ordering = ['level_num']
    # Methods

    # basic methods
    def __str__(self):
        return str(self.level_num)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

class DeviceModel(models.Model):
    # Fields
    TYPE_CHOICES = (
        ('IG', 'Intergration'),
        ('RD', 'Radar'),
        ('RF', 'RF'),
        ('UK', 'Unknown')
    )  # Type of IoT devices

    name = models.CharField(max_length=20)
    period = models.IntegerField(null=True)
    sensor_type = models.CharField(
        max_length=2, choices=TYPE_CHOICES)  # Type of IoT device

    def __str__(self):
        return self.name


class Sensor(models.Model):  # Model for IoT devices.
    STATUS_CHOICES = (
        ('OP', 'Operational'),
        ('TE', 'Temporary Error'),
        ('BR', 'Broken'),
        ('ND', 'Not Defined')
    )  # Has 4 sensor status choices
    sensor_code = models.CharField(max_length=10, unique=True, default="DGU")
    sensor_model = models.ForeignKey('DeviceModel', on_delete=models.CASCADE)
    # status that analyzed by data analyzing module.
    sensor_status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default='ND')

    is_handled = models.BooleanField(default='False')
    updated_time = models.DateTimeField(default=timezone.now)

    # Foreign key. Level ID that IoT Sensor is placed at(?)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    position_x = models.FloatField(default='-1') # Absolute position of IoT device icon in minimap.
    position_y = models.FloatField(default='-1')

    # Metadata
    class Meta:
        #ordering = ['sensor_id']
        ordering = ['sensor_code']

    # Methods
    # basic methods
    def __str__(self):
        return self.sensor_code

    def get_sensor_type(self):
        return str(self.sensor_model.sensor_type)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

class SME20U_Value(models.Model):
    sensor = models.ForeignKey(
        'Sensor', on_delete=models.CASCADE)
    updated_time = models.DateTimeField(default=timezone.now)

    # sensor specification referenced in https://documenter.getpostman.com/view/527712/SW14WcyW?version=latest#9b1079ca-8760-457f-8e38-bb8f6b8ef6ad
    temp = models.DecimalField(decimal_places=1, max_digits=3) # 온도 (-10.0 ~ +85.0 °C, ±1 °C)
    humid = models.DecimalField(decimal_places=2, max_digits=5) # 습도 (0.00 ~ 100.00 %, ±5 %RH)
    illum = models.DecimalField(decimal_places=2, max_digits=5) # 조도 (0.00 ~ 100.00 %, ±5 %CDS)
    rador = models.IntegerField() # 10분당 움직임 수 (0.00 ~ )
    last_movement_time = models.CharField(max_length=10) #	최종 움직임 감지 시간 (Unixtime +00:00) 연산 시 -9시간(9 * 60 *60)해야 한국 시간
    co2 = models.IntegerField() # Co2(0 ~ 8192 ppm)
    tvoc = models.IntegerField() #	tVOC(0 ~ 1187 ppb)

    # Methods
    def __str__(self):
        return str(self.sensor) + ": " + str(self.updated_time)
    

class Log(models.Model):  # Model for Logs.
    sensor = models.ForeignKey(
        'Sensor', on_delete=models.CASCADE, related_name='sensor')
    updated_time = models.DateTimeField(default=timezone.now)

    # Metadata
    class Meta:
        ordering = ['-id']

    # Methods
    # basic methods
    def __str__(self):
        # Ex) DGU0012: 2020-08-04 15:38:47
        return str(self.sensor.sensor_code) + ": " + str(self.updated_time)

    def get_sensor_code(self):
        return str(self.sensor.sensor_code)

    def get_sensor_model(self):
        return str(self.sensor.sensor_model)

    def get_sensor_type(self):
        return str(self.sensor.sensor_model.sensor_type)

    def get_sensor_status(self):
        return str(self.sensor.sensor_status)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    """
    값 넣는 방법 :
    ex)
        record =  MyModelName(my_field_name="Instance #1")
    
    값을 데이터베이스에 저장하는 방법:
    ex)
        record.save()
    
    모델의 필드 값에 접근하는 방법
    ex)
        print(record.id) # should return 1 for the first record.
        print(record.my_field_name)
    
    모델의 값을  변경하는 방법
    ex)
        record.my_field_name = "New Instance Name"
        record.save()

    레코드 검색하는 방법
    ex)
        all_books = Book.objects.all()
        wild_books = Book.objects.filter(title__contains='wild') #필터링하는 방법
        number_wild_books = Book.objects.filter(title__contains='wild').count() #숫자를 세는 방법.
       
        books_containing_genre = Book.objects.filter(genre__name__icontains='fiction') #다른 모델에 정의하는 필드를 필터링 해야할 때
        # 밑줄(__)을 사용하여 원하는 만큼 다양한 레벨의 관게를 탐색할 수 있다.(ForeignKey/ManyToManyField)
    """
