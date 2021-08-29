import csv
import json
from typing import TextIO

from telegram import Message

from giru.core.ports import BaseReplyStorageProvider, BaseScoreKeeper
from giru.core.repliers import create_replier, BaseReplier


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
                scores = json.load(f)
        except (IOError, EOFError):
            pass

        scores[name] = op(scores.get(name, 0))

        with open(self.path, "wb") as f:
            json.dump(scores, f)

    def remove_point(self, chatid, userid):
        self.change_points(userid, decr)

    def add_point(self, chatid, userid):
        self.change_points(userid, incr)

    def list_scores(self, chatid):
        try:
            with open(self.path, "rb") as f:
                _scores = json.load(f)
            return _scores
        except (IOError, EOFError):
            return {}


class FileSystemReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, message: Message):
        json_line = message.to_json() + "\n"

        with open(self.file_path, "a+") as file:
            file.write(json_line)

    def get_all_replies(self, chat_id: int) -> list[Message]:
        try:
            file_handle = open(self.file_path)
        except FileNotFoundError:
            file_handle = open(self.file_path, "a+")

        with file_handle as file:
            replies = [Message.de_json(json.loads(line), None) for line in file]

        return replies or []


def load_repliers_from_csv_file(file: TextIO) -> list[BaseReplier]:
    rows = csv.reader(file)
    for pattern, replier_type_value, config in rows:
        if replier_type_value == "document":
            config = config.split(" ")
        elif replier_type_value in ("text", "corrupted_text"):
            config = config.split(";")
        yield create_replier(pattern, replier_type_value, config)
