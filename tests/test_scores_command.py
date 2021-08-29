from unittest import TestCase
from unittest.mock import MagicMock

from giru.adapters.memory import InMemoryScoreKeeper
from giru.built_in_repliers.repliers import record_points_factory
from giru.core.commands import score_command_factory
from tests.mixins import CommandTestCaseMixin
from tests.mocks import MockChat, MockMessage

load_empty_scores_file = MagicMock(side_effect=FileNotFoundError)
load_scores_file = MagicMock(return_value={"giru": 1000})
load_score_keeper = MagicMock()


class ScoresCommandTestCase(CommandTestCaseMixin, TestCase):
    def setUp(self):
        super(ScoresCommandTestCase, self).setUp()
        self.keeper = InMemoryScoreKeeper()
        self.scores_command = score_command_factory(self.keeper)
        self.record_points_replier = record_points_factory(self.keeper)

    def test_it_sends_a_no_score_message_if_scores_file_is_not_found(self):
        expected_chat_id = 123
        self.bot.send_message = MagicMock()

        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id)

        self.scores_command(self.bot, update)

        self.bot.send_message.assert_called_with(
            chat_id=expected_chat_id, parse_mode="Markdown", text="No hay scores."
        )

    def test_it_sends_scores(self):
        expected_chat_id = 123
        expected_message_text = "*Scores:*\n\n" "*giru:*  1000\n"

        self.keeper.scores = {"giru": 1000}

        self.bot.send_message = MagicMock()

        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id)

        self.scores_command(self.bot, update)

        self.bot.send_message.assert_called_with(
            chat_id=expected_chat_id, parse_mode="Markdown", text=expected_message_text
        )

    def test_scores_are_kept(self):
        expected_chat_id = 123

        self.bot.send_message = MagicMock()

        reply_to = MockMessage(chat=MockChat(expected_chat_id), text="me enciende la")
        update = self.create_mock_update_with_chat_id_and_message(
            expected_chat_id, "+1", reply_to
        )

        self.record_points_replier(self.bot, update)

        self.assertEqual(self.keeper.scores, {expected_chat_id: 1})
