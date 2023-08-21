from django import forms
from .models import CardModel,WorkSpaceModel,BoardModel,LabelModel,SubTaskModel,ListModel

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

<<<<<<< HEAD
class UsernameSearch(forms.Form):
    search = forms.CharField(label='search user', widget=forms.TextInput)
=======

class ListCreateEditForm(forms.ModelForm):
    class Meta:
        model = ListModel
        fields = ['title']
        labels = {
            'title':'Title',
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
       
>>>>>>> dev
