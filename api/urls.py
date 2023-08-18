from django.urls import path
from rest_framework import routers
from .views.accounts import UserAPIView


app_name = 'api'
urlpatterns = [
    path('user/', UserAPIView.as_view(), name='user')
]
