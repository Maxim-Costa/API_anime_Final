from bs4 import BeautifulSoup
from GetHTML import *
from threading import Thread


def GetLinkEpisode(soup):
    ep = soup.find("a", {"class": "active"})

    AnimeID = soup.find("input", {"id": "movie_id"})['value']
    link = f"https://ajax.gogocdn.net/ajax/load-list-episode?ep_start={0}&ep_end={10000}&id={AnimeID}"
    soup = GetHTML(link)
    AnimeList = ["https://www19.gogoanime.io"+i['href'].lstrip()
                 for i in soup.find_all("a")]
    return AnimeID, AnimeList


def GetEpisodeMethodeGOGO(AnimeList):
    Dico = []
    threads = []
    start = 0
    end = 100
    continuer = True
    while continuer:
        threads = []
        for key, link in enumerate(AnimeList[start:end]):
            threads.append(Thread(target=GetEpisodeAsync,
                                  args=(link, key+start, Dico)))
            threads[key].start()
        for i in range(len(threads)):
            threads[i].join()

        if len(AnimeList) > end-1:
            start = end
            end = start + 100
        else:
            continuer = False
    return Dico


def GetEpisodeAsync(link, key, Dico):
    soup = GetHTML(link)
    embed = soup.find("div", {"class": "anime_muti_link"})
    embed = embed.find_all('li')
    title = soup.find("div", {"class": "title_name"}).text.rstrip().lstrip()
    methode = []
    for i in embed:
        link = i.a['data-video']
        if link[:2] == "//":
            link = "http:"+link
        methode.append({
            "link": link,
            "title": i.a.text.replace("Choose this server", "")
        })
    Dico.append({
        "index": key,
        "title": title,
        "methode": methode
    })
