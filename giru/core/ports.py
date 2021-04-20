from abc import ABC, abstractmethod
from typing import List

from telegram import Message


class BaseReplyStorageProvider:
    def save(self, message):  # type: (Message) -> None
        raise NotImplementedError

    def get_all_replies(self):  # type: () -> List[Message]
        raise NotImplementedError


class BaseScoreKeeper(ABC):
    @abstractmethod
    def add_point(self, chatid, userid):
        pass

    @abstractmethod
    def remove_point(self, chatid, userid):
        pass

    @abstractmethod
    def list_scores(self, chatid):
        pass
