import logging
import re
from abc import ABC
from random import choice
from typing import List, TypeVar

from telegram import Bot, Message, Update
from telegram.ext import MessageHandler
from telegram.ext.filters import BaseFilter
from zalgo_text.zalgo import zalgo

from giru.built_in_repliers.data import BAD_CONFIG_SECRET_MESSAGE
from giru.core.model import ReplierType

FilterType = TypeVar("FilterType", bound=BaseFilter)


class BaseReplier(BaseFilter, ABC):
    _filter = None

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        raise NotImplementedError

    def get_filter(self):  # type: () -> FilterType
        if not self._filter:
            raise ValueError("filter must be set")

        return self._filter

    def filter(self, message):  # type: (Message) -> bool
        return self.get_filter()(message)

    def to_message_handler(self):  # type: () -> MessageHandler
        handler = MessageHandler(self, self.reply)
        setattr(handler, "name", getattr(self, "name", ""))
        return handler


class ReplyWithTextMessageMixin(ABC):
    text = None

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        return bot.send_message(
            chat_id=message.chat_id, text=self.get_text(), parse_mode="markdown"
        )

    def get_text(self):
        if not self.text:
            raise ValueError("text must be set")

        return self.text


class MatchPatternInTextMessageMixin(ABC):
    pattern = None

    def filter(self, message):  # type: (Message) -> bool
        return bool(
            re.search(self.get_pattern(), message.text, re.MULTILINE | re.IGNORECASE)
        )

    def get_pattern(self):  # type: () -> str
        if not self.pattern:
            raise ValueError("pattern must be set")

        return self.pattern


class OnMatchPatternPickAndSendTextMessageReplier(
    MatchPatternInTextMessageMixin, ReplyWithTextMessageMixin, BaseReplier
):
    def __init__(self, pattern, text_options, name: str):
        self.name = name
        self.pattern = pattern
        self.text_options = text_options

    @property
    def text(self):
        return choice(self.text_options)


class ReplyWithDocumentMessageMixin(ABC):
    document = None

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        return bot.send_document(chat_id=message.chat_id, document=self.get_document())

    def get_document(self):
        if not self.document:
            raise ValueError("document must be set")

        return self.document


class ReplyWithAudioMessageMixin(ReplyWithDocumentMessageMixin):
    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        return bot.send_audio(chat_id=message.chat_id, audio=self.get_document())


class ReplyWithPictureMessageMixin(ReplyWithDocumentMessageMixin):
    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        return bot.send_photo(chat_id=message.chat_id, photo=self.get_document())


class ReplyWithStickerMixin(ABC):
    sticker_id = None
    message_text = None

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        if self.message_text:
            bot.send_message(chat_id=message.chat_id, text=self.get_message_text())
        return bot.send_sticker(chat_id=message.chat_id, sticker=self.get_sticker())

    def get_sticker(self):
        if not self.sticker_id:
            raise ValueError("document must be set")

        return self.sticker_id

    def get_message_text(self):
        if not self.message_text:
            raise ValueError("document must be set")

        return self.message_text


class OnMatchPatternSendAudioMessageReplier(
    MatchPatternInTextMessageMixin, ReplyWithAudioMessageMixin, BaseReplier
):
    def __init__(self, pattern, message_content):
        self.pattern = pattern
        self.document = message_content


class OnMatchPatternSendPictureMessageReplier(
    MatchPatternInTextMessageMixin, ReplyWithPictureMessageMixin, BaseReplier
):
    def __init__(self, pattern, message_content):
        self.pattern = pattern
        self.document = message_content


class OnMatchPatternSendStickerReplier(
    MatchPatternInTextMessageMixin, ReplyWithStickerMixin, BaseReplier
):
    def __init__(self, pattern, sticker_id, message_text):
        self.pattern = pattern
        self.sticker_id = sticker_id
        self.message_text = message_text


class OnMatchPatternPickAndSendDocumentMessageReplier(
    MatchPatternInTextMessageMixin, ReplyWithDocumentMessageMixin, BaseReplier
):
    def __init__(self, pattern, document_options: List[str], name: str):
        self.name = name
        self.pattern = pattern
        self.document_options = document_options

    @property
    def document(self):
        return choice(self.document_options)


class OnMatchPatternPickAndSendCorruptedTextMessageReplier(
    OnMatchPatternPickAndSendTextMessageReplier
):
    @property
    def text(self):
        return zalgo().zalgofy(choice(self.text_options))


def create_replier(pattern: str, type: ReplierType, data: list[str], name: str):
    if type == ReplierType.random_document_from_list:
        return OnMatchPatternPickAndSendDocumentMessageReplier(pattern, data, name)
    elif type == ReplierType.random_text_from_list:
        return OnMatchPatternPickAndSendTextMessageReplier(pattern, data, name)
    elif type == ReplierType.random_corrupted_text_from_list:
        return OnMatchPatternPickAndSendCorruptedTextMessageReplier(pattern, data, name)
    else:
        logging.error("Could not load replier %r", locals())
        return OnMatchPatternPickAndSendCorruptedTextMessageReplier(
            pattern, BAD_CONFIG_SECRET_MESSAGE, name
        )
