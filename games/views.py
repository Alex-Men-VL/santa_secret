from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


def index(request):
    return render(request, 'games/index.html')


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        users_count = User.objects.count()
        user.username = f'user{users_count + 1}'
        user.save()
        return super(RegisterUser, self).form_valid(form)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')
