from telegram import User, Message


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
