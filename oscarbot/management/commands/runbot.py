import json
import time
import requests
from django.conf import settings
from django.core.management import BaseCommand

from oscarbot.bot_logger import log
from oscarbot.services import get_bot_model
from oscarbot.views import handle_content


class Command(BaseCommand):
    """Run Telegram bot in polling mode."""

    class BotData:
        """Fallback bot data."""
        token = None

    def handle(self, *args, **options):
        bot_model = get_bot_model()
        bot = bot_model.objects.first()
        if not bot:
            bot = self.BotData()
            bot.token = getattr(settings, 'TELEGRAM_API_TOKEN', None)
        if not bot.token:
            log.error('Bot token not found in DB or settings')
            return None
        offset = 0
        log.info('🚀 Bot polling started')
        try:
            while True:
                url = f'{settings.TELEGRAM_URL}{bot.token}/getUpdates'
                params = {
                    'offset': offset,
                    'timeout': 30,
                }
                response = requests.get(url, params=params, timeout=35)
                content = response.json()
                if not content.get('ok'):
                    raise ValueError('Invalid Telegram response')
                updates = content.get('result', [])
                if not updates:
                    time.sleep(.5)
                    continue
                for update in updates:
                    offset = update['update_id'] + 1
                    handle_content(bot.token, update)
        except KeyboardInterrupt:
            log.info('🛑 Bot polling stopped manually')
        except Exception as e:
            log.error(f'❌ Bot crashed: {e}')
