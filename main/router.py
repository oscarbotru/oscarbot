from main.views import start, category_products, categories
from oscarbot.router import route

routes = [
    route('/start', start),

    route('/categories/', categories),
    route('/category/<pk>/', category_products),

]
