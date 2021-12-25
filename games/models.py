import string
import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

COSTS = (
    ('ANY', 'Без ограничения стоимости'),
    ('FIRST_RANGE', 'до 500 рублей'),
    ('SECOND_RANGE', '500-1000 рублей'),
    ('THIRD_RANGE', '1000-2000 рублей'),
)


def get_slug():
    letters_and_digits = string.ascii_letters + string.digits
    length = 10
    slug = ''.join(random.sample(letters_and_digits, length))
    return slug


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Участник',
    )
    game = models.ForeignKey(
        'Game',
        related_name='players',
        verbose_name='Игра',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    preferences = models.TextField(
        'Хотел бы получить',
        blank=True,
        null=True,
    )
    not_preferences = models.TextField(
        'Не хотел бы получить',
        blank=True,
        null=True,
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'


class Game(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='games',
        verbose_name='Организатор',
        on_delete=models.PROTECT,
    )
    title = models.CharField(
        'Название',
        max_length=200,
        db_index=True,
    )
    cost_limit = models.CharField(
        'Стоимость подарка',
        max_length=30,
        choices=COSTS,
        default='ANY',
    )
    registration_end = models.DateField(
        'Период регистрации участников',
    )
    dispatch_date = models.DateField(
        'Период отправки подарка',
    )
    slug = models.SlugField(
        'Идентификатор игры',
        unique=True,
        default=get_slug,
        db_index=True,
    )
    owner_joined = models.BooleanField(
        'Владелец присоединился к игре',
        default=False,
    )

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'
