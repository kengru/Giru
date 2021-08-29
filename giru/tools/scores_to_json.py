import json
import pickle
from pathlib import Path

from giru.config import settings

SCORES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "scores.pkl"

JSON_SCORES_FILE_PATH = Path(settings.GIRU_DATA_PATH) / "scores.json"


def main():
    with open(SCORES_FILE_PATH, "rb") as f:
        _scores = pickle.load(f)

    json.dump(_scores, JSON_SCORES_FILE_PATH.open('w'))


if __name__ == '__main__':
    main()
