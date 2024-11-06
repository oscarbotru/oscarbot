from django.conf import settings
from django.test import TestCase

from oscarbot.action import Action
from oscarbot.handler import BaseHandler
from oscarbot.menu import Menu
from oscarbot.response import TGResponse
from oscarbot.router import Router
from oscarbot.services import get_bot_user_model


class TGTestCase(TestCase):
    """Base class for testing Telegram bot."""

    def setUp(self):
        """Set up testing environment."""
        self.tg_user = get_bot_user_model().objects.create()

    @staticmethod
    def get_callback_dict(data: str, is_text: bool = True) -> dict:
        """
        Generates content dict for call_text_handler or call_voice_handler.

        :param data: user message text or voice_file_id
        :param is_text: indicates whether the dist is generated for call_text_handler (if True) or call_voice_handler
        :return: Dictionary with arguments for BaseHandler __init__
        """
        content = {
            'callback_query': {
                'message_id': 1,
                'from': {'id': 1, 'is_bot': False, 'first_name': '', 'username': '', 'language_code': 'ru'},
                'chat': {'id': 1, 'first_name': '', 'username': '', 'type': 'private'},
                'date': 1730743912}
        }
        if is_text:
            content['callback_query']['text'] = data
        else:
            content['callback_query']['voice'] = {'file_id': data}
        return content

    def call_router(self, path: str) -> TGResponse:
        """Returns TGResponse based on path."""
        func, args = Router(path)()
        tg_response = func(self.tg_user, **args)
        return tg_response

    def call_action(self, action_path: str) -> TGResponse:
        """Returns TGResponse based on action_path."""
        self.tg_user.want_action = action_path
        tg_response = Action(self.tg_user, '')()
        return tg_response

    def call_text_handler(self, text: str) -> TGResponse:
        """Returns TGResponse based on user input text message."""
        bot_token = None
        if getattr(settings, 'TELEGRAM_API_TOKEN', None):
            bot_token = settings.TELEGRAM_API_TOKEN
        content = self.get_callback_dict(text)
        handler = BaseHandler(bot_token, content)
        tg_response = handler.handle()
        return tg_response

    def call_voice_handler(self, voice_file_id: str) -> TGResponse:
        """Returns TGResponse after procession voice file based on Telegram voice_file_id."""
        bot_token = None
        if getattr(settings, 'TELEGRAM_API_TOKEN', None):
            bot_token = settings.TELEGRAM_API_TOKEN
        content = self.get_callback_dict(voice_file_id, False)
        handler = BaseHandler(bot_token, content)
        tg_response = handler.handle()
        return tg_response

    def assertMenu(self, response: TGResponse, menu: Menu):
        """Asserts that TGResponse contains provided menu."""
        self.assertEqual(len(response.menu.button_list), len(menu.button_list))

        for button_index, response_button in enumerate(response.menu.button_list):
            input_button = menu.button_list[button_index]
            self.assertEqual(response_button.text, input_button.text)
            self.assertEqual(response_button.callback, input_button.callback)
            self.assertEqual(response_button.url, input_button.url)
            self.assertEqual(response_button.web_app, input_button.web_app)

    def assertMessage(self, response: TGResponse, message: str):
        """Asserts that TGResponse 'message' param is equal to provided body."""
        self.assertEqual(response.message, message)

    def assertNeedUpdate(self, response: TGResponse, need_update: bool):
        """Asserts that TGResponse 'need_update' param is equal to provided one."""
        self.assertEqual(response.need_update, need_update)

    def assertUserAction(self, action: str):
        """Asserts that TGUser 'want_action' param is equal to provided one."""
        self.assertEqual(self.tg_user.want_action, action)
