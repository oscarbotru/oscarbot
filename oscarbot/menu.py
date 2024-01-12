import json


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

    def __init__(self, button_list: list, buttons_in_line=1, mode='inline'):
        """

        @param button_list:
        @param buttons_in_line:
        @param mode: inline or keyboard
        """
        self.button_list = button_list
        self.buttons_in_line = buttons_in_line
        self.mode = mode

    def build(self):
        menu_items = []
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
            return json.dumps({'inline_keyboard': menu_items})
        else:
            return json.dumps({
                'keyboard': menu_items,
                'resize_keyboard': True,
                'one_time_keyboard': True
            })
