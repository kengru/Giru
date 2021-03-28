from unittest import TestCase
from unittest.mock import MagicMock

from giru.commands import Caps
from tests.mixins import CommandTestCaseMixin


class CapsCommandTestCase(CommandTestCaseMixin, TestCase):
    def test_it_sends_a_message_with_back_with_call_caps(self):
        expected_chat_id = 123
        expected_message_text = "THIS IS A TEST!"

        self.bot.send_message = MagicMock()

        update = self.create_mock_update_with_chat_id_and_message(
            expected_chat_id, expected_message_text
        )

        Caps(self.bot, update, ["this is a test"])

        self.bot.send_message.assert_called_with(
            chat_id=expected_chat_id, text=expected_message_text
        )
