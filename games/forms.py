from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import COSTS, Game


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
        help_texts = {
            'review ': '',
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class AddGameForm(forms.ModelForm):
    title = forms.CharField(
        label='Название игры',
        widget=forms.TextInput(attrs={'placeholder': 'Тайный Санта 2022'})
       )

    cost_limit = forms.ChoiceField(
        label='Стоимость подарка',
        choices=COSTS,
        widget=forms.Select,
    )

    registration_end = forms.DateField(
        label='Нужно вступить до',
        widget=MyDateInput,
    )

    dispatch_date = forms.DateField(
        label='Дата отправки подарков',
        widget=forms.SelectDateWidget,
    )

    class Meta:
        model = Game
        fields = ['title', 'cost_limit', 'registration_end', 'dispatch_date']

    def clean_registration_end(self):
        registration_end = self.cleaned_data['registration_end']
        if registration_end < timezone.now().date():
            raise ValidationError(
                'Укажите корректную дату завершения регистрации'
            )
        return registration_end

    def clean_dispatch_date(self):
        dispatch_date = self.cleaned_data['dispatch_date']
        if dispatch_date < timezone.now().date():
            raise ValidationError('Укажите корректную дату отправки подарков')
        return dispatch_date
