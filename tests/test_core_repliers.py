from abc import ABC
from unittest import TestCase
from unittest.mock import MagicMock

from telegram.bot import Bot
from telegram.ext import MessageHandler
from telegram.message import Message
from telegram.update import Update

from giru.core.repliers import (
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternPickAndSendTextMessageReplier,
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


class OnMatchPatternPickAndSendTextMessageReplierTestCase(ReplierSetupMixin, TestCase):
    def test_it_matches_a_given_pattern(self):
        pattern = r"(foo)"
        expected_reply = "bar"
        replier = OnMatchPatternPickAndSendTextMessageReplier(
            pattern=pattern, text_options=[expected_reply]
        )
        message = MockMessage(text="A message matching pattern foo")

        self.assertTrue(replier.filter(message))

    def test_text_reply_is_sent_if_pattern_is_matched(self):
        pattern = r"(foo)"
        expected_reply_content = "bar"
        replier = OnMatchPatternPickAndSendTextMessageReplier(
            pattern=pattern, text_options=[expected_reply_content]
        )
        message = MockMessage(text="A message matching pattern foo")

        self.simulate_message_is_sent(message)

        reply = replier.reply(self.bot, self.update)

        self.assertEqual(reply.text, expected_reply_content)

    def test_it_does_not_reply_if_pattern_is_not_matched(self):
        pattern = r"(foo)"
        replier = OnMatchPatternPickAndSendTextMessageReplier(
            pattern=pattern, text_options=["bar"]
        )
        message = MockMessage(text="Message")

        self.assertFalse(replier.filter(message))

    def simulate_message_is_sent(self, message):
        self.update.message = message
        self.bot.send_message = MagicMock(
            side_effect=lambda **kwargs: MockMessage(text=kwargs.get("text"))
        )

    def test_can_be_converted_to_message_handler(self):
        replier = OnMatchPatternPickAndSendTextMessageReplier(
            pattern="foo", text_options=["match!"]
        )
        message_handler = replier.to_message_handler()

        self.assertTrue(isinstance(message_handler, MessageHandler))


class OnMatchPatternPickAndSendDocumentMessageReplierTestCase(
    ReplierSetupMixin, TestCase
):
    def setUp(self):
        super(OnMatchPatternPickAndSendDocumentMessageReplierTestCase, self).setUp()

        self.document_url = "https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif"

    def test_it_matches_a_given_pattern(self):
        replier = OnMatchPatternPickAndSendDocumentMessageReplier(
            pattern=r"(foo)", document_options=[self.document_url]
        )
        message = MagicMockMessage()
        message.text = "foo"

        self.assertTrue(replier.filter(message))

    def test_document_reply_is_sent_if_pattern_is_matched(self):
        replier = OnMatchPatternPickAndSendDocumentMessageReplier(
            pattern=r"(foo)", document_options=[self.document_url]
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
