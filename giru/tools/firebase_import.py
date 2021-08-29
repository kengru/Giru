import json
import logging
from pathlib import Path

import firebase_admin.firestore
from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud.firestore_v1 import Client
from telegram import Message

from giru.config import settings

cert_file_path = Path(settings.FIREBASE_ACCOUNT_KEY_FILE_PATH).absolute()

SAVED_REPLIES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "replies.ndjson"
SCORES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "scores.json"


def process_message(db: Client, message: Message):
    if not message.text:
        return
    chat_doc = db.collection("chats").document(str(message.chat_id))
    chat_doc.set(message.chat.to_dict())

    chat_doc.collection('messages').document(str(message.message_id)).set(message.to_dict())

    user = message.from_user
    try:
        db.collection('users').document(str(user.id)).create(user.to_dict())
    except AlreadyExists:
        logging.info('%s already existed', user.first_name)



def process_scores(db, first_name, score):
    chat_doc = db.collection("chats").document("-1001254163442")
    try:
        chat_doc.create({})
    except AlreadyExists:
        pass

    try:
        chat_doc.collection('scores').document(first_name).create(dict(score=score))
    except AlreadyExists:
        logging.warning('%s already had a score here', first_name)


def main():
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(cert_file_path)
    )

    db: Client = firebase_admin.firestore.client()
    for line in SAVED_REPLIES_FILE_PATH.read_text().splitlines():
        message = Message.de_json(json.loads(line), None)
        process_message(db, message)

    scores = json.load(SCORES_FILE_PATH.open('r'))
    for first_name, score in scores.items():
        process_scores(db, first_name, score)

if __name__ == '__main__':
    logging.basicConfig()
    main()
