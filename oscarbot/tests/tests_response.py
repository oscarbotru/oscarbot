from unittest.mock import patch

from django.test import TestCase

from oscarbot.models import User
from oscarbot.response import TGResponse
from oscarbot.tests.conf import mock_yaml_load


class ResponseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(t_id=1)

    @patch("yaml.load", mock_yaml_load)
    def test_add_message_to_response(self):
        """ Make response with auto got message text from yaml """
        def start(user):
            return TGResponse(need_update=False)

        called_function = start(self.user)

        self.assertEqual(called_function.message, '\' Hello! \'')
