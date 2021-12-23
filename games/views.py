from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from . import forms
from .models import Game


def index(request):
    return render(request, 'games/index.html')


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data["email"].split('@')[0]
        user.save()
        return super(RegisterUser, self).form_valid(form)


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def new_game(request):
    if request.method == 'POST':
        form = forms.AddGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = forms.AddGameForm()
    context = {
        'form': form,
        'title': 'Создание игры'
    }
    return render(request, 'games/new_game.html', context=context)
