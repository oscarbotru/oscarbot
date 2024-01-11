from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse


def start():
    menu = Menu([
        Button("Начнем", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        menu=menu
    )


def first_question():
    menu = Menu([
        Button("Да", callback="/diagnostic/"),
    ])
    return TGResponse(
        message="Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?",
        menu=menu
    )

