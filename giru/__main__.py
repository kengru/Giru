import logging

from telegram import Bot
from telegram.ext import Updater

from giru.config import settings
from giru.configure_disptcher import configure_dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start():
    # Initiate interactions.
    logging.info("starting giru")
    bot = Bot(settings.TELEGRAM_TOKEN)
    updater = Updater(bot=bot)
    configure_dispatcher(updater.dispatcher)

    logging.info("giru started")
    updater.start_polling()


if __name__ == "__main__":
    start()
