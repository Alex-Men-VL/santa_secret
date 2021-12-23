from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms
from .models import Game, COSTS


def index(request):
    return render(request, 'games/index.html')


class RegisterUser(CreateView):
    def get(self, request, *args, **kwargs):
        form = forms.RegisterUserForm
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.RegisterUserForm(request.POST)
        if not form.is_valid():
            return render(request, 'register.html', {'form': form})
        user = form.save(commit=False)
        username = form.cleaned_data['email'].split('@')[0]
        user.username = username
        user.save()
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def new_game(request):
    if request.method == 'POST':
        form = forms.AddGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            return redirect('index')
    else:
        form = forms.AddGameForm()
    context = {
        'form': form,
        'title': 'Создание игры'
    }
    return render(request, 'games/new_game.html', context=context)


def user_games(request):
    try:
        user = request.user
        user_games = Game.objects.filter(owner=user)
        costs = {i[0]: i[1] for i in COSTS}
        context = {
            'games': user_games,
            'games_count': user_games.count(),
            'costs': costs,
        }
    except TypeError:
        context = {
            'games_count': 0,
        }
    return render(request, 'games/user_games.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')
