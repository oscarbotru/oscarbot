import json

from django.conf import settings

from oscarbot.bot import Bot
from oscarbot.bot_logger import log


class TGResponse:

    def __init__(self, message: str, menu=None, need_update=True, photo=None, attache=None, video=None,
                 protect=False, callback_text='', callback_url=False, show_alert=False, cache_time=None,
                 disable_web_page_preview=False) -> None:
        self.tg_bot = None
        self.message = message
        self.menu = menu
        self.attache = attache
        self.need_update = need_update
        self.photo = photo
        self.video = video
        self.protect = protect
        self.parse_mode = settings.TELEGRAM_PARSE_MODE if getattr(settings, 'TELEGRAM_PARSE_MODE', None) else 'HTML'
        self.callback_url = callback_url
        self.callback_text = callback_text
        self.show_alert = show_alert
        self.cache_time = cache_time
        self.disable_web_page_preview = disable_web_page_preview

    def send(self, token, user=None, content=None, t_id=None):
        self.tg_bot = Bot(token)
        if content and (self.callback_text or self.callback_url):
            self.send_callback(content)
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
            'disable_web_page_preview': self.disable_web_page_preview
        }

        if self.need_update and user.last_message_id:
            response_content = self.tg_bot.update_message(**data_to_send, message_id=user.last_message_id)
            response_dict = json.loads(response_content)
            if not response_dict.get('ok'):
                response_content = self.tg_bot.send_message(**data_to_send)
        else:
            response_content = self.tg_bot.send_message(**data_to_send)
        log.info(f'{response_content}')
        if user:
            user.update_last_sent_message(response_content)

    def can_send(self):
        if self.message is not None:
            return True
        return False

    def send_callback(self, content):
        """Send callback"""
        callback_query = content.get('callback_query') if content else None
        callback_query_id = callback_query.get('id') if callback_query else None
        if callback_query_id:
            params = {
                'callback_query_id': callback_query_id,
                'text': self.callback_text,
                'url': self.callback_url,
                'show_alert': self.show_alert,
                'cache_time': self.cache_time,
            }
            response_content = self.tg_bot.answer_callback_query(**params)
            log.info(response_content)
