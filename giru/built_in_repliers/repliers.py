import random
import re
import time
from functools import partial

import spotipy
from emoji import emojize
from pkg_resources import resource_stream
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update
from telegram.ext import BaseFilter, MessageHandler

from giru.built_in_repliers.data import cposp, mmg, replies
from giru.config import settings
from giru.core.ports import BaseScoreKeeper
from giru.core.repliers import (
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternPickAndSendTextMessageReplier,
    OnMatchPatternSendAudioMessageReplier,
    OnMatchPatternSendPictureMessageReplier,
    OnMatchPatternSendStickerReplier,
)

giru_res = partial(resource_stream, "giru")
client_credentials = None


def save_dm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Mensaje guardado.")


class FilterSaveReply(BaseFilter):
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider

    def filter(self, message):
        if (
            message.text == "-save"
            and message.reply_to_message
            and message.reply_to_message.from_user.id != 487860520
        ):
            self.storage_provider.save(message.reply_to_message)


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


def record_points_factory(keeper: BaseScoreKeeper):
    def record_points(bot, update: Update):
        user = update.message.reply_to_message.from_user
        chat_id = update.message.chat_id

        if update.message.text == "+1":
            keeper.add_point(chat_id, user)
        else:
            keeper.remove_point(chat_id, user)

    return record_points


class SpotifyLinkFilter(BaseFilter):
    spotify_pattern = r"(open.spotify.com)"

    def filter(self, message):
        has_match = re.search(
            self.spotify_pattern, message.text, re.IGNORECASE | re.MULTILINE
        )
        return has_match


def send_spotify_link_reply(bot, update):
    global client_credentials
    if client_credentials is None:
        client_credentials = SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET,
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


mmg_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"(^|\s)(mmg)|(mamague(b|v))($|\s)", mmg, "mmg_replier"
)

salute_hola_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"(^|\s)(hol[ai]).*(giru)($|\s)", ["Hola!"], "salute_hola_replier"
)

salute_klk_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"(^|\s)(klk).*(giru)($|\s)", ["Dime buen barrial."], "salute_klk_replier"
)
salute_klk_post_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"(^|\s)(giru).*(klk)($|\s)", ["Dime buen barrial."], "salute_klk_post_replier"
)

salute_gay_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"(^|\s)la giru", ["Hermana, cuente todo"], "salute_gay_replier"
)

cposp_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"certified piece of shit person", cposp, "cposp_replier"
)

wtf_replier = OnMatchPatternPickAndSendDocumentMessageReplier(
    r"(^|\s)(wtf)|(what the fuck)|(dafuq)($|\s)",
    ["https://media.giphy.com/media/aZ3LDBs1ExsE8/giphy.gif"],
    "wtf_replier",
)

mentira_replier = OnMatchPatternPickAndSendDocumentMessageReplier(
    r"(^|\s)(liar)|(jablador)|(mentiroso)|(mentira)|(lies)($|\s)",
    ["http://78.media.tumblr.com/tumblr_m3zgenZn7S1r3tlbto1_400.gif"],
    "mentira_replier",
)

hbd_replier = OnMatchPatternPickAndSendDocumentMessageReplier(
    r"(^|\s)(feliz cumpleaños)|(feliz cumpleanos)|(happy birthday)|(hbd)($|\s)",
    ["https://media.giphy.com/media/xThtaqQYLPSIzd682A/giphy.gif"],
    "hbd_replier",
)

# Voicenotes Repliers
diablo_replier = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(y esa basura)|(y esa mielda)|(diablo arsenio)($|\s)", giru_res("res/audio/basura.ogg")
)

calmate_filter = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(ca[lr]mate)($|\s)", giru_res("res/audio/carmate.ogg")
)

felicidades_filter = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(ok felicidades)($|\s)", giru_res("res/audio/felicidades.ogg")
)

haters_replier = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(haterz)($|\s)", giru_res("res/audio/llegaronloshaterz.ogg")
)

ok_gracia_replier = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(okgracia)|(ok gracia)($|\s)", giru_res("res/audio/okgracias.ogg")
)

todo_bien_replier = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(todobie)|(todo bie)($|\s)", giru_res("res/audio/todobien.ogg")
)

lave_el_carro_filter = OnMatchPatternSendAudioMessageReplier(
    r"(^|\s)(lave el carro)($|\s)", giru_res("res/audio/laveelcarro.ogg")
)

# Stickers
menor_replier = OnMatchPatternSendStickerReplier(
    r"(^|\s)(meno[rl])($|\s)", "CAADAQADFwADGp7vCBkeqa14LgcnAg", "Quien dijo menor? :D"
)

alcohol_replier = OnMatchPatternPickAndSendDocumentMessageReplier(  # document?
    r"(^|\s)(booze|romo|beer|birra|alcohol)($|\s)",
    [
        "https://media.giphy.com/media/Jp3sIkRR030uGYVGpX/giphy.gif",
        "https://media.giphy.com/media/cC9nMt8P3gsUVka1Ul/giphy.gif",
    ],
    "alcohol_replier",
)

familia_replier = OnMatchPatternSendPictureMessageReplier(
    r"(^|\s)(familia|family)($|\s)", giru_res("res/images/familia.jpg")
)

droga_replier = OnMatchPatternSendPictureMessageReplier(
    r"(^|\s)(droga|drugs)($|\s)", giru_res("res/images/droga.jpg")
)

built_in_repliers = [
    mmg_replier.to_message_handler(),
    cposp_replier.to_message_handler(),
    wtf_replier.to_message_handler(),
    mentira_replier.to_message_handler(),
    hbd_replier.to_message_handler(),
    salute_gay_replier.to_message_handler(),
    salute_hola_replier.to_message_handler(),
    salute_klk_replier.to_message_handler(),
    salute_klk_post_replier.to_message_handler(),
    diablo_replier.to_message_handler(),
    calmate_filter.to_message_handler(),
    felicidades_filter.to_message_handler(),
    haters_replier.to_message_handler(),
    ok_gracia_replier.to_message_handler(),
    todo_bien_replier.to_message_handler(),
    menor_replier.to_message_handler(),
    alcohol_replier.to_message_handler(),
    familia_replier.to_message_handler(),
    droga_replier.to_message_handler(),
    MessageHandler(FilterRecon(), recon),
    MessageHandler(FilterReplyToGiru(), send_reply_to_user),
]
