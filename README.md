# TG Core from Oscar
> Telegram bot core only for webhooks way working

Telegram bot core, created in django style with routing and views(handlers) where you
can use included builders for menu or messages 

## Installing / Getting started

This is package only for using with Django project.

```shell
pip install django-oscarbot
```

### Initial Configuration

In settings.py file you need to specify application for tg use:
```python
OSCARBOT_APPS = ['main']

# set Telegram api token in your env variables TELEGRAM_API_TOKEN
TELEGRAM_API_TOKEN = '1234567890:AaBbCcDd...'

# set Telegram api url in your env variables TELEGRAM_URL
TELEGRAM_URL = 'https://api.telegram.org/bot'

# set location Bot model
OSCARBOT_BOT_MODEL = 'oscarbot.Bot'

# set location Bot User model
OSCARBOT_BOT_USER_MODEL = 'oscarbot.User'

# set the location of the TextProcessor to process user messages
TELEGRAM_TEXT_PROCESSOR = 'your_app.text_processor.handler'

# set the text of the message that the bot will send if it does not understand how to process it (not required).
NOT_UNDERSTAND_MESSAGE = 'Sorry, I do not understand you.'

# set a menu for the message that the bot will send if it does not understand how to process it (not required).
NOT_UNDERSTAND_MENU = 'your_app.menus.your_menu'  # Default - None

# whether to update the message when the bot does not understand how to process the user's message (not required).
NOT_UNDERSTAND_NEED_UPDATE = False  # Default - False

# Whether to delete a message if the bot does not understand how to process a user's message (not required).
NOT_UNDERSTAND_IS_DELETE_MESSAGE = True  # Default - False

# set Telegram message parse mode (not required):
TELEGRAM_PARSE_MODE = 'MARKDOWN'  # Default - 'HTML'

```
Run django server and open [localhost:8000/admin/](http://localhost:8000/admin/) and create new bot, 
at least fill bot token for testing ability
## Features
* User model
```python

from oscarbot.models import User

some_user = User.objects.filter(username='@maslov_oa').first()

```

* Menu and Buttons builder
```python
from oscarbot.menu import Menu, Button


button_list = [
    Button(text='Text for callback', callback='/some_callback/'),
    Button(text='Text for external url', url='https://oscarbot.site/'),
    Button(text='Web app view', web_app='https://oscarbot.site/'),
]

menu = Menu(button_list)

```

* Message builder
```python
from oscarbot.shortcut import QuickBot

quick_bot = QuickBot(
    chat=111111111,
    message='Hello from command line',
    token='token can be saved in DB and not required'
)
quick_bot.send()
```

* Application with routing and views(handlers):

    [example application](https://github.com/oscarbotru/oscarbot/tree/master/example/)

* Command to add or update a bot in the database
```shell
python manage.py create_bot_db
```

* Long polling server for testing
```shell
python manage.py runbot
```

* Update messages available
```python
# TODO: work in progress
```

* Messages log
```python
# TODO: work in progress
```

## Project Structure
```
Django-project
├── first_app/
├── second_app/
├── config/
├── main
│   ├── menus
│   │   ├── __init__.py
│   │   └── start_menu.py
│   ├── views
│   │   ├── __init__.py
│   │   └── start.py
│   ├── __init__.py
│   ├── actions.py  
│   ├── admin.py  
│   ├── app.py  
│   ├── models.py  
│   ├── router.py
│   └── text_processor.py
├ manage.py
├ requirements.txt
```

### Example menus/start_menu.py
```python
from oscarbot.menu import Button, Menu


def get_start_menu() -> Menu:
    """Get start menu."""
    feedback_url = 'https://example.com'
    buttons = [
        Button('Home', callback='/start'),
        Button('Page', callback='/my_router/'),
        Button('Feedback', url=feedback_url),
    ]
    return Menu(buttons)
```

### Example views/start.py
```python
from oscarbot.response import TGResponse

from main.actions import YOUR_ACTION
from main.menus import start_menu
from users.models import TGUser


def star(user: TGUser) -> TGResponse:
    """Home."""
    user.clean_state()  # clean want_action and state_information
    user.want_action = YOUR_ACTION
    user.save()
    message = 'Welcome!'
    menu = start_menu.get_start_menu()
    return TGResponse(message, menu, need_update=False)
```

### Example actions.py
```python
from oscarbot.response import TGResponse

from main.menus import start_menu
from users.models import TGUser

YOUR_ACTION = 'main.action__your_action'


def action__your_action(user: TGUser, message: str) -> TGResponse:
    """Action."""
    user.state_information = message  # your logic
    user.save()
    message_response = 'Your message'
    menu = start_menu.get_start_menu()
    return TGResponse(message_response, menu, need_update=True, is_delete_message=True)
```

# Example models.py
```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from oscarbot.models import BaseUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """User model."""

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class TGUser(BaseUser):
    """Telegram user."""
    user = models.OneToOneField(User, models.SET_NULL, **NULLABLE, related_name='tg_user', verbose_name='user tg')

    class Meta:
        verbose_name = 'profile Telegram'
        verbose_name_plural = 'profiles Telegram'

    def __str__(self):
        return f'{self.t_id}'

```

### Example router.py
```python
from oscarbot.router import route

from main.views import start

routes = [
    route('/start', start),
]
```

### Example text_processor.py
```python
from oscarbot.response import TGResponse

from main.menus import start_menu
from users.models import TGUser


def handler(user: TGUser, message: dict) -> TGResponse:
    """Handler."""
    message_response = 'Your message'
    menu = start_menu.get_start_menu()
    return TGResponse(message_response, menu)
```

## Links

- Project homepage: https://oscarbot.site/
- Repository: https://github.com/oscarbotru/oscarbot/

## Licensing

The code in this project is licensed under MIT license.