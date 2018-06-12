import uuid
from PIL import Image
from django.db import models

# Create your models here.

class Picture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to = 'uploads')
    name_image = models.CharField(max_length=30, verbose_name='Название изображения', blank=True, null=True)
    upload_time = models.DateTimeField(
        verbose_name='Время загрузки', blank=True, null=True)