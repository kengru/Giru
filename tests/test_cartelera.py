from unittest import TestCase

from commands import Cartelera
from tests.mocks import MockBot, MockUpdate


class Test_cartelera(TestCase):

    def test_catalogue_response_same_chat_same_day(self):
        bot = MockBot()
        update = MockUpdate()

        Cartelera(bot, update)
        response_1 = bot.last_message[update.message.chat_id]

        print(response_1)
