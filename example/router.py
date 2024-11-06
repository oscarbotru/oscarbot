from example.views import start, first_question
from oscarbot.router import route

routes = [
    route('/start', start),
    route('/diagnostic/', first_question),
    route('/hello/', first_question),
    route('/hello/<pk>/', first_question),
]
