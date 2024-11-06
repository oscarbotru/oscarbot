from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def handler(user, text):
    message = 'Я не знаю такой команды'
    user.want_action = 'example.do_something'
    user.save()
    # menu = Menu([
    #     Button("Да", callback="/diagnostic/"),
    # ])

    return TGResponse(
        message=message,
        # menu=menu
    )
