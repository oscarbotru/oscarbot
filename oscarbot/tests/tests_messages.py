from unittest.mock import patch

from django.test import TestCase

from oscarbot.messages import get_msg
from oscarbot.tests.conf import mock_yaml_load


class MessagesTestCase(TestCase):
    DEFAULT_HELLO = '\' Hello! \''
    DONT_KNOW = '\'Sorry, i do not know this command\''

    @patch("yaml.load", mock_yaml_load)
    def test_get_msg_basic(self):
        """ Positive test for get message only by alias """
        got_msg = get_msg('start')

        self.assertEqual(got_msg, self.DEFAULT_HELLO)

    @patch("yaml.load", mock_yaml_load)
    def test_get_msg_with_args(self):
        """ Positive test for get message by alias and args """
        first_arg = 'test1'
        second_arg = 'test2'
        got_msg = get_msg('args', text_args=[first_arg, second_arg])

        self.assertEqual(got_msg, f'\' Hello! {first_arg}, {second_arg} \'')

    @patch("yaml.load", mock_yaml_load)
    def test_get_msg_not_found(self):
        """ Negative test for get message """
        got_msg = get_msg('some_alias')

        self.assertEqual(got_msg, self.DONT_KNOW)

    @patch("yaml.load", mock_yaml_load)
    def test_get_msg_by_func_name(self):
        """ Positive test for get message by func name """
        def start():
            return get_msg()

        result = start()

        self.assertEqual(result, self.DEFAULT_HELLO)
