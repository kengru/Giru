from giru.core.ports import BaseReplyStorageProvider, BaseScoreKeeper


class InMemoryReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self):
        self.saved_replies = []

    def save(self, message):
        self.saved_replies.append(message)

    def get_all_replies(self):
        return self.saved_replies


class InMemoryScoreKeeper(BaseScoreKeeper):
    def __init__(self):
        self.scores = dict()

    def remove_point(self, name, userid):
        self.scores[name] = self.scores.get(name, 0) - 1

    def add_point(self, name, userid):
        self.scores[name] = self.scores.get(name, 0) + 1

    def list_scores(self, chatid):
        return self.scores
