# Generated by Django 3.2.10 on 2021-12-23 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import games.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('cost_limit', models.CharField(choices=[('ANY', 'Без ограничения стоимости'), ('FIRST_RANGE', 'до 500 рублей'), ('SECOND_RANGE', '500-1000 рублей'), ('THIRD_RANGE', '1000-2000 рублей')], default='ANY', max_length=30, verbose_name='Стоимость')),
                ('registration_end', models.DateField(verbose_name='Период регистрации участников')),
                ('dispatch_date', models.DateField(verbose_name='Период отправки подарка')),
                ('slug', models.SlugField(default=games.models.get_slug, unique=True, verbose_name='Идентификатор игры')),
            ],
            options={
                'verbose_name': 'игра',
                'verbose_name_plural': 'игры',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='players', to='games.game', verbose_name='Игра')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
            },
        ),
    ]
