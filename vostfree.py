from bs4 import BeautifulSoup
from threading import Thread


def asyncGet(k, i, Dico, soup):
    methode = []
    for j in i.find_all("div"):
        linkGet = soup.find("div", {"id": "content_"+j["id"]})
        if linkGet != None:
            linkGet = LinkConstruct(linkGet.text, j['class'][0])
        else:
            linkGet = "404"
        methode.append({
            "title": j.text,
            "link": linkGet
        })
    Dico.append({
        "index": k,
        "title": soup.find("option", {"value": i['id']}).text,
        "methode": methode
    })


def GetAllPlayer(soup):
    embed = soup.find_all("div", {"class": "new_player_bottom"})
    Dico = []
    threads = []
    start = 0
    end = 100
    continuer = True
    while continuer:
        threads = []
        for k, i in enumerate(embed[0].find_all("div", {"class": "button_box"})):
            threads.append(
                Thread(target=asyncGet, args=(k+start, i, Dico, soup)))
            threads[k].start()
        for i in range(len(threads)):
            threads[i].join()

        if len(AnimeList) > end-1:
            start = end
            end = start + 100
        else:
            continuer = False
    return Dico


def LinkConstruct(id, methode):
    if methode == "new_player_myvi":
        return 'https://myvi.ru/player/embed/html/'+id

    elif methode == "new_player_vip":
        return id

    elif methode == "new_player_gtv":
        return "https://iframedream.com/embed/"+id+".html"

    elif methode == "new_player_mp4":
        return "https://www.mp4upload.com/embed-"+id+".html"

    elif methode == "new_player_uqload":
        return "https://uqload.com/embed-"+id+".html"

    elif methode == "new_player_vidfast":
        return "http://vosmanga.tk/watch/"+id

    elif methode == "new_player_verystream":
        return "https://verystream.com/e/"+id

    elif methode == "new_player_rapids":
        return "https://rapidstream.co/embed-"+id+".html"

    elif methode == "new_player_cloudvideo":
        return "https://cloudvideo.tv/embed-"+id+".html"

    elif methode == "new_player_mytv":
        return "https://www.myvi.xyz/embed/"+id

    elif methode == "new_player_uptostream":
        return "https://uptostream.com/iframe/"+id

    elif methode == "new_player_fembed":
        return "https://www.fembed.com/v/"+id+".html"

    elif methode == "new_player_rapidvideo":
        return "https://www.rapidvideo.com/e/"+id

    elif methode == "new_player_tune":
        return "https://tune.pk/player/embed_player.php?vid="+id

    elif methode == "new_player_sibnet":
        return "https://video.sibnet.ru/shell.php?videoid="+id

    elif methode == "new_player_netu":
        return "https://waaw.tv/watch_video.php?v="+id

    elif methode == "new_player_rutube":
        return "https://rutube.ru/play/embed/"+id

    elif methode == "new_player_yandex":
        return id

    elif methode == "new_player_ok":
        return 'https://www.ok.ru/videoembed/'+id

    elif methode == "new_player_vid":
        return id

    elif methode == "new_player_cloudy":
        return id

    elif methode == "new_player_google":
        return 'https://drive.google.com/open?id='+id

    elif methode == "new_player_youtube":
        return id

    elif methode == "new_player_moevideo":
        return id

    elif methode == "new_player_mail":
        return "https://videoapi.my.mail.ru/videos/embed/mail/"+id

    elif methode == "new_player_mail2":
        return "https://my.mail.ru/video/embed/"+id

    elif methode == "new_player_vk2":
        return id

    elif methode == "new_player_dailymotion":
        return "https://dailymotion.com/embed/video/"+id

    elif methode == "new_player_openload":
        return "https://openload.co/embed/"+id

    elif methode == "new_player_kaztube":
        return "https://kaztube.kz/video/embed/"+id

    else:
        return id
