import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, Filters, Updater
from commands import Start, Caps, Julien

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='487860520:AAEgLKKYShLi9iut4v0Zl5HLnrUf8sNF418')

dispatcher = updater.dispatcher

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='No le llego mi loco.')

echo_handler = MessageHandler(Filters.text, echo)
start_handler = CommandHandler('start', Start)
caps_handler = CommandHandler('vociao', Caps, pass_args=True)
julien_handler = CommandHandler('julien', Julien)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)
# dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
# dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(julien_handler)
dispatcher.add_handler(unknown_handler)
updater.start_polling()
