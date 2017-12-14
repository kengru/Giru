import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from commands import Start, Caps, Saved, Julien, Spotify
from repliers import FilterMmg, FilterReply, FilterSalut, respondM, sdm, salute

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='487860520:AAEgLKKYShLi9iut4v0Zl5HLnrUf8sNF418')
filter_mmg = FilterMmg()
filter_reply = FilterReply()
filter_salut = FilterSalut()

dispatcher = updater.dispatcher

def unknown(bot, update):
    """ What to do when the command is not recognizable. """
    bot.sendMessage(chat_id=update.message.chat_id, text='No le llego mi loco.')

# Creating and adding handlers.
dispatcher.add_handler(CommandHandler('start', Start))
dispatcher.add_handler(CommandHandler('vociao', Caps, pass_args=True))
dispatcher.add_handler(CommandHandler('saved', Saved))
dispatcher.add_handler(CommandHandler('julien', Julien))
dispatcher.add_handler(CommandHandler('spotify', Spotify, pass_args=True))
dispatcher.add_handler(MessageHandler(filter_salut, salute))
dispatcher.add_handler(MessageHandler(filter_mmg, respondM))
dispatcher.add_handler(MessageHandler(filter_reply, sdm))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# Initiate interactions.
updater.start_polling()
