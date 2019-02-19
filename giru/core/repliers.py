import re

from abc import ABC
from typing import TypeVar

from telegram import Message, Bot, Update
from telegram.ext.filters import BaseFilter, Filters

FilterType = TypeVar("FilterType", bound=BaseFilter)


class BaseReplier(BaseFilter, ABC):
    _filter = Filters.all

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        raise NotImplementedError

    def get_filter(self):  # type: () -> FilterType
        if not self._filter:
            raise ValueError("filter must be set")

        return self._filter

    def filter(self, message):
        return self.get_filter()(message)


class ReplyWithTextMessageMixin(ABC):
    text = None

    def reply(self, bot, update):  # type: (Bot, Update) -> Message
        message = update.message  # type: Message

        return bot.send_message(chat_id=message.chat_id, text=self.get_text())

    def get_text(self):
        if not self.text:
            raise ValueError("text must be set")

        return self.text


class MatchPatternInTextMessageMixin(ABC):
    pattern = None

    def filter(self, message):  # type: (Message) -> bool
        return bool(re.search(self.get_pattern(), message.text))

    def get_pattern(self):  # type: () -> str
        if not self.pattern:
            raise ValueError("pattern must be set")

        return self.pattern


class OnMatchPatternSendTextMessageReplier(MatchPatternInTextMessageMixin, ReplyWithTextMessageMixin, BaseReplier):
    def __init__(self, pattern, message_content):  # type: (re, str) -> None
        self.pattern = pattern
        self.text = message_content
