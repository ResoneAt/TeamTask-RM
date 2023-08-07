from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from accounts.models import User



class ProfileView(View):
    templated_name = 'account/profile.html'
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id, is_active=True)
        return render(request, self.templated_name, {'user': user})


class EditProfileView(LoginRequiredMixin,View):
    form_class = ''
    templated_name = 'accounts/edit_profile.html'
    def get(self, request):
        form = self.form_class(isinstance=request.user,
        initial ={'email': request.user.email})
        return render(request, self.templated_name, {'form': form})
    def post(self, request):
        pass


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.is_authentication:
            logout(request)
            messages.success(request, 'you successfly logout profile', 'success')
            return redirect('home:home')
        messages.success(request, 'you must login account', 'warning')
        return redirect('home:home')