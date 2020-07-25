import logging
import os
from os.path import join

import firebase_admin
from firebase_admin import db
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

from giru.commands import Start, Caps, Julien, Spotify, PaDondeHoy, Ayuda, Cartelera, Scores, \
    create_get_saved_messages_callback, MePajeo
from giru.core.repliers import load_repliers_from_csv_file
from giru.repliers import *
from giru.settings import FIREBASE_ACCOUNT_KEY_FILE_PATH, FIREBASE_DATABASE_URL, GIRU_STORAGE_LOCATION
from giru.settings import TELEGRAM_TOKEN, GIRU_DATA_PATH, REPLIES_FILE_PATH

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=TELEGRAM_TOKEN)

# NOTE: Replies are being saved in new-line delimited JSON (.ndjson)
message_storage = FileSystemReplyStorageProvider(join(GIRU_DATA_PATH, 'replies.ndjson'))
if GIRU_STORAGE_LOCATION == 'in_memory':
    message_storage = InMemoryReplyStorageProvider()
elif GIRU_STORAGE_LOCATION == 'firebase':
    cert_file_path = os.path.realpath(FIREBASE_ACCOUNT_KEY_FILE_PATH)
    firebase_admin.initialize_app(firebase_admin.credentials.Certificate(cert_file_path), {
        'databaseURL': FIREBASE_DATABASE_URL,
    })
    message_storage = FirebaseReplyStorageProvider(db.reference())

dp = updater.dispatcher


def unknown(bot, update):
    """ What to do when the command is not recognizable. """
    bot.sendMessage(chat_id=update.message.chat_id, text='No le llego mi loco.')


# Creating and adding handlers.
commands = [
    CommandHandler('start', Start),
    CommandHandler('vociao', Caps, pass_args=True),
    CommandHandler('saved', create_get_saved_messages_callback(message_storage)),
    CommandHandler('julien', Julien),
    CommandHandler('mepajeo', MePajeo),
    CommandHandler('spotify', Spotify, pass_args=True),
    CommandHandler('padondehoy', PaDondeHoy),
    CommandHandler('cartelera', Cartelera),
    CommandHandler('scores', Scores),
    CommandHandler('ayuda', Ayuda)
]
for cmd in commands:
    dp.add_handler(cmd)

message_handlers = [
    MessageHandler(FilterMmg(), respond_mmg),
    MessageHandler(FilterCPOSP(), respond_certified),
    MessageHandler(FilterWtf(), send_wtf),
    MessageHandler(FilterMentira(), send_mentira),
    MessageHandler(FilterFelicidades(), send_hbd),
    MessageHandler(FilterSalut(), salute),
    MessageHandler(FilterSaveReply(message_storage), sdm),
    MessageHandler(FilterRecon(), recon),
    MessageHandler(FilterSK1(), send_sk1),
    MessageHandler(FilterVN1(), send_vn1),
    MessageHandler(FilterVN2(), send_vn2),
    MessageHandler(FilterVN3(), send_vn3),
    MessageHandler(FilterVN4(), send_vn4),
    MessageHandler(FilterVN5(), send_vn5),
    MessageHandler(FilterVN6(), send_vn6),
    MessageHandler(FilterVN7(), send_vn7),
    MessageHandler(FilterScores(), record_points),
    MessageHandler(FilterReplyToGiru(), send_reply_to_user),
    MessageHandler(AlcoholRelatedFilter(), send_alcohol_related_message_reply),
    MessageHandler(FamiliaFilter(), send_familia_message_reply),
    MessageHandler(DrogaFilter(), send_droga_message_reply)
]

for msg_h in message_handlers:
    dp.add_handler(msg_h)

try:
    with open(REPLIES_FILE_PATH, 'r') as replies_file:
        for r in load_repliers_from_csv_file(replies_file):
            dp.add_handler(r.to_message_handler())
except FileNotFoundError:
    logging.error(
        '[ERROR] replies file "{}" not found, file-based replies will not be triggered.'.format(REPLIES_FILE_PATH))
except ValueError:
    logging.error(
        '[ERROR] replies file "{}" cannot be processed, file-based replies will not be triggered.'.format(
            REPLIES_FILE_PATH))

dp.add_handler(MessageHandler(Filters.command, unknown))


def start():
    # Initiate interactions.
    logging.info('giru started')
    updater.start_polling()


if __name__ == "__main__":
    start()
