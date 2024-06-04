from django.apps import apps
from django.conf import settings

from oscarbot.models import User


def get_bot_model():
    try:
        app_name, app_model = settings.OSCARBOT_BOT_MODEL.split('.')
        bot_model = apps.get_model(app_name, app_model)
        return bot_model
    except Exception:
        raise RuntimeError('Failed to get Bot model. Add to settings.py OSCARBOT_BOT_MODEL = app.BotModel')


def get_bot_user_model():
    """Get bot user model"""
    try:
        app_name, app_model = settings.OSCARBOT_BOT_USER_MODEL.split('.')
        bot_model = apps.get_model(app_name, app_model)
        return bot_model
    except AttributeError:
        return User
    except Exception:
        raise RuntimeError('Failed to get Bot model. Add to settings.py OSCARBOT_BOT_USER_MODEL = app.BotModel')
