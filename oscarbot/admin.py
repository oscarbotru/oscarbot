from django.contrib import admin

from oscarbot.models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('t_id', 'username', 'name')
    # readonly_fields = ('token', )
