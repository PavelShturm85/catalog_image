from django import forms
from PIL import Image
from .models import Picture

class UploadPictureForm(forms.Form):
   
    name_image = forms.CharField(max_length=30, required=False)
    url = forms.URLField(required=False)
    img = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super(UploadPictureForm, self).clean()
        url = cleaned_data.get('url')
        img = cleaned_data.get('img')

        if (url and img) or (not url and not img):
            raise forms.ValidationError('херово заполнил')
        
        return cleaned_data
            
    


""" class UploadPictureForm(forms.Form):
   
    name_image = forms.CharField(max_length=30, required=False )
    url = forms.URLField(required=False)
    img = forms.ImageField(required=False)

    def clean(self):
        url = self.cleaned_data['url']
        img = self.cleaned_data['img']

        if (url and img) or (not url and not img):
            raise forms.ValidationError('херово заполнил')

        return self.cleaned_data """