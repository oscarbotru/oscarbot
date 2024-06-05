from oscarbot.menu import Menu
from oscarbot.response import TGResponse
from oscarbot.services import get_bot_model, get_bot_user_model


class QuickBot:

    def __init__(self, chat: object, message: str, token: str = None, menu: Menu = None):
        """
        Init QuickBot object for send message to Telegram user
        @param chat: user id, or username if this user in DB, can be oscarbot.models.User object
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

        user_model = get_bot_user_model()
        if isinstance(chat, int):
            self.chat = chat
        elif isinstance(chat, str):
            chat_user = user_model.objects.filter(username=chat).first()
            if chat_user:
                self.chat = chat_user.t_id
        elif isinstance(chat, user_model):
            chat: user_model
            self.chat = chat.t_id

        self.message = message
        self.menu = menu

    def send(self):
        response = TGResponse(message=self.message, menu=self.menu)

        response.send(
            self.token,
            t_id=self.chat
        )
