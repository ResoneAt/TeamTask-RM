from django import forms
from .models import CardModel,WorkSpaceModel,BoardModel,LabelModel,SubTaskModel


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
class CardCreateEditForm(forms.ModelForm):
    class Meta:
        model = CardModel
        exclude = ('list',)
        widgets = {
            # other attributes??
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
class LabelCreateEditForm(forms.ModelForm):
    class Meta:
        model = LabelModel
        exclude = ('card',)
        widgets = {
            'background_color': forms.Select(attrs={'class': 'form-control'}),
        }
        
class SubCardCreateEditForm(forms.ModelForm):
    class Meta:
        model = SubTaskModel
        exclude = ('card',)
       
