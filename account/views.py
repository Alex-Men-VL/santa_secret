from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, UserRegistrationForm


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_success_url(self):
        path = self.request.GET.get("next")
        if path:
            return path
        return reverse_lazy('games:index')


class Register(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            'button': 'Зарегистрироваться',
        })
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data['email'].split('@')[0]
        user.username = username
        user.save()

        login(self.request, user)
        path = self.request.GET.get("next")
        if path:
            return redirect(path)
        return redirect('games:index')


class UserAccount(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/register.html'
    fields = ['first_name', 'email']

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Личные данные',
            'button': 'Сохранить',
            'user_id': kwargs.get('pk'),
        })
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data['email'].split('@')[0]
        user.username = username
        user.save()

        login(self.request, user)
        path = self.request.GET.get("next")
        if path:
            return redirect(path)
        return redirect('games:index')


def logout_user(request):
    logout(request)
    return redirect('login')
