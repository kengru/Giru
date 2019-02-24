import logging
import os
from os.path import join

import firebase_admin
from firebase_admin import db
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

from giru.commands import Start, Caps, Julien, Spotify, PaDondeHoy, Ayuda, Cartelera, Scores, \
    create_get_saved_messages_callback
from giru.core.repliers import load_text_repliers_from_csv_file
from giru.repliers import *
from giru.repliers import FilterVN1, FilterVN2, FilterVN3, FilterVN4, FilterVN5, FilterVN6, FilterVN7, FilterSK1, FilterCPOSP
from giru.repliers import recordPoints, sendReplyToUser
from giru.repliers import respondM, respondCPOSP, sdm, salute, recon, sendWTF, sendMentira, sendHBD
from giru.repliers import sendVN1, sendVN2, sendVN3, sendVN4, sendVN5, sendVN6, sendVN7, sendSK1
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

filter_mmg = FilterMmg()
filter_cposp = FilterCPOSP()
filter_save_reply = FilterSaveReply(message_storage)
filter_salut = FilterSalut()
filter_recon = FilterRecon()
filter_wtf = FilterWtf()
filter_mentira = FilterMentira()
filter_felicidades = FilterFelicidades()

filter_vn1 = FilterVN1()
filter_vn2 = FilterVN2()
filter_vn3 = FilterVN3()
filter_vn4 = FilterVN4()
filter_vn5 = FilterVN5()
filter_vn6 = FilterVN6()
filter_vn7 = FilterVN7()

filter_sk1 = FilterSK1()

filter_score = FilterScores()
filter_reply_to_giru = FilterReplyToGiru()

dp = updater.dispatcher


def unknown(bot, update):
    """ What to do when the command is not recognizable. """
    bot.sendMessage(chat_id=update.message.chat_id, text='No le llego mi loco.')


# Creating and adding handlers.
commandsl = [
    CommandHandler('start', Start),
    CommandHandler('vociao', Caps, pass_args=True),
    CommandHandler('saved', create_get_saved_messages_callback(message_storage)),
    CommandHandler('julien', Julien),
    CommandHandler('spotify', Spotify, pass_args=True),
    CommandHandler('padondehoy', PaDondeHoy),
    CommandHandler('cartelera', Cartelera),
    CommandHandler('scores', Scores),
    CommandHandler('ayuda', Ayuda)
]
for cmd in commandsl:
    dp.add_handler(cmd)

dp.add_handler(MessageHandler(filter_mmg, respondM))
dp.add_handler(MessageHandler(filter_cposp, respondCPOSP))
dp.add_handler(MessageHandler(filter_wtf, sendWTF))
dp.add_handler(MessageHandler(filter_mentira, sendMentira))
dp.add_handler(MessageHandler(filter_sk1, sendSK1))
dp.add_handler(MessageHandler(filter_felicidades, sendHBD))
dp.add_handler(MessageHandler(filter_salut, salute))
dp.add_handler(MessageHandler(filter_save_reply, sdm))
dp.add_handler(MessageHandler(filter_recon, recon))

dp.add_handler(MessageHandler(filter_vn1, sendVN1))
dp.add_handler(MessageHandler(filter_vn2, sendVN2))
dp.add_handler(MessageHandler(filter_vn3, sendVN3))
dp.add_handler(MessageHandler(filter_vn4, sendVN4))
dp.add_handler(MessageHandler(filter_vn5, sendVN5))
dp.add_handler(MessageHandler(filter_vn6, sendVN6))
dp.add_handler(MessageHandler(filter_vn7, sendVN7))

dp.add_handler(MessageHandler(filter_score, recordPoints))
dp.add_handler(MessageHandler(filter_reply_to_giru, sendReplyToUser))
dp.add_handler(MessageHandler(AlcoholRelatedFilter(), send_alcohol_related_message_reply))

try:
    with open(REPLIES_FILE_PATH, 'r') as replies_file:
        for r in load_text_repliers_from_csv_file(replies_file):
            dp.add_handler(r.to_message_handler())
except FileNotFoundError:
    print(f'[ERROR] replies file "{REPLIES_FILE_PATH}" not found, file-based replies will not be triggered.')


dp.add_handler(MessageHandler(Filters.command, unknown))


def start():
    # Initiate interactions.
    logging.info('giru started')
    updater.start_polling()


if __name__ == "__main__":
    start()
