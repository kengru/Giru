import logging
from typing import NoReturn

from firebase_admin.exceptions import NotFoundError
from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud.firestore_v1 import Client, Increment
from telegram import Message, User

from giru.built_in_repliers.data import BAD_CONFIG_SECRET_MESSAGE
from giru.core.model import ReplierConfiguration, ReplierType
from giru.core.ports import BaseReplyStorageProvider, BaseScoreKeeper
from giru.core.repliers import BaseReplier, create_replier, OnMatchPatternPickAndSendCorruptedTextMessageReplier


class FirebaseReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, db: Client):
        self.db = db

    def save(self, message: Message):
        if not message.text:
            return
        chat_doc = self.db.collection("chats").document(str(message.chat_id))
        chat_doc.set(message.chat.to_dict())

        chat_doc.collection('messages').document(str(message.message_id)).set(message.to_dict())

    def get_all_replies(self, chat_id: int):
        try:
            chat_doc = self.db.collection("chats").document(str(chat_id))
            replies = chat_doc.collection('messages').get()
        except NotFoundError:
            replies = []

        return [
            Message.de_json(item.to_dict(), None)
            for item in replies
        ]


class FirebaseScoreStorageProvider(BaseScoreKeeper):
    def __init__(self, db: Client):
        self.db = db

    def change_points(self, chat_id, user: User, value):
        chat_doc = self.db.collection("chats").document(str(chat_id))
        try:
            chat_doc.create({})
        except AlreadyExists:
            pass

        try:
            self.db.collection('users').document(str(user.id)).update(user.to_dict())
        except NotFound:
            self.db.collection('users').document(str(user.id)).set(user.to_dict())

        user_doc = self.db.collection('users').document(str(user.id))

        try:
            chat_doc.collection('scores').document(user.first_name).update(dict(score=Increment(value), user=user_doc))
        except NotFound:
            chat_doc.collection('scores').document(user.first_name).set(dict(score=value, user=user_doc))

    def add_point(self, chat_id: str, user: User) -> NoReturn:
        self.change_points(chat_id, user, 1)

    def remove_point(self, chat_id: str, user: User) -> NoReturn:
        self.change_points(chat_id, user, -1)

    def list_scores(self, chat_id: str) -> dict[str, int]:
        try:
            chat_doc = self.db.collection("chats").document(str(chat_id))
            scores = chat_doc.collection('scores').get()
        except NotFoundError:
            scores = []

        result = dict()
        for ref in scores:
            item = ref.to_dict()
            try:
                user = item['user'].get().to_dict()
                result[user['first_name']] = item['score']
            except KeyError:
                result[ref.id] = item['score']

        return result


def get_firebase_repliers(db: Client) -> list[BaseReplier]:
    for ref in db.collection("repliers").get():
        ref_dict = ref.to_dict()
        try:
            yield create_replier(**ref_dict)
        except Exception as exc:
            logging.exception('Could not load replier %s - %r', ref.id, ref_dict, exc_info=exc)