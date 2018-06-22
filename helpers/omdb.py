# apikey=f95aa941
from functools import lru_cache
from typing import Tuple

from omdb import OMDBClient

omdb = OMDBClient(apikey='f95aa941')

IMDb_BASE_URL = "https://www.imdb.com"
IMDb_SEARCH_URL = IMDb_BASE_URL + "/search/title"  # ?title=ocean%27s%20eight&title_type=feature&view=simple"
IMDb_TITLE_URL = IMDb_BASE_URL + "/title/"  # /tt7388562



@lru_cache()
def get_rating_by_id(id) -> str:
    movie = omdb.get(imdbid=id)
    return movie.get('imdb_rating')


@lru_cache()
def get_rating_by_title(title) -> Tuple[str, str]:
    rating, url = 'No rating', ''
    movie = omdb.get(title=title)

    if movie.get('imdb_id'):
        url = IMDb_TITLE_URL + movie.get('imdb_id')
    else:
        rating = 'No IMDb'

    if movie.get('imdb_rating'):
        rating = movie.get('imdb_rating')

    return rating, url


if __name__ == '__main__':
    r = get_rating_by_title("Ocean's Eight")
    print(r)
