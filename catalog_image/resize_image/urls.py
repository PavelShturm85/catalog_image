#from django.conf.urls import url
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.UploadImage.as_view(), name='upload_image'),
    
]


