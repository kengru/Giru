import logging
import os

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from zalgo_text.zalgo import zalgo

from giru.core.commands import (
    Start,
    Caps,
    Julien,
    Spotify,
    PaDondeHoy,
    Cartelera,
    score_command_factory,
    create_get_saved_messages_callback,
    MePajeo,
    create_ayuda_cb,
)
from giru.core.repliers import *
from giru.adapters_memory import InMemoryReplyStorageProvider, InMemoryScoreKeeper
from giru.adapters_fs import (
    FileSystemReplyStorageProvider,
    FsScoreKeeper,
    load_repliers_from_csv_file,
)
from giru.settings import (
    FIREBASE_ACCOUNT_KEY_FILE_PATH,
    FIREBASE_DATABASE_URL,
    GIRU_STORAGE_LOCATION,
    SAVED_REPLIES_FILE_PATH,
    SCORES_FILE_PATH,
)
from giru.settings import TELEGRAM_TOKEN, REPLIES_FILE_PATH

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher

# NOTE: Replies are being saved in new-line delimited JSON (.ndjson)
message_storage = FileSystemReplyStorageProvider(SAVED_REPLIES_FILE_PATH)
score_keeper_storage = FsScoreKeeper(SCORES_FILE_PATH)
if GIRU_STORAGE_LOCATION == "in_memory":
    message_storage = InMemoryReplyStorageProvider()
    score_keeper_storage = InMemoryScoreKeeper()
elif GIRU_STORAGE_LOCATION == "firebase":
    import firebase_admin
    from giru.adapters_firebase import FirebaseReplyStorageProvider

    cert_file_path = os.path.realpath(FIREBASE_ACCOUNT_KEY_FILE_PATH)
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(cert_file_path),
        {
            "databaseURL": FIREBASE_DATABASE_URL,
        },
    )
    message_storage = FirebaseReplyStorageProvider(firebase_admin.db.reference())


def unknown(bot, update):
    """ What to do when the command is not recognizable. """
    t = zalgo().zalgofy(random.choice(data.BAD_CONFIG_SECRET_MESSAGE))
    bot.sendMessage(
        chat_id=update.message.chat_id, text=t, parse_mode=ParseMode.MARKDOWN
    )


# Creating and adding handlers.
commands = [
    CommandHandler("start", Start),
    CommandHandler("vociao", Caps, pass_args=True),
    CommandHandler("saved", create_get_saved_messages_callback(message_storage)),
    CommandHandler("julien", Julien),
    CommandHandler("mepajeo", MePajeo),
    CommandHandler("spotify", Spotify, pass_args=True),
    CommandHandler("padondehoy", PaDondeHoy),
    CommandHandler("cartelera", Cartelera),
    CommandHandler("scores", score_command_factory(score_keeper_storage)),
]
ayuda_cb = CommandHandler("ayuda", create_ayuda_cb(commands, data.ayuda))
commands.append(ayuda_cb)

for cmd in commands:
    dp.add_handler(cmd)

message_handlers = [
    MessageHandler(FilterSaveReply(message_storage), sdm),
    MessageHandler(FilterScores(), record_points_factory(score_keeper_storage)),
    MessageHandler(FilterRecon(), recon),
    MessageHandler(FilterReplyToGiru(), send_reply_to_user),
    *(m.to_message_handler() for m in built_in_repliers),
]

for msg_h in message_handlers:
    dp.add_handler(msg_h)

try:
    with open(REPLIES_FILE_PATH, "r") as replies_file:
        for r in load_repliers_from_csv_file(replies_file):
            dp.add_handler(r.to_message_handler())
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

dp.add_handler(MessageHandler(Filters.command, unknown))


def start():
    # Initiate interactions.
    logging.info("giru started")
    updater.start_polling()


if __name__ == "__main__":
    start()
