from django import forms
from PIL import Image
from .models import Picture


class UploadPictureForm(forms.Form):

    name_image = forms.CharField(max_length=30, required=False)
    url = forms.URLField(required=False)
    img = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        img = cleaned_data.get('img')

        if (url and img) or (not url and not img):
            raise forms.ValidationError(
                'Выберите только один источник загрузки')

        return cleaned_data


class EditPictureForm(forms.Form):

    image_w = forms.IntegerField(required=False)
    image_h = forms.IntegerField(required=False)
    image_quality = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        image_w = cleaned_data.get('image_w')
        image_h = cleaned_data.get('image_h')
        image_quality = cleaned_data.get('image_quality')
        
        if (image_w and image_w < 0) or (image_h and image_h < 0):
            raise forms.ValidationError(
                'Размер должен быть положительным числом')

        
        elif image_quality and (image_quality < 1 or image_quality > 99):
            raise forms.ValidationError(
                'Качество изображения должно быть числом от 1 до 99')

        elif not image_w and not image_h and not image_quality:
            raise forms.ValidationError(
                'Введите необходимый параметр')

        return cleaned_data
