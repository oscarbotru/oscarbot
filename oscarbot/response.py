import json

from django.conf import settings

from oscarbot.bot import Bot
from oscarbot.bot_logger import log


class TGResponse:

    def __init__(self, message: str, menu=None, need_update: bool | None = None, photo=None, attache=None, video=None,
                 file=None, media_group: list[dict] = None, media_group_type='photo', has_spoiler=False, protect=False,
                 callback_text='', callback_url=False, show_alert=False, cache_time=None,
                 disable_web_page_preview=False, is_delete_message=False) -> None:
        need_update_setting = settings.TELEGRAM_NEED_UPDATE if getattr(settings, 'TELEGRAM_NEED_UPDATE', None) else True
        self.tg_bot = None
        self.message = message
        self.menu = menu
        self.attache = attache
        self.need_update = need_update if need_update is not None else need_update_setting
        self.photo = photo
        self.video = video
        self.file = file
        self.media_group = media_group if media_group else None
        self.media_group_type = media_group_type
        self.has_spoiler = has_spoiler
        self.protect = protect
        self.parse_mode = settings.TELEGRAM_PARSE_MODE if getattr(settings, 'TELEGRAM_PARSE_MODE', None) else 'HTML'
        self.callback_url = callback_url
        self.callback_text = callback_text
        self.show_alert = show_alert
        self.cache_time = cache_time
        self.disable_web_page_preview = disable_web_page_preview
        self.is_delete_message = is_delete_message

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
            'disable_web_page_preview': self.disable_web_page_preview,
            'file': self.file,
            'is_delete_message': self.is_delete_message,
        }

        if self.media_group:
            data_to_send['media_group'] = self.media_group
            data_to_send['media_group_type'] = self.media_group_type
            data_to_send['has_spoiler'] = self.has_spoiler
            self.need_update = False

        update_chat_message = True
        update_chat_attr = getattr(settings, 'UPDATE_CHAT_MESSAGE', None)
        if update_chat_attr is not None:
            update_chat_message = update_chat_attr

        if update_chat_message:
            message_id = None
            if content:
                message = content.get('message')
                if not message:
                    callback_query = content.get('callback_query')
                    message = callback_query.get('message') if callback_query else None
                if message:
                    message_id = message.get('message_id')
        else:
            message_id = user.last_message_id
        data_to_send['message_delete'] = message_id

        if self.need_update:
            response_content = self.tg_bot.update_message(**data_to_send, message_id=message_id)
            response_dict = json.loads(response_content)
            if not response_dict.get('ok'):
                if self.is_delete_message:
                    response_content = self.tg_bot.update_message(**data_to_send, message_id=user.last_message_id)
        else:
            response_content = self.tg_bot.send_message(**data_to_send)
        log.info(response_content)
        if user:
            user.update_last_sent_message(response_content)

    def can_send(self):
        if self.message is not None or self.video is not None or self.photo is not None:
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
