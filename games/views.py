from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from account.models import Profile
from . import forms
from .models import COSTS, Game


def index(request):
    return render(request, 'games/index.html')


class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'games/game_edit.html'
    form_class = forms.AddGameForm
    success_url = reverse_lazy('games:user_games')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Создать игру',
            'button': 'Создать игру',
        })
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(GameCreate, self).form_valid(form)


class UserGames(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'games/user_games.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user).order_by('-pk')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        costs = {i[0]: i[1] for i in COSTS}
        context.update({
            'costs': costs,
            'base_url': settings.BASE_URL,
        })
        return context


class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = 'games/game_delete.html'
    success_url = reverse_lazy('games:user_games')

    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, slug=kwargs.get('slug'))
        if request.user != game.owner:
            return redirect('games:index')
        return super().get(request, *args, **kwargs)


@login_required
def game_join(request, slug):
    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Profile, user=request.user)
    if game.registration_end >= timezone.now().date():
        registration_is_possible = True
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
    else:
        registration_is_possible = False
        context = {
            'title': 'Срок регистрации в игре закончился',
        }
    context.update({'registration_is_possible': registration_is_possible})
    return render(request, 'games/join_success.html', context=context)


class AddUserPrefers(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'games/user_preferences.html'
    form_class = forms.UsersPreferencesForm
    success_url = reverse_lazy('games:index')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class GameEdit(LoginRequiredMixin, UpdateView):
    model = Game
    template_name = 'games/game_edit.html'
    form_class = forms.AddGameForm
    success_url = reverse_lazy('games:user_games')

    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, slug=kwargs.get('slug'))
        if request.user != game.owner:
            return redirect('games:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Изменить игру',
            'button': 'Применить изменения',
        })
        return context


class UsersPreferences(ListView):
    model = Profile
    template_name = 'games/preferences.html'
    context_object_name = 'preferences'

    def get_queryset(self):
        return Profile.objects.exclude(preferences=None).exclude(preferences='')


def csrf_failure(request, reason=""):
    context = RequestContext(request)
    response = render(request, '403.html', context)
    response.status_code = 403
    return response
