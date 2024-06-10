import json
import re

from oscarbot.bot_logger import log


class Button:

    def __init__(self, text, callback=None, url=None, web_app=None):
        self.text = text
        self.callback = callback
        self.url = url
        self.web_app = web_app

    def build(self):
        menu_button = {
            'text': self.text
        }
        if self.callback is not None:
            menu_button['callback_data'] = self.callback
        elif self.url is not None:
            menu_button['url'] = self.url
        elif self.web_app is not None:
            menu_button['web_app'] = {'url': self.web_app}
        return menu_button


class Menu:

    def __init__(self, button_list: list, buttons_in_line=1, mode='inline', schema_buttons: str = None):
        """

        @param button_list:
        @param buttons_in_line:
        @param mode: inline or keyboard
        @param schema_buttons: example 1:2:1
        """
        self.button_list = button_list
        self.buttons_in_line = buttons_in_line
        self.mode = mode
        self.schema_buttons = schema_buttons

    def build(self):
        menu_items = []
        if isinstance(self.schema_buttons, str) and re.search(r'^([1-9]:)*[1-9]$', self.schema_buttons):
            self.get_buttons_schema(menu_items)
        else:
            i = 0
            line_menu_items = []
            for menu_button in self.button_list:
                i += 1
                line_menu_items.append(menu_button.build())
                if i == self.buttons_in_line:
                    menu_items.append(line_menu_items)
                    i = 0
                    line_menu_items = []
            menu_items.append(line_menu_items)
        if self.mode == 'inline':
            log.info(f'{menu_items}')
            return json.dumps({'inline_keyboard': menu_items})
        else:
            return json.dumps({
                'keyboard': menu_items,
                'resize_keyboard': True,
                'one_time_keyboard': True
            })

    def get_buttons_schema(self, menu_items: list):
        """Get buttons schema"""
        schema = [int(s) for s in self.schema_buttons.split(':')]
        line_menu_items = []
        i = -1
        for menu_button in reversed(self.button_list):
            line_menu_items.insert(0, menu_button.build())
            try:
                schema_key = schema[i]
            except IndexError:
                if len(schema) == 1:
                    i = -1
                else:
                    i = -2
                schema_key = schema[i]
            if len(line_menu_items) == schema_key:
                menu_items.insert(0, line_menu_items)
                i -= 1
                line_menu_items = []
        if line_menu_items:
            menu_items.insert(0, line_menu_items)
        return menu_items
