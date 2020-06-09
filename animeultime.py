from bs4 import BeautifulSoup
import requests
import json


def jsonRequest(AnimeID, ListID):
    url = "https://v5.anime-ultime.net/VideoPlayer.html"
    headers = {'Content-Type': 'application/x-www-form-urlencoded', }
    quality = ['1080p', '720p', '480p', '360p', '240p', '144p']
    Dico = []
    key = 0
    old = None
    for i in ListID:
        payload = f"focusFile={i}&idserie={AnimeID}"
        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text.encode('utf8'))

        chosequality = response['quality']

        info = {
            "index": key,
            "title": response['title'],
            "quality": chosequality,
            "methode": [
                {
                    "link": response[chosequality]["mp4"]["url"],
                    "title": "anime-ultime"
                }
            ]
        }

        if response['title'] == old:
            if quality.index(chosequality) < quality.index(Dico[key-1]['quality']):
                Dico[key-1] = info
        else:
            Dico.append(info)
            key += 1
            old = response['title']
    return Dico


def GetIdEpisode(soup):
    embed = soup.find_all("li", {"id": "playlist-link"})
    AnimeID = soup.find("div", {"class": "AUVideoPlayer"})['data-serie']

    url = "https://v5.anime-ultime.net/VideoPlayer.html"
    headers = {'Content-Type': 'application/x-www-form-urlencoded', }
    payload = f"idserie={AnimeID}"
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text.encode('utf8'))

    ListID = [i["id"] for i in response["playlist"]]
    return AnimeID, ListID
