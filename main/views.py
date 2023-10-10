from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def some_messages():
    pass


def some_message(pk):
    menu = Menu([
        Button('text', callback='/courses/')
    ])
    return TGResponse(
        message='Test',
        menu=menu
    )
