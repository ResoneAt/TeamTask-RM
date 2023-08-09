from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns =[
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name= 'user_logout'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='user_profile'),
    path('profile/edit/<int:user_id>/', views.EditUserView.as_view(), name='user_edit'),
    
]