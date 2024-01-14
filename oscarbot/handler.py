import importlib

from django.conf import settings

from oscarbot.action import Action
from oscarbot.bot import Bot
from oscarbot.models import User
from oscarbot.response import TGResponse
from oscarbot.router import Router
from oscarbot.structures import Message


class BaseHandler:

    # logger: Logger

    def __init__(self, bot, content):
        self.bot_model = bot
        self.bot = Bot(bot.token)
        self.content = content
        self.message = Message(content)
        print(content)
        print(self.message.__dict__)
        self.user = self.__find_or_create_user_in_db()

    def __find_or_create_user_in_db(self):
        if self.message.user:
            user_in_db, _ = User.objects.update_or_create(
                t_id=self.message.user.id,
                defaults={
                    "username": self.message.user.username,
                    "name": f'{self.message.user.first_name} {self.message.user.last_name}'
                },
            )
            return user_in_db
        return None

    @staticmethod
    def __send_do_not_understand():
        return TGResponse(
            message="Извините, я не понимаю Вас :("
        )

    def handle(self) -> TGResponse:
        if self.message.data:
            return self.__handle_callback_data(self.message.data)
        elif self.message.text:
            return self.__handle_text_data()
        elif self.message.photo:
            return self.__handle_photo_data()
        elif self.message.document:
            return self.__handle_document_data()
        else:
            return self.__send_do_not_understand()

    def __handle_callback_data(self, path):
        router = Router(path)
        func, arguments = router()

        response = func(user=self.user, **arguments)
        if response:
            return response
        else:
            return self.__send_do_not_understand()

    def __handle_text_data(self):
        if self.message.text[0] == '/':
            return self.__handle_callback_data(self.message.text)

        if self.user.want_action:
            action = Action(self.user, self.message.text)
            return action()

        if settings.TELEGRAM_TEXT_PROCESSOR:
            mod_name, func_name = settings.TELEGRAM_TEXT_PROCESSOR.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            text_processor = getattr(mod, func_name)
            response = text_processor(self.user, self.message.text)
            if response:
                return response

        return self.__send_do_not_understand()

    def __handle_photo_data(self):
        """ WIP: """
        return TGResponse(
            message=''
        )

    def __handle_document_data(self):
        """ WIP: """
        return TGResponse(
            message=''
        )
