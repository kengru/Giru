from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from tests.mixins import CommandTestCaseMixin

load_empty_scores_file = MagicMock(side_effect=FileNotFoundError)
load_scores_file = MagicMock(return_value={'giru': 1000})


class ScoresCommandTestCase(CommandTestCaseMixin, TestCase):
    @patch('pickle.load', load_empty_scores_file)
    def test_it_sends_a_no_score_message_if_scores_file_is_not_found(self):
        expected_chat_id = 123
        self.bot.send_message = MagicMock()

        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id)

        from giru.commands import Scores

        Scores(self.bot, update)

        self.bot.send_message.assert_called_with(chat_id=expected_chat_id, parse_mode="Markdown", text="No hay scores.")

    @patch('pickle.load', load_scores_file)
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    def test_it_sends_scores(self, mock_file):
        expected_chat_id = 123
        expected_message_text = "*Scores:*\n\n" \
                                "*giru:*  1000\n"

        self.bot.send_message = MagicMock()

        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id)

        from giru.commands import Scores

        Scores(self.bot, update)

        self.bot.send_message.assert_called_with(chat_id=expected_chat_id, parse_mode="Markdown",
                                                 text=expected_message_text)
