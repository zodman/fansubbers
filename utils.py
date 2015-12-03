#!/usr/bin/env python
# encoding=utf8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import trakt
from webscraping import xpath
import requests
import xmltodict
import urllib2
from urllib import urlencode


my_client_id = "f4c5e2bc17fe61f01900a23eb41cead3e412e51eddc2177dbc8b88625778cc0b"
my_client_secret = "535bb4e0657f512503c0a18b302fe1a132295f56d8454c3f68f693980d0bcfaa"

def start_trakt(user):
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    trakt.init(user,client_id=my_client_id, client_secret=my_client_secret, store =True)


def translate(to_translate, to_langage="auto", langage="auto"):
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
#    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+").replace("\n",""))
    link = "http://translate.google.com/m?"
    params = dict(hl=to_langage,sl=langage,q=to_translate)
    data = urlencode(params)
    request = urllib2.Request(link+data, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

def search_trakt(trackt_slug):
    from trakt.errors import NotFoundException
    from trakt.movies import Movie
    from trakt.tv import TVShow
    print "search"
    try:
        tvshow = TVShow(trackt_slug)
    except NotFoundException:
        tvshow = Movie(trackt_slug)
    return tvshow

def mal_search(mal_title, mal_id=False):
    cookies = {"incap_ses_224_81958":"P6tYbUr7VH9V6shgudAbA1g5FVYAAAAAyt7eDF9npLc6I7roc0UIEQ=="}
    response = requests.get(
        "http://myanimelist.net/api/anime/search.xml",
        params={'q':mal_title},
        cookies=cookies,
        auth=("zodman1","zxczxc"),
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'}
         )
    content = response.content
    if mal_id is not False:
        for e in xpath.search(content,"//entry"):
            if  mal_id in e:
                content = xpath.get(e, "//anime")
                break
    else:
        content = xpath.get(content, "//anime")
    res = xmltodict.parse(content)
    return res.get("entry")

if __name__=="__main__":
    import os
    if not os.path.exists("/home/zodman/.pytrakt.json"):
        start_trakt("zodman")
    title = "Plastic Memories"
    print search_trakt(title)
    mal = mal_search(title)
    print translate(mal.get("synopsis"), "es")


