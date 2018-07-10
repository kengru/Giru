from functools import reduce
from re import findall
from typing import Dict

from omdb import OMDBClient

from secrets import OMDB_API_KEY

omdb = OMDBClient(apikey=OMDB_API_KEY)

RATING_EMOJI = {'Rotten Tomatoes': '🍅',
                'Internet Movie Database': '🍿',
                'Metacritic': 'Ⓜ️'}


def emojify_sources(s: Dict[str, str], rating: Dict[str, str]):
    source, value = rating.get('source'), rating.get('value')
    matches = findall(r"([\d.]+).*", value)
    if len(matches):
        value = matches[0]

    s[RATING_EMOJI.get(source, source)] = value

    return s


class Movie:
    def __init__(self, id=None, title=None):
        assert id or title, "Must have a title or id"
        self.id, self.title = id, title

    @property
    def emoji_ratings(self) -> Dict[str, str]:
        id, title = self.id, None if self.id else self.title

        movie = omdb.get(imdbid=id, title=title)
        if movie:
            ratings = movie.get('ratings')
            e_ratings = reduce(emojify_sources, ratings, {})

            return e_ratings


if __name__ == '__main__':
    print(Movie(title="Ocean's eight").emoji_ratings)
    print(Movie(title="Deadpool 2").emoji_ratings)
    print(Movie(title="L'Insulte").emoji_ratings)
