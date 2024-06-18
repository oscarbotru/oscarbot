import json

import requests
from django.conf import settings
from django.core.management import BaseCommand

from oscarbot.bot import Bot
from oscarbot.services import get_bot_model
from oscarbot.views import handle_content


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_model = get_bot_model()
        bot_object = bot_model.objects.all().first()
        bot = Bot(bot_object.token)
        res = bot.send_message(310780174, 'test',
                               video='https://file-examples.com/storage/fe5048eb7365a64ba96daa9/2017/04/file_example_MP4_480_1_5MG.mp4')
