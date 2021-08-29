from os import path
from tempfile import TemporaryDirectory
from unittest import TestCase

from tests.mocks import MockMessage, MockUser


class TestFilterSaveReply(TestCase):
    def test_filter_save_reply_stores_replies_in_a_storage_provider(self):
        from giru.adapters.memory import InMemoryReplyStorageProvider
        from giru.built_in_repliers.repliers import FilterSaveReply

        storage = InMemoryReplyStorageProvider()
        sut = FilterSaveReply(storage_provider=storage)
        message = _create_replied_message_mock("it works!")
        sut.filter(message)
        replies = storage.get_all_replies()

        self.assertGreater(len(replies), 0)
        self.assertTrue(replies[0].text == "it works!")

    def test_filter_save_reply_can_store_replies_in_filesystem(self):
        from giru.adapters.file_system import FileSystemReplyStorageProvider
        from giru.built_in_repliers.repliers import FilterSaveReply

        with TemporaryDirectory() as dir_name:
            storage = FileSystemReplyStorageProvider(
                file_path=path.join(dir_name, "tempfile")
            )
            sut = FilterSaveReply(storage_provider=storage)
            message = _create_replied_message_mock("it works!")
            sut.filter(message)
            replies = storage.get_all_replies(0)

            self.assertGreater(len(replies), 0)
            self.assertTrue(replies[0].text == "it works!")
            self.assertIsNotNone(dir_name)


def _create_replied_message_mock(text):
    user_denisse = MockUser(id=0, first_name="Denisse")
    user_ken = MockUser(id=1, first_name="Ken")
    message = MockMessage(text=text, from_user=user_denisse)
    replied_message = MockMessage(
        reply_to_message=message, text="-save", from_user=user_ken
    )

    return replied_message
