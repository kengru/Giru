import logging
from pathlib import Path

import firebase_admin.firestore
import typer
from google.cloud.firestore_v1 import Client

from giru.config import settings
from giru.core.model import ReplierType

cert_file_path = Path(settings.FIREBASE_ACCOUNT_KEY_FILE_PATH).absolute()


def process_replier(
    db: Client, name: str, type: ReplierType, pattern: str, replies: list[str]
):
    db.collection("repliers").document(name).create(
        dict(type=type.value, pattern=pattern, data=replies)
    )


def main(
    name: str,
    replier_type: ReplierType,
    pattern: str,
    file: Path = typer.Argument(..., file_okay=True),
):
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(cert_file_path)
    )

    db: Client = firebase_admin.firestore.client()
    file_path = Path(file)
    replies = file_path.read_text("utf-8").splitlines()

    process_replier(db, name, replier_type, pattern, replies)


if __name__ == "__main__":
    logging.basicConfig()
    typer.run(main)
