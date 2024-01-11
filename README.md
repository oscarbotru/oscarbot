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

# set Telegram api url in your env variables TELEGRAM_URL
# set Telegram message parse mode:
TELEGRAM_PARSE_MODE = 'HTML'
# or
TELEGRAM_PARSE_MODE = 'MARKDOWN'
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


## Links

- Project homepage: https://oscarbot.site/
- Repository: https://github.com/oscarbotru/oscarbot/

## Licensing

The code in this project is licensed under MIT license.