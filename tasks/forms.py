from django import forms
from .models import WorkSpaceModel,BoardModel


class WorkSpaceForm(forms.ModelForm):
    class Meta:
        model = WorkSpaceModel
        fields = ['title','category','background']
        labels = {
            'title':'Title',
            'category':'Category',
            'background':'Background'
        }

class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardModel
        fields = ['title','category','visibility','background']
        labels = {
            'title':'Title',
            'category':'Category',
            'visibility':'Visibility',
            'background':'Background'
        }