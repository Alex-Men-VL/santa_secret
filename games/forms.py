from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from account.models import Profile
from .models import COSTS, Game


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
        widget=MyDateInput,
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


class UsersPreferencesForm(forms.ModelForm):
    preferences = forms.CharField(
        label='Что хотели бы получить в подарок от Санты?',
        widget=forms.Textarea(attrs={'placeholder': 'Например, я люблю книги'}),
        required=False,
    )
    not_preferences = forms.CharField(
        label='Что точно не дарить?',
        widget=forms.Textarea(attrs={'placeholder': 'Не нужны носки'}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['preferences', 'not_preferences']
