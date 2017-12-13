import pickle
import random
from telegram import InputMediaPhoto

def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='KLK!!')

def Caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

def Julien(bot, update):
    with open('src/images/julien.pickle', 'rb') as f:
        julien = pickle.load(f)
    sel = random.choice(julien)
    # cal = InputMediaPhoto(sel, 'Julien')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=sel)
      