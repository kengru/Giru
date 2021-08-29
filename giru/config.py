from enum import Enum
from typing import Optional

from pydantic import BaseSettings, DirectoryPath, FilePath, HttpUrl


class StorageLocation(str, Enum):
    MEMORY = "in_memory"
    FIREBASE = "firebase"
    FILE_SYSTEM = "file_system"


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    OMDB_API_KEY: str
    GIRU_STORAGE_LOCATION: StorageLocation = StorageLocation.FILE_SYSTEM

    # for StorageLocation.FILE_SYSTEM
    GIRU_DATA_PATH: Optional[DirectoryPath] = "/data"

    # for StorageLocation.FIREBASE
    FIREBASE_ACCOUNT_KEY_FILE_PATH: Optional[FilePath]
    FIREBASE_DATABASE_URL: Optional[HttpUrl]

    class Config:
        env_file = ".env"


settings = Settings()
