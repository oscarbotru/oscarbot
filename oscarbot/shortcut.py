from oscarbot.bot import Bot
from oscarbot.menu import Menu
from oscarbot.models import User
from oscarbot.response import TGResponse
from oscarbot.services import get_bot_model


class QuickBot:

    def __init__(self, chat, message: str, token: str = None, menu: Menu = None):
        if token:
            self.token = token
        else:
            bot_model = get_bot_model()
            bot_object = bot_model.objects.all().first()
            if bot_object:
                self.token = bot_object.token

        if isinstance(chat, int):
            self.chat = chat
        elif isinstance(chat, str):
            chat_user = User.objects.filter(username=chat).first()
            if chat_user:
                self.chat = chat_user.t_id

        self.message = message
        self.menu = menu

    def send(self):
        response = TGResponse(message=self.message, menu=self.menu)

        response.send(
            self.token,
            t_id=self.chat
        )
