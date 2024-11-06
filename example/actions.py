from oscarbot.response import TGResponse


def action__do_something(user, message):
    return TGResponse(
        message='Выполняю что-то'
    )
