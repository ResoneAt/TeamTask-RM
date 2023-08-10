from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout , login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from accounts.models import User, NotificationModel, PvMessageModel
from .forms import UserRegistrationForm, UserLoginForm, SendMessageForm, EditProfileForm
from django.contrib.auth import authenticate


class SignUpView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

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

    def get(self, request, user_id):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id):
        form = self.form_class(request.POST, request.File, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile edited successfully')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you successfully logout profile', 'success')
        return redirect('home:home')


class NotificationListView(LoginRequiredMixin, View):
    template_name = 'accounts/notifications.html'

    def setup(self, request, *args, **kwargs):
        self.notifications_instance = NotificationModel.objects.filter(to_user=request.user)
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
        messages_ = self.messages_instance
        return render(request, self.template_name, context={messages_})


class SendMessageView(View):
    form_class = SendMessageForm
    template_name = 'accounts/send_message.html'

    def setup(self, request, *args, **kwargs):
        self.messages_instance = PvMessageModel.objects.select_related('from_user', 'to_user').filter(
                            Q(from_user=request.user, to_user=kwargs['user_id']) |
                            Q(to_user=request.user, from_user=kwargs['user_id']))
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

