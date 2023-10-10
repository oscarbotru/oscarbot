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

* Menu and Buttons builder
* Message builder
* Update messages available


## Links

- Project homepage: https://oscarbot.site/
- Repository: https://github.com/oscarbotru/oscarbot/

## Licensing

The code in this project is licensed under MIT license.