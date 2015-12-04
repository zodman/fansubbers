from nyaa import nyaa
from guessit import guessit
from utils import trakt_images, search_animenetwork, mal_search

nyaa_users = {
u"PuyaSubs!":239789,
u'Hoshizora':158741
}

def fetch_fansub(nyaa_result):
    anime_info = guessit(nyaa_result.title)
    anime_title = anime_info.get("title")
    anime_season = anime_info.get("season")
    anime_chapter = anime_info.get("episode", anime_info.get("episode_title"))
    fansub = anime_info.get("release_group")
    tvshow = trakt_images(anime_title)
    mal = mal_search(anime_title)
    mal_english_title = mal.get("english_title")
    mal_title = mal.get("title")
    mal_syno = mal.get("synonyms").split(";")
    res = []
    for i in [anime_title, mal_english_title, mal_title] + mal_syno:
        res = search_animenetwork(i)
        print (i,res)
        if res:
            print res
            return res


def main():
    for fansub, user_id in nyaa_users.items():
        result = nyaa.search(user=user_id,offset=2)
        map(fetch_fansub, result)


if __name__ == "__main__":
    main()
