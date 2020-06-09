from GetHTML import *
from bs4 import BeautifulSoup
from threading import Thread


def GetEpisodeDB(soup):
    embed = soup.find_all("a", {"class": "btn-default"})
    AnimeList = [i['href'] for i in embed]
    return AnimeList


def asyncGet(key, link, Dico):
    soup = GetHTML(link)
    title = soup.find("li", {"class": "breadcrumb-item active"}).text
    methodeDIC = []
    methode = soup.find_all("div", {"class": "player"})
    for i in methode:
        dataURL = i['data-url']
        if dataURL != " " and dataURL != "None" and dataURL != " ":
            linkMethode = BeautifulSoup(
                dataURL, "html.parser").find("iframe")['src']
            if linkMethode[:2] == "//":
                linkMethode = "http:"+linkMethode
        else:
            linkMethode = "link/methode/not_find"
        methodeDIC.append({
            "link": linkMethode,
            "title": linkMethode.split("/")[2]
        })
    Dico.append({
        "index": key,
        "title": title,
        "methode": methodeDIC
    })


def GetEpisodeMethodeDB(AnimeList):
    Dico = []
    threads = []
    start = 0
    end = 100
    continuer = True
    while continuer:
        threads = []
        for key, link in enumerate(AnimeList[start:end]):
            threads.append(
                Thread(target=asyncGet, args=(key+start, link, Dico)))
            threads[key].start()
        for i in range(len(threads)):
            threads[i].join()

        if len(AnimeList) > end-1:
            start = end
            end = start + 100
        else:
            continuer = False

    return Dico
