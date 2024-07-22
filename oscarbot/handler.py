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

    def __send_do_not_understand(self):
        if self.user:
            self.user.last_message_id = None
            self.user.save()
        message = "Извините, я не понимаю Вас :("
        if getattr(settings, 'NOT_UNDERSTAND_MESSAGE', None):
            message = settings.NOT_UNDERSTAND_MESSAGE
        return TGResponse(message=message)

    def handle(self) -> TGResponse:
        if hasattr(self.message, 'data') and self.message.data:
            return self.__handle_callback_data(self.message.data)
        elif hasattr(self.message, 'text') and self.message.text:
            return self.__handle_text_data()
        elif hasattr(self.message, 'photo') and self.message.photo:
            return self.__handle_photo_data()
        elif hasattr(self.message, 'document') and self.message.document:
            return self.__handle_document_data()
        else:
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

        if settings.TELEGRAM_TEXT_PROCESSOR:
            response = self.__get_text_handler()
            if response:
                return response

        return self.__send_do_not_understand()

    def __handle_photo_data(self):
        """ WIP: """
        photos = []
        for file in self.message.photo:
            file_id = file['file_id']
            res = requests.get(f'{settings.TELEGRAM_URL}{self.token}/getFile?file_id={file_id}')
            file_path = res.json()['result']['file_path']
            photos.append(
                f'https://api.telegram.org/file/bot{self.token}/{file_path}'
            )

        if settings.TELEGRAM_TEXT_PROCESSOR:
            response = self.__get_text_handler(photo=photos)
            if response:
                return response

        return self.__send_do_not_understand()

    def __handle_document_data(self):
        """ WIP: """
        return TGResponse(
            message=''
        )
