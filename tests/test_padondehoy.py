from unittest import TestCase

from giru.commands import PaDondeHoy
from tests.mocks import MockBot, MockUpdate


class TestPaDondeHoy(TestCase):
    def test_catalogue_response_same_chat_same_day(self):
        bot = MockBot()
        update = MockUpdate()

        PaDondeHoy(bot, update)
        response_1 = bot.last_message[update.message.chat_id]

        PaDondeHoy(bot, update)
        response_2 = bot.last_message[update.message.chat_id]

        self.assertEqual(response_1, response_2)
