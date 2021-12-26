from django.conf import settings
from django.core.mail import send_mail

from .models import COSTS_FORMATTED


EMAIL_TEMPLATE_COMMON = '''
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


EMAIL_TEMPLATE_FOR_OWNER = '''
Жеребьевка в игре “Тайный Санта” не проведена!
Название игры: {game_title}
Для участия в игре не достаточно участников.

С уважением, сайт Тайный Санта
{our_site}
'''


def send_email_to_owner(owner_email, game_title):
    send_mail(
        'Жеребьевка в игре "Тайный Санта"',
        EMAIL_TEMPLATE_FOR_OWNER.format(
            game_title=game_title,
            our_site=settings.BASE_URL,
        ),
        settings.EMAIL_HOST_USER,
        [owner_email],
        fail_silently=False,
    )


def send_email_to_players(players, game):
    for player_number in range(game.players_count - 1):
        sender = players[player_number]
        recipient = players[player_number + 1]
        send_alert(sender, recipient, game)

    sender = players[game.players_count - 1]
    recipient = players[0]
    send_alert(sender, recipient, game)


def send_alert(sender, recipient, game):
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
        EMAIL_TEMPLATE_COMMON.format(
            name=recipient.user.first_name,
            email=recipient.user.email,
            preferences=preferences,
            not_preferences=not_preferences,
            our_site=settings.BASE_URL,
            cost_limit=COSTS_FORMATTED[game.cost_limit],
            dispatch_date=game.dispatch_date
        ),
        settings.EMAIL_HOST_USER,
        [sender.user.email],
        fail_silently=False,
    )
