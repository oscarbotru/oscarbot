class RouteDoesNotExist(Exception):

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Route does not exists'
