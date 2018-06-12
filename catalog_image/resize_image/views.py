from django.shortcuts import render_to_response, redirect
from .models import Picture
from .forms import UploadPictureForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.utils import timezone
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from django.views.generic.edit import CreateView, FormView
# Create your views here.


def image_list(request):
    image_list = Picture.objects.all().order_by('-upload_time')

    return render_to_response(
        'resize_image/image_list.html', {
            'image_list': image_list,
        }
    )


class UploadImage(FormView):
    form_class = UploadPictureForm
    template_name = 'resize_image/upload_image.html'
    success_url = reverse_lazy('image_list')
    
    def form_valid(self, form):
        if form.cleaned_data['img'] and not form.cleaned_data['url']:
            self.object = Picture.objects.create(
                upload_time = timezone.now(),
                img = form.cleaned_data['img'],
                name_image = form.cleaned_data['name_image'],)

        if form.cleaned_data['url'] and not form.cleaned_data['img']:
            pic_url = form.cleaned_data['url']
            name = urlparse(pic_url).path.split('/')[-1]
            response = requests.get(pic_url)
            picture = Picture()
            if response.status_code == 200:
                picture.img.save(name, ContentFile(response.content), save=False)
                picture.upload_time = timezone.now()
                picture.name_image = name
                picture.save()

        
        return redirect(self.success_url)



