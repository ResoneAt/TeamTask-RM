from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from accounts.models import User, NotificationModel, PvMessageModel
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm
    templated_name = 'accounts/profile.html'
    def get(self, request, user_id):
        form = get_object_or_404(User, pk=user_id, is_active=True)
        return render(request, self.templated_name, {'form': form})

class EditProfileView(LoginRequiredMixin,View):
    form_class = ProfileForm
    templated_name = 'accounts/edit_profile.html'
    def get(self, request, user_id):
        form = get_object_or_404(User, pk=user_id)
        return render(request, self.templated_name, {'form': form})
    def post(self, request):
        pass


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.is_authentication:
            logout(request)
            messages.success(request, 'you successfly logout profile', 'success')
            # return redirect('home:home')
        # messages.success(request, 'you must login account', 'warning')
        # return redirect('home:home')


class NotificationListView(LoginRequiredMixin, View):
    template_name = 'accounts/notifications.html'

    def setup(self, request, *args, **kwargs):
        self.notifications_instance = get_list_or_404(NotificationModel, to_user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        notifications = self.notifications_instance
        return render(request, self.template_name, context={'notifications': notifications})


class MessageListView(View):
    template_name = 'accounts/messages_list.html'

    def setup(self, request, *args, **kwargs):
        self.messages_instance = get_list_or_404(PvMessageModel,
                                          Q(from_user=request.user) |
                                                Q(to_user=request.user))
        return super().setup(request, args, kwargs)

    def get(self, request):
        messages = self.messages_instance
        return render(request, self.template_name, context={messages})

