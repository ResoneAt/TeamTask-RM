from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'accounts'
urlpatterns =[
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name= 'user_logout'),
]
=======

app_name = 'accounts'
urlpatterns = [
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_user'),
    path('profile/edit_profile/<int:user_id>/', views.EditProfileView.as_view(), name='edit_user'),
    path('logout/', views.LogoutView.as_view(), name='logout_user'),
]
>>>>>>> fdc29809955e3cab539d1f6fa3c2de37c1128acd
