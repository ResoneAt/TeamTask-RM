from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [
	path('mycards/', views.ShowMyCards.as_view(), name='show_my_cards'),

]