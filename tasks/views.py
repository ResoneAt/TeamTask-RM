from django.shortcuts import render
from django.views import View
from .models import CardModel
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ShowMyCards(LoginRequiredMixin,View):
    template_name = 'show_my_cards.html'
    
    def get(self, request, *args, **kwargs):
        cards = CardModel.objects.filter(user=request.user) 
        return render(request, self.template_name, context={'cards': cards})