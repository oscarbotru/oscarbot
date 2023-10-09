from main.views import some_message
from oscarbot.router import route

routes = [
    route('/courses/', some_message)
]
