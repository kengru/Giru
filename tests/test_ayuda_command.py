from unittest import TestCase
from unittest.mock import MagicMock

from giru.data import ayuda as ayuda_text
from tests.mixins import CommandTestCaseMixin
from tests.mocks import MockUser

mock_commands = [
    MagicMock(command="command-1"),
    MagicMock(command="command-2"),
    MagicMock(command="start"),
    MagicMock(command="vociao"),
    MagicMock(command="saved"),
    MagicMock(command="julien"),
    MagicMock(command="mepajeo"),
    MagicMock(command="spotify"),
    MagicMock(command="padondehoy"),
    MagicMock(command="cartelera"),
    MagicMock(command="scores"),
]


class AyudaCommandTestCase(CommandTestCaseMixin, TestCase):
    def setUp(self):
        super(AyudaCommandTestCase, self).setUp()

    def test_it_sends_help(self):
        expected_chat_id = 123
        expected_message_regex = (
            r"Hola, soy Giru.\s+"
            r"\*Comandos:\*\s+"
            r"([/\w-]+: [\w\s\?]+?\n"
            r"\s+- [\w/\?]+\: [\w/\?-]+?\n)+"
        )

        self.bot.send_message = MagicMock()
        user = MockUser(id=expected_chat_id)
        update = self.create_mock_update_with_chat_id_message_and_user(
            chat_id=expected_chat_id, from_user=user
        )

        from giru.commands import create_ayuda_cb

        ayuda_cb = create_ayuda_cb(mock_commands, ayuda_text)
        ayuda_cb(self.bot, update)

        kwargs = self.bot.send_message.call_args[1]

        self.assertEqual(expected_chat_id, kwargs["chat_id"])
        self.assertEqual("Markdown", kwargs["parse_mode"])
        self.assertRegex(kwargs["text"], expected_message_regex)
