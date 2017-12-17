import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from commands import Start, Caps, Saved, Julien, Spotify, PaDondeHoy, Ayuda
from repliers import FilterMmg, FilterReply, FilterSalut, FilterRecon, respondM, sdm, salute, recon

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='487860520:AAEgLKKYShLi9iut4v0Zl5HLnrUf8sNF418')
filter_mmg = FilterMmg()
filter_reply = FilterReply()
filter_salut = FilterSalut()
filter_recon = FilterRecon()

dp = updater.dispatcher

def unknown(bot, update):
    """ What to do when the command is not recognizable. """
    bot.sendMessage(chat_id=update.message.chat_id, text='No le llego mi loco.')

# Creating and adding handlers.
commandsl = [
    CommandHandler('start', Start),
    CommandHandler('vociao', Caps, pass_args=True),
    CommandHandler('saved', Saved),
    CommandHandler('julien', Julien),
    CommandHandler('spotify', Spotify, pass_args=True),
    CommandHandler('padondehoy', PaDondeHoy),
    CommandHandler('ayuda', Ayuda)
] 
for cmd in commandsl:
    dp.add_handler(cmd)

dp.add_handler(MessageHandler(filter_mmg, respondM))
dp.add_handler(MessageHandler(filter_salut, salute))
dp.add_handler(MessageHandler(filter_reply, sdm))
dp.add_handler(MessageHandler(filter_recon, recon))
dp.add_handler(MessageHandler(Filters.command, unknown))

# Initiate interactions.
updater.start_polling()
