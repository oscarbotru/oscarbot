from django.test import TestCase

from oscarbot.models import Bot


class SmokeTestCase(TestCase):

    def setUp(self) -> None:
        self.token = 'token'
        self.bot = Bot.objects.create(
            t_id=1,
            username='oscarbot',
            token=self.token
        )

    def __get_command(self, command):
        command = '''{"update_id": 1,"callback_query": {"id": "1","from": {"id": 310780174,"is_bot": false, ''' \
                  '''"first_name": "Oleg","last_name": "Maslov","username": "maslov_oa","language_code": "en"},''' \
                  '''"message": {"message_id": 1,"from": {"id": 310780174,"is_bot": true,"first_name": ''' \
                  '''"Auto Seller","username": "autoseller_oscar_bot"},"chat": {"id": 310780174,"first_name": ''' \
                  '''"Oleg","last_name": "Maslov","username": "maslov_oa","type": "private"},"date": 1616245487,''' \
                  '''"text": "test","chat_instance": "310780174","data": "''' + command + '''"}}'''
        return command

    def __get_text(self, text):
        text = '''{"update_id": 1,"message": {"message_id": 1,"from": {"id": 310780174,"is_bot": false,''' \
               '''"first_name": "Oleg","last_name": "Maslov","username": "maslov_oa","language_code": "en"},''' \
               '''"chat": {"id": 310780174,"first_name": "Oleg","last_name": "Maslov","username": "maslov_oa",''' \
               '''"type": "1"},"date": 310780174,"text": "''' + text + '''","entities": [{"offset": 0,''' \
               '''"length": 6,"type": "bot_command"}]}}'''
        return text

    def test_smoke_bot(self):
        response = self.client.post(
            f'/api/bot{self.token}/',
            data=self.__get_command('/course/1/'),
            content_type='application/json'
        )

        self.assertEquals(
            response.status_code,
            200
        )
