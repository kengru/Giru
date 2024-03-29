import datetime
from random import randint

from telegram.chat import Chat
from telegram.message import Message
from telegram.user import User


class MockBot:
    last_message = {}

    def send_message(self, chat_id, text, **kwargs):
        self.last_message[chat_id] = text

    def sendMessage(self, *args, **kwargs):
        self.send_message(*args, **kwargs)

    def send_photo(self, chat_id, photo, *args, **kwargs):
        self.last_message[chat_id] = photo

    def sendPhoto(self, *args, **kwargs):
        self.send_photo(*args, **kwargs)


class MockChat(Chat):
    def __init__(self, id=None, type=Chat.PRIVATE):
        _id = id

        if not _id:
            _id = randint(1, 1000)

        super().__init__(id=_id, type=type)


class MockUser(User):
    def __init__(self, id=None, first_name=None, is_bot=False):
        super().__init__(
            id=id or randint(1, 1000),
            first_name=first_name or "MockUser",
            is_bot=is_bot or False,
        )


class MockMessage(Message):
    def __init__(
        self,
        text="",
        reply_to_message=None,
        from_user=None,
        chat=None,
        date=datetime.datetime.now(),
    ):
        message_id = randint(1, 1000)
        chat = chat or MockChat()
        from_user = from_user or MockUser()

        super().__init__(
            message_id=message_id,
            from_user=from_user,
            date=date,
            chat=chat,
            text=text,
            reply_to_message=reply_to_message,
        )


class MockUpdate:
    message = None

    def __init__(self, message=MockMessage()):
        self.message = message


"""
def PaDondeHoy(bot, update):
    day = datetime.date.today().weekday()

    @lru_cache()
    def cached_response(day_of_week, chat):
        with open('res/texts/days.pickle', 'rb') as f:
            days = pickle.load(f)
        return random.choice(days[day_of_week])

    response = cached_response(day, update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
    """
