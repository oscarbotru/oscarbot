from django.urls import path

from oscarbot.views import bot_view

app_name = 'oscarbot'

urlpatterns = [
    path('api/bot<str:token>/', bot_view),
]
