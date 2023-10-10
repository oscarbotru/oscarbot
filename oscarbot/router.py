from django.conf import settings


def route(path, func):
    return Route(path, func)


class Route:

    def __init__(self, pattern, func):
        self.pattern = pattern
        self.func = func
        self.params = dict()

    def __repr__(self):
        return self.pattern

    def check(self, path):
        path_list = path.split('/')
        pattern_list = self.pattern.split('/')
        self.params = dict()

        if len(pattern_list) == len(pattern_list):
            for i in range(len(path_list)):
                if len(pattern_list[i]) > 1:
                    if pattern_list[i][0] != '<':
                        if path_list[i] != pattern_list[i]:
                            return False
                    else:
                        self.params[pattern_list[i]] = path_list[i]
            return True
        return False

    def get_params(self):
        params = dict()
        for k, v in self.params.items():
            k = k.replace('<', '').replace('>', '')
            params[k] = v
        return params


class Router:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.routes = self.__collect_all_routes()

    def __call__(self):
        func, arguments = self.__recognise()
        if func == arguments is None:
            raise ModuleNotFoundError(f'Failed to load router')

        return func, arguments

    @staticmethod
    def __collect_all_routes() -> list:
        import importlib
        all_routes = []
        for app in settings.OSCARBOT_APPS:
            try:
                module_name = f'{app}.router'
                route_item = importlib.import_module(module_name)
                all_routes.extend(route_item.routes)
            except ImportError as ex:
                print(ex)
        return all_routes

    def __recognise(self):
        for route_item in self.routes:
            if route_item.check(self.path):
                return route_item.func, route_item.get_params()

        return None, None
