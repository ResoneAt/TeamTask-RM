from django import forms
from .models import CardModel,WorkSpaceModel,BoardModel


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
class CardEditForm(forms.ModelForm):
    class Meta:
        model = CardModel
        exclude = ('list',)
        widgets = {
            # other attributes??
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

