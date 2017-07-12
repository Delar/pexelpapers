# Change if website changes
import urllib.request

from bs4 import BeautifulSoup


PEXELS_URL = 'https://www.pexels.com/'
AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

def _get_pages_urls():
    main_page_html = send_get_request(PEXELS_URL)
    main_soup = BeautifulSoup(main_page_html, 'html.parser')
    photo_articles = main_soup('article', 'photo-item')
    return ['https://www.pexels.com/' + photo_article.a['href'] for photo_article in photo_articles]

def get_image_urls():
    pages_urls = _get_pages_urls()
    image_urls = []
    for page_url in pages_urls:
        photo_page_html = send_get_request(page_url)
        page_soup = BeautifulSoup(photo_page_html, 'html.parser')
        button_div = page_soup('div', 'btn-primary')[0]
        image_urls.append(button_div.a['href'])
    return image_urls


def send_get_request(url, file_name=None):
    """Optionally writes response to file if specified.

    :param url: url to send request to
    :param file_name: [opt] file to write response to
    :return: response context
    """
    request = urllib.request.Request(url, headers={'User-Agent': AGENT})
    with urllib.request.urlopen(request) as response:
        response_context = response.read()
    if file_name is None:
        return response_context
    with open(file_name, 'bw+') as f:
        f.write(response_context)
    return response_context