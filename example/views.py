from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def start(user):
    menu = Menu([
        Button("Начнем", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        video='https://file-examples.com/storage/fe5048eb7365a64ba96daa9/2017/04/file_example_MP4_480_1_5MG.mp4'
        # menu=menu
    )


def first_question(user):
    menu = Menu([
        Button("Да", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        menu=menu
    )
