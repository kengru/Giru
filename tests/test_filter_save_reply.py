from unittest import TestCase

from .mocks import MockMessage, MockUser

from repliers import FilterSaveReply, InMemoryReplyStorageProvider


class TestFilterSaveReply(TestCase):
    def test_filter_save_reply_stores_replies_in_a_cloud_storage(self):
        in_memory_storage_provider = InMemoryReplyStorageProvider()

        sut = FilterSaveReply(storage_provider=in_memory_storage_provider)

        message = _create_replied_message_mock("it works!")

        sut.filter(message)

        self.assertTrue(len(in_memory_storage_provider.saved_replies) > 0)
        self.assertTrue(in_memory_storage_provider.saved_replies[0].reply_to_message.text == "it works!")


def _create_replied_message_mock(text):
    user_denisse = MockUser(id=0, first_name="Denisse")
    user_ken = MockUser(id=1, first_name="Ken")
    message = MockMessage(text=text, from_user=user_denisse)
    replied_message = MockMessage(reply_to_message=message, text="-save", from_user=user_ken)

    return replied_message

