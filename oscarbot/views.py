import json
from django.conf import settings
from oscarbot.handler import BaseHandler
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from oscarbot.services import get_bot_model


@csrf_exempt
def bot_view(request, token):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        body = body.replace('\n', '')
        content = json.loads(body)
        return handle_content(token, content)


def handle_content(token, content):
    if getattr(settings, 'TELEGRAM_BOT_TOKEN', None):
        bot_token = settings.TELEGRAM_BOT_TOKEN
    else:
        bot_model = get_bot_model()
        current_bot = bot_model.objects.filter(token=token).first()
        bot_token = current_bot.token if current_bot else None
    if bot_token:
        try:
            handler = BaseHandler(bot_token, content)
            tg_response = handler.handle()
            if tg_response:
                if tg_response.can_send():
                    tg_response.send(token, handler.user, content)
                return HttpResponse("OK")
        except Exception as ex:
            print(ex)
            return HttpResponse("OK")
    else:
        raise RuntimeError('Failed to find bot')
