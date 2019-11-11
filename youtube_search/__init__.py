import requests
from bs4 import BeautifulSoup
import urllib.parse


class YoutubeSearch:

    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = 'https://youtube.com'
        url = f'{BASE_URL}/results?search_query={encoded_search}&pbj=1'
        results = self.parse_html(BeautifulSoup(requests.get(url).text))
        if self.max_results is not None and len(results) > self.max_results:
            self.videos = results[:self.max_results]
        else:
            self.videos = results

    def parse_html(self, soup):
        results = []
        for video in soup.select('.yt-uix-tile-link'):
            if '=' in video['href']:
                video_info = {
                    'title': video['title'],
                    'link': video['href'],
                    'id': video['href'][video['href'].index('=')+1:]
                }
                results.append(video_info)
        return results

    def to_dict(self):
        self.search()
        return self.videos

    def to_json(self):
        self.search()
        return self.videos
