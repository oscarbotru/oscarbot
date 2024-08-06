from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def handler(user, voice):
    message = 'Получил аудио сообщение'
    print(voice)
    user.want_action = 'example.do_something'
    user.save()
    # menu = Menu([
    #     Button("Да", callback="/diagnostic/"),
    # ])

    return TGResponse(
        message=message,
        # menu=menu
        need_update=False
    )
