from django.contrib import admin

from oscarbot.models import Bot, Group


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('t_id', 'username', 'name')
    # readonly_fields = ('token', )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('t_id', 'username', 'name')
