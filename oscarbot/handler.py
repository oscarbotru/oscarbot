import importlib

import requests
from django.conf import settings

from oscarbot.action import Action
from oscarbot.bot import Bot
from oscarbot.response import TGResponse
from oscarbot.router import Router
from oscarbot.services import get_bot_user_model
from oscarbot.structures import Message


class BaseHandler:

    # logger: Logger

    def __init__(self, token: str, content: str) -> None:
        self.bot = Bot(token)
        self.content = content
        self.message = Message(content)
        self.user = self.__find_or_create_user_in_db()

    def __find_or_create_user_in_db(self):
        if hasattr(self.message, 'user'):
            first_name = self.message.user.first_name if self.message.user.first_name else ''
            last_name = self.message.user.last_name if self.message.user.last_name else ''
            name = f'{first_name} {last_name}'.strip()
            user_in_db, _ = get_bot_user_model().objects.update_or_create(
                t_id=self.message.user.id,
                defaults={
                    "username": self.message.user.username,
                    "name": name,
                },
            )
            return user_in_db
        return None

    @classmethod
    def __send_do_not_understand(cls):
        need_update, is_delete_message, menu = False, False, None
        message = "Извините, я не понимаю Вас :("
        if getattr(settings, 'NOT_UNDERSTAND_MESSAGE', None):
            message = settings.NOT_UNDERSTAND_MESSAGE
        if getattr(settings, 'NOT_UNDERSTAND_NEED_UPDATE', None):
            need_update = settings.NOT_UNDERSTAND_NEED_UPDATE
        if getattr(settings, 'NOT_UNDERSTAND_IS_DELETE_MESSAGE', None):
            is_delete_message = settings.NOT_UNDERSTAND_IS_DELETE_MESSAGE
        if getattr(settings, 'NOT_UNDERSTAND_MENU', None):
            mod_name, func_name = settings.NOT_UNDERSTAND_MENU.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            get_menu = getattr(mod, func_name)
            menu = get_menu()
        return TGResponse(message=message, menu=menu, need_update=need_update, is_delete_message=is_delete_message)

    def __work_text_processor(self, photo=None):
        if getattr(settings, 'TELEGRAM_TEXT_PROCESSOR', None):
            response = self.__get_text_handler(photo=photo)
            if response:
                return response
        return self.__send_do_not_understand()

    def handle(self) -> TGResponse:
        if hasattr(self.message, 'data') and self.message.data:
            return self.__handle_callback_data(self.message.data)
        elif hasattr(self.message, 'text') and self.message.text:
            return self.__handle_text_data()
        elif hasattr(self.message, 'photo') and self.message.photo:
            return self.__handle_photo_data()
        elif hasattr(self.message, 'document') and self.message.document:
            return self.__handle_document_data()
        elif hasattr(self.message, 'voice') and self.message.voice:
            return self.__handle_voice_data()
        return self.__work_text_processor()

    def __handle_voice_data(self):
        if getattr(settings, 'TELEGRAM_VOICE_PROCESSOR', None):
            mod_name, func_name = settings.TELEGRAM_VOICE_PROCESSOR.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            audio_processor = getattr(mod, func_name)
            voice_file = self.bot.get_file(self.message.voice.get('file_id'))
            data = {
                'voice': voice_file,
            }
            response = audio_processor(self.user, data)
            if response:
                return response
        return self.__send_do_not_understand()

    def __get_text_handler(self, photo=None):
        mod_name, func_name = settings.TELEGRAM_TEXT_PROCESSOR.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        text_processor = getattr(mod, func_name)
        data = {
            'text': self.message.text,
            'photo': photo,
        }
        response = text_processor(self.user, data)
        if response:
            return response

        return False

    def __handle_callback_data(self, path):
        router = Router(path)
        func, arguments = router()
        if func:
            response = func(self.user, **arguments)
            if response:
                self.user.update_path(path)
                return response
        return self.__send_do_not_understand()

    def __handle_text_data(self):
        if self.message.text[0] == '/':
            return self.__handle_callback_data(self.message.text)

        if self.user.want_action:
            action = Action(self.user, self.message.text)
            return action()

        return self.__work_text_processor()

    def __handle_photo_data(self):
        """ WIP: """
        photos = []
        for file in self.message.photo:
            file_id = file['file_id']
            res = requests.get(f'{settings.TELEGRAM_URL}{self.bot.token}/getFile?file_id={file_id}')
            file_path = res.json()['result']['file_path']
            photos.append(
                f'https://api.telegram.org/file/bot{self.bot.token}/{file_path}'
            )
        return self.__work_text_processor(photo=photos)

    def __handle_document_data(self):
        """ WIP: """
        return self.__work_text_processor()
