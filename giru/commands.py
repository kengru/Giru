import datetime
import pickle
import random
from functools import lru_cache, reduce
from typing import List

import spotipy
from emoji import emojize
from requests import get
from spotipy.oauth2 import SpotifyClientCredentials
from telegram.ext import CommandHandler
from telegram.message import Message
from telegram.parsemode import ParseMode
from telegram.bot import Bot

from giru.core.scorekeeping import FsScoreKeeper
from giru.data import julien, days, mepajeo
from giru import data
from giru.helpers.movies import Movie
from giru.settings import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SCORES_FILE_PATH

client_credentials = None

SAVED_MESSAGE_LIST_IS_EMPTY_MESSAGE = "No hay mensajes guardao' mi loki"


def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='SOY GIRU MANIN!! Dale "/ayuda".')


def Caps(bot, update, args):
    text = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text + '!')


def create_get_saved_messages_callback(storage_provider):
    def get_saved_messages_callback(bot, update):
        replies = storage_provider.get_all_replies()

        def format_saved_message(message):  # type: (Message) -> str
            return '*{}* - [{}](tg://user?id={})'.format(message.text, message.from_user.first_name,
                                                         message.from_user.id)

        formatted_replies = list(map(format_saved_message, replies))

        text = '\n'.join(formatted_replies) if formatted_replies else SAVED_MESSAGE_LIST_IS_EMPTY_MESSAGE

        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

    return get_saved_messages_callback


def Julien(bot, update):
    sel = random.choice(julien)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=sel)


def Spotify(bot, update, args):
    global client_credentials
    if client_credentials is None:
        client_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                      client_secret=SPOTIPY_CLIENT_SECRET)

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


def MePajeo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(mepajeo))


def create_ayuda_cb(commands: List[CommandHandler], help_text):
    def Ayuda(bot: Bot, update):
        """ Sends a list of the commands and their use. """
        message = 'Hola, soy Giru.\n\n*Comandos:* \n'

        for c in commands:
            message += f'/{c.command[0]}: '
            message += '\n'.join((f'{desc}\n\t- Ejemplo: _{example}_\n'
                                  for desc, example in help_text.get(c.command[0], {"??": "??"}).items()))

        chat_id = update.message.from_user.id or update.message.chat_id
        bot.sendMessage(chat_id=chat_id, text=message, parse_mode='Markdown')

    return Ayuda


def Cartelera(bot, update):
    """ Get's all the movies in theathers right now. """
    movies = get('http://api.cine.com.do/v1/movies').json()

    message = '*Manga ahí*\n\n'

    for m in movies:
        if m.get('published') and not m.get('comingsoon'):
            ratings = Movie(m.get('imdbId'), m.get('title')).emoji_ratings
            if ratings and len(ratings):
                ratings = reduce(lambda s, i: s + "  {}{}".format(*i),
                                 ratings.items(),
                                 "")
            else:
                ratings = ''

            message += '[{}]({}) *{}*\n'.format(m.get('title'),
                                                "http://www.cine.com.do/peliculas/" + m.get('slug'),
                                                ratings)

    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=True)


def Scores(bot, update):
    """ Gets a list with the points scored by person. """
    k = FsScoreKeeper(SCORES_FILE_PATH)
    _scores = k.list_scores(update.message.chat_id)
    if len(_scores) == 0:

        message = 'No hay scores.'
    else:
        message = '*Scores:*\n\n'
        sorted_scores = sorted(_scores.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_scores:
            message += '*{0}:*  {1}\n'.format(k, v)
        # If it ever wants to be divided.
        #
        # loved = tuple(filter(lambda x: x[1] > 0, sorted_scores))
        # hated = tuple(filter(lambda x: x[1] < 0, sorted_scores))
        # if loved:
        #     message += '*Loved:*\n'
        #     for k, v in loved:
        #         message += '{0}: {1}\n'.format(k, v)
        # message += '\n'
        # if hated:
        #     message += '*Hated:*\n'
        #     for k, v in hated:
        #         message += '{0}: {1}\n'.format(k, v)
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
