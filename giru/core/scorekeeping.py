import pickle
from abc import ABC, abstractmethod


def incr(x):
    return x + 1


def decr(x):
    return x - 1


class BaseScoreKeeper(ABC):
    @abstractmethod
    def add_point(self, chatid, userid):
        pass

    @abstractmethod
    def remove_point(self, chatid, userid):
        pass

    @abstractmethod
    def list_scores(self, chatid):
        pass


class FsScoreKeeper(BaseScoreKeeper):
    def __init__(self, score_keeping_file_path):
        self.path = score_keeping_file_path

    def change_points(self, name, op):
        scores = {}
        try:
            with open(self.path, "rb") as f:
                scores = pickle.load(f)
        except (IOError, EOFError):
            pass

        scores[name] = op(scores.get(name, 0))

        with open(self.path, "wb") as f:
            pickle.dump(scores, f, pickle.HIGHEST_PROTOCOL)

    def remove_point(self, chatid, userid):
        self.change_points(userid, decr)

    def add_point(self, chatid, userid):
        self.change_points(userid, incr)

    def list_scores(self, chatid):
        try:
            with open(self.path, "rb") as f:
                _scores = pickle.load(f)
            return _scores
        except (IOError, EOFError):
            return {}
