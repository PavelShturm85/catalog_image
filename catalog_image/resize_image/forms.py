from django import forms
from PIL import Image

from .models import Picture


class UploadPictureForm(forms.Form):

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

    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    quality = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        quality = cleaned_data.get('quality')

        if (width and width < 0) or (height and height < 0):
            raise forms.ValidationError(
                'Размер должен быть положительным числом')

        elif quality and (quality < 1 or quality > 99):
            raise forms.ValidationError(
                'Качество изображения должно быть числом от 1 до 99')

        elif not width and not height and not quality:
            raise forms.ValidationError(
                'Введите необходимый параметр')

        return cleaned_data
