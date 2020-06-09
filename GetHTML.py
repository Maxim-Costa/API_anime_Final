from bs4 import BeautifulSoup
import requests


def GetHTML(link):
    html = requests.request("GET", link, headers={},
                            data={}).text.encode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    return soup
