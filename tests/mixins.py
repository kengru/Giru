from abc import ABC
from random import randint
from unittest import TestCase

from tests.mocks import MockBot, MockUpdate, MockMessage, MockChat


class CommandTestCaseMixin(ABC):
    bot = None

    def setUp(self):
        self.bot = MockBot()

    def create_mock_update_with_chat_id_and_message(self, chat_id=randint(1, 1000), message=''):
        return MockUpdate(message=MockMessage(chat=MockChat(chat_id), text=message))
