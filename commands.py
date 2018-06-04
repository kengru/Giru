import datetime
import os
import random
from functools import lru_cache
from firebase_admin import db
from dotenv import load_dotenv

import firebase_admin
import spotipy
from emoji import emojize
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Message, ParseMode

from data import julien, days, ayuda
from repliers import FirebaseReplyStorageProvider

SPOTIPY_CLIENT_ID = '0f9f9324ddd54895848e32fe5cea0d47'
SPOTIPY_CLIENT_SECRET = 'e6a9ce6a89ed4196a83e3fc65709ccc0'
client_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                              client_secret=SPOTIPY_CLIENT_SECRET)


def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='SOY GIRU MANIN!! Dale "/ayuda".')


def Caps(bot, update, args):
    text = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text + '!')


# TODO: please update this so it can be injected from caller (a higher order func, could work)
load_dotenv()
cert_file_path = os.path.realpath(os.getenv('FIREBASE_ACCOUNT_KEY_FILE_PATH'))
firebase_admin.initialize_app(firebase_admin.credentials.Certificate(cert_file_path), {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
})


def Saved(bot, update):
    storage = FirebaseReplyStorageProvider(db_reference=db.reference())
    replies = storage.get_all_replies()

    def format_saved_message(message):  # type: (Message) -> str
        return '*{}* - [{}](tg://user?id={})'.format(message.text, message.from_user.first_name, message.from_user.id)

    formatted_replies = list(map(format_saved_message, replies))

    text = '\n'.join(formatted_replies)

    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


def Julien(bot, update):
    sel = random.choice(julien)
    # cal = InputMediaPhoto(sel, 'Julien')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=sel)


def Spotify(bot, update, args):
    query = ' '.join(args).lower()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials)
    results = sp.search(q='' + query, type='track', limit=1)
    if results['tracks']['items']:
        artist = results['tracks']['items'][0]['artists'][0]['name']
        song = results['tracks']['items'][0]['name']
        audio = results['tracks']['items'][0]['preview_url']
        url = results['tracks']['items'][0]['external_urls']['spotify']
        message = emojize('*' + artist + '* - [' + song + '](' + url + ') ' + ':notes:', use_aliases=True)
        bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
        if audio:
            bot.sendAudio(chat_id=update.message.chat_id, audio=audio)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=emojize(':x:', use_aliases=True) + ' No hay preview.', parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='No encuentro la cancion bi.', parse_mode='Markdown')


@lru_cache()
def cached_padondehoy_response(date, chat):
    day_of_week = date.weekday()
    return random.choice(days[day_of_week])


def PaDondeHoy(bot, update):
    date = datetime.date.today()
    response = cached_padondehoy_response(date, update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)


def Ayuda(bot, update):
    message = 'Hola, soy Giru.\n\n*Comandos:* \n'
    for k in sorted(ayuda):
        message += '%s: ' % k
        for k2, i in ayuda[k].items():
            message += '%s\n\t- _Ejemplo: %s_\n' % (k2, i)
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
