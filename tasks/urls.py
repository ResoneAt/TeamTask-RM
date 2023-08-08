from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [
	path('mycards/', views.ShowMyCards.as_view(), name='show_my_cards'),
    path('edit_card/<int:card_id>/', views.CardEditView.as_view(), name='edit_card'),


]