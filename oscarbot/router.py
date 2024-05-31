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
        if path:
            if any([i.isspace() for i in path]):
                path = self.refactoring_path(path)
            path_list = path.split('/')
            pattern_list = self.pattern.split('/')
            self.params = dict()

            if len(pattern_list) == len(path_list):
                for i in range(len(path_list)):
                    if len(pattern_list[i]) > 1:
                        if pattern_list[i][0] != '<':
                            if path_list[i] != pattern_list[i]:
                                return False
                        else:
                            self.params[pattern_list[i]] = path_list[i]
                return True
        return False

    def refactoring_path(self, path: str) -> str:
        """Refactoring path"""
        path_result = ''
        space = False
        for p in path:
            if p.isspace():
                if not space:
                    p = '/<'
                    space = True
                else:
                    p = '>/'
                    space = False
            path_result += p
        if space:
            path_result += '>/'
        return path_result

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
            print('Failed to load router')
            return False, False

        return func, arguments

    @staticmethod
    def __collect_all_routes() -> list:
        import importlib
        all_routes = []
        if len(settings.OSCARBOT_APPS) > 0:
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
