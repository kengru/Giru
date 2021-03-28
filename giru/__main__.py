import logging
import os
from os.path import join

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from zalgo_text.zalgo import zalgo

from giru import data
from giru.commands import (
    Start,
    Caps,
    Julien,
    Spotify,
    PaDondeHoy,
    Cartelera,
    Scores,
    create_get_saved_messages_callback,
    MePajeo,
    create_ayuda_cb,
)
from giru.core.repliers import load_repliers_from_csv_file
from giru.repliers import *
from giru.settings import (
    FIREBASE_ACCOUNT_KEY_FILE_PATH,
    FIREBASE_DATABASE_URL,
    GIRU_STORAGE_LOCATION,
)
from giru.settings import TELEGRAM_TOKEN, GIRU_DATA_PATH, REPLIES_FILE_PATH

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
updater = Updater(token=TELEGRAM_TOKEN)

# NOTE: Replies are being saved in new-line delimited JSON (.ndjson)
message_storage = FileSystemReplyStorageProvider(join(GIRU_DATA_PATH, "replies.ndjson"))
if GIRU_STORAGE_LOCATION == "in_memory":
    message_storage = InMemoryReplyStorageProvider()
elif GIRU_STORAGE_LOCATION == "firebase":
    import firebase_admin
    from firebase_replier import FirebaseReplyStorageProvider

    cert_file_path = os.path.realpath(FIREBASE_ACCOUNT_KEY_FILE_PATH)
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(cert_file_path),
        {
            "databaseURL": FIREBASE_DATABASE_URL,
        },
    )
    message_storage = FirebaseReplyStorageProvider(firebase_admin.db.reference())

dp = updater.dispatcher


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
    CommandHandler("scores", Scores),
]
ayuda_cb = CommandHandler("ayuda", create_ayuda_cb(commands, data.ayuda))
commands.append(ayuda_cb)

for cmd in commands:
    dp.add_handler(cmd)

message_handlers = [
    MessageHandler(FilterSaveReply(message_storage), sdm),
    MessageHandler(FilterScores(), record_points),
    MessageHandler(FilterRecon(), recon),
    MessageHandler(FilterReplyToGiru(), send_reply_to_user),
    mmg_replier.to_message_handler(),
    cposp_replier.to_message_handler(),
    wtf_replier.to_message_handler(),
    mentira_replier.to_message_handler(),
    hbd_replier.to_message_handler(),
    salute_gay_replier.to_message_handler(),
    salute_hola_replier.to_message_handler(),
    salute_klk_replier.to_message_handler(),
    salute_klk_post_replier.to_message_handler(),
    diablo_replier.to_message_handler(),
    calmate_filter.to_message_handler(),
    felicidades_filter.to_message_handler(),
    haters_replier.to_message_handler(),
    ok_gracia_replier.to_message_handler(),
    todo_bien_replier.to_message_handler(),
    menor_replier.to_message_handler(),
    alcohol_replier.to_message_handler(),
    familia_replier.to_message_handler(),
    droga_replier.to_message_handler(),
]

for msg_h in message_handlers:
    dp.add_handler(msg_h)

try:
    with open(REPLIES_FILE_PATH, "r") as replies_file:
        for r in load_repliers_from_csv_file(replies_file):
            dp.add_handler(r.to_message_handler())
except FileNotFoundError:
    logging.error(
        '[ERROR] replies file "{}" not found, file-based replies will not be triggered.'.format(
            REPLIES_FILE_PATH
        )
    )
except ValueError:
    logging.error(
        '[ERROR] replies file "{}" cannot be processed, file-based replies will not be triggered.'.format(
            REPLIES_FILE_PATH
        )
    )

dp.add_handler(MessageHandler(Filters.command, unknown))


def start():
    # Initiate interactions.
    logging.info("giru started")
    updater.start_polling()


if __name__ == "__main__":
    start()
