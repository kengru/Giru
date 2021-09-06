import logging
from pathlib import Path

from telegram.ext import CommandHandler, Dispatcher, MessageHandler

from giru.adapters.file_system import (
    FileSystemReplyStorageProvider,
    FsScoreKeeper,
    load_repliers_from_csv_file,
)
from giru.adapters.memory import InMemoryReplyStorageProvider, InMemoryScoreKeeper
from giru.built_in_repliers import data
from giru.built_in_repliers.repliers import (
    UNKNOWN_COMMAND_ERROR_HANDLER,
    FilterSaveReply,
    FilterScores,
    built_in_repliers,
    record_points_factory,
    save_dm,
)
from giru.config import StorageLocation, settings
from giru.core.commands import (
    built_in_commands,
    create_ayuda_cb,
    create_get_saved_messages_callback,
    score_command_factory,
)

SAVED_REPLIES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "replies.ndjson"
SCORES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "scores.json"
REPLIES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "replies.csv"

message_storage = InMemoryReplyStorageProvider()
score_keeper_storage = InMemoryScoreKeeper()
additional_repliers = []

if settings.GIRU_STORAGE_LOCATION == StorageLocation.FIREBASE:
    import firebase_admin.firestore
    from google.cloud.firestore_v1 import Client

    from giru.adapters.firebase import (
        FirebaseReplyStorageProvider,
        FirebaseScoreStorageProvider,
        auto_update_dispatcher_from_firebase_repliers,
        get_firebase_repliers,
    )

    cert_file_path = Path(settings.FIREBASE_ACCOUNT_KEY_FILE_PATH).absolute()
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(cert_file_path)
    )

    db: Client = firebase_admin.firestore.client()
    message_storage = FirebaseReplyStorageProvider(db)
    score_keeper_storage = FirebaseScoreStorageProvider(db)

    try:
        additional_repliers = list(get_firebase_repliers(db))
    except Exception as exc:
        logging.error(
            "replier config could not be read from firebase, replies will not be triggered.",
            exc_info=exc,
        )
else:
    # NOTE: Replies are being saved in new-line delimited JSON (.ndjson)
    message_storage = FileSystemReplyStorageProvider(SAVED_REPLIES_FILE_PATH)
    score_keeper_storage = FsScoreKeeper(SCORES_FILE_PATH)
    try:
        with open(REPLIES_FILE_PATH, "r") as replies_file:
            # read all entries and THEN add them to the dispatcher
            additional_repliers = [r for r in load_repliers_from_csv_file(replies_file)]
    except FileNotFoundError:
        logging.error(
            "replies file %r not found, file-based replies will not be triggered.",
            REPLIES_FILE_PATH,
        )
    except ValueError:
        logging.error(
            "replies file %r cannot be processed, file-based replies will not be triggered.",
            REPLIES_FILE_PATH,
        )


def configure_dispatcher(dp: Dispatcher):
    # Creating and adding handlers.
    commands = [
        *(c for c in built_in_commands),
        CommandHandler("saved", create_get_saved_messages_callback(message_storage)),
        CommandHandler("scores", score_command_factory(score_keeper_storage)),
    ]
    ayuda_cb = CommandHandler("ayuda", create_ayuda_cb(commands, data.ayuda))
    commands.append(ayuda_cb)

    for cmd in commands:
        dp.add_handler(cmd)

    message_handlers = [
        MessageHandler(FilterSaveReply(message_storage), save_dm),
        MessageHandler(FilterScores(), record_points_factory(score_keeper_storage)),
        *(m for m in built_in_repliers),
    ]

    for msg_h in message_handlers:
        dp.add_handler(msg_h)

    handlers = [r for r in additional_repliers]
    for r in handlers:
        dp.add_handler(r.to_message_handler())

    if settings.GIRU_STORAGE_LOCATION == StorageLocation.FIREBASE:
        auto_update_dispatcher_from_firebase_repliers(db, dp)

    dp.add_handler(UNKNOWN_COMMAND_ERROR_HANDLER)
