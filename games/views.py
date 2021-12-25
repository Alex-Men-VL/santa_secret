from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from . import forms
from .models import Game, COSTS, Profile


def index(request):
    return render(request, 'games/index.html')


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data['email'].split('@')[0]
        user.username = username
        user.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        path = self.request.GET.get("next")
        if path:
            return path
        return reverse_lazy('index')


class GameCreate(CreateView):
    model = Game
    template_name = 'games/new_game.html'
    form_class = forms.AddGameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.owner = self.request.user
        game.save()
        return redirect('user_games')


def user_games(request):
    try:
        user = request.user
        games = Game.objects.filter(owner=user).order_by('-pk')
        costs = {i[0]: i[1] for i in COSTS}
        context = {
            'games': games,
            'games_count': games.count(),
            'costs': costs,
            'base_url': settings.BASE_URL,
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
    success_url = reverse_lazy('user_games')


@login_required
def game_join(request, slug):
    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Profile, user=request.user)
    if user in game.players.all():
        title = 'Вы уже присоединились к игре!'
    else:
        title = 'Вы успешно присоединились к игре!'
    game.players.add(user)
    if game.owner == request.user:
        game.owner_joined = True
        game.save()
    context = {
        'title': title,
        'game': game,
    }
    return render(request, 'games/join_success.html', context=context)


class AddUserPrefers(UpdateView):
    model = Profile
    template_name = 'games/users_preferences.html'
    form_class = forms.UsersPreferencesForm

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(AddUserPrefers, self).form_valid(form)

    def get_success_url(self):
        return reverse("index")
