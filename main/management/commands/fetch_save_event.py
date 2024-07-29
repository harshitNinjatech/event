from django.core.management.base import BaseCommand, CommandError

from main.tasks import fetch_and_save_events


class Command(BaseCommand):
    help = "fetch & save events"

    def handle(self, *args, **options):
        # This function will fetch & save events using management command
        fetch_and_save_events()
