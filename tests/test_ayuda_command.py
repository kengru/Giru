from unittest import TestCase
from unittest.mock import MagicMock, patch

from tests.mixins import CommandTestCaseMixin
from tests.mocks import MockUser

mock_help = {
    '/command-1': {
        'does something': '/command-1'
    },
    '/command-2': {
        'does something else': '/command-2'
    }
}


class AyudaCommandTestCase(CommandTestCaseMixin, TestCase):
    def setUp(self):
        super(AyudaCommandTestCase, self).setUp()

    @patch('giru.data.ayuda', mock_help)
    def test_it_sends_help(self):
        expected_chat_id = 123
        expected_message_text = "Hola, soy Giru." \
                                "\n\n" \
                                "*Comandos:* \n" \
                                "/command-1: does something\n" \
                                "\t- Ejemplo: _/command-1_\n" \
                                "/command-2: does something else\n" \
                                "\t- Ejemplo: _/command-2_\n"

        self.bot.send_message = MagicMock()
        user = MockUser(id=expected_chat_id)
        update = self.create_mock_update_with_chat_id_message_and_user(chat_id=expected_chat_id, from_user=user)

        from giru.commands import Ayuda

        Ayuda(self.bot, update)

        self.bot.send_message.assert_called_with(chat_id=expected_chat_id, text=expected_message_text,
                                                 parse_mode='Markdown')
