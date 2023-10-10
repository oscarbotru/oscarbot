import json

from oscarbot.hanlder import BaseHandler
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from oscarbot.services import get_bot_model


@csrf_exempt
def bot_view(request, token):
    bot_model = get_bot_model()
    current_bot = bot_model.objects.filter(token=token).first()
    if current_bot:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            content = json.loads(body_unicode)
            handler = BaseHandler(current_bot, content)
            tg_response = handler.handle()
            if tg_response.can_send():
                tg_response.send(token, handler.user)
        return HttpResponse("OK")
    else:
        raise RuntimeError('Failed to find bot')
