from os import getenv, path

from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
env = load_dotenv(dotenv_path=dotenv_path, verbose=True)

SPOTIPY_CLIENT_ID = getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = getenv('SPOTIPY_CLIENT_SECRET')
OMDB_API_KEY = getenv('OMDB_API_KEY')
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

FIREBASE_ACCOUNT_KEY_FILE_PATH = getenv('FIREBASE_ACCOUNT_KEY_FILE_PATH')
FIREBASE_DATABASE_URL = getenv('FIREBASE_DATABASE_URL')
GIRU_STORAGE_LOCATION = getenv('GIRU_STORAGE_LOCATION')

GIRU_DATA_PATH = getenv('GIRU_DATA_PATH')

# derived from other settings
SAVED_REPLIES_FILE_PATH = path.realpath(path.join(GIRU_DATA_PATH, 'replies.ndjson'))
SCORES_FILE_PATH = path.realpath(path.join(GIRU_DATA_PATH, 'scores.pkl'))
REPLIES_FILE_PATH = path.realpath(path.join(GIRU_DATA_PATH, 'replies.csv'))
