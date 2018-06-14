
from .forms import UploadPictureForm, EditPictureForm
from .models import Picture
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import os
from PIL import Image
import requests
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
        pic_url = form.cleaned_data['url']
        pic_img = form.cleaned_data['img']
        picture = Picture()
        name = "{}.jpeg".format(str(picture.id))

        if pic_img and not pic_url:
            picture.img.save(name, pic_img, save=False)

        elif pic_url and not pic_img:
            response = requests.get(pic_url)

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

    def resize_image(self, width, height, quality):
        context = self.get_context_data()
        picture = context['picture']
        image = Image.open(picture.img)

        if width or height:
            new_size = self.get_new_size(
                image, width, height)
            image = image.resize(new_size, Image.ANTIALIAS)

        if not quality:
            quality = 100

        path_to_file = os.path.join(
            settings.MEDIA_ROOT, "uploads/", picture.name_image)

        image.save(path_to_file,
                   quality=quality, optimize=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture'] = get_object_or_404(Picture, pk=self.kwargs['pk'])
        return context

    def get(self, request, pk):
        if request.GET.get('width') or request.GET.get('height') or request.GET.get('quality'):
            img_property = {}

            for key in ('width', 'height', 'quality'):

                if request.GET.get(key):
                    img_property[key] = int(request.GET[key])
                else:
                    img_property[key] = None

            self.resize_image(**img_property)
            return redirect(self.success_url)
        else:
            return super().get(request, pk)

    def form_valid(self, form):
        self.resize_image(**form.cleaned_data)
        return redirect(self.success_url)
