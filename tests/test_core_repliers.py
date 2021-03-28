from abc import ABC
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock

from telegram.bot import Bot
from telegram.ext import MessageHandler
from telegram.message import Message
from telegram.update import Update

from giru.core.repliers import (
    OnMatchPatternSendTextMessageReplier,
    load_repliers_from_csv_file,
    OnMatchPatternSendDocumentMessageReplier,
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternPickAndSendTextMessageReplier,
    OnMatchPatternPickAndSendCorruptedTextMessageReplier,
)
from tests.mocks import MockMessage

MockBot = MagicMock(spec=Bot)
MockUpdate = MagicMock(spec=Update)
MagicMockMessage = MagicMock(spec=Message)


class ReplierSetupMixin(ABC):
    bot = None
    update = None

    def setUp(self):
        self.bot = MockBot()
        self.update = MockUpdate()


class OnMatchPatternSendTextMessageReplierTestCase(ReplierSetupMixin, TestCase):
    def test_it_matches_a_given_pattern(self):
        pattern = r"(foo)"
        expected_reply = "bar"
        replier = OnMatchPatternSendTextMessageReplier(
            pattern=pattern, message_content=expected_reply
        )
        message = MockMessage(text="A message matching pattern foo")

        self.assertTrue(replier.filter(message))

    def test_text_reply_is_sent_if_pattern_is_matched(self):
        pattern = r"(foo)"
        expected_reply_content = "bar"
        replier = OnMatchPatternSendTextMessageReplier(
            pattern=pattern, message_content=expected_reply_content
        )
        message = MockMessage(text="A message matching pattern foo")

        self.simulate_message_is_sent(message)

        reply = replier.reply(self.bot, self.update)

        self.assertEqual(reply.text, expected_reply_content)

    def test_it_does_not_reply_if_pattern_is_not_matched(self):
        pattern = r"(foo)"
        replier = OnMatchPatternSendTextMessageReplier(
            pattern=pattern, message_content="bar"
        )
        message = MockMessage(text="Message")

        self.assertFalse(replier.filter(message))

    def simulate_message_is_sent(self, message):
        self.update.message = message
        self.bot.send_message = MagicMock(
            side_effect=lambda **kwargs: MockMessage(text=kwargs.get("text"))
        )

    def test_can_be_converted_to_message_handler(self):
        replier = OnMatchPatternSendTextMessageReplier(
            pattern="foo", message_content="match!"
        )
        message_handler = replier.to_message_handler()

        self.assertTrue(isinstance(message_handler, MessageHandler))


class OnMatchPatternSendDocumentMessageReplierTestCase(ReplierSetupMixin, TestCase):
    def setUp(self):
        super(OnMatchPatternSendDocumentMessageReplierTestCase, self).setUp()

        self.document_url = "https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif"

    def test_it_matches_a_given_pattern(self):
        replier = OnMatchPatternSendDocumentMessageReplier(
            pattern=r"(foo)", message_content=self.document_url
        )
        message = MagicMockMessage()
        message.text = "foo"

        self.assertTrue(replier.filter(message))

    def test_document_reply_is_sent_if_pattern_is_matched(self):
        replier = OnMatchPatternSendDocumentMessageReplier(
            pattern=r"(foo)", message_content=self.document_url
        )
        message = MagicMockMessage()
        message.text = "foo"
        message.chat_id = 123
        self.update.message = message
        self.bot.send_document = MagicMock()

        replier.reply(bot=self.bot, update=self.update)

        self.bot.send_document.assert_called_with(
            chat_id=123, document=self.document_url
        )


class LoadRepliersFromCSVFileTestCase(TestCase):
    def test_it_can_load_text_repliers_from_csv_file(self):
        file = StringIO("(foo),text,match")
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternSendTextMessageReplier)

    def test_it_can_load_document_repliers_from_csv_file(self):
        file = StringIO(
            "(foo),document,https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif"
        )
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternSendDocumentMessageReplier)

    def test_it_can_load_document_list_replier_from_csv_file(self):
        file = StringIO(
            "(foo),random_document,https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif "
        )
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendDocumentMessageReplier)

    def test_it_can_load_text_list_replier_from_csv_file(self):
        file = StringIO("(foo),random_text, hello;hello")
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendTextMessageReplier)

    def test_it_can_load_corrupted_text_replier_from_csv_file(self):
        file = StringIO("(foo),corrupted_random_text, NANI?!")
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(
            replier, OnMatchPatternPickAndSendCorruptedTextMessageReplier
        )

    def test_it_will_load_secret_message_replier_from_csv_file(self):
        file = StringIO("(foo),another_type_does_not_exist, hello;hello")
        repliers = load_repliers_from_csv_file(file)

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(
            replier, OnMatchPatternPickAndSendCorruptedTextMessageReplier
        )
