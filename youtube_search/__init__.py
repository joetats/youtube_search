import requests
import urllib.parse
import json


class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results

        self.videos = self.search_videos()
        self.channels = self.search_channels()

    def search_videos(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}&lang=en"
        response = requests.get(url).text
        while 'window["ytInitialData"]' not in response:
            response = requests.get(url).text
        results = self.parse_html_videos(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def search_channels(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while 'window["ytInitialData"]' not in response:
            response = requests.get(url).text
        results = self.parse_html_channels(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def parse_html_channels(self, response):
        results = []
        start = (
            response.index('window["ytInitialData"]')
            + len('window["ytInitialData"]')
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        datalist = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for channel in datalist:
            res = {}
            try:
                if "channelRenderer" in channel.keys():
                    channel_data = channel.get("channelRenderer", {})
                    res["id"] = channel_data.get("channelId", None)
                    res["name"] = channel_data.get("title", None).get("simpleText", None)
                    try:
                        res["suscriberCountText"] = channel_data.get("subscriberCountText", None).get("simpleText", None).split(" ")[0]
                    except:
                        res["suscriberCountText"] = "0"
                    res["thumbnails"] = [thumb.get("url", None) for thumb in channel_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                    res["url_suffix"] = channel_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                    results.append(res)

                if "shelfRenderer" in channel.keys():
                    print("Has latest content")
            except:
                return results
        return results

    def parse_html_videos(self, response):
        results = []
        start = (
            response.index('window["ytInitialData"]')
            + len('window["ytInitialData"]')
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0).split(" ")[0]
                res['publishedText'] = video_data.get("publishedTimeText", None).get("simpleText")
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results

    def videos_to_dict(self):
        return self.videos

    def channels_to_dict(self):
        return self.channels

    def videos_to_json(self):
        return json.dumps({"videos": self.videos})

    def channels_to_json(self):
        return json.dumps({"channels": self.channels})
