from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from . import forms
from .models import Game, COSTS


def index(request):
    return render(request, 'games/index.html')


class RegisterUser(CreateView):
    def get(self, request, *args, **kwargs):
        form = forms.RegisterUserForm
        context = {
            'form': form
        }
        return render(request, 'register.html', context=context)

    def post(self, request, *args, **kwargs):
        form = forms.RegisterUserForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'register.html', context=context)
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


class GameCreate(CreateView):
    fields = ['title', 'cost_limit', 'registration_end', 'dispatch_date']

    def get(self, request, *args, **kwargs):
        form = forms.AddGameForm
        context = {
            'form': form,
            'title': 'Создание игры',
            'button': 'Создать игру',
        }
        return render(request, 'games/new_game.html', context=context)

    def post(self, request, *args, **kwargs):
        form = forms.AddGameForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
                'title': 'Создание игры',
                'button': 'Создать игру',
            }
            return render(request, 'games/new_game.html', context=context)
        game = form.save(commit=False)
        game.owner = request.user
        game.save()
        return redirect('my_games')


def user_games(request):
    try:
        user = request.user
        games = Game.objects.filter(owner=user).order_by('-pk')
        costs = {i[0]: i[1] for i in COSTS}
        context = {
            'games': games,
            'games_count': games.count(),
            'costs': costs,
            'base_url': settings.BASE_URL
        }
    except TypeError:
        context = {
            'games_count': 0,
        }
    return render(request, 'games/user_games.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


class GameDelete(DeleteView):
    model = Game
    template_name = 'games/game_delete.html'
    success_url = reverse_lazy('my_games')


def game_join(request, slug):
    return redirect('index')
