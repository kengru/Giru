from unittest import TestCase
from unittest.mock import MagicMock

from giru.commands import Start
from tests.mixins import CommandTestCaseMixin


class StartCommandTestCase(CommandTestCaseMixin, TestCase):
    def test_start_command_send_a_hello_message(self):
        expected_chat_id = 123
        expected_message_text = 'SOY GIRU MANIN!! Dale "/ayuda".'

        self.bot.send_message = MagicMock()
        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id, expected_message_text)

        Start(self.bot, update)

        self.bot.send_message.assert_called_with(chat_id=expected_chat_id, text=expected_message_text)
