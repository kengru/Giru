import pickle
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import InputMediaPhoto

SPOTIPY_CLIENT_ID='0f9f9324ddd54895848e32fe5cea0d47'
SPOTIPY_CLIENT_SECRET='e6a9ce6a89ed4196a83e3fc65709ccc0'
client_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, \
     client_secret=SPOTIPY_CLIENT_SECRET)

def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='KLK!!')

def Caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

def Saved(bot, update):
    message = ''
    with open('src/saved.txt', 'r') as file:
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
    results = sp.search(q='' + query, type='artist',limit=1)
    link = results['artists']['items'][0]['external_urls']['spotify']
    bot.sendMessage(chat_id=update.message.chat_id, text=link)