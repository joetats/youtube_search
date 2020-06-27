import requests
from bs4 import BeautifulSoup
import urllib.parse
import json


class YoutubeSearch:

    def __init__(self, search_terms: str, max_results=None, noEmbedData=False):
        self.search_terms = search_terms
        self.max_results = max_results
        self.noEmbedData = noEmbedData
        self.videos = self.search()

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}&pbj=1"
        response = BeautifulSoup(requests.get(url).text, "html.parser")
        results = self.parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            if self.noEmbedData:
                return self.get_more_data(results[:self.max_results])
            return results[:self.max_results]
        if self.noEmbedData:
            return self.get_more_data(results)
        return results

    def parse_html(self, soup):
        results = []
        for video_div in soup.select("div.yt-lockup-content"):
            video = video_div.select_one(".yt-uix-tile-link")
            if video is not None:
                if video["href"].startswith("/watch?v="):
                    channel = video_div.select_one("a.spf-link")
                    video_info = {
                        "title": video["title"],
                        "link": video["href"],
                        "id": video["href"][video["href"].index("=")+1:],
                        "channel_name": channel.text,
                        "channel_link": channel["href"]
                    }
                    results.append(video_info)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos})

    def get_more_data(self, results):
        for i in range(len(results)):
            try:
                res = requests.get("https://noembed.com/embed?url=http://www.youtube.com" + results[i]['link'])
                results[i]['info'] = json.loads(res.text)
            except:
                results[i]['info'] = dict({})
        return results