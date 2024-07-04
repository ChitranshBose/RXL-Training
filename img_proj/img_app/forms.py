from django import forms as fm
from .models import Upload



class UploadImage(fm.ModelForm):

    class Meta:
        
        model = Upload
        fields = ['img','drop_down']
        labels = {'img': '', 'drop_down':'Select'}

        
     