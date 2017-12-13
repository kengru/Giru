def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='KLK!!')

def Caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)