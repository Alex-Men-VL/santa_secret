from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail


from .models import Profile, Game


EMAIL_TEMPLATE = '''
Жеребьевка в игре “Тайный Санта” проведена! Спешу сообщить кто тебе выпал.
Вы дарите подарок игру {name};
Email игрока: {email};
Хотел бы получить в качестве подарка: {preferences};
Не хотел бы получить: {not_preferences}
Стоимость подарка: {cost_limit}
Подарок нужно отправить до {dispatch_date}

С уважением, сайт Тайный Санта
{our_site}
'''


class UserInline(admin.TabularInline):
    model = Profile


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = [
        UserInline,
    ]
    actions = ['draw_lots']

    @admin.action(description='Провести жеребьевку')
    def draw_lots(self, request, queryset):
        for game in queryset:
            if game.draw_done:
                self.message_user(
                    request,
                    f'Жеребьевка игры (slug={game.slug}) проведена.',
                    messages.ERROR
                )
                continue
            players = game.players.all()
            if players.count() < 3:
                self.message_user(
                    request,
                    f'Для жеребьевки игры (slug={game.slug})'
                    'недостаточно игроков.',
                    messages.ERROR
                )
                continue
            for player_number in range(players.count - 1):
                sender = players[player_number]
                recipient = players[player_number + 1]

                if recipient.preferences:
                    preferences = recipient.preferences
                else:
                    preferences = 'Все, что угодно'
                if recipient.not_preferences:
                    not_preferences = recipient.not_preferences
                else:
                    not_preferences = 'Рад всему'

                send_mail(
                    'Жеребьевка в игре "Тайный Санта"',
                    EMAIL_TEMPLATE.format(
                        name=recipient.user.first_name,
                        email=recipient.user.email,
                        preferences=preferences,
                        not_preferences=not_preferences,
                        our_site=settings.BASE_URL,
                        cost_limit = game.cost_limit,
                        dispatch_date=game.dispatch_date
                    ),
                    settings.EMAIL_HOST_USER,
                    [sender.user.email],
                    fail_silently=False,
                )
        self.message_user(
            request,
            'Жеребьевка проведена',
            messages.SUCCESS
        )


admin.site.register(Game, GameAdmin)
