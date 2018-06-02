from random import randint


class MockBot:
    last_message = {}

    def sendMessage(self, chat_id, text):
        self.last_message[chat_id] = text


class MockMessage:
    def __init__(self):
        self.chat_id = randint(1,1000)


class MockUpdate:
    message = MockMessage()


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
