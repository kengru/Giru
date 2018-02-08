import re
import random
from telegram.ext import BaseFilter
from telegram import Message

saved = 'src/texts/saved.txt'

class FilterMmg(BaseFilter):
    def filter(self, message):
        found = re.search("(mmg)|(mamague(b|v))", message.text, re.IGNORECASE)
        return found

def respondM(bot, update):
    """ Respond to a pattern in FilterMmg. """
    # bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')
    # bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/basura.ogg', 'rb'))
    bot.sendDocument(chat_id=update.message.chat_id, document='http://a.memegen.com/zn4ros.gif')

class FilterReply(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if message.reply_to_message and message.text == '-save':
            with open(saved, 'a') as file:
                file.write('*' + reply.text + '* - [' + reply.from_user.first_name + '](tg://user?id=' \
                + str(reply.from_user.id) + ')\n')

def sdm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Mensaje guardado.')

class FilterSalut(BaseFilter):
    def filter(self, message):
        found = re.search("(giru)", message.text, re.IGNORECASE)
        if found:
            return True

def salute(bot, update):
    message = update.message.text.lower()
    if 'hola' in message or 'holi' in message:
        bot.sendMessage(chat_id=update.message.chat_id, text='Hola!')
    elif 'klk' in message:
        bot.sendMessage(chat_id=update.message.chat_id, text='Dime buen barrial.')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Dimelo.')

class FilterRecon(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if reply and reply.photo and message.text == '-recon':
            return True

def recon(bot, update):
    text = '*Reconocimiento empezado!*\nCargando respuesta.....'
    bot.sendMessage(chat_id=update.message.chat_id,text=text, parse_mode='Markdown')
    text = 'He encontrado un *' + str(random.randint(60,100)) + '%* de que en la imagen hay un *mamaguebo*.'
    bot.sendMessage(chat_id=update.message.chat_id,text=text.format(), parse_mode='Markdown')

class FilterWtf(BaseFilter):
    def filter(self, message):
        found = re.search("(wtf)|(what the fuck)|(dafuq)", message.text, re.IGNORECASE)
        if found:
            return True

def sendWTF(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='https://gph.is/1ppshye')

class FilterMentira(BaseFilter):
    def filter(self, message):
        found = re.search("(liar)|(jablador)|(mentiroso)|(mentira)|(lies)", message.text, re.IGNORECASE)
        if found:
            return True

def sendMentira(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='http://78.media.tumblr.com/tumblr_m3zgenZn7S1r3tlbto1_400.gif')

# Voicenotes Repliers

class FilterVN1(BaseFilter):
    def filter(self, message):
        found = re.search("(y esa basura)|(y esa mielda)|(diablo arsenio)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN1(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/basura.ogg', 'rb'))

class FilterVN2(BaseFilter):
    def filter(self, message):
        found = re.search("(carmate)|(calmate)|(ay)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN2(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/carmate.ogg', 'rb'))

class FilterVN3(BaseFilter):
    def filter(self, message):
        found = re.search("(ok felicidades)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN3(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/felicidades.ogg', 'rb'))

class FilterVN4(BaseFilter):
    def filter(self, message):
        found = re.search("(haterz)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN4(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/llegaronloshaterz.ogg', 'rb'))

class FilterVN5(BaseFilter):
    def filter(self, message):
        found = re.search("(okgracia)|(ok gracia)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN5(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/okgracias.ogg', 'rb'))

class FilterVN6(BaseFilter):
    def filter(self, message):
        found = re.search("(todobie)|(todo bie)",message.text, re.IGNORECASE)
        if found:
            return True

def sendVN6(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/todobien.ogg', 'rb'))

class FilterVN7(BaseFilter):
    def filter(self, message):
        found = re.search("(lave el carro)", message.text, re.IGNORECASE)
        if found:
            return True

def sendVN7(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('src/audio/laveelcarro.ogg', 'rb'))

# Stickers

#class FilterSck1(BaseFilter):


# class FilterPalomo(BaseFilter):
#     def filter(self, message):
#         reply = message.reply_to_message