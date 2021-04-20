import csv
import json
import pickle

from giru.core.data_based_repliers import create_replier
from giru.utils import convert_reply_dict_to_message
from giru.core.ports import BaseScoreKeeper, BaseReplyStorageProvider


def incr(x):
    return x + 1


def decr(x):
    return x - 1


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


def load_repliers_from_csv_file(file):  # type: (TextIO) -> List[BaseReplier]
    rows = csv.reader(file)
    repliers = []

    for pattern, replier_type_value, config in rows:
        if replier_type_value == "random_document":
            config = config.split(" ")
        elif replier_type_value in ("random_text", "corrupted_random_text"):
            config = config.split(";")
        repliers.append(create_replier(pattern, replier_type_value, config))

    return repliers
