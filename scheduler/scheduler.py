from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Count
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from games.models import Game
from games.utils import send_email_to_owner, send_email_to_players


def draw_lots():
    games = Game.objects.filter(draw_done=False).filter(
        registration_end=timezone.now().date().annotate(
            players_count=Count('players')
        )
    )
    for game in games:
        players = game.players.all()
        if game.players_count < 3:
            send_email_to_owner(game.owner.email, game.title)
            continue
        send_email_to_players(players, game)
        game.draw_done = True
    print('Письма отправлены')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(draw_lots, 'interval', minutes=2, name='send_emails',
                      jobstore='default')
    scheduler.start()
