from typing import Optional
import json
import asyncio
import aiohttp
from requests.utils import quote
import requests

BASE_URL = "https://youtube.com"

def url_encode(url: str) -> str:
    return quote(url).replace("%20", "+")

class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = url_encode(self.search_terms)
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self._parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def _parse_html(self, response):
        results = []
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        for contents in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                    res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                    res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                    res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                    res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                    res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                    res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                    res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                    results.append(res)

            if results:
                return results
        return results

    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result

class AsyncYoutubeSearch:
    """
    Entry point class for youtube searching
    """
    def __init__(self, search_query: str, max_results: Optional[int]=None):
        """
        Parameters
        ----------
        search_query : str
            The search query
        max_results : Optional[int]
            The maximum result that will be returned
        """
        self.__query=search_query
        self.__max_results=max_results
        self.__videos=""

    async def result(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/results?search_query={url_encode(self.__query)}") as resp:
                response_body=await resp.text()
                while "ytInitialData" not in response_body:
                    response_body = await resp.text()
        results = self._parse_html(response_body)
        if self.__max_results is not None and len(results) > self.__max_results:
            return results[: self.__max_results]
        return results

    def _parse_html(self, response):
        results = []
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        for contents in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                    res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                    res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                    res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                    res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                    res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                    res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                    res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                    results.append(res)

            if results:
                return results
        return results

    def to_dict(self, clear_cache=True):
        result = self.__videos
        if clear_cache:
            self.__videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.__videos})
        if clear_cache:
            self.__videos = ""
        return result
        