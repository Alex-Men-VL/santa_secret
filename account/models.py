from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from games.models import Game


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Участник',
    )
    games = models.ManyToManyField(
        Game,
        related_name='players',
        verbose_name='Игра',
        blank=True,
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
