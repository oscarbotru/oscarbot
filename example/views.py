from oscarbot.menu import Menu, Button
from oscarbot.messages import get_msg
from oscarbot.response import TGResponse


def start(_):
    return TGResponse(
        need_update=False
    )


def first_question(_):
    menu = Menu([
        Button("Да", callback="/diagnostic/"),
    ])
    return TGResponse(
        message='текст',
        file='https://s16.os-demo.tech/media/file.docx',
    )
