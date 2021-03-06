import uuid

from django.db import models
from PIL import Image

# Create your models here.


class Picture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to='uploads')
    upload_time = models.DateTimeField(
        verbose_name='Время загрузки', blank=True, null=True)
