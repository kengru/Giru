import time

from giru.saved_reply_storage import BaseReplyStorageProvider, convert_reply_dict_to_message
from firebase_admin.db import Reference


class FirebaseReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, db_reference):  # type: (Reference) -> None
        self.db_reference = db_reference

    def save(self, message):
        timestamp = str(int(time.time()))

        self.db_reference.child("replies").child(timestamp).set(message.to_dict())

    def get_all_replies(self):
        replies_dict = self.db_reference.child("replies").get() or {}
        return [
            convert_reply_dict_to_message(reply_dict)
            for (_, reply_dict) in replies_dict.items()
        ]
