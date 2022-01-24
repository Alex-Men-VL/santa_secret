import string
import random

from django.contrib.auth.models import User
from django.db import models

COSTS = (
    ('ANY', 'Без ограничения стоимости'),
    ('FIRST_RANGE', 'до 500 рублей'),
    ('SECOND_RANGE', '500-1000 рублей'),
    ('THIRD_RANGE', '1000-2000 рублей'),
)

COSTS_FORMATTED = {cost[0]: cost[1] for cost in COSTS}


def get_slug():
    letters_and_digits = string.ascii_letters + string.digits
    length = 10
    slug = ''.join(random.sample(letters_and_digits, length))
    return slug


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
        'Дата закрытия регистрации',
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
    draw_done = models.BooleanField(
        'Жеребьевка проведена?',
        default=False,
    )

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'
