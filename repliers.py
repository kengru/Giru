import random
import re
import os

from telegram.ext import BaseFilter

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


class BaseReplyStorageProvider:
    def save(self, message):
        raise NotImplementedError


class InMemoryReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self):
        self.saved_replies = []

    def save(self, message):
        self.saved_replies.append(message)


class FileSystemReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, file_path):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        default_file_path = os.path.realpath(os.path.join(dir_path, '..', 'src/texts/saved.txt'))

        self.file_path = file_path or default_file_path

    def save(self, message):
        text = message.reply_to_message.text
        user = message.reply_to_message.from_user
        serialized = '* {} * - [{}](tg://user?id={}\n'.format(text, user.first_name, user.id)

        with open(self.file_path, 'a') as file:
            file.write(serialized)


class FilterSaveReply(BaseFilter):
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider or InMemoryReplyStorageProvider()

    def filter(self, message):
        if message.reply_to_message and message.text == '-save':
            self.storage_provider.save(message)


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
    bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode='Markdown')
    text = 'He encontrado un *' + str(random.randint(60, 100)) + '%* de que en la imagen hay un *mamaguebo*.'
    bot.sendMessage(chat_id=update.message.chat_id, text=text.format(), parse_mode='Markdown')


class FilterWtf(BaseFilter):
    def filter(self, message):
        found = re.search("(wtf)|(what the fuck)|(dafuq)", message.text, re.IGNORECASE)
        if found:
            return True


def sendWTF(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='https://media.giphy.com/media/aZ3LDBs1ExsE8/giphy.gif')


class FilterMentira(BaseFilter):
    def filter(self, message):
        found = re.search("(liar)|(jablador)|(mentiroso)|(mentira)|(lies)", message.text, re.IGNORECASE)
        if found:
            return True


def sendMentira(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id,
                     document='http://78.media.tumblr.com/tumblr_m3zgenZn7S1r3tlbto1_400.gif')


class FilterFelicidades(BaseFilter):
    def filter(self, message):
        found = re.search("(feliz cumpleaños)|(feliz cumpleanos)|(happy birthday)|(hbd)", message.text, re.IGNORECASE)
        if found:
            return True


def sendHBD(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id,
                     document='https://media.giphy.com/media/xThtaqQYLPSIzd682A/giphy.gif')


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
        found = re.search("(carmate)|(calmate)", message.text, re.IGNORECASE)
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
        found = re.search("(todobie)|(todo bie)", message.text, re.IGNORECASE)
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

class FilterSK1(BaseFilter):
    def filter(self, message):
        if ('menor' or 'menol') in message.text.lower():
            return True


def sendSK1(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Quien dijo menor? :D')
    bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADAQADFwADGp7vCBkeqa14LgcnAg')

# class FilterPalomo(BaseFilter):
#     def filter(self, message):
#         reply = message.reply_to_message
