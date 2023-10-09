from django.db import models


class BaseBot(models.Model):
    t_id = models.CharField(max_length=100, default='', verbose_name='Telegram ID')
    token = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bot token')
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
    text = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    t_id = models.CharField(max_length=100, default='', verbose_name='Telegram ID')
    username = models.CharField(max_length=200, default='', verbose_name='Username')
    name = models.CharField(max_length=200, default='', verbose_name='Имя')
