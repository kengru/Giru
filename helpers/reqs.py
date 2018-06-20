from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from imdb import IMDb
import datetime

def simple_get(url):
    """ Tries to get html/xml and returns the text content, otherwise returns None. """
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """ Returns True if the response is html, False otherwise. """
    content_type = resp.headers['Content-Type'].lower()
    return (content_type is not None and content_type.find('html') > -1)

# url = input('Url: ')
# result = simple_get(url)
# print(len(result))
# message = 'Cartelera al día {0}:\n'.format(datetime.datetime.today().strftime('%d-%m-%Y'))
# html = BeautifulSoup(simple_get('http://www.cinema.com.do/index.php?x=cartelera'), 'html.parser')
# movies = html.find_all('ul', class_='small-block-grid-2')
# for item in movies:
#     for li in item.find_all('li'):
#         ia = IMDb()
#         search = ia.search_movie('matrix')
#         movie = search[0]
#         ia.update(movie, ['vote details'])
#         print(movie)
#         message += '[' + li.strong.text + '](http://www.cinema.com.do/' + li.a.get('href') + ')\n'
# print(message)
        # for a in li.find('a'):
        #     print('http://www.cinema.com.do/' + a['href'])