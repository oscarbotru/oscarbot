import json

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BaseBot(models.Model):
    t_id = models.CharField(max_length=100, default='', verbose_name='Telegram ID')
    token = models.CharField(max_length=255, **NULLABLE, verbose_name='Bot token')
    name = models.CharField(max_length=250, default='', verbose_name='Name')
    username = models.CharField(max_length=250, default='', verbose_name='Username')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    class Meta:
        abstract = True


class Bot(BaseBot):
    pass


class Message(models.Model):
    message_id = models.BigIntegerField()
    update_id = models.BigIntegerField()
    from_id = models.BigIntegerField()
    text = models.TextField(**NULLABLE)
    data = models.TextField(**NULLABLE)

    created = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    t_id = models.CharField(max_length=100, default='', verbose_name='Telegram ID')
    username = models.CharField(max_length=200, default='', verbose_name='Username')
    name = models.CharField(max_length=200, default='', verbose_name='Имя')
    last_message_id = models.BigIntegerField(**NULLABLE, verbose_name='Номер последнего сообщения')
    want_action = models.CharField(max_length=250, **NULLABLE)
    state_information = models.TextField(**NULLABLE)

    def update_last_sent_message(self, response_content):
        response_dict = json.loads(response_content)
        if response_dict.get('ok'):
            self.last_message_id = response_dict.get('result').get('message_id')
            self.save()


class Constructor(models.Model):
    pass
