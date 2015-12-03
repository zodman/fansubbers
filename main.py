from nyaa import nyaa
from guessit import guessit
import pprint

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
    print anime_info
    if anime_season:
        print "[{}] {} - s{}x{}".format(fansub,anime_title, anime_season, anime_chapter)
    else:
        print "[{}] {} - {}".format(fansub,anime_title,  anime_chapter)


def main():
    for fansub, user_id in nyaa_users.items():
        result = nyaa.search(user=user_id,offset=2)
        map(fetch_fansub, result)


if __name__ == "__main__":
    main()
