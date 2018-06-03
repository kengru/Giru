from random import randint


class MockBot:
    last_message = {}

    def sendMessage(self, chat_id, text):
        self.last_message[chat_id] = text


# TODO: extend from Telegram's `Message` class
class MockMessage:
    def __init__(self, text='', reply_to_message=None, from_user=None):
        self.chat_id = randint(1,1000)
        self.text = text
        self.reply_to_message = reply_to_message
        self.from_user = from_user


class MockUpdate:
    message = MockMessage()


class MockUser:
    """
    NOTE: We're only mocking the fields required to make the test we have pass.
    You should add new fields if new tests require them.
    """
    def __init__(self, id, first_name):
        self.id = id or randint(1, 1000)
        self.first_name = first_name


"""
def PaDondeHoy(bot, update):
    day = datetime.date.today().weekday()

    @lru_cache()
    def cached_response(day_of_week, chat):
        with open('src/texts/days.pickle', 'rb') as f:
            days = pickle.load(f)
        return random.choice(days[day_of_week])

    response = cached_response(day, update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
    """
