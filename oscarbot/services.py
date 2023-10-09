from django.apps import apps
from django.conf import settings


def get_bot_model():
    try:
        app_name, app_model = settings.OSCARBOT_BOT_MODEL.split('.')
        bot_model = apps.get_model(app_name, app_model)
        return bot_model
    except Exception:
        raise RuntimeError('Failed to get Bot model')
