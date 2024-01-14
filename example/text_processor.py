from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def handler(text):
    if text == 'привет':
        message = 'Привет, я бот'
    elif text == 'пока':
        message = 'Пока, я бот'
    else:
        message = 'Я не знаю такой команды'

    # menu = Menu([
    #     Button("Да", callback="/diagnostic/"),
    # ])

    return TGResponse(
        message=message,
        # menu=menu
    )
