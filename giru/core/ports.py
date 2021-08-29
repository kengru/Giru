from abc import ABC, abstractmethod
from typing import NoReturn

from telegram import Message, User


class BaseReplyStorageProvider:
    def save(self, message: Message) -> NoReturn:
        raise NotImplementedError

    def get_all_replies(self, chat_id: int) -> list[Message]:
        raise NotImplementedError


class BaseScoreKeeper(ABC):
    @abstractmethod
    def add_point(self, chatid: str, user: User) -> NoReturn:
        pass

    @abstractmethod
    def remove_point(self, chatid: str, user: User) -> NoReturn:
        pass

    @abstractmethod
    def list_scores(self, chatid: str) -> dict[str, int]:
        pass
