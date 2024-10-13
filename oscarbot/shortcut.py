from oscarbot.response import TGResponse
from oscarbot.services import get_bot_model
from oscarbot.models import User


class QuickBot(TGResponse):
    """QuickBot."""

    def __init__(self, user: User = None, token: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if token:
            self.token = token
        else:
            bot_model = get_bot_model()
            bot_object = bot_model.objects.first()
            if bot_object:
                self.token = bot_object.token
        self.user = user

    def send(self, token=None, user=None, content=None, t_id=None):
        """Send a message."""
        if token is None:
            token = self.token
        if user is None:
            user = self.user
        return super().send(token, user, content, t_id)

    def send_chat(self, chat_id: str | int):
        """Send a message to chat."""
        self.need_update = False
        return self.send(self.token, t_id=chat_id)
