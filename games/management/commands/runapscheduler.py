import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from games.models import Game
from games.email_utils import send_email_to_owner, send_email_to_players

logger = logging.getLogger(__name__)


def draw_lots():
    games = Game.objects.filter(draw_done=False).filter(
        registration_end=timezone.now().date()
    ).annotate(players_count=Count('players'))

    if games.count() > 0:
        for game in games:
            players = game.players.all()
            if game.players_count < 3:
                send_email_to_owner(game.owner.email, game.title)
                continue
            send_email_to_players(players, game)
            game.draw_done = True
            game.save()

        logger.info("Emails have been sent")


class Command(BaseCommand):
    help = "Проведение розыгрышей"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            draw_lots,
            trigger=CronTrigger(hour=23, minute=50),
            id="draw_lots",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'draw_lots'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

