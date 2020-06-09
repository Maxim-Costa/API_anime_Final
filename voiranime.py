from GetHTML import *
from bs4 import BeautifulSoup
from threading import Thread
import json


def GetSaison(link):
    soup = GetHTML(link)
    title = soup.find_all('div', {"class": "module-title"})
    titleLink = soup.find_all('a', {"title": "Regarder en VOSTFR"})
    return title, titleLink


def GetEpisodeLink(link):
    soup = GetHTML(link)
    embed = soup.find_all('a', {"class": "btn-default"})
    return embed


def GetEpisode(link):
    AnimeList = GetEpisodeLink(link)
    result = []
    threads = []
    start = 0
    end = 100
    continuer = True
    while continuer:
        threads = []
        for key, ep in enumerate(AnimeList[start:end]):
            threads.append(
                Thread(target=GetEpisodeMethode, args=(key, ep, result)))
            threads[key].start()

        for i in range(len(threads)):
            threads[i].join()

        if len(AnimeList) > end-1:
            start = end
            end = start + 100
        else:
            continuer = False
    return result


def GetEpisodeMethodeDICO(link):
    soup = GetHTML(link)
    embed = soup.find_all("script")
    embed = list(map(lambda data: str(data)
                     if "multilinks" in str(data) else None, embed))
    embed = list(filter(None, embed))[0]
    embed = embed.replace('<script type="text/javascript">', '')
    embed = embed.replace('</script>', '')
    embed = embed.replace('var multilinks = ', '')
    embed = embed.split(";")[0]
    Dico = json.loads(embed)[0]
    return Dico


def GetEpisodeMethode(key, ep, result):

    link = "null" if ep['title'].replace(
        " ", "") == ep.text.replace(" ", "") else ep['href']

    if link != "null":
        Dico = GetEpisodeMethodeDICO(link)
        Dico = [{
            "title": i['title'],
            "link": BeautifulSoup(i['url'], "html.parser").find_all('iframe')[0]['src']
        } for i in Dico]
    else:
        Dico = [link]

    result.append(
        {
            "index": key,
            "title": ep['title'],
            "methode": Dico
        }
    )
