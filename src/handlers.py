from typing import Iterable
import tools
import requests


def _get_images_from_imgur_album(url: str) -> Iterable[str]:
    """ Gather a collection images from an imgur image album link.
     e.g. {http://imgur.com/a/Dii3H} """

    headers = {
        "Host": "imgur.com",
        "User-Agent": tools.REQUESTS_HEADER,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        'Referer': url,
        "Connection": "keep-alive"
    }

    imgur_id = tools.remove_ending_slash(url).split("/")[-1]
    url = "http://imgur.com/ajaxalbums/getimages/{0}/hit.json?all=true".format(imgur_id)
    request = requests.get(url, headers=headers, params={"all": "true"}).json()

    if len(request['data']) == 0:
        return []
    # if request['data'] .get('error'):
    #     error = request['data']['error']
    #     if "rate" in error.lower():
    #         print("Rate limited.")
    #     return []

    else:
        images = [tools.question_mark_filename_strip("http://i.imgur.com/{0}{1}".format(image['hash'], image['ext']))
                  for image in request['data']['images']]
        return images


def imgur(url: str) -> Iterable[str]:
    if '/a/' in url:
        return _get_images_from_imgur_album(url)
    else:
        return [tools.question_mark_filename_strip(url)]


def gfycat(url: str) -> Iterable[str]:
    api = 'http://gfycat.com/cajax/get/{0}'.format(tools.get_url_filename(url))
    request = requests.get(api)

    if request.status_code == 200:
        data = request.json()
        if data.get('error') is None:
            link = data['gfyItem']['mp4Url']
            if link is not None:
                return [link]

    return []

