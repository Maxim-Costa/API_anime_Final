from flask import Flask, jsonify, request
from markupsafe import escape
from bs4 import BeautifulSoup

from GetHTML import *

import voiranime
import vostfree
import animeultime
import gogoanime
import dbanimes

import requests
import json

app = Flask(__name__)


@app.route('/api/v1/Anime/episode/voiranime.com/<PGname>', methods=['GET'])
def get_saison_anime_voiranime(PGname):
    link = "https://voiranime.com/"+escape(PGname)+"/"
    result = voiranime.GetEpisode(link)
    result = sorted(result, key=lambda anime: anime['index'])
    return jsonify({"Page_name": PGname, "link": link, "Episode": result})


""" ******************************vostfree******************************************************************* """


@app.route('/api/v1/Anime/episode/vostfree.com/<PGname>', methods=['GET'])
def get_saison_anime_vostfree(PGname):
    link = "https://vostfree.com/"+escape(PGname)+".html"
    soup = GetHTML(link)
    result = vostfree.GetAllPlayer(soup)
    result = sorted(result, key=lambda anime: anime['index'])
    return jsonify({"Page_name": PGname, "Link": link, "Episode": result})


"""*********************************animeultime***************************************************************************************************************************************************************"""


@app.route('/api/v1/Anime/episode/v5.anime-ultime.net/<PGname>', methods=['GET'])
def get_saison_anime_animeultime(PGname):
    link = "https://v5.anime-ultime.net/"+PGname+".html"
    soup = GetHTML(link)
    AnimeID, ListID = animeultime.GetIdEpisode(soup)
    result = animeultime.jsonRequest(AnimeID, ListID)
    result = sorted(result, key=lambda anime: anime['index'])
    return jsonify({"Page_name": PGname, "AnimeID": AnimeID, "Link": link, "Episode": result})


"""**************************************************19.gogoanime.io**************************************************************"""


@app.route('/api/v1/Anime/episode/19.gogoanime.io/<PGname>', methods=['GET'])
def get_saison_anime_gogoanime(PGname):
    link = "https://www19.gogoanime.io/category/"+escape(PGname)
    soup = GetHTML(link)
    AnimeID, AnimeList = gogoanime.GetLinkEpisode(soup)
    result = gogoanime.GetEpisodeMethodeGOGO(AnimeList)
    result = sorted(result, key=lambda anime: anime['index'])
    return jsonify({"Page_name": PGname, "AnimeID": AnimeID, "Link": link, "Episode": result})


"""***************************************dbanimes.com**************************************************************"""


@app.route('/api/v1/Anime/episode/dbanimes.com/<PGname>', methods=['GET'])
def get_saison_anime_dbanimes(PGname):
    link = "https://dbanimes.com/anime/"+escape(PGname)
    soup = GetHTML(link)
    AnimeList = dbanimes.GetEpisodeDB(soup)
    result = dbanimes.GetEpisodeMethodeDB(AnimeList)
    result = sorted(result, key=lambda anime: anime['index'])
    return jsonify({"Page_name": PGname, "Link": link, "Episode": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
