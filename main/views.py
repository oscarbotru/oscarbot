from main.models import Category, Product
from oscarbot.menu import Menu, Button
from oscarbot.response import TGResponse
from oscarbot.shortcut import QuickBot


def category_products(pk):
    buttons = []
    message = "Here is all product of category"

    for category_item in Product.objects.filter(category_pk=pk):
        buttons.append(Button(category_item.title, callback=f"/product/{category_item.pk}/"))
    if len(buttons) > 0:
        menu = Menu(buttons)
    else:
        menu = None
        message = "There is no categories, the shop is empty :("

    return TGResponse(
        message=message,
        menu=menu
    )


def categories():
    buttons = []
    message = "Here is all categories"

    for category_item in Category.objects.all():
        buttons.append(Button(category_item.title, callback=f"/category/{category_item.pk}/"))
    if len(buttons) > 0:
        menu = Menu(buttons)
    else:
        menu = None
        message = "There is no categories, the shop is empty :("

    return TGResponse(
        message=message,
        menu=menu
    )


def start():
    menu = Menu([
        Button("Categories", callback="/categories/")
    ])
    return TGResponse(
        message="Hi!",
        menu=menu
    )
