from abc import ABC
from random import randint

from tests.mocks import MockBot, MockUpdate, MockMessage, MockChat


class CommandTestCaseMixin(ABC):
    bot = None

    def setUp(self):
        self.bot = MockBot()

    def create_mock_update_with_chat_id_and_message(self, chat_id=randint(1, 1000), message='', reply_to_message=None):
        return MockUpdate(message=MockMessage(chat=MockChat(chat_id), text=message, reply_to_message=reply_to_message))

    def create_mock_update_with_chat_id_message_and_user(self, chat_id=randint(1, 1000), message='', from_user=None):
        return MockUpdate(message=MockMessage(chat=MockChat(chat_id), text=message, from_user=from_user))
