from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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
    return (resp.status.code == 200 and content_type is not None and content_type.find('html') > -1)

url = input('Url: ')
result = simple_get(url)
print(len(result))
