import requests
from bs4 import BeautifulSoup
import urllib.parse

class YoutubeSearch:

    def __init__(self, search_terms):
        self.search_terms = search_terms

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        url = f'https://youtube.com/results?search_query={encoded_search}&pbj=1'
        res = requests.get(url)
        soup = BeautifulSoup(res.text)

        self.videos = [(video['title'], video['href']) for video in soup.select('.yt-uix-tile-link')]

    def json(self):
        self.search()
        return self.videos