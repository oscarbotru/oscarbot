from quopri import needsquoting

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
        message=get_msg(text_args=['qweqwe', 'qwdqweqw']),
        menu=menu,
    )
