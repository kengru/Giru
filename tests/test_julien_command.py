from unittest import TestCase
from unittest.mock import MagicMock

from giru.core.commands import Julien
from giru.core.commands import julien as JULIEN_PICTURES
from tests.mixins import CommandTestCaseMixin


class JulienCommandTestCase(CommandTestCaseMixin, TestCase):
    def test_it_sends_a_photo(self):
        expected_chat_id = 123
        update = self.create_mock_update_with_chat_id_and_message(expected_chat_id)

        self.bot.send_photo = MagicMock()

        Julien(self.bot, update)

        self.assertIsNotNone(self.bot.send_photo.call_args)

        args, kwargs = self.bot.send_photo.call_args

        photo = kwargs.get("photo")

        self.assertIn(photo, JULIEN_PICTURES)
