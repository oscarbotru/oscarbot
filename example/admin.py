from django.contrib import admin

from oscarbot.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('t_id',)