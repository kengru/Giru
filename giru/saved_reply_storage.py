import json

from telegram import User, Message


class BaseReplyStorageProvider:
    def save(self, message):  # type: (Message) -> None
        raise NotImplementedError

    def get_all_replies(self):  # type: () -> List[Message]
        raise NotImplementedError


class InMemoryReplyStorageProvider(BaseReplyStorageProvider):
    def __init__(self):
        self.saved_replies = []

    def save(self, message):
        self.saved_replies.append(message)

    def get_all_replies(self):
        return self.saved_replies


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


def convert_reply_dict_to_message(reply_dict):
    reply_dict["from_user"] = User(
        **reply_dict["from"]
    )  # NOTE: required by python telegram API
    reply_dict["reply_to_message"] = (
        convert_reply_dict_to_message(reply_dict["reply_to_message"])
        if "reply_to_message" in reply_dict
        else None
    )
    return Message(**reply_dict)