import json
import random
import re
import time
from functools import partial

import spotipy
from emoji import emojize
from pkg_resources import resource_stream
from spotipy.oauth2 import SpotifyClientCredentials
from telegram.ext import BaseFilter
from telegram.message import Message
from telegram.user import User

import giru.core.scorekeeping
from giru.core.repliers import (
    OnMatchPatternSendDocumentMessageReplier,
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternSendStickerReplier,
)
from giru.data import replies, mmg, cposp
from giru.settings import (
    SAVED_REPLIES_FILE_PATH,
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SCORES_FILE_PATH,
)

giru_res = partial(resource_stream, "giru")
client_credentials = None


def sdm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Mensaje guardado.")


class FilterMmg(BaseFilter):
    def filter(self, message):
        found = re.search("(mmg)|(mamague(b|v))", message.text, re.IGNORECASE)
        return found


def respond_mmg(bot, update):
    """ Respond to a pattern in FilterMmg. """
    # bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(mmg))


def convert_reply_dict_to_message(reply_dict):
    reply_dict["from_user"] = User(
        **reply_dict["from"]
    )  # NOTE: required by python telegram API
    reply_dict["reply_to_message"] = (
        convert_reply_dict_to_message(reply_dict["reply_to_message"])
        if "reply_to_message" in reply_dict
        else None
    )
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
        json_line = message.to_json() + "\n"

        with open(self.file_path, "a+") as file:
            file.write(json_line)

    def get_all_replies(self):
        def convert_json_line_to_message(json_line):
            return convert_reply_dict_to_message(json.loads(json_line))

        try:
            file_handle = open(self.file_path)
        except FileNotFoundError:
            file_handle = open(self.file_path, "a+")

        with file_handle as file:
            replies = list(
                map(convert_json_line_to_message, [line.rstrip("\n") for line in file])
            )

        return replies or []


class FilterSaveReply(BaseFilter):
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider or FileSystemReplyStorageProvider(
            file_path=SAVED_REPLIES_FILE_PATH
        )

    def filter(self, message):
        if message.reply_to_message and message.text == "-save":
            self.storage_provider.save(message.reply_to_message)


class FilterSalut(BaseFilter):
    def filter(self, message):
        found = re.search("(giru)", message.text, re.IGNORECASE)
        if found:
            return True


def salute(bot, update):
    message = update.message.text.lower()
    if "hola" in message or "holi" in message:
        bot.sendMessage(chat_id=update.message.chat_id, text="Hola!")
    elif "klk" in message:
        bot.sendMessage(chat_id=update.message.chat_id, text="Dime buen barrial.")
    elif "la" in message:
        bot.sendMessage(chat_id=update.message.chat_id, text="Hermana, cuente todo")
    else:
        pass


class FilterCPOSP(BaseFilter):
    def filter(self, message):
        if "certified piece of shit person" in message.text.lower():
            return True
        return False


def respond_certified(bot, update):
    """ Respond to a pattern in FilterCPOSP. """
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(cposp))


class FilterRecon(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if reply and reply.photo and message.text == "-recon":
            return True


def recon(bot, update):
    text = "*Reconocimiento empezado!*\nCargando respuesta....."
    bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="Markdown")
    time.sleep(3)
    text = (
        "He encontrado un *"
        + str(random.randint(60, 100))
        + "%* de que en la imagen hay un *mamaguebo*."
    )
    bot.sendMessage(
        chat_id=update.message.chat_id, text=text.format(), parse_mode="Markdown"
    )


class FilterWtf(BaseFilter):
    def filter(self, message):
        found = re.search("(wtf)|(what the fuck)|(dafuq)", message.text, re.IGNORECASE)
        if found:
            return True


def send_wtf(bot, update):
    bot.sendDocument(
        chat_id=update.message.chat_id,
        document="https://media.giphy.com/media/aZ3LDBs1ExsE8/giphy.gif",
    )


class FilterMentira(BaseFilter):
    def filter(self, message):
        found = re.search(
            "((^|\s)liar)|(jablador)|(mentiroso)|(mentira)|((^|\s)lies)",
            message.text,
            re.IGNORECASE,
        )
        if found:
            return True


