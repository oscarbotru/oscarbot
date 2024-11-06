import inspect
import os

import yaml
from django.conf import settings
from typing_extensions import LiteralString

from oscarbot.router import Router


class ResponseMessage:
    FILE_NAME = 'messages.yaml'

    @classmethod
    def find_message(cls, alias, path='messages'):
        for app_item in settings.OSCARBOT_APPS:
            app_message_file_path = os.path.join(settings.BASE_DIR, app_item, cls.FILE_NAME)
            with open(app_message_file_path, 'r', encoding='utf8') as messages_file:
                messages_data = yaml.load(messages_file, yaml.Loader)
                message_text = messages_data[path].get(alias)
                if message_text:
                    return message_text

        return None

    @classmethod
    def collect(cls):
        """ Collect all routers in messages if not exists """
        for app_item in settings.OSCARBOT_APPS:

            new_keys = []
            router = Router('')
            for route in router.routes:
                new_keys.append(route.func.__name__)

            app_message_file_path = os.path.join(settings.BASE_DIR, app_item, cls.FILE_NAME)

            with open(app_message_file_path, 'r', encoding='utf8') as messages_file:
                messages_data = yaml.load(messages_file, yaml.Loader)

            for key in new_keys:

                if key not in messages_data.get('messages', {}).keys():
                    messages_data['messages'][key] = '\'  \''

            cls._save_to_file(messages_data, app_message_file_path)

    @staticmethod
    def _save_to_file(data: dict, path: LiteralString | str | bytes) -> None:
        """ Update file with messages """
        with open(path, 'w', encoding='utf8') as messages_file:
            messages_file.write("# To set multilines message text use triple quotes ''' set text here '''\n\n")
            yaml.preserve_quotes = True
            yaml.explicit_start = True
            yaml.dump(data=data, stream=messages_file)

    @classmethod
    def make_template(cls, force=False):
        """ Create empty default messages files """
        for app_item in settings.OSCARBOT_APPS:
            app_message_file_path = os.path.join(settings.BASE_DIR, app_item, cls.FILE_NAME)

            if os.path.exists(app_message_file_path) and not force:
                print(f'Messages file for "{app_item}" application exists')
            else:
                data = {
                    'messages': {'start': '\'  \''},
                    'defaults': {'text_processor': '\'  \'', 'dont_know': '\'Sorry, i do not know this command\'',
                                 'voice_processor': '\'  \''}
                }

                cls._save_to_file(data, app_message_file_path)


def get_msg(alias=None, text_args: list | None = None) -> str:
    """ Find message by alias """
    if text_args is None:
        text_args = []

    if alias is None:
        alias = inspect.stack()[1][3]

    final_message = ResponseMessage.find_message(alias)
    if final_message:
        counter = 1
        for arg in text_args:
            final_message = final_message.replace(f'{{{counter}}}', arg)
            counter += 1

        return final_message

    return ResponseMessage.find_message('dont_know', 'defaults')
