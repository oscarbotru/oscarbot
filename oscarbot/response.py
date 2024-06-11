import json

from django.conf import settings

from oscarbot.bot import Bot
from oscarbot.bot_logger import log


class TGResponse:

    def __init__(self, message: str, menu=None, need_update=True, photo=None, attache=None, video=None,
                 protect=False) -> None:
        # self.chat = chat
        self.message = message
        self.menu = menu
        self.attache = attache
        self.need_update = need_update
        self.photo = photo
        self.video = video
        self.protect = protect
        self.parse_mode = settings.TELEGRAM_PARSE_MODE if getattr(settings, 'TELEGRAM_PARSE_MODE', None) else 'HTML'

    def send(self, token, user=None, t_id=None):
        tg_bot = Bot(token)
        if self.menu:
            self.menu = self.menu.build()
        data_to_send = {
            'chat_id': user.t_id if user is not None else t_id,
            'message': self.message,
            'reply_keyboard': self.menu,
            'photo': self.photo,
            'video': self.video,
            'protect_content': self.protect,
            'parse_mode': self.parse_mode,
        }

        if self.need_update and user.last_message_id:
            response_content = tg_bot.update_message(**data_to_send, message_id=user.last_message_id)
            response_dict = json.loads(response_content)
            if not response_dict.get('ok'):
                response_content = tg_bot.send_message(**data_to_send)
        else:
            response_content = tg_bot.send_message(**data_to_send)
        log.info(f'{response_content}')
        if user:
            user.update_last_sent_message(response_content)

    def can_send(self):
        if self.message is not None:
            return True
        return False