def send_mentira(bot, update):
    bot.sendDocument(
        chat_id=update.message.chat_id,
        document="http://78.media.tumblr.com/tumblr_m3zgenZn7S1r3tlbto1_400.gif",
    )


class FilterFelicidades(BaseFilter):
    def filter(self, message):
        found = re.search(
            "(feliz cumpleaños)|(feliz cumpleanos)|(happy birthday)|(hbd)",
            message.text,
            re.IGNORECASE,
        )
        if found:
            return True


def send_hbd(bot, update):
    bot.sendDocument(
        chat_id=update.message.chat_id,
        document="https://media.giphy.com/media/xThtaqQYLPSIzd682A/giphy.gif",
    )


# Replying to user.
class FilterReplyToGiru(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if reply and reply.from_user.is_bot:
            return True


def send_reply_to_user(bot, update):
    sel = random.choice(replies)
    bot.sendMessage(
        chat_id=update.message.chat_id, text=sel, reply_to_message=update.message
    )


# Voicenotes Repliers
diablo_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(y esa basura)|(y esa mielda)|(diablo arsenio)", giru_res("res/audio/basura.ogg")
)

calmate_filter = OnMatchPatternSendDocumentMessageReplier(
    "(ca[lr]mate)", giru_res("res/audio/carmate.ogg")
)

felicidades_filter = OnMatchPatternSendDocumentMessageReplier(
    "(ok felicidades)", giru_res("res/audio/felicidades.ogg")
)

haters_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(haterz)", giru_res("res/audio/llegaronloshaterz.ogg")
)

ok_gracia_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(okgracia)|(ok gracia)", giru_res("res/audio/okgracias.ogg")
)

todo_bien_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(todobie)|(todo bie)", giru_res("res/audio/todobien.ogg")
)

lave_el_carro_filter = OnMatchPatternSendDocumentMessageReplier(
    r"(lave el carro)", giru_res("res/audio/laveelcarro.ogg")
)

# Stickers
menor_replier = OnMatchPatternSendStickerReplier(
    r"(meno[rl])", "CAADAQADFwADGp7vCBkeqa14LgcnAg", "Quien dijo menor? :D"
)


# Scoring system
class FilterScores(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if (
            reply
            and (message.text == "-1" or message.text == "+1")
            and message.from_user.id != reply.from_user.id
        ):
            return True


def record_points(bot, update):
    k = giru.core.scorekeeping.FsScoreKeeper(SCORES_FILE_PATH)

    name = update.message.reply_to_message.from_user.first_name
    chat_id = update.message.chat_id

    if update.message.text == "+1":
        k.add_point(chat_id, name)
    else:
        k.remove_point(chat_id, name)


alcohol_replier = OnMatchPatternPickAndSendDocumentMessageReplier(
    r"(booze|romo|beer|birra|alcohol)",
    [
        "https://media.giphy.com/media/Jp3sIkRR030uGYVGpX/giphy.gif",
        "https://media.giphy.com/media/cC9nMt8P3gsUVka1Ul/giphy.gif",
    ],
)

familia_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(familia|family)", giru_res("res/images/familia.jpg")
)


class SpotifyLinkFilter(BaseFilter):
    spotify_pattern = "r(open.spotify.com)"

    def filter(self, message):
        has_match = re.search(self.spotify_pattern, message.text, re.IGNORECASE)
        return has_match


def send_spotify_link_reply(bot, update):
    global client_credentials
    if client_credentials is None:
        client_credentials = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
        )

    start = update.message.text.find("https://open.spotify")
    query = update.message.text[start : start + 53]
    sp = spotipy.Spotify(client_credentials_manager=client_credentials)
    result = sp.track(track_id=query)
    if result["preview_url"]:
        audio = result["preview_url"]
        message = emojize("Here is a preview :notes:", use_aliases=True)
        bot.sendMessage(
            chat_id=update.message.chat_id, text=message, parse_mode="Markdown"
        )
        bot.sendAudio(chat_id=update.message.chat_id, audio=audio)
    else:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=emojize(":x:", use_aliases=True) + " No hay preview.",
            parse_mode="Markdown",
        )


droga_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(droga|drugs)", giru_res("res/images/droga.jpg")
)
