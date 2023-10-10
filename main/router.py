from main.views import some_message, some_messages, start
from oscarbot.router import route

routes = [
    route('/courses/', some_messages),
    route('/course/<pk>/', some_message),
    route('/start', start)
]
