from django.shortcuts import render
from django.views import View


app_name = 'home'
class HomeView(View):
    templated_name = 'tasks/home.html'
    def get(self, request):
        return render(request, self.templated_name)
