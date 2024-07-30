import datetime
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

    def __str__(self):
        return self.t_id


class Bot(BaseBot):
    pass


class Message(models.Model):
    message_id = models.BigIntegerField()
    update_id = models.BigIntegerField()
    from_id = models.BigIntegerField()
    text = models.TextField(**NULLABLE)
    data = models.TextField(**NULLABLE)

    created = models.DateTimeField(auto_now_add=True)


class BaseUser(models.Model):
    t_id = models.CharField(max_length=100, default='', verbose_name='Telegram ID')
    username = models.CharField(max_length=200, default='', verbose_name='Username', null=True, blank=True)
    name = models.CharField(max_length=200, default='', verbose_name='Имя', null=True, blank=True)
    last_message_id = models.BigIntegerField(**NULLABLE, verbose_name='Номер последнего сообщения')
    want_action = models.CharField(max_length=250, **NULLABLE)
    last_path = models.CharField(max_length=250, **NULLABLE, default='/start')
    path = models.CharField(max_length=250, **NULLABLE)
    state_information = models.TextField(**NULLABLE)
    created = models.DateTimeField('Creation date', default=datetime.datetime.now)

    def update_last_sent_message(self, response_content):
        response_dict = json.loads(response_content)
        if response_dict.get('ok'):
            result = response_dict.get('result')
            if isinstance(result, dict):
                last_message_id = result.get('message_id')
                self.last_message_id = last_message_id
            else:
                self.last_message_id = None
            self.save()

    def update_path(self, path):
        """Update path."""
        self.last_path = self.path if self.path else '/start'
        self.path = path
        self.save()

    def clean_state(self):
        """ Clean state of user, can be used in actions """
        self.want_action = None
        self.state_information = None
        self.save()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.t_id}'


class User(BaseUser):
    pass


class Constructor(models.Model):
    pass
