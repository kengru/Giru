import logging
import os

import firebase_admin
from dotenv import load_dotenv

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from firebase_admin import db

from commands import Start, Caps, Julien, Spotify, PaDondeHoy, Ayuda, Cartelera, create_get_saved_messages_callback
from repliers import FilterMmg, FilterSaveReply, FilterSalut, FilterRecon, FilterWtf, FilterMentira, FilterFelicidades, \
    FirebaseReplyStorageProvider, InMemoryReplyStorageProvider, FileSystemReplyStorageProvider
from repliers import FilterVN1, FilterVN2, FilterVN3, FilterVN4, FilterVN5, FilterVN6, FilterVN7, FilterSK1
from repliers import respondM, sdm, salute, recon, sendWTF, sendMentira, sendHBD
from repliers import sendVN1, sendVN2, sendVN3, sendVN4, sendVN5, sendVN6, sendVN7, sendSK1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='487860520:AAEgLKKYShLi9iut4v0Zl5HLnrUf8sNF418')

load_dotenv()

storage_location = os.getenv('STORAGE_LOCATION')
# NOTE: Replies are being saved in new-line delimited JSON (.ndjson)
message_storage = FileSystemReplyStorageProvider(os.path.realpath(os.path.join('.', 'src/texts/replies.ndjson')))
if storage_location == 'in_memory':
    message_storage = InMemoryReplyStorageProvider()
elif storage_location == 'firebase':
    cert_file_path = os.path.realpath(os.getenv('FIREBASE_ACCOUNT_KEY_FILE_PATH'))
    firebase_admin.initialize_app(firebase_admin.credentials.Certificate(cert_file_path), {
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    })
    message_storage = FirebaseReplyStorageProvider(db.reference())

filter_mmg = FilterMmg()
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
    CommandHandler('ayuda', Ayuda)
]
for cmd in commandsl:
    dp.add_handler(cmd)

dp.add_handler(MessageHandler(filter_mmg, respondM))
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

dp.add_handler(MessageHandler(Filters.command, unknown))

# Initiate interactions.
updater.start_polling()
