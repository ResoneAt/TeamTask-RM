from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_user'),
    path('profile/edit_profile/<int:user_id>/', views.EditProfileView.as_view(), name='edit_user'),
    path('logout/', views.LogoutView.as_view(), name='logout_user'),
]
