import pickle
import random
import spotipy
import datetime
from emoji import emojize
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import InputMediaPhoto

SPOTIPY_CLIENT_ID='0f9f9324ddd54895848e32fe5cea0d47'
SPOTIPY_CLIENT_SECRET='e6a9ce6a89ed4196a83e3fc65709ccc0'
client_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, \
     client_secret=SPOTIPY_CLIENT_SECRET)

def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='SOY GIRU MANIN!! Dale "/ayuda".')

def Caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps + '!')

def Saved(bot, update):
    message = ''
    with open('src/texts/saved.txt', 'r') as file:
        for line in file:
            message += line
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

def Julien(bot, update):
    with open('src/images/julien.pickle', 'rb') as f:
        julien = pickle.load(f)
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
            bot.sendMessage(chat_id=update.message.chat_id, \
            text=emojize(':x:', use_aliases=True) + ' No hay preview.', parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='No encuentro la cancion bi.', parse_mode='Markdown')

def PaDondeHoy(bot, update):
    day = datetime.date.today().weekday()
    with open('src/texts/days.pickle', 'rb') as f:
        days = pickle.load(f)
    print(days)
    bot.sendMessage(chat_id=update.message.chat_id, text=days[day])

def Ayuda(bot, update):
    with open('src/texts/commands.pickle', 'rb') as f:
        commands = pickle.load(f)
    message = 'Hola, soy Giru.\n\n*Comandos:* \n'
    for k in sorted(commands):
        message += '%s: ' % k
        for k2, i in commands[k].items():
            message += '%s\n\t- _Ejemplo: %s_\n' % (k2, i)
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')