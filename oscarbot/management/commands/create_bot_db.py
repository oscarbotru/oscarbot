from django.conf import settings
from django.core.management import BaseCommand
from oscarbot.bot import Bot
from oscarbot.models import Bot as TGBot


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Create or update bot in database"""
        if getattr(settings, 'TELEGRAM_API_TOKEN', None):
            bot = Bot(token=settings.TELEGRAM_API_TOKEN)
            response = bot.get_me()
            status, result = response.get('ok'), response.get('result')
            if status and result:
                bot_id, is_bot = result.get('id'), result.get('is_bot')
                if is_bot:
                    first_name, last_name = result.get('first_name', ' '), result.get('last_name', ' ')
                    name = f'{first_name} {last_name}'.strip()
                    username = result.get('username')
                    TGBot.objects.update_or_create(
                        token=settings.TELEGRAM_API_TOKEN,
                        defaults={
                            't_id': bot_id,
                            'name': name,
                            'username': username,
                        }
                    )
