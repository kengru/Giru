from telegram.ext import BaseFilter
from telegram import Message
import re

saved = 'src/saved.txt'

class FilterMmg(BaseFilter):
    def filter(self, message):
        found = re.search("(mmg)|(mamaguebo)", message.text, re.IGNORECASE)
        # print(message)
        return found

def respondM(bot, update):
    """ Respond to a pattern in FilterMmg. """
    bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')

class FilterReply(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if message.reply_to_message and message.text == '-save':
            print(message)
            with open(saved, 'a') as file:
                file.write(reply.text + ' - [' + reply.from_user.first_name + '](tg://user?id=' \
                + str(reply.from_user.id) + ')\n')

def sdm(bot, update):
    pass