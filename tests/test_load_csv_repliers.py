from io import StringIO
from unittest import TestCase

from giru.adapters.file_system import load_repliers_from_csv_file
from giru.core.repliers import (
    OnMatchPatternPickAndSendCorruptedTextMessageReplier,
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternPickAndSendTextMessageReplier,
)
from tests.mocks import MockMessage


class LoadRepliersFromCSVFileTestCase(TestCase):
    def test_it_can_load_text_repliers_from_csv_file(self):
        file = StringIO("(foo),text,match")
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendTextMessageReplier)

    def test_it_can_load_document_repliers_from_csv_file(self):
        file = StringIO(
            "(foo),document,https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif"
        )
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendDocumentMessageReplier)

    def test_it_can_load_document_list_replier_from_csv_file(self):
        file = StringIO(
            "(foo),document,https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif https://media.giphy.com/media/c6WtwzAXB1Aov1MejW/giphy.gif "
        )
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendDocumentMessageReplier)

    def test_it_can_load_text_list_replier_from_csv_file(self):
        file = StringIO("(foo),text, hello;hello")
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(replier, OnMatchPatternPickAndSendTextMessageReplier)

    def test_it_can_load_corrupted_text_replier_from_csv_file(self):
        file = StringIO("(foo),corrupted_text, NANI?!")
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(
            replier, OnMatchPatternPickAndSendCorruptedTextMessageReplier
        )

    def test_it_will_load_secret_message_replier_from_csv_file(self):
        file = StringIO("(foo),another_type_does_not_exist, hello;hello")
        repliers = list(load_repliers_from_csv_file(file))

        self.assertEqual(len(repliers), 1)

        replier = repliers[0]

        self.assertTrue(replier.filter(MockMessage(text="foo")))
        self.assertIsInstance(
            replier, OnMatchPatternPickAndSendCorruptedTextMessageReplier
        )
