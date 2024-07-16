from django.conf import settings

from oscarbot.menu import Menu
from oscarbot.response import TGResponse
from oscarbot.services import get_bot_model, get_bot_user_model


class QuickBot:

    def __init__(self, user: object, message: str, token: str = None, menu: Menu = None):
        """
        Init QuickBot object for send message to Telegram user
        @param user: user oscarbot.models.User object
        @param message: text message
        @param token: bot token, default get first bot from DB
        @param menu: should be oscarbot.menu.Menu object
        """
        if token:
            self.token = token
        else:
            bot_model = get_bot_model()
            bot_object = bot_model.objects.all().first()
            if bot_object:
                self.token = bot_object.token

        self.user = user
        self.message = message
        self.menu = menu

    def send(self):
        response = TGResponse(message=self.message, menu=self.menu, need_update=False)

        response.send(
            self.token,
            user=self.user
        )
