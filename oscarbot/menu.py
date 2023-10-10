import json


class Button:

    def __init__(self, text, callback=None, url=None):
        self.text = text
        self.callback = callback
        self.url = url

    def build(self):
        menu_button = {
            'text': self.text
        }
        if self.callback is not None:
            menu_button['callback_data'] = self.callback
        elif self.url is not None:
            menu_button['url'] = self.url
        return menu_button


class Menu:

    def __init__(self, button_list: list, buttons_in_line=1):
        self.button_list = button_list
        self.buttons_in_line = buttons_in_line

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
        return json.dumps({'inline_keyboard': menu_items})
