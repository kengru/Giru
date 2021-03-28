from unittest import TestCase

from tests.mocks import MockMessage, MockUser


class TestAlcoholRelatedFilter(TestCase):
    def test_drunk_reply_is_sent_if_filter_is_matched(self):
        from giru.repliers import AlcoholRelatedFilter

        matcher = AlcoholRelatedFilter()
        user = MockUser(first_name="Giru", is_bot=True)
        message_1 = MockMessage(text="denisse quiere romo", from_user=user)

        self.assertTrue(matcher.filter(message_1))

        message_2 = MockMessage(text="pero no hay cuarto", from_user=user)

        self.assertFalse(matcher.filter(message_2))

        message_3 = MockMessage(text="TRAIGANLE ROMO A DENISSE", from_user=user)

        self.assertTrue(matcher.filter(message_3))
