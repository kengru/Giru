import json
import pickle
import random
import re
import time
from functools import partial

from firebase_admin.db import Reference
from pkg_resources import resource_stream
from telegram import Message, User
from telegram.ext import BaseFilter

from giru.data import replies, mmg, cposp
from giru.settings import SAVED_REPLIES_FILE_PATH, SCORES_FILE_PATH

giru_res = partial(resource_stream, 'giru')


class FilterMmg(BaseFilter):
    def filter(self, message):
        found = re.search("(mmg)|(mamague(b|v))", message.text, re.IGNORECASE)
        return found


def respondM(bot, update):
    """ Respond to a pattern in FilterMmg. """
    # bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(mmg))


def convert_reply_dict_to_message(reply_dict):
    reply_dict['from_user'] = User(**reply_dict['from'])  # NOTE: required by python telegram API
    reply_dict['reply_to_message'] = convert_reply_dict_to_message(
        reply_dict['reply_to_message']) if 'reply_to_message' in reply_dict else None
    return Message(**reply_dict)


class BaseReplyStorageProvider:
    def save(self, message):  # type: (Message) -> None
        raise NotImplementedError

    def get_all_replies(self):  # type: () -> List[Message]
        raise NotImplementedError


class InMemoryReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self):
        self.saved_replies = []

    def save(self, message):
        self.saved_replies.append(message)

    def get_all_replies(self):
        return self.saved_replies


class FileSystemReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, message):
        json_line = message.to_json() + '\n'

        with open(self.file_path, 'a+') as file:
            file.write(json_line)

    def get_all_replies(self):
        def convert_json_line_to_message(json_line):
            return convert_reply_dict_to_message(json.loads(json_line))

        try:
            file_handle = open(self.file_path)
        except FileNotFoundError:
            file_handle = open(self.file_path, 'a+')

        with file_handle as file:
            replies = list(map(convert_json_line_to_message, [line.rstrip('\n') for line in file]))

        return replies or []


class FirebaseReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, db_reference):  # type: (Reference) -> None
        self.db_reference = db_reference

    def save(self, message):
        timestamp = str(int(time.time()))

        self.db_reference \
            .child('replies') \
            .child(timestamp) \
            .set(message.to_dict())

    def get_all_replies(self):
        replies_dict = self.db_reference.child('replies').get() or {}
        return [convert_reply_dict_to_message(reply_dict) for (_, reply_dict) in replies_dict.items()]


class FilterSaveReply(BaseFilter):
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider or FileSystemReplyStorageProvider(file_path=SAVED_REPLIES_FILE_PATH)

    def filter(self, message):
        if message.reply_to_message and message.text == '-save':
            self.storage_provider.save(message.reply_to_message)


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
    elif 'la' in message:
        bot.sendMessage(chat_id=update.message.chat_id, text='Hermana, cuente todo')
    else:
        pass


class FilterCPOSP(BaseFilter):
    def filter(self, message):
        found = re.search("CERTIFIED PIECE OF SHIT PERSON", message.text, re.IGNORECASE)
        return found


def respondCPOSP(bot, update):
    """ Respond to a pattern in FilterCPOSP. """
    # bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(cposp))


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


# Replying to user.
class FilterReplyToGiru(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if reply and reply.from_user.is_bot:
            return True


def sendReplyToUser(bot, update):
    sel = random.choice(replies)
    bot.sendMessage(chat_id=update.message.chat_id, text=sel, reply_to_message=update.message)


# Voicenotes Repliers

class FilterVN1(BaseFilter):
    def filter(self, message):
        found = re.search("(y esa basura)|(y esa mielda)|(diablo arsenio)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN1(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/basura.ogg'))


class FilterVN2(BaseFilter):
    def filter(self, message):
        found = re.search("(carmate)|(calmate)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN2(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/carmate.ogg'))


class FilterVN3(BaseFilter):
    def filter(self, message):
        found = re.search("(ok felicidades)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN3(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/felicidades.ogg'))


class FilterVN4(BaseFilter):
    def filter(self, message):
        found = re.search("(haterz)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN4(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/llegaronloshaterz.ogg'))


class FilterVN5(BaseFilter):
    def filter(self, message):
        found = re.search("(okgracia)|(ok gracia)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN5(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/okgracias.ogg'))


class FilterVN6(BaseFilter):
    def filter(self, message):
        found = re.search("(todobie)|(todo bie)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN6(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/todobien.ogg'))


class FilterVN7(BaseFilter):
    def filter(self, message):
        found = re.search("(lave el carro)", message.text, re.IGNORECASE)
        if found:
            return True


def sendVN7(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=giru_res('res/audio/laveelcarro.ogg'))


# Stickers

class FilterSK1(BaseFilter):
    def filter(self, message):
        if ('menor' or 'menol') in message.text.lower():
            return True


def sendSK1(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Quien dijo menor? :D')
    bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADAQADFwADGp7vCBkeqa14LgcnAg')


# Scoring system

class FilterScores(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if reply and (message.text == '-1' or message.text == '+1') and message.from_user.id != reply.from_user.id:
            return True


def recordPoints(bot, update):
    scores = {}
    try:
        with open(SCORES_FILE_PATH, 'rb') as f:
            scores = pickle.load(f)
    except:
        with open(SCORES_FILE_PATH, 'wb') as f:
            pickle.dump(scores, f, pickle.HIGHEST_PROTOCOL)
    name = update.message.reply_to_message.from_user.first_name
    if name in scores.keys():
        if update.message.text == '+1':
            scores[name] += 1
        else:
            scores[name] -= 1
    else:
        if update.message.text == '+1':
            scores[name] = scores.get(name, 0) + 1
        else:
            scores[name] = scores.get(name, 0) - 1
    with open(SCORES_FILE_PATH, 'wb') as f:
        pickle.dump(scores, f, pickle.HIGHEST_PROTOCOL)
