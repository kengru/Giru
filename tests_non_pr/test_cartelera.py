from unittest import TestCase, skip

from giru.commands import Cartelera
from tests.mocks import MockBot, MockUpdate


class CarteleraTestCase(TestCase):

    @skip
    def test_catalogue_response_same_chat_same_day(self):
        bot = MockBot()
        update = MockUpdate()

        Cartelera(bot, update)
        response_text = bot.last_message[update.message.chat_id]

        print(response_text)
