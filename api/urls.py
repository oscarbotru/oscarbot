from django.urls import path

from oscarbot.views import bot_view

app_name = 'api'

urlpatterns = [
    path('bot<str:token>/', bot_view),
]
