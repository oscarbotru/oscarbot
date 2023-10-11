from django.core.management import BaseCommand

from oscarbot.shortcut import QuickBot


class Command(BaseCommand):

    def handle(self, *args, **options):
        quick_bot = QuickBot(
            'maslov_oa',
            'Hello from command line'
        )
        quick_bot.send()
