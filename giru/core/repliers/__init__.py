import random
import re
import time
from functools import partial

import spotipy
from emoji import emojize
from pkg_resources import resource_stream
from spotipy.oauth2 import SpotifyClientCredentials
from telegram.ext import BaseFilter

from giru.core.data_based_repliers import (
    OnMatchPatternSendDocumentMessageReplier,
    OnMatchPatternPickAndSendDocumentMessageReplier,
    OnMatchPatternSendStickerReplier,
    OnMatchPatternSendAudioMessageReplier,
    OnMatchPatternSendPictureMessageReplier,
    OnMatchPatternSendTextMessageReplier,
    OnMatchPatternPickAndSendTextMessageReplier,
)
from giru.core.ports import BaseScoreKeeper
from giru.core.repliers.data import replies, mmg, cposp
from giru.settings import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

giru_res = partial(resource_stream, "giru")
client_credentials = None


def sdm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Mensaje guardado.")


class FilterSaveReply(BaseFilter):
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider

    def filter(self, message):
        if message.reply_to_message and message.text == "-save":
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
    def record_points(bot, update):
        # keeper = giru.adapters_fs.FsScoreKeeper(SCORES_FILE_PATH)

        name = update.message.reply_to_message.from_user.first_name
        chat_id = update.message.chat_id

        if update.message.text == "+1":
            keeper.add_point(chat_id, name)
        else:
            keeper.remove_point(chat_id, name)

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


mmg_replier = OnMatchPatternPickAndSendTextMessageReplier(r"(mmg)|(mamague(b|v))", mmg)

salute_hola_replier = OnMatchPatternSendTextMessageReplier(
    r"(hol[ai]).*(giru)", "Hola!"
)

salute_klk_replier = OnMatchPatternSendTextMessageReplier(
    r"(klk).*(giru)", "Dime buen barrial."
)
salute_klk_post_replier = OnMatchPatternSendTextMessageReplier(
    r"(giru).*(klk)", "Dime buen barrial."
)

salute_gay_replier = OnMatchPatternSendTextMessageReplier(
    r"(^|\s)la giru", "Hermana, cuente todo"
)

cposp_replier = OnMatchPatternPickAndSendTextMessageReplier(
    r"certified piece of shit person", cposp
)

wtf_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(wtf)|(what the fuck)|(dafuq)",
    "https://media.giphy.com/media/aZ3LDBs1ExsE8/giphy.gif",
)

mentira_replier = OnMatchPatternSendDocumentMessageReplier(
    r"((^|\s)liar)|(jablador)|(mentiroso)|(mentira)|((^|\s)lies)",
    "http://78.media.tumblr.com/tumblr_m3zgenZn7S1r3tlbto1_400.gif",
)

hbd_replier = OnMatchPatternSendDocumentMessageReplier(
    r"(feliz cumpleaños)|(feliz cumpleanos)|(happy birthday)|(hbd)",
    "https://media.giphy.com/media/xThtaqQYLPSIzd682A/giphy.gif",
)

# Voicenotes Repliers
diablo_replier = OnMatchPatternSendAudioMessageReplier(
    r"(y esa basura)|(y esa mielda)|(diablo arsenio)", giru_res("res/audio/basura.ogg")
)

calmate_filter = OnMatchPatternSendAudioMessageReplier(
    r"(ca[lr]mate)", giru_res("res/audio/carmate.ogg")
)

felicidades_filter = OnMatchPatternSendAudioMessageReplier(
    r"(ok felicidades)", giru_res("res/audio/felicidades.ogg")
)

haters_replier = OnMatchPatternSendAudioMessageReplier(
    r"(haterz)", giru_res("res/audio/llegaronloshaterz.ogg")
)

ok_gracia_replier = OnMatchPatternSendAudioMessageReplier(
    r"(okgracia)|(ok gracia)", giru_res("res/audio/okgracias.ogg")
)

todo_bien_replier = OnMatchPatternSendAudioMessageReplier(
    r"(todobie)|(todo bie)", giru_res("res/audio/todobien.ogg")
)

lave_el_carro_filter = OnMatchPatternSendAudioMessageReplier(
    r"(lave el carro)", giru_res("res/audio/laveelcarro.ogg")
)

# Stickers
menor_replier = OnMatchPatternSendStickerReplier(
    r"(meno[rl])", "CAADAQADFwADGp7vCBkeqa14LgcnAg", "Quien dijo menor? :D"
)

alcohol_replier = OnMatchPatternPickAndSendDocumentMessageReplier(  # document?
    r"(booze|romo|beer|birra|alcohol)",
    [
        "https://media.giphy.com/media/Jp3sIkRR030uGYVGpX/giphy.gif",
        "https://media.giphy.com/media/cC9nMt8P3gsUVka1Ul/giphy.gif",
    ],
)

familia_replier = OnMatchPatternSendPictureMessageReplier(
    r"(familia|family)", giru_res("res/images/familia.jpg")
)

droga_replier = OnMatchPatternSendPictureMessageReplier(
    r"(droga|drugs)", giru_res("res/images/droga.jpg")
)

built_in_repliers = [
    mmg_replier,
    cposp_replier,
    wtf_replier,
    mentira_replier,
    hbd_replier,
    salute_gay_replier,
    salute_hola_replier,
    salute_klk_replier,
    salute_klk_post_replier,
    diablo_replier,
    calmate_filter,
    felicidades_filter,
    haters_replier,
    ok_gracia_replier,
    todo_bien_replier,
    menor_replier,
    alcohol_replier,
    familia_replier,
    droga_replier,
]
