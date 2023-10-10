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

# set Telegram api url:
TELEGRAM_URL = ''
# set Telegram message parse mode:
TELEGRAM_PARSE_MODE = 'HTML'
# or
TELEGRAM_PARSE_MODE = 'MARKDOWN'
```
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
]

menu = Menu(button_list)

```

* Message builder
```python
from oscarbot.response import TGResponse
from oscarbot.bot import Bot

token = 'telegram bot token from @BotFather'
bot = Bot(token)

tg_response = TGResponse(
    message='Some text',
    menu=menu  # from menu builder
)

tg_response.send(token, user=user)  # user from user model point
# or 
tg_response.send(token, t_id=1111111)  # user's telegram id
```

* Update messages available
```python
# TODO: work in progress
```

* Messages log
```python
# TODO: work in progress
```


## Links

- Project homepage: https://oscarbot.site/
- Repository: https://github.com/oscarbotru/oscarbot/

## Licensing

The code in this project is licensed under MIT license.