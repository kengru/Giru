from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from telegram import Bot, Update
from telegram.ext import MessageHandler

from giru.core.repliers import OnMatchPatternSendTextMessageReplier, load_text_repliers_from_csv_file
from tests.mocks import MockMessage


class OnMatchPatternSendTextMessageReplierTestCase(TestCase):
    def setUp(self):
        self.bot = Mock(spec=Bot)
        self.update = Mock(spec=Update)

    def test_it_matches_a_given_pattern(self):
        pattern = r'(foo)'
        expected_reply = 'bar'
        replier = OnMatchPatternSendTextMessageReplier(pattern=pattern, message_content=expected_reply)
        message = MockMessage(text='A message matching pattern foo')

        self.assertTrue(replier.filter(message))

    def test_text_reply_is_sent_if_pattern_is_matched(self):
        pattern = r'(foo)'
        expected_reply_content = 'bar'
        replier = OnMatchPatternSendTextMessageReplier(pattern=pattern, message_content=expected_reply_content)
        message = MockMessage(text='A message matching pattern foo')

        self.simulate_message_is_sent(message)

        reply = replier.reply(self.bot, self.update)

        self.assertEqual(reply.text, expected_reply_content)

    def test_it_does_not_reply_if_pattern_is_not_matched(self):
        pattern = r'(foo)'
        replier = OnMatchPatternSendTextMessageReplier(pattern=pattern, message_content='bar')
        message = MockMessage(text='Message')

        self.assertFalse(replier.filter(message))

    def simulate_message_is_sent(self, message):
        self.update.message = message
        self.bot.send_message = MagicMock(side_effect=lambda **kwargs: MockMessage(text=kwargs.get('text')))

    def test_can_be_converted_to_message_handler(self):
        replier = OnMatchPatternSendTextMessageReplier(pattern='foo', message_content='match!')
        message_handler = replier.to_message_handler()

        self.assertTrue(isinstance(message_handler, MessageHandler))


class LoadTextRepliersFromCSVFileTestCase(TestCase):
    def setUp(self):
        self.file = StringIO('(foo),match')

    def test_it_can_load_text_repliers_from_csv_file(self):
        repliers = load_text_repliers_from_csv_file(self.file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text='foo')))
