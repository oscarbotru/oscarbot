from oscarbot.menu import Menu
from oscarbot.tests.base import TGTestCase


class TestExample(TGTestCase):
    """Example test case."""

    def test_example(self):
        """Example test method."""
        example_router = '/start'

        response = self.call_router(example_router)
        self.assertMessage(response, 'Привет! Мы здесь, чтобы продиагностировать твой бизнес. Начнем?')
        self.assertMenu(response, Menu([]))
        self.assertNeedUpdate(response, True)
