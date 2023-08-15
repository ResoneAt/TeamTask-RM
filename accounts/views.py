from itertools import count
from typing import Any
from django import http
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout , login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from accounts.models import User, NotificationModel, MessageModel
from .forms import UserRegistrationForm, UserLoginForm, SendMessageForm, EditProfileForm , EditMessageForm
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class HomePageView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'accounts/home.html')


class SignUpView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],
                                            cd['email'],
                                            cd['password1'])
            login(request, user)
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    from_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.from_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you successfully logout profile', 'success')
        return redirect('home:home')


class ProfileView(LoginRequiredMixin, View):
    templated_name = 'accounts/profile.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return render(request, self.templated_name, {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != kwargs['user_id']:
            messages.error(request, 'you can not access to  this profile!', 'danger')
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.File, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile edited successfully')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})


class NotificationListView(LoginRequiredMixin, View):
    notifications_instance: object
    template_name = 'accounts/notifications_list.html'

    def setup(self, request, *args, **kwargs):
        self.notifications_instance = NotificationModel.objects.filter(to_user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        notifications = self.notifications_instance
        return render(request, self.template_name, context={'notifications': notifications})


class MessageListView(View):
    messages_instance: object
    template_name = 'accounts/messages_list.html'

    def setup(self, request, *args, **kwargs):
        self.messages_instance = (MessageModel.objects.
                                  select_related('from_user').
                                  values('from_user', 'to_user').
                                  filter(Q(from_user=request.user) |
                                         Q(to_user=request.user)).
                                  annotate(unread_count=count(is_read=False)).
                                  order_by('from_user', 'to_user', 'created_at'))
        return super().setup(request, args, kwargs)

    def get(self, request):
        messages_ = self.messages_instance
        return render(request, self.template_name, context={messages_})


class SendMessageView(View):
    form_class = SendMessageForm
    template_name = 'accounts/pv_message.html'

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['user_id'])
        self.messages_instance = (MessageModel.objects.select_related('to_user')
                                  .filter(Q(from_user=request.user, to_user=self.user) |
                                          Q(from_user=self.user, to_user=request.user))
                                  .order_by('created_at'))
        return super().setup(request, args, kwargs)

    def get(self, request, user_id):
        messages_ = self.messages_instance
        form = self.form_class()
        context = {'messages': messages_,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        form = self.form_class(request.POST)
        user = get_object_or_404(User, pk=user_id)
        if form.is_valid():
            form.save(commit=False)
            form.from_user, form.to_user = request.user, user
            form.save()
            return redirect('accounts:send_message', user_id)
        messages.error(request,'you can not send message')
        return redirect('accounts:send_message', user_id)


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/delete_account.html




    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == kwargs['user_id']:
            messages.error(request, 'You Canot Do This Action!', 'danger')
            return redirect('accounts:profile', kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        return render(request, self.template_name)

    def post(self, request, user_id):
        request.user.delete()
        return redirect('accounts:login')



class EditMessageView(LoginRequiredMixin, View):
    form_class = EditMessageForm
    template_name = 'accounts/edit_message.html'

    def setup(self, request, *args, **kwargs):
        self.message_instance = MessageModel.objects.get(pk=kwargs['message_id'])
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        message = self.message_instance 
        if not message.user.id == request.user.id:
            messages.error(request, ' you canot Edit this Message', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        message = self.message_instance 
        form = self.form_class(instance=message)
        return render(request, 'accounts/edit_message.html', {'form':form})

    def post(self, request, *args, **kwargs):
        message = self.message_instance 
        form = self.form_class(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'you Editet this Message', 'success')
            return redirect('accounts:edit_message', message_id)
        


class DeleteMessageView(LoginRequiredMixin, View):

    def get(self, request, message_id):
        message = MessageModel.objects.get(pk=message_id)
        if message.user.id == request.user.id:
            message.delete()
            messages.success(request, 'message deleted successfully', 'success')
        else:
            messages.error(request, 'You canot delete in messages', 'danger')
        return redirect('accounts:message_list')
    



class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'



class UserPasswordResetDoneView(LoginRequiredMixin, View):
    template_name = 'accounts/password_reset_done.html'



class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(LoginRequiredMixin, View):
    template_name = 'accounts/password_reset_complete.html'
    