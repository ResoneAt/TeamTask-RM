from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [

    path('', views.HomePageView.as_view(), name='home'),

    # user
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LogoutView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:user_id>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),

    # notification
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),

    # message
    path('message/<int:user_id>/', views.SendMessageView.as_view(), name='message'),
    path('message/list/', views.MessageListView.as_view(), name='message_list'),
    path('message/edit/<int:message_id>/', views.EditMessageView.as_view(), name='edit_message'),
    path('message/delete/<int:message_id>/', views.DeleteMessageView.as_view(), name='delete_message'),

    # reset password
    path('reset-password/form/',
         views.UserPasswordResetView.as_view(),
         name='reset_password_form'),
    path('reset-password/done/',
         views.UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         views.UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
