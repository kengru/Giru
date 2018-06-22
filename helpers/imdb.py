from functools import lru_cache
from typing import Tuple

from bs4 import BeautifulSoup
from requests import get

IMDb_BASE_URL = "https://www.imdb.com"
IMDb_SEARCH_URL = IMDb_BASE_URL + "/search/title"  # ?title=ocean%27s%20eight&title_type=feature&view=simple"
IMDb_TITLE_URL = IMDb_BASE_URL + "/title/"  # /tt7388562



@lru_cache()
def get_rating_by_id(id) -> str:
    get

    movie = BeautifulSoup(get(IMDb_TITLE_URL + id).content, 'html.parser')
    rating = movie.find('span', attrs=dict(itemprop="ratingValue"))
    if rating:
        return rating.text.strip()

    return 'No rating'


@lru_cache()
def get_rating_by_title(title) -> Tuple[str, str]:
    rating, url = 'No rating', ''

    movie = BeautifulSoup(get(IMDb_SEARCH_URL,
                              params=dict(title=title,
                                          title_type='feature',
                                          view='simple')).content, 'html.parser')
    rating_html = movie.find('div', class_="col-imdb-rating")
    id_html = movie.find('span', class_="lister-item-header")
    if id_html:
        url = IMDb_BASE_URL + id_html.find('a').get('href').strip()
    else:
        rating = 'No IMDb'
    if rating_html:
        rating = rating_html.text.strip()

    return rating, url


if __name__ == '__main__':
    r = get_rating_by_title("Ocean's Eight")
    print(r)
