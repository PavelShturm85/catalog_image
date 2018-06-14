from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ImageList.as_view(), name='image_list'),
    path('upload/', views.UploadImage.as_view(), name='upload_image'),
    path('<pk>/', views.EditImage.as_view(), name='edit_image'),
]
