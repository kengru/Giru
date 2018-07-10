import os
import time
from tempfile import NamedTemporaryFile
from unittest import TestCase

import firebase_admin
from firebase_admin import db

from repliers import FilterSaveReply, InMemoryReplyStorageProvider, FileSystemReplyStorageProvider, \
    FirebaseReplyStorageProvider
from settings import FIREBASE_ACCOUNT_KEY_FILE_PATH, FIREBASE_DATABASE_URL
from tests.mocks import MockMessage, MockUser


class TestFilterSaveReply(TestCase):

    def test_filter_save_reply_stores_replies_in_a_storage_provider(self):
        storage = InMemoryReplyStorageProvider()
        sut = FilterSaveReply(storage_provider=storage)
        message = _create_replied_message_mock("it works!")
        sut.filter(message)
        replies = storage.get_all_replies()

        self.assertGreater(len(replies), 0)
        self.assertTrue(replies[0].text == "it works!")

    def test_filter_save_reply_can_store_replies_in_filesystem(self):
        file = NamedTemporaryFile()
        storage = FileSystemReplyStorageProvider(file_path=file.name)
        sut = FilterSaveReply(storage_provider=storage)
        message = _create_replied_message_mock("it works!")
        sut.filter(message)
        replies = storage.get_all_replies()

        self.assertGreater(len(replies), 0)
        self.assertTrue(replies[0].text == "it works!")

    def test_filter_save_reply_can_store_replies_in_firebase_db(self):
        cert_file_path = os.path.realpath(FIREBASE_ACCOUNT_KEY_FILE_PATH)
        firebase_admin.initialize_app(firebase_admin.credentials.Certificate(cert_file_path), {
            'databaseURL': FIREBASE_DATABASE_URL,
        })
        test_ref_name = '/integration-tests/{}'.format(str(int(time.time())))
        storage = FirebaseReplyStorageProvider(db_reference=db.reference(test_ref_name))
        sut = FilterSaveReply(storage_provider=storage)
        message = _create_replied_message_mock("foobar")
        sut.filter(message)
        replies = storage.get_all_replies()

        self.assertGreater((len(replies)), 0)
        self.assertTrue(replies[0].text == "foobar")

        # NOTE: clean-up
        db.reference(test_ref_name).delete()


def _create_replied_message_mock(text):
    user_denisse = MockUser(id=0, first_name="Denisse")
    user_ken = MockUser(id=1, first_name="Ken")
    message = MockMessage(text=text, from_user=user_denisse)
    replied_message = MockMessage(reply_to_message=message, text="-save", from_user=user_ken)

    return replied_message
