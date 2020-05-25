from django import forms
from .models import HotelsImages

class ImageUpload(forms.ModelForm):
    class Meta:
        model = HotelsImages
        fields = ('file',)
        def save(self):
            image = super(ImageUpload, self).save()
            return image