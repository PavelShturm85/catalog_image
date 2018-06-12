from django.shortcuts import render_to_response, redirect, get_object_or_404
from .models import Picture
from .forms import UploadPictureForm, EditPictureForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.utils import timezone
from urllib.parse import urlparse
import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.views.generic.edit import CreateView, FormView
# Create your views here.


class ImageList(TemplateView):
    template_name = 'resize_image/image_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_list'] = Picture.objects.all().order_by('-upload_time')
        return context


class UploadImage(FormView):
    form_class = UploadPictureForm
    template_name = 'resize_image/upload_image.html'
    success_url = reverse_lazy('image_list')

    def form_valid(self, form):
        data = form.cleaned_data
        if data['img'] and not data['url']:
            self.object = Picture.objects.create(
                upload_time=timezone.now(),
                img=data['img'],
                name_image=data['name_image'],)

        elif data['url'] and not data['img']:
            pic_url = data['url']
            name = urlparse(pic_url).path.split('/')[-1]
            response = requests.get(pic_url)
            picture = Picture()
            if response.status_code == 200:
                picture.img.save(name, ContentFile(
                    response.content), save=False)
                picture.upload_time = timezone.now()
                picture.name_image = name
                picture.save()

        return redirect(self.success_url)


class EditImage(FormView):
    template_name = 'resize_image/edit_image.html'
    form_class = EditPictureForm
    success_url = reverse_lazy('image_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture'] = get_object_or_404(Picture, pk=self.kwargs['pk'])
        return context

    def get_new_size(self, original_image, new_width, new_height):

        width_original, height_original = original_image.size
        if new_width and new_height:
            new_size = (new_width, new_height)
        elif new_width:
            height = int(new_width * height_original / width_original)
            new_size = (new_width, height)
        elif new_height:
            width = int(new_height * width_original / height_original)
            new_size = (width, new_height)
        return new_size

    def form_valid(self, form):
        context = self.get_context_data()
        picture = context['picture']
        data = form.cleaned_data
        image = Image.open(picture.img)
        if data['image_w'] or data['image_h']:
            new_size = self.get_new_size(
                image, data['image_w'], data['image_h'])
            image = image.resize(new_size, Image.ANTIALIAS)

        if data['image_quality']:
            quality = data['image_quality']
        else:
            quality = 100

        image.save(picture.name_image,
                   quality=quality, optimize=True)
        return redirect(self.success_url)
