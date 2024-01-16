import importlib
from inspect import getmembers

from django.conf import settings


class Action:

    def __init__(self, user, message):
        self.actions = self.__collect_all_actions()
        self.user = user
        self.message = message

    def __call__(self):
        if self.user.want_action:
            if self.user.want_action in self.actions.keys():
                action = self.actions[self.user.want_action]
                if action:
                    return action(self.user, self.message)
        self.user.want_action = None
        self.user.save()
        return None

    @staticmethod
    def __collect_all_actions() -> dict:
        all_actions = {}
        if len(settings.OSCARBOT_APPS) > 0:
            for app in settings.OSCARBOT_APPS:
                try:
                    module_name = f'{app}.actions'
                    action_item = importlib.import_module(module_name)
                    for action in dir(action_item):
                        if action.startswith('action__'):
                            all_actions[f'{app}.{action}'] = getattr(action_item, action)
                            all_actions[f'{app}.{action[8:]}'] = getattr(action_item, action)
                except ImportError as ex:
                    print(ex)
        return all_actions
